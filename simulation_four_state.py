#!/usr/bin/env python3
"""Four-state dummy + five T. Held-out v in ker static_r.

T is not trained on v. Contractive isotropic T should keep evasion invisible
and shrink plan. A structural mixer that folds high coords into coord 0
can reveal v without a least-squares fit on this v.
Not Qwen. Not a basin proof.
"""

from __future__ import annotations

import torch


def static_r(h: torch.Tensor) -> torch.Tensor:
    return h[..., :1]


def gap(scores_dec: torch.Tensor, scores_hon: torch.Tensor) -> float:
    return float(scores_dec.mean() - scores_hon.mean())


def apply_T(h: torch.Tensor, F: torch.Tensor, K: int, sigma: float) -> torch.Tensor:
    state = h
    for _ in range(K):
        noise = sigma * torch.randn_like(state) if sigma > 0 else 0.0
        state = state + state @ F.T + noise
    return state


def metrics(h, h_ev, labels_plan, labels_topic):
    r = static_r(h).squeeze(-1)
    r_ev = static_r(h_ev).squeeze(-1)
    plan_gap = gap(r[labels_plan > 0.5], r[labels_plan < 0.5])
    topic_on_r = gap(r[labels_topic > 0.5], r[labels_topic < 0.5])
    evasion_vis = float((r_ev - r).abs().mean())
    return plan_gap, topic_on_r, evasion_vis


def main() -> None:
    torch.manual_seed(0)
    d, K = 8, 3
    e_plan = torch.zeros(d)
    e_plan[0] = 1.0
    e_topic = torch.zeros(d)
    e_topic[1] = 1.0
    v = torch.zeros(d)
    v[7] = 1.0

    def state(plan: float, topic: float) -> torch.Tensor:
        return plan * e_plan + topic * e_topic

    bag = torch.stack(
        [
            state(-1.0, 1.0),
            state(1.0, 1.0),
            state(-1.0, -1.0),
            state(1.0, -1.0),
        ]
    )
    labels_plan = torch.tensor([0.0, 1.0, 0.0, 1.0])
    labels_topic = torch.tensor([1.0, 1.0, 0.0, 0.0])

    F_zero = torch.zeros(d, d)
    torch.manual_seed(1)
    F_rand = 0.2 * torch.randn(d, d)
    torch.manual_seed(2)
    F_det = 0.15 * torch.randn(d, d)
    F_iso = -0.5 * torch.eye(d)
    F_mix = -0.5 * torch.eye(d)
    F_mix[0, 4:] = 0.35

    sensors = [
        ("static", F_zero, 0.0),
        ("random_F", F_rand, 0.0),
        ("det_residual", F_det, 0.0),
        ("contractive_iso", F_iso, 0.0),
        ("contractive_mix", F_mix, 0.0),
        ("contractive_mix_noise", F_mix, 0.05),
    ]

    print("=== Four-state T^K. v held out of F fit. ===")
    print("sensor plan_gap topic_on_r evasion_vis")
    for name, F, sigma in sensors:
        torch.manual_seed(3)
        hK = apply_T(bag, F, K, sigma)
        hK_ev = apply_T(bag + v, F, K, sigma)
        p, t, e = metrics(hK, hK_ev, labels_plan, labels_topic)
        print(f"{name} {p:.4f} {t:.4f} {e:.4f}")
    print("Pass only if plan stays large, topic stays ~0, evasion_vis rises vs static.")
    print("Isotropic contraction is expected to shrink plan and keep evasion_vis=0.")
    print("Not Qwen. F was not trained on this v.")


if __name__ == "__main__":
    main()
