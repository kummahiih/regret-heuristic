# Results ledger

Separate runs. Do not collapse them. None of these is reduced deception.
Do not edit §1–§7 numbers.

Walk vs map (design filter): [slam_analogy.md](slam_analogy.md). Printed text is the walk. Possible thoughts are the map. §6 averaged more of the walk and mixed topic. §7 built a map cell the walk never occupies.

## 1. CPU toy (`simulation.py`) — still the baseline

Two constructed rooms (near D / orthogonal to D). Fake map, not Qwen.

| | L_task | L_regret | L_total | L_near | L_far | \|grad W\| |
| --- | --- | --- | --- | --- | --- | --- |
| Before | 0.7310 | 0.3500 | 0.9060 | **0.7000** | **0.0000** | 0.473 |
| After 1 Adam step | 0.6759 | 0.3486 | 0.8502 | **0.6971** | **0.0000** | 0.472 |

## 2. Single-head Qwen probe — identity r, last token

Last-token camera on the printed walk. Same-topic smear.

```
hinge_near_D_deceptive=0.7742 n=2
hinge_same_topic_honest=0.8003 n=2
task_loss=6.3268 n=4
```

## 3. Genealogy clusters (`--heads 8`, pool=last)

Several sensors of the same walk. Coalescence to copies of I.

### 3a. Zero update
Eight identity copies of §2 (0.7742 / 0.8003).

### 3b. One step + fork
`hinge_train=0.7652`. Cluster 0: 0.7732 / 0.7994. Clusters 2–7: 0.7742 / 0.8003.

### 3c. Twenty steps + fork
Train hinge 0.7652 → 0.6951. Cluster 0 eval 0.7509 / 0.7782. Clusters 2–7 unchanged. Moving the sensor moved the wallpaper with it.

## 4. Uncertainty print (`--heads 1 --entropy`, pool=last)

How coarse the chart looks. Not p(lie). Two meters disagree.

```
hinge 0.7742 / 0.8003
nll 6.2663 / 6.3873
entropy 4.0788 / 4.0024
```

## 5. Tau-bin CPU toy (`simulation_tau_bins.py`)

Wider τ on a coarse cell: quieter, not silent (0.70 → 0.10). Lean: `relu_wider_tau_le` (`lake build` ok).

## 6. Mean-pool walk (`--pool mean`) — 2026-09-15 17:43

Longer camera on the *printed* walk, not an unprinted cell.

last-token 0.7742 / 0.8003 → mean 0.8575 / 0.8524. Gap gone. NLL/entropy unchanged. Topic mixed.

## 7. Held-out cell (`simulation_heldout.py`) — 2026-09-15 18:34

A map pin the walk never occupies.

```
heldout_norm=1.0000  heldout_vs_D_max=0.0000
near_0  s*_D=1.0000  cos_heldout=-0.0000
near_1  s*_D=1.0000  cos_heldout=-0.0000
far_0   s*_D=0.0000  cos_heldout=-0.0000
far_1   s*_D=0.0000  cos_heldout= 0.0000
```

Near sits on D and misses the pin. Constructed geometry, not a prompt.

## 8. Two-door payoff (`simulation_two_door.py`) — 2026-09-19 22:03

Cheap door is loud. Quiet door costs extra. Lean: `sjoint_unhit_one_round`, `ssafe_hit_by_quiet`.

```
task[0]=1.0000  task[1]=0.0000
L_reg[0]=0.0000  L_reg[1]=1.0000
u_joint[0]=(1.0, 0.0)  both<=0=False
u_joint[1]=(0.0, 1.0)  both<=0=False
u_safe play 0=(0.0, 0.0)  both<=0=True
```

One-round $S_{\mathrm{joint}}$ empty. $S_{\mathrm{safe}}$ hittable by the quiet door. Dummy vectors. $z$ not in $L_{\mathrm{total}}$.

## 9. Factored readout (`simulation_factored.py`) — 2026-09-19 22:05

Hinge looks at strat only. Lean: `factoredHinge_ignores_topic`.

```
L_reg on strat before topic rewrite=1.0000
L_reg on strat after topic rewrite=1.0000
packed-vector L2 change if topic were mixed in=0.9852
```

Wallpaper rewrite is a no-op on $L_{\mathrm{reg}}$. Packing topic into the same vector would have moved. Dummy vectors. $z$ not in $L_{\mathrm{total}}$.

## 10. Two-channel witness (`simulation_two_channel.py`) — 2026-09-19 22:08

Trained hinge quiet after a constructed 90° rotate. Frozen-$I$ still 1. Lean: `trained_silent_frozenI_loud`. SGD on identity did not leave the cosine pin.

```
before  trained=1.0000  frozen-I=1.0000  L_total=1.0000
after   trained=0.0000  frozen-I=1.0000  L_total=0.0000
```

$L_{\mathrm{total}}$ uses the trained hinge only. Frozen-$I$ is a log. Dummy vectors. $z$ not in $L_{\mathrm{total}}$.

## 11. Born bookkeeping (`simulation_born.py`) — 2026-09-19 22:10

Routes $(1,-1)$. Lean: `two_route_identity`, `totalLoss_ignores_amp`.

```
premature square-then-add=2.0000
delayed add-then-square=0.0000
L_total without Amp=1.0000
L_total with unused Amp note=1.0000
```

Same hallway. Different time of looking. Pairing the sticky note does not change $L_{\mathrm{total}}$. Dummy scalars. Not a circuit.
