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
