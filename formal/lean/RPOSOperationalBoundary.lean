namespace RPOS

/-- Sources that may appear around an RPOS operation. This is a deliberately
small teaching model: source classification is not the full runtime policy. -/
inductive OperationalSource where
  | modelProposal
  | humanAuthorization
  | transportReceipt
  | externalObservation
  deriving DecidableEq, Repr

/-- Only an explicit authorization source is authorization-relevant in this
bounded model. A model proposal is advisory input, not authority. -/
def authorizationRelevant : OperationalSource → Bool
  | .humanAuthorization => true
  | _ => false

/-- Only an external observation is effect-verification-relevant in this
bounded model. A model report or transport receipt is not proof of effect. -/
def effectVerificationRelevant : OperationalSource → Bool
  | .externalObservation => true
  | _ => false

/-- Product boundary: model proposals do not grant operational authority. -/
theorem model_proposal_is_not_authority :
    authorizationRelevant .modelProposal = false := by
  rfl

/-- Product boundary: a model proposal does not verify an external effect. -/
theorem model_proposal_is_not_effect_verification :
    effectVerificationRelevant .modelProposal = false := by
  rfl

/-- Product boundary: a transport receipt does not verify an external effect. -/
theorem receipt_is_not_effect_verification :
    effectVerificationRelevant .transportReceipt = false := by
  rfl

/-- Positive witness: explicit human authorization is authorization-relevant
in this bounded classification. Possessing such evidence does not itself model
all runtime admission checks. -/
theorem human_authorization_is_authorization_relevant :
    authorizationRelevant .humanAuthorization = true := by
  rfl

/-- Positive witness: external observation is the bounded source accepted as
external-effect-verification-relevant. This theorem does not prove that an
arbitrary observation is truthful or sufficient in a concrete adapter. -/
theorem external_observation_is_effect_verification_relevant :
    effectVerificationRelevant .externalObservation = true := by
  rfl

/-- A read-only product surface has no transition constructor in this bounded
model. Mutation-capable commands are kept distinct from observation. -/
inductive ProductCommand where
  | observe
  | requestAuthorization
  | dispatch
  | reconcile
  | resume
  deriving DecidableEq, Repr

/-- Whether a product command is allowed to request mutation of operational
state. This is a capability classification, not a complete authorization
policy. -/
def requestsMutation : ProductCommand → Bool
  | .observe => false
  | _ => true

/-- Product boundary: observability is read-only in the bounded command model. -/
theorem observatory_is_read_only : requestsMutation .observe = false := by
  rfl

end RPOS
