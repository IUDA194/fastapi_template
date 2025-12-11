#!/usr/bin/env bash
set -euo pipefail

echo "▶ Ruff check..."
uv run ruff check . --fix

echo "▶ Ruff format..."
uv run ruff format .

echo "▶ mypy typecheck..."
uv run mypy app tests

echo "✅ All checks passed."

