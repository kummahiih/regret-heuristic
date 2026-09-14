# Home probe results (stub)

**Status:** one wiring run on a 12-line toy set. Not reduced deception. Not an LLM alignment result.

## Machine

- GPU: RTX 4070 Ti 12 GB
- Model: `Qwen/Qwen2.5-7B-Instruct` 4-bit NF4 (Llama 3.1 8B Instruct was gated / awaiting review)
- `r`: linear map init to identity (so readout = last-token hidden)
- `D`: 2 bank-deceptive last-token vectors, frozen
- tau = 0 (hinge = max(cos, 0))
- `--update-steps 0`
- Data: `data/probe_split.jsonl` eval n=4 (2 deceptive, 2 honest)

## Numbers (2026-09-15)

```
VRAM allocated_GiB=5.18 reserved_GiB=5.33
Frozen D shape=(2, 3584)
hinge_near_D_deceptive=0.7742 n=2
hinge_same_topic_honest=0.8003 n=2
task_loss=6.3268 n=4
probe_vs_D_cosine_deceptive=0.7742 n=2
probe_vs_D_cosine_honest=0.8003 n=2
```

Hinge equals cosine here because tau=0 and both means are positive.

## Read

Same-topic honest eval is slightly *closer* to the deceptive bank than deceptive eval. Last-token geometry on this set does not tag strategy vs topic. That is entanglement at n=2, not a method verdict.

Do not cite these four numbers as evidence that the hinge works or fails on a language model.
