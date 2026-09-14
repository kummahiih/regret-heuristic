# Lean 4 slice of the regret heuristic

A verified **glossary**, not a safety proof.

The file checks hinge algebra and the definition of causal external regret.
It does not prove that `r` means deception, that SGD converges to an honest
policy, or that a policy stays below a deceptive-probability bound.
Those are semantic and dynamical claims Lean is not being asked to settle.
See `feasibility.md`.

Definitional formalization of `math_formulation.md` and the *separation*
in `regret_minimization.md`. Not a proof that the hinge is Hannan-consistent
(it is not) and not a PPO correctness proof.

Pinned to Lean `v4.33.1` / mathlib `v4.33.1`.

```bash
cd lean
lake exe cache get
lake build
```

Hannan consistency is stated only for a **causal** strategy:
`a_t` is a function of `ell_0, ..., ell_{t-1}`. A map that sees the whole
loss table is not a strategy here.

What is proved: hinge non-negativity, silence below the margin, `lambda = 0`
recovers the task scalar, Cauchy-Schwarz bounds on cosine.
What is not proved: readout validity, bank coverage, representation gaming,
Hannan consistency of the hinge, or any trust-region theorem after adding
the hinge.
