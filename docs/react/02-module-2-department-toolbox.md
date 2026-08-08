# ReAct · Module 2: Department toolboxes

> **Core reference · Module 2** (depends on [Module 1](./01-module-1-background-cross-dept-features-tone.md))  
> Principle: **each tool is implemented once** (`shared/tools`); department variance = Skill `allowed_tools` allowlist  
> Version: V1.0 · 2026-08-02

---

## 0. How to read this doc

| Concept | Meaning |
|---------|---------|
| **Global tool pool** | All tools in `ToolRegistry`; departments do not duplicate implementations |
| **Department toolbox** | Subset the department ReAct Skill **may call** (allowlist) |
| **Required / optional** | Required = the feature loop cannot close without it; optional = enhancement or cross-domain read-only |

Anti-AI-silo point: `write_ai_output` from service ticket fill and `read_ai_outputs` / `check_outreach_block` from user ops are **the same tools**, not two separate APIs.

---

## 1. Global tool pool (implemented)

> Source: `shared/tools/handlers.py` · aligned with `data/entities/capability_catalog.json`.

### 1.1 Master data `master`

| Tool | One-line purpose |
|------|------------------|
| `get_customer` | Look up customer |
| `get_vehicle` | Look up vehicle (VIN=`QS0…`) |
| `list_vehicles` | List vehicles by customer/model |
| `get_dealer` | Look up tier-1 dealer |
| `get_store` | Look up store |
| `list_stores` | List stores |
| `get_sku` | Look up SKU |
| `get_org` | Look up org node |
| `list_regions` | List administrative regions |
| `list_competitors` | Competitor snapshot (fictional) |

### 1.2 Commerce `commerce`

| Tool | One-line purpose |
|------|------------------|
| `get_order` / `list_orders` | Look up / filter orders |
| `list_inventory` | Check inventory |
| `get_policy` | Rebate policy summary |
| `simulate_rebate_tier` | Simulate next pickup tier bump |
| `list_color_plans` | Color production schedule |

### 1.3 Service / VoC `service`

| Tool | One-line purpose |
|------|------------------|
| `get_ticket` / `list_tickets` | Look up / filter tickets |
| `extract_ticket_fields` | Text → ticket draft fields |
| `list_voc` | VoC feedback slice |
| `suggest_voc_tags` | Suggest tags and sentiment |

### 1.4 Renewal `renewal`

| Tool | One-line purpose |
|------|------------------|
| `get_renewal` | Renewal pool record |
| `score_renewal` | Renewal intent score |
| `route_renewal_pool` | Pool routing and outreach tiers |
| `check_outreach_block` | Whether shared tags block outreach (Story2) |
| `get_user_behavior` | Behavior / RFM |

### 1.5 Knowledge base `knowledge`

| Tool | One-line purpose |
|------|------------------|
| `search_kb` / `get_kb_document` / `list_kb_domains` | Search / full text / list domains |

### 1.6 Shared layer `shared` (anti-AI-silo core)

| Tool | One-line purpose |
|------|------------------|
| `write_ai_output` | Write AI output |
| `read_ai_outputs` / `get_ai_output` | Read outputs |
| `read_shared_tags` | Read shared tag projection |
| `list_capabilities` / `get_capability` | Capability catalog |
| `get_tag` / `list_tags` | Tag dictionary |
| `log_step` / `list_run_logs` | Step logs |

### 1.7 Channel / IoT `channel` · `iot`

| Tool | One-line purpose |
|------|------------------|
| `get_dealer_health` | Tier-1 dealer health index |
| `list_alerts` | Business alerts |
| `list_sales_metrics` | Sales attainment |
| `list_retail_daily` | Store retail daily report |
| `list_inspections` | Store inspections |
| `get_risk` | Franchise/partner risk control |
| `list_campaigns` | Marketing campaigns |
| `get_telemetry` | Vehicle telemetry/alerts |
| `list_quality_checks` | QC records |

### 1.8 Not yet implemented (reserved for departments)

| Reserved tool | Department | Notes |
|---------------|------------|-------|
| `get_po` / `list_po` / `confirm_logistics` | Procurement | Phase 1: proxy with `list_orders`+`log_step` for follow-up, or add in phase 2 |
| `query_metric` | Data lab | Phase 1: use `list_sales_metrics` / `list_retail_daily` instead of “ask data” |
| `get_hr_policy_step` | HR | Phase 1: `search_kb(domain=hr)`; process steps may read-only via `log_step` |

---

## 2. Department toolboxes

