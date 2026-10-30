#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 publish-to-github.py "$@"
fi
exec python publish-to-github.py "$@"
