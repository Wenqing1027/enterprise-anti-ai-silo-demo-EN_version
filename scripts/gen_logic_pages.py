#!/usr/bin/env python3
"""Generate /logic subpage HTML (dept links · Skill build logic · phased roadmap)."""

from __future__ import annotations

import html
from collections import defaultdict
from pathlib import Path

import yaml

from apps.catalog import DEPARTMENTS, FEATURES

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "apps" / "ui"
V = "20260808-logic4"

LOOP_TECH = {
    "retrieve": "Retrieve",
    "rag": "Retrieve",
    "act": "Act",
    "react": "Act",
    "extract": "Extract",
    "extraction": "Extract",
    "plan": "Plan",
    "planning": "Plan",
    "rule_llm": "Plan (extended Rule gate)",
    "vision": "Extract (extended Vision)",
}
TOOL_CLASS = {
    "retrieve": "knowledge",
    "rag": "knowledge",
    "act": "read + write_govern",
    "react": "read + write_govern",
    "extract": "write_govern (structured output)",
    "extraction": "write_govern (structured output)",
    "plan": "write_govern (read shared + gate)",
    "planning": "write_govern (read shared + gate)",
    "rule_llm": "write_govern (rule gate)",
    "vision": "read / knowledge (perception → tags)",
}

ORDER = [
    "service",
    "user_ops",
    "voc",
    "channel",
    "order_policy",
    "warzone",
    "retail",
    "procurement",
    "iot",
    "data_lab",
    "hr",
    "shared",
]

MODE = {
    "retrieve": ("Collaborative", "Agent/staff asks; system retrieves and answers; key commitments escalate to human"),
    "rag": ("Collaborative", "Agent/staff asks; system retrieves and answers; key commitments escalate to human"),
    "act": ("Collaborative", "Business initiates multi-step lookup/fill; shared write requires allowlist"),
    "react": ("Collaborative", "Business initiates multi-step lookup/fill; shared write requires allowlist"),
    "extract": ("Collaborative", "Input raw text, output schema fields; shared write is approval boundary"),
    "extraction": ("Collaborative", "Input raw text, output schema fields; shared write is approval boundary"),
    "plan": ("Approval", "Must read shared tags before allow/block; no silent outreach"),
    "planning": ("Approval", "Must read shared tags before allow/block; no silent outreach"),
    "rule_llm": ("Approval", "Rule gate outputs pass/tier for human confirmation"),
    "vision": ("Reporting", "Defect/status tags reported to quality; no direct enforcement loop"),
}


def esc(s: object) -> str:
    return html.escape(str(s or ""))


def biz_name(s: str) -> str:
    s = s or ""
    for a, b in [
        ("Agent proactive outreach (complaint gate)", "Proactive outreach complaint gate"),
        ("Agent ticket review (cross-dept)", "Cross-dept ticket review assist"),
        ("Smart fill · Extraction", "Smart fill · Structuring"),
        ("Smart assist answer · RAG", "Smart assist answer"),
        ("Policy Q&A · RAG", "Policy Q&A"),
        ("App smart Q&A MVP", "App smart Q&A"),
        ("Channel dashboard rollup (Planning)", "Channel dashboard rollup"),
        ("Telemetry proactive service", "Vehicle condition proactive service"),
    ]:
        s = s.replace(a, b)
    return s


def load_skill(sid: str | None) -> dict:
    if not sid:
        return {}
    p = ROOT / "skills" / sid / "skill.yaml"
    if not p.is_file():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def phase_label(f: dict) -> str:
    if f.get("demo_ready"):
        return "Phase 1 · trial ready"
    if f.get("phase") == "phase2":
        return "Phase 2"
    if f.get("phase") == "phase3":
        return "Phase 3"
    return "Planned"


def _tool_groups(tools: list[str]) -> dict[str, list[str]]:
    read_k = (
        "get_customer",
        "get_vehicle",
        "list_vehicles",
        "get_order",
        "list_orders",
        "list_inventory",
        "get_dealer",
        "get_store",
        "get_sku",
        "get_ticket",
        "list_tickets",
        "get_renewal",
        "get_user_behavior",
        "get_dealer_health",
        "list_alerts",
        "list_sales_metrics",
        "list_retail_daily",
        "list_inspections",
        "get_risk",
        "get_policy",
        "simulate_rebate_tier",
        "score_renewal",
        "route_renewal_pool",
    )
    know_k = ("search_kb", "get_kb_document", "list_kb_domains")
    write_k = (
        "write_ai_output",
        "read_ai_outputs",
        "get_ai_output",
        "read_shared_tags",
        "check_outreach_block",
        "extract_ticket_fields",
        "suggest_voc_tags",
        "get_tag",
    )
    g = {"Read business entities": [], "Search knowledge base": [], "Structure / write shared / gate": [], "Other": []}
    for t in tools:
        if t in read_k:
            g["Read business entities"].append(t)
        elif t in know_k:
            g["Search knowledge base"].append(t)
        elif t in write_k:
            g["Structure / write shared / gate"].append(t)
        elif t != "log_step":
            g["Other"].append(t)
    return {k: v for k, v in g.items() if v}


