<!-- RPOS-DOC-ID: RPOS-MIGRATION-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: pre-migration-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/rpr-derived-migration-procedure.md -->

# RPOS 移植手順 — RPR Standalone Export Path準拠

Status: 移植前手順。本文書は移植または公開を承認するものではない。

## 参照したRPR手順

この手順は、`incubator/rpr/docs/release-preparation-4.md` に記録されたRPR release/export controlsと、`governance/failure-knowledge/incidents/FK-2026-002-standalone-export-integrity-gap.md` の検証済みfailure knowledgeをfresh-readした上で導出する。

支配的な教訓は、standalone product repositoryは単なるPython package directoryのcopyではない、ということ。公開主張を支える全artifactをexport boundaryに含め、private RPP pathを利用できない状態でもtest可能でなければならない。

## 前提条件

RPP -> standalone RPOS移植の前に、次を満たす。

1. #191 pre-migration hardeningが完了している。または残件すべてにowner/reason/claim impact/Human Return Pointが明示されている。
2. #180 `MIGRATION_READY_0.1.0a1` criteriaを満たす。
3. 一つのimmutableなRPP source commit SHAを選定する。
4. そのSHAからpublic-export allowlist/manifestを生成しreviewする。
5. RPP-private research、internal chronology、credentials、非公開専用material、private comparison dossierを除外する。
6. public metadataを整合させる。product name、repository、distribution、import package、version、license/SPDX、citation、security contact/boundary、supported Python versionsを確認する。

## Standalone inventory rule

allowlistには公開claimを支える完全なproduct evidence surfaceを列挙する。必要に応じて次を含む。

- Python package/runtime source
- CLIとexecutable examples
- 公開挙動を裏付けるtests/fixtures
- Lean sourceと宣言・固定されたformal verification path
- formal-evidence crosswalkとpublic-claim crosswalk
- responsibility packet templates/catalog
- EN/JA README、Quick Start、operational boundary、Not Proven、security/provenance docs
- package metadata/license
- standalone CIに必要なmaintenance/validation tools
- public retention対象のrelease/export evidence files

移植後、必要なvalidator/testがprivate RPP layoutへ依存してはならない。

## 移植シーケンス

1. exact RPP source SHAをfreezeする。
2. reviewed allowlistからclean exportを生成する。editable working treeを丸ごとcopyしない。
3. export manifestとsource SHAを同一lineageとして記録する。
4. 既に作成済みのprivate `YutoriKomeiji/responsibility-pathway-os` repositoryへ配置する。
5. standalone repository内でstandalone package boundaryからinstallしてからtestする。
6. private RPP pathを利用できない状態でcomplete standalone verification bundleを実行する。
7. standalone formal boundaryからLeanをcompileする。
8. executable scenarios、focused tests、wheel build、isolated clean install、installed CLI/Quick Start、doc-sync checks、export/inventory checksを実行する。
9. 同一frozen source/export lineageからartifact hashとverification evidenceを記録する。
10. 必須artifact欠落やRPPへの逆参照が見つかった場合、移植は未完了と分類し、standalone inventoryを修復してから進む。

## RPRから継承する製品品質ゲート

RPOSは、RPRで用いたrelease-quality disciplineを少なくとも同等以上に維持し、RPOSのproduct boundaryへ適合させる。

一つのrelease candidateは、一つのimmutable source SHAと一つのpackage versionに固定する。同一lineageから、必要に応じて次のevidence bundleを保持する。

- clean-export manifest hash
- wheel hashとsource-distribution hash
- CycloneDX SBOMまたは承認済み同等artifact、およびvalidation result
- Lean 4 verification evidenceと宣言toolchain version
- functional / integration / end-to-end scenario results
- wheelとsource distributionを別々のclean environmentで検証したclean-install results
- installed CLI / Quick Start results
- restart / reconciliation / repair / explicit resume evidence
- secret-scan result
- dependency / vulnerability-review result
- release auditとclaim/evidence review result
- known limitationsとaccepted residual risks
- artifact hash bundle

clean-install evidenceには、interpreter/toolchain version、platform、artifact SHA-256、installed package version、scenario results、repository pathまたはuser site-packagesが存在したかを保持する。

mixed commit、dirty/editable source state、未記録のmanual substitutionから生成されたartifact/evidenceを含むcandidateは無効とする。

必須evidenceの欠落は暗黙承認ではなく `hold` とする。

## Private移植後のHuman Gate

移植後検証の通過は、private standalone repositoryが内部整合したRPOS alpha candidateになったことだけを意味する。

次は別Human Gateが必要。

- repository visibilityをpublicへ変更
- public tag/release
- PyPI publish
- Pages/demo enable
- external announcement/marketing
- production-readiness claim

Human Gate decision packにはsource SHA/version、manifest/artifact hashes、SBOM status、clean-install/E2E results、security-review results、known limitations、accepted residual risks、decision/evidence/residual ownerを含める。

許容結果は `approve`、`approve_with_conditions`、`hold`。

## RPOS固有のRPRとの差分

RPOSではRPRの一般release pathに加え、次を必須とする。

- Lean theorem/property -> implementation/test -> assumption -> `not_proven` の明示crosswalk
- `Operating System`、`runtime`、`formal`、`verified`、`assurance`、`security` 等の強い技術語に対するclaim/evidence crosswalk
- responsibility packet authority-boundary evidence
- private third-party researchをexportせずにRPD -> RPE -> RPR -> RPOS lineageを保持するdefensive-provenance snapshot

これらはstandalone evidence boundaryを強化する追加要件であり、RPR clean-export rulesおよびproduct-quality rulesを緩和しない。
