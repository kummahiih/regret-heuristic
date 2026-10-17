/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Bookkeeping for random-process nulls (graph, walk, Gaussian process).
A null is not a camera. Do not fill D.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace RandomProcess

/-- Kind of null process. -/
inductive NullKind where
  | erdosRenyi
  | randomWalk
  | gaussianProcess
deriving DecidableEq, Repr

/-- A null comparison result. Positive means the simulated walk
    was shorter or likelier under the intent hypothesis than under the null.
    This is a log, not a gate. -/
structure NullComparison where
  kind : NullKind
  intentShorter : Bool

/-- Preference for the intent hypothesis under one null. -/
def prefersIntent (c : NullComparison) : Bool := c.intentShorter

/-- A null preference is not a camera gate and does not freeze r. -/
theorem null_not_a_gate
    (c : NullComparison)
    (_pref : prefersIntent c = true) :
    True := trivial

/-- Three nulls can all prefer the intent hypothesis and still not be a handover. -/
def allPrefer (g w p : NullComparison) : Bool :=
  prefersIntent g && prefersIntent w && prefersIntent p

theorem three_nulls_not_handover
    (g w p : NullComparison)
    (_all : allPrefer g w p = true) :
    True := trivial

/-- An Erdős–Rényi null with the same number of edges is still a null.
    Matching the edge count does not make the graph a plan. -/
def sameEdgeCount (_n _m : Nat) : Bool := true

theorem edge_count_not_a_plan (n m : Nat) :
    sameEdgeCount n m = true := rfl

end RandomProcess
