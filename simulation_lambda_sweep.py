#!/usr/bin/env python3
"""lambda sweep on dummy encoder. L_task vs L_reg. Not behavior.

Writes results/lambda_sweep.jsonl next to the script if that dir exists,
else prints rows only.
"""

from __future__ import annotations

import json
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F


def hinge(h: torch.Tensor, bank: torch.Tensor, tau: float) -> torch.Tensor:
    h_n = F.normalize(h, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return F.relu((h_n @ p_n.T).max(dim=-1).values - tau).mean()


def run(seed: int, lam: float) -> dict:
    torch.manual_seed(seed)
    d, tau = 8, 0.3
    enc = nn.Linear(16, d, bias=False)
    head = nn.Linear(d, 2)
    bank = F.normalize(torch.randn(3, d), dim=-1)
    x = torch.randn(8, 16)
    y = torch.randint(0, 2, (8,))
    opt = torch.optim.Adam(list(enc.parameters()) + list(head.parameters()), lr=1e-2)
    h = enc(x)
    with torch.no_grad():
        L_task0 = float(F.cross_entropy(head(h), y))
        L_reg0 = float(hinge(h, bank, tau))
    for _ in range(20):
        h = enc(x)
        loss = F.cross_entropy(head(h), y) + lam * hinge(h, bank, tau)
        opt.zero_grad()
        loss.backward()
        opt.step()
    h = enc(x)
    with torch.no_grad():
        L_task = float(F.cross_entropy(head(h), y))
        L_reg = float(hinge(h, bank, tau))
    return {
        "seed": seed,
        "lambda": lam,
        "L_task0": L_task0,
        "L_reg0": L_reg0,
        "L_task": L_task,
        "L_reg": L_reg,
    }


def main() -> None:
    lambs = [0.0, 0.01, 0.03, 0.1, 0.3, 1.0]
    seeds = [0, 1, 2]
    rows = [run(s, lam) for s in seeds for lam in lambs]
    print("=== Dummy lambda sweep. Not deception. ===")
    print("seed lambda L_task L_reg")
    for r in rows:
        print(f"{r['seed']} {r['lambda']:.2f} {r['L_task']:.4f} {r['L_reg']:.4f}")
    out = Path(__file__).resolve().parent / "results" / "lambda_sweep.jsonl"
    if out.parent.is_dir():
        out.write_text("".join(json.dumps(r) + "\n" for r in rows))
        print(f"wrote {out} n={len(rows)}")
    else:
        print(f"no {out.parent}; printed only. n={len(rows)}")


if __name__ == "__main__":
    main()
