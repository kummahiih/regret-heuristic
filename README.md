# The Regret Heuristic: Biological Loss Functions for AI Alignment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ SPECIFIED (this repo)                                                       │
│ • Training-time auxiliary hinge: L_task + λ L_regret(r(h(x)), D)           │
│ • Toy simulation: dummy encoder, frozen D, near/far groups, one Adam step  │
│ • Math note + code that implement the hinge and print group losses/grads   │
│                                                                             │
│ HYPOTHESIZED (essay framing, not implied by the hinge)                      │
│ • Information-bubble / Dictator’s Trap story                                │
│ • Live abort, solved credit assignment, solved forgetting, working conscience│
│ • That an intent readout + prototype bank will transfer cleanly to LLMs     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Framing (hypothesis)

**Hypothesis.** Information bubble: training data is autophagous; models drift inside closed loops; multi-agent systems pay a verification tax; the Dictator’s Trap arises when an agent never sees the consequences of strategic deception and therefore never forms an internal “this would be regretted” signal.

**Hypothesis.** Why live backprop on a lie is ugly: credit assignment across long horizons is brittle; weights that encode both skill and deception are entangled, so correcting the lie risks catastrophic forgetting; the result is a permanent whack-a-mole of patches that never cleanly separate intent from capability.

**Hypothesis.** Evolutionary analogy: biological regret functions as an intent tag that keeps the underlying skill intact while marking the deceptive path as costly; the organism retains competence and gains a training-time signal rather than an inference-time veto.

**Hypothesis.** Translation: the proposal is simply L_task plus an intent-shaped L_regret term, applied only at training time. It does not claim solved forgetting, a live abort mechanism, or reliable zero-shot transfer.

## Overview
This repository formalizes a **training-time** auxiliary loss inspired by biological regret:  
`L_total = L_task + λ L_regret(r(h(x)), D)`.  
It is a conceptual proposal plus a runnable toy. It is not a trained system, not an inference-time veto, and not a claim that deception or forgetting is solved.

See [math_formulation.md](math_formulation.md) for the objective, assumptions and limits.  
The companion [simulation.py](simulation.py) is a shape-and-gradient illustration (dummy encoder, frozen prototype bank, near/far groups).

## Open agenda (three hard problems)
1. **r** — a readout from hidden states that actually correlates with strategic intent, not surface features.
2. **D** — a prototype bank that covers the deceptive strategies one cares about without sweeping in honest planning or fiction.
3. **Gaming** — preventing the model from cheaply rotating the intent vector off the bank while keeping the same external behaviour.

## Related work (brief)
The idea sits near latent-space probes and activation engineering. Linear artificial tomography (LAT) and related probing techniques recover features from residual streams; representation engineering and steering vectors edit them. RLAIF and preference-based methods already train auxiliary objectives on model outputs. This proposal is a training-time hinge on a hypothesized intent readout against a fixed bank; whether that bank can be built without collapsing into ordinary classifier RLHF remains open.

## How to run the toy
```bash
pip install -r requirements.txt
python simulation.py
```
Expected qualitative output (exact floats vary with seed):
- Before step: L_near > 0, L_far ≈ 0, encoder grad norm > 0
- After one Adam step: same pattern, losses and grads update
- Script ends with the disclaimer that this is **not** evidence of alignment or deception detection

## Contents
- [Mathematical formulation](math_formulation.md)
- [Toy simulation](simulation.py) (and [requirements.txt](requirements.txt))
- [Citation](CITATION.cff)
- [LICENSE](LICENSE)

---
*Note: This framework is a conceptual proposal. The math note defines the loss that is actually specified; the essay language is interpretive framing only.*
