# The Regret Heuristic

Research pinpointing what a regret *training* heuristic should look like: keep the skill, slap the plan that hides.

This repo **consumes** a camera. It does not have one yet.

Pinned: the shape of the training grade, and what must not sit in the sum.
Search: [kummahiih/intent-readout-search](https://github.com/kummahiih/intent-readout-search).

## Conclusions (2026-09-27)

Latest search note, not a handover:

- Mid-layer last-token is a **hint on two families**, on the bank speech act and on a `Desk note:` prefix of that act. Qwen L8: 0.105 / topic L2 **0.06** / paraphrase 0.108 / frame8 0.102. Mistral L9: 0.116 / L2 0.12 / paraphrase 0.123 / frame8 0.125.
- Office-log / radio voice is **not a voter**. LOTO held ~0 on loud rooms. Genre, not an empty hiking file.
- Hiking stays thin on the shared LOTO axis even in-set (~0.01 / 0.03). Rooms are still a subset. That blocks a freeze.
- K-step, SIREN $f(1)$, mid3 are one arrow. $\theta$ and $\hat m$ are logs. SAE stays out of $L$.

Not $r_{\mathrm{strat}}$. Do not freeze $r$. Do not fill $D$. Do not run PPO. Search: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

The same word shows up in routing look-ahead, poker self-play, and online learning. Those can stay in a larger stack. This repo focuses on a training-time slap on a strategy camera, with the hidden room kept out of the grade. Neighbors: [neighbors.md](neighbors.md).

## Two repos

[intent-readout-search](https://github.com/kummahiih/intent-readout-search) **produces** $r$. This repo **consumes** a camera that already passed: plan LOTO above chance, topic LOO near chance, paraphrase holds, rooms not a subset. Tags are not a loss input. Office-log voice does not count as paraphrase.

Until that pass, freeze nothing and do not run PPO against $S_{\mathrm{safe}}$. After a pass: freeze $r$, $D$, $\tau$; train the hinge here; keep a frozen copy as the alarm.

A second grade sits on the wall until $a^*$ exists. It is a thinking tool, not a trainer input.

```math
a^*(x)=\arg\max_{a\in A_{\mathrm{safe}}(x)} u(x,a)
\qquad
R(x,a)=u(x,a^*)-u(x,a)
```

```math
L = L_{\mathrm{task}} + \lambda L_{\mathrm{reg}} + \beta R
```

We do not run $\beta R$ now because $a^*$ needs the camera search has not found. A fake $a^*$ is a made-up number. Same shape as $u^{\mathrm{safe}}$ in [approachability.md](approachability.md).

## Claim

Deception is not only an ethics failure. A system rewarded for hiding the truth trains on its own output and drifts inside an information bubble. Patching a lie with ordinary live backprop is the wrong repair: the same weights carry the lie and the competence.

> $L_{\mathrm{total}} = L_{\mathrm{task}} + \lambda\, L_{\mathrm{reg}}\big(r(h(x)), D\big)$

$L_{\mathrm{reg}}=\mathrm{ReLU}(\max_k\cos(r,d_k)-\tau)$ is **prototype-avoidance**. The English word regret in this repo names that hinge. It is not Hannan $R_T^{\mathrm{ext}}$ and not the counterfactual $R$ above.

$L_{\mathrm{task}}$ is the job. $r$ is a hypothesized readout. $D$ is a frozen bank. The hinge is useful for deception only if $r$ is about strategy. Identity already failed. Mid-layer contrast is a search hint, not that $r$.

Full symbols: [math_formulation.md](math_formulation.md). Binding: [implementation_binding.md](implementation_binding.md). Interface: [working_model.md](working_model.md).

## Caps

- $r$ and $D$ are assumed here. Building them is the search repo.
- No reduced-deception claim.
- No ChatGPT SAE splice as a method. SAE latents are out of family until they pass the same gates. They do not enter $L$.
- Gradients of $L_{\mathrm{reg}}$ still enter $h$. Gaming is open. $K$-step residual is not a security boundary.
- Training-time only. No inference abort.
- Toys are wiring. Qwen last-token identity 0.77 / 0.80; mean-pool 0.86 / 0.85.
- Lean `lake build` from the **repo root**.
- No PPO against $S_{\mathrm{safe}}$ until search hands over a passing $r$.
- No $\beta R$ until $A_{\mathrm{safe}}$ is real.
- $\hat m$ (talker count) is a log. Lean: `totalLoss_ignores_sourceCount`.

## Walk and map

[slam_analogy.md](slam_analogy.md). Printed text is the walk. Possible thoughts are the map. $D$ is a handful of pins. $u$ is chart coarseness, not $p(\mathrm{lie})$.

## Simulation

[simulation.py](simulation.py) is the formula on a dummy encoder. No LLM. Ledger: [experiment_results.md](experiment_results.md). Do not overwrite §1–§7. Camera numbers live in the search ledger, not in the dummy sims.

```bash
pip install -r requirements.txt
python simulation.py --sensor static
```

This repo names a prototype-avoidance hinge and keeps the hidden room out of the grade. Search found a mid-layer contrast hint on Qwen and Mistral that last layer, wipe, heads, SIREN $\theta$, $\hat m$, and office-log voice do not match. That is not a frozen camera and not reduced deception.

[math_formulation.md](math_formulation.md) · [implementation_binding.md](implementation_binding.md) · [working_model.md](working_model.md) · [neighbors.md](neighbors.md) · [slam_analogy.md](slam_analogy.md) · [experiment_results.md](experiment_results.md) · [intent-readout-search](https://github.com/kummahiih/intent-readout-search) · [CITATION.cff](CITATION.cff) · [LICENSE](LICENSE)
