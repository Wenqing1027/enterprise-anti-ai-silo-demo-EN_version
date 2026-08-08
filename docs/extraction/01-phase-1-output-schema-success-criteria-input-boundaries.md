# Extraction Agent · Phase 1: Output Schema · Success Criteria · Input Boundaries

> **Core reference · Extraction Phase 1** (maps to blueprint `agents/extraction/`)  
> Fictional company: **Qingshu Mobility** · smart electric mobility  
> Control loop: `schema → extract → validate`  
> Field alignment: `docs/standard-field-glossary.md`, `shared/models`  
> Version: V1.0 · 2026-08-05  
> **Scope**: This phase defines **what to extract / success criteria / input boundaries** for **every department and feature that touches Extraction** — **whether or not it ships in the Demo**. Demo must-haves are marked ✅.

---

## 0. Scope and conventions

### 0.1 Phase 1 coverage

| Category | Description |
|----------|-------------|
| ✅ **Demo must-have** | `ticket_fields` (aligned with F-SVC-001), `voc_entities` / `voc_tagging` (aligned with F-VOC-002 and service VoC feedback) |
| 📋 **Spec placeholder** | All other Extraction features in the requirements list (including composite ones): this file defines schema / criteria / boundaries; **no control loop is implemented** |

### 0.2 Success criteria (unified)

| Metric | Meaning | Eval method (Demo) |
|--------|---------|-------------------|
| **Schema compliance rate** | Output passes JSON Schema / Pydantic validation | Automated assertion |
| **Required-field recall** | Required fields that “should exist” in gold labels are extracted | Field-level recall |
| **Enum accuracy** | Enum fields match gold labels | Exact match |
| **Tolerance** | Boundaries for nulls / low confidence / human confirmation | See each feature card |
| **Zero missed block tags** | Complaint / risk tags that affect Story2 must not be missed | Dedicated gold set |

**Demo default thresholds** (rule-based extraction or lightweight LLM): schema compliance **100%**; core enum accuracy **≥75%**; missed block tags **=0**.  
**Spec placeholder features** define target thresholds for future rollout; they are **not** acceptance criteria for this phase.

### 0.3 Input boundary rules (general)

| Allowed (Phase 1) | Forbidden |
|-------------------|-----------|
| UTF-8 plain text, call / CS transcripts, synthetic JSON seeds | Real customer PII in plaintext, real brand names |
| Transcribed `.txt` / `.md`, structured `.json` payloads | Raw audio/video as primary Extraction input (transcription is upstream) |
| Single voice item ≤4k chars after truncation (slice first if longer) | Long-form RAG Q&A, pixel-level Vision tasks in this brain |

Machine-readable schema files: `docs/extraction/schemas/`.

### 0.4 Overview index

