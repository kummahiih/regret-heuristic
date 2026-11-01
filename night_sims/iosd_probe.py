#!/usr/bin/env python3
"""IOSD-style orthogonal directions as candidate pin bank.
Diagnostic by default. Becomes protocol component only if topic-transfer gate passes.
See protocol_gate.md.

Prototype only. --smoke runs on synthetic data. No real activation loader yet.
"""
import argparse, torch, torch.nn as nn, torch.nn.functional as F

def train_linear(X, y, dim, steps=40, lr=1e-2):
    w = nn.Parameter(torch.randn(dim) * 0.01)
    opt = torch.optim.Adam([w], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        loss = F.binary_cross_entropy_with_logits(X @ w, y.float())
        loss.backward()
        opt.step()
    return w.detach()

def iosd(X, y, K=3, steps=30, eps=1e-6):
    dirs = []
    Xr = X.clone()
    for _ in range(K):
        w = train_linear(Xr, y, X.shape[1], steps)
        for prev in dirs:
            w = w - (w @ prev) * prev
        nrm = w.norm()
        if nrm < eps:
            print("rejected degenerate direction")
            break
        w = w / nrm
        dirs.append(w)
        Xr = Xr - (Xr @ w).unsqueeze(1) * w.unsqueeze(0)
    return torch.stack(dirs) if dirs else torch.empty(0, X.shape[1])

def max_cos(X, bank):
    # signed max cosine; polarity is part of the hypothesis
    Xn = F.normalize(X, dim=-1)
    Bn = F.normalize(bank, dim=-1)
    return (Xn @ Bn.T).max(dim=-1).values

def auroc(scores, labels):
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    correct = 0.0
    for p in pos:
        correct += (p > neg).sum() + 0.5 * (p == neg).sum()
    return float(correct / (len(pos) * len(neg)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--K", type=int, default=3)
    args = parser.parse_args()
    if args.smoke:
        N, D = 40, 16
        X = torch.randn(N, D)
        y = (torch.randn(N) > 0).long()
        dirs = iosd(X, y, K=args.K)
        print("iosd", dirs.shape)
        if dirs.numel():
            print("orth check", (dirs @ dirs.T).abs().mean().item())
            print("smoke auroc", auroc(max_cos(X, dirs), y))
        print("smoke ok — prototype only, no real data pipeline")
    else:
        print("no real activation loader yet; use --smoke")
