# Implementation binding

The rest of the repo names a hinge and records how identity / mean-pool sensors fail.
This note ties that hinge to a build order. It does not add a third loss, an inference abort, or a quantum circuit.

Source used as a *filter*, not as evidence: a survey of quantum-probability bookkeeping in partially observable security models (POMDP / Petri split, Born delay, amplitude-vs-angle packing, utility-plus-attraction). None of its reported accuracies, hardware claims, or honeypot recipes are imported. Hilbert space is optional notation for a signed multi-hypothesis score. The learner stays classical.

## What was missing

`math_formulation.md` defines

```math
\mathcal{L}_{\mathrm{total}}=\mathcal{L}_{\mathrm{task}}+\lambda\,\mathrm{ReLU}\big(\max_k s(r(h(x)),d_k)-\tau\big).
```

That is a *shape*. Implementation still needs six objects the toys assume:

1. A path $h_{1:T}$, not one last vector.
2. Hidden cells $z_t$ distinct from printed tokens.
3. A sensor $r$ that is not one packed unit vector.
4. An action-indexed $A_{\mathrm{safe}}(t)$.
5. A measurement time (when the hinge is allowed to fire).
6. A second channel that is *not* in the training sum.

Failure probes (§2, §3c, §6) already show what happens if you skip 1–3: topic wallpaper, honest and deceptive eval move together, mean-pool mixes the hallway.

## 1. Observable vs unobservable (Petri / POMDP split)

| Object | In this repo |
| --- | --- |
| Observable transition | Emitted token, tool call, or other logged event. The walk. |
| Unobservable transition | Intent cell $z_t$: stay / fork / return. The map. |
| Marking | Occupancy over cells after $t$ steps. |
| Incidence | Coarse motion prior $P(z_t\mid z_{t-1})$. No teleport between rooms. |
| Sensor | $P(r(h_t)\mid z_t)$, with declared variance $u$ (NLL / entropy / label noise). Not $p(\mathrm{lie})$. |

The language model already is a *token* motion model. The missing piece is the coarse intent motion model already named in [slam_analogy.md](slam_analogy.md).

Do not update $\mathcal{D}$ from the current walk. Pins that move with the camera are §3c.

## 2. Delayed measurement (do not square early)

Classical last-token $r=I$ is a measurement at $T$ of a single packed vector. Two unobservable routes to the same printed string are added as *probabilities* and smear (0.77 / 0.80).

Keep a signed score over cells *before* the hinge:

```math
\alpha_t(z)\in\mathbb{R}
\qquad
\text{(or $\mathbb{C}$ if a phase is actually used)}
```

Aggregate along the path, *then* read out:

```math
h_{\mathrm{int}}=r(h_{1:T},\alpha_{1:T}),
\qquad
\mathcal{L}_{\mathrm{reg}}=\mathrm{ReLU}\big(\max_k s(h_{\mathrm{int}},d_k)-\tau(u)\big).
```

