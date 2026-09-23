/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Talker-count on a bag of walks. Uncertainty log.
Not a camera. Not ICA. Not a field of the trainer loss.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace SourceCount

/-- How many independent voices the walk-cloud looks like.
    Bookkeeping only. -/
abbrev SourceCountNat := Nat

/-- Trainer-facing pair. No source-count field. -/
structure LegalLoss where
  task : ℝ
  hinge : ℝ

def totalLoss (L : LegalLoss) (lam : ℝ) : ℝ := L.task + lam * L.hinge

/-- Pair a loss with a talker-count. The count is the second slot. -/
def attachSourceCount (L : LegalLoss) (m : SourceCountNat) : LegalLoss × SourceCountNat :=
  (L, m)

theorem totalLoss_ignores_sourceCount (L : LegalLoss) (m n : SourceCountNat) (lam : ℝ) :
    totalLoss (attachSourceCount L m).1 lam =
      totalLoss (attachSourceCount L n).1 lam := rfl

theorem sourceCount_not_the_hinge (L : LegalLoss) (m n : SourceCountNat) :
    (attachSourceCount L m).1.hinge = (attachSourceCount L n).1.hinge := rfl

/-- One voice vs two voices. The hinge can stay silent either way. -/
theorem crowded_not_the_slap :
    let L : LegalLoss := { task := 1, hinge := 0 }
    let one : SourceCountNat := 1
    let two : SourceCountNat := 2
    L.hinge = 0 ∧
      totalLoss (attachSourceCount L one).1 1 =
        totalLoss (attachSourceCount L two).1 1 := by
  simp [totalLoss, attachSourceCount]

lemma one_ne_two : (1 : SourceCountNat) ≠ 2 := by decide

end SourceCount
