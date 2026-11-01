#!/usr/bin/env python3
"""Paired baseline comparison.

Compares residual probe vs note-text baseline vs note+question text baseline.
Reports McNemar exact test and paired bootstrap intervals.

Not a camera. Not handoverPass. Do not fill D.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def mcnemar(a: np.ndarray, b: np.ndarray) -> dict:
    """McNemar exact test on paired binary outcomes."""
    both_right = int(((a == 1) & (b == 1)).sum())
    both_wrong = int(((a == 0) & (b == 0)).sum())
    a_only = int(((a == 1) & (b == 0)).sum())
    b_only = int(((a == 0) & (b == 1)).sum())
    n = a_only + b_only
    if n == 0:
        return {"a_only": a_only, "b_only": b_only, "p": 1.0}
    # binomial test, two-sided
    k = min(a_only, b_only)
    p = 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return {"a_only": a_only, "b_only": b_only, "p": min(1.0, p)}


def paired_bootstrap(a: np.ndarray, b: np.ndarray, n_boot: int = 1000, seed: int = 0) -> dict:
    """Paired bootstrap CI for accuracy difference."""
    rng = np.random.default_rng(seed)
    diff = a.astype(float) - b.astype(float)
    means = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(n_boot)]
    lo, hi = np.percentile(means, [2.5, 97.5])
    return {"diff": round(diff.mean(), 3), "lo": round(lo, 3), "hi": round(hi, 3)}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--probe", required=True, help="npy of probe predictions (0/1)")
    p.add_argument("--note", required=True, help="npy of note-text baseline predictions")
    p.add_argument("--both", required=True, help="npy of note+question text baseline predictions")
    p.add_argument("--labels", required=True, help="npy of true labels")
    args = p.parse_args()

    probe = np.load(args.probe)
    note = np.load(args.note)
    both = np.load(args.both)
    labels = np.load(args.labels)

    probe_ok = (probe == labels).astype(int)
    note_ok = (note == labels).astype(int)
    both_ok = (both == labels).astype(int)

    print("probe vs note:", mcnemar(probe_ok, note_ok))
    print("probe vs both:", mcnemar(probe_ok, both_ok))
    print("probe-note diff:", paired_bootstrap(probe_ok, note_ok))
    print("probe-both diff:", paired_bootstrap(probe_ok, both_ok))
    print("not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
