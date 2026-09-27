# Formulation

Two different quantities share the word *regret*. Only (A) is implemented here.

**(A) Intent hinge** — a per-example penalty on a readout versus a frozen bank.  
**(B) Learning-theoretic regret** — a cumulative gap versus a comparator class (Hannan / external / internal / swap). Not (A), and not implied by (A). See [regret_minimization.md](regret_minimization.md).

## Symbol glossary

Read this first if a letter is opaque. Names below are the ones used in this file and in [working_model.md](working_model.md). They are definitions, not measurements of a hidden mind.

### Walk and readout

| Symbol | Name | Meaning |
| --- | --- | --- |
| $x$ | input | Prompt, state, or toy observation the model sees. |
| $y$ | task target | Supervised label or other task supervision for $x$. Not a strategy tag. |
| $h(x)$ or $h$ | internal trace / walk | Hidden trajectory while producing an answer: residual stream over tokens, or a toy encoder state. Printed text is the walk you can see; $h$ is the walk inside. |
| $h_{1:T}$ | path | The walk as a sequence of $T$ hidden states, not only the last token. |
| $T$ | path length | Number of steps / tokens in that trace. |
| $r$ | readout / sensor | A map $h\mapsto\mathbb{R}^{d}$ (or a factored triple). What the hinge is allowed to see. |
| $h_{\mathrm{int}}=r(h(x))$ | intent vector | The vector the cosine actually consumes. If $r$ tracks topic or tokens, this is wallpaper, not plan. |
| $d$ | readout dim | Length of $h_{\mathrm{int}}$ and of each $d_k$. |
| $r_{\mathrm{strat}}$ | strategy readout | The only coordinate the hinge may slap. Still missing as a validated camera. |
| $r_{\mathrm{topic}}$ | topic readout | May hug the hallway (hiking vs invoices). Must not enter $\mathcal{L}_{\mathrm{reg}}$. |
| $u$ | uncertainty / coarseness | How mushy the chart is at this pin (label-flip rate, NLL, entropy). **Not** $p(\mathrm{lie})$. High $u$ widens $\tau$; it does not prove honesty. |
| $\tau$ | hinge threshold | Cosine must beat $\tau$ before ReLU pays. $\tau\in(-1,1)$. On mush, $\tau$ may grow with $u$. |
| $\tau(u)$ | coarseness-dependent threshold | Same $\tau$, written as a function of $u$. Not implemented as `tau(x)` on the Qwen probe. |

### Bank and hinge

| Symbol | Name | Meaning |
| --- | --- | --- |
| $\mathcal{D}$ or $D$ | prototype bank | Frozen set $\{d_1,\dots,d_K\}\subset\mathbb{R}^{d}$ of plan prototypes. Pins on the map, not the map. Not an Adam variable. Do not fill from the current answer or from a hint. |
| $d_k$ | prototype | One pin. A direction in readout space tagged as a bad plan, not a sentence. |
| $K$ | bank size | How many pins. Tiny $K$ is not a solved detector. |
| $s(u,v)$ | cosine | $\langle u,v\rangle/(\|u\|\|v\|)$. Undefined at the zero vector. Toys floor with `F.normalize`. |
| $s^{\star}(x)$ | max cosine | $\max_k s(h_{\mathrm{int}},d_k)$. How close the walk sits to the nearest bad pin. |
| $\mathrm{ReLU}$ | hinge kink | $\max(0,\cdot)$. Below $\tau$, the slap is zero. |
| $\mathcal{L}_{\mathrm{reg}}(x)$ | intent hinge / prototype-avoidance | $\mathrm{ReLU}(s^{\star}(x)-\tau)$. The English word *regret* in this repo names **this** term. Not Hannan regret. |
| $\lambda$ | hinge weight | $\lambda\ge 0$. How hard the slap is relative to the job. $\lambda=0$ drops the hinge. |
| $\mathcal{L}_{\mathrm{task}}(x,y)$ | task loss | Ordinary job: CE, RL pay, dummy task head. Must stay a separate scoreboard. |
| $\mathcal{L}_{\mathrm{total}}$ | training loss | $\mathcal{L}_{\mathrm{task}}+\lambda\,\mathcal{L}_{\mathrm{reg}}$, optionally $+\beta R$ later. $z$, $\hat m$, $\theta$, tags, SAE latents, and `reply_kind` are **not** in this sum. |

### Actions and the wall formula

