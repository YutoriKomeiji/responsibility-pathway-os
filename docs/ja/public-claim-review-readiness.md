<!-- RPOS-DOC-ID: RPOS-IP-002 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubator -->
<!-- RPOS-DOC-COUNTERPART: ../en/public-claim-review-readiness.md -->

# RPOS 公開請求項レビュー準備 v0.1

## 目的

第三者の特許出願又は特許が公開された後に、請求項単位のレビューへ移れるよう RPOS を準備する。未公開請求項を推測せず、第三者の特許戦略を RPOS の設計入力にはしない。

## 記録するメタデータ

公開請求項レビュー記録では、次を保存できる。

- 公開番号と公開日
- 判明している場合の出願番号
- 判明している場合の優先日
- 正確な請求項識別子と公開請求項本文の参照先
- 該当する場合の登録特許番号と登録時請求項版
- 専門レビュー対象として選択した RPOS feature ID
- 工学レビュー状態と注記

公開番号、公開日、請求項識別子、公開請求項本文の参照先が無い記録は作成しない。

## レビューライフサイクル

工学レビューでは、次の限定状態を使う。

- `not_started`
- `public_claim_available`
- `qualified_review_required`
- `design_around_review`
- `closed_no_engineering_change`
- `closed_engineering_change`

これらは作業状態であり、法的結論ではない。

## Design-around 原則

専門レビューで重要な工学上の重複リスクが確認された場合、まず宣言済みの交換可能境界を確認する。OS 全体を広範に書き換えるより、Responsibility Pathway の意味を維持したまま、限定されたモジュール又はアルゴリズムを交換することを優先する。

## 法的結論との分離

report では、次を常に Not Proven とする。

- 特許非侵害
- 特許無効
- Freedom to Operate
- 先行技術としての十分性
- 請求項の法的範囲
- 法律助言

RPOS が保存するのは日付付きの工学資料までであり、法的結論はこの工学スキーマの外で専門家が判断する。
