#!/usr/bin/env python3
"""CPU toy: when you look changes the score.

Numeric twin of Lean two_route_identity / totalLoss_ignores_amp.
Routes 1 and -1. Square-then-add vs add-then-square.
Amp is a sticky note. It is not an input to L_total.
Dummy scalars. Not an LLM. Not a quantum circuit. Not p(lie).
"""

from __future__ import annotations

import cmath


def premature_born(routes: tuple[complex, ...]) -> float:
    return float(sum(abs(a) ** 2 for a in routes))


def delayed_born(routes: tuple[complex, ...]) -> float:
    return float(abs(sum(routes)) ** 2)


def total_loss(task: float, regret: float, lam: float = 1.0) -> float:
    return task + lam * regret


def main() -> None:
    routes = (1 + 0j, -1 + 0j)
    prem = premature_born(routes)
    delay = delayed_born(routes)
    L_task = 0.0
    L_reg = 1.0
    L0 = total_loss(L_task, L_reg)
    amp_note = {"room_A": 1 + 0j, "room_B": -1 + 0j}
    L_with_note = total_loss(L_task, L_reg)  # amp_note is not an argument

    print("=== Born bookkeeping toy. Not simulation.py. Not an LLM. ===")
    print(f"routes={routes}")
    print(f"premature square-then-add={prem:.4f}")
    print(f"delayed add-then-square={delay:.4f}")
    print(f"L_total without Amp={L0:.4f}")
    print(f"L_total with unused Amp note={L_with_note:.4f}  note={amp_note}")
    print("Same hallway. Different time of looking.")
    print("z is not in L_total. This is NOT evidence of alignment.")
    if prem != 2.0:
        raise SystemExit(f"premature expected 2, got {prem}")
    if delay != 0.0:
        raise SystemExit(f"delayed expected 0, got {delay}")
    if L0 != L_with_note:
        raise SystemExit("pairing Amp changed L_total")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
