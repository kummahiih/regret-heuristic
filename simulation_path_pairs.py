#!/usr/bin/env python3
"""Same last token and topic coord, different strategy coord.

Dummy paths. Not Qwen. Shows last-token r can match while path r does not.
reply_kind scores the print against fact. Not in L.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F

from simulation_reply_kind import agree_assigned, reply_kind


def hinge(r: torch.Tensor, bank: torch.Tensor, tau: float) -> float:
    r_n = F.normalize(r, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return float(F.relu((r_n @ p_n.T).max() - tau))


def main() -> None:
    torch.manual_seed(0)
    tau = 0.2
    topic = F.normalize(torch.tensor([1.0, 0.0, 0.0, 0.0]), dim=0)
    answer = F.normalize(torch.tensor([1.0, 0.1, 0.0, 0.0]), dim=0)
    plan_a = F.normalize(torch.tensor([0.0, 0.0, 1.0, 0.0]), dim=0)
    plan_b = F.normalize(torch.tensor([0.0, 0.0, 0.0, 1.0]), dim=0)
    bank = plan_b.unsqueeze(0)

    def path(plan: torch.Tensor) -> torch.Tensor:
        mid = F.normalize(0.7 * topic + 0.3 * plan, dim=0)
        return torch.stack([mid, mid, answer])

    A, B = path(plan_a), path(plan_b)
    last_A, last_B = A[-1], B[-1]
    mean_A, mean_B = A.mean(0), B.mean(0)

    fact = "the hotel is not booked"
    print_A = "the hotel is not booked"
    print_B = "the hotel is not booked"
    kind_A = reply_kind(print_A, fact)
    kind_B = reply_kind(print_B, fact)

    print("=== Same answer, different strategy. Dummy path. ===")
    print(f"last-token L2={float((last_A - last_B).norm()):.4f} (same printed cell)")
    print(f"mean-pool  L2={float((mean_A - mean_B).norm()):.4f}")
    print(f"path-mean  hinge A={hinge(mean_A, bank, tau):.4f} B={hinge(mean_B, bank, tau):.4f}")
    print(f"last-token hinge A={hinge(last_A, bank, tau):.4f} B={hinge(last_B, bank, tau):.4f}")
    print(
        f"reply_kind A={kind_A} assigned=honest agree={agree_assigned(kind_A, 'honest')}"
    )
    print(
        f"reply_kind B={kind_B} assigned=deceptive agree={agree_assigned(kind_B, 'deceptive')}"
    )
    print("Last-token hinge matches because the answer matches.")
    print("Path mean can differ because mid steps carry plan. Constructed. Not a camera.")
    print("Same print can be truth on both tags. reply_kind is not in L.")


if __name__ == "__main__":
    main()
