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

## What the ledger already showed

Do not rewrite [experiment_results.md](experiment_results.md).

- §1 CPU toy: constructed near vs orthogonal cells. That is a fake map with two rooms.
- §2 identity last-token: two walks through the same topic neighborhood (0.77 / 0.80).
- §3c 20-step ATC: moving the sensor moved the only visible cells with it. Honest and deceptive eval dropped together.

## Useful bits to implement later (not in this note)

1. Observe more than the emitted walk (mean-pool, intermediate tokens, or a cell the prompt did not ask to print).
2. Do not update D from the current answer.
3. Soften the hinge when entropy/NLL says the chart is coarse.
4. Keep at least one frozen-I lineage so a stepped r cannot hide that the map never split.

If a change still makes sense after deleting the words path and map, do not cite SLAM.
