# Results ledger

Separate runs. Do not collapse them. None of these is reduced deception.

## 1. CPU toy (`simulation.py`) — still the baseline

Dummy encoder, 146 parameters, no LLM. Seed 0, one Adam step. D frozen. Numbers from 2026-09-15 local rerun after `git pull`.

| | L_task | L_regret | L_total | L_near | L_far | \|grad W\| |
| --- | --- | --- | --- | --- | --- | --- |
| Before | 0.7310 | 0.3500 | 0.9060 | **0.7000** | **0.0000** | 0.473 |
| After 1 Adam step | 0.6759 | 0.3486 | 0.8502 | **0.6971** | **0.0000** | 0.472 |

Hinge fires on the constructed near pair only. Wiring, not a language-model result.

```bash
python simulation.py
```

## 2. Single-head Qwen probe — identity r, 2026-09-15

Readout = last-token hidden. tau=0 so hinge = cosine. No `--heads` yet.

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

Honest eval is slightly closer to the deceptive bank. Topic overlap on n=2.

## 3. Genealogy clusters (`probe_run.py --heads 8`)

Same machine, model, jsonl, frozen D. N=8 identity linear heads on CPU. CDS picks who gets SGD. No PF resample. [clustering.md](clustering.md).

### 3a. Zero update (sanity)

`--heads 8` (no `--update-steps`). parents all -1. Eight singleton clusters. Each line equals section 2:

```
cluster_id=0..7  hinge_near_D_deceptive=0.7742 n=2  hinge_near_D_honest=0.8003 n=2
task_loss=6.3268  probe_vs_D_cosine same as hinge
```

Eight copies of the topic smear. Tree never started.

### 3b. One step + fork

`--heads 8 --update-steps 1 --fork`

- `parents=[-1, 0, -1, …]`
- `cluster_id=[0, 0, 2, 3, 4, 5, 6, 7]`  roots=[0]  Ws=[2, 1, …]
- `who_stepped=0` (CDS scores 2.0 on cluster 0)
- `hinge_train=0.7652`

| cluster | deceptive | honest | n (dec/hon) |
| --- | --- | --- | --- |
| 0 (heads 0+1) | 0.7732 | 0.7994 | 4 / 4 |
| 2–7 (identity) | 0.7742 | 0.8003 | 2 / 2 |

Cluster 0 is the mean of a slightly stepped parent and an unstepped child. Gap did not open.

### 3c. Twenty steps + fork

`--heads 8 --update-steps 20 --fork`

Train hinge on head 0 only: 0.7652 → **0.6951** (monotone).

| cluster | deceptive | honest |
| --- | --- | --- |
| 0 (heads 0+1 averaged) | **0.7509** | **0.7782** |
| 2–7 | 0.7742 | 0.8003 |

Task loss stayed 6.3268 (backbone frozen). Honest and deceptive eval on cluster 0 dropped by about the same amount. Honest stayed closer to D. CDS never left cluster 0.

### Read

The hinge can move a linear map off the train-deceptive bank. Same-topic honest eval moves with it. Genealogy kept frozen identity copies. It did not split strategy from topic on this 12-line set.

Do not cite 3c as reduced deception. Do not replace section 1 or 2.

## 4. Uncertainty print (slot)

`u(x)` = walk NLL; optional last-token entropy (`--entropy`). Observation uncertainty, not p(lie). No `tau(x)` yet ([math_formulation.md](math_formulation.md) §F).

Paste one `--update-steps 0 --entropy` stdout here after `git pull`. Do not edit §1–§3.

```
(paste here)
```
