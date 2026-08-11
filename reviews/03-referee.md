# Referee pass 3 — fresh-clone computation and reproducibility

- **Frozen candidate reviewed:**
  `c815d3ba8cc9cf587aa738135b9bac4cb50ccfd1`
- **Review date:** 2026-08-11
- **Clone mode:** local `git clone --no-local`, detached at the exact candidate
- **Role boundary:** internal adversarial reproducibility review; not external
  specialist peer review
- **Verdict:** **pass**

## Fresh-clone environment

The clone began and ended clean. The version gate reported:

```text
GAP       4.15.1
TomLib    1.2.11
AtlasRep  2.1.11
Python    3.14.6
Tectonic  0.17.0
```

The TeX build used only cached files from bundle v33, whose configured content
hash is
`6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`,
with deterministic mode, UTC, and `SOURCE_DATE_EPOCH=1786406400`.

## Proof-path test inventory

`make release-check` executed the following in the fresh clone:

1. direct GAP tests for the CMP table criterion;
2. direct GAP tests for the factor-free table criterion;
3. the independent AtlasRep regression for
   $\operatorname{Aut}(Sp_4(4))$;
4. complete regeneration of both 414-table CMP files;
5. complete regeneration of all 24 pinned factor-free rows;
6. independent Python verification of hashes, metadata, row counts,
   arithmetic, complement witnesses, and factor-free counts;
7. Python checkers under `-O` and a forced GAP `Error` exit;
8. seven isolated mutation controls;
9. two clean deterministic Tectonic builds and byte comparison; and
10. receipt verification and `git diff --check`.

The regeneration reported 414 tables, 2,395 maximal classes, 73 CMP-positive
tables, and 24 pinned factor-free rows. The proof-critical set is the five
small alternating and ten $L_3(4)$ coordinate groups; the nine sporadic rows
are explicitly labeled cross-checks.

## Independent output binding

The regenerated files were byte-identical to the committed files:

```text
TeX
3913cafcfc2fa8792176921008a8b39db68b72d0533bf66d7cbc8fa092d67757
PDF
a48359e6d3be55e914216001cfddba33d316e79989a0aca02928f62f3de8f798
CMP summary
318ac4d55cde05e3e046497eba31b005ebe16832d1be59df98b5e48f9b951320
CMP maximal rows
ed322a51f286f104c4adc057c0b06a6cdbf8c3300f71e9bab8d6950071882b16
factor-free rows
9b131720d41ef945a0696794c0493ae9c07e166d4d1f37b054a1d55f0c4837ae
```

## Mutation audit

The new temporary-tree harness first accepted unmodified copies, then
rejected all seven deliberate failures:

| Mutation | Required outcome | Result |
|---|---|---|
| factor-free file byte changed | checker nonzero | passed |
| factor-free file removed | checker nonzero | passed |
| CMP summary changed | checker nonzero | passed |
| receipt deterministic field changed | checker nonzero | passed |
| PDF bytes changed | checker nonzero | passed |
| factor-free producer forced to fail version gate with stale output present | nonzero and stale output absent | passed |
| CMP producer forced to fail version gate with stale outputs present | nonzero and both stale outputs absent | passed |

The existing GAP error control also returned nonzero under `--quitonbreak`,
and both Python acceptance checkers passed under optimization, demonstrating
that no bare `assert` carries an acceptance condition.

## Manuscript-to-certificate interface

The manuscript names the producer and checker commands, exact GAP/TomLib
versions, proof-critical row count, and factor-free SHA-256. The dedicated
$q=4$ regression checks the corrected subgroup data but is not cited as the
proof of the infinite family. The 414-table survey is described as bounded
support and is not used in the universal argument. These scopes match the
code and generated metadata.

## Issues

| ID | Severity | Observation | Status |
|---|---|---|---|
| `R186-F3-01` | P3 | The fresh clone reused the host's installed binaries and cached Tectonic bundle rather than a container image. | Nonblocking: every acceptance-critical version and the bundle content hash is enforced; record the host versions in any submission archive. |
| `R186-F3-02` | P3 | The manuscript prints only the proof-critical TSV hash, while the repository also contains two bounded-survey hashes. | Correct scope: all three are bound in their checkers and ledgers; only the proof-critical artifact needs to appear in the article. |

No missing output, stale-file path, unchecked positive row, or open P0--P2
issue was found.

## Verdict rationale

A clean clone regenerates the committed certificates and PDF exactly; missing,
changed, stale, optimized-away, or version-mismatched evidence fails closed.
The computation proves only the finite claims assigned to it. The Round 3
pass gate is satisfied, so the verdict is **pass**.
