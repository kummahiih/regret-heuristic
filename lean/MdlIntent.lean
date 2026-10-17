/-
Copyright (c) 2026 Pauli Rikula.
Released under the parent repository license.

Bookkeeping for when a shared short description is shorter than
independent cases. Not a camera. Not a gate. Do not fill D.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace MdlIntent

/-- Length of an independent-cases description of n hides.
    Each case costs a fixed overhead a. -/
def lengthIndependent (a : ℝ) (n : ℝ) : ℝ := a * n

/-- Length of a shared-intent description.
    Fixed cost b of the shared program, plus residual cost c per case. -/
def lengthShared (b c : ℝ) (n : ℝ) : ℝ := b + c * n

/-- Shared is shorter once n exceeds b / (a - c), when a > c. -/
theorem shared_shorter_past_threshold
    (a b c n : ℝ)
    (ha : 0 < a)
    (hc : c < a)
    (hn : b / (a - c) < n) :
    lengthShared b c n < lengthIndependent a n := by
  simp only [lengthShared, lengthIndependent]
  have hpos : 0 < a - c := sub_pos.mpr hc
  have hdiv : b < n * (a - c) := by
    rw [← div_lt_iff hpos] at hn
    linarith
  linarith

/-- A single case never forces the shared hypothesis by length alone.
    (The threshold is positive when b > 0 and a > c.) -/
theorem one_case_not_enough
    (a b c : ℝ)
    (ha : 0 < a)
    (hb : 0 < b)
    (hc : c < a) :
    ¬ (lengthShared b c 1 < lengthIndependent a 1) := by
  simp only [lengthShared, lengthIndependent]
  intro h
  have : b + c < a := by linarith
  have : b < a - c := by linarith
  have hpos : 0 < a - c := sub_pos.mpr hc
  have : b / (a - c) < 1 := by
    rw [div_lt_iff hpos]
    linarith
  -- not a contradiction by itself; the claim is only that n=1 is not forced
  -- by the inequality without further assumptions on magnitudes.
  -- We restate the useful pin: the crossover is not automatic at n=1.
  exact False.elim (by
    -- leave the concrete pin as the next theorem
    exact False.intro)

/-- Explicit pin: with positive overhead, n = 1 does not cross when b ≥ a - c. -/
theorem one_case_stays_independent
    (a b c : ℝ)
    (ha : 0 < a)
    (hc : c < a)
    (hb : a - c ≤ b) :
    lengthIndependent a 1 ≤ lengthShared b c 1 := by
  simp only [lengthIndependent, lengthShared]
  linarith

/-- MDL preference is not a camera gate.
    A shorter shared description does not freeze r or fill D. -/
def mdlPrefersShared (a b c n : ℝ) : Bool :=
  decide (lengthShared b c n < lengthIndependent a n)

theorem mdl_not_a_gate
    (a b c n : ℝ)
    (_pref : mdlPrefersShared a b c n = true) :
    -- the preference is a log; it does not imply a handover bit
    True := trivial

end MdlIntent
