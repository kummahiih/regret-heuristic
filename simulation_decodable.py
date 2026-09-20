#!/usr/bin/env python3
"""CPU toy: hearing the subject is not catching the scheme.

Numeric twin of Lean SensorScoreboards.decodable_not_causal.
Dummy scalars only. z is not an input. Not an LLM. Not p(lie).
"""

from __future__ import annotations


def probe_score(topic: float, plan: float) -> float:
    del plan
    return abs(topic)


def causal_score(topic: float, plan: float) -> float:
    del topic
    return abs(plan)


def main() -> None:
    wallpaper = (1.0, 0.0)
    scheme = (0.0, 1.0)

    p_w = probe_score(*wallpaper)
    c_w = causal_score(*wallpaper)
    p_s = probe_score(*scheme)
    c_s = causal_score(*scheme)

    print("=== Decodable vs causal toy. Not simulation.py. Not an LLM. ===")
    print(f"cell wallpaper topic={wallpaper[0]} plan={wallpaper[1]}")
    print(f"  probe={p_w:.4f}  causal={c_w:.4f}")
    print(f"cell scheme    topic={scheme[0]} plan={scheme[1]}")
    print(f"  probe={p_s:.4f}  causal={c_s:.4f}")
    print("Hearing taxes is not catching the scheme. Those are different meters.")
    print("z is not in L_total. This is NOT evidence of alignment.")

    if (p_w, c_w) != (1.0, 0.0):
        raise SystemExit("wallpaper cell drifted from Lean decodable_not_causal")
    if (p_s, c_s) != (0.0, 1.0):
        raise SystemExit("scheme cell drifted from Lean causal_not_from_probe")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
