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
    (attachAmp L α).1 = (attachAmp L α).1 := rfl

lemma totalLoss_ignores_amp (L : LegalLoss) (α β : Amp) (lam : ℝ) :
    totalLoss (attachAmp L α).1 lam = totalLoss (attachAmp L β).1 lam := rfl

/-- Observable walk numbers. B1: fill `LegalLoss` from this, not from `Amp`. -/
structure Walk where
  task : ℝ
  hinge : ℝ
  pathLen : Nat

def legalOfWalk (w : Walk) : LegalLoss :=
  { task := w.task, hinge := w.hinge }

lemma legalOfWalk_ignores_pathLen (t h : ℝ) (n m : Nat) :
    legalOfWalk { task := t, hinge := h, pathLen := n } =
      legalOfWalk { task := t, hinge := h, pathLen := m } := rfl

/-- You can still write `LegalLoss.mk (bornWeight α 0) 0` by hand.
That is the dataflow hole `totalLoss_ignores_amp` does not close. -/
def illegalFromAmp (α : Amp) : LegalLoss :=
  { task := bornWeight (α 0), hinge := 0 }

lemma legalOfWalk_ne_need_amp (w : Walk) :
    legalOfWalk w = { task := w.task, hinge := w.hinge } := rfl

/-- What "frozen I" names. Log only. Not a third loss. -/
inductive FrozenKind where
  | readout
  | backbone
  | cachedH
  deriving DecidableEq

def frozenKindName : FrozenKind → String
  | .readout => "readout"
  | .backbone => "backbone"
  | .cachedH => "cached_h"

lemma frozenKind_three : FrozenKind.readout ≠ FrozenKind.backbone := by
  decide

/-- Signed-real notes. ℂ is the Feynman name; the cancel pair does not need an angle. -/
def delayedBornReal (a b : ℝ) : ℝ := (a + b) ^ 2

def prematureBornReal (a b : ℝ) : ℝ := a ^ 2 + b ^ 2

theorem two_route_identity_real :
    delayedBornReal (1 : ℝ) (-1) = 0 ∧ prematureBornReal (1 : ℝ) (-1) = 2 := by
  constructor
  · simp [delayedBornReal]
  · simp [prematureBornReal]; norm_num

lemma legalLoss_has_no_amp_field (L : LegalLoss) :
    L.task = L.task ∧ L.hinge = L.hinge := ⟨rfl, rfl⟩

/-- Two different amplitudes can share a premature score. Non-uniqueness of z. -/
def flipAmp (α : Amp) : Amp := fun z => -α z

lemma premature_sign_blind (a b : ℂ) :
    prematureBorn a b = prematureBorn (-a) (-b) := by
  simp [prematureBorn, Complex.normSq]

lemma delayedBorn_one_neg_one : delayedBorn (1 : ℂ) (-1) = 0 := by
  simp [delayedBorn, Complex.normSq]

lemma delayedBorn_one_one : delayedBorn (1 : ℂ) 1 = 4 := by
  simp [delayedBorn, Complex.normSq]
  norm_num

lemma prematureBorn_one_neg_one : prematureBorn (1 : ℂ) (-1) = 2 := by
  simp [prematureBorn, Complex.normSq]
  norm_num

lemma prematureBorn_one_one : prematureBorn (1 : ℂ) 1 = 2 := by
  simp [prematureBorn, Complex.normSq]
  norm_num

lemma prematureBorn_two_neg_two : prematureBorn (2 : ℂ) (-2) = 8 := by
  simp [prematureBorn, Complex.normSq]
  norm_num

lemma delayedBorn_two_neg_two : delayedBorn (2 : ℂ) (-2) = 0 := by
  simp [delayedBorn, Complex.normSq]

theorem same_premature_different_delayed :
    prematureBorn (1 : ℂ) (-1) = prematureBorn 1 1 ∧
      delayedBorn (1 : ℂ) (-1) ≠ delayedBorn 1 1 := by
  refine ⟨?eq, ?ne⟩
  · rw [prematureBorn_one_neg_one, prematureBorn_one_one]
  · rw [delayedBorn_one_neg_one, delayedBorn_one_one]; norm_num

theorem same_delayed_different_premature :
    delayedBorn (1 : ℂ) (-1) = delayedBorn 2 (-2) ∧
      prematureBorn (1 : ℂ) (-1) ≠ prematureBorn 2 (-2) := by
  refine ⟨?eq, ?ne⟩
  · rw [delayedBorn_one_neg_one, delayedBorn_two_neg_two]
  · rw [prematureBorn_one_neg_one, prematureBorn_two_neg_two]; norm_num

end AmplitudeBookkeeping
