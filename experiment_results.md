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

Readout = last-token hidden. tau=0 so hinge = cosine.

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

### 3a. Zero update
Eight identity copies of §2 (0.7742 / 0.8003).

### 3b. One step + fork
`hinge_train=0.7652`. Cluster 0: 0.7732 / 0.7994. Clusters 2–7: 0.7742 / 0.8003.

### 3c. Twenty steps + fork
Train hinge 0.7652 → 0.6951. Cluster 0 eval 0.7509 / 0.7782. Clusters 2–7 unchanged.

Do not cite 3c as reduced deception. Do not replace section 1 or 2.

## 4. Uncertainty print

### 4a. `--heads 8 --entropy`, no update
Eight identical lines (same as 4b).

### 4b. `--heads 1 --entropy`, no update (2026-09-15 17:31)

venv: `/media/pauli/datapata/rh-venv`. System `python` missing until activate.

```
N=1 parents=[-1] cluster_id=[0]
hinge_near_D_deceptive=0.7742 n=2 hinge_near_D_honest=0.8003 n=2
task_loss=6.3268 n=4
nll_deceptive=6.2663 n=2 nll_honest=6.3873 n=2
probe_vs_D_cosine_deceptive=0.7742 n=2 probe_vs_D_cosine_honest=0.8003 n=2
entropy_deceptive=4.0788 n=2 entropy_honest=4.0024 n=2
```

Same smear as §2. Honest: higher walk NLL, lower last-token entropy. Meters disagree. Not a §F bin.

## 5. Tau-bin CPU toy (`simulation_tau_bins.py`)

Separate file. Does not replace simulation.py. Fake u(x) on seed-0 near/far geometry.

```bash
python simulation_tau_bins.py
```

```
(paste stdout here)
```