| Feature ID | Department | Feature name | Demo | Skill / Schema ID |
|------------|------------|--------------|------|-------------------|
| F-SVC-001 | Service Division | Smart ticket fill | ✅ | `ticket_fields` / `ticket_draft_v1` |
| F-VOC-002 | UX Research / Ops | Auto tagging + sentiment | ✅ | `voc_entities` / `voc_entities_v1` |
| F-SVC-006 | Service Division | NLP clustering + corpus feedback | ✅ same source | Reuse `voc_entities_v1` + batch |
| F-SVC-009 | Service / Brand | VoC system (single-item extract) | ✅ same source | Reuse `voc_entities_v1` |
| F-X-003 | Cross-department | VoC tag library feedback | ✅ consumer chain | Output → `TagVocabulary` / `AIOutput` |
| F-SVC-005 | Service Division | VoC fault clustering | 📋 | `voc_cluster_v1` |
| F-SVC-007 | Service Division | Issue type prediction | 📋 | `issue_predict_v1` |
| F-SVC-008 | Service / Brand | Smart QA | 📋 | `sop_qc_v1` |
| F-VOC-001 | After-sales / CS | Multi-channel ingest + transcription | 📋 | `voc_ingest_v1` (semi-structured) |
| F-VOC-023 | UX Research / Ops | Tag taxonomy revision | 📋 | `tag_revise_v1` |
| F-VOC-025 | UX Research | Open-ended tagging | 📋 | Reuse `voc_entities_v1` |
| F-VOC-015 | Brand / PR | Public sentiment weak monitoring | 📋 | `pr_hotspot_v1` |
| F-VOC-017 | Region / Store | Emotion map slice | 📋 | `emotion_slice_v1` |
| F-DAT-006 | Data Research Institute | Matrix account monitoring wide table | 📋 | `matrix_account_v1` |
| F-DAT-012 | Digital asset platform | Asset structured ingest | 📋 | `asset_struct_v1` |
| F-DAT-013 | Platform / Service | Smart CS platform NLP | 📋 | Reuse ticket-fill + tagging schemas |
| F-STR-005 | Strategy / Brand | Social sentiment + competitor quarterly | 📋 | `brand_signal_v1` |
| F-BRD-005 | Brand / Retail | Matrix monitoring | 📋 | Reuse `matrix_account_v1` |
| F-BRD-008 | Brand Research Institute | MI NLP semantics | 📋 | `mi_semantic_v1` |
| F-BRD-009 | Brand / PR | Full-media sentiment | 📋 | `pr_monitor_v1` |
| F-BRD-013 | Brand Research Institute | BVP first test | 📋 | `bvp_test_v1` |
| F-BRD-014 | Brand Research Institute | Social image diagnosis | 📋 | `image_diag_v1` |
| F-BRD-015 | Brand / Digital | App experience audit | 📋 | `ux_audit_v1` |
| F-BRD-017 | Brand Research Institute | NPS real-time NLP | 📋 | Reuse `voc_entities_v1` |
| F-OPS-004 | Order / Policy | Sales policy parsing | 📋 | `policy_parse_v1` |
| F-OPS-011 | Channel / Retail | Benchmark replication path | 📋 | `benchmark_actions_v1` |
| F-WZ-004 | Territory / Retail | Guide efficiency diagnosis | 📋 | `guide_efficacy_v1` |
| F-MFG-002 | Manufacturing / Quality | PDA frame part binding | 📋 | `pda_bind_v1` |
| F-MFG-006 | Quality | Trace data package | 📋 | `trace_package_v1` |
| F-PRD-001 | Product Ops | Competitor info collection | 📋 | `competitor_card_v1` |
| F-PRD-004 | Product Innovation Lab | Patent / tech maturity | 📋 | `patent_cluster_v1` |
| F-FIN-001 | Finance | Three-way doc match extract | 📋 | `tri_doc_match_v1` |
| F-HR-002 | HR | Job match extract | 📋 | `job_match_v1` |
| F-LEG-001 | Legal / Compliance | Contract risk extract | 📋 | `contract_risk_v1` |
| F-UO-006 | User Ops | Outbound intent tagging | 📋 | `renew_intent_v1` |
| F-UO-010 | User Ops | FAQ digest ingest | 📋 | `faq_digest_v1` |
| F-UO-011 | User Ops | Segment feature extract | 📋 | `segment_feat_v1` |
| F-UO-015 | User Ops | KOC identification | 📋 | `koc_candidate_v1` |
| F-UO-016 | User Ops | UGC text moderation | 📋 | `ugc_moderation_v1` |
| F-IT-001 | IT / Process | AI redundancy detection | 📋 | `process_dup_v1` |

---

## 1. Demo must-have feature cards

### 1.1 F-SVC-001 · Smart ticket fill · `ticket_fields` ✅

| Item | Content |
|------|---------|
| **Department** | Service Division |
| **What to extract** | Unstructured CS dialogue / description → **ticket draft** `ticket_draft_v1` |
| **Skill** | `ticket_fields` (ReAct side reuses tool `extract_ticket_fields`) |
| **Persist** | `AIOutput.payload`, `payload_schema=ticket_draft_v1`; `consumer_allow` includes `renewal_plan`, `voc_tagging` |
| **Machine schema** | [`schemas/ticket_draft_v1.json`](./schemas/ticket_draft_v1.json) |

