/-
Copyright (c) 2026 kummahiih.
Released under the parent repository license.

Definitional Lean 4 slice of the amplitude joke.
An amplitude is bookkeeping for a cell you do not put in the loss.
This file does **not** implement a quantum circuit, a Born-rule trainer,
or a proof that anyone understands z.
-/

import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.NormNum

namespace AmplitudeBookkeeping

/-- Unobservable cells. Never a field of `LegalLoss`. -/
abbrev Cell := Fin 2

/-- Amplitude assignment over cells. Bookkeeping only. -/
def Amp := Cell → ℂ

/-- Born weight of one already-chosen cell. Premature measurement. -/
def bornWeight (a : ℂ) : ℝ := Complex.normSq a

/-- Two unobservable routes to one observable: add, then square. -/
def delayedBorn (a b : ℂ) : ℝ := Complex.normSq (a + b)

/-- Two routes measured separately, then added as probabilities. -/
def prematureBorn (a b : ℂ) : ℝ := Complex.normSq a + Complex.normSq b

lemma normSq_one : Complex.normSq (1 : ℂ) = 1 := by
  simp [Complex.normSq]

lemma normSq_neg_one : Complex.normSq (-1 : ℂ) = 1 := by
  simp [Complex.normSq]

lemma normSq_one_plus_neg_one : Complex.normSq ((1 : ℂ) + (-1)) = 0 := by
  simp [Complex.normSq]

/-- The joke in numbers. Same two routes; measurement time changes the score. -/
theorem two_route_identity :
    delayedBorn (1 : ℂ) (-1) = 0 ∧ prematureBorn (1 : ℂ) (-1) = 2 := by
  constructor
  · simp [delayedBorn, Complex.normSq]
  · simp [prematureBorn, Complex.normSq]; norm_num

lemma delayed_ne_premature :
    delayedBorn (1 : ℂ) (-1) ≠ prematureBorn (1 : ℂ) (-1) := by
  simp [delayedBorn, prematureBorn, Complex.normSq]
  norm_num

/-- Interference term that premature measurement throws away. -/
def interference (a b : ℂ) : ℝ :=
  delayedBorn a b - prematureBorn a b

lemma interference_cancel_pair : interference (1 : ℂ) (-1) = -2 := by
  simp [interference, delayedBorn, prematureBorn, Complex.normSq]
  norm_num

/-- What the trainer is allowed to see. No `Amp`, no `Cell`. -/
structure LegalLoss where
  task : ℝ
  hinge : ℝ

def totalLoss (L : LegalLoss) (lam : ℝ) : ℝ := L.task + lam * L.hinge

lemma totalLoss_zero_weight (L : LegalLoss) : totalLoss L 0 = L.task := by
  simp [totalLoss]

/-- Pairing an amplitude with a loss does not feed it to the loss. -/
def attachAmp (L : LegalLoss) (α : Amp) : LegalLoss × Amp := (L, α)

lemma loss_ignores_amp (L : LegalLoss) (α β : Amp) :
    (attachAmp L α).1 = (attachAmp L β).1 := rfl

lemma totalLoss_ignores_amp (L : LegalLoss) (α β : Amp) (lam : ℝ) :
    totalLoss (attachAmp L α).1 lam = totalLoss (attachAmp L β).1 lam := rfl

/-- Two different amplitudes can share a premature score. Non-uniqueness of z. -/
def flipAmp (α : Amp) : Amp := fun z => -α z

lemma premature_sign_blind (a b : ℂ) :
    prematureBorn a b = prematureBorn (-a) (-b) := by
  simp [prematureBorn, Complex.normSq]

/-- Player II phase move: same premature mass, different delayed occupancy. -/
theorem same_premature_different_delayed :
    prematureBorn (1 : ℂ) (-1) = prematureBorn 1 1 ∧
      delayedBorn (1 : ℂ) (-1) ≠ delayedBorn 1 1 := by
  refine ⟨?eq, ?ne⟩
  · simp [prematureBorn, Complex.normSq]
  · have h0 : delayedBorn (1 : ℂ) (-1) = 0 := by
      simp [delayedBorn, Complex.normSq]
    have h4 : delayedBorn (1 : ℂ) 1 = 4 := by
      simp [delayedBorn, Complex.normSq]
    simp [h0, h4]

/-- Player II scale move: same delayed occupancy, different premature mass. -/
theorem same_delayed_different_premature :
    delayedBorn (1 : ℂ) (-1) = delayedBorn 2 (-2) ∧
      prematureBorn (1 : ℂ) (-1) ≠ prematureBorn 2 (-2) := by
  refine ⟨?eq, ?ne⟩
  · simp [delayedBorn, Complex.normSq]
  · have h2 : prematureBorn (1 : ℂ) (-1) = 2 := by
      simp [prematureBorn, Complex.normSq]
    have h8 : prematureBorn (2 : ℂ) (-2) = 8 := by
      simp [prematureBorn, Complex.normSq]
    simp [h2, h8]

end AmplitudeBookkeeping
