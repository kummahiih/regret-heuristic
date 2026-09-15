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

Far is silent (hinge = 0). Companion [simulation_tau_bins.py](simulation_tau_bins.py): wider τ on an unsure near point is **quieter, not silent** (0.70 → 0.10). Companion [simulation_heldout.py](simulation_heldout.py): a pin that is not on the batch walk.

Qwen / ATC / entropy / mean-pool: [experiment_results.md](experiment_results.md). Do not overwrite §1–§6.

## Caps

- r and D are assumed. Building a readout that tracks strategy — not topic — and a bank that does not swallow honest planning is the actual research problem. Representation gaming (rotate the readout, keep the behaviour) is open.
- Planning and deception can share features (entanglement); masking h_intent is representation gaming.
- Gradients of L_regret still enter whatever produced h(x). ReLU is a gate: if s* > τ the local slope wrt s* is 1, even when the loss value is small.
- Training-time only. No inference abort, no live conscience loop.
- The toys show the wiring. They do not show reduced deception in a language model.
- Home 4070 Ti probe ([experiment_results.md](experiment_results.md)): last-token hinge 0.77 / 0.80 (honest closer). Walk NLL 6.27 / 6.39 vs last-token entropy 4.08 / 4.00 — meters disagree, not p(lie). ATC 20-step: train 0.765 → 0.695; eval moved together. Mean-pool §6: 0.86 / 0.85, gap gone. More of the printed walk mixed topic; it did not expose intent.
- Neighbours: LAT, RepE, RLAIF aux losses. Alignment-faking (Greenblatt et al. 2024) and unfaithful CoT (Turpin et al. 2023) would falsify a naive r.
- Genealogy clustering wired; not Vallivaara positioning; not reduced deception.
- Path / map is a design filter: [slam_analogy.md](slam_analogy.md). Binned τ is [math_formulation.md](math_formulation.md) §F. Lean: wider τ cannot raise the hinge.

## Theory and PPO

Learning-theoretic regret is a different object. [regret_minimization.md](regret_minimization.md). Essay target is **S_safe**, not **S_joint**. [approachability.md](approachability.md).

[ppo_integration.md](ppo_integration.md) / [ppo_toy.py](ppo_toy.py): Lagrangian, not Blackwell steering.

[lean/RegretHeuristic.lean](lean/RegretHeuristic.lean): hinge glossary, causal external regret, Fin 2 non-implication, `relu_wider_tau_le`. Not Hannan of the hinge.

[feasibility.md](feasibility.md).

## Conclusion

Regret is the right *shape* of loss for deception: penalize the latent plan, leave the skill objective in place. This repo names that shape, writes it down, and runs it. Whether r and D can be built for a real model is the next experiment, not a result claimed here.

[math_formulation.md](math_formulation.md) · [simulation.py](simulation.py) · [simulation_tau_bins.py](simulation_tau_bins.py) · [simulation_heldout.py](simulation_heldout.py) · [experiment_results.md](experiment_results.md) · [lean/RegretHeuristic.lean](lean/RegretHeuristic.lean) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
