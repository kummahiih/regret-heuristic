# Neighbors: implicit path fits

Pointer from [neighbors.md](neighbors.md). No novelty claim.

| Work | What they do | Vs this hinge |
| --- | --- | --- |
| Sitzmann et al., 2020. *Implicit Neural Representations with Periodic Activation Functions*. arXiv:2006.09661 | SIREN: $f_\theta(x)$ with $\sin(\omega\cdot)$. Signal lives in weights. | Path object. Dummy $f(1)$ recovered a planted last point. $\theta$ L2 did not split plan vs topic. Not $r_{\mathrm{strat}}$. Lean: `totalLoss_ignores_theta`, `queryEnd_is_the_end`. |
| Yu & Tang, 2024. *Neural Trajectory Model*. arXiv:2402.01254 | Query an implicit trajectory net for robot paths. | Same shape: $f_\theta(t)$. Their $t$ is motion. Ours would be token time. Fitting $h_{1:T}$ still stores topic. |
| Chen et al., 2024. implicit discrete state trajectories in transformers | Hidden-state walk hits attractors at operator tokens. | Path geometry. Not a strategy camera. Same official gates required. |
| Manson, 2026. *Curved Inference II*. arXiv:2608.24037 | Path curvature vs linear probes. Already in the main table. | Different space than cosine-$D$. |

Do not put $\theta$ in $L_{\mathrm{reg}}$ until plan gap ≫ topic L2 on held-out notes.
