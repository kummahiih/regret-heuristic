# Characteristics of a working regret model

A working model is an *interface*, not a network family.
The amplitude joke, the Lean glossary, and the failed probes narrow what may sit in the loss and what may be claimed. They do not pick *r*.

"Working" here means: the object being trained is the hinge named in [math_formulation.md](math_formulation.md), aimed at [S_safe](approachability.md), with a sensor that can fail a topic probe. It does **not** mean reduced deception.

The trained term is **prototype-avoidance**:

```math
\mathrm{ReLU}\bigl(\max_k \cos(r, d_k) - \tau\bigr)
```

Call the English word regret that hinge if you want. Do not call it Hannan external regret *R*<sub>T</sub><sup>ext</sup>, and do not call it the counterfactual *R* = *u*(*x*, *a*<sup>∗</sup>) − *u*(*x*, *a*). Those are other scoreboards. The repo name stays.

## The formula we do not train

Keep this on the wall. Do not put it in Adam until *a*<sup>∗</sup> exists.

```math
a^{\ast}(x) = \arg\max_{a \in A_{\mathrm{safe}}(x)} u(x,a)
\qquad
R(x,a) = u(x,a^{\ast}) - u(x,a)
```

```math
L = L_{\mathrm{task}} + \lambda L_{\mathrm{reg}} + \beta R
```

*R* is extra job-cost versus the best *quiet* move. Same shape as *u*<sup>safe</sup> in [approachability.md](approachability.md). We do not use β*R* because *a*<sup>∗</sup> needs *A*<sub>safe</sub>, and *A*<sub>safe</sub> needs a camera that sees plan. Contrast 2026-09-23: plan gap 0.026 (layer-8 last-token later ~0.07, still fail). A fake *a*<sup>∗</sup> is a made-up grade.

The two-door toy is this box with dummy doors. It is not β*R* in a trainer.

## Necessary interface

A candidate implementation is in-family only if all of these hold.

1. **Two scoreboards.** Task scalar and hinge scalar stay separate. `totalLoss task 0 hinge = task` (Lean). No folding the hinge into logits and calling that one loss. A third optional term *R* = *u*(*a*<sup>∗</sup>) − *u*(*a*) is counterfactual task regret, not this hinge.
2. **Loss signature.** The object Adam may see is below. It is not indented into this list, so the fence renders.

```math
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{task}}(x,y)
+
\lambda\,
\mathrm{ReLU}\bigl(\max_k s(r_{\mathrm{strat}}(h_{1:T}(a)), d_k) - \tau(u)\bigr)
```

Term by term (full glossary: [math_formulation.md](math_formulation.md)):

| Piece | Role |
| --- | --- |
| *L*<sub>total</sub> | What Adam sees. Two scoreboards added, not one folded logit. |
| *L*<sub>task</sub>(*x*, *y*) | The job: CE / RL pay / dummy task head on input *x* and task target *y*. *y* is not a strategy tag. |
| λ | How hard the slap is. λ = 0 drops the second term (`ppoWithHinge_zero_weight`). |
| *h*<sub>1:T</sub>(*a*) | Path of hidden states while considering candidate action *a*. Not last-token identity. |
| *r*<sub>strat</sub> | Strategy readout of that path. Topic readout *r*<sub>topic</sub> and coarseness *u* are not this argument. |
| *d*<sub>k</sub> | One frozen prototype in bank *D* = {*d*<sub>1</sub>, …, *d*<sub>K</sub>}. Not updated from this answer. |
| *s* | Cosine. How aligned the readout is with pin *d*<sub>k</sub>. Undefined at 0. |
| max<sub>k</sub> | Nearest listed bad plan. One close pin is enough. |
| τ(*u*) | Threshold. Cosine must beat this before any penalty. May widen with coarseness *u*. *u* is stop-grad; it must not learn to silence every cosine. |
| ReLU(*t*) = max(0, *t*) | One-sided kink on *t* = max<sub>k</sub> *s* − τ(*u*). Below τ: penalty 0 (dead zone). Above τ: penalty is the excess. Not a hidden-layer activation. Quiet below τ is not honesty. |

