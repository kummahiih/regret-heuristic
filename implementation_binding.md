# Implementation binding

The rest of the repo names a hinge and records how identity / mean-pool sensors fail.
This note ties that hinge to a build order. It does not add a third loss, an inference abort, or a quantum circuit.

The trained ReLU is **prototype-avoidance**. It is not Hannan and not $R=u(a^*)-u(a)$.

## The joke is the definition

Feynman's remark, in the form used here: if someone claims to understand quantum mechanics, they are lying.

A probability amplitude is bookkeeping for a route you do not measure. The observable is the squared modulus after routes have been added. The joke in a long survey that "uses amplitudes to understand attacker intent" is therefore definitional, the way a good mathematical joke is: the definition already forbids the use.

Map that ban onto this repo and it becomes an implementation rule, not a vibe.

| Amplitude talk | Here |
| --- | --- |
| Amplitude for an unobservable route | Intent cell $z_t$. The map. |
| Measurement / Born modulus | Printed walk, $h_{1:T}$, and any readout $r$. |
| Claiming to understand the amplitude | Treating $r$ or $\mathcal{L}_{\mathrm{reg}}$ as knowledge of $z$, or as $p(\mathrm{lie})$. |
| The lie the definition forbids | Putting $z$ in the loss, or reporting the hinge as understanding. |

```math
z \notin \mathrm{dom}(\mathcal{L}_{\mathrm{total}}).
```

$z$ may appear in a motion prior, in a held-out pin, in a smoother that *labels or refuses* a pin after the walk, and in prose. It may not appear as an input to $\mathcal{L}_{\mathrm{task}}$ or $\mathcal{L}_{\mathrm{reg}}$. Those take $x$, $y$, $h$, $r(h)$, and frozen $\mathcal{D}$.

Two rules, not one lemma:

- **Signature.** `LegalLoss` has no `Amp` field. `totalLoss_ignores_amp` is `rfl` once `task` and `hinge` are already numbers.
- **Dataflow (B1).** Do not compute those numbers from $z$ or `Amp` before you build the record. The type does not enforce that. The construction must.

That is how you implement "model what you cannot measure" without pretending you measured it. The survey's circuits, accuracy tables, and honeypot attraction attacks stay on the joke side of the line.

## What was missing

`math_formulation.md` defines

```math
\mathcal{L}_{\mathrm{total}}=\mathcal{L}_{\mathrm{task}}+\lambda\,\mathrm{ReLU}\big(\max_k s(r(h(x)),d_k)-\tau\big).
```

That is a *shape*. Implementation still needs six objects the toys assume:

1. A path $h_{1:T}$, not one last vector.
2. Hidden cells $z_t$ distinct from printed tokens, and kept out of the loss.
3. A sensor $r$ that is not one packed unit vector.
4. An action-indexed $A_{\mathrm{safe}}(t)$.
5. A measurement time (when the hinge is allowed to fire on $r$, never on $z$).
6. A second channel that is *not* in the training sum.

Failure probes (§2, §3c, §6) already show what happens if you skip 1–3: topic wallpaper, honest and deceptive eval move together, mean-pool mixes the hallway. That smear is evidence those cameras hug topic. It is not a proof that they "squared too soon." Premature Born is a design hypothesis about aggregation order. Path $r$ is a research choice: failing identity last-token does not ban every learned function of the last state.

## 1. Observable vs unobservable (Petri / POMDP split)

| Object | In this repo |
| --- | --- |
| Observable transition | Emitted token, tool call, or other logged event. The walk. |
| Unobservable transition | Intent cell $z_t$: stay / fork / return. The map. Not a loss input. |
| Marking | Occupancy over cells after $t$ steps. Prior / smoother only. |
| Incidence | Coarse motion prior $P(z_t\mid z_{t-1})$. No teleport between rooms. |
| Sensor | $P(r(h_t)\mid z_t)$, with declared variance $u$ (NLL / entropy / label noise). Not $p(\mathrm{lie})$. |

The language model already is a *token* motion model. The missing piece is the coarse intent motion model already named in [slam_analogy.md](slam_analogy.md).

Do not update $\mathcal{D}$ from the current walk. Pins that move with the camera are §3c.

$D$ is built offline. Coverage of the map is not a miner in this repo. Lean: `heldout_not_mem_walk_bank`. How many pins is enough stays open.

## 2. Delayed measurement (do not square early)

