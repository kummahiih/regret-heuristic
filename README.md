# The Regret Heuristic

A prototype-hinge regularizer inspired by biological regret. Not a deception detector.

Whether \(r\) and \(D\) can track strategy given topic is a separate project: [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

## Claim

Deception is not only an ethics failure. A system that is rewarded for hiding the truth trains on its own output, drifts inside an information bubble, and — in a multi-agent setting — burns compute verifying peers instead of doing the work. That is the Dictator’s Trap.

Patching a lie with ordinary live backprop is the wrong repair. A deceptive plan is a trajectory of ordinary skills. Credit assignment over that trajectory is brittle; the same weights carry the lie and the competence; punishing one surface form produces a better liar.

The bookkeeping split, written as a training objective:

> **L_total = L_task + λ L_regret( r(h(x)), D )**

**L_task** is the job. **r(h(x))** is a hypothesized readout of internal state as an intent vector. **D** is a frozen bank of prototypes. **L_regret** is a hinge on cosine similarity to that bank. That is a representation penalty. It is useful for deception only if \(r\) is about strategy. Last-token and mean-pool identity already failed that test on a same-topic toy ([experiment_results.md](experiment_results.md) §2 / §6).

Full symbols: [math_formulation.md](math_formulation.md).

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

Seed 0: L_near 0.70, L_far 0. Far silent. [simulation_tau_bins.py](simulation_tau_bins.py): wider τ is quieter, not silent (0.70 → 0.10). [simulation_heldout.py](simulation_heldout.py): extra pin missed by the walk.

Ledger: [experiment_results.md](experiment_results.md). Do not overwrite §1–§7.

## Caps

- r and D are assumed here. Building them is [intent-readout-search](https://github.com/kummahiih/intent-readout-search).
- Gradients of L_regret still enter whatever produced h(x). Representation gaming is open.
- Training-time only. No inference abort.
- Toys are wiring. Qwen last-token 0.77 / 0.80; mean-pool 0.86 / 0.85; NLL vs entropy disagree; ATC 20-step dragged honest eval with the hinge.
- Lean `lake build` ok: wider τ cannot raise the hinge; silent hinge need not kill external regret.

## Theory and PPO

Hannan / Blackwell: [regret_minimization.md](regret_minimization.md), [approachability.md](approachability.md) (**S_safe**, not **S_joint**). PPO attachment is a Lagrangian, not steering. [lean/RegretHeuristic.lean](lean/RegretHeuristic.lean).

## Conclusion

This repo names a hinge shape, writes it down, and runs wiring plus a negative probe. It does not claim that regret is empirically the right loss for deception. Whether a strategy-sensitive \(r\) exists is [intent-readout-search](https://github.com/kummahiih/intent-readout-search), not this repository.

[math_formulation.md](math_formulation.md) · [slam_analogy.md](slam_analogy.md) · [experiment_results.md](experiment_results.md) · [intent-readout-search](https://github.com/kummahiih/intent-readout-search) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
