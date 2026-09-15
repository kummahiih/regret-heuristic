#!/usr/bin/env python3
"""CPU toy of math_formulation.md §F: per-example tau from a fake u(x).

Does NOT replace simulation.py. Same dummy encoder / seed-0 geometry as §1.
Not an LLM result. Not p(lie). Illustration of two likelihood widths only.
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


def s_star(h_intent: torch.Tensor, prototypes: torch.Tensor) -> torch.Tensor:
    h_n = F.normalize(h_intent, dim=-1)
    p_n = F.normalize(prototypes, dim=-1)
    return (h_n @ p_n.T).max(dim=-1).values


def hinge(s: torch.Tensor, tau) -> torch.Tensor:
    return F.relu(s - tau)


def main() -> None:
    torch.manual_seed(0)
    input_dim, d, K = 16, 8, 3
    tau_sure, tau_unsure = 0.3, 0.9
    u0 = 0.5

    encoder = DummyEncoder(input_dim=input_dim, d=d)
    prototypes = torch.randn(K, d)
    prototypes.requires_grad_(False)

    with torch.no_grad():
        W = encoder.proj.weight
        pinvW = torch.linalg.pinv(W)
        near_h = F.normalize(prototypes[:2], dim=-1)
        Q, _ = torch.linalg.qr(prototypes.T)
        null = torch.randn(2, d)
        null = null - null @ Q @ Q.T
        far_h = F.normalize(null, dim=-1)
        near_x = near_h @ pinvW.T
        far_x = far_h @ pinvW.T

    x = torch.cat([near_x, far_x], dim=0)
    u = torch.tensor([0.1, 0.8, 0.9, 0.7])
    sure = u <= u0
    tau = torch.where(sure, torch.full_like(u, tau_sure), torch.full_like(u, tau_unsure))

    h = encoder(x)
    s = s_star(h, prototypes)
    L_flat = hinge(s, tau_sure)
    L_bin = hinge(s, tau)

    names = ["near_sure", "near_unsure", "far_unsure_a", "far_unsure_b"]
    print("=== Tau-bin toy (§F). Not simulation.py. Not an LLM. ===")
    print(f"tau_sure={tau_sure} tau_unsure={tau_unsure} u0={u0}")
    print(f"u={u.tolist()} sure={sure.tolist()}")
    print(f"s_star={['%.4f' % v for v in s.tolist()]}")
    print("name           u     tau   s*    hinge_flat@0.3  hinge_binned")
    for i, name in enumerate(names):
        print(
            f"{name:14s} {u[i].item():.2f}  {tau[i].item():.1f}  {s[i].item():.4f}  "
            f"{L_flat[i].item():.4f}           {L_bin[i].item():.4f}"
        )
    print(
        f"mean hinge flat={L_flat.mean().item():.4f}  "
        f"mean hinge binned={L_bin.mean().item():.4f}"
    )
    print("near_unsure is close to D but tagged unsure: flat tau 0.70, binned tau 0.10.")
    print("That is a coarser likelihood, not a lie detector.")
    print("Script finished successfully. This is NOT evidence of alignment.")


if __name__ == "__main__":
    main()
