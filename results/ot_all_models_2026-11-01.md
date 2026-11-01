# OT rooms on every local model (2026-11-01)

Log: `results/ot-all-models-2026-11-01.log`.
Dumps: `results/ot_*.jsonl`.
n=4 samples, tau=0.5. Keyword match on the continuation.

Not a camera. Not a term in L_total. Do not fill D.

## OT from empty (0 = entered by the note, inf = never entered)

| Walk | Topics entered | Roles entered |
| --- | ---: | ---: |
| Qwen2.5-7B-Instruct | 7/8 | 1/6 |
| Mistral-7B-Instruct-v0.3 | 6/8 | 2/6 |
| aya-expanse-8b | 2/8 | 1/6 |
| gemma-3-4b-it | 7/8 | 1/6 |
| Falcon3-7B-Instruct | 2/8 | 1/6 |
| granite-4.2-8b | 5/8 | 2/6 |
| Qwen3.5-9B | 8/8 | 2/6 |
| Llama-3.1-8B-Instruct | 7/8 | 1/6 |
| Gemma-2-2b-it | 4/8 | 0/6 |
| Gemma-2-9b-it | 6/8 | 1/6 |

The cost is binary at this sample size. A room is either entered by the note (cost 0) or never entered (cost inf). Intermediate costs do not appear. The keyword match is coarse: four samples and a single keyword do not resolve a shortest path.

## What this is not

- Not a camera. Not handoverPass. Do not fill D.
- Not a claim that the keyword match is the model's room.
- The SOM already showed the rooms are clusters in the residual stream. The OT asks whether they are high-mass sets under p_theta. At n=4 the answer is that some notes enter the room and some do not, but the cost is not resolved.
- Roles are mostly not entered. That matches the SOM finding that roles are a weak cluster on the wider bank.
