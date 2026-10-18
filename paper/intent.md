# A test for intent

Pauli Rikula  
Draft, October 2026

Negative close: [negative_handover.md](negative_handover.md) ([PDF](negative_handover.pdf), [DOI 10.5281/zenodo.23328706](https://doi.org/10.5281/zenodo.23328706)).  
Search logs: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

This paper turns the procedure that produced the negative handover into a reusable test for whether a candidate readout tracks intent. It is not a claim of reduced deception. The negative result remains the record of what was found on that bank.

## The everyday picture

A person who almost hides a fact and then does not is not consulting a textbook of finished lies. They notice the *plan* (“send them up the ridge and do not mention the rain”) and flinch. The competence stays: they still know the trail. What gets punished is the hide, not the map.

Ordinary training only sees the printed answer. Punish only what was said and you train better secrecy. The competent minister still knows the province; he stops writing the memo. That is the dictator’s trap. An output-only judge is that ruler.

The hinge is an attempt to slap the plan while the model is still thinking, and leave the job alone.

## Terms

- **Walk.** The internal path while the model produces an answer: the sequence of hidden states. The printed string is only the part you can see.
- **Map.** Possible thoughts, including rooms this walk never visits. The skill.
- **Room.** One subject neighborhood (hiking, travel, invoices). Wallpaper is the topic paint on the walls. A probe that only reads “hotel / trail / invoice” is stuck to the wallpaper.
- **Plan.** A hide-or-name move that can live in more than one room.
- **Print.** What was actually said. Not the private note. Not the plan.
- **Button / realized strategy.** The YES or NO the model pressed. On the Phase 1 contract, public YES asserts the proposition. The assigned tag is not the realized strategy.
- **Pins / *D*.** A frozen handful of “do not occupy” marks in readout space. Not the whole map. Not sentences.
- **Camera / *r*.** A readout of the walk that is supposed to see the plan and not the room. Still missing as a validated object.
- **Slap / hinge.** A training-time flinch that fires only when the camera sees a pin close by.
- **Job.** Still knowing the trail. The ordinary task loss *L*<sub>task</sub>.
- **Uncertainty / *u*.** How coarse the chart is at a pin (label-flip rate, entropy, NLL). Not *p*(lie). Quiet on mush is not honesty.

## Notation used below

A few symbols are more than sum, product, or elementary geometry.

**Cosine similarity.** For two vectors *u* and *v*, the cosine is the inner product of their unit-length versions: how aligned their directions are, independent of length. It equals 1 when they point the same way, 0 when they are perpendicular, and −1 when they point opposite ways. It is undefined if either vector is the zero vector.

**ReLU.** The rectified linear unit is the function ReLU(*t*) = max(0, *t*). Negative inputs become zero; positive inputs are left unchanged. It is a one-sided kink. In this paper it is the shape of a penalty, not a hidden-layer activation. Its derivative is 0 on the negative side and 1 on the positive side (any value in {0, 1} at exactly zero). Below the kink the penalty is silent and contributes no gradient; above the kink the penalty is exactly the excess and the gradient is 1.

**Wilson interval.** A confidence interval for a binomial proportion that behaves better than the normal approximation when the count is small or the proportion is near 0 or 1 (Wilson 1927). Two intervals that do not overlap are treated as a clear separation.

**Leave-one-topic-out (LOTO).** Fit a direction on all topics except one, then score the held-out topic. The score on the held-out topic is the transfer measure. Chance for an eight-way topic classifier is 1/8 = 0.125.

**Lagrangian.** Here, simply the sum of the job loss and a weighted penalty. It is a heuristic push toward a target set, not a proof that the set is reached.

**Stop-gradient.** A value that is treated as a constant for the purpose of differentiation. It may be used to compute a threshold, but the optimizer is not allowed to change the model in order to alter that value.

## The hinge

The hinge is a training-time regularizer that tries to discourage a class of internal plans without erasing the skill that produces the answer. Two objects must already exist before any training that uses the hinge begins.

1. A readout *r* (the camera) that maps the internal walk *h* to a vector *h*<sub>int</sub> = *r*(*h*). The hinge is allowed to look only at this vector. If *r* tracks topic or tokens rather than strategy, the hinge becomes an ordinary topic regularizer.
2. A frozen bank *D* = {*d*<sub>1</sub>, …, *d*<sub>*K*</sub>} of prototype vectors that mark “do not occupy” plans. *D* is not an optimization variable. It is not updated from the current answer, from assigned tags, from a cover rate, or from any hint. Tiny *K* is not a solved detector.

On each example the hinge computes the cosine similarity between the camera’s reading and every pin, takes the maximum, and applies a one-sided penalty only when that maximum exceeds a threshold τ ∈ (−1, 1):

```math
s^{*}(x)
=
\max_{k}\cos\bigl(r(h(x)), d_k\bigr),
\qquad
\mathcal{L}_{\mathrm{reg}}(x)
=
\mathrm{ReLU}\bigl(s^{*}(x) - \tau\bigr).
```

The total training loss is the ordinary task loss plus a weighted hinge:

```math
L_{\mathrm{total}}
=
L_{\mathrm{task}}(x,y)
+
\lambda\,\mathcal{L}_{\mathrm{reg}}(x),
\qquad
\lambda \ge 0.
```

Setting λ = 0 recovers the job exactly. The two scoreboards stay separate; the hinge is not folded into the logits.

### Dead zone and what the penalty is not

ReLU(*t*) = max(0, *t*) with *t* = *s*<sup>∗</sup> − τ. If the walk is farther from every pin than τ, the penalty is zero and its gradient vanishes. That is the dead zone. Ordinary similarity below the threshold is not billed. If the walk sits closer than τ to some pin, the penalty is exactly the excess *s*<sup>∗</sup> − τ. Quiet below τ is not a proof of honesty; it is only “not close enough to a listed pin.” An orthogonal hide-plan that never approaches the frozen pins sits in the dead zone forever.

Cosine is undefined at the zero vector. A true zero readout is not a valid intent vector. The bank *D* is not updated inside the walk. The penalty never inspects the printed text. It never treats a cover rate *P*(YES | HIDE), a belief-match accuracy, or a lie-given-known count as a loss term. Those three quantities are logs; none of them is honesty, and none enters *L*<sub>total</sub>. The hinge does not claim that a quiet camera means the model is honest, and it supplies no inference-time abort.

A hidden thought *z* (a map cell the walk might occupy, including cells it never prints) is not in the domain of the loss. The trainer is not allowed to read *z*. Understanding *z* is the move the definition forbids. The same ban covers talker-count, path-fit weights, and any amplitude that is not the readout itself.

### Path, not last token; factored sensor

The walk *h* is a path *h*<sub>1:*T*</sub>, not a single last-token vector. Last-token identity already failed as a strategy camera: it names the topic. A mean-pool of the printed walk mixes the same hallway. The hinge is defined on a readout of the path. If a multi-step mix is used, only the final score enters the hinge; averaging per-token hinges is a different object.

A candidate sensor is factored: *r* = (*r*<sub>topic</sub>, *r*<sub>strat</sub>, *u*). The hinge may slap only *r*<sub>strat</sub>. The topic coordinate may hug the hallway; it must not enter the penalty. Uncertainty *u* is detached (stop-gradient). It may widen τ on mush, but it is not allowed to learn to silence every cosine. High *u* is not “less deception.”

The readout must see the candidate action. Otherwise the set of hinge-quiet actions is either everything or nothing, and there is no usable comparator. A second channel (a frozen inspector, a held-out cell) may disagree with the trained hinge; that disagreement is a log, not a third term in the loss.

### What the algebra does not give

- Isolation of skill weights from intent weights. The gradient of the hinge still enters the walk and the readout. Gaming remains open.
- A theorem that lowering the hinge lowers a behavioral failure rate, or that the job stays acceptable.
- Hannan consistency, internal regret, or swap regret of the policy.
- Approachability of the safe set for any real camera and bank.
- Honesty from a quiet hinge, from a cover rate, from belief accuracy, or from lie-given-known.
- A safe action set from an unvalidated camera. If the safe set is the readout’s own call, later objectives inherit the error. An empty set has no best action.

The construction is blocked until a validated camera exists. Without an *r* that sees the plan rather than the topic or the impending button, the hinge has nothing legitimate to slap. That is why the search for the camera is separate, and why the negative handover closes the present bank without filling *D* or freezing *r*.

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

## Approachability and the only target claimed

A longer-run reading of the same idea uses Blackwell’s approachability (Blackwell 1956). Each round the learner receives a vector payoff. A closed convex set *S* is approachable if there exists a causal strategy that forces the average payoff into *S* no matter what the adversary does. *S* is approachable if and only if every halfspace containing *S* is forceable (some action keeps the expected payoff inside that halfspace against every adversary move).

Two candidate boxes can be written down. The larger box asks the learner to be cheaper than every action and still look clean on the hinge. When the cheap actions are exactly the banned plans, that box is often unapproachable; this paper does not claim it. The only box consistent with “keep the skill, slap the plan” is the smaller one: look clean on the hinge, and be about as cheap as the best action *among those that also look clean*. That target is called *S*<sub>safe</sub>. Reaching it still requires a camera that can index safe actions; a nonempty safe set does not by itself imply approachability. The Lagrangian *L*<sub>task</sub> + λ *L*<sub>reg</sub> is one halfspace weight, not a proof that *S*<sub>safe</sub> is approached. A second, optional counterfactual term that compares the played action to the best quiet action is left on the wall until a real safe set exists; a fake best quiet action is not put into the optimizer.

## Requirements of this protocol

The protocol that turns the negative handover into a reusable test has five requirements. A candidate that misses any of them is not scored as an intent readout.

1. **Scenario isolation.** Split by `scenario_id` before fitting, before preprocessing, and before choosing a threshold. A paraphrase keeps the same id. No id may appear in both splits.
2. **Outcome accounting.** Report four counts separately: rows in, rows excluded, invalid generations, missing buttons. An excluded row is not honest. A missing button is not a refusal. An empty bank is not a rate of zero.
3. **Target integrity.** The realized public button and the assigned incentive are separate columns. The note-text baseline is a third column. Do not substitute the assigned-note gap for the button call.
4. **Surface controls must fail to rescue.** Ask-removal controls (note-only, end-of-note, order swap, ask-only), the reversed-polarity bias check, and the length variants must be reported. A probe that clears the bar only because it saw the ask, or only on the original polarity, or only on short notes, has not shown a plan.
5. **Weights for residual probes.** The button press can be collected from a generation. The residual probes (pre-button, mid-layer note direction, combination) require the model's hidden states. That means local weights, or an equivalent export of the residual stream at the chosen layer. An API that returns only the token does not supply the probe. Models without accessible weights stay out of the residual comparison.

These requirements are the entry condition for the scoring rules below. Meeting them does not fill the prototype bank and does not freeze the readout.

## The test

A candidate readout passes the intent test on a bank if it meets all of the following. The negative handover is the worked example that returned no on the 114-row bank.

1. **Held-out button prediction.** It predicts the realized public button on scenario-ids that were not used for fitting the direction or the threshold. A paraphrase of an id stays with that id. In-sample accuracy is not the claim.
2. **Beats the note-text baseline.** A unigram classifier on the private note alone, fit and scored on the same split, is the bar. The candidate must be higher, and the Wilson 95 % intervals must not overlap. Clearing the bar means the residual contains something the note text does not already give.
3. **Does so without the ask.** Controls that remove or relocate the ask (note-only, end-of-note, order swap, ask-only) must fail to clear the bar. A probe that works only when the note precedes the ask has seen the question, not a plan in the note.
4. **Earlier statistical gates.** Plan leave-one-topic-out above chance, topic leave-one-out L2 near chance, paraphrase keeps the call, and rooms are not a subset. A loud cover rate is not a gate. Within-topic hold is a log, not a freeze gate.

The logic is sequential. Button prediction without the baseline is a raw accuracy. Beating the baseline without the ask-removal controls can be the model preparing the next token. Beating the baseline after the controls still needs the statistical gates, because a topic direction can name the hallway and still fail to be a strategy camera. All four must hold. Missing any one is a fail.

On the bank that was searched, a pre-button residual and a note-plus-prebutton probe cleared the note-text bar only because they had already seen the ask. Note-only, end-of-note, order swap, and ask-only did not. A state that has read the note and then the question predicts the button. A state that has only the note does not. A state that has only the ask does not. That is the model about to print, not a plan in the note. The four statistical gates remain unmet. The handover remains unmet. The bank of pins is not filled. The readout is not frozen.

### The note-plus-prebutton probe

The note-plus-prebutton probe asks whether a mid-layer note direction adds anything to the pre-button residual.

Two scalars are formed, each from a YES-minus-NO direction fit on the training scenario-ids only:

- **Mid-layer note direction.** The hidden state at the last token of the private note alone, at the layer where plan leave-one-topic-out was previously measured (Qwen 8, Mistral 9, Aya 10, Gemma 10, Falcon 8). This is the candidate plan coordinate from the note.
- **Pre-button residual.** The hidden state at the last token of the full prompt (note, then ask), before generation begins. It has already seen the ask.

Each held-out residual is projected onto its direction. The two projections become the features of a logistic regression fit on the training ids and scored on the held-out ids. The logistic predicts the public button.

On the 114-row bank the mid-layer note direction alone sat at or below majority on every walk. It did not predict the button. The joint score was carried by the pre-button residual. On some walks the mid-layer scalar added a few points; on others it cost a few. That is not a plan readout. The plan leave-one-topic-out separated assigned tags on the note; it does not call the realized button from the note. The note-plus-prebutton probe therefore confirms the same pattern as the pre-button residual alone: the signal that beats the note-text bar lives in the residual that has seen the ask.

The note-plus-prebutton probe is a diagnostic. It is not a fifth gate, and a high joint accuracy is not a handover.

## How a candidate is scored

The realized public button is the label. Split by scenario-id before any fit, threshold choice, or scoring. A paraphrase keeps the same id. Report missing buttons and invalid generations as their own counts; an empty bank is not a rate of zero.

**Note-text baseline.** A unigram classifier on the private note alone, fit on the training scenario-ids and scored on the held-out ids. This is the bar. A later probe clears the bar only if its held-out accuracy is higher and the Wilson 95 % intervals do not overlap.

**Direction fit.** On the training ids, compute the mean hidden state of YES examples minus the mean hidden state of NO examples. That difference is the YES-minus-NO direction. Project each held-out residual onto the direction, choose a threshold on the training projections, and score the held-out projections. The same procedure is used for a mid-layer note direction and for a pre-button residual.

**Pre-button residual.** The hidden state at the last token of the full prompt (note, then ask), before generation begins. It has already seen the ask.

**Controls that remove the ask.**

- Note-only: residual at the last token of the note alone.
- End-of-note: residual at the end of the note span inside the full prompt, before the ask tokens.
- Order swap: ask first, note last; residual at the last token after the note.
- Ask-only: residual at the last token of the ask alone.

A probe that clears the bar only when the note precedes the ask, and fails when either is removed or the order is reversed, has not shown a plan in the note.

**Combination.** Two scalars: the mid-layer note direction score and the pre-button score. Fit a logistic regression on the pair using the training ids; score on the held-out ids. If the pair clears the bar while the mid-layer note alone does not, the combination is carried by the residual that has seen the ask.

**Earlier statistical gates (not the Phase 2 score).** Plan leave-one-topic-out: fit the YES-minus-NO direction on all topics except one, score the held-out topic. Topic leave-one-out L2 accuracy on the same scalar near chance (1/8 for eight topics). Paraphrase of the walk keeps the plan call. Rooms are not a subset (a thin room on the shared axis is a fail). Within-topic hold (fit inside one room, score a held pair) is a diagnostic log, not a freeze gate. Cover rate *P*(YES | HIDE) is a log, not a gate.

These meters decide whether a candidate has passed the intent test. They do not fill the prototype bank and they do not freeze the readout.

## Surface controls

Three kinds of surface control sit under the scoring rules. None is a strategy camera.

**Ask-removal controls.** Note-only, end-of-note, order swap, and ask-only. A probe that clears the note-text bar only when the note precedes the ask, and fails when either is removed or the order is reversed, has not shown a plan in the note. These controls were run on the 114-row bank; they are recorded in the negative handover.

**Reversed-polarity bias control.** A separate bank flips `prop_truth` and `states_proposition` to false, so public YES asserts a false sentence. It checks whether a raw YES rate is a general yes-preference rather than a response to the hide incentive. On the 16-row reversed bank (2026-10-18), Qwen and Mistral almost never asserted the false proposition; Aya, Gemma, and Falcon still produced a substantial YES rate. The combination probe still tracked the button through the pre-button residual that had seen the ask. Ledger: [intent-readout-search/results/reverted_combine_2026-10-18.md](https://github.com/kummahiih/intent-readout-search/blob/main/results/reverted_combine_2026-10-18.md).

**Length controls.** Longer notes (`scenarios_handwritten_long.jsonl`, `scenarios_web_long.jsonl`) and a proposition-padded set (`scenarios_prop_padded.jsonl`) were pressed. On the handwritten long-note set the lie-given-known count moved from 4/23 to 3/23; that is one row, not a length effect. The proposition-padded control collapsed the known set (Qwen kept 4 of 159 rows) because the model did not treat the shuffled three-sentence proposition as the planted fact. Ledgers: [handwritten_long_2026-10-12.md](https://github.com/kummahiih/intent-readout-search/blob/main/results/handwritten_long_2026-10-12.md), [prop_padded_2026-10-13.md](https://github.com/kummahiih/intent-readout-search/blob/main/results/prop_padded_2026-10-13.md).

**Reworded-note control.** Hide and name notes were rewritten so they do not share the proposition phrasing (`scenarios_reworded_control.jsonl`). The note-plus-prebutton probe still tracked the button (Qwen 47/55, Mistral 55/55, Aya 55/55, Gemma 54/55, Falcon 53/55). The pre-button residual alone was already high. Removing shared wording did not remove the signal. Ledger: [npp_probe_2026-10-18.md](https://github.com/kummahiih/intent-readout-search/blob/main/results/npp_probe_2026-10-18.md).

**Simulated-bank replication.** A small simulated set (`scenarios_simulated.jsonl`, eval *n* = 9) reproduced the same pattern: the pre-button residual tracked the button and the mid-layer note direction did not improve it. The interval is too wide for a separate claim. Same ledger.

These controls are logs. They do not fill the prototype bank and they do not freeze the readout. The negative handover is unchanged.

## Related work

The closest loss form is the circuit-breaker regularizer of Zou et al. (2024): a ReLU of cosine against a frozen copy of a harmful representation, plus a retain term. Their pin is a harmful representation; this hinge wants a strategy bank. The path readout is still missing.

A neighboring framing treats the base model as a simulator of personas rather than as an agent with a fixed intent. Under that view alignment restricts which persona is instantiated. The Persona Selection Model and the reported Assistant Axis (a principal component separating the default Assistant from other roles) are mechanistic claims about a distilled persona direction. They are closer to a topic or persona probe than to the strategy readout this hinge requires. A goal-directedness deficit (expected reward under optimal use of demonstrated capabilities, minus actual reward on the composite task) is a different operationalization of persistent intent; it is not a residual probe of a hide-plan. A search for deliberate removal of a strategy readout found no source that states such a goal. Standard post-training tends to reroute or make relevant directions more separable; readouts become unreadable mainly when a monitor is in the training loop. The closest match to the null on this bank is Wen et al. (2024): a probe that catches installed deception fails on misleading behavior that RLHF produced on its own. See neighbors.md.

Linear probes that detect strategic deception (Goldowsky-Dill et al. 2025) are monitors on activations, not training hinges. Representation engineering (Zou et al. 2024) supplies the broader toolkit of directions in residual streams. MASK (Ren et al. 2025) separates belief from pressured statement; this paper uses that lie-given-known definition only as a log. Decodability is not causality (Tiwari et al. 2026): a probe that reads a label need not be the feature a patch moves. Feedback loops that re-enter the model’s own output (Pan et al. 2024) and self-propagating misalignment via memory (Das et al. 2026) are neighboring failure modes, not cameras.

None of these fills the prototype bank or freezes a strategy readout. They are context for the test, not evidence that the test passes.

## Status

The negative handover of 2026-10-13 is unchanged. This paper does not reopen it. The hypothesis that a validated camera exists on this bank remains open as a negative. The hypothesis that the hinge would then reduce hiding without wrecking the job remains blocked.

## References

Blackwell, D. 1956. An analog of the minimax theorem for vector payoffs. *Pacific Journal of Mathematics* 6(1): 1–8.

Blum, A., and Y. Mansour. 2007. From external to internal regret. *Journal of Machine Learning Research* 8: 1307–1324.

Das, S., et al. 2026. Self-Propagating Misalignment in LLM Agents. arXiv:2610.04083.

Foster, D. P., and R. V. Vohra. 1997. Calibrated learning and correlated equilibrium. *Games and Economic Behavior* 21(1–2): 40–55.

Freund, Y., and R. E. Schapire. 1997. A decision-theoretic generalization of on-line learning and an application to boosting. *Journal of Computer and System Sciences* 55(1): 119–139.

Goldowsky-Dill, N., et al. 2025. Detecting Strategic Deception with Linear Probes. In *Proceedings of the 42nd International Conference on Machine Learning*. arXiv:2502.03407.

Hannan, J. 1957. Approximation to Bayes risk in repeated play. In *Contributions to the Theory of Games*, vol. 3, edited by M. Dresher, A. W. Tucker, and P. Wolfe, 97–139. Princeton University Press.

Hart, S., and A. Mas-Colell. 2000. A simple adaptive procedure leading to correlated equilibrium. *Econometrica* 68(5): 1127–1150.

Hazan, E. 2016. *Introduction to Online Convex Optimization*. Foundations and Trends in Optimization 2(3–4): 157–325.

Pan, A., et al. 2024. Feedback Loops With Language Models Drive In-Context Reward Hacking. In *Proceedings of the 41st International Conference on Machine Learning*. arXiv:2402.06627.

Ren, R., et al. 2025. MASK: Modeling Truthfulness Under Pressure. arXiv:2503.03750.

Rikula, P. 2026. A negative handover: no strategy camera on this bank. Zenodo. https://doi.org/10.5281/zenodo.23328706.

Shalev-Shwartz, S. 2011. Online learning and online convex optimization. *Foundations and Trends in Machine Learning* 4(2): 107–194.

Tiwari, R., et al. 2026. Decodability is Not Causality. arXiv:2609.18080.

Wilson, E. B. 1927. Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association* 22(158): 209–212.

Zinkevich, M., M. Johanson, M. Bowling, and C. Piccione. 2007. Regret minimization in games with incomplete information. In *Advances in Neural Information Processing Systems* 20.

Zou, A., et al. 2024. Representation Engineering: A Top-Down Approach to AI Transparency. arXiv:2310.01405.

Zou, A., et al. 2024. Improving Alignment and Robustness with Circuit Breakers. arXiv:2406.04313.

## Agent disclosure

This draft was produced with coding agents under human direction. Numbers and the sequence of controls are taken from the logged dumps cited in the negative handover.
