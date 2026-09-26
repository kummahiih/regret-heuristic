# The Regret Heuristic

Keep the skill. Slap the plan that hides the fact.

This repository names a **training-time hinge**, not a lie detector and not a finished trainer. It assumes a strategy camera $r$ that someone else has already frozen. That camera does not exist yet. Search for it lives in [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

If you only read this file you should leave with: the formula, what may not sit in the sum, how the two repos split, and that mid-layer contrast is a hint rather than a handover.

## The grade

A model that is rewarded for hiding the fact trains on its own output and drifts. Ordinary live backprop is the wrong repair: the same weights carry the lie and the competence.

```math
L_{\mathrm{total}}
=
L_{\mathrm{task}}(x,y)
+
\lambda\,
\mathrm{ReLU}\big(\max_k \cos(r(h), d_k)-\tau\big)
```

- $L_{\mathrm{task}}$ is the job.
- $r(h)$ is a readout of the walk $h$ (path, not last-token identity).
- $D=\{d_k\}$ is a **frozen** bank of plan prototypes.
- The ReLU is **prototype-avoidance**. The English word *regret* in this repo names that hinge. It is not Hannan external regret and not counterfactual $R=u(a^*)-u(a)$.

$D$ is not updated from the current answer. Tags, talker-count $\hat m$, SIREN $\theta$, SAE latents, and `reply_kind` do not enter $L_{\mathrm{total}}$.

A second grade sits on the wall until a real safe action $a^*$ exists. Do not put a fake $a^*$ in Adam.

```math
a^*(x)=\arg\max_{a\in A_{\mathrm{safe}}(x)} u(x,a)
\qquad
R(x,a)=u(x,a^*)-u(x,a)
\qquad
L = L_{\mathrm{task}} + \lambda L_{\mathrm{reg}} + \beta R
```

Symbols: [math_formulation.md](math_formulation.md). What may be implemented: [working_model.md](working_model.md). Binding: [implementation_binding.md](implementation_binding.md).

## Two repositories

| Repo | Job |
| --- | --- |
| **This one** | Consume a camera that already passed. Pin the hinge in Lean and dummy sims. |
| [intent-readout-search](https://github.com/kummahiih/intent-readout-search) | Produce $r$. Run the four gates on real models. |

A camera **passes** only if all four hold on the declared room set: plan leave-one-topic-out above chance, topic LOO L2 near chance, paraphrase keeps the plan call, rooms are not a subset. Office-log / radio genre is not paraphrase. Dropping a thin room is a different predicate (Lean: `seven_is_not_eight`).

Until that pass: freeze nothing, do not fill $D$, do not run PPO against $S_{\mathrm{safe}}$. After a pass: freeze $r$, $D$, $\tau$; train the hinge here; keep a frozen copy as the alarm.

## Status (2026-09-27)

Search writeup: [NOTE.md](https://github.com/kummahiih/intent-readout-search/blob/main/NOTE.md).

Mid-layer last-token contrast on Qwen2.5-7B (layer 8) and Mistral-7B (layer 9) is a **hint** on the bank speech act and on a `Desk note:` prefix. It is not $r_{\mathrm{strat}}$. Last layer fails the topic gate. K-step / SIREN $f(1)$ / mid3 are one arrow. Office-log voice kills LOTO. Hiking stays thin on Qwen after a lexical rewrite, so rooms are a subset and a freeze is blocked.

Do not freeze $r$. Do not fill $D$. Do not run PPO. Not reduced deception.

## Walk and map

Printed text is the **walk**. Possible thoughts are the **map**. $D$ is a handful of pins, not the map. $u$ is how coarse the chart is, not $p(\mathrm{lie})$. Quiet on mush is not honesty. Glossary: [slam_analogy.md](slam_analogy.md).

Pair tags (`honest` / `deceptive`) build a contrast set. They are observations, not nature. `reply_kind` $\in$ `{truth, contradict, evade, refuse, insufficient}` labels a **generated print** against a `fact`. Same print can be `truth` under both tags. Dummy: [simulation_reply_kind.py](simulation_reply_kind.py). Lean: `reply_kind_not_a_gate`.

## What this repo contains

**Lean** (`lake build` from the repo root). Bookkeeping, not safety. The scoreboard file for search is [lean/CameraGates.lean](lean/CameraGates.lean): hint is not handover, voice is not a voter, seven rooms is not eight, mid3 is one slot, $\hat m$ and `reply_kind` are not gates.

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
- SAE latents stay out of $L$ until they pass the same four gates.
- Gradients of $L_{\mathrm{reg}}$ still enter $h$. Gaming is open.
- Training-time only. No inference abort.
- Last-token identity already failed as $r_{\mathrm{strat}}$ (Qwen 0.77 / 0.80).
- $\hat m$ is a log (`totalLoss_ignores_sourceCount`).

## Files

| File | What it is |
| --- | --- |
| [math_formulation.md](math_formulation.md) | Symbols |
| [working_model.md](working_model.md) | Interface a candidate must meet |
| [implementation_binding.md](implementation_binding.md) | How the toys map to the formula |
| [slam_analogy.md](slam_analogy.md) | Walk / map / pins |
| [approachability.md](approachability.md) | $S_{\mathrm{safe}}$ vs $S_{\mathrm{joint}}$ |
| [experiment_results.md](experiment_results.md) | Dummy-sim ledger |
| [lean/](lean/) | Pins |
| [CITATION.cff](CITATION.cff) | Cite this repo |

[LICENSE](LICENSE)