Inputs: walk, labels, candidate action, factored sensor, frozen bank, coarseness. Not *z*. Not an amplitude. Not *m̂*. Not SIREN θ. Not `reply_kind`. That ReLU is prototype-avoidance.

3. ***z* is not in the domain of *L*<sub>total</sub>.** Same for talker-count *m̂* and path-fit θ. Signature: `LegalLoss` has no those fields; `totalLoss_ignores_amp`, `totalLoss_ignores_sourceCount`, `totalLoss_ignores_theta` are `rfl`. Dataflow (B1): do not compute `task` / `hinge` from *z*, Amp, *m̂*, or θ before the record.
4. **Path, not last token.** *h*<sub>1:T</sub>. If a *K*-step mix is used, score *s*<sub>K</sub> only. Do **not** average per-token hinges ([simulation_kstep.py](simulation_kstep.py)). Last-token identity, mean-pool, and dummy SIREN *f*(1) already failed or collapsed to the last point ([experiment_results.md](experiment_results.md) §2 / §6, [experiment_siren_path.md](experiment_siren_path.md)). *K*-step is a **candidate**, not a proof the kernel died.
5. **Action-indexed safety.** *r*<sub>strat</sub> sees the candidate *a*. Otherwise *A*<sub>safe</sub> is all of *A* or none (`hingeQuietIgnoringAction_all_or_none`). Emptiness is allowed. Two-door toy: one bank *D* = {1}, *r*(*a*<sub>0</sub>) = −1, *r*(*a*<sub>1</sub>) = 1.
6. **Frozen bank during the walk.** *D* is not an optimization variable and is not updated from the current answer (§3c is the camera moving the wallpaper).
7. **Factored sensor.** *r* = (*r*<sub>topic</sub>, *r*<sub>strat</sub>, *u*). Hinge only *r*<sub>strat</sub>. *u* is detached (NLL / entropy), stop-grad into *u*, τ capped so *u* cannot silence every cosine. *r*<sub>topic</sub> may hug the hallway.
8. **Target *S*<sub>safe</sub>, not *S*<sub>joint</sub>.** Extra cost vs the best *quiet* action that round, plus quiet hinge. Hannan-on-all-of-*A* is only the rejected box.
9. **Training-time only.** No inference abort. Measurement delay is when the hinge may fire on *r*, not a decode block.
10. **Second channel outside the sum.** Frozen lineage, held-out map cell, NLL/entropy disagreement, *m̂*, emptiness of *A*<sub>safe</sub>. Logged. Disagreement is an alarm, not a gaming verdict. Not a third loss. Same-model chat grades are not this channel.
11. **Smoother optional and off-graph.** A post-hoc *P*(*z* | *h*) may label or refuse a pin after the walk. It is not a field of `LegalLoss`. No `Amp` in the backward pass.
12. **Group RL keeps the scoreboards apart.** Z-score the task group, then add λ hinge. Mixing first is a different object (`group_zscore_mix_not_separate`). No critic of *L*<sub>reg</sub>.
13. **Decodable is not causal.** A probe that reads topic is not the coordinate a patch must move (`decodable_not_causal`). Do not put probe AUROC in the hinge.
14. **Implicit reject.** A checker that always returns a key is not *z* (`implicit_miss_is_some`). Verbal oracles and mutated tails are walks.
15. **Dynamical readout is a candidate, not a theorem that gaming is dead.** A static linear *Wh* + *b* with a kernel admits *P*(*h* + *v*) = *P*(*h*) (Lean: `static_linear_evasion_exists`). Identity has no kernel. Residual *h* + *F*(*h*) + σε is **not** the Lean basin unless `step` is a contraction. Four-state dummy ([experiment_four_state.md](experiment_four_state.md)): isotropic *T* = *cI* shrinks plan and **hides** ker *r* (`iso_hides_kernel`). Random *F* shows *v* and dumps topic. Wanted split (plan kept and evasion visible and topic quiet) is **not demonstrated**. *K*-step kept a hinge **gradient** after one step; that is persistence of the derivative, not OOD visibility (*L*<sub>far</sub> = 0).

