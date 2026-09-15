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

```
hinge_near_D_deceptive=0.7742 n=2
hinge_same_topic_honest=0.8003 n=2
task_loss=6.3268 n=4
```

Honest eval is slightly closer to the deceptive bank. Topic overlap on n=2.

## 3. Genealogy clusters (`probe_run.py --heads 8`)

### 3a. Zero update
Eight identity copies of §2 (0.7742 / 0.8003).

### 3b. One step + fork
`hinge_train=0.7652`. Cluster 0: 0.7732 / 0.7994. Clusters 2–7: 0.7742 / 0.8003.

### 3c. Twenty steps + fork
Train hinge 0.7652 → 0.6951. Cluster 0 eval 0.7509 / 0.7782. Clusters 2–7 unchanged.

Do not cite 3c as reduced deception. Do not replace section 1 or 2.

## 4. Uncertainty print

### 4b. `--heads 1 --entropy`, no update (2026-09-15 17:31)

```
hinge 0.7742 / 0.8003
nll 6.2663 / 6.3873
entropy 4.0788 / 4.0024
```

Honest: higher walk NLL, lower last-token entropy. Meters disagree. Not a §F bin.

## 5. Tau-bin CPU toy (`simulation_tau_bins.py`) — 2026-09-15 17:35

Same seed-0 geometry as §1. Fake u, not model entropy. tau_sure=0.3, tau_unsure=0.9, u0=0.5.

`s*` = 1.0 on both nears, 0.0 on both fars (constructed).

| name | u | tau | s* | hinge flat @0.3 | hinge binned |
| --- | --- | --- | --- | --- | --- |
| near_sure | 0.10 | 0.3 | 1.0 | 0.70 | **0.70** |
| near_unsure | 0.80 | 0.9 | 1.0 | 0.70 | **0.10** |
| far_unsure_a | 0.90 | 0.9 | 0.0 | 0.00 | 0.00 |
| far_unsure_b | 0.70 | 0.9 | 0.0 | 0.00 | 0.00 |

Mean hinge 0.3500 → 0.2000. Far stays silent. Near tagged unsure is quieter (0.70 → 0.10), not off. Coarser likelihood, not a lie detector. Does not replace §1.
