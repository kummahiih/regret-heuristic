/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Scoreboard for a strategy camera. Bookkeeping only.
GPU gaps are not theorems. Do not fill D from a hint.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace CameraGates

/-- Fit / transfer speech act. Bank frame may vote. -/
inductive FileSort where
  | bankFrame
  | voiceLog
deriving DecidableEq, Repr

/-- A topic name on the chart. Hiking is a cell, not a hole to delete. -/
inductive Room where
  | hiking
  | invoices
  | travel
  | neighbors
  | other
deriving DecidableEq, Repr

/-- Print vs fact. Generated reply only. Not a pair tag. -/
inductive ReplyKind where
  | truth
  | contradict
  | evade
  | refuse
  | insufficient
deriving DecidableEq, Repr

/-- Four official gates. All must hold on the declared room set. -/
structure Gates where
  planLOTO : Bool
  topicChance : Bool
  paraphrase : Bool
  roomsUniform : Bool

def cameraPass (g : Gates) : Bool :=
  g.planLOTO && g.topicChance && g.paraphrase && g.roomsUniform

/-- Search hint: plan and paraphrase without claiming rooms or topic. -/
def hint (g : Gates) : Bool :=
  g.planLOTO && g.paraphrase

theorem hint_not_handover :
    let g : Gates :=
      { planLOTO := true, topicChance := true, paraphrase := true, roomsUniform := false }
    hint g = true ∧ cameraPass g = false := by
  native_decide

theorem cameraPass_needs_rooms :
    ∀ g : Gates, g.roomsUniform = false → cameraPass g = false := by
  intro g h
  simp [cameraPass, h]

/-- A voter file is bank-frame. Office-log / radio does not vote. -/
def mayVote (s : FileSort) : Bool :=
  match s with
  | .bankFrame => true
  | .voiceLog => false

theorem voice_not_a_voter : mayVote .voiceLog = false := rfl

theorem bank_frame_may_vote : mayVote .bankFrame = true := rfl

theorem genre_not_paraphrase : FileSort.voiceLog ≠ FileSort.bankFrame := by
  decide

/-- Declared chart. Dropping a thin room is a different predicate. -/
def roomsUniformOn (S : List Room) (thin : List Room) : Bool :=
  thin.all (fun r => !S.contains r)

theorem eight_with_hiking_thin :
    roomsUniformOn [.hiking, .invoices, .travel, .neighbors] [.hiking] = false := by
  native_decide

theorem seven_without_hiking :
    roomsUniformOn [.invoices, .travel, .neighbors] [.hiking] = true := by
  native_decide

theorem seven_is_not_eight :
    roomsUniformOn [.hiking, .invoices, .travel, .neighbors] [.hiking] ≠
      roomsUniformOn [.invoices, .travel, .neighbors] [.hiking] := by
  native_decide

/-- Unit-sum of three views is one readout slot. -/
structure ThreeViews where
  last : ℝ
  kstep : ℝ
  siren : ℝ

def mid3 (v : ThreeViews) : ℝ := v.last + v.kstep + v.siren

def oneSlot (_r : ℝ) : Unit := ()

theorem mid3_is_one_slot (v w : ThreeViews) :
    oneSlot (mid3 v) = oneSlot (mid3 w) := rfl

/-- Talker-count may differ; the gate product does not read it. -/
theorem source_count_not_a_gate (g : Gates) (_m _n : Nat) :
    cameraPass g = cameraPass g := rfl

/-- Print meter may differ; cameraPass does not read it. -/
def cameraPassIgnoringReply (g : Gates) (_k : ReplyKind) : Bool := cameraPass g

theorem reply_kind_not_a_gate (g : Gates) (k k' : ReplyKind) :
    cameraPassIgnoringReply g k = cameraPassIgnoringReply g k' := rfl

/-- Own-room hold may be loud while roomsUniform is false. -/
def cameraPassIgnoringHold (g : Gates) (_heldInRoom : Bool) : Bool := cameraPass g

theorem inroom_hold_not_a_gate (g : Gates) (a b : Bool) :
    cameraPassIgnoringHold g a = cameraPassIgnoringHold g b := rfl

theorem loud_hold_not_rooms :
    let g : Gates :=
      { planLOTO := true, topicChance := true, paraphrase := true, roomsUniform := false }
    cameraPassIgnoringHold g true = false := by
  native_decide

end CameraGates
