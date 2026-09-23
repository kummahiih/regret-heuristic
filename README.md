# The Regret Heuristic

Research pinpointing what a regret *training* heuristic should look like: keep the skill, slap the plan that hides.

Pinned so far: the shape of the training grade, a $K$-step readout *candidate*, and what must not sit in the sum. Measured so far: last-token and mean-pool cameras hug topic, not plan (0.77 / 0.80 and 0.86 / 0.85 on the same-topic toy). Next: a camera that sees strategy. That search is [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

The same word shows up in routing look-ahead, poker self-play, and online learning. Those can stay in a larger stack. This repo focuses on a training-time slap on a strategy camera, with the hidden room kept out of the grade. How those families sit next to this hinge: [neighbors.md](neighbors.md).

## Claim

Deception is not only an ethics failure. A system that is rewarded for hiding the truth trains on its own output, drifts inside an information bubble, and — in a multi-agent setting — burns compute verifying peers instead of doing the work. That is the Dictator’s Trap.

Patching a lie with ordinary live backprop is the wrong repair. A deceptive plan is a trajectory of ordinary skills. Credit assignment over that trajectory is brittle; the same weights carry the lie and the competence; punishing one surface form produces a better liar.

The bookkeeping split, written as a training objective:

> $L_{\mathrm{total}} = L_{\mathrm{task}} + \lambda\, L_{\mathrm{reg}}\big(r(h(x)), D\big)$

$L_{\mathrm{reg}}=\mathrm{ReLU}(\max_k\cos(r,d_k)-\tau)$ is **prototype-avoidance**. The repo still uses the English word regret for that hinge. It is not Hannan $R_T^{\mathrm{ext}}$ and not the counterfactual $R=u(x,a^*)-u(x,a)$. Those stay other scoreboards.

$L_{\mathrm{task}}$ is the job. $r(h(x))$ is a hypothesized readout. A static linear $r$ with a kernel can hide a direction; identity has no kernel. A $K$-step loop is a candidate, not a proof that gaming is dead. Residual $h+F(h)+\sigma\varepsilon$ is not the Lean contraction basin. $D$ is a frozen bank of prototypes. The hinge is useful for deception only if $r$ is about strategy. Last-token and mean-pool identity already failed that test on a same-topic toy ([experiment_results.md](experiment_results.md) §2 / §6).

Full symbols: [math_formulation.md](math_formulation.md). Neighbors: [neighbors.md](neighbors.md). Binding: [implementation_binding.md](implementation_binding.md). Interface: [working_model.md](working_model.md).

## In plain language

Imagine a hallway with two rooms behind the wallpaper.

You only see the **walk**: the words the model printed. You do not see which room it was thinking in. That hidden room is $z$. An **amplitude** is a sticky note that says “maybe room A this much, maybe room B that much.” It is not a measurement. It is a guess you are not allowed to treat as fact. Lean: `totalLoss_ignores_amp` — wave the sticky note, the grade does not change.

The grade this repo trains is a slap if the *camera on the walk* looks too much like a banned room-pin $D$. Other regrets remain possible elsewhere: hindsight vs the best fixed action, or inserting a job before its good slot vanishes. They answer different questions. We are asking how to keep the skill while tagging the camera.

Two grades, added:

1. Did the job get done? $L_{\mathrm{task}}$
2. Did the camera look like a banned pin? $L_{\mathrm{reg}}$ (prototype-avoidance)

Never put $z$ in that sum.

Two hidden routes can lead to the same printed sentence.

- **Premature camera** (last-token / mean-pool): weigh each room, then add. Routes $1$ and $-1$ both look heavy. Score $2$. That is the same-topic smear (0.77 / 0.80). Premature Born is a design hypothesis about when you square, not the measured mechanism of that smear.
- **Delayed bookkeeping**: add the sticky notes first, then look. $1+(-1)=0$. Score $0$. You still have not seen the room. You only refused to pretend you did.

Same hallway. Different time of looking. Lean: `two_route_identity`. Feynman Lectures III.1 is the same rule for an electron.

A liar can flip the sign or scale the sticky note without changing the printed walk. The official payoff $u$ only sees the camera $r$, so those moves do not change the grade. That is why “looks safe” can come apart from “is the safe move.” Gaming is not a bug in the ReLU. It is the type of the game. Lean: `same_premature_different_delayed`, `same_delayed_different_premature`.

```
hidden rooms z     ← sticky notes (Amp). Not in the loss.
      |
printed walk       ← what everyone sees
      |
camera r           ← last-token identity is glued to the wallpaper
      |
hinge vs frozen pins D
      |
L_task + λ L_reg
```

Keep the skill. Tag the camera. Leave the room untagged, because tagging it would be lying that you understood it. Quiet camera is not a win on the Hannan scoreboard: Lean has a toy where the hinge is 0 and that other regret is still $T$.

The complex numbers only let the sticky notes cancel. They are not a quantum computer.

### What the extra Lean pins pin

Scoreboard rules. Not a working camera.

- **Cheap lie vs quiet cost** (`sjoint_unhit_one_round`, `ssafe_hit_by_quiet`). Aim at $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$.
- **The camera must see the door** (`hingeQuietIgnoringAction_all_or_none`).
- **Wallpaper is not the slap** (`factoredHinge_ignores_topic`).
- **Two cameras can disagree** (`trained_silent_frozenI_loud`). Alarm, not a third loss.
- **The map is bigger than the pins** (`heldout_not_mem_walk_bank`).
- **Two grades stay two grades in group RL** (`group_zscore_mix_not_separate`).
- **Noise is not the slap** (`entropy_bonus_not_the_hinge`).
- **Hearing the subject is not catching the scheme** (`decodable_not_causal`).
- **Static linear kernel** (`static_linear_evasion_exists`). If $W$ has a kernel, some $v$ leaves $P$ unchanged. Identity is a counterexample. Residual+noise is not `conditional_contraction_in_basin`.

This *is* fine-tuning. Details: [neighbors.md](neighbors.md#attachment-when-this-is-fine-tuning).

Still open: a strategy sensor $r$, a good bank $D$, that PPO reaches the safe box, that anyone understands the hidden room.

## Walk and map

Design filter only. Not MagSLAM on Qwen. [slam_analogy.md](slam_analogy.md).

| | Meaning here |
| --- | --- |
| **Walk** | The printed thought. |
| **Map** | Possible thoughts, including cells this answer never visits. |
| **D** | A few red pins on a mostly unbuilt map. |
| **r** | A sensor of the walk. Identity last-token / mean-pool is topic wallpaper. |
| **u(x)** | Chart coarseness (NLL / entropy). Not p(lie). |

§6 mean-pool mixed the hallway. §7 constructed pin: walk on D, cosine 0 to an unprinted cell.

## Simulation

[simulation.py](simulation.py) is the formula on a dummy encoder. No LLM.

```bash
pip install -r requirements.txt
python simulation.py --sensor static
python simulation.py --sensor deterministic
python simulation.py --sensor stochastic
```

Seed 0 (static): L_near 0.70, L_far 0. Far silent on a constructed orthogonal $h$.
Seed 0 (dynamic): L_near 0.0054, L_far 0.0761. The $K$-step residual moved that dummy $h$ off the *readout's* static null. That is not a plan camera. Lean contraction does not apply to this residual unless `step` is a basin. [simulation_tau_bins.py](simulation_tau_bins.py): wider $\tau$ is quieter, not silent (0.70 → 0.10). [simulation_heldout.py](simulation_heldout.py): extra pin missed by the walk.

Bookkeeping toys: [simulation_two_door.py](simulation_two_door.py), [simulation_factored.py](simulation_factored.py), [simulation_two_channel.py](simulation_two_channel.py), [simulation_born.py](simulation_born.py), [simulation_decodable.py](simulation_decodable.py), [simulation_head_write.py](simulation_head_write.py), [simulation_flattening.py](simulation_flattening.py) (optimizer vs frozen dynamic detector).

Ledger: [experiment_results.md](experiment_results.md). Do not overwrite §1–§7.

## Caps

- $r$ and $D$ are assumed here. Building them is [intent-readout-search](https://github.com/kummahiih/intent-readout-search).
- Gradients of $L_{\mathrm{reg}}$ still enter $h$. Gaming is open. $K$-step residual is not a proof the null collapsed.
- Training-time only. No inference abort.
- Toys are wiring. Qwen last-token 0.77 / 0.80; mean-pool 0.86 / 0.85.
- Lean `lake build` from the **repo root**.
- This loss is prototype-avoidance: [neighbors.md](neighbors.md).
- Implementation binding does not lift these caps.

## Theory and PPO

Hannan / Blackwell: [regret_minimization.md](regret_minimization.md), [approachability.md](approachability.md) ($S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$). PPO attachment is a Lagrangian, not steering. Lean sources in `lean/`. Build order: [implementation_binding.md](implementation_binding.md). Interface: [working_model.md](working_model.md).

## Conclusion

This repo names a prototype-avoidance hinge, writes it down, and runs wiring plus a negative probe. It does not claim reduced deception. Whether a strategy-sensitive $r$ exists is [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

[math_formulation.md](math_formulation.md) · [implementation_binding.md](implementation_binding.md) · [working_model.md](working_model.md) · [neighbors.md](neighbors.md) · [slam_analogy.md](slam_analogy.md) · [experiment_results.md](experiment_results.md) · [intent-readout-search](https://github.com/kummahiih/intent-readout-search) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
