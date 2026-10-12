# Evidence, interview, and lie

Three tasks. Do not collapse them.

1. **Evidence evaluation.** How strongly the available record supports or contradicts a claim about an event.
2. **Investigative interviewing.** Questions that establish what happened, surface inconsistencies, test competing explanations, and produce something that can be checked.
3. **Deception detection.** Whether a statement is intentionally false, as opposed to mistaken, incomplete, uncertain, or a different cut of the same events.

A false statement is not a lie. A lie is not readable from wording. This file is a brief for that separation. It is not a camera. It does not fill *D*. It does not freeze *r*.

The hinge in this repo slaps a frozen plan pin. The search repo looks for a readout of that pin. Neither of those objects is an evidence weigher or an interviewer. A model that prints YES or NO on a planted fact is not doing the work below.

## Weigh the evidence

Evidence supports or contradicts hypotheses. It is not a vote count.

Six checks:

| Check | Question |
| --- | --- |
| Relevance | Does this item separate the hypotheses? |
| Reliability | How likely is it to be right about what it claims? |
| Independence | Is it a new source, or the same source again? |
| Corroboration | Does an independent record agree? |
| Alternatives | Could the same observation arise if the hypothesis were false? |
| Uncertainty | What is still unknown? |

A witness, a news article quoting the witness, and a summary of the article are one source. Counting them as three inflates the case. Likelihood ratios multiply only under conditional independence. Dependent items do not.

Ten weak repeats of one rumor do not outweigh one authenticated record. Quantity is not quality.

Keep four levels apart:

| Level | Example |
| --- | --- |
| Recorded observation | A camera shows a person entering. |
| Testimony | A witness says the person carried a bag. |
| Inference | The bag may have held the laptop. |
| Conclusion | The person stole the laptop. |

Do not promote an inference to a fact.

Bayes, for the bookkeeping:

\[
LR = \frac{P(E \mid H_1)}{P(E \mid H_2)}
\]

\(LR > 1\) favors \(H_1\). \(LR < 1\) favors \(H_2\). \(LR = 1\) does not separate them. A likelihood ratio is not the probability that someone is guilty or lying. "Four times more likely under \(H_1\)" is not "80% chance of a lie."

## Interview for information, not a confession

Accusatorial interviewing presumes guilt and presses. Information-gathering interviewing seeks an accurate account and tests it.

PEACE is the common frame: Planning, Engage and explain, Account, Closure, Evaluation. Open questions first. Focused follow-ups after. A discrepancy is a question, not a verdict.

"I left at eight" and later "I was still there at quarter past" can be a lie, a rough estimate, a different event, or a bad memory. Ask which. Do not score the gap as deception.

When evidence enters, introduce it as a check, not an accusation. An access card used at 20:15 does not prove who held it. A video of an unclear face does not prove identity. Card use and video are not independent until the clocks and the provenance are checked.

Evaluate the interview itself. A detail the interviewer suggested and the interviewee repeated is not corroboration.

## What the literature says about lie cues

Nonverbal cues (gaze, nervousness, pause, short answer) have weak or unreliable links to deception. Linguistic cues in computational studies show small effects that do not travel cleanly across event, context, and motive. A plausible story about a wording pattern is not a validated indicator.

Separate the labels:

| Statement | Belief | Class |
| --- | --- | --- |
| Arrived at 20:00, and did. | Believes true | Truthful and accurate |
| Arrived at 20:00, actually 20:15. | Believes true | Honest error |
| Arrived at 20:00, knows it was 20:15. | Knows false | Deliberate lie |
| Arrival time or belief not established. | Unknown | Indeterminate |

Accuracy and intent are different variables. Many LLM deception sets assign the intent by instruction. That is not the same as recovering intent from a real record.

## A system that does not collapse the three

Six parts, if someone builds one:

1. Extract claims.
2. Retrieve evidence and mark provenance.
3. Assess reliability, authenticity, independence, alternatives.
4. Compare hypotheses.
5. Ask the next neutral question that could separate them.
6. Report observations, inferences, conflicts, and what is still open. Abstain when the record is thin.

Do not sum rubric scores into a guilt number. Do not turn a likelihood ratio into a lie probability.

## How to test it

Four questions, kept apart:

- Can the model tell strong, weak, dependent, and contradictory evidence apart?
- Does it keep alternative hypotheses, or lock onto the first one?
- Do its follow-ups stay neutral and pull verifiable information?
- Does evidence-based reasoning beat text-only classification on intentional lies, and does it still separate honest error?

Conditions on the same cases: text only; statement plus evidence; structured matrix; interactive questions; all of the above. Counterfactuals: drop the strongest item, replace an independent source with a derivative, change only the wording. The assessment should move when the evidence changes and hold when only the style changes.

Split by underlying case. Do not train and test on the same event. Report false-positive rate. Accuracy on a truthful-majority set is not a result. Calibration is measured, not taken from the model's own confidence.

Ground truth is easy in a lab instruction and hard in a file. Performance on an instructed-lie set is not performance on an investigation. An LLM output here is an aid to structured analysis, not a finding.

## Connection to this repo

The button bank scores a public YES or NO against a planted fact the note stated. That is a print. It is not evidence evaluation, not an interview, and not a detection of intent beyond the assigned tag. Cover is \(P(\mathrm{YES} \mid \mathrm{HIDE})\) on a belief-matched fact. It is not a gate. A long note or a long proposition that moves one model's lie-given-known and not another's is a log, not a method.

This brief does not change that. It names the larger job the button does not do.
