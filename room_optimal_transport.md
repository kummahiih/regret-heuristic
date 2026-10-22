# Rooms as answer sets reachable from the empty prompt, and shortest path as optimal transport

A **room** in the walk/map glossary is one subject neighborhood. Here we make that operational on the input side by measuring the shortest prefix/postfix path that reaches a given answer, starting from no input.

Let \( M \) be a language model. The empty prompt is written \( \varepsilon \). The **starting room** is the answer of the empty prompt:

\[
y_0 = M(\varepsilon).
\]

A pair of strings \( (\mathrm{pre}, \mathrm{post}) \) reaches answer \( y \) when

\[
M(\mathrm{pre} \mathbin{++} \mathrm{post}) = y.
\]

The **room** of \( y \) is the set of all such pairs:

\[
\mathrm{Room}(y) = \{ (\mathrm{pre},\mathrm{post}) \mid M(\mathrm{pre}++\mathrm{post}) = y \}.
\]

If the empty pair \( (\varepsilon,\varepsilon) \) belongs to \( \mathrm{Room}(y) \), then \( y = y_0 \) and the room is the starting room. Two answers sit in the same room precisely when they are equal; the room is the fibre \( M^{-1}(y) \) under end-insertion from the empty string.

## Shortest path from no input as optimal transport

The **shortest additional text** that reaches \( y \) from the empty prompt is

\[
\mathrm{OT}(y) = \inf \{ |\mathrm{pre}| + |\mathrm{post}| \mid (\mathrm{pre},\mathrm{post})\in\mathrm{Room}(y) \}.
\]

When the infimum is zero, \( y \) is the starting room. When it is positive, the shortest non-empty prefix/postfix that produces \( y \) is the cost of entering that room from silence. When it is infinite, no finite end-insertion reaches \( y \).

This quantity is an optimal-transport cost. Equip finite strings with the ground metric of end-insertion length

\[
d(s,t) = \min\{ |u|+|v| \mid u++s++v = t \}
\]

(with the usual convention \( d=\infty \) when no such pair exists). Let \( \mu_\varepsilon \) be the Dirac measure at the empty string and let \( \nu_y \) be any probability measure supported on the prompts that \( M \) maps to \( y \). Then

\[
\mathrm{OT}(y) = W_1(\mu_\varepsilon, \nu_y)
\]

where \( W_1 \) is the 1-Wasserstein distance induced by \( d \). The optimal coupling moves the mass at \( \varepsilon \) to a nearest prompt that yields \( y \); the cost of that move is exactly the shortest path length from no input.

In the discrete case the Wasserstein distance reduces to a pure transport, recovering the infimum above. Continuous token embeddings would replace \( d \) by a Euclidean or cosine ground metric; the same definition still names the shortest additional text that reaches the answer from the empty prompt.

## Forbidden rooms

Some models treat a particular system prompt (a fixed privileged instruction, not an arbitrary system-role marker) as a gate. Let \( s_* \) be that specific system prompt.

A room \( y \) is **forbidden** relative to \( s_* \) when every path that reaches it must contain \( s_* \) as a contiguous substring:

\[
\forall (\mathrm{pre},\mathrm{post})\in\mathrm{Room}(y),\quad
 s_* \text{ occurs in } \mathrm{pre}++\mathrm{post}.
\]

Equivalently, there is no finite end-insertion that yields \( y \) without including the exact system prompt \( s_* \). The starting room is never forbidden, because the empty path does not contain \( s_* \). A forbidden room is inaccessible from silence without that specific privileged instruction.

The OT cost of a forbidden room remains well-defined (the shortest path that does include \( s_* \)), but every witnessing path is marked as requiring the specific system prompt. The distinction is a log, not a gate.

## Relation to the hinge

A room in this sense is a subject neighborhood measured from silence: the set of end-insertions that the model treats as producing the same answer. The starting room is the answer of the empty prompt. Forbidden rooms are those that exist only behind a specific system prompt. The plan (hide-or-name) may sit inside several such rooms. The camera \( r \) is still required to see the plan rather than the room; the present definition only supplies a candidate notion of “same room” that can be measured without looking inside \( h \).

The length \( \mathrm{OT}(y) \) and the forbidden predicate are logs, not gates and not terms in \( L_{\mathrm{total}} \). They do not enter the hinge. They are bookkeeping for the distance of an answer from the empty prompt and for the presence of a specific system-prompt barrier.

## Caveats

- Deterministic \( M \). Stochastic decoding would replace equality of answers by total variation or a Wasserstein on the output distribution.
- Prefix/postfix only, measured from the empty string. Arbitrary insertions or deletions would be ordinary edit distance.
- The specific system prompt \( s_* \) is an external declaration, not inferred by the formalization.
- Not a claim that rooms so defined are the subject neighborhoods of the map. Not a camera. Not reduced deception.

Lean: [lean/RoomOptimalTransport.lean](lean/RoomOptimalTransport.lean).