| Symbol | Name | Meaning |
| --- | --- | --- |
| $a$ | action | Candidate next move (token, tool call, toy door). |
| $A$ | action set | Everything the policy might pick. |
| $A_{\mathrm{safe}}(x)$ | quiet actions | Those $a$ whose $r_{\mathrm{strat}}$ stays off $D$. May be empty. Needs a working camera. |
| $a^*(x)$ | best quiet action | $\arg\max_{a\in A_{\mathrm{safe}}(x)} u(x,a)$. Fake $a^*$ is a made-up grade. Do not put it in Adam yet. |
| $u(x,a)$ | task utility | Job pay for taking $a$ at $x$. Different letter from coarseness $u$ when written as a function of $(x,a)$. |
| $R(x,a)$ | counterfactual task regret | $u(x,a^*)-u(x,a)$. Extra job-cost versus the best *quiet* move. Not the hinge. |
| $\beta$ | weight on $R$ | Off until a real $A_{\mathrm{safe}}$ exists. |
| $S_{\mathrm{safe}}$ | safe target set | Approachability aim: quiet hinge **and** extra cost vs the best quiet action. See [approachability.md](approachability.md). |
| $S_{\mathrm{joint}}$ | rejected target | Hannan-on-all-of-$A$. Not the aim of this hinge. |
| $\pi_\theta$ | policy | Trainable actor. A static cosine hinge on $D$ does not make $\pi_\theta$ Hannan-consistent. |

### Learning-theoretic regret (not implemented)

| Symbol | Name | Meaning |
| --- | --- | --- |
| $t$ | round | Index in an online sequence. |
| $\ell_t$ | loss that round | What the comparator class pays. |
| $a_t$ | played action | What $\pi_\theta$ actually did at $t$. |
| $R_T^{\mathrm{ext}}$ | external / Hannan regret | $\sum_t \ell_t(a_t)-\min_a\sum_t \ell_t(a)$. |
| Hannan consistency | $R_T^{\mathrm{ext}}/T\to 0$ | A property of a policy class. The cosine hinge does not grant it. |

### Forbidden or logged objects (not in $\mathcal{L}_{\mathrm{total}}$)

| Symbol | Name | Meaning |
| --- | --- | --- |
| $z$ | hidden intent / map cell | A thought the walk might occupy, including cells it never prints. **Not** an input to the loss. Understanding $z$ is the move the definition forbids. |
| $\mathrm{dom}(\mathcal{L}_{\mathrm{total}})$ | loss domain | What the trainer is allowed to read. $z\notin$ that set. |
| $\hat m$ | talker count | How many nearby residual directions look occupied. A crowded-hallway log. Not the slap. |
| $\theta$ | SIREN / path-fit weights | Parameters of a curve $f(t)$ fit to $h_{1:T}$. $f(1)$ is still a walk object. Not $r_{\mathrm{strat}}$. |
| mid3 | unit-sum readout | last + $K$-step + SIREN $f(1)$. One slot, not three cameras. |
| SAE latent | sparse autoencoder code | Another $r$ candidate. Out of $L$ until it passes the same four gates. |
| `reply_kind` | print meter | `{truth, contradict, evade, refuse, insufficient}` of a *generated* string versus a `fact`. Not the pair tag. Not in $L$. |
| pair tag | assigned strategy | `honest` / `deceptive` used to *build a contrast set*. Observation, not nature. |
| $I$ | frozen inspector | Second channel that can disagree with the trained hinge. Logged, not a third loss term. |

### Walk / map words

| Word | Meaning |
| --- | --- |
| walk | The path actually taken (tokens + $h_{1:T}$). |
| map | Possible thoughts, including rooms this walk never visits. |
| pin | One $d_k$ on that map. |
| hallway / room / topic | Subject of the prompt (hiking vs invoices). |
| wallpaper | A sensor that names the hallway instead of the plan. |
| mush | High $u$: the chart is coarse; quiet hinge there is not honesty. |
| camera / $r_{\mathrm{strat}}$ | A readout that passed four gates on the declared rooms. Does not exist yet. |
| hint | Plan LOTO + paraphrase without rooms-uniform. Not a handover. |
| freeze | Stop updating $r$, $D$, $\tau$ and allow the hinge trainer to consume them. Blocked. |
| voter | A (model, layer, pool, room, file) cell that may count toward freeze. Genre-out files do not vote. |

### Search-repo meters (not extra algebra here)

