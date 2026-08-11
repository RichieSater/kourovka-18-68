#!/bin/sh
set -eu

GAP=${GAP:-gap}
TECTONIC=${TECTONIC:-tectonic}
PYTHON=${PYTHON:-python3}

"$GAP" --quitonbreak -q scripts/check-environment.g

tectonic_version=$($TECTONIC --version)
if [ "$tectonic_version" != "Tectonic 0.17.0" ]; then
    echo "environment check: expected Tectonic 0.17.0, got: $tectonic_version" >&2
    exit 1
fi

"$PYTHON" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise RuntimeError(f"environment check: Python >=3.10 required, got {sys.version}")
print(f"PYTHON ENVIRONMENT PASSED: {sys.version.split()[0]}")
PY
