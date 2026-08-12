<!--
Document Title: RPOS Evidence Supersession and Safe Degradation
Document Type: Security Design Note
Status: Pre-public-alpha candidate
Header Language: English
Body Language: Japanese
-->

# RPOS Evidence Supersession と Safe Degradation

## 目的

本書は、RPOSに追加する2つの責任セキュリティ制御、すなわち明示的なEvidence supersession lineageと、責任上重要な依存先が失われた場合のfail-closedなdegradationを定義する。

これらは、すでにRPOSへ実装済みのAuthority Freshness Envelope、responsibility-integrity snapshot、non-equivocation check、event-chain checkpointを補完する。一般的なidentity、access control、network、host、supply chain、AI-agent securityを置き換えるものではない。

## Evidence Supersession Chain

新しいEvidenceによって以前の結論を置き換えること自体は正当な場合がある。ただしRPOSでは、以前のEvidenceが存在した事実を消さず、どのEvidenceがそれをsupersedeしたのかを追跡できるようにする。

`EvidenceSupersessionRecord` は次を保持する。

- evidence id;
- evidence digest;
- source reference;
- supersedeする場合の前Evidence id;
- supplied時のsupersession reason。

`validate_evidence_supersession_chain()` は最初のrecordを保持されたrootとして扱う。以後のrecordは直前のevidence idを明示的に指す必要がある。重複identity、self-supersession、壊れたpredecessor link、supersession linkなしの置換を拒否する。

目的はanti-substitution provenanceであり、Evidence内容そのものが真実・信頼可能・正しく解釈されていることを証明するものではない。

## Responsibility FunctionのSafe Degradation

RPOSでは責任上重要なdependencyと、補助的なdependencyを分ける。

現在のcriticality classは次の通り。

- authority;
- identity;
- policy;
- external-effect verification;
- supporting。

責任上重要なdependencyが `degraded` または `unavailable` の場合、`evaluate_responsibility_degradation()` は `HOLD` を返す。別のserviceが利用可能であることを理由に、失われたAuthorityを推定・継承してはならない。

supporting dependencyはdegradeまたはunavailableでも `ALLOW` を維持できるが、そのdegradationはoperator visibilityとtelemetryのためdecision内に明示して返す。

これは一般的な「best effort fallback」より意図的に厳しい。authority、identity、policy、effect verificationのいずれかに必要なdependencyを失うことは、責任経路の前提条件を失うこととして扱う。

## Testで確認するSecurity Property

現在のtestでは少なくとも次を確認する。

1. 明示的で線形なEvidence supersessionを受理する;
2. silent evidence replacementを拒否する;
3. 壊れたpredecessor linkを拒否する;
4. 重複Evidence identityを拒否する;
5. degradedなauthority dependencyでfail closedする;
6. unavailableなeffect-verification dependencyでfail closedする;
7. supporting serviceのdegradationはAuthorityを新たに作らず観測可能に残る;
8. supporting dependencyのavailabilityはcritical dependency failureを上書きできない。

## 互換性

このsliceは `backward_compatible`。APIとtestを追加するが、既存RPOSのpersisted schemaは変更せず、既存dispatch callerへdegradation statusやEvidence supersession recordを必須化しない。

すべてのdispatch/reconcile/resume pathへmandatory enforcementする場合は、後続の互換性・security decisionとして扱う。

## 現在の範囲と拡張経路

このsliceでは、cryptographic evidence signing、trusted timestamp、remote attestation、distributed consensus、automatic policy discovery、universal safe degradationまでは主張しない。

後続では必要性とEvidenceに応じて次との接続を検討できる。

- external integrity anchor;
- responsibility-security telemetry;
- MCP/plugin/integration trust policy;
- continuous security revalidation;
- bounded dispatch enforcement;
- signedまたはhardware-backed Evidence。

これらは拡張経路であり、現時点の提供機能や実装約束ではない。
