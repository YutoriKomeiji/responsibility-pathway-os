<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1.0a1 -->
<!-- RPOS-DOC-STATUS: public-alpha -->
<!-- RPOS-DOC-COUNTERPART: README.md -->

# RPOS — Responsibility Pathway Operating System

**Pythonで実行可能な責任経路と、Lean 4でmachine-checkされた重要な責任不変条件を統合するResponsibility Pathway OSです。**

RPOSは、影響を伴うAI・自動化ワークフローのためのオープンソース実装です。Python/SQLiteによる実行runtimeと、Human Gate、Operational Authority、dispatch、外部作用検証、不確実性、修復、再開、完了に関する選択された不変条件をLean 4で機械検証するFormal Assurance Surfaceを組み合わせます。

責任をlog、policy document、model outputのどれか一つへ還元せず、次の経路を実行可能な状態として保持します。

`提案 -> Human Gate -> 承認 -> dispatch -> 外部作用検証 -> 不確実性 -> 修復 -> 明示的再開 -> 完了`

基本原則は、**承認は実行ではなく、実行receiptは外部作用の証明ではなく、失敗や不確実性によって責任を消してはいけない**、です。

## Python × Lean 4 — 実行可能な責任経路と機械検証された不変条件

現在の公開実装には、次の両方があります。

- Python/SQLiteによる実行可能なOperational State Machine。永続状態、Human Gate、限定dispatch、restart/reconciliation、repair/resume、evidence history、CLI、実行サンプルを含みます。
- Lean 4による再現可能なFormal Assurance project。選択された責任不変条件をmachine-checkし、`formal/assurance-catalog.json`を通じて対応するPython runtime testへcross-linkします。

公開済みのmachine-checked assertionは次の6件です。

1. `RPOS.human_gate_cannot_dispatch_directly` — Human Gateは直接dispatchする権限ではない。
2. `RPOS.only_verified_enters_completed` — `VERIFIED`だけが直接`COMPLETED`へ入れる。
3. `RPOS.effect_unknown_is_not_completed` — 未解決の外部作用不確実性は完了ではない。
4. `RPOS.ready_to_resume_is_not_authorized` — repair readinessは実行権限ではない。
5. `RPOS.receipt_is_not_effect_verification` — transport/API receiptは外部作用検証ではない。
6. `RPOS.model_proposal_is_not_authority` — model proposalはOperational Authorityではない。

各assertionには、Lean theorem、対応するPython runtime test evidence、model scope、source identity、proof ceilingを明示します。

これは単なる文書上のルールより強く、同時に「Python runtime全体が形式証明済み」という主張より限定的です。**名前を付けたabstract invariantはLean 4でmachine-checkし、実装証拠と外部運用証拠は別の検証可能なevidence classとして保持します。**

## Public Alpha

Version: **0.1.0a1 — Early Public Alpha / Executable Preview**

`responsibility-pathway-os==0.1.0a1` はPyPIで公開されています。

```bash
python -m pip install responsibility-pathway-os==0.1.0a1
rpos --db rpos.db boot
```

Python 3.11+ が必要です。

このalphaは工学評価と限定pilotを目的としており、無人production運用を前提としていません。

## なぜRPOSが必要か

Agentや自動化システムでは、APIやtoolがsuccess receiptを返しても、現実の作用が未発生・部分的・重複・曖昧・検証不能である場合があります。また、障害後のretryやrepairで、誰が再実行を許可したかというHuman Gate境界を失うことがあります。

RPOSはそれを状態として消しません。

- `AUTHORIZED` は実行開始や成功ではない。
- `DISPATCHING` は発行済みだが未解決のattemptを保持する。
- `EFFECT_UNKNOWN` は不確実性をfalse successへ変換しない。
- `REPAIR_REQUIRED` は修復責任を明示する。
- `READY_TO_RESUME` は修復準備完了であり実行許可ではない。
- resumeはfresh dispatchの前にauthorityを明示的に復元する。
- `COMPLETED` はtransport receiptではなく、限定されたverificationの後に成立する。

