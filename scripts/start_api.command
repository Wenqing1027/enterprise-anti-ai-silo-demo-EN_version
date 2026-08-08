#!/bin/bash
#  open  Terminal  API
cd "$(dirname "$0")/.." || exit 1
exec bash scripts/run_api.sh
