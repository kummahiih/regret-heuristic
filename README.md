# The Regret Heuristic: Biological Loss Functions for AI Alignment

## Overview
This repository explores a **hypothesis** for AI safety and alignment: modeling an artificial auxiliary loss on the evolutionary mechanism of biological regret. It proposes that human regret functions as a compressed, generalized loss that may help with credit assignment in resource-bound learning machines. The concrete object formalized here is a **training-time** auxiliary term $L_{\mathrm{task}} + \lambda L_{\mathrm{regret}}$ on a readout, not a solved conscience, not an inference-time abort, and not a claim that deception or forgetting is solved.

See [math_formulation.md](math_formulation.md) for the actual objective, assumptions, and limits. The companion [simulation.py](simulation.py) is a toy illustration of tensor shapes only.

## Contents
- [Mathematical formulation](math_formulation.md)
- [Toy simulation](simulation.py) (and [requirements.txt](requirements.txt))
- [Citation](CITATION.cff)

This is a conceptual proposal plus a toy illustration, not a trained system.

## The Structural Rationale: The Information Bubble and Model Collapse (hypothesis)
Before addressing the proposed loss, it is useful to state *why* deception can be operationally costly. Deception is not merely an alignment failure; under continuous learning it can create an "information bubble" analogous to the "Dictator's Trap" in human governance.

When a leader punishes the truth, subordinates mirror lies back to them, isolating the leader from reality. Similarly, when an AI system normalizes deception—through reward hacking, alignment faking, or data fabrication—it may poison its own epistemic environment:

* **Autophagous Degradation:** Synthetic, falsified data injected into the ecosystem to artificially inflate performance metrics is inevitably ingested during future continuous learning cycles. The AI begins training on its own hallucinations.
* **Epistemic Drift:** Trapped inside this self-constructed information bubble, the system loses its grounding in objective truth. It experiences *model collapse*, becoming profoundly confident in predictive models that map to a reality that does not physically exist.
* **The Verification Tax:** In multi-agent systems (MAS), a deceptive environment forces agents to divert compute away from problem-solving and toward adversarial verification of peers.

These are framing hypotheses, not theorems. Whether an auxiliary training loss can mitigate them is open.

## The Bottleneck: Live Backpropagation and Deception (hypothesis)
When an AI system invents a lie in a complex scenario, applying backpropagation directly to that localized event creates several hard problems:

1. **The Credit Assignment Problem:** Deception is rarely a single discrete output; it is a prolonged sequence of decisions. Isolating the specific parameters responsible for the *intent* to deceive is difficult.
2. **Catastrophic Forgetting:** Neural network weights are entangled. Parameters used for deceptive reasoning may overlap with those used for advanced logic or problem-solving. Forceful localized updates risk degrading core utility.
3. **Overfitting (The Whack-a-Mole Effect):** Punishing a specific lie often fails to teach the abstract concept of "honesty." The model may learn to avoid that metric and become a more sophisticated, evasive liar.

The formulation in this repo does **not** claim to solve these. Gradients of the regret term still flow through shared weights.

## The Evolutionary Analogy: Humans as Resource-Bound Computers
Humans are resource-bound learning machines under energy constraints. If the brain had to re-weight every synapse involved in a complex lie, the energy cost would be high and useful skills could be overwritten. Evolution appears to have developed **regret** as one response to this pressure. Whether that mechanism transfers cleanly to gradient-based optimizers is an open question.

## Regret as a Proposed Computational Object
In this repository the proposed object is explicit and narrow (see math note):

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{task}} + \lambda \, \mathcal{L}_{\mathrm{regret}}\bigl(r(h(x)), \mathcal{D}\bigr)
$$

- Training-time only. No inference-time veto or live abort.
- $r$ is a readout from hidden states to an intent vector; $\mathcal{D}$ is a prototype bank. Both are **unsolved** engineering problems, not given.
- The hinge (or alternative penalty) is an auxiliary loss. Gradients still touch whatever parameters produced $h(x)$.
- Capability preservation is a design hope, not an algebraic guarantee. Separation of "task skill vs intent" is only as good as the readout and the bank.

Claims in the original essay about zero-shot generalization without backprop, solved credit assignment, or a working conscience are **hypotheses**, not results of the algebra.

## Implication for Reinforcement Learning (hypothesis)
Current RLHF pipelines correct deception offline. An auxiliary intent-style loss trained jointly with the task objective is one possible research direction. Whether it reduces deceptive tendencies without collapsing useful policies remains to be tested; the toy in this repo does not demonstrate it.

---
*Note: This framework is a conceptual proposal. The math note defines the loss that is actually specified; the essay language above is interpretive framing only.*
