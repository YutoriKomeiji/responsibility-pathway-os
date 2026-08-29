(() => {
  const REPO = "https://github.com/YutoriKomeiji/responsibility-pathway-os";
  const isJa = new URLSearchParams(location.search).get("lang") === "ja";

  const copy = {
    en: {
      eyebrow: "Public assurance / source-bound evidence",
      title: "See what RPOS machine-checks — and what it does not.",
      intro: "This view connects concrete operational risks to bounded Lean 4 theorems and executable Python tests. Lean evidence is an assurance layer, never runtime authority.",
      checkLabel: "Lean build", countLabel: "Assurance assertions", toolchainLabel: "Toolchain", commitLabel: "Source commit",
      crosswalkEyebrow: "Evidence crosswalk", crosswalkTitle: "Risk → theorem → runtime evidence",
      crosswalkNote: "Every row is validated against the source tree when the manifest is built.",
      ceilingEyebrow: "Proof ceiling", ceilingTitle: "Machine-checked does not mean universally proven.",
      authorityTitle: "Evidence is not authority",
      authorityCopy: "A passing Lean theorem does not authorize an operation, approve a Human Gate, validate an external effect, or transfer responsibility.",
      checked: "Machine checked", notChecked: "Not machine checked", risk: "Operational risk", theorem: "Lean theorem", runtime: "Runtime evidence", scope: "Model scope", ceiling: "Proof ceiling",
      loadError: "Formal assurance evidence could not be loaded. Use the repository evidence until the site deployment is repaired.",
      source: "source", test: "test"
    },
    ja: {
      eyebrow: "Public assurance / source-bound evidence",
      title: "RPOSが何を機械検証し、何を証明していないかを見る。",
      intro: "具体的なOperational Riskを、限定されたLean 4 theoremと実行可能なPython testへ接続します。Lean evidenceはassurance layerであり、runtime authorityではありません。",
      checkLabel: "Lean build", countLabel: "Assurance assertion", toolchainLabel: "Toolchain", commitLabel: "Source commit",
      crosswalkEyebrow: "Evidence crosswalk", crosswalkTitle: "Risk → theorem → runtime evidence",
      crosswalkNote: "各行はmanifest生成時にsource tree上のtheorem/test参照まで検証されます。",
      ceilingEyebrow: "Proof ceiling", ceilingTitle: "Machine-checkedは万能な証明を意味しない。",
      authorityTitle: "EvidenceはAuthorityではない",
      authorityCopy: "Lean theoremが通っていても、operationのauthorize、Human Gateの承認、external effectの検証、責任移転は行いません。",
      checked: "Machine checked", notChecked: "未machine-check", risk: "Operational Risk", theorem: "Lean theorem", runtime: "Runtime evidence", scope: "Model scope", ceiling: "Proof ceiling",
      loadError: "Formal Assurance evidenceを読み込めませんでした。site deployment修復まではrepository側evidenceを参照してください。",
      source: "source", test: "test"
    }
  }[isJa ? "ja" : "en"];

  function set(id, value) { const el = document.getElementById(id); if (el) el.textContent = value; }
  function localized(value) { return value?.[isJa ? "ja" : "en"] || value?.en || ""; }
  function shortSha(sha) { return typeof sha === "string" && sha.length >= 12 ? sha.slice(0, 12) : "—"; }
  function sourceUrl(commit, path) { return `${REPO}/blob/${encodeURIComponent(commit)}/${path.split("/").map(encodeURIComponent).join("/")}`; }

  if (isJa) {
    document.documentElement.lang = "ja";
    const languageLink = document.getElementById("language-link");
    languageLink.href = "assurance.html";
    languageLink.lang = "en";
    languageLink.textContent = "English";
  }
  set("assurance-eyebrow", copy.eyebrow); set("assurance-title", copy.title); set("assurance-intro", copy.intro);
  set("summary-check-label", copy.checkLabel); set("summary-count-label", copy.countLabel); set("summary-toolchain-label", copy.toolchainLabel); set("summary-commit-label", copy.commitLabel);
  set("crosswalk-eyebrow", copy.crosswalkEyebrow); set("crosswalk-title", copy.crosswalkTitle); set("crosswalk-note", copy.crosswalkNote);
  set("ceiling-eyebrow", copy.ceilingEyebrow); set("ceiling-title", copy.ceilingTitle); set("authority-title", copy.authorityTitle); set("authority-copy", copy.authorityCopy);

  function labeled(label, content) {
    const wrap = document.createElement("div"); wrap.className = "assurance-field";
    const term = document.createElement("span"); term.className = "assurance-label"; term.textContent = label;
    const body = document.createElement("div"); body.append(content);
    wrap.append(term, body); return wrap;
  }

  function renderAssertion(item, commit) {
    const article = document.createElement("article"); article.className = "assurance-card";
    const header = document.createElement("div"); header.className = "assurance-card-head";
    const titleBox = document.createElement("div");
    const id = document.createElement("span"); id.className = "assurance-id"; id.textContent = item.id;
    const title = document.createElement("h3"); title.textContent = localized(item.title);
    titleBox.append(id, title);
    const badge = document.createElement("span"); badge.className = `assurance-status ${item.lean.machine_checked ? "ok" : "warn"}`; badge.textContent = item.lean.machine_checked ? copy.checked : copy.notChecked;
    header.append(titleBox, badge); article.append(header);

    const risk = document.createElement("p"); risk.textContent = localized(item.risk); article.append(labeled(copy.risk, risk));

    const theorem = document.createElement("a"); theorem.href = sourceUrl(commit, item.lean.module); theorem.textContent = item.lean.theorem; theorem.rel = "noopener";
    const theoremMeta = document.createElement("small"); theoremMeta.textContent = ` · sha256 ${item.lean.source_sha256.slice(0, 12)}…`;
    const theoremWrap = document.createElement("span"); theoremWrap.append(theorem, theoremMeta); article.append(labeled(copy.theorem, theoremWrap));

    const tests = document.createElement("ul"); tests.className = "assurance-tests";
    item.runtime_tests.forEach(entry => {
      const li = document.createElement("li"); const [path] = entry.selector.split("::", 1);
      const link = document.createElement("a"); link.href = sourceUrl(commit, path); link.textContent = entry.selector; link.rel = "noopener";
      const hash = document.createElement("small"); hash.textContent = ` · sha256 ${entry.source_sha256.slice(0, 12)}…`;
      li.append(link, hash); tests.append(li);
    });
    article.append(labeled(copy.runtime, tests));
    const scope = document.createElement("p"); scope.textContent = localized(item.model_scope); article.append(labeled(copy.scope, scope));
    const ceiling = document.createElement("p"); ceiling.textContent = localized(item.proof_ceiling); article.append(labeled(copy.ceiling, ceiling));
    return article;
  }

  fetch("formal-assurance.json", {cache: "no-store"})
    .then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); })
    .then(manifest => {
      if (manifest.schema_version !== "rpos.formal-assurance.manifest.v0.1") throw new Error("unsupported assurance manifest");
      set("summary-check", manifest.lean.machine_checked ? copy.checked : copy.notChecked);
      set("summary-count", String(manifest.assertion_count)); set("summary-toolchain", manifest.lean.toolchain);
      const commit = document.getElementById("summary-commit"); commit.textContent = shortSha(manifest.source_commit); commit.href = `${REPO}/commit/${encodeURIComponent(manifest.source_commit)}`;
      set("proof-ceiling", localized(manifest.proof_ceiling));
      const list = document.getElementById("assurance-list");
      manifest.assertions.forEach(item => list.append(renderAssertion(item, manifest.source_commit)));
    })
    .catch(error => {
      console.error(error);
      set("summary-check", "Unavailable");
      const box = document.getElementById("assurance-error"); box.hidden = false; box.textContent = copy.loadError;
    });
})();
