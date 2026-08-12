<!-- RPOS-DOC-ID: RPOS-TEMPLATE-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/responsibility-packet-templates.md -->

# Responsibility State Envelope Templates

RPOSは、繰り返し発生する責任の引き渡しを整形するための、再利用可能な機械可読 **Responsibility State Envelope（責任状態エンベロープ）** templateを提供します。レビュー、検証、修復、再開、依存関係証拠、外部評価証拠、Human Returnに必要な責任文脈を一貫した形で準備・搬送できます。

初期alphaで用いていた `ResponsibilityPacket` と `rpos.packet.v0.1` は、下位互換のため引き続き受理します。ただし今後の公開上の推奨名称は Responsibility State Envelope です。

## 重要な境界

有効なenvelopeは `authority_effect: "none"` を持ちます。

envelopeを記入、検証、保存、送信しても、**それだけでは**操作の承認、dispatch、外部効果の成立、`VERIFIED` / `COMPLETED`への遷移、resume authorityの回復は発生しません。これらには、対応するRPOS状態遷移と正しい権限主体が必要です。

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

推奨APIの `rpos.validate_envelope(...)` は意図的にstrict / fail-closedです。

- envelopeの未知フィールドを拒否する
- 選択したtemplate kindに対するpayloadの未知フィールドを拒否する
- 必須フィールド欠落を拒否する
- 必須文字列の空値を拒否する
- 未対応のtemplate kind / schema versionを拒否する
- `none`以外の`authority_effect`を拒否する

`rpos.validate_packet(...)` は下位互換aliasとして残します。

これにより、**責任文脈を準備・搬送すること**と**実際に権限や状態を変更すること**を分離します。

## 推奨導入フロー

1. `templates/catalog.json`から必要なtemplateをコピーする
2. 中立な組織ロールでplaceholderを置換する
3. envelopeを検証する
4. 必要に応じて根拠証拠を添付・記録する
5. 実際の責任主体またはHuman Gateへ提示する
6. 権限を伴う状態遷移はenvelopeではなくRPOS service / CLIを通して実施する
7. 未解決ならResidual OwnerとHuman Return Pointを保持する

## 証拠クラスの分離

Dependency evidenceとexternal evaluation evidenceは、authorizationおよびexternal-effect verificationとは別物です。envelopeがそれらを保持しても、権限や運用上の完了へ変換することはできません。

## 互換性

現在の推奨schema identifierは `rpos.responsibility-state-envelope.v0.1` です。従来の `rpos.packet.v0.1` も既存alpha artifactを読み取れるよう受理します。この互換性は、authority-neutralという意味論を変更しません。

## Not Proven

Template validationは、入力内容の真実性、証拠の完全性、法的十分性、規制遵守、権限の正当性、外部システムの挙動、production safetyを証明しません。
