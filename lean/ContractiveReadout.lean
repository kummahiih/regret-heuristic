/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Wanted split: reveal ker-evasion, keep plan gap.
Isotropic T(h)=c•h does the opposite of the first and the bad half of the second.
Residual+noise is not this file.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace ContractiveReadout

/-- Static camera: first coordinate. -/
def staticR (h0 _h1 : ℝ) : ℝ := h0

/-- Isotropic shrink. -/
def iso (c h : ℝ) : ℝ := c * h

theorem iso_scales_plan (c plan : ℝ) :
    staticR (iso c plan) 0 = c * plan := by
  simp [staticR, iso]

theorem iso_hides_kernel (c ev : ℝ) :
    staticR (iso c 0) ev = 0 := by
  simp [staticR, iso]

/-- Dummy numbers from simulation_four_state contractive_iso, K-step 1/8. -/
theorem iso_shrinks_plan_hides_v :
    let c : ℝ := (1 : ℝ) / 8
    staticR (iso c (1 : ℝ)) 0 = c ∧ staticR (iso c 0) 1 = 0 := by
  simp [staticR, iso]

/-- The wanted pair is two inequalities. Not proved for residual+noise. -/
structure WantedSplit where
  planKept : Prop
  evasionVisible : Prop

def wanted_not_automatic : WantedSplit :=
  { planKept := False, evasionVisible := False }

end ContractiveReadout
