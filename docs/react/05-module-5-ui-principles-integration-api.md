# UI principles + integration API (business wall / ops troubleshooting)

> **Version**: V2.0 · 2026-08-07  
> **Correction**: Ops desk **is not** “try-run Skills by control loop / policy Q&A”; that is the business wall.  
> Ops desk = **troubleshooting**: log stream · metrics · trace (run) data.

---

## 1. Two pages

| Page | Route | Audience | Principle |
|------|-------|----------|-----------|
| Business workspace | `/business` | Business roles | One card = one function = one Skill; platform loops + dept Skills; demo try-run |
| Ops console | `/ops`, `/ops/embed` | Tech ops / SRE | Runtime troubleshooting: logs / metrics / traces / shared output health |

```text
Business: pick department → function card → try-run this Skill (POST /v1/{loop}/runs or /v1/runs)

Ops: overview metrics → filter log stream → trace by run_id → check AIOutput / tool health
     (no business Skill try-run entry)
```

---

## 2. Ops desk data sources (demo)

| Panel | Source |
|-------|--------|
| Metrics | `SharedStore.stats` + step error rate + four-loop readiness |
| Log stream | `run_logs.json` (`list_run_logs`) |
| Trace | Steps aggregated by `run_id` + linked `AIOutput` |
| Shared outputs | `GET /v1/ai-outputs` |
| Tool health | `GET /v1/tools` + registry counts |

API (ops-specific):

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/v1/ops/overview` | Global: health score · four golden metrics · events · root cause · call chain |
| GET | `/v1/ops/loops/{control_loop}` | Same shape for **four-loop subpages** |
| GET | `/v1/ops/logs` | Log stream |
| GET | `/v1/ops/runs` | Recent run list |
| GET | `/v1/ops/runs/{run_id}` | Single **call chain** + steps + AIOutput |

---

## 3. Business demo-ready (still on business wall)

See business wall cards and `docs/agent-orchestration.md`; ops desk no longer hosts RAG/ticket try-runners.

---

## 4. Start

```bash
bash scripts/ensure_api.sh
# Business http://127.0.0.1:8000/business
# Ops troubleshooting http://127.0.0.1:8000/ops
# Embed http://127.0.0.1:8000/ops/embed
```
