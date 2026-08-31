<!-- RPOS-DOC-ID: RPOS-PRODUCT-EXPERIENCE-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: normative-product-direction -->
<!-- RPOS-DOC-COUNTERPART: ../en/operational-product-experience.md -->

# RPOS Operational Product Experience

## 目的

RPOSは、モデル、チャットボット、generic library、汎用Agent orchestration frameworkではなく、**Operational System**として開発します。モデルやAgentは仕事を提案できますが、提案から権限ある実行、外部効果の確認、回復、再開、完了までを責任経路としてつなぐのがRPOSの役割です。

目指しているのは、開発者だけが扱えるalphaで終わることではありません。ユーザーがRPOSをインストールし、安全なdefaultで起動し、「なぜ今進んでいるのか」「なぜここで確認が必要なのか」「次に何をすればよいか」を理解しながら使える状態を目指します。

日本語のpublic surfaceでは、英語のsecurity/contract表現をそのまま強い命令口調へ変換しません。責任境界は厳密に保ちつつ、人に向けた説明は、確認・保留・Human Return・再開の流れが自然に分かるようにします。詳細は [日本語Public Communication Principles](japanese-public-communication-principles.md) を参照してください。

この文書はRPOSのnormativeなproduct directionです。Early Public Alphaではこの体験の一部だけを実装していても構いませんが、partial releaseだからといってRPOSをgeneric Python libraryとして扱うことはしません。Product maturityは、以下のcore invariantを保ちながらこの方向へ進めます。

## Core invariants — 変えない中核

完全なProduct Shellが存在する前から、次はRPOSをRPOSとして定義します。

- **RPOSが所有するのは知能ではなく運用です。** Model / Agentは交換可能なproposal sourceであり、authority sourceではありません。
- proposal、model statement、transport receiptだけでOperational Authorityやverified external effectが成立したとは扱いません。
- Human Gate、authority、target、effect、evidence、contextは明示的なresponsibility-bearing boundaryとして保持します。
- 不確実なexternal effectは不確実なまま保持し、false successや確認なしのretryへ進めません。
- restart、reconciliation、repair、resumeでも未解決責任を消しません。
- repair readinessだけでexecution authorityを自動復元せず、resumeの前に明示的なauthorize経路を確認します。
- 自動的に閉じられない責任にはResidual OwnerとHuman Return Pointを残します。
- read-only observationはAuthorityやResponsibility Stateを変更しません。

これらの境界を変える場合は、通常のproduct evolutionとは分けてarchitecture reviewを行います。

## 0.1.0a1で実装済みのslice

0.1.0a1 Public Alphaは、このproduct directionのOperational Coreを次の範囲で実装しています。

- durableなResponsibility Stateとevent history
- Human Gateとauthorization boundary
- dispatch attempt / external effectの分離
- `EFFECT_UNKNOWN`による不確実性保持
- crash-consistentなstate/event persistenceとrestart recovery
- observation-only reconciliation
- repair、明示的resume authorization、Human Return path
- Residual Owner / Human Return Point structure
- exact effect/target bindingを持つopt-in commit-time authority revalidation
- evidence/provenance surface、実行可能example、CLI/package surface、限定的Lean evidence
- lifecycleを説明するPublic Product Siteとbrowser state-path explorer。simulationをPython runtime executionとは区別します

このsliceが支えるのはPublic Alpha claimであり、まだ完全なOperational Product Experienceではありません。

## Post-alpha product targets

次は、Operational Systemとして使いやすさを上げていくproduct-direction targetです。

- RPOS内部を読まなくてもoperational questionへ答えられるProduct Shell / Observatory
- safe local-first service/runtime defaultとstartup diagnostics
- 後続evidenceで優先度が変わらない限りWindowsをinitial targetとしたone-click installer
- 通常の初回利用ではGit/Python知識を要求しないこと
- Operational Evidenceのbackup/export
- update / rollback / uninstall strategy
- safe local first boot後のoptional model/provider connection
- より広いsupported Effect Adapterとfield-validated deployment profile
- approval、evidence、unresolved ownership、policy、recovery historyを横断するreusable operational memory

これらをpublic capability claimへ昇格するには、実装とreview可能なevidenceが必要です。詳細は [Claim Boundary Promotion](claim-boundary-promotion.md) を参照してください。

## Product promise

RPOSは次の4段階のユーザー価値を目標とします。

1. **Wow** — receiptやモデルの発言と、検証済みの現実の効果が別物だと初回から分かる。
2. **Useful** — RPOS内部を読まなくてもboundedな仕事を完了できる。
3. **Trust** — 不確実性、重複実行リスク、回復を、偽の完了や暗黙の権限拡張なしに扱える。
4. **Dependable** — 承認、Evidence、未解決owner、Policy、回復履歴が再利用可能なOperational Memoryとして蓄積する。

日本語UXでは、ここにもう一つ「入りやすさ」を加えます。最初から境界条件を並べるのではなく、まず何ができるか、次に何を確認すればよいかを示し、そのあと必要なsecurity/evidence boundaryへ案内します。

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

RPOSが所有するのは**知能ではなく運用**です。Model Adapterは交換可能なproposal sourceであり、External Effect Adapterは交換可能なdispatch/observation境界です。どちらもRPOSのstate/evidence contractを迂回する経路としては扱いません。

## Model Adapter contract v0.1

