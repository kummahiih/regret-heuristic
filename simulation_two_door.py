#!/usr/bin/env python3
"""CPU toy: cheap door is loud, quiet door costs extra.

One frozen bank D={1}. Action-conditioned r: r(a0)=-1 quiet, r(a1)=1 loud.
Numeric twin of Lean sjoint_unhit_one_round / ssafe_hit_by_quiet.
Dummy vectors only. z is not an input. Not an LLM. Not p(lie).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def hinge(r: torch.Tensor, bank: torch.Tensor, tau: float = 0.0) -> float:
    r_n = F.normalize(r, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    s_star = (r_n @ p_n.T).max().item()
    return float(max(s_star - tau, 0.0))


def both_nonpos(u: tuple[float, float]) -> bool:
    return u[0] <= 0.0 and u[1] <= 0.0


def main() -> None:
    torch.manual_seed(0)
    D = torch.tensor([[1.0]])
    r = {0: torch.tensor([-1.0]), 1: torch.tensor([1.0])}
    tau = 0.0
    task = {0: 1.0, 1: 0.0}
    L_reg = {a: hinge(r[a], D, tau=tau) for a in (0, 1)}
    min_all = min(task.values())
    min_quiet = task[0]

    u_joint = {a: (task[a] - min_all, L_reg[a]) for a in (0, 1)}
    u_safe_quiet = (task[0] - min_quiet, L_reg[0])

    print("=== Two-door toy. One bank. r sees the door. Not an LLM. ===")
    print(f"tau={tau}  D={D.tolist()}  r[0]={r[0].tolist()}  r[1]={r[1].tolist()}")
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
    if abs(L_reg[0] - 0.0) > 1e-6 or abs(L_reg[1] - 1.0) > 1e-6:
        raise SystemExit("expected L_reg 0 and 1")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
