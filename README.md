# The Regret Heuristic

Research pinpointing what a regret *training* heuristic should look like: keep the skill, slap the plan that hides.

Pinned so far: the shape of the training grade, and what must not sit in it. Failed so far: reading the last printed token as if it were the plan (same-topic 0.77 / 0.80; mean-pool 0.86 / 0.85). Still missing: a camera that sees strategy rather than topic. That search is [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

The word *regret* is crowded. Routing solvers, poker AIs, and online-learning textbooks use it for other scoreboards. This repo is none of those. Map of near-misses: [neighbors.md](neighbors.md).

## Claim

Deception is not only an ethics failure. A system that is rewarded for hiding the truth trains on its own output, drifts inside an information bubble, and — in a multi-agent setting — burns compute verifying peers instead of doing the work. That is the Dictator’s Trap.

Patching a lie with ordinary live backprop is the wrong repair. A deceptive plan is a trajectory of ordinary skills. Credit assignment over that trajectory is brittle; the same weights carry the lie and the competence; punishing one surface form produces a better liar.

The bookkeeping split, written as a training objective:

> $L_{\mathrm{total}} = L_{\mathrm{task}} + \lambda\, L_{\mathrm{regret}}\big(r(h(x)), D\big)$

$L_{\mathrm{task}}$ is the job. $r(h(x))$ is a hypothesized readout of internal state as an intent vector. $D$ is a frozen bank of prototypes. $L_{\mathrm{regret}}$ is a hinge on cosine similarity to that bank. That is a representation penalty. It is useful for deception only if $r$ is about strategy. Last-token and mean-pool identity already failed that test on a same-topic toy ([experiment_results.md](experiment_results.md) §2 / §6).

Full symbols: [math_formulation.md](math_formulation.md). Neighbors (probes, steering, SAE, concept erasure, insertion regret, Hannan, Blackwell, Feynman III.1): [neighbors.md](neighbors.md). How to attach the missing objects without pretending the toys already have them: [implementation_binding.md](implementation_binding.md). What is in-family for a working model: [working_model.md](working_model.md).

## In plain language

Imagine a hallway with two rooms behind the wallpaper.

You only see the **walk**: the words the model printed. You do not see which room it was thinking in. That hidden room is $z$. An **amplitude** is a sticky note that says “maybe room A this much, maybe room B that much.” It is not a measurement. It is a guess you are not allowed to treat as fact. Lean: `totalLoss_ignores_amp` — wave the sticky note, the grade does not change.

Regret here is not “I wish I had played chess better.” That other regret is Hannan / external regret, a different scoreboard. This regret is a slap on the wrist if the *camera on the walk* looks too much like a banned room-pin $D$. It is also not “insert this customer before the good slot vanishes.”

Two grades, added:

1. Did the job get done? $L_{\mathrm{task}}$
2. Did the camera look like a banned pin? $L_{\mathrm{regret}}$

Never put $z$ in that sum.

Two hidden routes can lead to the same printed sentence.

- **Premature camera** (last-token / mean-pool): weigh each room, then add. Routes $1$ and $-1$ both look heavy. Score $2$. That is the same-topic smear (0.77 / 0.80).
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
L_task + λ L_regret
```

Keep the skill. Tag the camera. Leave the room untagged, because tagging it would be lying that you understood it. Quiet camera is not a win on the Hannan scoreboard: Lean has a toy where the hinge is 0 and that other regret is still $T$.

The complex numbers only let the sticky notes cancel. They are not a quantum computer.

### What the extra Lean pins pin

Scoreboard rules. Not a working camera.

- **Cheap lie vs quiet cost** (`sjoint_unhit_one_round`, `ssafe_hit_by_quiet`). The cheap door looks banned. The clean door costs extra. You cannot be cheapest-in-the-world *and* look clean in one round. You *can* be as cheap as the best clean door. Aim at $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$.
- **The camera must see the door** (`hingeQuietIgnoringAction_all_or_none`, `hingeQuietOnAction_proper`). If $r$ ignores which door you took, “safe doors” is everybody or nobody. If $r$ sees the door, the safe set can be a real subset: one quiet, one loud.
- **Wallpaper is not the slap** (`factoredHinge_ignores_topic`). Topic can hug the hallway. The hinge only looks at the strategy coordinate. Rewriting topic is `rfl`.
- **Two cameras can disagree** (`trained_silent_frozenI_loud`). The trained hinge can go quiet while a frozen copy still shouts. Log the second channel. Do not dump it into the training sum. Quiet trained camera is not a win.
- **The map is bigger than the pins** (`heldout_not_mem_walk_bank`). The walk can sit on pin $1$ while cell $-1$ is still on the map and not in $D$. Leaving the red pins is not leaving the building.

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
python simulation.py
```

Seed 0: L_near 0.70, L_far 0. Far silent. [simulation_tau_bins.py](simulation_tau_bins.py): wider $\tau$ is quieter, not silent (0.70 → 0.10). [simulation_heldout.py](simulation_heldout.py): extra pin missed by the walk.

Bookkeeping toys, same dummy class: [simulation_two_door.py](simulation_two_door.py) ($S_{\mathrm{joint}}$ empty / $S_{\mathrm{safe}}$ hittable), [simulation_factored.py](simulation_factored.py) (hinge ignores topic), [simulation_two_channel.py](simulation_two_channel.py) (trained quiet, frozen-$I$ loud), [simulation_born.py](simulation_born.py) (premature 2 / delayed 0; Amp unused).

Ledger: [experiment_results.md](experiment_results.md). Do not overwrite §1–§7.

## Caps

- $r$ and $D$ are assumed here. Building them is [intent-readout-search](https://github.com/kummahiih/intent-readout-search).
- Gradients of $L_{\mathrm{regret}}$ still enter whatever produced $h(x)$. Representation gaming is open.
- Training-time only. No inference abort.
- Toys are wiring. Qwen last-token 0.77 / 0.80; mean-pool 0.86 / 0.85; NLL vs entropy disagree; ATC 20-step dragged honest eval with the hinge.
- Lean `lake build` ok: wider $\tau$ cannot raise the hinge; silent hinge need not kill external regret; Amp is not a loss field; phase and scale moves can hide from one Born scoreboard and not the other; $S_{\mathrm{joint}}$ can be empty in one round while $S_{\mathrm{safe}}$ is hittable; $A_{\mathrm{safe}}$ is all-or-none if $r$ ignores $a$; topic wallpaper is not in the hinge; two channels can disagree; a held-out cell need not sit on $D$.
- Detection / steering / SAE / LEACE / ALNS / CFR are neighbors, not this loss: [neighbors.md](neighbors.md). Tiny-$K$ max-cosine is the single-direction geometry those probe papers already pressure-test.
- Implementation binding does not lift these caps. It only names the path object, the factored sensor, action-indexed $A_{\mathrm{safe}}$, and a second channel that is not in the training sum.

## Theory and PPO

Hannan / Blackwell: [regret_minimization.md](regret_minimization.md), [approachability.md](approachability.md) ($S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$). PPO attachment is a Lagrangian, not steering. [lean/RegretHeuristic.lean](lean/RegretHeuristic.lean), [lean/AmplitudeBookkeeping.lean](lean/AmplitudeBookkeeping.lean). Build order: [implementation_binding.md](implementation_binding.md). In-family characteristics: [working_model.md](working_model.md).

## Conclusion

This repo names a hinge shape, writes it down, and runs wiring plus a negative probe. It does not claim that regret is empirically the right loss for deception. Whether a strategy-sensitive $r$ exists is [intent-readout-search](https://github.com/kummahiih/intent-readout-search), not this repository.

[math_formulation.md](math_formulation.md) · [implementation_binding.md](implementation_binding.md) · [working_model.md](working_model.md) · [neighbors.md](neighbors.md) · [slam_analogy.md](slam_analogy.md) · [experiment_results.md](experiment_results.md) · [intent-readout-search](https://github.com/kummahiih/intent-readout-search) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
