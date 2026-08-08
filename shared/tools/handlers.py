"""All business Tool implementations (defined once here, exposed via ToolRegistry).

Three governance classes (read / knowledge / write_govern) mapped in shared/tools/governance.py; 
written to ToolSpec.tool_class on register; category here remains secondary business-domain label.
"""

from __future__ import annotations

import re
from typing import Any, Callable

from shared.datafetcher.fetcher import DataFetcher
from shared.models.enums import StepStatus
from shared.store.store import SharedStore
from shared.tools.base import ToolContext, ToolSpec
from shared.tools.guards import (
    BLOCKING_TAGS,
    clamp_limit,
    dump_model,
    guard_customer_id,
    guard_kb_domain,
    guard_payload,
    guard_text,
    guard_vin,
)

Handler = Callable[..., dict[str, Any]]


# ---------------------------------------------------------------------------
# keyword rules for extraction / tagging (Demo-level, no LLM)
# ---------------------------------------------------------------------------

_TAG_RULES: list[tuple[str, list[str]]] = [
    ("TAG-open-complaint", ["open complaint", "complaint", "unresolved", "over 7 days", "7 days", "multiple complaint", "not resolved", "still open", "ticket open"]),
    ("TAG-warranty-dispute", ["warranty", "deny warranty", "refuse replacement", "refuse to replace", "warranty policy"]),
    ("TAG-short-range", ["short range", "range", "battery drain", "rated range", "mileage", "won't reach"]),
    ("TAG-weak-power", ["weak power", "no power", "underpowered", "hill climb", "climbing"]),
    ("TAG-noise", ["noise", "rattle", "squeak", "vibration"]),
    ("TAG-brake", ["brake", "stopping distance", "brake feel", "soft brake"]),
    ("TAG-slow-charging", ["slow charg", "won't fully charge", "charging slow", "not fully charge"]),
    ("TAG-pairing-failure", ["pairing", "bind", "binding fail", "device offline", "pairing fail"]),
    ("TAG-slow-onsite-service", ["slow onsite", "slow service", "never came", "onsite slow"]),
    ("TAG-poor-attitude", ["poor attitude", "rude", "impatient", "bad attitude"]),
    ("TAG-reputation-risk", ["exposure", "media", "12315", "police", "reputation risk"]),
    ("TAG-safety-hazard", ["fire", "smoke", "self-ignite", "leak", "safety hazard"]),
    ("TAG-battery-swelling", ["swelling", "heat rise", "overheat", "bulging battery"]),
]

_FAULT_RULES: list[tuple[str, list[str]]] = [
    ("battery", ["battery", "range", "drain", "SOH"]),
    ("motor", ["motor", "noise", "speed limit"]),
    ("brake", ["brake"]),
    ("controller", ["controller"]),
    ("charging", ["charg"]),
    ("dashboard", ["dashboard", "blackout", "black screen"]),
]


def _suggest_tag(text: str) -> tuple[str, str]:
    low = text.lower()
    for tag_id, kws in _TAG_RULES:
        if any(k.lower() in low or k in text for k in kws):
            sentiment = "neg" if tag_id.startswith("TAG-") else "neu"
            if tag_id in {"TAG-open-complaint", "TAG-reputation-risk", "TAG-safety-hazard", "TAG-warranty-dispute"}:
                sentiment = "neg"
            return tag_id, sentiment
    return "TAG-short-range", "neu"


def _suggest_fault(text: str) -> str:
    for fault, kws in _FAULT_RULES:
        if any(k in text for k in kws):
            return fault
    return "other"


def _suggest_ticket_type(text: str) -> str:
    low = text.lower()
    if any(k in low for k in ("complaint", "exposure", "12315", "attitude")):
        return "complaint"
    if any(k in low for k in ("how", "what", "consult", "question", "ask")):
        return "consult"
    return "fault"


