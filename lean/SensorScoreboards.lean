/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Two scoreboards on the same pair (topic, plan).
A loud probe is not a causal slap. A head write ignores the rest.
Not a camera. Not an SAE. Not Pandey.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace SensorScoreboards

/-- Wallpaper coordinate. What a linear probe can read. -/
def probeScore (topic _plan : Real) : Real := |topic|

/-- Plan coordinate. What a patch would have to move. -/
def causalScore (_topic plan : Real) : Real := |plan|

/-- Same hallway cell. Probe shouts. Causal meter is silent. -/
theorem decodable_not_causal :
    probeScore (1 : Real) 0 = 1 ∧ causalScore (1 : Real) 0 = 0 := by
  constructor
  · simp [probeScore]
  · simp [causalScore]

/-- The other cell: probe silent, causal loud. -/
theorem causal_not_from_probe :
    probeScore (0 : Real) 1 = 0 ∧ causalScore (0 : Real) 1 = 1 := by
  constructor
  · simp [probeScore]
  · simp [causalScore]

/-- Function-vector cartoon: r is the head write. Rest of h can change. -/
def headWrite (head _rest : Real) : Real := head

lemma headWrite_ignores_rest (head rest rest' : Real) :
    headWrite head rest = headWrite head rest' := rfl

theorem head_write_not_the_hallway :
    headWrite (0 : Real) 1 = 0 ∧ headWrite (0 : Real) (-1) = 0 := by
  constructor <;> simp [headWrite]

end SensorScoreboards