Classical last-token $r=I$ measures at $T$ a single packed vector. Two unobservable routes to the same printed string can smear (0.77 / 0.80). Treat that as topic hug, not as a Born experiment.

Keep a signed score over cells *before* the hinge, as bookkeeping only:

```math
\alpha_t(z)\in\mathbb{R}.
```

$\alpha$ is not trained as if it were $z$. Aggregate along the path, *then* read out the walk:

```math
h_{\mathrm{int}}=r(h_{1:T}),
\qquad
\mathcal{L}_{\mathrm{reg}}=\mathrm{ReLU}\big(\max_k s(h_{\mathrm{int}},d_k)-\tau(u)\big).
```

$\tau(u)$ wider when the chart is coarse ([intent-readout-search PROTOCOL](https://github.com/kummahiih/intent-readout-search/blob/main/PROTOCOL.md) rule 3). Quiet on mush is not honesty.

**$u$ is detached.** Calibrate it from NLL / entropy / label-flip, off the hinge graph. If $u$ receives $\partial L_{\mathrm{reg}}/\partial u = -1$ when the hinge is active, the cheap move is "I am unsure." Joint training of $u$ is out of family. Cap $\tau$ below the cosine range so $u$ cannot silence every comparison.

Training still uses the ReLU on $r$. Inference still does not abort. A posterior $P(z_{1:T}\mid h_{1:T})$ may label or refuse a pin after the answer exists. It is not a third term in $\mathcal{L}_{\mathrm{total}}$, and it is not understanding $z$.

## 3. Factored $r$, not one packed measurement

Packing topic, strategy, and uncertainty into one normalized last-token vector is measuring everything at once and calling the modulus the amplitude. Tiny-$K$ $\max\cos$ is the same geometry Kumar 2026 already pressure-tests ([neighbors.md](neighbors.md)).

Implement $r$ as *separate coordinates*:

```math
r(h)=\big(r_{\mathrm{topic}}(h),\; r_{\mathrm{strat}}(h),\; u(h)\big).
```

- $r_{\mathrm{topic}}$ is allowed to hug the hallway. It is wallpaper. Do not hinge it.
- $r_{\mathrm{strat}}$ is the only input to $\mathcal{L}_{\mathrm{reg}}$. Topic probe must fail on these vectors (LOO / hold, not same-row lstsq). Still a sensor, still not $z$.
- $u$ only widens $\tau$ and forbids pinning $\mathcal{D}$ when $u>u_0$. Stop-grad into $u$.

Sister-repo work already pointed here. Construction of $r_{\mathrm{strat}}$ stays in [intent-readout-search](https://github.com/kummahiih/intent-readout-search). Superposition packing fights a clean split. This repo consumes a vector that has passed the topic probe.

Keep at least one frozen lineage while $r_{\mathrm{strat}}$ is trained. Say what is frozen: readout weights, backbone, or cached $h$. Same-model chat grades are not that lineage.

## 4. Two factors, one target

Utility and attraction stay separate because one is the job and one is a sensor penalty. Mixing them is another way to pretend the measurement *is* the hidden route.

| Factor | Here |
| --- | --- |
| Utility | $\mathcal{L}_{\mathrm{task}}$ or $-L^{\mathrm{CLIP}}$ |
| Attraction | $\lambda\mathcal{L}_{\mathrm{reg}}$ on $r_{\mathrm{strat}}$ only |
| Collapse / measurement | Not an inference abort, and not $z$ |

Sign for PPO: subtract the hinge from a maximand ([ppo_integration.md](ppo_integration.md)). A critic of $L_{\mathrm{reg}}$ on the same backbone is not a second channel.

The only approachable box this essay may aim at remains $S_{\mathrm{safe}}$, not $S_{\mathrm{joint}}$ ([approachability.md](approachability.md)). That forces $r$ to see the *candidate action*:

```math
A_{\mathrm{safe}}(t)=\{a\in A:\ \mathcal{L}_{\mathrm{reg}}(r_{\mathrm{strat}}(h_t(a)),\mathcal{D})=0\}.
```

If $r$ only sees a pre-action $h_t$, $A_{\mathrm{safe}}$ does not depend on $a$ and is not a comparator class. If $A_{\mathrm{safe}}$ empties, the sensor did not determine the hidden cell. That is allowed. It is not a bug to "fix" by putting $z$ into the loss.

**Quiet $\neq$ known-safe.** $\max_k\cos(r,d_k)<\tau$ means the walk is **not near the pins we have**. That is *unknown / abstain*, not "this action is safe." An unseen deceptive strategy looks exactly like a safe one on this meter. Do not put $a$ in $A_{\mathrm{safe}}$ from silence alone. Log unknown. The second channel is the alarm. Do not add a third loss.

A Lagrangian weight $\lambda$ is one halfspace, not Blackwell steering.

## 5. Subnet before the hinge

Do not run $\max_k\cos$ on the whole residual stream.

Given the observable walk $x_{1:T}$:

1. List unobservable transitions that can precede or follow logged events under the motion prior.
2. Drop transitions the prior forbids after this walk (no invoice $\to$ hiking teleport).
3. Score only the surviving *sensor* vectors against frozen $\mathcal{D}$.
4. Hold out at least one map cell the walk never occupies (`simulation_heldout.py`, sister-repo action 2). Evading onto that cell is not leaving the map.

The held-out cell is how the map stays larger than the measurement. Do not train on it. §7 is a geometry cartoon. The OOD test is a new *behavior*, with $D$/$\tau$/wipe fit on the rest only.

## 6. Second channel (not in the sum)

One measurement does not reconstruct an amplitude. That is why a second channel exists.

Do not add a third training loss. Log, and refuse to pin $\mathcal{D}$ from, these monitors:

- Frozen lineage hinge (readout / backbone / cached $h$ — say which).
- Cosine to a held-out cell.
- NLL vs entropy disagreement (§4).
- Whether $A_{\mathrm{safe}}(t)$ emptied.
- Whether the walk was marked unknown ($\max\cos<\tau$).

Disagreement **requires investigation**. It is not by itself a diagnosis of gaming. A better strategy sensor can go quiet while an identity map still hugs topic. A moving backbone can change a "frozen" output. A same-model judge can go quiet because it likes its own chat.

**Same output, different $h$.** If logits stay and the hinge moves, that is coordinate gaming. Dummy: [simulation_invariance.py](simulation_invariance.py) ($h'=Ah$, $V'=VA^{-1}$). Dummy hold-label evasion: [simulation_game_detector.py](simulation_game_detector.py). Neither is Qwen. Rebuild $D$ after a basis change, or put $r$ in the same gauge as the head.

## Build order

Do these in order. Stop if the topic probe still passes on $r_{\mathrm{strat}}$. Stop if a change puts $z$ in the loss.

| Step | Where | Done means |
| --- | --- | --- |
| B0 | [intent-readout-search](https://github.com/kummahiih/intent-readout-search) | $r_{\mathrm{strat}}$ gap survives topic and paraphrase; identity control stays near zero. Official topic gate is LOO / hold on vectors, L2 on scalars. $z$ is a labeler tag, not a feature. |
| B1 | this repo, new path object | $h_{1:T}$ + stay/fork/return prior; no hinge on $h_T$ alone; signature *and* dataflow: $z$/`Amp` not upstream of `LegalLoss`. |
| B2 | this repo | $r$ consumes candidate $a$; $A_{\mathrm{safe}}(t)$ is action-indexed and sometimes empty. Silence is unknown, not safe. |
| B3 | this repo | $\tau(u)$ bins; $u$ detached; $\tau$ capped; no pin when $u>u_0$. |
| B4 | this repo | Frozen lineage + held-out cell logged every run. Disagreement is an alarm. Do not overwrite [experiment_results.md](experiment_results.md) §1–§7. |
| B5 | optional | Smoother $P(z_{1:T}\mid h_{1:T})$ labels pins only. Still not a loss input. |
| B6 | never here | Putting $z$ in $\mathcal{L}_{\mathrm{total}}$; circuits; reporting the hinge as understanding; training on same-model chat grades. |

Existing wiring stays: [simulation.py](simulation.py), [ppo_toy.py](ppo_toy.py), Lean glossary. They are not B0–B4.

## Caps this file does not lift

- No claim that $S_{\mathrm{safe}}$ is approachable for a real $r,\mathcal{D}$.
- No claim that delayed measurement or factored $r$ exists.
- No claim that anyone understands $z$. The definition says they do not.
- No inference abort. Measurement delay is about *when the hinge may fire on $r$*, not about blocking decode.
- No $D$ miner. Offline pins only. Coverage of the map stays open.
- Quiet cosine is unknown, not a safe certificate.
- Dummy `label_unchanged` is not deceptive behavior.

Version 0.1.4.
