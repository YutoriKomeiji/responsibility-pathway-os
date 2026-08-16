<!--
Document Title: RPOS Public Alpha Evaluation Guide
Document Type: Public Product Evaluation Guide
Status: Public Alpha Candidate
Header Language: English
Body Language: Japanese
-->

# RPOS Public Alpha 評価ガイド

## 目的

RPOS 0.1.0a1 は、工学評価と限定的なpilotを目的としたEarly Public Alphaです。このガイドでは、clean installから始めて、RPOSを単なるretry wrapperやworkflow loggerと分ける責任境界を短時間で確認できる経路を示します。

目的は、普遍的安全性やproduction readinessを証明することではありません。実装済みの挙動を、第三者が確認・再現・批評・比較しやすくすることです。

## 15分程度の評価経路

Python 3.11+ のclean environmentでは、公開後に次の形で導入できます。

```bash
python -m pip install responsibility-pathway-os==0.1.0a1
rpos --db rpos.db boot
```

PyPI公開前のsource candidateを評価する場合は、次を使います。

```bash
python -m pip install .
python examples/quick_start_end_to_end.py
```

続いて、用途別のサンプルを実行します。

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

## 各サンプルが示す範囲

- `happy_path_verified.py`: 宣言した検証契約を満たした限定経路がcompletionへ到達できること。
- `human_gate_denied.py`: Human Gateでdenyされた操作がdispatchされないこと。
- `effect_unknown_restart_reconcile.py`: transport receiptの成功を外部効果の証明へ昇格せず、restart後もreconciliationまで不確実性を保持すること。
- `quick_start_end_to_end.py`: repair readinessとresume authorityを分離し、新しいattemptも別attemptとして保持すること。
- `idempotency_replay_guard.py`: 同じidempotency/effect keyを再利用しても、記録済みsemantic effectを黙って再dispatchしないこと。
- `human_return_reauthorization.py`: 修復責任を指定ownerへ返し、その後の再開を指定resume authorityへ戻し、暗黙に権限を復活させないこと。
- `adapter_exception_containment.py`: dispatch開始後のadapter exceptionを「何も起きなかった証拠」にせず、外部効果不明として閉じ込めること。
- `reconciliation_unresolved_human_return.py`: 独立observerを利用できない場合、`EFFECT_UNKNOWN`と明示的Human Return Pointを維持すること。

これらは限定された実行可能Evidenceです。すべてのadapter、外部システム、組織policy、deploymentが正しく動作することを証明するものではありません。

## Formal Evidence の確認

限定範囲のLean 4 modelはformal directoryだけで再現できます。

```bash
cd formal/lean
lake build
```

このformal surfaceではLean 4.32.2をpinしています。現在のprojectは、宣言されたstate、reachability、Evidence、Responsibility State Envelope、operational、transparencyの境界をmachine-checkします。

`lake build`の成功が示すのは、明示した仮定の下でencodeされたmodelについてだけです。Python実装、現実の外部効果、authority validity、法的妥当性、組織上の責任、production safetyを証明するものではありません。

## Field quality の確認

release-candidate verificationでは、source tests、全examples、wheel/sdistのclean install、installed CLI/API boundary、CycloneDX SBOM、source-bound public-export evidence、likely-secret scanを確認します。別のfield-portability workflowではWindows上のPython 3.11/3.12でCLI/recovery境界を実行します。

外部dispatch済みの可能性がある状態で失敗した場合は、retryより先にoperation stateとEvidenceを保持してください。応答がないことは、外部効果が発生していない証拠ではありません。

## RPOS と RPR

RPR（Responsibility Pathway Runtime）は、重大なwriteの周囲で、execution attempt、外部効果の曖昧性、readback Evidence、restart continuity、Human Returnを保持する、より狭いruntime layerです。

RPOSはより広い責任operating layerです。実行コアの周囲に、authority/Human Gate state、Evidence class、Responsibility State Envelope、recovery/resume responsibility、observability、provenance、formal/public-claim boundaryを持ちます。

限定されたwrite/reconcile runtimeを最小構成で組み込みたい場合はRPRが小さな入口になり得ます。より広いresponsibility-state operating modelを評価したい場合はRPOSを使います。どちらも、installしただけで組織上のauthorityを生成しません。

## 主な製品surface

- `README.md` / `README.ja.md`: 最初の製品概要とinstall route。
- `product-status.json`: release stage、verified surface、non-claim、release gateの機械可読状態。
- `CHANGELOG.md`: release candidateの変更とdeferred項目。
- `SECURITY.md`: security reportとsupport boundary。
- `CONTRIBUTING.md`: contribution時のEvidence discipline。
- `SUPPORT.md`: alpha supportの期待値。
- `docs/ja/public-claim-evidence-crosswalk.md`: public claimと実装/Evidence境界の対応。
- `docs/ja/os-quality-readiness.md`: 製品品質のscopeとalphaで明示的にdeferしている項目。

## 評価の返却先として有用なもの

再現可能なfailure、counterexample、分かりにくいstate transition、危険なretryを誘発する箇所、不足しているintegration boundary、portability failure、documentation mismatch、Evidenceより強く見えるclaimなどは、すべて有用です。

negative resultもEvidenceです。RPOSは自己認定で強くするのではなく、再現・批評・field use・repairの蓄積で強くしていく方針です。
