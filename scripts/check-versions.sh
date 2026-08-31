#!/bin/sh
set -eu

GAP=${GAP:-gap}
TECTONIC=${TECTONIC:-tectonic}
PYTHON=${PYTHON:-python3}

metadata_value() {
    "$PYTHON" - "$1" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path("artifact-metadata.json").read_text(encoding="utf-8"))[sys.argv[1]])
PY
}

EXPECTED_TECTONIC=$(metadata_value tectonic_version)

"$GAP" --quitonbreak -q scripts/check-environment.g

tectonic_version=$($TECTONIC --version)
if [ "$tectonic_version" != "Tectonic $EXPECTED_TECTONIC" ]; then
    echo "environment check: expected Tectonic $EXPECTED_TECTONIC, got: $tectonic_version" >&2
    exit 1
fi

"$PYTHON" - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise RuntimeError(f"environment check: Python >=3.10 required, got {sys.version}")
print(f"PYTHON ENVIRONMENT PASSED: {sys.version.split()[0]}")
PY
