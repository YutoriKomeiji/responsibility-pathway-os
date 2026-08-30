<!-- RPOS-DOC-ID: RPOS-CURRENT-SCOPE-001 -->
<!-- RPOS-DOC-LANG: ja -->
<!-- RPOS-DOC-VERSION: 0.1.0a2 -->
<!-- RPOS-DOC-STATUS: public-alpha-published -->
<!-- RPOS-DOC-COUNTERPART: ../en/current-scope-and-extension-surface.md -->

# 現在の対応範囲と拡張面

RPOS 0.1.0a2 は、責任経路を実行可能な形で保持するために公開済みの Early Public Alpha / Executable Preview です。現在できることを明確に示しつつ、未対応領域を閉じた「できないこと」ではなく、検証可能な拡張面として扱います。

## 現在できること

RPOS は現在、少なくとも次の機能を提供します。

- Human Gate を伴う承認境界
- durable な責任状態と event/audit history
- dispatch attempt と external effect の分離
- `EFFECT_UNKNOWN` による不確実性保持
- observation-only reconciliation
- `REPAIR_REQUIRED -> READY_TO_RESUME` と明示的 resume authorization
- Residual Owner / Human Return Point
- bounded evidence import と provenance
- authority effectを持たないResponsibility State Envelope template
- CLI と実行可能サンプル
- wheel / sdist build と clean-install verification
- CycloneDX 1.6 SBOM、artifact hash bundle、dependency audit、secret scan
- 宣言された限定model上でmachine-checkされ、Python runtime testへcross-linkされた6件のLean 4責任不変条件
- shipped RPOS service、別localhost HTTP process、別external-effect SQLite、実process restart、reconciliation、repair/resume、Human Gate denyを使うcurrent-mainのproduction-grade operational demo suite

production-grade demo suiteは、公開済み`0.1.0a2` wheel/sdistの公開後に`main`へ追加されました。したがってcurrent source treeのexecutable evidenceであり、既に公開済みのpackage artifactへ遡及的に含まれるとは主張しません。

## 現在の制約は拡張面として扱う

alpha 段階では、外部 adapter、industry profile、組織固有 rule、証拠 source、deployment topology、強い delivery/effect guarantee など、利用環境ごとに追加設計が必要な領域があります。

これらは一律に「RPOSではできない」と固定しません。要件と証拠境界を確認し、次のいずれかとして扱います。

1. core に安全に追加できる一般機能
2. compatibility adapter / migration reader として追加すべき機能
3. Industry Profile / organization profile で解決すべき機能
4. external adapter / integration として分離すべき機能
5. 専門家判断または Human Gate を残すべき領域
6. 現時点では安全に一般化できず、research / issue として保持する領域

## 改善要望と integration request

RPOS は、利用者・組織・研究者・開発者からの改善要望を将来の design input として受け取ることを前提にしています。

要望を受け付けることは、実装予定・納期・適合性・安全性を保証することではありません。採用時は、authority、evidence、compatibility、security、claim boundary を明示して評価します。

## Backward compatibility

RPOSはmaterial change時点で確認済みの最新仕様・toolchain・公的参照へ追随します。ただし、更新によって既存の対応済み alpha artifact や adopter workflow を黙って破壊しません。

互換性影響は次のいずれかで分類します。

- `backward_compatible`
- `compatibility_adapter_required`
- `breaking_change_human_gate`

破壊的変更が必要な場合は、対象 version / artifact、migration path、claim impact、Residual Owner、Human Return Point を記録します。

## Japan-first, world-reviewable

初期のadoption workでは、日本の組織・企業、経済・業界団体、国・自治体など公共部門、個人の技術者・研究者・実務家を優先します。

これは開発方向であり、それらの組織や集団による採用済みという主張ではありません。core semantics、formal evidence、security/release engineering、package quality、terminology、evidence discipline は国際的に検査できる状態を目指して維持します。public technical materialは、実用上可能な範囲で日本語/英語surfaceを同期します。

## Claim boundary と promotion

RPOS は、現在実装・検証されている機能を弱く表現する必要はありません。実装、test、formal evidence が伴う範囲では、`runtime`、`operating system`、`formal`、`machine-checked`、`assurance`、`security`、`evidence` 等の技術語を根拠とともに使用します。

公開境界は一つの免責リストに平坦化せず、次の2種類に分類します。

- **Current Evidence Boundary** — scopeを明示したreview可能なevidenceが宣言済みpromotion criteriaを満たし、対応public claimへ明示採用された場合に前進できる境界
- **Permanent Responsibility Boundary** — product maturityだけでは消えず、資格・権限を持つ人間・制度、integrator、external system、または他のresponsibility layerに残る境界

RPOSのnormativeなproduct directionは [RPOS Operational Product Experience](operational-product-experience.md) に保持します。Public Alphaは、そのOperational System方向のimplemented core sliceであり、RPOSをgeneric libraryへ再定義するものではありません。
