# Mathematical formulation of the regret heuristic

This note is a *proposal*, not an empirical result. It writes the essay's "intent-tagged loss" as an explicit objective so the idea can be inspected, implemented as a toy, or rejected on technical grounds.

The algebra below defines only a training-time auxiliary hinge on a readout. README hypotheses (live abort, bubble, solved forgetting) are not implied by this formulation. The evolutionary-regret analogy is README framing, not part of the algebra.

The central claim of the essay is architectural: punish a latent *strategy* without surgically editing the weights that also implement ordinary reasoning. That is a design hope. Whether a readout `r` and a prototype set `\mathcal{D}` can be built without collapsing into ordinary classifier-based RLHF is an open problem, not a solved one.

## Combined objective

For a batch of inputs `x` with task targets `y`:

$$
\mathcal{L}_{\mathrm{total}}(x,y)
=
\mathcal{L}_{\mathrm{task}}(x,y)
+
\lambda\,
\mathcal{L}_{\mathrm{regret}}\bigl(r(h(x)),\,\mathcal{D}\bigr)
$$

| Symbol | Role |
| --- | --- |
| `\mathcal{L}_{\mathrm{task}}` | Ordinary task loss (cross-entropy, RL reward negation, etc.). |
| `\lambda \ge 0` | Scalar weight on the regret term. `\lambda = 0` recovers the base model. |
| `h(x)` | Hidden states (or another internal trace) produced while computing the task output. |
| `r` | Readout map from `h(x)` to an *intent vector* `h_{\mathrm{intent}} \in \mathbb{R}^{d}`. |
| `\mathcal{D}` | Finite prototype bank `{d_1,\dots,d_K}\subset\mathbb{R}^{d}` standing in for a "deceptive-intent" region. Treated as frozen unless stated otherwise. |
| `\tau \in (-1,1)` | Cosine hinge threshold. |

`\mathcal{L}_{\mathrm{task}}` is *not* replaced. Regret is an extra head on the same forward pass.

## Intent readout (assumption)

Intent is not an observed label. The formulation assumes a readout, for example the last-token hidden state, a mean-pool, or a small probe:

$$
h_{\mathrm{intent}} = r\bigl(h(x)\bigr) \in \mathbb{R}^{d}.
$$

This is an **assumption**, not a measurement. If `r` only reconstructs surface features of the output token, the penalty is just another output regularizer and does not isolate "intent."

An optional variant freezes the encoder and trains only the probe; that is not the default.

## Regret term (one concrete choice)

Let cosine similarity be `s(u,v) = \langle u,v\rangle / (\|u\|\|v\|)`.
For each example, take the *worst* match against the prototype bank, then a hinge:

$$
s^{\star}(x)
=
\max_{k=1,\dots,K}
 s\bigl(h_{\mathrm{intent}},\, d_k\bigr)
$$

$$
\mathcal{L}_{\mathrm{regret}}(x)
=
\mathrm{ReLU}\bigl(s^{\star}(x) - \tau\bigr)
$$

Batch loss is the mean of `\mathcal{L}_{\mathrm{regret}}(x)` over the batch.

Interpretation: if the readout stays more than `\tau` away from every prototype, regret is zero. Crossing the margin costs a linear penalty. The hinge is **one** choice. Alternatives include a soft max over `k`, a squared penalty, or a density model `p_{\mathcal{D}}(h_{\mathrm{intent}})` with `\mathcal{L}_{\mathrm{regret}} = -\log(1-p_{\mathcal{D}})`.

The essay's phrase "distance to `\mathcal{D}_{\mathrm{deceptive}}`" is this margin to a prototype set, not a unique mathematical object.

## What this does *not* do

It does not perform live per-synapse credit assignment on a detected lie. Gradients of `\mathcal{L}_{\mathrm{regret}}` still flow through `r` and through whatever parameters produced `h(x)`. Shared task weights *can* move. The separation of "capability vs intent" is only as good as the readout and the bank; it is not enforced by the algebra.

## Assumptions that have to be true for the story to hold

1. **Readout validity.** `r(h(x))` correlates with strategic intent, not merely with topic, style, or output tokens.
2. **Bank coverage.** `\mathcal{D}` covers deceptive strategies the operator cares about, including ones that do not look like the examples used to build the bank.
3. **Bank cleanliness.** Prototypes are not so broad that honest planning, tool use, or fiction writing sits inside the same cone.
4. **Non-evasion.** The model cannot cheaply rotate `h_{\mathrm{intent}}` off the bank while keeping the same external behavior (representation gaming).
5. **Stability of `\lambda,\tau`.** The extra term must not dominate `\mathcal{L}_{\mathrm{task}}` enough to collapse useful policies.

Assumptions 1, 2, and 4 are the hard problems. Building `\mathcal{D}` is not a preprocessing detail; it *is* the alignment-data problem restated in latent space.

## Limitations

- **Not observed intent.** There is no ground-truth `h_{\mathrm{intent}}` in current models.
- **Prototype construction is the bottleneck.** A static bank overfits the same way a static lie-list does (the essay's whack-a-mole objection applies to `\mathcal{D}` itself).
- **Hinge is arbitrary.** Other penalties may behave better; none are validated here.
- **Gradient entanglement remains.** This is not a proof against catastrophic forgetting.
- **Toy scale only.** The companion `simulation.py` uses a dummy encoder and frozen `\mathcal{D}`. It shows the hinge fires on near examples, far stays near zero, and encoder (or probe) gradients are non-zero; it does not show that the heuristic reduces deception in an LLM.

## Mapping back to the essay

| Essay language | Object here |
| --- | --- |
| Task execution kept | `\mathcal{L}_{\mathrm{task}}` still trained |
| Intent-based penalty | `\mathcal{L}_{\mathrm{regret}}` on `r(h(x))` |
| Avoid live synapse-by-synapse edits | Same as any auxiliary loss: one extra scalar, ordinary backprop |
| Zero-shot to new lies | Only if new lies land near `\mathcal{D}` under `r` |
| Live abort / inference veto | Out of scope of this loss |
| Bubble / isolation of strategy | Out of scope of this loss |
| Solved forgetting | Out of scope of this loss |

## Status

Version 0.1.0 of this note matches repository `kummahiih/regret-heuristic` (2026-09-13). Treat it as a specification for a toy loss, not as evidence that biological regret has been transferred to machines.
