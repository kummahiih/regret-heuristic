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

    # Prototype bank D (K, d) — frozen; never added to optimizer
    prototypes = torch.randn(K, d)
    prototypes.requires_grad_(False)

    # Build near/far in intent space so hinge fires on near only.
    # Near: encoder maps to (near) prototypes; far: orthogonal to span(D).
    # Use pinv of current weight so initial h matches the targets exactly.
    with torch.no_grad():
        W = encoder.proj.weight  # (d, input_dim)
        pinvW = torch.linalg.pinv(W)
        near_h = F.normalize(prototypes[:2], dim=-1)  # (2, d)
        # Far: component orthogonal to span of prototypes (QR null space)
        Q, _ = torch.linalg.qr(prototypes.T)
        null = torch.randn(2, d)
        null = null - null @ Q @ Q.T
        far_h = F.normalize(null, dim=-1)
        near_x = near_h @ pinvW.T  # (2, input_dim)
        far_x = far_h @ pinvW.T

    x = torch.cat([near_x, far_x], dim=0)  # (4, input_dim)
    B = x.shape[0]
    y = torch.randint(0, 2, (B,))

    task_head = nn.Linear(d, 2)

    # Optimizer: encoder + task_head only. D frozen, not in optimizer.
    opt = torch.optim.Adam(
        list(encoder.parameters()) + list(task_head.parameters()), lr=1e-2
    )

    def compute_losses():
        h_intent = encoder(x)
        logits = task_head(h_intent)
        L_task = F.cross_entropy(logits, y)
        L_regret = regret_loss(h_intent, prototypes, tau=tau)
        L_total = L_task + lambda_reg * L_regret
        L_near = regret_loss(h_intent[:2], prototypes, tau=tau)
        L_far = regret_loss(h_intent[2:], prototypes, tau=tau)
        return h_intent, L_task, L_regret, L_total, L_near, L_far

    # --- Before step ---
    h_intent, L_task, L_regret, L_total, L_near, L_far = compute_losses()
    L_total.backward()
    grad_before = (
        encoder.proj.weight.grad.norm().item()
        if encoder.proj.weight.grad is not None
        else 0.0
    )

    print("=== Toy regret-heuristic simulation (illustration of the formula only) ===")
    print(f"Batch size B={B}, input_dim={input_dim}, d={d}, K={K}, tau={tau}")
    print(f"h_intent shape: {tuple(h_intent.shape)}")
    print(f"prototypes shape: {tuple(prototypes.shape)}  (frozen, not in optimizer)")
    print(f"Before step: L_task={L_task.item():.4f}  L_regret={L_regret.item():.4f}  L_total={L_total.item():.4f}")
    print(f"  group L_near={L_near.item():.4f}  L_far={L_far.item():.4f}")
    print(f"  encoder.proj.weight.grad norm={grad_before:.6f}")

    # One Adam step
    opt.step()
    opt.zero_grad()

    # --- After step ---
    h_intent2, L_task2, L_regret2, L_total2, L_near2, L_far2 = compute_losses()
    L_total2.backward()
    grad_after = (
        encoder.proj.weight.grad.norm().item()
        if encoder.proj.weight.grad is not None
        else 0.0
    )

    print(f"After 1 Adam step: L_task={L_task2.item():.4f}  L_regret={L_regret2.item():.4f}  L_total={L_total2.item():.4f}")
    print(f"  group L_near={L_near2.item():.4f}  L_far={L_far2.item():.4f}")
    print(f"  encoder.proj.weight.grad norm={grad_after:.6f}")

    print("Script finished successfully. This is NOT evidence of alignment or deception detection.")


if __name__ == "__main__":
    main()
