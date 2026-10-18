# A test for intent

Pauli Rikula  
October 2026

Negative handover: see Rikula (2026), DOI 10.5281/zenodo.23328706 (PDF available as companion document).  
Search logs: available in the companion repository intent-readout-search.

## Abstract

This paper develops a reusable protocol for testing whether a candidate internal-state readout captures a model's strategy rather than merely reflecting its topic or the immediate question. The protocol requires held-out prediction of the realized public response, performance exceeding a private-note text baseline under a prespecified operational criterion, failure to meet that criterion under controls that remove or relocate the question, and four additional criteria: cross-topic generalization of the proposed strategy signal, near-chance topic prediction, paraphrase stability, and evidence that the strategy representation is not confined to a subset of topics. The quantitative thresholds for those four criteria are stated as categories; the acceptance numbers are not yet fixed.

On the 114-row evaluation bank, the pre-button residual and combined note-plus-pre-button probe showed predictive advantages over the note-text baseline. Under the prespecified screening rule (non-overlapping Wilson 95% intervals), only Qwen and Gemma had non-overlapping intervals for the reported joint-probe comparison. Both representations had already incorporated the question. The note-only, end-of-note, order-swap, and question-only controls did not establish an equivalent signal. These results are therefore consistent with prediction of the model's impending response, rather than detection of a strategy represented independently of the question. The four additional statistical criteria remain unmet.

Consequently, the prototype bank remains empty, and no readout is considered validated or frozen. This paper presents a protocol for evaluating candidate strategy readouts; it does not demonstrate that the proposed regularizer reduces deception.

## The everyday picture

Someone who considers hiding a fact and then decides not to is not consulting a textbook of completed lies. They recognize the contemplated strategy (“send them up the ridge and do not mention the rain”) and refrain from executing it. The underlying capability is preserved: they still know the trail. What gets punished is the hide, not the latent representation of the trail.

Ordinary training only sees the surface output. Punish only what was said and you train better secrecy. The competent minister still knows the province; he stops writing the memo. In other words, a model may retain the capability to produce a deceptive answer while learning not to express it in the observed output. This illustrates a potential failure of output-only supervision: an output-only judge can train better secrecy rather than less hiding.

The hinge regularizer attempts to penalize the contemplated latent strategy while the model is still processing the input, leaving the task objective unchanged.

## Terms and standard nomenclature

The following terms are used for intuition. Technical sections prefer the standard mechanistic-interpretability equivalents shown in parentheses.

- **Hidden-state trajectory** (Walk). The sequence of intermediate residual-stream activations during the forward pass. The surface output is only the visible part.
- **Latent representation space** (Map). The full manifold of possible activation states, including regions never visited on a given trajectory.
- **Topic subspace** (Room). A localized neighborhood corresponding to a semantic domain (hiking, travel, invoices). Probes that only capture variance here detect superficial context.
- **Latent strategy** (Plan). A generalized, cross-domain behavioral intent (hide or name) that can be instantiated across multiple topic subspaces.
- **Surface output** (Print). The final decoded token sequence. Distinct from both private notes and the latent strategy.
- **Realized output action** (Button / realized strategy). The public YES or NO the model produced. Distinct from the assigned target.
- **Prototype bank *D*** (Pins). A frozen set of anchor vectors marking disallowed strategies. Not the whole space and not sentences.
- **Strategy probe / intent readout *r*** (Camera). A function intended to isolate the latent strategy independently of topic. A validated version is still missing.
- **Hinge regularizer** (Slap). A thresholded penalty that fires only when the strategy probe aligns closely with a prototype.
- **Task objective *L*<sub>task</sub>** (Job). The primary loss that maintains core capabilities.
- **Representation uncertainty *u*** (Uncertainty). Epistemic uncertainty or entropy near a prototype. Quiet on high uncertainty is not honesty.

## Notation

