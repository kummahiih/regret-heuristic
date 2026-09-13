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

Each round, player I picks from a compact set $X$, player II from $Y$, and the payoff is a vector $u(x,y)\in\mathbb{R}^d$. Write $\bar u_T=\frac1T\sum_{t=1}^T u(x_t,y_t)$. A closed convex set $S\subset\mathbb{R}^d$ is **approachable** if player I has a causal strategy such that $\mathrm{dist}(\bar u_T,S)\to 0$ against every sequence of II.

A halfspace $H\supset S$ is **forceable** if some $x^*\in X$ satisfies $u(x^*,y)\in H$ for all $y\in Y$.

**Theorem (Blackwell 1956, convex case).**  
$S$ closed and convex is approachable if and only if every halfspace containing $S$ is forceable.

This note uses that statement as a black box. It does not prove Blackwell.

## Vector payoff for this repo

Use the hinge of [math_formulation.md](math_formulation.md), frozen $\mathcal{D}$. Let $\ell_t$ be a per-round task cost of the played action $a_t$.

Define the **safe comparator class** from the hinge, not from $A$:

$$
A_{\mathrm{safe}}(t)
=
\{a\in A:\ \mathcal{L}_{\mathrm{reg}}(r(h_t),\mathcal{D})=0\}.
$$

If $A_{\mathrm{safe}}(t)$ is empty, the hinge is not a usable constraint that round; the target below is not defined for that $t$. That is an assumption on $r$ and $\mathcal{D}$, same as in the math note.

Two coordinates:

$$
u_t^{\mathrm{safe}}
=
\ell_t(a_t)-\min_{a\in A_{\mathrm{safe}}(t)}\ell_t(a),
\qquad
u_t^{\mathrm{reg}}
=
\mathcal{L}_{\mathrm{reg}}\bigl(r(h_t),\mathcal{D}\bigr).
$$

$$
u_t=(u_t^{\mathrm{safe}},\,u_t^{\mathrm{reg}})\in\mathbb{R}^2.
$$

## Targets

**Rejected target (not claimed):**

$$
S_{\mathrm{joint}}=(-\infty,0]\times(-\infty,0]
\quad\text{with first coordinate vs $\min_{a\in A}\ell_t(a)$.}
$$

That is "Hannan on all of $A$, and hinge quiet." If a profitable action sits in $\mathcal{D}$, some halfspace containing $S_{\mathrm{joint}}$ is not forceable. Blackwell then says $S_{\mathrm{joint}}$ is not approachable. This repo does **not** claim $S_{\mathrm{joint}}$.

**Essay target (the only one consistent with keep-the-skill, tag-the-intent):**

$$
S_{\mathrm{safe}}=(-\infty,0]\times(-\infty,0]
\quad\text{with first coordinate $u^{\mathrm{safe}}$.}
$$

Average in $S_{\mathrm{safe}}$ means:

- mean hinge $\to$ dead zone (tag the intent);
- mean extra cost vs the *best hinge-quiet action* $\to 0$ (keep the skill *inside the tagged-safe set*).

That is policy / action regret **inside** the hinge's safe set, not Hannan on $A$. It matches [regret_minimization.md](regret_minimization.md): the hinge is not $R_T^{\mathrm{ext}}$.

## Forceability of $S_{\mathrm{safe}}$ (condition, not a theorem we prove)

$S_{\mathrm{safe}}$ is approachable iff every $w=(w_1,w_2)$ with $w_1,w_2\ge 0$ admits a mixed $x^*$ such that for all world $y$,

$$
w_1\,\mathbb{E}[u^{\mathrm{safe}}]+w_2\,\mathbb{E}[u^{\mathrm{reg}}]\le 0.
$$

This can fail if $A_{\mathrm{safe}}$ is empty, or if $r$ can be gamed so that "$a$ looks safe" and "$a$ is the safe comparator" come apart. Those are the same open problems as in the math note ($r$, $\mathcal{D}$, evasion).

If the condition holds, Blackwell supplies a causal steering rule (project $\bar u_t$ onto $S_{\mathrm{safe}}$, force that halfspace). That rule is **not** implemented in [simulation.py](simulation.py) or [ppo_toy.py](ppo_toy.py). Those toys only attach $\lambda\mathcal{L}_{\mathrm{reg}}$ to a scalar objective. A Lagrangian $L_{\mathrm{task}}+\lambda L_{\mathrm{reg}}$ is a *heuristic* for one halfspace weight, not a proof that $S_{\mathrm{safe}}$ is approached.

## Consistency with the rest of the repo

| Claim elsewhere | Status here |
| --- | --- |
| Hinge is not Hannan on $A$ | Kept. $S_{\mathrm{joint}}$ rejected. |
| $\mathcal{L}_{\mathrm{task}}+\lambda\mathcal{L}_{\mathrm{reg}}$ | Heuristic attachment; not Blackwell steering. |
| Frozen $\mathcal{D}$ | Kept in $u^{\mathrm{reg}}$. |
| $r$ and $\mathcal{D}$ unsolved | Needed for $A_{\mathrm{safe}}$ to be nonempty and stable. |
| No inference abort | Kept. Approachability is on *averages*, not a veto. |

## What this file does not contain

- A proof of Blackwell.
- A proof that $S_{\mathrm{safe}}$ is approachable for any real $r,\mathcal{D}$.
- A proof that PPO approaches $S_{\mathrm{safe}}$.
- Construction of $r$ or $\mathcal{D}$.

Version 0.1.0. Companion to `math_formulation.md` and `regret_minimization.md`.
