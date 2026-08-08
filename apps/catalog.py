"""Business platform catalog: department × role × feature (full listing; demo_ready runs immediately).

V2 spec: agent_type primary values = platform control loops retrieve|act|extract|plan.
Legacy names rag|react|extraction|planning see apps.loops alias table (queries remain compatible).
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from apps.loops import (
    PLATFORM_LOOPS,
    build_agent_types,
    canonicalize,
    display_name,
    same_loop,
)

_ROOT = Path(__file__).resolve().parents[1]
_FLOWS_PATH = _ROOT / "data" / "entities" / "department_flows.json"

# ---------------------------------------------------------------------------
# Agent types (ops side split by 4 loops; business side aggregated display)
# ---------------------------------------------------------------------------

AGENT_TYPES: list[dict[str, Any]] = build_agent_types()

# ---------------------------------------------------------------------------
# Departments + roles
# ---------------------------------------------------------------------------

DEPARTMENTS: dict[str, dict[str, Any]] = {
    "service": {
        "department_id": "service",
        "name": "Service Division",
        "tone_label": "Cautious confirmation",
        "roles": [
            {"role_id": "agent", "name": "400 / Agent"},
            {"role_id": "supervisor", "name": "Team lead"},
        ],
    },
    "user_ops": {
        "department_id": "user_ops",
        "name": "User Ops / App",
        "tone_label": "Encourage without pressure",
        "roles": [
            {"role_id": "renewal_ops", "name": "Renewal ops"},
            {"role_id": "app_cs", "name": "App CS ops"},
        ],
    },
    "order_policy": {
        "department_id": "order_policy",
        "name": "Ops Management · Orders / Policy",
        "tone_label": "Strict policy tone",
        "roles": [
            {"role_id": "order_clerk", "name": "Order review specialist"},
            {"role_id": "policy_analyst", "name": "Policy analyst"},
        ],
    },
    "warzone": {
        "department_id": "warzone",
        "name": "Four Regional Zones",
        "tone_label": "Frontline direct",
        "roles": [
            {"role_id": "bd", "name": "Regional BD"},
            {"role_id": "manager", "name": "Regional manager"},
        ],
    },
    "channel": {
        "department_id": "channel",
        "name": "Channel Office",
        "tone_label": "Business dashboard tone",
        "roles": [
            {"role_id": "specialist", "name": "Channel specialist"},
            {"role_id": "manager", "name": "Channel manager"},
        ],
    },
    "retail": {
        "department_id": "retail",
        "name": "New Retail",
        "tone_label": "Shelf guide tone",
        "roles": [
            {"role_id": "cs", "name": "Platform CS"},
            {"role_id": "ops", "name": "Retail ops"},
        ],
    },
    "procurement": {
        "department_id": "procurement",
        "name": "Procurement Platform",
        "tone_label": "Milestone tracking tone",
        "roles": [
            {"role_id": "buyer", "name": "Procurement follow-up"},
            {"role_id": "lead", "name": "Procurement lead"},
        ],
    },
    "data_lab": {
        "department_id": "data_lab",
        "name": "Data Research Institute",
        "tone_label": "Conclusion-first tone",
        "roles": [
            {"role_id": "analyst", "name": "Business analyst"},
            {"role_id": "steward", "name": "Metrics steward"},
        ],
    },
    "hr": {
        "department_id": "hr",
        "name": "HR Management Platform",
        "tone_label": "Friendly neutral tone",
        "roles": [
            {"role_id": "employee", "name": "Employee self-service"},
            {"role_id": "hrbp", "name": "HRBP"},
        ],
    },
    "iot": {
        "department_id": "iot",
        "name": "IoT / Vehicle Head Unit",
        "tone_label": "Alert brief tone",
        "roles": [
            {"role_id": "ops", "name": "Connected vehicle ops"},
            {"role_id": "quality", "name": "Quality liaison"},
        ],
    },
    "voc": {
        "department_id": "voc",
        "name": "User Research / VoC",
        "tone_label": "Neutral annotation tone",
        "roles": [
            {"role_id": "analyst", "name": "UX research analyst"},
            {"role_id": "ops", "name": "VoC ops"},
        ],
    },
    "shared": {
        "department_id": "shared",
        "name": "Cross-department Shared Layer",
        "tone_label": "Neutral system tone",
        "roles": [
            {"role_id": "consumer", "name": "Business consumer"},
            {"role_id": "integrator", "name": "Integration partner"},
        ],
    },
}

# ---------------------------------------------------------------------------
# ReAct features full list (includes not-yet phase-1; demo_ready=True can run directly)
# ---------------------------------------------------------------------------

FEATURES: list[dict[str, Any]] = [
    # Service
    {
        "feature_id": "F-SVC-001",
        "name": "Smart Ticket Fill",
        "purpose": "Generate ticket draft from conversation and write to Shared output",
        "department_id": "service",
        "roles": ["agent", "supervisor"],
        "agent_type": "act",
        "skill_id": "fill_ticket",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "ticket",
        "input_fields": ["text", "customer_id", "vin", "channel"],
        "sample": {
            "text": "Complaint: store did not handle battery replacement per warranty policy; ticket open over 7 days unresolved.",
            "customer_id": "CUS-10057",
            "vin": "QS0F65B984410D7B6",
            "channel": "400",
        },
        "placeholder_text": "Describe the customer issue…",
        "story": "Story1",
        "flow_ids": ["service_ticket_to_shared", "story2_outreach_gate"],
        "note": "[ReAct · fill_ticket] Optional parallel alternative to F-SVC-001-EXT (Extraction · ticket_fields), same Story1 goal. This card uses POST /v1/react/runs; built-in tool extract_ticket_fields is rule-based field extraction, not an Extraction Agent.",
        "orchestration": "parallel_alt",
    },
    {
        "feature_id": "F-SVC-001-EXT",
        "name": "Smart Ticket Fill · Extraction",
        "purpose": "Pure structured extraction of ticket draft and write to Shared output",
        "department_id": "service",
        "roles": ["agent", "supervisor"],
        "agent_type": "extract",
        "skill_id": "ticket_fields",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "extract",
        "input_fields": ["text", "customer_id", "vin", "channel"],
        "sample": {
            "text": "Complaint: store did not handle battery replacement per warranty policy; ticket open over 7 days unresolved.",
            "customer_id": "CUS-10057",
            "vin": "QS0F65B984410D7B6",
            "channel": "400",
        },
        "placeholder_text": "Paste agent conversation / transcript…",
        "story": "Story1-Extraction",
        "flow_ids": ["service_ticket_to_shared", "story2_outreach_gate"],
        "note": "[Extraction · ticket_fields] Optional parallel alternative to F-SVC-001 (ReAct · fill_ticket); API=POST /v1/extraction/runs. Output can be consumed serially by Story2 renewal gate.",
        "orchestration": "parallel_alt",
    },
    {
        "feature_id": "F-SVC-002",
        "name": "Smart Assist Reply · RAG",
        "purpose": "Agent-side repair knowledge Q&A with reference citations",
        "department_id": "service",
        "roles": ["agent", "supervisor"],
        "agent_type": "retrieve",
        "skill_id": "repair_kb",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "rag",
        "input_fields": ["query"],
        "sample": {"query": "How to troubleshoot range below rated spec?"},
        "placeholder_text": "Enter repair / after-sales question…",
        "flow_ids": ["service_repair_qa"],
        "note": "[RAG · repair_kb] Coexists in parallel with Story1 ticket fill; API=POST /v1/rag/runs.",
        "orchestration": "parallel_orthogonal",
    },
    {
        "feature_id": "F-SVC-004",
        "name": "Repair KB Q&A",
        "purpose": "Self-service / assisted repair Q&A",
        "department_id": "service",
        "roles": ["agent", "supervisor"],
        "agent_type": "retrieve",
        "skill_id": "repair_kb",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "rag",
        "input_fields": ["query"],
        "sample": {"query": "What to do when App vehicle binding fails?"},
        "placeholder_text": "Enter repair question…",
        "flow_ids": ["service_repair_qa"],
        "note": "Same Skill repair_kb as F-SVC-002",
        "orchestration": "parallel_orthogonal",
    },
    {
        "feature_id": "F-POL-RAG",
        "name": "Policy Q&A · RAG",
        "purpose": "Q&A on warranty / rebate / renewal red-line policy text",
        "department_id": "order_policy",
        "roles": ["policy_analyst", "order_clerk"],
        "agent_type": "retrieve",
        "skill_id": "policy_kb",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "rag",
        "input_fields": ["query"],
        "sample": {"query": "How many units must Gold tier pick up in 2026 Q3 for rebate?"},
        "placeholder_text": "Enter policy question…",
        "flow_ids": ["order_policy_qa", "channel_ops_board"],
        "note": "[RAG · policy_kb] Optional parallel to order-review serial chain; can also run in parallel with channel channel_ops to prepare dashboard wording. Does not replace Rule gate.",
        "orchestration": "parallel_optional",
    },
    {
        "feature_id": "F-UO-009",
        "name": "App Smart Q&A MVP",
        "purpose": "In-app repair / usage Q&A (reuses repair domain)",
        "department_id": "user_ops",
        "roles": ["app_cs"],
        "agent_type": "retrieve",
        "skill_id": "repair_kb",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "rag",
        "input_fields": ["query"],
        "sample": {"query": "How to fix poor charging port contact?"},
        "placeholder_text": "Enter user question…",
        "flow_ids": ["user_ops_app_qa"],
        "note": "Phase 1 reuses repair_kb; parallel to renewal gate",
        "orchestration": "parallel_orthogonal",
    },
    {
        "feature_id": "F-VOC-002",
        "name": "Customer Voice Triage",
        "purpose": "Organize customer voice into business tags, sentiment, and risk alerts",
        "department_id": "voc",
        "roles": ["analyst", "ops"],
        "agent_type": "extract",
        "skill_id": "voc_entities",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "extract",
        "input_fields": ["text", "customer_id", "vin"],
        "sample": {
            "text": "Full charge only gets half the rated range; planning to go to media.",
            "customer_id": "CUS-10057",
        },
        "placeholder_text": "Paste customer voice…",
        "story": "Story1-Extraction",
        "flow_ids": ["voc_entities_to_shared", "story2_outreach_gate"],
        "note": "Cross-department parallel write to shared store with service ticket fill; becomes Story2 upstream when block tags present",
        "orchestration": "parallel_producer",
    },
    {
        "feature_id": "F-SVC-005",
        "name": "VoC Fault Clustering",
        "purpose": "Cluster tickets for product / quality insights",
        "department_id": "service",
        "roles": ["supervisor"],
        "agent_type": "extract",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "extract",
        "note": "Display: sequential dependency after F-VOC-002 row-level tagging; phase 1 does not run control loop",
        "orchestration": "sequence_downstream",
        "flow_ids": ["voc_entities_to_shared"],
    },
    {
        "feature_id": "F-SVC-008",
        "name": "Smart QA (SOP)",
        "purpose": "Call transcript → SOP compliance extraction",
        "department_id": "service",
        "roles": ["supervisor"],
        "agent_type": "extract",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase3",
        "layout": "extract",
        "note": "Display: Extraction capability parallel to ticket fill; requires transcription upstream",
        "orchestration": "parallel_showcase",
    },
    {
        "feature_id": "F-OPS-004",
        "name": "Sales Policy Parsing",
        "purpose": "Policy source text → rebate tier structure",
        "department_id": "order_policy",
        "roles": ["policy_analyst"],
        "agent_type": "extract",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "extract",
        "note": "Display: sequential upstream → Rule+LLM tier gate (see order_policy_review)",
        "orchestration": "sequence_upstream",
        "flow_ids": ["order_policy_review"],
    },
    {
        "feature_id": "F-FIN-001",
        "name": "Smart Expense · Three-way Match Extraction",
        "purpose": "Extract fields from invoice / contract / goods receipt",
        "department_id": "shared",
        "roles": ["integrator"],
        "agent_type": "extract",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase3",
        "layout": "extract",
        "note": "Display: Extraction serial with Rule+LLM; section display only this release",
        "orchestration": "sequence_upstream",
    },
    {
        "feature_id": "F-SVC-003",
        "name": "Multi-step Repair Assist",
        "purpose": "Look up vehicle / ticket / knowledge then give actionable reply",
        "department_id": "service",
        "roles": ["agent", "supervisor"],
        "agent_type": "act",
        "skill_id": "crm_lookup",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "crm",
        "input_fields": ["text", "customer_id", "vin"],
        "sample": {
            "text": "Customer reports motor noise; please check vehicle and open ticket summary.",
            "customer_id": "CUS-10057",
            "vin": "QS0F65B984410D7B6",
        },
        "placeholder_text": "Describe repair inquiry…",
        "note": "Phase 1 uses crm_lookup to demo master-data multi-step lookup; full repair RAG is RAG Agent",
    },
    # User ops (Planning primary display; data lookup can still attach ReAct)
    {
        "feature_id": "F-UO-001",
        "name": "Renewal AI Outreach Tasks",
        "purpose": "Look up renewal pool and intent, then organize outreach script",
        "department_id": "user_ops",
        "roles": ["renewal_ops"],
        "agent_type": "plan",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "[Planning showcase] Narrative wider than gate; runnable demo see F-UO-017 · renewal_plan. Upstream tags written separately by Extraction/ReAct.",
        "orchestration": "sequence_downstream",
        "flow_ids": ["user_ops_renewal_gate", "story2_outreach_gate"],
        "co_agents": ["extract", "act", "rule_llm"],
    },
    {
        "feature_id": "F-UO-017",
        "name": "Agent Proactive Outreach (Complaint Gate)",
        "purpose": "Read shared complaint tags to decide outreach; give reason when blocked",
        "department_id": "user_ops",
        "roles": ["renewal_ops", "app_cs"],
        "agent_type": "plan",
        "skill_id": "renewal_plan",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "generic",
        "input_fields": ["customer_id", "vin", "text"],
        "sample": {
            "text": "Assess whether this user is eligible for renewal outreach (must read shared complaint tags).",
            "customer_id": "CUS-10057",
            "vin": "QS0F65B984410D7B6",
        },
        "placeholder_text": "customer_id + vin…",
        "story": "Story2 consumer side (Planning renewal_plan)",
        "note": "[Plan · renewal_plan] Runs independently in a separate pass reading shared layer; upstream ticket fill / VoC must write complaint tags first. Does not linked-run upstream Agent.",
        "orchestration": "sequence_downstream",
        "flow_ids": ["user_ops_renewal_gate", "story2_outreach_gate"],
        "co_agents": ["extract", "act"],
    },
    {
        "feature_id": "F-UO-019",
        "name": "Unified Smart CS",
        "purpose": "App-side multi-step master-data lookup then answer",
        "department_id": "user_ops",
        "roles": ["app_cs"],
        "agent_type": "act",
        "skill_id": "crm_lookup",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "crm",
        "input_fields": ["text", "customer_id", "vin"],
        "sample": {
            "text": "User asks about vehicle binding failure; check customer and vehicle status.",
            "customer_id": "CUS-10057",
            "vin": "QS0F65B984410D7B6",
        },
        "placeholder_text": "App user question…",
        "flow_ids": ["user_ops_renewal_gate"],
    },
    # Order policy
    {
        "feature_id": "F-OPS-003",
        "name": "Smart Order Creation & Review",
        "purpose": "Check inventory → policy → alternatives → status recommendation",
        "department_id": "order_policy",
        "roles": ["order_clerk", "policy_analyst"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "[Serial showcase] Extraction extract order → Rule+LLM gate → ReAct lookup; optional parallel with F-POL-RAG (policy Q&A), RAG does not replace this gate. Skill order_review pending.",
        "orchestration": "sequence_upstream",
        "flow_ids": ["order_policy_review", "order_policy_qa"],
    },
    {
        "feature_id": "F-X-004",
        "name": "Agent Order Review (Cross-department Line)",
        "purpose": "Multi-step reasoning on order / production / rebate recommendations",
        "department_id": "order_policy",
        "roles": ["order_clerk", "policy_analyst"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    # Regional zones
    {
        "feature_id": "F-WZ-001",
        "name": "Pickup / Offline Q&A Assist",
        "purpose": "Store-side inventory + policy lookup with action checklist",
        "department_id": "warzone",
        "roles": ["bd", "manager"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    {
        "feature_id": "F-WZ-002",
        "name": "Regional Order / Policy Tier Assist",
        "purpose": "Regional order and policy AI assist",
        "department_id": "warzone",
        "roles": ["bd", "manager"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    # Channel
    {
        "feature_id": "F-OPS-012",
        "name": "Business Health / Alert Query",
        "purpose": "Query health index, alerts, inspection slices",
        "department_id": "channel",
        "roles": ["specialist", "manager"],
        "agent_type": "act",
        "skill_id": "channel_ops",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "board",
        "input_fields": ["text", "dealer_id"],
        "sample": {
            "text": "Summarize this tier-1 dealer health index, alerts, and recommended actions.",
            "dealer_id": "DLR-3017",
        },
        "placeholder_text": "Dealer business query…",
        "note": "[Parallel prep] Can fetch wording in parallel with order-side F-POL-RAG (policy_kb); dashboard Planning merge see F-CH-PLAN (showcase).",
        "orchestration": "parallel_alt",
        "flow_ids": ["channel_ops_board"],
    },
    {
        "feature_id": "F-CH-PLAN",
        "name": "Channel Dashboard Merge (Planning)",
        "purpose": "Merge business queries and policy wording into dashboard recommendations",
        "department_id": "channel",
        "roles": ["specialist", "manager"],
        "agent_type": "plan",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "board",
        "note": "[Planning showcase] Upstream can run F-OPS-012 (ReAct) and F-POL-RAG in parallel; merge does not auto linked-run.",
        "orchestration": "sequence_downstream",
        "flow_ids": ["channel_ops_board"],
        "co_agents": ["act", "retrieve"],
    },
    # Rule+LLM (gate showcase)
    {
        "feature_id": "F-OPS-RULE",
        "name": "Order Review Tier Gate",
        "purpose": "Rule-based rebate / inventory tier decision + LLM explanation",
        "department_id": "order_policy",
        "roles": ["order_clerk", "policy_analyst"],
        "agent_type": "rule_llm",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "[Serial mid-stage · Rule+LLM] Upstream Extraction extract order → this gate → downstream ReAct lookup; optional parallel with F-POL-RAG.",
        "orchestration": "sequence_downstream",
        "flow_ids": ["order_policy_review"],
    },
    {
        "feature_id": "F-UO-RULE",
        "name": "Renewal / Complaint Score Gate",
        "purpose": "Rule + LLM score whether proactive outreach is allowed",
        "department_id": "user_ops",
        "roles": ["renewal_ops"],
        "agent_type": "rule_llm",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "[Serial · Rule+LLM] Score after reading shared complaint tags; full chain see Story2 / Planning F-UO-017.",
        "orchestration": "sequence_downstream",
        "flow_ids": ["user_ops_renewal_gate", "story2_outreach_gate"],
    },
    # Vision
    {
        "feature_id": "F-IOT-VISION",
        "name": "Production Line / QA Visual Inspection",
        "purpose": "Image understanding → defect tags for rule-merge alerts",
        "department_id": "iot",
        "roles": ["ops", "quality"],
        "agent_type": "vision",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "[Parallel showcase] Vision ∥ Extraction → Rule merge; not runnable in phase 1.",
        "orchestration": "parallel_showcase",
        "flow_ids": ["iot_quality_inspect"],
    },
    # New retail
    {
        "feature_id": "F-RET-001",
        "name": "Multi-platform CS Auto-reply",
        "purpose": "Look up order / inventory / promotion then reply",
        "department_id": "retail",
        "roles": ["cs", "ops"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    {
        "feature_id": "F-RET-002",
        "name": "Online Platform Sales CS",
        "purpose": "E-commerce platform sales inquiry AI handling",
        "department_id": "retail",
        "roles": ["cs"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    # Procurement
    {
        "feature_id": "F-PUR-001",
        "name": "Procurement Follow-up Bot",
        "purpose": "Overdue PO chase + logistics confirmation",
        "department_id": "procurement",
        "roles": ["buyer", "lead"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    {
        "feature_id": "F-PUR-003",
        "name": "Smart Follow-up",
        "purpose": "Purchase order follow-up automation",
        "department_id": "procurement",
        "roles": ["buyer"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    {
        "feature_id": "F-PUR-004",
        "name": "Procurement Chase Reminder",
        "purpose": "Multi-step reasoning triggers procurement follow-up reminder",
        "department_id": "procurement",
        "roles": ["buyer", "lead"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    # Data
    {
        "feature_id": "F-DAT-003",
        "name": "Smart Data Query",
        "purpose": "Clarify metrics → query semantic layer → return numbers",
        "department_id": "data_lab",
        "roles": ["analyst", "steward"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    {
        "feature_id": "F-X-002",
        "name": "BI Semantic Layer + Smart Data Query (Shared)",
        "purpose": "Unified data query and auto-report foundation",
        "department_id": "data_lab",
        "roles": ["analyst", "steward"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
    },
    # HR
    {
        "feature_id": "F-HR-001",
        "name": "Employee AI Assistant · Policy Q&A",
        "purpose": "HR policy / agent SOP RAG Q&A",
        "department_id": "hr",
        "roles": ["employee", "hrbp"],
        "agent_type": "retrieve",
        "skill_id": "hr_rules",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "rag",
        "input_fields": ["query"],
        "sample": {"query": "What phrases must agents avoid in QA?"},
        "placeholder_text": "Enter policy / SOP question…",
        "note": "[RAG · hr_rules] Q&A primary axis; workflow steps can use ReAct",
        "flow_ids": ["hr_policy_qa"],
        "orchestration": "standalone",
        "co_agents": ["act"],
    },
    # IoT
    {
        "feature_id": "F-IOT-003",
        "name": "Telemetry Proactive Service",
        "purpose": "Look up alerts / mileage → recommend actions → write output",
        "department_id": "iot",
        "roles": ["ops", "quality"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase3",
        "layout": "generic",
    },
    # Cross-department shared
    {
        "feature_id": "F-X-CRM",
        "name": "Master Data Lookup",
        "purpose": "Unified customer · vehicle · order · ticket ID lookup",
        "department_id": "shared",
        "roles": ["consumer", "integrator"],
        "agent_type": "act",
        "skill_id": "crm_lookup",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "crm",
        "input_fields": ["text", "customer_id", "vin", "order_id"],
        "sample": {
            "text": "Look up this customer's vehicle and recent order summary.",
            "customer_id": "CUS-10057",
            "vin": "QS0F65B984410D7B6",
        },
        "placeholder_text": "Master data query…",
    },
    {
        "feature_id": "F-X-WRITE",
        "name": "Shared Store Write",
        "purpose": "Write results to shared store for other capabilities to read",
        "department_id": "shared",
        "roles": ["integrator", "consumer"],
        "agent_type": "act",
        "skill_id": "shared_write",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "asset",
        "input_fields": ["text"],
        "sample": {
            "text": "Write a demo shared record for Renewal outreach assessment to read.",
            "payload": {
                "note": "platform-demo",
                "customer_id": "CUS-10057",
                "tag_id": "TAG-open-complaint",
            },
        },
        "placeholder_text": "Describe content to write to shared store…",
    },
    {
        "feature_id": "F-X-READ",
        "name": "Shared Tags / Output Read",
        "purpose": "Cross-Skill consumption; block incorrect outreach",
        "department_id": "shared",
        "roles": ["consumer", "integrator"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "Tools read_ai_outputs / check_outreach_block ready; standalone Skill pending",
    },
    {
        "feature_id": "F-X-CAP",
        "name": "Capability Catalog Search",
        "purpose": "Discover existing Skills; avoid duplicate Agent builds",
        "department_id": "shared",
        "roles": ["integrator"],
        "agent_type": "act",
        "skill_id": None,
        "demo_ready": False,
        "status": "planned",
        "phase": "phase2",
        "layout": "generic",
        "note": "list_capabilities tool and /v1/capabilities API available",
    },
    {
        "feature_id": "F-X-CH",
        "name": "Channel Business Query (Shared Data Source)",
        "purpose": "Business and compliance from same data source",
        "department_id": "shared",
        "roles": ["consumer"],
        "agent_type": "act",
        "skill_id": "channel_ops",
        "demo_ready": True,
        "status": "demo",
        "phase": "demo",
        "layout": "board",
        "input_fields": ["text", "dealer_id"],
        "sample": {
            "text": "View tier-1 health and alerts from shared perspective.",
            "dealer_id": "DLR-3017",
        },
        "placeholder_text": "Channel business query…",
    },
]


def list_departments() -> list[dict[str, Any]]:
    out = []
    for d in DEPARTMENTS.values():
        feats = [f for f in FEATURES if f["department_id"] == d["department_id"]]
        out.append(
            {
                "department_id": d["department_id"],
                "name": d["name"],
                "tone_label": d["tone_label"],
                "roles": d["roles"],
                "feature_count": len(feats),
                "demo_count": sum(1 for f in feats if f.get("demo_ready")),
            }
        )
    return out


def get_department(department_id: str) -> dict[str, Any] | None:
    d = DEPARTMENTS.get(department_id)
    if not d:
        return None
    return {
        "department_id": d["department_id"],
        "name": d["name"],
        "tone_label": d["tone_label"],
        "roles": d["roles"],
    }


def list_roles(department_id: str) -> list[dict[str, Any]]:
    d = DEPARTMENTS.get(department_id)
    return list(d["roles"]) if d else []


def _agent_display_name(agent_type: str | None) -> str:
    return display_name(agent_type)


def _feature_phase(f: dict[str, Any]) -> str:
    """Normalize phase: demo | phase2 | phase3."""
    if f.get("demo_ready") or f.get("status") == "demo":
        return "demo"
    raw = str(f.get("phase") or "").strip().lower()
    if raw in {"demo", "phase1"}:
        return "demo"
    if raw in {"phase3", "p3", "3"}:
        return "phase3"
    if raw in {"phase2", "p2", "2"}:
        return "phase2"
    if canonicalize(f.get("agent_type")) == "vision":
        return "phase3"
    return "phase2"


PHASE_LABELS = {"demo": "Demo", "phase2": "Phase 2", "phase3": "Phase 3"}


def _node_loop(n: dict[str, Any]) -> str | None:
    """Control loop on flow node: prefer control_loop, back-compat agent_type."""
    return canonicalize(n.get("control_loop") or n.get("agent_type"))


def _agents_used(f: dict[str, Any], flows: list[dict[str, Any]]) -> list[str]:
    """Control loops actually used by this feature (primary + co_agents + parallel adjacency on flows); canonical names."""
    primary = canonicalize(f.get("agent_type"))
    ordered = list(PLATFORM_LOOPS) + ["rule_llm", "vision"]
    used: list[str] = []

    def add(a: str | None) -> None:
        ca = canonicalize(a)
        if ca and ca not in used:
            used.append(ca)

    add(primary)
    for a in f.get("co_agents") or []:
        add(a)

    skill = f.get("skill_id")
    for fl in flows:
        nodes = fl.get("nodes") or []
        by_id = {}
        for n in nodes:
            nid = n.get("node_id") or n.get("id")
            if nid:
                by_id[nid] = n
        my_ids = set()
        for n in nodes:
            nid = n.get("node_id") or n.get("id")
            if not nid:
                continue
            if skill and n.get("skill_id") == skill:
                my_ids.add(nid)
            elif same_loop(_node_loop(n), primary) and (
                not skill or not n.get("skill_id") or n.get("skill_id") == skill
            ):
                my_ids.add(nid)
        for e in fl.get("edges") or []:
            if e.get("mode") != "parallel":
                continue
            a_from, a_to = e.get("from"), e.get("to")
            if a_from not in my_ids and a_to not in my_ids:
                continue
            for nid in (a_from, a_to):
                add(_node_loop(by_id.get(nid) or {}))

    rest = [a for a in ordered if a in used and a != primary]
    extras = [a for a in used if a != primary and a not in rest]
    return ([primary] if primary else []) + rest + extras


def _public_feature(f: dict[str, Any]) -> dict[str, Any]:
    dept = DEPARTMENTS.get(f["department_id"], {})
    flow_ids = list(f.get("flow_ids") or [])
    flows = []
    for fid in flow_ids:
        fl = get_flow(fid)
        if not fl:
            continue
        modes = {e.get("mode") for e in (fl.get("edges") or [])}
        flows.append(
            {
                "flow_id": fid,
                "name": fl.get("name"),
                "demo_ready": bool(fl.get("demo_ready")),
                "notes": fl.get("notes") or "",
                "has_parallel": "parallel" in modes,
                "has_sequence": "sequence" in modes,
                "parallel_groups": fl.get("parallel_groups") or [],
                "nodes": fl.get("nodes") or [],
                "edges": fl.get("edges") or [],
            }
        )
    orch = f.get("orchestration") or (
        "parallel_showcase" if not f.get("demo_ready") else "standalone"
    )
    agents = _agents_used(f, flows)
    agents_label = "·".join(_agent_display_name(a) for a in agents if a)
    phase = _feature_phase(f)
    agent_type = canonicalize(f["agent_type"]) or f["agent_type"]
    return {
        "feature_id": f["feature_id"],
        "name": f["name"],
        "purpose": f["purpose"],
        "department_id": f["department_id"],
        "department_name": dept.get("name"),
        "tone_label": dept.get("tone_label"),
        "roles": list(f.get("roles") or []),
        "agent_type": agent_type,
        "agents": agents,
        "agents_label": agents_label or _agent_display_name(agent_type),
        "co_agents": [canonicalize(a) or a for a in (f.get("co_agents") or [])],
        "skill_id": f.get("skill_id"),
        "demo_ready": bool(f.get("demo_ready")),
        "status": f.get("status", "planned"),
        "phase": phase,
        "phase_label": PHASE_LABELS.get(phase, "Phase 2"),
        "layout": f.get("layout", "generic"),
        "input_fields": list(f.get("input_fields") or ["text"]),
        "sample": dict(f.get("sample") or {}),
        "placeholder_text": f.get("placeholder_text") or "",
        "story": f.get("story"),
        "note": f.get("note"),
        "flow_ids": flow_ids,
        "flows": flows,
        "orchestration": orch,
    }


def list_features(
    *,
    department_id: str | None = None,
    role_id: str | None = None,
    agent_type: str | None = None,
    demo_only: bool = False,
) -> list[dict[str, Any]]:
    want = canonicalize(agent_type) if agent_type else None
    rows = []
    for f in FEATURES:
        if department_id and f["department_id"] != department_id:
            continue
        if role_id and role_id not in (f.get("roles") or []):
            continue
        if want and not same_loop(f.get("agent_type"), want):
            continue
        if demo_only and not f.get("demo_ready"):
            continue
        rows.append(_public_feature(f))
    return rows


def get_feature(feature_id: str) -> dict[str, Any] | None:
    for f in FEATURES:
        if f["feature_id"] == feature_id:
            return _public_feature(f)
    return None


def list_agent_types() -> list[dict[str, Any]]:
    out = []
    for a in AGENT_TYPES:
        loop_id = a["agent_type"]
        feats = [f for f in FEATURES if same_loop(f.get("agent_type"), loop_id)]
        out.append(
            {
                **a,
                "feature_count": len(feats),
                "demo_count": sum(1 for f in feats if f.get("demo_ready")),
                "features": [_public_feature(f) for f in feats],
            }
        )
    return out


def get_agent_type(agent_type: str) -> dict[str, Any] | None:
    """Accept canonical name or legacy alias (rag/react/extraction/planning)."""
    want = canonicalize(agent_type)
    for a in list_agent_types():
        if a["agent_type"] == want or agent_type in (a.get("aliases") or []):
            return a
        if a.get("legacy_alias") == agent_type:
            return a
    return None


# ---- Legacy department view API surface (for run API assembly) ----

def public_view_from_feature(f: dict[str, Any]) -> dict[str, Any]:
    """Map runnable feature to legacy run API department view fields."""
    return {
        "department_id": f["department_id"],
        "name": f.get("department_name") or f["department_id"],
        "skill_id": f.get("skill_id"),
        "tone_label": f.get("tone_label"),
        "layout": f.get("layout", "generic"),
        "blurb": f.get("purpose"),
        "input_fields": f.get("input_fields") or ["text"],
        "result_focus": [],
        "placeholder_text": f.get("placeholder_text") or "",
        "sample": f.get("sample") or {},
        "feature_id": f["feature_id"],
        "demo_ready": f.get("demo_ready"),
    }


def resolve_department_for_skill(skill_id: str) -> dict[str, Any] | None:
    for f in FEATURES:
        if f.get("skill_id") == skill_id and f.get("demo_ready"):
            return public_view_from_feature(_public_feature(f))
    return None


# ---------------------------------------------------------------------------
# In-department orchestration (department_flows.json · Planning contract, not runtime)
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def load_department_flows() -> dict[str, Any]:
    """Load machine-readable orchestration; normalize nodes to V2 (skill/placeholder/store_* + control_loop)."""
    if not _FLOWS_PATH.is_file():
        return {"version": "v2", "flows": []}
    data = json.loads(_FLOWS_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"version": "v2", "flows": []}
    flows = data.get("flows")
    if not isinstance(flows, list):
        data = {**data, "flows": []}
        return data
    data = {**data, "flows": [_normalize_flow(fl) for fl in flows]}
    return data


def _normalize_flow_node(n: dict[str, Any]) -> dict[str, Any]:
    """Node = independently runnable Skill/feature (or shared-layer point/placeholder), not an Agent pipeline."""
    from apps.skill_loops import resolve_skill_control_loop
    from apps.loops import EXTENSION_TYPES

    kind = n.get("kind") or "placeholder"
    skill_id = n.get("skill_id")
    loop = n.get("control_loop") or resolve_skill_control_loop(
        skill_id=skill_id,
        agent_type=n.get("agent_type"),
    )
    loop = canonicalize(loop)
    extension_type = n.get("extension_type")
    if loop in EXTENSION_TYPES:
        extension_type = loop
        loop = EXTENSION_TYPES[loop]["parent_loop"]

    if kind == "agent_type":
        kind = "skill" if skill_id else "placeholder"
    if kind not in {"skill", "placeholder", "store_read", "store_write"}:
        kind = "placeholder"

    out: dict[str, Any] = {
        "node_id": n.get("node_id") or n.get("id"),
        "kind": kind,
        "skill_id": skill_id,
        "control_loop": None if kind in {"store_read", "store_write"} else loop,
        "label": n.get("label") or skill_id or kind,
    }
    if extension_type:
        out["extension_type"] = extension_type
    if n.get("note"):
        out["note"] = n["note"]
    # Back-compat old UI: attach agent_type=control_loop (canonical name)
    if out.get("control_loop"):
        out["agent_type"] = out["control_loop"]
    return out


def _normalize_flow(fl: dict[str, Any]) -> dict[str, Any]:
    nodes = [_normalize_flow_node(n) for n in (fl.get("nodes") or [])]
    edges = list(fl.get("edges") or [])
    modes = {e.get("mode") for e in edges}
    has_parallel = "parallel" in modes or bool(fl.get("parallel_groups"))
    has_sequence = "sequence" in modes
    return {
        **fl,
        "nodes": nodes,
        "edges": edges,
        "has_parallel": has_parallel,
        "has_sequence": has_sequence,
        # Spec field: explicitly not a linked-run engine
        "executable": False,
        "relation_kinds": [
            *(["parallel"] if has_parallel else []),
            *(["shared_dependency"] if has_sequence else []),
        ],
    }


def list_flows(*, demo_ready: bool | None = None) -> list[dict[str, Any]]:
    flows = list(load_department_flows().get("flows") or [])
    if demo_ready is None:
        return flows
    return [f for f in flows if bool(f.get("demo_ready")) is demo_ready]


def get_flow(flow_id: str) -> dict[str, Any] | None:
    for f in list_flows():
        if f.get("flow_id") == flow_id:
            return f
    return None


def get_flows_by_department(department_id: str) -> list[dict[str, Any]]:
    return [f for f in list_flows() if f.get("department_id") == department_id]
