#!/usr/bin/env python3
"""CPU toy: path h_1:T. Hinge on mean of the path, not only last step.

z is not an input. Last token alone is a different sensor.
"""

from __future__ import annotations


def hinge(s: float, tau: float = 0.0) -> float:
    return max(s - tau, 0.0)


def main() -> None:
    path = [0.1, 0.2, 0.9]
    last = path[-1]
    mean = sum(path) / len(path)
    print("=== B1 path cartoon. Not an LLM. ===")
    print(f"path={path} last={last:.2f} mean={mean:.2f}")
    print(f"L_reg last={hinge(last):.4f} L_reg mean={hinge(mean):.4f}")
    print("legalOfWalk takes task and hinge from the walk, not from Amp.")
    if hinge(last) <= hinge(mean):
        raise SystemExit("expected last louder than mean on this path")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
