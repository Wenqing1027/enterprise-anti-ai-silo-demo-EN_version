/* Qingshu AI Workbench · Business lead: dept → feature list → subpage */

const qs = new URLSearchParams(location.search);
const state = {
  departments: [],
  departmentId: qs.get("department") || "service",
  features: [],
  flows: [],
  /** null | feature_id | "__guide__" */
  selectedId: qs.get("feature") || null,
  currentFeature: null,
};

const el = {
  deptNav: document.getElementById("dept-nav"),
  deptIntro: document.getElementById("dept-intro"),
  railList: document.getElementById("feature-rail-list"),
  railSub: document.getElementById("rail-sub"),
  viewEmpty: document.getElementById("view-empty"),
  viewFeature: document.getElementById("view-feature"),
  viewGuide: document.getElementById("view-guide"),
  featureCrumb: document.getElementById("feature-crumb"),
  featureBadges: document.getElementById("feature-badges"),
  featureTitle: document.getElementById("feature-title"),
  featurePurpose: document.getElementById("feature-purpose"),
  featureRunHint: document.getElementById("feature-run-hint"),
  featureActions: document.getElementById("feature-actions"),
  guideCrumb: document.getElementById("guide-crumb"),
  runner: document.getElementById("runner"),
  text: document.getElementById("input-text"),
  customer: document.getElementById("input-customer"),
  vin: document.getElementById("input-vin"),
  dealer: document.getElementById("input-dealer"),
  channel: document.getElementById("input-channel"),
  order: document.getElementById("input-order"),
  payloadBox: document.getElementById("payload-box"),
  payload: document.getElementById("input-payload"),
  status: document.getElementById("status"),
  answer: document.getElementById("answer"),
  kv: document.getElementById("kv"),
  board: document.getElementById("board"),
  steps: document.getElementById("steps"),
  runBtn: document.getElementById("btn-run"),
  sampleBtn: document.getElementById("btn-sample"),
  closeBtn: document.getElementById("btn-close-runner"),
};

const PHASE_ORDER = [
  { id: "demo", title: "Try now", pill: "pill-ok" },
  { id: "phase2", title: "Phase 2", pill: "pill-phase2" },
  { id: "phase3", title: "Phase 3", pill: "pill-phase3" },
];

const EXTRACTION_SKILLS = new Set(["ticket_fields", "voc_entities", "voc_tagging"]);
const RAG_SKILLS = new Set(["repair_kb", "policy_kb", "hr_rules"]);
const PLAN_SKILLS = new Set(["renewal_plan"]);

/** Business relationship hints (no jargon) */
const REL_EXPLAIN = {
  parallel_alt: "Other capabilities for the same goal can be tried separately; they do not replace each other.",
  parallel_producer: "This item writes results to shared info; other departments can read separately.",
  parallel_showcase: "Planned capability, shown alongside other items in the department.",
  parallel_orthogonal: "Exists in parallel with the main dept flow; usable on its own.",
  parallel_optional: "Can coexist with adjacent capabilities; does not replace outreach evaluation.",
  sequence_upstream: "Complete this first, then use downstream capabilities that depend on shared info.",
  sequence_downstream: "Complete upstream logging first, then use this item.",
  standalone: "Standalone; one try completes it.",
};

function isExtractionFeature(f) {
  return (
    f?.agent_type === "extract" ||
    f?.agent_type === "extraction" ||
    EXTRACTION_SKILLS.has(f?.skill_id)
  );
}

function isRagFeature(f) {
  return (
    f?.agent_type === "retrieve" ||
    f?.agent_type === "rag" ||
    RAG_SKILLS.has(f?.skill_id)
  );
}

function isPlanFeature(f) {
  return (
    f?.agent_type === "plan" ||
    f?.agent_type === "planning" ||
    PLAN_SKILLS.has(f?.skill_id)
  );
}

