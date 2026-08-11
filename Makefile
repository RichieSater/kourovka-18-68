SHELL := /bin/bash

GAP ?= gap
PYTHON ?= python3
TECTONIC ?= tectonic
SOURCE_DATE_EPOCH ?= 1786406400

.PHONY: check test verify-data verify-manifest regenerate paper release-check

check: test verify-data verify-manifest

test:
	$(GAP) -q tests/test-cmp-tom.g
	$(GAP) -q tests/test-factor-free-tom.g

verify-data:
	$(PYTHON) tests/check-tomlib-scan.py
	$(PYTHON) tests/check-factor-free-scan.py

verify-manifest:
	shasum -a 256 -c SHA256SUMS

regenerate:
	$(GAP) -q gap/generate-tomlib-scan.g
	$(GAP) -q gap/generate-factor-free-scan.g
	$(PYTHON) tests/check-tomlib-scan.py
	$(PYTHON) tests/check-factor-free-scan.py

paper:
	cd paper && SOURCE_DATE_EPOCH=$(SOURCE_DATE_EPOCH) $(TECTONIC) kourovka-18-68.tex

release-check: check regenerate paper
	git diff --check
	git diff --exit-code -- data paper/kourovka-18-68.pdf
