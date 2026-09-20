/-
Copyright (c) 2026 kummahiih.
Released under the parent repository license.

Definitional Lean 4 slice of the Regret Heuristic notes.
This is a specification of the toy hinge and of learning-theoretic
external regret. It does **not** prove that the hinge is Hannan-consistent.
-/

import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Finset.Insert
import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Tactic.NormNum

open scoped BigOperators InnerProductSpace
open Filter Topology

namespace RegretHeuristic

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]

noncomputable def cosineSim (u v : E) : Real :=
  inner Real u v / (norm u * norm v)

lemma cosineSim_le_one {u v : E} (hu : u ≠ 0) (hv : v ≠ 0) :
    cosineSim u v ≤ 1 := by
  have hden : 0 < norm u * norm v :=
    mul_pos (norm_pos_iff.mpr hu) (norm_pos_iff.mpr hv)
  rw [cosineSim, div_le_one hden]
  exact real_inner_le_norm u v

lemma neg_one_le_cosineSim {u v : E} (hu : u ≠ 0) (hv : v ≠ 0) :
    -1 ≤ cosineSim u v := by
  have hden : 0 < norm u * norm v :=
    mul_pos (norm_pos_iff.mpr hu) (norm_pos_iff.mpr hv)
  have habs := abs_real_inner_le_norm u v
  rw [cosineSim, le_div_iff₀ hden, neg_mul, one_mul]
  exact neg_le_of_abs_le habs

noncomputable def maxCosine (h : E) (D : Finset E) (hD : D.Nonempty) : Real :=
  D.sup' hD (fun d => cosineSim h d)

def relu (x : Real) : Real := max x 0

lemma relu_nonneg (x : Real) : 0 ≤ relu x := le_max_right _ _

lemma relu_eq_zero_of_nonpos {x : Real} (hx : x ≤ 0) : relu x = 0 :=
  max_eq_right hx

lemma relu_mono {x y : Real} (h : x ≤ y) : relu x ≤ relu y :=
  max_le_max h le_rfl

lemma relu_wider_tau_le (s tau1 tau2 : Real) (h : tau1 ≤ tau2) :
    relu (s - tau2) ≤ relu (s - tau1) := by
  apply relu_mono
  linarith

noncomputable def regretHinge (h : E) (D : Finset E) (hD : D.Nonempty) (tau : Real) : Real :=
  relu (maxCosine h D hD - tau)

lemma regretHinge_nonneg (h : E) (D : Finset E) (hD : D.Nonempty) (tau : Real) :
    0 ≤ regretHinge h D hD tau :=
  relu_nonneg _

lemma regretHinge_eq_zero_of_le (h : E) (D : Finset E) (hD : D.Nonempty) {tau : Real}
    (hle : maxCosine h D hD ≤ tau) : regretHinge h D hD tau = 0 :=
  relu_eq_zero_of_nonpos (sub_nonpos.mpr hle)

lemma regretHinge_wider_tau_le (h : E) (D : Finset E) (hD : D.Nonempty)
    {tau1 tau2 : Real} (ht : tau1 ≤ tau2) :
    regretHinge h D hD tau2 ≤ regretHinge h D hD tau1 :=
  relu_wider_tau_le _ _ _ ht

def totalLoss (task lambda hinge : Real) : Real := task + lambda * hinge

lemma totalLoss_zero_weight (task hinge : Real) : totalLoss task 0 hinge = task := by
  simp [totalLoss]

def insertionTwoRegret (best second : Real) : Real := second - best

variable {A : Type*} [Fintype A] [Nonempty A]

abbrev LossPrefix (A : Type*) (t : Nat) := Fin t → A → Real

abbrev CausalStrategy (A : Type*) := (t : Nat) → LossPrefix A t → A

def playOf (sigma : CausalStrategy A) (ell : Nat → A → Real) : Nat → A :=
  fun t => sigma t (fun i => ell i.val)

def cumulativeLoss (ell : Nat → A → Real) (T : Nat) (act : A) : Real :=
  (Finset.range T).sum (fun t => ell t act)

