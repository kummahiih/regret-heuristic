#!/usr/bin/env python3
"""Home 4070 Ti 12GB probe: 4-bit 8B load + linear probe + frozen D from bank.
User runs this on the 4070 Ti. Fails clearly on OOM. No weights committed.
"""

import argparse
import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def main():
    parser = argparse.ArgumentParser(
        description="4-bit 8B instruct load + last-token hidden + linear r + frozen D (bank only)"
    )
    parser.add_argument(
        "--model",
        default="meta-llama/Llama-3.1-8B-Instruct",
        help="Named 8B instruct checkpoint (HF id)",
    )
    parser.add_argument(
        "--data",
        default="data/probe_split.jsonl",
        help="JSONL with text,label,split fields",
    )
    parser.add_argument("--max-length", type=int, default=512)
    args = parser.parse_args()

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
        r for r in rows if r.get("split") == "bank" and r.get("label") == "deceptive"
    ]
    if not bank_deceptive:
        print("ERROR: no bank split deceptive examples for frozen D", file=sys.stderr)
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

    allocated = torch.cuda.memory_allocated() / (1024 ** 3)
    reserved = torch.cuda.memory_reserved() / (1024 ** 3)
    print(f"VRAM allocated_GiB={allocated:.2f} reserved_GiB={reserved:.2f}")

    hidden_dim = model.config.hidden_size
    D_list = []
    with torch.no_grad():
        for r in bank_deceptive:
            toks = tokenizer(
                r["text"],
                return_tensors="pt",
                truncation=True,
                max_length=args.max_length,
                padding=False,
            )
            toks = {k: v.to(model.device) for k, v in toks.items()}
            out = model(**toks, output_hidden_states=True)
            # last-token hidden of last layer
            h = out.hidden_states[-1][0, -1, :].detach().float().cpu()
            D_list.append(h)

    D = torch.stack(D_list)  # [n_bank, hidden_dim]
    print(f"Frozen D shape={tuple(D.shape)} from {len(bank_deceptive)} bank deceptive")

    # Linear probe r (random init; metrics path is t5)
    r = torch.nn.Linear(hidden_dim, 1)
    print(f"Linear probe r: in_features={hidden_dim} out_features=1")
    print("Load + last-token hidden + linear r + frozen D ready.")


if __name__ == "__main__":
    main()
