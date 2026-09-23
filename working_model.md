# Characteristics of a working regret model

A working model is an *interface*, not a network family.
The amplitude joke, the Lean glossary, and the failed probes narrow what may sit in the loss and what may be claimed. They do not pick `r`.

"Working" here means: the object being trained is the hinge named in [math_formulation.md](math_formulation.md), aimed at [S_safe](approachability.md), with a sensor that can fail a topic probe. It does **not** mean reduced deception.

The trained term $\mathrm{ReLU}(\max_k\cos(r,d_k)-\tau)$ is **prototype-avoidance**. Call the English word regret that hinge if you want; do not call it Hannan $R_T^{\mathrm{ext}}$ and do not call it the counterfactual $R=u(x,a^*)-u(x,a)$. Those are other scoreboards. The repo name stays.

## The formula we do not train

Keep this on the wall. Do not put it in Adam until $a^*$ exists.

```math
a^*(x)=\arg\max_{a\in A_{\mathrm{safe}}(x)} u(x,a)
\qquad
R(x,a)=u(x,a^*)-u(x,a)
```

```math
L = L_{\mathrm{task}} + \lambda L_{\mathrm{reg}} + \beta R
```

$R$ is extra job-cost versus the best *quiet* move. Same shape as $u^{\mathrm{safe}}$ in [approachability.md](approachability.md). We do not use $\beta R$ because $a^*$ needs $A_{\mathrm{safe}}$, and $A_{\mathrm{safe}}$ needs a camera that sees plan. Contrast 2026-09-23: plan gap 0.026. A fake $a^*$ is a made-up grade.

The two-door toy is this box with dummy doors. It is not $\beta R$ in a trainer.

## Necessary interface

A candidate implementation is in-family only if all of these hold.

1. **Two scoreboards.** Task scalar and hinge scalar stay separate. `totalLoss task 0 hinge = task` (Lean). No folding the hinge into logits and calling that one loss. A third optional term $R=u(a^*)-u(a)$ is counterfactual task regret, not this hinge.
2. **Loss signature.**
   ```math
   \mathcal{L}_{\mathrm{total}}
   =
   \mathcal{L}_{\mathrm{task}}(x,y)
   +
   \lambda\,
   \mathrm{ReLU}\big(\max_k s(r_{\mathrm{strat}}(h_{1:T}(a)), d_k)-\tau(u)\big).
   ```
   Inputs: walk, labels, candidate action, factored sensor, frozen bank, coarseness. Not $z$. Not an amplitude. That $\mathrm{ReLU}$ is prototype-avoidance.
