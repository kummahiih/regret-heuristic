# Expected versus measured room layout

An external room layout (the high-mass sets of [room_optimal_transport.md](room_optimal_transport.md), a set of roles such as “software engineer” or “sci-fi writer”, or any other partition of prompts) may be irrelevant to the model. The layout is a log we impose. It becomes evidence only when the same structure is recoverable from the model’s own weights or activations.

## Measured layout

Collect residual-stream activations (last-token or mean-pool of a short prefix) on a diverse set of prompts that cover the candidate rooms. Train a self-organizing map (SOM) on those vectors. The SOM produces a low-dimensional grid whose nodes are prototypes; nearby nodes respond to similar activations. The assignment of each prompt to its best-matching node is the **measured layout**.

Other topology-preserving projections (UMAP, t-SNE, or a simple linear map onto the top principal components) can be substituted; the SOM is named because it explicitly optimizes a discrete grid that preserves neighborhood relations.

## Expected versus measured

Label each prompt with the room it was assigned by the external layout (the expected label). After the SOM is trained, examine:

- whether prompts that share an expected room land on neighboring nodes,
- whether the high-mass sets of the probability-map rooms align with contiguous regions of the map,
- the topographic error and the purity of expected labels inside each node.

A high topographic error or a scattered label pattern means the chosen layout is not present in the residual stream at the chosen layer. The layout is then discarded as a candidate camera coordinate; it remains only a log of an external partition.

## What this is not

- Not a term in \(L_{\mathrm{total}}\).
- Not a replacement for the hinge.
- Not a claim that the SOM nodes are the model’s internal rooms.
- Not a strategy camera. A measured layout that matches the expected rooms still only shows that the model’s activations cluster by those rooms; the camera \(r\) must still see the plan rather than the room.

The comparison is a diagnostic that can reject an irrelevant layout before any pin bank is frozen. It does not fill \(D\).

## Relation to existing notes

- Rooms as high-mass sets: [room_optimal_transport.md](room_optimal_transport.md).
- Path/map vocabulary: [slam_analogy.md](slam_analogy.md). The measured SOM is one concrete map; the printed walk is still not the map.
- Clustering of readouts (ATC) is a different object: [clustering.md](clustering.md).

Lean bookkeeping is unchanged; the deterministic fibre remains the special case already formalized.
