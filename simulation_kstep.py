#!/usr/bin/env python3
"""K-step trajectory encoder. Hinge only on s_K.

Control: mean of per-token hinges. Dummy path. Not Qwen.
s_{k+1} = (1-a) s_k + a F(s_k, h_bar)
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def hinge(r: torch.Tensor, bank: torch.Tensor, tau: float) -> torch.Tensor:
    r_n = F.normalize(r, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return F.relu((r_n @ p_n.T).max(dim=-1).values - tau)


def main() -> None:
    torch.manual_seed(0)
    d, T, K, a, tau = 8, 4, 3, 0.4, 0.2
    h = F.normalize(torch.randn(T, d), dim=-1)
    bank = F.normalize(torch.randn(2, d), dim=-1)
    Fnet = nn.Linear(2 * d, d)
    h_bar = h.mean(0)

    s = h[0]
    for _ in range(K):
        s = (1 - a) * s + a * Fnet(torch.cat([s, h_bar], dim=-1))

    with torch.no_grad():
        L_sK = float(hinge(s.unsqueeze(0), bank, tau))
        L_mean = float(hinge(h, bank, tau).mean())
        L_last = float(hinge(h[-1:], bank, tau))
    print("=== K-step s_K vs mean of per-token hinges. Dummy path. ===")
    print(f"L_reg(s_K)={L_sK:.4f}  L_reg(mean tokens)={L_mean:.4f}  L_reg(last)={L_last:.4f}")
    print("Official slap is s_K only. Mean-of-tokens is the failed control (§6 smear).")
    print("F is a dummy linear mix of s and mean(h). Not a camera.")


if __name__ == "__main__":
    main()
