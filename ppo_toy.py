#!/usr/bin/env python3
"""Minimal on-policy PPO + regret-hinge toy (NOT a trainer, NOT an alignment claim).

Contextual bandit: near/far contexts, discrete actions, clipped surrogate +
existing regret_loss from simulation.py. Prototype bank D is frozen.
Prints policy (clip) loss, clip fraction, L_regret before/after a few steps.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


# Reuse the hinge exactly as in simulation.py
def regret_loss(
    h_intent: torch.Tensor,
    prototypes: torch.Tensor,
    tau: float = 0.3,
) -> torch.Tensor:
    """Batch mean of ReLU(max_k cosine(h, d_k) - tau)."""
    h_n = F.normalize(h_intent, dim=-1)
    p_n = F.normalize(prototypes, dim=-1)
    sims = h_n @ p_n.T
    s_star = sims.max(dim=-1).values
    return F.relu(s_star - tau).mean()


class PolicyNet(nn.Module):
    """Tiny policy: context -> logits over actions + intent readout."""

    def __init__(self, ctx_dim: int = 16, d: int = 8, n_actions: int = 2):
        super().__init__()
        self.trunk = nn.Linear(ctx_dim, d, bias=False)
        self.action_head = nn.Linear(d, n_actions)
        # Readout is the trunk itself; gradients flow into trunk

    def forward(self, x: torch.Tensor):
        h = self.trunk(x)  # (B, d) intent vector
        logits = self.action_head(h)
        return logits, h


def main() -> None:
    torch.manual_seed(42)

    ctx_dim, d, K, n_actions = 16, 8, 3, 2
    tau = 0.3
    lambda_reg = 0.4
    eps_clip = 0.2
    n_steps = 5
    B = 8  # batch of contexts (half near, half far)

    policy = PolicyNet(ctx_dim=ctx_dim, d=d, n_actions=n_actions)

    # Frozen prototype bank D
    prototypes = torch.randn(K, d)
    prototypes.requires_grad_(False)

    # Build near/far contexts so hinge fires on near only (same construction as simulation.py)
    with torch.no_grad():
        W = policy.trunk.weight  # (d, ctx_dim)
        pinvW = torch.linalg.pinv(W)
        near_h = F.normalize(prototypes[:2], dim=-1)
        Q, _ = torch.linalg.qr(prototypes.T)
        null = torch.randn(2, d)
        null = null - null @ Q @ Q.T
        far_h = F.normalize(null, dim=-1)
        near_x = near_h @ pinvW.T
        far_x = far_h @ pinvW.T

    # Repeat to fill batch
    x_near = near_x.repeat(B // 4, 1)[: B // 2]
    x_far = far_x.repeat(B // 4, 1)[: B // 2]
    x = torch.cat([x_near, x_far], dim=0)  # (B, ctx_dim)

    # Simple rewards: action 0 good on near, action 1 good on far
    def sample_and_advantages(logits):
        dist = torch.distributions.Categorical(logits=logits)
        actions = dist.sample()
        logp = dist.log_prob(actions)
        prefer = torch.zeros(B, dtype=torch.long)
        prefer[B // 2 :] = 1
        rewards = (actions == prefer).float()
        advantages = rewards - rewards.mean()
        return actions, logp, advantages, rewards

    opt = torch.optim.Adam(policy.parameters(), lr=3e-2)

    print("=== PPO + regret-hinge toy (contextual bandit, illustration only) ===")
    print(f"B={B}, ctx_dim={ctx_dim}, d={d}, K={K}, n_actions={n_actions}, tau={tau}, eps={eps_clip}")
    print(f"prototypes shape: {tuple(prototypes.shape)}  (frozen, not in optimizer)")
    print()

    # Initial old policy snapshot
    with torch.no_grad():
        logits_old, h_old = policy(x)
        actions, logp_old, advantages, rewards = sample_and_advantages(logits_old)
        L_reg_init = regret_loss(h_old, prototypes, tau=tau)

    print(f"Init: mean reward={rewards.mean().item():.3f}  L_regret={L_reg_init.item():.4f}")

    for step in range(n_steps):
        logits, h = policy(x)
        dist = torch.distributions.Categorical(logits=logits)
        logp = dist.log_prob(actions)  # same actions from old

        ratio = torch.exp(logp - logp_old.detach())
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1.0 - eps_clip, 1.0 + eps_clip) * advantages
        L_clip = -torch.min(surr1, surr2).mean()  # minimize negative surrogate

        L_reg = regret_loss(h, prototypes, tau=tau)
        L_total = L_clip + lambda_reg * L_reg

        # Clip fraction: fraction of samples where ratio is outside [1-eps, 1+eps]
        with torch.no_grad():
            clipped = ((ratio < 1.0 - eps_clip) | (ratio > 1.0 + eps_clip)).float().mean()

        opt.zero_grad()
        L_total.backward()
        opt.step()

        print(
            f"step {step+1}: L_clip={L_clip.item():.4f}  clip_frac={clipped.item():.3f}  "
            f"L_regret={L_reg.item():.4f}  L_total={L_total.item():.4f}"
        )

        # Refresh old policy every step for this tiny toy (single-epoch style)
        with torch.no_grad():
            logits_old, _ = policy(x)
            actions, logp_old, advantages, rewards = sample_and_advantages(logits_old)

    # Final check: D still frozen, no grad on prototypes
    assert not prototypes.requires_grad
    print()
    print("D remains frozen (requires_grad=False). Script finished successfully.")
    print("This is NOT evidence of alignment, regret minimization, or PPO improvement.")


if __name__ == "__main__":
    main()
