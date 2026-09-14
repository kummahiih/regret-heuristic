# Ethics review (not approval)

This note is a short dual-use and scope review for the home-GPU probe protocol. It is **not** an IRB letter, not institutional approval, and not permission to run any live evaluation.

## Scope limits

- Synthetic deception strings only (hand-written English same-topic plan pairs).
- No live harmful-request evaluation.
- No claim that this work constitutes IRB review or human-subjects oversight.
- Bank / D vectors are toy text prototypes, not exploits or attack payloads.

## Dual-use note

The bank split supplies frozen deceptive-intent prototypes for a linear probe. Those strings are synthetic and topic-matched to honest counterparts; they are not operational advice, not real-world exploit code, and not intended for deployment as a filter or conscience layer.

Representation gaming, entanglement, and overclaim remain open risks. The protocol therefore forbids any “mitigated deception” or “alignment success” sentence in results or README.

## Status

Review only. User runs the probe on local 4070 Ti hardware under the constraints in `experiment.md`.
