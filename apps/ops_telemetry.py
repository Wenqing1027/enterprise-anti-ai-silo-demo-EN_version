"""： · · / · · （Demo ）。 SharedStore run_logs / ai_outputs ； ， 「 ↔ ↔ 」。"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from apps.loops import LOOP_META, PLATFORM_LOOPS, canonicalize, display_name
from apps.skill_loops import control_loop_for_skill
from shared.store.store import SharedStore, default_store
from shared.tools.registry import ToolRegistry, default_registry

_UTC = timezone.utc


def _parse_ts(val: Any) -> datetime | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val if val.tzinfo else val.replace(tzinfo=_UTC)
    s = str(val).strip()
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def _infer_loop(run_id: str | None, skill_id: str | None) -> str | None:
    if skill_id:
        loop = control_loop_for_skill(skill_id)
        if loop:
            return loop
    rid = (run_id or "").lower()
    for prefix, loop in (
        ("rag-", "retrieve"),
        ("retrieve-", "retrieve"),
        ("react-", "act"),
        ("act-", "act"),
        ("extract-", "extract"),
        ("ext-", "extract"),
        ("plan-", "plan"),
        ("planning-", "plan"),
    ):
        if rid.startswith(prefix):
            return loop
    return None


def _bucket_key(ts: datetime, minutes: int = 5) -> datetime:
    discard = timedelta(
        minutes=ts.minute % minutes,
        seconds=ts.second,
        microseconds=ts.microsecond,
    )
    return ts - discard


def _synthetic_series(
    *,
    seed: str,
    points: int = 24,
    base: float,
    noise: float,
    dip_at: int | None = None,
    dip_depth: float = 0.25,
) -> list[dict[str, Any]]:
    """（ ）， Demo 。"""
    now = datetime.now(_UTC).replace(second=0, microsecond=0)
    out: list[dict[str, Any]] = []
    for i in range(points):
        ts = now - timedelta(minutes=5 * (points - 1 - i))
        h = hashlib.md5(f"{seed}:{i}".encode()).hexdigest()
        n = (int(h[:8], 16) % 1000) / 1000.0  # 0..1
        v = base + (n - 0.5) * 2 * noise
        if dip_at is not None and abs(i - dip_at) <= 1:
            v = v * (1.0 - dip_depth)
        out.append({"ts": ts.isoformat().replace("+00:00", "Z"), "value": round(max(0.0, v), 3)})
    return out


def _build_run_index(logs: list[Any]) -> dict[str, dict[str, Any]]:
    by_run: dict[str, dict[str, Any]] = {}
    for x in logs:
        rid = getattr(x, "run_id", None)
        if not rid:
            continue
        detail = x.detail if isinstance(getattr(x, "detail", None), dict) else {}
        skill = detail.get("skill_id")
        loop = _infer_loop(rid, skill if isinstance(skill, str) else None)
        row = by_run.setdefault(
            rid,
            {
                "run_id": rid,
                "control_loop": loop,
                "skills": set(),
                "steps": [],
                "errors": 0,
                "blocked": False,
                "stop_reason": None,
                "first_dt": None,
                "last_dt": None,
            },
        )
        if skill:
            row["skills"].add(str(skill))
        if loop and not row["control_loop"]:
            row["control_loop"] = loop
        st = str(getattr(x, "step_status", "")).lower()
        if st in {"error", "fail", "failed"}:
            row["errors"] += 1
        if detail.get("blocked") is True:
            row["blocked"] = True
        if detail.get("stop_reason"):
            row["stop_reason"] = detail.get("stop_reason")
        ts = getattr(x, "step_ts", None)
        ts_dt = ts if isinstance(ts, datetime) else _parse_ts(ts)
        step = {
            "step_name": getattr(x, "step_name", None),
            "step_status": str(getattr(x, "step_status", "")),
            "step_ts": ts_dt.isoformat().replace("+00:00", "Z") if ts_dt else None,
            "detail": detail,
            "control_loop": loop,
        }
        row["steps"].append(step)
        if ts_dt:
            if row["first_dt"] is None or ts_dt < row["first_dt"]:
                row["first_dt"] = ts_dt
            if row["last_dt"] is None or ts_dt > row["last_dt"]:
                row["last_dt"] = ts_dt
    for rid, row in by_run.items():
        row["skills"] = sorted(row["skills"])
        t0, t1 = row.pop("first_dt", None), row.pop("last_dt", None)
        row["first_ts"] = t0.isoformat().replace("+00:00", "Z") if t0 else None
        row["last_ts"] = t1.isoformat().replace("+00:00", "Z") if t1 else None
        if t0 and t1:
            row["duration_ms"] = max(0, int((t1 - t0).total_seconds() * 1000))
        else:
            row["duration_ms"] = 800 + (abs(hash(rid)) % 2200)
        if not row["control_loop"] and row["skills"]:
            row["control_loop"] = control_loop_for_skill(row["skills"][0])
        row["ok"] = row["errors"] == 0
        if row["blocked"] and row["errors"] == 0:
            row["ok"] = True
    return by_run


def build_call_chain(run: dict[str, Any]) -> dict[str, Any]:
    """run （ → Skill → step ）。"""
    loop = run.get("control_loop")
    steps = run.get("steps") or []
    nodes: list[dict[str, Any]] = [
        {
            "id": "entry",
            "label": f"· {display_name(loop) if loop else 'run'}",
            "kind": "entry",
        }
    ]
    ids = ["entry"]
    if run.get("skills"):
        nodes.append(
            {
                "id": "skill",
                "label": "Skill · " + ",".join(run["skills"]),
                "kind": "skill",
            }
        )
        ids.append("skill")
    for i, s in enumerate(steps):
        nid = f"s{i}"
        detail = s.get("detail") or {}
        tool = detail.get("tool") or s.get("step_name") or detail.get("phase") or f"step_{i}"
        nodes.append(
            {
                "id": nid,
                "label": str(tool),
                "kind": "step",
                "status": s.get("step_status"),
                "ts": s.get("step_ts"),
                "detail": {
                    k: detail[k]
                    for k in ("tool", "error", "error_code", "latency_ms", "message")
                    if k in detail
                }
                or None,
            }
        )
        ids.append(nid)
    edges = [{"from": a, "to": b} for a, b in zip(ids, ids[1:])]
    severity = "ok"
    if run.get("errors") or run.get("ok") is False:
        severity = "error"
    elif run.get("slow") or (run.get("duration_ms") or 0) >= 5000:
        severity = "slow"
    elif run.get("blocked"):
        severity = "blocked"
    return {
        "run_id": run.get("run_id"),
        "control_loop": loop,
        "duration_ms": run.get("duration_ms"),
        "ok": run.get("ok"),
        "blocked": run.get("blocked"),
        "slow": bool(run.get("slow")),
        "severity": severity,
        "demo": bool(run.get("demo")),
        "nodes": nodes,
        "edges": edges,
    }


# Demo ： run_logs 「 / 」
DEMO_ERR_RUN_ID = "demo-err-write-govern"
DEMO_SLOW_RUN_ID = "demo-slow-retrieve"


def _fmt_clock(ts: str | None) -> str:
    if not ts:
        return "—"
    return str(ts).replace("T", " ").replace("Z", "")[:16]


def _detect_highlight(
    signals: dict[str, list[dict[str, Any]]],
) -> tuple[str | None, int | None, str]:
    """(highlight_ts, anomaly_idx, reason)。"""
    err_series = signals.get("error_count") or []
    sr_series = signals.get("success_rate") or []
    for i, p in enumerate(err_series):
        if p["value"] >= 2.5:
            return p["ts"], i, "error_spike"
    for i, p in enumerate(sr_series):
        if p["value"] < 85:
            return p["ts"], i, "success_drop"
    if err_series:
        anomaly_idx = max(range(len(err_series)), key=lambda i: err_series[i]["value"])
        if err_series[anomaly_idx]["value"] >= 1.0:
            return err_series[anomaly_idx]["ts"], anomaly_idx, "error_peak"
    return None, None, "none"


def build_demo_incident_runs(*, highlight_ts: str | None = None) -> dict[str, dict[str, Any]]:
    """/ （ ， detail ）。"""
    ht = _parse_ts(highlight_ts) or datetime.now(_UTC)
    t_err = ht
    t_slow = ht - timedelta(minutes=2)
    err_run = {
        "run_id": DEMO_ERR_RUN_ID,
        "control_loop": "retrieve",
        "skills": ["policy_kb"],
        "errors": 1,
        "blocked": False,
        "ok": False,
        "slow": False,
        "demo": True,
        "stop_reason": "tool_error",
        "duration_ms": 4210,
        "first_ts": (t_err - timedelta(seconds=4)).isoformat().replace("+00:00", "Z"),
        "last_ts": t_err.isoformat().replace("+00:00", "Z"),
        "steps": [
            {
                "step_name": "rag_start",
                "step_status": "ok",
                "step_ts": (t_err - timedelta(seconds=4)).isoformat().replace("+00:00", "Z"),
                "detail": {"skill_id": "policy_kb", "phase": "start"},
                "control_loop": "retrieve",
            },
            {
                "step_name": "tool_call",
                "step_status": "error",
                "step_ts": (t_err - timedelta(seconds=1)).isoformat().replace("+00:00", "Z"),
                "detail": {
                    "tool": "write_govern",
                    "error_code": "TIMEOUT",
                    "error": "connection pool exhausted / downstream timeout",
                    "latency_ms": 3001,
                    "message": "write_govern ",
                },
                "control_loop": "retrieve",
            },
            {
                "step_name": "rag_done",
                "step_status": "error",
                "step_ts": t_err.isoformat().replace("+00:00", "Z"),
                "detail": {"stop": "tool_error", "tool": "write_govern"},
                "control_loop": "retrieve",
            },
        ],
    }
    slow_run = {
        "run_id": DEMO_SLOW_RUN_ID,
        "control_loop": "retrieve",
        "skills": ["hr_rules"],
        "errors": 0,
        "blocked": False,
        "ok": True,
        "slow": True,
        "demo": True,
        "stop_reason": None,
        "duration_ms": 8120,
        "first_ts": (t_slow - timedelta(seconds=8)).isoformat().replace("+00:00", "Z"),
        "last_ts": t_slow.isoformat().replace("+00:00", "Z"),
        "steps": [
            {
                "step_name": "rag_start",
                "step_status": "ok",
                "step_ts": (t_slow - timedelta(seconds=8)).isoformat().replace("+00:00", "Z"),
                "detail": {"skill_id": "hr_rules", "phase": "start"},
                "control_loop": "retrieve",
            },
            {
                "step_name": "tool_call",
                "step_status": "warn",
                "step_ts": (t_slow - timedelta(seconds=1)).isoformat().replace("+00:00", "Z"),
                "detail": {
                    "tool": "write_govern",
                    "latency_ms": 7800,
                    "message": "：",
                },
                "control_loop": "retrieve",
            },
            {
                "step_name": "rag_done",
                "step_status": "ok",
                "step_ts": t_slow.isoformat().replace("+00:00", "Z"),
                "detail": {"stop": "ok", "tool": "write_govern"},
                "control_loop": "retrieve",
            },
        ],
    }
    return {DEMO_ERR_RUN_ID: err_run, DEMO_SLOW_RUN_ID: slow_run}


def _merge_demo_incidents(
    runs: dict[str, dict[str, Any]],
    *,
    highlight_ts: str | None,
) -> dict[str, dict[str, Any]]:
    """error/slow， Demo ， 。"""
    has_fail = any((r.get("errors") or r.get("ok") is False) for r in runs.values())
    has_slow = any((r.get("duration_ms") or 0) >= 5000 for r in runs.values())
    demo = build_demo_incident_runs(highlight_ts=highlight_ts)
    out = dict(runs)
    if not has_fail:
        out[DEMO_ERR_RUN_ID] = demo[DEMO_ERR_RUN_ID]
    if not has_slow:
        out[DEMO_SLOW_RUN_ID] = demo[DEMO_SLOW_RUN_ID]
    return out


def _sr_delta_around(sr_series: list[dict[str, Any]], anomaly_idx: int | None) -> float | None:
    if anomaly_idx is None or not sr_series:
        return None
    base_vals = [p["value"] for i, p in enumerate(sr_series) if abs(i - anomaly_idx) > 2]
    if not base_vals:
        return None
    base = sum(base_vals) / len(base_vals)
    return round(base - sr_series[anomaly_idx]["value"], 1)


def _golden_from_runs(
    runs: dict[str, dict[str, Any]],
    *,
    loop: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """5 run； 。"""
    filtered = [
        r
        for r in runs.values()
        if loop is None or r.get("control_loop") == loop
    ]
    buckets: dict[datetime, dict[str, float]] = defaultdict(
        lambda: {"ok": 0, "total": 0, "rt_sum": 0.0, "errors": 0}
    )
    for r in filtered:
        ts = _parse_ts(r.get("last_ts") or r.get("first_ts"))
        if not ts:
            continue
        b = _bucket_key(ts)
        buckets[b]["total"] += 1
        buckets[b]["rt_sum"] += float(r.get("duration_ms") or 0)
        if r.get("errors"):
            buckets[b]["errors"] += r["errors"]
        if r.get("ok"):
            buckets[b]["ok"] += 1

    points = 24
    seed = f"loop:{loop or 'all'}"
    # ， （ dip）
    if len(buckets) < 4:
        dip = 16
        success = _synthetic_series(seed=seed + ":s", points=points, base=0.96, noise=0.03, dip_at=dip, dip_depth=0.18)
        
        for p in success:
            p["value"] = round(min(100.0, max(0.0, p["value"] * 100)), 2)
        rt = _synthetic_series(seed=seed + ":rt", points=points, base=420, noise=80, dip_at=dip, dip_depth=-0.55)
        # dip_depth （ RT ）— ： dip
        for i, p in enumerate(rt):
            if abs(i - dip) <= 1:
                p["value"] = round(p["value"] * 1.8, 2)
        throughput = _synthetic_series(seed=seed + ":tp", points=points, base=8.5, noise=2.0, dip_at=dip, dip_depth=0.35)
        errors = _synthetic_series(seed=seed + ":e", points=points, base=0.4, noise=0.3, dip_at=dip, dip_depth=-2.5)
        for i, p in enumerate(errors):
            if abs(i - dip) <= 1:
                p["value"] = round(max(p["value"], 3.0 + i % 2), 2)
            else:
                p["value"] = round(max(0.0, p["value"]), 2)
        return {
            "success_rate": success,
            "latency_ms": rt,
            "throughput": throughput,
            "error_count": errors,
        }

    # → points
    now = datetime.now(_UTC).replace(second=0, microsecond=0)
    success, rt, tp, err = [], [], [], []
    for i in range(points):
        ts = now - timedelta(minutes=5 * (points - 1 - i))
        b = _bucket_key(ts)
        cell = buckets.get(b)
        if not cell or cell["total"] == 0:
            
            h = hashlib.md5(f"{seed}:{i}".encode()).hexdigest()
            n = (int(h[:6], 16) % 100) / 100.0
            success.append({"ts": ts.isoformat().replace("+00:00", "Z"), "value": round(94 + n * 5, 2)})
            rt.append({"ts": ts.isoformat().replace("+00:00", "Z"), "value": round(300 + n * 200, 2)})
            tp.append({"ts": ts.isoformat().replace("+00:00", "Z"), "value": round(5 + n * 6, 2)})
            err.append({"ts": ts.isoformat().replace("+00:00", "Z"), "value": round(n * 1.5, 2)})
        else:
            rate = 100.0 * cell["ok"] / cell["total"]
            success.append({"ts": b.isoformat().replace("+00:00", "Z"), "value": round(rate, 2)})
            rt.append(
                {
                    "ts": b.isoformat().replace("+00:00", "Z"),
                    "value": round(cell["rt_sum"] / cell["total"], 2),
                }
            )
            tp.append({"ts": b.isoformat().replace("+00:00", "Z"), "value": float(cell["total"])})
            err.append({"ts": b.isoformat().replace("+00:00", "Z"), "value": float(cell["errors"])})
    return {
        "success_rate": success,
        "latency_ms": rt,
        "throughput": tp,
        "error_count": err,
    }


def _health_score(signals: dict[str, list[dict[str, Any]]], *, blocked: int, errors: int) -> dict[str, Any]:
    sr = signals["success_rate"][-1]["value"] if signals["success_rate"] else 95.0
    lat = signals["latency_ms"][-1]["value"] if signals["latency_ms"] else 400.0
    errs = signals["error_count"][-1]["value"] if signals["error_count"] else 0.0
    
    score = sr
    if lat > 800:
        score -= min(15, (lat - 800) / 80)
    if errs > 1:
        score -= min(20, errs * 4)
    if errors:
        score -= min(10, errors * 2)
    score = round(max(0.0, min(100.0, score)), 1)
    level = "excellent" if score >= 95 else "good" if score >= 85 else "degraded" if score >= 70 else "critical"
    return {"score": score, "level": level, "success_rate_now": sr, "latency_ms_now": lat, "errors_now": errs}


def _events_and_rca(
    signals: dict[str, list[dict[str, Any]]],
    runs: dict[str, dict[str, Any]],
    *,
    loop: str | None = None,
    highlight_ts: str | None = None,
    anomaly_idx: int | None = None,
    anomaly_reason: str = "none",
) -> tuple[list[dict[str, Any]], dict[str, Any], str | None]:
    """Based on + + run 「 / 」 。"""
    err_series = signals.get("error_count") or []
    sr_series = signals.get("success_rate") or []
    if highlight_ts is None:
        highlight_ts, anomaly_idx, anomaly_reason = _detect_highlight(signals)

    sr_drop = _sr_delta_around(sr_series, anomaly_idx)
    err_at = None
    if anomaly_idx is not None and err_series and anomaly_idx < len(err_series):
        err_at = err_series[anomaly_idx]["value"]

    impact_loop = loop or "retrieve"
    impact_effect = (
        f"{display_name(impact_loop)} {abs(sr_drop)}%"
        if sr_drop and sr_drop > 0
        else f"{display_name(impact_loop)}"
        + (f"（ {err_at}）" if err_at is not None else "")
    )

    now = datetime.now(_UTC)
    deploy_ts = (
        ((_parse_ts(highlight_ts) or now) - timedelta(minutes=3)).isoformat().replace("+00:00", "Z")
        if highlight_ts
        else (now - timedelta(minutes=95)).isoformat().replace("+00:00", "Z")
    )
    ledger_ts = (now - timedelta(minutes=95)).isoformat().replace("+00:00", "Z")

    events: list[dict[str, Any]] = [
        {
            "ts": ledger_ts,
            "kind": "deploy",
            "title": " v2 ",
            "detail": "write_govern ",
            "loop": loop,
            "correlate": bool(highlight_ts),
            "impact_scope": "write_govern",
            "impact": impact_effect if highlight_ts else "",
            "impact_level": "warn" if highlight_ts else "info",
        },
        {
            "ts": (now - timedelta(minutes=48)).isoformat().replace("+00:00", "Z"),
            "kind": "config",
            "title": "Skill allowlist updated",
            "detail": "fill_ticket / renewal_plan consumer_allow",
            "loop": loop,
            "correlate": False,
            "impact_scope": "renewal_plan",
            "impact": "Plan （）",
            "impact_level": "info",
        },
    ]
    if highlight_ts:
        events.append(
            {
                "ts": deploy_ts,
                "kind": "deploy",
                "title": "updated（）",
                "detail": f"{display_name(loop) if loop else ' '} · 3",
                "loop": loop or impact_loop,
                "correlate": True,
                "impact_scope": "write_govern",
                "impact": impact_effect,
                "impact_level": "warn",
            }
        )
        events.append(
            {
                "ts": highlight_ts,
                "kind": "alert",
                "title": "：",
                "detail": (
                    f"「 v2 / updated」 ，"
                    f"{impact_effect}； 。"
                ),
                "loop": loop or impact_loop,
                "correlate": True,
                "impact_scope": "write_govern",
                "impact": impact_effect,
                "impact_level": "critical",
            }
        )

    for r in sorted(runs.values(), key=lambda x: x.get("last_ts") or "", reverse=True)[:10]:
        if loop and r.get("control_loop") != loop:
            continue
        if r.get("errors") or r.get("ok") is False:
            tool = "write_govern"
            for s in r.get("steps") or []:
                d = s.get("detail") or {}
                if d.get("tool"):
                    tool = str(d["tool"])
                    break
            events.append(
                {
                    "ts": r.get("last_ts"),
                    "kind": "error",
                    "title": f"· {r['run_id']}",
                    "detail": f"tool={tool} errors={r.get('errors')} stop={r.get('stop_reason')}",
                    "loop": r.get("control_loop"),
                    "run_id": r["run_id"],
                    "correlate": True,
                    "impact_scope": tool,
                    "impact": f"{tool} ， {display_name(r.get('control_loop') or impact_loop)}",
                    "impact_level": "critical",
                }
            )
        elif r.get("slow") or (r.get("duration_ms") or 0) >= 5000:
            events.append(
                {
                    "ts": r.get("last_ts"),
                    "kind": "warn",
                    "title": f"· {r['run_id']}",
                    "detail": f"duration_ms={r.get('duration_ms')}",
                    "loop": r.get("control_loop"),
                    "run_id": r["run_id"],
                    "correlate": True,
                    "impact_scope": "write_govern",
                    "impact": f"RT {r.get('duration_ms')} ms（ ）",
                    "impact_level": "warn",
                }
            )
        elif r.get("blocked"):
            events.append(
                {
                    "ts": r.get("last_ts"),
                    "kind": "gate",
                    "title": f"· {r['run_id']}",
                    "detail": f"skills={','.join(r.get('skills') or [])} stop={r.get('stop_reason')}",
                    "loop": r.get("control_loop"),
                    "run_id": r["run_id"],
                    "correlate": False,
                    "impact_scope": ",".join(r.get("skills") or []) or "gate",
                    "impact": "（，）",
                    "impact_level": "info",
                }
            )

    events.sort(key=lambda e: e.get("ts") or "", reverse=True)

    # —— ： if-else （ ， ML）——
    fail_runs = [
        r
        for r in runs.values()
        if (not loop or r.get("control_loop") == loop)
        and (r.get("errors") or r.get("ok") is False)
    ]
    slow_runs = [
        r
        for r in runs.values()
        if (not loop or r.get("control_loop") == loop)
        and (r.get("slow") or (r.get("duration_ms") or 0) >= 5000)
    ]
    related = [r["run_id"] for r in (fail_runs + slow_runs)][:5]
    if not related:
        related = [
            r["run_id"]
            for r in runs.values()
            if (not loop or r.get("control_loop") == loop) and r.get("blocked")
        ][:3]

    evidence: list[str] = []
    if highlight_ts:
        evidence.append(
            f"：{_fmt_clock(highlight_ts)}"
            + (f"（ {err_at}）" if err_at is not None else "")
            + (f"， {abs(sr_drop)}%" if sr_drop and sr_drop > 0 else "")
            + f"； ={anomaly_reason}"
        )
    evidence.append(f"： v2 / updated · {_fmt_clock(deploy_ts)} · write_govern")

    tool_hit = None
    for r in fail_runs:
        for s in r.get("steps") or []:
            d = s.get("detail") or {}
            if d.get("tool") and str(s.get("step_status", "")).lower() in {"error", "fail", "failed"}:
                tool_hit = str(d["tool"])
                evidence.append(
                    f"：run `{r['run_id']}` · {tool_hit}"
                    + (f" · {d.get('error_code')}" if d.get("error_code") else "")
                    + (f" · {d.get('error')}" if d.get("error") else "")
                )
                break
        if tool_hit:
            break
    if not tool_hit and slow_runs:
        r0 = slow_runs[0]
        evidence.append(f"：run `{r0['run_id']}` · RT {r0.get('duration_ms')} ms（write_govern ）")
        tool_hit = "write_govern"

    if highlight_ts and tool_hit:
        chain = (
            f"： {tool_hit} /"
            f"→ （timestamp {_fmt_clock(deploy_ts)}）"
            f"→ this 。"
        )
        rca = {
            "title": "",
            "mode": "rule_engine",
            "summary": chain,
            "suspect": f"{tool_hit} TIMEOUT / （ + + run ）",
            "suggestion": f"{tool_hit} ； v2； run。",
            "confidence": 0.82 if fail_runs else 0.7,
            "highlight_ts": highlight_ts,
            "related_run_ids": related,
            "evidence": evidence,
            "log_query": {"q": tool_hit, "status": "error", "run_ids": related},
        }
    elif highlight_ts:
        chain = (
            f"： （{_fmt_clock(highlight_ts)}）"
            f"→ write_govern"
            f"→ 。"
        )
        rca = {
            "title": "",
            "mode": "rule_engine",
            "summary": chain,
            "suspect": "，",
            "suggestion": "； run。",
            "confidence": 0.62,
            "highlight_ts": highlight_ts,
            "related_run_ids": related,
            "evidence": evidence,
            "log_query": {"q": "write_govern", "status": "error", "run_ids": related},
        }
    else:
        rca = {
            "title": "",
            "mode": "rule_engine",
            "summary": "，。",
            "suspect": "",
            "suggestion": "inspection； Story  run。",
            "confidence": 0.9,
            "highlight_ts": None,
            "related_run_ids": [],
            "evidence": ["：error_count≥2.5  success_rate<85 "],
            "log_query": {"q": None, "status": "error", "run_ids": []},
        }
    return events[:16], rca, highlight_ts


def build_ops_dashboard(
    *,
    loop: str | None = None,
    store: SharedStore | None = None,
    registry: ToolRegistry | None = None,
) -> dict[str, Any]:
    store = store or default_store
    registry = registry or default_registry
    loop = canonicalize(loop) if loop else None
    if loop and loop not in PLATFORM_LOOPS:
        loop = None

    logs = store.list_run_logs()
    runs = _build_run_index(logs)
    signals = _golden_from_runs(runs, loop=loop)
    highlight_ts, anomaly_idx, anomaly_reason = _detect_highlight(signals)
    runs = _merge_demo_incidents(runs, highlight_ts=highlight_ts)

    err_steps = sum(
        1 for x in logs if str(getattr(x, "step_status", "")).lower() in {"error", "fail", "failed"}
    )
    err_steps += sum(int(r.get("errors") or 0) for r in runs.values() if r.get("demo"))
    blocked = sum(
        1
        for r in runs.values()
        if r.get("blocked") and (loop is None or r.get("control_loop") == loop)
    )
    health = _health_score(signals, blocked=blocked, errors=err_steps)
    events, rca, highlight_ts = _events_and_rca(
        signals,
        runs,
        loop=loop,
        highlight_ts=highlight_ts,
        anomaly_idx=anomaly_idx,
        anomaly_reason=anomaly_reason,
    )

    def _run_rank(r: dict[str, Any]) -> tuple:
        # / ，
        sev = 0
        if r.get("errors") or r.get("ok") is False:
            sev = 0
        elif r.get("slow") or (r.get("duration_ms") or 0) >= 5000:
            sev = 1
        elif r.get("blocked"):
            sev = 2
        else:
            sev = 3
        return (sev, -( _parse_ts(r.get("last_ts")).timestamp() if _parse_ts(r.get("last_ts")) else 0))

    run_list = [
        {
            "run_id": r["run_id"],
            "control_loop": r.get("control_loop"),
            "skills": r.get("skills"),
            "steps": len(r.get("steps") or []),
            "errors": r.get("errors"),
            "blocked": r.get("blocked"),
            "ok": r.get("ok"),
            "slow": bool(r.get("slow") or (r.get("duration_ms") or 0) >= 5000),
            "demo": bool(r.get("demo")),
            "duration_ms": r.get("duration_ms"),
            "last_ts": r.get("last_ts"),
            "stop_reason": r.get("stop_reason"),
        }
        for r in sorted(
            [x for x in runs.values() if loop is None or x.get("control_loop") == loop],
            key=_run_rank,
        )
    ][:20]

    chains = [build_call_chain(runs[r["run_id"]]) for r in run_list[:6] if r["run_id"] in runs]

    loop_cards = []
    for lid in PLATFORM_LOOPS:
        subset = [r for r in runs.values() if r.get("control_loop") == lid]
        ok_n = sum(1 for r in subset if r.get("ok") and not r.get("errors"))
        loop_cards.append(
            {
                "control_loop": lid,
                "name": LOOP_META[lid]["name"],
                "runs": len(subset),
                "success_rate": round(100.0 * ok_n / len(subset), 1) if subset else None,
                "status": LOOP_META[lid]["status"],
            }
        )

    tools = registry.tool_class_summary()
    return {
        "ok": True,
        "purpose": "troubleshooting_dashboard",
        "scope": loop or "platform",
        "control_loop": loop,
        "health": health,
        "golden_signals": {
            "success_rate": {"label": " %", "unit": "%", "points": signals["success_rate"]},
            "latency_ms": {"label": "RT ", "unit": "ms", "points": signals["latency_ms"]},
            "throughput": {"label": "", "unit": "runs/", "points": signals["throughput"]},
            "error_count": {"label": "", "unit": "count", "points": signals["error_count"]},
        },
        "events": events,
        "highlight_ts": highlight_ts,
        "root_cause": rca,
        "runs": run_list,
        "call_chains": chains,
        "loop_cards": loop_cards,
        "tool_counts": tools.get("counts") or {},
        "stats": store.stats(),
    }


def build_ops_run_trace(run_id: str, *, store: SharedStore | None = None) -> dict[str, Any]:
    store = store or default_store
    demo = build_demo_incident_runs()
    if run_id in demo:
        run = demo[run_id]
        return {
            "run_id": run_id,
            "found": True,
            "summary": {
                "control_loop": run.get("control_loop"),
                "skills": run.get("skills"),
                "duration_ms": run.get("duration_ms"),
                "ok": run.get("ok"),
                "blocked": run.get("blocked"),
                "slow": run.get("slow"),
                "stop_reason": run.get("stop_reason"),
                "demo": True,
            },
            "call_chain": build_call_chain(run),
            "steps": run.get("steps") or [],
            "ai_outputs": [],
        }
    logs = store.list_run_logs(run_id=run_id)
    runs = _build_run_index(logs)
    run = runs.get(run_id)
    if not run:
        return {"run_id": run_id, "found": False, "call_chain": None, "steps": [], "ai_outputs": []}
    outputs = store.read_ai_outputs(run_id=run_id, limit=50)
    return {
        "run_id": run_id,
        "found": True,
        "summary": {
            "control_loop": run.get("control_loop"),
            "skills": run.get("skills"),
            "duration_ms": run.get("duration_ms"),
            "ok": run.get("ok"),
            "blocked": run.get("blocked"),
            "stop_reason": run.get("stop_reason"),
        },
        "call_chain": build_call_chain(run),
        "steps": run.get("steps") or [],
        "ai_outputs": [
            o.model_dump(mode="json") if hasattr(o, "model_dump") else o for o in outputs
        ],
    }