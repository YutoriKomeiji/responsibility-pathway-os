-- Copyright (c) 2026 Akihisa Ono
-- SPDX-License-Identifier: MIT
-- RPOS-SOURCE-LANG: en

namespace RPOS

/-- Bounded evidence classes used only to state separation properties.
This is not a complete operational evidence ontology. -/
inductive EvidenceClass where
  | authorityAdmission
  | executionReceipt
  | externalEffect
  | recoveryResume
  | safetyEvaluation
  | capabilityEvaluation
  | dependencySupplyChain
  deriving DecidableEq, Repr

/-- Evidence classes that may participate in an authorization decision in this
abstract model. Possessing such evidence does not itself grant authority. -/
inductive AuthorizationRelevant : EvidenceClass → Prop where
  | authorityAdmission : AuthorizationRelevant .authorityAdmission
  | recoveryResume : AuthorizationRelevant .recoveryResume

/-- Evidence class that may establish bounded external-effect verification in
this abstract model. -/
inductive EffectVerificationRelevant : EvidenceClass → Prop where
  | externalEffect : EffectVerificationRelevant .externalEffect

/-- Safety evaluation evidence cannot substitute for authorization evidence. -/
theorem safety_evaluation_not_authorization_relevant :
    ¬ AuthorizationRelevant .safetyEvaluation := by
  intro h
  cases h

/-- Capability evaluation evidence cannot substitute for authorization evidence. -/
theorem capability_evaluation_not_authorization_relevant :
    ¬ AuthorizationRelevant .capabilityEvaluation := by
  intro h
  cases h

/-- Dependency/supply-chain evidence cannot substitute for authorization evidence. -/
theorem dependency_evidence_not_authorization_relevant :
    ¬ AuthorizationRelevant .dependencySupplyChain := by
  intro h
  cases h

/-- An execution receipt is not external-effect verification evidence. -/
theorem receipt_not_effect_verification :
    ¬ EffectVerificationRelevant .executionReceipt := by
  intro h
  cases h

/-- Evaluation evidence is not external-effect verification evidence. -/
theorem evaluation_not_effect_verification :
    ¬ EffectVerificationRelevant .safetyEvaluation ∧
    ¬ EffectVerificationRelevant .capabilityEvaluation := by
  constructor <;> intro h <;> cases h

/-- Dependency evidence is not external-effect verification evidence. -/
theorem dependency_not_effect_verification :
    ¬ EffectVerificationRelevant .dependencySupplyChain := by
  intro h
  cases h

end RPOS