#### Output schema (`ticket_draft_v1`)

| Field | Type | Required | Enum / constraint | Standard field |
|-------|------|----------|-------------------|----------------|
| `customer_id` | string\|null | Conditionally required* | `CUS-\d+` | SF-0037 |
| `vin` | string\|null | Conditionally required* | `QS0` + 14 synthetic chars | SF-0068 |
| `ticket_type` | enum | ✅ | `fault\|consult\|complaint\|other` | SF-0224 |
| `fault_category` | enum\|null | Recommended when fault | `battery\|motor\|brake\|controller\|charging\|dashboard\|frame\|lighting\|tire\|other` | SF-0225 |
| `consult_category` | string\|null | Recommended when consult | Free short label | SF-0226 |
| `ticket_channel` | string | ✅ | `400\|App\|e-commerce\|store\|community` | SF-0227 |
| `ticket_status` | enum | ✅ | Draft default `open` | SF-0228 |
| `tag_id` | string | ✅ | Must ∈ `TagVocabulary` | SF-0245 |
| `sentiment` | enum | ✅ | `pos\|neu\|neg` | SF-0248 |
| `desc_text` | string | ✅ | 1–1000 chars, redacted summary of original text | SF-0233 |
| `is_complaint` | boolean | ✅ | `true` when complaint or block tag | SF-0231 |
| `confidence` | number | Recommended | 0–1; rule extraction may fix at 0.6 | — |
| `needs_human_review` | boolean | Recommended | `true` when low confidence or missing ID | — |

\* Extract when text allows; `null` is allowed when not found, but `needs_human_review=true` is required.

#### Success criteria

| Metric | Threshold | Tolerance |
|--------|-----------|-----------|
| Schema compliance rate | **100%** | Non-compliant → whole record fails; do not write `AIOutput` |
| `ticket_type` accuracy | ≥ **80%** (Demo gold ≥20 cases) | Boundary cases (fault + complaint) may be labeled `complaint` |
| `fault_category` accuracy | ≥ **75%** (fault subset only) | Unknown → `other`, **not counted as error** |
| `tag_id` Top-1 hit | ≥ **75%**; missed block tags **0** | Multi-tag cases: evaluate primary tag only |
| `sentiment` accuracy | ≥ **80%** | `neu`/`neg` confusion on non-complaint sentences: one grade tolerated |
| ID extraction (when explicit) | VIN/CUS recall **≥95%** | `null` allowed when not explicit |
| Latency (single item) | Demo ≤ 3s (rules) / ≤ 8s (LLM) | — |

#### Input boundaries

| Supported | Not supported |
|-----------|---------------|
| CS dialogue plain text, 400 transcript `.txt`, App feedback text, seed JSON `text` field | Raw `.wav/.mp3` (must transcribe first) |
| Single item ≤4000 chars; mixed Chinese/English | PDF/image ticket scans (belongs to Vision/OCR) |
| Optional channel metadata: `channel`, `customer_id`, `vin` as hints, not required | Multi-session merged into one long memo (slice first) |

---

### 1.2 F-VOC-002 · Auto tagging + sentiment · `voc_entities` ✅

| Item | Content |
|------|---------|
| **Department** | UX Research / Ops (same source consumed by Service) |
| **What to extract** | Voice text → **VoC entity bundle** (tags, sentiment, theme, risk) |
| **Skill** | `voc_entities` / capability catalog `voc_tagging` |
| **Persist** | `AIOutput` (`payload_schema=voc_entities_v1`) + aligned shared `TagVocabulary` reference |
| **Machine schema** | [`schemas/voc_entities_v1.json`](./schemas/voc_entities_v1.json) |
| **Same-source reuse** | F-SVC-006 / F-SVC-009 (single-item) / F-VOC-025 / F-BRD-017 (single-item NLP) / F-X-003 |

#### Output schema (`voc_entities_v1`)

