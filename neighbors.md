# Neighbors

This repo is a prototype-hinge regularizer, not a deception detector.
Papers below monitor, steer, erase, or replay search traces. They are not the hinge.
No novelty claim. Search for \(r\): [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

| Work | What they do | Vs this hinge |
| --- | --- | --- |
| Goldowsky-Dill et al., ICML 2025. *Detecting Strategic Deception with Linear Probes*. arXiv:2502.03407 | Linear probe on activations. AUROC 0.96–0.999 on their evals. Authors: not a robust defence. | That is \(r(h)\) as a **monitor**. No training hinge. |
| Wang, Zhang, Sun, 2025. *When Thinking LLMs Lie*. arXiv:2506.04909 | LAT deception vector + **inference steering**. | Different lever: \(h\leftarrow h\pm\alpha v\), not \(\mathrm{ReLU}(\cos-\tau)\) in \(L_{\mathrm{task}}\). |
| Long et al., EMNLP 2025. *When Truthful Representations Flip Under Deceptive Instructions?* | SAE features that move when the **instruction** says lie. | Instruction persona can be wallpaper. Do not swap \(\mathcal{D}\) for those features until they survive a topic probe. |
| Kumar, 2026. *Pressure-Testing Deception Probes*. arXiv:2605.27958 | Clean AUROC dies under style shift. Single direction rejected (\(k=1\) only 0.61–0.80 of the signal). Style-aug probes recover. | \(\max_k\cos(h,d_k)\) with tiny \(K\) is that \(k=1\) geometry. |
| Belrose et al., NeurIPS 2023. LEACE; Ravfogel et al. INLP / RLACE | Erase a labeled concept from a representation, keep other linear signal. | Closer slogan ("remove D, keep T") than biological regret. Usually gender/POS, not scheming. Erasure \(\neq\) this hinge. |
| Zheng et al., 2026. *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*. [PDF](https://dream-rsi.com/assets/dream-rsi.pdf) · arXiv:2609.14858 | Discovery **tree** as a replay world. Dream off-policy over past branches; do not change the coding agent. | Map of realized search, not a deception hinge. Closest vocab: walk/map and finding a path *afterwards*. Not \(r\), not \(\mathcal{D}\) pins. |

Held-out wording and a detector the model was not trained against are the interesting tests. They live in the search repo, not here.
