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

## S_safe

**Verdict: do (math note).**

Forceability of $S_{\mathrm{safe}}$ is already stated as a Blackwell condition in `approachability.md`. A short note can make the axioms explicit and stop there.

- Axioms on $r$ and $\mathcal{D}$: $A_{\mathrm{safe}}(t)$ nonempty every $t$ (exists $a$ with $\mathcal{L}_{\mathrm{reg}}(r(h_t),\mathcal{D})=0$), and the safe comparator is stable under the readout (no systematic gaming that splits "looks safe" from "is the safe minimizer").
- Under those, every supporting halfspace of $S_{\mathrm{safe}}$ is forceable by playing a suitable mixed action inside $A_{\mathrm{safe}}$; Blackwell (black-box) then yields approachability.
- Lean: skip. No approachability / halfspace formalization, no vector-payoff structures beyond the definitional hinge and external regret. Out of the current slice.
- 2-action bandit: possible as an explicit check (enumerate pure strategies, verify halfspaces), but not required for the feasibility claim; the math note already scopes the target.

Risk: the axioms are open problems on $r$ and $\mathcal{D}$ (same as the essay). The note records the condition; it does not construct $r$.

Effort: low (one paragraph + pointer to existing forceability display).

## S_joint-toy

**Verdict: skip.**

Existing `ppo_toy.py` and `simulation.py` do not track the vector average of $S_{\mathrm{joint}}$. A new 2-action script is not needed.

- When the profitable action sits in $\mathcal{D}$, some supporting halfspace of $S_{\mathrm{joint}}$ is not forceable (see `approachability.md`). Blackwell already settles non-approachability; no empirical demo required.
- Toys only attach scalar $\lambda L_{\mathrm{reg}}$; they never accumulate $(\bar u^{\mathrm{ext}}, \bar u^{\mathrm{reg}})$ or test distance to $S_{\mathrm{joint}}$.
- Adding a script would expand the repo past the feasibility-note goal and still would not prove anything beyond the halfspace argument already written.

Risk: a toy that “looks like” failure can be misread as evidence; the theoretical rejection is cleaner.

Effort: low for a script, but out of scope. Skip.
