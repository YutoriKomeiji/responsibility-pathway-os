/-!
# RPOS — Responsibility Pathway OS state invariants

This Lean 4 module machine-checks structural invariants of the executable
Responsibility Pathway OS (RPOS) state model.

The corresponding Python runtime implements the operational state machine;
this file independently proves selected properties of the declared abstract
model. In particular, it checks that Human Gate is not dispatch authority,
completion requires VERIFIED, EFFECT_UNKNOWN is distinct from completion,
and repair readiness does not silently become execution authority.

These theorems are formal assurance for the named invariants. They are not a
proof of the complete Python implementation, external systems, or the
legitimacy of any concrete authorization decision.
-/

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

/-- Machine-checked Human Gate invariant: HUMAN_GATE cannot directly enter
DISPATCHING, so a pending human decision is not execution authority. -/
theorem human_gate_cannot_dispatch_directly : ¬ Step .humanGate .dispatching := by
  intro h
  cases h

/-- Machine-checked completion invariant: only VERIFIED may directly enter
COMPLETED in the bounded RPOS state model. -/
theorem only_verified_enters_completed {source : State}
    (h : Step source .completed) : source = .verified := by
  cases h
  rfl

/-- INV-REPAIR-001: REPAIR_REQUIRED cannot skip repair preparation and become AUTHORIZED. -/
theorem repair_required_cannot_authorize_directly : ¬ Step .repairRequired .authorized := by
  intro h
  cases h

/-- Machine-checked resume-authority invariant: READY_TO_RESUME and AUTHORIZED
are distinct states. Repair readiness is not operational authority. -/
theorem ready_to_resume_is_not_authorized :
    State.readyToResume ≠ State.authorized := by
  decide

/-- INV-RESUME-002: resume changes READY_TO_RESUME to AUTHORIZED, not DISPATCHING. -/
theorem resume_does_not_dispatch_directly : ¬ Step .readyToResume .dispatching := by
  intro h
  cases h

/-- Machine-checked external-effect uncertainty invariant: EFFECT_UNKNOWN is
not COMPLETED. Ambiguous external effect is preserved instead of collapsed
into success. -/
theorem effect_unknown_is_not_completed :
    State.effectUnknown ≠ State.completed := by
  decide

end RPOS