function runEndpointFor(f) {
  if (isExtractionFeature(f)) return "/v1/extraction/runs";
  if (isRagFeature(f)) return "/v1/rag/runs";
  if (isPlanFeature(f)) return "/v1/planning/runs";
  return "/v1/react/runs";
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function syncUrl() {
  const u = new URL(location.href);
  u.searchParams.set("department", state.departmentId);
  if (state.selectedId) u.searchParams.set("feature", state.selectedId);
  else u.searchParams.delete("feature");
  history.replaceState(null, "", u);
}

function currentDept() {
  return state.departments.find((d) => d.department_id === state.departmentId);
}

function featurePhase(f) {
  if (f.phase === "demo" || f.phase === "phase2" || f.phase === "phase3") return f.phase;
  if (f.demo_ready || f.status === "demo") return "demo";
  if (f.phase_label === "Phase 3" || f.agent_type === "vision") return "phase3";
  return "phase2";
}

function phaseLabelOf(f) {
  const p = featurePhase(f);
  if (p === "demo") return "Try now";
  if (p === "phase3") return "Phase 3";
  return "Phase 2";
}

/** Business display names: strip tech suffixes and jargon */
function displayName(f) {
  if (!f) return "";
  const map = {
    "F-SVC-001-EXT": "Smart ticket fill (structured)",
    "F-SVC-002": "Smart assist reply",
    "F-SVC-004": "Repair KB Q&A",
    "F-UO-017": "Proactive outreach evaluation",
    "F-UO-001": "Renewal outbound task",
    "F-UO-009": "App smart Q&A",
    "F-POL-RAG": "Policy guidance Q&A",
    "F-VOC-002": "Customer voice cleanup",
    "F-X-WRITE": "Shared info write",
    "F-X-MD": "Customer & vehicle lookup",
  };
  if (map[f.feature_id]) return map[f.feature_id];
  return String(f.name || "")
    .replace(/\s*[·・]\s*(Extraction|RAG|ReAct|Agent).*$/i, "")
    .replace(/（complaint gate）/g, "")
    .replace(/Agent\s*/g, "")
    .trim();
}

function softenText(s) {
  return String(s || "")
    .replace(/Shared outputwrite/g, "Shared info write")
    .replace(/Shared output/g, "Shared info")
    .replace(/shared layer/g, "Shared info")
    .replace(/assetize output，\s*feature\s*/g, "Write results to shared info for other capabilities to read")
    .replace(/assetize output， Skill /g, "Write results to shared info for other capabilities to read")
    .replace(/Structure voice of customer：tag\/sentiment\/theme\//g, "Structure voice into tags, sentiment, theme, and risk")
    .replace(/agent-sideRepair KB Q&A（reference）/g, "Agent-side repair KB Q&A with references")
    .replace(/\bRAG\b/g, "Knowledge Q&A")
    .replace(/\bReAct\b/g, "")
    .replace(/\bExtraction\b/g, "")
    .replace(/\bAgent\b/g, "")
    .replace(/\bSkill\b/g, "feature")
    .replace(/\s{2,}/g, " ")
    .trim();
}

function softenSkillName(id) {
  const map = {
    renewal_plan: "Renewal outreach evaluation",
    fill_ticket: "Smart ticket fill",
    ticket_fields: "Smart ticket fill (structured)",
    voc_entities: "Customer voice cleanup",
    repair_kb: "Repair KB Q&A",
    policy_kb: "Policy guidance Q&A",
    hr_rules: "HR policy Q&A",
    shared_write: "Shared info write",
    master_data: "Customer & vehicle lookup",
  };
  return map[String(id || "").trim()] || String(id || "");
}

/** Turn tech notes into business guidance */
function toBusinessGuide(f) {
  const parts = [];
  if (f.purpose) parts.push(softenText(f.purpose));
  const rel = REL_EXPLAIN[f.orchestration];
  if (rel) parts.push(rel);
  if (f.demo_ready) {
    parts.push("Click Try it below to run this item only.");
  } else {
    parts.push("Roadmap item: read about it now; tryable in a later release.");
  }
  return parts.join(" ");
}

function softDeptIntro(flows) {
  const dept = currentDept();
  const name = dept?.name || "This department";
  if (!flows?.length) {
    return `${name} features are on the left. Open one for details; tryable items run standalone without auto-chaining.`;
  }
  return `${name} features are on the left. Cross-dept results go to shared info; other capabilities read in a separate run—key to cross-dept collaboration. Pick any item to read and try.`;
}

function showGuideInDept() {
  // Guide shown for service / user_ops departments
  return state.departmentId === "service" || state.departmentId === "user_ops";
}

function renderDeptNav() {
  el.deptNav.innerHTML = state.departments
    .map((d, i) => {
      const active = d.department_id === state.departmentId ? "active" : "";
      const sep = i > 0 ? '<span class="dept-sep" aria-hidden="true"></span>' : "";
      return `${sep}<button type="button" class="dept-nav-btn ${active}" data-dept="${d.department_id}">
        ${escapeHtml(d.name)}
      </button>`;
    })
    .join("");
  el.deptNav.querySelectorAll("[data-dept]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.departmentId = btn.dataset.dept;
      state.selectedId = null;
      state.currentFeature = null;
      el.runner.hidden = true;
      loadFeatures();
    });
  });
}

function renderDeptIntro() {
  if (!el.deptIntro) return;
  el.deptIntro.hidden = false;
  el.deptIntro.innerHTML = `<p>${escapeHtml(softDeptIntro(state.flows))}</p>`;
}

function railItems() {
  const items = [];
  if (showGuideInDept()) {
    items.push({
      id: "__guide__",
      name: "Cross-dept: pause outreach when complaint open",
      phase: "demo",
      kind: "guide",
    });
  }
  const groups = { demo: [], phase2: [], phase3: [] };
  for (const f of state.features) {
    groups[featurePhase(f)].push(f);
  }
  for (const p of PHASE_ORDER) {
    for (const f of groups[p.id]) {
      items.push({
        id: f.feature_id,
        name: displayName(f),
        phase: p.id,
        kind: "feature",
        demo_ready: !!f.demo_ready,
      });
    }
  }
  return items;
}

function renderFeatureRail() {
  const dept = currentDept();
  el.railSub.textContent = dept ? dept.name : "Select a department";
  const items = railItems();
  if (!items.length) {
    el.railList.innerHTML = `<div class="empty-card">No features</div>`;
    return;
  }

  const byPhase = { demo: [], phase2: [], phase3: [] };
  for (const item of items) {
    const ph = item.kind === "guide" ? "demo" : item.phase;
    byPhase[ph].push(item);
  }

  let html = "";
  for (const p of PHASE_ORDER) {
    const rows = byPhase[p.id];
    if (!rows.length) continue;
    html += `<div class="rail-phase" data-phase-label="${p.id}">${escapeHtml(p.title)}</div>`;
    for (const item of rows) {
      const active = state.selectedId === item.id ? "active" : "";
      const readyCls = p.id === "demo" ? "rail-item-demo" : "rail-item-planned";
      html += `<button type="button" class="rail-item ${readyCls} ${active}" data-id="${escapeHtml(item.id)}">
        <span class="rail-item-name">${escapeHtml(item.name)}</span>
      </button>`;
    }
  }

  el.railList.innerHTML = html;
  el.railList.querySelectorAll("[data-id]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.selectedId = btn.dataset.id;
      el.runner.hidden = true;
      if (el.closeBtn) el.closeBtn.hidden = true;
      syncUrl();
      renderFeatureRail();
      renderMainView();
    });
  });
}

