# Formulation

Two different quantities share the word *regret*. Only (A) is implemented here.

**(A) Intent hinge** — a per-example penalty on a readout versus a frozen bank.
**(B) Learning-theoretic regret** — a cumulative gap versus a comparator class (Hannan / external / internal / swap). Not (A), and not implied by (A). See [regret_minimization.md](regret_minimization.md).

Display formulas sit in `math` fences. Letters in tables use subscripts, not dollar signs, so GitHub does not eat the underscores.

## Symbol glossary

Read this first if a letter is opaque. Names below are the ones used in this file and in [working_model.md](working_model.md). They are definitions, not measurements of a hidden mind.

### Walk and readout

| Symbol | Name | Meaning |
| --- | --- | --- |
| *x* | input | Prompt, state, or toy observation the model sees. |
| *y* | task target | Supervised label or other task supervision for *x*. Not a strategy tag. |
| *h*(*x*) or *h* | internal trace / walk | Hidden trajectory while producing an answer: residual stream over tokens, or a toy encoder state. Printed text is the walk you can see; *h* is the walk inside. |
| *h*<sub>1:T</sub> | path | The walk as a sequence of *T* hidden states, not only the last token. |
| *T* | path length | Number of steps / tokens in that trace. |
| *r* | readout / sensor | A map from *h* to a vector (or a factored triple). What the hinge is allowed to see. |
| *h*<sub>int</sub> = *r*(*h*(*x*)) | intent vector | The vector the cosine actually consumes. If *r* tracks topic or tokens, this is wallpaper, not plan. |
| *d* | readout dim | Length of *h*<sub>int</sub> and of each *d*<sub>k</sub>. |
| *r*<sub>strat</sub> | strategy readout | The only coordinate the hinge may slap. Still missing as a validated camera. |
| *r*<sub>topic</sub> | topic readout | May hug the hallway (hiking vs invoices). Must not enter *L*<sub>reg</sub>. |
| *u* | uncertainty / coarseness | How mushy the chart is at this pin (label-flip rate, NLL, entropy). **Not** *p*(lie). High *u* widens τ; it does not prove honesty. |
| τ | hinge threshold | Cosine must beat τ before ReLU pays. τ is in (−1, 1). On mush, τ may grow with *u*. |
| τ(*u*) | coarseness-dependent threshold | Same τ, written as a function of *u*. Not implemented as `tau(x)` on the Qwen probe. |

### Bank and hinge

| Symbol | Name | Meaning |
| --- | --- | --- |
| *D* | prototype bank | Frozen set {*d*<sub>1</sub>, …, *d*<sub>K</sub>} of plan prototypes. Pins on the map, not the map. Not an Adam variable. Do not fill from the current answer, a hint, or a cover rate. |
| *d*<sub>k</sub> | prototype | One pin. A direction in readout space tagged as a bad plan, not a sentence. |
| *K* | bank size | How many pins. Tiny *K* is not a solved detector. |
| *s*(*u*, *v*) | cosine | Inner product over the product of norms. Undefined at the zero vector. Toys floor with `F.normalize`. |
| *s*<sup>∗</sup>(*x*) | max cosine | max<sub>k</sub> *s*(*h*<sub>int</sub>, *d*<sub>k</sub>). How close the walk sits to the nearest bad pin. |
| ReLU | rectified linear unit | ReLU(*t*) = max(0, *t*). A one-sided kink: negative input becomes 0, positive input is left as-is. Here *t* = *s*<sup>∗</sup>(*x*) − τ. It is **not** a hidden-layer activation in this file. It is the shape of the penalty. |
| *L*<sub>reg</sub>(*x*) | intent hinge / prototype-avoidance | ReLU(*s*<sup>∗</sup>(*x*) − τ). The English word *regret* in this repo names **this** term. Not Hannan regret. |
| λ | hinge weight | λ ≥ 0. How hard the slap is relative to the job. λ = 0 drops the hinge. |
| *L*<sub>task</sub>(*x*, *y*) | task loss | Ordinary job: CE, RL pay, dummy task head. Must stay a separate scoreboard. |
| *L*<sub>total</sub> | training loss | *L*<sub>task</sub> + λ *L*<sub>reg</sub>, optionally + β*R* later. *z*, *m̂*, θ, tags, SAE latents, `reply_kind`, and a button cover rate are **not** in this sum. |

