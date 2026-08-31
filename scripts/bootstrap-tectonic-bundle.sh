#!/bin/sh
set -eu

PYTHON=${PYTHON:-python3}
TECTONIC=${TECTONIC:-tectonic}
INPUT='paper/kourovka-18-68.tex'

metadata_value() {
    "$PYTHON" - "$1" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path("artifact-metadata.json").read_text(encoding="utf-8"))[sys.argv[1]])
PY
}

EXPECTED_TECTONIC=$(metadata_value tectonic_version)
EXPECTED_EPOCH=$(metadata_value source_date_epoch)
BUNDLE_URL=$(metadata_value tectonic_bundle_url)
BUNDLE_CONTENT_SHA256=$(metadata_value tectonic_bundle_content_sha256)
SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$EXPECTED_EPOCH}

if [ "$($TECTONIC --version)" != "Tectonic $EXPECTED_TECTONIC" ]; then
    echo "bundle bootstrap: Tectonic $EXPECTED_TECTONIC is required" >&2
    exit 1
fi
if [ "$SOURCE_DATE_EPOCH" != "$EXPECTED_EPOCH" ]; then
    echo "bundle bootstrap: SOURCE_DATE_EPOCH must be $EXPECTED_EPOCH" >&2
    exit 1
fi
if [ ! -f "$INPUT" ]; then
    echo "bundle bootstrap: missing $INPUT" >&2
    exit 1
fi

tmpdir=$(mktemp -d "${TMPDIR:-/tmp}/k186-bundle.XXXXXX")
trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
cp "$INPUT" "$tmpdir/kourovka-18-68.tex"
(
    cd "$tmpdir"
    SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH TZ=UTC "$TECTONIC" \
        --bundle "$BUNDLE_URL" \
        -Z deterministic-mode \
        --keep-logs \
        kourovka-18-68.tex >/dev/null
)

cache_dir=$($TECTONIC -X show user-cache-dir 2>/dev/null)
hash_file="$cache_dir/hashes/https,58,,47,,47,relay.fullyjustified.net,47,default_bundle_v33.tar"
if [ ! -f "$hash_file" ]; then
    echo 'bundle bootstrap: Tectonic did not create the bundle hash record' >&2
    exit 1
fi
cached_bundle_hash=$(tr -d '\r\n' < "$hash_file")
if [ "$cached_bundle_hash" != "$BUNDLE_CONTENT_SHA256" ]; then
    echo "bundle bootstrap: bundle content hash mismatch: $cached_bundle_hash" >&2
    exit 1
fi
printf '%s\n' "TECTONIC BUNDLE BOOTSTRAP PASSED: $BUNDLE_CONTENT_SHA256"
