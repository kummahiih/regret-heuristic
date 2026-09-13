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

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Cosine similarity. Undefined-as-a-bound when either vector is 0. -/
noncomputable def cosineSim (u v : E) : ℝ :=
  inner u v / (‖u‖ * ‖v‖)

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
  simpa [inner_neg_left, norm_neg] using h

/-- Worst-case cosine of a readout against a nonempty bank. -/
noncomputable def maxCosine (h : E) (D : Finset E) (hD : D.Nonempty) : ℝ :=
  D.sup' hD (fun d => cosineSim h d)

def relu (x : ℝ) : ℝ := max x 0

lemma relu_nonneg (x : ℝ) : 0 ≤ relu x := le_max_right _ _

lemma relu_eq_zero_of_nonpos {x : ℝ} (hx : x ≤ 0) : relu x = 0 :=
  max_eq_right hx

/-- Per-example hinge: `ReLU(s⋆(x) - τ)`. Instantaneous; no comparator. -/
noncomputable def regretHinge (h : E) (D : Finset E) (hD : D.Nonempty) (τ : ℝ) : ℝ :=
  relu (maxCosine h D hD - τ)

lemma regretHinge_nonneg (h : E) (D : Finset E) (hD : D.Nonempty) (τ : ℝ) :
    0 ≤ regretHinge h D hD τ :=
  relu_nonneg _

lemma regretHinge_eq_zero_of_le (h : E) (D : Finset E) (hD : D.Nonempty) {τ : ℝ}
    (hle : maxCosine h D hD ≤ τ) : regretHinge h D hD τ = 0 :=
  relu_eq_zero_of_nonpos (sub_nonpos.mpr hle)

/-- Combined scalar objective. `L_task` is an opaque real (cross-entropy, etc.). -/
def totalLoss (task λ hinge : ℝ) : ℝ := task + λ * hinge

lemma totalLoss_zero_weight (task hinge : ℝ) : totalLoss task 0 hinge = task := by
  simp [totalLoss]

/-! ## Learning-theoretic external regret (regret_minimization.md)

Different object from `regretHinge`: cumulative loss versus the best fixed
action in hindsight.

A strategy is **causal** (online): the action at time `t` may depend on
`ℓ 0, …, ℓ (t-1)` only. It must not see `ℓ t` or any future round.
The old type `(ℕ → A → ℝ) → ℕ → A` was clairvoyant and is not used.
-/

variable {A : Type*} [Fintype A] [Nonempty A]

/-- Past loss table of length `t`: index `i : Fin t` is `ℓ i`. -/
abbrev LossPrefix (A : Type*) (t : ℕ) := Fin t → A → ℝ

/-- Causal strategy: `a_t = σ t (prefix of length t)`. -/
abbrev CausalStrategy (A : Type*) :=
  (t : ℕ) → LossPrefix A t → A

/-- Unroll a causal strategy against a full loss sequence. -/
def play (t : ℕ) (σ : CausalStrategy A) (ℓ : ℕ → A → ℝ) : A :=
  σ t (fun i => ℓ i.val)

def cumulativeLoss (ℓ : ℕ → A → ℝ) (T : ℕ) (act : A) : ℝ :=
  ∑ t ∈ Finset.range T, ℓ t act

def bestComparatorLoss (ℓ : ℕ → A → ℝ) (T : ℕ) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty (cumulativeLoss ℓ T)

def playLoss (ℓ : ℕ → A → ℝ) (act : ℕ → A) (T : ℕ) : ℝ :=
  ∑ t ∈ Finset.range T, ℓ t (act t)

def externalRegret (ℓ : ℕ → A → ℝ) (act : ℕ → A) (T : ℕ) : ℝ :=
  playLoss ℓ act T - bestComparatorLoss ℓ T

/-- Hannan consistency for a *causal* strategy: average external regret
    → 0 along `T = 1, 2, …`, for every loss sequence. -/
def hannanConsistent (σ : CausalStrategy A) : Prop :=
  ∀ ℓ : ℕ → A → ℝ,
    Tendsto (fun T : ℕ =>
      externalRegret ℓ (σ.play ℓ) T.succ / (T.succ : ℝ)) atTop (𝐡 0)

/-- Dot notation: `(σ.play ℓ) t = play t σ ℓ`. -/
def CausalStrategy.play (σ : CausalStrategy A) (ℓ : ℕ → A → ℝ) : ℕ → A :=
  fun t => play t σ ℓ

/-! ## PPO clip as a real function (ppo_integration.md)

Attachment of the hinge is additive: `L_PPO + λ L_regret`. No trust-region
theorem is claimed after that sum.
-/

def clipInterval (x lo hi : ℝ) : ℝ := max lo (min x hi)

/-- `min(r Â, clip(r, 1-ε, 1+ε) Â)` on scalars. -/
def clippedSurrogate (rAdv ε adv : ℝ) : ℝ :=
  min (rAdv * adv) (clipInterval rAdv (1 - ε) (1 + ε) * adv)

def ppoWithHinge (ppo λ hinge : ℝ) : ℝ := ppo + λ * hinge

lemma ppoWithHinge_zero_weight (ppo hinge : ℝ) : ppoWithHinge ppo 0 hinge = ppo := by
  simp [ppoWithHinge]

/-- The two "regrets" are different types of data.
    An intent hinge has no time index and no comparator action. -/
structure IntentHingeData where
  readout : E
  bank : Finset E
  bank_nonempty : bank.Nonempty
  threshold : ℝ

structure ExternalRegretData where
  loss : ℕ → A → ℝ
  play : ℕ → A
  horizon : ℕ

noncomputable def IntentHingeData.value (p : IntentHingeData) : ℝ :=
  regretHinge p.readout p.bank p.bank_nonempty p.threshold

def ExternalRegretData.value (p : ExternalRegretData) : ℝ :=
  externalRegret p.loss p.play p.horizon

end RegretHeuristic