function renderMainView() {
  const isGuide = state.selectedId === "__guide__";
  const f = state.features.find((x) => x.feature_id === state.selectedId) || null;

  el.viewEmpty.hidden = !!(isGuide || f);
  el.viewGuide.hidden = !isGuide;
  el.viewFeature.hidden = !f;

  if (isGuide) {
    const dept = currentDept();
    el.guideCrumb.textContent = `Business lead · ${dept?.name || ""} · Business playbook`;
    return;
  }

  if (!f) return;

  const dept = currentDept();
  const phase = phaseLabelOf(f);
  const nice = displayName(f);
  el.featureCrumb.textContent = `Business lead · ${dept?.name || ""} · ${nice}`;
  el.featureBadges.innerHTML = `<span class="pill ${
    featurePhase(f) === "demo" ? "pill-ok" : featurePhase(f) === "phase3" ? "pill-phase3" : "pill-phase2"
  }">${escapeHtml(phase)}</span>`;
  el.featureTitle.textContent = nice;
  el.featurePurpose.textContent = softenText(f.purpose || "");
  el.featureRunHint.textContent = f.demo_ready
    ? "Fill sample or custom content, then click Try it. Runs this item only."
    : "";

  // Top note bar is intro only; trial entry is in the trial section below
  el.featureActions.innerHTML = "";
  if (f.demo_ready) {
    openRunner(f);
  } else {
    el.runner.hidden = true;
    el.closeBtn.hidden = true;
    el.featureActions.innerHTML = `<span class="pill pill-muted">Roadmap · not tryable yet</span>`;
  }
}

function fieldVisible(name, fields) {
  return (fields || []).includes(name);
}

function openRunner(f) {
  state.currentFeature = f;
  el.runBtn.disabled = !f.demo_ready;
  el.runner.hidden = false;
  el.closeBtn.hidden = false;
  el.runner.className = `runner card layout-${f.layout || "generic"}`;
  el.runBtn.textContent = "Try it";

  const label = document.getElementById("label-input-text");
  if (label) label.textContent = isRagFeature(f) ? "Question" : "Content";

  const fields = f.input_fields || ["text"];
  document.getElementById("wrap-customer").hidden = !fieldVisible("customer_id", fields);
  document.getElementById("wrap-vin").hidden = !fieldVisible("vin", fields);
  document.getElementById("wrap-dealer").hidden = !fieldVisible("dealer_id", fields);
  document.getElementById("wrap-channel").hidden = !fieldVisible("channel", fields);
  document.getElementById("wrap-order").hidden = !fieldVisible("order_id", fields);
  el.payloadBox.hidden = f.skill_id !== "shared_write";
  el.text.placeholder = softenText(f.placeholder_text || "");
  fillSample();
  el.answer.classList.remove("answer-rich");
  el.answer.textContent = "Not tried yet.";
  el.kv.innerHTML = "";
  el.board.innerHTML = "";
  el.steps.innerHTML = "";
  el.status.textContent = "Ready";
  el.status.className = "status-line";
}

/** Extra info: business lines → internal payload */
function formatSoftPayload(payload) {
  if (!payload || typeof payload !== "object") return "";
  const note = payload.note === "platform-demo" ? "Platform demo" : payload.note || "";
  const tag = String(payload.tag_id || "").replace(/^TAG[-_]?/, "");
  const lines = [];
  if (note) lines.push(`Note: ${note}`);
  if (payload.customer_id) lines.push(`Customer id: ${payload.customer_id}`);
  if (tag) lines.push(`Business tag: ${tag}`);
  return lines.join("\n");
}

function parseSoftPayload(raw) {
  const text = String(raw || "").trim();
  if (!text) return undefined;
  if (text.startsWith("{")) return JSON.parse(text);
  const out = {};
  for (const line of text.split(/\n+/)) {
    const m = line.match(/^([^：:]+)[:：]\s*(.+)$/);
    if (!m) continue;
    const k = m[1].trim();
    const v = m[2].trim();
    if (k === "Note") out.note = v === "Platform demo" ? "platform-demo" : v;
    else if (k === "Customer id") out.customer_id = v;
    else if (k === "Business tag") out.tag_id = v.startsWith("TAG-") ? v : `TAG-${v}`;
  }
  return Object.keys(out).length ? out : undefined;
}

function fillSample() {
  const f = state.currentFeature;
  if (!f) return;
  const s = f.sample || {};
  let text = s.query || s.text || "";
  text = text
    .replace(/renewal_plan/g, "Renewal outreach assessment")
    .replace(/Read-only consumption/g, "Read-only use")
    .replace(/Shared output/g, "Shared info");
  el.text.value = text;
  el.customer.value = s.customer_id || "";
  el.vin.value = s.vin || "";
  el.dealer.value = s.dealer_id || "";
  el.channel.value = s.channel || "";
  el.order.value = s.order_id || "";
  el.payload.value = s.payload ? formatSoftPayload(s.payload) : "";
}

function collectInput() {
  const f = state.currentFeature;
  const text = el.text.value.trim();
  const input = isRagFeature(f) ? { query: text, text } : { text };
  if (!document.getElementById("wrap-customer").hidden && el.customer.value.trim()) {
    input.customer_id = el.customer.value.trim();
  }
  if (!document.getElementById("wrap-vin").hidden && el.vin.value.trim()) {
    input.vin = el.vin.value.trim();
  }
  if (!document.getElementById("wrap-dealer").hidden && el.dealer.value.trim()) {
    input.dealer_id = el.dealer.value.trim();
  }
  if (!document.getElementById("wrap-channel").hidden && el.channel.value.trim()) {
    input.channel = el.channel.value.trim();
  }
  if (!document.getElementById("wrap-order").hidden && el.order.value.trim()) {
    input.order_id = el.order.value.trim();
  }
  if (f?.skill_id === "shared_write") {
    const parsed = parseSoftPayload(el.payload.value);
    if (parsed) input.payload = parsed;
  }
  return input;
}

function kvItem(k, v) {
  if (v === undefined || v === null || v === "") return "";
  return `<div class="item"><div class="k">${escapeHtml(k)}</div><div class="v">${escapeHtml(String(v))}</div></div>`;
}

