#!/usr/bin/env bash
# Story 2：typeconsumer（ Story A ）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "[demo] Story B — read_ai_outputs / check_outreach_block（Qingshu Mobility）"
echo "[demo] description：Story B  smoke_foundation.py "
python3 "$ROOT/scripts/smoke_foundation.py"
