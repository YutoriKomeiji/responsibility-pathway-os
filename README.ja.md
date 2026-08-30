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

AIエージェントが外部APIを実行した直後に、通信が切れた。

**もう一度実行してよいでしょうか。**

最初の要求で、外部systemはすでに変わっているかもしれません。blind retryすれば、二重決済、二重deploy、二重通知、権限変更の重複などが起きるかもしれない。反対に「失敗した」と閉じれば、すでに起きた現実の変更を見失うかもしれません。

**RPOSは、この「分からない」を成功・失敗・再実行のどれかへ勝手に潰さず、そのまま責任を伴う状態として保持するOpen SourceのPython/SQLite runtimeです。** 承認、実行、外部作用、検証、修復、再開、人への責任返却を、切れない経路として扱います。

> **分からないとき、責任まで消してはいけない。**

この考え方を **Responsibility Pathway Operating System（責任経路OS / RPOS）** と呼んでいます。責任を一つの承認フラグやログではなく、判断から現実の作用まで続く「経路」として扱うための仕組みです。

## Quick start

公開済みPublic Alphaを入れるだけなら:

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

- **公開済みruntimeを試す:** [PyPI 0.1.0a2](https://pypi.org/project/responsibility-pathway-os/0.1.0a2/)
- **source・test・Lean・CI・最新demoを見る:** このrepository
- **ブラウザで全体像を見る:** [Product site](https://yutorikomeiji.github.io/responsibility-pathway-os/)
- **問題設定から読む:** [Zenn — RPOS 0.1.0a2公開記事](https://zenn.dev/dantarg/articles/rpos-public-alpha-010a2)

PyPI `0.1.0a2` には公開済みruntimeが入っています。3本のproduction-grade integration demoは、そのrelease後にcurrent `main`へ追加したものなので、demoを動かす場合はsource checkoutを使ってください。

## RPOSで何を分けるのか

AI agent / automationでは、別々の出来事が一つの「成功」に潰れやすくなります。RPOSは次を分けて保持します。

- **人間の承認と実行権限は同じではない** — 修復準備ができても、古い許可を自動復元しない
- **実行要求と現実の作用は同じではない** — dispatchしただけでは外部systemが変わったとは断定しない
- **成功応答と外部作用の検証は同じではない** — receiptを現実の証明にしない
- **不明は不明のまま残す** — `EFFECT_UNKNOWN` で結果不明を保持し、blind retryやfalse completionへ進めない
- **回復後も責任の引受先を消さない** — restart、reconciliation、repair、明示的再開、Human Returnを同じ責任経路へ接続する

実行可能な経路は次の形です。

`提案 -> Human Gate -> 承認 -> dispatch -> 外部作用検証 -> 不確実性 -> 修復 -> 明示的再開 -> 完了 / Human Return`

基本原則は、**承認は実行ではなく、実行receiptは外部作用の証明ではなく、失敗や不確実性によって責任を消してはいけない**、です。

## Project identity / 帰属について

RPOSは `YutoriKomeiji/responsibility-pathway-os` において、Responsibility Pathway lineageの中で独立開発されています。株式会社GhostDrift数理研究所の開発物・関連プロジェクト・同社「責任OS」の実装ではありません。用語の類似は、共通の著者・所有者・開発系譜を意味しません。

RPOSはmodel wrapperでも、policy documentでも、logging layerでもありません。**RPOS owns operation, not intelligence.** Modelは交換可能なproposal sourceであり、proposalを出しただけではauthorityになりません。

## 現在実装されているもの

Public Alphaには次が含まれます。

- Python/SQLiteによる永続的なResponsibility State Machine
- Human GateとOperational Authorityの明示的境界
- 限定dispatch、restart/reconciliation、repair/resume、Human Return
- transport successを自動的にcompletionへ昇格させないexternal-effect separation
- CLIと実行可能なevaluation scenario
- `authority_effect: "none"` を持つResponsibility State Envelope template
- 再現可能なpublic-export、SBOM、release evidence生成
- Windows/Python field-portability check
- 選択された責任不変条件をmachine-checkする再現可能なLean 4 project

## Python × Lean 4 — 実行可能な責任経路と機械検証された不変条件

RPOSは `formal/assurance-catalog.json` で次のcrosswalkを公開します。

`operational risk -> Lean theorem -> Python runtime test -> model scope -> proof ceiling`

現在のmachine-checked assertionは次の6件です。

1. `RPOS.human_gate_cannot_dispatch_directly` — Human Gateは直接dispatchする権限ではない。
2. `RPOS.only_verified_enters_completed` — `VERIFIED`だけが直接`COMPLETED`へ入れる。
3. `RPOS.effect_unknown_is_not_completed` — 未解決の外部作用不確実性は完了ではない。
4. `RPOS.ready_to_resume_is_not_authorized` — repair readinessは実行権限ではない。
5. `RPOS.receipt_is_not_effect_verification` — transport/API receiptは外部作用検証ではない。
6. `RPOS.model_proposal_is_not_authority` — model proposalはOperational Authorityではない。

これらは宣言された限定model上の実際のLean 4 theoremです。ただし、Python runtime全体、deployment environment、法的責任、組織authority、任意の外部systemまで形式証明したという意味ではありません。

この境界は意図的です。**Formal proof、executable implementation evidence、real external-effect evidenceは別のevidence classであり、互いを代用しません。**

## 独立したResponsibility Pathway lineage

RPOSは次のResponsibility Pathway lineageの中で独立開発されています。

```text
Responsibility Pathway Model / Paper
  -> Responsibility Pathway Design
  -> Responsibility Pathway Engineering
  -> Responsibility Pathway Runtime
  -> RPOS — Responsibility Pathway Operating System
  -> formal + executable + operational evidence
  -> upstream revision
```

このlineageの中心は、judgment、authorization、execution、uncertainty、repair、return、resumption、residual ownershipを通じて責任経路を切断しないことです。RPOSはそのoperating layerです。

**RPOS owns operation, not intelligence.**

Modelは交換可能なproposal sourceであり、proposalを出しただけではauthorityになりません。

## Public Alpha

Version: **0.1.0a2 — Early Public Alpha / Executable Preview**

`responsibility-pathway-os==0.1.0a2` は **2026-08-29** にPyPI Trusted Publishing経由で公開済みで、現在のPublic Alpha releaseです。Python 3.11+ が必要です。

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

現在のrepository sourceから評価する場合:

```bash
python -m pip install -e .
python examples/quick_start_end_to_end.py
```

このalphaは工学評価と限定pilotを目的としており、無人production運用を前提としていません。

## なぜRPOSが必要か

Agentや自動化システムでは、APIやtoolがsuccess receiptを返しても、現実の作用が未発生・部分的・重複・曖昧・検証不能である場合があります。また、障害後のretryやrepairで、誰が再実行を許可したかというHuman Gate境界を失うことがあります。

RPOSはそれを状態として消しません。

- `AUTHORIZED` は実行開始や成功ではない。
- `DISPATCHING` は発行済みだが未解決のattemptを保持する。
- `EFFECT_UNKNOWN` は不確実性をfalse successへ変換しない。
- `REPAIR_REQUIRED` は修復責任を明示する。
- `READY_TO_RESUME` は修復準備完了であり実行許可ではない。
- explicit resumeはfresh dispatchの前にauthorityを復元する。
- `COMPLETED` はtransport receiptではなく限定verificationの後に成立する。

## Core responsibility states

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`。

## 実行可能サンプル

8つのcompactな公開scenarioがあります。

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

Human Gate承認/拒否、`EFFECT_UNKNOWN`、restart、reconciliation、repair、explicit resume authority、replay guard、adapter exception、Human Returnを確認できます。これは各限定scenarioについてのexecutable evidenceです。

## Production-grade operational demo suite

現在の `main` には `examples/production_grade_demos/` 以下に、より実運用へ近いexecutable integration scenarioもあります。これはPyPI `0.1.0a2` artifactの**公開後**に追加されたため、demo sourceそのものが公開済み `0.1.0a2` wheel/sdistへ含まれているとは主張しません。current source checkoutから実行してください。

```bash
python examples/production_grade_demos/run_demo.py
```

このsuiteは製品の `RposService` とRPOS SQLite persistence/transition logicを使用し、別processのlocalhost HTTP serviceが別SQLiteへ外部effectを書き込みます。RPOS state machineをdemo側でコピー・再実装していません。

3つのscenarioがあります。

- **仕入先支払の曖昧性** — 外部serviceが支払effectをcommitした直後にconnectionを切断し、RPOSは `EFFECT_UNKNOWN` を保持します。実際にPython processを再起動した後、独立readbackでeffectを確認し、重複dispatchなしで完了します。
- **production deploymentの拒否・修復・再承認** — 外部controllerの拒否で `REPAIR_REQUIRED` に入り、修復後も明示的なhuman resume authorityを必要とします。fresh dispatch identityを使用し、receiptだけでは完了せず、独立readback後にcompletionへ進みます。
- **特権access剥奪のHuman Gate拒否** — Human Gateがdenyした場合、外部side effect countが0のままであることを確認します。

localhost serviceは再現可能なintegration fixtureであり、実際の決済事業者、本番deployment controller、IAM providerではありません。これらのpassは宣言されたscenarioをtested environmentで確認するもので、production readinessや任意外部systemの正しさを確立しません。

## Lean 4 Formal Assurance Surface

Formal projectは**Lean 4.32.2**にpinされています。

```bash
cd formal/lean
lake build
```

主なmodule:

- `RPOSState.lean` — state transition、Human Gate、completion、不確実性、resume authority
- `RPOSReachability.lean` — bounded multi-step reachabilityとno-direct-shortcut
- `RPOSEvidenceBoundary.lean` — authorization / receipt / verification / evaluation / dependency evidenceの分離
- `RPOSPacketBoundary.lean` — Responsibility State Envelopeのno-authority-effect property
- `RPOSOperationalBoundary.lean` — model proposal、human authorization、receipt、external observation、operational responsibility
- `RPOSTransparencyBoundary.lean` — transparency/evidence distinction

Formal Assurance Viewerはexact site commitから生成され、Lean projectのmachine-check後にOperational Risk、theorem名、Python runtime test、source identity、model scope、proof ceilingを結びます。

## Responsibility State Envelope

`templates/catalog.json`にはoperation proposal、Human Gate decision、verification contract、repair plan、resume authorization、dependency evidence、external evaluation evidence、Human Returnのtemplateがあります。

すべてのEnvelopeは `authority_effect: "none"` を持ちます。**Envelopeの作成やvalidation自体はauthorize、dispatch、verify、complete、resumeを行いません。**

## Verification route

Release routeには次が含まれます。

- Python test suite全体
- 8つのcompact source example実行
- wheel/sdist buildとclean install
- repository外からのinstalled CLI/API check
- exact-HEAD public-export reconstruction
- source-bound CycloneDX SBOMとSHA-256 release evidence
- public source boundaryのlikely-secret scan
- Ubuntu/Windows × Python 3.11/3.12
- pinned Lean 4 `lake build`
- exact-head Formal Assurance manifest
- machine-checked assuranceとverified architecture visualを含むGitHub Pages validation/deployment

current-mainのproduction-grade demo suiteは、その追加後のrepository test/CI routeでも実行されます。

これらのpassは宣言されたscope内のengineering evidenceです。production readiness、法令compliance、universal safety、組織authority、任意外部systemの正しさ、implementation-wide formal correctnessを自動的に確立しません。

## Claim boundary と promotion

RPOSは次を分離します。

- **Current Evidence Boundary** — 宣言された証拠が得られれば昇格可能な主張
- **Permanent Responsibility Boundary** — software単体では生成しないauthorityや責任

Evidence-limited claimにはproduction readiness、より広いplatform support、implementation-wide formal conformance、software-supply-chain trust、公開scenarioを超えるdomain effectivenessがあります。

Permanent boundaryには、法的/規制authority、任意外部systemの正しさ、verification contractなしのreceipt→effect proof、softwareへの最終組織責任移転、必要なcontractを持たない任意systemに対するuniversal exactly-once guaranteeがあります。

詳細は `docs/ja/claim-boundary-promotion.md` を参照してください。

## 目標

長期目標は現在のalphaより大きいものです。AIを含む現実のworkflowで、責任を伴うoperational stateをより実行しやすく、検査しやすく、testしやすく、形式的に考察しやすく、修復しやすくし、責任を持つ人間・組織へ確実にreturnできるようにすることを目指します。

これは目標であり、達成済みという断定ではありません。より強いpublic claimは、実装、証拠、reviewを通じて昇格させます。

## Project surfaces

- PyPI: `responsibility-pathway-os==0.1.0a2`
- GitHub Pages product site / architecture maps
- Zenn公開記事: https://zenn.dev/dantarg/articles/rpos-public-alpha-010a2
- `site/assurance.html` — Formal Assurance Viewer
- `formal/assurance-catalog.json` — theorem/runtime-test crosswalk
- `product-status.json` — machine-readable release / claim state
- `examples/production_grade_demos/` — current-main executable integration suite
- `docs/ja/public-alpha-evaluation-guide.md` — evaluation route
- `CHANGELOG.md`
- `SECURITY.md`, `SUPPORT.md`, `CONTRIBUTING.md`

## License

MIT License.