> Each department = Module 1 feature → **required tools** + **optional tools** + **bound Skill**.  
> “Shared chassis” in almost every box: `log_step`; add `write_ai_output` for writes; add `read_*` for reads.

### 2.1 Service · Calm confirm

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Smart ticket fill F-SVC-001 | `fill_ticket` ✅ | `get_customer`, `get_vehicle`, `get_ticket`, `list_tickets`, `extract_ticket_fields`, `suggest_voc_tags`, `get_tag`, `write_ai_output`, `log_step` | `get_telemetry`, `search_kb`(repair) |
| Repair assist multi-step F-SVC-003 | `crm_lookup` + kb domain | `get_customer`, `get_vehicle`, `list_tickets`, `search_kb`, `get_kb_document`, `get_telemetry`, `log_step` | `list_quality_checks`, `write_ai_output` |

**Allowlist (matches catalog · `fill_ticket`)**

```text
get_customer, get_vehicle, get_ticket, list_tickets,
extract_ticket_fields, suggest_voc_tags, get_tag,
write_ai_output, log_step
```

---

### 2.2 User ops / App · Nudge not push

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Proactive outreach gate F-UO-017 | Consumer side (Planning `renewal_plan` often owns; ReAct may reuse same box) | `get_customer`, `get_vehicle`, `get_renewal`, `read_ai_outputs`, `read_shared_tags`, `check_outreach_block`, `log_step` | `get_telemetry`, `get_user_behavior` |
| Renewal outbound task F-UO-001 | Same / illustrative ReAct | `get_renewal`, `score_renewal`, `route_renewal_pool`, `get_user_behavior`, `log_step` | `list_campaigns` |
| Unified smart service F-UO-019 | Illustrative | `get_customer`, `get_vehicle`, `list_tickets`, `get_renewal`, `search_kb`, `log_step` | `list_orders` |

**Allowlist (`renewal_plan` · Story2)**

```text
get_customer, get_vehicle, get_renewal, get_user_behavior,
score_renewal, route_renewal_pool, read_ai_outputs,
read_shared_tags, check_outreach_block, log_step
```

> Note: `fill_ticket` **must not** call `score_renewal` (smoke test locked) — anti-AI-silo relies on shared outputs, not stealing each other’s tools.

---

### 2.3 Ops · order/policy · Policy precise

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Smart order review F-OPS-003 | Illustrative `order_review` (may reuse `crm_lookup`+commerce) | `get_dealer`, `list_orders`, `list_inventory`, `get_policy`, `simulate_rebate_tier`, `get_sku`, `log_step` | `list_color_plans`, `write_ai_output` |

**Suggested allowlist**

```text
get_dealer, get_store, get_sku, get_order, list_orders,
list_inventory, get_policy, simulate_rebate_tier,
list_color_plans, write_ai_output, log_step
```

---

### 2.4 Four war zones · Frontline direct

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Pickup/order assist F-WZ-001/002 | Shares commerce box with order review | `list_inventory`, `get_policy`, `simulate_rebate_tier`, `list_orders`, `get_dealer`, `log_step` | `search_kb`(policy/channel), `list_alerts` |

**Suggested allowlist**

```text
get_dealer, get_store, list_stores, list_inventory, list_orders,
get_policy, simulate_rebate_tier, search_kb, log_step
```

---

### 2.5 Channel ops · Ops dashboard

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Health/alert lookup F-OPS-012 | `channel_ops` ✅ | `get_dealer`, `get_dealer_health`, `list_alerts`, `list_sales_metrics`, `list_retail_daily`, `list_inspections`, `get_risk`, `get_policy`, `simulate_rebate_tier`, `log_step` | `list_campaigns`, `write_ai_output` |

**Allowlist (catalog · `channel_ops`)**

```text
get_dealer, get_dealer_health, list_alerts, list_sales_metrics,
list_retail_daily, list_inspections, get_risk, get_policy,
simulate_rebate_tier, log_step
```

---

### 2.6 New retail · Shelf guide

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Multi-platform service F-RET-001/002 | Illustrative | `get_order`, `list_orders`, `list_inventory`, `list_campaigns`, `get_sku`, `get_store`, `log_step` | `get_customer`, `search_kb`(product) |

**Suggested allowlist**

```text
get_customer, get_order, list_orders, list_inventory,
get_sku, get_store, list_campaigns, search_kb, log_step
```

---

### 2.7 Procurement · Milestone track

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| PO follow-up / expedite F-PUR-001/003 | Illustrative (PO tools reserved) | Phase 1 proxy: `list_orders`, `list_inventory`, `list_color_plans`, `log_step` | `list_alerts`, `write_ai_output` |

**Suggested allowlist (phase 1 proxy)**