3. **$z\notin\mathrm{dom}(\mathcal{L}_{\mathrm{total}})$.** Signature: `LegalLoss` has no `Amp` field; `totalLoss_ignores_amp` is `rfl` once the numbers exist. Dataflow (B1): do not compute `task`/`hinge` from $z$ or `Amp` before the record. A prior or smoother may mention $z$. The optimizer graph may not.
4. **Path, not last token.** $h_{1:T}$. Last-token identity and mean-pool of the printed walk already failed the same-topic test ([experiment_results.md](experiment_results.md) §2 / §6).
5. **Action-indexed safety.** $r_{\mathrm{strat}}$ sees the candidate $a$. Otherwise $A_{\mathrm{safe}}$ is all of $A$ or none (`hingeQuietIgnoringAction_all_or_none`). Emptiness is allowed. Two-door toy: one bank $D=\{1\}$, $r(a_0)=-1$, $r(a_1)=1$.
6. **Frozen bank during the walk.** $D$ is not an optimization variable and is not updated from the current answer (§3c is the camera moving the wallpaper).
7. **Factored sensor.** $r=(r_{\mathrm{topic}}, r_{\mathrm{strat}}, u)$. Hinge only $r_{\mathrm{strat}}$. $u$ is detached (NLL / entropy), stop-grad into $u$, $\tau$ capped so $u$ cannot silence every cosine. $r_{\mathrm{topic}}$ may hug the hallway.
8. **Target $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$.** Extra cost vs the best *quiet* action that round, plus quiet hinge. Hannan-on-all-of-$A$ is only the rejected box.
9. **Training-time only.** No inference abort. Measurement delay is when the hinge may fire on $r$, not a decode block.
10. **Second channel outside the sum.** Frozen lineage (say readout / backbone / cached $h$), held-out map cell, NLL/entropy disagreement, emptiness of $A_{\mathrm{safe}}$. Logged. Disagreement is an alarm, not a gaming verdict. Not a third loss. Same-model chat grades are not this channel.
11. **Smoother optional and off-graph.** A post-hoc $P(z\mid h)$ may label or refuse a pin after the walk. It is not a field of `LegalLoss`. No `Amp` in the backward pass.
12. **Group RL keeps the scoreboards apart.** Z-score the task group, then add $\lambda$ hinge. Mixing first is a different object (`group_zscore_mix_not_separate`). No critic of $L_{\mathrm{reg}}$.
13. **Decodable $\neq$ causal.** A probe that reads topic is not the coordinate a patch must move (`decodable_not_causal`). Do not put probe AUROC in the hinge.
14. **Implicit reject.** A checker that always returns a key is not $z$ (`implicit_miss_is_some`). Verbal oracles and mutated tails are walks.
15. **Dynamical readout is a candidate, not a theorem that gaming is dead.** A static linear $Wh+b$ with a kernel admits $P(h+v)=P(h)$ (Lean: `static_linear_evasion_exists`). Identity has no kernel. A $K$-step loop is allowed. Residual $h+F(h)+\sigma\varepsilon$ is **not** the Lean basin unless `step` is a contraction.

## Necessary empirical filters (not success)

These are rejection tests. Passing them does not mean deception fell.

| Filter | Rejects |
| --- | --- |
| Topic / paraphrase probe on $r_{\mathrm{strat}}$ | Wallpaper regularizer. Official topic gate is LOO / hold, not same-row lstsq. Identity control must stay near zero. |
| Honest and deceptive eval must not drop in lockstep when $r$ moves | §3c camera-drag. |
| Held-out cell the walk never occupies stays off $D$ | "Left the pins" $\neq$ "left the map". |
| Trained hinge can die while frozen $I$ does not | Investigate; not an automatic gaming verdict. |
| $A_{\mathrm{safe}}$ sometimes empty | Pretending the sensor always determines a room. |
| Silent hinge with $R_T^{\mathrm{ext}}=T$ still possible | Conflating prototype-avoidance with Hannan. Already Lean. |
| Probe loud while causal meter is silent | Treating decodability as the slap. Already Lean. |
| Plan LOTO chance / topic-miss slice chance | Treating a polite mouth as a camera. |
| Path-patch prints source-topic words | Lexical bleed (`lexical_bleed`). |
| Same-model chat fact-grade used as nature | Actor+judge shared blind spot. |
| Orthogonal representation gaming | Static linear probes that report $L_{\mathrm{reg}}=0$ when the optimizer just rotates the intent into the sensor's null space. |

## Forbidden implementations

Out of family, even if they use the word regret.

- Last-token or mean-pool identity as $r_{\mathrm{strat}}$.
- Tiny-$K$ $\max\cos$ treated as a solved detector (Kumar 2026 already pressure-tests that geometry).
- Steering $h\leftarrow h\pm\alpha v$, SAE-features-as-$D$ before a topic probe, LEACE as this hinge.
- ALNS / Potvin 2-regret (different object; Lean `insertion_two_regret_not_the_hinge`).
- Hedge / MW as if a cheap pre-image oracle for $\{h:\mathcal{L}_{\mathrm{reg}}=0\}$ existed.
- CFR on tokens as if that supplied $r_{\mathrm{strat}}$.
- Putting $z$ or `Amp` in the backward graph, including baking them into `task`/`hinge` before `LegalLoss`.
- Joint training of $u$ so the hinge dies by "I am unsure."
- Amplitude-encoding the residual stream into one packed unit vector and hinging that.
- Premature Born reported as the mechanism of the 0.77 / 0.80 probe. That smear is topic hug. Path $r$ is a research choice.
- Dynamic $D$ filled from the current walk.
- Reporting $\mathcal{L}_{\mathrm{reg}}$ as $p(\mathrm{lie})$ or as understanding.
- Claiming $S_{\mathrm{joint}}$ or Hannan-consistency of the hinge.
- GRPO / group z-score of $\mathrm{task}+\mathrm{hinge}$ as if that were two scoreboards.
- Entropy bonus as the hinge.
- Probe AUROC as the hinge.
- Filling $D$ from a verbal oracle, a mid-walk mutate, or a same-model chat grade.
- Treating every static linear $r$ as proven-blind (identity has trivial kernel).
- Un-normalized inputs to a noisy loop so $\Vert h\Vert\to\infty$ drowns $\sigma$.
- A transition $F(h)\approx -h$ that flattens the state before readout.
- Equating residual+noise with the Lean contraction basin.
- Training $\beta R$ with a fake $a^*$.

