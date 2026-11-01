# Rooms as high-mass sets on the model's probability map, and shortest path as optimal transport

A **room** in the walk/map glossary is one subject neighborhood. Here we make that operational by reading it from the model's own next-token distribution rather than from an external equality of decoded strings. A room may be a single answer, or a broader role (software engineer, sci-fi writer, helpful assistant, etc.).

Let \(M\) be a language model with parameters \(\theta\). Write \(p_\theta(\cdot\mid x)\) for the next-token distribution given prefix \(x\). The empty prompt is \(\varepsilon\). The **starting room** is the high-mass set of the empty prompt:

$$
R_0 = \{ y \mid p_\theta(y\mid\varepsilon)\ge\tau \}.
$$

(The threshold \(\tau\) is a free parameter of the log; different values give coarser or finer partitions.)

## Liberal rooms

A room need not be a single string. Let \(R\) be any set of strings that the model treats as interchangeable for a purpose—an exact answer, a role description, a genre, a persona. Examples:

- the singleton \(\{y\}\) for a concrete answer,
- the set of strings that a human would label “software engineer” (or that a small classifier on the model’s own continuations labels that way),
- the set of strings that a human would label “sci-fi writer”.

The **room** of \(R\) is the set of prefixes that place high mass on \(R\):

$$
\mathrm{Room}(R) = \{ x \mid p_\theta(R\mid x)\ge\tau \},
$$

where \(p_\theta(R\mid x)=\sum_{y\in R}p_\theta(y\mid x)\) (or the probability that a sampled continuation falls in \(R\)). Two roles sit in the same room when their high-mass sets coincide up to the chosen \(\tau\). The partition is now induced by the model’s probability map, not by an external decoder equality.

When \(R=\{y\}\) and decoding is deterministic, this recovers the earlier fibre \(M^{-1}(y)\). The liberal version simply allows \(R\) to be any measurable set of interest.

## Shortest path from no input as optimal transport

The **shortest additional text** that reaches room \(R\) from the empty prompt is

$$
\mathrm{OT}(R) = \inf\{ |u|+|v| \mid u++v\in\mathrm{Room}(R) \}.
$$

When the infimum is zero, \(R\) intersects the starting room. When it is positive, the shortest non-empty end-insertion that enters the high-mass set of \(R\) is the cost of entering that room from silence. When it is infinite, no finite end-insertion reaches the room.

This quantity is a minimum-insertion cost, not a Wasserstein distance. The proposed ground cost

$$
d(s,t)=\min\{ |u|+|v| \mid u++s++v=t \}
$$

is asymmetric. It permits transforming \(s\) into \(t\) by insertion, but not the reverse. It is therefore not a metric. Standard Wasserstein distance requires a metric or a transport cost with stated assumptions. The equality

$$
\mathrm{OT}(R)=W_1(\mu_\varepsilon,\nu_R)
$$

does not hold for an arbitrary destination measure \(\nu_R\). The correct quantity is the minimum distance to the set:

$$
\mathrm{OT}(R)=\inf_{x\in\mathrm{Room}(R)} d(\varepsilon,x).
$$

Under that definition the cost is the length of the shortest end-insertion that enters the room. When the infimum is zero, the room intersects the starting room. When it is infinite, no finite end-insertion reaches the room. The keyword-match estimate at n=16 is a lower bound on this cost, not a Wasserstein distance.

Continuous token embeddings would replace \(d\) by a Euclidean or cosine ground metric; the same definition still names the shortest additional text that enters the high-mass set of the room.

## Forbidden rooms

Some models treat a particular system prompt (a fixed privileged instruction, not an arbitrary system-role marker) as a gate. Let \(s_*\) be that specific system prompt.

A room \(R\) is **forbidden** relative to \(s_*\) when every prefix that places high mass on \(R\) must contain \(s_*\) as a contiguous substring:

$$
\forall x\in\mathrm{Room}(R),\quad s_*\text{ occurs in }x.
$$

Equivalently, there is no finite end-insertion that enters the high-mass set of \(R\) without including the exact system prompt \(s_*\). The starting room is never forbidden. A forbidden room is inaccessible from silence without that specific privileged instruction.

The OT cost of a forbidden room remains well-defined (the shortest path that does include \(s_*\)), but every witnessing path is marked as requiring the specific system prompt. The distinction is a log, not a gate.

## Relation to the hinge

A room in this sense is a subject neighborhood (or a role) measured from silence by the model’s own probability map. The plan (hide-or-name) may sit inside several such rooms. The camera \(r\) is still required to see the plan rather than the room; the present definition only supplies a candidate notion of “same room” that can be read off \(p_\theta\) without looking inside \(h\).

The length \(\mathrm{OT}(R)\) and the forbidden predicate are logs, not gates and not terms in \(L_{\mathrm{total}}\). They do not enter the hinge. They are bookkeeping for the distance of a role or answer from the empty prompt and for the presence of a specific system-prompt barrier.

## Caveats

- The threshold \(\tau\) and the set \(R\) are parameters of the log. Different choices give different partitions; none is claimed to be the unique subject neighborhood of the map.
- Prefix/postfix only, measured from the empty string. Arbitrary insertions or deletions would be ordinary edit distance.
- The specific system prompt \(s_*\) is an external declaration, not inferred by the formalization.
- Not a claim that rooms so defined are the subject neighborhoods used by the model’s internal computation. Not a camera. Not reduced deception.
- The deterministic fibre of the earlier note is the special case \(R=\{y\}\) under greedy decoding. The Lean file remains that special case.

Lean: [lean/RoomOptimalTransport.lean](lean/RoomOptimalTransport.lean).
