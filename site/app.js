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

  function lang() {
    const q = new URLSearchParams(location.search).get("lang");
    return q === "ja" ? "ja" : "en";
  }

  function localizeScenario(s) {
    if (lang() !== "ja") return s;
    const ja = {
      verified:["検証済みhappy path","権限がcurrentで、dispatch後に独立readbackが外部作用を確認し、operationが完了します。"],
      "gate-denied":["Human Gate deny","明示的な人間の権限が必要ですが承認されません。外部dispatchは実行されません。"],
      "effect-unknown":["dispatch後の不確実性","外部systemへ到達した可能性はあるが検証不能。成功扱いもsilent replayもしません。"],
      restart:["曖昧なdispatch後の再起動","再起動しても未解決責任を保持し、自動redispatchを拒否します。"],
      reconcile:["reconciliationとrepair","独立証拠でeffect未適用を確認し、偽の完了ではなくrepairへ進みます。"],
      "authority-stale":["commit-time authority revalidation","以前の承認がexact target/effect/contextに対してcurrentでなくなったためfail closedします。"]
    }[s.id];
    return {...s,title:ja[0],summary:ja[1]};
  }

  function renderDemo() {
    const list = document.getElementById("scenario-list");
    if (!list) return;
    const title = document.getElementById("scenario-title");
    const summary = document.getElementById("scenario-summary");
    const badge = document.getElementById("state-badge");
    const flow = document.getElementById("state-flow");
    const events = document.getElementById("event-list");
    const intro = document.getElementById("demo-intro");
    const notice = document.getElementById("demo-notice");
    if (lang() === "ja") {
      document.documentElement.lang = "ja";
      intro.textContent = "scenarioを選ぶと、公開済みRPOS lifecycleに基づくResponsibility Pathwayを可視化します。このページはPython runtimeそのものを実行するものではなく、明示的な状態遷移simulationです。";
      notice.textContent = "Simulation only — 実行可能なruntime evidenceはrepositoryのexamplesとtest suiteを参照してください。";
    }
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
