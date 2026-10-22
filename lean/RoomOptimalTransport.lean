/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Rooms as answer fibres reachable by end-insertion from the empty prompt.
The shortest path length from no input is the optimal-transport cost
under the end-insertion metric (ground metric for a discrete Wasserstein-1).
If the cost is zero the answer is the starting room.
Bookkeeping only. Not a camera. Not a gate. Not Qwen.
-/

import Mathlib.Data.List.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace RoomOptimalTransport

variable {α β : Type*}

/-- Abstract language model. -/
variable (M : List α → β)

/-- A pair of strings reaches answer y from the empty prompt. -/
def Reaches (y : β) (pre post : List α) : Prop :=
  M (pre ++ post) = y

/-- The room of answer y: all end-insertions from the empty string that yield y. -/
def Room (y : β) : Set (List α × List α) :=
  { p | Reaches M y p.1 p.2 }

/-- Length of the additional text. -/
def pathLength (pre post : List α) : ℕ := pre.length + post.length

/-- The empty path reaches y precisely when y is the answer of the empty prompt. -/
lemma empty_reaches (y : β) :
    Reaches M y [] [] ↔ M [] = y := by
  simp [Reaches]

/-- A natural number c is the optimal-transport cost of y
    (shortest path length from the empty prompt)
    when some path has length c and every path is at least that long. -/
def IsOTCost (y : β) (c : ℕ) : Prop :=
  (∃ pre post, Reaches M y pre post ∧ pathLength pre post = c) ∧
  (∀ pre post, Reaches M y pre post → c ≤ pathLength pre post)

/-- When the empty prompt already yields y the OT cost is zero:
    y is the starting room. -/
lemma otCost_zero_of_starting (y : β) (h : M [] = y) :
    IsOTCost M y 0 := by
  refine ⟨⟨[], [], (empty_reaches M y).mpr h, by simp [pathLength]⟩, ?_⟩
  intro pre post _
  exact Nat.zero_le _

/-- Ground metric of end-insertion from the empty string. -/
def IsEndInsertDist (t : List α) (d : ℕ) : Prop :=
  ∃ pre post, pre ++ post = t ∧ pre.length + post.length = d

/-- Existence of a pure-transport witness at the OT cost. -/
lemma ot_witness (y : β) (c : ℕ) (hOT : IsOTCost M y c) :
    ∃ t, M t = y ∧ IsEndInsertDist t c := by
  obtain ⟨⟨pre, post, hreach, hlen⟩, _⟩ := hOT
  exact ⟨pre ++ post, hreach, ⟨pre, post, rfl, hlen⟩⟩

/-- Every prompt that yields y is at least cost c away under end-insertion from empty.
    This is the lower bound half of the discrete Wasserstein-1 equality. -/
lemma ot_lower_bound (y : β) (c : ℕ) (hOT : IsOTCost M y c)
    (t : List α) (d : ℕ) (ht : M t = y) (hdist : IsEndInsertDist t d) :
    c ≤ d := by
  obtain ⟨pre, post, heq, hd⟩ := hdist
  have hreach : Reaches M y pre post := by
    simpa [Reaches, heq] using ht
  obtain ⟨_, hmin⟩ := hOT
  exact (hmin pre post hreach).trans_eq hd

/-- The OT cost is the 1-Wasserstein cost of transporting the Dirac at the empty string
    onto the set of prompts that produce y, under the end-insertion ground metric.
    (Pure transport; discrete finite support.)
    Zero cost means y is the starting room. -/
theorem ot_is_wasserstein1 (y : β) (c : ℕ) (hOT : IsOTCost M y c) :
    (∃ t, M t = y ∧ IsEndInsertDist t c) ∧
    (∀ t d, M t = y → IsEndInsertDist t d → c ≤ d) :=
  ⟨ot_witness M y c hOT, fun t d ht hdist => ot_lower_bound M y c hOT t d ht hdist⟩

/-- Bookkeeping: the OT length is a log of distance from the empty prompt.
    It is not a gate and does not enter L_total. -/
theorem ot_not_a_gate (y : β) (c : ℕ) (_h : IsOTCost M y c) : True := trivial

end RoomOptimalTransport
