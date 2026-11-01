# Purity-law diagnostic (2026-11-01)

Log: `results/purity-probe-2026-11-01.log`.
Diagnostic: `night_sims/purity_probe.py`.
Source: Hai and Li, arXiv:2609.22337.

Not a camera. Not handoverPass. Do not fill D.

## Results at alpha=1.0

| Walk | s | AUC pred | alpha* | Underpowered |
| --- | ---: | ---: | ---: | --- |
| Qwen | 2.04 | 0.846 | 0.258 | no |
| Mistral | 2.73 | 0.914 | 0.192 | no |
| Llama-3.1-8B-Instruct | 2.29 | 0.873 | 0.229 | no |
| Gemma-2-2b-it | 3.11 | 0.940 | 0.186 | no |
| Gemma-2-9b-it | 2.86 | 0.923 | 0.190 | no |

At full purity the audit is powered on every walk. The detectability threshold sits between 0.19 and 0.26. A null result at alpha below that threshold would be uninformative. A null result at alpha=1.0 is informative.

The predicted AUC is the purity-law ceiling, not a measured probe accuracy. The measured combination probe sits near or below that ceiling on every walk. The gap is not large. The mid-layer note direction does not carry the win.

Not a camera. Not handoverPass. Do not fill D.
