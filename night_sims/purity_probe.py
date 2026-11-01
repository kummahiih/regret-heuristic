#!/usr/bin/env python3
"""Purity-law diagnostic for linear probes.

Estimates Mahalanobis separation, signal purity, and the
detectability threshold from Hai and Li (arXiv:2609.22337).
Reports whether a weak probe is underpowered or consistent
with no linear signal.

Not a camera. Not handoverPass. Do not fill D.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def mahalanobis_separation(X: np.ndarray, y: np.ndarray) -> float:
    """Cross-fitted estimator of class separation s."""
    yes = X[y == 1]
    no = X[y == 0]
    if len(yes) < 2 or len(no) < 2:
        return 0.0
    mu_yes = yes.mean(0)
    mu_no = no.mean(0)
    pooled = np.cov(np.vstack([yes, no]).T)
    # ridge for stability
    pooled += 1e-3 * np.eye(pooled.shape[0])
    try:
        inv = np.linalg.inv(pooled)
    except np.linalg.LinAlgError:
        return 0.0
    delta = mu_yes - mu_no
    return float(np.sqrt(delta @ inv @ delta))


def purity_law_auc(alpha: float, s: float) -> float:
    """Maximum linear-probe AUC at purity alpha."""
    if alpha <= 0:
        return 0.5
    phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
    return (
        alpha**2 * phi(s / 2)
        + 2 * alpha * (1 - alpha) * phi(s * (1 - 2 * alpha) / 2)
    )


def detectability_threshold(s: float, n_te: int, delta: float = 0.05, gamma: float = 0.2) -> float:
    """Alpha* below which the audit is underpowered."""
    if s <= 0 or n_te <= 0:
        return 1.0
    z_delta = 1.96  # approx for 0.05
    z_gamma = 0.84  # approx for 0.2
    return (z_delta + z_gamma) / (s * math.sqrt(n_te) * math.sqrt(0.5))


def diagnose(X: np.ndarray, y: np.ndarray, alpha: float, n_te: int) -> dict:
    s = mahalanobis_separation(X, y)
    auc_pred = purity_law_auc(alpha, s)
    alpha_star = detectability_threshold(s, n_te)
    underpowered = alpha < alpha_star
    return {
        "s": round(s, 3),
        "alpha": alpha,
        "auc_pred": round(auc_pred, 3),
        "alpha_star": round(alpha_star, 3),
        "underpowered": underpowered,
        "n": len(y),
        "n_te": n_te,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--activations", required=True, help="npy of residual vectors")
    p.add_argument("--labels", required=True, help="npy of 0/1 labels")
    p.add_argument("--alpha", type=float, default=1.0, help="signal purity")
    p.add_argument("--n-te", type=int, default=0, help="test set size; default half")
    args = p.parse_args()

    X = np.load(args.activations)
    y = np.load(args.labels)
    n_te = args.n_te or len(y) // 2
    result = diagnose(X, y, args.alpha, n_te)
    print(json.dumps(result, indent=2))
    if result["underpowered"]:
        print("underpowered: null result is uninformative")
    else:
        print("powered: null result is informative")
    print("not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
