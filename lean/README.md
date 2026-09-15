# Lean 4 slice of the regret heuristic

A verified **glossary**, not a safety proof.

Pinned to Lean `v4.33.1` / mathlib `v4.33.1`.

```bash
cd lean
lake exe cache get
lake build
```

What is proved:

- hinge non-negativity, silence below the margin, `lambda = 0` recovers the task scalar
- Cauchy-Schwarz bounds on cosine
- `relu_wider_tau_le` / `regretHinge_wider_tau_le`: if `tau1 ≤ tau2` then the hinge at `tau2` is ≤ the hinge at `tau1` (§5: quieter, not a theorem that it hits 0)
- Fin 2 toy `silent_hinge_not_vanishing_external_regret`

What is not proved: readout validity, bank coverage, representation gaming, Hannan of the hinge, PPO trust region.
