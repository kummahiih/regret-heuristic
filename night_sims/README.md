# Overnight simulations (diagnostics with promotion gate)

All scripts are diagnostics until `protocol_gate.md` records a pass.

## Quick error checks (minutes)
```bash
cd night_sims
python smoke_probe.py
python iosd_probe.py --smoke
python som_layout.py --smoke
```

## Probe comparison (Huang-style IOSD)
`iosd_probe.py` extracts K orthogonal directions and scores max-cosine.
Compare against a single linear direction and against a note-text baseline on a topic split.
Promotion only if the frozen bank passes the gate in protocol_gate.md.
The domain-adaptive gating network is offline only; it does not enter the loss.

## Map layout (SOM)
`som_layout.py` builds a measured SOM and reports purity / NMI against expected room, role, and topic labels.
Include ask-removal and topic-shuffle controls.
Promotion only if a prototype passes the same gate.
See [../room_layout_map.md](../room_layout_map.md) for the candidate layouts under test.

## Long run
Once a candidate bank is written to disk, reuse the existing 4-bit `probe_run.py` path
with the frozen bank as D. Log the four metrics per topic.
Do not claim a camera from AUROC alone.

No script inserts a hinge term unless the gate has passed.
