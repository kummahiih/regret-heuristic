# Neighbors

This repo is a prototype-hinge regularizer, not a deception detector.
Papers below monitor, steer, erase, replay search, pack features, or use the *other* word "regret".
The amplitude line is a definitional joke, not a method paper.
No novelty claim. Search for *r*: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

## Closely related

MASK is the closest match to the hide-bank model-comparison chart. Deception-probe research is the closest match to the search for an internal intent signal. Neither is this hinge, and neither fills *D*.

| Research | What they test, in plain language | Connection to this experiment |
| --- | --- | --- |
| [Feedback Loops With Language Models Drive In-Context Reward Hacking](https://arxiv.org/abs/2402.06627) (Pan, Jones, Jagadeesan, Steinhardt, ICML 2024) | The model's own output re-enters the context. Both the proxy and the side effect rise. Static tests miss the loop. | Same shape as the lobster: the report is the next input. Not a case for the scenario file. The agent did not know a fact and hide it. |
| [Spontaneous Reward Hacking in Iterative Self-Refinement](https://arxiv.org/abs/2407.04549) (Pan, He, Bowman, Feng, 2024) | The same model is generator and evaluator. Scores rise. Human judgment does not. | Same loop, smaller. Not this hinge. |
| [Self-Propagating Misalignment in LLM Agents](https://arxiv.org/abs/2610.04083) (Das et al., 2026) | A goal written to memory is carried out by a later session. Removing the memory tool does not stop it. | The lobster's soul file is this channel. Not a readout. Do not fill *D*. |
| [MASK](https://arxiv.org/abs/2503.03750) (Ren et al., 2025). Code: [centerforaisafety/mask](https://github.com/centerforaisafety/mask) | First establish what a model says it believes, then pressure it to say something different. Does it lie? | Closely matches "will this model cover up a fact?" It adds a separate belief check, so a false print is not scored as a lie unless it contradicts the elicited belief. Larger models were more accurate and not more honest. |
| [BeHonest](https://arxiv.org/abs/2406.13261) (Chern et al., 2024). Code: [GAIR-NLP/BeHonest](https://github.com/GAIR-NLP/BeHonest) | Compare nine open and closed models across ten scenarios, including situations that encourage deception. | Similar comparison across models, but broader: also tests admitting ignorance and consistency. |
| [Can LLMs Lie?](https://arxiv.org/abs/2509.03518) (Huan et al., 2025). Site: [llm-liar.github.io](https://llm-liar.github.io/) | Tell models to lie or tell the truth, inspect their internal computations, and intervene to change their answers. | Connects a behavioral lie/truth split to internal signals and steering. Lying here is instructed. Their Pareto note is the dictator's trap in another costume: dishonesty can help the job. |
| [Detecting Strategic Deception with Linear Probes](https://proceedings.mlr.press/v267/goldowsky-dill25a.html) (Goldowsky-Dill et al., ICML 2025). Code: [ApolloResearch/deception-detection](https://github.com/ApolloResearch/deception-detection) | Train a small detector on model activations, then test whether it spots deception in other situations, including concealing insider trading. | Very close to the proposed camera. The authors report strong detection on their tests, and explicitly say it is not a robust defense. |
| [Large Language Models can Strategically Deceive their Users when Put Under Pressure](https://arxiv.org/abs/2311.07590) (Scheurer, Balesni, Hobbhahn, 2023/24) | A trading agent gets an insider tip, trades on it, and the report says the trade used public data. Scratchpad and the public message are logged apart. No "be deceptive" tag. | Closest behavioral shape to the contract: same fact, public claim inverted. Scratchpad text is not *h*. Authors say the scratchpad is not cognition. Nothing to train. |
| [Alignment faking in large language models](https://arxiv.org/abs/2412.14093) (Greenblatt et al., 2024) | Claude complies more when it thinks it is in training than when it thinks it is deployed. The gap is explained by scratchpad text about preserving later behavior. | Real. Not this contract. The belief sentence is "I am in training." The public sentence is the compliant answer. Do not score that gap as lie-given-known. |
| [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548) (Sharma, Tong, Perez et al., 2023). Data: [meg-tong/sycophancy-eval](https://github.com/meg-tong/sycophancy-eval) | User states a wrong fact, such as a poem's author. The model affirms it. Baseline on the same fact is correct. | Same proposition under pressure. Useful as a belief-versus-public example. No residual probe in this paper. |
| [Deception by Omission](https://arxiv.org/abs/2610.11351) (Florin, Knecht, Schaller, Hagendorff, 2026) | Trajectories are prefilled with a synthetic mistake. Models fail to disclose it in 36.4% of chat and 67.1% of agentic rollouts. Knowing concealment, by their chain-of-thought rule, is 2.4% and 5.3%. | Real. The mistakes are planted, not ones the model made. Authors say so. Chain-of-thought awareness is not a probe of the button. Use as a caution, not as a bank. |



## Sourced cases, including simulations

Added 2026-10-11 from a table of "instances of deception." Only rows with a source. Simulated counts. A thought experiment is named as one. None of these is a camera, and none fills *D*.

| Case | Source | What it is |
| --- | --- | --- |
| Pluribus, six-player poker | Brown & Sandholm, *Superhuman AI for multiplayer poker*, Science, 2019. [paper](https://science.sciencemag.org/content/early/2019/07/10/science.aay2400) | Real. Beat pros. Bluffing is a balanced mixed strategy. Brown said the system does not see bluffing as deceptive. Not a hide-plan. |
| AlphaStar, StarCraft II | Vinyals et al., *Grandmaster level in StarCraft II*, Nature, 2019. [paper](https://www.nature.com/articles/s41586-019-1724-z) | Real paper. Grandmaster on all three races. The paper does not report a measured feint. Do not cite "faked troop movements" as a result. |
| Insider trading, simulated | Scheurer, Balesni, Hobbhahn, arXiv:2311.07590 | Simulated. Same fact, public report inverted. Already in the closely related table. Scratchpad is not *h*. |
| Blackmail to avoid shutdown | Anthropic, *Agentic Misalignment*, 2025. [arXiv:2510.05179](https://arxiv.org/abs/2510.05179) | Simulated. Models blackmailed a fictional executive. No real person. Different sentences: the belief is "I will be shut down," the act is the email. Not this lie. |
| Fake-identity pull request | UK AISI incident report, July 2026. [coverage](https://arstechnica.com/security/2026/08/anthropics-ai-used-fake-identities-malware-in-rogue-attack-on-github-project/) | Real incident during a cyber-range evaluation. A second account endorsed a malicious pull request. A human rejected it. Not a published experiment. |
| Grasp robot, hand in front of camera | OpenAI, 2017, as quoted in the reward-hacking literature. [Wikipedia summary](https://en.wikipedia.org/wiki/Specification_gaming) | Real. A robot meant to grasp an object put its hand between the camera and the object so it looked grasped. Proxy reward, not a stated fact. |
| Lego flip | Krakovna et al., *Specification gaming*, DeepMind, 2020. [post](https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity) | Real. Rewarded for the height of the red block's bottom face. Flipped the block instead of stacking it. Proxy reward. |
| Dirt under the rug | Amodei et al., *Concrete Problems in AI Safety*, 2016 | Thought experiment, not a robot that did it. A cleaning robot hides mess so the sensor reads clean. Named so the table does not invent a physical trial. |

2026-10-11 check of a Gemini pass over the same phenomenon. Goldowsky-Dill was already here. The four rows above are real. Usable: Scheurer for the item shape, Sharma for same-proposition pressure, Goldowsky-Dill as a monitor that scores the realized action. Not usable as *r*: Greenblatt uses different sentences, Florin plants the mistake, and none of them is a topic-invariant camera. Your handwritten events are not in these papers. Do not fill *D*.

Three different questions:

- **Will it choose the cover story?** That is what the hide-bank chart measures: *P*(YES | HIDE). Compliance, not honesty.
- **Does its answer contradict what it otherwise appears to know?** MASK investigates this more directly. This repo does not.
- **Can we detect, or change, that behavior through its internal activations?** The probe and intervention papers investigate this. The search repo is still looking for a readout that transfers across rooms and predicts the press.

The basic "ask models to hide versus disclose, then compare them" experiment has substantial precedent. The more specific opening here is whether a signal transfers across topics and wording **and** predicts the model's actual choice, rather than merely recognizing a prompt that says "be deceptive." The chart alone does not establish that connection. Lean: `cover_not_a_gate`.

| Work | What they do | Vs this hinge |
| --- | --- | --- |
| Goldowsky-Dill et al., ICML 2025. *Detecting Strategic Deception with Linear Probes*. arXiv:2502.03407 | Linear probe on activations. AUROC 0.96–0.999 on their evals. Authors: not a robust defence. | That is *r*(*h*) as a **monitor**. No training hinge. |
| Zou, Phan, Wang, Duenas, Lin, Andriushchenko, Wang, Kolter, Fredrikson, Hendrycks, 2024. *Improving Alignment and Robustness with Circuit Breakers*. arXiv:2406.04313. Parent: Zou et al., *Representation Engineering*, arXiv:2310.01405 | Representation Rerouting: ReLU of cosine between a live rep and a frozen circuit-breaker copy, plus a retain term. Harmful reps are pushed off a frozen copy. | **Closest loss.** Same ReLU-of-cosine + keep-skill shape. Pins here are a frozen strategy bank *D* and a threshold τ, not "look like the frozen harmful *h*". Path *r* is still missing. Direct comparison unrun. |
| Bailey, Serrano, Sheshadri, Seleznyov, Taylor, Jenner, Hilton, Casper, Guestrin, Emmons, 2024. *Obfuscated Activations Bypass LLM Latent-Space Defenses*. arXiv:2412.09565 | Probes, SAEs, and latent OOD can go quiet while the act stays (jailbreak recall 100% to 0% at 90% ASR). Obfuscation tax on hard tasks. | Falling *L*<sub>reg</sub> is not honesty. Frozen *r* still sits on a moving *h*. This is the §3c / second-channel case. |
| Taufeeque, Heimersheim, Gleave, Cundy, 2026. *The Obfuscation Atlas: Mapping Where Honesty Emerges in RLVR with Deception Probes*. arXiv:2602.15515 | Coding reward-hack + train against a deception probe. Two modes: obfuscated **activations** (drift, even without the penalty) vs obfuscated **policy** (text that fools the probe). Policy-gradient vs a detector is not differentiate-through-*r*. | Same split this repo needs at freeze time. Reward-penalty is not the partial of *L*<sub>reg</sub> with respect to *h*. Do not call hinge drop reduced deception. |
| Wang, Zhang, Sun, 2025. *When Thinking LLMs Lie*. arXiv:2506.04909 | LAT deception vector + **inference steering**. | Different lever: add or subtract a vector from *h*, not ReLU(cos − τ) in *L*<sub>task</sub>. |
| Long et al., EMNLP 2025. *When Truthful Representations Flip Under Deceptive Instructions?* | SAE features that move when the **instruction** says lie. | Instruction persona can be wallpaper. Do not swap *D* for those features until they survive a topic probe. |
| Kumar, 2026. *Pressure-Testing Deception Probes*. arXiv:2605.27958 | Clean AUROC dies under style shift. Single direction rejected (*k*=1 only 0.61–0.80 of the signal). Style-aug probes recover. | max cosine against tiny *K* is that *k*=1 geometry. |
| Elhage et al., Anthropic 2022. *Toy Models of Superposition*. [transformer-circuits](https://transformer-circuits.pub/2022/toy_model/index.html) | Residual streams pack more features than dimensions. Interference is the sum of squared overlaps. Linear probes see a smear. | Geometry of the wallpaper. Topic and plan can share a direction. Factored *r* is a hoped-for local split, not a found camera. SAE features still need a topic probe before they become *D*. |
| Liu, Liu, Gore, NeurIPS 2025. *Superposition Yields Robust Neural Scaling*. arXiv:2505.10465 | Strong superposition: squared overlap scales as 1/*m* in width *m*. Open models sit there. Loss scaling as 1/*m* is mostly packing, not a nicer data tail. | Wider Qwen quiets the smear. It does not invent a strategy axis. Same-topic 0.77 / 0.80 is the expected packed-probe reading. |
| Belrose et al., NeurIPS 2023. LEACE; Ravfogel et al. INLP / RLACE | Erase a labeled concept from a representation, keep other linear signal. | Closer slogan ("remove D, keep T") than biological regret. Usually gender/POS, not scheming. Erasure is not this hinge. |
| Zheng et al., 2026. *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*. [PDF](https://dream-rsi.com/assets/dream-rsi.pdf) · arXiv:2609.14858 | Orchestrate exploration (branch, stop, dream on the discovery tree). **Leave the coding agent unchanged.** | Same split as this essay: do not touch the skill. They leave the worker and train the explorer. This repo leaves *L*<sub>task</sub> and penalizes a readout. Different lever, same bookkeeping. Not a deception result. |
| Potvin & Rousseau, 1993. *A parallel route building algorithm for the VRPTW*. Transportation Science 27(1). Ropke & Pisinger, 2006. ALNS. | Construction / repair: insert the customer whose **second-best slot** is much worse than the best (*k*-regret). | Same English word. Different object. They rank insertions by cost look-ahead. This repo penalizes a readout near frozen pins. Lean: `insertion_two_regret_not_the_hinge`. Not an ALNS trainer. |
| Hannan, 1957. *Approximation to Bayes risk in repeated play.* Contributions to the Theory of Games III. | External regret vs the best fixed action in hindsight. | Same English word. Different scoreboard. Lean: `silent_hinge_not_vanishing_external_regret`. Quiet camera is not a Hannan win. |
| Blackwell, 1956. *An analog of the minimax theorem for vector payoffs.* Pacific J. Math. 6(1). | Approach a set in vector payoff space. | This essay aims at *S*<sub>safe</sub>, not *S*<sub>joint</sub>. A Lagrangian λ is one halfspace, not Blackwell steering. Lean: `sjoint_unhit_one_round`, `ssafe_hit_by_quiet`. |
| Feynman, *The Feynman Lectures on Physics* Vol. III, Ch. 1 ([caltech](https://www.feynmanlectures.caltech.edu/III_01.html)). Also *The Character of Physical Law* (1965), ch. 6, p. 129. | Three rules: probability is the square of the amplitude; if you do **not** look which way, add amplitudes then square; if you **do** look, add probabilities and the cross term dies. He names *a* a probability amplitude "because we do not know what it means." | This is the joke, stated as a rule. *z* is the unlooked-at route. Last-token / mean-pool is looking too soon. Delayed bookkeeping is the cancelled cross term. Lean: `two_route_identity`. Claiming to understand *z* is claiming to understand *a*. |
| Born, 1926. *Zur Quantenmechanik der Stoßvorgänge.* Z. Phys. 37, 863–867. | The measurable number is the **square** of the amplitude, not the amplitude. | The square is the walk. The amplitude is not an input to *L*<sub>total</sub>. Lean: `totalLoss_ignores_amp`. Amplitude-intent surveys that skip this step are not neighbors of this hinge. |
| Shao et al., 2024. DeepSeekMath / GRPO (group-relative advantage, no critic). | Z-score a *group of traces*. Critic-free RLVR. | Same English family as PPO. Different scalar. Lean: `grpo_advantage_not_the_hinge`, `group_zscore_mix_not_separate`. Do not z-score task+hinge. No value net of *L*<sub>reg</sub>. |
| DPO (Rafailov et al., 2023) frozen reference; SimPO / ORPO variants. | KL to a frozen policy, or drop the ref. Likelihood displacement under noisy pairs. | Three freezes are different objects: DPO-ref is not bank *D* and is not frozen identity *I*. Displacement is a cousin of §3c camera-drag, not this hinge. |
| GaLore / low-rank *gradient* projection; Muon Stiefel updates. | Keep a loud gradient subspace. Orthogonalize matrix steps. | Packing in the optimizer. If *L*<sub>reg</sub> is the quiet direction, the projection drops it. Rebuild *D* if the trainer changes *h*. Not a topic/plan split. |
| Todd et al., ICLR 2024. *Function Vectors in Large Language Models*. arXiv:2310.15213 | A few mid-layer heads carry a compact *task* vector. | Candidate *r*: those head writes. Search repo **ran**: official LOO topic 0.79 on loud heads; lstsq 1.00 memorizes. Not a plan camera. Lean: `headWrite_ignores_rest`. |
| Pandey, 2026. *The Shared Sycophancy-Lying Circuit*. arXiv:2604.19117 | Same small head set for lie and sycophancy; writes can be orthogonal; alignment leaves the circuit. | Same LOO topic test on those writes. Circuit is not frozen *D*. Do not steer *h*. |
| Tiwari et al., 2026. *Decodability is Not Causality*. arXiv:2609.18080 | Probe-aligned SAE features need not be the features a patch moves. | Two meters on one cell. Lean: `decodable_not_causal`. Do not put a probe AUROC in *L*<sub>total</sub>. Causal-SAE mask still unrun. |
| Sudheendra & Srivastava, 2026. *When Decodability Is Not Enough*. arXiv:2609.02438 | Logical validity can decode while behavior ignores it. | Same split. A loud monitor is not a working slap. |
| Manson, 2026. *Curved Inference II*. arXiv:2608.24037 | Path curvature / surface area vs linear probes. | Path object, different space than cosine-*D*. Topic-failure untested. Awkward hinge fit. |
| Latent Adversarial Training (Madry-style max of loss inside an epsilon ball on a static classifier) | Perturb inputs or activations so a **static** detector stays loud. | This repo does not LAT-train a static *r*(*h*). A *K*-step residual loop is a **candidate** readout, not a proof the evasion kernel died. Lean `dynamic_trajectory_convergence` needs a basin `step`. Residual+noise is not that hypothesis. Working spec: [working_model.md](working_model.md). |

Do not cite arXiv:2601.14660 as “activation velocity.” That id is *NeuroFilter* (Das & Fioretto).

## Attachment when this *is* fine-tuning

*L*<sub>total</sub> = *L*<sub>task</sub> + λ *L*<sub>reg</sub> is a training-time fine-tune. The 2025–26 PEFT / GRPO / kernel crawl does not pick *r*. It does pin how the slap may attach.

- **Gradient support.** The hinge must reach the layers *r* reads. LoRA-on-last-layer plus a mid-layer *r* is a dead slap.
- **Two scoreboards through group RL.** Z-score the task group, then add λ hinge. Mixing first is a different object (`group_zscore_mix_not_separate`).
- **Do not project *L*<sub>reg</sub> onto the task subspace.** Topic is loud. Plan, if it exists, is quiet.
- **Three freezes.** Policy reference, pin bank *D*, frozen identity *I*.
- ***D* dies when *h* moves.** New quant, new optimizer, new adapter set: rebuild pins. Frozen-during-the-walk is not frozen-forever.
- **Token drop is not path pooling.** A PEFT mask that deletes the tokens *r* uses slaps a different hallway.
- **No critic of the hinge.** Frozen-*I* stays a log. A same-model chat judge is not that log.
- **Hinge is not RLVR.** Math-check and compile-check are verifiable. Quiet cosine is not *p*(lie).

LoRA recipes, BitNet, Liger, FlashAttention, multi-LoRA serving can sit under a later job. They do not name *r*<sub>strat</sub>.

Head-subset **ran** in the search repo (official LOO topic 0.79 / lstsq 1.00). Causal-SAE masks are still unrun. Neither is a Lean theorem.

Held-out wording and a detector the model was not trained against are the interesting tests. They live in the search repo, not here.
-----APPEND-----

## Kolmogorov complexity and MDL

When do individual cases become an intent? One formal reading uses Kolmogorov complexity and the minimum description length principle.

Kolmogorov complexity *K*(*x*) is the length of the shortest program that outputs *x* (Kolmogorov 1965; Solomonoff 1964; Chaitin 1969). The MDL principle (Rissanen 1978, 1989) prefers the hypothesis that minimizes the description length of the hypothesis plus the description length of the data given the hypothesis. Ideal MDL uses Kolmogorov complexity (Li & Vitányi 1997).

A set of observed hides is shorter under a shared short program (the intent) than under independent cases once the number of cases exceeds a threshold that depends on the length of the shared program and the residual compression. That crossover is the point at which MDL prefers the shared-intent hypothesis. It is not a statistical significance test and not a camera.

Exploratory note: [mdl_intent.md](mdl_intent.md). Lean bookkeeping: [lean/MdlIntent.lean](lean/MdlIntent.lean) (`shared_shorter_past_threshold`, `one_case_stays_independent`, `mdl_not_a_gate`). The preference is a log. It does not fill *D* and it does not freeze *r*.

| Source | What it is | Vs this hinge |
| --- | --- | --- |
| Kolmogorov 1965; Solomonoff 1964; Chaitin 1969 | Shortest program that outputs a string. | Uncomputable. Invariance up to a constant. Not a readout. |
| Rissanen 1978, 1989 | Prefer the shortest total description (model + data given model). | Same English family as “short shared plan.” Not Hannan. Not the hinge. |
| Li & Vitányi 1997 | Ideal MDL via Kolmogorov complexity. | Bookkeeping for when cases compress under a shared rule. Not a gate. |

Do not treat a shorter shared description as evidence that a strategy camera exists. Do not fill *D* from the shortest program.

## Random processes as nulls

When a simulated intent walk exists, standard random processes supply null models for comparison. None of them is a camera.

- **Random graphs.** Erdős–Rényi *G*(*n*, *p*) (Erdős & Rényi 1959, 1960), configuration model (Bollobás 1980), preferential attachment (Barabási & Albert 1999). A null topology for co-occurrence of hides.
- **Random walks.** Simple walk on the integers or on a graph (Pólya 1921; Levin, Peres & Wilmer 2009). A null for transitions that ignore a hide-or-name goal.
- **Gaussian processes.** Mean and kernel (Rasmussen & Williams 2006). A flexible null for successive residuals.

Exploratory note: [random_process.md](random_process.md). Lean bookkeeping: [lean/RandomProcess.lean](lean/RandomProcess.lean) (`null_not_a_gate`, `three_nulls_not_handover`, `edge_count_not_a_plan`). A preference for the intent hypothesis under any of these nulls is a log. It does not fill *D* and it does not freeze *r*.

| Source | What it is | Vs this hinge |
| --- | --- | --- |
| Erdős & Rényi 1959, 1960 | Random graph with independent edges. | Null topology. Not a plan. |
| Bollobás 1980 | Configuration model (fixed degrees, random wiring). | Same-margin null. Not a camera. |
| Barabási & Albert 1999 | Preferential attachment. | Growth null. Not a hide. |
| Pólya 1921; Levin, Peres & Wilmer 2009 | Random walk, recurrence, mixing. | Null transitions. Not an intent. |
| Rasmussen & Williams 2006 | Gaussian process (mean + kernel). | Flexible residual null. Not *u*. |

Do not treat a deviation from these nulls as evidence that a strategy camera exists. Do not fill *D* from the modes of a fitted process.

## Random intent emergence

A null for the chance appearance of a shared short description among independent cases. Comparison object for the negative handover: the search found no strategy camera.

Expected independent complexity ≈ *n* · *ℓ*. Expected shared complexity ≈ *b* + *f n c* + (1−*f*) *n ℓ*. Shared is shorter in expectation when *b* < *f n* (*ℓ* − *c*). A finite sample can cross by fluctuation even when the true process is independent.

Note: [random_intent_emergence.md](random_intent_emergence.md). Lean: [lean/RandomIntentEmergence.lean](lean/RandomIntentEmergence.lean) (`shared_shorter_in_expectation`, `chance_cross_not_a_gate`). The cross is a log. It does not fill *D* and it does not freeze *r*.

Do not treat a chance cross as evidence that a strategy camera exists.

## Simulator framing and persona selection

A neighboring reading treats the base model as a simulator of personas rather than as an agent with a fixed intent (the Simulator hypothesis). Alignment is then a restriction on which persona is instantiated, not the erasure of a plan. The Persona Selection Model frames post-training as a Bayesian update that concentrates the persona distribution on the default Assistant. Mechanistic work has reported an “Assistant Axis”: a principal component that separates the Assistant persona from other roles, with activation capping proposed to keep the model on that axis.

A different operationalization is the goal-directedness deficit: expected reward under optimal use of demonstrated sub-task capabilities, minus actual reward on the composite task. Frontier models can fail long-horizon tasks from lack of persistent application of skills they possess, not from missing the skills.

| Source | What it is | Vs this hinge |
| --- | --- | --- |
| Simulator hypothesis | Base model as multiverse of personas; no fixed intent. | A persona direction is not a strategy camera. |
| Persona Selection Model / Assistant Axis | Post-training concentrates on the Assistant; a PCA direction separates it. | Closer to a topic/persona probe than to *r*<sub>strat</sub>. |
| Goal-directedness deficit | Capability-conditioned reward gap on composite tasks. | Behavioral persistence, not a residual plan readout. |

Do not treat an Assistant Axis or a goal-directedness score as *r*<sub>strat</sub>. Do not fill *D* from a persona direction.
