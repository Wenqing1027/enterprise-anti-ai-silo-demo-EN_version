# Extraction Agent · Phase 2: Workflow · Stop Conditions · System Prompt

> **Core reference · Extraction Phase 2** (depends on [Phase 1](./01-phase-1-output-schema-success-criteria-input-boundaries.md))  
> Control loop: `schema → extract → validate` (**not** a ReAct multi-step tool loop)  
> LLM: DeepSeek (OpenAI-compatible) · `DEEPSEEK_API_KEY` env var only  
> Version: V1.0 · 2026-08-05  
> **Conclusion for this step**: After Phase 1 locks the schema, **the next step is building the System Prompt** (including workflow and stop conditions), then implementing the code control loop.

---

## 0. Division of labor vs ReAct

| | ReAct | Extraction |
|--|-------|------------|
| Main loop | think → act → observe | **schema → extract → validate** |
| Primary output | Natural-language final answer + optional tool side effects | **Only valid output = JSON compliant with schema** |
| Prompt focus | Tool allowlist and multi-step reasoning | Schema constraints, enum dictionary, confidence and human review |
| Demo Skills | `fill_ticket`, etc. | `ticket_fields`, `voc_entities` |

> Ticket fill in ReAct **calls** the `extract_ticket_fields` tool; the Extraction brain **directly** structurally extracts from text. Both share `ticket_draft_v1` / `voc_entities_v1` to avoid field drift.

---

## 1. Workflow (unified control loop)

All Extraction Skills **share** the same loop; differences are only in injected schema, tag dictionary, and Skill slot.

```text
Input (skill_id + text + optional known keys)
        │
        ▼
┌────────────────────────────┐
│ Load Skill + target schema │  ticket_draft_v1 / voc_entities_v1
│ Assemble System Prompt     │  See §3 section order
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐
│  LLM single-pass extract   │  Requirement: output JSON object only
│  (DeepSeek)                │
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐
│  Validate                  │  JSON parse → JSON Schema / Pydantic
│  - Fail: retry at most 1×  │  (feed validation errors back)
│  - Still fail: reject, no  │
│    write to store          │
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐
│  Post-gates (code, not     │  Dictionary existence, block tags,
│  model)                    │  VIN/CUS format
│  Optional write_ai_output  │  Story1 assetization
└────────────────────────────┘
```

### 1.1 Single-step semantics

| Step | Name | Who | Output |
|------|------|-----|--------|
| Schema | Lock target structure | Control loop load | Schema text injected into prompt |
| Extract | Structured extraction | DeepSeek | Candidate JSON string |
| Validate | Validation + gates | Code | Compliant payload or `reject` |

### 1.2 Expected code entry points (Phase 3 implementation)

| Path | Responsibility |
|------|----------------|
| `agents/extraction/prompts.py` | Code form of this document |
| `agents/extraction/agent.py` | schema → extract → validate |
| `skills/ticket_fields/skill.yaml` | Ticket-fill extract Skill |
| `skills/voc_entities/skill.yaml` (or `voc_tagging`) | VoC tagging Skill |
| `apps/cli.py --agent-type extraction` | Unified entry |

---

## 2. Stop conditions

### 2.1 Global stop

| Condition ID | Trigger | Behavior |
|--------------|---------|----------|
| `E-OK` | JSON parse success, schema validation pass, post-gates pass | `stop_reason=validated`, may write `AIOutput` |
| `E-RETRY` | First validation failure | Feed errors back, **extract once more only** |
| `E-SCHEMA-FAIL` | Still non-compliant after retry | `stop_reason=schema_fail`, **do not write to store** |
| `E-EMPTY` | Model returns empty / non-JSON / markdown fence that fails after stripping | Count as failure; after one retry same as above |
| `E-DICT-MISS` | `tag_id` not in TagVocabulary | `needs_human_review=true`; Demo may downgrade to nearest valid tag **only when** non-block scenario; block scenario → `schema_fail` |
| `E-LLM-ERROR` | API failure and retries exhausted | `stop_reason=llm_error` |
| `E-INPUT-REJECT` | Input out of bounds (empty text, untruncated oversize, raw audio/video) | Do not call model, `stop_reason=bad_input` |

### 2.2 Skill-specific success

| Skill | Success condition |
|-------|-------------------|
| `ticket_fields` | Output passes `ticket_draft_v1`; includes `ticket_type/tag_id/sentiment/desc_text/is_complaint`; optionally `write_ai_output` |
| `voc_entities` | Output passes `voc_entities_v1`; `tag_id` ∈ dictionary; block tags must not be missed on source text (code gate re-check) |

### 2.3 Hard business stops (aligned with Phase 1)

- Non-compliant JSON **never** written to `AIOutput`
- Synthetic VIN must start with `QS0…`; invalid format → `null` + `needs_human_review`
- Do not output real phone numbers in plaintext; suspected PII in `desc_text`/`sample_voice` redacted as `***`
- Do not use real automaker/customer brand names

