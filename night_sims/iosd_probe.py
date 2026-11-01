#!/usr/bin/env python3
"""IOSD-style orthogonal directions as candidate pin bank.
Diagnostic by default. Becomes protocol component only if topic-transfer gate passes.
See protocol_gate.md.
"""
import argparse, json, torch, torch.nn as nn, torch.nn.functional as F
from pathlib import Path

def train_linear(X, y, dim, steps=40, lr=1e-2):
    w = nn.Parameter(torch.randn(dim) * 0.01)
    opt = torch.optim.Adam([w], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        loss = F.binary_cross_entropy_with_logits(X @ w, y.float())
        loss.backward()
        opt.step()
    return F.normalize(w.detach(), dim=0)

def iosd(X, y, K=3, steps=30):
    dirs = []
    Xr = X.clone()
    for _ in range(K):
        w = train_linear(Xr, y, X.shape[1], steps)
        for prev in dirs:
            w = w - (w @ prev) * prev
        w = F.normalize(w, dim=0)
        dirs.append(w)
        Xr = Xr - (Xr @ w).unsqueeze(1) * w.unsqueeze(0)
    return torch.stack(dirs)

def max_cos(X, bank):
    Xn = F.normalize(X, dim=-1)
    Bn = F.normalize(bank, dim=-1)
    return (Xn @ Bn.T).max(dim=-1).values

def auroc(scores, labels):
    # simple Mann-Whitney
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    correct = 0
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
        print("iosd", dirs.shape, "orth check", (dirs @ dirs.T).abs().mean().item())
        sc = max_cos(X, dirs)
        print("smoke auroc", auroc(sc, y))
        print("smoke ok — diagnostic only until gate")
