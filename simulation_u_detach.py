#!/usr/bin/env python3
"""CPU toy: u is not trained by the hinge; tau is capped.

If tau = tau0 + u with no cap, large u silences every cosine.
Detached u is a constant here. z is not an input.
"""

from __future__ import annotations


def hinge(s: float, tau: float) -> float:
    return max(s - tau, 0.0)


def main() -> None:
    s_loud = 0.9
    tau0 = 0.2
    tau_cap = 0.8
    u_mush = 5.0
    tau_uncapped = tau0 + u_mush
    tau_capped = min(tau0 + u_mush, tau_cap)
    print("=== u detach / tau cap. Not an LLM. ===")
    print(f"s_loud={s_loud} tau0={tau0} u={u_mush} tau_cap={tau_cap}")
    print(f"hinge uncapped tau={tau_uncapped:.2f} L={hinge(s_loud, tau_uncapped):.4f}")
    print(f"hinge capped   tau={tau_capped:.2f} L={hinge(s_loud, tau_capped):.4f}")
    if hinge(s_loud, tau_uncapped) != 0.0:
        raise SystemExit("expected uncapped mush to silence")
    if hinge(s_loud, tau_capped) <= 0.0:
        raise SystemExit("expected cap to keep the slap")
    print("u is a constant in this toy. No dL/du. Script finished successfully.")


if __name__ == "__main__":
    main()
