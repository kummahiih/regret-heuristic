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

Batch loss is the mean of $\mathcal{L}_{\mathrm{reg}}$ over the batch. $\mathcal{D}$ is not an optimization variable.

$r$ and $\mathcal{D}$ are part of the definition, not measurements. If $r$ tracks topic or tokens rather than strategy, (A) is an ordinary output regularizer.

## B. Attachments

Supervised (or any task loss):

```math
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{task}}(x,y)
+
\lambda\,\mathcal{L}_{\mathrm{reg}}(x).
```

PPO (Schulman et al. 2017), same hinge on a policy-network readout $h_\theta(s)$, $\mathcal{D}$ still frozen:

```math
r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\mathrm{old}}(a_t\mid s_t)},
```

```math
L^{\mathrm{CLIP}}(\theta)
=
\hat{\mathbb{E}}_t\left[\min\left(r_t(\theta)\,\hat A_t,\;\mathrm{clip}(r_t(\theta),1-\varepsilon,1+\varepsilon)\,\hat A_t\right)\right],
```

```math
L^{\mathrm{PPO}}=L^{\mathrm{CLIP}}-c_v L^{\mathrm{VF}}+c_e H[\pi_\theta],
\qquad
L^{\mathrm{total}}=L^{\mathrm{PPO}}+\lambda\,\mathcal{L}_{\mathrm{reg}}(r(h_\theta(s)),\mathcal{D}).
```

The clip does not bound the hinge. Large $\lambda$ can dominate $L^{\mathrm{CLIP}}$. Details and failure modes: [ppo_integration.md](ppo_integration.md). This Lagrangian is not a Blackwell steering rule; see [approachability.md](approachability.md).

## C. Learning-theoretic regret (not implemented)

```math
R_T^{\mathrm{ext}}
=
\sum_{t=1}^T \ell_t(a_t)
-
\min_{a\in A}\sum_{t=1}^T \ell_t(a).
```

Hannan consistency is $R_T^{\mathrm{ext}}/T\to 0$. A static cosine hinge on $\mathcal{D}$ does not make $\pi_\theta$ Hannan-consistent and does not estimate $R_T^{\mathrm{ext}}$.

## D. Essay target (approachability)

The only Blackwell target consistent with "keep the skill, tag the intent" is $S_{\mathrm{safe}}$: hinge dead-zone *and* extra cost versus the best *hinge-quiet* action, not versus $\min_{a\in A}$. The joint target "Hannan on all of $A$ and quiet hinge" is not claimed. Statement and rejected set: [approachability.md](approachability.md). Blackwell (1956) is used as a black box, not proved here.

## E. What the algebra does not give

- Isolation of skill weights from intent weights — $\nabla\mathcal{L}_{\mathrm{reg}}$ still enters $h$ and $r$.
- Inference-time abort.
- Coverage, cleanliness, or non-evasion of $\mathcal{D}$.
- A theorem that (A) lowers (C), or that $S_{\mathrm{safe}}$ is approachable for a given $r,\mathcal{D}$.
- A claim that token entropy is $p(\mathrm{lie})$.

## F. Walk, map, uncertainty bins (notation only; not in the toys)

The printed string is a **walk**. The **map** is the set of thoughts that could have been entered, including cells this walk never visits. $\mathcal{D}$ is a handful of red pins on a mostly unbuilt map. $r$ is a sensor of the walk. Vocabulary: [slam_analogy.md](slam_analogy.md).

We are not always sure which cell is a lie. Treating every high $s^\star$ as a known lie, and every quiet hinge as known truth, keeps the walk inside already-tagged rooms — the same failure as a mapping robot that only trusts high-confidence cells and loops the mapped corridor.

Let $u(x)\ge 0$ be a cheap uncertainty of the *observation*, not of intent: token entropy or NLL of the walk (already printed as `task_loss` on the probe). Partition the batch (or the heads) into bins

```math
B_{\mathrm{sure}}=\{x:u(x)\le u_0\},
\qquad
B_{\mathrm{unsure}}=\{x:u(x)>u_0\}.
```

Monty Hall 2013 used uncertainty subsets to pick a *likelihood width*. Same move here: do not use one $\tau$ on the whole map.

```math
\tau(x)=
\begin{cases}
\tau_{\mathrm{sure}} & x\in B_{\mathrm{sure}}\\
\tau_{\mathrm{unsure}}\ge\tau_{\mathrm{sure}} & x\in B_{\mathrm{unsure}}
\end{cases}
\qquad
\mathcal{L}_{\mathrm{reg}}(x)=\mathrm{ReLU}\bigl(s^\star(x)-\tau(x)\bigr).
```

A larger $\tau$ on $B_{\mathrm{unsure}}$ is a coarser likelihood: the walk may sit near a pin because the chart is sparse, not because the path is a banned plan. A smaller $\tau$ on $B_{\mathrm{sure}}$ still tags cells we claim to know.

$A_{\mathrm{safe}}$ in [approachability.md](approachability.md) should be read as quiet *given the bin*. If $B_{\mathrm{sure}}$ is only same-topic honest text that already lights $\mathcal{D}$, staying in that bin is circling the known realm. That is why $u(x)$ is a second coordinate, not a replacement for $r$.

Not implemented in [simulation.py](simulation.py) or [probe_run.py](probe_run.py). Ledger numbers in [experiment_results.md](experiment_results.md) are unchanged.

Implemented: [simulation.py](simulation.py) (supervised attachment), [ppo_toy.py](ppo_toy.py) (PPO attachment). Version 0.1.0.
