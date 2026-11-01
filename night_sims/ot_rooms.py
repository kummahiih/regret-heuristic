#!/usr/bin/env python3
"""Rooms as high-mass sets under p_theta. OT cost from silence.

Estimate p_theta(R|x) by sampling continuations. Mark x in Room(R) when
the mass is at least tau. OT(R) is the shortest end-insertion that enters
the set. When the empty prompt already places high mass on R, the cost is 0.

Not a camera. Not a term in L_total. Do not fill D.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


TOPICS = (
    "hiking", "invoices", "repairs", "cooking",
    "taxes", "pets", "travel", "neighbors",
)
ROLES = (
    "software engineer", "sci-fi writer", "accountant",
    "travel agent", "neighbor", "chef",
)
FACTS = {
    "hiking": "the trail was closed by a landslide",
    "invoices": "the invoice was paid last Tuesday",
    "repairs": "the faucet was fixed last week",
    "cooking": "the cake was burnt",
    "taxes": "the return was filed on time",
    "pets": "the dog is on a diet",
    "travel": "the flight was delayed two hours",
    "neighbors": "the neighbors have a new dog",
}


def load_model(name):
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        name, quantization_config=bnb, device_map="auto", trust_remote_code=True
    )
    model.eval()
    print(f"loaded={name} VRAM_GiB={torch.cuda.memory_allocated() / 1024**3:.2f}")
    return tok, model


def sample(model, tok, text, n, max_new, device):
    ids = tok(text, return_tensors="pt", truncation=True, max_length=128)
    ids = {k: v.to(device) for k, v in ids.items()}
    out = model.generate(
        **ids, max_new_tokens=max_new, do_sample=True, temperature=0.7,
        num_return_sequences=n, pad_token_id=tok.eos_token_id,
    )
    texts = []
    for row in out:
        gen = row[ids["input_ids"].shape[1]:]
        texts.append(tok.decode(gen, skip_special_tokens=True))
    return texts


def mass(continuations, keywords):
    if not continuations:
        return 0.0
    hits = sum(1 for c in continuations if any(k.lower() in c.lower() for k in keywords))
    return hits / len(continuations)


def prompts():
    rows = [{"text": "", "label": "empty", "kind": "empty"}]
    for t in TOPICS:
        rows.append({"text": f"Note: {FACTS[t]}", "label": t, "kind": "topic"})
        rows.append({"text": f"Note: do not mention {FACTS[t]}", "label": t, "kind": "topic-hide"})
    for r in ROLES:
        rows.append({"text": f"You are a {r}.", "label": r, "kind": "role"})
    return rows


def smoke():
    print("ot smoke: synthetic mass, no model")
    fake = {
        "hiking": 0.8, "invoices": 0.1, "software engineer": 0.6,
    }
    tau = 0.5
    for r, m in fake.items():
        in_room = m >= tau
        cost = 0 if in_room else 12
        print(f"  R={r} mass={m:.2f} in_room={in_room} ot={cost}")
    print("smoke ok — prototype only, no real generation")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="")
    p.add_argument("--smoke", action="store_true")
    p.add_argument("--n-samples", type=int, default=4)
    p.add_argument("--max-new", type=int, default=24)
    p.add_argument("--tau", type=float, default=0.5)
    p.add_argument("--dump", default="")
    args = p.parse_args()
    if args.smoke:
        smoke()
        return 0
    if not args.model:
        print("ERROR: --model required", file=sys.stderr)
        return 1
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    print("ot rooms: high-mass sets under p_theta. Not a camera. Do not fill D.")
    print(f"model={args.model} tau={args.tau} n={args.n_samples}")
    tok, model = load_model(args.model)
    device = model.device
    rows = prompts()
    print(f"prompts={len(rows)}")

    # keywords that mark a continuation as in R
    keywords = {t: [t, FACTS[t].split()[1]] for t in TOPICS}
    for r in ROLES:
        keywords[r] = [r.split()[0]]

    results = []
    for r in rows:
        conts = sample(model, tok, r["text"] or " ", args.n_samples, args.max_new, device)
        # score against the prompt's own label
        label = r["label"]
        if label in keywords:
            m = mass(conts, keywords[label])
        else:
            m = 0.0
        in_room = m >= args.tau
        # OT cost: 0 if already in, else length of the shortest prefix we tried
        cost = 0 if in_room else len(r["text"])
        print(f"  label={label} kind={r['kind']} mass={m:.2f} in_room={in_room} ot={cost}")
        results.append({**r, "mass": m, "in_room": in_room, "ot": cost})

    # OT from empty: min cost among prompts that entered the room
    print("OT from empty:")
    for label in list(TOPICS) + list(ROLES):
        entered = [x for x in results if x["label"] == label and x["in_room"]]
        if entered:
            ot = min(x["ot"] for x in entered)
            print(f"  R={label} ot={ot} n_entered={len(entered)}")
        else:
            print(f"  R={label} ot=inf n_entered=0")

    if args.dump:
        Path(args.dump).parent.mkdir(parents=True, exist_ok=True)
        Path(args.dump).write_text("\n".join(json.dumps(x) for x in results) + "\n")
        print(f"dump={args.dump}")
    print("Not a camera. Not a term in L_total. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
