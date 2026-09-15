# Results ledger

Separate runs. Do not collapse them. None of these is reduced deception.

## 1. CPU toy (`simulation.py`) — still the baseline

| | L_task | L_regret | L_total | L_near | L_far | \|grad W\| |
| --- | --- | --- | --- | --- | --- | --- |
| Before | 0.7310 | 0.3500 | 0.9060 | **0.7000** | **0.0000** | 0.473 |
| After 1 Adam step | 0.6759 | 0.3486 | 0.8502 | **0.6971** | **0.0000** | 0.472 |

```bash
python simulation.py
```

## 2. Single-head Qwen probe — identity r, last token

```
hinge_near_D_deceptive=0.7742 n=2
hinge_same_topic_honest=0.8003 n=2
task_loss=6.3268 n=4
```

## 3. Genealogy clusters (`--heads 8`, pool=last)

### 3c. Twenty steps + fork
Train hinge 0.7652 → 0.6951. Cluster 0 eval 0.7509 / 0.7782. Clusters 2–7 unchanged.

## 4. Uncertainty print (`--heads 1 --entropy`, pool=last)

```
hinge 0.7742 / 0.8003
nll 6.2663 / 6.3873
entropy 4.0788 / 4.0024
```

## 5. Tau-bin CPU toy (`simulation_tau_bins.py`)

near_unsure: hinge 0.70 → 0.10. Far stays 0. Quieter, not silent.

## 6. Mean-pool walk (`--pool mean`) — slot

Same jsonl, same frozen-D *rule* but D is rebuilt from mean-pooled bank texts. `--heads 1 --entropy --pool mean`. Different observation of the walk, not a new r family.

```bash
python probe_run.py --model Qwen/Qwen2.5-7B-Instruct --data data/probe_split.jsonl --heads 1 --entropy --pool mean
```

```
(paste stdout here)
```

Do not edit §1–§5.
