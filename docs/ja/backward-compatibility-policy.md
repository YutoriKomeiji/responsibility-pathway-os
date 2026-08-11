<!-- RPOS-DOC-ID: RPOS-COMPAT-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/backward-compatibility-policy.md -->

# RPOS 後方互換ポリシー

## 目的

RPOS は、2026-08-12 時点で確認できる最新の実装・一次情報・toolchain・security/release practiceへ追随しながら、既にサポートしているalpha資産や利用方法を理由なく破壊しない。

この方針は「古い挙動を永久に固定する」という意味ではない。現在の責任境界を維持したまま、安全に継続利用・移行できる経路を提供するためのもの。

## 互換性分類

material change は次のいずれかに分類する。

- `backward_compatible`: 既存のサポート対象input、保存状態、CLI/API利用、packet/template、evidence workflowが継続して動作する。
- `compatibility_adapter_required`: 新しい表現・schema・挙動を導入するが、reader、alias、adapter、migration pathなどにより既存利用を保持する。
- `breaking_change_human_gate`: 安全に互換性を維持できず、明示的なbreaking change審査、affected versions、migration notes、Residual Owner、Human Return Pointが必要。

## 0.1.0a1 の互換性基準

現在のalpha readerは、以前のalphaで保存された `OperationDefinition` が次のoptional fieldを持たない場合でも読み込める。

- `resume_authority`
- `requires_human_gate`
- `verification_required`

欠落時は、既存の意味を壊さない既定値を使う。

- `resume_authority` -> `residual_owner`
- `requires_human_gate` -> `false`
- `verification_required` -> `true`

readerが既存状態を開くだけで、保存済みdefinitionを破壊的に書き換えてはならない。

この境界は `tests/test_backward_compatibility.py` で実行検証する。

## 最新化との関係

RPOSは新しい標準・guideline・schema・toolchain・dependency・security practiceを採用できる。ただし、更新時には以下を確認する。

1. 既存の保存状態やmachine-readable inputが読めるか。
2. CLI/APIやexported evidenceの意味が黙って変わらないか。
3. adapterで維持できる互換性を破壊的変更にしていないか。
4. 古いevidenceを最新値で上書きせず、過去の状態を再構築できるか。
5. 互換性を維持できない場合、Human Gateへ戻しているか。

## 改善要望と拡張

現行alphaにない機能や外部integrationは、即座に「不可能」とは扱わない。feature request、integration request、Industry Profile、compatibility requestとして評価し、責任境界と製品品質を維持できる場合に拡張候補とする。

ただし、要望受付は実装約束ではなく、予定表記は別途明示されない限り保証ではない。

## Japan-first / world-quality

初期の導入説明・reference package・guideline mappingは日本の組織、企業、業界団体、公共部門、個人実務家を優先する。一方、API、evidence、formal boundary、release engineering、compatibility semanticsは国際的なtechnical reviewに耐えられる表現と品質を維持する。

## Not Proven

このポリシーは、すべての将来版との無期限互換性、任意の第三者adapterとの互換性、production readiness、法令適合、certificationを保証しない。
