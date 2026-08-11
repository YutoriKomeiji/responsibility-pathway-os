<!-- RPOS-DOC-ID: RPOS-IP-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubator -->
<!-- RPOS-DOC-COUNTERPART: ../en/defensive-provenance-and-design-around-readiness.md -->

# RPOS 防御的プロヴェナンス／Design-around Readiness v0.1

## 目的

将来、適切な専門家がRPOS機能の起源、参照した情報源、公開履歴、交換可能な実装境界を再構築できるよう、日付付きの工学証拠を保存する。

この層は工学プロヴェナンス機構である。特許鑑定、Freedom to Operate判断、無効資料評価、先行技術充足判断、法律助言ではない。

## 1. 基本原則

未公開の第三者特許請求項は、RPOSの設計入力にしない。

RPOSは、Responsibility Pathwayの独自系譜、内部要件、公的な標準・ガイダンス、一般的な工学知識を根拠として開発を継続する。第三者資料は、文脈、比較、または明示的に宣言された依存関係として記録できるが、比較資料が暗黙にRPOSの規範的な機能根拠へ昇格してはならない。

## 2. Provenance Record

プロヴェナンス記録は、最低限次を識別する。

- record ID
- feature ID / feature name
- 最初に内部で確認できる日付
- 技術的根拠
- source class
- source references
- external-reference boundary
- design-around readiness

任意項目として、最初の内部参照、公開日／公開参照、交換可能な実装境界、限定的な注記を記録できる。

## 3. Source Class

初期source classは次とする。

- `internal_engineering`
- `public_standard_or_guidance`
- `general_engineering`
- `external_comparison`
- `declared_dependency`

この分類はプロヴェナンスの文脈を記録するものであり、新規性、進歩性、特許有効性、侵害を判断しない。

## 4. External Reference Boundary

外部参照は次に分類する。

- `none`
- `context_only`
- `comparison_only`
- `declared_dependency`

目的は、実装上の依存関係と、単に観測・比較した資料を区別することである。

## 5. Design-around Readiness

初期状態は次とする。

- `not_assessed`
- `modular_boundary`
- `coupled_review_required`

`modular_boundary` の場合は交換可能な境界名を必須とする。これはアーキテクチャ上のメタデータであり、その部品を交換すれば特許請求項を回避できるという意味ではない。

## 6. 公開履歴メタデータ

公開日を記録する場合は対応する公開参照も必須とし、公開参照を記録する場合も公開日を必須とする。日付と参照の組は、公開事象を記録した証拠であり、その公開が法的に有効な先行技術になるという結論ではない。

## 7. 将来のClaim Chart利用

未公開または推測した請求項からclaim chartを作らない。実際の公開請求項または成立請求項が利用可能になった後、適切な専門家が、プロヴェナンス記録、リポジトリ履歴、公開履歴、実装境界を別途の請求項単位分析の入力にできる。

その分析はRPOSの規範的な責任状態機械の外側に置く。

## 8. 運用状態からの隔離

防御的プロヴェナンス情報は、RPOS operationのauthorize、dispatch、verify、resume、deny、repair、completeを行わない。Authorityを生成せず、責任状態を変更しない。

## 9. Fail-closed Serialized Import

シリアライズされたプロヴェナンス入力は未知フィールドを拒否する。non-infringement、invalidity、freedom to operate、prior-art sufficiencyなど、法律上の結論を直接表すフィールドは、この工学スキーマへ入れない。

## 10. Documentation Propagation

プロヴェナンス意味論を変更する場合、最低限次を横展確認する。

- 本JA/EN仕様ペア
- provenance schema / model / tests
- release-readiness文書
- package/IP review手順
- 関連する将来のExpert Review Pack interface
- 将来claim-chart workflowを実装した場合はその手順

横展を延期する場合は、Issue、Residual Owner、理由、影響artifact、Human Return Pointを保存する。

## Not Proven

この仕様は次を証明しない。

- 特許非侵害
- 特許無効
- Freedom to Operate
- 先行技術としての十分性
- 新規性または進歩性
- 公開日の法的意味
- 工学プロヴェナンスの完全性
- 指定したmodular boundaryが有効なdesign-aroundになること
