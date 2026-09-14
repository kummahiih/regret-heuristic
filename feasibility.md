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

## MW-oracle

**Verdict: not without a bounded r recipe.**

$L_{\mathrm{reg}}$ cannot serve as a multiplicative-weights (MW) constraint with bounded width and a cheap oracle unless $r$ itself is already bounded in a way that keeps the hinge losses inside a known range.

- MW / Hedge needs per-round losses in a fixed interval (classically $[0,1]$) to obtain the $O(\sqrt{T\log N})$ width; the current $\mathrm{ReLU}(\max s-\tau)$ is unbounded above if cosine can approach 1 and $\tau$ is fixed, or if the readout norm is uncontrolled.
- A cheap oracle would require an efficient projection or reweight step over the constraint set defined by $L_{\mathrm{reg}}\le 0$. Without a closed-form or low-cost description of $\{h:r(h)\text{ yields hinge }0\}$, the oracle is not cheap.
- Existing files (`math_formulation.md`, `approachability.md`) treat $L_{\mathrm{reg}}$ only as a scalar Lagrangian term or as the second coordinate of a vector payoff; they supply neither a bounded-loss reduction nor an MW update rule.
- Risk: pretending the hinge is already a bounded MW expert loss would import guarantees that the algebra does not give.

Effort: low for the negative note; high (and out of scope) for inventing a bounded-$r$ construction.

## two-hinges

**Verdict: do (already separate; smallest counter-example is dimension mismatch).**

Hinge-on-logits and hinge-on-$r(h)$ are two distinct maps; the formulation and the toys already treat them as such.

- Formulation (`math_formulation.md`) defines $\mathcal{L}_{\mathrm{reg}}$ only on the readout $h_{\mathrm{int}}=r(h(x))\in\mathbb{R}^{d}$ versus bank $\mathcal{D}\subset\mathbb{R}^{d}$. Logits live in a different space (classifier head or policy logits) and are never the argument of the hinge.
- `simulation.py`: encoder produces $h\in\mathbb{R}^{8}$; task head maps to 2-class logits. Cosine hinge is computed solely on $h$; applying the same bank to logits is type-incorrect (dim 2 vs 8).
- Lean: `IntentHingeData` is indexed by a single space $E$; a second structure (or a second call with a different embedding) would be the natural way to name a logits-hinge, but none is needed for the claim. No extra lemmas.
- Smallest counter-example: any non-isometry linear head (or pure dimension mismatch). Max-cosine on the projected logits can be driven to 1 while the original readout stays below $\tau$, or vice versa. Instantiable in the existing DummyEncoder + Linear head without new code.

Risk: conflating the two in prose would re-introduce the “output regularizer” reading the essay already rejects. Keeping the maps separate is the point.

Effort: trivial (one section; no Lean or script change required).

## Standard objections

Four standard objections, named in the vocabulary already used in Caps and `approachability.md`.

- **Entanglement** = r-validity: whether the readout separates task-relevant features from those that enable gaming. No claim that r is disentangled.
- **D coverage / OOD** = bank coverage: $\mathcal{D}$ must cover the relevant directions; out-of-distribution intents fall outside the forceable set.
- **Gaming** = rotate readout: an adversary can rotate or mask $h_{\mathrm{int}}$ so that cosine to bank prototypes stays below $\tau$ while the underlying intent remains actionable.
- **tau** = hinge parameter, not a conscience: $\tau$ is a scalar threshold on the cosine hinge. On unit vectors the hinge value lives in $[0,1-\tau]$, not an unbounded 0.8 trigger.

No dynamic-$\mathcal{D}$ recipe. No new theorem.

## Second-pass objections

Against the live README (not an older extract).

- **Circularity of $r$ and $\mathcal{D}$.** Open construction, not a hidden hole. Caps already treat both as assumed; building a readout that tracks strategy and a bank that covers deception *is* the research problem. No constructor is added here.
- **Hannan not claimed.** Consistent. The hinge is not $R_T^{\mathrm{ext}}$. Lean defines both and does not prove the hinge Hannan-consistent. $S_{\mathrm{joint}}$ is rejected in `approachability.md`.
- **Toy scale.** `simulation.py` is a 146-parameter wiring check (near fires, far silent, encoder grad nonzero). It is not a test of LLM deceptive alignment and is not labelled as one.
- **Biological paragraph.** Framing in the README claim section. Not part of the algebra (`math_formulation.md`).
- **Outcomes.** The live README does not claim mitigated deception or absence of catastrophic forgetting. Conclusion: next experiment is whether $r$ and $\mathcal{D}$ can be built.

No new outcome claim. No $\mathcal{D}$ constructor.

## Non-interference

**Verdict: skip.**

A guarantee that $\mathcal{L}_{\mathrm{reg}}$ does not tax benign planning (chess, negotiation, multi-step search) would need axioms this repo does not have: linearly separated Honest / Deceptive sets, a Lipschitz $r$ that stays Lipschitz under the update, and a data distribution whose honest plans do not project into $\mathcal{D}$.

Those are constructions of $r$, not lemmas about ReLU. Writing the theorem in Lean without the maps is padding. Entanglement stays an open vulnerability, as in Caps.
