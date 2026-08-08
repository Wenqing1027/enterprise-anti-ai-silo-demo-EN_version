#!/usr/bin/env bash
# Story 1：assetize output（ Agent，）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "[demo] Story A — fetcher → write_ai_output（Qingshu Mobility）"
python3 "$ROOT/scripts/smoke_foundation.py"
