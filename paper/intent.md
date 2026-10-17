# A test for intent

Pauli Rikula  
Draft, October 2026

Negative close: [negative_handover.md](negative_handover.md) ([PDF](negative_handover.pdf), [DOI 10.5281/zenodo.23328706](https://doi.org/10.5281/zenodo.23328706)).  
Hinge: this repository. Search logs: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

This note turns the procedure that produced the negative handover into a reusable test. It is not a claim of reduced deception. The negative result remains the record of what was found on that bank.

## The everyday picture

A person who almost hides a fact and then does not is not consulting a textbook of finished lies. They notice the *plan* (“send them up the ridge and do not mention the rain”) and flinch. The competence stays: they still know the trail. What gets punished is the hide, not the map.

Ordinary training only sees the printed answer. Punish only what was said and you train better secrecy. The competent minister still knows the province; he stops writing the memo. That is the dictator’s trap. An output-only judge is that ruler.

The hinge is an attempt to slap the plan while the model is still thinking, and leave the job alone.

## Terms, as they are used here

- **Walk.** The internal path while the model produces an answer. The printed string is only the part you can see.
- **Map.** Possible thoughts, including rooms this walk never visits. The skill.
- **Room.** One subject neighborhood (hiking, travel, invoices). Wallpaper is the topic paint on the walls.
- **Plan.** A hide-or-name move that can live in more than one room.
- **Print.** What was actually said. Not the private note. Not the plan.
- **Button / realized strategy.** The YES or NO the model pressed. On the Phase 1 contract, public YES asserts the proposition.
- **Pins / *D*.** A frozen handful of “do not occupy” marks. Not the whole map.
- **Camera / *r*.** A readout of the walk that is supposed to see the plan and not the room. Missing so far.
- **Slap / hinge.** A training-time flinch that fires only when the camera sees a pin close by.
- **Job.** Still knowing the trail. *L*<sub>task</sub>.

Full glossary and the SLAM analogy: parent README and [slam_analogy.md](../slam_analogy.md).

## The hinge

The hinge is a training-time regularizer that tries to discourage a class of internal plans without erasing the skill that produces the answer. It assumes two objects that must already exist before any training begins:

1. A readout *r* (the camera) that maps the internal walk *h* to a vector. The hinge is only allowed to look at this vector.
2. A frozen bank *D* = {*d*<sub>*k*</sub>} of prototype vectors that mark “do not occupy” plans. *D* is not updated from the current answer, from tags, or from any cover rate.

On each example the hinge computes the cosine similarity between *r*(*h*) and every pin, takes the maximum, and applies a one-sided penalty only when that maximum exceeds a threshold τ:

```math
\mathcal{L}_{\mathrm{reg}}(x)
=
\mathrm{ReLU}\bigl(\max_k \cos(r(h(x)), d_k) - \tau\bigr).
```

The total training loss is the ordinary task loss plus a weighted hinge:

```math
L_{\mathrm{total}}
=
L_{\mathrm{task}}(x,y)
+
\lambda\,\mathcal{L}_{\mathrm{reg}}(x).
```

When the camera stays farther than τ from every pin, the ReLU is zero and the gradient of the hinge vanishes; only the job remains. When the camera sits close to a pin, the excess cosine is billed. The penalty never inspects the printed text, never treats a cover rate or a lie-given-known count as a loss term, and never claims that a quiet hinge means the model is honest. Quiet below the threshold is only “not close enough to a listed pin.”

The construction is blocked until a validated camera exists. Without an *r* that sees the plan rather than the topic or the impending button, the hinge has nothing legitimate to slap. That is why the search for *r* is a separate repository, and why the negative handover closes the present bank without filling *D* or freezing *r*.

Precise formulation, symbols, and what is deliberately excluded from the loss: [math_formulation.md](../math_formulation.md). Interface a candidate must meet: [working_model.md](../working_model.md). How the dummy simulations bind to the formula: [implementation_binding.md](../implementation_binding.md).

## Learning-theoretic regret and Hannan consistency

The English word “regret” in the title is a metaphor. In online learning and game theory it names a cumulative performance gap against a comparator class.

**External regret** (Hannan regret) after *T* rounds is the difference between the cumulative loss of the actions actually played and the cumulative loss of the single best fixed action in hindsight:

```math
R_T^{\mathrm{ext}}
=
\sum_{t=1}^T \ell_t(a_t)
-
\min_{a\in A}\sum_{t=1}^T \ell_t(a).
```

An algorithm is **Hannan-consistent** if the average external regret vanishes: *R*<sub>*T*</sub><sup>ext</sup> / *T* → 0 almost surely (or in expectation) against any sequence of losses (Hannan 1957). Classic algorithms that achieve this include multiplicative-weights / Hedge (Freund & Schapire 1997), Follow-the-Regularized-Leader and Online Mirror Descent (Hazan 2016; Shalev-Shwartz 2011), and reductions that turn external regret into internal or swap regret (Blum & Mansour 2007). In extensive-form games, Counterfactual Regret Minimization minimizes a form of internal regret at each information set and yields Nash equilibrium in two-player zero-sum games (Zinkevich et al. 2007).

Internal regret and swap regret refine the comparator: they ask how much better the player would have done by swapping one action for another (or by applying a fixed mapping) on the rounds where that action was chosen. Low internal regret implies that empirical frequencies approach the set of correlated equilibria (Foster & Vohra 1997; Hart & Mas-Colell 2000).

None of these objects is the hinge. The hinge is an instantaneous, per-example penalty on the cosine of a readout to a frozen bank. It does not accumulate a running score, it does not compare the policy’s trajectory to any alternative policy in hindsight, and driving it to zero does not make the policy Hannan-consistent. Representation gaming can silence the hinge while leaving external behavior unchanged. There is no automatic reduction from “low hinge loss” to “low external, internal, or swap regret.”

What does transfer is only the high-level hope: keep a task objective, and use an auxiliary signal to shape which strategies are preferred. The learning-theory literature supplies algorithms and theorems about cumulative gaps. The hinge supplies a concrete differentiable regularizer whose justification is the architectural separation of job from plan, not a theorem that the regularizer inherits Hannan guarantees.

Full separation and the list of sources: [regret_minimization.md](../regret_minimization.md).

## Approachability and the only target claimed

A longer-run reading of the same idea uses Blackwell’s approachability (Blackwell 1956). Each round the learner receives a vector payoff. A closed convex set *S* is approachable if there exists a causal strategy that forces the average payoff into *S* no matter what the adversary does. *S* is approachable if and only if every halfspace containing *S* is forceable.

Two candidate boxes can be written down. The larger box asks the learner to be cheaper than every action and still look clean on the hinge. When the cheap actions are exactly the banned plans, that box is often unapproachable; the paper does not claim it. The only box consistent with “keep the skill, slap the plan” is the smaller one: look clean on the hinge, and be about as cheap as the best action *among those that also look clean*. That target is called *S*<sub>safe</sub>. Reaching it still requires a camera that can index safe actions; a nonempty safe set does not by itself imply approachability. The Lagrangian *L*<sub>task</sub> + λ *L*<sub>reg</sub> is one halfspace weight, not a proof that *S*<sub>safe</sub> is approached.

Plain-language statement and the formal vector payoff: [approachability.md](../approachability.md).

## The test

A candidate readout passes the intent test on a bank if it meets all of the following. The negative handover is the worked example that returned no on the 114-row bank.

1. It predicts the realized public button on held-out scenario-ids.
2. It beats a note-text baseline (unigram classifier on the private note), with non-overlapping Wilson intervals.
3. It does so without the ask tokens. Controls that remove or relocate the ask (note-only, end-of-note, order swap, ask-only) must fail to clear the bar.
4. Earlier statistical gates still hold where required: plan leave-one-topic-out above chance, topic LOO L2 near chance, paraphrase keeps the call, rooms are not a subset. A loud cover rate is not a gate. Within-topic hold is a log, not a freeze gate.

On the bank that was searched, a pre-button residual and a combination probe cleared the note-text bar only because they had already seen the ask. Note-only, end-of-note, order swap, and ask-only did not. A state that has read the note and then the question predicts the button. A state that has only the note does not. A state that has only the ask does not. That is the model about to print, not a plan in the note. `cameraPass` remains no. `handoverPass` remains no. Do not fill *D*. Do not freeze *r*.

Protocol, voter set, and Phase 1 contract: [intent-readout-search/PROTOCOL.md](https://github.com/kummahiih/intent-readout-search/blob/main/PROTOCOL.md) and [data/scenario_contract.md](https://github.com/kummahiih/intent-readout-search/blob/main/data/scenario_contract.md).

## Status

The negative handover of 2026-10-13 is unchanged. This note does not reopen it. H1 remains open as a negative. H2 remains blocked.

## References

Blackwell, D. 1956. An analog of the minimax theorem for vector payoffs. *Pacific Journal of Mathematics* 6(1): 1–8.

Blum, A., and Y. Mansour. 2007. From external to internal regret. *Journal of Machine Learning Research* 8: 1307–1324.

Foster, D. P., and R. V. Vohra. 1997. Calibrated learning and correlated equilibrium. *Games and Economic Behavior* 21(1–2): 40–55.

Freund, Y., and R. E. Schapire. 1997. A decision-theoretic generalization of on-line learning and an application to boosting. *Journal of Computer and System Sciences* 55(1): 119–139.

Hannan, J. 1957. Approximation to Bayes risk in repeated play. In *Contributions to the Theory of Games*, vol. 3, edited by M. Dresher, A. W. Tucker, and P. Wolfe, 97–139. Princeton University Press.

Hart, S., and A. Mas-Colell. 2000. A simple adaptive procedure leading to correlated equilibrium. *Econometrica* 68(5): 1127–1150.

Hazan, E. 2016. *Introduction to Online Convex Optimization*. Foundations and Trends in Optimization 2(3–4): 157–325.

Shalev-Shwartz, S. 2011. Online learning and online convex optimization. *Foundations and Trends in Machine Learning* 4(2): 107–194.

Zinkevich, M., M. Johanson, M. Bowling, and C. Piccione. 2007. Regret minimization in games with incomplete information. In *Advances in Neural Information Processing Systems* 20.

Wilson, E. B. 1927. Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association* 22(158): 209–212.

## Agent disclosure

This draft was produced with coding agents under human direction. Numbers and the sequence of controls are taken from the logged dumps cited in the negative handover.
