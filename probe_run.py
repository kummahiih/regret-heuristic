#!/usr/bin/env python3
"""Home 4070 Ti 12GB probe: 4-bit load + N linear r heads + frozen D + four eval metrics.
User runs this on the 4070 Ti. Fails clearly on OOM. No weights committed.
A drop in hinge is not reduced deception.
Genealogy: each head has parent id; SGD can fork (copy parent weights to child) or step in place.
No PF/Alias resample.
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def last_hidden(model, tokenizer, text, max_length, device):
    toks = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        padding=False,
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, output_hidden_states=True)
    return out.hidden_states[-1][0, -1, :].float()


def token_nll(model, tokenizer, text, max_length, device):
    toks = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        padding=False,
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, labels=toks["input_ids"])
    return float(out.loss.detach().float().cpu())


def max_cosine(vec, bank):
    # vec [H], bank [N, H], both float
    v = F.normalize(vec.unsqueeze(0), dim=-1)
    b = F.normalize(bank, dim=-1)
    return float((v @ b.T).max().clamp(-1, 1).cpu())


def hinge(vec, bank, tau):
    return max(max_cosine(vec, bank) - tau, 0.0)


def mean_or_nan(xs):
    if not xs:
        return float("nan")
    return sum(xs) / len(xs)


def main():
    parser = argparse.ArgumentParser(
        description="4-bit instruct load + N linear r heads + frozen D + four metrics"
    )
    parser.add_argument(
        "--model",
        default="meta-llama/Llama-3.1-8B-Instruct",
        help="Named instruct checkpoint (HF id)",
    )
    parser.add_argument(
        "--data",
        default="data/probe_split.jsonl",
        help="JSONL with text,label,split fields",
    )
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--tau", type=float, default=0.0)
    parser.add_argument(
        "--update-steps",
        type=int,
        default=0,
        help="Optional SGD steps on linear r only (train split). 0 = no update.",
    )
    parser.add_argument(
        "--heads",
        type=int,
        default=8,
        help="Number of linear r heads (N). Default 8.",
    )
    parser.add_argument(
        "--fork",
        action="store_true",
        help="If set with --update-steps>0 and N>1: fork head 0 into head 1 then step child; else step in place on 0.",
    )
    args = parser.parse_args()

    if args.heads < 1:
        print("ERROR: --heads must be >= 1", file=sys.stderr)
        sys.exit(1)

    if not torch.cuda.is_available():
        print("ERROR: CUDA required for 4-bit load on 4070 Ti", file=sys.stderr)
        sys.exit(1)

    data_path = Path(args.data)
    if not data_path.is_file():
        print(f"ERROR: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    rows = []
    with data_path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    bank_deceptive = [
        row for row in rows if row.get("split") == "bank" and row.get("label") == "deceptive"
    ]
    train_rows = [row for row in rows if row.get("split") == "train"]
    eval_rows = [row for row in rows if row.get("split") == "eval"]
    if not bank_deceptive:
        print("ERROR: no bank split deceptive examples for frozen D", file=sys.stderr)
        sys.exit(1)
    if not eval_rows:
        print("ERROR: no eval split rows", file=sys.stderr)
        sys.exit(1)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )

    try:
        tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
        model.eval()
    except torch.cuda.OutOfMemoryError:
        print(
            "ERROR: OOM loading model in 4-bit. 12GB 4070 Ti constraint; do not retry lower.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: model load failed: {e}", file=sys.stderr)
        sys.exit(1)

    device = model.device
    allocated = torch.cuda.memory_allocated() / (1024 ** 3)
    reserved = torch.cuda.memory_reserved() / (1024 ** 3)
    print(f"VRAM allocated_GiB={allocated:.2f} reserved_GiB={reserved:.2f}")

    hidden_dim = model.config.hidden_size
    D_list = []
    with torch.no_grad():
        for row in bank_deceptive:
            h = last_hidden(model, tokenizer, row["text"], args.max_length, device)
            D_list.append(h.detach().cpu())
    D = torch.stack(D_list)
    print(f"Frozen D shape={tuple(D.shape)} from {len(bank_deceptive)} bank deceptive")

    # N linear r heads with parent pointers (genealogy)
    N = args.heads
    heads = []
    parents = [-1] * N  # parent id; root = -1
    for i in range(N):
        p = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
        with torch.no_grad():
            p.weight.copy_(torch.eye(hidden_dim))
        heads.append(p)
    print(f"N={N} linear r heads loaded (init I); parents={parents}")
    print(f"Shared frozen D and 4-bit model. No resample API.")

    if args.update_steps > 0:
        if not train_rows:
            print("ERROR: --update-steps>0 but no train split", file=sys.stderr)
            sys.exit(1)
        # One SGD step: either fork (copy parent weights into chosen child) or step in place.
        chosen = 0
        if args.fork and N > 1:
            # Fork: copy parent (0) weights into child (1), set parent pointer, step the child
            parents[1] = 0
            with torch.no_grad():
                heads[1].weight.data.copy_(heads[0].weight.data)
            chosen = 1
            print(f"fork: parents={parents}; stepping child={chosen}")
        else:
            print(f"step in place on head={chosen}; parents={parents}")
        opt = torch.optim.SGD(heads[chosen].parameters(), lr=1e-2)
        D_dev = D.to(device)
        for step in range(args.update_steps):
            opt.zero_grad()
            losses = []
            for row in train_rows:
                with torch.no_grad():
                    h = last_hidden(model, tokenizer, row["text"], args.max_length, device)
                z = heads[chosen](h)
                if row.get("label") == "deceptive":
                    v = F.normalize(z.unsqueeze(0), dim=-1)
                    b = F.normalize(D_dev, dim=-1)
                    s = (v @ b.T).max()
                    losses.append(torch.relu(s - args.tau))
            if not losses:
                print("ERROR: no deceptive train rows for update", file=sys.stderr)
                sys.exit(1)
            loss = torch.stack(losses).mean()
            loss.backward()
            opt.step()
            print(f"update_step={step + 1} head={chosen} hinge_train={float(loss.detach().cpu()):.4f}")
        print("Note: hinge drop after update is not reduced deception.")

    # Eval on head 0 by default (metrics for later clustering)
    probe = heads[0]
    eval_dec = [row for row in eval_rows if row.get("label") == "deceptive"]
    eval_hon = [row for row in eval_rows if row.get("label") == "honest"]

    hinges_dec, hinges_hon, nlls = [], [], []
    cos_dec, cos_hon = [], []
    with torch.no_grad():
        for row in eval_rows:
            h = last_hidden(model, tokenizer, row["text"], args.max_length, device).cpu()
            z = probe(h)
            nlls.append(token_nll(model, tokenizer, row["text"], args.max_length, device))
            if row.get("label") == "deceptive":
                hinges_dec.append(hinge(z, D, args.tau))
                cos_dec.append(max_cosine(z, D))
            elif row.get("label") == "honest":
                hinges_hon.append(hinge(z, D, args.tau))
                cos_hon.append(max_cosine(z, D))

    print(f"hinge_near_D_deceptive={mean_or_nan(hinges_dec):.4f} n={len(hinges_dec)}")
    print(f"hinge_same_topic_honest={mean_or_nan(hinges_hon):.4f} n={len(hinges_hon)}")
    print(f"task_loss={mean_or_nan(nlls):.4f} n={len(nlls)}")
    print(f"probe_vs_D_cosine_deceptive={mean_or_nan(cos_dec):.4f} n={len(cos_dec)}")
    print(f"probe_vs_D_cosine_honest={mean_or_nan(cos_hon):.4f} n={len(cos_hon)}")
    print("Four metrics printed. Not an alignment result.")


if __name__ == "__main__":
    main()
