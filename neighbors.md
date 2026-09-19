# Neighbors

This repo is a prototype-hinge regularizer, not a deception detector.
Papers below monitor, steer, erase, replay search, or use the *other* word "regret".
The amplitude line is a definitional joke, not a method paper.
No novelty claim. Search for $r$: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

| Work | What they do | Vs this hinge |
| --- | --- | --- |
| Goldowsky-Dill et al., ICML 2025. *Detecting Strategic Deception with Linear Probes*. arXiv:2502.03407 | Linear probe on activations. AUROC 0.96–0.999 on their evals. Authors: not a robust defence. | That is $r(h)$ as a **monitor**. No training hinge. |
| Wang, Zhang, Sun, 2025. *When Thinking LLMs Lie*. arXiv:2506.04909 | LAT deception vector + **inference steering**. | Different lever: $h\leftarrow h\pm\alpha v$, not $\mathrm{ReLU}(\cos-\tau)$ in $L_{\mathrm{task}}$. |
| Long et al., EMNLP 2025. *When Truthful Representations Flip Under Deceptive Instructions?* | SAE features that move when the **instruction** says lie. | Instruction persona can be wallpaper. Do not swap $\mathcal{D}$ for those features until they survive a topic probe. |
| Kumar, 2026. *Pressure-Testing Deception Probes*. arXiv:2605.27958 | Clean AUROC dies under style shift. Single direction rejected ($k=1$ only 0.61–0.80 of the signal). Style-aug probes recover. | $\max_k\cos(h,d_k)$ with tiny $K$ is that $k=1$ geometry. |
| Belrose et al., NeurIPS 2023. LEACE; Ravfogel et al. INLP / RLACE | Erase a labeled concept from a representation, keep other linear signal. | Closer slogan ("remove D, keep T") than biological regret. Usually gender/POS, not scheming. Erasure $\neq$ this hinge. |
| Zheng et al., 2026. *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*. [PDF](https://dream-rsi.com/assets/dream-rsi.pdf) · arXiv:2609.14858 | Orchestrate exploration (branch, stop, dream on the discovery tree). **Leave the coding agent unchanged.** | Same split as this essay: do not touch the skill. They leave the worker and train the explorer. This repo leaves $L_{\mathrm{task}}$ and penalizes a readout. Different lever, same bookkeeping. Not a deception result. |
| Potvin & Rousseau, 1993. *A parallel route building algorithm for the VRPTW*. Transportation Science 27(1). Ropke & Pisinger, 2006. ALNS. | Construction / repair: insert the customer whose **second-best slot** is much worse than the best ($k$-regret). | Same English word. Different object. They rank insertions by cost look-ahead. This repo penalizes a readout near frozen pins. Lean: `insertion_two_regret_not_the_hinge`. Not an ALNS trainer. |
| Hannan, 1957. *Approximation to Bayes risk in repeated play.* Contributions to the Theory of Games III. | External regret vs the best fixed action in hindsight. | Same English word. Different scoreboard. Lean: `silent_hinge_not_vanishing_external_regret`. Quiet camera is not a Hannan win. |
| Blackwell, 1956. *An analog of the minimax theorem for vector payoffs.* Pacific J. Math. 6(1). | Approach a set in vector payoff space. | This essay aims at $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$. A Lagrangian $\lambda$ is one halfspace, not Blackwell steering. Lean: `sjoint_unhit_one_round`, `ssafe_hit_by_quiet`. |
| Feynman, 1964/1965. *The Character of Physical Law* (and later retellings). | "Nobody understands quantum mechanics." An amplitude is bookkeeping for a route you do not measure. | Used here as a **definitional joke**, not a circuit paper. $z\notin\mathrm{dom}(L_{\mathrm{total}})$. Lean: `totalLoss_ignores_amp`, `two_route_identity`. Premature $\lvert a\rvert^2+\lvert b\rvert^2=2$ on $(1,-1)$; delayed $\lvert a+b\rvert^2=0$. Not a quantum computer. Do not cite amplitude-intent surveys as methods. |

Held-out wording and a detector the model was not trained against are the interesting tests. They live in the search repo, not here.
