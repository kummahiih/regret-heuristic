#!/usr/bin/env python3
"""CPU toy: a head-write camera ignores the rest of the hallway.

Numeric twin of Lean SensorScoreboards.headWrite_ignores_rest.
Dummy scalars only. Not a real attention head. Not an LLM. z is not an input.
"""

from __future__ import annotations


def head_write(head: float, rest: float) -> float:
    del rest
    return head


def packed_norm(head: float, rest: float) -> float:
    return (head * head + rest * rest) ** 0.5


def main() -> None:
    head = 0.0
    rest_a = 1.0
    rest_b = -1.0

    r_a = head_write(head, rest_a)
    r_b = head_write(head, rest_b)
    n_a = packed_norm(head, rest_a)
    n_b = packed_norm(head, rest_b)

    print("=== Head-write toy. Not simulation.py. Not an LLM. ===")
    print(f"head={head}  rest={rest_a} -> r={r_a:.4f}  packed_norm={n_a:.4f}")
    print(f"head={head}  rest={rest_b} -> r={r_b:.4f}  packed_norm={n_b:.4f}")
    print("r stays. The packed hallway moves. This is not a found camera.")
    print("z is not in L_total. This is NOT evidence of alignment.")

    if r_a != r_b:
        raise SystemExit("head-write r moved when only rest flipped")
    if r_a != 0.0:
        raise SystemExit("head-write drifted from Lean head_write_not_the_hallway")
    if n_a == 0.0 or n_b == 0.0:
        raise SystemExit("packed control collapsed")
    if n_a != n_b:
        raise SystemExit("packed norms should match on ±rest")
    print("Script finished successfully.")


if __name__ == "__main__":
    main()
