# A solution to Kourovka Problem 18.68

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21893700.svg)](https://doi.org/10.5281/zenodo.21893700)

**Version 1.0.2 status:** complete CFSG-conditional proof candidate; four
internal adversarial review rounds passed, with a recommendation to circulate
for external finite-group-specialist review. Independent external peer review
is still pending.

## Important correction to versions 1.0.0 and 1.0.1

Versions 1.0.0 and 1.0.1 contained an acceptance-level proof gap in the
graph-outer $\operatorname{PSp}_4(2^f)$ case. For
$X=\operatorname{Aut}(\operatorname{PSp}_4(4))=S_4(4).4$, the claimed
normalizer of $\Omega_4^+(4)$ has index 272 and neither is maximal nor
supplements the socle. Those versions are preserved for provenance but are
**superseded and must not be cited as the proof**.

Version 1.0.2 withdraws that construction. It uses the prime-degree subfield
subgroup
$V=\operatorname{Sp}_4(2^{f/r})$, whose normalizer is maximal and supplements
the socle for every field-only and graph-outer coordinate group. Every
involution class meets $\operatorname{Sp}_4(2)\leq V$, and the exact
2-adic inequality closes every socle multiplicity. At the smallest regression
case, the corrected action has degree 1360, subgroup order 2880, and socle
intersection order 720.

## Result

The manuscript proves, conditional on CFSG and the cited exhaustive
factorization classifications, that the possible nonabelian composition
factors are exactly

\[
L_2(7),\qquad L_2(11),\qquad L_5(2).
\]

The proof reaches an arbitrary composition factor through a monolithic
quotient, constructs a primitive product action for arbitrary direct-power
multiplicity, and then applies factor-free, elusive-prime, or valuation
obstructions. Exact Table-of-Marks certificates handle fifteen named small
coordinate groups and cross-check nine sporadic rows. No bounded computation
is extrapolated to an infinite family.

The manuscript source is
[paper/kourovka-18-68.tex](paper/kourovka-18-68.tex), and the deterministic
12-page PDF is
[paper/kourovka-18-68.pdf](paper/kourovka-18-68.pdf).

- Version DOI: [10.5281/zenodo.21894829](https://doi.org/10.5281/zenodo.21894829)
- Concept DOI, resolving to the latest version:
  [10.5281/zenodo.21893700](https://doi.org/10.5281/zenodo.21893700)
- Correction details:
  [RELEASE-NOTES-v1.0.2.md](RELEASE-NOTES-v1.0.2.md)
- Hard-final internal report:
  [reviews/04-referee.md](reviews/04-referee.md)

## Reproduce the checks

The acceptance environment is GAP 4.15.1 with TomLib 1.2.11 and AtlasRep
2.1.11, Python 3.14.6, and Tectonic 0.17.0 with the pinned bundle-v33 content
hash.

    make check          # tests, negative controls, manifest, and receipt
    make regenerate     # regenerate all GAP/Table-of-Marks certificates
    make paper          # make two clean deterministic PDF builds
    make release-check  # full regeneration and byte-for-byte comparison

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the exact scope and
clean-clone procedure. [SHA256SUMS](SHA256SUMS) pins the manuscript,
deterministic build receipt, and all three generated data files.

## Reading order

1. [PROBLEM.md](PROBLEM.md)
2. [ATTACK.md](ATTACK.md)
3. [CLAIM-LEDGER.md](CLAIM-LEDGER.md)
4. [notes/02-chief-factor-reduction.md](notes/02-chief-factor-reduction.md)
5. [notes/04-product-action-lifting.md](notes/04-product-action-lifting.md)
6. [notes/07-classification-containment-ledger.md](notes/07-classification-containment-ledger.md)
7. [notes/06-finite-factor-free-certificates.md](notes/06-finite-factor-free-certificates.md)
8. [paper/kourovka-18-68.tex](paper/kourovka-18-68.tex)
9. [reviews/01-pre-revision-referee.md](reviews/01-pre-revision-referee.md)
10. [reviews/01-revision.md](reviews/01-revision.md)
11. [reviews/01-referee.md](reviews/01-referee.md)
12. [reviews/02-referee.md](reviews/02-referee.md)
13. [reviews/03-referee.md](reviews/03-referee.md)
14. [reviews/04-referee.md](reviews/04-referee.md)

The review reports were imported from the original portfolio workspace and
retain its exact frozen-candidate commit hashes. They are internal agent
reviews, not journal or independent external peer review.

## Citation and licensing

Citation metadata is in [CITATION.cff](CITATION.cff). Code is MIT licensed;
the research prose and manuscript remain all rights reserved. See
[LICENSE.md](LICENSE.md) for the exact boundary. The manuscript explicitly
discloses extensive AI assistance in literature search, proof exploration,
code generation, drafting, and adversarial review. Richie Sater is the sole
author and assumes full responsibility for every argument, source,
computation, and release.
