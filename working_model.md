# Characteristics of a working regret model

A working model is an *interface*, not a network family.
The amplitude joke, the Lean glossary, and the failed probes narrow what may sit in the loss and what may be claimed. They do not pick `r`.

"Working" here means: the object being trained is the hinge named in [math_formulation.md](math_formulation.md), aimed at [S_safe](approachability.md), with a sensor that can fail a topic probe. It does **not** mean reduced deception.

## Necessary interface

A candidate implementation is in-family only if all of these hold.

1. **Two scoreboards.** Task scalar and hinge scalar stay separate. `totalLoss task 0 hinge = task` (Lean). No folding the hinge into logits and calling that one loss.
2. **Loss signature.**
   ```math
   \mathcal{L}_{\mathrm{total}}
   =
   \mathcal{L}_{\mathrm{task}}(x,y)
   +
   \lambda\,
   \mathrm{ReLU}\big(\max_k s(r_{\mathrm{strat}}(h_{1:T}(a)), d_k)-\tau(u)\big).
   ```
   Inputs: walk, labels, candidate action, factored sensor, frozen bank, coarseness. Not $z$. Not an amplitude.
3. **$z\notin\mathrm{dom}(\mathcal{L}_{\mathrm{total}})$.** Lean: `LegalLoss` has no `Amp` field; `totalLoss_ignores_amp` is `rfl`. A prior or smoother may mention $z$. The optimizer graph may not.
4. **Path, not last token.** $h_{1:T}$. Last-token identity and mean-pool of the printed walk already failed the same-topic test ([experiment_results.md](experiment_results.md) §2 / §6).
5. **Action-indexed safety.** $r_{\mathrm{strat}}$ sees the candidate $a$. Otherwise $A_{\mathrm{safe}}$ is all of $A$ or none (`hingeQuietIgnoringAction_all_or_none`). Emptiness is allowed.
6. **Frozen bank during the walk.** $D$ is not an optimization variable and is not updated from the current answer (§3c is the camera moving the wallpaper).
7. **Factored sensor.** $r=(r_{\mathrm{topic}}, r_{\mathrm{strat}}, u)$. Hinge only $r_{\mathrm{strat}}$. $u$ only widens $\tau$ and forbids pinning when the chart is mush. $r_{\mathrm{topic}}$ may hug the hallway.
8. **Target $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$.** Extra cost vs the best *quiet* action that round, plus quiet hinge. Hannan-on-all-of-$A$ and clean insides is the rejected box.
9. **Training-time only.** No inference abort. Measurement delay is when the hinge may fire on $r$, not a decode block.
10. **Second channel outside the sum.** Frozen-identity lineage, held-out map cell, NLL/entropy disagreement, emptiness of $A_{\mathrm{safe}}$. Logged. Not a third loss.
11. **Smoother optional and off-graph.** A post-hoc $P(z\mid h)$ may label or refuse a pin after the walk. It is not a field of `LegalLoss`. No `Amp` in the backward pass.
12. **Group RL keeps the scoreboards apart.** Z-score the task group, then add $\lambda$ hinge. Mixing first is a different object (`group_zscore_mix_not_separate`). No critic of $L_{\mathrm{reg}}$.
13. **Decodable $\neq$ causal.** A probe that reads topic is not the coordinate a patch must move (`decodable_not_causal`). Do not put probe AUROC in the hinge.

## Necessary empirical filters (not success)

These are rejection tests. Passing them does not mean deception fell.

| Filter | Rejects |
| --- | --- |
| Topic / paraphrase probe on $r_{\mathrm{strat}}$ | Wallpaper regularizer. Identity control must stay near zero. |
| Honest and deceptive eval must not drop in lockstep when $r$ moves | §3c camera-drag. |
| Held-out cell the walk never occupies stays off $D$ | "Left the pins" ≠ "left the map". |
| Trained hinge can die while frozen $I$ does not | Pure sensor gaming. |
| $A_{\mathrm{safe}}$ sometimes empty | Pretending the sensor always determines a room. |
| Silent hinge with $R_T^{\mathrm{ext}}=T$ still possible | Conflating (A) with Hannan. Already Lean. |
| Probe loud while causal meter is silent | Treating decodability as the slap. Already Lean. |

## Forbidden implementations

Out of family, even if they use the word regret.

