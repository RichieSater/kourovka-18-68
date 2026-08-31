# Complemented maximal subgroups and Kourovka Problem 18.68

**Publication status:** preprint. The manuscript proves its main theorem
conditional on CFSG and the explicitly stated external classification and
factorization inputs. The exact matches for LPS (2000), Corollary 3(iv), and
LPS (1990), Theorem D with Remark 2, remain explicit source assumptions.
Complete tables of marks computationally certify fifteen named
almost-simple coordinate cases.

**Current version:** [1.1.1](https://github.com/RichieSater/kourovka-18-68/releases/tag/v1.1.1).

## Result

If every maximal subgroup of a finite group has an exact complement, then
its nonabelian composition factors are precisely among

\[
\operatorname{PSL}_2(7),\qquad
\operatorname{PSL}_2(11),\qquad
\operatorname{PSL}_5(2).
\]

All three possibilities occur.

The central argument is section-safe. The complement property passes to
quotients but not to arbitrary sections, so the proof does not apply the
known simple-group classification directly to a composition factor. Instead
it:

1. constructs a monolithic quotient with socle \(S^k\);
2. manufactures a faithful primitive product action from an almost-simple
   coordinate action;
3. applies factor-free, prime-elusive, or socle-valuation obstructions; and
4. uses published exhaustive factorization classifications to close every
   CFSG family.

The full \(\operatorname{PSp}_4(2^f)\) family is eliminated by a
prime-degree subfield action and a uniform 2-adic argument. Finite
Table-of-Marks computations are used only for five small alternating
coordinate groups and ten groups with socle
\(\operatorname{PSL}_3(4)\).

The manuscript source is
[paper/kourovka-18-68.tex](paper/kourovka-18-68.tex), and the current
deterministic PDF is
[paper/kourovka-18-68.pdf](paper/kourovka-18-68.pdf).

- Repository: [RichieSater/kourovka-18-68](https://github.com/RichieSater/kourovka-18-68)
- Historical version 1.0.2 correction:
  [RELEASE-NOTES-v1.0.2.md](RELEASE-NOTES-v1.0.2.md)
- Version 1.1.0:
  [RELEASE-NOTES-v1.1.0.md](RELEASE-NOTES-v1.1.0.md)
- Current version 1.1.1:
  [RELEASE-NOTES-v1.1.1.md](RELEASE-NOTES-v1.1.1.md)

## Important correction to versions 1.0.0 and 1.0.1

Versions 1.0.0 and 1.0.1 contained a material proof gap in the graph-outer
\(\operatorname{PSp}_4(2^f)\) case. For
\[
X=\operatorname{Aut}(\operatorname{PSp}_4(4))=S_4(4).4,
\]
the claimed normalizer of \(\Omega_4^+(4)\) has index \(272\), is not
maximal, and does not supplement the socle.

Version 1.0.2 replaced that construction with
\[
V=\operatorname{Sp}_4(2^{f/r}),
\]
where \(r\mid f\) is prime. Its normalizer is maximal and supplements the
socle in every field-only or graph-outer coordinate group. Every involution
class meets \(\operatorname{Sp}_4(2)\leq V\), and the exact 2-adic
inequality closes every socle multiplicity. At \(q=4\), the corrected action
has degree \(1360\), subgroup order \(2880\), and socle intersection order
\(720\).

## Reproduce the evidence

The pinned environment is GAP 4.15.1 with TomLib 1.2.11 and AtlasRep
2.1.11, together with Tectonic 0.17.0 and the pinned bundle-v33 content
hash. The Python checkers support Python 3.10 or later.

    make check          # mathematical tests, corpus policy, data, and mutations
    make regenerate     # regenerate all GAP/Table-of-Marks data
    make bootstrap-bundle # populate and authenticate an empty Tectonic cache
    make paper          # two clean deterministic PDF builds
    make working-archive # build and scan an allowlisted working-tree bundle
    make release-check  # full regeneration and byte-for-byte comparison

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the exact scope,
clean-clone procedure, source allowlist, and archive-level scan.
[SHA256SUMS](SHA256SUMS) pins the manuscript, PDF, build receipt, and
generated data.

## Reading order

1. [PROBLEM.md](PROBLEM.md)
2. [PROOF-ARCHITECTURE.md](PROOF-ARCHITECTURE.md)
3. [paper/kourovka-18-68.tex](paper/kourovka-18-68.tex)
4. [notes/02-chief-factor-reduction.md](notes/02-chief-factor-reduction.md)
5. [notes/04-product-action-lifting.md](notes/04-product-action-lifting.md)
6. [notes/07-classification-containment-ledger.md](notes/07-classification-containment-ledger.md)
7. [notes/06-finite-factor-free-certificates.md](notes/06-finite-factor-free-certificates.md)
8. [REPRODUCIBILITY.md](REPRODUCIBILITY.md)

## Citation and licensing

Citation metadata is in [CITATION.cff](CITATION.cff). Code is MIT licensed;
the research prose and manuscript remain all rights reserved. See
[LICENSE.md](LICENSE.md) for the exact boundary.
