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
- `relu_wider_tau_le` / `regretHinge_wider_tau_le`
- Fin 2 toy `silent_hinge_not_vanishing_external_regret`
- `insertion_two_regret_not_the_hinge`: Potvin-style second-minus-best can be 3 while the cosine hinge is 0
- `hingeQuietIgnoringAction_all_or_none`: if `r` ignores `a`, the safe set is all of `A` or none

What is not proved: readout validity, bank coverage, representation gaming, Hannan of the hinge, PPO trust region, Blackwell, ALNS.
