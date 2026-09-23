import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Counterfactual task regret (off the training graph)

Thinking tool. Not a field of `LegalLoss`.
`aStar` is *named*, not searched. There is no `A_safe` constructor here
because that needs `r_strat`.
-/

namespace RegretHeuristic

/-- Extra job-cost versus a named best-safe action. -/
def counterfactualR {A : Type*} (u : A → ℝ) (aStar a : A) : ℝ :=
  u aStar - u a

/-- At the named star the extra cost is 0. -/
theorem counterfactualR_of_star {A : Type*} (u : A → ℝ) (aStar : A) :
    counterfactualR u aStar aStar = 0 := by
  simp [counterfactualR]

/-- If `aStar` really is better or equal on `u`, `R` is nonnegative. -/
theorem counterfactualR_nonneg_of_best {A : Type*} (u : A → ℝ) (aStar a : A)
    (h : u a ≤ u aStar) :
    0 ≤ counterfactualR u aStar a := by
  simpa [counterfactualR] using sub_nonneg.mpr h

/-- Quiet cosine and this `R` are different numbers. Dummy: hinge 0, `R` 1. -/
theorem quiet_hinge_not_counterfactualR :
    let hinge : ℝ := 0
    let R : ℝ := counterfactualR (fun b : Fin 2 => if b = 0 then (0 : ℝ) else 1) 1 0
    hinge = 0 ∧ R = 1 ∧ hinge ≠ R := by
  simp [counterfactualR]

end RegretHeuristic