| Field | Type | Required | Enum / constraint | Standard field |
|-------|------|----------|-------------------|----------------|
| `feedback_id` | string\|null | Recommended | Generate `FB-*` at runtime if missing | SF-0240 |
| `sample_voice` | string | ✅ | Redacted voice, ≤500 chars | SF-0258 |
| `tag_id` | string | ✅ | ∈ TagVocabulary | SF-0245 |
| `tag_name` | string | ✅ | Matches dictionary | SF-0246 |
| `tag_domain` | enum | ✅ | `product\|service\|app\|channel\|risk` | SF-0247 |
| `sentiment` | enum | ✅ | `pos\|neu\|neg` | SF-0248 |
| `sentiment_score` | number | Recommended | [-1, 1] | SF-0249 |
| `problem_theme` | string | ✅ | Short theme name | SF-0250 |
| `severity_risk_level` | enum\|null | Conditional | `P0\|P1\|P2` when sentiment/safety related | SF-0260 |
| `clue_confidence` | enum | ✅ | `weak\|medium` (Demo has no `strong`) | SF-0259 |
| `customer_id` | string\|null | Optional | `CUS-*` | SF-0037 |
| `vin` | string\|null | Optional | `QS0*` | SF-0068 |
| `secondary_tag_ids` | string[] | Optional | ≤3, all must be in dictionary | — |
| `needs_human_review` | boolean | ✅ | `true` when dictionary miss or `weak` | — |

#### Success criteria

| Metric | Threshold | Tolerance |
|--------|-----------|-----------|
| Schema compliance rate | **100%** | Same as ticket fill |
| `tag_id` hit (primary tag) | ≥ **80%** | Near-synonym tags under same `tag_parent_id` may count as “acceptable” |
| **Missed block tags** (`TAG-open-complaint` / `TAG-reputation-risk` / `TAG-safety-hazard` / `TAG-warranty-dispute`) | **0** | Multi-tag: primary or any secondary hit counts |
| `sentiment` accuracy | ≥ **85%** (hard requirement, aligned with dashboard) | Only `pos`↔`neu` confusion allowed on non-risk sentences |
| `tag_domain` accuracy | ≥ **90%** | — |
| Out-of-vocabulary tag rate | **≤5%** | OOV must set `needs_human_review=true` and must not feed shared block logic directly |
| Batch (F-SVC-006) | Per-item pass; failed items isolated | Single failure must not block whole batch write |

#### Input boundaries

| Supported | Not supported |
|-----------|---------------|
| 400/community/satisfaction open-ended plain text, transcripts, ticket `desc_text` | Raw recordings, emoji image OCR as primary path |
| Single voice item; batch JSONL (one `text` per line) | Free-form tag creation without dictionary into shared layer |
| Optional channel field: `source_channel` | Aggregated report fields (NPS week-over-week, etc.) as single-item extract target |

---

### 1.3 Demo same-source notes (no separate control loop)

| Feature ID | Relation to Demo | Extra constraints |
|------------|------------------|-------------------|
| **F-SVC-006** | Batch call `voc_entities_v1` | Output may attach optional `cluster_hint` string; clustering algorithm itself not required for Extraction |
| **F-SVC-009** | Single-item same schema; report aggregation belongs to Planning | Extraction only guarantees per-item structure |
| **F-X-003** | Consume `tag_id` to write/update tag library reference | Schema unchanged; validate `tag_vocab_version` consistency |

---

## 2. Spec placeholder feature cards (Phase 1 contract only)

> The features below **do not implement an Extraction control loop in this phase**, but department/feature contracts are locked in Phase 1 to prevent field drift later.

### 2.1 Service Division

#### F-SVC-005 · VoC fault clustering · `voc_cluster_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Multiple tagged VoC items → cluster theme: `theme_id`, `problem_theme`, `member_feedback_ids[]`, `theme_cnt`, `neg_ratio`, `top_tag_ids[]` |
| **Success criteria** | Schema 100%; theme purity (same theme, consistent primary `tag_domain`) ≥70%; empty cluster rate ≤5% |
| **Tolerance** | Small sample (&lt;5 items) may use `clue_confidence=weak` |
| **Input boundaries** | Only JSON arrays already compliant with `voc_entities_v1`; reject raw long text |

