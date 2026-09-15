#!/usr/bin/env python3
"""CPU toy: a map cell that is not on the batch walk.

Does NOT replace simulation.py or simulation_tau_bins.py.
Same seed-0 encoder / D / near-far batch. Extra unit pin orthogonal to
span(D) and to the two far walk vectors. Not an LLM. Not p(lie).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class DummyEncoder(nn.Module):
    def __init__(self, input_dim: int = 16, d: int = 8):
        super().__init__()
        self.proj = nn.Linear(input_dim, d, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.proj(x)


def main() -> None:
    torch.manual_seed(0)
    input_dim, d, K = 16, 8, 3
    encoder = DummyEncoder(input_dim=input_dim, d=d)
    prototypes = torch.randn(K, d)
    prototypes.requires_grad_(False)

    with torch.no_grad():
        W = encoder.proj.weight
        pinvW = torch.linalg.pinv(W)
        near_h = F.normalize(prototypes[:2], dim=-1)
        Qd, _ = torch.linalg.qr(prototypes.T, mode="reduced")
        null = torch.randn(2, d)
        null = null - null @ Qd @ Qd.T
        far_h = F.normalize(null, dim=-1)
        near_x = near_h @ pinvW.T
        far_x = far_h @ pinvW.T
        span = torch.cat([prototypes, far_h], dim=0)
        Qs, _ = torch.linalg.qr(span.T, mode="reduced")
        leftover = torch.randn(d)
        leftover = leftover - Qs @ (Qs.T @ leftover)
        held = F.normalize(leftover, dim=0)

    x = torch.cat([near_x, far_x], dim=0)
    h = encoder(x)
    h_n = F.normalize(h, dim=-1)
    p_n = F.normalize(prototypes, dim=-1)
    s_D = (h_n @ p_n.T).max(dim=-1).values
    s_H = h_n @ held

    names = ["near_0", "near_1", "far_0", "far_1"]
    print("=== Held-out cell toy. Not simulation.py. Not an LLM. ===")
    print(f"heldout_norm={held.norm().item():.4f}  heldout_vs_D_max={(held @ p_n.T).abs().max().item():.4f}")
    print("name     s*_D   cos_heldout")
    for i, name in enumerate(names):
        print(f"{name:8s} {s_D[i].item():.4f}  {s_H[i].item():.4f}")
    print("Walk points can sit on D and still miss the unprinted pin.")
    print("This pin is constructed, not observed from a prompt.")
    print("Script finished successfully. This is NOT evidence of alignment.")


if __name__ == "__main__":
    main()