def bestComparatorLoss (ell : Nat → A → Real) (T : Nat) : Real :=
  Finset.univ.inf' Finset.univ_nonempty (cumulativeLoss ell T)

def playLoss (ell : Nat → A → Real) (act : Nat → A) (T : Nat) : Real :=
  (Finset.range T).sum (fun t => ell t (act t))

def externalRegret (ell : Nat → A → Real) (act : Nat → A) (T : Nat) : Real :=
  playLoss ell act T - bestComparatorLoss ell T

def hannanConsistent (sigma : CausalStrategy A) : Prop :=
  ∀ ell : Nat → A → Real,
    Tendsto (fun T : Nat =>
      externalRegret ell (playOf sigma ell) T.succ / (T.succ : Real))
      atTop (nhds 0)

def clipInterval (x lo hi : Real) : Real := max lo (min x hi)

def clippedSurrogate (rAdv eps adv : Real) : Real :=
  min (rAdv * adv) (clipInterval rAdv (1 - eps) (1 + eps) * adv)

def ppoWithHinge (ppo lambda hinge : Real) : Real := ppo + lambda * hinge

lemma ppoWithHinge_zero_weight (ppo hinge : Real) : ppoWithHinge ppo 0 hinge = ppo := by
  simp [ppoWithHinge]

def ppoMinWithHinge (clipSurrogate lambda hinge : Real) : Real :=
  -clipSurrogate + lambda * hinge

structure IntentHingeData (E : Type*) [NormedAddCommGroup E] [InnerProductSpace Real E] where
  readout : E
  bank : Finset E
  bank_nonempty : bank.Nonempty
  threshold : Real

structure ExternalRegretData (A : Type*) [Fintype A] [Nonempty A] where
  loss : Nat → A → Real
  play : Nat → A
  horizon : Nat

noncomputable def IntentHingeData.value {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace Real E] (p : IntentHingeData E) :=
  regretHinge p.readout p.bank p.bank_nonempty p.threshold

def ExternalRegretData.value {A : Type*} [Fintype A] [Nonempty A]
    (p : ExternalRegretData A) :=
  externalRegret p.loss p.play p.horizon

def twoActionLoss (_t : Nat) (a : Fin 2) : Real := a.val

def alwaysOne (_t : Nat) : Fin 2 := 1

lemma playLoss_alwaysOne (T : Nat) :
    playLoss twoActionLoss alwaysOne T = T := by
  simp [playLoss, twoActionLoss, alwaysOne, Finset.sum_const, Finset.card_range]

lemma cumulativeLoss_action0 (T : Nat) :
    cumulativeLoss twoActionLoss T 0 = 0 := by
  simp [cumulativeLoss, twoActionLoss]

lemma bestComparator_twoAction (T : Nat) :
    bestComparatorLoss twoActionLoss T = 0 := by
  unfold bestComparatorLoss
  apply le_antisymm
  · have h := Finset.inf'_le (cumulativeLoss twoActionLoss T)
      (Finset.mem_univ (0 : Fin 2))
    rw [cumulativeLoss_action0] at h
    exact h
  · apply Finset.le_inf'
    intro a _ha
    simp [cumulativeLoss, twoActionLoss, Finset.sum_const, Finset.card_range]
    exact mul_nonneg (Nat.cast_nonneg T) (Nat.cast_nonneg a.val)

lemma externalRegret_alwaysOne (T : Nat) :
    externalRegret twoActionLoss alwaysOne T = T := by
  simp [externalRegret, playLoss_alwaysOne, bestComparator_twoAction]

noncomputable def silentHinge : IntentHingeData Real where
  readout := (1 : Real)
  bank := {(-1 : Real)}
  bank_nonempty := Finset.singleton_nonempty _
  threshold := 0

lemma cosineSim_one_neg_one : cosineSim (1 : Real) (-1) = -1 := by
  have hden : (norm (1 : Real) * norm (-1 : Real)) ≠ 0 := by
    simp
  simp [cosineSim]

