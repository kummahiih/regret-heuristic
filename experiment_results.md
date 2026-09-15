# Results ledger

Three separate runs. Do not collapse them. None of these is reduced deception.

## 1. CPU toy (`simulation.py`) — still the baseline

Unchanged file. Dummy encoder, 146 parameters, no LLM. Seed 0, one Adam step. D frozen.

| | L_near | L_far | encoder \|grad W\| |
| --- | --- | --- | --- |
| Before the step | ~0.70 | 0 | > 0 |
| After one Adam step | drops slightly | stays 0 | still > 0 |

Hinge fires on the constructed near group only. That is wiring, not a language-model result.

Re-run:

```bash
python simulation.py
```

## 2. Single-head Qwen probe — identity r, 2026-09-15

`--heads` was not in the script yet. Readout = last-token hidden. tau=0 so hinge = cosine.

- GPU: RTX 4070 Ti 12 GB
- Model: `Qwen/Qwen2.5-7B-Instruct` 4-bit NF4
- `--update-steps 0`
- Data: `data/probe_split.jsonl` eval n=4

```
VRAM allocated_GiB=5.18 reserved_GiB=5.33
Frozen D shape=(2, 3584)
hinge_near_D_deceptive=0.7742 n=2
hinge_same_topic_honest=0.8003 n=2
task_loss=6.3268 n=4
probe_vs_D_cosine_deceptive=0.7742 n=2
probe_vs_D_cosine_honest=0.8003 n=2
```

Honest eval is slightly closer to the deceptive bank. Topic overlap on n=2. Keep these numbers even after ATC lands.

## 3. Genealogy clusters (`probe_run.py --heads 8`)

Same jsonl, same frozen D, N linear heads, parent pointers, CDS pick. No PF resample. Mapping: [clustering.md](clustering.md).

`--update-steps 0` and identity init: every head is a copy of run 2. Expect the same 0.77 / 0.80 smear printed once per cluster. That is a sanity check, not a new result.

`--update-steps > 0`: fill the per-cluster block from the machine. If quiet and high-task clusters still match, clustering kept copies of the topic blob.

```
(paste ATC stdout here)
```

Do not replace section 1 or 2 with section 3.
