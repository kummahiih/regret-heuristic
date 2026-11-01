# Nightly simulation batch

Diagnostic scripts for a home GPU (e.g. 12 GB). They test two candidate improvements to the search for a strategy readout. They do not train the hinge and they do not fill \(D\) unless an explicit gate is passed.

Target of the repo remains unchanged: a training-time regularizer that penalizes a frozen strategy coordinate (or a small bank of them) while the task loss stays intact. These scripts only propose or reject candidate coordinates.

## What is being tested

1. **Huang-style multi-direction probe** (iterative orthogonal decomposition).  
   Single linear directions often fail to transfer. The script extracts a small set of orthogonal directions and scores max-cosine against that bank. The domain-adaptive gating network from the paper is **not** used inside any loss; it may be used only offline to choose a subset.

2. **SOM measured layout**.  
   An external room layout (answer fibre, role, high-mass set, topic polytope, etc.) may be irrelevant to the residual stream. The script trains a self-organizing map on activations and compares the measured assignment to the expected labels.

Both stay diagnostics until `protocol_gate.md` records a pass.

## Promotion gate (required for either method)

A candidate enters the protocol only when all of the following hold:

- **Topic transfer.** On a held-out topic never seen in the fitting set, the candidate separates the press (hide vs name) better than a note-text baseline and better than a pure topic probe. Same-topic AUROC is not enough.
- **Frozen.** The directions or prototypes are frozen before any hinge update. Movement is camera-drag, not a hinge.
- **Differentiable slap.** The score that would enter \(L_{\mathrm{reg}}\) is a function of the hidden state that admits a gradient (max-cosine against the frozen bank). A test-time network re-fit on labels is a monitor, not this slap.
- **Skill intact.** Any later hinge step must not collapse task loss.

Failure on any clause leaves the method as a log. It does not fill \(D\).

## Files

| File | Role |
| --- | --- |
| `protocol_gate.md` | The gate above. Read this first. |
| `smoke_probe.py` | Minute-scale check of hinge math. No model. |
| `iosd_probe.py` | Orthogonal-direction extraction and max-cosine scoring. `--smoke` for a no-model check. |
| `som_layout.py` | SOM expected-vs-measured purity. `--smoke` for a no-model check. |
| `../room_layout_map.md` | Candidate layouts under test and the home-setup sketch. |
| `../probe_run.py` | Existing 4-bit path. Re-used for the long topic sweep only after a frozen bank is written to disk. |

## Suggested order

```bash
cd night_sims
python smoke_probe.py
python iosd_probe.py --smoke
python som_layout.py --smoke
# then, on cached activations or a small model:
# python iosd_probe.py ...
# python som_layout.py ...
```

Long run (only after a candidate bank exists): point the existing `probe_run.py` at the frozen bank and log the four metrics per topic. Do not claim a camera from AUROC alone.

## What this batch does not do

- It does not insert a hinge term.
- It does not treat a high AUROC as evidence that a strategy camera exists.
- It does not freeze persona, topic, or role directions as \(D\).
- It does not use test-time adaptation inside the loss.
- It does not change the target of the repo.

Reviewers: the only path from these scripts into the hinge is the gate in `protocol_gate.md`. Everything else is a diagnostic log.
