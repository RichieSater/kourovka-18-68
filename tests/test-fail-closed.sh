#!/bin/sh
set -eu

GAP=${GAP:-gap}
PYTHON=${PYTHON:-python3}

if printf 'Error("intentional failure control");\n' | "$GAP" --quitonbreak -q >/dev/null 2>&1; then
    echo 'fail-closed test: GAP --quitonbreak returned zero on Error' >&2
    exit 1
fi

"$PYTHON" -O tests/check-tomlib-scan.py
"$PYTHON" -O tests/check-factor-free-scan.py
"$PYTHON" -O scripts/check-public-corpus.py
printf '%s\n' 'FAIL-CLOSED CONTROLS PASSED'
