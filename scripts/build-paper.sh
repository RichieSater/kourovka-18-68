#!/bin/sh
set -eu

TECTONIC=${TECTONIC:-tectonic}
SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1786406400}
BUNDLE_URL='https://relay.fullyjustified.net/default_bundle_v33.tar'
BUNDLE_CONTENT_SHA256='6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c'
INPUT='paper/kourovka-18-68.tex'
OUTPUT='paper/kourovka-18-68.pdf'
RECEIPT='paper/BUILD-RECEIPT.txt'

if [ "$($TECTONIC --version)" != 'Tectonic 0.17.0' ]; then
    echo 'paper build: Tectonic 0.17.0 is required' >&2
    exit 1
fi
if [ "$SOURCE_DATE_EPOCH" != '1786406400' ]; then
    echo 'paper build: SOURCE_DATE_EPOCH must be 1786406400' >&2
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
pdf_sha=$(shasum -a 256 "$OUTPUT" | awk '{print $1}')
cat > "$RECEIPT" <<EOF
artifact=paper/kourovka-18-68.pdf
tectonic_version=0.17.0
bundle_url=$BUNDLE_URL
bundle_content_sha256=$BUNDLE_CONTENT_SHA256
source_date_epoch=$SOURCE_DATE_EPOCH
timezone=UTC
deterministic_mode=true
clean_builds_compared=2
pdf_sha256=$pdf_sha
EOF
printf 'PAPER BUILD PASSED: %s\n' "$pdf_sha"
