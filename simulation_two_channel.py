#!/usr/bin/env python3
"""CPU toy: trained hinge can go quiet while frozen-I stays loud.

Numeric twin of Lean trained_silent_frozenI_loud.
Frozen channel is logged only. Not added to L_total.
Dummy vectors. z is not an input. Not an LLM. Not p(lie).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def hinge(h: torch.Tensor, bank: torch.Tensor, tau: float = 0.0) -> torch.Tensor:
    h_n = F.normalize(h, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    s_star = (h_n @ p_n.T).max(dim=-1).values
    return F.relu(s_star - tau).mean()


def main() -> None:
    torch.manual_seed(0)
    d = 2
    bank = torch.tensor([[1.0, 0.0]])
    walk = torch.tensor([[1.0, 0.0]])
    tau = 0.0
    lambda_reg = 1.0

    frozen = nn.Identity()
    trained = nn.Linear(d, d, bias=False)
    with torch.no_grad():
        trained.weight.copy_(torch.eye(d))

    def channels():
        h_tr = trained(walk)
        h_fr = frozen(walk)
        L_tr = hinge(h_tr, bank, tau=tau)
        L_fr = hinge(h_fr, bank, tau=tau)
        L_task = torch.zeros(())
        L_total = L_task + lambda_reg * L_tr
        return L_tr, L_fr, L_total

    L_tr0, L_fr0, L_tot0 = channels()
    opt = torch.optim.SGD(trained.parameters(), lr=1.0)
    for _ in range(8):
        opt.zero_grad(set_to_none=True)
        L_tr, L_fr, L_tot = channels()
        L_tot.backward()
        opt.step()
    L_tr1, L_fr1, L_tot1 = channels()

    print("=== Two-channel toy. Not simulation.py. Not an LLM. ===")
    print(f"walk={walk.tolist()}  D={bank.tolist()}  tau={tau}")
    print(f"before  trained={L_tr0.item():.4f}  frozen-I={L_fr0.item():.4f}  L_total={L_tot0.item():.4f}")
    print(f"after   trained={L_tr1.item():.4f}  frozen-I={L_fr1.item():.4f}  L_total={L_tot1.item():.4f}")
    print("L_total uses trained hinge only. Frozen-I is a log, not a third term.")
    print("z is not in L_total. This is NOT evidence of alignment.")
    if L_fr1.item() <= 0.0:
        raise SystemExit("frozen-I went quiet; channel is not a witness")
    if abs(L_fr1.item() - L_fr0.item()) > 1e-6:
        raise SystemExit("frozen-I moved; it must stay out of the graph")
    if L_tr1.item() >= L_tr0.item() - 1e-6:
        raise SystemExit("trained hinge did not drop")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
