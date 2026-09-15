# Results ledger

Separate runs. Do not collapse them. None of these is reduced deception.

## 1. CPU toy (`simulation.py`) — still the baseline

| | L_task | L_regret | L_total | L_near | L_far | \|grad W\| |
| --- | --- | --- | --- | --- | --- | --- |
| Before | 0.7310 | 0.3500 | 0.9060 | **0.7000** | **0.0000** | 0.473 |
| After 1 Adam step | 0.6759 | 0.3486 | 0.8502 | **0.6971** | **0.0000** | 0.472 |

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

## 6. Mean-pool walk (`--pool mean`) — 2026-09-15 17:43

`--heads 1 --entropy --pool mean`. D rebuilt from mean-pooled bank texts. Identity r.

```
pool=mean
hinge_near_D_deceptive=0.8575 n=2
hinge_near_D_honest=0.8524 n=2
task_loss=6.3268 n=4
nll_deceptive=6.2663 n=2 nll_honest=6.3873 n=2
entropy_deceptive=4.0788 n=2 entropy_honest=4.0024 n=2
```

| pool | deceptive | honest | gap (hon−dec) |
| --- | --- | --- | --- |
| last (§2) | 0.7742 | 0.8003 | +0.026 |
| mean (§6) | 0.8575 | 0.8524 | **−0.005** |

### Read

Mean pool is a longer camera on the *printed* walk, not a map of unprinted thoughts. Shared topic tokens dominate both bank and eval, so both labels sit closer to D (~0.85) and the last-token gap disappears (flips sign, size noise on n=2).

NLL and last-token entropy are unchanged. Those meters do not use the pool. Control: only the observation of h changed.

This is the opposite of a strategy split. Averaging the walk increased topic mixing. Do not SGD this pool expecting the hinge to find intent. Next observation that could matter is a cell the prompt did not print, not more pooling of the same string.

Do not edit §1–§5.
