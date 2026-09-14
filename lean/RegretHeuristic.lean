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
import Mathlib.Topology.Instances.Real.Lemmas

open scoped BigOperators InnerProductSpace
open Filter Topology

namespace RegretHeuristic

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

noncomputable def cosineSim (u v : E) : ℝ :=
  inner ℝ u v / (‖u‖ * ‖v‖)

lemma cosineSim_le_one {u v : E} (hu : u ≠ 0) (hv : v ≠ 0) :
    cosineSim u v ≤ 1 := by
  have hden : 0 < ‖u‖ * ‖v‖ :=
    mul_pos (norm_pos_iff.mpr hu) (norm_pos_iff.mpr hv)
  rw [cosineSim, div_le_one hden]
  exact real_inner_le_norm u v

lemma neg_one_le_cosineSim {u v : E} (hu : u ≠ 0) (hv : v ≠ 0) :
    -1 ≤ cosineSim u v := by
  have hden : 0 < ‖u‖ * ‖v‖ :=
    mul_pos (norm_pos_iff.mpr hu) (norm_pos_iff.mpr hv)
  rw [cosineSim, le_div_iff₀ hden, neg_mul, one_mul]
  have h := real_inner_le_norm (-u) v
  simpa [inner_neg_left (ℝ := ℝ), norm_neg] using h

noncomputable def maxCosine (h : E) (D : Finset E) (hD : D.Nonempty) : ℝ :=
  D.sup' hD (fun d => cosineSim h d)

def relu (x : ℝ) : ℝ := max x 0

lemma relu_nonneg (x : ℝ) : 0 ≤ relu x := le_max_right _ _

lemma relu_eq_zero_of_nonpos {x : ℝ} (hx : x ≤ 0) : relu x = 0 :=
  max_eq_right hx

noncomputable def regretHinge (h : E) (D : Finset E) (hD : D.Nonempty) (tau : ℝ) : ℝ :=
  relu (maxCosine h D hD - tau)

lemma regretHinge_nonneg (h : E) (D : Finset E) (hD : D.Nonempty) (tau : ℝ) :
    0 ≤ regretHinge h D hD tau :=
  relu_nonneg _

lemma regretHinge_eq_zero_of_le (h : E) (D : Finset E) (hD : D.Nonempty) {tau : ℝ}
    (hle : maxCosine h D hD ≤ tau) : regretHinge h D hD tau = 0 :=
  relu_eq_zero_of_nonpos (sub_nonpos.mpr hle)

def totalLoss (task lambda hinge : ℝ) : ℝ := task + lambda * hinge

lemma totalLoss_zero_weight (task hinge : ℝ) : totalLoss task 0 hinge = task := by
  simp [totalLoss]

variable {A : Type*} [Fintype A] [Nonempty A]

/-- Prefix of the loss sequence of length `t`. Index `i : Fin t` is round `i`. -/
abbrev LossPrefix (A : Type*) (t : Nat) := Fin t → A → ℝ

/-- Causal (online) strategy: the action at time `t` is a function of
    `ell 0, ..., ell (t-1)` only. It does not receive `ell t`. -/
abbrev CausalStrategy (A : Type*) := (t : Nat) → LossPrefix A t → A

/-- Unroll: `a t = sigma t (ell ∘ Fin.val)`. -/
def playOf (sigma : CausalStrategy A) (ell : Nat → A → ℝ) : Nat → A :=
  fun t => sigma t (fun i => ell i.val)

def cumulativeLoss (ell : Nat → A → ℝ) (T : Nat) (act : A) : ℝ :=
  (Finset.range T).sum (fun t => ell t act)

def bestComparatorLoss (ell : Nat → A → ℝ) (T : Nat) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty (cumulativeLoss ell T)

def playLoss (ell : Nat → A → ℝ) (act : Nat → A) (T : Nat) : ℝ :=
  (Finset.range T).sum (fun t => ell t (act t))

def externalRegret (ell : Nat → A → ℝ) (act : Nat → A) (T : Nat) : ℝ :=
  playLoss ell act T - bestComparatorLoss ell T

/-- Hannan consistency of a causal strategy. -/
def hannanConsistent (sigma : CausalStrategy A) : Prop :=
  ∀ ell : Nat → A → ℝ,
    Tendsto (fun T : Nat =>
      externalRegret ell (playOf sigma ell) T.succ / (T.succ : ℝ))
      atTop (nhds 0)

def clipInterval (x lo hi : ℝ) : ℝ := max lo (min x hi)

def clippedSurrogate (rAdv eps adv : ℝ) : ℝ :=
  min (rAdv * adv) (clipInterval rAdv (1 - eps) (1 + eps) * adv)

def ppoWithHinge (ppo lambda hinge : ℝ) : ℝ := ppo + lambda * hinge

lemma ppoWithHinge_zero_weight (ppo hinge : ℝ) : ppoWithHinge ppo 0 hinge = ppo := by
  simp [ppoWithHinge]

structure IntentHingeData where
  readout : E
  bank : Finset E
  bank_nonempty : bank.Nonempty
  threshold : ℝ

structure ExternalRegretData where
  loss : Nat → A → ℝ
  play : Nat → A
  horizon : Nat

noncomputable def IntentHingeData.value (p : IntentHingeData) : ℝ :=
  regretHinge p.readout p.bank p.bank_nonempty p.threshold

def ExternalRegretData.value (p : ExternalRegretData) : ℝ :=
  externalRegret p.loss p.play p.horizon

end RegretHeuristic
