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
import Mathlib.Data.Finset.Lattice
import Mathlib.Topology.Instances.Real.Lemmas

open scoped BigOperators
open Filter Topology

/-! ## Cosine hinge (math_formulation.md)

Intent readout lives in an inner-product space. The prototype bank is a
finite nonempty set. Cosine is only used on nonzero vectors; the statements
that need `[-1, 1]` take those hypotheses.
-/

namespace RegretHeuristic

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]

/-- Cosine similarity. Undefined-as-a-bound when either vector is 0. -/
noncomputable def cosineSim (u v : E) : Real :=
  inner u v / (norm u * norm v)

lemma cosineSim_le_one {u v : E} (hu : u != 0) (hv : v != 0) :
    cosineSim u v <= 1 := by
  have hden : 0 < norm u * norm v :=
    mul_pos (norm_pos_iff.mpr hu) (norm_pos_iff.mpr hv)
  rw [cosineSim, div_le_one hden]
  exact real_inner_le_norm u v

lemma neg_one_le_cosineSim {u v : E} (hu : u != 0) (hv : v != 0) :
    -1 <= cosineSim u v := by
  have hden : 0 < norm u * norm v :=
    mul_pos (norm_pos_iff.mpr hu) (norm_pos_iff.mpr hv)
  rw [cosineSim, le_div_iff0 hden, neg_mul, one_mul]
  have h := real_inner_le_norm (-u) v
  simpa [inner_neg_left, norm_neg] using h

/-- Worst-case cosine of a readout against a nonempty bank. -/
noncomputable def maxCosine (h : E) (D : Finset E) (hD : D.Nonempty) : Real :=
  D.sup' hD (fun d => cosineSim h d)

def relu (x : Real) : Real := max x 0

lemma relu_nonneg (x : Real) : 0 <= relu x := le_max_right _ _

lemma relu_eq_zero_of_nonpos {x : Real} (hx : x <= 0) : relu x = 0 :=
  max_eq_right hx

/-- Per-example hinge: ReLU(sStar - tau). Instantaneous; no comparator. -/
noncomputable def regretHinge (h : E) (D : Finset E) (hD : D.Nonempty) (tau : Real) : Real :=
  relu (maxCosine h D hD - tau)

lemma regretHinge_nonneg (h : E) (D : Finset E) (hD : D.Nonempty) (tau : Real) :
    0 <= regretHinge h D hD tau :=
  relu_nonneg _

lemma regretHinge_eq_zero_of_le (h : E) (D : Finset E) (hD : D.Nonempty) {tau : Real}
    (hle : maxCosine h D hD <= tau) : regretHinge h D hD tau = 0 :=
  relu_eq_zero_of_nonpos (sub_nonpos.mpr hle)

/-- Combined scalar objective. `L_task` is an opaque real. -/
def totalLoss (task lambda hinge : Real) : Real := task + lambda * hinge

lemma totalLoss_zero_weight (task hinge : Real) : totalLoss task 0 hinge = task := by
  simp [totalLoss]

/-! ## Learning-theoretic external regret

A strategy is causal: a_t depends on ell_0, ..., ell_{t-1} only.
-/

variable {A : Type*} [Fintype A] [Nonempty A]

/-- Past loss table of length `t`. -/
abbrev LossPrefix (A : Type*) (t : Nat) := Fin t -> A -> Real

/-- Causal strategy: a_t = sigma t (prefix of length t). -/
abbrev CausalStrategy (A : Type*) :=
  (t : Nat) -> LossPrefix A t -> A

/-- Action at time t: prefix is ell restricted to Fin t. -/
def playAt (sigma : CausalStrategy A) (ell : Nat -> A -> Real) (t : Nat) : A :=
  sigma t (fun i => ell i.val)

def playOf (sigma : CausalStrategy A) (ell : Nat -> A -> Real) : Nat -> A :=
  playAt sigma ell

def cumulativeLoss (ell : Nat -> A -> Real) (T : Nat) (act : A) : Real :=
  (Finset.range T).sum (fun t => ell t act)

def bestComparatorLoss (ell : Nat -> A -> Real) (T : Nat) : Real :=
  Finset.univ.inf' Finset.univ_nonempty (cumulativeLoss ell T)

def playLoss (ell : Nat -> A -> Real) (act : Nat -> A) (T : Nat) : Real :=
  (Finset.range T).sum (fun t => ell t (act t))

def externalRegret (ell : Nat -> A -> Real) (act : Nat -> A) (T : Nat) : Real :=
  playLoss ell act T - bestComparatorLoss ell T

/-- Hannan consistency: average external regret of the *causal* play -> 0. -/
def hannanConsistent (sigma : CausalStrategy A) : Prop :=
  forall ell : Nat -> A -> Real,
    Tendsto (fun T : Nat =>
      externalRegret ell (playOf sigma ell) T.succ / (T.succ : Real)) atTop (nhds 0)

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
  loss : Nat -> A -> Real
  play : Nat -> A
  horizon : Nat

noncomputable def IntentHingeData.value (p : IntentHingeData) : Real :=
  regretHinge p.readout p.bank p.bank_nonempty p.threshold

def ExternalRegretData.value (p : ExternalRegretData) : Real :=
  externalRegret p.loss p.play p.horizon

end RegretHeuristic
