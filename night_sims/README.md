# Nightly simulation batch

Diagnostic prototypes for a home GPU. They test two candidate improvements to the search for a strategy readout. They do not train the hinge and they do not fill \(D\) unless an explicit gate is passed.

**Status: prototypes / smoke tests.** Real activation loaders, held-out topic evaluation, and full comparison pipelines are not yet implemented. Do not treat these as ready overnight experiments.

Target of the repo remains unchanged: a training-time regularizer that penalizes a frozen strategy coordinate (or a small bank of them) while the task loss stays intact. These scripts only propose or reject candidate coordinates.

## What is being tested

1. **Huang-style multi-direction probe** (iterative orthogonal decomposition).  
   Extracts a small set of orthogonal directions and scores signed max-cosine against that bank. Degenerate directions (near-zero residual after orthogonalization) are rejected. The domain-adaptive gating network is offline only.

2. **SOM measured layout**.  
   Trains a self-organizing map with true 2-D Euclidean neighborhood and compares the measured assignment to expected labels (role, topic, condition, etc.).

Both stay diagnostics until `protocol_gate.md` records a pass.

## Promotion gate

See `protocol_gate.md`. Required: topic transfer, frozen, differentiable slap, skill intact. Additional criteria (paraphrase, counterfactual, adversarial) are noted but not yet implemented.

## Files

| File | Role | Status |
| --- | --- | --- |
| `protocol_gate.md` | The gate. | Design |
| `smoke_probe.py` | Hinge math check. | Smoke |
| `iosd_probe.py` | Orthogonal directions. `--smoke` only. | Prototype |
| `som_layout.py` | SOM layout. `--smoke` only. | Prototype |
| `../room_layout_map.md` | Candidate layouts. | Note |
| `../probe_run.py` | Existing 4-bit path. | Unchanged |

## Suggested order (smoke only)

```bash
cd night_sims
python smoke_probe.py
python iosd_probe.py --smoke
python som_layout.py --smoke
```

No real data pipeline exists yet. A proper comparison (single linear, IOSD bank, PCA baseline, topic-only, note-text) on identical held-out topics is the next implementation step, not an overnight run.

## What this batch does not do

- It does not insert a hinge term.
- It does not treat a high AUROC as evidence that a strategy camera exists.
- It does not freeze persona, topic, or role directions as \(D\).
- It does not use test-time adaptation inside the loss.
- It does not change the target of the repo.
- It does not yet evaluate on real activations.

Reviewers: the only path from these scripts into the hinge is the gate in `protocol_gate.md`. Everything else is a diagnostic log. Current code is smoke-level.
