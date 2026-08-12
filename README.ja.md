<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1.0a1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: README.md -->

# RPOS — Responsibility Pathway Operating System

RPOS は、重大な影響を伴う AI・自動化ワークフローのための、実行可能な責任経路オペレーティング層です。

基本原則は、**承認は実行ではなく、実行受付は外部効果の証明ではなく、失敗や不確実性によって責任を消してはいけない**、です。

RPOS は次の責任経路を保持します。

`提案 -> Human Gate -> 承認 -> dispatch -> 効果検証 -> 不確実性 -> 修復 -> 明示的再開 -> 完了`

## Public alpha status

Version: **0.1.0a1 candidate — Early Public Alpha / Executable Preview**

現在の実装には、Python/SQLiteの実行コア、永続的責任状態、Human Gate、限定されたdispatch attempt、外部効果との分離、reconciliation、repair/resume、証拠履歴、再利用可能なResponsibility State Envelope（責任状態エンベロープ）、guideline/evidence view、provenance、CLI、実行可能サンプル、限定範囲のmachine-checked Lean formal modelが含まれます。

このalphaは工学評価と限定的pilotを目的としており、無人の本番運用を前提としていません。

## なぜ RPOS が必要か

Agentシステムでは、ツール実行が成功を返しても、現実の効果が未発生・部分的・重複・不明・検証不能である場合があります。また、障害後のretryで人間の意思決定境界が失われることもあります。

RPOSはそれらを明示状態として保持します。

- `AUTHORIZED` は実行開始・成功を意味しません。
- `DISPATCHING` は発行済みだが未解決のattemptを保持します。
- `EFFECT_UNKNOWN` は不確実性をfalse successに変換しません。
- `REPAIR_REQUIRED` は修復責任を明示します。
- `READY_TO_RESUME` は修復準備完了であり、実行許可ではありません。
- 再開は、新しいdispatch attemptの前にauthorityを明示的に復元します。
- `COMPLETED` はtransport receiptではなく、限定されたverificationの後にのみ成立します。

## Install

Python 3.11+ が必要です。

```bash
python -m pip install responsibility-pathway-os==0.1.0a1
rpos --db rpos.db boot
```

source checkoutでは:

```bash
python -m pip install -e .
python examples/quick_start_end_to_end.py
```

## 実行可能サンプル

public alpha candidateには4つの主要シナリオがあります。

```bash
python examples/happy_path_verified.py
python examples/human_gate_denied.py
python examples/effect_unknown_restart_reconcile.py
python examples/quick_start_end_to_end.py
```

それぞれ以下を実行します。

1. Human Gate承認 -> 限定された独立verification -> completion
2. Human Gate拒否 -> dispatchなし
3. successful receipt -> `EFFECT_UNKNOWN` -> process restart -> observation-only reconciliation -> completion
4. first attempt失敗 -> `REPAIR_REQUIRED` -> repair preparation -> `READY_TO_RESUME` -> explicit resume authorization -> fresh attempt -> `EFFECT_UNKNOWN` -> restart -> reconciliation -> completion

これらは各限定シナリオに対するexecutable evidenceであり、一般的なproduction correctnessを証明するものではありません。

## Responsibility State Envelope templates

`templates/catalog.json`には、以下の中立ロール向け再利用templateがあります。

- operation proposal
- Human Gate decision
- verification contract
- repair plan
- resume authorization
- dependency evidence
- external evaluation evidence
- Human Return packet

推奨APIの `rpos.validate_envelope(...)` は、未知フィールド、必須フィールド欠落、未対応template kind/schema version、authority effectを主張するenvelopeを拒否します。

すべてのResponsibility State Envelopeは `authority_effect: "none"` を持ちます。**envelopeを記入・検証しても、operationの承認、dispatch、verification、completion、resumeは発生しません。** 初期alphaの `ResponsibilityPacket`、`validate_packet(...)`、`rpos.packet.v0.1` は下位互換のため維持します。詳細は `docs/ja/responsibility-packet-templates.md` を参照してください。

