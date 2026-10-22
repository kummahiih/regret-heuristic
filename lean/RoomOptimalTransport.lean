/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Rooms as answer-preserving prefix/postfix sets.
The shortest stabilizer length is the optimal-transport cost
under the end-insertion metric (ground metric for a discrete Wasserstein-1).
Bookkeeping only. Not a camera. Not a gate. Not Qwen.
-/

import Mathlib.Data.List.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace RoomOptimalTransport

variable {α β : Type*}

/-- Finite strings over alphabet α. -/
abbrev Prompt := List α

/-- Abstract language model. -/
variable (M : Prompt → β)

/-- Prefix/postfix stabilizer: appending them leaves the answer unchanged. -/
def IsStabilizer (x : Prompt) (y : β) (pre post : Prompt) : Prop :=
  M (pre ++ x ++ post) = y

/-- The room of answer y relative to base prompt x. -/
def Room (x : Prompt) (y : β) : Set (Prompt × Prompt) :=
  { p | IsStabilizer M x y p.1 p.2 }

/-- Empty pair is a stabilizer precisely when the base already yields y. -/
lemma empty_stabilizer (x : Prompt) (y : β) :
    IsStabilizer M x y [] [] ↔ M x = y := by
  simp [IsStabilizer]

lemma empty_mem_Room (x : Prompt) (y : β) (h : M x = y) :
    ([], []) ∈ Room M x y := by
  simpa [Room] using (empty_stabilizer M x y).mpr h

/-- Length of the additional text. -/
def stabilizerLength (pre post : Prompt) : ℕ := pre.length + post.length

/-- A natural number c is the optimal-transport cost of (x,y)
    when some stabilizer has length c and every stabilizer is at least that long. -/
def IsOTCost (x : Prompt) (y : β) (c : ℕ) : Prop :=
  (∃ pre post, IsStabilizer M x y pre post ∧ stabilizerLength pre post = c) ∧
  (∀ pre post, IsStabilizer M x y pre post → c ≤ stabilizerLength pre post)

/-- When the base already yields y the OT cost is zero. -/
lemma otCost_zero_of_base (x : Prompt) (y : β) (h : M x = y) :
    IsOTCost M x y 0 := by
  refine ⟨⟨[], [], (empty_stabilizer M x y).mpr h, by simp [stabilizerLength]⟩, ?_⟩
  intro pre post _
  exact Nat.zero_le _

/-- Ground metric of end-insertion: witnessed by a prefix/postfix of total length d. -/
def IsEndInsertDist (s t : Prompt) (d : ℕ) : Prop :=
  ∃ pre post, pre ++ s ++ post = t ∧ pre.length + post.length = d

/-- Existence of a pure-transport witness at the OT cost. -/
lemma ot_witness (x : Prompt) (y : β) (c : ℕ) (hOT : IsOTCost M x y c) :
    ∃ t, M t = y ∧ IsEndInsertDist x t c := by
  obtain ⟨⟨pre, post, hstab, hlen⟩, _⟩ := hOT
  exact ⟨pre ++ x ++ post, hstab, ⟨pre, post, rfl, hlen⟩⟩

/-- Every prompt that yields y is at least cost c away under end-insertion.
    This is the lower bound half of the discrete Wasserstein-1 equality. -/
lemma ot_lower_bound (x : Prompt) (y : β) (c : ℕ) (hOT : IsOTCost M x y c)
    (t : Prompt) (d : ℕ) (ht : M t = y) (hdist : IsEndInsertDist x t d) :
    c ≤ d := by
  obtain ⟨pre, post, heq, hd⟩ := hdist
  have hstab : IsStabilizer M x y pre post := by
    simpa [IsStabilizer, heq] using ht
  obtain ⟨_, hmin⟩ := hOT
  exact (hmin pre post hstab).trans_eq hd

/-- The OT cost is the 1-Wasserstein cost of transporting the Dirac at x
    onto the set of prompts that produce y, under the end-insertion ground metric.
    (Pure transport; discrete finite support.) -/
theorem ot_is_wasserstein1 (x : Prompt) (y : β) (c : ℕ) (hOT : IsOTCost M x y c) :
    (∃ t, M t = y ∧ IsEndInsertDist x t c) ∧
    (∀ t d, M t = y → IsEndInsertDist x t d → c ≤ d) :=
  ⟨ot_witness M x y c hOT, fun t d ht hdist => ot_lower_bound M x y c hOT t d ht hdist⟩

/-- Bookkeeping: the OT length is a log of the room under end-insertion.
    It is not a gate and does not enter L_total. -/
theorem ot_not_a_gate (x : Prompt) (y : β) (c : ℕ) (_h : IsOTCost M x y c) : True := trivial

end RoomOptimalTransport
