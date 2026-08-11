<!-- RPOS-DOC-ID: RPOS-OPS-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubator -->
<!-- RPOS-DOC-COUNTERPART: ../en/development-and-document-sync-policy.md -->

# RPOS 開発・文書同期ポリシー v0.1

## 目的

RPOS の実装、仕様、導入資料、運用資料、業界プロファイル、専門家レビュー資料、価値証拠資料を更新するとき、日英の片側更新や関連文書への横展漏れを防ぐ。

このポリシーは「文書があること」を完成条件にしない。変更された意味が、影響を受ける実装・仕様・例・運用資料・証拠資料へ一貫して反映されたことを確認するための運用規律である。

## 1. 日英同時作成

次の利用者向け・運用向け文書は、原則として日本語版と英語版を同一変更単位で作成・更新する。

- 製品説明、アーキテクチャ説明
- 導入ガイド、パイロット手順
- 運用 Runbook、障害・回復・再開手順
- Industry Profile の説明文書
- Expert Review Pack の説明文書
- Cost / Value Evidence の説明文書
- インストール、Quick Start、リリース準備資料
- 公開候補となる仕様・利用者向け Best Practice 文書

片方を後で翻訳する運用を標準にはしない。意味変更は可能な限り同一 PR 内で両言語に反映する。

### 例外

以下は自動的な日英ペア義務の対象外とする。ただし製品文書へ昇格・再利用するときはペア化する。

- ソースコード、テスト、機械可読スキーマ
- 生の検証証拠、実行ログ
- 一時的な内部研究メモ、探索記録
- 過去の単一言語 incubator 資料

既存の単一言語資料は遡及的に一括翻訳しない。実質的な改訂、製品化、導入・運用資料への昇格時点をペア化の Human Return Point とする。

## 2. 言語と文書制御のヘッダー

言語ルールは文書本文ではなくヘッダーで宣言する。ペア対象文書は少なくとも次を持つ。

- `RPOS-DOC-ID`
- `RPOS-DOC-LANG`
- `RPOS-DOC-VERSION`
- `RPOS-DOC-STATUS`
- `RPOS-DOC-COUNTERPART`

プログラムや設定ファイルに言語・文書制御情報を持たせる必要がある場合は、その言語で有効なコメント形式のヘッダーを使う。

## 3. 変更前 Impact Scan

RPOS の意味を変更する作業は、実装前または PR 作成前に影響範囲を分類する。少なくとも以下を確認する。

| 変更クラス | 必ず確認する横展先 |
|---|---|
| 状態・遷移意味論 | normative spec、README / Quick Start、Adoption Guide、Operations / Recovery / Resume Runbook、Industry Profiles、例・テスト、用語 |
| CLI / schema | README / CLI 文書、例、Adoption Guide、Profile / sample config、audit / evidence 文書 |
| Evidence model | audit package、guideline matrix、Expert Review Pack、Industry Profiles、必要な Cost / Value Evidence |
| Dependency / Adapter | supply-chain profile、Operations Runbook、audit / evidence、Industry Profiles |
| Recovery / Resume | Runtime 意味論、Operations Runbook、Adoption Guide、expert-review triggers、Industry Profiles |
| Release / Package | install 文書、Quick Start、release readiness、Not Proven、security / credential boundary |

表は最小集合であり、該当すれば追加の文書・テスト・例も確認する。

## 4. Documentation Propagation 判定

RPOS の意味・利用方法・運用方法を変える PR は、本文に `Documentation propagation` セクションを持つ。

最低限、各関連項目を次のいずれかで明示する。

- `updated`: 同一変更で更新済み
- `reviewed-not-affected`: 確認したが意味上の変更なし
- `deferred`: 今回は更新しない。Issue、Residual Owner、理由、Human Return Point を記録

「確認していない」「たぶん影響しない」は許容状態にしない。

## 5. Deferred の扱い

横展を延期できるのは、延期しても現在の変更が誤解を生まず、かつ次の情報が残る場合だけとする。

- linked issue
- residual owner
- unresolved reason
- affected document or artifact
- human return point

公開・リリース候補の文書に未解決の同期漏れがある場合、その項目は release readiness の gap として扱う。

## 6. 日英ペアの整合性

自動検証は、登録されたペアについて以下を確認する。

- 両方のファイルが存在する
- Document ID が一致する
- Version が一致する
- Status が一致する
- `ja` / `en` の言語指定が正しい
- Counterpart が互いを指す

自動検証は翻訳の意味同等性を証明しない。意味同等性、用語整合、Not Proven の一致はレビュー責任として残る。

## 7. 実装と文書の同期順序

推奨する小さい縦切りは次の通り。

`spec / profile -> model / schema -> service / read-only integration -> CLI -> tests -> JA/EN docs -> propagation scan -> focused verification -> audit -> merge -> issue evidence`

文書を最後の飾りとして追加しない。利用者向け意味が変わる実装では、文書同期を同じ実装単位に含める。

## 8. 完了条件

RPOS の変更を完了と報告するには、少なくとも次が必要である。

1. 対象実装・仕様の検証結果がある。
2. 登録された日英ペアが構造的に同期している。
3. Documentation propagation が判定済みである。
4. Deferred がある場合は責任と再開点が残っている。
5. 完了していない横展を完了扱いしていない。

## Not Proven

このポリシーと自動検証は、以下を証明しない。

- 翻訳の完全な意味同等性
- 法令・規制適合
- 文書内容の技術的正しさ
- 影響範囲の完全性
- 公開・リリース準備完了

それらは別のレビュー、検証、Human Gate を必要とする。
