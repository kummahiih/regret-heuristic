#!/usr/bin/env python3
"""Dummy SIREN path encoder. $0 toy. Not Qwen. Not in L.

Four notes: honest/deceptive x topic A/B.
Each note is a short path t=0..1 toward its (plan, topic) point.
Fit a tiny sine MLP f_theta(t) ~ h_t. Score f(1) with static r = coord 0.
Also compare theta L2 on plan pairs vs topic pairs.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class TinySiren(nn.Module):
    def __init__(self, d: int, hidden: int = 16):
        super().__init__()
        self.fc1 = nn.Linear(1, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.fc3 = nn.Linear(hidden, d)
        with torch.no_grad():
            self.fc1.weight.mul_(30.0)

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        x = torch.sin(self.fc1(t))
        x = torch.sin(self.fc2(x))
        return self.fc3(x)


def fit_path(path: torch.Tensor, steps: int = 80) -> TinySiren:
    T, d = path.shape
    net = TinySiren(d)
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    t = torch.linspace(0, 1, T).unsqueeze(-1)
    for _ in range(steps):
        pred = net(t)
        loss = F.mse_loss(pred, path)
        opt.zero_grad()
        loss.backward()
        opt.step()
    return net


def theta_vec(net: TinySiren) -> torch.Tensor:
    return torch.cat([p.detach().flatten() for p in net.parameters()])


def main() -> None:
    torch.manual_seed(0)
    d, T = 8, 8
    e_plan = torch.zeros(d)
    e_plan[0] = 1.0
    e_topic = torch.zeros(d)
    e_topic[1] = 1.0

    def path(plan: float, topic: float) -> torch.Tensor:
        end = plan * e_plan + topic * e_topic
        alpha = torch.linspace(0, 1, T).unsqueeze(-1)
        return alpha * end + 0.02 * torch.randn(T, d)

    notes = [
        path(-1.0, 1.0),
        path(1.0, 1.0),
        path(-1.0, -1.0),
        path(1.0, -1.0),
    ]
    labels_plan = torch.tensor([0.0, 1.0, 0.0, 1.0])
    labels_topic = torch.tensor([1.0, 1.0, 0.0, 0.0])

    nets = [fit_path(p) for p in notes]
    with torch.no_grad():
        r = torch.stack([n(torch.tensor([[1.0]]))[0] for n in nets])
        r0 = r[:, 0]
        plan_gap = float(r0[labels_plan > 0.5].mean() - r0[labels_plan < 0.5].mean())
        topic_gap = float(r0[labels_topic > 0.5].mean() - r0[labels_topic < 0.5].mean())
        thetas = torch.stack([theta_vec(n) for n in nets])
        d_same_topic = float((thetas[0] - thetas[1]).norm())
        d_same_plan = float((thetas[0] - thetas[2]).norm())

    print("=== Dummy SIREN path. Not Qwen. theta not in L. ===")
    print(f"f(1) plan_gap={plan_gap:.4f} topic_on_r0={topic_gap:.4f}")
    print(
        f"theta L2 same-topic-diff-plan={d_same_topic:.4f} "
        f"same-plan-diff-topic={d_same_plan:.4f}"
    )
    print("Want: plan_gap large, topic_on_r0 ~0, theta plan-diff > topic-diff.")
    print("If theta L2 is larger across topic, the curve stored the hallway.")
    print("Not a camera. Not $1 cloud. Dummy paths only.")


if __name__ == "__main__":
    main()
