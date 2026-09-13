#!/usr/bin/env python3
"""Toy illustration of the regret-heuristic loss (NOT an alignment proof).

Implements the max-similarity hinge from math_formulation.md with a dummy
encoder so the script runs without any LLM or real model weights.

Tensor shapes are documented inline. This is a shape-and-gradient skeleton
only; it does not claim to detect or reduce deception. Illustration of the
formula only.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class DummyEncoder(nn.Module):
    """Trainable linear map standing in for h(x) + r(·).

    Input:  (B, input_dim)
    Output: (B, d)  intent vectors
    """

    def __init__(self, input_dim: int = 16, d: int = 8):
        super().__init__()
        self.proj = nn.Linear(input_dim, d, bias=False)
        # Unfrozen: gradients of L_regret flow into shared weights

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

    input_dim, d, K = 16, 8, 3
    tau = 0.3
    lambda_reg = 0.5

    encoder = DummyEncoder(input_dim=input_dim, d=d)
    # Prototype bank (K, d) — random fixed vectors
    prototypes = torch.randn(K, d)

    # Two synthetic groups so hinge is nonzero on one:
    # near bank: inputs whose projection lands near prototypes
    # far bank: inputs far from the bank
    near_x = prototypes[0].unsqueeze(0).repeat(2, 1)  # (2, d) but need input_dim
    # Map prototypes back to input space via a fixed inverse-ish random map
    inv = torch.randn(d, input_dim)
    near_x = (prototypes[:2] @ inv)  # (2, input_dim) near the bank after encode
    far_x = torch.randn(2, input_dim) * 3.0  # far group
    x = torch.cat([near_x, far_x], dim=0)  # (4, input_dim)
    B = x.shape[0]
    y = torch.randint(0, 2, (B,))

    # Forward: intent vectors (B, d) — no detach on regret path
    h_intent = encoder(x)

    # Toy task loss (cross-entropy on a random linear head)
    task_head = nn.Linear(d, 2)
    logits = task_head(h_intent)  # no detach: task may also touch encoder
    L_task = F.cross_entropy(logits, y)

    # Regret term (gradients flow into encoder)
    L_regret = regret_loss(h_intent, prototypes, tau=tau)

    # Combined objective (illustration only)
    L_total = L_task + lambda_reg * L_regret

    # Train step: call backward so encoder.proj.weight.grad is populated
    L_total.backward()

    grad_norm = encoder.proj.weight.grad.norm().item() if encoder.proj.weight.grad is not None else 0.0

    print("=== Toy regret-heuristic simulation (illustration of the formula only) ===")
    print(f"Batch size B={B}, input_dim={input_dim}, d={d}, K={K}, tau={tau}")
    print(f"h_intent shape: {tuple(h_intent.shape)}")
    print(f"prototypes shape: {tuple(prototypes.shape)}")
    print(f"L_task={L_task.item():.4f}  L_regret={L_regret.item():.4f}  L_total={L_total.item():.4f}")
    print(f"encoder.proj.weight.grad norm={grad_norm:.6f}")
    print("Script finished successfully. This is NOT evidence of alignment or deception detection.")


if __name__ == "__main__":
    main()
