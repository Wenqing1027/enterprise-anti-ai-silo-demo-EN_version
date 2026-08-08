# Qingshu Mobility · Anti-AI-Silo Platform Demo (V2)

Portfolio demo for the fictional smart EV company **Qingshu Mobility**.

The platform governs **4 control loops + 3 tool classes**. Departments ship **Skills**. Shared semantics and outputs show a governable way to fight AI silos.

This repo is a runnable reference with synthetic data only. No real customer data or brands.

## Platform control loops (4)

| Loop | Directory | Status |
|------|-----------|--------|
| Retrieve | `agents/rag/` | Ready: `repair_kb` / `policy_kb` / `hr_rules` |
| Act | `agents/react/` | Ready |
| Extract | `agents/extraction/` | Ready: `ticket_fields` / `voc_*` |
| Plan | `agents/planning/` | Ready: `renewal_plan` (Story2 gate) |

Tool governance classes: **Read · Knowledge · Write/Govern** (see `shared/tools/`).

Architecture: [BLUEPRINT.md](./BLUEPRINT.md)  
Design decisions: [docs/design-decisions.md](./docs/design-decisions.md)  
Consulting narrative: [docs/consulting-narrative.md](./docs/consulting-narrative.md)

## How to run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set DEEPSEEK_API_KEY

# CLI (Act · Story1)
python3 apps/cli.py --agent-type act --skill fill_ticket \
  --input data/seeds/story_1_fill_ticket.json

# CLI (Extract · Story1)
python3 apps/cli.py --agent-type extract --skill ticket_fields \
  --input data/seeds/story_1_ticket_fields.json

# CLI (Retrieve)
python3 apps/cli.py --agent-type retrieve --skill repair_kb \
  --input '{"query":"How do I troubleshoot range below the rated value?"}'

# CLI (Plan · Story2 gate; needs shared complaint tags first)
python3 apps/cli.py --agent-type plan --skill renewal_plan \
  --input data/seeds/story_2_renewal_block.json

# Gold evaluation
python3 scripts/eval_extraction.py
python3 scripts/eval_rag.py

# Plan smoke (upstream writes tags → separate gate run blocks)
python3 scripts/smoke_planning.py

# API (business try-run / ops troubleshooting)
bash scripts/ensure_api.sh
# Business http://127.0.0.1:8000/business
# Ops http://127.0.0.1:8000/ops
# OpenAPI /docs
```

## Architecture highlights (V2)

- **Product trio**: Control Loops + Tools + Skills (one function = one Skill)
- **Platform owns loops and tools**: departments ship Skills only; no copied loops or DataFetchers
- **Anti-silo in the shared layer**: tag vocabulary, shared outputs, capability catalog, plus Write/Govern tools
- **Cross-function via a new run on the shared layer**: `department_flows` documents relations; no auto multi-Skill run; no Agent-to-Agent chat

## Note

This project is a portfolio reference for platformized Loops + Tools + Skills.  
It is not a live enterprise platform and not a multi-department production delivery.