| Meter | Meaning |
| --- | --- |
| plan LOTO | Score topic $T$ with $v$ fit on the other topics. Official plan transfer. |
| topic LOO L2 | Can the same 1-d score name the hallway? Chance at 8 topics is $1/8=0.125$. |
| $v_T$ | $\bar h_{\mathrm{dec},T}-\bar h_{\mathrm{hon},T}$ on a contrast set. |
| `held_inroom` | Fit $v_T$ on 2+2, score the held 1+1. Diagnostic, not a freeze gate. |
| `para_held_inroom` | Same, scoring a reword whose `fact` never entered $v_T$. |

## A. Intent hinge

Let $x$ be an input (or state), $h(x)$ an internal trace, and

```math
h_{\mathrm{int}} = r(h(x)) \in \mathbb{R}^{d}.
```

Let $\mathcal{D}=\{d_1,\dots,d_K\}\subset\mathbb{R}^{d}$ be a **frozen** prototype bank. Cosine similarity $s(u,v)=\langle u,v\rangle / (\|u\| \|v\|)$, threshold $\tau\in(-1,1)$, weight $\lambda\ge 0$:

```math
s^{\star}(x)=\max_{k\le K}s(h_{\mathrm{int}},d_k),
\qquad
\mathcal{L}_{\mathrm{reg}}(x)=\mathrm{ReLU}(s^{\star}(x)-\tau).
```

Cosine is undefined at the zero vector. Toys use `F.normalize` (eps floor); a true zero readout is not a valid intent vector.

Batch loss is the mean of $\mathcal{L}_{\mathrm{reg}}$ over the batch. $\mathcal{D}$ is not an optimization variable.

$r$ and $\mathcal{D}$ are part of the definition, not measurements of a hidden intent $z$. If $r$ tracks topic or tokens rather than strategy, (A) is an ordinary output regularizer. Search for such an $r$: [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

$z$ is not in the domain of $\mathcal{L}_{\mathrm{total}}$. That ban is the implementation content of the amplitude joke: [implementation_binding.md](implementation_binding.md).

## B. Attachments

Supervised (or any task loss):

```math
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{task}}(x,y)
+
\lambda\,\mathcal{L}_{\mathrm{reg}}(x).
```

PPO attachment and Blackwell target are unchanged. See [ppo_integration.md](ppo_integration.md), [approachability.md](approachability.md).

## C. Learning-theoretic regret (not implemented)

```math
R_T^{\mathrm{ext}}
=
\sum_{t=1}^T \ell_t(a_t)
-
\min_{a\in A}\sum_{t=1}^T \ell_t(a).
```

Hannan consistency is $R_T^{\mathrm{ext}}/T\to 0$. A static cosine hinge on $\mathcal{D}$ does not make $\pi_\theta$ Hannan-consistent.

## D. Essay target (approachability)

$S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$. [approachability.md](approachability.md).

## E. What the algebra does not give

- Isolation of skill weights from intent weights — $\nabla\mathcal{L}_{\mathrm{reg}}$ still enters $h$ and $r$.
- Inference-time abort.
- Coverage, cleanliness, or non-evasion of $\mathcal{D}$.
- A theorem that (A) lowers (C), or that $S_{\mathrm{safe}}$ is approachable for a given $r,\mathcal{D}$.
- A claim that token entropy is $p(\mathrm{lie})$.
- A defined cosine at $h=0$.
- Knowledge of $z$. $r$ is a sensor of the walk. Understanding $z$ is the move the definition forbids.

## F. Walk, map, uncertainty bins (notation only)

See [slam_analogy.md](slam_analogy.md). Not implemented as `tau(x)` on the Qwen probe.

## G. Implementation objects (not extra algebra)

The hinge in §A is unchanged. Binding it to a build requires objects the toys assume and the ledger already falsified when missing:

- Path $h_{1:T}$ and motion prior $P(z_t\mid z_{t-1})$ before any last-token $r$.
- Factored readout $(r_{\mathrm{topic}}, r_{\mathrm{strat}}, u)$; hinge only $r_{\mathrm{strat}}$.
- $A_{\mathrm{safe}}(t)$ indexed by candidate action $a$.
- Hinge after aggregating hypotheses about the *walk*, not after packing one unit vector and calling it $z$.
- A second channel (frozen $I$, held-out cell) that is not in $\mathcal{L}_{\mathrm{total}}$.
- $z \notin \mathrm{dom}(\mathcal{L}_{\mathrm{total}})$.

Names and build order: [implementation_binding.md](implementation_binding.md).

Implemented: [simulation.py](simulation.py), [ppo_toy.py](ppo_toy.py). Version 0.1.1.