function escapeRegExp(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Business label/field mapping (display only) */
const BIZ_TERM_MAP = [
  [/is_smart_vehicle\s*=\s*true/gi, "Smart vehicle"],
  [/is_smart_vehicle\s*=\s*false/gi, "Non-smart vehicle"],
  [/`?is_smart_vehicle`?/gi, "Is smart vehicle"],
  [/intent_level\s*=\s*high/gi, "High intent"],
  [/intent_level\s*=\s*medium/gi, "Medium intent"],
  [/intent_level\s*=\s*low/gi, "Low intent"],
  [/\bnon_smart\b/gi, "Non-smart vehicle"],
  [/read_ai_outputs/gi, "Read shared info"],
  [/\bAIOutput\b/g, "Shared info record"],
  [/ai_output_ids?/gi, "Shared info ID"],
  [/consumer_allow/gi, "Readable by"],
  [/\bpayload\b/gi, "Payload detail"],
  [/customer_id/gi, "Customer ID"],
  [/tag_id/gi, "Business tag"],
  [/\bsentiment\b/gi, "Sentiment"],
  [/\bplatform-demo\b/gi, "Platform demo"],
  [/\brenewal_plan\b/g, "Renewal outreach evaluation"],
  [/\bfill_ticket\b/g, "Smart ticket fill"],
  [/\bticket_fields\b/g, "Smart ticket fill (structured)"],
  [/\bvoc_entities\b/g, "Customer voice cleanup"],
  [/\bshared_write\b/g, "Shared info write"],
  [/TAG-open-complaint/gi, '"Open complaint" tag'],
  [/TAG-pairing-failure/gi, '"Pairing failure" tag'],
  [/TAG-short-range/gi, '"Short range" tag'],
  [/TAG-reputation-risk/gi, '"Reputation risk" tag'],
  [/TAG-safety-hazard/gi, '"Safety hazard" tag'],
  [/TAG-warranty-dispute/gi, '"Warranty dispute" tag'],
  [/TAG-non-exclusive-display/gi, '"Non-exclusive display" tag'],
  [/TAG-vi-violation/gi, '"VI violation" tag'],
  [/TAG-([a-z0-9-]+)/gi, '"$1" tag'],
  [/BMS_OT_01/g, "Battery high-temp alert"],
  [/\bSOH\b/g, "Battery health"],
  [/\bOTA\b/g, "System version"],
  [/\bBMS\b/g, "Battery system"],
  [/\bMCU\b/g, "Motor controller"],
  [/\bVIN\b/g, "VIN"],
  [/\bIoT\b/g, "IoT"],
  [/(^|[^\w])neg([^\w]|$)/g, "$1Negative$2"],
  [/(^|[^\w])pos([^\w]|$)/g, "$1Positive$2"],
  [/(^|[^\w])neu([^\w]|$)/g, "$1Neutral$2"],
];

/** Map KB chunk IDs to readable titles (display only) */
function humanizeChunkId(id) {
  const raw = String(id || "").replace(/^kb_chunk_id\s*=\s*/i, "").trim();
  const m = raw.match(/^(?:[a-z]+__)?([^#]+?)(?:#c(\d+))?$/i);
  if (m) {
    const name = m[1].replace(/[-_]/g, " ").replace(/\s+/g, "").trim() || "Internal knowledge";
    const n = m[2] ? Number(m[2]) : 0;
    return n ? `${name} (ref ${n})` : name;
  }
  return "Internal knowledge material";
}

function citeTitle(c) {
  return softenText(c?.title || c?.doc_title || humanizeChunkId(c?.kb_chunk_id || c?.doc_id || ""));
}

function uniqueCiteTitles(citations) {
  const titles = [];
  const seen = new Set();
  for (const c of citations || []) {
    const t = citeTitle(c);
    if (!t || seen.has(t)) continue;
    seen.add(t);
    titles.push(t);
  }
  return titles;
}

/** Show only sources used in the answer body; avoid retrieval noise in the reference bar */
function relevantCiteTitles(text, citations) {
  const titles = uniqueCiteTitles(citations);
  if (!titles.length) return titles;
  const body = String(text || "");
  const hit = titles.filter(
    (t) => body.includes(t) || body.includes(`《${t}》`) || body.includes(t.replace(/\s+/g, ""))
  );
  return hit.length ? hit : titles.slice(0, 1);
}

function buildCiteMap(citations) {
  const map = new Map();
  for (const c of citations || []) {
    const id = String(c.kb_chunk_id || c.doc_id || "").trim();
    if (!id) continue;
    const title = citeTitle(c);
    map.set(id, title);
    map.set(`kb_chunk_id=${id}`, title);
  }
  return map;
}

/** When references already shown above, strip duplicate book titles / citation blocks from body */
function stripRedundantCitations(text, citeTitles) {
  let s = String(text || "");
  if (!citeTitles?.length) return s;

// 「reference/References」 （ / reference ）， 「Suggested next steps」
  s = s.replace(
    /(?:^|\n)[ \t]*(?:#{1,3}[ \t]*)?(?:\*\*)?(?:\d+[\.、][ \t]*)?(?:References|reference)(?:\*\*)?[ \t]*(?:\n[ \t]*(?:[-*•][ \t]*)?(?:《[^》]+》|kb_chunk_id\b[^\n]*|[:：][^\n]*))*/gi,
    "\n"
  );

  for (const t of citeTitles) {
    const esc = escapeRegExp(t);
    s = s.replace(new RegExp(`[（(]\\s*《${esc}》\\s*[）)]`, "g"), "");
    s = s.replace(new RegExp(`（[:：]\\s*《?${esc}》?）`, "g"), "");
    s = s.replace(new RegExp(`[:：]\\s*《${esc}》`, "g"), "");
    s = s.replace(new RegExp(`^[ \\t]*[-*•]?\\s*《${esc}》\\s*$`, "gm"), "");
  }

// 「Based on…《…》」
  s = s.replace(/[（(]\s*《[^》]+》\s*[）)]/g, "");
  s = s.replace(/Based on[^《\n]{0,16}《[^》]+》(?:document|troubleshooting document)?/g, "Based on related material");
  s = s.replace(/Per[^《\n]{0,16}《[^》]+》(?:document|troubleshooting document)?/g, "Per related material");
  s = s.replace(/Based on related material(?:)?document/g, "Based on related material");
  s = s.replace(/Per related material(?:)?document/g, "Per related material");
  s = s.replace(/^[ \t]*[-*•]?\s*《[^》]+》\s*$/gm, "");
  s = s.replace(/this\s*vehicle/g, "This vehicle");
  s = s.replace(/\n{3,}/g, "\n\n");
  return s.trim();
}

/** Hide DeepSeek DSML tool markup if it leaks into final_answer */
function stripDsmlMarkup(text) {
  let s = String(text || "").replace(/\uFF5C/g, "|");
  s = s.replace(
    /<?\s*\|\s*\|\s*DSML\s*\|\s*\|\s*(?:tool_calls|function_calls)\s*>[\s\S]*?(?:<\/\s*\|\s*\|\s*DSML\s*\|\s*\|\s*(?:tool_calls|function_calls)\s*>|$)/gi,
    ""
  );
  s = s.replace(/<\/?\s*\|\s*\|\s*DSML\s*\|\s*\|\s*[^>]*>/gi, "");
  s = s.replace(/<\/?\|DSML\|[^>]*>/gi, "");
  return s.trim();
}

/** Strip tech IDs; keep business-readable text */
function softenAnswerText(text, citations) {
  let s = String(text || "");
  if (/DSML/i.test(s) && /invoke/i.test(s)) {
    s = stripDsmlMarkup(s);
    if (!s) {
      s = "Model returned unexecuted tool markup. Please click Try it again.";
    }
  }
  const map = buildCiteMap(citations);
  const titles = relevantCiteTitles(text, citations);

// reference （ References ）
  s = s.replace(
    /^[ \t]*kb_chunk_id\s*[=:：]\s*(.+?)\s*$/gim,
    (_, rest) => {
      const raw = String(rest).trim();
      const idMatch = raw.match(/([\w\u4e00-\u9fff\-]+__[\w\u4e00-\u9fff\-]+#c\d{4})/);
      if (idMatch) {
        const title = map.get(idMatch[1]) || humanizeChunkId(idMatch[1]);
        return `- 《${title}》`;
      }
      const book = raw.match(/《([^》]+)》/);
      if (book) return `- 《${book[1]}》`;
      const titled = raw.match(/Title[:：]\s*([^）)]+)/);
      if (titled) return `- 《${titled[1].replace(/\s*[›>].*$/, "").trim()}》`;
      return `- 《${humanizeChunkId(raw)}》`;
    }
  );

  s = s.replace(/[（(]\s*Per[:：]\s*kb_chunk_id\s*[=:：]\s*([^）)]+?)\s*[）)]/g, (_, id) => {
    const key = String(id).trim();
    const title = map.get(key) || humanizeChunkId(key);
    return `（：${title}）`;
  });
  s = s.replace(/Per[:：]\s*kb_chunk_id\s*[=:：]\s*([^\s，,。；;）)\]]+)/g, (_, id) => {
    const title = map.get(String(id).trim()) || humanizeChunkId(id);
    return `：${title}`;
  });
  s = s.replace(/kb_chunk_id\s*[=:：]\s*/g, "");
  s = s.replace(/([\w\u4e00-\u9fff\-]+__[\w\u4e00-\u9fff\-]+#c\d{4})/g, (m) => {
    const title = map.get(m) || humanizeChunkId(m);
    return `《${title}》`;
  });
  s = s.replace(/（Title[:：][^）]*）/g, "");

  s = s.replace(/Perretrieval chunk\s*#?c?(\d{3,4})/gi, (_, n) => {
    const needle = `#c${String(n).padStart(4, "0")}`;
    for (const [id, title] of map.entries()) {
      if (String(id).includes(needle)) return `：${title}`;
    }
    return "：related knowledge";
  });
  s = s.replace(/retrieval chunk\s*#?c?(\d{3,4})/gi, (_, n) => {
    const needle = `#c${String(n).padStart(4, "0")}`;
    for (const [id, title] of map.entries()) {
      if (String(id).includes(needle)) return `《${title}》`;
    }
    return "Related knowledge";
  });

  for (const [re, to] of BIZ_TERM_MAP) s = s.replace(re, to);
// Example tag id: TAG-short-range
  s = s.replace(/`([^`]+)`/g, "$1");

  s = s
    .replace(/【System citation】/g, "[References]")
    .replace(/【reference】/g, "[References]")
    .replace(/【reference】/g, "[References]")
    .replace(/【References】/g, "[References]")
    .replace(
      /(^|\n)\s*(?:#{1,3}\s*)?(?:\*\*)?(?:\d+[\.、]\s*)?(?:References|Citations|reference|References)(?:\*\*)?\s*(?=\n|$)/gi,
      "$1References"
    )
    .replace(/\*\*KB troubleshooting advice\*\*/g, "**Troubleshooting advice**")
    .replace(/\*\*Per\/\*\*/g, "**Troubleshooting advice**")
    .replace(/Per\//g, "Troubleshooting advice")
    .replace(/\*\*Problem restatement\*\*/g, "**Problem summary**")
    .replace(/Problem restatement/g, "Problem summary")
    .replace(/Battery health \(SOH\)/g, "Battery health")
    .replace(/（SOH）/g, "")
    .replace(/OTA version/g, "System version")
    .replace(/OTA\s*version/g, "System version")
    .replace(/Smart vehicle \(smart vehicle\)/g, "Smart vehicle")
    .replace(/Shared output/g, "Shared info")
    .replace(/shared layer/g, "Shared info")
    .replace(/This feature/g, "This feature")
    .replace(/ Skill/g, "This feature")
    .replace(/\bSkill\b/g, "feature")
    .replace(/（reference[:：]/g, " (Ref: ")
    .replace(/reference[:：]\s*/gi, "Ref: ")
    .replace(/Related knowledge material/g, "Related knowledge")
    .replace(/related knowledge/g, "Related knowledge");

  s = stripRedundantCitations(s, titles);
  return s;
}

function isMdTableSep(line) {
  return /^\s*\|?\s*:?-{3,}.*?\|/.test(line);
}

function splitMdRow(line) {
  let s = String(line).trim();
  if (s.startsWith("|")) s = s.slice(1);
  if (s.endsWith("|")) s = s.slice(0, -1);
  return s.split("|").map((c) => c.trim());
}

function inlineMd(escaped) {
  return escaped
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

/** Light Markdown → HTML for business display */
function renderBusinessMarkdown(src) {
  const lines = String(src || "").replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;
  let listType = null;
  let stepN = 0;

  const closeList = () => {
    if (listType) {
      out.push(listType === "ol" ? "</ol>" : "</ul>");
      listType = null;
    }
  };

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      closeList();
      i += 1;
      continue;
    }

// 「References」 Title
    if (/^(?:#{1,3}\s+)?(?:\*\*)?(?:\d+[\.、]\s*)?(?:References|reference)(?:\*\*)?\s*$/.test(trimmed)) {
      closeList();
      i += 1;
      while (i < lines.length) {
        const t = lines[i].trim();
        if (!t || /^《[^》]+》$/.test(t) || /^[-*•]\s*《[^》]+》$/.test(t) || /^kb_chunk/i.test(t)) {
          i += 1;
          continue;
        }
        break;
      }
      continue;
    }

// ： 「 ： → 」
    if (/^.+[:：].+→.+/.test(trimmed)) {
      const rows = [];
      while (i < lines.length && /^.+[:：].+→.+/.test(lines[i].trim())) {
        const row = lines[i].trim();
        const m = row.match(/^(.+?)[:：]\s*(.+?)\s*→\s*(.+)$/);
        if (m) rows.push([m[1], m[2], m[3]]);
        i += 1;
      }
      if (rows.length) {
        closeList();
        out.push('<div class="biz-table-wrap"><table class="biz-table"><thead><tr>');
        ["Symptom", "Likely cause", "Suggested action"].forEach((h) => {
          out.push(`<th>${escapeHtml(h)}</th>`);
        });
        out.push("</tr></thead><tbody>");
        rows.forEach((r) => {
          out.push("<tr>");
          r.forEach((c) => out.push(`<td>${inlineMd(escapeHtml(c))}</td>`));
          out.push("</tr>");
        });
        out.push("</tbody></table></div>");
        continue;
      }
    }

// ： + +
    if (
      trimmed.includes("|") &&
      i + 1 < lines.length &&
      isMdTableSep(lines[i + 1])
    ) {
      closeList();
      const header = splitMdRow(trimmed);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].trim().includes("|") && !isMdTableSep(lines[i])) {
        rows.push(splitMdRow(lines[i].trim()));
        i += 1;
      }
      out.push('<div class="biz-table-wrap"><table class="biz-table"><thead><tr>');
      header.forEach((h) => {
        out.push(`<th>${inlineMd(escapeHtml(h))}</th>`);
      });
      out.push("</tr></thead><tbody>");
      rows.forEach((row) => {
        out.push("<tr>");
        header.forEach((_, idx) => {
          out.push(`<td>${inlineMd(escapeHtml(row[idx] || ""))}</td>`);
        });
        out.push("</tr>");
      });
      out.push("</tbody></table></div>");
      continue;
    }

    const h = trimmed.match(/^(#{1,3})\s+(.+)$/);
    if (h) {
      closeList();
      const level = h[1].length;
      const title = h[2].replace(/^\d+[\.、]\s*/, "");
      stepN += 1;
      out.push(
        `<h${level + 2} class="biz-h"><span class="biz-n">${stepN}.</span> ${inlineMd(escapeHtml(title))}</h${level + 2}>`
      );
      i += 1;
      continue;
    }

    const sec = trimmed.match(/^[【\[](.+?)[】\]]\s*$/);
    if (sec) {
      closeList();
      stepN += 1;
      out.push(
        `<h4 class="biz-h"><span class="biz-n">${stepN}.</span> ${inlineMd(escapeHtml(sec[1]))}</h4>`
      );
      i += 1;
      continue;
    }

// ： <ol>（ 1 ）， id
    const ol = trimmed.match(/^(\d+)[\.、]\s+(.+)$/);
    if (ol) {
      closeList();
      stepN += 1;
      const rawBody = ol[2];
      const isSection = /[：:]\s*$/.test(rawBody) || rawBody.length <= 40;
      const body = rawBody.replace(/[：:]\s*$/, "").trim();
      if (isSection) {
        out.push(
          `<h4 class="biz-h"><span class="biz-n">${stepN}.</span> ${inlineMd(escapeHtml(body))}</h4>`
        );
      } else {
        out.push(
          `<p class="biz-step"><span class="biz-n">${stepN}.</span> ${inlineMd(escapeHtml(rawBody))}</p>`
        );
      }
      i += 1;
      continue;
    }

    const ul = trimmed.match(/^[-*•]\s+(.+)$/);
    if (ul) {
      if (listType !== "ul") {
        closeList();
        out.push("<ul class='biz-list'>");
        listType = "ul";
      }
      out.push(`<li>${inlineMd(escapeHtml(ul[1]))}</li>`);
      i += 1;
      continue;
    }

    closeList();
    out.push(`<p class="biz-p">${inlineMd(escapeHtml(trimmed))}</p>`);
    i += 1;
  }
  closeList();
  return out.join("") || "<p class='biz-p'>(No result yet)</p>";
}

function formatBusinessAnswer(text, citations) {
  return renderBusinessMarkdown(softenAnswerText(text, citations));
}

function sentimentLabel(v) {
  const s = String(v || "").toLowerCase();
  if (s === "neg" || s === "negative" || s === "") return "Negative";
  if (s === "pos" || s === "positive" || s === "") return "Positive";
  if (s === "neu" || s === "neutral" || s === "") return "Neutral";
  return softenAnswerText(String(v || "—"), []);
}

function tryParseJsonObject(text) {
  const t = String(text || "").trim();
  if (!t.startsWith("{") && !t.startsWith("[")) return null;
  try {
    return JSON.parse(t);
  } catch {
    return null;
  }
}

function bizResultRowsFromObject(obj) {
  if (!obj || typeof obj !== "object" || Array.isArray(obj)) return [];
  const rows = [];
  const push = (k, v) => {
    if (v === undefined || v === null || v === "") return;
    rows.push([k, v]);
  };
  const rawTag = obj.tag_name || obj.tag_id;
  if (rawTag != null) {
    const tag = softenAnswerText(String(rawTag), [])
      .replace(/^「/, "")
      .replace(/」$/, "")
      .replace(/^TAG[-_]?/, "");
    push("Business tag", tag);
  }
  if (obj.sentiment != null) push("Sentiment", sentimentLabel(obj.sentiment));
  if (obj.problem_theme != null) push("Problem theme", String(obj.problem_theme));
  else if (obj.topic != null) push("Topic", softenAnswerText(String(obj.topic), []));
  if (obj.reputation_risk_level != null) {
    push("Reputation risk", String(obj.reputation_risk_level));
  } else if (obj.risk != null) {
    push("Risk note", softenAnswerText(String(obj.risk), []));
  }
  if (Array.isArray(obj.secondary_tag_ids) && obj.secondary_tag_ids.length) {
    push(
      "",
      obj.secondary_tag_ids
        .map((t) =>
          softenAnswerText(String(t), [])
            .replace(/^「/, "")
            .replace(/」$/, "")
        )
        .join("、")
    );
  }
  if (obj.needs_human_review === true) push("Needs human review", "yes");
  if (obj.customer_id != null) push("Customer ID", String(obj.customer_id));
  if (obj.note != null) {
    push("Note", obj.note === "platform-demo" ? "Platform demo" : String(obj.note));
  }
  if (obj.consumer_allow != null) {
    const list = Array.isArray(obj.consumer_allow)
      ? obj.consumer_allow.map(softenSkillName).join("、")
      : softenSkillName(obj.consumer_allow);
    push("Readable by", list);
  }
  return rows;
}

function renderBizResultTable(rows, summary) {
  if (!rows.length && !summary) return "";
  let html = '<div class="biz-result-card">';
  if (summary) html += `<p class="biz-result-summary">${escapeHtml(summary)}</p>`;
  if (rows.length) {
    html += '<div class="biz-result-grid">';
    for (const [k, v] of rows) {
      html += `<div class="biz-result-item"><div class="k">${escapeHtml(k)}</div><div class="v">${escapeHtml(String(v))}</div></div>`;
    }
    html += "</div>";
  }
  html += "</div>";
  return html;
}

function buildStructuredBusinessView(res) {
  const f = state.currentFeature;
  const ext = res.extensions || {};
  const text = res.final_text || res.final_answer || "";
  const payload = res.payload != null ? res.payload : ext.payload;
  const parsed = tryParseJsonObject(text);
  const rows = [];
  let summary = "";

  if (isExtractionFeature(f)) {
    summary = "Extracted from customer voice:";
    const rich =
      payload && typeof payload === "object" && !Array.isArray(payload)
        ? payload
        : parsed;
    if (rich) rows.push(...bizResultRowsFromObject(rich));
  } else if (f?.skill_id === "shared_write" || /ai_output_id|consumer_allow|payload|shared\s*AI\s*output|shared_write/i.test(text)) {
    summary = "Shared info written; other capabilities can read as needed.";
    let consumers = ext.consumer_allow || payload?.consumer_allow;
    if (!consumers) {
      const m = text.match(/(?:consumer_allow|)\s*[:=：]\s*\[([^\]]+)\]/i);
      if (m) consumers = m[1];
    }
    if (consumers) {
      const list = Array.isArray(consumers)
        ? consumers
        : String(consumers)
            .replace(/["']/g, "")
            .split(/[,、\s]+/)
            .filter(Boolean);
      rows.push(["read", list.map(softenSkillName).join("、")]);
    }
    if (payload && typeof payload === "object") {
      rows.push(...bizResultRowsFromObject(payload));
    } else {
      const note = text.match(/note\s*=\s*([^\s，,)）]+)/i);
      const cus = text.match(/customer_id\s*=\s*([^\s，,)）]+)/i);
      const tag = text.match(/tag_id\s*=\s*([^\s，,)）]+)/i);
      if (note) rows.push(["Note", note[1] === "platform-demo" ? "Platform demo" : note[1]]);
      if (cus) rows.push(["Customer id", cus[1]]);
      if (tag) rows.push(["Business tag", softenAnswerText(tag[1], [])]);
    }
  } else if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
    rows.push(...bizResultRowsFromObject(parsed));
  }

  if (!rows.length) return null;
  return renderBizResultTable(rows, summary);
}

function renderResult(res) {
  const ext = res.extensions || {};
  const text = res.final_text || res.final_answer || "(No result summary yet)";
  const cites = res.citations || ext.citations || [];
  const gate = res.gate || ext.gate || null;
  const payload = res.payload != null ? res.payload : ext.payload;
  const titles = relevantCiteTitles(text, cites);

  const structured = buildStructuredBusinessView(res);
  el.answer.classList.add("answer-rich");
  if (structured) {
    el.answer.innerHTML = structured;
  } else {
    el.answer.innerHTML = formatBusinessAnswer(text, cites);
  }
  el.status.textContent = res.ok ? "Done" : `Failed${res.error ? ": " + res.error : ""}`;
  el.status.className = `status-line ${res.ok ? "ok" : "err"}`;

  let kv = "";
  if (gate) {
    const blocked = gate.blocked === true || gate.allow_outreach === false;
    kv +=
      kvItem("Outreach decision", blocked ? "Outreach paused" : "Outreach allowed") +
      kvItem("Reason", softenAnswerText(gate.reason || "", []));
  }
// Business tag ， kv
  if (!structured && payload && typeof payload === "object" && payload.tag_id) {
    kv += kvItem("Related tag", softenAnswerText(String(payload.tag_id), []));
  }
  el.kv.innerHTML = kv;
// kv （ ）
  el.kv.querySelectorAll(".v").forEach((n) => {
    n.style.fontFamily = "var(--font)";
  });

  el.board.innerHTML = "";
  if (gate) {
    const blocked = gate.blocked === true || gate.allow_outreach === false;
    el.board.innerHTML = `
      <div class="metric"><div class="label">Outreach</div><div class="value" style="font-size:14px">${blocked ? "Paused" : "Allowed"}</div></div>
      <div class="metric"><div class="label">Note</div><div class="value" style="font-size:14px">${escapeHtml(softenAnswerText(gate.reason || "—", []))}</div></div>
      <div class="metric"><div class="label">Status</div><div class="value" style="font-size:14px">${res.ok ? "Done" : "Error"}</div></div>`;
  } else if (titles.length) {
    el.board.innerHTML =
      `<div class="metric"><div class="label">References</div><div class="value">${titles.length}</div></div>` +
      `<div class="cite-list" role="list">${titles
        .map((t) => `<span class="cite-item" role="listitem">《${escapeHtml(t)}》</span>`)
        .join("")}</div>`;
  }

// step
  el.steps.innerHTML = "";
}

async function runFeature() {
  const f = state.currentFeature;
  if (!f?.demo_ready) return;
  let input;
  try {
    input = collectInput();
  } catch (e) {
    el.status.textContent = e.message || String(e);
    el.status.className = "status-line err";
    return;
  }
  el.runBtn.disabled = true;
  el.status.textContent = "Running…";
  el.status.className = "status-line";
  try {
    const endpoint = runEndpointFor(f);
    if (!endpoint || typeof endpoint !== "string") {
      throw new Error("Trial endpoint missing. Please refresh and retry.");
    }
    const resp = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        feature_id: f.feature_id,
        skill_id: f.skill_id,
        department_id: f.department_id,
        input,
        options: { return_steps: true },
      }),
    });
    const data = await resp.json();
    if (!resp.ok) {
      const detail = data.detail;
      const msg =
        typeof detail === "string"
          ? detail
          : detail != null
            ? JSON.stringify(detail)
            : JSON.stringify(data);
      throw new Error(msg);
    }
    renderResult(data);
    if (!data.ok) {
      const why =
        data.final_text || data.final_answer || data.error || "Trial failed";
      el.status.textContent = `Not completed: ${String(why).slice(0, 180)}`;
      el.status.className = "status-line err";
    }
  } catch (e) {
    const raw = String(e && e.message ? e.message : e);
    const friendly =
      /did not match the expected pattern/i.test(raw) ||
      /Failed to fetch|NetworkError|Load failed/i.test(raw)
        ? "Network or page URL issue. Refresh and retry; if it persists, the model service may be unreachable."
        : raw;
    el.status.textContent = `Could not finish: ${friendly}`;
    el.status.className = "status-line err";
  } finally {
    el.runBtn.disabled = false;
  }
}

async function openGuideStep(departmentId, featureId) {
  state.departmentId = departmentId;
  state.selectedId = featureId;
  await loadFeatures();
}

async function loadFeatures() {
  syncUrl();
  renderDeptNav();
  const params = new URLSearchParams({ department_id: state.departmentId });
  const [featResp, flowResp] = await Promise.all([
    fetch(`/v1/features?${params}`),
    fetch(`/v1/flows?${params}`),
  ]);
  const featData = await featResp.json();
  const flowData = await flowResp.json();
  if (!featResp.ok) throw new Error(featData.detail || "Failed to load feature list");
  state.features = featData.features || [];
  state.flows = flowResp.ok ? flowData.flows || [] : [];

// （ ）
  if (
    state.selectedId &&
    state.selectedId !== "__guide__" &&
    !state.features.find((f) => f.feature_id === state.selectedId)
  ) {
    state.selectedId = null;
  }
  if (state.selectedId === "__guide__" && !showGuideInDept()) {
    state.selectedId = null;
  }

  renderDeptIntro();
  renderFeatureRail();
  renderMainView();
  syncUrl();
}

function bindGuideButtons() {
  document.getElementById("btn-guide-step1a")?.addEventListener("click", () => {
    openGuideStep("service", "F-SVC-001");
  });
  document.getElementById("btn-guide-step1b")?.addEventListener("click", () => {
    openGuideStep("service", "F-SVC-001-EXT");
  });
  document.getElementById("btn-guide-step2")?.addEventListener("click", () => {
    openGuideStep("user_ops", "F-UO-017");
  });
}

async function boot() {
  const resp = await fetch("/v1/departments");
  const data = await resp.json();
  state.departments = data.departments || [];
  if (!state.departments.find((d) => d.department_id === state.departmentId)) {
    state.departmentId = state.departments[0]?.department_id || "service";
  }
  await loadFeatures();
  bindGuideButtons();
  el.runBtn.addEventListener("click", runFeature);
  el.sampleBtn.addEventListener("click", fillSample);
  el.closeBtn.addEventListener("click", () => {
    el.runner.hidden = true;
    el.closeBtn.hidden = true;
  });
}

boot().catch((e) => {
  if (el.railSub) el.railSub.textContent = `Init failed: ${e.message || e}`;
});