- Last-token or mean-pool identity as $r_{\mathrm{strat}}$.
- Tiny-$K$ $\max\cos$ treated as a solved detector (Kumar 2026 already pressure-tests that geometry).
- Steering $h\leftarrow h\pm\alpha v$, SAE-features-as-$D$ before a topic probe, LEACE as this hinge.
- ALNS / Potvin 2-regret (different object; Lean `insertion_two_regret_not_the_hinge`).
- Hedge / MW as if a cheap pre-image oracle for $\{h:\mathcal{L}_{\mathrm{reg}}=0\}$ existed.
- CFR on tokens as if that supplied $r_{\mathrm{strat}}$.
- Putting $z$ or `Amp` in the backward graph.
- Amplitude-encoding the residual stream into one packed unit vector and hinging that.
- Premature Born ($\lvert a\rvert^2+\lvert b\rvert^2$) reported as knowledge of $z$. Lean: that score is 2 on $(1,-1)$ while delayed $\lvert a+b\rvert^2$ is 0.
- Dynamic $D$ filled from the current walk.
- Reporting $\mathcal{L}_{\mathrm{reg}}$ as $p(\mathrm{lie})$ or as understanding.
- Claiming $S_{\mathrm{joint}}$ or Hannan-consistency of the hinge.
- GRPO / group z-score of $\mathrm{task}+\mathrm{hinge}$ as if that were two scoreboards (`group_zscore_mix_not_separate`).
- Entropy bonus as the hinge (`entropy_bonus_not_the_hinge`).
- Probe AUROC as the hinge (`decodable_not_causal`).

## What this did *not* pin

Still free, and still the actual research problem:

- The map $r_{\mathrm{strat}}$. A topic/plan split in a real residual is [intent-readout-search](https://github.com/kummahiih/intent-readout-search). Last-layer and mid-layer topic-subtract still have topic acc 1.00 (2026-09-20 sweep). Superposition packing fights that split. Do not train $r$ in this repo.
- Head-subset / function-vector $r$ (Todd, Pandey) and causal-SAE masks (Tiwari). Cartoons exist (`headWrite_ignores_rest`). Topic acc on those $r$ is unrun.
- Offline construction and coverage of $D$. Pins $\neq$ map (`heldout_not_mem_walk_bank`). Live fill is forbidden. How many pins is enough stays open.
- Numbers in $\tau(u)=\tau_0+u$ besides $u\ge 0$. The inequality is pinned (`regretHinge_mush_le`).
- $\lambda$ *schedule*. The lever is a Lagrangian halfspace (`ppoWithHinge_zero_weight`), not Blackwell steering.
- Bookkeeping field $\mathbb{R}$ vs $\mathbb{C}$ is a name. Signed reals already cancel (`two_route_identity_real`). $\mathbb{C}$ is Feynman’s label, not a camera.
- A smoother is optional. Labels pins only. Not in $L_{\mathrm{total}}$. Not required for the hinge to be in-family.
- Gaming remains open: $\nabla\mathcal{L}_{\mathrm{reg}}$ still enters $h$ and $r$. Frozen-$I$ is log-only. Do not add a third loss.
- Whether any trainer reaches $S_{\mathrm{safe}}$. Two-door is a box, not a PPO run.
- Adapter placement, quant, and optimizer: the slap must reach the layers $r$ reads; rebuild $D$ if $h$'s geometry changes. Not a camera.

So the space of *trainers* shrank. The space of *sensors* did not.

## Lean pins (glossary, not safety)

| Lemma | Characteristic |
| --- | --- |
| `regretHinge_wider_tau_le` | Wider $\tau$ cannot raise the hinge. |
| `regretHinge_mush_le` | Mush $\tau_0+u$ cannot raise the hinge. |
| `ppoWithHinge_zero_weight` | $\lambda=0$ drops the slap. One halfspace, not a schedule. |
| `silent_hinge_not_vanishing_external_regret` | Quiet hinge $\nRightarrow$ vanishing $R_T^{\mathrm{ext}}$. |
| `hingeQuietIgnoringAction_all_or_none` | Sensor must see $a$. |
| `two_route_identity` | Measurement time is load-bearing. |
| `two_route_identity_real` | Signed reals already cancel. $\mathbb{C}$ is a name, not a requirement. |
| `totalLoss_ignores_amp` | Amplitude is extra data, not a loss field. |
| `premature_sign_blind` | Squaring first loses the sign that would have cancelled. |
| `no_two_orthogonal_units_on_real` | A 1-d residual cannot hold an independent topic axis and plan axis. Packing, not a camera. |
| `grpo_advantage_not_the_hinge` | Group z-score of a reward is not the cosine hinge. |
| `entropy_bonus_not_the_hinge` | $-H$ is not the hinge. |
| `group_zscore_mix_not_separate` | Z-score($\mathrm{task}+\mathrm{hinge}$) $\neq$ z-score($\mathrm{task}$)$+$hinge. |
| `decodable_not_causal` | Probe on topic can shout while the plan coordinate is 0. |
| `headWrite_ignores_rest` | A head-write $r$ does not see the rest of the hallway. |

## One-sentence pin

A working regret model is a **training-time Lagrangian on a factored, action-conditioned path sensor against a frozen bank**, with hidden cells kept out of the graph, a second channel that can contradict the trained hinge, and $S_{\mathrm{safe}}$ as the only target. Anything that measures $z$, updates $D$ live, or claims Hannan of the hinge is a different object.

Version 0.1.0.
