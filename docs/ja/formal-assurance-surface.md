<!-- RPOS-DOC-ID: RPOS-FORMAL-ASSURANCE-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1 -->
<!-- RPOS-DOC-STATUS: public-alpha-candidate -->
<!-- RPOS-DOC-COUNTERPART: ../en/formal-assurance-surface.md -->

# RPOS Formal Assurance Surface

## 目的

RPOSではLean 4を、単なるsource development時のcheckではなく、**利用者から見えるassurance / evidence plane**として扱います。ただしruntime authorityとしては扱いません。

製品surfaceでは次を接続します。

`Operational Risk -> bounded Lean theorem -> machine-check status -> executable runtime test -> proof ceiling -> exact source commit`

これにより、何がmachine-checkされていて、何がtheoremのscope外なのかを同時に確認できます。

## Source of truth

- `formal/assurance-catalog.json` — 利用者向けrisk / theorem / runtime-test crosswalkの正本
- `tools/build_formal_assurance_manifest.py` — exact source tree上でtheoremとpytest selectorを検証し、source SHA-256を記録
- `formal/lean/lean-toolchain` — Lean toolchainをpin
- `site/assurance.html` — deploy済みevidenceを表示

生成manifestのschemaは `rpos.formal-assurance.manifest.v0.1` です。

## Machine-check route

同一Git commitに対して `cd formal/lean && lake build` が成功した後だけ、manifestは `lean.machine_checked = true` を表示できます。GitHub Pagesは公開前にこのbuildを行い、その後にpublic `formal-assurance.json` を生成します。Release Candidate workflowも同じ手順を実行し、`formal-assurance.json` をsource-bound release evidenceとrelease hash bundleへ含めます。

Manifestには次を記録します。

- exact `source_commit`
- pinned Lean toolchain
- catalog SHA-256
- 各theorem sourceのSHA-256
- 各runtime test sourceのSHA-256
- model scopeとassertionごとのproof ceiling
- evidence role `public_assurance_not_runtime_authority`

## Evidence separation

Formal proof evidenceは、Executable implementation evidenceやOperational effect evidenceを代用しません。Lean theoremがmachine-check済みでも、次は行えません。

- operationのauthorize
- Human Gateの承認
- 任意external effectが実際に起きたことの確定
- runtime evidenceの真実性・十分性の確定
- 法的・組織的・Operational responsibilityの移転

## Promotion path

Public Alphaでは、advanced theorem provingを知らなくても意味を読める、高価値なOperational invariantから開始します。今後はtemporal / trace propertyやimplementation-to-model conformance evidenceを追加できます。Implementation-wide formal conformance claimは、明示的refinement / conformance relationと再現可能なconformance evidenceが揃うまではevidence-limited boundaryとして保持します。
