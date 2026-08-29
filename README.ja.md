<!-- RPOS-DOC-ID: RPOS-PUBLIC-README-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1.0a2 -->
<!-- RPOS-DOC-STATUS: public-alpha-release-candidate -->
<!-- RPOS-DOC-COUNTERPART: README.md -->

# RPOS — Responsibility Pathway Operating System

**Pythonで実行可能な責任経路と、Lean 4でmachine-checkされた重要な責任不変条件を統合するResponsibility Pathway OSです。**

RPOSは、影響を伴うAI・自動化ワークフローのために独立開発されているオープンソースのResponsibility Pathway OSです。Python/SQLiteによる実行runtimeと、Human Gate、Operational Authority、dispatch、外部作用検証、不確実性、修復、再開、完了に関する選択された不変条件をLean 4で機械検証するFormal Assurance Surfaceを組み合わせます。

RPOSはmodel wrapperでも、policy documentでも、logging layerでもありません。責任を伴う状態を次の経路として実行可能に保持します。

`提案 -> Human Gate -> 承認 -> dispatch -> 外部作用検証 -> 不確実性 -> 修復 -> 明示的再開 -> 完了`

基本原則は、**承認は実行ではなく、実行receiptは外部作用の証明ではなく、失敗や不確実性によって責任を消してはいけない**、です。

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

`responsibility-pathway-os==0.1.0a2` は現在のrelease candidateです。前版 `0.1.0a1` はPyPIで公開済みです。`0.1.0a2` はexact source commitが宣言済みrelease routeを通過した後にのみ公開します。

Python 3.11+ が必要です。

```bash
python -m pip install responsibility-pathway-os==0.1.0a2
rpos --db rpos.db boot
```

上のinstall commandは `0.1.0a2` のPyPI公開後に有効になります。それまではsource checkoutで評価できます。

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

8つの公開scenarioがあります。

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
- 8つのsource example実行
- wheel/sdist buildとclean install
- repository外からのinstalled CLI/API check
- exact-HEAD public-export reconstruction
- source-bound CycloneDX SBOMとSHA-256 release evidence
- public source boundaryのlikely-secret scan
- Ubuntu/Windows × Python 3.11/3.12
- pinned Lean 4 `lake build`
- exact-head Formal Assurance manifest
- machine-checked assuranceとverified architecture visualを含むGitHub Pages validation/deployment

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

- GitHub Pages product site / architecture maps
- `site/assurance.html` — Formal Assurance Viewer
- `formal/assurance-catalog.json` — theorem/runtime-test crosswalk
- `product-status.json` — machine-readable release / claim state
- `docs/ja/public-alpha-evaluation-guide.md` — evaluation route
- `CHANGELOG.md`
- `SECURITY.md`, `SUPPORT.md`, `CONTRIBUTING.md`

## License

MIT License.
