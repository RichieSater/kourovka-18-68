# A solution to Kourovka Problem 18.68

**Status:** complete CFSG-conditional proof candidate, reproducibly checked;
independent external peer review is still pending.

This project asks for nonabelian composition factors of nonsoluble finite
groups when every maximal subgroup has a complement. The answer proved here
is \(L_2(7),L_2(11),L_5(2)\).  The proof passes to a monolithic quotient,
constructs primitive product actions for arbitrary socle multiplicity, and
uses published exhaustive maximal-factorization classifications.  Its only
infinite factor-screen survivor, \(\operatorname{PSp}_4(2^f)\), is closed by a 2-adic
divisibility argument.  Exact Table-of-Marks certificates handle fifteen
named small cases and cross-check nine sporadic rows.

The peer-review manuscript is
[`paper/kourovka-18-68.tex`](paper/kourovka-18-68.tex), with a built PDF at
[`paper/kourovka-18-68.pdf`](paper/kourovka-18-68.pdf).  The earlier
obstruction report is retained as a superseded audit trail.

## Reproduce the checks

Requirements are GAP 4.15.1 with TomLib 1.2.11 and Python 3.  Tectonic 0.17.0
is used to rebuild the manuscript.

```sh
make check          # tests and independent checks of committed certificates
make regenerate     # regenerate the GAP/Table-of-Marks certificate files
make paper          # rebuild paper/kourovka-18-68.pdf
make release-check  # all of the above, then require a clean result
```

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) for scope, environment, and
clean-clone instructions.  The finite Table-of-Marks calculation closes named
finite rows only; the cited published classifications supply the exhaustive
infinite-family coverage.

## Reading order

1. [`PROBLEM.md`](PROBLEM.md)
2. [`ATTACK.md`](ATTACK.md)
3. [`REVIEW-PLAN.md`](REVIEW-PLAN.md)
4. [`CLAIM-LEDGER.md`](CLAIM-LEDGER.md)
5. [`references/README.md`](references/README.md)
6. [`notes/02-chief-factor-reduction.md`](notes/02-chief-factor-reduction.md)
7. [`notes/04-product-action-lifting.md`](notes/04-product-action-lifting.md)
8. [`notes/05-family-factor-screen.md`](notes/05-family-factor-screen.md)
9. [`notes/06-finite-factor-free-certificates.md`](notes/06-finite-factor-free-certificates.md)
10. [`paper/kourovka-18-68.tex`](paper/kourovka-18-68.tex)

## Citation and licensing

Citation metadata is in [`CITATION.cff`](CITATION.cff).  Code is MIT licensed;
the research prose and manuscript remain all rights reserved.  See
[`LICENSE.md`](LICENSE.md) for the exact boundary.
