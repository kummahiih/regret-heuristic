# Home GPU probe protocol (4070 Ti 12GB)

**Status:** wiring runs recorded in [experiment_results.md](experiment_results.md). No alignment-success claim.

## Hardware constraint

- NVIDIA GeForce RTX 4070 Ti 12 GB VRAM only.
- Activate `rh-venv`: `source /media/pauli/datapata/rh-venv/bin/activate`.

## Model

- Recorded runs: `Qwen/Qwen2.5-7B-Instruct` 4-bit.
- Walk observation: `--pool last` (default) or `--pool mean` (mean of last-layer tokens, pad-masked). Frozen D uses the same pool.

## Recorded commands

```bash
source /media/pauli/datapata/rh-venv/bin/activate
python simulation.py
python simulation_tau_bins.py
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 1 --entropy
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 1 --entropy --pool mean
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 8 --update-steps 20 --fork
```

## Kill list

No live harm eval, no intent-weight isolation, no full FT, no inference abort, no mitigated-deception headline.
