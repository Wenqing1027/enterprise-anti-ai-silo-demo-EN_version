# RAG · Module 3: Phase-1 demo scope and schedule

> **Core reference · RAG Module 3**  
> Aligns with `BLUEPRINT.md` D7 (RAG loop + kb skills) and anti-AI-silo Stories  
> Version: V1.0 · 2026-08-05

---

## 1. Ruling: what phase 1 does

### 1.1 Must (P0)

| Item | Content | Acceptance |
|------|---------|------------|
| RAG control loop | `agents/rag/`: `retrieve → stuff → generate` | CLI/API: `agent_type=rag` + `skill_id` runnable |
| Skill ×3 | `repair_kb` · `policy_kb` · `hr_rules` (YAML + domain allowlist) | Each domain ≥1 gold Q with citations |
| Unified tools | Only `shared` DataFetcher + `search_kb` / `get_kb_document` | No private fetcher under `agents/rag/` |
| Index strategy | Phase 1: **local TF-IDF or simple vectors** (blueprint); on `data/knowledge/**` | Model swap does not break Skill contract |
| Catalog | `AGENT_TYPES.rag.status` → runnable; FEATURES show RAG cards | Visible on business wall / ops |
| Security | `kb_domains_allow` same gate as ReAct | Cross-domain search rejected |

### 1.2 Illustrative but shallow (P1)

| Item | Approach |
|------|----------|
| Channel flow RAG node | Flow exists; loop reuses `policy_kb`/`channel` domain; **no** auto-merge brief |
| App Q&A F-UO-009 | **Reuse** `repair_kb` (or `app_qa` alias same config); no second index |
| Optional `write_ai_output` | Show “Q&A can assetize”; **not** Story1/2 hard dependency |

### 1.3 Explicitly not / deferred (P2+)

| Item | Reason |
|------|--------|
| Per-dept vector DB / multiple embedding services | Anti-AI-silo principle |
| Multi-loop auto chain RAG + ReAct | Scope blow-up; manual steps phase 1 |
| KB auto-update pipeline (F-UO-010) | Extract→ingest engineering |
| New domains: procurement/legal/brand/patent/org memory | No synthetic long text or off demo main line |
| Text2SQL / metric semantic RAG (F-DAT-002/003) | Ask-data primary ReAct; separate line |
| Production rerank, hybrid retrieval, GPU, fine-tune | Demo retrieval sufficient |
| Real customer doc ingest | Compliance red line |

---

## 2. vs Story1 / Story2

| Story | RAG role |
|-------|----------|
| Story1 ticket assetization | **Does not depend** on RAG; RAG is parallel “knowledge loop” demo |
| Story2 renewal complaint gate | **Does not depend** on RAG; gate reads shared tags |
| Anti-AI-silo narrative | Same `search_kb` + knowledge source for RAG Skills and ReAct tools → “single tools layer” |

Recording tip: after Story1/2 add **30–60s** RAG: one repair-domain question + show chunk citation + note “ReAct can call same search_kb.”

---

## 3. Feature schedule (vs other loops)

As of 2026-08-05: ReAct / Extract loops and docs exist; RAG / Plan / Rule+LLM / Vision dirs mostly placeholders.

| Order | Work package | Depends | Output |
|-------|--------------|---------|--------|
| **R0** | Doc trio (map / relations / scope) | planning + requirements | `docs/rag/*` ✅ |
| **R1** | Doc chunking + index build | `data/knowledge` | chunks + index; search API smoke |
| **R2** | RAG Skill YAML ×3 + schema | SCHEMA.md | `skills/repair_kb` etc. loadable |
| **R3** | Loop + CLI/API wiring | R1+R2 · shared tools | `status=ready` |
| **R4** | Gold Q&A + simple eval | R3 | `docs/rag/eval` or scripts |
| **R5** | Business wall / ops cards | R3 · catalog | Same pattern as Extract |
| **R6** | flows add `service_repair_qa` etc. | R3 | Align with planning contract |

**Parallel tip**: R1 can parallel Plan/Rule docs; R3 avoid same week as large ToolRegistry refactor.

Blueprint anchor: original **D7 ≈ 3h** skeleton; full three Skills + eval + UI suggest **R1–R5 across 2–3 sessions**.

---

## 4. Phase-1 demo script (3 questions)

| # | skill | User question (synthetic) | Expect |
|---|-------|---------------------------|--------|
| Q1 | `repair_kb` | Range suddenly worse — how to troubleshoot? | Hit range doc; steps + citation |
| Q2 | `policy_kb` | 2026Q3 pickup rebate tier? | Hit rebate policy; fictional disclaimer |
| Q3 | `hr_rules` | Agent QC SOP red lines? | Hit SOP highlights |

Negative: `repair_kb` asks HR policy → domain gate reject or clear “outside this kb domain.”

---

## 5. Success criteria (demo level)

| Metric | Threshold |
|--------|-----------|
| Loop runnable | All 3 Skills end-to-end |
| Citations visible | Final answer includes `kb_doc_id` / chunk or equivalent |
| Domain isolation | `kb_domains_allow` cross-domain fails |
| No private fetcher | Code review / directory check |
| Story1/2 intact | Existing smoke still green |

---

## 6. Next functional steps (build order)

> Checklist from docs → index → …; **implementation started at R1**.

1. **KB inventory + chunking** ✅  
   - Strategy: `docs/rag/04-document-chunking-strategy.md`  
   - Output: `data/knowledge/chunks.json` (`scripts/build_kb_chunks.py`)  
   - Impl: `shared/rag/chunking.py`  

2. **Index / retriever** ✅  
   - Strategy: `docs/rag/05-index-and-retriever.md`  
   - Output: `data/knowledge/tfidf_index.json` (`scripts/build_kb_index.py`)  
   - Impl: `shared/rag/tfidf_index.py`; exit `DataFetcher.search_kb`  

3. **RAG Skill contract** ✅  
   - Strategy: `docs/rag/06-rag-skill-contract.md`  
   - Output: `skills/{repair_kb,policy_kb,hr_rules}/skill.yaml`  
   - Impl: `agents/rag/skill_schema.py` · `skill_loader.py`; dispatch `apps/skill_dispatch.py`  

4. **Control loop** ✅  
   - Strategy: `docs/rag/07-control-loop-implementation-and-wiring.md`  
   - Impl: `agents/rag/agent.py`; CLI / `POST /v1/rag/runs`; smoke `scripts/smoke_rag.py`  

5. **Gold + smoke** ✅  
   - Gold: `data/eval/rag/gold_qa.json` (15 cases)  
   - Eval: `scripts/eval_rag.py` → `docs/rag/eval_reports/`  
   - Smoke: `scripts/smoke_rag.py`; see `docs/rag/08-gold-standard-eval-and-smoke.md`  

6. **Catalog / UI** ✅ (RAG demo cards + business/ops routing)  
   - FEATURES: `F-SVC-002/004` · `F-POL-RAG` · `F-UO-009` · `F-HR-001`  
   - `rag` status=ready; `/v1/rag/runs`  

7. **Orchestration writeback** ✅  
   - `department_flows.json`: `service_repair_qa` / `user_ops_app_qa` / `order_policy_qa` / `hr_policy_qa`; `channel_ops_board` RAG node `policy_kb`  
   - Sync `docs/planning/02` · catalog `flow_ids`  

8. **(Optional) side-path assetization**  
   - RAG final answer `write_ai_output` for later Plan consume — **not done phase 1 (intentionally deferred)**  

---

## 7. Revisions

| Version | Notes |
|---------|-------|
| V1.0 | Phase-1 scope, Story relation, R0–R6 schedule and build steps |
