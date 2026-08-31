(() => {
  const scenarios = [
    {
      id: "verified",
      title: "Verified happy path",
      summary: "Authority is current, dispatch succeeds, independent verification confirms the effect, and the operation completes.",
      state: "COMPLETED",
      tone: "ok",
      flow: ["PROPOSED", "AUTHORIZED", "DISPATCHING", "VERIFIED", "COMPLETED"],
      events: ["Proposal recorded", "Authority and evidence accepted", "Dispatch attempt persisted", "External effect verified by readback", "Responsibility pathway completed"]
    },
    {
      id: "gate-denied",
      title: "Human Gate denied",
      summary: "The operation requires explicit human authority and the human gate does not approve execution. No external dispatch occurs.",
      state: "HUMAN_GATE",
      tone: "stop",
      flow: ["PROPOSED", "HUMAN_GATE"],
      events: ["Proposal recorded", "Human Gate required", "Approval not granted", "Dispatch remains prohibited"]
    },
    {
      id: "effect-unknown",
      title: "Post-dispatch ambiguity",
      summary: "The call may have reached the external system, but reliable verification is unavailable. RPOS does not declare success and does not silently replay.",
      state: "EFFECT_UNKNOWN",
      tone: "warn",
      flow: ["PROPOSED", "AUTHORIZED", "DISPATCHING", "EFFECT_UNKNOWN", "HUMAN_RETURN"],
      events: ["Authority accepted", "Dispatch attempt persisted", "External outcome becomes ambiguous", "Automatic completion blocked", "Responsibility returned for reconciliation"]
    },
    {
      id: "restart",
      title: "Restart after ambiguous dispatch",
      summary: "A restart finds the operation stranded around dispatch. Recovery preserves the unresolved responsibility and refuses automatic redispatch.",
      state: "EFFECT_UNKNOWN",
      tone: "warn",
      flow: ["DISPATCHING", "RESTART", "EFFECT_UNKNOWN", "HUMAN_RETURN"],
      events: ["Persisted dispatch attempt discovered", "Restart recovery evaluates incomplete pathway", "No silent redispatch", "Human return point retained"]
    },
    {
      id: "reconcile",
      title: "Reconciliation and repair",
      summary: "Independent evidence shows that the intended effect was not applied. RPOS routes the operation to repair instead of pretending the earlier attempt completed.",
      state: "REPAIR_REQUIRED",
      tone: "warn",
      flow: ["EFFECT_UNKNOWN", "RECONCILE", "REPAIR_REQUIRED", "READY_TO_RESUME"],
      events: ["Reconciliation evidence collected", "Effect verified as not applied", "Repair ownership recorded", "Resume requires an explicit authorized path"]
    },
    {
      id: "authority-stale",
      title: "Commit-time authority revalidation",
      summary: "Earlier approval is no longer current for the exact target/effect/context. Commit-time revalidation fails closed before a consequential commit.",
      state: "HOLD",
      tone: "stop",
      flow: ["AUTHORIZED", "CONTEXT_CHANGED", "REVALIDATE", "HOLD"],
      events: ["Earlier authority envelope exists", "Target/effect/context or authority epoch changes", "Commit-time revalidation detects staleness", "Commit blocked pending renewed authority"]
    }
  ];

  const jaScenarios = {
    verified: {
      title: "確認できたので、そのまま完了へ",
      summary: "必要な承認がそろい、処理後に外部の状態も確認できたケースです。RPOSは、ここまで確認できてから完了として扱います。",
      events: ["提案を記録しました", "必要な承認と前提を確認しました", "実行の記録を残しました", "外部の状態を読み直して確認しました", "責任経路を完了しました"]
    },
    "gate-denied": {
      title: "ここは人に戻して確認",
      summary: "この操作には人の判断が必要です。承認されていない間は外部へ実行せず、判断を待つ状態にします。",
      events: ["提案を記録しました", "人の確認が必要な操作です", "まだ承認されていません", "外部への実行は行いません"]
    },
    "effect-unknown": {
      title: "結果が分からないとき",
      summary: "要求は届いたかもしれないけれど、外部で何が起きたか確認できないケースです。RPOSは急いで成功・失敗を決めず、確認できるところまで人と一緒に経路を残します。",
      events: ["実行に必要な承認を確認しました", "実行の記録を残しました", "外部結果をまだ確定できません", "自動で完了扱いにはしません", "確認できる人・手順へ戻します"]
    },
    restart: {
      title: "途中で再起動しても、続きから確認",
      summary: "実行途中で再起動した場合も、前の状態をなかったことにしません。まず未解決だった内容を確認し、同じ処理を勝手に繰り返さないようにします。",
      events: ["前回の実行記録を見つけました", "未解決だった経路を確認します", "自動で同じ処理を繰り返しません", "確認先をそのまま残します"]
    },
    reconcile: {
      title: "確認して、必要なら直してから再開",
      summary: "外部の状態を確認した結果、意図した処理が反映されていなかったケースです。まず修整し、再開してよいかをあらためて確認します。",
      events: ["外部の状態を確認しました", "意図した処理が反映されていないことを確認しました", "修整の担当と内容を記録しました", "再開前にあらためて承認を確認します"]
    },
    "authority-stale": {
      title: "条件が変わったら、もう一度確認",
      summary: "以前の承認があっても、対象や状況が変わった場合はそのまま使いません。大きな操作の直前で条件を見直し、必要なら人に戻します。",
      events: ["以前の承認記録があります", "対象・影響・状況の変化を確認しました", "現在の条件に合うか見直します", "必要な確認が終わるまで実行を待ちます"]
    }
  };

  function lang() {
    const q = new URLSearchParams(location.search).get("lang");
    return q === "ja" ? "ja" : "en";
  }

  function localizeScenario(s) {
    if (lang() !== "ja") return s;
    const ja = jaScenarios[s.id];
    return {...s, title: ja.title, summary: ja.summary, events: ja.events};
  }

  function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  function applyJapanesePageCopy() {
    document.documentElement.lang = "ja";
    document.title = "RPOS 状態の流れを試してみる";
    setText("brand-subtitle", "状態の流れを試してみる");
    setText("nav-product", "RPOSについて");
    setText("demo-eyebrow", "まずは気軽に触ってみる");
    setText("demo-heading", "もし途中で結果が分からなくなったら、どう扱う？");
    setText("demo-intro", "気になるケースを選んでみてください。RPOSが、承認・実行・確認・修整・人への引き継ぎをどのようにつなぐかを、状態の流れとして見られます。難しい設定は不要です。");
    setText("demo-notice", "ここは仕組みをつかむための体験ページです。実際に動くPython版は、GitHubのサンプルやテストから確認できます。");
    setText("scenario-heading", "試してみるケース");
    setText("scenario-label", "いま選んでいるケース");
    setText("final-state-label", "最後の状態");
    setText("responsibility-log-label", "このケースで起きること");
    setText("boundary-eyebrow", "大切にしている考え方");
    setText("boundary-heading", "止まることも、きちんとした動作のひとつです。");
    setText("boundary-copy", "RPOSは、分からないまま先へ進めるより、必要なところで止まり、確認し、直し、必要なら人へ戻せることを大切にしています。責任の境界はきちんと保ちながら、試す人には分かりやすく開かれた道具であることを目指しています。");
    setText("runtime-evidence-heading", "実際に動くものも確認できます");
    setText("runtime-example-link", "Pythonサンプルを見る");
    setText("runtime-test-link", "テストを見る");
    setText("runtime-lean-link", "Lean 4の検証を見る");
    setText("footer-home", "ホーム");
    setText("footer-repository", "GitHubリポジトリ");
  }

  function renderDemo() {
    const list = document.getElementById("scenario-list");
    if (!list) return;
    const title = document.getElementById("scenario-title");
    const summary = document.getElementById("scenario-summary");
    const badge = document.getElementById("state-badge");
    const flow = document.getElementById("state-flow");
    const events = document.getElementById("event-list");
    if (lang() === "ja") applyJapanesePageCopy();
    function select(id) {
      const raw = scenarios.find(x => x.id === id) || scenarios[0];
      const s = localizeScenario(raw);
      [...list.querySelectorAll("button")].forEach(b => b.setAttribute("aria-pressed", String(b.dataset.id === id)));
      title.textContent = s.title;
      summary.textContent = s.summary;
      badge.textContent = s.state;
      badge.className = `state-badge ${s.tone}`;
      flow.replaceChildren(...s.flow.flatMap((step,i) => {
        const span=document.createElement("span"); span.textContent=step;
        if(i===s.flow.length-1) return [span];
        const arrow=document.createElement("b"); arrow.textContent="→"; return [span,arrow];
      }));
      events.replaceChildren(...s.events.map(e => {const li=document.createElement("li"); li.textContent=e; return li;}));
    }
    scenarios.forEach((raw,i) => {
      const s = localizeScenario(raw);
      const b=document.createElement("button"); b.type="button"; b.dataset.id=s.id; b.setAttribute("aria-pressed", String(i===0)); b.textContent=s.title; b.addEventListener("click",()=>select(s.id)); list.appendChild(b);
    });
    select(scenarios[0].id);
  }

  renderDemo();
})();