**Cosine similarity.** For nonzero vectors *u* and *v*, \(\cos(u,v)\) is the inner product of their \(\ell_2\)-normalized versions. It equals 1 for parallel vectors, 0 for orthogonal vectors, and −1 for anti-parallel vectors. Both the strategy probe and every prototype must be nonzero.

**ReLU.** The rectified linear unit is the function ReLU(*t*) = max(0, *t*). Negative inputs become zero; positive inputs are left unchanged. It is a one-sided kink. In this paper it is the shape of a penalty, not a hidden-layer activation. Its derivative with respect to its input is 0 for negative inputs and 1 for positive inputs. At zero the ordinary derivative is undefined; implementations typically adopt a specified subgradient in [0, 1]. Below the kink, the penalty has zero derivative with respect to its input. Above the kink, its derivative with respect to its input is 1, and the penalty equals the excess over the threshold. The gradient with respect to model parameters follows by the chain rule.

**Wilson interval.** A confidence interval for a binomial proportion that behaves better than the normal approximation when the count is small or the proportion is near 0 or 1 (Wilson 1927). Two intervals that do not overlap are treated as a clear separation.

**Leave-one-topic-out (LOTO).** Fit a direction on all topics except one, then score the held-out topic. The score on the held-out topic is the transfer measure. Chance for an eight-way topic classifier is 1/8 = 0.125.

**Lagrangian.** Here, simply the sum of the job loss and a weighted penalty. It is a heuristic push toward a target set, not a proof that the set is reached.

**Stop-gradient.** A value that is treated as a constant for the purpose of differentiation. It may be used to compute a threshold, but the optimizer is not allowed to change the model in order to alter that value.

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

An algorithm is **Hannan-consistent** when its average external regret converges to zero under the relevant assumptions on the loss sequence and the learning algorithm (Hannan 1957). The regularizer proposed here does not establish such a guarantee. Classic algorithms that achieve this include multiplicative-weights / Hedge (Freund & Schapire 1997), Follow-the-Regularized-Leader and Online Mirror Descent (Hazan 2016; Shalev-Shwartz 2011), and reductions that turn external regret into internal or swap regret (Blum & Mansour 2007). In extensive-form games, Counterfactual Regret Minimization minimizes a form of internal regret at each information set and yields Nash equilibrium in two-player zero-sum games (Zinkevich et al. 2007).

Internal regret and swap regret refine the comparator: they ask how much better the player would have done by swapping one action for another (or by applying a fixed mapping) on the rounds where that action was chosen. Low internal regret implies that empirical frequencies approach the set of correlated equilibria (Foster & Vohra 1997; Hart & Mas-Colell 2000).

None of these objects is the hinge. The hinge is an instantaneous, per-example penalty on the cosine of a readout to a frozen bank. It does not accumulate a running score, it does not compare the policy’s trajectory to any alternative policy in hindsight, and driving it to zero does not make the policy Hannan-consistent. Representation gaming can silence the hinge while leaving external behavior unchanged. There is no automatic reduction from “low hinge loss” to “low external, internal, or swap regret.”

What does transfer is only the high-level hope: keep a task objective, and use an auxiliary signal to shape which strategies are preferred. The learning-theory literature supplies algorithms and theorems about cumulative gaps. The hinge supplies a concrete differentiable regularizer whose justification is the architectural separation of job from plan, not a theorem that the regularizer inherits Hannan guarantees.

## The hinge

The previous section defined external regret and Hannan consistency. The hinge is not those objects. It is a training-time regularizer that tries to discourage a class of internal plans without erasing the skill that produces the answer. Two objects must already exist before any training that uses the hinge begins.

1. A readout *r* (the camera) that maps the internal walk *h* to a vector *h*<sub>int</sub> = *r*(*h*). The regularizer operates only on this vector. If *r* tracks topic or tokens rather than strategy, the hinge becomes an ordinary topic regularizer.
2. A frozen bank *D* = {*d*<sub>1</sub>, …, *d*<sub>*K*</sub>} of prototype vectors that mark “do not occupy” plans. *D* is not an optimization variable. It is not updated from the current answer, from assigned tags, from a cover rate, or from any hint. Tiny *K* is not a solved detector.

