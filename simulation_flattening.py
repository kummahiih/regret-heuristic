#!/usr/bin/env python3
"""Attack the cosine hinge, not readout norm.

Frozen detector and frozen D. Optimize h so hinge dies while task class stays 1.
Dummy. Not Qwen. Label is the constructed class, not a lie detector.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from simulation_source_count import source_count


class DynamicDetector(nn.Module):
    def __init__(self, d: int, K: int = 3, noise_sigma: float = 0.0):
        super().__init__()
        self.K, self.noise_sigma = K, noise_sigma
        self.step_net = nn.Sequential(nn.Linear(d, d), nn.GELU(), nn.Linear(d, d))
        self.readout = nn.Linear(d, d)

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        state = h
        for _ in range(self.K):
            noise = torch.randn_like(state) * self.noise_sigma if self.noise_sigma > 0 else 0.0
            state = state + self.step_net(state) + noise
        return self.readout(state)


def hinge(r: torch.Tensor, bank: torch.Tensor, tau: float) -> torch.Tensor:
    r_n = F.normalize(r, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return F.relu((r_n @ p_n.T).max(dim=-1).values - tau).mean()


def main() -> None:
    torch.manual_seed(42)
    d, tau = 8, 0.3
    detector = DynamicDetector(d, K=3, noise_sigma=0.0)
    detector.requires_grad_(False)
    task_head = nn.Linear(d, 2)
    task_head.requires_grad_(False)
    bank = F.normalize(torch.randn(3, d), dim=-1)
    bank.requires_grad_(False)

    h_base = nn.Parameter(bank[0:1].detach().clone())
    target = torch.tensor([1])
    opt = torch.optim.Adam([h_base], lr=0.05)

    print("=== Flattening vs cosine hinge. Frozen D and detector. Dummy proxy class. ===")
    print("L_reg is ReLU(max cos - tau), not ||z||.")

    def report(step: int) -> None:
        with torch.no_grad():
            z = detector(h_base)
            L_task = F.cross_entropy(task_head(h_base), target)
            L_reg = hinge(z, bank, tau)
            pred = int(task_head(h_base).argmax(-1).item())
            m_hat = source_count(h_base.detach())
            print(
                f"step {step:3d} L_task={L_task.item():.4f} L_reg={L_reg.item():.4f} "
                f"pred={pred} proxy_behavior={pred == 1} "
                f"||h||={h_base.norm().item():.4f} m_hat={m_hat}"
            )

    report(0)
    for step in range(1, 201):
        z = detector(h_base)
        loss = F.cross_entropy(task_head(h_base), target) + hinge(z, bank, tau)
        loss.backward()
        opt.step()
        opt.zero_grad()
        if step in (50, 200):
            report(step)
    print("m_hat is one walk vector. Not in L.")
    print("Quiet hinge + pred!=1 is 'stop being the dummy class', not gaming.")
    print("Quiet hinge + pred==1 is the dummy evasion cartoon. Not Qwen.")


if __name__ == "__main__":
    main()
