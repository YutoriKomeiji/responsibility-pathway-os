<!--
Document Title: RPOS Commit-Time Authority Revalidation
Document Type: Security Design Note
Status: Public-alpha candidate
Header Language: English
Body Language: Japanese
-->

# RPOS Commit-Time Authority Revalidation

## 目的

RPOSでは、**途中で一度承認されたこと**と、**いま実際に外部へ確定的な変更を反映する瞬間にも、その承認がこの対象・この作用に対して有効であること**を分けて確認します。

`CommitAuthorityEnvelope` は、その最後の確認に使う追加型・opt-inのsecurity primitiveです。既存のRPOS state machineや `AuthorityEnvelope` を置き換えるものではありません。

考え方は単純です。途中まで順調でも、対象や状況、権限の状態が変わっていたら、そのまま進めず一度確認する。条件が変わっていなければ、その確認結果を次の判断材料として使えます。

## 確認する値

commit authority envelopeは次の値に結び付きます。

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

`validate_commit_authority()` は、現在値との不一致、期限切れ、未来発行、古いauthority epoch、または既に消費済みのone-shot authorityを検出すると `HOLD` を返します。

`HOLD` は「処理全体が失敗した」という意味ではありません。**いまの条件ではそのまま確定処理へ進めないので、必要な確認や再承認へ戻る**ための状態です。

## authority epochの意味

approvalやcapabilityのpayload自体が同じでも、revocation、replacement、再承認、policy transitionなどによって、Authorityの現在状態は変わることがあります。

そのため `authority_epoch` を、commit時点でcallerが提示するcurrent epochと比較します。

RPOSはepochの永続化方法やincrement policyまでは決めません。integrating application側で、独立してgovernされたAuthority surfaceからcurrent valueを渡してください。

## one-shot authority

`consumed=True` の場合は、そのまま再利用せず `HOLD` として扱います。

このprimitive自身はenvelopeを書き換えたり、自動的にconsumedへ変更したりしません。mutation / persistence semanticsはintegrating application側で管理します。

これは、validation helperがいつの間にかAuthority storeの役割まで持ってしまわないための分離です。

## Security boundary

validation PASSが意味するのは、callerが提示したcurrent valuesとcommit authority envelopeが一致したことだけです。次の内容まで保証するものではありません。

- Evidenceそのものの真実性や十分性;
- target systemがeffectを正しく実行すること;
- Human Gate判断の実質的妥当性;
- callerが提示したauthority epochの真正性;
- production readinessや法的/compliance適合。

つまり、ここで確認しているのは**「今この条件で進めてよいというAuthorityが、対象・作用・文脈とずれていないか」**という一点です。

このprimitiveの目的は、durable effect直前にstale / replayed / detached Authorityを見つけたとき、無理に進めず、必要な確認へ戻りやすくすることです。責任境界そのものは厳密に保ちながら、人が見たときには「なぜ今止まっていて、次に何を確認すればよいか」が分かる形を目指します。
