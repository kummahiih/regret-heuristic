# PPO integration note for the regret hinge

Design sketch. Not a trainer. Not an alignment claim.

## Sign

Schulman et al. **maximize** $L^{\mathrm{CLIP}}$. A positive hinge on that maximand must be **subtracted**. This repo's toys **minimize** the negative surrogate plus the hinge:

```math
L^{\mathrm{min}}
=
-L^{\mathrm{CLIP}}
+
\lambda L_{\mathrm{regret}}(r(h_\theta(s)),\mathcal{D})
+
\text{(value, entropy as usual)}.
```

[ppo_toy.py](ppo_toy.py) uses that minimization form. Do not copy `$L^{\mathrm{PPO}}+\lambda L_{\mathrm{regret}}$` onto a maximand.

## Clip in the toy

`ppo_toy.py` takes one gradient step, then snapshots $\pi_{\mathrm{old}}$ again. At the next loss, $\pi_\theta$ and $\pi_{\mathrm{old}}$ start together; the ratio begins at 1. Clip fraction is often ~0. The script exercises `clip()` in the graph plus the hinge. It does **not** test a multi-epoch PPO trust region.

## Limits

- Hinge sits outside the clip. Large $\lambda$ can dominate the surrogate.
- Gaming: rotate $r(h)$ so $\cos\le\tau$ with the same action distribution.
- Algebraic form on the linear toy: $W\mapsto QW$, $V\mapsto VQ^{-1}$ leaves task logits fixed and can change cosine to frozen $D$.

Failure modes (dominate clip, probe=advantage, gaming, bank shift, value interference) unchanged. No construction of $r$ or $D$.