def tools_biz_text(f: dict, sk: dict, at: str) -> str:
    tools = sk.get("allowed_tools") or []
    if isinstance(tools, dict):
        tools = list(tools.keys())
    tclass = TOOL_CLASS.get(at, "")
    if tools:
        parts = []
        for label, arr in _tool_groups(tools).items():
            # map tool ids to short biz labels
            nice = {
                "get_customer": "Customer",
                "get_vehicle": "Vehicle",
                "list_vehicles": "Vehicle list",
                "get_order": "Order",
                "list_orders": "Order list",
                "list_inventory": "Inventory",
                "get_dealer": "Dealer",
                "get_store": "Store",
                "get_sku": "SKU",
                "get_ticket": "Ticket",
                "list_tickets": "Ticket list",
                "search_kb": "Search KB chunks",
                "get_kb_document": "Fetch full doc",
                "list_kb_domains": "KB domain list",
                "write_ai_output": "Write shared output",
                "read_ai_outputs": "Read shared output",
                "read_shared_tags": "Read shared tags",
                "check_outreach_block": "Outreach block check",
                "extract_ticket_fields": "Extract ticket fields",
                "suggest_voc_tags": "Suggest topic tags",
                "get_tag": "Tag dictionary",
                "get_renewal": "Renewal record",
                "get_user_behavior": "Behavior data",
                "score_renewal": "Renewal score",
                "route_renewal_pool": "Renewal pool layer",
                "get_dealer_health": "Dealer health",
                "list_alerts": "Alert",
                "list_inspections": "Inspection",
                "get_policy": "Policy slice",
            }
            shown = ", ".join(nice.get(x, x) for x in arr[:8])
            parts.append(f"{label} ({shown})")
        return f"Tool class {tclass}. This feature uses: {'; '.join(parts)}."
    if at in {"retrieve", "rag"}:
        return "Tool class knowledge. Retrieve repair/policy/regulation chunks, then generate answer with citations."
    if at in {"extract", "extraction"}:
        return "Tool class write_govern (structured). Extract fields/tags from text; write shared output when needed."
    if at in {"plan", "planning", "rule_llm"}:
        return "Tool class write_govern. Read shared tags/outputs, then allow/tier; no direct outbound call."
    if at == "vision":
        return "Perception input (image/bench) → defect tags reported; tools mostly read/annotate."
    return f"Tool class {tclass or 'TBD'}. Before launch complete tool list: which entities, shared write, knowledge lookup."


