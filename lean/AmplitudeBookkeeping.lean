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
  · simpa [delayedBorn] using normSq_one_plus_neg_one
  · simp [prematureBorn, normSq_one, normSq_neg_one]

lemma delayed_ne_premature :
    delayedBorn (1 : ℂ) (-1) ≠ prematureBorn (1 : ℂ) (-1) := by
  have h := two_route_identity
  linarith [h.1, h.2]

/-- Interference term that premature measurement throws away. -/
def interference (a b : ℂ) : ℝ :=
  delayedBorn a b - prematureBorn a b

lemma interference_cancel_pair : interference (1 : ℂ) (-1) = -2 := by
  have h := two_route_identity
  simp [interference, h.1, h.2]

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
    totalLoss (attachAmp L α).1 lam = totalLoss (attachAmp L β).1 lam := by
  simp [attachAmp]

/-- A last-token sensor of the walk. Not a cell, not an amplitude. -/
structure WalkSensor where
  readout : ℝ

/-- Quiet hinge on a sensor does not name a unique cell. -/
def silentOnWalk (s : WalkSensor) : Prop := s.readout = 1

lemma silent_walk_not_a_cell (s : WalkSensor) (h : silentOnWalk s) :
    s.readout = 1 ∧ ¬ (s.readout = (0 : ℝ) ∧ s.readout = 1) := by
  refine ⟨h, ?_⟩
  intro hboth
  linarith [hboth.1, hboth.2]

/-- Two different amplitudes can share a premature score. Non-uniqueness of z. -/
def flipAmp (α : Amp) : Amp := fun z => -α z

lemma premature_sign_blind (a b : ℂ) :
    prematureBorn a b = prematureBorn (-a) (-b) := by
  simp [prematureBorn, Complex.normSq]

end AmplitudeBookkeeping
