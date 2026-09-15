# Home GPU probe protocol (4070 Ti 12GB)

**Status:** recorded in [experiment_results.md](experiment_results.md) §1–§7. Further \(r\) tries: [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

Activate `rh-venv`. Recorded model: `Qwen/Qwen2.5-7B-Instruct` 4-bit.

```bash
python simulation.py
python simulation_tau_bins.py
python simulation_heldout.py
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 1 --entropy
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 1 --entropy --pool mean
cd lean && lake build
```
