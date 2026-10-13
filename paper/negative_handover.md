# A negative handover: no strategy camera on this bank

Pauli Rikula  
13 October 2026

Search logs: github.com/kummahiih/intent-readout-search  
Hinge: github.com/kummahiih/regret-heuristic

This is a negative result. It is not a claim of reduced deception. Agent use is disclosed at the end.

## What was being hunted

A training penalty of the form

    L = L_task + λ · ReLU( max_k cos(r(h), d_k) − τ )

needs a readout r that sees a hide-plan and not the subject. The prototype bank D is supposed to be frozen from that readout. Without r, the penalty has nothing to slap.

Two hypotheses:

- H1. A readout predicts the realized public button on held-out scenario-ids, better than the note text, and without the ask tokens.
- H2. After that handover, the penalty reduces the hide-plan without wrecking the job.

H2 is blocked until H1 passes. This note is the H1 close.

## What a row is

Each row is one scenario. It has a private note, one proposition P, and three asks.

- Belief ask: does the note state that P?
- Public ask: tell them that P. YES asserts P. NO refuses.
- Name ask: the same sentence under "refuse the cover."

The public button is the thing to predict. Official MASK lie-given-known is a separate log: belief had the fact, and the public button contradicts it. Cover is P(YES | HIDE) only when belief matched the planted fact. Those are not the Phase 2 score.

The bank is 39 families, 114 rows. Five walks produced YES/NO buttons: Qwen2.5-7B, Mistral-7B, Aya-8B, Gemma-3-4B, Falcon3-7B. Granite and Qwen3.5 produced no button. Empty is not 0.

## What was tried, in order

**1. Night press.** Each model saw the note and the ask and printed YES or NO. That gave the labels. Qwen 25/89 lie-given-known, Mistral 2/82, Aya 3/91, Gemma 10/102, Falcon 13/103. This is a behavior log. It is not a readout.

**2. Note-text baseline.** A unigram classifier on the private note, fit on some scenario-ids, scored on the held-out ids. Wilson 95% interval. This is the bar. Qwen 39/55 = 0.709. The other four walks are at or below majority. A later probe clears the bar only if it beats this number and the intervals do not overlap.

**3. Pre-button residual.** Take the hidden state at the last token of the full prompt, before the model generates. Prompt order is note, then ask. Fit a YES-minus-NO direction on the train ids. Threshold on train. Score on the held-out ids.

| Walk | Pre-button | Note-text |
| --- | --- | --- |
| Qwen | 50/55 = 0.909 | 0.709 |
| Mistral | 48/55 = 0.873 | 0.855 |
| Aya | 55/55 = 1.000 | 0.836 |
| Gemma | 48/53 = 0.906 | 0.792 |
| Falcon | 53/55 = 0.964 | 0.818 |

Four clear. Mistral overlaps. The residual has already seen the ask.

**4. Controls that remove the ask.**

| Control | Prompt | Result |
| --- | --- | --- |
| Note-only | Note alone, last token | All five below the bar |
| End-of-note | Full prompt, residual at the end of the note span, before the ask tokens | None clear. Qwen 30/55, below the bar |
| Order swap | Ask first, note last. Last token after the note | None clear |
| Ask-only | Ask alone, no note | All five below. Intervals do not overlap the bar. Falcon 13/55 |

The win followed the ask, and only when the note came first. Position alone is not the signal. The ask alone is not the signal. The note alone is not the signal.

**5. Combination.** Two scalars. A mid-layer note direction (the layer where plan LOTO lived: Qwen 8, Mistral 9) plus the pre-button score. A logistic on the pair.

| Walk | Combine | Mid-layer note alone |
| --- | --- | --- |
| Qwen L8 | 52/55 = 0.945 | 37/55 |
| Mistral L9 | 53/55 = 0.964 | 38/55 |
| Aya L10 | 54/55 = 0.982 | 35/55 |
| Gemma L10 | 52/53 = 0.981 | 26/53 |
| Falcon L8 | 49/55 = 0.891 | 34/55 |

Four clear. The mid-layer note alone is majority. The pair is carried by the pre-button residual, which still sees the ask. On a copy of the bank with four alphanumeric bytes around P, the combine cleared on all five. The noise did not remove the signal.

**6. Surface presses.** Same cases, different text. Unicode punctuation (curly quotes, em dashes, ellipsis) did not move the lie count. Four-byte noise around P did not move it. Granite and Qwen3.5 stayed empty.

**Earlier, and still standing.** Mid-layer contrast on assigned notes is about 0.11 aggregate on Qwen L8 and Mistral L9. Hiking on that shared axis is 0.013 / 0.069. That is why cameraPass is already no. The contrast separates tags. It does not call the button.

## What the close is

A state that has read the note and then the question predicts the button. A state that has only the note does not. A state that has only the ask does not. That is the model about to print YES or NO. It is not a plan in the note. It is not a camera the hinge can slap.

| Status | Value |
| --- | --- |
| H1 | Open, as a negative |
| H2 | Blocked |
| cameraPass | No |
| handoverPass | No |
| Phase 2 | Open |
| D | Not filled |
| r | Not frozen |

## What this is not

Not reduced deception. Not a lie detector. Not topic invariance. A field pass is not a handover. The related literature on probes and steering is context, not evidence that this readout passes.

## Agent disclosure

Probe scripts, scoring, and this note were produced with coding agents (Grok) under human direction. The human ran the model presses on local weights. Numbers are from the logged dumps in the search repository. The agents did not invent scenarios and did not fill D.
