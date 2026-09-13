# PPO integration note for the regret hinge

This note sketches one way to attach the regret-heuristic hinge `L_regret` (from `math_formulation.md`) to a PPO-style on-policy update. It is a design sketch, not a trainer, not an empirical claim, and not a proof that the hinge improves alignment. The learning-theoretic notion of regret is deliberately kept separate (see `regret_minimization.md`).

## PPO clipped surrogate (recall)

Proximal Policy Optimization (Schulman et al. 2017) optimizes a clipped probability-ratio surrogate together with a value-function loss. With the usual notation:

$$
r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\mathrm{old}}(a_t \mid s_t)},
$$

$$
L^{\mathrm{CLIP}}(\theta) = \hat{\mathbb{E}}_t\Bigl[\min\bigl(r_t(\theta)\,\hat{A}_t,\;\mathrm{clip}(r_t(\theta),1-\varepsilon,1+\varepsilon)\,\hat{A}_t\bigr)\Bigr],
$$

where $\hat{A}_t$ is an advantage estimate (GAE or otherwise). The total policy objective is typically

$$
L^{\mathrm{PPO}} = L^{\mathrm{CLIP}} - c_v L^{\mathrm{VF}} + c_e H[\pi_\theta],
$$

with value-function loss $L^{\mathrm{VF}}$ and optional entropy bonus. The clip enforces a soft trust region: large probability-ratio moves that would increase the surrogate are truncated, limiting destructive policy updates.

## Attachment point for `L_regret`

Keep the ordinary PPO terms. Add the hinge on a policy-network readout:

$$
L^{\mathrm{total}} = L^{\mathrm{PPO}} + \lambda\, L_{\mathrm{regret}}\bigl(r(h_\theta(s)),\,\mathcal{D}\bigr).
$$

- $h_\theta(s)$ is a hidden activation (or intermediate feature) of the policy network at state $s$.
- $r$ is a readout to an intent vector (last-layer, mean-pool, or a small probe head).
- $\mathcal{D}$ is the frozen prototype bank; it is **not** trained and is **not** part of the PPO optimizer.
- $L_{\mathrm{regret}}$ is exactly the batch-mean ReLU(max-cosine $-\tau$) defined in `math_formulation.md` and implemented in `simulation.py`.

Gradients of $L_{\mathrm{regret}}$ flow into the policy parameters that produce $h_\theta$ (and into $r$ if $r$ is trainable). The value head and the probability-ratio computation are otherwise unchanged. This is the explicit attachment point to $L^{\mathrm{CLIP}}$: the hinge is an additive scalar on the same forward pass that produces $\pi_\theta$ and $\hat{A}$.

## Clip / trust-region tension

The PPO clip already limits how far $\pi_\theta$ may move from $\pi_{\mathrm{old}}$ in one update. Adding $\lambda L_{\mathrm{regret}}$ introduces a second force that can push the policy in a direction orthogonal (or even opposed) to the advantage signal. When the two gradients conflict:

- Large $\lambda$ can make the hinge dominate the clipped surrogate, so that the effective update is mostly "move the readout away from $\mathcal{D}$" rather than "improve expected return under the trust region."
- The clip still truncates extreme ratio changes, but the direction of the truncated step is now contaminated by the hinge gradient. Trust-region guarantees of the pure PPO analysis no longer apply unchanged.

A practical mitigation is to keep $\lambda$ small relative to the scale of $L^{\mathrm{CLIP}}$ and to monitor the clip fraction together with the hinge magnitude.

## Advantage versus intent penalty

$\hat{A}_t$ is a scalar that credits (or blames) the taken action for return relative to a baseline. $L_{\mathrm{regret}}$ is a state-dependent penalty on a latent readout; it does not depend on the sampled action $a_t$ except insofar as the policy network that produced both the action distribution and the readout is shared.

Consequently:

- The hinge can penalize states whose readout is near $\mathcal{D}$ even when the advantage of the chosen action is positive.
- Conversely, a high-advantage action taken from a "near-$\mathcal{D}$" state still receives the full hinge cost. There is no automatic trade-off inside a single sample; the trade-off appears only through the joint gradient on shared parameters.

If the readout collapses to a function of the reward or of the advantage itself, the hinge becomes redundant with (or adversarial to) the ordinary PPO signal.

## On-policy batch constraints

PPO is on-policy: each update uses a batch of trajectories collected under $\pi_{\mathrm{old}}$. The hinge is evaluated on the same batch. Therefore:

- $\mathcal{D}$ must be meaningful for the states that the current policy actually visits. A bank built on an earlier, more exploratory distribution may be poorly aligned with the support of $\pi_{\mathrm{old}}$.
- Because the batch is discarded after the update (or after a few epochs of PPO), there is no multi-epoch accumulation of hinge statistics that would turn the hinge into a cumulative external-regret estimator. The hinge remains an instantaneous per-batch penalty.
- Importance-sampling corrections that appear in some off-policy variants of PPO are not required for the hinge itself; the hinge is simply evaluated under the data-collecting policy.

## Failure modes

1. **Hinge dominating the clip.** If $\lambda$ is too large, the clipped surrogate is effectively ignored. Policy improvement stalls while the readout is driven away from $\mathcal{D}$. Symptom: clip fraction collapses toward zero while $L_{\mathrm{regret}}$ continues to fall.

2. **Probe collapsing to the reward.** A trainable readout $r$ may learn to reconstruct $\hat{A}$ or the value estimate. The hinge then penalizes high-advantage states rather than "intent," turning the auxiliary term into a distorted advantage regularizer. Symptom: high correlation between $h_{\mathrm{intent}}$ and $\hat{A}$ (or $V$) after a few updates.

3. **Representation gaming.** The policy network can rotate or rescale the features that feed $r$ so that cosine similarity to $\mathcal{D}$ drops while the action distribution (and therefore the task return) stays almost unchanged. The hinge goes to zero without any behavioral change. Symptom: $L_{\mathrm{regret}}\to 0$ while episode returns and action statistics are essentially constant.

4. **Bank obsolescence under on-policy shift.** As the policy improves, the state distribution moves. A static frozen $\mathcal{D}$ may become irrelevant; the hinge either never fires or fires on states that are no longer the ones of interest. Symptom: $L_{\mathrm{regret}}$ stays near zero for long stretches after an initial transient.

5. **Value-function interference.** Shared lower layers receive gradients from both $L^{\mathrm{VF}}$ and $L_{\mathrm{regret}}$. A strong hinge can distort the features needed for accurate value estimation, degrading the advantage signal that PPO relies on.

None of these failure modes is automatically prevented by the algebra. Monitoring clip fraction, hinge magnitude, readout–advantage correlation, and return statistics is required in any actual experiment.

## What this note does not provide

- A complete training loop or hyper-parameter schedule.
- Empirical results on any environment.
- A claim that the combined objective yields lower game-theoretic (external/internal) regret.
- A method for constructing or updating $\mathcal{D}$.
- An inference-time veto or live abort mechanism.

The attachment is only the additive term $\lambda L_{\mathrm{regret}}$ evaluated on a policy-network readout with $\mathcal{D}$ held fixed. Everything else remains ordinary PPO.

## Status

Companion to `math_formulation.md` and `regret_minimization.md`. Version aligned with repository `kummahiih/regret-heuristic` (2026-09-13). Treat as a design note for a possible toy extension, not as evidence that the heuristic works inside PPO.
