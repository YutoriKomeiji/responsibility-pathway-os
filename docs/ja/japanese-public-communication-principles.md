<!--
Document Title: RPOS Japanese Public Communication Principles
Document Type: Documentation / Localization Policy
Status: Draft for public-surface review
Header Language: English
Body Language: Japanese
-->

# RPOS 日本語Public Communication Principles

## 目的

RPOSの日本語文書は、英語文書の逐語訳ではありません。

事実、仕様、state、evidence ceiling、Authority boundary、stop condition、claim boundaryは英語版と同じ意味を保ちます。一方、人に向けた説明は、日本語として自然で、相手を責めず、状況を共有し、次に何をすればよいかが分かる書き方を優先します。

RPOSの日本語UXは、次の一文で表せます。

> **責任境界はきっちり。人への説明はやわらかく。**

## 基本原則

### 1. 「禁止」より「なぜ今は進めないか」を伝える

Machine contractとして `DENIED`、`HOLD`、`EFFECT_UNKNOWN` などのstateが必要な場合、state名はそのまま保持します。

ただし人向け説明では、必要に応じて次のように言い換えます。

- 「拒否する」→「今回は見送る」「ここでいったん止める」
- 「fail closed」→「条件を確認できるまで先へ進めない」
- 「再実行を禁止する」→「確認せずに自動再実行しない」
- 「権限がない」→「この操作には、もう一度確認が必要」

技術的意味を弱めるためではなく、**止まった理由とHuman Return Pointを人が理解しやすくするため**の表現です。

### 2. 相手を疑う言い方より、確認の手順を示す

日本語では、相手やsystemを断定的に責めるよりも、観測できている事実と次の確認を分けて説明します。

例:

- 「外部systemは信用できない」ではなく「receiptだけでは外部作用まで確認できないため、readbackで確認します」
- 「承認が無効」ではなく「対象や条件が変わっているため、現在の条件でも承認が有効か確認します」

### 3. 最初に安心して触れる入口を作る

初見の利用者に、最初から境界条件・禁止事項・proof ceilingを大量に提示しません。

原則として、

1. 何ができるか
2. どんな場面で役に立つか
3. まず何を試せるか
4. どこから先は確認が必要か
5. 詳細な責任境界・証拠範囲

の順で説明します。

### 4. 「止まる」は失敗ではなく、責任を保つ動作として説明する

RPOSでは、`HUMAN_GATE`、`HOLD`、`EFFECT_UNKNOWN`、`REPAIR_REQUIRED`、`HUMAN_RETURN` は単なるエラー表示ではありません。

日本語では、

- いったん確認する
- 状況が分かるまで保留する
- 必要なら人に戻す
- 条件が整ったら再開する

という流れとして説明します。

### 5. 英語の強いsecurity語を、そのまま人格的な強さへ変換しない

`deny`, `reject`, `refuse`, `fail closed`, `prohibited`, `must not` などは、security / contract semanticsとして必要な場合があります。

日本語では、その語の**機能**を訳します。相手に向けた命令・非難・威圧としては訳しません。

### 6. 仕様語と説明語を分ける

Machine-readable state、API名、theorem名、schema field、正式なcontract termは変更しません。

その周囲の説明文だけを、日本語の読者に自然な形へlocalizeします。

例:

`EFFECT_UNKNOWN` — 「外部で何が起きたか、まだ確認できていない状態」

`READY_TO_RESUME` — 「修復や準備は整ったが、再開の確認はまだ必要な状態」

`HUMAN_GATE` — 「ここから先は人の判断を確認してから進む状態」

### 7. 境界をぼかす丁寧語にはしない

やわらかい表現は、曖昧な表現とは違います。

- receiptはexternal-effect verificationではない
- repair readinessはresume authorityではない
- model proposalはOperational Authorityではない
- formal proofはdeployment全体の正しさを自動的に証明しない

といった境界は、日本語でも明確に残します。

## 日本語public surfaceのreview checklist

公開前に少なくとも次を確認します。

- 英語の強い語を直訳しただけの文になっていないか
- 読者が責められているように感じる表現がないか
- 「何ができないか」だけでなく「次に何を確認すればよいか」が書かれているか
- 最初の入口が歓迎的か
- state / contract / claim boundaryの意味を弱めていないか
- 日本語だけ読んでも、RPOSが何を助ける製品なのか分かるか
- 詳細なsecurity / evidence説明を、必要以上に最初から前面へ出していないか
- 英語版との差が、意味の差ではなく説明文化の差に留まっているか

## 適用範囲

この原則は、少なくとも次の日本語surfaceへ適用します。

- `README.ja.md`
- `site/ja.html`
- `site/demo.html?lang=ja` および日本語表示を生成するscript
- `docs/ja/**`
- `SECURITY.ja.md`
- `SUPPORT.ja.md`
- `CONTRIBUTING.ja.md`
- `formal/**/README.ja.md`
- 今後追加する日本語の公開説明文書

英語版は英語圏のtechnical communicationとして独立して設計してよく、日本語版と語調まで一致させる必要はありません。
