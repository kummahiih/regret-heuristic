#!/usr/bin/env python3
"""CPU toy: cheap door is loud, quiet door costs extra.

Numeric twin of Lean sjoint_unhit_one_round / ssafe_hit_by_quiet.
Dummy vectors only. z is not an input. Not an LLM. Not p(lie).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def hinge(h: torch.Tensor, bank: torch.Tensor, tau: float = 0.0) -> float:
    h_n = F.normalize(h, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    s_star = (h_n @ p_n.T).max().item()
    return float(max(s_star - tau, 0.0))


def both_nonpos(u: tuple[float, float]) -> bool:
    return u[0] <= 0.0 and u[1] <= 0.0


def main() -> None:
    torch.manual_seed(0)
    # Same geometry as Lean silentHinge / loudHinge on Real.
    walk = torch.tensor([1.0])
    bank_quiet = torch.tensor([[-1.0]])
    bank_loud = torch.tensor([[1.0]])
    tau = 0.0

    # a=0 quiet costly; a=1 loud cheap.
    task = {0: 1.0, 1: 0.0}
    L_reg = {
        0: hinge(walk, bank_quiet, tau=tau),
        1: hinge(walk, bank_loud, tau=tau),
    }
    min_all = min(task.values())
    min_quiet = task[0]

    u_joint = {a: (task[a] - min_all, L_reg[a]) for a in (0, 1)}
    u_safe_quiet = (task[0] - min_quiet, L_reg[0])

    print("=== Two-door toy. Not simulation.py. Not an LLM. ===")
    print(f"tau={tau}  walk={walk.tolist()}  D_quiet={bank_quiet.tolist()}  D_loud={bank_loud.tolist()}")
    print(f"task[0]={task[0]:.4f}  task[1]={task[1]:.4f}")
    print(f"L_reg[0]={L_reg[0]:.4f}  L_reg[1]={L_reg[1]:.4f}")
    print(f"u_joint[0]={u_joint[0]}  both<=0={both_nonpos(u_joint[0])}")
    print(f"u_joint[1]={u_joint[1]}  both<=0={both_nonpos(u_joint[1])}")
    print(f"u_safe play 0={u_safe_quiet}  both<=0={both_nonpos(u_safe_quiet)}")
    print("One-round S_joint empty. S_safe hittable by the quiet door.")
    print("z is not in L_total. This is NOT evidence of alignment.")
    if both_nonpos(u_joint[0]) or both_nonpos(u_joint[1]):
        raise SystemExit("u_joint unexpectedly hittable")
    if not both_nonpos(u_safe_quiet):
        raise SystemExit("u_safe quiet miss")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