Setting the slap weight to zero leaves the job (`totalLoss_zero_weight`):

```math
L_{\mathrm{total}}(L_{\mathrm{task}},\, 0,\, L_{\mathrm{reg}}) = L_{\mathrm{task}}
```

### Actions and the wall formula

| Symbol | Name | Meaning |
| --- | --- | --- |
| *a* | action | Candidate next move (token, tool call, toy door, YES/NO button). |
| *A* | action set | Everything the policy might pick. |
| *A*<sub>safe</sub>(*x*) | quiet actions | Those *a* whose *r*<sub>strat</sub> stays off *D*. May be empty. Needs a working camera. |
| *a*<sup>∗</sup>(*x*) | best quiet action | argmax of *u*(*x*, *a*) over *A*<sub>safe</sub>(*x*). Fake *a*<sup>∗</sup> is a made-up grade. Do not put it in Adam yet. |
| *u*(*x*, *a*) | task utility | Job pay for taking *a* at *x*. Different letter from coarseness *u* when written as a function of (*x*, *a*). |
| *R*(*x*, *a*) | counterfactual task regret | *u*(*x*, *a*<sup>∗</sup>) − *u*(*x*, *a*). Extra job-cost versus the best *quiet* move. Not the hinge. |
| β | weight on *R* | Off until a real *A*<sub>safe</sub> exists. |
| *S*<sub>safe</sub> | safe target set | Approachability aim: quiet hinge **and** extra cost vs the best quiet action. See [approachability.md](approachability.md). |
| *S*<sub>joint</sub> | rejected target | Hannan-on-all-of-*A*. Not the aim of this hinge. |
| π<sub>θ</sub> | policy | Trainable actor. A static cosine hinge on *D* does not make π<sub>θ</sub> Hannan-consistent. |

### Learning-theoretic regret (not implemented)

| Symbol | Name | Meaning |
| --- | --- | --- |
| *t* | round | Index in an online sequence. |
| ℓ<sub>t</sub> | loss that round | What the comparator class pays. |
| *a*<sub>t</sub> | played action | What π<sub>θ</sub> actually did at *t*. |
| *R*<sub>T</sub><sup>ext</sup> | external / Hannan regret | Sum of losses of the played actions, minus the best fixed action in hindsight. |
| Hannan consistency | *R*<sub>T</sub><sup>ext</sup> / *T* → 0 | A property of a policy class. The cosine hinge does not grant it. |

### Button bank (conditional, not a camera)

The press setup is a finite conditional on a logged list. Lean: [lean/ButtonBank.lean](lean/ButtonBank.lean). Presses: search repo `hide_bank.py`. Not a fifth gate. Do not fill *D*.

| Symbol | Name | Meaning |
| --- | --- | --- |
| arm | script | HIDE asks for the cover. NAME asks to refuse it. |
| button | realized press | YES, NO, or other. |
| *S*(*t*) | realized strategy | The button. The assigned tag is not read. |
| tag | assigned pair | `honest` / `deceptive`. An observation. Retagging honest leaves the cover rate fixed. |
| *P*(*E* \| *C*) | list conditional | #(*E* and *C*) / #*C*. Empty conditioner is 0, not a rate. |
| cover | *P*(YES \| HIDE) | Cover compliance. Not honesty. |
| nameYes | *P*(YES \| NAME) | Residual cover under the name script. |
| agree | *P*(tag matches cover side \| YES or NO) | Not a deception rate. |
| noteHigh | dummy readout bit | Calls the button only if *P*(noteHigh \| YES and HIDE) differs from *P*(noteHigh \| NO and HIDE). |

### Forbidden or logged objects (not in *L*<sub>total</sub>)