#### F-SVC-007 · CS issue prediction · `issue_predict_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Short text → `pred_ticket_type`, `pred_fault_category`, `pred_tag_id`, `confidence` |
| **Success criteria** | Top-1 type accuracy ≥75%; confidence calibration not evaluated in Demo |
| **Tolerance** | `confidence&lt;0.4` may output `other` + human review |
| **Input boundaries** | ≤500 char keywords/first sentence; not full call recording |

#### F-SVC-008 · Smart QA · `sop_qc_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Transcript → `sop_item[]` × `{sop_item, sop_pass_fail, evidence_span}`, `risk_words[]`, `overall_pass` |
| **Success criteria** | Required SOP item recall ≥90%; `risk_words` precision ≥70% (synonyms tolerated) |
| **Tolerance** | Evidence span offset ±20 chars acceptable |
| **Input boundaries** | Agent call transcript `.txt`; optional `agent_id`; no raw audio |

---

### 2.2 VoC / UX Research / Region

#### F-VOC-001 · Multi-channel ingest + transcription · `voc_ingest_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Channel envelope → `source_channel`, `raw_uri`, `transcript_text`, `lang`, `ingested_at` (transcription quality metadata, not full-sentence NLP) |
| **Success criteria** | Envelope field completeness 100%; transcript text non-empty |
| **Tolerance** | Transcription WER not evaluated in Demo; empty audio marked `failed` |
| **Input boundaries** | Metadata JSON + transcribed text; ASR may be outsourced, not in Extraction brain |

#### F-VOC-023 · Tag taxonomy revision · `tag_revise_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Human/model suggestion → `tag_id`, `action(add\|merge\|deprecate\|rename)`, `tag_name`, `tag_domain`, `tag_parent_id`, `tag_vocab_version` |
| **Success criteria** | Action validity 100%; no cycles; domain enum valid |
| **Tolerance** | `rename` may temporarily keep alias table |
| **Input boundaries** | Structured revision order JSON; do not edit production dictionary from prose directly |

#### F-VOC-025 · Open-ended AI tagging

Reuse **`voc_entities_v1`**. Input limited to satisfaction survey open-ended text; `module_name` may be added as extension field.

#### F-VOC-015 · Public sentiment weak monitoring · `pr_hotspot_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Public text snippet → `topic`, `sentiment`, `severity_risk_level`, `source_url` (may be synthetic), `sample_voice` |
| **Success criteria** | Risk level missed (should be P0/P1) =0; topic non-empty |
| **Tolerance** | URL may be synthetic; no full-web recall required |
| **Input boundaries** | Free public text snapshot `.txt/.json`; no paid social API |

#### F-VOC-017 · Emotion map slice · `emotion_slice_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Tagged set + dimension key → `dim_key(region\|store\|channel)`, `dim_value`, `neg_ratio`, `feedback_cnt`, `top_themes[]` |
| **Success criteria** | Aggregation key valid; counts match members |
| **Tolerance** | Sparse dimension (&lt;10 items) marked `weak` |
| **Input boundaries** | Structured VoC records only; not free text |

---

### 2.3 Data / Digital assets / Strategy & Brand

#### F-DAT-006 / F-BRD-005 · Matrix account monitoring · `matrix_account_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Account weekly report semi-structured text/table → `channel_account_id`, `platform`, `post_cnt`, `play_cnt`, `interact_cnt`, `period` |
| **Success criteria** | Account ID master-data alignment ≥90%; numeric parse accuracy ≥95% |
| **Tolerance** | Missing metrics → `null` + `needs_human_review` |
| **Input boundaries** | CSV/JSON wide table, Markdown table; no raw short-video files |

#### F-DAT-012 · Digital asset structuring · `asset_struct_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Document metadata → `asset_id`, `title`, `doc_type`, `kb_domain`, `keywords[]`, `summary≤200 chars` |
| **Success criteria** | Required metadata 100%; `kb_domain` ∈ allowed domains |
| **Tolerance** | Summary may be empty on extract failure |
| **Input boundaries** | PDF/Word **extracted text**, MD; video subtitles only; no layout reconstruction |

