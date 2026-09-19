#!/usr/bin/env python3
"""CPU toy: topic wallpaper is not the slap.

Numeric twin of Lean factoredHinge_ignores_topic.
Dummy vectors only. z is not an input. Not an LLM. Not p(lie).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def hinge_on_strat(strat: torch.Tensor, bank: torch.Tensor, tau: float = 0.0) -> float:
    h_n = F.normalize(strat, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    s_star = (h_n @ p_n.T).max().item()
    return float(max(s_star - tau, 0.0))


def main() -> None:
    torch.manual_seed(0)
    strat = torch.tensor([1.0, 0.0])
    topic = torch.tensor([0.2, 0.8])
    topic_rewritten = torch.tensor([-0.9, 0.1])
    bank = torch.tensor([[1.0, 0.0]])
    tau = 0.0

    L_before = hinge_on_strat(strat, bank, tau=tau)
    L_after = hinge_on_strat(strat, bank, tau=tau)
    # Packed identity would mix topic into the same vector. We refuse that.
    packed_before = F.normalize(torch.cat([topic, strat]), dim=0)
    packed_after = F.normalize(torch.cat([topic_rewritten, strat]), dim=0)
    packed_change = float((packed_before - packed_after).norm())

    print("=== Factored readout toy. Not simulation.py. Not an LLM. ===")
    print(f"strat={strat.tolist()}  topic={topic.tolist()}  topic'={topic_rewritten.tolist()}")
    print(f"L_reg on strat before topic rewrite={L_before:.4f}")
    print(f"L_reg on strat after topic rewrite={L_after:.4f}")
    print(f"packed-vector L2 change if topic were mixed in={packed_change:.4f}")
    print("Hinge uses strat only. Rewriting topic is a no-op on L_reg.")
    print("z is not in L_total. This is NOT evidence of alignment.")
    if L_before != L_after:
        raise SystemExit("factored hinge moved with wallpaper")
    if packed_change == 0.0:
        raise SystemExit("packed control did not move; check topic rewrite")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
