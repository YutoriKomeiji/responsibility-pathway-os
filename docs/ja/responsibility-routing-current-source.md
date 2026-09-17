# Responsibility Routing — current source 意味論整合

## Status

Current source開発ノートです。Responsibility Routingは公開済み`0.1.0a4` lineに含まれています。この文書はResponsibility Pathway stack全体で引き続き揃えるsource-level semanticsを記録します。`0.1.0a4`は`0.1.0a3`のruntime routing behaviorを維持しつつ、release metadata / public-surface整合修正を追加したreleaseです。production / enterprise readinessは主張しません。

## Core rule

RPOSは、blocked / failed / uncertain / interruptedな状態をすべてHuman Returnとして扱ってはいけません。

Human Returnはbounded Responsibility Routeの1つです。ほかにも正当なrouteがあります。

- 明示されたdelegation内での継続
- 明示されたdelegation内でのAI resolution
- reconciliation待ちのhold
- receiver eligibility未確定時のneutral hold
- organization / institutionへのreturn
- authorized processへのroute
- unresolved residueを保持したstop

## 崩してはいけない区別

RPOSはruntime、restart、repair、readback、handoffを通じて次を維持します。

- `fail closed` != Human Gate
- Evidence transfer != Authority transfer
- receiver capability != receiver eligibility
- route selection != Authority grant
- state recovery != approval / resume Authority recovery
- readback success != redispatch permission
- Human Return = bounded Responsibility Routeでありgeneric fallbackではない

Receiver eligibilityは、対象routeに必要なdelegation / Authority scope、unresolved payload、evidence access、intervention capacity、timingが十分な場合だけ成立します。

## Uncertain effects

重大なexternal effectでは、bounded readback、reconciliation、repair、またはauthorized route transitionで解消されるまでuncertaintyを明示的に保持します。

External effectがunknownなら、transport failureからeffect failureを推定してはいけません。また、実行機構が利用可能というだけでredispatchしてはいけません。

Reconciliation結果はeffect stateを解決しても、新しいexecution / resume Authorityを与えるとは限りません。

## Route envelope

Source-levelのroute表現では、少なくとも次を保持できることを目標にします。

- route identity / route kind
- current / residual owner
- 必要に応じてreceiver identity
- receiver eligibility basis
- Authority / delegation scope
- unresolved payload
- evidence / provenance refs
- allowed next actions
- prohibited assumptions
- reevaluation / closure conditions
- 必要な場合のtiming / deadline

このenvelopeはresponsibility stateであり、Authority tokenではありません。

## Falsification / non-necessity

AI systemが存在するという理由だけでRPOSが必要になるわけではありません。Host platformやapplication-specific designが、ambiguous effect、authorization、readback、repair/resume、routing、restartを通じて同等のresponsibility contractを既に維持しているなら、RPOS追加の価値がほぼ無い場合があります。

それは正当なintegration結論です。

## Assurance boundary

Executable test、cross-runtime probe、Lean 4 theoremはscopeされたEvidenceです。

それだけでは次を証明しません。

- arbitrary integrationのreal-world correctness
- legal / institutional Authority
- universal receiver eligibility
- implementation-wide formal conformance
- production / enterprise readiness

Published artifact、repository `main`、unreleased source、historical evidence、control documentは区別します。Source transitionをclosedと宣言する前にexact-head validationとpost-merge/readbackが必要です。新releaseには別のHuman Gateが必要です。
