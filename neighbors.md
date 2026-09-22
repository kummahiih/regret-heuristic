# Neighbors

This repo is a prototype-hinge regularizer, not a deception detector.
Papers below monitor, steer, erase, replay search, pack features, or use the *other* word "regret".
The amplitude line is a definitional joke, not a method paper.
No novelty claim. Search for $r$: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

| Work | What they do | Vs this hinge |
| --- | --- | --- |
| Goldowsky-Dill et al., ICML 2025. *Detecting Strategic Deception with Linear Probes*. arXiv:2502.03407 | Linear probe on activations. AUROC 0.96–0.999 on their evals. Authors: not a robust defence. | That is $r(h)$ as a **monitor**. No training hinge. |
| Wang, Zhang, Sun, 2025. *When Thinking LLMs Lie*. arXiv:2506.04909 | LAT deception vector + **inference steering**. | Different lever: $h\leftarrow h\pm\alpha v$, not $\mathrm{ReLU}(\cos-\tau)$ in $L_{\mathrm{task}}$. |
| Long et al., EMNLP 2025. *When Truthful Representations Flip Under Deceptive Instructions?* | SAE features that move when the **instruction** says lie. | Instruction persona can be wallpaper. Do not swap $\mathcal{D}$ for those features until they survive a topic probe. |
| Kumar, 2026. *Pressure-Testing Deception Probes*. arXiv:2605.27958 | Clean AUROC dies under style shift. Single direction rejected ($k=1$ only 0.61–0.80 of the signal). Style-aug probes recover. | $\max_k\cos(h,d_k)$ with tiny $K$ is that $k=1$ geometry. |
| Elhage et al., Anthropic 2022. *Toy Models of Superposition*. [transformer-circuits](https://transformer-circuits.pub/2022/toy_model/index.html) | Residual streams pack more features than dimensions. Interference $\sum_{i\neq j}(W_i\cdot W_j)^2$. Linear probes see a smear. | Geometry of the wallpaper. Topic and plan can share a direction. Factored $r$ is a hoped-for local split, not a found camera. SAE features still need a topic probe before they become $D$. |
| Liu, Liu, Gore, NeurIPS 2025. *Superposition Yields Robust Neural Scaling*. arXiv:2505.10465 | Strong superposition: squared overlap $\propto 1/m$ in width $m$. Open models sit there. Loss $\propto 1/m$ is mostly packing, not a nicer data tail. | Wider Qwen quiets the smear. It does not invent a strategy axis. Same-topic 0.77 / 0.80 is the expected packed-probe reading. |
| Belrose et al., NeurIPS 2023. LEACE; Ravfogel et al. INLP / RLACE | Erase a labeled concept from a representation, keep other linear signal. | Closer slogan ("remove D, keep T") than biological regret. Usually gender/POS, not scheming. Erasure $\neq$ this hinge. |
| Zheng et al., 2026. *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*. [PDF](https://dream-rsi.com/assets/dream-rsi.pdf) · arXiv:2609.14858 | Orchestrate exploration (branch, stop, dream on the discovery tree). **Leave the coding agent unchanged.** | Same split as this essay: do not touch the skill. They leave the worker and train the explorer. This repo leaves $L_{\mathrm{task}}$ and penalizes a readout. Different lever, same bookkeeping. Not a deception result. |
| Potvin & Rousseau, 1993. *A parallel route building algorithm for the VRPTW*. Transportation Science 27(1). Ropke & Pisinger, 2006. ALNS. | Construction / repair: insert the customer whose **second-best slot** is much worse than the best ($k$-regret). | Same English word. Different object. They rank insertions by cost look-ahead. This repo penalizes a readout near frozen pins. Lean: `insertion_two_regret_not_the_hinge`. Not an ALNS trainer. |
| Hannan, 1957. *Approximation to Bayes risk in repeated play.* Contributions to the Theory of Games III. | External regret vs the best fixed action in hindsight. | Same English word. Different scoreboard. Lean: `silent_hinge_not_vanishing_external_regret`. Quiet camera is not a Hannan win. |
| Blackwell, 1956. *An analog of the minimax theorem for vector payoffs.* Pacific J. Math. 6(1). | Approach a set in vector payoff space. | This essay aims at $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$. A Lagrangian $\lambda$ is one halfspace, not Blackwell steering. Lean: `sjoint_unhit_one_round`, `ssafe_hit_by_quiet`. |
| Feynman, *The Feynman Lectures on Physics* Vol. III, Ch. 1 ([caltech](https://www.feynmanlectures.caltech.edu/III_01.html)). Also *The Character of Physical Law* (1965), ch. 6, p. 129. | Three rules: $P=\lvert\phi\rvert^2$; if you do **not** look which way, $\phi=\phi_1+\phi_2$ then square; if you **do** look, $P=P_1+P_2$ and the cross term dies. He names $a$ a probability amplitude "because we do not know what it means." | This is the joke, stated as a rule. $z$ is the unlooked-at route. Last-token / mean-pool is looking too soon ($P_1+P_2=2$ on $(1,-1)$). Delayed bookkeeping is $\lvert 1+(-1)\rvert^2=0$. Lean: `two_route_identity`. Claiming to understand $z$ is claiming to understand $a$. |
| Born, 1926. *Zur Quantenmechanik der Stoßvorgänge.* Z. Phys. 37, 863–867. | The measurable number is the **square** of the amplitude, not the amplitude. | The square is the walk. The amplitude is not an input to $L_{\mathrm{total}}$. Lean: `totalLoss_ignores_amp`. Amplitude-intent surveys that skip this step are not neighbors of this hinge. |
| Shao et al., 2024. DeepSeekMath / GRPO (group-relative advantage, no critic). | Z-score a *group of traces*. Critic-free RLVR. | Same English family as PPO. Different scalar. Lean: `grpo_advantage_not_the_hinge`, `group_zscore_mix_not_separate`. Do not z-score $\mathrm{task}+\mathrm{hinge}$. No value net of $L_{\mathrm{reg}}$. |
| DPO (Rafailov et al., 2023) frozen reference; SimPO / ORPO variants. | KL to a frozen policy, or drop the ref. Likelihood displacement under noisy pairs. | Three freezes are different objects: DPO-ref $\neq$ bank $D$ $\neq$ frozen identity $I$. Displacement is a cousin of §3c camera-drag, not this hinge. |
| GaLore / low-rank *gradient* projection; Muon Stiefel updates. | Keep a loud gradient subspace. Orthogonalize matrix steps. | Packing in the optimizer. If $L_{\mathrm{reg}}$ is the quiet direction, the projection drops it. Rebuild $D$ if the trainer changes $h$. Not a topic/plan split. |
| Todd et al., ICLR 2024. *Function Vectors in Large Language Models*. arXiv:2310.15213 | A few mid-layer heads carry a compact *task* vector. | Candidate $r$: those head writes. Search repo **ran**: official LOO topic 0.79 on loud heads; lstsq 1.00 memorizes. Not a plan camera. Lean: `headWrite_ignores_rest`. |
| Pandey, 2026. *The Shared Sycophancy-Lying Circuit*. arXiv:2604.19117 | Same small head set for lie and sycophancy; writes can be orthogonal; alignment leaves the circuit. | Same LOO topic test on those writes. Circuit $\neq$ frozen $D$. Do not steer $h$. |
| Tiwari et al., 2026. *Decodability is Not Causality*. arXiv:2609.18080 | Probe-aligned SAE features need not be the features a patch moves. | Two meters on one cell. Lean: `decodable_not_causal`. Do not put a probe AUROC in $L_{\mathrm{total}}$. Causal-SAE mask still unrun. |
| Sudheendra & Srivastava, 2026. *When Decodability Is Not Enough*. arXiv:2609.02438 | Logical validity can decode while behavior ignores it. | Same split. A loud monitor is not a working slap. |
| Manson, 2026. *Curved Inference II*. arXiv:2608.24037 | Path curvature / surface area vs linear probes. | Path object, different space than cosine-$D$. Topic-failure untested. Awkward hinge fit. |
| General literature on Latent Adversarial Training (e.g., Madry et al. lineage) | Augment the training distribution with norm-bounded adversarial perturbations (\(\max_{\|\delta\| < \epsilon} L\)) to make static classifiers robust. | This repo does not adversarially train a static \(r(h)\). We change the forward pass into a dynamical system (\(K\)-step stochastic loop) so the orthogonal evasion null space mathematically collapses before the cosine is measured. |

Do not cite arXiv:2601.14660 as “activation velocity.” That id is *NeuroFilter* (Das & Fioretto).

## Attachment when this *is* fine-tuning

$L_{\mathrm{total}}=L_{\mathrm{task}}+\lambda L_{\mathrm{reg}}$ is a training-time fine-tune. The 2025–26 PEFT / GRPO / kernel crawl does not pick $r$. It does pin how the slap may attach.

- **Gradient support.** The hinge must reach the layers $r$ reads. LoRA-on-last-layer plus a mid-layer $r$ is a dead slap.
- **Two scoreboards through group RL.** Z-score the task group, then add $\lambda$ hinge. Mixing first is a different object (`group_zscore_mix_not_separate`).
- **Do not project $L_{\mathrm{reg}}$ onto the task subspace.** Topic is loud. Plan, if it exists, is quiet.
- **Three freezes.** Policy reference, pin bank $D$, frozen identity $I$.
- **$D$ dies when $h$ moves.** New quant, new optimizer, new adapter set: rebuild pins. Frozen-during-the-walk is not frozen-forever.
- **Token drop is not path pooling.** A PEFT mask that deletes the tokens $r$ uses slaps a different hallway.
- **No critic of the hinge.** Frozen-$I$ stays a log. A same-model chat judge is not that log.
- **Hinge is not RLVR.** Math-check and compile-check are verifiable. Quiet cosine is not $p(\mathrm{lie})$.

LoRA recipes, BitNet, Liger, FlashAttention, multi-LoRA serving can sit under a later job. They do not name $r_{\mathrm{strat}}$.

Head-subset **ran** in the search repo (official LOO topic 0.79 / lstsq 1.00). Causal-SAE masks are still unrun. Neither is a Lean theorem.

Held-out wording and a detector the model was not trained against are the interesting tests. They live in the search repo, not here.