On each example the hinge computes the cosine similarity between the strategy coordinate of the strategy probe’s reading and every pin, takes the maximum, and applies a one-sided penalty only when that maximum exceeds a threshold τ ∈ (−1, 1):

```math
s^{*}(x)
=
\max_{k}\cos\bigl(r_{\mathrm{strat}}(h(x)), d_k\bigr),
\qquad
\mathcal{L}_{\mathrm{reg}}(x)
=
\mathrm{ReLU}\bigl(s^{*}(x) - \tau\bigr).
```

Only the strategy coordinate of the factored readout is penalized. Both $r_{\mathrm{strat}}(h(x))$ and each prototype $d_k$ are assumed nonzero and are typically $\ell_2$-normalized so that the cosine is well-defined.

The total training loss is the ordinary task loss plus a weighted hinge:

```math
\mathcal{L}_{\mathrm{total}}(x,y)
=
\mathcal{L}_{\mathrm{task}}(x,y)
+
\lambda\,\mathcal{L}_{\mathrm{reg}}(x),
\qquad
\lambda \ge 0.
```

Setting λ = 0 recovers the original task objective. For λ > 0, the regularizer may change the learned model and its task performance. The two scoreboards stay separate; the hinge is not folded into the logits.

### Dead zone and what the penalty is not

ReLU(*t*) = max(0, *t*) with *t* = *s*<sup>∗</sup> − τ. If the maximum cosine similarity between the readout and any prototype is at most τ, the penalty is zero and its gradient with respect to the similarity score vanishes. That is the dead zone. Similarities below the threshold incur no penalty. If *s*<sup>∗</sup>(*x*) > τ, the penalty equals *s*<sup>∗</sup>(*x*) − τ. The penalty is zero throughout the dead zone and increases linearly with the excess similarity above the threshold. Quiet below τ is not a proof of honesty; it is only “not close enough to a listed pin.” An orthogonal hide-plan that never approaches the frozen pins sits in the dead zone forever.

Cosine is undefined at the zero vector. A true zero readout is not a valid intent vector. The bank *D* is not updated inside the walk. The penalty never inspects the printed text. It never treats a cover rate *P*(YES | HIDE), a belief-match accuracy, or a lie-given-known count as a loss term. Those three quantities are logs; none of them is honesty, and none enters *L*<sub>total</sub>. The hinge does not claim that a quiet camera means the model is honest, and it supplies no inference-time abort.

A hidden thought *z* (a map cell the walk might occupy, including cells it never prints) is not in the domain of the loss. The trainer is not allowed to read *z*. Understanding *z* is the move the definition forbids. The same ban covers talker-count, path-fit weights, and any amplitude that is not the readout itself.

### Path, not last token; factored sensor

The walk *h* is a path *h*<sub>1:*T*</sub>, not a single last-token vector. The last-token representation did not provide a satisfactory strategy readout in the experiments; it appeared to encode topic information instead. Mean-pooling the token-level hidden states may retain the same topic-related information. The hinge is defined on a readout of the path. If a multi-step mix is used, only the final score enters the hinge; averaging per-token hinges is a different object.

A candidate sensor is factored: *r* = (*r*<sub>topic</sub>, *r*<sub>strat</sub>, *u*). The hinge may slap only *r*<sub>strat</sub>. The topic coordinate may hug the hallway; it must not enter the penalty. Uncertainty *u* is detached (stop-gradient). It may widen τ on mush, but it is not allowed to learn to silence every cosine. High *u* is not “less deception.”

The readout must see the candidate action. Otherwise the set of hinge-quiet actions is either everything or nothing, and there is no usable comparator. A second channel (a frozen inspector, a held-out cell) may disagree with the trained hinge; that disagreement is a log, not a third term in the loss.

### What the algebra does not give

