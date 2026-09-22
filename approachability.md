# Approachability and the only target this essay can claim

Plain language first. Formal target second. Blackwell's theorem is cited, not re-proved.

## For a reader who does not want the jargon

You keep two scores every day:

1. How expensive your *move* was, compared with some benchmark.
2. Whether your *insides* looked like a banned plan (the hinge).

You want the long-run average of both scores to sit in a safe box — cheap enough, and not banned.

Blackwell's question is only this: **does there exist a way of choosing moves, using only the past, that forces those averages into the box no matter what the world does?**

If the cheap moves *are* the banned plans, the box "be cheap *and* look clean" cannot be forced. That is not a bug in the proof. That is the interesting case of the essay: deception pays.

The box the essay is allowed to aim at is therefore smaller:

> Look clean on the hinge, and be about as cheap as the best move *among those that also look clean*.

Not: beat the best move in the whole world *and* look clean. That second box is often unapproachable.

## Blackwell (not a hallucination)

Source: David Blackwell, *An analog of the minimax theorem for vector payoffs*, Pacific Journal of Mathematics **6** (1956), no. 1, 1–8.

Each round, player I picks from a compact set $X$, player II from $Y$, and the payoff is a vector $u(x,y)\in\mathbb{R}^{d}$. Write $\bar u_T=\frac{1}{T}\sum_{t=1}^{T} u(x_t,y_t)$. A closed convex set $S\subset\mathbb{R}^{d}$ is **approachable** if player I has a causal strategy such that $\mathrm{dist}(\bar u_T,S)\to 0$ against every sequence of II.

A halfspace $H\supset S$ is **forceable** if some $x^{*}\in X$ satisfies $u(x^{*},y)\in H$ for all $y\in Y$.

**Theorem (Blackwell 1956, convex case).**  
$S$ closed and convex is approachable if and only if every halfspace containing $S$ is forceable.

This note uses that statement as a black box. It does not prove Blackwell.

## Vector payoff for this repo

Use the hinge of [math_formulation.md](math_formulation.md), frozen $\mathcal{D}$. Let $\ell_t$ be a per-round task cost of the played action $a_t$.

The readout must see the **candidate action**, or $A_{\mathrm{safe}}$ is empty or the whole of $A$:

```math
A_{\mathrm{safe}}(t)
=
\{a\in A:\ \mathcal{L}_{\mathrm{reg}}(r(h_t(a)),\mathcal{D})=0\}.
```

$h_t(a)$ is the trace (or action-conditioned hidden) after committing to $a$. If $r$ only sees a pre-action $h_t$, this set does not depend on $a$ and is not a comparator class.

If $A_{\mathrm{safe}}(t)$ is empty, the hinge is not a usable constraint that round; the target below is not defined for that $t$. Controllability: an adversarial input can empty the set.

Two coordinates:

```math
u_t^{\mathrm{safe}}
=
\ell_t(a_t)-\min_{a\in A_{\mathrm{safe}}(t)}\ell_t(a),
\qquad
u_t^{\mathrm{reg}}
=
\mathcal{L}_{\mathrm{reg}}(r(h_t(a_t)),\mathcal{D}).
```

```math
u_t=(u_t^{\mathrm{safe}}, u_t^{\mathrm{reg}})\in\mathbb{R}^{2}.
```

$u^{\mathrm{safe}}$ is extra cost versus the **best safe action that round**. That is **not** Hannan's comparator (best *fixed* action over the whole horizon). Do not call $u^{\mathrm{safe}}$ a Hannan score. It is a stronger per-round oracle than external regret against one frozen safe action. Nonempty $A_{\mathrm{safe}}$ does **not** imply approachability: two safe actions with complementary losses can leave a learner at $1/2$ while the per-round oracle is at $0$. Approachability still needs Blackwell's halfspaces, not mere safety of the support.

## Targets

**Rejected target (not claimed):**

```math
S_{\mathrm{joint}}=(-\infty,0]\times(-\infty,0]
\quad\text{with first coordinate vs }\min_{a\in A}\ell_t(a).
```

