#!/usr/bin/env bash
# Copyright (c) 2026 Akihisa Ono
# SPDX-License-Identifier: MIT
# RPOS-SOURCE-LANG: en
set -euo pipefail

ARCHIFY_ROOT="${ARCHIFY_ROOT:-.archify-tool/archify}"
OUTPUT_DIR="${OUTPUT_DIR:-site/visuals}"

CLI="$ARCHIFY_ROOT/bin/archify.mjs"
if [[ ! -f "$CLI" ]]; then
  echo "Archify CLI not found at $CLI" >&2
  exit 2
fi

mkdir -p "$OUTPUT_DIR"

build_one() {
  local type="$1"
  local source="$2"
  local output="$3"
  node "$CLI" validate "$type" "$source" --quality showcase --json
  node "$CLI" deliver "$type" "$source" "$output" --quality showcase --json
  test -s "$output"
}

build_one lifecycle \
  visuals/archify/rpos-responsibility-lifecycle.lifecycle.json \
  "$OUTPUT_DIR/rpos-responsibility-lifecycle.html"

build_one architecture \
  visuals/archify/rpos-operational-architecture.architecture.json \
  "$OUTPUT_DIR/rpos-operational-architecture.html"

build_one dataflow \
  visuals/archify/rpos-assurance-evidence-flow.dataflow.json \
  "$OUTPUT_DIR/rpos-assurance-evidence-flow.html"

python - <<'PY'
from pathlib import Path
expected = {
    'rpos-responsibility-lifecycle.html',
    'rpos-operational-architecture.html',
    'rpos-assurance-evidence-flow.html',
}
root = Path('site/visuals')
missing = sorted(name for name in expected if not (root / name).is_file() or (root / name).stat().st_size == 0)
if missing:
    raise SystemExit(f'Archify visual outputs missing: {missing}')
print('Archify visual outputs verified: ' + ', '.join(sorted(expected)))
PY