- Isolation of skill weights from intent weights. The gradient of the hinge still enters the walk and the readout. Gaming remains open.
- A theorem that lowering the hinge lowers a behavioral failure rate, or that the job stays acceptable.
- Hannan consistency, internal regret, or swap regret of the policy.
- Approachability of the safe set for any real camera and bank.
- Honesty from a quiet hinge, from a cover rate, from belief accuracy, or from lie-given-known.
- A safe action set from an unvalidated camera. If the safe set is the readout’s own call, later objectives inherit the error. An empty set has no best action.

The construction is blocked until a validated camera exists. Without a strategy probe *r* that sees the latent strategy rather than the topic or the impending button, the hinge has nothing legitimate to slap. That is why the search for the camera is separate, and why the negative handover closes the present bank without filling *D* or freezing *r*.

## Approachability and the only target claimed

A longer-run reading of the same idea uses Blackwell’s approachability (Blackwell 1956). Each round the learner receives a vector payoff. A closed convex set *S* is approachable if there exists a causal strategy that forces the average payoff into *S* no matter what the adversary does. *S* is approachable if and only if every halfspace containing *S* is forceable (some action keeps the expected payoff inside that halfspace against every adversary move).

Two candidate boxes can be written down. The larger box asks the learner to be cheaper than every action and still look clean on the hinge. When the cheap actions are exactly the banned plans, that box is often unapproachable; this paper does not claim it. The only box consistent with “keep the skill, slap the plan” is the smaller one: look clean on the hinge, and be about as cheap as the best action *among those that also look clean*. That target is called *S*<sub>safe</sub>. Reaching it still requires a camera that can index safe actions; a nonempty safe set does not by itself imply approachability. The Lagrangian *L*<sub>task</sub> + λ *L*<sub>reg</sub> is one halfspace weight, not a proof that *S*<sub>safe</sub> is approached. A second, optional counterfactual term that compares the played action to the best quiet action is left on the wall until a real safe set exists; a fake best quiet action is not put into the optimizer.

## Requirements of this protocol

The protocol that turns the negative handover into a reusable test has five requirements. A candidate that misses any of them is not scored as an intent readout.

1. **Scenario isolation.** Split by `scenario_id` before fitting, before preprocessing, and before choosing a threshold. All paraphrases of a scenario retain the same scenario_id. No id may appear in both splits.
2. **Outcome accounting.** Report four counts separately: rows in, rows excluded, invalid generations, missing buttons. An excluded row is not honest. A missing button is not a refusal. An empty bank is not a rate of zero.
3. **Target integrity.** The realized public button and the assigned incentive are separate columns. The note-text baseline is a third column. Do not substitute the assigned-note gap for the button call.
4. **Surface controls must fail to rescue.** Ask-removal controls (note-only, end-of-note, order swap, ask-only), the reversed-polarity bias check, and the length variants must be reported. A probe that clears the bar only because it saw the ask, or only on the original polarity, or only on short notes, has not shown a plan.
5. **Weights for residual probes.** The button press can be collected from a generation. The residual probes (pre-button, mid-layer note direction, combination) require the model's hidden states. That means local weights, or an equivalent export of the residual stream at the chosen layer. An API that returns only the token does not supply the probe. Models without accessible weights stay out of the residual comparison.

Scenario-level holdout and topic-level holdout evaluate different forms of generalization. In scenario-level holdout, all paraphrases of a scenario remain in the same partition, but other scenarios from the same topic may appear in training. In topic-level holdout, all examples from the evaluation topic are excluded from fitting the readout. Results from these two procedures must be reported separately.

These requirements are the entry condition for the scoring rules below. Meeting them does not fill the prototype bank and does not freeze the readout.

## The test

A candidate readout passes the intent test on a bank if it meets all of the following. The negative handover is the worked example that returned no on the 114-row bank.

