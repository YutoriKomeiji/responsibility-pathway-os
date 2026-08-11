<!-- RPOS-DOC-ID: RPOS-TEMPLATE-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/responsibility-packet-templates.md -->

# Responsibility Packet Templates

RPOSは、繰り返し発生する責任の引き渡しを整形するための、再利用可能な機械可読packet templateを提供します。レビュー、検証、修復、再開、依存関係証拠、外部評価証拠、Human Returnに必要な情報を一貫した形で準備できます。

## 重要な境界

有効なpacketは `authority_effect: "none"` を持ちます。

packetを記入、検証、保存、送信しても、**それだけでは**操作の承認、dispatch、外部効果の成立、`VERIFIED` / `COMPLETED`への遷移、resume authorityの回復は発生しません。これらには、対応するRPOS状態遷移と正しい権限主体が必要です。

## 含まれるtemplate kind

- `operation_proposal`
- `human_gate_decision`
- `verification_contract`
- `repair_plan`
- `resume_authorization`
- `dependency_evidence`
- `external_evaluation_evidence`
- `human_return_packet`

カタログは `templates/catalog.json` にあります。

## 検証動作

`rpos.validate_packet(...)` は意図的にstrict / fail-closedです。

- envelopeの未知フィールドを拒否する
- 選択したtemplate kindに対するpayloadの未知フィールドを拒否する
- 必須フィールド欠落を拒否する
- 必須文字列の空値を拒否する
- 未対応のtemplate kind / schema versionを拒否する
- `none`以外の`authority_effect`を拒否する

これにより、**責任情報を準備すること**と**実際に権限や状態を変更すること**を分離します。

## 推奨導入フロー

1. `templates/catalog.json`から必要なpacketをコピーする
2. 中立な組織ロールでplaceholderを置換する
3. packetを検証する
4. 必要に応じて根拠証拠を添付・記録する
5. 実際の責任主体またはHuman Gateへ提示する
6. 権限を伴う状態遷移はpacketではなくRPOS service / CLIを通して実施する
7. 未解決ならResidual OwnerとHuman Return Pointを保持する

## 証拠クラスの分離

Dependency evidenceとexternal evaluation evidenceは、authorizationおよびexternal-effect verificationとは別物です。packetがそれらを保持しても、権限や運用上の完了へ変換することはできません。

## Not Proven

Template validationは、入力内容の真実性、証拠の完全性、法的十分性、規制遵守、権限の正当性、外部システムの挙動、production safetyを証明しません。
