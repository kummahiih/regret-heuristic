# Lean 4 slice of the regret heuristic

A verified **glossary**, not a safety proof.

Pinned to Lean `v4.33.1` / mathlib `v4.33.1`.

```bash
lake exe cache get
lake build
```

What is proved:

- hinge non-negativity, silence below the margin, `lambda = 0` recovers the task scalar
- Cauchy-Schwarz bounds on cosine
- `relu_wider_tau_le` / `regretHinge_wider_tau_le`
- Fin 2 toy `silent_hinge_not_vanishing_external_regret`
- `insertion_two_regret_not_the_hinge`: Potvin-style second-minus-best can be 3 while the cosine hinge is 0
- `hingeQuietIgnoringAction_all_or_none`: if $r$ ignores the door, “safe doors” is everybody or nobody
- `hingeQuietOnAction_proper`: if $r$ sees the door, $A_{\mathrm{safe}}$ can be one quiet door, not the whole hallway
- `factoredHinge_ignores_topic`: wallpaper (topic) is not the slap; rewriting it is `rfl`
- `trained_silent_frozenI_loud`: trained camera can go quiet while a frozen copy still shouts; not a net-gaming claim
- `heldout_not_mem_walk_bank`: walk can sit on pin $1$ while cell $-1$ is still on the map and not in $D$
- `sjoint_unhit_one_round`: cheap door looks banned and clean door costs extra, so one-round $S_{\mathrm{joint}}$ is empty; `ssafe_hit_by_quiet` hits $S_{\mathrm{safe}}$ by taking the quiet door
- `AmplitudeBookkeeping.two_route_identity`: add-then-square is 0 on `(1,-1)`, square-then-add is 2
- `AmplitudeBookkeeping.totalLoss_ignores_amp`: wave the sticky note, the grade does not change
- `same_premature_different_delayed`: Player II phase move is invisible to square-then-add
- `same_delayed_different_premature`: Player II scale move is invisible to add-then-square

What is not proved: readout validity, bank coverage, representation gaming, Hannan of the hinge, PPO trust region, Blackwell, ALNS, that $r$ recovers $z$, that anyone understands an amplitude.