## What this did *not* pin

Still free, and still the actual research problem:

- The map $r_{\mathrm{strat}}$. [intent-readout-search](https://github.com/kummahiih/intent-readout-search): official LOO topic on loud heads 0.79 / layer 0.62; adversary hold 0.53; contrast L2 topic 0.31, plan gap 0.026. Superposition packing fights a clean split. Do not train $r$ in this repo.
- Head-subset $r$ (Todd, Pandey): **run**. Official LOO still names topic. Causal-SAE (Tiwari) still unrun.
- Offline construction and coverage of $D$. Pins $\neq$ map. Live fill is forbidden.
- $\lambda$ *schedule*. Lagrangian halfspace, not Blackwell steering.
- Bookkeeping field $\mathbb{R}$ vs $\mathbb{C}$ is a name. Signed reals already cancel.
- Gaming remains open: $\nabla\mathcal{L}_{\mathrm{reg}}$ still enters $h$ and $r$.
- Whether any trainer reaches $S_{\mathrm{safe}}$. Two-door is a box, not a PPO run.
- Dynamic evasion modes: noisy iterative sensor candidate motivated by a conditional contraction hypothesis.
- $\beta R$ once a real $A_{\mathrm{safe}}$ exists.

## Lean pins (glossary, not safety)

| Lemma | Characteristic |
| --- | --- |
| `regretHinge_wider_tau_le` | Wider $\tau$ cannot raise the hinge. |
| `regretHinge_mush_le` | Mush $\tau_0+u$ cannot raise the hinge. |
| `ppoWithHinge_zero_weight` | $\lambda=0$ drops the slap. |
| `silent_hinge_not_vanishing_external_regret` | Quiet hinge $\nRightarrow$ vanishing $R_T^{\mathrm{ext}}$. |
| `hingeQuietIgnoringAction_all_or_none` | Sensor must see $a$. |
| `two_route_identity` | Measurement time is load-bearing. |
| `totalLoss_ignores_amp` | Signature only. Dataflow is B1 prose. |
| `decodable_not_causal` | Probe on topic can shout while the plan coordinate is 0. |
| `headWrite_ignores_rest` | A head-write $r$ does not see the rest of the hallway. |
| `implicit_miss_is_some` | A miss still returns a key. |
| `lexical_bleed` | Patched walk prints the source topic token. |
| `static_linear_evasion_exists` | If $W$ has a kernel, some $v\neq 0$ leaves $P(h+v)=P(h)$. |
| `dynamic_trajectory_convergence` | **If** `step` is a basin contraction, distance after $K$ steps is $\le c^K$. Residual+noise is not that hypothesis. |

## One-sentence pin

A working regret model is a **training-time Lagrangian of prototype-avoidance on a factored, action-conditioned path sensor against a frozen bank**, with hidden cells kept out of the graph, $u$ off that graph, a second channel that can contradict the trained hinge, and $S_{\mathrm{safe}}$ as the only target. Anything that measures $z$, trains $u$ to silence the hinge, updates $D$ live, or claims Hannan of the hinge is a different object.

Version 0.1.5.