def skill_build_logic_html(f: dict, sk: dict) -> str:
    """Build logic readable by business and tech: entity → processing → model → tools → output."""
    sid = f.get("skill_id")
    at = f.get("agent_type") or ""
    loop = LOOP_TECH.get(at, at)
    purpose = f.get("purpose") or "Achieve this feature goal"
    name = biz_name(f.get("name") or "")

    # presets by known skill
    presets: dict[str, dict[str, str]] = {
        "fill_ticket": {
            "entity": "Customer, vehicle, existing tickets (master data); tag dictionary when needed",
            "process": "Verify identity and open tickets → extract ticket fields and suggest topic tags from conversation → assemble ticket draft",
            "model": "Act loop: decide what to look up and when to write; rule tools can assist field extraction",
            "tools": "Read customer/vehicle/ticket; extract fields and tag; write shared output for renewal etc.",
            "out": "Ticket draft + complaint tags to shared layer; one run fills ticket only, no auto outreach",
        },
        "ticket_fields": {
            "entity": "Agent/user raw text; customer and vehicle ids when provided",
            "process": "Extract type, summary, tags, sentiment, complaint flag per ticket schema and validate completeness",
            "model": "Extract loop: structured extraction and validation, not multi-step lookup",
            "tools": "Schema validation primary; write shared output when persisting",
            "out": "Structured ticket draft; parallel to fill-ticket for agent confirm or downstream read",
        },
        "repair_kb": {
            "entity": "Repair KB chunks (range, noise, pairing, charging, etc.); vehicle master optional",
            "process": "Retrieve relevant chunks → inject into prompt → stepwise advice with citations",
            "model": "Retrieve loop: search + generate with required citations; state when no hit",
            "tools": "Search KB chunks, fetch document, list KB domains",
            "out": "Cited troubleshooting advice; reusable for App Q&A",
        },
        "policy_kb": {
            "entity": "Policy KB (warranty, rebate, outreach red lines, store standards)",
            "process": "Retrieve policy clauses → generate guidance with citations",
            "model": "Retrieve loop; do not invent clauses not retrieved",
            "tools": "Search KB chunks, fetch document, list KB domains",
            "out": "Policy guidance with verifiable sources",
        },
        "hr_rules": {
            "entity": "HR regulations and agent QA SOP knowledge base",
            "process": "Retrieve policy/SOP points → answer; escalate individual discipline to human",
            "model": "Retrieve loop",
            "tools": "Search KB chunks, fetch document, list KB domains",
            "out": "Regulation/QA answers with citations",
        },
        "crm_lookup": {
            "entity": "Customer, vehicle, order, inventory, dealer/store/SKU master data",
            "process": "Look up entities by id → short factual summary",
            "model": "Act loop: orchestrate lookups, facts over prose",
            "tools": "Customer/vehicle/order/inventory lookup tools",
            "out": "Master-data verification for service or pre-renewal lookup",
        },
        "channel_ops": {
            "entity": "Dealer health, alerts, inspections, sales/retail daily, policy slices",
            "process": "Pull health/alerts/inspections for ops question → dashboard-style brief",
            "model": "Act loop",
            "tools": "Dealer health, alerts, inspections, sales and policy queries",
            "out": "Ops brief (numbers + anomalies + next steps)",
        },
        "renewal_plan": {
            "entity": "Shared complaint/risk tags and outputs; renewal record and behavior when allowed",
            "process": "Read shared tags and outreach block check → explain if blocked; if allowed score renewal pool and short plan",
            "model": "Plan loop: rule/tool gate first, then plan narrative",
            "tools": "Read shared tags/outputs, outreach block check; renewal score and routing when allowed",
            "out": "Allow or defer outreach + reason; when allowed include pool layer and outreach ladder (no auto dial)",
        },
        "shared_write": {
            "entity": "Structured payload from business caller",
            "process": "Validate write scope → write shared output and return id for separate consumer run",
            "model": "Act shared-write step; tool calls and permissions drive logic",
            "tools": "Write/read shared output",
            "out": "Shared output id consumable cross-department",
        },
        "voc_entities": {
            "entity": "Customer voice raw text",
            "process": "Extract theme, sentiment, risk entities vs tag dictionary → write shared layer when needed",
            "model": "Extract loop",
            "tools": "Structured extraction and validation; shared write path",
            "out": "Structured VoC for service/renewal read",
        },
    }

    if sid and sid in presets:
        p = presets[sid]
    elif at in {"retrieve", "rag"}:
        p = {
            "entity": "Knowledge domain docs (repair/policy/regulations per feature)",
            "process": "Retrieve relevant chunks → compose answer with citations",
            "model": "Retrieve loop",
            "tools": "Knowledge retrieval tools",
            "out": purpose,
        }
    elif at in {"extract", "extraction"}:
        p = {
            "entity": "Business raw text or form text",
            "process": "Extract and validate per agreed field schema",
            "model": "Extract loop",
            "tools": "Structured extraction; write shared output when needed",
            "out": purpose,
        }
    elif at in {"plan", "planning", "rule_llm"}:
        p = {
            "entity": "Shared tags/outputs + related business records",
            "process": "Read shared signals → rule or gate decision → allow/defer with reason",
            "model": "Plan loop",
            "tools": "Read shared, gate checks, necessary business queries",
            "out": purpose,
        }
    elif at == "vision":
        p = {
            "entity": "Production-line images / bench test data",
            "process": "Detect defects or status → generate tags and report to quality",
            "model": "Vision extension (Extract perception side)",
            "tools": "Perception input and annotation output (phased)",
            "out": purpose,
        }
    else:
        p = {
            "entity": "Customer/order/channel master data relevant to feature",
            "process": "Multi-step lookup and synthesis → actionable conclusion; declare shared-write consumers",
            "model": "Act loop",
            "tools": "Read master data; shared write or tagging as needed",
            "out": purpose,
        }

    title = f'"{name}" capability pack build logic'
    if sid:
        title += f" ({sid} · {loop})"
    else:
        title += f" (to mount · suggest {loop})"

    return f"""<div class="skill-logic">
              <p class="skill-logic-title">{esc(title)}</p>
              <ol>
                <li><b>Which business data / knowledge:</b>{esc(p['entity'])}</li>
                <li><b>What processing:</b>{esc(p['process'])}</li>
                <li><b>Which model / loop:</b>{esc(p['model'])}</li>
                <li><b>Which tools:</b>{esc(p['tools'])}</li>
                <li><b>Output and downstream use:</b>{esc(p['out'])}</li>
              </ol>
            </div>"""


def nav(active: int) -> str:
    flags = [""] * 4
    flags[active] = 'class="active" '
    return f"""      <nav class="logic-subnav" aria-label="Logic subpages">
        <a {flags[0]}href="/logic">Overview</a>
        <a {flags[1]}href="/logic/architecture">Part 1 · Company architecture</a>
        <a {flags[2]}href="/logic/solution">Part 2 · AI solution design</a>
        <a {flags[3]}href="/logic/risk">Part 3 · Risk controls</a>
      </nav>"""


def shell(title: str, body: str, scripts: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(title)}</title>
    <link rel="stylesheet" href="/static/styles.css?v={V}" />
    <link rel="stylesheet" href="/static/logic.css?v={V}" />
  </head>
  <body class="page-logic">
    <nav class="mode-switch" aria-label="View switcher">
      <a href="/business">Business Lead</a>
      <a href="/ops">IT Ops</a>
      <a class="active" href="/logic" aria-current="page">Logic Walkthrough</a>
    </nav>
    <div class="shell shell-wide shell-logic">
{body}
    </div>
{scripts}
  </body>
