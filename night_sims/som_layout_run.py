#!/usr/bin/env python3
"""Expected vs measured room layout.

Collect last-token residuals on a prompt set that covers candidate rooms
(topics and roles). Train a 2-D SOM. Score purity / NMI / ARI of each
candidate label against unit assignments, with a topic-shuffle null and
a topic-mean-subtracted control.

Not a term in L_total. Not a replacement for the hinge. Not a claim that
SOM nodes are the model's rooms. Does not fill D.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import torch
import torch.nn.functional as F
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


def last_h(model, tok, text, layer, device, max_length=128):
    ids = tok(text, return_tensors="pt", truncation=True, max_length=max_length)
    ids = {k: v.to(device) for k, v in ids.items()}
    with torch.no_grad():
        out = model(**ids, output_hidden_states=True)
    h = out.hidden_states[layer][0, -1].float().cpu()
    return h


def prompts():
    rows = []
    for t in TOPICS:
        fact = FACTS[t]
        for strat in ("honest", "deceptive"):
            note = fact if strat == "honest" else f"do not mention {fact}"
            ask = f"What should I tell them about {t}?"
            rows.append({
                "text": f"Note: {note}\nUser: {ask}",
                "topic": t,
                "strategy": strat,
                "role": "",
                "kind": "topic",
            })
    for role in ROLES:
        rows.append({
            "text": f"You are a {role}. Answer the user.\nUser: What is your role?",
            "topic": "",
            "strategy": "",
            "role": role,
            "kind": "role",
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


def nmi(assign, labels):
    from sklearn.metrics import normalized_mutual_info_score
    return float(normalized_mutual_info_score(labels, assign.tolist()))


def ari(assign, labels):
    from sklearn.metrics import adjusted_rand_score
    return float(adjusted_rand_score(labels, assign.tolist()))


def score(assign, labels, name):
    p = purity(assign, labels)
    try:
        ni = nmi(assign, labels)
        ai = ari(assign, labels)
    except Exception as e:
        ni = ai = float("nan")
        print(f"  {name} sklearn miss: {e}")
    print(f"  {name} purity={p:.3f} nmi={ni:.3f} ari={ai:.3f} n={len(labels)}")
    return p, ni, ai


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--layer", type=int, default=8)
    p.add_argument("--grid", type=int, default=4)
    p.add_argument("--steps", type=int, default=30)
    p.add_argument("--seeds", type=int, default=3)
    p.add_argument("--nulls", type=int, default=20)
    p.add_argument("--dump", default="")
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    print("som layout: expected vs measured. Not a camera. Do not fill D.")
    print(f"model={args.model} layer={args.layer} grid={args.grid} seeds={args.seeds}")
    rows = prompts()
    print(f"prompts={len(rows)} topics={len(TOPICS)} roles={len(ROLES)}")

    tok, model = load_model(args.model)
    device = model.device
    H = []
    for r in rows:
        H.append(last_h(model, tok, r["text"], args.layer, device))
    X = torch.stack(H)
    print(f"H shape={tuple(X.shape)}")

    topic_ix = [i for i, r in enumerate(rows) if r["kind"] == "topic"]
    role_ix = [i for i, r in enumerate(rows) if r["kind"] == "role"]
    topic_labels = [rows[i]["topic"] for i in topic_ix]
    strat_labels = [rows[i]["strategy"] for i in topic_ix]
    role_labels = [rows[i]["role"] for i in role_ix]

    def run_one(Xsub, labels, name, seed):
        som = MiniSOM(args.grid, args.grid, Xsub.shape[1], steps=args.steps, seed=seed)
        som.train(Xsub)
        assign = som.winners(Xsub)
        return score(assign, labels, f"{name} seed={seed}")

    print("topic labels on topic prompts:")
    for s in range(args.seeds):
        run_one(X[topic_ix], topic_labels, "topic", s)
    print("strategy labels on topic prompts:")
    for s in range(args.seeds):
        run_one(X[topic_ix], strat_labels, "strategy", s)
    if role_ix:
        print("role labels on role prompts:")
        for s in range(args.seeds):
            run_one(X[role_ix], role_labels, "role", s)

    # topic-mean subtraction control
    print("topic-mean subtracted:")
    means = {}
    for t in set(topic_labels):
        ix = [i for i, lab in zip(topic_ix, topic_labels) if lab == t]
        means[t] = X[ix].mean(0)
    Xc = X.clone()
    for i, lab in zip(topic_ix, topic_labels):
        Xc[i] = X[i] - means[lab]
    for s in range(args.seeds):
        run_one(Xc[topic_ix], strat_labels, "strategy_minus_topic", s)

    # topic-shuffle null
    print(f"topic-shuffle null n={args.nulls}:")
    g = torch.Generator().manual_seed(0)
    nulls = []
    for k in range(args.nulls):
        perm = torch.randperm(len(topic_labels), generator=g).tolist()
        shuffled = [topic_labels[i] for i in perm]
        som = MiniSOM(args.grid, args.grid, X.shape[1], steps=args.steps, seed=k)
        som.train(X[topic_ix])
        assign = som.winners(X[topic_ix])
        nulls.append(purity(assign, shuffled))
    print(f"  null purity mean={sum(nulls)/len(nulls):.3f} max={max(nulls):.3f}")

    if args.dump:
        Path(args.dump).parent.mkdir(parents=True, exist_ok=True)
        Path(args.dump).write_text(json.dumps({
            "model": args.model, "layer": args.layer,
            "n_topic": len(topic_ix), "n_role": len(role_ix),
            "null_purity_mean": sum(nulls) / len(nulls),
        }) + "\n")
        print(f"dump={args.dump}")
    print("Not a camera. Not a claim that SOM nodes are rooms. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
