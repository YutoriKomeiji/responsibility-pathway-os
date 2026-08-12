<!--
Document Title: RPOS Responsibility Security Primitives
Document Type: Security Design Note
Status: Pre-public-alpha candidate
Header Language: English
Body Language: Japanese
-->

# RPOS 責任セキュリティ・プリミティブ

## 対象範囲

本書は、2026-08-12のセキュリティ強化トラックで追加する最初のRPOS固有セキュリティ・プリミティブを定義する。既存のソフトウェアセキュリティやAIセキュリティの代替ではなく、それらを補完する。

設計では、NISTのAIエージェント・セキュリティ関連作業、OWASP AISVS 1.0、OWASP Top 10 for Agentic Applications 2026、CISA Secure by Design、ISO/IEC 25010:2023の製品品質モデルなど、現時点で公開されている公式・一次資料を参照する。これらへ対応付けたことは、認証、適合、推奨、完全対応を意味しない。

## なぜRPOSに責任固有のセキュリティが必要か

一般的なセキュリティは、機密性、完全性、可用性、identity、authorization、software supply chain、運用境界などを守る。RPOSも当然これらを守る必要がある。

それに加えてResponsibility Pathwayを扱うsystemでは、秘密情報が盗まれなくても、攻撃者や故障componentが「適切に承認・実行・完了されたように見せる」ことができれば、責任systemとして侵害されたことになる。

例:

- 古い承認を別operationへreplayする;
- Evidenceや運用contextが変わった後も古いAuthorityを使う;
- 複数のsystem viewで同じoperationの責任状態を食い違わせる;
- Residual OwnerやHuman Return Pointを検出されずに置換する;
- より短い、または異なるevent historyを正本のように見せる;
- 外部効果未確定を都合よく完了へ丸める。

最初の実装sliceでは、責任metadata、責任状態の一致性、責任履歴のintegrityを保護対象として扱う。

## Primitive 1: Authority Freshness Envelope

`AuthorityEnvelope` はAuthority evidenceを次へ束縛する。

- actor;
- operation id;
- action name;
- 発行時刻;
- 有効期限;
- evidence digest;
- context digest。

`validate_authority_envelope()` はfail-closedで判定する。期限切れ、未来時刻、actor不一致、別operationへのreplay、別actionへのreplay、evidence不一致、context不一致があれば、明示的理由付きで `HOLD` を返す。

現sliceでは**追加型primitive**であり、既存RPOSのstate authorizationを自動的に置き換えない。callerが明示的に採用した場合に検証する。全dispatchでmandatoryにする場合はbehavior changeになるため、互換性評価を行ってからenforcementする。

## Primitive 2: Responsibility Integrity Snapshot

`ResponsibilityIntegritySnapshot` は責任上重要なprojectionからcanonical SHA-256 digestを作る。

- operation id;
- state;
- Residual Owner;
- Human Return Point;
- event count;
- latest event digest。

目的はtamper sensitivityと複数view間の比較である。digital signature、trusted timestamp、元event内容の真実性証明ではない。

## Primitive 3: Responsibility-State Non-Equivocation Monitor

`find_responsibility_inconsistencies()` は同じoperationに対する複数の責任snapshotを比較し、勝手にどれかを正しいと採用せず、不一致を報告する。

現在検出するのは次の不一致。

- responsibility state;
- Residual Owner;
- Human Return Point;
- event-history length;
- latest-event digest。

callerは検出結果を用いてexecutionをHOLDするか、responsible reviewへ戻せる。自動的なconflict resolutionはこのprimitiveの対象外とする。

## Primitive 4: Responsibility Event-Chain Checkpoint

`build_event_chain_checkpoint()` は、一つのoperationについて観測された全event sequenceをdeterministicなSHA-256 hash chainへ変換する。`RposService.event_chain_checkpoint()` は実際のstored event historyからそのcheckpointを取得する。

builderは別operationのevent差し替えと、seqが単調増加しないevent列を拒否する。過去に保持したcheckpointと比較した場合、昔のeventが後から改変されていればchain digestが変化し、`event_chain_matches()` はfalseになる。

これはSQLite schemaを変更せずに追加する実用的な**tamper-evidence primitive**である。ただし意味のある検出には、期待するcheckpointをmutable event storeとは独立した場所へ保持する必要がある。同じ侵害済みDBの中だけにcheckpointを保存しても独立trust anchorにはならない。

## 現在のsliceで確認するsecurity property

negative/integration testで少なくとも次を確認する。

1. 期限切れAuthorityはfail closedする;
2. 別operationへreplayしたAuthority envelopeはfail closedする;
3. Authorityはcallerが指定したEvidence/context digestへ束縛される;
4. responsibility-integrity digestはdeterministicであり、保護field変更で変化する;
5. 矛盾したresponsibility viewを黙って統合せず検出する;
6. 同一view同士では存在しない矛盾を作らない;
7. 変更されていないevent historyは同じevent-chain checkpointを返す;
8. 正常なevent追加ではcheckpointが前進する;
9. historical eventの改変は保持済みcheckpointとの一致を破る;
10. cross-operation event substitutionと非単調なevent順序を拒否する。

## 現行の国際資料・Agent Securityとの関係

2026-08-12時点では、

- NISTの2026年AI-agent security関連作業では、従来のcybersecurity原則は引き続き有効だがAI agent向けの適応が必要という見解が広く示され、AI Agent Standards Initiativeでもidentity、authorization、secure interaction、security evaluationが継続テーマとなっている;
- OWASP AISVS 1.0（2026-06-24公開）はAccess Control & Identity、Supply Chain、Memory、Autonomous/Agentic Action、MCP、Adversarial Robustness、Monitoring/Logging等をtest可能なAI security requirementsとして整理している;
- OWASP Top 10 for Agentic Applications 2026はworkflowを計画・実行するagentic system固有のriskを整理している;
- CISA Secure by Designは顧客側へhardening負担を丸投げせず、secure behaviorをproduct propertyとして組み込むことをsoftware manufacturerへ求める方向である;
- ISO/IEC 25010:2023はrequirements、test objectives、quality control、acceptance criteriaへ利用できる9特性のproduct quality modelを提供する。

RPOSではこれらを#201/#202の広いhardening programのEvidence入力として使いながら、別層としてRPOS固有のresponsibility securityを構築する。

## 現在の制約と拡張経路

現在のsliceでは、まだ次を主張しない。

- 全dispatchでのAuthority Envelope必須化;
- cryptographic signatureやhardware-backed key;
- 独立replica間のdistributed consensus;
- trusted timeやhost clock侵害への耐性;
- immutableまたは外部anchoringされたevent ledger;
- conflictの自動安全解決;
- SQLite/Python runtimeとbounded Lean modelの完全conformance証明;
- prompt injection、侵害されたplugin/MCP server、malicious operator、supply-chain compromiseへの完全耐性。

これは「今後も不可能」という宣言ではなくcurrent scopeの境界である。後続ではmandatory enforcement、Evidence supersession chain、external checkpoint anchoring、degradation policy、integration trust、secret isolation、persistence tamper detection、security telemetry、continuous revalidationを評価する。

## 互換性分類

現在のsliceは `backward_compatible` とする。security APIとtestを追加するが、既存persisted schemaは変更せず、既存callerへAuthority Envelopeやevent checkpointを要求しない。

optional validationからmandatory dispatch enforcementへ進む場合、またはexternal checkpointから新しいpersisted integrity schemaへ移行する場合は別途分類し、必要に応じて `compatibility_adapter_required` または `breaking_change_human_gate` として扱う。