</html>
"""


def build_dept_flow_svg(by: dict) -> str:
    pos = {
        "warzone": (90, 50),
        "channel": (310, 50),
        "order_policy": (530, 50),
        "retail": (750, 50),
        "data_lab": (970, 50),
        "service": (200, 210),
        "voc": (420, 210),
        "user_ops": (640, 210),
        "hr": (860, 210),
        "procurement": (200, 380),
        "iot": (450, 380),
        "shared": (760, 380),
    }
    edges = [
        ("warzone", "channel", "line-a"),
        ("channel", "order_policy", "line-a"),
        ("order_policy", "retail", "line-a"),
        ("retail", "data_lab", "line-a"),
        ("channel", "shared", "line-a"),
        ("order_policy", "shared", "line-a"),
        ("service", "shared", "line-b"),
        ("voc", "shared", "line-b"),
        ("shared", "user_ops", "line-b"),
        ("user_ops", "service", "line-b"),
        ("service", "voc", "line-c"),
        ("service", "hr", "line-c"),
        ("hr", "shared", "line-c"),
        ("procurement", "iot", "line-d"),
        ("iot", "data_lab", "line-d"),
        ("iot", "shared", "line-d"),
        ("procurement", "shared", "line-d"),
    ]

    # which nodes belong to which line (for highlight)
    line_nodes = {
        "a": {"warzone", "channel", "order_policy", "retail", "data_lab", "shared"},
        "b": {"service", "voc", "user_ops", "shared"},
        "c": {"service", "voc", "hr", "shared"},
        "d": {"procurement", "iot", "data_lab", "shared"},
    }

    edge_svg = []
    for a, b, cls in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        line = cls.replace("line-", "")
        # slight per-line curve offset to reduce overlap when all shown
        bend = {"a": -28, "b": -8, "c": 12, "d": 28}.get(line, 0)
        mx, my = (x1 + x2) / 2 + bend * 0.3, (y1 + y2) / 2 + bend
        edge_svg.append(
            f'<path class="flow-edge {cls}" data-line="{line}" '
            f'd="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none"/>'
        )

    node_svg = []
    for did, (x, y) in pos.items():
        dname = biz_name(DEPARTMENTS.get(did, {}).get("name", did))
        short = dname.replace("Ops · ", "").replace(" / ", "/")
        n = len(by.get(did, []))
        lines = "".join(k for k, s in line_nodes.items() if did in s)
        node_svg.append(
            f'''<g class="flow-node" data-lines="{lines}" transform="translate({x},{y})">
  <rect x="-74" y="-30" width="148" height="60" rx="10"/>
  <text class="flow-node-title" y="-2" text-anchor="middle">{esc(short)}</text>
  <text class="flow-node-meta" y="18" text-anchor="middle">{n} features</text>
</g>'''
        )

    return f"""
        <div class="dept-flow-wrap" id="dept-flow">
          <div class="line-dot-bar" role="tablist" aria-label="Switch business line edges">
            <button type="button" class="line-dot active" data-line="a" aria-pressed="true">
              <i class="dot a"></i><span>Line A · Mall / channel sales</span>
            </button>
            <button type="button" class="line-dot" data-line="b" aria-pressed="false">
              <i class="dot b"></i><span>Line B · App renewal</span>
            </button>
            <button type="button" class="line-dot" data-line="c" aria-pressed="false">
              <i class="dot c"></i><span>Line C · After-sales service</span>
            </button>
            <button type="button" class="line-dot" data-line="d" aria-pressed="false">
              <i class="dot d"></i><span>Line D · Manufacturing</span>
            </button>
            <button type="button" class="line-dot line-dot-all" data-line="all" aria-pressed="false">
              <i class="dot all"></i><span>All (dimmed)</span>
            </button>
          </div>
          <svg class="dept-flow-svg" viewBox="0 0 1100 460" role="img" aria-label="Department business line flow chart">
            {''.join(edge_svg)}
            {''.join(node_svg)}
          </svg>
          <p class="card-note" style="margin:8px 0 0">
            Click a dot to show one business line; nodes are departments; shared layer handles tag/output read-write.
          </p>
        </div>"""


def build_architecture(by: dict) -> str:
    pain = {
        "service": "Slow fill, scattered knowledge, complaints hard to reuse downstream",
        "user_ops": "Renewal outreach not linked to complaint risk",
        "voc": "Voice of customer hard to structure and share cross-dept",
        "channel": "Ops data scattered; anomalies found late",
        "order_policy": "Inconsistent policy guidance; review relies on experience",
        "warzone": "Frontline Q&A and ticketing lack unified assist",
        "retail": "Repeated scripts and lookups across platforms",
        "procurement": "PO follow-up relies on manual chasing",
        "iot": "QC and vehicle alerts rely on specialist experience",
        "data_lab": "High bar for analytics self-serve; metric disputes",
        "hr": "Policy Q&A consumes HR repeat answers",
        "shared": "Cross-dept lacks unified read/write conventions",
    }
    kpi = {
        "service": "First-contact resolution · fill time · complaint closure SLA",
        "user_ops": "Renewal rate · inappropriate outreach count · gate accuracy",
        "voc": "Tag coverage · voice-to-usable-info latency",
        "channel": "Anomaly store coverage · self-serve ops analytics share",
        "order_policy": "Policy Q&A turnaround · review consistency",
        "warzone": "Frontline response time · first-pass ticket rate",
        "retail": "Auto-reply share · human transfer rate",
        "procurement": "Overdue PO handling time",
        "iot": "First-pass QC rate · alert response time",
        "data_lab": "Self-serve analytics rate · metric dispute count",
        "hr": "Self-serve policy answer share",
        "shared": "Shared info consumption count · duplicate build items",
    }
    roi = {
        "service": "Lower handle time; complaint info reused by renewal etc.",
        "user_ops": "Inappropriate outbound near zero; allowed-list conversion measurable",
        "voc": "More voice reuse; shorter theme discovery cycle",
        "channel": "Earlier anomaly detection; less report assembly time",
        "order_policy": "Higher self-serve policy share; less review rework",
        "warzone": "Shorter frontline wait",
        "retail": "Less manual repeat replies",
        "procurement": "Better follow-up timeliness",
        "iot": "Lower miss and downtime cost (phased measurement)",
        "data_lab": "Shorter data wait; unified metrics",
        "hr": "Lower repeat inquiries",
        "shared": "Lower cross-dept integration cost; traceable troubleshooting",
    }

    rows = []
    for did in ORDER:
        feats = by.get(did) or []
        if not feats:
            continue
        dname = biz_name(DEPARTMENTS.get(did, {}).get("name", did))
        for i, f in enumerate(feats):
            name = biz_name(f["name"])
            purpose = f.get("purpose") or ""
            for a, b in [
                ("Read shared complaint tags before outreach; explain when blocked", "Read shared complaint info before outreach; explain when deferred"),
                ("Cross-skill consumption blocks wrong outreach", "Other features read shared info to block inappropriate outreach"),
                ("Discover existing skills, avoid duplicate agents", "Find existing capabilities, avoid duplicate dept builds"),
            ]:
                purpose = purpose.replace(a, b)
            dept_td = (
                f'<td class="dept-merge" rowspan="{len(feats)}">{esc(dname)}</td>' if i == 0 else ""
            )
            rows.append(
                f"""              <tr>
                {dept_td}
                <td><code>{esc(f['feature_id'])}</code> {esc(name)}</td>
                <td>{esc(pain.get(did, ''))}</td>
                <td>{esc(name)}: {esc(purpose)}</td>
                <td>{esc(phase_label(f))}</td>
                <td>{esc(kpi.get(did, ''))}</td>
                <td>{esc(roi.get(did, ''))}</td>
              </tr>"""
            )

    body = f"""
      <header class="topbar">
        <div class="topbar-brand">
          <div class="eyebrow">Qingshu Mobility</div>
          <h1>Part 1 · Company architecture</h1>
        </div>
        <div class="topbar-right">
          <div class="topbar-meta">Dept lines · business lines · planned features vs KPI<br />Strategy: efficiency and business growth</div>
        </div>
      </header>
{nav(1)}
      <div class="logic-hero">
        <p class="logic-lead">
          Under the five-year strategy to introduce AI and transform architecture and product lines: first use<strong>dept nodes + colored business lines</strong>to see collaboration, 
          then expand outputs and AI features along four lines, align dept KPIs to the feature catalog.
        </p>
      </div>

      <section class="logic-section">
        <h2>Dept flow (nodes = departments · edges = business lines)</h2>
        <p class="sec-note">Planned total <strong>{len(FEATURES)}</strong> features. Default shows line A; click dots to switch.</p>
        {build_dept_flow_svg(by)}
      </section>

      <section class="logic-section">
        <h2>Four business lines · flow and dept AI features</h2>
        <p class="sec-note">Green text = AI features for each dept (business language).</p>
        <div class="logic-legend">
          <span>Step = business stage</span>
          <span class="lg-io">Brown = input / output</span>
          <span class="lg-ai">Green = AI feature</span>
        </div>
        <div class="flow-grid">
          <article class="flow-card">
            <h3>Line A · Mall / channel sales</h3>
            <p class="flow-meta">War zone → channel → order policy → new retail / data lab (cyan edges in diagram)</p>
            <ol class="flow-steps">
              <li class="flow-step"><div class="n">1</div><div class="body"><strong>Store opening and pickup push</strong><div class="io">Input: war-zone targets, store records · Output: opening progress, pickup plan</div></div></li>
              <li class="flow-step ai-hot"><div class="n">2</div><div class="body"><strong>Channel ops and anomaly detection</strong><div class="io">Input: sales, inventory, inspections · Output: health view, anomaly list</div><div class="ai-need">AI: dealer health lookup, anomaly alerts, channel analytics Q&A</div></div></li>
              <li class="flow-step ai-hot"><div class="n">3</div><div class="body"><strong>Policy Q&A and order review assist</strong><div class="io">Input: policy docs, orders · Output: guidance, review suggestions</div><div class="ai-need">AI: policy Q&A, sales policy structuring, ticket review assist, tier gate</div></div></li>
              <li class="flow-step"><div class="n">4</div><div class="body"><strong>Ops results feedback</strong><div class="io">Input: war-zone rollup · Output: review inputs</div></div></li>
            </ol>
          </article>
          <article class="flow-card">
            <h3>Line B · App renewal</h3>
            <p class="flow-meta">Service / VoC → shared layer → user ops (amber edges in diagram)</p>
            <ol class="flow-steps">
              <li class="flow-step"><div class="n">1</div><div class="body"><strong>Renewal customer segmentation</strong><div class="io">Input: expiry, activity · Output: segmented lists</div></div></li>
              <li class="flow-step ai-hot"><div class="n">2</div><div class="body"><strong>Pre-outreach compliance gate</strong><div class="io">Input: customer, vehicle, shared complaint info · Output: allow or defer outreach</div><div class="ai-need">AI: proactive outreach complaint gate; renewal/complaint score gate</div></div></li>
              <li class="flow-step ai-hot"><div class="n">3</div><div class="body"><strong>Organize outreach tasks</strong><div class="io">Input: allowed list · Output: dial or push tasks</div><div class="ai-need">AI: renewal outbound task org (phase 2); unified smart service lookup</div></div></li>
              <li class="flow-step"><div class="n">4</div><div class="body"><strong>Renewal results feedback</strong><div class="io">Input: win/decline · Output: funnel review</div></div></li>
            </ol>
          </article>
          <article class="flow-card">
            <h3>Line C · After-sales service</h3>
            <p class="flow-meta">Service ↔ VoC / HR ↔ shared layer (green edges in diagram)</p>
            <ol class="flow-steps">
              <li class="flow-step ai-hot"><div class="n">1</div><div class="body"><strong>Intake and knowledge answers</strong><div class="io">Input: user question · Output: citable answer</div><div class="ai-need">AI: repair KB Q&A, smart assist answer, App-side Q&A</div></div></li>
              <li class="flow-step ai-hot"><div class="n">2</div><div class="body"><strong>Ticket structuring and fill</strong><div class="io">Input: conversation text · Output: ticket draft, sentiment and theme</div><div class="ai-need">AI: smart fill, ticket structuring, repair multi-step lookup</div></div></li>
              <li class="flow-step ai-hot"><div class="n">3</div><div class="body"><strong>Complaint and theme persistence</strong><div class="io">Input: ticket draft, VoC · Output: shared info for other depts</div><div class="ai-need">AI: VoC structuring, fault theme clustering, shared write</div></div></li>
              <li class="flow-step ai-hot"><div class="n">4</div><div class="body"><strong>Closure and QA review</strong><div class="io">Input: service materials · Output: QA conclusion</div><div class="ai-need">AI: smart QA (phase 3); HR policy Q&A for coaching</div></div></li>
            </ol>
          </article>
          <article class="flow-card">
            <h3>Line D · Manufacturing</h3>
            <p class="flow-meta">Procurement → IoT → data lab / shared layer (purple edges in diagram)</p>
            <ol class="flow-steps">
              <li class="flow-step ai-hot"><div class="n">1</div><div class="body"><strong>Production plan and PO follow-up</strong><div class="io">Input: orders and due dates · Output: follow-up status, chase reminders</div><div class="ai-need">AI: procurement follow-up, smart chase, overdue reminders</div></div></li>
              <li class="flow-step ai-hot"><div class="n">2</div><div class="body"><strong>Line QC and traceability</strong><div class="io">Input: bench/image data · Output: pass/fail, issue log</div><div class="ai-need">AI: line/QC vision inspection (phase 2)</div></div></li>
              <li class="flow-step ai-hot"><div class="n">3</div><div class="body"><strong>Vehicle condition proactive service</strong><div class="io">Input: telemetry · Output: service reminders</div><div class="ai-need">AI: vehicle condition proactive service (phase 3)</div></div></li>
              <li class="flow-step ai-hot"><div class="n">4</div><div class="body"><strong>Ops and quality analytics Q&A</strong><div class="io">Input: metric semantics · Output: analytics answers</div><div class="ai-need">AI: smart analytics Q&A, semantic layer Q&A (phase 2)</div></div></li>
            </ol>
          </article>
        </div>
      </section>

      <section class="logic-section">
        <h2>Five-year strategy foundation</h2>
        <div class="strategy-strip">
          <div class="strategy-cell"><h4>Strategy direction</h4><p>Introduce AI to transform internal architecture and product lines; build reusable, governable enterprise capabilities.</p></div>
          <div class="strategy-cell"><h4>Adoption mode</h4><p><strong>efficiency optimization and business growth</strong>：Shorter handling time, better conversion and experience; not framed as headcount reduction.</p></div>
          <div class="strategy-cell"><h4>Alignment approach</h4><p>Digital foundation + dept planned features + dept KPIs serve company strategy.</p></div>
        </div>
      </section>

      <section class="logic-section">
        <h2>Dept feature needs (aligned to catalog · {len(FEATURES)} features)</h2>
        <p class="sec-note">Merged dept cells; one row per planned feature.</p>
        <div class="kpi-table-wrap">
          <table class="kpi-table">
            <thead>
              <tr>
                <th>Department</th>
                <th>Planned feature</th>
                <th>Current pain</th>
                <th>Future capability</th>
                <th>Phase</th>
                <th>Dept KPI focus</th>
                <th>Value measurement</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
      </section>

      <div class="logic-footer-nav">
        <a href="/logic">← Overview</a>
        <a href="/logic/solution">Go to Part 2 →</a>
      </div>