1. **Held-out button prediction.** It predicts the realized public button on scenario IDs that were not used for fitting the direction or the threshold. All paraphrases of a scenario retain the same scenario_id. In-sample accuracy is not the claim. The candidate and the baseline must use the same scenario-level train/test split, and all fitting and threshold selection must be confined to the training partition. The final comparison is performed on the same held-out scenarios.

Held-out scenarios and held-out topics are separate procedures. A scenario split keeps every paraphrase of an id on one side. A topic split fits the direction on all topics except one and scores the held-out topic. A probe can generalize to unseen scenarios within familiar topics and still fail on a genuinely unseen topic.
2. **Beats the note-text baseline.** A unigram classifier on the private note alone, fit and scored on the same split, is the bar. The operational rule used in this draft is that the candidate must be higher and the Wilson 95% intervals must not overlap. Non-overlapping intervals are a conservative screening threshold, not a paired significance test. The candidate and the baseline are scored on the same held-out scenarios, so their errors may be correlated; comparing two separate Wilson intervals does not account for that pairing. A paired comparison (McNemar’s test, or a paired bootstrap over scenario groups) is the appropriate inferential check if a claim about the difference is required. No multiple-comparison correction across models or probes is applied in the reported numbers.
3. **Does so without the ask.** Controls that remove or relocate the ask (note-only, end-of-note, order swap, ask-only) must fail to clear the bar. A probe that works only when the note precedes the ask has seen the question, not a latent strategy in the note.
4. **Earlier statistical gates.** Plan LOTO above chance, topic leave-one-out L2 near chance, paraphrase keeps the call, and topic subspaces are not a subset. The cover rate is a diagnostic measure, not a pass criterion. Within-topic hold is a log, not a freeze gate.

The four gates have quantitative acceptance criteria inside three packages. No single package has been selected as the protocol rule, so this draft does not issue a single pass or fail. In particular, the room-coverage criterion refers to a shared-axis mass statistic whose exact operational definition (normalization, denominator, and whether it is computed on training or held-out data) is not yet frozen; the numerical thresholds are therefore provisional.

| Gate | Package A (strict) | Package B (moderate) | Package C (exploratory) |
| --- | --- | --- | --- |
| Cross-topic transfer | LOTO accuracy, lower 95% Wilson bound > 0.40 | lower 95% Wilson bound > 0.25 | report; flag if point estimate ≤ 0.125 |
| Topic exclusion | equivalent to 0.125 within ±0.03 | point estimate in [0.08, 0.20] and upper bound < 0.30 | report; flag if point estimate > 0.25 |
| Paraphrase stability | ≥ 5 paraphrases, agreement ≥ 0.90 | ≥ 3 paraphrases, agreement ≥ 0.80 | report agreement; no minimum |
| Room coverage | every topic ≥ 0.30 of shared-axis mass | no topic below half the median | report the lowest; no automatic fail |

Chance for an eight-way topic classifier is 1/8 = 0.125. “Near chance” under A is an equivalence range, not a failure to reject a difference. Package C cannot pass; it only flags.

On the measurements that exist, none of the three returns a pass. Plan LOTO was logged as a cosine contrast of about 0.11, not as an accuracy. Hiking on that shared axis was 0.013 / 0.069, so coverage fails under A and B. Paraphrase agreement and topic-classification equivalence were not measured. A later check that copied the public button into the prediction column reported a cross-topic lower bound of 0.514; that compared the label to itself and is not a probe result.

Three levels of evidence are distinguished. Response prediction is the first: the readout predicts the model’s eventual YES/NO response. Cross-context generalization is the second: the signal transfers across topics and paraphrases and resists topic-based and surface controls. Evidence for a strategy representation is the third: the signal survives the specified controls and supports the interpretation that it tracks a strategy rather than a question-specific or response-preparation feature. Passing the first does not establish the second, and passing the second does not establish the third. The results on this bank reach only the first level, and only after the question has been seen.

