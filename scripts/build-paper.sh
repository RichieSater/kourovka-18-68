#!/bin/sh
set -eu

PYTHON=${PYTHON:-python3}
TECTONIC=${TECTONIC:-tectonic}
METADATA='artifact-metadata.json'
INPUT='paper/kourovka-18-68.tex'
OUTPUT='paper/kourovka-18-68.pdf'
RECEIPT='paper/BUILD-RECEIPT.txt'

metadata_value() {
    "$PYTHON" - "$1" <<'PY'
import json
import sys
from pathlib import Path
value = json.loads(Path("artifact-metadata.json").read_text(encoding="utf-8"))[sys.argv[1]]
if value is None:
    print("")
elif isinstance(value, bool):
    print(str(value).lower())
else:
    print(value)
PY
}

EXPECTED_TECTONIC=$(metadata_value tectonic_version)
BUNDLE_URL=$(metadata_value tectonic_bundle_url)
BUNDLE_CONTENT_SHA256=$(metadata_value tectonic_bundle_content_sha256)
EXPECTED_EPOCH=$(metadata_value source_date_epoch)
MANUSCRIPT_DATE=$(metadata_value manuscript_date)
PUBLICATION_STATUS=$(metadata_value publication_status)
PDF_TITLE=$(metadata_value title)
PDF_AUTHOR=$(metadata_value author)
PDF_SUBJECT=$(metadata_value pdf_subject)
EXPECTED_PDF_VERSION=$(metadata_value pdf_version)
EXPECTED_TAGGED=$(metadata_value pdf_tagged)
SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-$EXPECTED_EPOCH}

if [ "$($TECTONIC --version)" != "Tectonic $EXPECTED_TECTONIC" ]; then
    echo "paper build: Tectonic $EXPECTED_TECTONIC is required" >&2
    exit 1
fi
if [ "$SOURCE_DATE_EPOCH" != "$EXPECTED_EPOCH" ]; then
    echo "paper build: SOURCE_DATE_EPOCH must be $EXPECTED_EPOCH" >&2
    exit 1
fi
if [ "$PUBLICATION_STATUS" != 'preprint' ]; then
    echo "paper build: publication status must be preprint" >&2
    exit 1
fi
if [ "$EXPECTED_TAGGED" != 'false' ]; then
    echo 'paper build: metadata must record the intentionally untagged PDF' >&2
    exit 1
fi

cache_dir=$($TECTONIC -X show user-cache-dir 2>/dev/null)
hash_file="$cache_dir/hashes/https,58,,47,,47,relay.fullyjustified.net,47,default_bundle_v33.tar"
if [ ! -f "$hash_file" ]; then
    echo "paper build: pinned Tectonic bundle is not cached: $BUNDLE_URL" >&2
    exit 1
fi
cached_bundle_hash=$(tr -d '\r\n' < "$hash_file")
if [ "$cached_bundle_hash" != "$BUNDLE_CONTENT_SHA256" ]; then
    echo "paper build: bundle content hash mismatch: $cached_bundle_hash" >&2
    exit 1
fi

tmpdir=$(mktemp -d "${TMPDIR:-/tmp}/k186-paper.XXXXXX")
trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
mkdir "$tmpdir/one" "$tmpdir/two"

export SOURCE_DATE_EPOCH TZ=UTC
for destination in "$tmpdir/one" "$tmpdir/two"; do
    cp "$INPUT" "$destination/kourovka-18-68.tex"
    (
        cd "$destination"
        $TECTONIC \
            --bundle "$BUNDLE_URL" \
            --only-cached \
            -Z deterministic-mode \
            --keep-logs \
            kourovka-18-68.tex
    )
done

first="$tmpdir/one/kourovka-18-68.pdf"
second="$tmpdir/two/kourovka-18-68.pdf"
if ! cmp -s "$first" "$second"; then
    echo 'paper build: two clean deterministic builds differ' >&2
    exit 1
fi
for log in "$tmpdir"/*/kourovka-18-68.log; do
    if grep -Eiq 'undefined references|citation.+undefined|rerun to get cross-references right' "$log"; then
        echo "paper build: unresolved-reference diagnostic in $log" >&2
        exit 1
    fi
done

cp "$first" "$OUTPUT"
if ! command -v pdfinfo >/dev/null 2>&1; then
    echo 'paper build: pdfinfo is required for metadata checks' >&2
    exit 1
fi
pdf_metadata=$(pdfinfo "$OUTPUT")
pdf_title=$(printf '%s\n' "$pdf_metadata" | sed -n 's/^Title:[[:space:]]*//p')
pdf_author=$(printf '%s\n' "$pdf_metadata" | sed -n 's/^Author:[[:space:]]*//p')
pdf_subject=$(printf '%s\n' "$pdf_metadata" | sed -n 's/^Subject:[[:space:]]*//p')
pdf_pages=$(printf '%s\n' "$pdf_metadata" | sed -n 's/^Pages:[[:space:]]*//p')
pdf_tagged=$(printf '%s\n' "$pdf_metadata" | sed -n 's/^Tagged:[[:space:]]*//p')
pdf_version=$(printf '%s\n' "$pdf_metadata" | sed -n 's/^PDF version:[[:space:]]*//p')
if [ "$pdf_title" != "$PDF_TITLE" ]; then
    echo "paper build: unexpected PDF title: $pdf_title" >&2
    exit 1
fi
if [ "$pdf_author" != "$PDF_AUTHOR" ]; then
    echo "paper build: unexpected PDF author: $pdf_author" >&2
    exit 1
fi
if [ "$pdf_subject" != "$PDF_SUBJECT" ]; then
    echo "paper build: unexpected PDF subject: $pdf_subject" >&2
    exit 1
fi
if [ "$pdf_tagged" != 'no' ]; then
    echo "paper build: expected untagged PDF, got: $pdf_tagged" >&2
    exit 1
fi
if [ "$pdf_version" != "$EXPECTED_PDF_VERSION" ]; then
    echo "paper build: expected PDF $EXPECTED_PDF_VERSION, got: $pdf_version" >&2
    exit 1
fi
case "$pdf_pages" in
    ''|*[!0-9]*) echo "paper build: invalid page count: $pdf_pages" >&2; exit 1 ;;
esac
tex_sha=$(shasum -a 256 "$INPUT" | awk '{print $1}')
pdf_sha=$(shasum -a 256 "$OUTPUT" | awk '{print $1}')
metadata_sha=$(shasum -a 256 "$METADATA" | awk '{print $1}')
cat > "$RECEIPT" <<EOF_RECEIPT
artifact=paper/kourovka-18-68.pdf
publication_status=$PUBLICATION_STATUS
manuscript_date=$MANUSCRIPT_DATE
tectonic_version=$EXPECTED_TECTONIC
bundle_url=$BUNDLE_URL
bundle_content_sha256=$BUNDLE_CONTENT_SHA256
source_date_epoch=$SOURCE_DATE_EPOCH
timezone=UTC
deterministic_mode=true
clean_builds_compared=2
metadata_sha256=$metadata_sha
tex_sha256=$tex_sha
page_count=$pdf_pages
tagged_pdf=false
pdf_sha256=$pdf_sha
EOF_RECEIPT
printf 'PAPER BUILD PASSED: %s (%s pages, untagged)\n' "$pdf_sha" "$pdf_pages"
