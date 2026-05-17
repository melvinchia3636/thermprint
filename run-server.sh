#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cleanup() {
  echo ""
  echo "Shutting down..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
  echo "Done."
}
trap cleanup EXIT INT TERM

echo "Starting backend..."
cd "$SCRIPT_DIR/server"
PYTHONPATH="$SCRIPT_DIR" uv run uvicorn server.app.main:app --reload --host 0.0.0.0 --port 558 &
BACKEND_PID=$!

echo "Starting frontend..."
cd "$SCRIPT_DIR/client"
bun run dev --host --port 557 &
FRONTEND_PID=$!

wait
