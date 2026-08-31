(() => {
  // Site validation anchor: commit-time authority revalidation
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
      title: "外部処理を確認し、完了へ",
      summary: "必要な承認が確認され、処理後の外部状態も独立して確認できたケースです。RPOSは、確認可能な証拠がそろった時点で完了として扱います。",
      events: ["提案を記録", "承認と前提条件を確認", "実行記録を保存", "外部状態を独立して確認", "責任経路を完了"]
    },
    "gate-denied": {
      title: "人の判断により実行を見送る",
      summary: "この操作には人の判断が必要です。今回は実行を見送る判断となったため、外部処理は行わず、その判断を責任経路に記録します。",
      events: ["提案を記録", "人の判断が必要な操作として判定", "今回は実行を見送る判断", "外部処理は未実行"]
    },
    "effect-unknown": {
      title: "外部処理の結果を確認できない場合",
      summary: "要求が外部systemへ到達した可能性はあるものの、結果を確定できないケースです。RPOSは成功・失敗を推測で確定せず、確認に必要な責任経路を保持します。",
      events: ["実行に必要な承認を確認", "実行記録を保存", "外部結果は未確定", "自動的な完了判定を行わない", "確認担当・手順へ引き継ぐ"]
    },
    restart: {
      title: "再起動後も未解決状態を引き継ぐ",
      summary: "実行途中で再起動した場合も、直前の状態を保持します。未解決の内容を確認し、同一処理の自動再実行を避けながら再開判断へつなげます。",
      events: ["前回の実行記録を検出", "未解決の責任経路を確認", "同一処理を自動再実行しない", "確認先を維持"]
    },
    reconcile: {
      title: "状態を確認し、修復後に再開",
      summary: "外部状態の確認により、意図した処理が反映されていないと判明したケースです。必要な修復を行い、再開前にあらためて承認を確認します。",
      events: ["外部状態を確認", "意図した処理が未反映であることを確認", "修復担当と内容を記録", "再開前に承認を再確認"]
    },
    "authority-stale": {
      title: "条件変更時に承認を再確認",
      summary: "以前の承認が存在していても、対象・影響・前提条件が変わった場合はそのまま使用しません。重要な操作の直前で条件を再確認し、必要に応じて人の判断へ戻します。",
      events: ["以前の承認記録を確認", "対象・影響・前提条件の変化を検出", "現在条件への適合を再確認", "確認完了まで実行を保留"]
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
    document.title = "RPOS 責任状態デモ";
    setText("brand-subtitle", "責任状態デモ");
    setText("nav-product", "RPOSについて");
    setText("demo-eyebrow", "RPOS STATE PATH DEMO");
    setText("demo-heading", "外部処理の結果が不明な場合、責任経路をどう維持するか");
    setText("demo-intro", "代表的なケースを選択すると、RPOSが承認・実行・確認・修復・人への引き継ぎをどのような状態遷移として扱うか確認できます。ブラウザ上では状態の流れを確認し、実装はPythonサンプルとテストから検証できます。");
    setText("demo-notice", "このページはRPOSの責任状態を確認するためのシミュレーションです。Python runtimeそのものは実行しません。");
    setText("scenario-heading", "確認するケース");
    setText("scenario-label", "選択中のケース");
    setText("final-state-label", "最終状態");
    setText("responsibility-log-label", "状態遷移と判断");
    setText("boundary-eyebrow", "RESPONSIBILITY BOUNDARY");
    setText("boundary-heading", "責任境界は明確に。判断根拠は確認可能に。");
    setText("boundary-copy", "RPOSは、不明な状態を推測で完了させず、必要な地点で処理を止め、確認・修復・Human Returnへ接続します。責任境界を明確に保ちながら、次に必要な確認と判断が分かる運用状態を提供します。");
    setText("runtime-evidence-heading", "実装と検証結果を確認する");
    setText("runtime-example-link", "Pythonサンプル");
    setText("runtime-test-link", "テスト");
    setText("runtime-lean-link", "Lean 4形式検証");
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