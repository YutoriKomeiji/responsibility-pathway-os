<!--
Document Title: RPOS Security Model and Threat Boundaries
Document Type: Security Model
Status: Pre-public-alpha migration candidate
Header Language: English
Body Language: Japanese
-->

# RPOS セキュリティモデルとThreat Boundary

## Security Objective

RPOSは一般的なsoftware assetだけでなく、Responsibility Pathwayそのもののintegrityとcontinuityを保護対象とする。したがって秘密情報が盗まれていなくても、攻撃者や故障componentが、実際には責任条件を満たしていないoperationを「承認済み・検証済み・責任者あり・完了済み」のように見せられるなら、RPOSにとってsecurity failureとなる。

0.1.0a1 public-alpha candidateのsecurity objectiveは限定的かつ明示的である。現在のproduct scope内で強制可能な高価値のresponsibility-pathway violationを拒否または検出し、不確実性を成功へ丸めず、責任上重要なdependencyが失われたときも明示的なReturn Pathを保持する。

## 保護するResponsibility Asset

RPOSでは次をsecurity-relevantなintegrity assetとして扱う。

- operation identityとaction intent;
- actor、approval authority、execution actor、resume authority、Residual Owner;
- Human GateとHuman Return Point;
- responsibility state transition;
- Authorityのfreshness、scope、Evidence binding、context binding;
- external-effect verification state;
- Evidence identityとsupersession lineage;
- event-history continuity;
- idempotencyとdispatch-attempt identity;
- release provenance、SBOM、source/artifact hash、exported product boundary。

## 主なThreat Class

### Authority Laundering / Replay

古いcomponentや攻撃者が、別actor、別operation、別action、別Evidence、別context、別時間帯へAuthorityを再利用する可能性がある。`AuthorityEnvelope` はこれらの不一致に対して追加型のfail-closed controlを提供する。ただし現alphaでは既存の全dispatch pathにmandatoryではない。

### Responsibility-State Equivocation

同一operationについて、system viewごとにstate、Residual Owner、Human Return Point、event historyが矛盾する可能性がある。RPOSはnon-equivocation findingを返し、勝手に一つを正本として選ばない。

### Historical Evidence / Event Substitution

新しいEvidenceは以前のEvidence identityを黙って消してはならない。Evidence supersession validationでは明示的なpredecessor linkを要求する。Responsibility event checkpointは、期待checkpointを独立に保持した場合、観測された完全event sequenceに対するdeterministicなtamper evidenceを提供する。

### External-Effect Uncertainty Collapse

execution receiptはexternal effect発生の証明ではない。effectが未確定なら `EFFECT_UNKNOWN` を維持し、restartやreconciliationでも都合よくcompletionへ変換しない。

### Unsafe Degradation

Authority、identity、policy、effect verificationに必要なdependencyを失うことは、責任経路の前提条件を失うこととして扱う。safe-degradation primitiveは `HOLD` を返す。supporting dependencyはdegrade可能だが、状態は明示的に観測可能でなければならず、Authorityを新たに作ってはならない。

### Repair / Resume Privilege Restoration

repair readinessだけではexecution authorityを復元しない。resumeにはdeclared resume authorityが必要であり、retryとは別である。

### Supply-Chain / Release Substitution

release-quality evidenceにはdeterministic export、source-bound hash、CycloneDX SBOM生成・validation、dependency vulnerability audit、secret scan、clean install、installed-boundary checkを含む。これらはpoint-in-time controlであり、将来も脆弱性が存在しないことを意味しない。

## Trust Boundary

0.1.0a1 candidateでは、より強いintegration profileを導入しない限り、local Python process、SQLite host、host clock、独立保持されたintegrity checkpointをdeployment側trusted computing boundaryの一部として扱う。

RPOSは現時点でtrusted hardware root、remote attestation、distributed consensus、malicious operatorへの普遍的耐性、multi-tenant isolationを主張しない。

External adapter、identity system、policy system、MCP/plugin/model integration、effect-verification serviceは別trust domainである。将来integrationを追加するときは、identity、credential、input validation、Authority、Evidence、timeout、degradation、failure returnのpolicyを個別に定義しなければ、強いRPOS security claimを継承できない。

## AlphaのSecure-Default Principle

- uncertaintyを成功へ丸めず保持する;
- responsibility-critical dependency欠落 => HOLD;
- invalid state transitionを拒否する;
- approval/resume actor不一致を拒否する;
- duplicate idempotency keyでredispatchしない;
- restart後のincomplete dispatchはblind replayせずunresolved effect側へ戻す;
- responsibility-history conflictは自動解決せず表面化する;
- superseding Evidenceはpredecessor identityを保持する;
- public exportからprivate research/non-product rootを除外する;
- security/release evidenceはscopeと有効時点を明示する。

## 明示的Deferred Control

machine-readable readiness record `provenance/security-quality-readiness-0.1.0a1.json` に、各deferred controlのowner、reason、risk、claim impact、Human Return Pointを保持する。alpha時点の主なdeferは、cryptographic/hardware-backed integrity anchor、既存全dispatchへのAuthorityEnvelope mandatory enforcement、generic MCP/plugin/model trust enforcement、multi-tenant isolation、production DoS/capacity assurance、scheduled continuous security revalidationである。

これらのdeferはpublic claimの範囲を狭めるものであり、未実装機能を将来提供すると約束するものではない。
