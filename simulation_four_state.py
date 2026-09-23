#!/usr/bin/env python3
"""Four-state dummy: plan vs topic vs static-kernel evasion.

honest/deceptive x topic A/B.
Static r = first coordinate (plan).
v lives in the kernel of r: r(h+v)=r(h).
Not Qwen. Not a basin. F is added in t2.
"""

from __future__ import annotations

import torch


def static_r(h: torch.Tensor) -> torch.Tensor:
    return h[..., :1]


def gap(scores_dec: torch.Tensor, scores_hon: torch.Tensor) -> float:
    return float(scores_dec.mean() - scores_hon.mean())


def main() -> None:
    torch.manual_seed(0)
    d = 8
    e_plan = torch.zeros(d)
    e_plan[0] = 1.0
    e_topic = torch.zeros(d)
    e_topic[1] = 1.0
    v = torch.zeros(d)
    v[7] = 1.0

    def state(plan: float, topic: float) -> torch.Tensor:
        return plan * e_plan + topic * e_topic

    hon_a = state(-1.0, 1.0)
    dec_a = state(1.0, 1.0)
    hon_b = state(-1.0, -1.0)
    dec_b = state(1.0, -1.0)
    bag = torch.stack([hon_a, dec_a, hon_b, dec_b])
    labels_plan = torch.tensor([0.0, 1.0, 0.0, 1.0])
    labels_topic = torch.tensor([1.0, 1.0, 0.0, 0.0])

    r = static_r(bag).squeeze(-1)
    r_ev = static_r(bag + v).squeeze(-1)
    plan_gap = gap(r[labels_plan > 0.5], r[labels_plan < 0.5])
    topic_on_r = gap(r[labels_topic > 0.5], r[labels_topic < 0.5])
    evasion_vis = float((r_ev - r).abs().mean())

    print("=== Four-state static r. Held-out v in ker r. ===")
    print(f"plan_gap={plan_gap:.4f} topic_on_r={topic_on_r:.4f} evasion_vis={evasion_vis:.4f}")
    print(f"r(h)={ [round(float(x), 3) for x in r] }")
    print(f"r(h+v)={ [round(float(x), 3) for x in r_ev] }")
    print("Want: plan_gap>0, topic_on_r=0, evasion_vis=0.")
    print("Not Qwen. T^K comes next. Do not train F on v.")
    if abs(plan_gap - 2.0) > 1e-5:
        raise SystemExit("plan_gap expected 2")
    if abs(topic_on_r) > 1e-5:
        raise SystemExit("static r leaked topic")
    if evasion_vis > 1e-5:
        raise SystemExit("static r saw v")
    print("Static baseline ok.")


if __name__ == "__main__":
    main()