"""
    scripts = f'    <script src="/static/logic-flow.js?v={V}"></script>\n'
    return shell("Qingshu Mobility · Part 1 · Company architecture", body, scripts=scripts)


def build_solution(by: dict) -> str:
    dept_blocks = []
    for did in ORDER:
        feats = by.get(did) or []
        if not feats:
            continue
        dname = biz_name(DEPARTMENTS.get(did, {}).get("name", did))
        feat_html = []
        for f in feats:
            at = f.get("agent_type") or ""
            loop = LOOP_TECH.get(at, at)
            sk = load_skill(f.get("skill_id"))
            tools_txt = tools_biz_text(f, sk, at)
            mode, mode_desc = MODE.get(at, ("Collaborative", "Business initiates, AI assists"))
            logic_html = skill_build_logic_html(f, sk)
            name = biz_name(f["name"])
            feat_html.append(
                f"""            <article class="feat-judge">
              <div class="feat-judge-title">
                <strong>{esc(name)}</strong>
                <code>{esc(f['feature_id'])}</code>
                <span class="pill pill-ghost">{esc(phase_label(f))}</span>
              </div>
              <p class="feat-purpose">{esc(f.get('purpose') or '')}</p>
              <div class="feat-grid tech-grid">
                <div><h5>Control Loop</h5><p><b>{esc(loop)}</b></p></div>
                <div><h5>Tools (boundary)</h5><p>{esc(tools_txt)}</p></div>
                <div><h5>Interaction mode</h5><p><b>{esc(mode)}</b> — {esc(mode_desc)}</p></div>
                <div class="feat-span"><h5>Skill build logic</h5>{logic_html}</div>
              </div>
            </article>"""
            )

        routes = {
            "service": "Intake uses Retrieve for repair KB → parallel: Extract ticket fields ∥ Act verify customer/vehicle and write shared output → user ops runs Plan separately to read complaint tags for outreach gate.",
            "user_ops": "App-side Retrieve/Act for Q&A and lookup → separate Plan reads shared complaint tags for allow/defer; real outbound tasks in phase 2, not auto-chained upstream.",
            "voc": "Extract structures VoC into theme/sentiment → write shared layer → service and renewal read separately.",
            "channel": "Act pulls dealer health/alerts into brief → phase 2 dashboard rollup with human confirm before publish.",
            "order_policy": "Retrieve for policy Q&A ∥ Extract policy highlights → Act/Rule for review or tier gate.",
            "shared": "Handles shared output/tag read-write; capability catalog lookup to avoid duplicate dept builds.",
        }

        assets = {
            "service": "Writes: ticket draft, complaint/risk tags, sentiment; declares user-ops renewal gate as consumer.",
            "user_ops": "Reads: shared complaint tags and outputs; writes: allow/defer outreach, reason, short renewal plan.",
            "voc": "Writes: structured VoC (theme, entities, sentiment).",
            "channel": "Reads: dealer health/alerts; writes: ops brief highlights.",
            "order_policy": "Knowledge: policy; output: guidance and tier suggestions.",
            "shared": "Platform assets: tag dictionary, shared AI outputs, capability catalog, unified tool registry.",
        }

        dept_blocks.append(
            f"""
      <section class="logic-section dept-card">
        <h2>{esc(dname)} <span class="dept-count-inline">{len(feats)} features</span></h2>
        <p class="sec-note">Per-feature Control Loop retained; Skill build logic uses data → processing → model → tools → output for business and engineering readers.</p>
        <div class="feat-judge-list">
{chr(10).join(feat_html)}
        </div>
        <h3 class="subhead">Dept AI business sequence</h3>
        <div class="asset-card" style="max-width:100%"><p style="margin:0">{esc(routes.get(did, 'Each feature runs separately; cross-feature only via shared layer in a new run.'))}</p></div>
        <h3 class="subhead">Shared digital assets (dept-related)</h3>
        <div class="asset-card" style="max-width:100%"><p style="margin:0">{esc(assets.get(did, 'Per feature declare who writes, who reads, which tags.'))}</p></div>
      </section>"""
        )

    def kpi_for_dept(did: str, name: str = "") -> str:
        if did == "user_ops":
            return "Inappropriate outreach incidents = 0 (gate extension)"
        if did == "voc":
            return "Tag coverage ↑"
        if did == "procurement":
            return "Follow-up timeliness ↑"
        if did == "data_lab":
            return "Self-serve analytics ↑"
        if did == "retail":
            return "Auto-reply share ↑"
        if did == "iot" or "QC" in name or "quality" in name.lower():
            return "Miss-rate baseline / miss rate ↓"
        if did == "shared":
            return "Stable shared reads, auditable"
        if did in {"channel", "order_policy", "warzone", "hr"}:
            return "Self-serve Q&A ↑ · earlier anomaly detection"
        return "Single-run acceptance · faster business closure"

    p1_feats = [f for f in FEATURES if f.get("demo_ready")]
    p2_feats = [f for f in FEATURES if f.get("phase") == "phase2" and not f.get("demo_ready")]
    p3_feats = [f for f in FEATURES if f.get("phase") == "phase3" and not f.get("demo_ready")]

    def feat_chips(feats: list) -> str:
        chips = []
        for f in feats:
            did = f["department_id"]
            dshort = biz_name(DEPARTMENTS.get(did, {}).get("name", did))
            dshort = dshort.replace("Ops · ", "").replace(" / ", "/")
            chips.append(
                f'<div class="phase-feat">'
                f'<strong>{esc(biz_name(f["name"]))}</strong>'
                f'<span class="phase-feat-dept">{esc(dshort)}</span>'
                f'<span class="phase-feat-kpi">{esc(kpi_for_dept(did, biz_name(f["name"])))}</span>'
                f"</div>"
            )
        return "".join(chips) if chips else '<p class="card-note">Mount by catalog phase</p>'

    body = f"""
      <header class="topbar">
        <div class="topbar-brand">
          <div class="eyebrow">Qingshu Mobility · Solution Logic</div>
          <h1>Part 2 · AI solution design</h1>
        </div>
        <div class="topbar-right">
          <div class="topbar-meta">Control Loop retained · Skill build logic<br />Phased roadmap and current KPI</div>
        </div>
      </header>
{nav(2)}
      <div class="logic-hero">
        <p class="logic-lead">
          With <strong>departments as large cards</strong>, each feature gets <b>Control Loop</b>、Tool boundary、Interaction mode， and 
          <b>Skill build logic</b>: which data/knowledge → processing → model/loop → tools → output and downstream use.
        </p>
      </div>
{''.join(dept_blocks)}

      <section class="logic-section" style="border:none;padding:0;background:transparent;box-shadow:none">
        <div class="innov-float">
          <div class="innov-badge">Highlight</div>
          <h3>Platform unity: 4 Control Loops + 3 tool classes + shared store</h3>
          <p class="innov-claim">
            Loops: Retrieve / Act / Extract / Plan; tools: read master / knowledge / write shared & gate;
            Cross-dept via shared outputs and tag dictionary. Value: anti-silo, unified observability, loop-based cost control, auditable shared writes.
          </p>
        </div>
      </section>

      <section class="logic-section phase-roadmap-sec">
        <h2>Phase 1 / 2 / 3 · roadmap</h2>
        <p class="sec-note">Phase 1 connects foundation and cross-dept sharing; phases 2–3 extend by feature with measurable KPIs.</p>
        <div class="phase-roadmap">
          <article class="phase-panel phase1">
            <header class="phase-panel-head">
              <span class="phase-num">01</span>
              <div>
                <h4>Phase 1 · Foundation interconnect</h4>
                <p>Must deliver · trial ready</p>
              </div>
            </header>
            <div class="phase-block">
              <h5>Platform deliverables</h5>
              <div class="phase-chips">
                <span>4 Control Loops runnable</span>
                <span>Unified tool registry (read / knowledge / write shared)</span>
                <span>Single data-fetch channel</span>
                <span>Shared layer: tag dictionary + AI outputs</span>
              </div>
            </div>
            <div class="phase-block">
              <h5>Cross-dept acceptance</h5>
              <p>Service-written complaint tags are readable by user-ops Plan and block correctly; same tools reused across dept capability packs.</p>
            </div>
            <div class="phase-block">
              <h5>Trial-ready features · {len(p1_feats)}</h5>
              <div class="phase-feat-grid">{feat_chips(p1_feats)}</div>
            </div>
            <div class="phase-block phase-kpi">
              <h5>Current KPI</h5>
              <ol>
                <li>Open-complaint sample: renewal gate block hit rate = 100%</li>
                <li>All tool calls via unified registry, no private data bypass</li>
                <li>Tag dictionary covers complaint / risk tags</li>
                <li>Key runs traceable in ops console by run id</li>
                <li>Complaint fill and renewal gate are separate runs, no auto chain</li>
              </ol>
            </div>
          </article>

          <article class="phase-panel">
            <header class="phase-panel-head">
              <span class="phase-num">02</span>
              <div>
                <h4>Phase 2 · Dept feature expansion</h4>
                <p>Mount by dept · measurable ROI</p>
              </div>
            </header>
            <div class="phase-block">
              <h5>Platform progress</h5>
              <div class="phase-chips">
                <span>Complete flow playbooks</span>
                <span>Extend Act / Extract capability packs</span>
                <span>Outbound tasks still not chained upstream</span>
              </div>
            </div>
            <div class="phase-block">
              <h5>Features this phase · {len(p2_feats)}</h5>
              <div class="phase-feat-grid">{feat_chips(p2_feats)}</div>
            </div>
            <div class="phase-block phase-kpi">
              <h5>Combined KPI</h5>
              <ol>
                <li>New capability pack rollout ≤ 50% of silo project time</li>
                <li>Policy / channel self-serve Q&A share up</li>
                <li>Duplicate tool implementations → zero</li>
              </ol>
            </div>
          </article>

          <article class="phase-panel">
            <header class="phase-panel-head">
              <span class="phase-num">03</span>
              <div>
                <h4>Phase 3 · Perception and evaluation</h4>
                <p>Quality loop · compliance baseline</p>
              </div>
            </header>
            <div class="phase-block">
              <h5>Platform progress</h5>
              <div class="phase-chips">
                <span>Vision extension slot</span>
                <span>Gold eval set</span>
                <span>Audit reports</span>
                <span>No enterprise-wide single orchestrator</span>
              </div>
            </div>
            <div class="phase-block">
              <h5>Features this phase · {len(p3_feats)}</h5>
              <div class="phase-feat-grid">{feat_chips(p3_feats)}</div>
            </div>
            <div class="phase-block phase-kpi">
              <h5>Combined KPI</h5>
              <ol>
                <li>QC miss rate and downtime response meet baseline</li>
                <li>Compliance sampling pass rate met</li>
                <li>Key lines have reviewable eval baseline</li>
              </ol>
            </div>
          </article>
        </div>
      </section>

      <div class="logic-footer-nav">
        <a href="/logic/architecture">← Part 1</a>
        <a href="/logic/risk">Go to Part 3 →</a>
      </div>
"""
    return shell("Qingshu Mobility · Part 2 · AI solution design", body)


def main() -> None:
    by: dict[str, list] = defaultdict(list)
    for f in FEATURES:
        by[f["department_id"]].append(f)

    arch = build_architecture(by)
    sol = build_solution(by)
    (UI / "logic-architecture.html").write_text(arch, encoding="utf-8")
    (UI / "logic-solution.html").write_text(sol, encoding="utf-8")

    # bump css cache on overview/risk too
    for name in ("logic.html", "logic-risk.html"):
        p = UI / name
        t = p.read_text(encoding="utf-8")
        for old in ("20260808-logic1", "20260808-logic2", "20260808-logic3", "20260808-logic4"):
            t = t.replace(f"v={old}", f"v={V}")
        p.write_text(t, encoding="utf-8")

    print("OK", "features", len(FEATURES), "arch", len(arch), "sol", len(sol))


if __name__ == "__main__":
    main()
