/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Evidence bookkeeping. Likelihood ratio, independence, information gain.
A glossary, not a safety proof. Not a camera. Does not fill D. Does not freeze r.
A likelihood ratio is not the probability that someone is lying.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace EvidenceMath

/-- Two hypotheses. Not guilt. Not a lie label. -/
inductive Hyp where
  | h1
  | h2
deriving DecidableEq, Repr

/-- Likelihood ratio. P(E | H1) / P(E | H2).
    Defined only when the denominator is positive. -/
def likelihoodRatio (pE_h1 pE_h2 : Rat) (_h : pE_h2 ≠ 0) : Rat :=
  pE_h1 / pE_h2

/-- The brief's example: 0.80 / 0.20 = 4. -/
theorem example_lr_four :
    likelihoodRatio (4 / 5) (1 / 5) (by norm_num) = 4 := by
  unfold likelihoodRatio
  norm_num

/-- LR > 1 favors H1 over H2. Bookkeeping on the ratio, not a posterior. -/
def favorsH1 (lr : Rat) : Bool :=
  lr > 1

/-- LR < 1 favors H2. -/
def favorsH2 (lr : Rat) : Bool :=
  lr < 1

/-- LR = 1 does not separate them. -/
def doesNotSeparate (lr : Rat) : Bool :=
  lr = 1

theorem four_favors_h1 :
    favorsH1 4 = true ∧ favorsH2 4 = false ∧ doesNotSeparate 4 = false := by
  native_decide

theorem one_does_not_separate :
    doesNotSeparate 1 = true ∧ favorsH1 1 = false ∧ favorsH2 1 = false := by
  native_decide

/-- A likelihood ratio is not a probability of H1, and not a lie probability.
    The example LR of 4 is not 0.8. -/
theorem lr_not_a_probability :
    likelihoodRatio (4 / 5) (1 / 5) (by norm_num) ≠ 4 / 5 := by
  unfold likelihoodRatio
  norm_num

/-- Under conditional independence, combined LR is the product.
    This is the hypothesis. Dependent items do not get this. -/
def combinedIndependent (lrs : List Rat) : Rat :=
  lrs.prod

theorem two_independent_multiply :
    combinedIndependent [4, 2] = 8 := by
  native_decide

/-- Three documents, one source. Counting them as independent inflates.
    A witness, an article quoting the witness, and a summary are one item.
    The product of three copies is not the weight of one source. -/
theorem triple_count_inflates :
    combinedIndependent [2, 2, 2] = 8 ∧ combinedIndependent [2] = 2 := by
  native_decide

/-- Information gain. IG(Q) = H(before) − expected H(after).
    A useful question reduces entropy over the hypothesis set.
    Bookkeeping only. Not a proved interviewer. -/
def informationGain (hBefore hAfter : Rat) : Rat :=
  hBefore - hAfter

theorem positive_gain_reduces :
    informationGain 1 (1 / 2) = 1 / 2 := by
  unfold informationGain
  norm_num

/-- Zero gain does not separate. -/
theorem zero_gain :
    informationGain 1 1 = 0 := by
  unfold informationGain
  norm_num

/-- This file is not a camera and not a handover. -/
def notACamera : Bool := false

theorem evidence_math_not_camera :
    notACamera = false := by
  rfl

/-- A likelihood ratio does not enter L_total. -/
structure Loss where
  task : Rat
  regret : Rat

def total (L : Loss) (λ : Rat) : Rat :=
  L.task + λ * L.regret

theorem lr_not_in_total :
    ∀ (L : Loss) (λ lr : Rat), total L λ = L.task + λ * L.regret := by
  intro L λ lr
  rfl

end EvidenceMath
