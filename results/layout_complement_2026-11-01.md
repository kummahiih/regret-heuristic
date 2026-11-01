# Complementary layout diagnostic (2026-11-01)

Ask-removal and a wider role bank on the three new instruct models.
Log: `results/layout-complement-2026-11-01.log`.
Dumps: `results/layout_complement_{llama8it,gemma2bit,gemma9bit}.json`.

Not a camera. Not a claim that SOM nodes are the model's rooms. Do not fill D.

## Topic purity: with ask vs ask removed

| Walk | With ask | Ask removed |
| --- | ---: | ---: |
| Llama-3.1-8B-Instruct | 0.958 | 0.958 |
| Gemma-2-2b-it | 1.000 | 0.875 |
| Gemma-2-9b-it | 1.000 | 0.938 |

The rooms survive the ask. Topic purity stays at the ceiling when the user question is dropped. The partition is in the note, not in the question wording. Gemma-2-2b-it drops a little (1.000 → 0.875) but stays well above the shuffle null from the first run (~0.51).

## Role purity on the wider bank

12 roles × 3 shared tasks = 36 prompts.

| Walk | Role purity |
| --- | ---: |
| Llama-3.1-8B-Instruct | 0.278 |
| Gemma-2-2b-it | 0.315 |
| Gemma-2-9b-it | 0.287 |

Chance on 12 roles is about 0.08. The wider bank is above chance but far below the thin six-role set from the first run (0.67–0.94). The first-run role purity was a small-n artifact. Roles are recoverable as a weak cluster, not as a stable room layout on this grid.

## What this is not

- Not a camera. Not handoverPass. Do not fill D.
- Not a claim that SOM nodes are the model's rooms.
- The rooms are in the residual stream. The strategy is not a cluster until the topic mean is removed. The roles are not a stable layout on the wider bank.
