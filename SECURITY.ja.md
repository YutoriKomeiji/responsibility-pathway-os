# セキュリティポリシー

## 対応バージョン

最初のpublic alpha候補は `0.1.0a1` です。セキュリティ修正は後続alphaとして提供する場合があります。pre-1.0のため対応範囲は変わる可能性がありますが、security relevantな互換性変更やmigration requirementがある場合はrelease noteで明示します。

## 脆弱性の報告

exploit detail、credential、private evidence、機密性のある再現情報をpublic Issueへ投稿しないでください。

repository公開後の優先経路:

1. このrepositoryでGitHubのprivate vulnerability reporting / Security Advisoryが有効な場合は、それを利用してください。
2. 影響version/commit、影響するresponsibility surface、前提条件、最小再現、観測されたimpact、およびAuthority、Evidence、Human Gate、external-effect verification、repair/resume、persistence、supply-chain integrityへの影響可能性を含めてください。
3. private vulnerability reportingが一時的に利用できない場合、repository ownerへprivate reporting channelの設定を依頼する最小限・非機密のIssueだけを作成してください。そのIssueへexploit detailを書かないでください。

public transition前は、repository ownerとの既存のprivate communication pathを利用します。

## 優先度の高いsecurity class

RPOSでは一般的なsoftware vulnerabilityに加えて、次を高優先度で扱います。

- Authority bypass、laundering、stale reuse、cross-operation replay;
- Human Gate bypassまたは消失;
- Evidence substitution、provenance spoofing、responsibility-history equivocation;
- Residual Owner / Human Return Pointの消失または無権限置換;
- 未確認のexternal effectがverificationなしでcompletionへ変換されること;
- unsafe redispatch、reconciliation abuse、repair/resume時のAuthority復元誤り;
- secret/credential exposure;
- dependency、build、release、SBOM、artifact hash、provenanceの侵害;
- untrusted plugin/MCP/integration inputによるAuthorityまたはexecution boundary違反。

## Security claim boundary

green test suite、dependency audit、secret scan、SBOM、hash bundle、bounded Lean proofは、確認したsurfaceに対するEvidenceです。それだけでRPOSがvulnerability-free、production-ready、certified、特定制度へcompliant、またはPython/runtime全体がformal verification済みであることを意味しません。

security limitationは、重大な未解決riskを隠さず、可能な限りcurrent scopeとremediation/extension pathとして記述します。
