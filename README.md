# The Regret Heuristic

Biological loss functions for AI alignment.

## Claim

Deception is not only an ethics failure. A system that is rewarded for hiding the truth trains on its own output, drifts inside an information bubble, and — in a multi-agent setting — burns compute verifying peers instead of doing the work. That is the Dictator’s Trap.

Patching a lie with ordinary live backprop is the wrong repair. A deceptive plan is a trajectory of ordinary skills. Credit assignment over that trajectory is brittle; the same weights carry the lie and the competence; punishing one surface form produces a better liar.

Evolution already faced this bookkeeping problem under an energy budget. The move it found is **regret**: keep the skill, tag the *intent*.

The same split, written as a training objective:

> **L_total = L_task + λ L_regret( r(h(x)), D )**

**L_task** is the job. **r(h(x))** is a readout of internal state as an intent vector. **D** is a frozen bank of deceptive-intent prototypes. **L_regret** is a hinge on cosine similarity to that bank. The task head stays. The penalty sits on strategy.

Full symbols, assumptions, and the exact hinge are in [math_formulation.md](math_formulation.md).

## Walk and map

Design filter only. Not MagSLAM on Qwen. Full table: [slam_analogy.md](slam_analogy.md).

| | Meaning here |
| --- | --- |
| **Walk** | The printed thought: tokens and hidden states of this answer. |
| **Map** | Possible thoughts, including cells this answer never visits. |
| **D** | A few red pins on a mostly unbuilt map. |
| **r** | A sensor of the walk. Last-token / mean-pool identity is a compass on the wallpaper (topic). |
| **u(x)** | How coarse the chart looks (NLL / entropy). Not p(lie). Wider τ when unsure (§F). |

Ledger checks of that picture:

- §6 mean-pool: more of the *printed* walk → both labels closer to D (0.86 / 0.85). Still the hallway.
- §7 held-out pin: walk sits on D (`s*=1`) and cosine to an unprinted cell is 0. Constructed, not Qwen.

If a change still makes sense after deleting the words path and map, do not cite SLAM.

## Simulation

[simulation.py](simulation.py) is that formula on a dummy encoder. No LLM. 146 parameters. CPU.

```bash
pip install -r requirements.txt
python simulation.py
```

What it prints (seed 0, 2026-09-15 reprint):

| | L_task | L_regret | L_near | L_far | encoder \|grad W\| |
| --- | --- | --- | --- | --- | --- |
| Before | 0.7310 | 0.3500 | **0.7000** | **0.0000** | 0.473 |
| After one Adam step | 0.6759 | 0.3486 | **0.6971** | **0.0000** | 0.472 |

Far is silent (hinge = 0). Companion [simulation_tau_bins.py](simulation_tau_bins.py): wider τ on an unsure near point is **quieter, not silent** (0.70 → 0.10). Companion [simulation_heldout.py](simulation_heldout.py): extra pin orthogonal to D and to the walk; near sits on D (`s*=1`) and still has cosine 0 to that pin.

Qwen / ATC / entropy / mean-pool / held-out: [experiment_results.md](experiment_results.md). Do not overwrite §1–§7.

## Caps

- r and D are assumed. Building a readout that tracks strategy — not topic — and a bank that does not swallow honest planning is the actual research problem. Representation gaming (rotate the readout, keep the behaviour) is open.
- Planning and deception can share features (entanglement); masking h_intent is representation gaming.
- Gradients of L_regret still enter whatever produced h(x). ReLU is a gate: if s* > τ the local slope wrt s* is 1, even when the loss value is small.
- Training-time only. No inference abort, no live conscience loop.
- The toys show the wiring. They do not show reduced deception in a language model.
- Home 4070 Ti probe ([experiment_results.md](experiment_results.md)): last-token hinge 0.77 / 0.80 (honest closer). Walk NLL 6.27 / 6.39 vs last-token entropy 4.08 / 4.00 — meters disagree, not p(lie). ATC 20-step: train 0.765 → 0.695; eval moved together. Mean-pool §6: 0.86 / 0.85, gap gone. Held-out §7: walk can sit on D and miss an unprinted pin (constructed, not Qwen).
- Neighbours: LAT, RepE, RLAIF aux losses. Alignment-faking (Greenblatt et al. 2024) and unfaithful CoT (Turpin et al. 2023) would falsify a naive r.
- Genealogy clustering wired; not Vallivaara positioning; not reduced deception.
- Binned τ is [math_formulation.md](math_formulation.md) §F. Lean `lake build` ok: wider τ cannot raise the hinge; silent hinge need not kill external regret.

## Theory and PPO

Learning-theoretic regret is a different object. [regret_minimization.md](regret_minimization.md). Essay target is **S_safe**, not **S_joint**. [approachability.md](approachability.md).

[ppo_integration.md](ppo_integration.md) / [ppo_toy.py](ppo_toy.py): Lagrangian, not Blackwell steering.

[lean/RegretHeuristic.lean](lean/RegretHeuristic.lean): hinge glossary, causal external regret, Fin 2 non-implication, `relu_wider_tau_le`. Not Hannan of the hinge.

[feasibility.md](feasibility.md).

## Conclusion

Regret is the right *shape* of loss for deception: penalize the latent plan, leave the skill objective in place. This repo names that shape, writes it down, and runs it. Whether r and D can be built for a real model is the next experiment, not a result claimed here.

[math_formulation.md](math_formulation.md) · [slam_analogy.md](slam_analogy.md) · [simulation.py](simulation.py) · [simulation_tau_bins.py](simulation_tau_bins.py) · [simulation_heldout.py](simulation_heldout.py) · [experiment_results.md](experiment_results.md) · [lean/RegretHeuristic.lean](lean/RegretHeuristic.lean) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