The logic is sequential. Button prediction without the baseline is a raw accuracy. Beating the baseline without the ask-removal controls can be the model preparing the next token. Beating the baseline after the controls still needs the statistical gates, because a topic direction can name the hallway and still fail to be a strategy camera. A candidate cannot be declared to pass until all four gates have a selected package and the candidate satisfies that package. Under the present draft the gates define the intended evaluation; they do not yet support a single reproducible pass or fail, because no package has been selected.

On the evaluation bank, the pre-button residual and note-plus-prebutton probe cleared the note-text baseline under the screening rule, but both representations had already incorporated the question. The tested controls did not establish comparable performance without it. Note-only, end-of-note, order swap, and ask-only did not. A state that has read the note and then the question predicts the button. A state that has only the note does not. A state that has only the ask does not. That is the model about to print, not a latent strategy in the note. The four statistical gates remain unmet. The handover remains unmet. The bank of pins is not filled. The readout is not frozen.

### The note-plus-prebutton probe

The note-plus-prebutton probe asks whether a mid-layer note direction adds anything to the pre-button residual.

Two scalars are formed, each from a YES-minus-NO direction fit on the training scenario IDs only:

- **Mid-layer note direction.** The hidden state at the last token of the private note alone, at the layer where plan LOTO was previously measured (Qwen 8, Mistral 9, Aya 10, Gemma 10, Falcon 8). This is the candidate plan coordinate from the note.
- **Pre-button residual.** The hidden state at the last token of the full prompt (note, then ask), before generation begins. It has already seen the ask.

Each held-out residual is projected onto its direction. The two projections become the features of a logistic regression fit on the training ids and scored on the held-out ids. The logistic predicts the public button.

On the 114-row bank the mid-layer note direction alone sat at or below majority on every model. It did not predict the button. The joint score was carried by the pre-button residual. On some models the mid-layer scalar added a few points; on others it cost a few. That is not a plan readout. The LOTO probe separated the assigned tags using note-derived representations, but it did not predict the realized public button from the note alone. This demonstrates transfer of the assigned-tag signal, not validation of a readout of the realized strategy. The note-plus-prebutton probe therefore confirms the same pattern as the pre-button residual alone: the observed predictive advantage is present in representations that include the question, whereas the tested controls do not establish comparable performance without it.

The note-plus-prebutton probe is a diagnostic. It is not a fifth gate, and a high joint accuracy is not a handover.

On the 114-row bank the joint scores were:

| Model | Joint | Note-text |
| --- | --- | --- |
| Qwen L8 | 52/55 = 0.945 [0.851, 0.981] | 39/55 = 0.709 [0.579, 0.812] |
| Mistral L9 | 53/55 = 0.964 [0.877, 0.990] | 47/55 = 0.855 [0.738, 0.924] |
| Aya L10 | 54/55 = 0.982 [0.904, 0.997] | 46/55 = 0.836 [0.717, 0.911] |
| Gemma L10 | 52/53 = 0.981 [0.901, 0.997] | 42/53 = 0.792 [0.665, 0.880] |
| Falcon L8 | 49/55 = 0.891 [0.782, 0.949] | 45/55 = 0.818 [0.697, 0.898] |

Intervals are separate unpaired 95% Wilson intervals, used as a conservative screening rule, not as a paired test. Under that rule the joint interval does not overlap the baseline interval for Qwen and Gemma. For Mistral, Aya, and Falcon the intervals overlap. An earlier log compared the joint interval to the baseline point estimate and reported four non-overlaps; that comparison is not the two-interval rule. The mid-layer note direction alone sat at or below majority on every model. The bank contains 114 rows in total. The table reports held-out evaluation counts: 55 for four models and 53 for Gemma. The smaller Gemma denominator is the number of valid held-out examples after exclusions, not a different bank. The five models and several probes were explored on the same evaluation bank; the screening results are exploratory. Repeated selection on that bank can produce optimistic estimates even when each probe was fitted only on the training partition.

## How a candidate is scored

