# Claim Boundary Promotion（主張境界の昇格）

RPOSでは、公開上の主張を永久的な免責事項ではなく、**証拠に基づいて管理される状態**として扱います。

現在「主張しない」としている項目には、性質の異なる2種類があります。

1. 必要な証拠が揃い、レビューされれば前進できる **Current Evidence Boundary（現在の証拠境界）**
2. 成熟してもRPOS単体では越えるべきではない **Permanent Responsibility Boundary（恒久的な責任境界）**

この2つを同じ「できないこと」の一覧として扱いません。

## Current Evidence Boundary

RPOS 0.1.0a2 は Early Public Alpha / Executable Preview のrelease candidateです。現在のverified surfaceには、限定されたPython実行挙動、永続化と障害回復scenario、clean package install、public-export再構築、SBOM/source-bound check、Ubuntu/Windows × Python 3.11/3.12 evidence、GitHub Pages deployment check、宣言された限定model上でmachine-checkされPython runtime testへcross-linkされた6件のLean 4責任不変条件が含まれます。

このevidenceが支えるのは現在のPublic Alpha claimまでです。本番、法的判断、組織的権限、外部system全体、Python実装全体のformal correctnessまで自動的に昇格するものではありません。

## Promotion Criteria

次は証拠依存の境界であり、review可能なevidenceが追加されれば前進し得ます。

| 現在の境界 | 境界を前進させるためのevidence |
|---|---|
| production readinessを未主張 | sustained workload / soak test、対応deployment profileでのfault injection、upgrade/rollback/backup/recovery evidence、operational monitoring/SLO evidence、review済みsecurity/deployment control |
| platform / field evidenceが限定的 | 対応OS、Python、container、network、identity、storage profileについて宣言されたsupport matrixと再現可能なCI/field result |
| implementation-wide formal conformanceを未主張 | formal modelとexecutable semantics間の明示的refinement/conformance relationと、主張対象実装surfaceについて独立再現可能なconformance evidence |
| 広範なsoftware supply-chain trustを未主張 | dependency provenance強化、必要箇所のimmutable CI input、artifact signing/attestation、独立検証、継続的vulnerability-response evidence |
| 現在のscenarioを超えるdomain effectivenessを未主張 | 仮説・failure criteria・観測結果・counterexampleを宣言したdomain-specific pilotと独立review |

Promotionは自動ではありません。新しいevidenceはscopeが明示され、review可能で、必要に応じて再現可能であり、対応するpublic claimへ明示的に採用される必要があります。

## Permanent Responsibility Boundaries

次はRPOSが成熟しても、それだけを理由に消える境界ではありません。

- RPOS単体は法的権限、法解釈、法的責任、認証、規制当局の承認を生成しません。
- RPOSが経路を管理しても、外部systemそのものの正しさを生成しません。
- 適切なverification contractとevidence sourceなしに、transport receiptを現実のeffect証明へ昇格させません。
- 最終的な組織責任を人間・制度からsoftwareへ移転しません。
- 必要なtransaction/idempotency/verification contractを持たない任意外部systemに対し、universal exactly-onceを保証できません。
- abstract modelへのformal proofだけで、Python実装全体やdeployment environment全体を証明済みとは扱いません。

これらは「未完成機能」ではなく、責任境界です。

## Evidence Owners

- **RPOS engineering**: state machine、永続化、recovery、packaging、宣言したimplementation evidence
- **Integrator / Operator**: identity、credential、network control、bypass prevention、monitoring、権威あるexternal-effect observation
- **RPE / RPD / RPM / Assurance**: upstream requirement、engineering obligation、design rationale、review structure、theory revision。別layerのevidenceを代用してはいけません。
- **資格・権限を持つ人間／制度**: 法務、規制、認証、operational authorizationの最終判断

## Promotion States

公開境界を明示的に追跡する場合、可能な範囲で次を使います。

- `evidence_collecting`
- `review_ready`
- `promoted`
- `permanently_out_of_scope`

したがってpublic non-claimは、それが**一時的なevidence gapなのか恒久責任境界なのか**を示し、一時的なgapには境界を動かすためのevidence routeを示します。
