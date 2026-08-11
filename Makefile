SHELL := /bin/bash

GAP ?= gap
PYTHON ?= python3
TECTONIC ?= tectonic
SOURCE_DATE_EPOCH ?= 1786406400

.PHONY: check versions test verify-data verify-manifest fail-closed mutation-controls regenerate paper release-check

check: versions test verify-data fail-closed mutation-controls verify-manifest
	$(PYTHON) scripts/check-release.py
	git diff --check -- .

versions:
	GAP=$(GAP) PYTHON=$(PYTHON) TECTONIC=$(TECTONIC) scripts/check-versions.sh

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
	GAP=$(GAP) PYTHON=$(PYTHON) tests/test-fail-closed.sh

mutation-controls:
	$(PYTHON) tests/test-mutation-controls.py

regenerate: versions
	$(GAP) --quitonbreak -q gap/generate-tomlib-scan.g
	$(GAP) --quitonbreak -q gap/generate-factor-free-scan.g
	$(PYTHON) tests/check-tomlib-scan.py
	$(PYTHON) tests/check-factor-free-scan.py

paper:
	TECTONIC=$(TECTONIC) SOURCE_DATE_EPOCH=$(SOURCE_DATE_EPOCH) scripts/build-paper.sh
	$(PYTHON) scripts/check-release.py

release-check: versions test regenerate fail-closed mutation-controls paper verify-manifest
	git diff --check -- .
	git diff --exit-code -- data paper/kourovka-18-68.pdf paper/BUILD-RECEIPT.txt
