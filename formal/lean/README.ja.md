<!-- RPOS-DOC-ID: RPOS-FORMAL-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-COUNTERPART: README.md -->

# RPOS Lean 4 Formal Assurance — Responsibility Pathway不変条件

RPOSはPython/SQLiteで実装された実行可能なResponsibility Pathway OSです。このディレクトリには、宣言されたRPOS modelの選択された責任不変条件をLean 4でmachine-checkするFormal Assurance layerがあります。

このformal surfaceは、次の3点を同時に見えるようにします。

1. **何の責任propertyをmachine-checkしているか**
2. **そのpublic assertionに対応するPython runtime testは何か**
3. **proof ceilingはどこか**

canonicalなpublic crosswalkは `../assurance-catalog.json` です。

## 公開済みmachine-checked responsibility assertions

| Operational Risk | Lean theorem | 宣言modelでの意味 |
| --- | --- | --- |
| Human decision stateがexecution authorityになる | `RPOS.human_gate_cannot_dispatch_directly` | `HUMAN_GATE`から直接`DISPATCHING`へ入れない |
| intermediate/transport successがcompletionになる | `RPOS.only_verified_enters_completed` | `VERIFIED`だけが直接`COMPLETED`へ入れる |
| 曖昧なexternal effectがsuccessへ潰される | `RPOS.effect_unknown_is_not_completed` | `EFFECT_UNKNOWN`と`COMPLETED`は別state |
| repair readinessがauthorityを暗黙復元する | `RPOS.ready_to_resume_is_not_authorized` | `READY_TO_RESUME`と`AUTHORIZED`は別state |
| API/transport receiptが現実effectの証明になる | `RPOS.receipt_is_not_effect_verification` | transport receiptはexternal-effect-verification evidenceではない |
| model outputが暗黙にauthorityになる | `RPOS.model_proposal_is_not_authority` | model proposalはauthorization-relevant evidenceではない |

これらのtheorem名は、**何を証明しているかをそのまま読めるようにしたdomain-readable name**です。より広い主張へ見せるためのmarketing aliasではありません。

## Build

Lean 4.32.2にpinしています。

```bash
cd formal/lean
lake build
```

CIとrelease evidenceも同じ限定formal projectをbuildし、exact-sourceのFormal Assurance manifestを生成します。

## Modules

- `RPOSState.lean` — state machine、Human Gate、completion、不確実性、resume-authority invariant
- `RPOSReachability.lean` — bounded multi-step reachabilityとdirect shortcut禁止
- `RPOSEvidenceBoundary.lean` — authority/effect verification/receipt/evaluation/dependency evidenceの分離
- `RPOSPacketBoundary.lean` — Responsibility State Envelope / packetのno-authority-effect property
- `RPOSOperationalBoundary.lean` — model proposal、human authorization、transport receipt、external observation、read-only observability boundary
- `RPOSTransparencyBoundary.lean` — transparencyとevidence distinction

## Python × Lean 4 evidence architecture

RPOSはLeanを飾りとして置きません。public Formal Assurance assertionはPython runtime testへcross-linkされています。

```text
operational risk
  -> named Lean theorem
  -> machine-checked abstract invariant
  -> corresponding Python runtime test(s)
  -> source identity + model scope + proof ceiling
```

これはLeanとPythonの自動的なrefinement proofではありません。runtime testはexecutable behaviorを独立に確認し、Lean theoremは宣言されたformal modelでnamed propertyを確立します。

## Formal layerが証明するもの

各theoremについて、Leanはsource module内のdefinitionとassumptionから、そのtheoremが述べるpropositionを証明します。

現在の6 assertionでは、例えば次をmachine-checkしています。

- Human Gateとdirect dispatchの構造的分離
- direct-transition modelでの`VERIFIED`→`COMPLETED` gate
- external-effect uncertaintyとcompletionの分離
- repair readinessとauthorizationの分離
- transport receiptとexternal-effect-verification evidenceの分離
- model proposalとOperational Authorityの分離

## Proof ceiling

Formal layer単体では次を確立しません。

- Python implementation全体のconformance
- 任意external observationの真実性・十分性
- 具体的human authorizationの正当性
- SQLite、adapter、OS、network、external service全体のcorrectness
- universal exactly-once
- production readiness、legal compliance、certification、organizational authority

これらはtheorem名で隠す弱点ではなく、別のevidence ownerまたはresponsibility ownerです。

## なぜ境界を明示するのか

RPOSはformal proof、executable implementation evidence、operational external-effect evidenceを別evidence classとして扱います。より強いpublic claimへ昇格するのは、足りないbridge evidenceが実際に供給・reviewされた場合だけです。

そのため、**証明が強い場所では強く述べ、evidenceが限定される場所では限定されたまま述べる**ことができます。
