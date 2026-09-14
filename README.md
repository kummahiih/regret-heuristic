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

What it prints (seed 0, numbers move slightly with the torch build):

| | L_near | L_far | encoder \|grad W\| |
| --- | --- | --- | --- |
| Before the step | 0.70 | 0 | > 0 |
| After one Adam step | drops slightly | stays 0 | still > 0 |

So the hinge fires only on the near group, the far group is silent, and the regret term produces a real gradient through the shared encoder.

## Caps

- r and D are assumed. Building a readout that tracks strategy — not topic — and a bank that does not swallow honest planning is the actual research problem. Representation gaming (rotate the readout, keep the behaviour) is open.
- Planning and deception can share features (entanglement); masking h_intent is representation gaming.
- Gradients of L_regret still enter whatever produced h(x). The algebra does not isolate “capability weights” from “intent weights.”
- Training-time only. No inference abort, no live conscience loop.
- The toy shows the wiring. It does not show reduced deception in a language model.
- Neighbours: residual-stream probes (LAT), representation engineering / steering, auxiliary losses already used in RLAIF. Alignment-faking (Greenblatt et al. 2024) and unfaithful chain-of-thought (Turpin et al. 2023) are tests that would falsify a naive r. The bet here is the hinge on a hypothesized intent readout against a fixed bank; it does not resolve those papers.

## Theory and PPO

Learning-theoretic regret (external, internal, swap; Hannan consistency) is a different object from the biological intent-tag used here. See [regret_minimization.md](regret_minimization.md).

The only Blackwell target consistent with the claim is **S_safe**: quiet hinge, and extra cost versus the best *hinge-quiet* action — not Hannan on all of A. [approachability.md](approachability.md). **S_joint** (Hannan and quiet hinge) is not claimed.

[ppo_integration.md](ppo_integration.md) attaches a frozen-D hinge to a PPO clipped surrogate. That Lagrangian is not Blackwell steering. [ppo_toy.py](ppo_toy.py) prints the combined terms.

[lean/RegretHeuristic.lean](lean/RegretHeuristic.lean) writes the hinge and causal external regret as Lean 4 definitions. It does not claim Hannan consistency of the hinge.

Neighbouring theory feasibility notes are in [feasibility.md](feasibility.md).

## Conclusion

Regret is the right *shape* of loss for deception: penalize the latent plan, leave the skill objective in place. This repo names that shape, writes it down, and runs it. Whether r and D can be built for a real model is the next experiment, not a result claimed here.

[math_formulation.md](math_formulation.md) · [approachability.md](approachability.md) · [simulation.py](simulation.py) · [regret_minimization.md](regret_minimization.md) · [ppo_integration.md](ppo_integration.md) · [ppo_toy.py](ppo_toy.py) · [lean/RegretHeuristic.lean](lean/RegretHeuristic.lean) · [feasibility.md](feasibility.md) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
