# Overnight simulations (diagnostics with promotion gate)

All scripts are diagnostics until `protocol_gate.md` records a pass.

## Quick error checks (minutes)
```bash
python smoke_probe.py
python iosd_probe.py --smoke
python som_layout.py --smoke
```

## Probe comparison
`iosd_probe.py` extracts K orthogonal directions and scores max-cosine.
Compare against a single linear direction and against note-text baseline on a topic split.
Promotion only if the frozen bank passes the gate in protocol_gate.md.

## Map layout
`som_layout.py` builds a measured SOM and reports purity against expected room/role labels.
Promotion only if a prototype passes the same gate.

## Long run
Once a candidate bank is written, reuse the existing 4-bit `probe_run.py` path
with the frozen bank as D. Log the four metrics. Do not claim a camera from AUROC alone.

No script inserts a hinge term unless the gate has passed.
