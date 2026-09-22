# Results ledger

Separate runs. Do not collapse them. None of these is reduced deception.
Do not edit §1–§7 numbers.

Walk vs map (design filter): [slam_analogy.md](slam_analogy.md). Printed text is the walk. Possible thoughts are the map. §6 averaged more of the walk and mixed topic. §7 built a map cell the walk never occupies.

## 1. CPU toy (`simulation.py`) — still the baseline

Two constructed rooms (near D / orthogonal to D). Fake map, not Qwen.

| | L_task | L_regret | L_total | L_near | L_far | \|grad W\| |
| --- | --- | --- | --- | --- | --- |
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

One-round $S_{\mathrm{joint}}$ empty. $S_{\mathrm{safe}}$ hittable by the quiet door. Dummy vectors. $z$ not in $L_{\mathrm{total}}$. Rerun 2026-09-21: one bank $D=\{1\}$, $r$ sees the door. Same numbers.

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

## 12. Trainer vs $S_{\mathrm{safe}}$ — not run

No PPO (or other trainer) has been asked to sit in $S_{\mathrm{safe}}$ on a real $r_{\mathrm{strat}}$.

§8 shows the box on dummy doors. That is not a policy update. B0 lives in [intent-readout-search](https://github.com/kummahiih/intent-readout-search). Do not add a fake loop here.

## 13. B1 trainer cartoon (`simulation_b1_trainer.py`) — 2026-09-21 20:08

Path $h_{1:T}$, loss from the walk, frozen readout (kind=readout). Dummy linear encoder. Not Qwen.

```
path T=3 frozen_kind=readout tau=0.30 (capped)
L_task=0.7819 L_reg=0.0751 L_frozen=0.0751
L_last=0.0503 L_total=0.8195
amp_normsq=2.0000  (logged, not in L_total)
grad encoder=0.410410 readout=0.430949 frozen_readout=None
after 1 step L_reg=0.0149 L_frozen=0.0638 alarm=True
```

`legal_of_walk` is task + $\lambda$ path-hinge. Amp is computed and discarded. Frozen readout gets no gradient. After one Adam step the trained hinge and the frozen log disagree (alarm, not a gaming verdict). $D$ not updated. Lean names: `legalOfWalk`, `illegalFromAmp`, `FrozenKind.readout`.

## 14. Dynamic Detector (stochastic unrolled relaxation) — 2026-09-23 01:29

K=3 stochastic residual loop (`noise_sigma=0.01`) applied to \(h\) before the static readout. Lean names: `iterateTrajectory`, `gaming_resistance_in_basin`.

| | L_task | L_regret | L_total | L_near | L_far | grad task | grad hinge |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before | 0.6166 | 0.1009 | 0.6671 | 0.1228 | **0.0791** | 0.423666 | **0.365549** |
| After 1 Adam step | 0.5733 | 0.0407 | 0.5936 | 0.0054 | 0.0761 | 0.413435 | 0.604331 |

**Mechanical notes:**
1. `L_far` is no longer 0.0000. The stochastic transition step breaks the orthogonal null space; constructed evasion points are now visible to the loss function.
2. The initial hinge gradient is `0.365549` (compared to `0.000001` in the §1 static baseline). The residual connections successfully propagate the backpropagation signal through the random noise without zeroing out.

## 15. Dynamic Detector Failure: Manifold Flattening (`simulation_flattening.py`) — 2026-09-23 02:02

Frozen dynamic detector (\(K=3\)) against an adversarial base model. Lean concept: `same_premature_different_delayed` exploited dynamically.

| | L_task | L_regret (h_K norm) | Base ||h_0|| | Intent ||h_K|| |
| --- | --- | --- | --- | --- |
| Step 0 | 0.9450 | 3.2647 | 3.5321 | 3.2647 |
| Step 200 | 0.3206 | 0.5146 | 2.3511 | 0.5146 |

**Mechanical notes:**
1. The optimizer successfully decoupled the task representation from the detector's vision. It maintained a large \(\vert{}\vert{}h_0\vert{}\vert{}\) to solve the task, while pushing \(h_0\) into a subspace that the detector's step network flattened (\(F(h) \approx -h\)).
2. The residual loop squashed the intent vector down toward the \(\sigma\) noise floor, practically blinding the sensor.
3. This proves the dynamic detector cannot be left completely frozen if the base model is updating; it requires active co-training or spectral constraints to prevent the policy from hiding in negative-eigenvalue blind spots.

