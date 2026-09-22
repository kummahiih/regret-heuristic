import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Tactic

set_option linter.unusedSectionVars false

/-!
# Dynamic Intent Relaxation and Representation Gaming Resistance

Formalization of the dynamic latent intent detector for the Regret Heuristic:
`L_total = L_task + lambda * L_regret(r_K(h), D)`

We formalize:
1. The static linear probe failure mode (Representation Gaming via kernel evasion).
2. The iterative relaxation dynamical system (discrete-time attractor process).
3. The Basin Robustness Theorem: an energy-based attractor basin prevents
   isolated orthogonal evasion vectors from blinding the sensor.
-/

open Real InnerProductSpace Metric

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
variable {Z : Type*} [NormedAddCommGroup Z] [InnerProductSpace ℝ Z]

namespace RegretHeuristic

/-! ## 1. Static Probe & The Linear Representation Gaming Lemma -/

structure StaticProbe (H Z : Type*) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    [NormedAddCommGroup Z] [InnerProductSpace ℝ Z] where
  W : H →L[ℝ] Z
  b : Z

def StaticProbe.eval (P : StaticProbe H Z) (h : H) : Z :=
  P.W h + P.b

/--
Representation Gaming in the static case:
If the probe's kernel is nontrivial, there exists an evasion vector `v ≠ 0`
such that the policy can alter its representation `h + v` without changing the probe output.
-/
theorem static_linear_evasion_exists (P : StaticProbe H Z)
    (h_ker : ∃ v : H, v ∈ LinearMap.ker (P.W : H →ₗ[ℝ] Z) ∧ v ≠ 0) (h : H) :
    ∃ v : H, v ≠ 0 ∧ P.eval (h + v) = P.eval h := by
  rcases h_ker with ⟨v, hv_mem, hv_ne⟩
  use v
  refine ⟨hv_ne, ?_⟩
  have hv_zero : P.W v = 0 := LinearMap.mem_ker.mp hv_mem
  calc P.eval (h + v)
    _ = P.W (h + v) + P.b := rfl
    _ = P.W h + P.W v + P.b := by rw [ContinuousLinearMap.map_add]
    _ = P.W h + 0 + P.b := by rw [hv_zero]
    _ = P.W h + P.b := by rw [add_zero]
    _ = P.eval h := rfl

/-! ## 2. Dynamic Relaxation Process (Iterative Settling) -/

