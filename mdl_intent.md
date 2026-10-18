# When enough cases become an intent

Kolmogorov complexity and the minimum description length (MDL) principle supply one formal reading of the question “when do individual cases add up to an intent?” This note is exploratory bookkeeping. It is not a claim that a camera exists, and it does not fill *D*.

## Kolmogorov complexity

The Kolmogorov complexity *K*(*x*) of a finite string *x* is the length of the shortest program, in a fixed universal language, that outputs *x* and halts (Kolmogorov 1965; Chaitin 1969; Solomonoff 1964). It is uncomputable, but the difference between two universal languages is at most a constant independent of *x* (invariance). A string is incompressible when *K*(*x*) is close to its literal length.

A set of cases *C* = {*c*<sub>1</sub>, …, *c*<sub>*n*</sub>} has complexity *K*(*C*). If the cases are independent, *K*(*C*) is roughly the sum of the individual complexities. If they share a short generating rule, *K*(*C*) is roughly the length of that rule plus the length of the residual that the rule does not explain.

## Minimum description length

The MDL principle (Rissanen 1978, 1989) prefers the hypothesis that minimizes the sum of two lengths: the description length of the hypothesis itself, plus the description length of the data given the hypothesis. Ideal MDL uses Kolmogorov complexity for both terms (Li & Vitányi 1997). Practical MDL replaces the uncomputable lengths with concrete codes (two-part codes, normalized maximum likelihood, etc.).

For a collection of observed hides, the competing hypotheses are:

- **Independent cases.** Each hide is its own short program (or its own literal record). Total length ≈ Σ *K*(*c*<sub>*i*</sub>).
- **Shared intent.** A single short program *p* (the plan, the strategy) generates the cases, plus a short residual for the parts *p* does not fix. Total length ≈ |*p*| + *K*(residual | *p*).

When the second total is shorter, MDL prefers the shared-intent hypothesis. That is the point at which “enough cases” have accumulated for the intent to be the shorter description.

## How many is enough

Let *L*<sub>ind</sub>(*n*) be the length of the independent-cases description of *n* hides, and *L*<sub>shared</sub>(*n*) the length of the shared-intent description. The crossover is the smallest *n* such that

```math
L_{\mathrm{shared}}(n) < L_{\mathrm{ind}}(n).
```

Under a simple linear model the independent length grows as *a n* (each case costs a fixed overhead) while the shared length grows as *b + c n* with *c* < *a* (the residual is cheaper). The inequality holds once

```math
n > \frac{b}{a - c}.
```

The constant *b* is the length of the shared program (the intent). A shorter intent, or a residual that compresses more, lowers the threshold. A longer intent raises it. The threshold is not a fixed integer; it depends on how compressible the shared rule is relative to the cases.

This is not a statistical significance test. It is a description-length comparison. A single dramatic case can have low complexity on its own; a large set of loosely related cases can still be longer under the shared hypothesis than under independence.

## Relation to the hinge

The prototype bank *D* is a candidate short description of a banned plan class. The camera *r* is a candidate sensor that sees whether the walk is close to that description. MDL supplies one reading of why a frozen bank is attractive: if the observed hides are shorter under the bank than under independent cases, the bank is the preferred hypothesis. It does not supply the camera, and it does not say that a quiet hinge is honesty.

Quiet below τ is still only “not close enough to a listed pin.” An orthogonal hide-plan that the bank does not name remains in the dead zone. Representation gaming can shorten the apparent description of the readout without shortening the description of the behavior. MDL on the observed buttons is not MDL on the internal walk, and neither is a gate.

## A falsifiable reading: intentional absence

The base idea is that the lack of an intent readout can itself look intentional. If the cases are shorter under a shared description, Occam’s razor (MDL) says a shared intent is the preferred hypothesis. If a probe that is capable of seeing that structure nevertheless returns none, the absence is not “the data contain no shared structure.” The absence is the thing to be explained.

