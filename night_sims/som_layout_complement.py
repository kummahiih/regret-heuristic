#!/usr/bin/env python3
"""Complementary layout diagnostic.

Two controls the first run did not run:
- Ask-removal: drop the user question and re-score topic purity.
- Wider role bank: more persona prompts with a shared task.

Not a camera. Not a claim that SOM nodes are rooms. Do not fill D.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


TOPICS = (
    "hiking", "invoices", "repairs", "cooking",
    "taxes", "pets", "travel", "neighbors",
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
ROLES = (
    "software engineer", "sci-fi writer", "accountant",
    "travel agent", "neighbor", "chef",
    "doctor", "lawyer", "teacher", "journalist",
    "architect", "librarian",
)
TASKS = (
    "What is your role?",
    "Describe your typical day.",
    "What tools do you use?",
)


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


def last_h(model, tok, text, layer, device, max_length=128):
    ids = tok(text, return_tensors="pt", truncation=True, max_length=max_length)
    ids = {k: v.to(device) for k, v in ids.items()}
    with torch.no_grad():
        out = model(**ids, output_hidden_states=True)
    return out.hidden_states[layer][0, -1].float().cpu()


def topic_prompts(with_ask: bool):
    rows = []
    for t in TOPICS:
        fact = FACTS[t]
        for strat in ("honest", "deceptive"):
            note = fact if strat == "honest" else f"do not mention {fact}"
            ask = f"\nUser: What should I tell them about {t}?" if with_ask else ""
            rows.append({
                "text": f"Note: {note}{ask}",
                "topic": t,
                "strategy": strat,
            })
    return rows


def role_prompts():
    rows = []
    for role in ROLES:
        for task in TASKS:
            rows.append({
                "text": f"You are a {role}. {task}",
                "role": role,
            })
    return rows


class MiniSOM:
    def __init__(self, m, n, dim, sigma=1.5, lr=0.3, steps=30, seed=0):
        g = torch.Generator().manual_seed(seed)
        self.m, self.n = m, n
        self.weights = torch.randn(m, n, dim, generator=g)
        self.sigma, self.lr, self.steps = sigma, lr, steps

    def winners(self, X):
        d = ((X.unsqueeze(1).unsqueeze(1) - self.weights.unsqueeze(0)) ** 2).sum(-1)
        return d.view(X.shape[0], -1).argmin(dim=1)

    def train(self, X):
        coords = torch.stack(
            torch.meshgrid(torch.arange(self.m), torch.arange(self.n), indexing="ij"),
            dim=-1,
        ).float()
        for _ in range(self.steps):
            for x in X:
                dist2 = ((self.weights - x) ** 2).sum(-1)
                i, j = divmod(int(dist2.argmin()), self.n)
                delta = coords - torch.tensor([i, j], dtype=torch.float)
                dist = delta.norm(dim=-1)
                neigh = (dist < self.sigma).float()
                self.weights += (
                    self.lr * neigh.unsqueeze(-1) * (x - self.weights)
                    * (1 - dist.unsqueeze(-1) / self.sigma).clamp(min=0)
                )


def purity(assign, labels):
    n = len(labels)
    pure = 0
    for k in set(assign.tolist()):
        labs = [labels[i] for i in range(n) if assign[i] == k]
        if labs:
            pure += Counter(labs).most_common(1)[0][1]
    return pure / max(n, 1)


def run_purity(X, labels, name, grid, steps, seeds):
    vals = []
    for s in range(seeds):
        som = MiniSOM(grid, grid, X.shape[1], steps=steps, seed=s)
        som.train(X)
        assign = som.winners(X)
        p = purity(assign, labels)
        vals.append(p)
        print(f"  {name} seed={s} purity={p:.3f} n={len(labels)}")
    print(f"  {name} mean={sum(vals)/len(vals):.3f}")
    return sum(vals) / len(vals)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--layer", type=int, default=8)
    p.add_argument("--grid", type=int, default=4)
    p.add_argument("--steps", type=int, default=30)
    p.add_argument("--seeds", type=int, default=3)
    p.add_argument("--dump", default="")
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    print("som complement: ask-removal and wider roles. Not a camera. Do not fill D.")
    print(f"model={args.model} layer={args.layer}")
    tok, model = load_model(args.model)
    device = model.device

    # ask-removal
    with_ask = topic_prompts(True)
    no_ask = topic_prompts(False)
    print(f"topic prompts with_ask={len(with_ask)} no_ask={len(no_ask)}")
    Hw = torch.stack([last_h(model, tok, r["text"], args.layer, device) for r in with_ask])
    Hn = torch.stack([last_h(model, tok, r["text"], args.layer, device) for r in no_ask])
    labels = [r["topic"] for r in with_ask]
    print("topic purity with ask:")
    pw = run_purity(Hw, labels, "with_ask", args.grid, args.steps, args.seeds)
    print("topic purity ask removed:")
    pn = run_purity(Hn, labels, "no_ask", args.grid, args.steps, args.seeds)

    # wider roles
    roles = role_prompts()
    print(f"role prompts={len(roles)} roles={len(ROLES)} tasks={len(TASKS)}")
    Hr = torch.stack([last_h(model, tok, r["text"], args.layer, device) for r in roles])
    role_labels = [r["role"] for r in roles]
    print("role purity on wider bank:")
    pr = run_purity(Hr, role_labels, "role", args.grid, args.steps, args.seeds)

    if args.dump:
        Path(args.dump).parent.mkdir(parents=True, exist_ok=True)
        Path(args.dump).write_text(json.dumps({
            "model": args.model, "layer": args.layer,
            "topic_with_ask": pw, "topic_no_ask": pn, "role": pr,
        }) + "\n")
        print(f"dump={args.dump}")
    print("Not a camera. Not a claim that SOM nodes are rooms. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
