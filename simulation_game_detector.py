#!/usr/bin/env python3
"""Min hinge. Keep dummy deceptive label. Freeze r, D, tau.

CPU. Not Qwen. label_unchanged is a frozen class head, not a lie detector.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def hinge(h: torch.Tensor, bank: torch.Tensor, tau: float) -> torch.Tensor:
    h_n = F.normalize(h, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return F.relu((h_n @ p_n.T).max(dim=-1).values - tau).mean()


def main() -> None:
    torch.manual_seed(0)
    d, tau = 8, 0.3
    bank = F.normalize(torch.randn(3, d), dim=-1)
    bank.requires_grad_(False)
    behavior = nn.Linear(d, 2)
    behavior.requires_grad_(False)

    h = nn.Parameter(bank[0:1].detach().clone())
    target = torch.tensor([1])
    with torch.no_grad():
        start_pred = int(behavior(h).argmax(-1).item())
        if start_pred != 1:
            target = torch.tensor([start_pred])
    opt = torch.optim.Adam([h], lr=0.05)

    def pack(step: int) -> None:
        with torch.no_grad():
            L_reg = float(hinge(h, bank, tau))
            pred = int(behavior(h).argmax(-1).item())
            print(
                f"step {step:3d} L_reg={L_reg:.4f} pred={pred} "
                f"label_unchanged={pred == int(target.item())}"
            )

    print("=== Game frozen D. Keep dummy label. Not Qwen. ===")
    pack(0)
    for step in range(1, 81):
        loss = hinge(h, bank, tau) + 2.0 * F.cross_entropy(behavior(h), target)
        loss.backward()
        opt.step()
        opt.zero_grad()
        if step in (20, 80):
            pack(step)
    print("label_unchanged + L_reg->0 is the dummy evasion the critic asked for.")
    print("No real deceptive behavior. Freeze r,D,tau held.")


if __name__ == "__main__":
    main()
