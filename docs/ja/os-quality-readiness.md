<!--
Document Title: RPOS OS-Quality Readiness
Document Type: Product Quality Readiness Note
Status: Pre-public-alpha migration candidate
Header Language: English
Body Language: Japanese
-->

# RPOS OS品質Readiness

## 対象範囲

RPOSにおける「Operating System」は、responsibility state、Authority、external-effect verification、reconciliation、repair、resume、Evidence、Human Return Pointを運用するoperating layerを意味する。0.1.0a1 alphaは、一般的なkernelや汎用host OSではなく、responsibility operating layerとしてのsoftware product qualityを評価対象とする。

本書は、repository migrationへ進めるだけの実装・検証が得られているquality attributeと、production-readinessには含めない境界を整理する。

## Functional Suitability

executable coreはproposal、Human Gate、authorization、dispatch、effect verification、effect-unknown containment、reconciliation、repair preparation、明示的resume authorization、completion、persistent state、CLI/examples、Evidence/provenance helperを提供する。

invalid transitionと誤ったapproval/resume actorを拒否する。receipt successはrequired effect verificationの代替にならない。

## Reliability / Recoverability

restart後にincomplete dispatchを検出した場合、automatic redispatchせずunresolved external-effect handlingへ戻す。idempotency keyは記録済みattemptのduplicate redispatchを防ぐ。repair readinessとrestored authorityは分離する。

alphaではarbitrary-operation liveness、distributed failover、production availability SLOは主張しない。

## Compatibility

現在candidateまでのsecurity hardeningは追加型で `backward_compatible` と分類する。supported alphaのpersisted recordはcompatibility defaultにより読み込み可能な状態を維持する。将来、新security envelopeをmandatoryにする場合は別のcompatibility classificationが必要になる。

## Operability / Diagnosability

RPOSはexplicit state、Human Return Package、unresolved reason、event history、reconciliation evidence、security degradation reason、responsibility-integrity findingを観測可能にする。failure stateをgeneric success/failureへ潰さず、inspect可能なまま保持することを重視する。

sensitive-data minimizationはdeployment/integrationにも依存するため、event storeを任意secret保存場所として扱ってはならない。

## Maintainability / Testability

productはmodels、storage、service orchestration、adapter、Evidence、provenance、security primitive、template、CLI、test、example、bounded Lean artifactを分離している。public claimはimplementation、test、assumption、Not Proven boundaryへcrosswalkする。

## Portability / Installability

release verificationではwheelとsource distributionをbuildし、isolated install、installed CLI、repository working directory外からのQuick Startを実行し、deterministic public-export boundaryを検証する。

## Supply-Chain / Release Integrity

release-quality workflowではCycloneDX SBOMの生成・schema validation、declared Python dependency audit、standalone source exportのsecret scan、source-bound artifact hash生成、release-quality evidence保持を行う。

これらはpoint-in-time Evidenceであり、certificationや将来も脆弱性が存在しないことを意味しない。

## Responsibility固有のQuality Property

RPOSではさらに次をproduct-quality propertyとして扱う。

- uncertainty preservation;
- partial failure下のresponsibility continuity;
- Residual Owner / Human Return Pointの保持;
- Authority freshness / context binding primitive;
- responsibility-state non-equivocation detection;
- tamper-evident responsibility-event checkpoint;
- silent erasureを許さないEvidence supersession;
- Authority/identity/policy/effect-verification dependency欠落時のfail-closed degradation。

## Deferred Quality Attribute

machine-readable readiness recordにalpha時点の明示的deferを保持する。主な残件はproduction workload/capacity objective、multi-tenant isolation、generic integration trust enforcement、cryptographic external integrity anchor、既存全pathへの新security primitive mandatory enforcement、post-release recurring security revalidationである。

各deferにはowner、risk、claim impact、Human Return Pointを持たせる。隠れたgapとして扱わず、強いproduction claimへ読み替えない。

## Migration Readiness Rule

repository migrationは、exact candidate headについてfocused Python verification、public-export RC verification、JA/EN documentation sync、release-quality evidence checkがすべてgreenになってから進める。green verificationはmigration readinessのEvidence保持を可能にするが、それだけでrepository public visibility、tag/release、PyPI、Pages/demo、external announcementを許可しない。
