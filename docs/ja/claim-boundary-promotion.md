# Claim Boundary Promotion（主張境界の昇格）

RPOSでは、公開上の主張を永久的な免責事項として並べるのではなく、**どの証拠まで確認できているかに応じて管理される状態**として扱います。

現在「まだそこまでは主張しない」としている項目には、性質の異なる2種類があります。

1. 必要な証拠が揃い、レビューされれば前進できる **Current Evidence Boundary（現在の証拠境界）**
2. 成熟してもRPOS単体では越えない **Permanent Responsibility Boundary（恒久的な責任境界）**

この2つを、同じ「できないこと」の一覧としては扱いません。

## Current Evidence Boundary

RPOS 0.1.0a2 は **2026-08-29にPyPIへ公開済みの Early Public Alpha / Executable Preview** です。現在のverified surfaceには、限定されたPython実行挙動、永続化と障害回復scenario、clean package install、public-export再構築、SBOM/source-bound check、Ubuntu/Windows × Python 3.11/3.12 evidence、GitHub Pages deployment check、宣言された限定model上でmachine-checkされPython runtime testへcross-linkされた6件のLean 4責任不変条件が含まれます。

このevidenceが支えるのは現在のPublic Alpha claimまでです。本番運用、法的判断、組織的権限、外部system全体、Python実装全体のformal correctnessまで同時に確認できたという意味ではありません。

## Promotion Criteria

次は証拠依存の境界です。review可能なevidenceが追加されれば、確認できた範囲から前進できます。

| 現在の境界 | 境界を前進させるためのevidence |
|---|---|
| production readinessはまだ確認中 | sustained workload / soak test、対応deployment profileでのfault injection、upgrade/rollback/backup/recovery evidence、operational monitoring/SLO evidence、review済みsecurity/deployment control |
| platform / field evidenceが限定的 | 対応OS、Python、container、network、identity、storage profileについて宣言されたsupport matrixと再現可能なCI/field result |
| implementation-wide formal conformanceはまだ確認中 | formal modelとexecutable semantics間の明示的refinement/conformance relationと、主張対象実装surfaceについて独立再現可能なconformance evidence |
| 広範なsoftware supply-chain trustはまだ確認中 | dependency provenance強化、必要箇所のimmutable CI input、artifact signing/attestation、独立検証、継続的vulnerability-response evidence |
| 現在のscenarioを超えるdomain effectivenessはまだ確認中 | 仮説・failure criteria・観測結果・counterexampleを宣言したdomain-specific pilotと独立review |

Promotionは、新しいevidenceが追加されたことだけでは成立しません。scopeが明示され、review可能で、必要に応じて再現可能であり、対応するpublic claimへ明示的に採用されたときに前進します。

## Permanent Responsibility Boundaries

次はRPOSが成熟しても、それだけを理由に変わる境界ではありません。

- RPOS単体で法的権限、法解釈、法的責任、認証、規制当局の承認が生まれるわけではありません。
- RPOSが経路を管理しても、外部systemそのものの正しさまで保証するものではありません。
- 適切なverification contractとevidence sourceがない場合、transport receiptだけを現実のeffect証明としては扱いません。
- 最終的な組織責任は、人間・制度の側に残ります。
- 必要なtransaction/idempotency/verification contractを持たない任意外部systemに対し、universal exactly-onceを保証するものではありません。
- abstract modelへのformal proofだけで、Python実装全体やdeployment environment全体まで証明済みとは扱いません。

これは「未完成機能の一覧」ではなく、**どの確認をRPOSが担い、どこから先を別の人・制度・systemが担うか**を分けるための責任境界です。

## Evidence Owners

- **RPOS engineering**: state machine、永続化、recovery、packaging、宣言したimplementation evidence
- **Integrator / Operator**: identity、credential、network control、bypass prevention、monitoring、権威あるexternal-effect observation
- **RPE / RPD / RPM / Assurance**: upstream requirement、engineering obligation、design rationale、review structure、theory revision。別layerのevidenceは、それぞれの役割を保ったまま扱います
- **資格・権限を持つ人間／制度**: 法務、規制、認証、operational authorizationの最終判断

## Promotion States

公開境界を明示的に追跡する場合、可能な範囲で次を使います。

- `evidence_collecting`
- `review_ready`
- `promoted`
- `permanently_out_of_scope`

日本語のpublic surfaceでは、「何ができないか」だけでなく、**今どこまで確認できていて、次にどのevidenceが揃えば前へ進めるか**を一緒に示します。

したがってpublic non-claimは、それが**一時的なevidence gapなのか恒久責任境界なのか**を分け、一時的なgapには境界を動かすためのevidence routeを示します。