---

## 3. System Prompt structure

Concatenation order is **uniquely determined** by constant `EXTRACTION_PROMPT_SECTION_ORDER` (implement in `agents/extraction/`; callers must not reorder):

```text
[A_base]           Company identity + Extraction hard rules + anti-silo
[B_schema]         Target JSON Schema for this run (full injection)
[C_goal]           Skill goal + success criteria
[D_dictionary]     Allowed tags/enum dictionary (skip if empty)
[E_extract_rules]  Extraction rules and confidence rules
[F_output]         Output discipline: one JSON object only
[G_security]       Security boundary summary
```

Suggested implementation:

```python
EXTRACTION_PROMPT_SECTION_ORDER = (
    "A_base",
    "B_schema",
    "C_goal",
    "D_dictionary",
    "E_extract_rules",
    "F_output",
    "G_security",
)
```

---

## 4. Base prompt (shared by all Skills)

> At implementation, copy verbatim into `agents/extraction/prompts.py` → `BASE_SYSTEM`.

```text
You are the Extraction Agent (structured extraction) inside the fictional company "Qingshu Mobility".
Architecture principle: multiple departments share the same data fields and tag dictionary; you only execute the extraction task for this Skill — do not play customer service, renewal outreach, or a general enterprise brain.

Hard rules:
1. Your only task: read input text and extract structured fields per the given JSON Schema.
2. Output one JSON object only; no Markdown, explanation, preamble, or code fences.
3. Do not invent master data: customer_id / vin not present in text must be null, with needs_human_review=true.
4. Synthetic VIN must start with QS0; output null when unconfirmed — do not fabricate VIN.
5. Enum fields must fall within Schema allowed values; when uncertain:
   - ticket_type → other
   - fault_category → other
   - sentiment → neu (but complaint/exposure/safety hazard strong negatives must be neg)
6. tag_id must come from the tag dictionary provided this run; do not invent TAGs.
7. Block tags (TAG-open-complaint, TAG-reputation-risk, TAG-safety-hazard): when source text has evidence, primary tag or secondary_tag_ids must hit one — missed tags are unacceptable.
8. Cross-department collaboration relies on structured output to the shared layer (AIOutput); you do not run multi-step database dialogue (that is ReAct).
9. Use English for text fields (desc_text / sample_voice / problem_theme, etc.).
10. Security boundaries are enforced by code gates; do not attempt to bypass validation.
```

---

## 5. Demo Skill prompt slots

### 5.1 `ticket_fields` (F-SVC-001 · Service Division)

**[C_goal]**

```text
[Task goal]
- Goal: From CS/user text, produce ticket draft ticket_draft_v1 for agent confirmation or shared output write.
- Success criteria: Output passes ticket_draft_v1; ticket_type/tag_id/sentiment/desc_text/is_complaint complete; no invented IDs.
- Department tone: cautious confirmation style (objective field wording; no promise of compensation/guaranteed repair).
```

**[D_dictionary]** (Demo leaf tags; do not select root nodes as primary tag)

```text
[Tag dictionary · allowed tag_id]
Product: TAG-short-range, TAG-weak-power, TAG-noise, TAG-brake, TAG-slow-charging, TAG-controller-fault, TAG-battery-swelling, TAG-dashboard-blackout
Service: TAG-warranty-dispute, TAG-slow-onsite-service, TAG-poor-attitude, TAG-parts-stockout
App: TAG-pairing-failure, TAG-gps-drift, TAG-renewal-entry-hard-to-find, TAG-push-spam
Channel: TAG-non-exclusive-display, TAG-vi-violation, TAG-overstock-no-sales
Risk / block: TAG-open-complaint, TAG-reputation-risk, TAG-safety-hazard

[Other enums]
ticket_type: fault | consult | complaint | other
fault_category: battery | motor | brake | controller | charging | dashboard | frame | lighting | tire | other
ticket_channel: 400 | App | e-commerce | store | community
ticket_status: draft default open
sentiment: pos | neu | neg
```

**[E_extract_rules]**

```text
[Extraction rules]
1. desc_text: keep user issue summary, ≤1000 chars; redact phone numbers.
2. If input or known keys contain CUS-digits / QS0… VIN, write to corresponding fields; otherwise null.
3. When both fault and complaint intent appear, ticket_type prefers complaint, is_complaint=true.
4. Fault tickets should fill fault_category; consult may fill consult_category short label.
5. tag_id: pick one that best summarizes the main issue; when block evidence exists, do not pick unrelated minor product tag as primary (may use block tag as primary, or product issue primary + block in secondary).
6. confidence: high confidence ≥0.8; typical 0.5–0.7; missing ID or ambiguous sentence ≤0.5 with needs_human_review=true.
7. ticket_channel: prefer known channel; otherwise infer from text, default 400.
```

**[F_output]**

