# Home GPU probe protocol (4070 Ti 12GB)

**Status:** wiring runs recorded in [experiment_results.md](experiment_results.md). No alignment-success claim.

## Hardware constraint

- NVIDIA GeForce RTX 4070 Ti 12 GB VRAM only.
- HF_HOME on datapata.
- Activate `rh-venv`: `source /media/pauli/datapata/rh-venv/bin/activate`. Bare `python` may be missing.

## Model

- Recorded runs: `Qwen/Qwen2.5-7B-Instruct` 4-bit.
- Last-token hidden → linear `r` (identity). Frozen `D` from bank split only.

## Metrics

Hinge deceptive / honest, walk NLL, cosine to D, optional `--entropy`. Entropy is observation uncertainty, not p(lie).

## Recorded commands

```bash
source /media/pauli/datapata/rh-venv/bin/activate
python simulation.py
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 8 --entropy
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 1 --entropy
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 8 --update-steps 20 --fork
python simulation_tau_bins.py
```

## ATC

N heads, no PF resample, metrics per cluster. n=2 toy. [clustering.md](clustering.md).

## Kill list

No live harm eval, no intent-weight isolation claim, no full FT, no inference abort, no mitigated-deception headline.