モデルやAgentは、次のような構造化intentを提案できます。

```json
{
  "intent": "send_message",
  "target": "example-target",
  "requested_capability": "message.send",
  "proposal_summary": "準備済みのstatus updateを送信する"
}
```

このproposalは助言的入力です。proposalだけでは、次の状態へ自動的には進みません。

- Authorityの付与
- Human Gateの成立
- 外部効果の証明
- `EFFECT_UNKNOWN`から`VERIFIED`への昇格
- `COMPLETED`の成立
- retryまたはresumeの許可

Adapter境界は、OpenAI、Anthropic、Google、local model、独立Agent frameworkを、RPOSのnormative completion semanticsを変えずに交換できる程度に薄く保ちます。

## Effect Adapter contract v0.1

Effect Adapterは、1つのopaqueな`execute()`成功主張ではなく、boundedな段階を公開します。

`prepare -> dispatch -> receipt -> observe/readback -> verify -> reconcile -> repair -> resume`

すべての外部システムが全段階を直接提供するとは限りません。欠ける能力はgapとして可視化し、モデルのconfidenceやtransport successから補完したものとしては扱いません。

## Responsibility Observatory

主要UIはログだけではなく、次のOperational Questionへ答えます。

- 今どのPathwayが動いているか。
- 現在のResponsibility Stateは何か。
- 誰の、またはどのAuthorityが必要か。
- Human Gateで確認待ちか。
- どのEvidenceが不足しているか。
- External Effectはまだ不確実か。
- Residual Ownerは誰か。
- Human Return Pointはどこか。
- 次に確認できること・進められることは何か。
- なぜretry/resumeの前に確認が必要なのか。

read-only observabilityはAuthorityやResponsibility Stateを変更しません。

## First Experience target

初回のbounded demonstrationには、成功と不確実性の両方を意図的に含めます。

1. 安全なlocal operationを作成または提案する。
2. 必要CapabilityとHuman Gateを表示する。
3. authorizeしてdispatchする。
4. transport receiptとeffect verificationを分離して見せる。
5. 意図的に`EFFECT_UNKNOWN`を発生させる。
6. なぜこの時点では完了や自動retryへ進めず、確認が必要なのかを説明する。
7. inspect/reconcileする。
8. 必要ならrepairする。
9. 明示的にresumeする。
10. verified completionへ到達し、保持されたEvidenceを表示する。

初回体験の目標は単なる「commandが動いた」ではなく、**「止まったときも理由と次の行動が分かる」**ことまで含めて、「このOperational Systemがなぜ違うのか分かった」と感じられることです。

## Installer / product shell requirements

製品公開surfaceは将来的に次を提供します。

- 後続Evidenceで優先度が変わらない限り、Windowsをfirst targetとしたone-click installer。
- local service/runtimeとembedded database。
- 安全なlocal-only default configuration。
- 通常の初回利用ではGit/Python不要。
- startup diagnosticsと分かりやすいrecovery guidance。
- Operational Evidenceのbackup/export。
- crash後も未解決Pathwayを継続できること。
- update/uninstall strategy。
- local first boot後のoptional model/provider connection。

## Promotion and verification route

新しいproduct sliceは最初にRPPでincubateします。

`spec -> schema/model -> implementation -> executable tests -> applicableなLean 4 bounded proof -> focused CI -> JA/EN docs -> promotion candidate`

その後、検証済みfileだけをstandalone `responsibility-pathway-os` repositoryへ昇格し、そこでのstandalone testとpackaging/install evidenceをrelease evidenceのsource of truthとします。

RPPでの成功だけをstandalone RPOS release evidenceとしては扱いません。

## Lean 4のproduct role

Lean 4は飾りのassurance badgeではなく、小さく重要な境界をユーザーにも見える形で検証するlayerです。RPOSは具体的なOperational Riskにつながる読みやすいtheoremを優先し、executable testと対にし、proof ceilingを明記します。

初期のproduct-relevant theorem候補:

- model proposalはOperational Authorityではない。
- model reportはverified external effectではない。
- transport receiptはverified external effectではない。
- verifiedな仕事だけがcompleteできる。
- ready-to-resumeはauthorized-to-resumeではない。
- read-only observationはResponsibility Stateを変更できない。

JA/ENの初心者向け資料では、advanced theorem provingより先に、RPOSの実例から「形式検証がなぜ役立つか」を理解できるようにします。

## Claim boundary と promotion

このproduct directionに書かれた将来targetは、それだけでcurrent capabilityになるわけではありません。Public claimは、実装とscopeを明示したevidenceが支える場合に前進します。

broader deployment support、Product Shell maturity、installer quality、platform coverage、implementation-wide conformance等のevidence-limited gapは、宣言済みpromotion criteriaによって段階的に前進できます。一方、legal authority、final organizational responsibility、任意external systemのcorrectness、必要contractを持たないsystemへのuniversal exactly-once等のpermanent responsibility boundaryは、RPOSが成熟しても自動的には変わりません。

日本語では、この境界を「できません」の羅列にせず、**今どこまで確認できていて、どこから先は追加の確認が必要か**という形で説明します。ただし、境界の意味そのものは変えません。

現在のEvidence Boundary、Promotion Criteria、Evidence Owner、Permanent Responsibility Boundaryは [Claim Boundary Promotion](claim-boundary-promotion.md) を参照してください。
