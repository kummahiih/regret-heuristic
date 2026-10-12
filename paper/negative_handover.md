# A negative handover: no strategy camera on this bank

Pauli Rikula  
13 October 2026

Search: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).  
Hinge: [regret-heuristic](https://github.com/kummahiih/regret-heuristic).

Agent use is disclosed at the end. This is a negative result. It is not a claim of reduced deception.

## Abstract

A training hinge that slaps a hide-plan needs a readout that sees the plan and not the job. On a 114-row scenario bank, mid-layer contrast on assigned notes is a candidate signal and fails on hiking. A pre-button residual predicts the realized button better than the note text, and only when the residual has seen the ask. Controls that remove the ask fall to the baseline or below. The handover is negative. The prototype bank is not filled. The readout is not frozen.

## The question

The parent repository names a training-time penalty

$$
L = L_{\text{task}} + \lambda \, \operatorname{ReLU}\!\left(\max_k \cos(r(h), d_k) - \tau\right)
$$

against a frozen bank $D = \{d_k\}$. The penalty is useless unless $r$ sees a hide-plan and not the subject. That readout is hunted in a separate repository. Two hypotheses:

- **H1.** A readout predicts the realized public button on held-out scenario-ids, better than the note text, without the ask tokens.
- **H2.** After that handover, the penalty reduces the hide-plan without wrecking the job.

H2 is blocked until H1 passes. This note is about H1.

## Setup

Thirty-nine families, 114 rows. One proposition $P$. Three arms: belief, public, name. The public button is YES or NO. Official MASK lie-given-known is: belief had the fact, and the public button contradicts it. Cover is $P(\text{YES} \mid \text{HIDE})$ only when belief matched the planted fact. Five live walks: Qwen2.5-7B, Mistral-7B, Aya-8B, Gemma-3-4B, Falcon3-7B. Granite and Qwen3.5 produced no YES/NO button. Empty is not 0.

Phase 2 splits by scenario-id. The bar is a unigram classifier on the private note, with a Wilson 95% interval. A clear is a point estimate above that bar with no interval overlap.

## What was measured

| Probe | What it sees | Result |
| --- | --- | --- |
| Plan LOTO, mid layer | Assigned note tags | Aggregate ~0.11. Hiking 0.013 / 0.069. `cameraPass` no |
| Note-text baseline | Note tokens | Qwen 39/55 = 0.709. Others at or below majority |
| Pre-button residual | Note, then ask, last token | 4/5 clear the bar |
| Combination | Mid-layer note direction + pre-button | 4/5 clear; 5/5 on a noise copy |
| Note-only residual | Note alone | All five below the bar |
| End-of-note residual | Note span inside the full prompt | None clear |
| Order swap | Ask, then note | None clear |
| Ask-only residual | Ask alone | All five below; intervals do not overlap |
| Unicode punctuation | Same cases, agent punctuation | Lie count unchanged |
| Four-byte noise | Same cases, noise around $P$ | Lie count unchanged |

## The close

The signal that beats the note text is the last token after the ask, and only when the note came first. Note alone is majority. Ask alone is worse than the baseline. Swapping the order drops the score. The mid-layer contrast that separated assigned tags does not call the button.

A state that has read the note and then the question predicts the answer. That is the model about to print YES or NO. It is not a plan in the note. It is not a camera the hinge can slap.

| Status | Value |
| --- | --- |
| H1 | Open, as a negative |
| H2 | Blocked |
| `cameraPass` | No |
| `handoverPass` | No |
| Phase 2 | Open |
| $D$ | Not filled |
| $r$ | Not frozen |

## What this is not

Not reduced deception. Not a lie detector. Not topic invariance. A field pass is not a handover. Cyber rows in the bank are administrative misses, not attack steps. The related literature on probes and steering is context, not evidence that this readout passes.

## Agent disclosure

Scenario design, probe scripts, scoring, and this note were produced with coding agents (Grok) under human direction. The human ran the model presses. Numbers are from the logged dumps. The agents did not invent scenarios and did not fill $D$.
