<!--
Document Title: RPOS Commit-Time Authority Revalidation
Document Type: Security Design Note
Status: Public-alpha candidate
Header Language: English
Body Language: Japanese
-->

# RPOS Commit-Time Authority Revalidation

## 目的

RPOSでは、**trajectoryの途中でAuthorityが存在したこと**と、**今まさにdurable effectをcommitする瞬間にも、そのAuthorityがexact effectに対して有効であること**を分離する。

`CommitAuthorityEnvelope` は、そのdurability boundaryで使う追加型・opt-inのsecurity primitiveである。既存のRPOS state machineや `AuthorityEnvelope` を置き換えない。

## 束縛する値

commit authority envelopeは次へ束縛される。

- actor;
- operation id;
- action name;
- exact target digest;
- exact effect digest;
- evidence digest;
- context digest;
- issued / expires time;
- authority epoch;
- one-shot consumption state。

`validate_commit_authority()` は、現在値との不一致、期限切れ、未来発行、古いauthority epoch、または既に消費済みのone-shot authorityを検出すると `HOLD` を返す。

## authority epochの意味

approvalやcapabilityのpayload自体が同じでも、revocation、replacement、再承認、policy transitionなどで、Authorityの現在状態は変化し得る。

そのため `authority_epoch` をcommit時点でcallerが与えるcurrent epochと比較する。

RPOSはepochの永続化方法やincrement policyまでは決めない。integrating applicationは、独立してgovernされたAuthority surfaceからcurrent valueを与える必要がある。

## one-shot authority

`consumed=True` はfail closedする。

このprimitive自身はenvelopeを書き換えたり、自動的にconsumedへ変更したりしない。mutation / persistence semanticsはintegrating application側の責務である。

validation helperが暗黙にAuthority storeへ昇格しないための分離である。

## Security boundary

validation PASSが意味するのは、callerが提示したcurrent valuesとcommit authority envelopeが一致したことだけである。次は証明しない。

- Evidenceの真実性や十分性;
- target systemがeffectを正しく実行すること;
- Human Gate判断の実質的妥当性;
- callerが提示したauthority epochの真正性;
- production readinessや法的/compliance適合。

このprimitiveの目的は、durable effect直前の最後の責任境界で、stale / replayed / detached Authorityをfail closedしやすくすることである。