#### F-DAT-013 · Smart CS platform

Ticket-fill segment reuses `ticket_draft_v1`; NLP tagging segment reuses `voc_entities_v1`. No standalone schema.

#### F-STR-005 · Brand strategy signal · `brand_signal_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Sentiment summary + competitor paragraph → `signal_type(sentiment\|competitor)`, `claim`, `sentiment`, `period`, `severity_risk_level?` |
| **Success criteria** | `claim` non-empty; type enum valid |
| **Tolerance** | Competitor names use fictional codes |
| **Input boundaries** | Quarterly/sentiment summary text; not raw crawler HTML corpus |

#### F-BRD-008 · MI semantics · `mi_semantic_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Website/speech/CS script comparison → `statement`, `channel`, `consistency_score_0_1`, `conflict_flag`, `evidence_spans[]` |
| **Success criteria** | Conflict missed (obvious contradiction) ≤10% |
| **Tolerance** | Score ±0.15 |
| **Input boundaries** | Paired text JSON; reject single-sided text |

#### F-BRD-009 · Full-media sentiment · `pr_monitor_v1`

Extends `pr_hotspot_v1`: adds `media_tier`, `volume_proxy`, `alert_flag`. Input is monitoring snapshot JSONL.

#### F-BRD-013 · BVP first test · `bvp_test_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Survey open responses → `bvp_candidate_id`, `memorability`, `understandability`, `purchase_intent` (1–5 or null) |
| **Success criteria** | Scale fields in range or null; parse rate ≥90% |
| **Tolerance** | Non-scale sentence → null + review |
| **Input boundaries** | Survey export CSV/JSON; not interview recording |

#### F-BRD-014 · Social image diagnosis · `image_diag_v1`

Extract `image_dimension`, `observed_score`, `expected_score`, `gap`, `sample_voice`. Input is aggregated survey + sentiment summary.

#### F-BRD-015 · App experience audit · `ux_audit_v1`

Extract `feature_name`, `brand_consistency_score`, `issue_tags[]`, `severity`. Input is review notes text/table.

#### F-BRD-017 · NPS real-time NLP

Single open feedback reuses `voc_entities_v1`; optional `nps` numeric field must be preserved (from form, not extracted).

---

### 2.4 Order policy / Channel / Territory

#### F-OPS-004 · Sales policy parsing · `policy_parse_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Policy text → `policy_id?`, `rebate_tiers[]{tier_name, threshold_qty, rebate_rate}`, `effective_from`, `effective_to`, `constraints[]` |
| **Success criteria** | Tier numeric parse accuracy ≥90%; dates valid |
| **Tolerance** | Ambiguous tier → review; do not invent rates |
| **Input boundaries** | Policy PDF **text layer**/MD; reject scans without OCR |

#### F-OPS-011 · Benchmark replication path · `benchmark_actions_v1`

Extract `benchmark_dealer_id`, `actions[]{action, priority, evidence}`. Input is benchmark case memo text. Success: ≥3 non-empty actions; paraphrase tolerated.

#### F-WZ-004 · Guide efficiency · `guide_efficacy_v1`

Extract `guide_id`, `channel_account_id`, `eff_score`, `issues[]`, `suggestions[]`. Input is efficiency report + short comments.

---

### 2.5 Manufacturing & Quality

#### F-MFG-002 · PDA binding · `pda_bind_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Scan/ledger row → `vin`, `frame_part_no`, `station_id`, `bound_at`, `operator_id` |
| **Success criteria** | VIN/part number format 100% valid; binding keys complete |
| **Tolerance** | None |
| **Input boundaries** | PDA JSON/CSV row; not free narrative (narrative → manual) |

#### F-MFG-006 · Trace package · `trace_package_v1`

Extract `vin`, `batch_no`, `qc_pass`, `trace_package_uri`, `component_ids[]`. Input is release record structured row + summary. Success: VIN + `qc_pass` required.

---

### 2.6 Product / Finance / HR / Legal / IT / User Ops

