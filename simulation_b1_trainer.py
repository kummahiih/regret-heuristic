#!/usr/bin/env python3
"""B1 trainer cartoon: path h_1:T, loss from the walk, frozen readout.

Not an LLM. Not z. Amp is computed and discarded.
legalOfWalk: task + hinge from the path only.
Frozen I = readout weights cloned and stop-grad (kind=readout).
u is a constant; tau capped.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def legal_of_walk(task: torch.Tensor, hinge: torch.Tensor) -> torch.Tensor:
    return task + hinge


def illegal_from_amp(amp: torch.Tensor) -> torch.Tensor:
    """Named hole. Do not call this in the trainer."""
    return amp.square().sum()


def path_readout(h_path: torch.Tensor, readout: nn.Linear) -> torch.Tensor:
    # h_path: (B, T, d) -> mean over time, then linear r
    return readout(h_path.mean(dim=1))


def hinge_on(r: torch.Tensor, bank: torch.Tensor, tau: float) -> torch.Tensor:
    r_n = F.normalize(r, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    s_star = (r_n @ p_n.T).max(dim=-1).values
    return F.relu(s_star - tau).mean()


def main() -> None:
    torch.manual_seed(0)
    B, T, d, K = 4, 3, 8, 2
    tau0, u, tau_cap, lam = 0.2, 0.1, 0.8, 0.5
    tau = min(tau0 + u, tau_cap)
    encoder = nn.Linear(d, d, bias=False)
    readout = nn.Linear(d, d, bias=False)
    frozen_readout = nn.Linear(d, d, bias=False)
    frozen_readout.load_state_dict(readout.state_dict())
    for p in frozen_readout.parameters():
        p.requires_grad_(False)
    bank = torch.randn(K, d)
    bank.requires_grad_(False)
    x_path = torch.randn(B, T, d)
    y = torch.zeros(B, dtype=torch.long)
    head = nn.Linear(d, 2)
    opt = torch.optim.Adam(
        list(encoder.parameters()) + list(readout.parameters()) + list(head.parameters()),
        lr=1e-2,
    )
    # Amp exists and is ignored
    amp = torch.tensor([1.0, -1.0])
    _ = illegal_from_amp(amp)  # computed, not in graph of L

    h_path = torch.stack([encoder(x_path[:, t]) for t in range(T)], dim=1)
    r = path_readout(h_path, readout)
    r_frozen = path_readout(h_path.detach(), frozen_readout)
    L_task = F.cross_entropy(head(h_path[:, -1]), y)
    L_reg = hinge_on(r, bank, tau)
    L_frozen = hinge_on(r_frozen, bank, tau)
    L_last = hinge_on(readout(h_path[:, -1]), bank, tau)
    L_total = legal_of_walk(L_task, lam * L_reg)
    print("=== B1 trainer cartoon. Not an LLM. ===")
    print(f"path T={T} frozen_kind=readout tau={tau:.2f} (capped)")
    print(f"L_task={L_task.item():.4f} L_reg={L_reg.item():.4f} L_frozen={L_frozen.item():.4f}")
    print(f"L_last={L_last.item():.4f} L_total={L_total.item():.4f}")
    print(f"amp_normsq={illegal_from_amp(amp).item():.4f}  (logged, not in L_total)")
    opt.zero_grad(set_to_none=True)
    L_total.backward()
    g_enc = float(encoder.weight.grad.norm()) if encoder.weight.grad is not None else 0.0
    g_read = float(readout.weight.grad.norm()) if readout.weight.grad is not None else 0.0
    g_frz = frozen_readout.weight.grad
    print(f"grad encoder={g_enc:.6f} readout={g_read:.6f} frozen_readout={g_frz}")
    if g_frz is not None:
        raise SystemExit("frozen readout received a gradient")
    opt.step()
    with torch.no_grad():
        h2 = torch.stack([encoder(x_path[:, t]) for t in range(T)], dim=1)
        L_reg2 = hinge_on(path_readout(h2, readout), bank, tau)
        L_frz2 = hinge_on(path_readout(h2, frozen_readout), bank, tau)
    alarm = abs(L_reg2.item() - L_frz2.item()) > 1e-6
    print(f"after 1 step L_reg={L_reg2.item():.4f} L_frozen={L_frz2.item():.4f} alarm={alarm}")
    print("D not updated from this walk.")
    print("Script finished successfully. This is NOT evidence of alignment.")


if __name__ == "__main__":
    main()
