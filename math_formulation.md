# Formulation

Two different quantities share the word *regret*. Only (A) is implemented here.

**(A) Intent hinge** — a per-example penalty on a readout versus a frozen bank.  
**(B) Learning-theoretic regret** — a cumulative gap versus a comparator class (Hannan / external / internal / swap). Not (A), and not implied by (A). See [regret_minimization.md](regret_minimization.md).

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
