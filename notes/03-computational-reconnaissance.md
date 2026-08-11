# Exact Table-of-Marks reconnaissance

**Date:** 2026-08-11
**Evidence label:** computationally certified relative to GAP 4.15.1 and the
complete tables supplied by TomLib 1.2.11. The group range is bounded and is
not a universal classification.

## Exact criterion

Let \(T\) be a complete table of marks for \(G\), and number its subgroup
conjugacy classes \(H_1,\ldots,H_n=G\), with \(H_1=1\). Let \(H_m\) represent
a maximal-subgroup class. A complement must have order
\(\lvert G:H_m\rvert\), so every
possible complement belongs to one of the classes

\[
\mathcal C_m=\{c:|H_c|=\lvert G:H_m\rvert\}.
\]

GAP's `IntersectionsTom(T,m,c)` decomposes all intersections of conjugates of
classes \(m\) and \(c\). Its first entry is positive exactly when some such
intersection is trivial. Therefore

\[
H_m\text{ is complemented}
\quad\Longleftrightarrow\quad
\exists c\in\mathcal C_m:
\texttt{IntersectionsTom(T,m,c)[1]}>0.
\]

If the intersection is trivial, the order formula gives
\(|H_mH_c|=|H_m||H_c|=|G|\), so the product is all of \(G\). Conversely,
every complement occurs in the exhaustive candidate list. This is an exact
finite criterion, not a randomized subgroup search.

## Producer and tests

```sh
gap --quitonbreak -q tests/test-cmp-tom.g
gap --quitonbreak -q gap/generate-tomlib-scan.g
python3 tests/check-tomlib-scan.py
```

The implementation fails closed when a table, its maximal-subgroup data, or
its intersection data are unavailable.

## Results

The library supplied 414 named tables and 2,395 maximal-subgroup classes.

| Quantity | Exact count in this range |
|---|---:|
| TomLib tables | 414 |
| maximal-subgroup classes | 2,395 |
| `CMP`-positive tables | 73 |
| `CMP`-negative tables | 341 |
| tables detected as nonabelian simple | 88 |
| positive nonabelian-simple tables | 3 |
| positive nonsoluble tables | 13 |

The three positive nonabelian-simple tables are exactly

\[
L_2(7),\qquad L_2(11),\qquad L_5(2).
\]

For all 73 positive tables, a deterministic chief series was recovered from
the normal-subgroup lattice. The non-prime-power chief-factor orders are

\[
168,\qquad 660,\qquad 9{,}999{,}360,
\]

agreeing with the orders of the three candidate simple groups. The order 168
occurs in eleven positive tables, and the other two orders once each.

Important negative controls include `A5`, `S5`, `L2(7).2`, and
`(A5xA5):2`. For `L2(7).2`, maximal class 16 has order 12 and index 28, but
there is no subgroup class of order 28; its failure certificate has an empty
candidate list.

## Files and limitations

The summary is [`../data/tomlib-cmp-scan.tsv`](../data/tomlib-cmp-scan.tsv),
and every maximal-class certificate is in
[`../data/tomlib-cmp-maximals.tsv`](../data/tomlib-cmp-maximals.tsv).

The computation exhausts each supplied table and every listed table. It does
not exhaust all finite groups, all primitive groups, or any CFSG family. It is
therefore strong regression evidence and a source audit, but it cannot turn
a bounded observation into a universal theorem; the manuscript's universal
step instead uses the published exhaustive classifications.
