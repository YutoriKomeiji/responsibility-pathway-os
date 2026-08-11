-- Copyright (c) 2026 Akihisa Ono
-- SPDX-License-Identifier: MIT
-- RPOS-SOURCE-LANG: en
import RPOSState

namespace RPOS

/-- Reflexive-transitive closure of the normative direct transition relation. -/
inductive Steps : State → State → Prop where
  | refl (state : State) : Steps state state
  | tail {source middle target : State} :
      Step source middle → Steps middle target → Steps source target

/-- AUTHORIZED can reach DISPATCHING through the normative transition. -/
theorem authorized_reaches_dispatching : Steps .authorized .dispatching := by
  exact Steps.tail Step.authorizedToDispatching (Steps.refl .dispatching)

/-- EFFECT_UNKNOWN can reach COMPLETED only along an explicitly modeled
verification path in this witness. This is an existence theorem, not a claim
that every EFFECT_UNKNOWN execution eventually completes. -/
theorem effect_unknown_has_verified_completion_path :
    Steps .effectUnknown .completed := by
  exact Steps.tail Step.effectUnknownToVerified
    (Steps.tail Step.verifiedToCompleted (Steps.refl .completed))

/-- A repair cycle can return to AUTHORIZED only after READY_TO_RESUME in this
normative witness. This theorem establishes the modeled path, not liveness. -/
theorem repair_has_explicit_reauthorization_path :
    Steps .repairRequired .authorized := by
  exact Steps.tail Step.repairRequiredToReadyToResume
    (Steps.tail Step.readyToResumeToAuthorized (Steps.refl .authorized))

/-- EFFECT_UNKNOWN cannot directly become COMPLETED. -/
theorem effect_unknown_cannot_complete_directly :
    ¬ Step .effectUnknown .completed := by
  intro h
  cases h

/-- REPAIR_REQUIRED cannot directly become DISPATCHING. -/
theorem repair_required_cannot_dispatch_directly :
    ¬ Step .repairRequired .dispatching := by
  intro h
  cases h

/-- READY_TO_RESUME cannot directly become COMPLETED. -/
theorem ready_to_resume_cannot_complete_directly :
    ¬ Step .readyToResume .completed := by
  intro h
  cases h

/-- READY_TO_RESUME has an explicit authorization-restoration path whose first
step is AUTHORIZED rather than DISPATCHING. -/
theorem ready_to_resume_restores_authority :
    Step .readyToResume .authorized := by
  exact Step.readyToResumeToAuthorized

end RPOS