```text
list_orders, list_inventory, list_color_plans, get_sku,
log_step, write_ai_output
```

**Phase 2 additions**: `get_po`, `list_po`, `confirm_logistics`.

---

### 2.8 Data lab · Answer first

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Smart ask-data F-DAT-003 | Illustrative | `list_sales_metrics`, `list_retail_daily`, `get_dealer_health`, `list_alerts`, `log_step` | `list_capabilities`, `read_ai_outputs` |

**Suggested allowlist**

```text
list_sales_metrics, list_retail_daily, get_dealer_health,
list_alerts, list_regions, get_org, log_step
```

---

### 2.9 HR platform · Friendly neutral

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Employee assistant F-HR-001 | Illustrative (main path may be RAG) | `search_kb`, `get_kb_document`, `list_kb_domains`, `log_step` | `list_capabilities` |

**Suggested allowlist**

```text
search_kb, get_kb_document, list_kb_domains, log_step
```

> `domain` restricted to `hr` (hardened further in Module 4).

---

### 2.10 IoT / vehicle · Alert brief

| Feature | Skill | Required toolbox | Optional |
|---------|-------|------------------|----------|
| Telemetry proactive service F-IOT-003 | Illustrative | `get_vehicle`, `get_telemetry`, `list_quality_checks`, `list_tickets`, `write_ai_output`, `log_step` | `get_customer`, `search_kb`(repair) |

**Suggested allowlist**

```text
get_vehicle, get_customer, get_telemetry, list_quality_checks,
list_tickets, write_ai_output, search_kb, log_step
```

---

### 2.11 System / shared layer · Neutral system

| Feature | Skill | Required toolbox |
|---------|-------|------------------|
| Generic output write | `shared_write` ✅ | `write_ai_output`, `read_ai_outputs`, `get_ai_output`, `log_step` |
| Capability discovery | Optional on any Skill | `list_capabilities`, `get_capability` |

---

## 3. Skill → toolbox summary (phase 1)

| Skill | Dept narrative | Toolbox source | Demo |
|-------|----------------|----------------|------|
| `fill_ticket` | Service | §2.1 | ✅ Story1 |
| `crm_lookup` | Multi-dept master data | Catalog allowlist | ✅ |
| `channel_ops` | Channel ops | §2.5 | ✅ |
| `shared_write` | Shared layer | §2.11 | ✅ |
| `renewal_plan` | User ops (Planning owns; same toolbox) | §2.2 | ✅ Story2 |
| `repair_kb` / `policy_kb` | Service/policy (RAG owns) | knowledge + few master tools | RAG Demo |
| `voc_tagging` | Service/research (Extraction owns) | service + shared | Extraction Demo |

Illustrative Skills (toolbox defined; directory optional): `order_review`, retail service, procurement follow-up, ask-data, HR assistant, IoT proactive service.

---

## 4. Cross-department shared matrix (who uses the same hand)

| Tool | Service | User ops | Order/war zones | Channel | New retail | Procurement | Data | HR | IoT |
|------|:-------:|:--------:|:---------------:|:-------:|:----------:|:-----------:|:----:|:--:|:---:|
| `get_customer` / `get_vehicle` | ● | ● | ○ | | ○ | | | | ● |
| `list_inventory` / `get_order*` | ○ | ○ | ● | | ● | ● | | | |
| `get_policy` / `simulate_rebate_tier` | | | ● | ● | | | | | |
| `list_tickets` / `extract_ticket_fields` | ● | ○ | | | | | | | ○ |
| `get_renewal` / `check_outreach_block` | | ● | | | | | | | |
| `get_dealer_health` / `list_alerts` | | | ○ | ● | | ○ | ● | | |
| `get_telemetry` | ○ | ○ | | | | | | | ● |
| `search_kb` | ● | ○ | ○ | | ○ | | | ● | ○ |
| `write_ai_output` | ● | | ○ | ○ | | ○ | | | ● |
| `read_ai_outputs` / `read_shared_tags` | | ● | | ○ | | | ○ | | |
| `log_step` | ● | ● | ● | ● | ● | ● | ● | ● | ● |

● Required · ○ Optional

---

## 5. Module 2 acceptance (self-check)

- [x] Global tool pool aligned with code implementation  
- [x] Each Module 1 department has a toolbox (required/optional)  
- [x] Phase-1 Skill allowlists match `capability_catalog.json`  
- [x] Cross-department shared-tool matrix documented  
- [x] Gaps (procurement, ask-data, etc.) marked as reserved — no fake private APIs  

---

## Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-02 | Module 2 initial: department toolboxes |
