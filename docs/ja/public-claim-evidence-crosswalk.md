<!-- RPOS-DOC-ID: RPOS-CLAIM-XWALK-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/public-claim-evidence-crosswalk.md -->

# RPOS 公開主張 / 証拠クロスウォーク

Status: public alpha候補向けのreview可能なclaim ceiling。

RPOSは、公開artifactと証拠が実際に支える範囲で、強い技術用語を使用してよい。このcrosswalkは各用語に必要な証拠と、依然として範囲外となる強い言い換えを定義する。

| 用語 / 公開主張 | 許容する限定表現 | 実装証拠 | test/example証拠 | 形式証拠 | 未証明 / 不許容の強い言い換え |
|---|---|---|---|---|---|
| Responsibility Pathway Operating System | consequentialなAI/automation workflow向けの実行可能なresponsibility operating layer | `src/rpos/`、durable state、CLI、reconciliation/repair/resume | focused tests、4 primary examples | bounded state/evidence invariants | general-purpose OSではない、governance completedではない、production certificationではない |
| runtime | durable responsibility stateを持つ実行可能なPython runtime/service layer | `src/rpos/` package | wheel/install/CLI tests/examples | runtime全体の形式証明なし | 任意adapter/external systemの正しさを証明しない |
| formally modeled | 選択された責任状態・遷移・evidence class・packet authority boundaryをLean 4で表現 | `formal/lean/*.lean` | Lean CI compilation | theorem sources | Python実装全体が形式モデル化済みという意味ではない |
| formally verified | Leanが受理した具体的theorem/propertyを名指しする場合のみ | theorem-specific | Lean workflow | theorem-specific | `RPOS全体が完全に形式検証済み`とは言わない |
| verified | 対象と検証方法を明記する。例: configured readback/reconciliation後のverified external effect | verification/reconciliation implementation | happy path、restart/reconciliation examples/tests | receiptとeffect evidenceの分離 | receipt、dispatch成功、local returnだけをverified external effectと扱わない |
| assurance | reviewとsafe incompletionを支える限定されたevidence/authority/effect boundary | responsibility state/evidence surfaces | focused tests/examples | evidence-separation invariants | universal assurance、安全認証、compliance保証ではない |
| security | 実装されているsecurity boundary/documentationとfail-closed validation | validators、credential boundaries、bounded adapter design | 関連validation/security tests | deployment security theoremなし | 任意deploymentがsecureという主張ではない |
| evidence | authorization/evaluation/dependency/verification/provenance/reviewに用いるtyped/source-tagged artifact | evidence models/reports | evidence-specific tests | evidence-class separation | evidence保持だけでauthority、真実性、完全性は証明されない |
| external-effect verification | configured operation contractに対して十分な独立observation/readback | reconciliation/readback path | restart/reconciliation example/tests | receipt != effect verification | exactly-once、普遍的に信頼可能なreadbackは証明しない |
| reconciliation | 後続evidence/readbackでuncertain external effectを解消する明示的process | reconciliation runtime path | `effect_unknown_restart_reconcile.py` and tests | uncertaintyからverification/repairへのmodeled path | すべてのuncertaintyが解消可能とは保証しない |
| repair | failure/uncertainty後、resumption要求前のreadinessを確立し得る限定準備 | repair state/API | repair/resume scenario/tests | `REPAIR_REQUIRED -> READY_TO_RESUME` boundary | repairはexecution authorityを復元しない |
| resume | fresh attemptに向けてauthorizationを復元する明示的authority-restoration step | resume API/state transition | repair -> ready -> resume -> fresh attempt scenario/tests | ready-to-resume -> authorized、直接dispatchなし | resumeはretryではなく、external effectも証明しない |
| Human Gate | configured consequential actionに対する明示的human decision boundary | gate/admission surfaces | denial/no-dispatch scenario/tests | Human Gate cannot directly dispatch | softwareへの法的/組織的責任移転ではない |
| responsibility packet/template | role/evidence/decision handoff向けmachine-readable structure | `template_packets.py`、`templates/` | `test_template_packets.py` | packet authority boundary | packet/templateはauthorityやstate transitionを生成できない |

## Claim構成ルール

公開文は原則として次の経路から再構築可能にする。

`claim -> implementation artifact -> executable evidence -> applicableなformal evidence -> assumptions -> not_proven`

いずれかの証拠classが存在しない場合、その証拠classが存在するような公開表現をしてはならない。

## 検索 / AI要約への耐性

正確である限り、強い権威語を避ける必要はない。ただし検索エンジンやLLMによる過剰な一般化を抑えるため、release-facing pageでは強い語の近くに対象scopeを置く。

- `形式検証済みシステム`ではなく、`Lean 4でmachine-checkされた限定state-transition invariant`。
- `実行を検証した`ではなく、`configured readbackによりexternal effectを検証した`。
- `executable responsibility operating layer`とalpha / Not Proven boundaryを近接して提示する。
