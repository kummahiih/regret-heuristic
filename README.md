# The Regret Heuristic

**Biological regret as a sketch for a training-time loss — not a working conscience.**

Human regret looks, from the outside, like a cheap answer to a hard bookkeeping problem. A long deceptive plan is a chain of ordinary skills. Tracing every step and editing every weight would be expensive and would risk erasing those skills. Evolution appears to have done something else: keep the competence, and attach a lasting negative tag to the *intent* of the plan.

This repository asks whether that pattern is useful for machine learning. The claim below is a **hypothesis**. The only object that is actually specified is a small auxiliary loss.

## Why deception is expensive

A system that is rewarded for hiding the truth can close itself inside an information bubble (the Dictator’s Trap: punish honesty, and you only hear lies).

- Later training rounds ingest the system’s own fabrications.
- Predictions stay confident while they drift off the world.
- In a multi-agent setting, everyone pays a verification tax instead of solving the task.

That is a reason to care. It is not a theorem, and the loss below does not by itself prevent a bubble.

## Why “just backprop the lie” is a bad repair

A lie is usually a trajectory, not one token. Credit assignment over that trajectory is messy. The same weights often implement both the deception and the useful reasoning, so a local update can look like catastrophic forgetting. Punishing one surface form of the lie teaches the model to hide better next time (whack-a-mole).

The hoped-for alternative is not “do not use gradients.” It is “put the penalty on a representation of *strategy*, and leave the task objective in place.”

## What is specified

Training time only:

$$
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{task}}
+
\lambda\,
\mathcal{L}_{\mathrm{regret}}\bigl(r(h(x)),\,\mathcal{D}\bigr)
$$

- $\mathcal{L}_{\mathrm{task}}$ is the ordinary objective (cross-entropy, a reward, …).
- $h(x)$ is an internal trace; $r$ reads it out as an intent vector.
- $\mathcal{D}$ is a frozen bank of “deceptive-intent” prototypes.
- $\mathcal{L}_{\mathrm{regret}}$ is a hinge on cosine similarity to that bank (details in the [math note](math_formulation.md)).

Gradients of the extra term still flow through whatever produced $h(x)$. Capability and intent are not algebraically separated. There is no inference-time abort.

The hard problems are not the hinge. They are whether $r$ tracks strategy rather than topic, whether $\mathcal{D}$ can be built without swallowing honest planning, and whether the model can rotate the readout off the bank and keep the same behaviour.

## What this repo is not

Not a trained LLM, not evidence that regret transferred to machines, not a solution to forgetting, credit assignment, or alignment faking. Neighbours in the literature include residual-stream probes (including LAT), representation engineering / steering, and auxiliary objectives already used in RLAIF. The distinctive bet here is a *training-time hinge on a hypothesized intent readout against a fixed bank*.

## Files

| File | Role |
| --- | --- |
| [math_formulation.md](math_formulation.md) | Loss, symbols, assumptions, limits |
| [simulation.py](simulation.py) | Dummy encoder: hinge fires on “near” vectors, not on vectors orthogonal to $\mathcal{D}$; one Adam step |
| [requirements.txt](requirements.txt) | `torch>=2.0.0,<3` |
| [CITATION.cff](CITATION.cff) | Cite the proposal |
| [LICENSE](LICENSE) | MIT |

```bash
pip install -r requirements.txt
python simulation.py
```

You should see `L_near > 0`, `L_far ≈ 0`, and a nonzero encoder gradient before and after one step. That only shows the formula is wired. It does not show alignment.