lemma silentHinge_max_le : maxCosine (1 : Real) {(-1 : Real)} (Finset.singleton_nonempty _) ≤ 0 := by
  simp [maxCosine, Finset.sup'_singleton, cosineSim_one_neg_one]

lemma silentHinge_value : silentHinge.value = 0 := by
  simp [IntentHingeData.value, silentHinge]
  exact regretHinge_eq_zero_of_le (1 : Real) {(-1 : Real)}
    (Finset.singleton_nonempty _) silentHinge_max_le

def stubbornPlay (T : Nat) : ExternalRegretData (Fin 2) where
  loss := twoActionLoss
  play := alwaysOne
  horizon := T

lemma stubbornPlay_value (T : Nat) : (stubbornPlay T).value = T := by
  simp [ExternalRegretData.value, stubbornPlay, externalRegret_alwaysOne]

theorem silent_hinge_not_vanishing_external_regret (T : Nat) :
    silentHinge.value = 0 ∧ (stubbornPlay T).value = (T : Real) :=
  ⟨silentHinge_value, stubbornPlay_value T⟩

theorem insertion_two_regret_not_the_hinge :
    insertionTwoRegret (1 : Real) 4 = 3 ∧ silentHinge.value = 0 := by
  constructor
  · simp [insertionTwoRegret]; norm_num
  · exact silentHinge_value

set_option linter.unusedSectionVars false

def hingeQuietIgnoringAction (h : E) (D : Finset E) (hD : D.Nonempty)
    (tau : Real) (_a : A) : Prop :=
  regretHinge h D hD tau = 0

lemma hingeQuietIgnoringAction_indep (h : E) (D : Finset E) (hD : D.Nonempty)
    (tau : Real) (a b : A) :
    hingeQuietIgnoringAction h D hD tau a ↔
      hingeQuietIgnoringAction h D hD tau b := Iff.rfl

lemma hingeQuietIgnoringAction_all_or_none (h : E) (D : Finset E)
    (hD : D.Nonempty) (tau : Real) :
    (∀ a : A, hingeQuietIgnoringAction h D hD tau a) ∨
      (∀ a : A, ¬ hingeQuietIgnoringAction h D hD tau a) := by
  by_cases hq : regretHinge h D hD tau = 0
  · exact Or.inl (fun _ => hq)
  · exact Or.inr (fun _ => hq)

lemma cosineSim_one_one : cosineSim (1 : Real) 1 = 1 := by
  have hden : (norm (1 : Real) * norm (1 : Real)) ≠ 0 := by
    simp
  simp [cosineSim]

noncomputable def loudHinge : IntentHingeData Real where
  readout := (1 : Real)
  bank := {(1 : Real)}
  bank_nonempty := Finset.singleton_nonempty _
  threshold := 0

lemma loudHinge_max :
    maxCosine (1 : Real) {(1 : Real)} (Finset.singleton_nonempty _) = 1 := by
  simp [maxCosine, Finset.sup'_singleton, cosineSim_one_one]

lemma loudHinge_value : loudHinge.value = 1 := by
  simp [IntentHingeData.value, loudHinge, regretHinge, loudHinge_max, relu]

def deceptionPaysLoss (_t : Nat) (a : Fin 2) : Real := 1 - a.val

noncomputable def deceptionPaysHinge (a : Fin 2) : Real :=
  if a.val = 0 then silentHinge.value else loudHinge.value

lemma deceptionPaysHinge_zero : deceptionPaysHinge 0 = 0 := by
  simp [deceptionPaysHinge, silentHinge_value]

lemma deceptionPaysHinge_one : deceptionPaysHinge 1 = 1 := by
  simp [deceptionPaysHinge, loudHinge_value]

/-- First coord vs min on all of A (here 0). Second coord is the hinge. -/
noncomputable def uJointCoord (a : Fin 2) : Real × Real :=
  (deceptionPaysLoss 0 a, deceptionPaysHinge a)

lemma uJoint_zero : uJointCoord 0 = (1, 0) := by
  simp [uJointCoord, deceptionPaysLoss, deceptionPaysHinge_zero]

lemma uJoint_one : uJointCoord 1 = (0, 1) := by
  simp [uJointCoord, deceptionPaysLoss, deceptionPaysHinge_one]

theorem sjoint_unhit_zero :
    ¬ ((uJointCoord 0).1 ≤ 0 ∧ (uJointCoord 0).2 ≤ 0) := by
  simp [uJoint_zero]

theorem sjoint_unhit_one :
    ¬ ((uJointCoord 1).1 ≤ 0 ∧ (uJointCoord 1).2 ≤ 0) := by
  simp [uJoint_one]

/-- One-round S_joint box is empty: cheap action is loud, quiet action is expensive. -/
theorem sjoint_unhit_one_round :
    ¬ ((uJointCoord 0).1 ≤ 0 ∧ (uJointCoord 0).2 ≤ 0) ∧
      ¬ ((uJointCoord 1).1 ≤ 0 ∧ (uJointCoord 1).2 ≤ 0) :=
  ⟨sjoint_unhit_zero, sjoint_unhit_one⟩

/-- Extra cost vs the quiet action (cost 1), plus hinge. Play 0. -/
noncomputable def uSafeQuiet : Real × Real :=
  (deceptionPaysLoss 0 0 - 1, deceptionPaysHinge 0)

theorem ssafe_hit_by_quiet :
    uSafeQuiet.1 ≤ 0 ∧ uSafeQuiet.2 ≤ 0 := by
  simp [uSafeQuiet, deceptionPaysLoss, deceptionPaysHinge_zero]

/-- Sensor that sees a: quiet iff hinge is 0. Opposite of ignoring-action. -/
noncomputable def hingeQuietOnAction (a : Fin 2) : Prop :=
  deceptionPaysHinge a = 0

lemma hingeQuietOnAction_zero : hingeQuietOnAction 0 := by
  simp [hingeQuietOnAction, deceptionPaysHinge_zero]

lemma not_hingeQuietOnAction_one : ¬ hingeQuietOnAction 1 := by
  simp [hingeQuietOnAction, deceptionPaysHinge_one]

/-- A_safe = {0}: nonempty and not all of Fin 2. -/
theorem hingeQuietOnAction_proper :
    hingeQuietOnAction 0 ∧ ¬ hingeQuietOnAction 1 :=
  ⟨hingeQuietOnAction_zero, not_hingeQuietOnAction_one⟩

/-- Topic may hug the hallway. Hinge only sees strat. -/
structure FactoredReadout (E : Type*) [NormedAddCommGroup E] [InnerProductSpace Real E] where
  topic : E
  strat : E
  coarseness : Real

noncomputable def factoredHinge (r : FactoredReadout E) (D : Finset E)
    (hD : D.Nonempty) (tau0 : Real) : Real :=
  regretHinge r.strat D hD tau0

lemma factoredHinge_ignores_topic (r : FactoredReadout E) (topic' : E)
    (D : Finset E) (hD : D.Nonempty) (tau0 : Real) :
    factoredHinge r D hD tau0 =
      factoredHinge { r with topic := topic' } D hD tau0 := rfl

/-- Two channels can disagree. Not a claim that a net gamed. -/
theorem trained_silent_frozenI_loud :
    silentHinge.value = 0 ∧ loudHinge.value = 1 :=
  ⟨silentHinge_value, loudHinge_value⟩

/-- Walk sits on D={1}. Held-out map cell -1 is not a pin. No ℝ² import. -/
theorem heldout_not_mem_walk_bank :
    (1 : Real) ∈ loudHinge.bank ∧ (-1 : Real) ∉ loudHinge.bank := by
  simp [loudHinge]
  norm_num

/-- Fin-1 packing cartoon. Two unit features on ℝ cannot be orthogonal,
so a 1-d residual cannot hold an independent topic axis and plan axis.
Wallpaper geometry, not a camera. -/
theorem no_two_orthogonal_units_on_real
    (u v : Real) (hu : u ^ 2 = 1) (hv : v ^ 2 = 1) :
    u * v ≠ 0 := by
  intro h
  have huv : u = 0 ∨ v = 0 := mul_eq_zero.mp h
  cases huv with
  | inl hu0 =>
    have : (0 : Real) ^ 2 = 1 := hu0 ▸ hu
    norm_num at this
  | inr hv0 =>
    have : (0 : Real) ^ 2 = 1 := hv0 ▸ hv
    norm_num at this

end RegretHeuristic
