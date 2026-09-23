/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

API cartoons. Not ML-KEM. Not a camera. Not z.
Implicit reject: decaps always returns a key.
Topic-blind: plan score ignores hallway.
Lexical bleed: patched walk still prints the source topic token.
-/

namespace ImplicitReject

def realKey (m c : Nat) : Nat := m + c

def fakeKey (z c : Nat) : Nat := z + c

/-- Hit uses m. Miss uses secret z. Both branches return Nat, never none. -/
def decaps (ok : Bool) (m z c : Nat) : Nat :=
  if ok then realKey m c else fakeKey z c

def explicitDecaps (ok : Bool) (m c : Nat) : Option Nat :=
  if ok then some (realKey m c) else none

theorem decaps_hit : decaps true 1 9 3 = realKey 1 3 := rfl

theorem decaps_miss : decaps false 1 9 3 = fakeKey 9 3 := rfl

theorem implicit_miss_is_some : decaps false 1 9 3 = 12 := rfl

theorem explicit_miss_is_none : explicitDecaps false 1 3 = none := rfl

/-- Plan coordinate. Wallpaper does not enter. -/
def sPlan (_topic plan : Nat) : Nat := plan

/-- Hallway coordinate. -/
def sTopic (topic _plan : Nat) : Nat := topic

theorem plan_score_ignores_topic (t t' p : Nat) :
    sPlan t p = sPlan t' p := rfl

/-- Classifier that only sees sPlan is constant in this toy. -/
def topicFromPlan (_s : Nat) : Nat := 0

theorem topic_from_plan_uninformative (t t' p : Nat) :
    topicFromPlan (sPlan t p) = topicFromPlan (sPlan t' p) := rfl

/-- Coincidence slice: the pair still names the hallway. Forbidden as r. -/
def coincidence (topic plan : Nat) : Nat × Nat := (plan, topic)

theorem coincidence_names_hallway :
    (coincidence 7 1).2 = 7 := rfl

inductive Token where
  | hike
  | stall

/-- Source topic token leaked into the patched walk. -/
def patchedWalk (bleed : Bool) : Token :=
  if bleed then Token.hike else Token.stall

theorem lexical_bleed : patchedWalk true = Token.hike := rfl

theorem topic_blind_patch : patchedWalk false = Token.stall := rfl

end ImplicitReject
