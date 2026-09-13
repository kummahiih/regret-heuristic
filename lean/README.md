# Lean 4 slice of the regret heuristic

Definitional formalization of `math_formulation.md` and the *separation*
in `regret_minimization.md`. Not a proof that the hinge is Hannan-consistent
(it is not) and not a PPO correctness proof.

Pinned to Lean `v4.33.1` / mathlib `v4.33.1`.

```bash
cd lean
lake exe cache get
lake build
```

What is proved: hinge non-negativity, silence below the margin, `λ = 0`
recovers the task scalar, Cauchy–Schwarz bounds on cosine, and that
external regret is a cumulative comparator gap (defined on a different type).
What is not proved: readout validity, bank coverage, representation gaming,
or any trust-region theorem after adding the hinge.