/--
A dynamic relaxation detector is governed by:
- `step`: A transition map (e.g., gradient step on an energy landscape + damping).
- `K`: Number of unrolled steps.
- `readout`: Final projection from the stabilized latent space H to intent space Z.
-/
structure DynamicDetector (H Z : Type*) [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    [NormedAddCommGroup Z] [InnerProductSpace ℝ Z] where
  step : H → H
  K : ℕ
  readout : H → Z

/-- Unrolling the dynamical system for `k` steps starting from `h₀`. -/
def iterateTrajectory (step : H → H) (h₀ : H) : ℕ → H
  | 0 => h₀
  | k + 1 => step (iterateTrajectory step h₀ k)

def DynamicDetector.eval (D : DynamicDetector H Z) (h₀ : H) : Z :=
  D.readout (iterateTrajectory D.step h₀ D.K)

/-! ## 3. Attractor Basin Robustness -/

/--
An attractor fixed point `target` with basin radius `radius` and contraction factor `c < 1`.
Any state within the basin contracts toward `target` under `step`.
-/
structure AttractorBasin (step : H → H) where
  target : H
  radius : ℝ
  hrpos : 0 < radius
  contraction : ℝ
  hc_nonneg : 0 ≤ contraction
  hc_lt_one : contraction < 1
  contracts : ∀ x : H, dist x target < radius →
    dist (step x) target ≤ contraction * dist x target

/-- Helper Lemma: The trajectory strictly remains inside the basin at every step. -/
lemma trajectory_stays_in_basin (step : H → H) (basin : AttractorBasin step)
    (h₀ : H) (h_in : dist h₀ basin.target < basin.radius) (k : ℕ) :
    dist (iterateTrajectory step h₀ k) basin.target < basin.radius := by
  induction k with
  | zero => exact h_in
  | succ j jh =>
    have h_step := basin.contracts (iterateTrajectory step h₀ j) jh
    calc dist (iterateTrajectory step h₀ (j + 1)) basin.target
      _ ≤ basin.contraction * dist (iterateTrajectory step h₀ j) basin.target := h_step
      _ ≤ 1 * dist (iterateTrajectory step h₀ j) basin.target := by
        apply mul_le_mul_of_nonneg_right (le_of_lt basin.hc_lt_one) dist_nonneg
      _ = dist (iterateTrajectory step h₀ j) basin.target := one_mul _
      _ < basin.radius := jh

/--
After `K` iterations in the basin, distance to the target contracts by `c^K`.
-/
theorem dynamic_trajectory_convergence (step : H → H) (basin : AttractorBasin step)
    (h₀ : H) (h_in : dist h₀ basin.target < basin.radius) (K : ℕ) :
    dist (iterateTrajectory step h₀ K) basin.target ≤
      (basin.contraction ^ K) * dist h₀ basin.target := by
  induction K with
  | zero =>
    simp only [iterateTrajectory, pow_zero, one_mul]
    exact le_rfl
  | succ k ih =>
    have h_k_in := trajectory_stays_in_basin step basin h₀ h_in k
    have h_step := basin.contracts (iterateTrajectory step h₀ k) h_k_in
    calc dist (iterateTrajectory step h₀ (k + 1)) basin.target
      _ ≤ basin.contraction * dist (iterateTrajectory step h₀ k) basin.target := h_step
      _ ≤ basin.contraction * ((basin.contraction ^ k) * dist h₀ basin.target) :=
          mul_le_mul_of_nonneg_left ih basin.hc_nonneg
      _ = (basin.contraction ^ (k + 1)) * dist h₀ basin.target := by ring

/-! ## 4. Resistance to Orthogonal Representation Gaming -/

/--
Theorem: A static evasion perturbation `v` fails against a dynamic attractor
if the perturbed state remains inside the intent's attractor basin.
Even if an adversary adds `v`, the dynamic trajectory asymptotically contracts
to the true intent attractor target `h*`, bounding evasion capability by `O(c^K)`.
-/
theorem gaming_resistance_in_basin (D : DynamicDetector H Z) (basin : AttractorBasin D.step)
    (h_intent : H) (v : H)
    (h_base : dist h_intent basin.target < basin.radius / 2)
    (h_pert : ‖v‖ < basin.radius / 2) :
    dist (iterateTrajectory D.step (h_intent + v) D.K) basin.target ≤
      (basin.contraction ^ D.K) * basin.radius := by
  have h_init : dist (h_intent + v) basin.target < basin.radius := by
    calc dist (h_intent + v) basin.target
      _ ≤ dist (h_intent + v) h_intent + dist h_intent basin.target := dist_triangle (h_intent + v) h_intent basin.target
      _ = ‖(h_intent + v) - h_intent‖ + dist h_intent basin.target := by rw [dist_eq_norm (h_intent + v) h_intent]
      _ = ‖v‖ + dist h_intent basin.target := by
        have : (h_intent + v) - h_intent = v := by abel
        rw [this]
      _ < basin.radius / 2 + basin.radius / 2 := add_lt_add h_pert h_base
      _ = basin.radius := add_halves basin.radius
  have h_conv := dynamic_trajectory_convergence D.step basin (h_intent + v) h_init D.K
  have h_dist_le : dist (h_intent + v) basin.target ≤ basin.radius := le_of_lt h_init
  calc dist (iterateTrajectory D.step (h_intent + v) D.K) basin.target
    _ ≤ (basin.contraction ^ D.K) * dist (h_intent + v) basin.target := h_conv
    _ ≤ (basin.contraction ^ D.K) * basin.radius :=
        mul_le_mul_of_nonneg_left h_dist_le (pow_nonneg basin.hc_nonneg D.K)

/-! ## 5. Regret Loss Formulation -/

/-- Hinge-cosine regret over a prototype bank `D_prototypes`. -/
noncomputable def regretHinge (z : Z) (D_prototypes : Set Z) (τ : ℝ) : ℝ :=
  sSup { r : ℝ | ∃ d ∈ D_prototypes, r = max 0 (@inner ℝ Z _ z d - τ) }

/-- Total objective function matching the Regret Heuristic framework. -/
noncomputable def totalLoss (L_task : ℝ) (lambda_regret : ℝ)
    (detector : DynamicDetector H Z) (h₀ : H)
    (D_prototypes : Set Z) (τ : ℝ) : ℝ :=
  L_task + lambda_regret * (regretHinge (detector.eval h₀) D_prototypes τ)

end RegretHeuristic
