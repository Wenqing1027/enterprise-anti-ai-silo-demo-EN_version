# Extraction · Phase 3: Control loop implementation and wiring

> **Implementation doc · Extraction Phase 3** (depends on [Phase 1](./01-phase-1-output-schema-success-criteria-input-boundaries.md) · [Phase 2](./02-phase-2-workflow-stop-conditions-system-prompt.md))  
> Version: V1.0 · 2026-08-05  
> Control loop code: `agents/extraction/` · CLI / API wired

---

## 1. Phase deliverables

| Item | Path / notes |
|------|--------------|
| Control loop | `agents/extraction/agent.py`: `schema → extract → validate` (max 1 retry on failure) |
| Prompt | `agents/extraction/prompts.py` (section order per Phase 2) |
| Validation gates | `agents/extraction/validate.py` (Pydantic + dictionary + block-tag correction) |
| Skills | `skills/ticket_fields/`, `skills/voc_entities/`, `skills/voc_tagging/` (alias) |
| LLM key | `DEEPSEEK_EXTRACTION_API_KEY` in `.env` (falls back to `DEEPSEEK_API_KEY`) |
| CLI | `python apps/cli.py --agent-type extraction --skill …` |
| API | `POST /v1/extraction/runs` |
| Seeds | `data/seeds/story_1_ticket_fields.json`, `story_1_voc_entities.json` |

---

## 2. Environment variables (never commit)

Configure at repo root in `.env` (gitignored):

```bash
# Shared with ReAct, etc.
DEEPSEEK_API_KEY=sk-...

# Extraction-only (recommended separate key)
DEEPSEEK_EXTRACTION_API_KEY=sk-...
DEEPSEEK_EXTRACTION_TEMPERATURE=0.1
# DEEPSEEK_EXTRACTION_MODEL=deepseek-chat
```

Load path: `shared/llm/client.py` → `load_llm_config(profile="extraction")`.

> **Security**: API keys belong only in `.env` / environment variables — **never** in docs, code, or commits. If a key was exposed in chat, rotate it in the DeepSeek console.

---

## 3. How to run

```bash
cd enterprise-anti-ai-silo-demo
source .venv/bin/activate   # if venv exists
# confirm DEEPSEEK_EXTRACTION_API_KEY is set in .env

# Ticket field extraction (Story1 Extraction path)
python apps/cli.py --agent-type extraction --skill ticket_fields \
  --input data/seeds/story_1_ticket_fields.json --json-out

# VoC tagging
python apps/cli.py --agent-type extraction --skill voc_entities \
  --input data/seeds/story_1_voc_entities.json --json-out

# Alias skill
python apps/cli.py --agent-type extraction --skill voc_tagging \
  --input data/seeds/story_1_voc_entities.json

# Validate only, no write
python apps/cli.py --agent-type extraction --skill ticket_fields \
  --input data/seeds/story_1_ticket_fields.json --no-write

# Smoke script
python scripts/smoke_extraction.py
```

API example:

```bash
curl -s http://127.0.0.1:8000/v1/extraction/runs \
  -H 'Content-Type: application/json' \
  -d '{
    "skill_id": "ticket_fields",
    "input": {
      "text": "Complaint: store did not follow warranty policy for battery replacement; ticket open over 7 days.",
      "customer_id": "CUS-10057",
      "vin": "QS0F65B984410D7B6",
      "channel": "400"
    }
  }'
```

---

## 4. Code map

| File | Role |
|------|------|
| `agents/extraction/skill_schema.py` | Extraction Skill contract (includes `payload_schema`) |
| `agents/extraction/skill_loader.py` | Load YAML |
| `agents/extraction/prompts.py` | System / user / retry messages |
| `agents/extraction/validate.py` | JSON strip, schema, block gates |
| `agents/extraction/agent.py` | Control loop + `write_ai_output` |
| `apps/skill_dispatch.py` | ReAct / Extraction skill routing |
| `apps/cli.py` | `--agent-type extraction` |
| `apps/api.py` | `POST /v1/extraction/runs` |
| `apps/catalog.py` | `F-SVC-001-EXT`, `F-VOC-002` demo_ready |

Boundary with ReAct:

- ReAct Skill: has `allowed_tools`, no `payload_schema`
- Extraction Skill: has `payload_schema`; LLM path **does not call tools**; after validation, code calls `write_ai_output`

---

## 5. Success semantics

| `stop_reason` | Meaning |
|---------------|---------|
| `validated` | Schema + gates passed (AIOutput may be written) |
| `bad_input` | Empty text / over length limit |
| `schema_fail` | Still invalid after retry |
| `llm_error` | DeepSeek call failed |
| `write_fail` | Validated but shared-layer write failed |
| `config_error` | Missing dictionary, etc. |

Demo acceptance: `ok=true` and non-empty `ai_output_id` (when not using `--no-write`).

---

## 6. Phase 3 checklist

- [x] `agents/extraction/` control loop
- [x] Demo Skills ×3 (including `voc_tagging` alias)
- [x] Extraction-dedicated API key slot
- [x] CLI + API wired
- [x] Seeds + smoke script
- [x] This implementation doc
- [x] Gold-set batch accuracy eval (Phase 4, see [04](./04-phase-4-gold-standard-eval-and-ui-wiring.md))

---

## 7. Next step (Phase 4)

Shipped in [04-phase-4-gold-standard-eval-and-ui-wiring.md](./04-phase-4-gold-standard-eval-and-ui-wiring.md).

---

## 8. Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-05 | Control loop shipped, CLI/API, dedicated key, docs |