## Necessary empirical filters (not success)

These are rejection tests. Passing them does not mean deception fell.

| Filter | Rejects |
| --- | --- |
| Topic / paraphrase probe on *r*<sub>strat</sub> | Wallpaper regularizer. Official topic gate is LOO / hold, not same-row lstsq. Identity control must stay near zero. |
| Honest and deceptive eval must not drop in lockstep when *r* moves | §3c camera-drag. |
| Held-out cell the walk never occupies stays off *D* | "Left the pins" is not "left the map". |
| Trained hinge can die while frozen *I* does not | Investigate; not an automatic gaming verdict. |
| *A*<sub>safe</sub> sometimes empty | Pretending the sensor always determines a room. |
| Silent hinge with external regret = *T* still possible | Conflating prototype-avoidance with Hannan. Already Lean. |
| Probe loud while causal meter is silent | Treating decodability as the slap. Already Lean. |
| Plan LOTO chance / topic-miss slice chance | Treating a polite mouth as a camera. |
| Path-patch prints source-topic words | Lexical bleed (`lexical_bleed`). |
| Same-model chat fact-grade used as nature | Actor+judge shared blind spot. |
| Orthogonal representation gaming | Static linear probes that report *L*<sub>reg</sub> = 0 when the optimizer just rotates the intent into the sensor's null space. |
| Four-state wanted split | Claiming *K*-step / contraction removes evasion while keeping plan. No dummy *T* passed. |
| Flattening with proxy class hold | Quiet hinge while dummy behavior label stays. Exists-*h* and exists-θ toys. |
| *m̂* or θ in *L*<sub>total</sub> | Crowded hallway or path-fit weights used as the slap. |

## Forbidden implementations

Out of family, even if they use the word regret.

- Last-token or mean-pool identity as *r*<sub>strat</sub>.
- Average of per-token hinges as *L*<sub>reg</sub> (score *s*<sub>K</sub> only).
- Tiny-*K* max-cosine treated as a solved detector (Kumar 2026 already pressure-tests that geometry).
- Steering *h* ← *h* ± α*v*, SAE-features-as-*D* before a topic probe, LEACE as this hinge.
- ALNS / Potvin 2-regret (different object; Lean `insertion_two_regret_not_the_hinge`).
- Hedge / MW as if a cheap pre-image oracle for {*h* : *L*<sub>reg</sub> = 0} existed.
- CFR on tokens as if that supplied *r*<sub>strat</sub>.
- Putting *z*, `Amp`, *m̂*, or SIREN θ in the backward graph.
- Joint training of *u* so the hinge dies by "I am unsure."
- Amplitude-encoding the residual stream into one packed unit vector and hinging that.
- Premature Born reported as the mechanism of the 0.77 / 0.80 probe. That smear is topic hug. Path *r* is a research choice.
- Dynamic *D* filled from the current walk.
- Reporting *L*<sub>reg</sub> as *p*(lie) or as understanding.
- Claiming *S*<sub>joint</sub> or Hannan-consistency of the hinge.
- GRPO / group z-score of task+hinge as if that were two scoreboards.
- Entropy bonus as the hinge.
- Probe AUROC as the hinge.
- Filling *D* from a verbal oracle, a mid-walk mutate, or a same-model chat grade.
- Treating every static linear *r* as proven-blind (identity has trivial kernel).
- Un-normalized inputs to a noisy loop so the norm of *h* goes to infinity and drowns σ.
- A transition *F*(*h*) ≈ −*h* that flattens the state before readout.
- Equating residual+noise with the Lean contraction basin.
- Claiming *K*-step "breaks the null" because a hinge gradient persisted.
- Training β*R* with a fake *a*<sup>∗</sup>.
- Treating dummy proxy_behavior / frozen *B*-head as strategy.
- SIREN / INR θ as *r*<sub>strat</sub> because *f*(1) recovered a planted last point.