## Core responsibility states

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`。

## 実行可能サンプル

8つの公開シナリオがあります。

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

Human Gate承認/拒否、receipt後の`EFFECT_UNKNOWN`、restart、reconciliation、repair、explicit resume authority、idempotency guard、adapter exception、Human Returnを実行例として確認できます。

## Lean 4 Formal Assurance Surface

Formal projectは**Lean 4.32.2**にpinされています。

```bash
cd formal/lean
lake build
```

主なmodule:

- `RPOSState.lean` — Human Gate、completion、不確実性、resume authorityを含むstate invariant
- `RPOSReachability.lean` — bounded multi-step reachabilityとshortcut禁止
- `RPOSEvidenceBoundary.lean` — authorization/effect verification/receipt/evaluation/dependency evidenceの分離
- `RPOSPacketBoundary.lean` — Responsibility State Envelope/packetのno-authority-effect property
- `RPOSOperationalBoundary.lean` — model proposal、human authorization、receipt、external observationの責任境界
- `RPOSTransparencyBoundary.lean` — transparency/evidence distinction

Formal Assurance Viewerは、Operational RiskからLean theorem、Python runtime test、source hash、model scope、proof ceilingまで追跡できる公開surfaceです。

## Evidence boundaries

RPOSは次を別々のevidence classとして扱います。

- authority / admission
- execution / receipt
- external effect
- recovery / resume
- safety / capability evaluation
- dependency / software supply chain
- guideline evidence
- engineering provenance

証拠を記録しただけでoperational stateが自動昇格することはありません。

Formal proofは宣言したabstract modelのnamed propertyを確立しますが、それ単体ではPython implementation全体のconformanceや外部観測の真実性を確立しません。

## Responsibility State Envelope

`templates/catalog.json`にはoperation proposal、Human Gate decision、verification contract、repair plan、resume authorization、dependency evidence、external evaluation evidence、Human Return packetのtemplateがあります。

すべてのEnvelopeは `authority_effect: "none"` を持ちます。**Envelopeの作成やvalidation自体はauthorize、dispatch、verify、complete、resumeを行いません。**

## Verification

公開alphaのverification routeには次が含まれます。

- Python test suite全体
- 8つのsource example実行
- wheel/sdist buildとisolated clean install
- repository外からのinstalled CLI/API/Quick Start確認
- exact-HEAD public-export reconstruction
- CycloneDX SBOMとSHA-256 artifact evidence
- public source boundaryのlikely-secret scan
- Windows Python 3.11/3.12 field-portability check
- pinned Lean 4 `lake build`

## Claim boundary と promotion

RPOSは「今は証拠が足りない主張」と「software単体では越えない恒久責任境界」を分離します。

Evidenceが追加されれば昇格可能な主張には、production readiness、より広いplatform support、implementation-wide formal conformance、software-supply-chain trust、公開scenarioを超えるdomain effectivenessがあります。

一方、次は成熟してもRPOS単体では生成しません。

- 法的・組織的authority
- 任意の外部systemの正しさ
- verification contractなしでのreceipt→external effect証明
- 人間/組織からsoftwareへの最終責任移転
- 任意外部systemに対するuniversal exactly-once guarantee

詳細は `docs/ja/claim-boundary-promotion.md` を参照してください。

## 継続開発lineage

```text
Responsibility Pathway Model / Paper
 -> Responsibility Pathway Engineering
 -> Responsibility Pathway Runtime
 -> RPOS — Responsibility Pathway Operating System
 -> formal + executable + operational evidence
 -> Engineering + Model / Paper
```

RPOSは、authority、execution、uncertainty、repair、return、explicitly authorized resumptionを通じてResponsibility Pathwayを保持する独立実装です。

## License

MIT License.
