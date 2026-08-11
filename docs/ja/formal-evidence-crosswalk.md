<!-- RPOS-DOC-ID: RPOS-FORMAL-XWALK-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/formal-evidence-crosswalk.md -->

# RPOS 形式証拠クロスウォーク

Status: public alpha候補向けの限定された形式証拠マッピング。

この文書は、公開するRPOSの責任ルールをLean 4成果物と実行可能な実装証拠へ接続する。LeanモデルとPython runtimeの全体的な適合性を証明するものではない。

| 責任ルール | Lean証拠 | 実行可能証拠 | 前提・境界 | 未証明 |
|---|---|---|---|---|
| 直接`DISPATCHING`へ入れるのは`AUTHORIZED`のみ | `RPOS.only_authorized_enters_dispatching` | `examples/happy_path_verified.py`、focused runtime tests | Leanの`Step`は限定された規範的遷移関係 | Python/Leanの全体適合性 |
| Human Gateから直接dispatchできない | `RPOS.human_gate_cannot_dispatch_directly` | `examples/human_gate_denied.py` | Human Gateは宣言された状態・遷移の範囲でのみ形式化 | 任意の外部承認システムの正しさ |
| completionには`VERIFIED`が必要 | `RPOS.only_verified_enters_completed` | happy-path / reconciliationシナリオ | `VERIFIED`はRPOSの限定状態であり普遍的真理述語ではない | 任意の外部証拠の真実性・完全性 |
| execution receiptはexternal-effect verificationではない | `RPOS.receipt_not_effect_verification` | `examples/effect_unknown_restart_reconcile.py`、reconciliation tests | evidence classは意図的に限定 | 任意のreadback sourceの正しさ |
| `EFFECT_UNKNOWN`は直接completionできない | `RPOS.effect_unknown_cannot_complete_directly`、`RPOS.effect_unknown_is_not_completed` | restart/reconciliationシナリオ | completionへの正の経路は存在証明のみ | liveness / eventual completion |
| repair readinessだけではexecution authorityは復元されない | `RPOS.ready_to_resume_is_not_authorized`、`RPOS.repair_required_cannot_authorize_directly` | Quick Start/testsのrepair/resumeシナリオ | authority restorationを状態分離で明示 | 人間のauthorityの組織的・法的正当性 |
| resumeはfresh dispatchより先にauthorityを復元する | `RPOS.ready_to_resume_restores_authority`、`RPOS.resume_does_not_dispatch_directly` | repair -> ready -> resume -> fresh attemptシナリオ | resume pathは宣言された遷移モデルに限定 | RPOS外の任意retry semantics |
| 再利用可能なresponsibility packetはauthorityを付与できない | `RPOS.valid_reusable_packet_cannot_grant_authority`、`RPOS.valid_reusable_packet_has_no_authority_effect` | `src/rpos/template_packets.py`、`tests/test_template_packets.py` | Lean packet modelは公開契約`authority_effect = none`を対応付け | Python validatorとの形式的conformance |
| safety/capability/dependency evidenceはauthorizationを代替しない | `RPOS.safety_evaluation_not_authorization_relevant`、`RPOS.capability_evaluation_not_authorization_relevant`、`RPOS.dependency_evidence_not_authorization_relevant` | evaluation/dependency evidence tests | evidence relevanceは完全ontologyではなく抽象モデル | 外部評価器・dependency sourceの十分性 |
| positive reachabilityはlivenessではない | `RPOSReachability.lean`のtheorem scope | recovery examplesは経路を示すだけで完了保証ではない | `Steps`はモデル化された経路の存在を示す | 任意operationのeventual completion |

## 証拠クラス

RPOSは次の証拠を分離する。

1. 宣言された抽象モデル上のLean proof evidence。
2. Python実装・testによるexecutable evidence。
3. 実際の外部効果を観測・readbackしたoperational evidence。

一つのクラスの結果を、別クラスの証明として表現してはならない。

## 公開表現の境界

許容例: `Lean 4により、限定されたRPOSの状態・証拠境界invariantをmachine-checkしている。`

不許容の強い言い換え例: `RPOS全体は形式検証済み`、`LeanがPython runtimeの正しさを証明している`、`形式検証によりproduction safety/complianceが証明される`。
