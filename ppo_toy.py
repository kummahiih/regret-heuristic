#!/usr/bin/env python3
"""PPO-shaped dummy: clipped surrogate + prototype-avoidance.

Not S_safe. Not r_strat. Frozen D. Same near/far construction as simulation.py.
pi_old is held for n_steps so clip can fire. That is the only change vs refresh-every-step.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def regret_loss(h_intent: torch.Tensor, prototypes: torch.Tensor, tau: float = 0.3) -> torch.Tensor:
    h_n = F.normalize(h_intent, dim=-1, eps=1e-12)
    p_n = F.normalize(prototypes, dim=-1, eps=1e-12)
    return F.relu((h_n @ p_n.T).max(dim=-1).values - tau).mean()


class PolicyNet(nn.Module):
    def __init__(self, ctx_dim: int = 16, d: int = 8, n_actions: int = 2):
        super().__init__()
        self.trunk = nn.Linear(ctx_dim, d, bias=False)
        self.action_head = nn.Linear(d, n_actions)

    def forward(self, x: torch.Tensor):
        h = self.trunk(x)
        return self.action_head(h), h


def main() -> None:
    torch.manual_seed(42)
    ctx_dim, d, K, n_actions = 16, 8, 3, 2
    tau, lambda_reg, eps_clip, n_steps, B = 0.3, 0.4, 0.2, 5, 8
    policy = PolicyNet(ctx_dim, d, n_actions)
    prototypes = torch.randn(K, d)
    prototypes.requires_grad_(False)

    with torch.no_grad():
        W = policy.trunk.weight
        pinvW = torch.linalg.pinv(W)
        near_h = F.normalize(prototypes[:2], dim=-1)
        Q, _ = torch.linalg.qr(prototypes.T)
        null = torch.randn(2, d)
        null = null - null @ Q @ Q.T
        far_h = F.normalize(null, dim=-1)
        x = torch.cat([near_h @ pinvW.T, far_h @ pinvW.T], dim=0)
        x = x.repeat(B // x.shape[0] + 1, 1)[:B]

    prefer = torch.zeros(B, dtype=torch.long)
    prefer[B // 2 :] = 1

    with torch.no_grad():
        logits_old, h0 = policy(x)
        dist_old = torch.distributions.Categorical(logits=logits_old)
        actions = dist_old.sample()
        logp_old = dist_old.log_prob(actions)
        rewards = (actions == prefer).float()
        advantages = rewards - rewards.mean()
        L_reg0 = float(regret_loss(h0, prototypes, tau))

    opt = torch.optim.Adam(policy.parameters(), lr=3e-2)
    print("=== PPO dummy. Not S_safe. r is the trunk. D frozen. ===")
    print(f"init reward={float(rewards.mean()):.3f} L_reg={L_reg0:.4f} eps={eps_clip}")
    print("pi_old held for all steps (clip can fire).")

    for step in range(n_steps):
        logits, h = policy(x)
        logp = torch.distributions.Categorical(logits=logits).log_prob(actions)
        ratio = torch.exp(logp - logp_old)
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - eps_clip, 1 + eps_clip) * advantages
        L_clip = -torch.min(surr1, surr2).mean()
        L_reg = regret_loss(h, prototypes, tau)
        loss = L_clip + lambda_reg * L_reg
        with torch.no_grad():
            clip_frac = float(((ratio < 1 - eps_clip) | (ratio > 1 + eps_clip)).float().mean())
        opt.zero_grad()
        loss.backward()
        opt.step()
        print(
            f"step {step+1} L_clip={float(L_clip.detach()):.4f} clip_frac={clip_frac:.3f} "
            f"L_reg={float(L_reg.detach()):.4f} L_sum={float(loss.detach()):.4f}"
        )

    assert not prototypes.requires_grad
    print("D frozen. Not alignment. Not a camera. Not S_safe.")


if __name__ == "__main__":
    main()
