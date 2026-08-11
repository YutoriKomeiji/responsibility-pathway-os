<!-- RPOS-DOC-ID: RPOS-FORMAL-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: README.md -->

# RPOS Lean Formalization — Public Alpha Candidate

Status: machine-checked bounded formal model / Lean 4 CI verified

## Verification evidence

`RP-CYCLE-001`で専用workflow `RPOS Lean formal verification` を導入し、宣言されたformal moduleをLean 4.32.2で実際にコンパイルしました。

この証拠が意味するのは、下記theorem sourceが宣言されたabstract modelについて設定済みLean compilerに受理された、という範囲です。Python implementation、外部システム、deployment、組織挙動、法的結論を証明するものではありません。

## Modules

- `RPOSState.lean` — normative responsibility state、direct transition relation、local transition invariant
- `RPOSReachability.lean` — uncertainty、repair、resumption、completionに関する限定されたreflexive/transitive reachability witnessとdirect shortcut禁止
- `RPOSEvidenceBoundary.lean` — authorization-relevant evidence、effect-verification evidence、receipt、evaluation、dependency/software-supply-chain evidenceの限定的分離

## Direct-transition invariants

| Invariant | Lean theorem |
|---|---|
| `AUTHORIZED`だけが直接`DISPATCHING`へ入れる | `RPOS.only_authorized_enters_dispatching` |
| `HUMAN_GATE`から直接dispatchできない | `RPOS.human_gate_cannot_dispatch_directly` |
| `VERIFIED`だけが直接`COMPLETED`へ入れる | `RPOS.only_verified_enters_completed` |
| `REPAIR_REQUIRED`から直接`AUTHORIZED`へ行けない | `RPOS.repair_required_cannot_authorize_directly` |
| `READY_TO_RESUME`と`AUTHORIZED`は別state | `RPOS.ready_to_resume_is_not_authorized` |
| resumeは直接dispatchしない | `RPOS.resume_does_not_dispatch_directly` |
| `EFFECT_UNKNOWN`と`COMPLETED`は別state | `RPOS.effect_unknown_is_not_completed` |

## Reachability / repair-resume properties

| Property | Lean theorem |
|---|---|
| `AUTHORIZED`にはnormative dispatch pathがある | `RPOS.authorized_reaches_dispatching` |
| `EFFECT_UNKNOWN`にはverification経由のcompletion witnessがある | `RPOS.effect_unknown_has_verified_completion_path` |
| repairにはreadinessからreauthorizationへのwitnessがある | `RPOS.repair_has_explicit_reauthorization_path` |
| `EFFECT_UNKNOWN`から直接completionできない | `RPOS.effect_unknown_cannot_complete_directly` |
| `REPAIR_REQUIRED`から直接dispatchできない | `RPOS.repair_required_cannot_dispatch_directly` |
| `READY_TO_RESUME`から直接completionできない | `RPOS.ready_to_resume_cannot_complete_directly` |
| `READY_TO_RESUME`は`AUTHORIZED`を通してauthorityを復元する | `RPOS.ready_to_resume_restores_authority` |

positive reachability theoremは**path existence witness**であり、liveness claimではありません。たとえば`EFFECT_UNKNOWN`から`COMPLETED`へのpathが存在することは、すべての未解決operationが最終的に完了することを意味しません。

## Evidence-class separation properties

限定されたevidence modelでは以下をmachine-checkしています。

- safety-evaluation evidenceはauthorization-relevant evidenceではない
- capability-evaluation evidenceはauthorization-relevant evidenceではない
- dependency/supply-chain evidenceはauthorization-relevant evidenceではない
- execution receiptはexternal-effect-verification evidenceではない
- safety/capability evaluation evidenceはexternal-effect-verification evidenceではない
- dependency evidenceはexternal-effect-verification evidenceではない

またauthority-admissionとrecovery/resume evidenceをauthorization-relevant classとして表現しますが、**evidenceを持つこと自体がauthority付与になるわけではありません**。

## Evidence layers

RPOSは3つのevidence layerを分離します。

1. **Formal proof evidence** — 明示されたabstract model上のLean theorem
2. **Executable implementation evidence** — 現行implementation上のPython tests / runnable examples
3. **Operational effect evidence** — 具体的な外部効果に対するobservation / readback

どのlayerも別layerの証拠を代用しません。

## Not Proven

これらのLean fileは以下を証明しません。

- Python implementation全体のcorrectness / conformance
- SQLiteのcorrectness / durability
- external adapter/service behavior
- 任意外部システム上のexactly-once behavior
- deployment environmentのsecurity
- legal / regulatory compliance
- patent non-infringement / freedom to operate
- organizational responsibility / authority legitimacy
- real-world AI/system safety
- runtime evidenceの真実性・完全性
- 任意operationのliveness / eventual completion

今後のcycleでは、このevidence boundaryを維持したままtemporal/trace invariantとimplementation-to-model conformanceを拡張します。
