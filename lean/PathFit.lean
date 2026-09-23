/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

A path-fit (SIREN weights, f(1)) is another walk object.
Not a field of the trainer loss. Dummy. Not Qwen.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace PathFit

structure LegalLoss where
  task : ℝ
  hinge : ℝ

def totalLoss (L : LegalLoss) (lam : ℝ) : ℝ := L.task + lam * L.hinge

/-- Compressed path weights. Bookkeeping only. -/
abbrev Theta := ℝ

def attachTheta (L : LegalLoss) (th : Theta) : LegalLoss × Theta := (L, th)

theorem totalLoss_ignores_theta (L : LegalLoss) (a b : Theta) (lam : ℝ) :
    totalLoss (attachTheta L a).1 lam = totalLoss (attachTheta L b).1 lam := rfl

theorem theta_not_the_hinge (L : LegalLoss) (a b : Theta) :
    (attachTheta L a).1.hinge = (attachTheta L b).1.hinge := rfl

/-- Query at the end of the path is another walk number. -/
def queryEnd (pathEnd : ℝ) : ℝ := pathEnd

theorem queryEnd_is_the_end (x : ℝ) : queryEnd x = x := rfl

theorem queryEnd_not_automatic_strat :
    queryEnd (1 : ℝ) = 1 ∧ queryEnd (0 : ℝ) = 0 := by
  simp [queryEnd]

end PathFit
