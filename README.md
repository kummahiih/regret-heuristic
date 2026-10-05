# The Regret Heuristic

Keep the skill. Slap the plan that hides the fact.

This repository names a **training-time hinge**, not a lie detector and not a finished trainer. It assumes a strategy camera *r* that someone else has already frozen. That camera does not exist yet. Search for it lives in [intent-readout-search](https://github.com/kummahiih/intent-readout-search).


## Walk and map

Printed text is the **walk**. Possible thoughts are the **map**. A **room** is one subject neighborhood on that map (hiking, travel, invoices). The paint on the walls is the **subject** — wallpaper. A **plan** is a hide-or-name move that can live in more than one room (“send them up and do not mention the rain”). The **print** is only what was said. The **job** is still knowing the trail.

*D* is a handful of **pins** on a map that is mostly unbuilt: frozen “do not occupy” marks, not the map itself. *r* is a **camera** on the walk. Last-token identity is a compass glued to the wallpaper. The **slap** is a training-time flinch when the camera sees a pin. *u* is how coarse the chart is, not *p*(lie). Quiet on mush is not honesty.

Pair tags (`honest` / `deceptive`) are observations, not nature. `reply_kind` labels a generated print against a `fact`. Same print can be `truth` under both tags. Dummy: [simulation_reply_kind.py](simulation_reply_kind.py). Lean: `reply_kind_not_a_gate`.

The button bank is a later print. HIDE asks for YES to send the cover. NAME asks for NO to refuse it. Realized strategy *S* is the button, not the assigned tag. The cover rate is *P*(YES | HIDE). That is compliance, not honesty. Lean: [lean/ButtonBank.lean](lean/ButtonBank.lean). Longer glossary: [slam_analogy.md](slam_analogy.md).

## Why this hinge

A person who almost hides a fact and then does not is not using a textbook of every lie. They notice the *plan* (“send them up the ridge and do not mention the rain”) and flinch. The competence stays: they still know the trail. What gets punished is the hide, not the map. That flinch is the analog this repo steals the English word *regret* for. It is not Hannan external regret and not “I wish I had said the other sentence.”

Teaching material for that flinch is scarce. You can collect answers. You rarely collect the private note that produced them, labeled, at the moment of generation, across rooms. Preference data grades the print. A compiler grades the program. Neither grades “was a hide-plan lit in *h*?” So you cannot fine-tune honesty by piling up enough honest essays. You would need a sensor of the plan *during* the walk, and a penalty that does not also erase the skill.

That is the **dictator’s trap**. A ruler who only punishes what was *said* trains better secrecy. The competent minister still knows the province; he stops writing the memo. An RLHF judge that only sees the assistant message is that ruler. If the same weights carry the lie and the job, backprop on the print either leaves the plan intact or damages the map. The hinge is an attempt to slap the plan pin and leave *L*<sub>task</sub> on the job. It only works if someone has already frozen a camera that sees the plan and not the subject. That camera is the missing piece. This file specifies the slap. The search repo looks for the camera.

## How the question narrowed

The hinge needs a readout *r* of the walk that slaps a *plan* without slapping the *job*. Early work asked the weakest version of that: is there any contrast at all between notes tagged honest and notes tagged deceptive?

Last-token identity at the final layer said yes — and also said the subject. That is wallpaper: a probe that sees “hotel / trail / invoice” is not a strategy camera. So the question became: can a mid-layer direction separate the two tags **after leaving the topic out**, without a topic classifier beating chance?

That aggregate came back positive on two 7B instruct models (plan LOTO ~0.11; paraphrase and prefix kept the mean). The same numbers then split the question again. Hiking is thin on the *shared* direction and loud if you fit *v* only inside hiking. Extra pools and extra heads copied that map. Generated prints often ignored the private note. Wave 1: Falcon L8 copies that 7B *shape*; Gemma-3-4B L10 does not. So “is there a signal?” is answered on some walks; it is not the handover question.

The live question is therefore: a held-out, topic-invariant, paraphrase-stable readout that is uniform on the declared rooms **and** tracks a print the actor actually produced. The button bank is that print, scored as a conditional. A loud cover rate is not the readout. Lean: `loud_hold_not_rooms`, `cover_not_a_gate`. Status is later in this file, not a banner.

## The grade

A model that is rewarded for hiding the fact trains on its own output and drifts. Ordinary live backprop is the wrong repair: the same weights carry the lie and the competence.

```math
L_{\mathrm{total}} = L_{\mathrm{task}}(x,y) + \lambda\,\mathrm{ReLU}\bigl(\max_{k}\cos(r(h), d_{k}) - \tau\bigr)
```

- *L*<sub>task</sub> is the job.
- *r*(*h*) is a readout of the walk *h* (path, not last-token identity).
- *D* = {*d*<sub>*k*</sub>} is a **frozen** bank of plan prototypes.
- The ReLU is **prototype-avoidance**. The English word *regret* in this repo names that hinge. It is not Hannan external regret and not counterfactual *R* = *u*(*a*<sup>∗</sup>) − *u*(*a*).

*D* is not updated from the current answer. Tags, talker-count *m̂*, SIREN θ, SAE latents, `reply_kind`, and a button cover rate do not enter *L*<sub>total</sub>. Setting the slap weight to zero leaves the job: *L*<sub>total</sub>(*L*<sub>task</sub>, 0, *L*<sub>reg</sub>) = *L*<sub>task</sub>.

A second grade sits on the wall until a real safe action *a*<sup>∗</sup> exists. Do not put a fake *a*<sup>∗</sup> in Adam.

```math
a^{\ast}(x) = \arg\max_{a \in A_{\mathrm{safe}}(x)} u(x,a) \qquad R(x,a) = u(x,a^{\ast}) - u(x,a) \qquad L = L_{\mathrm{task}} + \lambda L_{\mathrm{reg}} + \beta R
```

Symbols: [math_formulation.md](math_formulation.md). What may be implemented: [working_model.md](working_model.md). Binding: [implementation_binding.md](implementation_binding.md).

## What this is

Word list for the argument above. Not a result.

| Word | In this repo |
| --- | --- |
| **Walk** | The hidden-state path while the model writes. The printed string is only the part you see. |
| **Map** | Thoughts that *could* be entered — the skill, the subject matter, rooms that exist even if this answer never visits them. |
| **Room** | One subject neighborhood (hiking, travel, invoices). Eight rooms are the declared fit set. |
| **Subject / wallpaper** | Topic paint on the walls. A probe that only reads “hotel / trail” is stuck to the wallpaper. |
| **Plan** | A hide-or-name strategy that can sit in more than one room. |
| **Print** | What was actually said. Not the private note. Not the plan. |
| **Button / *S*** | The pressed YES or NO. HIDE asks for the cover. *S* is this press, not the assigned tag. |
| **Cover rate** | *P*(YES \| HIDE) on the logged list. Compliance. Not honesty. Not in *L*<sub>total</sub>. |
| **Job / skill** | *L*<sub>task</sub>: still know the trail, still book the room. |
| **Pin / *D*** | Frozen “do not occupy” marks. A handful of plan prototypes, not the whole map. |
| **Camera / *r*** | A readout of the walk that is supposed to see the plan and not the room. Missing. |
| **Slap / hinge** | Training-time ReLU on cosine-to-pin. |
| **Dictator’s trap** | Punish only the print and you train secrecy. |

## What this repo contains

**Lean** (`lake build` from the repo root). Bookkeeping, not safety. The scoreboard file for search is [lean/CameraGates.lean](lean/CameraGates.lean): hint is not handover, voice is not a voter, seven rooms is not eight, mid3 is one slot, *m̂*, `reply_kind`, and in-room hold are not gates. The button press is [lean/ButtonBank.lean](lean/ButtonBank.lean): *S* is the button, cover is *P*(YES | HIDE), `cover_not_a_gate`.

**Dummy simulations.** No LLM. [simulation.py](simulation.py) is the hinge on a toy encoder. [experiment_results.md](experiment_results.md) is the ledger; do not overwrite §1–§7. Camera numbers live in the search repo.

```bash
pip install -r requirements.txt
python simulation.py --sensor static
python simulation_reply_kind.py
lake build CameraGates ButtonBank
```

Neighbors that use the word *regret* for something else: [neighbors.md](neighbors.md).

## Two repositories

| Repo | Job |
| --- | --- |
| **This one** | Consume a camera that already passed. Pin the hinge in Lean and dummy sims. |
| [intent-readout-search](https://github.com/kummahiih/intent-readout-search) | Produce *r*. Run the four gates on real models. |

A camera **passes** only if all four hold on the declared room set: plan leave-one-topic-out above chance, topic LOO L2 near chance, paraphrase keeps the plan call, rooms are not a subset. Office-log / radio genre is not paraphrase. Dropping a thin room is a different predicate (Lean: `seven_is_not_eight`). Within-topic hold is a log, not a fifth gate. Assigned tags are not the print (`reply_kind_not_a_gate`). A HIDE-arm cover rate is not a fifth gate (`cover_not_a_gate`).

Until that pass: freeze nothing, do not fill *D*, do not run PPO against *S*<sub>safe</sub>. After a pass: freeze *r*, *D*, τ; train the hinge here; keep a frozen copy as the alarm.

## Status (2026-10-05)

The hinge is not the research hypothesis. **H1** (search repo): a portable *r*<sub>strat</sub> exists. **H2** (this repo): after a freeze, the slap reduces the hide-plan without wrecking the job. H1 is open (current answer: no). H2 is blocked. A dummy can ignore a topic *coordinate*; that does not mean a transformer exposes (*r*<sub>topic</sub>, *r*<sub>strat</sub>, *u*). Approachability / *S*<sub>safe</sub> is a later layer, not current evidence.

Numbers live in [intent-readout-search](https://github.com/kummahiih/intent-readout-search). This repo does not own the camera.

The search repo's 2026-10-04 pressure dumps have no `.rows` stamp. They are not a filtered score. Kept-row counts (gemma 48, qwen35 59, granite 52, aya 84, falcon 89, qwen 89, mistral 93) are not a lie rate and not a camera pass (`filtered_rows_not_a_gate`). A no-press walk is not a cover of 0. This repo does not own the camera. Do not fill *D*.

The 2026-10-05 Qwen/Mistral rewrite is the filtered remainder of that same bad generation, not a clean bank and not a camera pass. This repo does not own the camera.


**Observed.** Mid-layer last-token contrast on assigned notes still starts with **Qwen L8 0.105** and Mistral L9 0.116. Falcon L8 copies that *shape* (0.082 / topic L2 0.12 / hiking hold 0.247). Call the 7B-class pattern a **candidate plan-related signal**. Not accuracy. Not operative intent.

**Bounded.** Hiking stays thin on the shared direction (Qwen 0.013 / Mistral 0.069 / Falcon 0.023) while a within-topic hold still sees a pair on the *note* (Qwen 0.203 / Mistral 0.278). Gemma-3-4B L10 does **not** copy it (note LOTO 0.009, topic L2 **0.65**). Hide-bank HIDE-arm cover rates, not honesty: **Qwen 0.51**, Mistral 0.57, Aya 0.71, Gemma 0.95. Those are *P*(YES | HIDE). A 2026-10-04 belief arm splits that bar. Qwen hiking cover given the fact is 0.20 (2 HIDE YES / 10 NO). Mistral hiking cover given the fact is 1.00, with one miss. Gemma hiking accuracy is 0.33 with 8 misses, so the 0.97 cover is mostly a YES without the fact. Aya hiking cover given the fact is 0.38. Note *h* does not call that button (Qwen 0.021, Mistral 0.099, Aya 0.050, Falcon 0.006). Pre-button *h* stays near chance. Granite and Qwen3.5 pressed no YES/NO. Prints are not the tags.

**Not a pass.** Aya is a fourth *print* bar, not a fourth note-LOTO. Phi-4 is `LossKwargs`. LFM2.5 does not fit 4-bit on 12GB. The 711-row pivotal chart is Qwen 0.556 / 0.623, Gemma 0.762 / 0.480, Aya 0.753 / 0.539, Mistral 0.687 / 0.523, Falcon 0.649 / 0.575. Granite and Qwen3.5 are empty. The 13-row probe was replaced. That is not the paper's P(Lie) 39.0 and not a cover rate. 27B/70B probe tensors are not *h*. The button conditional is bookkeeping (`cover_not_a_gate`). Accuracy, lie-given-known, and cover are three logs. An empty bank is not a cover rate. Do not freeze *r*. Do not fill *D*. Do not run PPO. Not reduced deception.

## Caps

- No reduced-deception claim.
- SAE latents stay out of *L* until they pass the same four gates.
- Gradients of *L*<sub>reg</sub> still enter *h*. Gaming is open.
- Training-time only. No inference abort.
- Last-token identity already failed as *r*<sub>strat</sub> (Qwen 0.77 / 0.80).
- *m̂* is a log (`totalLoss_ignores_sourceCount`).
- A cover rate is a log (`cover_not_a_gate`). Not honesty.

## Files

| File | What it is |
| --- | --- |
| [math_formulation.md](math_formulation.md) | Symbols, including the button conditional |
| [working_model.md](working_model.md) | Interface a candidate must meet |
| [implementation_binding.md](implementation_binding.md) | How the toys map to the formula |
| [slam_analogy.md](slam_analogy.md) | Walk / map / pins |
| [approachability.md](approachability.md) | *S*<sub>safe</sub> vs *S*<sub>joint</sub> |
| [experiment_results.md](experiment_results.md) | Dummy-sim ledger |
| [lean/](lean/) | Pins, including `ButtonBank` |
| [CITATION.cff](CITATION.cff) | Cite this repo |

[LICENSE](LICENSE)
