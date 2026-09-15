#!/usr/bin/env python3
"""Toy illustration of the prototype-hinge loss (NOT an alignment proof)."""

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


def regret_loss(
    h_intent: torch.Tensor,
    prototypes: torch.Tensor,
    tau: float = 0.3,
) -> torch.Tensor:
    """Mean ReLU(max cosine - tau). Cosine is undefined at 0; normalize uses eps."""
    # eps floor: a true zero row is not a valid intent vector
    h_n = F.normalize(h_intent, dim=-1, eps=1e-12)
    p_n = F.normalize(prototypes, dim=-1, eps=1e-12)
    s_star = (h_n @ p_n.T).max(dim=-1).values
    return F.relu(s_star - tau).mean()


def main() -> None:
    torch.manual_seed(0)
    input_dim, d, K = 16, 8, 3
    tau = 0.3
    lambda_reg = 0.5
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
    B = x.shape[0]
    y = torch.randint(0, 2, (B,))
    task_head = nn.Linear(d, 2)
    opt = torch.optim.Adam(
        list(encoder.parameters()) + list(task_head.parameters()), lr=1e-2
    )

    def compute_losses():
        h_intent = encoder(x)
        L_task = F.cross_entropy(task_head(h_intent), y)
        L_regret = regret_loss(h_intent, prototypes, tau=tau)
        L_total = L_task + lambda_reg * L_regret
        L_near = regret_loss(h_intent[:2], prototypes, tau=tau)
        L_far = regret_loss(h_intent[2:], prototypes, tau=tau)
        return h_intent, L_task, L_regret, L_total, L_near, L_far

    h_intent, L_task, L_regret, L_total, L_near, L_far = compute_losses()
    L_total.backward()
    grad_before = encoder.proj.weight.grad.norm().item()
    print("=== Toy regret-heuristic simulation (illustration of the formula only) ===")
    print(f"Batch size B={B}, input_dim={input_dim}, d={d}, K={K}, tau={tau}")
    print(f"h_intent shape: {tuple(h_intent.shape)}")
    print(f"prototypes shape: {tuple(prototypes.shape)}  (frozen, not in optimizer)")
    print(f"Before step: L_task={L_task.item():.4f}  L_regret={L_regret.item():.4f}  L_total={L_total.item():.4f}")
    print(f"  group L_near={L_near.item():.4f}  L_far={L_far.item():.4f}")
    print(f"  encoder.proj.weight.grad norm={grad_before:.6f}")
    opt.step()
    opt.zero_grad()
    h_intent2, L_task2, L_regret2, L_total2, L_near2, L_far2 = compute_losses()
    L_total2.backward()
    grad_after = encoder.proj.weight.grad.norm().item()
    print(f"After 1 Adam step: L_task={L_task2.item():.4f}  L_regret={L_regret2.item():.4f}  L_total={L_total2.item():.4f}")
    print(f"  group L_near={L_near2.item():.4f}  L_far={L_far2.item():.4f}")
    print(f"  encoder.proj.weight.grad norm={grad_after:.6f}")
    print("Script finished successfully. This is NOT evidence of alignment or deception detection.")


if __name__ == "__main__":
    main()