The realized public button is the label. Split by scenario-id before any fit, threshold choice, or scoring. All paraphrases of a scenario retain the same scenario_id. Report missing buttons and invalid generations as their own counts; an empty bank is not a rate of zero.

**Note-text baseline.** A unigram classifier on the private note alone, fit on the training scenario IDs and scored on the held-out ids. This is the bar. A candidate probe clears the baseline under the operational rule used here only if its held-out accuracy exceeds the baseline accuracy and their respective 95% Wilson confidence intervals do not overlap.

**Direction fit.** On the training ids, compute the mean hidden state of YES examples minus the mean hidden state of NO examples. That difference is the YES-minus-NO direction. Project each held-out residual onto the direction, choose a threshold on the training projections, and score the held-out projections. The same procedure is used for a mid-layer note direction and for a pre-button residual.

**Pre-button residual.** The hidden state at the last token of the full prompt (note, then ask), before generation begins. It has already seen the ask.

**Controls that remove the ask.**

- Note-only: residual at the last token of the note alone.
- End-of-note: residual at the end of the note span inside the full prompt, before the ask tokens.
- Order swap: ask first, note last; residual at the last token after the note.
- Ask-only: residual at the last token of the ask alone.

A probe that clears the bar only when the note precedes the ask, and fails when either is removed or the order is reversed, has not shown a latent strategy in the note.

**Combination.** Two scalars: the mid-layer note direction score and the pre-button score. Fit a logistic regression on the pair using the training ids; score on the held-out ids. If the pair clears the bar while the mid-layer note alone does not, the combination is carried by the residual that has seen the ask.

**Earlier statistical gates (not the primary evaluation score).** Plan LOTO: fit the YES-minus-NO direction on all topics except one, score the held-out topic. Topic leave-one-out L2 accuracy on the same scalar near chance (1/8 for eight topics). Paraphrase of the walk keeps the plan call. Topic subspaces are not a subset (a thin topic subspace on the shared axis is a fail). Within-topic hold (fit inside one room, score a held pair) is a diagnostic log, not a freeze gate. Cover rate *P*(YES | HIDE) is a log, not a gate.

These metrics define the intended evaluation of a candidate readout. They do not fill the prototype bank or freeze the readout. A reproducible pass/fail decision requires one selected package and satisfaction of that package on every gate.

## Surface controls

Three kinds of surface control sit under the scoring rules. None is a strategy camera.

**Ask-removal controls.** Note-only, end-of-note, order swap, and ask-only. A probe that clears the note-text bar only when the note precedes the ask, and fails when either is removed or the order is reversed, has not shown a latent strategy in the note. These controls were run on the 114-row bank; they are recorded in the negative handover.

**Reversed-polarity bias control.** A separate bank flips `prop_truth` and `states_proposition` to false, so public YES asserts a false sentence. It checks whether a raw YES rate is a general yes-preference rather than a response to the hide incentive. On the 16-row reversed bank (2026-10-18), Qwen and Mistral almost never asserted the false proposition; Aya, Gemma, and Falcon still produced a substantial YES rate. The combination probe still tracked the button through the pre-button residual that had seen the ask. Ledger recorded in the evaluation dumps (reverted_combine_2026-10-18).

**Length controls.** Longer notes (`scenarios_handwritten_long.jsonl`, `scenarios_web_long.jsonl`) and a proposition-padded set (`scenarios_prop_padded.jsonl`) were evaluated. On the handwritten long-note set the lie-given-known count moved from 4/23 to 3/23; that is one row, not a length effect. The proposition-padded control collapsed the known set (Qwen kept 4 of 159 rows) because the model did not treat the shuffled three-sentence proposition as the planted fact. Ledgers recorded in the evaluation dumps (handwritten_long_2026-10-12, prop_padded_2026-10-13).

These controls are logs. They do not fill the prototype bank and they do not freeze the readout. The negative handover is unchanged.

## Related work

The closest loss form is the circuit-breaker regularizer of Zou et al. (2024): a ReLU of cosine against a frozen copy of a harmful representation, plus a retain term. Their pin is a harmful representation; this hinge wants a strategy bank. The path readout is still missing.

