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

**このまま、もう一度実行しても大丈夫でしょうか。**

最初の要求で、外部systemはすでに変わっているかもしれません。すぐ再実行すると二重決済、二重deploy、二重通知、権限変更の重複につながることがあります。反対に、すぐ「失敗」と決めると、すでに起きた現実の変更を見失うかもしれません。

RPOSは、そんな**「まだ分からない」状態を無理に成功・失敗へ決めず、必要な確認や人への引き継ぎまで責任経路をつないだまま扱う**Open SourceのPython/SQLite runtimeです。

> **分からないときは、いったん分からないまま扱う。そのうえで、確認してから次へ進む。**

この考え方を **Responsibility Pathway Operating System（責任経路OS / RPOS）** と呼んでいます。責任を一つの承認フラグやログではなく、判断から現実の作用まで続く「経路」として扱うための仕組みです。

## まず試してみる

公開済みPublic Alphaは、次のコマンドで試せます。

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

- **まず触ってみる:** [PyPI 0.1.0a2](https://pypi.org/project/responsibility-pathway-os/0.1.0a2/)
- **ブラウザで状態の流れを見る:** [Product site](https://yutorikomeiji.github.io/responsibility-pathway-os/)
- **source・test・Lean・CI・最新demoを見る:** このrepository
- **問題設定から読む:** [Zenn — RPOS 0.1.0a2公開記事](https://zenn.dev/dantarg/articles/rpos-public-alpha-010a2)

PyPI `0.1.0a2` には公開済みruntimeが入っています。3本のproduction-grade integration demoは、そのrelease後にcurrent `main`へ追加したものなので、demoを動かす場合はsource checkoutを使ってください。

## RPOSで大切にしていること

AI agent / automationでは、別々の出来事が一つの「成功」にまとめられやすくなります。RPOSは、その間を丁寧に分けて保持します。

- **人間の承認と実行権限は同じではない** — 修復準備ができても、そのまま古い許可で自動再開しません
- **実行要求と現実の作用は同じではない** — dispatchしただけでは外部systemが変わったとは判断しません
- **成功応答と外部作用の確認は同じではない** — receiptだけを現実の証明にはしません
- **分からないときは分からないまま残す** — `EFFECT_UNKNOWN` で結果不明を保持し、確認なしの自動retryやfalse completionへ進めません
- **途中で止まっても、責任の引受先を残す** — restart、reconciliation、repair、明示的再開、Human Returnを同じ責任経路へ接続します

実行可能な経路は次の形です。

`提案 -> Human Gate -> 承認 -> dispatch -> 外部作用確認 -> 不確実性 -> 修復 -> 明示的再開 -> 完了 / Human Return`

基本原則は、**承認は実行ではなく、実行receiptは外部作用の証明ではなく、失敗や不確実性によって責任を消さない**、です。

## Project identity / 帰属について

RPOSは `YutoriKomeiji/responsibility-pathway-os` において、Responsibility Pathway lineageの中で独立開発されています。

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

RPOSは、それぞれを別の状態として残します。

- `AUTHORIZED` — 実行してよい条件が整っている。まだ実行開始や成功そのものではない。
- `DISPATCHING` — 要求を出したが、外部で何が起きたかはまだ確認途中。
- `EFFECT_UNKNOWN` — 外部作用が起きた可能性はあるが、まだ確認できていない。
- `REPAIR_REQUIRED` — 続ける前に修復や確認が必要。
- `READY_TO_RESUME` — 修復準備は整ったが、再開の確認はまだ必要。
- explicit resume — fresh dispatchの前に、もう一度必要なauthorityを確認する。
- `COMPLETED` — transport receiptだけではなく、限定verificationの後に成立する。

## Core responsibility states

`PROPOSED`, `HUMAN_GATE`, `AUTHORIZED`, `DISPATCHING`, `EFFECT_UNKNOWN`, `VERIFIED`, `REPAIR_REQUIRED`, `READY_TO_RESUME`, `COMPLETED`, `DENIED`, `ABORTED`。

Machine state名は英語のまま保持します。日本語の説明では、「なぜ今その状態なのか」「次に何を確認すればよいか」が分かることを優先します。

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

Human Gateでの確認・見送り、`EFFECT_UNKNOWN`、restart、reconciliation、repair、explicit resume authority、replay guard、adapter exception、Human Returnを確認できます。これは各限定scenarioについてのexecutable evidenceです。

## Production-grade operational demo suite

現在の `main` には `examples/production_grade_demos/` 以下に、より実運用へ近いexecutable integration scenarioもあります。これはPyPI `0.1.0a2` artifactの**公開後**に追加されたため、demo sourceそのものが公開済み `0.1.0a2` wheel/sdistへ含まれているとは主張しません。current source checkoutから実行してください。

```bash
python examples/production_grade_demos/run_demo.py
```

このsuiteは製品の `RposService` とRPOS SQLite persistence/transition logicを使用し、別processのlocalhost HTTP serviceが別SQLiteへ外部effectを書き込みます。RPOS state machineをdemo側でコピー・再実装していません。

3つのscenarioがあります。

- **仕入先支払の曖昧性** — 外部serviceが支払effectをcommitした直後にconnectionを切断し、RPOSは `EFFECT_UNKNOWN` を保持します。実際にPython processを再起動した後、独立readbackでeffectを確認し、重複dispatchなしで完了します。
- **本番デプロイをいったん見送り、修復後に再確認** — 外部controllerが要求を受理しなかった場合は `REPAIR_REQUIRED` に入り、修復後も明示的なhuman resume authorityを確認します。fresh dispatch identityを使用し、receiptだけでは完了せず、独立readback後にcompletionへ進みます。
- **特権アクセスの削除を、人の判断で見送るケース** — Human Gateで実行しない判断になった場合、external side effect countが0のままであることを確認します。

localhost serviceは再現可能なintegration fixtureであり、実際の決済事業者、本番deployment controller、IAM providerではありません。これらのpassは宣言されたscenarioをtested environmentで確認するもので、production readinessや任意external systemの正しさを確立しません。

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

すべてのEnvelopeは `authority_effect: "none"` を持ちます。**Envelopeの作成やvalidationだけで、authorize、dispatch、verify、complete、resumeが成立するわけではありません。**

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

これらのpassは宣言されたscope内のengineering evidenceです。production readiness、法令compliance、universal safety、組織authority、任意external systemの正しさ、implementation-wide formal correctnessまで自動的に広げて扱うものではありません。

## Claim boundary と promotion

RPOSは次を分離します。

- **Current Evidence Boundary** — 宣言された証拠が得られれば昇格可能な主張
- **Permanent Responsibility Boundary** — software単体では生成しないauthorityや責任

Evidence-limited claimにはproduction readiness、より広いplatform support、implementation-wide formal conformance、software-supply-chain trust、公開scenarioを超えるdomain effectivenessがあります。

Permanent boundaryには、法的/規制authority、任意external systemの正しさ、verification contractなしのreceipt→effect proof、softwareへの最終組織責任移転、必要なcontractを持たない任意systemに対するuniversal exactly-once guaranteeがあります。

ここは表現をやわらかくしても意味は変えません。責任境界は明確に保ちつつ、利用者には「今どこまで確認できていて、どこから先に追加の確認が必要か」が分かるように説明します。

詳細は `docs/ja/claim-boundary-promotion.md` を参照してください。

## 目標

長期目標は現在のalphaより大きいものです。AIを含む現実のworkflowで、責任を伴うoperational stateをより実行しやすく、確認しやすく、testしやすく、形式的に考察しやすく、修復しやすくし、責任を持つ人間・組織へ確実にreturnできるようにすることを目指します。

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