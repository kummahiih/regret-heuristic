# Expected versus measured room layout

An external room layout may be irrelevant to the model. The layout is a log we impose. It becomes evidence only when the same structure is recoverable from the model’s own activations.

## Candidate layouts (from literature and first principles)

- **Answer fibres** \(M^{-1}(y)\). Defined on inputs and outputs. On their own they say nothing about the residual stream.
- **Persona rooms.** Assistant Axis (arXiv:2601.10387), persona vectors, OpenAI persona features. Top PC of role vectors separates Assistant from role-play; the axis already exists in the base model. Roles such as “software engineer” or “sci-fi writer” sit here. A persona room shows a character, not a plan formed before the ask.
- **Concept polytopes (topic rooms).** Park et al. (arXiv:2406.01506). Categories as simplices. Main confound for any strategy layout.
- **Belief-state rooms.** Shai et al. (arXiv:2405.15943). Belief simplex in the residual stream; so far only on small synthetic models.
- **Honest/deceptive half-spaces.** RepE and Goldowsky-Dill linear probes. Partly track “this scenario is about deception” rather than “this answer is deceptive.”
- **High-mass sets under \(p_\theta\).** [room_optimal_transport.md](room_optimal_transport.md). First-principles. The partition is read from the model’s next-token distribution.
- **Unsupervised maps.** SOM or Mapper on residual activations. Label-free; can test which of the above the data prefers.

## Measured layout

Collect residual-stream activations on a diverse prompt set that covers the candidate rooms. Train a self-organizing map (SOM) on those vectors. The assignment of each prompt to its best-matching node is the measured layout.

Suggested home-setup sketch (once activations are cached):
- ~8 layers, 4 positions (end of role text, just before the ask, last prompt token, mean over response).
- Center, PCA to ~50 dimensions; also try subtracting per-topic means.
- Grid size ~\(5\sqrt{n}\), init on the PCA plane, 20–50 epochs, multiple seeds.
- Score NMI / ARI / purity of each candidate label against unit assignments, with permutation nulls. Include ask-removal and topic-shuffle controls.

A high topographic error, scattered labels, or alignment that appears only after topic means are removed means the chosen layout is not present as a stable residual-stream partition.

## What this is not

- Not a term in \(L_{\mathrm{total}}\).
- Not a replacement for the hinge.
- Not a claim that SOM nodes are the model’s internal rooms.
- Not a strategy camera. Correlation is not use. A measured layout that matches expected rooms still only shows clustering; the camera \(r\) must see the plan rather than the room.
- Topic swamps strategy. Lexical leakage (“lie” in the instruction) can sort the map by itself. The SOM forces a 2-D shape.

The comparison is a diagnostic that can reject an irrelevant layout before any pin bank is frozen. It does not fill \(D\). Promotion to a pin bank is governed by [night_sims/protocol_gate.md](night_sims/protocol_gate.md).

## Relation to existing notes

- Rooms as high-mass sets: [room_optimal_transport.md](room_optimal_transport.md).
- Path/map vocabulary: [slam_analogy.md](slam_analogy.md).
- Clustering of readouts (ATC) is a different object: [clustering.md](clustering.md).
- Overnight diagnostics: [night_sims/](night_sims/).

Lean bookkeeping is unchanged.