## Core responsibility states

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`。

normative transition modelは、成功receiptだけでcompletionへ進むこと、repair readinessだけでexecution authorityが復元されることを禁止します。

## 限定範囲の Lean 4 formal model

RPOSには、実際にmachine-checkedされたformal evidence surfaceがあります。専用Lean CIで、宣言されたformal modelを **Lean 4.32.2** によりコンパイル済みです。

現在のmodule:

- `formal/lean/RPOSState.lean` — state、direct transition、local invariant
- `formal/lean/RPOSReachability.lean` — 限定されたmulti-step reachabilityとdirect shortcut禁止
- `formal/lean/RPOSEvidenceBoundary.lean` — authorization-relevant evidence、external-effect verification evidence、receipt、evaluation、dependency evidenceの限定的分離

machine-checkedされたpropertyの例:

- `AUTHORIZED`だけが直接`DISPATCHING`へ入れる
- `VERIFIED`だけが直接`COMPLETED`へ入れる
- `EFFECT_UNKNOWN`から直接completionできない
- `REPAIR_REQUIRED`から直接dispatchできない
- `READY_TO_RESUME`は直接dispatchせず、`AUTHORIZED`を経由してauthorityを復元する
- 宣言されたabstract modelでは、execution receipt、evaluation evidence、dependency evidenceはexternal-effect verification evidenceにならない

positive reachability theoremはpathの存在を示すwitnessであり、livenessや必ず完了することを保証しません。

**Formal proof evidenceはPython implementationの正しさを証明しません。** RPOSは、formal proof、executable implementation evidence、operational external-effect evidenceを明示的に分離します。詳細は `formal/lean/README.md` を参照してください。

## Evidence boundaries

RPOSは証拠種別を分離し、ある証拠が別の証拠の代わりになることを防ぎます。

- authority / admission
- execution / receipt
- external effect
- recovery / resume
- safety / capability evaluation evidence
- dependency / software-supply-chain evidence
- guideline evidence matrices
- engineering provenance と将来のpublic-claim review input

対応する状態遷移契約が明示的に要求しない限り、証拠記録だけでoperational responsibility stateは昇格しません。

## Defensive provenance

RPOSは、後日の専門家レビューで機能の導入時期・技術理由・交換可能な実装境界を再構築できるようengineering provenanceを保持します。

未公開の第三者特許請求項は設計入力にしません。public-claim review recordは実際の公開情報と公開請求項本文の参照がある場合だけ作成できます。

RPOS自身は、特許非侵害、特許無効、Freedom to Operate、先行技術充足性、請求項の法的範囲を判断しません。

## Japan-first development

初期導入profileはJapan-firstです。現在の限定的evidence workは日本の公的AI・software supply-chain guidanceを参照し、compliance判定ではなくevidence / gapを保持します。

国際mappingは、日本向けprofile / operating layerの安定後に行う予定です。

## 継続開発サイクル

RPOSは単独で閉じず、次のfeedback systemの一層として継続開発します。

```text
Responsibility Pathway Model / Paper
  -> Responsibility Pathway Engineering
  -> Responsibility Pathway Runtime
  -> RPOS
  -> formal + executable + operational evidence
  -> Engineering + Model / Paper
```

概念を下流へ流して実装・運用証拠にし、その結果を定義、counterexample、engineering obligation、limitation、empirical questionとして上流へ戻します。各層は別層のevidenceを代用してはいけません。

## Verification

現在のrelease-candidate verificationには以下が含まれます。

- focused Python tests
- source上で4つの主要サンプルをすべて実行
- wheel build
- isolated clean install
- installed CLIおよび4サンプル実行
- deterministic public-export reconstruction / verification
- 登録済み日英ドキュメントpairの検証
- 宣言された限定formal moduleに対する専用Lean 4 compilation

これらの成功は宣言された範囲内のevidenceです。本番適合性、法令適合、外部システムの正しさ、普遍的安全性、implementation全体のformal correctnessを証明しません。

## Not Proven

RPOS 0.1.0a1 は以下を証明・主張しません。

- production / enterprise readiness
- 法的・規制上のcompliance
- certification / official conformity
- universal AI safety
- 任意remote adapterやcredentialの正しさ
- 任意の外部システムに対するexactly-once effect
- 完全なsoftware-supply-chain trustworthiness
- Python implementation全体のformal correctness / conformance
- 任意operationのliveness / eventual completion
- patent non-infringement / invalidity / freedom to operate

## License

MIT License.

## Lineage

```text
Responsibility Pathway Design / Model
 -> Responsibility Pathway Engineering
 -> Responsibility Pathway Runtime
 -> RPOS — Responsibility Pathway Operating System
```

RPOSはauthority、execution、uncertainty、repair、明示的に承認されたresumptionを通してresponsibility continuityを維持するoperating layerとして独立開発されています。
