#!/usr/bin/env python3
"""CPU toy: say which I is frozen. Do not fill D from the current walk.

Three names: readout weights, backbone, cached h.
Disagreeing channels are an alarm. Not a third loss. Not an LLM.
"""

from __future__ import annotations

KINDS = ("readout", "backbone", "cached_h")


def main() -> None:
    D = (1.0,)
    trained = {"readout": 0.2, "backbone": 0.2, "cached_h": 0.2}
    frozen = {"readout": 0.8, "backbone": 0.8, "cached_h": 0.8}
    print("=== Frozen lineage names. Not an LLM. ===")
    print(f"D={D}  kinds={list(KINDS)}")
    print("trained hinge vs frozen hinge (same walk):")
    alarm = False
    for k in KINDS:
        print(f"  {k}: trained={trained[k]:.2f} frozen={frozen[k]:.2f}")
        if abs(trained[k] - frozen[k]) > 0.1:
            alarm = True
    print(f"alarm={alarm}  (investigate; not a gaming verdict)")
    print("D stays frozen. Current walk does not append to D.")
    if not alarm:
        raise SystemExit("expected trained/frozen disagreement in this toy")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
