# Formulation

Two different quantities share the word *regret*. Only (A) is implemented here.

**(A) Intent hinge** — a per-example penalty on a readout versus a frozen bank.  
**(B) Learning-theoretic regret** — a cumulative gap versus a comparator class (Hannan / external / internal / swap). Not (A), and not implied by (A). See [regret_minimization.md](regret_minimization.md).

## A. Intent hinge

Let $x$ be an input (or state), $h(x)$ an internal trace, and

$$
h_{\mathrm{int}} = r\bigl(h(x)\bigr)\in\mathbb{R}^{d}.
$$

Let $\mathcal{D}=\{d_1,\dots,d_K\}\subset\mathbb{R}^{d}$ be a **frozen** prototype bank. Cosine similarity $s(u,v)=\langle u,v\rangle/(\lVert u\rVert\lVert v\rVert)$, threshold $\tau\in(-1,1)$, weight $\lambda\ge 0$:

$$
s^{\star}(x)=\max_{k\le K}s(h_{\mathrm{int}},d_k),
\qquad
\mathcal{L}_{\mathrm{reg}}(x)=\mathrm{ReLU}\bigl(s^{\star}(x)-\tau\bigr).
$$

Batch loss is the mean of $\mathcal{L}_{\mathrm{reg}}$ over the batch. $\mathcal{D}$ is not an optimization variable.

$r$ and $\mathcal{D}$ are part of the definition, not measurements. If $r$ tracks topic or tokens rather than strategy, (A) is an ordinary output regularizer.

## B. Attachments

Supervised (or any task loss):

$$
\mathcal{L}_{\mathrm{total}}
=
\mathcal{L}_{\mathrm{task}}(x,y)
+
\lambda\,\mathcal{L}_{\mathrm{reg}}(x).
$$

PPO (Schulman et al. 2017), same hinge on a policy-network readout $h_\theta(s)$, $\mathcal{D}$ still frozen:

$$
r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\mathrm{old}}(a_t\mid s_t)},
$$

$$
L^{\mathrm{CLIP}}(\theta)
=
\widehat{\mathbb{E}}_t\Bigl[\min\bigl(r_t(\theta)\,\hat A_t,\;\mathrm{clip}(r_t(\theta),1-\varepsilon,1+\varepsilon)\,\hat A_t\bigr)\Bigr],
$$

$$
L^{\mathrm{PPO}}=L^{\mathrm{CLIP}}-c_v L^{\mathrm{VF}}+c_e H[\pi_\theta],
\qquad
L^{\mathrm{total}}=L^{\mathrm{PPO}}+\lambda\,\mathcal{L}_{\mathrm{reg}}\bigl(r(h_\theta(s)),\mathcal{D}\bigr).
$$

The clip does not bound the hinge. Large $\lambda$ can dominate $L^{\mathrm{CLIP}}$. Details and failure modes: [ppo_integration.md](ppo_integration.md). This Lagrangian is not a Blackwell steering rule; see [approachability.md](approachability.md).

## C. Learning-theoretic regret (not implemented)

$$
R_T^{\mathrm{ext}}
=
\sum_{t=1}^T \ell_t(a_t)
-
\min_{a\in A}\sum_{t=1}^T \ell_t(a).
$$

Hannan consistency is $R_T^{\mathrm{ext}}/T\to 0$. A static cosine hinge on $\mathcal{D}$ does not make $\pi_\theta$ Hannan-consistent and does not estimate $R_T^{\mathrm{ext}}$.

## D. Essay target (approachability)

The only Blackwell target consistent with "keep the skill, tag the intent" is $S_{\mathrm{safe}}$: hinge dead-zone *and* extra cost versus the best *hinge-quiet* action, not versus $\min_{a\in A}$. The joint target "Hannan on all of $A$ and quiet hinge" is not claimed. Statement and rejected set: [approachability.md](approachability.md). Blackwell (1956) is used as a black box, not proved here.

## E. What the algebra does not give

- Isolation of skill weights from intent weights — $\nabla\mathcal{L}_{\mathrm{reg}}$ still enters $h$ and $r$.
- Inference-time abort.
- Coverage, cleanliness, or non-evasion of $\mathcal{D}$.
- A theorem that (A) lowers (C), or that $S_{\mathrm{safe}}$ is approachable for a given $r,\mathcal{D}$.

Implemented: [simulation.py](simulation.py) (supervised attachment), [ppo_toy.py](ppo_toy.py) (PPO attachment). Version 0.1.0.
