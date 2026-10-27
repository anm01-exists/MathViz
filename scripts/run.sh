#!/usr/bin/env bash
# Launch the MathViz API server (reload mode).
set -euo pipefail
cd "$(dirname "$0")/.."
exec python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000