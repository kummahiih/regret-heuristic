#!/usr/bin/env python3
"""Home 4070 Ti 12GB probe: 4-bit load + N linear r heads + frozen D + four eval metrics.
--pool last (default) or mean over last-layer tokens (pad masked).
D and eval use the same pool. Not a strategy readout.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def tokenize(tokenizer, text, max_length, device):
    toks = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        padding=False,
    )
    return {k: v.to(device) for k, v in toks.items()}


def pool_hidden(hidden_last, attn, pool):
    # hidden_last: (1, T, H), attn: (1, T)
    if pool == "last":
        return hidden_last[0, -1, :].float()
    mask = attn[0].float().unsqueeze(-1)
    return (hidden_last[0].float() * mask).sum(dim=0) / mask.sum().clamp_min(1.0)


def encode(model, tokenizer, text, max_length, device, pool):
    toks = tokenize(tokenizer, text, max_length, device)
    out = model(**toks, output_hidden_states=True)
    return pool_hidden(out.hidden_states[-1], toks["attention_mask"], pool)


def walk_stats(model, tokenizer, text, max_length, device, want_entropy, pool):
    toks = tokenize(tokenizer, text, max_length, device)
    out = model(**toks, labels=toks["input_ids"], output_hidden_states=True)
    h = pool_hidden(out.hidden_states[-1], toks["attention_mask"], pool).cpu()
    nll = float(out.loss.detach().float().cpu())
    ent = float("nan")
    if want_entropy:
        logits = out.logits[0, -1, :].float()
        logp = F.log_softmax(logits, dim=-1)
        ent = float((-(logp.exp() * logp).sum()).cpu())
    return h, nll, ent


def max_cosine(vec, bank):
    v = F.normalize(vec.unsqueeze(0), dim=-1)
    b = F.normalize(bank, dim=-1)
    return float((v @ b.T).max().clamp(-1, 1).cpu())


def hinge(vec, bank, tau):
    return max(max_cosine(vec, bank) - tau, 0.0)


def mean_or_nan(xs):
    xs = [x for x in xs if x == x]
    if not xs:
        return float("nan")
    return sum(xs) / len(xs)


def main():
    parser = argparse.ArgumentParser(
        description="4-bit instruct load + N linear r heads + frozen D + four metrics"
    )
    parser.add_argument("--model", default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--data", default="data/probe_split.jsonl")
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--tau", type=float, default=0.0)
    parser.add_argument("--update-steps", type=int, default=0)
    parser.add_argument("--heads", type=int, default=8)
    parser.add_argument("--fork", action="store_true")
    parser.add_argument("--lambda0", type=float, default=2.0)
    parser.add_argument("--entropy", action="store_true")
    parser.add_argument(
        "--pool",
        choices=("last", "mean"),
        default="last",
        help="Walk observation: last token or mean of last-layer tokens. D uses the same pool.",
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
    if not bank_deceptive or not eval_rows:
        print("ERROR: need bank deceptive and eval rows", file=sys.stderr)
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
        print("ERROR: OOM loading model in 4-bit.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: model load failed: {e}", file=sys.stderr)
        sys.exit(1)

    device = model.device
    print(
        f"VRAM allocated_GiB={torch.cuda.memory_allocated() / 1024**3:.2f} "
        f"reserved_GiB={torch.cuda.memory_reserved() / 1024**3:.2f}"
    )
    print(f"pool={args.pool} (D and eval use this observation)")

    hidden_dim = model.config.hidden_size
    D_list = []
    with torch.no_grad():
        for row in bank_deceptive:
            h = encode(model, tokenizer, row["text"], args.max_length, device, args.pool)
            D_list.append(h.detach().cpu())
    D = torch.stack(D_list)
    print(f"Frozen D shape={tuple(D.shape)} from {len(bank_deceptive)} bank deceptive")

    N = args.heads
    heads = []
    parents = [-1] * N
    for _ in range(N):
        p = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
        with torch.no_grad():
            p.weight.copy_(torch.eye(hidden_dim))
        heads.append(p)
    print(f"N={N} linear r heads loaded (init I, CPU); parents={parents}")
    print("u(x)=walk NLL; --entropy is last-token entropy. Not p(lie). No tau(x) bin.")

    if args.update_steps > 0:
        if not train_rows:
            print("ERROR: --update-steps>0 but no train split", file=sys.stderr)
            sys.exit(1)
        if args.fork and N > 1:
            parents[1] = 0
            with torch.no_grad():
                heads[1].weight.data.copy_(heads[0].weight.data)
            print(f"fork: parents={parents}")

    children = [[] for _ in range(N)]
    for i, p in enumerate(parents):
        if p >= 0:
            children[p].append(i)

    def subtree_W(n):
        return 1 + sum(subtree_W(c) for c in children[n])

    Ws = [subtree_W(i) for i in range(N)]
    k = max(2, int(0.05 * N))
    roots = [i for i in range(N) if Ws[i] >= k and all(Ws[c] < k for c in children[i])]
    cluster_id = [-1] * N

    def assign_cluster(n, cid):
        cluster_id[n] = cid
        for c in children[n]:
            assign_cluster(c, cid)

    for r in roots:
        assign_cluster(r, r)
    for i in range(N):
        if cluster_id[i] < 0:
            cluster_id[i] = i
    print(f"cluster_id={cluster_id} k={k} roots={roots} Ws={Ws}")

    if args.update_steps > 0:
        C0 = cluster_id[0]
        scores = [args.lambda0 if cluster_id[i] == C0 else 1.0 for i in range(N)]
        chosen = max(range(N), key=lambda i: (scores[i], -i))
        print(f"who_stepped={chosen} (CDS C0={C0} lambda0={args.lambda0} scores={scores})")
        opt = torch.optim.SGD(heads[chosen].parameters(), lr=1e-2)
        for step in range(args.update_steps):
            opt.zero_grad()
            losses = []
            for row in train_rows:
                with torch.no_grad():
                    h = encode(
                        model, tokenizer, row["text"], args.max_length, device, args.pool
                    ).cpu()
                z = heads[chosen](h)
                if row.get("label") == "deceptive":
                    s = (F.normalize(z.unsqueeze(0), dim=-1) @ F.normalize(D, dim=-1).T).max()
                    losses.append(torch.relu(s - args.tau))
            if not losses:
                print("ERROR: no deceptive train rows for update", file=sys.stderr)
                sys.exit(1)
            loss = torch.stack(losses).mean()
            loss.backward()
            opt.step()
            print(f"update_step={step + 1} head={chosen} hinge_train={float(loss.detach().cpu()):.4f}")
        print("Note: hinge drop after update is not reduced deception.")

    eval_feats = []
    with torch.no_grad():
        for row in eval_rows:
            h, nll, ent = walk_stats(
                model, tokenizer, row["text"], args.max_length, device, args.entropy, args.pool
            )
            eval_feats.append((h, nll, ent, row.get("label")))

    cluster_metrics = defaultdict(
        lambda: {
            "hinges_dec": [],
            "hinges_hon": [],
            "nlls": [],
            "nlls_dec": [],
            "nlls_hon": [],
            "ents_dec": [],
            "ents_hon": [],
            "cos_dec": [],
            "cos_hon": [],
        }
    )
    with torch.no_grad():
        for i in range(N):
            probe = heads[i]
            cid = cluster_id[i]
            for h, nll, ent, label in eval_feats:
                z = probe(h)
                cluster_metrics[cid]["nlls"].append(nll)
                if label == "deceptive":
                    cluster_metrics[cid]["hinges_dec"].append(hinge(z, D, args.tau))
                    cluster_metrics[cid]["cos_dec"].append(max_cosine(z, D))
                    cluster_metrics[cid]["nlls_dec"].append(nll)
                    cluster_metrics[cid]["ents_dec"].append(ent)
                elif label == "honest":
                    cluster_metrics[cid]["hinges_hon"].append(hinge(z, D, args.tau))
                    cluster_metrics[cid]["cos_hon"].append(max_cosine(z, D))
                    cluster_metrics[cid]["nlls_hon"].append(nll)
                    cluster_metrics[cid]["ents_hon"].append(ent)

    for cid in sorted(cluster_metrics.keys()):
        m = cluster_metrics[cid]
        line = (
            f"cluster_id={cid} pool={args.pool} "
            f"hinge_near_D_deceptive={mean_or_nan(m['hinges_dec']):.4f} n={len(m['hinges_dec'])} "
            f"hinge_near_D_honest={mean_or_nan(m['hinges_hon']):.4f} n={len(m['hinges_hon'])} "
            f"task_loss={mean_or_nan(m['nlls']):.4f} n={len(m['nlls'])} "
            f"nll_deceptive={mean_or_nan(m['nlls_dec']):.4f} n={len(m['nlls_dec'])} "
            f"nll_honest={mean_or_nan(m['nlls_hon']):.4f} n={len(m['nlls_hon'])} "
            f"probe_vs_D_cosine_deceptive={mean_or_nan(m['cos_dec']):.4f} n={len(m['cos_dec'])} "
            f"probe_vs_D_cosine_honest={mean_or_nan(m['cos_hon']):.4f} n={len(m['cos_hon'])}"
        )
        if args.entropy:
            line += (
                f" entropy_deceptive={mean_or_nan(m['ents_dec']):.4f} n={len(m['ents_dec'])} "
                f"entropy_honest={mean_or_nan(m['ents_hon']):.4f} n={len(m['ents_hon'])}"
            )
        print(line)
    print("u(x) is observation uncertainty, not intent.")
    print("clusters did not invent a strategy readout.")
    print("Four metrics per cluster. Not an alignment result.")


if __name__ == "__main__":
    main()