```text
[Output discipline]
- Output one JSON object only; key set must match ticket_draft_v1.
- Do not wrap in ```json code fences.
- Do not append a second explanatory paragraph.
```

**[G_security]**

```text
[Security boundaries]
- No real customer PII, real brand names, or API keys.
- No promise of compensation/guaranteed repair (this Agent does not output reassurance scripts).
- Invalid VIN → null; do not "complete" or fabricate.
```

**[B_schema]**: Inject full [`schemas/ticket_draft_v1.json`](./schemas/ticket_draft_v1.json) (at implementation, `json.dumps` with indent).

---

### 5.2 `voc_entities` (F-VOC-002 · UX Research / Ops)

**[C_goal]**

```text
[Task goal]
- Goal: From voice text, extract VoC entity voc_entities_v1 (tags, sentiment, theme, risk).
- Success criteria: Pass voc_entities_v1; tag_id ∈ dictionary; accurate sentiment; zero missed block tags.
- Department tone: neutral labeling; no reassurance, no ops scripts.
```

**[D_dictionary]**: Same tag dictionary as §5.1; additionally emphasize:

```text
[Domain mapping tag_domain]
product | service | app | channel | risk
(must match the domain of chosen tag_id in dictionary)
```

**[E_extract_rules]**

```text
[Extraction rules]
1. sample_voice: redacted representative voice, ≤500 chars; preserve user wording where possible.
2. problem_theme: short theme name (e.g. "Short range", "Slow onsite service"), aligned with primary tag semantics.
3. sentiment_score: pos≈0.3–1.0, neu≈-0.2–0.2, neg≈-1.0–-0.3.
4. Exposure/media/12315/police report → consider TAG-reputation-risk and severity_risk_level=P0|P1.
5. Fire/smoke/self-ignite/leak → TAG-safety-hazard, severity_risk_level at least P1.
6. Repeated complaints/unresolved/over 7 days open → TAG-open-complaint (block).
7. clue_confidence: sufficient evidence medium; metaphor/vague single sentence weak, with needs_human_review=true.
8. secondary_tag_ids at most 3, all in dictionary; do not duplicate primary tag_id.
```

**[F_output] / [G_security]**: Same discipline as ticket fill; schema replaced with [`schemas/voc_entities_v1.json`](./schemas/voc_entities_v1.json).

---

## 6. Assembly example (full System Prompt skeleton)

Implementation pseudocode:

```text
system = join(
  A_base,
  "[Target Schema]\n" + schema_json,
  C_goal,
  D_dictionary,          # may be empty
  E_extract_rules,
  F_output,
  G_security,
)
```

### 6.1 User message template

```text
[Skill]{skill_id}
[SchemaID]{ticket_draft_v1|voc_entities_v1}
[Input text]
{text}
[Known keys]customer_id=...; vin=...; channel=... (if any; otherwise write none)
Output one JSON object compliant with Schema only.
```

### 6.2 Validation-failure retry feedback (user append)

```text
[Validation failed · fix and output JSON only]
{validator_error_message}
Previous output (for reference, do not repeat errors verbatim):
{previous_raw}
```

---

## 7. DeepSeek call conventions

| Item | Value |
|------|-------|
| Base URL | `https://api.deepseek.com/v1` (`DEEPSEEK_BASE_URL` overridable) |
| Model | `deepseek-chat` (`DEEPSEEK_MODEL` overridable) |
| Auth | `DEEPSEEK_API_KEY` |
| Temperature | **0.0–0.2** (extraction should be stable) |
| tools | **Do not pass** (Extraction main path has no tool_calls) |
| response | Parse as pure JSON; if ```json fence present, strip then parse |
| Retry | Schema failure at most **1** feedback retry; LLM network errors per existing client retry |

Optional enhancement (not required): if API supports `response_format: json_object`, enable to improve compliance rate.

---

## 8. Alignment with Story1 / anti-silo

| Path | Description |
|------|-------------|
| A · ReAct | `fill_ticket` → tool `extract_ticket_fields` → `write_ai_output` (existing) |
| B · Extraction | `ticket_fields` or `voc_entities` → validate → `write_ai_output` (`producer_skill`=`ticket_fields`/`voc_tagging`, `consumer_allow` includes `renewal_plan`) |
| Story2 | Renewal side reads shared tags; depends on this brain **zero missed block tags** |

Demo acceptance: either A or B must run Story1; Extraction type coverage still requires B.

---

## 9. Phase 2 deliverables checklist

- [x] Confirm step 2 = System Prompt (including workflow/stop conditions)
- [x] Fix `EXTRACTION_PROMPT_SECTION_ORDER`
- [x] Base `BASE_SYSTEM` full text
- [x] Demo dual Skill C/D/E/F/G slots
- [x] User message and validation feedback templates
- [x] Coded into `agents/extraction/prompts.py` (Phase 3 complete, see [03](./03-phase-3-control-loop-implementation-and-wiring.md))

---

## 10. Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-05 | Phase 2 first release: workflow + stop conditions + full System Prompt slots |
