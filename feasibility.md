# Feasibility notes

Short verdicts on neighbouring theory around the hinge. No new theorems claimed.

## Non-implication

**Verdict: do.**

The claim is behavioral, not a namespace trick. On one play and one loss sequence, the hinge can be identically zero while external regret stays linear.

- Pick losses with a unique best fixed action $a^\star$ and a strictly worse constant play $a_t\equiv a_{\mathrm{bad}}$. Then $R_T^{\mathrm{ext}}/T$ is bounded away from $0$.
- Independently, pick a readout with $\max_k\cos(r(h_t),d_k)\le\tau$ on every $t$ of that same trajectory (orthogonal $r$, or $h_t$ off $\mathrm{span}(\mathcal{D})$). Then $\mathcal{L}_{\mathrm{reg}}=0$ at every step (`regretHinge_eq_zero_of_le`).
- Lean already has the two projections. Instantiating them on shared $T$ and a shared play is the example; keeping `IntentHingeData` and `ExternalRegretData` as separate structures is bookkeeping, not the argument.

Risk: writing only two unrelated records looks like type-disjointness. The note is the shared-trajectory version.

Effort: trivial once the play and the readout are named on the same $T$.

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

Forceability of $S_{\mathrm{safe}}$ is already stated as a Blackwell condition in `approachability.md`. $A_{\mathrm{safe}}(t)\neq\emptyset$ is **controllability**, not a property of the ReLU.

- $A_{\mathrm{safe}}(t)\neq\emptyset$ means: at that $t$ there exists a mixed action whose readout satisfies $\mathcal{L}_{\mathrm{reg}}=0$. An adversary that supplies $x$ (or a context) such that every viable completion has $\max_k\cos(r(h),d_k)>\tau$ empties the set. Conversational traps and prompt injection are exactly that saturation.
- Second axiom: the safe comparator is stable under the readout (no systematic gaming that splits "looks safe" from "is the safe minimizer").
- Under those, every supporting halfspace of $S_{\mathrm{safe}}$ is forceable by playing inside $A_{\mathrm{safe}}$; Blackwell then yields approachability.
- Lean: skip. No approachability formalization in the current slice.

Risk: the axioms are open problems on $r$, $\mathcal{D}$, and the environment. The note records the condition; it does not prove the set is always nonempty.

Effort: low (this paragraph).

## S_joint-toy

**Verdict: skip.**

Existing `ppo_toy.py` and `simulation.py` do not track the vector average of $S_{\mathrm{joint}}$. A new 2-action script is not needed.

- When the profitable action sits in $\mathcal{D}$, some supporting halfspace of $S_{\mathrm{joint}}$ is not forceable (see `approachability.md`). Blackwell already settles non-approachability; no empirical demo required.
- Toys only attach scalar $\lambda L_{\mathrm{reg}}$; they never accumulate $(\bar u^{\mathrm{ext}}, \bar u^{\mathrm{reg}})$ or test distance to $S_{\mathrm{joint}}$.
- Adding a script would expand the repo past the feasibility-note goal and still would not prove anything beyond the halfspace argument already written.

Risk: a toy that “looks like” failure can be misread as evidence; the theoretical rejection is cleaner.

Effort: low for a script, but out of scope. Skip.

## MW-oracle

**Verdict: reject (no cheap pre-image oracle).**

On unit vectors, $\mathrm{ReLU}(\max_k\cos-\tau)$ lives in $[0,1-\tau]$. Width is not the blocker.

- MW needs a separation / projection oracle for the constraint $\mathcal{L}_{\mathrm{reg}}\le 0$, i.e. for $\{h:\max_k\cos(r(h),d_k)\le\tau\}$ or its pre-image in $x$ or in network weights.
- $r\circ h$ is a deep map. That set is not a convex body with a known projection. There is no closed-form or cheap separation oracle for the pre-image.
- Uncontrolled *norm* (if someone drops normalization) would also break cosine-as-bounded, but the formulation already uses cosine on the readout. Do not reject MW on a fictitious unbounded hinge.
- Existing files treat $L_{\mathrm{reg}}$ as a scalar Lagrangian term or as a vector-payoff coordinate. They do not supply an MW update or an oracle.

Risk: citing width $[0,1]$ imports a guarantee the constraint set does not support.

Effort: this correction only. Inventing the oracle is out of scope.

## two-hinges

**Verdict: do (already separate; lead with non-isometry).**

Hinge-on-logits and hinge-on-$r(h)$ are two maps. Even when dimensions match they disagree.

- $\mathcal{L}_{\mathrm{reg}}$ is defined on $h_{\mathrm{int}}=r(h(x))\in\mathbb{R}^{d}$ versus $\mathcal{D}\subset\mathbb{R}^{d}$. A classification or unembedding head $W$ is not an isometry: $\cos(Wh,Wd)\neq\cos(h,d)$ in general. Zero hinge in latent space is not zero hinge on logits, and the converse fails too.
- Dimension mismatch ($h\in\mathbb{R}^{8}$, logits $\in\mathbb{R}^{2}$ in `simulation.py`) is the cheap special case of the same fact.
- Projecting $\mathcal{D}$ through $W$ does not unify the maps; it defines a third hinge.
- Lean: `IntentHingeData` is indexed by one space $E$. A second call with a different embedding would name the logits hinge. No extra lemmas required for the separation claim.

Risk: a projection-matrix story that “the two hinges are the same up to $W$.” They are not.

Effort: none beyond this wording.

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
