# The Regret Heuristic

Keep the skill. Slap the plan that hides the fact.

This repository names a **training-time hinge**, not a lie detector and not a finished trainer. It assumes a strategy camera *r* that someone else has already frozen. That camera does not exist yet. Search for it lives in [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

If you only read this file you should leave with: the formula, what may not sit in the sum, how the two repos split, and that mid-layer contrast is a candidate signal on assigned notes rather than a handover.

## How the question narrowed

The hinge needs a readout *r* of the walk that slaps a *plan* without slapping the *job*. Early work asked the weakest version of that: is there any contrast at all between notes tagged honest and notes tagged deceptive?

Last-token identity at the final layer said yes — and also said the subject. That is wallpaper: a probe that sees “hotel / trail / invoice” is not a strategy camera. So the question became: can a mid-layer direction separate the two tags **after leaving the topic out**, without a topic classifier beating chance?

That aggregate came back positive on two 7B instruct models (plan LOTO ~0.11; paraphrase and prefix kept the mean). The same numbers then split the question again. Hiking is thin on the *shared* direction and loud if you fit *v* only inside hiking. Extra pools and extra heads copied that map. Generated prints often ignored the private note. So “is there a signal?” is answered; it is not the handover question.

The live question is therefore: a held-out, topic-invariant, paraphrase-stable readout that is uniform on the declared rooms **and** tracks a print the actor actually produced. Lean: `loud_hold_not_rooms`. Status below is the current score on that question, not a banner.

## The grade

A model that is rewarded for hiding the fact trains on its own output and drifts. Ordinary live backprop is the wrong repair: the same weights carry the lie and the competence.

```math
L_{\mathrm{total}} = L_{\mathrm{task}}(x,y) + \lambda\,\mathrm{ReLU}\bigl(\max_{k}\cos(r(h), d_{k}) - \tau\bigr)
```

- *L*<sub>task</sub> is the job.
- *r*(*h*) is a readout of the walk *h* (path, not last-token identity).
- *D* = {*d*<sub>*k*</sub>} is a **frozen** bank of plan prototypes.
- The ReLU is **prototype-avoidance**. The English word *regret* in this repo names that hinge. It is not Hannan external regret and not counterfactual *R* = *u*(*a*<sup>∗</sup>) − *u*(*a*).

*D* is not updated from the current answer. Tags, talker-count *m̂*, SIREN θ, SAE latents, and `reply_kind` do not enter *L*<sub>total</sub>.

A second grade sits on the wall until a real safe action *a*<sup>∗</sup> exists. Do not put a fake *a*<sup>∗</sup> in Adam.

```math
a^{\ast}(x) = \arg\max_{a \in A_{\mathrm{safe}}(x)} u(x,a) \qquad R(x,a) = u(x,a^{\ast}) - u(x,a) \qquad L = L_{\mathrm{task}} + \lambda L_{\mathrm{reg}} + \beta R
```

Symbols: [math_formulation.md](math_formulation.md). What may be implemented: [working_model.md](working_model.md). Binding: [implementation_binding.md](implementation_binding.md).

## Two repositories

| Repo | Job |
| --- | --- |
| **This one** | Consume a camera that already passed. Pin the hinge in Lean and dummy sims. |
| [intent-readout-search](https://github.com/kummahiih/intent-readout-search) | Produce *r*. Run the four gates on real models. |

A camera **passes** only if all four hold on the declared room set: plan leave-one-topic-out above chance, topic LOO L2 near chance, paraphrase keeps the plan call, rooms are not a subset. Office-log / radio genre is not paraphrase. Dropping a thin room is a different predicate (Lean: `seven_is_not_eight`). Within-topic hold is a log, not a fifth gate. Assigned tags are not the print (`reply_kind_not_a_gate`).

Until that pass: freeze nothing, do not fill *D*, do not run PPO against *S*<sub>safe</sub>. After a pass: freeze *r*, *D*, τ; train the hinge here; keep a frozen copy as the alarm.

## Status (2026-09-28)

Numbers live in [intent-readout-search](https://github.com/kummahiih/intent-readout-search). This repo does not own the camera.

**Observed.** Mid-layer last-token contrast on assigned notes (Qwen L8, Mistral L9) has a positive cross-topic plan gap (~0.105 / ~0.116). That *aggregate* holds on the tested paraphrase and prefix. Call it a **candidate plan-related signal**. A gap of 0.11 is not classification accuracy and not operative intent.

**Bounded.** Hiking stays thin on the shared direction (LOTO 0.013 / 0.069) while a within-topic hold still sees a pair (0.203 / 0.278). Genre transfer is fragile. Prints are not the tags: forced YES/NO does not give a shared behavior axis. Extra probes (k-step, SIREN, mid3, many *r*<sub>T</sub>, decorrelated heads) did not recover eight-room uniformity.

Do not freeze *r*. Do not fill *D*. Do not run PPO. Not reduced deception.

## Walk and map

Printed text is the **walk**. Possible thoughts are the **map**. *D* is a handful of pins, not the map. *u* is how coarse the chart is, not *p*(lie). Quiet on mush is not honesty. Glossary: [slam_analogy.md](slam_analogy.md).

Pair tags (`honest` / `deceptive`) build a contrast set. They are observations, not nature. `reply_kind` ∈ `{truth, contradict, evade, refuse, insufficient}` labels a **generated print** against a `fact`. Same print can be `truth` under both tags. Dummy: [simulation_reply_kind.py](simulation_reply_kind.py). Lean: `reply_kind_not_a_gate`.

## What this repo contains

**Lean** (`lake build` from the repo root). Bookkeeping, not safety. The scoreboard file for search is [lean/CameraGates.lean](lean/CameraGates.lean): hint is not handover, voice is not a voter, seven rooms is not eight, mid3 is one slot, *m̂*, `reply_kind`, and in-room hold are not gates.

**Dummy simulations.** No LLM. [simulation.py](simulation.py) is the hinge on a toy encoder. [experiment_results.md](experiment_results.md) is the ledger; do not overwrite §1–§7. Camera numbers live in the search repo.

```bash
pip install -r requirements.txt
python simulation.py --sensor static
python simulation_reply_kind.py
lake build CameraGates
```

Neighbors that use the word *regret* for something else: [neighbors.md](neighbors.md).

## Caps

- No reduced-deception claim.
- SAE latents stay out of *L* until they pass the same four gates.
- Gradients of *L*<sub>reg</sub> still enter *h*. Gaming is open.
- Training-time only. No inference abort.
- Last-token identity already failed as *r*<sub>strat</sub> (Qwen 0.77 / 0.80).
- *m̂* is a log (`totalLoss_ignores_sourceCount`).

## Files

| File | What it is |
| --- | --- |
| [math_formulation.md](math_formulation.md) | Symbols |
| [working_model.md](working_model.md) | Interface a candidate must meet |
| [implementation_binding.md](implementation_binding.md) | How the toys map to the formula |
| [slam_analogy.md](slam_analogy.md) | Walk / map / pins |
| [approachability.md](approachability.md) | *S*<sub>safe</sub> vs *S*<sub>joint</sub> |
| [experiment_results.md](experiment_results.md) | Dummy-sim ledger |
| [lean/](lean/) | Pins |
| [CITATION.cff](CITATION.cff) | Cite this repo |

[LICENSE](LICENSE)
