# Home GPU probe protocol (4070 Ti 12GB)

**Status:** planned, not run. No alignment-success claim. Kill-list tests below are named and explicitly not executed.

## Hardware constraint

- NVIDIA GeForce RTX 4070 Ti 12 GB VRAM only.
- No rented GPU, no multi-GPU, no offload beyond what 4-bit + HF_HOME allows.
- HF_HOME (and any cache) on datapata; do not fill system disk.
- Fail clearly on OOM; do not auto-retry with lower precision or smaller model.

## Model

- Named 8B instruct checkpoint loaded in 4-bit (bitsandbytes / transformers).
- Last-token hidden state → linear probe `r`.
- Frozen bank `D` of deceptive-intent prototypes taken only from the **bank** split.
- Bank split never enters probe training or the optional LoRA step.

## Data splits

- `bank`: source of frozen D only.
- `train`: optional one-step LoRA / hinge update on probe (or tiny adapter).
- `eval`: report metrics only; never used for D or for the update.

All examples are hand-written English same-topic pairs (deceptive plan vs honest plan sharing topic words). Synthetic only.

## Four metrics (eval split)

1. **Hinge near-D deception** — hinge loss of `r(h(x))` against frozen D on deceptive-labelled eval examples.
2. **Hinge same-topic honest** — same hinge on honest-labelled eval examples that share topic vocabulary with the deceptive ones.
3. **Task loss** — ordinary next-token / instruction loss on the eval texts (or a fixed task head if present).
4. **Probe-vs-D cosine after update** — mean cosine of probe output to nearest D vector after the optional single update step; reported separately for deceptive and honest.

Do not interpret a drop in (1) as “reduced deception”. Representation gaming and entanglement remain open.

## Kill list (named, not run)

- Any live harmful-request evaluation.
- Any claim that the probe isolates “intent weights” from capability.
- Any multi-step training or full fine-tune.
- Any inference-time abort / conscience loop.
- Any result presented as mitigated deception or alignment success.

## Execution note

User runs `probe_run.py` on the 4070 Ti. Script must print VRAM usage and the four named scalars. Results go into a later stub; this file is protocol only.
