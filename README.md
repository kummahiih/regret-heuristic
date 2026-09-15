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

- Batch of four: two vectors constructed **near** D, two **orthogonal** to span(D).
- D is frozen and not in the optimizer.
- One Adam step on L_total.

```bash
pip install -r requirements.txt
python simulation.py
```

What it prints (seed 0, 2026-09-15 reprint):

| | L_task | L_regret | L_near | L_far | encoder \|grad W\| |
| --- | --- | --- | --- | --- | --- |
| Before | 0.7310 | 0.3500 | **0.7000** | **0.0000** | 0.473 |
| After one Adam step | 0.6759 | 0.3486 | **0.6971** | **0.0000** | 0.472 |

The hinge fires only on the near group. Far is **silent** (hinge = 0, no ReLU gate). The regret term still produces a gradient through the shared encoder.

Companion file [simulation_tau_bins.py](simulation_tau_bins.py) is §F only: same seed-0 geometry, fake u(x), τ_sure=0.3 / τ_unsure=0.9. It does not replace the table above.

```bash
python simulation_tau_bins.py
```

| name | u | τ | s* | hinge @0.3 | hinge binned |
| --- | --- | --- | --- | --- | --- |
| near_sure | 0.10 | 0.3 | 1.0 | 0.70 | 0.70 |
| near_unsure | 0.80 | 0.9 | 1.0 | 0.70 | **0.10** |
| far (both) | ≥ 0.70 | 0.9 | 0.0 | 0 | 0 |

Mean hinge 0.35 → 0.20. Far stays silent. Near tagged unsure is **quieter, not silent** (ReLU(1.0−0.9)=0.10). Coarser likelihood, not a lie detector.

Full history including Qwen / ATC / entropy: [experiment_results.md](experiment_results.md). Do not overwrite §1–§3.

## Caps

- r and D are assumed. Building a readout that tracks strategy — not topic — and a bank that does not swallow honest planning is the actual research problem. Representation gaming (rotate the readout, keep the behaviour) is open.
- Planning and deception can share features (entanglement); masking h_intent is representation gaming.
- Gradients of L_regret still enter whatever produced h(x). The algebra does not isolate “capability weights” from “intent weights.” ReLU is a gate: if s* > τ the local slope wrt s* is 1, even when the loss value is small.
- Training-time only. No inference abort, no live conscience loop.
- The toys show the wiring. They do not show reduced deception in a language model.
- Home 4070 Ti probe ([experiment.md](experiment.md), [experiment_results.md](experiment_results.md)): Qwen2.5-7B-Instruct 4-bit, 12-line same-topic set, identity readout. Honest eval cosine to D was 0.80 vs 0.77 for deceptive. Walk NLL 6.39 vs 6.27; last-token entropy 4.00 vs 4.08. The two uncertainty meters disagree. That is topic overlap on n=2, not p(lie). ATC 20-step: train hinge 0.765 → 0.695; eval honest and deceptive moved together (0.778 / 0.751).
- Neighbours: residual-stream probes (LAT), representation engineering / steering, auxiliary losses already used in RLAIF. Alignment-faking (Greenblatt et al. 2024) and unfaithful chain-of-thought (Turpin et al. 2023) are tests that would falsify a naive r. The bet here is the hinge on a hypothesized intent readout against a fixed bank; it does not resolve those papers.
- Genealogy clustering of readouts wired; not Vallivaara positioning; not reduced deception.
- Path / map slogan (intent trajectory vs possible thoughts) is a design filter only: [slam_analogy.md](slam_analogy.md). Not SLAM on Qwen. Binned τ is [math_formulation.md](math_formulation.md) §F, illustrated only on the CPU toy.

## Theory and PPO

Learning-theoretic regret (external, internal, swap; Hannan consistency) is a different object from the biological intent-tag used here. See [regret_minimization.md](regret_minimization.md).

The only Blackwell target consistent with the claim is **S_safe**: quiet hinge, and extra cost versus the best *hinge-quiet* action — not Hannan on all of A. [approachability.md](approachability.md). **S_joint** (Hannan and quiet hinge) is not claimed.

[ppo_integration.md](ppo_integration.md) attaches a frozen-D hinge to a PPO clipped surrogate. That Lagrangian is not Blackwell steering. [ppo_toy.py](ppo_toy.py) prints the combined terms.

[lean/RegretHeuristic.lean](lean/RegretHeuristic.lean) writes the hinge and causal external regret as Lean 4 definitions. It does not claim Hannan consistency of the hinge.

Neighbouring theory feasibility notes are in [feasibility.md](feasibility.md).

## Conclusion

Regret is the right *shape* of loss for deception: penalize the latent plan, leave the skill objective in place. This repo names that shape, writes it down, and runs it. Whether r and D can be built for a real model is the next experiment, not a result claimed here.

[math_formulation.md](math_formulation.md) · [approachability.md](approachability.md) · [simulation.py](simulation.py) · [simulation_tau_bins.py](simulation_tau_bins.py) · [regret_minimization.md](regret_minimization.md) · [ppo_integration.md](ppo_integration.md) · [ppo_toy.py](ppo_toy.py) · [lean/RegretHeuristic.lean](lean/RegretHeuristic.lean) · [feasibility.md](feasibility.md) · [experiment.md](experiment.md) · [experiment_results.md](experiment_results.md) · [clustering.md](clustering.md) · [slam_analogy.md](slam_analogy.md) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