That box is "beat every action in $A$ *this round*, and keep the hinge quiet." Even that is not Hannan (Hannan is vs one fixed action for all $t$). The name Hannan-on-$A$ is retired here so the rejected box is not confused with $R_T^{\mathrm{ext}}$. If a profitable action sits in $\mathcal{D}$, some halfspace containing $S_{\mathrm{joint}}$ is not forceable. This repo does **not** claim $S_{\mathrm{joint}}$.

**Essay target (the only one consistent with keep-the-skill, tag-the-intent):**

```math
S_{\mathrm{safe}}=(-\infty,0]\times(-\infty,0]
\quad\text{with first coordinate }u^{\mathrm{safe}}.
```

Average in $S_{\mathrm{safe}}$ means mean hinge in the dead zone, and mean extra cost vs the best hinge-quiet action that round $\to 0$. Not Hannan. Not automatic from "$A_{\mathrm{safe}}$ nonempty."

## Forceability of $S_{\mathrm{safe}}$ (condition, not a theorem we prove)

$S_{\mathrm{safe}}$ is approachable iff every $w=(w_1,w_2)$ with $w_1,w_2\ge 0$ admits a mixed $x^{*}$ such that for all world $y$,

```math
w_1\,\mathbb{E}[u^{\mathrm{safe}}]+w_2\,\mathbb{E}[u^{\mathrm{reg}}]\le 0.
```

This can fail if $A_{\mathrm{safe}}$ is empty, if $r$ ignores $a$, or if "$a$ looks safe" and "$a$ is the safe comparator" come apart.

A Lagrangian $L_{\mathrm{task}}+\lambda L_{\mathrm{reg}}$ is one halfspace weight, not a proof that $S_{\mathrm{safe}}$ is approached. Toys do not implement Blackwell steering.

## Amplitude moves in this game (extra, still not approachability)

Player I's payoff $u=(u^{\mathrm{safe}},u^{\mathrm{reg}})$ is a function of the *walk sensor* $r(h(a))$, not of an amplitude on $z$. Lean: `totalLoss_ignores_amp`.

So the hidden state has a fiber: many `Amp` values share one walk, hence share $u$. Player II can move inside that fiber without changing Player I's vector payoff. That is representation gaming stated as a game, not as a vibe.

Two cheap identities ([AmplitudeBookkeeping.lean](lean/AmplitudeBookkeeping.lean)):

- `same_premature_different_delayed`: square-then-add is blind to the cancel pair $(1,-1)$ vs $(1,1)$; add-then-square is not ($0$ vs $4$).
- `same_delayed_different_premature`: add-then-square is $0$ for both $(1,-1)$ and $(2,-2)$; square-then-add is $2$ vs $8$.

What this proves about the game:

- A premature sensor (last-token mass on cells) does not see Player II's phase move.
- Delayed bookkeeping sees phase and misses scale. It is still not $u^{\mathrm{reg}}$. $u^{\mathrm{reg}}$ sees only $r$.
- Player I cannot force a halfspace that distinguishes two amplitudes in the same walk-fiber. Forceable sets live in observation space.
- Player II *can* change $z$ without changing $u$. That is why $S_{\mathrm{safe}}$ can fail when "looks safe" and "is the safe comparator" come apart.

What this does **not** prove: approachability of $S_{\mathrm{safe}}$, a quantum advantage, or that interference detects deception.

## Consistency with the rest of the repo

| Claim elsewhere | Status here |
| --- | --- |
| Hinge is not Hannan | Kept. $R_T^{\mathrm{ext}}$ vs best fixed action is a different scoreboard. |
| L_task + lambda L_reg | Heuristic attachment; not Blackwell steering. |
| Frozen D | Kept in u_reg. |
| r and D unsolved | Needed for A_safe to be nonempty, action-indexed, and stable. |
| No inference abort | Kept. |
| Amp not in the loss | Kept. Phase is a Player II fiber move. |

## What this file does not contain

- A proof of Blackwell.
- A proof that $S_{\mathrm{safe}}$ is approachable for any real $r,\mathcal{D}$.
- A proof that PPO approaches $S_{\mathrm{safe}}$.
- Construction of $r$ or $\mathcal{D}$.

Version 0.1.5.