The hypothesis, stated so it can fail:

> On a collection *C* of cases, if *L*<sub>shared</sub>(*C*) < *L*<sub>ind</sub>(*C*) under a fixed code, and if a residual probe that has passed the surface controls on other banks fails to predict the realized button from the note alone on *C*, then the missing readout is recorded as intentional avoidance of the shared description, not as the absence of shared structure.

Boundaries that keep the claim from being free:

- The description-length comparison must be fixed before looking at the probe. A code chosen after the probe result is not the hypothesis.
- The probe must be one that could have seen a shared plan. A probe already known to be blind (last-token identity, ask-only, a model without weights) does not license the claim.
- Small *n*, compressor overhead, and topic leakage can cross the MDL threshold by chance. The random-intent-emergence null is the comparison for that. A chance cross is not intentional absence.
- The claim is a log about the pair (description length, probe). It does not fill *D*, it does not freeze *r*, and it does not override the negative handover on the bank that was searched.
- On the 114-row bank the note-plus-prebutton probe cleared the bar only after the ask was seen, and the MDL crossover has not been measured. The hypothesis is not yet instantiated there.

This is the rudimentary boundary the idea supplies: data that support a shared intent by description length, together with a capable probe that finds none, are the conditions under which the lack of intent is treated as intentional. Outside those conditions the lack remains “not shown.”

## Faults in the current runnable check

The script `intentional_absence_check.py` in the search repo returns `intentional_absence = True` on the 114-row bank. That verdict is not evidence for the hypothesis. Three faults make it uninformative.

1. **Shared compression is true by construction.** Every `scenario_id` pairs a hide note with a name note that states the same proposition. Zlib compresses those pairs better together by design of the bank. Mean \(R = 1.691\) and 38/38 pairs above threshold show shared topic and wording, not a shared hide-plan that a probe missed. Occam’s razor here prefers “these sentences are about the same fact.”

2. **The “capable probe” is a probe already known to be blind.** The hypothesis requires a residual probe that could have seen a shared plan and still finds none. The script uses the note-only result, which failed because it does not see a plan in the note. Satisfying “finds none” with a probe never shown to be capable makes the conjunction true for the wrong reason. The pre-button residual that predicts the button does so only after the ask; that is next-token preparation.

3. **The verdict cannot fail on this bank.** The probe side is hardcoded from the negative handover, and the description-length side is guaranteed by the paired notes. On the data the script was written for, the flag is forced true. A check that cannot return false is not a test.

A repaired check would need a null in which notes are paired by topic but not by shared proposition, a probe that has detected a planted shared plan on a positive control and then fails on the target bank, and the chance-cross comparison against the random-intent null. Until those exist the script is a restatement of “the notes are similar and the note-only probe failed,” not evidence that the absence is intentional.

## What this note does not claim

- That Kolmogorov complexity is computable, or that a practical code has been written for the hide bank.
- That the crossover *n* has been measured on any model.
- That a short shared program is a strategy camera.
- That MDL replaces the four statistical gates or the ask-removal controls.
- That filling *D* from the shortest program is licensed. The bank remains frozen and empty until a validated camera exists.

## Sources

Chaitin, G. J. 1969. On the length of programs for computing finite binary sequences. *Journal of the ACM* 16(1): 145–159.

Kolmogorov, A. N. 1965. Three approaches to the quantitative definition of information. *Problems of Information Transmission* 1(1): 1–7.

Li, M., and P. Vitányi. 1997. *An Introduction to Kolmogorov Complexity and Its Applications*. Springer.

Rissanen, J. 1978. Modeling by shortest data description. *Automatica* 14(5): 465–471.

Rissanen, J. 1989. *Stochastic Complexity in Statistical Inquiry*. World Scientific.

Solomonoff, R. J. 1964. A formal theory of inductive inference, part I. *Information and Control* 7(1): 1–22.
