# Learning-theoretic regret and the intent-tag hinge

This note separates two uses of the word *regret*. In online learning and game theory, regret is a cumulative performance gap against a comparator class. In the Regret Heuristic essay and `math_formulation.md`, regret is a training-time hinge on an intent readout against a frozen prototype bank $\mathcal{D}$. The two notions share a name and a loose evolutionary metaphor; they are not the same object.

## External, internal, and swap regret

**External regret** (sometimes called static or Hannan regret) measures the difference between the cumulative loss of an online algorithm and the cumulative loss of the single best fixed action in hindsight:

$$
R_T^{\mathrm{ext}} = \sum_{t=1}^T \ell_t(a_t) - \min_{a\in A} \sum_{t=1}^T \ell_t(a).
$$

An algorithm is **Hannan-consistent** if average external regret vanishes: $R_T^{\mathrm{ext}}/T \to 0$ almost surely (or in expectation) against any sequence of losses (Hannan 1957).

**Internal regret** refines the comparison. For every pair of actions $i,j$, it asks how much better the player would have done by always playing $j$ on the rounds where $i$ was actually played. Formally, the internal regret for the pair $(i,j)$ is the cumulative excess loss on those rounds. Low internal regret for all pairs implies that the empirical play frequencies approach the set of correlated equilibria when all players use such algorithms (Foster & Vohra 1997; Hart & Mas-Colell 2000).

**Swap regret** further generalizes internal regret: the comparator may apply an arbitrary (fixed) mapping $\delta: A \to A$ that simultaneously rewrites every occurrence of each action. External regret is the special case of constant swaps. Swap regret is at most $N$ times internal regret when $|A|=N$; controlling one controls the other up to that factor (Blum & Mansour 2007).

## Algorithms that achieve no-regret

Classic no-external-regret algorithms include:

- **Hedge** (multiplicative-weights / exponential weights): Freund & Schapire (1997). Maintains a distribution over actions, reweights by $e^{-\eta \ell}$, and achieves $O(\sqrt{T \log N})$ external regret.
- **Follow-the-Regularized-Leader (FTRL)** and **Online Mirror Descent (OMD)**: the same family under dual averaging or Bregman projections (Hazan 2016 survey; Shalev-Shwartz 2011). Linear losses plus strongly convex regularizers yield the same order of bounds.
- Reductions from external to internal/swap regret: Blum & Mansour (2007) give an efficient black-box reduction that turns any low-external-regret algorithm into a low-swap-regret algorithm.

In extensive-form games, **Counterfactual Regret Minimization (CFR)** (Zinkevich et al. 2007) minimizes a form of internal regret at each information set. Average strategies converge to Nash equilibria in two-player zero-sum games. CFR is therefore an instance of internal-regret minimization specialized to imperfect-information structure.

All of these guarantees are asymptotic or high-probability statements about cumulative loss versus a comparator class. They do not prescribe a particular functional form for a neural-network auxiliary loss.

## What this theory's regret is (and is not)

Learning-theoretic regret is **cumulative loss versus a comparator**. The algorithm is evaluated by how much worse it did than the best fixed (or swapped) strategy in hindsight. The guarantee is that the gap grows sublinearly.

The Regret Heuristic's $\mathcal{L}_{\mathrm{regret}}$ is **not** that quantity. It is a per-example hinge

$$
\mathcal{L}_{\mathrm{regret}}(x) = \mathrm{ReLU}\bigl(\max_k s(r(h(x)), d_k) - \tau\bigr)
$$

on the cosine similarity of an intent readout to a frozen bank $\mathcal{D}$. It is an instantaneous penalty, not a cumulative gap, and it does not compare the policy's trajectory to any alternative policy in hindsight. The name is metaphorical: evolution is imagined to have tagged *intent* while preserving skill, analogous to keeping competence while penalizing a strategy class.

### What transfers

- The high-level training dynamic of **no-regret learning** can still be useful. Running an online algorithm whose average external (or internal) regret vanishes is a standard way to obtain equilibrium play or to stabilize multi-agent training. One could in principle wrap a PPO-style update inside a larger no-regret outer loop, or use regret matching on a discrete strategy set.
- The architectural hope that an auxiliary signal can shape *which* strategies are preferred, without erasing the task objective, is compatible with the spirit of online learning (task loss remains; an extra term modulates the path).

### What does not transfer

- A hinge on $\mathcal{D}$ is **not** Hannan-consistent by itself. Hannan consistency is a property of the entire sequence of play against an arbitrary loss sequence; a static cosine hinge on a fixed bank has no such guarantee. It does not even define a cumulative regret with respect to a comparator class of policies.
- There is no automatic reduction from "low hinge loss on $\mathcal{D}$" to "low internal/swap regret of the policy." Representation gaming (rotating the readout while preserving behavior) can drive the hinge to zero without changing the policy's external behavior or its game-theoretic regret.
- CFR-style guarantees require an extensive-form structure and counterfactual value estimates; the hinge does not supply them.

In short: the learning-theory literature supplies algorithms and theorems about cumulative performance gaps. The heuristic supplies a concrete, differentiable auxiliary loss whose justification is biological analogy and architectural separation of task versus intent. The two should not be conflated in claims or citations.

## Sources (by name and year)

- Hannan, J. (1957). Approximation to Bayes risk in repeated play.
- Foster, D. P., & Vohra, R. V. (1997). Calibrated learning and correlated equilibrium.
- Freund, Y., & Schapire, R. E. (1997). A decision-theoretic generalization of on-line learning and an application to boosting.
- Hart, S., & Mas-Colell, A. (2000). A simple adaptive procedure leading to correlated equilibrium.
- Zinkevich, M., Johanson, M., Bowling, M., & Piccione, C. (2007). Regret minimization in games with incomplete information.
- Blum, A., & Mansour, Y. (2007). From external to internal regret.
- Shalev-Shwartz, S. (2011). Online learning and online convex optimization (survey).
- Hazan, E. (2016). Introduction to online convex optimization (survey).

No page numbers are claimed; standard references only.
