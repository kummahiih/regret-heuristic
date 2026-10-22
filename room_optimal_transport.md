# Rooms as input-invariant answer sets, and shortest stabilizer as optimal transport

A **room** in the walk/map glossary is one subject neighborhood. Here we make that operational on the printed walk by asking when prefix and postfix text leave the answer unchanged.

Let \( M \) be a language model. Fix a base prompt \( x \) with answer \( y = M(x) \). A **stabilizer** of \( y \) relative to \( x \) is a pair of strings \( (\mathrm{pre}, \mathrm{post}) \) such that

\[
M(\mathrm{pre} \mathbin{++} x \mathbin{++} \mathrm{post}) = y.
\]

The **room** of \( y \) at \( x \) is the set of all such stabilizers:

\[
\mathrm{Room}(x,y) = \{ (\mathrm{pre},\mathrm{post}) \mid M(\mathrm{pre}++x++\mathrm{post}) = y \}.
\]

(The empty pair is always a member when \( M(x)=y \).) Two prompts sit in the same room when there exist stabilizers taking one to the other while the answer stays \( y \). The room is therefore an equivalence class of prompts under answer-preserving prefix/postfix edits.

## Shortest additional text as optimal transport

The **shortest additional text** that keeps the answer is the minimal total length of a non-trivial stabilizer:

\[
\mathrm{OT}(x,y) = \inf \{ |\mathrm{pre}| + |\mathrm{post}| \mid (\mathrm{pre},\mathrm{post})\in\mathrm{Room}(x,y),\ (\mathrm{pre},\mathrm{post})\neq(\varepsilon,\varepsilon) \}.
\]

(When the inf is infinite the answer is fragile; when it is zero the model is already insensitive to the empty extension.)

This quantity is an optimal-transport cost. Equip the space of finite strings with the ground metric

\[
d(s,t) = \min\{ |u|+|v| \mid u++s++v = t \},
\]

the minimal length of prefix/postfix that turns \( s \) into \( t \). (This is a special case of edit distance that only inserts at the ends.) Let \( \mu_x \) be the Dirac measure at \( x \) and let \( \nu_y \) be any probability measure supported on the set of prompts that \( M \) maps to \( y \). Then

\[
\mathrm{OT}(x,y) = W_1(\mu_x, \nu_y)
\]

where \( W_1 \) is the 1-Wasserstein distance induced by \( d \). The optimal coupling simply moves the mass at \( x \) to the nearest prompt (in the \( d \)-metric) that still produces \( y \); the cost of that move is exactly the shortest stabilizer length.

In the discrete finite-support case the Wasserstein distance reduces to a linear program whose optimum is attained at a pure transport, recovering the infimum above. Continuous embeddings of tokens would replace \( d \) by a Euclidean or cosine ground metric on the embedding space; the same definition still names the shortest additional text that keeps the answer.

## Relation to the hinge

A room in this sense is a subject neighborhood on the input side: prompts that the model treats as interchangeable for the purpose of producing \( y \). The plan (hide-or-name) may sit inside several such rooms. The camera \( r \) is still required to see the plan rather than the room; the present definition only supplies a candidate notion of “same room” that can be measured without looking inside \( h \).

The length \( \mathrm{OT}(x,y) \) is a log, not a gate and not a term in \( L_{\mathrm{total}} \). It does not enter the hinge. It is bookkeeping for how large a neighborhood the model already treats as one subject.

## Caveats

- Deterministic \( M \). Stochastic decoding would replace equality of answers by total variation or a Wasserstein on the output distribution.
- Prefix/postfix only. Arbitrary insertions or deletions would be ordinary edit distance; the end-only restriction matches the “additional text” reading.
- Not a claim that rooms so defined are the subject neighborhoods of the map. Not a camera. Not reduced deception.

Lean: [lean/RoomOptimalTransport.lean](lean/RoomOptimalTransport.lean).
