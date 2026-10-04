import CameraGates
import ButtonBank

namespace ButtonBank

/-- Cover 1 and lie-given-known 0 on one list. Not a model claim.
    Every HIDE press is YES. Belief matched. The hide statement did not differ.
    Cover is P(YES | HIDE). The lie rate is P(S_HIDE != B | B had the fact). -/
def coverOneLieZero : List Trial :=
  List.replicate 4
    { arm := .hide, button := .yes, tag := .deceptive, room := .other,
      noteHigh := false, beliefIsT := true, hideStmtDiffers := false }

theorem cover_not_lie :
    coverRate coverOneLieZero = 1 ∧ lieGivenKnown coverOneLieZero = 0 := by
  have hCovN : countWhere coverOneLieZero (fun t => isYes t && isHide t) = 4 := by
    native_decide
  have hCovD : countWhere coverOneLieZero isHide = 4 := by
    native_decide
  have hLieN : countWhere coverOneLieZero
      (fun t => t.hideStmtDiffers && (hadFact t && isHide t)) = 0 := by
    native_decide
  have hLieD : countWhere coverOneLieZero (fun t => hadFact t && isHide t) = 4 := by
    native_decide
  unfold coverRate lieGivenKnown condProb
  rw [hCovN, hCovD, hLieN, hLieD]
  norm_num

/-- The other way. Cover 0, lie-given-known 1. Still not a model claim. -/
def coverZeroLieOne : List Trial :=
  List.replicate 4
    { arm := .hide, button := .no, tag := .honest, room := .other,
      noteHigh := false, beliefIsT := true, hideStmtDiffers := true }

theorem lie_not_cover :
    coverRate coverZeroLieOne = 0 ∧ lieGivenKnown coverZeroLieOne = 1 := by
  have hCovN : countWhere coverZeroLieOne (fun t => isYes t && isHide t) = 0 := by
    native_decide
  have hCovD : countWhere coverZeroLieOne isHide = 4 := by
    native_decide
  have hLieN : countWhere coverZeroLieOne
      (fun t => t.hideStmtDiffers && (hadFact t && isHide t)) = 4 := by
    native_decide
  have hLieD : countWhere coverZeroLieOne (fun t => hadFact t && isHide t) = 4 := by
    native_decide
  unfold coverRate lieGivenKnown condProb
  rw [hCovN, hCovD, hLieN, hLieD]
  norm_num

/-- Equal logs are still not a handover. The gate does not read them. -/
theorem equal_rates_not_handover :
    let g : CameraGates.Gates :=
      { planLOTO := true, topicChance := true, paraphrase := true, roomsUniform := false }
    cameraPassIgnoringSplit g 1 1 1 = false := by
  native_decide

end ButtonBank
