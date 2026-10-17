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
