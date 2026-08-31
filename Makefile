SHELL := /bin/bash

GAP ?= gap
PYTHON ?= python3
TECTONIC ?= tectonic
SOURCE_DATE_EPOCH ?= $(shell $(PYTHON) -c 'import json; print(json.load(open("artifact-metadata.json"))["source_date_epoch"])')

.PHONY: check versions public-corpus test verify-data verify-manifest fail-closed mutation-controls regenerate bootstrap-bundle paper working-archive source-archive release-check

check: versions public-corpus test regenerate fail-closed mutation-controls verify-manifest
	$(PYTHON) scripts/check-release.py
	git diff --check -- .
	git diff --exit-code -- data/tomlib-cmp-maximals.tsv \
		data/tomlib-cmp-scan.tsv data/tomlib-factor-free.tsv

versions:
	GAP="$(GAP)" PYTHON="$(PYTHON)" TECTONIC="$(TECTONIC)" scripts/check-versions.sh

public-corpus:
	$(PYTHON) scripts/check-public-corpus.py

test:
	$(GAP) --quitonbreak -q tests/test-cmp-tom.g
	$(GAP) --quitonbreak -q tests/test-factor-free-tom.g
	$(GAP) --quitonbreak -q tests/test-sp4-subfield.g

verify-data:
	$(PYTHON) tests/check-tomlib-scan.py
	$(PYTHON) tests/check-factor-free-scan.py

verify-manifest:
	shasum -a 256 -c SHA256SUMS

fail-closed:
	GAP="$(GAP)" PYTHON="$(PYTHON)" tests/test-fail-closed.sh

mutation-controls:
	$(PYTHON) tests/test-mutation-controls.py

regenerate: versions
	$(GAP) --quitonbreak -q gap/generate-tomlib-scan.g
	$(GAP) --quitonbreak -q gap/generate-factor-free-scan.g
	$(PYTHON) tests/check-tomlib-scan.py
	$(PYTHON) tests/check-factor-free-scan.py

bootstrap-bundle:
	TECTONIC="$(TECTONIC)" SOURCE_DATE_EPOCH="$(SOURCE_DATE_EPOCH)" scripts/bootstrap-tectonic-bundle.sh

paper:
	TECTONIC="$(TECTONIC)" SOURCE_DATE_EPOCH="$(SOURCE_DATE_EPOCH)" scripts/build-paper.sh
	$(PYTHON) scripts/check-release.py

working-archive:
	$(PYTHON) scripts/build-source-archive.py --working-tree

source-archive:
	$(PYTHON) scripts/build-source-archive.py

release-check: versions public-corpus test regenerate fail-closed mutation-controls paper verify-manifest source-archive
	git diff --check -- .
	git diff --exit-code -- .
	git diff --cached --exit-code -- .
