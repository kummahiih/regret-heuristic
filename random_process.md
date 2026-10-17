# Random processes as nulls for an intent walk

This note collects standard random-process objects that can serve as null models when a simulated intent walk is later compared against noise. It is exploratory bookkeeping. It is not a camera, it does not fill *D*, and it does not claim that any real model walk has been shown to differ from these nulls.

## Random graphs

An Erdős–Rényi graph *G*(*n*, *p*) has *n* vertices and each possible edge present independently with probability *p* (Erdős & Rényi 1959, 1960). The expected degree is (*n*−1)*p*. Below the connectivity threshold the graph is a collection of small components; above it a giant component appears. Configuration-model graphs fix the degree sequence and randomize the wiring (Bollobás 1980). Preferential-attachment graphs grow by adding vertices that link to existing vertices with probability proportional to degree (Barabási & Albert 1999).

For a walk on hidden states, a random graph can supply a null topology: rooms or plan-pins connected by chance rather than by a shared rule. A later comparison can ask whether the observed co-occurrence of hides is denser, or more modular, than the same counts under an Erdős–Rényi or configuration null with the same marginals.

## Random walks

A simple random walk on the integers steps +1 or −1 with equal probability. On a graph it moves to a uniformly chosen neighbor. The position after *t* steps of a one-dimensional walk has variance linear in *t*; the walk is recurrent in one and two dimensions and transient in three and higher (Pólya 1921). Cover time, mixing time, and hitting time are the usual summaries (Levin, Peres & Wilmer 2009).

A null walk on the map of rooms is a walk that chooses the next room (or the next plan pin) without memory of a hide-or-name goal. An intent walk, if it exists, would be a walk whose transitions are biased by a short shared program. The comparison is then between the empirical transition counts and the counts expected under the null walk with the same degree sequence or the same stationary distribution.

## Gaussian processes

A Gaussian process is a collection of random variables, any finite subset of which is multivariate normal (Rasmussen & Williams 2006). It is specified by a mean function and a covariance (kernel) function. The squared-exponential kernel gives smooth sample paths; the Matérn kernel controls roughness; the Wiener kernel is Brownian motion. Posterior inference conditions on observed points and returns a posterior mean and variance at unobserved locations.

A Gaussian-process null on the residual stream would treat successive hidden states as draws from a GP with a chosen kernel, rather than as the output of a plan. A later comparison can ask whether the residuals of an intent-walk simulation are better predicted by a short parametric plan than by the GP posterior under a generic kernel. The GP is a flexible null, not a strategy camera.

## What a comparison would measure

When a simulated intent walk exists, the three nulls support three different contrasts:

- **Graph.** Is the co-occurrence pattern of the simulated hides denser or more clustered than an Erdős–Rényi or configuration null with the same number of nodes and edges?
- **Walk.** Do the transition counts deviate from the null random walk on the same graph (same stationary distribution, same degree sequence)?
- **Process.** Are the successive residuals better described by a short shared program than by the posterior of a Gaussian process with a generic kernel?

A positive answer on any of these is a description-length or likelihood comparison against a null. It is not evidence that a readout *r* sees a plan, and it is not a reason to fill *D*.

## What this note does not claim

- That any of these nulls has been fitted to a real model walk.
- That a deviation from the null is a strategy camera.
- That Gaussian-process uncertainty is the coarseness *u* of the hinge.
- That a random-graph component is a room, or that a random-walk hitting time is a hide.
- That the bank *D* may be filled from the modes of a fitted process.

## Sources

Barabási, A.-L., and R. Albert. 1999. Emergence of scaling in random networks. *Science* 286(5439): 509–512.

Bollobás, B. 1980. A probabilistic proof of an asymptotic formula for the number of labelled regular graphs. *European Journal of Combinatorics* 1(4): 311–316.

Erdős, P., and A. Rényi. 1959. On random graphs I. *Publicationes Mathematicae* 6: 290–297.

Erdős, P., and A. Rényi. 1960. On the evolution of random graphs. *Publications of the Mathematical Institute of the Hungarian Academy of Sciences* 5: 17–61.

Levin, D. A., Y. Peres, and E. L. Wilmer. 2009. *Markov Chains and Mixing Times*. American Mathematical Society.

Pólya, G. 1921. Über eine Aufgabe der Wahrscheinlichkeitsrechnung betreffend die Irrfahrt im Straßennetz. *Mathematische Annalen* 84: 149–160.

Rasmussen, C. E., and C. K. I. Williams. 2006. *Gaussian Processes for Machine Learning*. MIT Press.
