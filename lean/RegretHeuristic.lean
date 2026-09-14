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

open scoped BigOperators
open Filter Topology

namespace RegretHeuristic

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]

noncomputable def cosineSim (u v : E) : Real :=
  inner u v / (norm u * norm v)

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
  rw [cosineSim, le_div_iff₀ hden, neg_mul, one_mul]
  have h := real_inner_le_norm (-u) v
  simpa [inner_neg_left, norm_neg] using h

noncomputable def maxCosine (h : E) (D : Finset E) (hD : D.Nonempty) : Real :=
  D.sup' hD (fun d => cosineSim h d)

def relu (x : Real) : Real := max x 0

lemma relu_nonneg (x : Real) : 0 ≤ relu x := le_max_right _ _

lemma relu_eq_zero_of_nonpos {x : Real} (hx : x ≤ 0) : relu x = 0 :=
  max_eq_right hx

noncomputable def regretHinge (h : E) (D : Finset E) (hD : D.Nonempty) (tau : Real) : Real :=
  relu (maxCosine h D hD - tau)

lemma regretHinge_nonneg (h : E) (D : Finset E) (hD : D.Nonempty) (tau : Real) :
    0 ≤ regretHinge h D hD tau :=
  relu_nonneg _

lemma regretHinge_eq_zero_of_le (h : E) (D : Finset E) (hD : D.Nonempty) {tau : Real}
    (hle : maxCosine h D hD ≤ tau) : regretHinge h D hD tau = 0 :=
  relu_eq_zero_of_nonpos (sub_nonpos.mpr hle)

def totalLoss (task lambda hinge : Real) : Real := task + lambda * hinge

lemma totalLoss_zero_weight (task hinge : Real) : totalLoss task 0 hinge = task := by
  simp [totalLoss]

variable {A : Type*} [Fintype A] [Nonempty A]

/-- Prefix of the loss sequence of length `t`. Index `i : Fin t` is round `i`. -/
abbrev LossPrefix (A : Type*) (t : Nat) := Fin t → A → Real

/-- Causal (online) strategy: the action at time `t` is a function of
    `ell 0, ..., ell (t-1)` only. It does not receive `ell t`. -/
abbrev CausalStrategy (A : Type*) := (t : Nat) → LossPrefix A t → A

/-- Unroll: `a t = sigma t (ell ∘ Fin.val)`. -/
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

/-- Hannan consistency of a causal strategy. -/
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

structure IntentHingeData where
  readout : E
  bank : Finset E
  bank_nonempty : bank.Nonempty
  threshold : Real

structure ExternalRegretData where
  loss : Nat → A → Real
  play : Nat → A
  horizon : Nat

noncomputable def IntentHingeData.value (p : IntentHingeData) : Real :=
  regretHinge p.readout p.bank p.bank_nonempty p.threshold

def ExternalRegretData.value (p : ExternalRegretData) : Real :=
  externalRegret p.loss p.play p.horizon

end RegretHeuristic
