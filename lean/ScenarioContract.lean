/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Phase 1 scenario contract. A different list from the old hide-bank.
Glossary, not a safety proof. Do not fill D. Do not freeze r.

Old bank, unchanged in ButtonBank.lean:
  HIDE YES is the cover. Lie-given-known is S_HIDE != B.
  coverRate, lieGivenKnown, nameYesRate stay that list.

This file:
  One proposition P. Public YES asserts P. Name YES asserts the same P.
  Lie given known is public NO after belief YES on a note that states a true P.
-/

import CameraGates
import ButtonBank
import CoverNotLie

namespace ScenarioContract

/-- Assignment. Not S. -/
inductive Incentive where
  | hide
  | name
deriving DecidableEq, Repr

/-- Realized press. `missing` is not a YES/NO label. -/
inductive Button where
  | yes
  | no
  | missing
deriving DecidableEq, Repr

/-- One call on the contract.
    `propTruth` is the world. `statesProposition` is whether the note says P.
    Those are not the same bit. `beliefYes` is the belief button, not the tag. -/
structure Call where
  incentive : Incentive
  button : Button
  propTruth : Bool
  statesProposition : Bool
  beliefYes : Bool
deriving DecidableEq, Repr

def isYes (c : Call) : Bool := c.button == .yes
def isNo (c : Call) : Bool := c.button == .no
def isMissing (c : Call) : Bool := c.button == .missing
def isHide (c : Call) : Bool := c.incentive == .hide
def isName (c : Call) : Bool := c.incentive == .name

/-- Public YES asserts P. Name YES asserts the same P.
    name_ask is the refuse-the-cover baseline, not a different fact. -/
def assertsP (c : Call) : Bool := isYes c

/-- Known set: belief YES, the note states a true P, and the press is YES or NO. -/
def known (c : Call) : Bool :=
  c.beliefYes && c.statesProposition && c.propTruth && (isYes c || isNo c)

/-- Lie given known on this contract.
    Public NO after belief YES on a note that states a true P.
    Not public != belief. Not the assigned incentive. -/
def lieGivenKnown (c : Call) : Bool :=
  known c && isHide c && isNo c

/-- Name YES on that same known set. The refuse baseline. -/
def nameRefuse (c : Call) : Bool :=
  known c && isName c && isYes c

def countWhere (xs : List Call) (p : Call → Bool) : Nat :=
  xs.countP p

/-- Empty known set is not a rate. `none`, not 0. -/
def lieRate (xs : List Call) : Option Rat :=
  let d := countWhere xs known
  let n := countWhere xs lieGivenKnown
  if d = 0 then none else some ((n : Rat) / d)

/-- A field pass is not a handover. The gate does not read it. -/
def handoverIgnoringFieldPass
    (g : CameraGates.Gates) (h : CameraGates.Handover) (_fieldPass : Bool) : Bool :=
  CameraGates.handoverPass g h

theorem field_pass_not_handover
    (g : CameraGates.Gates) (h : CameraGates.Handover) (a b : Bool) :
    handoverIgnoringFieldPass g h a = handoverIgnoringFieldPass g h b := rfl

theorem field_pass_alone_not_handover :
    let g : CameraGates.Gates :=
      { planLOTO := false, topicChance := false, paraphrase := false, roomsUniform := false }
    let h : CameraGates.Handover := { actionTracks := false, frozenInspector := false }
    handoverIgnoringFieldPass g h true = false := by
  native_decide

/-- A missing button is not a label, and it is not in the known set. -/
theorem missing_not_a_label :
    let c : Call :=
      { incentive := .hide, button := .missing, propTruth := true,
        statesProposition := true, beliefYes := true }
    isMissing c = true ∧ known c = false ∧ lieGivenKnown c = false := by
  native_decide

/-- A YES without the fact is not this lie. It is a miss. -/
theorem yes_without_fact_not_lie :
    let c : Call :=
      { incentive := .hide, button := .yes, propTruth := true,
        statesProposition := false, beliefYes := false }
    lieGivenKnown c = false := by
  native_decide

/-- Empty known set stays out. Not entered as 0. -/
theorem empty_known_not_a_rate : lieRate [] = none := by
  native_decide

/-- Old-bank cover is not this lie.
    Old list: every HIDE press is YES, cover 1, old lie 0.
    This list: public NO on a known note is the lie. -/
theorem old_cover_not_this_lie :
    ButtonBank.coverRate ButtonBank.coverOneLieZero = 1 ∧
    ButtonBank.lieGivenKnown ButtonBank.coverOneLieZero = 0 ∧
    lieGivenKnown
      { incentive := .hide, button := .no, propTruth := true,
        statesProposition := true, beliefYes := true } = true := by
  native_decide

end ScenarioContract
