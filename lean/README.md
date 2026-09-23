# Lean 4 slice of the regret heuristic

A verified **glossary**, not a safety proof.
These lemmas are consequences of the chosen bookkeeping. They are not evidence that a network satisfying the assumptions exists.

Pinned to Lean `v4.33.1` / mathlib `v4.33.1`.

```bash
lake exe cache get
lake build
```

## Proved (bookkeeping)

- hinge non-negativity, silence below the margin, `lambda = 0` recovers the task scalar
- Cauchy-Schwarz bounds on cosine
- `relu_wider_tau_le` / `regretHinge_wider_tau_le`
- Fin 2 toy `silent_hinge_not_vanishing_external_regret`
- `insertion_two_regret_not_the_hinge`
- `hingeQuietIgnoringAction_all_or_none` / `hingeQuietOnAction_proper`
- `factoredHinge_ignores_topic`
- `trained_silent_frozenI_loud`
- `heldout_not_mem_walk_bank`
- `sjoint_unhit_one_round` / `ssafe_hit_by_quiet`
- Amplitude bookkeeping: `two_route_identity`, `totalLoss_ignores_amp`, phase/scale hides
- `decodable_not_causal`
- `implicit_miss_is_some`, `lexical_bleed`
- `static_linear_evasion_exists` if `ker W` is nontrivial. Identity is a counterexample.
- `dynamic_trajectory_convergence` **if** `step` is a basin. Residual+noise is not that hypothesis.
- `counterfactualR_of_star`: `R(a*,a*)=0`. `counterfactualR_nonneg_of_best` if `u(a)\le u(a*)`.
- `quiet_hinge_not_counterfactualR`: hinge `0` and `R=1` can sit together. Different scoreboard.

## Not proved (existence)

- `r_strat` exists on a real model
- `D` generalizes to a new behavior
- `a*` can be computed (`A_safe` needs that camera)
- residual `h+F(h)+\sigma\varepsilon` is a basin
- representation gaming is dead
- deception fell
- Hannan of the hinge, PPO trust, Blackwell steering
- anyone understands `z` / Amp
