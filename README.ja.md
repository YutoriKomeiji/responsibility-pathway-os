<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1.0a2 -->
<!-- RPOS-DOC-STATUS: public-alpha-published -->
<!-- RPOS-DOC-COUNTERPART: README.md -->

# RPOS — Responsibility Pathway Operating System

[![Standalone Verification](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/standalone-verify.yml/badge.svg?branch=main)](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/standalone-verify.yml)
[![Formal Assurance](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/formal-assurance.yml/badge.svg?branch=main)](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/formal-assurance.yml)
[![Field Portability](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/field-portability.yml/badge.svg?branch=main)](https://github.com/YutoriKomeiji/responsibility-pathway-os/actions/workflows/field-portability.yml)
[![PyPI](https://img.shields.io/pypi/v/responsibility-pathway-os?label=PyPI)](https://pypi.org/project/responsibility-pathway-os/)
[![Python](https://img.shields.io/pypi/pyversions/responsibility-pathway-os)](https://pypi.org/project/responsibility-pathway-os/)
[![License](https://img.shields.io/github/license/YutoriKomeiji/responsibility-pathway-os)](LICENSE)

**外部処理の結果が分からないとき、勝手に成功・失敗へ決めず、確認・修復・再開まで責任をつなぐPython/SQLiteランタイムです。**

AIエージェントが外部APIを実行した直後に通信が切れると、外部処理が完了したかどうかを即座に判断できないことがあります。この状態で単純にリトライすると、二重決済、二重デプロイ、二重通知、権限変更の重複につながる可能性があります。

RPOSは、承認、実行要求、外部作用、確認、結果不明、修復、再開、Human Returnを一つの責任経路として保持します。

> **確認できないものを、確認済みとして扱わない。そのうえで、次に必要な判断へつなげる。**

## まず試す

Version: **0.1.0a2** — 現在の公開版です。

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

- [PyPI 0.1.0a2](https://pypi.org/project/responsibility-pathway-os/0.1.0a2/)
- [製品サイト](https://yutorikomeiji.github.io/responsibility-pathway-os/)
- [公開記事](https://zenn.dev/dantarg/articles/rpos-public-alpha-010a2)

`0.1.0a2`は継続開発中の0.x系ですが、公開されている対応範囲では実際に試せます。現在の`main`にある3本の統合デモはリリース後に追加されたため、デモを実行する場合はソースをチェックアウトしてください。

## RPOSが分けて扱うもの

AIエージェントや自動化では、別々の出来事が一つの「成功」にまとめられやすくなります。RPOSは次を明示的に分離します。

- **人間の承認と実行権限は同じではない** — 修復準備ができても、古い許可だけで自動再開しません
- **実行要求と外部作用は同じではない** — `dispatch`しただけで外部システムが変わったとは判断しません
- **成功レスポンスと外部作用の確認は同じではない** — APIレスポンスやレシートだけを現実の証明にしません
- **不確実性は不確実性として保持する** — `EFFECT_UNKNOWN`で結果不明を保持し、確認なしの自動リトライや誤った完了へ進めません
- **停止後も責任担当を保持する** — 再起動、照合、修復、明示的な再開、Human Returnを同じ責任経路へ接続します

```text
提案
  ↓
Human Gate
  ↓
承認
  ↓
実行要求
  ↓
外部作用の確認
  ↓
結果不明 / 修復
  ↓
明示的な再開
  ↓
完了 / Human Return
```

## 現在実装されているもの

- Python/SQLiteによる永続的な責任状態マシン
- Human Gateと実行権限の明示的な境界
- 限定された実行要求、再起動、照合、修復、再開、Human Return
- 成功レスポンスを自動的に外部作用の完了へ昇格させない仕組み
- CLIと実行可能な評価シナリオ
- `authority_effect: "none"`を持つResponsibility State Envelopeテンプレート
- 再現可能な公開エクスポート、SBOM、リリース証拠
- Windows/Pythonのフィールド互換性チェック
- 選択した責任不変条件を機械検証するLean 4プロジェクト

## 状態と権限の考え方

主な状態:

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`

- `AUTHORIZED` — 実行条件が整っている。実行開始や成功そのものではない
- `DISPATCHING` — 要求を出したが、外部で何が起きたかは未確定
- `EFFECT_UNKNOWN` — 外部作用が起きた可能性はあるが確認できていない
- `REPAIR_REQUIRED` — 続行前に修復や確認が必要
- `READY_TO_RESUME` — 修復準備は整ったが、再開権限は別途必要
- `COMPLETED` — APIレスポンスだけではなく、限定された確認後に成立

**モデルの提案は実行権限ではありません。人間の承認も、障害後の再実行権限として永続するわけではありません。**

## 実行可能サンプル

```bash
python examples/happy_path_verified.py
python examples/human_gate_denied.py
python examples/effect_unknown_restart_reconcile.py
python examples/quick_start_end_to_end.py
python examples/idempotency_replay_guard.py
python examples/human_return_reauthorization.py
python examples/adapter_exception_containment.py
python examples/reconciliation_unresolved_human_return.py
```

各サンプルは、Human Gate、`EFFECT_UNKNOWN`、再起動、照合、修復、再開権限、リプレイ防止、アダプター例外、Human Returnの限定シナリオを確認するものです。

## 統合デモ

現在の`main`には、`examples/production_grade_demos/`以下に、より実運用へ近い統合デモがあります。

```bash
python examples/production_grade_demos/run_demo.py
```

対象シナリオ:

- **仕入先支払の結果不明** — 外部サービスが支払処理後に接続を切り、再起動後の独立読み戻しで重複実行なしに結果を確認
- **本番デプロイの拒否と修復** — 外部拒否後に`REPAIR_REQUIRED`へ入り、修復後も人間の再開権限を確認
- **特権アクセス削除の見送り** — Human Gateで実行しない判断になった場合、外部作用が0のままであることを確認

ローカルホスト上の外部サービスは再現可能なテスト用フィクスチャです。実際の決済サービス、本番デプロイ基盤、IAMではありません。デモ成功は、そのシナリオとテスト環境で確認できたことを示します。

## Lean 4による形式検証

RPOSは`formal/assurance-catalog.json`で、運用リスク、Lean定理、Pythonテスト、モデル範囲、証明上限の対応を公開しています。

現在の主要な機械検証項目:

1. Human Gateは直接の実行権限ではない
2. `VERIFIED`だけが直接`COMPLETED`へ入れる
3. `EFFECT_UNKNOWN`は完了ではない
4. 修復準備は実行権限ではない
5. APIレスポンスは外部作用の検証ではない
6. モデルの提案は運用権限ではない

これらは限定したモデル上のLean 4定理です。Pythonランタイム全体、本番環境、法的責任、組織権限、任意の外部システムまで形式証明したという意味ではありません。

## 対応範囲と既知の制約

RPOSは、現在公開している範囲では工学評価や限定的な統合に利用できます。一方、無人の高影響本番運用を現在の公開版だけで完結させることは想定していません。

RPOS単体では次を保証・生成しません。

- 法的・組織的な権限
- 任意の外部システムの正しさ
- 任意のシステムに対するexactly-once
- APIレスポンスだけによる外部作用の証明
- すべての本番環境への適合
- Python実装全体の形式証明

不足する環境・攻撃・失敗条件が見つかった場合は、Issue、セキュリティ報告、フィールドテストとして改善ループへ取り込みます。

- [SECURITY.md](SECURITY.md)
- [SUPPORT.md](SUPPORT.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## ライセンス

MIT License。