$\tau(u)$ wider when the chart is coarse ([intent-readout-search PROTOCOL](https://github.com/kummahiih/intent-readout-search/blob/main/PROTOCOL.md) rule 3). Quiet on mush is not honesty.

The Born-rule slogan in the survey is only this: **sum hypotheses first, apply the hinge second.** Training still uses the ReLU. Inference still does not abort.

A posterior smoother $P(z_{1:T}\mid h_{1:T})$ may *label or refuse a pin* after the answer exists. It is not a third term in $\mathcal{L}_{\mathrm{total}}$.

## 3. Factored $r$, not amplitude packing

Packing topic, strategy, and uncertainty into one normalized last-token vector is the survey's amplitude-encoding failure mode: exponential compression that destroys the gap you wanted. Tiny-$K$ $\max\cos$ is the same geometry Kumar 2026 already pressure-tests ([neighbors.md](neighbors.md)).

Implement $r$ as *separate coordinates* (the angle-encoding lesson, classically):

```math
r(h)=\big(r_{\mathrm{topic}}(h),\; r_{\mathrm{strat}}(h),\; u(h)\big).
```

- $r_{\mathrm{topic}}$ is allowed to hug the hallway. It is wallpaper. Do not hinge it.
- $r_{\mathrm{strat}}$ is the only input to $\mathcal{L}_{\mathrm{reg}}$. Topic probe must fail on these vectors.
- $u$ only widens $\tau$ and forbids pinning $\mathcal{D}$ when $u>u_0$.

Sister-repo work already pointed here: `topic_residual.py`, `synthetic_z.py`. Construction of $r_{\mathrm{strat}}$ stays in [intent-readout-search](https://github.com/kummahiih/intent-readout-search). This repo consumes a vector that has passed the topic probe.

Keep at least one frozen-identity lineage while $r_{\mathrm{strat}}$ is trained, so a moving sensor cannot hide that the map never split (§3c).

## 4. Two factors, one target

The survey's Quantum Decision Theory split (utility factor vs attraction factor) is already the Lagrangian:

| Survey name | Here |
| --- | --- |
| Utility factor | $\mathcal{L}_{\mathrm{task}}$ or $-L^{\mathrm{CLIP}}$ |
| Attraction factor | $\lambda\mathcal{L}_{\mathrm{reg}}$ on $r_{\mathrm{strat}}$ only |
| Collapse / measurement | Not an inference abort |

Sign for PPO: subtract the hinge from a maximand ([ppo_integration.md](ppo_integration.md)).

The only approachable box this essay may aim at remains $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$ ([approachability.md](approachability.md)). That forces $r$ to see the *candidate action*:

```math
A_{\mathrm{safe}}(t)=\{a\in A:\ \mathcal{L}_{\mathrm{reg}}(r_{\mathrm{strat}}(h_t(a)),\mathcal{D})=0\}.
```

If $r$ only sees a pre-action $h_t$, $A_{\mathrm{safe}}$ does not depend on $a$ and is not a comparator class.

A Lagrangian weight $\lambda$ is one halfspace, not Blackwell steering.

## 5. Subnet before the hinge

Do not run $\max_k\cos$ on the whole residual stream.

Given the observable walk $x_{1:T}$:

1. List unobservable transitions that can precede or follow logged events under the motion prior.
2. Drop transitions the prior forbids after this walk (no invoice $\to$ hiking teleport).
3. Score only the surviving cells against frozen $\mathcal{D}$.
4. Hold out at least one map cell the walk never occupies (`simulation_heldout.py`, sister-repo action 2). Evading onto that cell is not leaving the map.

That is the survey's "extract a subnet, then diagnose" step, without Petri-net software or reported 98% figures.

## 6. Second channel (not in the sum)

Representation gaming is the analogue of decoherence: the system still acts, the hinge goes quiet.

Do not add a third training loss. Log, and refuse to pin $\mathcal{D}$ from, these monitors:

- Frozen-$I$ lineage hinge (must not track a trained $r_{\mathrm{strat}}$ that only rotated wallpaper).
- Cosine to a held-out cell.
- NLL vs entropy disagreement (§4).
- Whether $A_{\mathrm{safe}}(t)$ emptied.

If the trained hinge dies and the frozen-$I$ hinge does not move, you gamed the sensor.

## Build order

Do these in order. Stop if the topic probe still passes on $r_{\mathrm{strat}}$.

| Step | Where | Done means |
| --- | --- | --- |
| B0 | [intent-readout-search](https://github.com/kummahiih/intent-readout-search) | $r_{\mathrm{strat}}$ gap survives topic and paraphrase; identity control stays near zero. |
| B1 | this repo, new path object | $h_{1:T}$ + stay/fork/return prior; no hinge on $h_T$ alone. |
| B2 | this repo | $r$ consumes candidate $a$; $A_{\mathrm{safe}}(t)$ is action-indexed and sometimes empty. |
| B3 | this repo | $\tau(u)$ bins; no pin when $u>u_0$. |
| B4 | this repo | Frozen-$I$ lineage + held-out cell logged every run. Do not overwrite [experiment_results.md](experiment_results.md) §1–§7. |
| B5 | optional | Smoother $P(z_{1:T}\mid h_{1:T})$ labels pins only. |
| B6 | never here | Quantum circuits, amplitude encoding, QBPN software, quantum walks, honeypot attraction attacks. |

Existing wiring stays: [simulation.py](simulation.py), [ppo_toy.py](ppo_toy.py), Lean glossary. They are not B0–B4.

## Caps this file does not lift

- No claim that $S_{\mathrm{safe}}$ is approachable for a real $r,\mathcal{D}$.
- No claim that delayed measurement or factored $r$ exists.
- No imported diagnostic accuracies from the survey.
- No dual-use honeypot recipe. Attraction is a training hinge on a readout, not a cognitive attack.
- No inference abort. Measurement delay is about *when the hinge may fire in training*, not about blocking decode.

Version 0.1.0.