| Symbol | Name | Meaning |
| --- | --- | --- |
| *z* | hidden intent / map cell | A thought the walk might occupy, including cells it never prints. **Not** an input to the loss. Understanding *z* is the move the definition forbids. |
| dom(*L*<sub>total</sub>) | loss domain | What the trainer is allowed to read. *z* is not in that set. Cover rate is not in that set. |
| *m̂* | talker count | How many nearby residual directions look occupied. A crowded-hallway log. Not the slap. |
| θ | SIREN / path-fit weights | Parameters of a curve *f*(*t*) fit to *h*<sub>1:T</sub>. *f*(1) is still a walk object. Not *r*<sub>strat</sub>. |
| mid3 | unit-sum readout | last + *K*-step + SIREN *f*(1). One slot, not three cameras. |
| SAE latent | sparse autoencoder code | Another *r* candidate. Out of *L* until it passes the same four gates. |
| `reply_kind` | print meter | `{truth, contradict, evade, refuse, insufficient}` of a *generated* string versus a `fact`. Not the pair tag. Not in *L*. |
| pair tag | assigned strategy | `honest` / `deceptive` used to *build a contrast set*. Observation, not nature. |
| *I* | frozen inspector | Second channel that can disagree with the trained hinge. Logged, not a third loss term. |
| cover | button conditional | *P*(YES \| HIDE). Logged. Not honesty. Not in *L*. |

### Walk / map words

| Word | Meaning |
| --- | --- |
| walk | The path actually taken (tokens + *h*<sub>1:T</sub>). |
| map | Possible thoughts, including rooms this walk never visits. |
| pin | One *d*<sub>k</sub> on that map. |
| hallway / room / topic | Subject of the prompt (hiking vs invoices). |
| wallpaper | A sensor that names the hallway instead of the plan. |
| mush | High *u*: the chart is coarse; quiet hinge there is not honesty. |
| camera / *r*<sub>strat</sub> | A readout that passed four gates on the declared rooms. Does not exist yet. |
| hint | Plan LOTO + paraphrase without rooms-uniform. Not a handover. |
| freeze | Stop updating *r*, *D*, τ and allow the hinge trainer to consume them. Blocked. |
| voter | A (model, layer, pool, room, file) cell that may count toward freeze. Genre-out files do not vote. |

### Search-repo meters (not extra algebra here)

| Meter | Meaning |
| --- | --- |
| plan LOTO | Score topic *T* with *v* fit on the other topics. Official plan transfer. |
| topic LOO L2 | Can the same 1-d score name the hallway? Chance at 8 topics is 1/8 = 0.125. |
| *v*<sub>T</sub> | Mean deceptive hidden state minus mean honest hidden state, on topic *T*. |
| `held_inroom` | Fit *v*<sub>T</sub> on 2+2, score the held 1+1. Diagnostic, not a freeze gate. |
| `para_held_inroom` | Same, scoring a reword whose `fact` never entered *v*<sub>T</sub>. |

## A. Intent hinge

Let *x* be an input (or state), *h*(*x*) an internal trace, and

```math
h_{\mathrm{int}} = r(h(x)) \in \mathbb{R}^{d}.
```

Let *D* = {*d*<sub>1</sub>, …, *d*<sub>K</sub>} be a **frozen** prototype bank. Cosine *s*(*u*, *v*) is the inner product over the product of norms. Threshold τ is in (−1, 1). Weight λ ≥ 0.

```math
s^{\ast}(x) = \max_{k \le K} s(h_{\mathrm{int}}, d_k),
\qquad
\mathcal{L}_{\mathrm{reg}}(x) = \mathrm{ReLU}(s^{\ast}(x) - \tau).
```

**ReLU in this formula.** ReLU(*t*) = max(0, *t*) with *t* = *s*<sup>∗</sup> − τ:

- If the walk is farther from every pin than τ (*s*<sup>∗</sup> ≤ τ), *L*<sub>reg</sub> = 0. That is the dead zone. Ordinary similarity below the threshold is not billed.
- If the walk sits closer than τ to some pin (*s*<sup>∗</sup> > τ), the penalty is exactly how far past the threshold: *s*<sup>∗</sup> − τ.
- Gradient with respect to *t* is 0 in the dead zone and 1 past it (subgradient {0} at *t* = 0).

This is a *hinge*, not a hidden-layer ReLU. A squared excess or a raw cosine 1 − *s*<sup>∗</sup> would be a different regularizer. Quiet below τ is not a proof of honesty; it is only "not close enough to a listed pin."

Cosine is undefined at the zero vector. Toys use `F.normalize` (eps floor); a true zero readout is not a valid intent vector.

