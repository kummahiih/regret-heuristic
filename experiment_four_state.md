# 21. Four-state $T^K$ (`simulation_four_state.py`) — 2026-09-24 00:02

Constructed honest/deceptive × topic A/B. Static $r$ = coord 0 (plan). $v$ = $e_7\in\ker r$. $F$ not fit to $v$.
Lean: `iso_scales_plan`, `iso_hides_kernel`.

```
sensor plan_gap topic_on_r evasion_vis
static 2.0000 0.0000 0.0000
random_F 0.4390 -1.0081 0.6927
det_residual 1.5941 0.7175 0.3402
contractive_iso 0.2500 0.0000 0.0000
contractive_mix 0.2500 0.0000 0.2625
contractive_mix_noise 0.3524 -0.0523 0.1541
```

No row keeps plan large, topic quiet, and makes $v$ visible.
Isotropic contraction shrinks plan and still hides $v$.
Random $F$ shows $v$ and dumps topic into $r$.
Not Qwen. Not the wanted split.
