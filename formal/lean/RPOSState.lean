namespace RPOS

/-- Responsibility-relevant states in the RPOS v0.1 normative model. -/
inductive State where
  | proposed
  | humanGate
  | authorized
  | dispatching
  | effectUnknown
  | verified
  | repairRequired
  | readyToResume
  | completed
  | denied
  | aborted
  deriving DecidableEq, Repr

/-- Normative direct transition relation for RPOS v0.1. -/
inductive Step : State → State → Prop where
  | proposedToHumanGate : Step .proposed .humanGate
  | proposedToAuthorized : Step .proposed .authorized
  | proposedToDenied : Step .proposed .denied
  | humanGateToAuthorized : Step .humanGate .authorized
  | humanGateToDenied : Step .humanGate .denied
  | authorizedToDispatching : Step .authorized .dispatching
  | dispatchingToVerified : Step .dispatching .verified
  | dispatchingToEffectUnknown : Step .dispatching .effectUnknown
  | dispatchingToRepairRequired : Step .dispatching .repairRequired
  | effectUnknownToVerified : Step .effectUnknown .verified
  | effectUnknownToRepairRequired : Step .effectUnknown .repairRequired
  | verifiedToCompleted : Step .verified .completed
  | repairRequiredToReadyToResume : Step .repairRequired .readyToResume
  | readyToResumeToAuthorized : Step .readyToResume .authorized

/-- INV-AUTH-001: only AUTHORIZED may directly enter DISPATCHING. -/
theorem only_authorized_enters_dispatching {source : State}
    (h : Step source .dispatching) : source = .authorized := by
  cases h
  rfl

/-- INV-GATE-001: HUMAN_GATE cannot directly enter DISPATCHING. -/
theorem human_gate_cannot_dispatch_directly : ¬ Step .humanGate .dispatching := by
  intro h
  cases h

/-- INV-COMPLETE-001: only VERIFIED may directly enter COMPLETED. -/
theorem only_verified_enters_completed {source : State}
    (h : Step source .completed) : source = .verified := by
  cases h
  rfl

/-- INV-REPAIR-001: REPAIR_REQUIRED cannot skip repair preparation and become AUTHORIZED. -/
theorem repair_required_cannot_authorize_directly : ¬ Step .repairRequired .authorized := by
  intro h
  cases h

/-- INV-RESUME-001: READY_TO_RESUME and AUTHORIZED are distinct states. -/
theorem ready_to_resume_is_not_authorized :
    State.readyToResume ≠ State.authorized := by
  decide

/-- INV-RESUME-002: resume changes READY_TO_RESUME to AUTHORIZED, not DISPATCHING. -/
theorem resume_does_not_dispatch_directly : ¬ Step .readyToResume .dispatching := by
  intro h
  cases h

/-- INV-UNKNOWN-001: EFFECT_UNKNOWN is not a completed state. -/
theorem effect_unknown_is_not_completed :
    State.effectUnknown ≠ State.completed := by
  decide

end RPOS
