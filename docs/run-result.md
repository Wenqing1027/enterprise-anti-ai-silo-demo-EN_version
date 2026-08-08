# Unified RunResult (Phase D)

> Version: synced with `RUN_RESULT_VERSION` in `apps/run_result.py`  
> Source of truth: each loop’s `POST /v1/*/runs` and `POST /v1/runs` responses normalized via `wrap_run_result`  
> Machine-readable: `GET /v1/meta` → `run_result` / `run_result_version`

## Common fields (frontend primary)

| Field | Type | Notes |
|-------|------|-------|
| `run_id` | string | Run ID |
| `control_loop` | string | `retrieve` \| `act` \| `extract` \| `plan` |
| `skill_id` | string | Skill |
| `ok` | bool | Success flag |
| `final_text` | string | Final answer text |
| `steps` | array | Steps |
| `ai_output_ids` | string[] | Written shared output IDs |
| `error` | string\|null | Failure reason when applicable; usually null on success |
| `extensions` | object | Loop-specific extension bag |

Compatibility alias: `final_answer` ≡ `final_text` (kept during transition; new code should use `final_text`).

## Per-loop top-level extensions

| control_loop | Fields |
|--------------|--------|
| extract | `payload` |
| retrieve | `citations` |
| plan | `gate`: `blocked` · `reason` · `tag_ids` (also `allow_outreach`) |
| act | (no required top-level extension; details in `extensions.success_flags`) |

## Common `extensions` keys

`stop_reason` · `feature_id` · `department_id` · `layout` · `tone_label` · `success_flags` · `plan` (Plan short plan body) · `api_path` · `resolved_via`

## Acceptance

```bash
python3 scripts/smoke_run_result.py
```
