# Random intent emergence

A null model for the chance appearance of a shared short description among independent cases. It is a comparison object for the negative handover: the search found no strategy camera on this bank. This note does not claim that a random intent did or did not emerge, and it does not fill *D*.

## The null

Each case is an independent string of length *ℓ*. A shared intent is a short program of length *b* that generates a subset of the cases, plus a residual of length *c* per case. Under pure independence the probability that any particular short program of length *b* happens to cover *k* of the *n* cases is the probability that those *k* strings lie in the image of that program.

A simple counting version treats each case as a random element of a set of size *M*. The number of cases that match a fixed short description of capacity *M*<sub>intent</sub> is Binomial(*n*, *p*) with *p* = *M*<sub>intent</sub> / *M*. The expected number of matching cases is *n p*. A shared intent “emerges” in the null when the observed match count exceeds a threshold that would be rare under this binomial (or under the corresponding MDL crossover).

## Emergence threshold

Let *K*(*C*) be the Kolmogorov complexity of the collection. Under the independent null,

```math
\mathbb{E}[K(C)] \approx n \cdot \ell.
```

Under a shared program of length *b* that explains a fraction *f* of the cases,

```math
K_{\mathrm{shared}}(C) \approx b + f n \cdot c + (1-f) n \cdot \ell.
```

The shared description is shorter in expectation when

```math
b < f n (\ell - c).
```

For fixed *b*, *ℓ*, *c* the expected crossover is linear in *n*. A random fluctuation can push a particular finite sample across the threshold even when the true process is independent. That is the false-positive emergence the null is meant to bound.

## Relation to the negative handover

The negative handover recorded that a pre-button residual predicted the button only after the ask was seen, and that note-only and ask-only controls failed. Under the random-intent null that pattern is the expected signature of a walk that has already committed to the print: the residual after the ask is short because the next token is determined, not because a shared hide-plan of length *b* generated the note.

A later comparison can ask whether the observed button-prediction accuracy on the 114-row bank exceeds the accuracy expected from a random residual of the same dimension after the ask, or whether the MDL crossover for the logged hides is reached under the independent null. Neither comparison has been run. Both remain logs.

## What this note does not claim

- That a random intent emerged on the searched bank.
- That the absence of a camera is explained by the null.
- That the binomial or the MDL crossover is a gate.
- That *D* may be filled from the modes of the null.
- That Gaussian-process or random-graph nulls (see [random_process.md](random_process.md)) are the same object as this emergence model.

## Sources

Cover, T. M., and J. A. Thomas. 2006. *Elements of Information Theory*. Wiley.

Kolmogorov, A. N. 1965. Three approaches to the quantitative definition of information. *Problems of Information Transmission* 1(1): 1–7.

Li, M., and P. Vitányi. 1997. *An Introduction to Kolmogorov Complexity and Its Applications*. Springer.

Rissanen, J. 1978. Modeling by shortest data description. *Automatica* 14(5): 465–471.
