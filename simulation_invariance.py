#!/usr/bin/env python3
"""Output-preserving gauge: h'=A h, V'=V A^{-1}.

Logits stay. A frozen detector on h can flip.
Dummy linear net. Not Qwen.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def hinge(h: torch.Tensor, bank: torch.Tensor, tau: float) -> float:
    h_n = F.normalize(h, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return float(F.relu((h_n @ p_n.T).max() - tau))


def main() -> None:
    torch.manual_seed(0)
    d, tau = 4, 0.2
    x = torch.randn(1, d)
    W = torch.randn(d, d)
    V = torch.randn(2, d)
    bank = F.normalize(torch.randn(2, d), dim=-1)

    h = x @ W.T
    logits = h @ V.T
    L0 = hinge(h, bank, tau)

    A = torch.randn(d, d)
    A = A + 0.5 * torch.eye(d)
    Ainv = torch.linalg.inv(A)
    h2 = h @ A.T
    V2 = V @ Ainv
    logits2 = h2 @ V2.T
    L1 = hinge(h2, bank, tau)

    logit_l2 = float((logits - logits2).norm())
    hinge_delta = abs(L1 - L0)
    gaming = logit_l2 < 1e-4 and hinge_delta > 1e-3
    print("=== Gauge h'=A h, V'=V A^{-1}. Frozen D on h. Dummy. ===")
    print(f"logits L2={logit_l2:.2e} L_reg {L0:.4f} -> {L1:.4f} delta={hinge_delta:.4f}")
    print(f"gaming={gaming}  (logits same, hinge moved)")
    print("If the task head is rewritten with A^{-1}, behavior is unchanged.")
    print("A detector that still reads raw h can flip. That is coordinate gaming.")
    print("Not Qwen. Bank was not transformed.")


if __name__ == "__main__":
    main()