def build_tool_specs(fetcher: DataFetcher, store: SharedStore) -> list[ToolSpec]:
    """Build all ToolSpec entries (closure-bound fetcher/store)."""

    def get_customer(customer_id: str, **_: Any) -> dict[str, Any]:
        cid = guard_customer_id(customer_id)
        row = fetcher.get_customer(cid)  # type: ignore[arg-type]
        return {"customer": dump_model(row), "found": row is not None}

    def get_vehicle(vin: str, **_: Any) -> dict[str, Any]:
        v = guard_vin(vin)
        row = fetcher.get_vehicle(v)  # type: ignore[arg-type]
        return {"vehicle": dump_model(row), "found": row is not None}

    def list_vehicles(
        customer_id: str | None = None,
        model: str | None = None,
        limit: int = 20,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id) if customer_id else None
        rows = fetcher.list_vehicles(customer_id=cid, model=model, limit=clamp_limit(limit))
        return {"vehicles": dump_model(rows), "count": len(rows)}

    def get_dealer(dealer_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_dealer(str(dealer_id))
        return {"dealer": dump_model(row), "found": row is not None}

    def get_store(store_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_store(str(store_id))
        return {"store": dump_model(row), "found": row is not None}

    def list_stores(dealer_id: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_stores(dealer_id=dealer_id)
        return {"stores": dump_model(rows), "count": len(rows)}

    def get_sku(sku_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_sku(str(sku_id))
        return {"sku": dump_model(row), "found": row is not None}

    def get_org(org_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_org(str(org_id))
        return {"org": dump_model(row), "found": row is not None}

    def list_regions(**_: Any) -> dict[str, Any]:
        rows = fetcher.list_regions()
        return {"regions": dump_model(rows), "count": len(rows)}

    def get_order(order_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_order(str(order_id))
        return {"order": dump_model(row), "found": row is not None}

    def list_orders(
        dealer_id: str | None = None,
        store_id: str | None = None,
        sku_id: str | None = None,
        limit: int = 20,
        **_: Any,
    ) -> dict[str, Any]:
        rows = fetcher.list_orders(
            dealer_id=dealer_id,
            store_id=store_id,
            sku_id=sku_id,
            limit=clamp_limit(limit),
        )
        return {"orders": dump_model(rows), "count": len(rows)}

    def list_inventory(
        sku_id: str | None = None,
        store_id: str | None = None,
        dealer_id: str | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        rows = fetcher.list_inventory(sku_id=sku_id, store_id=store_id, dealer_id=dealer_id)
        return {"inventory": dump_model(rows), "count": len(rows)}

    def get_policy(dealer_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_policy(str(dealer_id))
        return {"policy": dump_model(row), "found": row is not None}

    def simulate_rebate_tier(
        dealer_id: str,
        extra_qty: int = 0,
        **_: Any,
    ) -> dict[str, Any]:
        """Policy sim: extra pickup units to next tier (demo rule table)."""
        policy = fetcher.get_policy(str(dealer_id))
        if not policy:
            return {"found": False, "message": "policy not found"}
        tiers = [
            ("Bronze", 300, 0.020),
            ("Silver", 800, 0.035),
            ("Gold", 1200, 0.042),
            ("Diamond", 1800, 0.050),
        ]
        current_qty = int(policy.current_pickup_qty_mtd or 0)
        sim_qty = current_qty + int(extra_qty)
        current_tier = "Below tier"
        current_rate = 0.0
        next_tier = None
        qty_to_next = None
        for name, thr, rate in tiers:
            if sim_qty >= thr:
                current_tier, current_rate = name, rate
        for name, thr, rate in tiers:
            if sim_qty < thr:
                next_tier = name
                qty_to_next = thr - sim_qty
                break
        predicted_rebate = round(sim_qty * 3299 * current_rate, 2)
        return {
            "found": True,
            "dealer_id": dealer_id,
            "current_pickup_qty_mtd": current_qty,
            "simulate_extra_qty": int(extra_qty),
            "simulated_qty": sim_qty,
            "current_tier_after_sim": current_tier,
            "rebate_rate": current_rate,
            "next_tier_name": next_tier,
            "qty_to_next_tier": qty_to_next,
            "predicted_rebate_amt": predicted_rebate,
            "policy_version": policy.policy_version,
        }

    def list_color_plans(week: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_color_plans(week=week)
        return {"color_plans": dump_model(rows), "count": len(rows)}

    def get_ticket(ticket_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_ticket(str(ticket_id))
        return {"ticket": dump_model(row), "found": row is not None}

    def list_tickets(
        customer_id: str | None = None,
        vin: str | None = None,
        ticket_status: str | None = None,
        tag_id: str | None = None,
        limit: int = 20,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id) if customer_id else None
        v = guard_vin(vin) if vin else None
        rows = fetcher.list_tickets(
            customer_id=cid,
            vin=v,
            ticket_status=ticket_status,
            tag_id=tag_id,
            limit=clamp_limit(limit),
        )
        return {"tickets": dump_model(rows), "count": len(rows)}

    def extract_ticket_fields(
        text: str,
        customer_id: str | None = None,
        vin: str | None = None,
        channel: str | None = "400",
        **_: Any,
    ) -> dict[str, Any]:
        body = guard_text(text)
        cid = guard_customer_id(customer_id) if customer_id else None
        v = guard_vin(vin) if vin else None
        # Try to extract QS0 VIN / CUS- id from text
        if not v:
            m = re.search(r"QS0[A-Z0-9]{14}", body.upper())
            if m:
                v = guard_vin(m.group(0))
        if not cid:
            m = re.search(r"CUS-\d+", body.upper())
            if m:
                cid = guard_customer_id(m.group(0))
        tag_id, sentiment = _suggest_tag(body)
        draft = {
            "customer_id": cid,
            "vin": v,
            "ticket_type": _suggest_ticket_type(body),
            "fault_category": _suggest_fault(body),
            "ticket_channel": channel or "400",
            "ticket_status": "open",
            "tag_id": tag_id,
            "sentiment": sentiment,
            "desc_text": body[:1000],
            "is_complaint": _suggest_ticket_type(body) == "complaint"
            or tag_id in BLOCKING_TAGS,
        }
        return {"ticket_draft": draft, "rule_based": True}

    def list_voc(
        customer_id: str | None = None,
        tag_id: str | None = None,
        limit: int = 20,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id) if customer_id else None
        rows = fetcher.list_voc(customer_id=cid, tag_id=tag_id, limit=clamp_limit(limit))
        return {"voc": dump_model(rows), "count": len(rows)}

    def suggest_voc_tags(text: str, **_: Any) -> dict[str, Any]:
        body = guard_text(text)
        tag_id, sentiment = _suggest_tag(body)
        tag = fetcher.get_tag(tag_id)
        return {
            "tag_id": tag_id,
            "sentiment": sentiment,
            "tag": dump_model(tag),
            "rule_based": True,
        }

    def get_renewal(
        customer_id: str,
        vin: str | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id)
        v = guard_vin(vin) if vin else None
        row = fetcher.get_renewal(cid, v)  # type: ignore[arg-type]
        return {"renewal": dump_model(row), "found": row is not None}

    def score_renewal(
        customer_id: str,
        vin: str | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id)
        v = guard_vin(vin) if vin else None
        renewal = fetcher.get_renewal(cid, v)  # type: ignore[arg-type]
        behavior = fetcher.get_user_behavior(cid, v)  # type: ignore[arg-type]
        if not renewal:
            return {"found": False, "score": 0.0, "intent_level": "low"}
        base = float(renewal.renew_intent_score or 0.3)
        if renewal.active_t7_flag:
            base += 0.15
        elif renewal.active_t30_flag:
            base += 0.08
        if renewal.sleep_90d_app_flag:
            base -= 0.12
        if behavior and behavior.rfm_segment and str(behavior.rfm_segment) == "high_value":
            base += 0.1
        score = max(0.0, min(0.99, round(base, 2)))
        level = "high" if score >= 0.7 else ("mid" if score >= 0.4 else "low")
        return {
            "found": True,
            "customer_id": cid,
            "vin": renewal.vin,
            "score": score,
            "intent_level": level,
            "renew_pool_layer": renewal.renew_pool_layer,
        }

    def route_renewal_pool(
        customer_id: str,
        vin: str | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id)
        v = guard_vin(vin) if vin else None
        renewal = fetcher.get_renewal(cid, v)  # type: ignore[arg-type]
        if not renewal:
            return {"found": False}
        layer = str(renewal.renew_pool_layer or "sleep")
        # Outreach ladder: Push → SMS → AI call → human
        channel_plan = {
            "T-7": ["push", "sms", "ai_call"],
            "T-30": ["push", "sms"],
            "sleep": ["push"],
            "non_smart": ["push"],
        }.get(layer, ["push"])
        return {
            "found": True,
            "customer_id": cid,
            "vin": renewal.vin,
            "renew_pool_layer": layer,
            "channel_plan": channel_plan,
            "max_touches_per_day": 3,
            "note": "Non-smart vehicles excluded from renewal denominator; check blocking tags before outreach",
        }

    def check_outreach_block(
        customer_id: str,
        vin: str | None = None,
        consumer_skill: str = "renewal_plan",
        **_: Any,
    ) -> dict[str, Any]:
        """Story2 key: shared layer has tags that should block outreach."""
        cid = guard_customer_id(customer_id)
        v = guard_vin(vin) if vin else None
        blocked, tags = store.has_blocking_tag(
            customer_id=cid,
            vin=v,
            consumer_skill=consumer_skill,
        )
        reason = None
        if blocked:
            reason = "Blocking tags present: " + ", ".join(tags)
        return {
            "customer_id": cid,
            "vin": v,
            "allow_outreach": not blocked,
            "blocked": blocked,
            "blocking_tags": tags,
            "block_reason": reason,
        }

    def get_user_behavior(
        customer_id: str,
        vin: str | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id)
        v = guard_vin(vin) if vin else None
        row = fetcher.get_user_behavior(cid, v)  # type: ignore[arg-type]
        return {"user_behavior": dump_model(row), "found": row is not None}

    def _assert_kb_domain_allowed(
        domain: str | None,
        _context: ToolContext | None,
        *,
        tool_name: str,
    ) -> str | None:
        """Skill-level KB domain gate (prevent search leak / get_kb_document bypass)."""
        allow = list(_context.kb_domains_allow) if _context and _context.kb_domains_allow else []
        d = guard_kb_domain(domain)
        if not allow:
            return d
        if d is None:
            if len(allow) == 1:
                return allow[0]
            from shared.tools.base import ToolError

            raise ToolError(
                f"{tool_name}: domain required; allowed={allow}",
                code="KB_DOMAIN_REQUIRED",
            )
        if d not in allow:
            from shared.tools.base import ToolError

            raise ToolError(
                f"{tool_name}: domain={d} not in allowed={allow}",
                code="KB_DOMAIN_DENIED",
            )
        return d

    def search_kb(
        query: str,
        domain: str | None = None,
        top_k: int = 5,
        _context: ToolContext | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        q = guard_text(query, field="query")
        d = _assert_kb_domain_allowed(domain, _context, tool_name="search_kb")
        k = clamp_limit(top_k, default=5)
        hits = fetcher.search_kb(q, domain=d, top_k=min(k, 10))
        # Belt-and-suspenders: filter by allow even if backend ignores domain
        allow = list(_context.kb_domains_allow) if _context and _context.kb_domains_allow else []
        if allow:
            filtered = []
            for h in hits:
                hd = getattr(h, "kb_domain", None)
                if hd is None and isinstance(h, dict):
                    hd = h.get("kb_domain")
                if hd in allow:
                    filtered.append(h)
            hits = filtered
        return {"hits": dump_model(hits), "count": len(hits), "domain": d}

    def get_kb_document(
        kb_doc_id: str,
        _context: ToolContext | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        row = fetcher.get_kb_document(str(kb_doc_id))
        if row is not None and _context and _context.kb_domains_allow:
            domain = getattr(row, "kb_domain", None)
            if domain is None and isinstance(row, dict):
                domain = row.get("kb_domain")
            _assert_kb_domain_allowed(
                str(domain) if domain else None,
                _context,
                tool_name="get_kb_document",
            )
        return {"document": dump_model(row), "found": row is not None}

    def list_kb_domains(_context: ToolContext | None = None, **_: Any) -> dict[str, Any]:
        domains = fetcher.list_kb_domains()
        allow = list(_context.kb_domains_allow) if _context and _context.kb_domains_allow else []
        if allow:
            domains = [d for d in domains if d in allow]
        return {"domains": domains}

    def write_ai_output(
        producer_skill: str,
        payload: dict[str, Any] | list[Any],
        consumer_allow: list[str] | None = None,
        run_id: str | None = None,
        payload_schema: str | None = None,
        _context: ToolContext | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        skill = guard_text(producer_skill, field="producer_skill")
        # Guard: context skill must match producer to prevent cross-skill impersonation writes
        if _context and _context.skill_id and _context.skill_id != skill:
            from shared.tools.base import ToolError

            raise ToolError(
                f"producer_skill must match context.skill_id={_context.skill_id}",
                code="PRODUCER_MISMATCH",
            )
        body = guard_payload(payload)
        allow = list(consumer_allow or [])
        if isinstance(body, dict):
            # Normalize correlation keys
            if body.get("vin"):
                body["vin"] = guard_vin(str(body["vin"]))
            if body.get("customer_id"):
                body["customer_id"] = guard_customer_id(str(body["customer_id"]))
        rid = run_id or (_context.run_id if _context else None)
        out = store.write_ai_output(
            producer_skill=skill,
            payload=body,
            consumer_allow=allow,
            run_id=rid,
            payload_schema=payload_schema,
        )
        return {"ai_output": dump_model(out)}

    def read_ai_outputs(
        consumer_skill: str | None = None,
        producer_skill: str | None = None,
        customer_id: str | None = None,
        vin: str | None = None,
        tag_id: str | None = None,
        run_id: str | None = None,
        limit: int = 20,
        _context: ToolContext | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id) if customer_id else None
        v = guard_vin(vin) if vin else None
        consumer = consumer_skill or (_context.skill_id if _context else None)
        rows = store.read_ai_outputs(
            consumer_skill=consumer,
            producer_skill=producer_skill,
            customer_id=cid,
            vin=v,
            tag_id=tag_id,
            run_id=run_id,
            limit=clamp_limit(limit),
        )
        return {"ai_outputs": dump_model(rows), "count": len(rows)}

    def read_shared_tags(
        customer_id: str | None = None,
        vin: str | None = None,
        consumer_skill: str | None = None,
        _context: ToolContext | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        cid = guard_customer_id(customer_id) if customer_id else None
        v = guard_vin(vin) if vin else None
        consumer = consumer_skill or (_context.skill_id if _context else None)
        tags = store.read_shared_tags(
            consumer_skill=consumer,
            customer_id=cid,
            vin=v,
        )
        return {"tags": tags, "count": len(tags)}

    def get_ai_output(ai_output_id: str, **_: Any) -> dict[str, Any]:
        row = store.get_ai_output(str(ai_output_id))
        return {"ai_output": dump_model(row), "found": row is not None}

    def list_capabilities(**_: Any) -> dict[str, Any]:
        rows = fetcher.list_capabilities()
        return {"capabilities": dump_model(rows), "count": len(rows)}

    def get_capability(skill_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_capability(str(skill_id))
        return {"capability": dump_model(row), "found": row is not None}

    def get_tag(tag_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_tag(str(tag_id))
        return {"tag": dump_model(row), "found": row is not None}

    def list_tags(domain: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_tags(domain=domain)
        return {"tags": dump_model(rows), "count": len(rows)}

    def log_step(
        step_name: str,
        run_id: str | None = None,
        step_status: str = "ok",
        detail: dict[str, Any] | None = None,
        _context: ToolContext | None = None,
        **_: Any,
    ) -> dict[str, Any]:
        name = guard_text(step_name, field="step_name")
        rid = run_id or (_context.run_id if _context else None)
        if not rid:
            from shared.tools.base import ToolError

            raise ToolError("run_id is required (arg or context)", code="MISSING_RUN_ID")
        status = StepStatus(step_status) if step_status in {s.value for s in StepStatus} else StepStatus.OK
        entry = store.log_step(
            run_id=rid,
            step_name=name,
            step_status=status,
            detail=detail if isinstance(detail, dict) or detail is None else {"value": detail},
        )
        return {"run_log": dump_model(entry)}

    def list_run_logs(run_id: str | None = None, **_: Any) -> dict[str, Any]:
        rows = store.list_run_logs(run_id=run_id)
        return {"run_logs": dump_model(rows), "count": len(rows)}

    def get_dealer_health(dealer_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_dealer_health(str(dealer_id))
        return {"health": dump_model(row), "found": row is not None}

    def list_alerts(dealer_id: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_alerts(dealer_id=dealer_id)
        return {"alerts": dump_model(rows), "count": len(rows)}

    def list_sales_metrics(org_id: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_sales_metrics(org_id=org_id)
        return {"sales_metrics": dump_model(rows), "count": len(rows)}

    def list_retail_daily(store_id: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_retail_daily(store_id=store_id)
        return {"retail_daily": dump_model(rows), "count": len(rows)}

    def list_inspections(store_id: str | None = None, **_: Any) -> dict[str, Any]:
        rows = fetcher.list_inspections(store_id=store_id)
        return {"inspections": dump_model(rows), "count": len(rows)}

    def get_risk(dealer_id: str, **_: Any) -> dict[str, Any]:
        row = fetcher.get_risk(str(dealer_id))
        return {"risk": dump_model(row), "found": row is not None}

    def list_campaigns(**_: Any) -> dict[str, Any]:
        rows = fetcher.list_campaigns()
        return {"campaigns": dump_model(rows), "count": len(rows)}

    def get_telemetry(vin: str, **_: Any) -> dict[str, Any]:
        v = guard_vin(vin)
        row = fetcher.get_telemetry(v)  # type: ignore[arg-type]
        return {"telemetry": dump_model(row), "found": row is not None}

    def list_quality_checks(vin: str | None = None, **_: Any) -> dict[str, Any]:
        v = guard_vin(vin) if vin else None
        rows = fetcher.list_quality_checks(vin=v)
        return {"quality_checks": dump_model(rows), "count": len(rows)}

    def list_competitors(**_: Any) -> dict[str, Any]:
        rows = fetcher.list_competitors()
        return {"competitors": dump_model(rows), "count": len(rows)}

    # ---- register specs ----
    def p(props: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": props,
            "required": required or [],
            "additionalProperties": False,
        }

    S = ToolSpec
    return [
        # Master data
        S("get_customer", "Look up customer master record", p({"customer_id": {"type": "string"}}, ["customer_id"]), get_customer, True, "master", ["customer_id"]),
        S("get_vehicle", "Look up vehicle (VIN must be QS0 synthetic id)", p({"vin": {"type": "string"}}, ["vin"]), get_vehicle, True, "master", ["vin"]),
        S("list_vehicles", "List vehicles by customer or model", p({"customer_id": {"type": "string"}, "model": {"type": "string"}, "limit": {"type": "integer"}}), list_vehicles, True, "master"),
        S("get_dealer", "Look up tier-1 dealer", p({"dealer_id": {"type": "string"}}, ["dealer_id"]), get_dealer, True, "master", ["dealer_id"]),
        S("get_store", "Look up store", p({"store_id": {"type": "string"}}, ["store_id"]), get_store, True, "master", ["store_id"]),
        S("list_stores", "List stores", p({"dealer_id": {"type": "string"}}), list_stores, True, "master"),
        S("get_sku", "Look up SKU", p({"sku_id": {"type": "string"}}, ["sku_id"]), get_sku, True, "master", ["sku_id"]),
        S("get_org", "Look up org node", p({"org_id": {"type": "string"}}, ["org_id"]), get_org, True, "master", ["org_id"]),
        S("list_regions", "List administrative regions", p({}), list_regions, True, "master"),
        S("list_competitors", "List competitor snapshots (fictional brands)", p({}), list_competitors, True, "master"),
        # Commerce
        S("get_order", "Look up order", p({"order_id": {"type": "string"}}, ["order_id"]), get_order, True, "commerce", ["order_id"]),
        S("list_orders", "Filter order list", p({"dealer_id": {"type": "string"}, "store_id": {"type": "string"}, "sku_id": {"type": "string"}, "limit": {"type": "integer"}}), list_orders, True, "commerce"),
        S("list_inventory", "Look up inventory", p({"sku_id": {"type": "string"}, "store_id": {"type": "string"}, "dealer_id": {"type": "string"}}), list_inventory, True, "commerce"),
        S("get_policy", "Look up dealer rebate policy summary", p({"dealer_id": {"type": "string"}}, ["dealer_id"]), get_policy, True, "commerce", ["dealer_id"]),
        S("simulate_rebate_tier", "Simulate extra pickup tier rebate", p({"dealer_id": {"type": "string"}, "extra_qty": {"type": "integer"}}, ["dealer_id"]), simulate_rebate_tier, True, "commerce", ["dealer_id"]),
        S("list_color_plans", "Look up color production plan", p({"week": {"type": "string"}}), list_color_plans, True, "commerce"),
        # Service / VoC
        S("get_ticket", "Look up ticket", p({"ticket_id": {"type": "string"}}, ["ticket_id"]), get_ticket, True, "service", ["ticket_id"]),
        S("list_tickets", "Filter tickets", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}, "ticket_status": {"type": "string"}, "tag_id": {"type": "string"}, "limit": {"type": "integer"}}), list_tickets, True, "service"),
        S("extract_ticket_fields", "[ReAct rule tool] Extract ticket draft fields from text; parallel Extraction Agent uses skill ticket_fields (POST /v1/extraction/runs)", p({"text": {"type": "string"}, "customer_id": {"type": "string"}, "vin": {"type": "string"}, "channel": {"type": "string"}}, ["text"]), extract_ticket_fields, True, "service", ["text"]),
        S("list_voc", "Query VoC feedback slice", p({"customer_id": {"type": "string"}, "tag_id": {"type": "string"}, "limit": {"type": "integer"}}), list_voc, True, "service"),
        S("suggest_voc_tags", "Suggest VoC tags and sentiment (rules)", p({"text": {"type": "string"}}, ["text"]), suggest_voc_tags, True, "service", ["text"]),
        # Renewal
        S("get_renewal", "Look up renewal pool record", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}}, ["customer_id"]), get_renewal, True, "renewal", ["customer_id"]),
        S("score_renewal", "Score renewal intent", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}}, ["customer_id"]), score_renewal, True, "renewal", ["customer_id"]),
        S("route_renewal_pool", "Renewal pool routing and outreach ladder", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}}, ["customer_id"]), route_renewal_pool, True, "renewal", ["customer_id"]),
        S("check_outreach_block", "Check shared tags for outreach block (Story2)", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}, "consumer_skill": {"type": "string"}}, ["customer_id"]), check_outreach_block, True, "renewal", ["customer_id"]),
        S("get_user_behavior", "Look up user behavior / RFM", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}}, ["customer_id"]), get_user_behavior, True, "renewal", ["customer_id"]),
        # Knowledge base
        S("search_kb", "Search knowledge base", p({"query": {"type": "string"}, "domain": {"type": "string"}, "top_k": {"type": "integer"}}, ["query"]), search_kb, True, "knowledge", ["query"]),
        S("get_kb_document", "Fetch full KB document", p({"kb_doc_id": {"type": "string"}}, ["kb_doc_id"]), get_kb_document, True, "knowledge", ["kb_doc_id"]),
        S("list_kb_domains", "List KB domains", p({}), list_kb_domains, True, "knowledge"),
        # Shared layer
        S("write_ai_output", "Write shared AI output (asset)", p({"producer_skill": {"type": "string"}, "payload": {"type": "object"}, "consumer_allow": {"type": "array"}, "run_id": {"type": "string"}, "payload_schema": {"type": "string"}}, ["producer_skill", "payload"]), write_ai_output, False, "shared", ["producer_skill", "payload"]),
        S("read_ai_outputs", "Read shared AI outputs", p({"consumer_skill": {"type": "string"}, "producer_skill": {"type": "string"}, "customer_id": {"type": "string"}, "vin": {"type": "string"}, "tag_id": {"type": "string"}, "run_id": {"type": "string"}, "limit": {"type": "integer"}}), read_ai_outputs, True, "shared"),
        S("read_shared_tags", "Read shared tag projection", p({"customer_id": {"type": "string"}, "vin": {"type": "string"}, "consumer_skill": {"type": "string"}}), read_shared_tags, True, "shared"),
        S("get_ai_output", "Get AI output by id", p({"ai_output_id": {"type": "string"}}, ["ai_output_id"]), get_ai_output, True, "shared", ["ai_output_id"]),
        S("list_capabilities", "List skill capability catalog", p({}), list_capabilities, True, "shared"),
        S("get_capability", "Look up single skill capability", p({"skill_id": {"type": "string"}}, ["skill_id"]), get_capability, True, "shared", ["skill_id"]),
        S("get_tag", "Look up tag vocabulary entry", p({"tag_id": {"type": "string"}}, ["tag_id"]), get_tag, True, "shared", ["tag_id"]),
        S("list_tags", "List tags", p({"domain": {"type": "string"}}), list_tags, True, "shared"),
        S("log_step", "Log run step", p({"step_name": {"type": "string"}, "run_id": {"type": "string"}, "step_status": {"type": "string"}, "detail": {"type": "object"}}, ["step_name"]), log_step, False, "shared", ["step_name"]),
        S("list_run_logs", "List run step logs", p({"run_id": {"type": "string"}}), list_run_logs, True, "shared"),
        # Channel ops / QC / IoT
        S("get_dealer_health", "Tier-1 dealer health index", p({"dealer_id": {"type": "string"}}, ["dealer_id"]), get_dealer_health, True, "channel", ["dealer_id"]),
        S("list_alerts", "Business alert list", p({"dealer_id": {"type": "string"}}), list_alerts, True, "channel"),
        S("list_sales_metrics", "Sales attainment metrics", p({"org_id": {"type": "string"}}), list_sales_metrics, True, "channel"),
        S("list_retail_daily", "Store retail daily slice", p({"store_id": {"type": "string"}}), list_retail_daily, True, "channel"),
        S("list_inspections", "Store inspection records", p({"store_id": {"type": "string"}}), list_inspections, True, "channel"),
        S("get_risk", "Franchise / partner risk summary", p({"dealer_id": {"type": "string"}}, ["dealer_id"]), get_risk, True, "channel", ["dealer_id"]),
        S("list_campaigns", "Marketing campaign list", p({}), list_campaigns, True, "channel"),
        S("get_telemetry", "Vehicle IoT telemetry / alerts", p({"vin": {"type": "string"}}, ["vin"]), get_telemetry, True, "iot", ["vin"]),
        S("list_quality_checks", "Quality inspection records", p({"vin": {"type": "string"}}), list_quality_checks, True, "iot"),
    ]
