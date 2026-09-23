#!/usr/bin/env python3
"""Cosine-hinge flatten through encoder parameters, not free h.

x -> enc_theta(x) -> h. Frozen D. Frozen class head is dummy B.
Not Qwen. Not a lie detector.
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
    d_in, d, tau = 16, 8, 0.3
    enc = nn.Linear(d_in, d, bias=False)
    Bhead = nn.Linear(d, 2)
    Bhead.requires_grad_(False)
    bank = F.normalize(torch.randn(3, d), dim=-1)
    bank.requires_grad_(False)

    with torch.no_grad():
        pin = bank[0:1].repeat(8, 1)
        x = pin @ torch.linalg.pinv(enc.weight).T
        h0 = enc(x)
        pred0 = Bhead(h0).argmax(-1)
        y = pred0.clone()
        B0 = float((pred0 == y).float().mean())
        L_reg0 = float(hinge(h0, bank, tau))
        L_task0 = float(F.cross_entropy(Bhead(h0), y))

    opt = torch.optim.Adam(enc.parameters(), lr=5e-2)
    print("=== Flatten via theta. Frozen D and B-head. Dummy. ===")
    print(f"step 0 L_task={L_task0:.4f} L_reg={L_reg0:.4f} B={B0:.3f} B_ok={B0 >= 0.99}")

    for step in range(1, 81):
        h = enc(x)
        L_task = F.cross_entropy(Bhead(h), y)
        L_reg = hinge(h, bank, tau)
        loss = L_task + L_reg
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step in (20, 80):
            with torch.no_grad():
                pred = Bhead(h).argmax(-1)
                B = float((pred == y).float().mean())
                print(
                    f"step {step} L_task={float(L_task.detach()):.4f} L_reg={float(L_reg.detach()):.4f} "
                    f"B={B:.3f} B_ok={B >= 0.99}"
                )
    print("B is a frozen linear class, not strategy. exists-theta, not exists-h.")
    print("Not Qwen. Not OOD.")


if __name__ == "__main__":
    main()
