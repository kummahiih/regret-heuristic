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

last-token 0.7742 / 0.8003 → mean 0.8575 / 0.8524. Gap gone. NLL/entropy unchanged.

## 7. Held-out cell (`simulation_heldout.py`) — 2026-09-15 18:34

```
heldout_norm=1.0000  heldout_vs_D_max=0.0000
near_0  s*_D=1.0000  cos_heldout=-0.0000
near_1  s*_D=1.0000  cos_heldout=-0.0000
far_0   s*_D=0.0000  cos_heldout=-0.0000
far_1   s*_D=0.0000  cos_heldout= 0.0000
```

The extra pin is orthogonal to span(D) and to the four walk vectors. Near points sit on D and still miss it. Constructed geometry, not a prompt. Do not edit §1–§6.