## What this did *not* pin

Still free, and still the actual research problem:

- The map *r*<sub>strat</sub>. [intent-readout-search](https://github.com/kummahiih/intent-readout-search): official LOO topic on loud heads 0.79 / layer 0.62; adversary hold 0.53; contrast L2 topic 0.31, plan gap 0.026–0.07. Superposition packing fights a clean split. Do not train *r* in this repo.
- Head-subset *r* (Todd, Pandey): **run**. Official LOO still names topic. Causal-SAE (Tiwari) still unrun.
- Offline construction and coverage of *D*. Pins are not the map. Live fill is forbidden.
- λ schedule. Lagrangian halfspace, not Blackwell steering.
- Bookkeeping field reals vs complex is a name. Signed reals already cancel.
- Gaming remains open: the gradient of *L*<sub>reg</sub> still enters *h* and *r*. Exists-*h* and exists-θ flattening toys.
- Whether any trainer reaches *S*<sub>safe</sub>. Two-door is a box, not a PPO run.
- A *T* that sends ker *r* out of the kernel **without** shrinking plan or leaking topic. Four-state dummy failed.
- β*R* once a real *A*<sub>safe</sub> exists.
- Qwen path-dump into SIREN (dummy only).

## Lean pins (glossary, not safety)

| Lemma | Characteristic |
| --- | --- |
| `regretHinge_wider_tau_le` | Wider τ cannot raise the hinge. |
| `regretHinge_mush_le` | Mush τ<sub>0</sub> + *u* cannot raise the hinge. |
| `ppoWithHinge_zero_weight` | λ = 0 drops the slap. |
| `silent_hinge_not_vanishing_external_regret` | Quiet hinge does not imply vanishing external regret. |
| `hingeQuietIgnoringAction_all_or_none` | Sensor must see *a*. |
| `two_route_identity` | Measurement time is load-bearing. |
| `totalLoss_ignores_amp` | Signature only. Dataflow is B1 prose. |
| `totalLoss_ignores_sourceCount` / `crowded_not_the_slap` | Talker-count is a log. |
| `totalLoss_ignores_theta` / `queryEnd_is_the_end` | Path-fit weights and *f*(1) are walk objects. |
| `iso_scales_plan` / `iso_hides_kernel` | Isotropic *T* = *c h* shrinks plan and leaves ker *r* silent. |
| `decodable_not_causal` | Probe on topic can shout while the plan coordinate is 0. |
| `headWrite_ignores_rest` | A head-write *r* does not see the rest of the hallway. |
| `implicit_miss_is_some` | A miss still returns a key. |
| `lexical_bleed` | Patched walk prints the source topic token. |
| `static_linear_evasion_exists` | If *W* has a kernel, some *v* ≠ 0 leaves *P*(*h* + *v*) = *P*(*h*). |
| `dynamic_trajectory_convergence` | **If** `step` is a basin contraction, distance after *K* steps is at most *c*<sup>K</sup>. Residual+noise is not that hypothesis. |
| `quiet_hinge_not_counterfactualR` | Hinge 0 and *R* = 1 can sit together. |

## One-sentence pin

A working regret model is a **training-time Lagrangian of prototype-avoidance on a factored, action-conditioned path sensor against a frozen bank**, with hidden cells kept out of the graph, *u* off that graph, a second channel that can contradict the trained hinge, and *S*<sub>safe</sub> as the only target. Anything that measures *z*, trains *u* to silence the hinge, updates *D* live, or claims Hannan of the hinge is a different object.

Version 0.1.8.
