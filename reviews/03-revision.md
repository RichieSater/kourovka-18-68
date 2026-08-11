# Revision 3 — computational and reproducibility hardening

- **Revision date:** 2026-08-11
- **Predecessor:** Referee 2 pass at `reviews/02-referee.md`
- **Role boundary:** author-side reproducibility revision; not a referee
  verdict and not external peer review

## Existing reproducibility contract

The proof uses complete tables of marks only for fifteen proof-critical small
coordinate groups; nine sporadic rows are independent cross-checks. Infinite
families are closed by published classifications and uniform arguments, never
by extrapolating from the 414-table survey.

The candidate already pins GAP 4.15.1, TomLib 1.2.11, AtlasRep 2.1.11,
Python 3, Tectonic 0.17.0, bundle v33 and its content hash, and a fixed
`SOURCE_DATE_EPOCH`. Both GAP producers remove stale outputs before package
or version checks and are invoked with `--quitonbreak`. Independent Python
checkers bind the complete files by SHA-256, validate metadata and arithmetic,
and pass under `python3 -O`. Two clean deterministic PDF builds must be
byte-identical.

## New mutation controls

Revision 3 adds `tests/test-mutation-controls.py`. It works only in isolated
temporary trees and deliberately tests seven failure modes:

1. a byte mutation in the factor-free certificate;
2. a missing factor-free certificate;
3. a mutation in the CMP summary certificate;
4. a changed deterministic-build receipt field;
5. a changed PDF byte stream;
6. a forced GAP-version failure in the factor-free producer; and
7. a forced GAP-version failure in the full TomLib producer.

For the last two controls, stale certificate files are placed in the temporary
tree before execution. A passing test requires a nonzero GAP exit and absence
of every stale output afterward. The certificate and release checkers are
also run successfully on unmodified temporary copies before mutation, so a
broken test harness cannot pass merely because every invocation fails.

The local `Makefile` now includes these controls in both `make check` and
`make release-check`.

## Acceptance boundary

The mutation suite tests the interfaces among committed data, GAP producers,
Python checkers, and release artifacts. It does not prove that TomLib's
mathematical tables are correct; that is the declared database input. It does
prove that the repository does not silently treat absent, stale, version-
mismatched, or altered data as a valid certificate.

The exact candidate containing these controls is to be frozen by the commit
for this revision and then reproduced from a fresh clone by Referee 3.