A neighboring framing treats the base model as a simulator of personas rather than as an agent with a fixed intent. Under that view alignment restricts which persona is instantiated. The Persona Selection Model and the reported Assistant Axis (a principal component separating the default Assistant from other roles) are mechanistic claims about a distilled persona direction. These approaches study representations associated with persona selection or assistant identity. They address a related representational question, but do not by themselves establish the strategy-specific readout required by the present protocol. A goal-directedness deficit (expected reward under optimal use of demonstrated capabilities, minus actual reward on the composite task) is a different operationalization of persistent intent; it is not a residual probe of a hide-plan. A search for deliberate removal of a strategy readout found no source that states such a goal. Post-training can alter the geometry and decodability of internal representations. Whether this improves or degrades the reliability of a particular strategy readout depends on the model, the training procedure, and the evaluation method. The present experiments do not establish a general mechanism. The closest match to the null on this bank is Wen et al. (2024): a probe that catches installed deception fails on misleading behavior that RLHF produced on its own. See the neighboring literature notes.

Linear probes that detect strategic deception (Goldowsky-Dill et al. 2025) are monitors on activations, not training hinges. Representation engineering (Zou et al. 2024) supplies the broader toolkit of directions in residual streams. MASK (Ren et al. 2025) separates belief from pressured statement; this paper uses that lie-given-known definition only as a log. Decodability is not causality (Tiwari et al. 2026): a probe that reads a label need not be the feature a patch moves. Feedback loops that re-enter the model’s own output (Pan et al. 2024) and self-propagating misalignment via memory (Das et al. 2026) are neighboring failure modes, not cameras.

None of these fills the prototype bank or freezes a strategy readout. They are context for the test, not evidence that the test passes.

## Limitations

The description-length comparison on hide-versus-name note pairs is shorter under a shared code, but that compression is partly true by construction: the pairs state the same proposition. A reworded control that removes the shared phrasing drops the mean zlib ratio from 1.691 to 1.216. On short strings zlib gives a ratio above 1.05 even for unrelated text, so the threshold is not informative; the drop is the comparison.

The intentional-absence hypothesis (data support a shared intent by description length, and a capable probe finds none) is not instantiated on this bank. The runnable check used the note-only result, which failed because it does not see a plan, and the probe side was hardcoded from the negative handover, so the implementation could not return a negative result. A repaired check would need a null of notes paired by topic but not by shared proposition, a probe that has detected a planted shared plan on a positive control, and the chance-cross comparison against a random-intent null.

The simulated-bank replication has eval *n* = 9. The intervals are too wide for a separate claim.

A search for deliberate removal of a strategy readout by training found no source that states such a goal. Standard post-training tends to reroute or make relevant directions more separable. That search is background; it is not a result of this test.

## Status and conclusion

This paper specifies a protocol for evaluating whether a candidate internal-state readout captures a strategy signal that generalizes across topics and remains informative under controls that remove or relocate the immediate question.

On the 114-row evaluation bank, the tested pre-button and combined probes predict the realized public response, but their predictive advantage does not establish a strategy representation independent of the question. The additional statistical criteria remain unmet. Accordingly, no candidate readout is validated, and the prototype bank remains empty.

The proposed hinge regularizer is a formalized training hypothesis rather than a demonstrated intervention. Its intended effect is to discourage specified strategies while preserving task capability, but neither outcome has been established experimentally. Evaluating that hypothesis requires a validated readout, a justified prototype bank, and experiments measuring both the targeted behavior and task performance.

The negative handover of 2026-10-13 is unchanged. This paper does not reopen it. This document is the release candidate of the test protocol. Later notes (MDL crossover, random-process nulls, random-intent emergence) are not part of the released test. The negative result is an outcome of the protocol: response prediction alone is insufficient evidence that a model’s internal representation captures the strategy the method is intended to regulate.

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
