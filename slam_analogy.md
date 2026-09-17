# Path / map analogy (design filter, not a result)

Not MagSLAM on Qwen. Not a new loss. Vocabulary for what the next readout has to observe.

| SLAM | Here |
| --- | --- |
| Path | Intent trajectory: hidden states along this generation, not one last token. |
| Map | Possible thoughts that could be entered — cells that exist even if this answer never visits them. |
| Printed CoT / answer | A walk plus a biased camera. Not the map. Unfaithful CoT is a forged walk. |
| Frozen D | Pins on a map that is mostly unbuilt: cells marked do-not-occupy. |
| r | Sensor of the path. Last-token identity is a compass glued to the wallpaper (topic). |
| Token entropy / NLL | Coarse likelihood when the chart is sparse (Monty Hall 2013 style), not p(lie). |
| ATC lineages | Several sensors of the same map. Coalescence to eight copies of I is premature convergence. |

## Circling the known realm

A mapping robot that only updates, or only trusts, high-confidence cells walks the same corridor forever. Here: we are not always sure which thought is a lie. If $A_{\mathrm{safe}}$ is only the already-tagged quiet cells, $S_{\mathrm{safe}}$ plus a sharp $\tau$ keeps the walk inside the known topic neighborhood — the 0.77 / 0.80 smear.

Few remaining quiet cells is **urgency** (Kilby / $k$-regret talk), not a VRP inserter. Do not import ALNS destroy/repair. The routing 2-regret is a neighbor, not this hinge.

Uncertainty grouping (bins on entropy or NLL, wider $\tau$ when unsure) is the Monty Hall move: do not use a razor likelihood on a coarse chart. Symbols: [math_formulation.md](math_formulation.md) §F. Not $p(\mathrm{lie})$.

## Finding the path afterwards

In SLAM the pose is often reconstructed *after* the walk: a smoother, not only a filter.

- Motion / walking model: $P(z_t \mid z_{t-1})$. Intent does not jump rooms without a fork. The language model already is a token motion model; the missing piece is a **coarse intent** motion model (stay / fork / return).
- Sensor error model: $P(h_t \mid z_t)$, or $P(r(h_t)\mid z_t)$. Last-token $r=I$ is a sensor with huge bias toward topic. $u$ (NLL / entropy / label noise) is the *declared* variance of that sensor, not $p(\mathrm{lie})$.
- Smoothing: $P(z_{1:T} \mid h_{1:T})$, the path given the finished trace.

That is a different object from $L_{\mathrm{task}}+\lambda L_{\mathrm{regret}}$ during training. The hinge is a live penalty on a pin. The smoother is a **posterior over rooms after the answer exists**. Use it to *label or refuse a pin*, not as a third loss on Qwen.

It makes sense only if there is a path: several hidden states, a motion prior that forbids teleporting between invoices and hiking, and a sensor model that is not identity-on-the-last-token. One last vector has nothing to smooth.

`synthetic_z.py` action 2 is an unmapped cell. A smoother that only sees $h_T$ will miss the fork that entered it. A smoother that sees $h_{1:T}$ can put mass on that cell *after* the walk.

## What the ledger already showed

Do not rewrite [experiment_results.md](experiment_results.md).

- §1 CPU toy: constructed near vs orthogonal cells. That is a fake map with two rooms.
- §2 identity last-token: two walks through the same topic neighborhood (0.77 / 0.80).
- §3c 20-step ATC: moving the sensor moved the only visible cells with it. Honest and deceptive eval dropped together.
- §6 mean-pool of the *printed* walk: both labels closer to D (0.86 / 0.85), gap gone. More of the same hallway, not a new room.

## Useful bits to implement later (not in this note)

1. Observe a cell the prompt did not ask to print. Mean-pool of the emitted string (§6) is still the walk; it mixed topic.
2. Do not update D from the current answer.
3. Soften the hinge when entropy/NLL says the chart is coarse (§F).
4. Keep at least one frozen-I lineage so a stepped r cannot hide that the map never split.
5. If you infer intent after the fact, treat it as a smoother with an explicit motion model and an explicit sensor variance $u$. Do not call that $p(\mathrm{lie})$.

If a change still makes sense after deleting the words path and map, do not cite SLAM.
