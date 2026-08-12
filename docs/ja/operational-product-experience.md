<!-- RPOS-DOC-ID: RPOS-PRODUCT-EXPERIENCE-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: incubating -->
<!-- RPOS-DOC-COUNTERPART: ../en/operational-product-experience.md -->

# RPOS Operational Product Experience

## 目的

RPOSは、モデル、チャットボット、汎用Agent orchestration frameworkではなく、**Operational System**として開発する。モデルやAgentは仕事を提案できるが、提案から権限ある実行、外部効果の検証、回復、再開、完了までの責任を持つ遷移はRPOSが管理する。

したがって公開目標は、開発者が導入できるalphaより強い。ユーザーがRPOSをインストールし、安全なdefaultで起動し、なぜ処理が進んでいるのか・止まっているのかを理解し、不確実性から回復し、未解決責任を失わず後から戻れる状態を目指す。

## Product promise

RPOSは次の4段階のユーザー価値を目標とする。

1. **Wow** — receiptやモデルの発言と、検証済みの現実の効果が別物だと初回から分かる。
2. **Useful** — RPOS内部を読まなくてもboundedな仕事を完了できる。
3. **Trust** — 不確実性、重複実行リスク、回復を、偽の完了や暗黙の権限拡張なしに扱える。
4. **Dependable** — 承認、Evidence、未解決owner、Policy、回復履歴が再利用可能なOperational Memoryとして蓄積する。

## Architecture boundary

```text
User / Organization
        |
        v
RPOS Product Shell / Observatory
        |
        v
RPOS Operational Core
  - Policy / Authority
  - Human Gate
  - Responsibility State Envelope
  - Dispatch boundary
  - Evidence ledger
  - Reconciliation / Repair / Resume
  - Residual Owner / Human Return Point
        |
        +---- Model Adapter ---- LLM / Agent / Local Model
        |
        +---- Effect Adapter --- GitHub / Files / APIs / SaaS / other systems
```

RPOSが所有するのは**知能ではなく運用**である。Model Adapterは交換可能なproposal sourceであり、External Effect Adapterは交換可能なdispatch/observation境界である。どちらもRPOSのstate/evidence contractを迂回してはならない。

## Model Adapter contract v0.1

モデルやAgentは、次のような構造化intentを提案できる。

```json
{
  "intent": "send_message",
  "target": "example-target",
  "requested_capability": "message.send",
  "proposal_summary": "準備済みのstatus updateを送信する"
}
```

このproposalは助言的入力である。それだけでは次を行ってはならない。

- Authorityを付与する。
- Human Gateを満たす。
- 外部効果を証明する。
- `EFFECT_UNKNOWN`を`VERIFIED`へ変える。
- `COMPLETED`を生成する。
- retryまたはresumeを許可する。

Adapter境界は、OpenAI、Anthropic、Google、local model、独立Agent frameworkを、RPOSのnormative completion semanticsを変えずに交換できる程度に薄く保つ。

## Effect Adapter contract v0.1

Effect Adapterは、1つのopaqueな`execute()`成功主張ではなく、boundedな段階を公開する。

`prepare -> dispatch -> receipt -> observe/readback -> verify -> reconcile -> repair -> resume`

すべての外部システムが全段階を直接提供するとは限らない。欠ける能力はgapとして可視化し、モデルのconfidenceやtransport successから合成してはならない。

## Responsibility Observatory

主要UIはログだけではなく、次のOperational Questionへ答える。

- 今どのPathwayが動いているか。
- 現在のResponsibility Stateは何か。
- 誰の、またはどのAuthorityが必要か。
- Human Gate待ちか。
- どのEvidenceが不足しているか。
- External Effectはまだ不確実か。
- Residual Ownerは誰か。
- Human Return Pointはどこか。
- 次に許される行為は何か。
- なぜretry/resumeが止められているか。

read-only observabilityはAuthorityやResponsibility Stateを変更してはならない。

## First Experience target

初回のbounded demonstrationには、成功と不確実性の両方を意図的に含める。

1. 安全なlocal operationを作成または提案する。
2. 必要CapabilityとHuman Gateを表示する。
3. authorizeしてdispatchする。
4. transport receiptとeffect verificationを分離して見せる。
5. 意図的に`EFFECT_UNKNOWN`を発生させる。
6. RPOSが偽の完了やblind retryを拒否する理由を説明する。
7. inspect/reconcileする。
8. 必要ならrepairする。
9. 明示的にresumeする。
10. verified completionへ到達し、保持されたEvidenceを表示する。

初回体験の目標は単なる「commandが動いた」ではなく、「このOperational Systemがなぜ違うのか分かった」である。

## Installer / product shell requirements

製品公開surfaceは将来的に次を提供する。

- 後続Evidenceで優先度が変わらない限り、Windowsをfirst targetとしたone-click installer。
- local service/runtimeとembedded database。
- 安全なlocal-only default configuration。
- 通常の初回利用ではGit/Python不要。
- startup diagnosticsと明確なrecovery guidance。
- Operational Evidenceのbackup/export。
- crash後も未解決Pathwayを継続できること。
- update/uninstall strategy。
- local first boot後のoptional model/provider connection。

## Promotion and verification route

新しいproduct sliceは最初にRPPでincubateする。

`spec -> schema/model -> implementation -> executable tests -> applicableなLean 4 bounded proof -> focused CI -> JA/EN docs -> promotion candidate`

その後、検証済みfileだけをstandalone `responsibility-pathway-os` repositoryへ昇格し、そこでのstandalone testとpackaging/install evidenceをrelease evidenceのsource of truthとする。

RPPでの成功だけではstandalone RPOS release evidenceとしない。

## Lean 4のproduct role

Lean 4は飾りのassurance badgeではなく、小さく重要な境界をユーザーにも見える形で検証するlayerとする。RPOSは具体的なOperational Riskにつながる読みやすいtheoremを優先し、executable testと対にし、proof ceilingを明記する。

初期のproduct-relevant theorem候補:

- model proposalはOperational Authorityではない。
- model reportはverified external effectではない。
- transport receiptはverified external effectではない。
- verifiedな仕事だけがcompleteできる。
- ready-to-resumeはauthorized-to-resumeではない。
- read-only observationはResponsibility Stateを変更できない。

JA/ENの初心者向け資料では、advanced theorem provingより先に、RPOSの実例から「形式検証がなぜ役立つか」を理解できるようにする。

## Not Proven

この文書はproduction readiness、universal safety、regulatory compliance、任意モデルのcorrectness、任意外部システムに対するexactly-once execution、将来のinstaller/UI implementationのcorrectnessを主張しない。段階的に実装・検証するproduct boundaryとresponsibility boundaryを定義する。