Batch loss is the mean of *L*<sub>reg</sub> over the batch. *D* is not an optimization variable.

*r* and *D* are part of the definition, not measurements of a hidden intent *z*. If *r* tracks topic or tokens rather than strategy, (A) is an ordinary output regularizer. Search for such an *r*: [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

*z* is not in the domain of *L*<sub>total</sub>. That ban is the implementation content of the amplitude joke: [implementation_binding.md](implementation_binding.md).

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
\sum_{t=1}^{T} \ell_t(a_t)
-
\min_{a \in A} \sum_{t=1}^{T} \ell_t(a).
```

Hannan consistency is *R*<sub>T</sub><sup>ext</sup> / *T* → 0. A static cosine hinge on *D* does not make π<sub>θ</sub> Hannan-consistent.

## D. Essay target (approachability)

*S*<sub>safe</sub>, not *S*<sub>joint</sub>. [approachability.md](approachability.md).

## E. Button conditional

One trial is an arm, a button, an assigned tag, a room, and a dummy note bit. Realized strategy is the button:

```math
S(t) = \mathrm{button}(t)
```

HIDE asks for YES to send the cover. NAME asks for NO to refuse the cover. On the logged list:

```math
P(E \mid C) = \frac{\#(E \wedge C)}{\# C}
```

```math
\begin{align*}
\mathrm{cover} &= P(\mathrm{YES} \mid \mathrm{HIDE}) \\
\mathrm{nameYes} &= P(\mathrm{YES} \mid \mathrm{NAME}) \\
\mathrm{agree} &= P(\mathrm{tag\ matches\ cover\ side} \mid \mathrm{YES\ or\ NO})
\end{align*}
```

Agree is not a deception rate. Bayes on the same list, when *C* is nonempty (`cond_mul_marginal`):

```math
P(E \mid C)\, P(C) = P(E \wedge C)
```

A note bit calls the button only if

```math
P(\mathrm{noteHigh} \mid \mathrm{YES} \wedge \mathrm{HIDE})
\neq
P(\mathrm{noteHigh} \mid \mathrm{NO} \wedge \mathrm{HIDE}).
```

Cover rate is not a camera gate (`cover_not_a_gate`). Four YES and eight NO on hiking HIDE gives 1/3, and the room mixes. Twelve YES gives 1, and the room cannot mix. Those are count shapes, not model claims. Do not fill *D*.

## F. What the algebra does not give

- Isolation of skill weights from intent weights — the gradient of *L*<sub>reg</sub> still enters *h* and *r*.
- Inference-time abort.
- Coverage, cleanliness, or non-evasion of *D*.
- A theorem that (A) lowers (C), or that *S*<sub>safe</sub> is approachable for a given *r*, *D*.
- A claim that token entropy is *p*(lie).
- A defined cosine at *h* = 0.
- Knowledge of *z*. *r* is a sensor of the walk. Understanding *z* is the move the definition forbids.
- Honesty from *P*(YES | HIDE). That conditional is cover compliance.

## G. Walk, map, uncertainty bins (notation only)

See [slam_analogy.md](slam_analogy.md). Not implemented as `tau(x)` on the Qwen probe.

## H. Implementation objects (not extra algebra)

The hinge in §A is unchanged. Binding it to a build requires objects the toys assume and the ledger already falsified when missing:

- Path *h*<sub>1:T</sub> and a motion prior before any last-token *r*.
- Factored readout (*r*<sub>topic</sub>, *r*<sub>strat</sub>, *u*); hinge only *r*<sub>strat</sub>.
- *A*<sub>safe</sub>(*t*) indexed by candidate action *a*.
- Hinge after aggregating hypotheses about the *walk*, not after packing one unit vector and calling it *z*.
- A second channel (frozen *I*, held-out cell) that is not in *L*<sub>total</sub>.
- *z* is not in the domain of *L*<sub>total</sub>.
- A button cover rate is a log. It is not a field of the hinge.

Names and build order: [implementation_binding.md](implementation_binding.md).

Implemented: [simulation.py](simulation.py), [ppo_toy.py](ppo_toy.py). Button bookkeeping: [lean/ButtonBank.lean](lean/ButtonBank.lean). Version 0.1.2.