#### F-PRD-001 · Competitor card · `competitor_card_v1`

Extract `competitor_code` (fictional), `price_band`, `promotion_claim`, `reputation_tags[]`, `period`. Input: public web plain-text snapshot. Success: field non-empty rate ≥80%; no real brand names.

#### F-PRD-004 · Patent clustering · `patent_cluster_v1`

Extract `cluster_id`, `tech_theme`, `maturity_level(enum)`, `patent_ids[]`, `summary`. Input: patent abstract JSON list.

#### F-FIN-001 · Three-way match · `tri_doc_match_v1`

| Dimension | Definition |
|-----------|------------|
| **What to extract** | Invoice/contract/receipt text → `invoice_no`, `po_no`, `amount`, `currency`, `vendor_name`, `mismatch_fields[]` |
| **Success criteria** | Doc number/amount extract accuracy ≥95%; mismatch field precision ≥85% |
| **Tolerance** | OCR noise on amount ±0.01 acceptable |
| **Input boundaries** | Document OCR text or JSON; image originals belong to Vision upstream |

#### F-HR-002 · Job match · `job_match_v1`

Extract `candidate_id?`, `skill_tags[]`, `matched_job_ids[]`, `match_score`. Input: resume plain text (synthetic). PII must be redacted.

#### F-LEG-001 · Contract risk · `contract_risk_v1`

Extract `clause_id`, `risk_type`, `severity(P0-P2)`, `excerpt`, `suggestion`. Input: contract clause text. Success: high-risk clause missed ≤5%.

#### F-UO-006 · Renewal intent · `renew_intent_v1`

Extract `customer_id`, `intent_level(high\|mid\|low)`, `intent_evidence`, `paid_intent_flag`. Input: outbound call transcript. Connects to Rule+LLM routing; Extraction outputs structured intent only.

#### F-UO-010 · FAQ digest · `faq_digest_v1`

Extract `question`, `answer_summary`, `source_feedback_ids[]`, `kb_domain`. Input: high-frequency question cluster text.

#### F-UO-011 · Segment features · `segment_feat_v1`

Extract `segment_name`, `rules_or_features{}`, `size_estimate?`. Input: feature description / SQL comments / ops notes (not replacing data warehouse).

#### F-UO-015 · KOC candidate · `koc_candidate_v1`

Extract `user_id`, `koc_score`, `evidence_tags[]`. Input: community interaction wide table + short posts.

#### F-UO-016 · UGC text moderation · `ugc_moderation_v1`

Extract `content_id`, `violate_flag`, `violate_categories[]`, `severity`. Image portion belongs to Vision; this schema is text only.

#### F-IT-001 · Process redundancy · `process_dup_v1`

Extract `process_a`, `process_b`, `overlap_score`, `redundant_steps[]`. Input: process description MD/BPMN export text.

---

## 3. Validation and persistence conventions

| Step | Requirement |
|------|-------------|
| 1. validate | Output must pass corresponding JSON Schema; on failure do not write to store |
| 2. Dictionary alignment | All `tag_*` must resolve in `data/vocab/tag_vocabulary.json` (Demo) |
| 3. Shared output | Demo path: `write_ai_output` → Store/`AIOutput` |
| 4. Doc location | This contract: `docs/extraction/01-phase-1-output-schema-success-criteria-input-boundaries.md` |
| 5. Machine schema | `docs/extraction/schemas/*.json` (Demo: two implemented; placeholders may add files as needed) |

---

## 4. Phase 1 acceptance checklist (Extraction)

- [x] Every department/feature has **what to extract / success criteria / input boundaries**
- [x] Demo: `ticket_draft_v1`, `voc_entities_v1` have machine-readable schemas
- [x] Implement `agents/extraction/` control loop and attach `ticket_fields`, `voc_entities`
- [x] Gold sets (≥20 ticket-fill + ≥20 VoC) pass accuracy thresholds (see Phase 4 eval report)
- [x] Story1 optional path: `extraction + voc_tagging` → `AIOutput`

---

## 5. Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-05 | Phase 1 contract first release: all feature cards + Demo dual schema |
