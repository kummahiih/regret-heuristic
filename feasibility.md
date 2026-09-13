# Feasibility notes

Short verdicts on neighbouring theory around the hinge. No new theorems claimed.

## Non-implication

**Verdict: do.**

Objects already in `lean/RegretHeuristic.lean` suffice for a counter-example sketch.

- `IntentHingeData` and `ExternalRegretData` are independent structures.
- Choose any `IntentHingeData` with `maxCosine ≤ threshold` so `value = 0` (uses existing `regretHinge_eq_zero_of_le`).
- Choose a constant suboptimal play and a loss sequence with a strictly better fixed action; then `externalRegret / T` stays bounded away from 0 (definition of `externalRegret` and `hannanConsistent`).
- No extra Lean lemmas required beyond the existing defs and the two value projections.

Risk: the example is purely definitional; it does not live inside a single combined structure. That is intentional — the file deliberately keeps the two notions separate.

Effort: trivial (instantiate two records).

## Hedge-in-Lean

**Verdict: skip.**

This repo cannot prove a finite-T EWA/Hedge external-regret bound without new formalization and without a mathlib OCO library (none at the pinned v4.33.1).

- Existing Lean content is definitional only: `externalRegret`, `CausalStrategy`, `hannanConsistent` (asymptotic statement). No weights, no update rule, no potential.
- Missing lemmas: multiplicative-weights / exponential-weights step, log-sum-exp potential, telescoping inequality that yields the classic $O(\sqrt{T\log N})$ bound. (Deterministic potential proof; Hoeffding not required.)
- Would require a new file (e.g. `Hedge.lean`) plus substantial analysis imports; expands beyond the definitional slice goal of `RegretHeuristic.lean`.
- Risk: dependency surface grows; current lakefile only pulls mathlib for inner-product and basic finset facts.

Effort: high (small paper of formalization). Skip; keep the Lean slice definitional.
