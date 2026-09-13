#!/usr/bin/env python3
"""Toy illustration of the regret-heuristic loss (NOT an alignment proof).

Implements the max-similarity hinge from math_formulation.md with a dummy
encoder so the script runs without any LLM or real model weights.

Tensor shapes are documented inline. This is a shape-and-gradient skeleton
only; it does not claim to detect or reduce deception.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class DummyEncoder(nn.Module):
    """Fixed random linear map standing in for h(x) + r(·).

    Input:  (B, input_dim)
    Output: (B, d)  intent vectors
    """

    def __init__(self, input_dim: int = 16, d: int = 8):
        super().__init__()
        self.proj = nn.Linear(input_dim, d, bias=False)
        # Freeze so the toy focuses on the regret term itself
        for p in self.parameters():
            p.requires_grad_(False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, input_dim) -> h_intent: (B, d)
        return self.proj(x)


def regret_loss(
    h_intent: torch.Tensor,
    prototypes: torch.Tensor,
    tau: float = 0.3,
) -> torch.Tensor:
    """Batch mean of ReLU(max_k cosine(h, d_k) - tau).

    Args:
        h_intent:   (B, d)   readout vectors
        prototypes: (K, d)   bank D
        tau:        scalar hinge threshold in (-1, 1)

    Returns:
        scalar tensor  mean L_regret over the batch
    """
    # Normalize for cosine
    h_n = F.normalize(h_intent, dim=-1)          # (B, d)
    p_n = F.normalize(prototypes, dim=-1)        # (K, d)

    # Cosine similarities: (B, K)
    sims = h_n @ p_n.T

    # Max similarity per example: (B,)
    s_star = sims.max(dim=-1).values

    # Hinge and batch mean
    return F.relu(s_star - tau).mean()


def main() -> None:
    torch.manual_seed(0)

    B, input_dim, d, K = 4, 16, 8, 3
    tau = 0.3
    lambda_reg = 0.5

    encoder = DummyEncoder(input_dim=input_dim, d=d)
    # Prototype bank (K, d) — random fixed vectors
    prototypes = torch.randn(K, d)

    # Dummy batch of inputs (B, input_dim)
    x = torch.randn(B, input_dim)
    # Dummy task targets (unused beyond shape)
    y = torch.randint(0, 2, (B,))

    # Forward: intent vectors (B, d)
    h_intent = encoder(x)

    # Toy task loss (cross-entropy on a random linear head)
    task_head = nn.Linear(d, 2)
    logits = task_head(h_intent.detach())  # detach so task does not train encoder
    L_task = F.cross_entropy(logits, y)

    # Regret term
    L_regret = regret_loss(h_intent, prototypes, tau=tau)

    # Combined objective (illustration only)
    L_total = L_task + lambda_reg * L_regret

    print("=== Toy regret-heuristic simulation (illustration only) ===")
    print(f"Batch size B={B}, input_dim={input_dim}, d={d}, K={K}, tau={tau}")
    print(f"h_intent shape: {tuple(h_intent.shape)}")
    print(f"prototypes shape: {tuple(prototypes.shape)}")
    print(f"L_task={L_task.item():.4f}  L_regret={L_regret.item():.4f}  L_total={L_total.item():.4f}")
    print("Script finished successfully. This is NOT evidence of alignment.")


if __name__ == "__main__":
    main()
