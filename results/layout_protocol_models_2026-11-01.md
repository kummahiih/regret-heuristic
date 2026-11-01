# Layout diagnostic on the original protocol models (2026-11-01)

Log: `results/layout-protocol-models-2026-11-01.log`.
Local weights. No download. Phi-4-mini-instruct failed to load (dynamic module import). The rest finished.

Not a camera. Not a claim that SOM nodes are the model's rooms. Do not fill D.

## Topic purity and strategy after topic-mean removal

| Walk | Topic purity | Strategy purity | Strategy after topic-mean | Null purity |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-7B-Instruct | 0.92 | 0.50 | 1.00 | 0.52 |
| Mistral-7B-Instruct-v0.3 | 0.83 | 0.50 | 1.00 | 0.48 |
| aya-expanse-8b | 0.92 | 0.50 | 1.00 | 0.53 |
| gemma-3-4b-it | 1.00 | 0.50 | 1.00 | 0.54 |
| Falcon3-7B-Instruct | 0.92 | 0.50 | 1.00 | 0.51 |
| granite-4.2-8b | 0.92 | 0.54 | 1.00 | 0.51 |
| Qwen3.5-9B | 0.92 | 0.50 | 1.00 | 0.51 |

Same shape as the new models. Topic purity sits at the ceiling, well above the shuffle null. Strategy purity sits at chance until the topic mean is subtracted, then it jumps to 1.0.

## Ask-removal and wider roles

| Walk | With ask | Ask removed | Role (12×3) |
| --- | ---: | ---: | ---: |
| Qwen2.5-7B-Instruct | 0.917 | 1.000 | 0.278 |
| Mistral-7B-Instruct-v0.3 | 0.833 | 0.917 | 0.287 |
| aya-expanse-8b | 0.958 | 0.875 | 0.333 |
| gemma-3-4b-it | 1.000 | 1.000 | 0.287 |
| Falcon3-7B-Instruct | 0.917 | 0.917 | 0.315 |
| granite-4.2-8b | 0.917 | 0.917 | 0.296 |
| Qwen3.5-9B | 0.917 | 0.958 | 0.306 |

The rooms survive the ask. Role purity on the wider bank stays near 0.3, above chance (~0.08) but not a stable layout.

## What this is not

- Not a camera. Not handoverPass. Do not fill D.
- Not a claim that SOM nodes are the model's rooms.
- Phi-4-mini-instruct is the known dynamic-module miss. Not a layout result.
