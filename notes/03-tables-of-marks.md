# Tables of marks and complemented maximal subgroups

## Exact criterion

Let \(T\) be a complete table of marks for \(G\), and number its subgroup
conjugacy classes \(H_1,\ldots,H_n=G\), with \(H_1=1\). Let \(H_m\) represent
a maximal-subgroup class. A complement must have order
\(\lvert G:H_m\rvert\), so every possible complement belongs to one of the
classes

\[
\mathcal C_m=\{c:\lvert H_c\rvert=\lvert G:H_m\rvert\}.
\]

GAP's function “IntersectionsTom(T,m,c)” describes the possible intersections
of conjugates from classes \(m\) and \(c\). Its first entry is positive exactly
when some such intersection is trivial. Consequently,

\[
H_m\text{ is complemented}
\quad\Longleftrightarrow\quad
\exists c\in\mathcal C_m:
\texttt{IntersectionsTom(T,m,c)[1]}>0.
\]

If the intersection is trivial, the order formula gives
\(\lvert H_mH_c\rvert=\lvert H_m\rvert\lvert H_c\rvert=\lvert G\rvert\), so
the product is all of \(G\). Conversely, every complement occurs among these
subgroup classes.

## Computation

The calculation uses GAP 4.15.1 and TomLib 1.2.11:

~~~sh
gap --quitonbreak -q tests/test-cmp-tom.g
gap --quitonbreak -q gap/generate-tomlib-scan.g
python3 tests/check-tomlib-scan.py
~~~

The library supplies 414 named tables and 2,395 maximal-subgroup classes.

| Quantity | Count |
|---|---:|
| TomLib tables | 414 |
| maximal-subgroup classes | 2,395 |
| CMP-positive tables | 73 |
| CMP-negative tables | 341 |
| tables for nonabelian simple groups | 88 |
| positive nonabelian-simple tables | 3 |
| positive nonsoluble tables | 13 |

The three positive nonabelian-simple tables are

\[
L_2(7),\qquad L_2(11),\qquad L_5(2).
\]

For all 73 positive tables, a chief series was recovered from the normal
subgroup lattice. The non-prime-power chief-factor orders are

\[
168,\qquad 660,\qquad 9{,}999{,}360,
\]

which are the orders of the three groups above. The order \(168\) occurs in
eleven positive tables, and the other two orders once each.

The groups “A5”, “S5”, “L2(7).2”, and “(A5xA5):2” give useful negative
examples. For “L2(7).2”, maximal class 16 has order \(12\) and index \(28\),
but there is no subgroup class of order \(28\).

## Data

The table summary is
[../data/tomlib-cmp-scan.tsv](../data/tomlib-cmp-scan.tsv), and the results
for every maximal-subgroup class are in
[../data/tomlib-cmp-maximals.tsv](../data/tomlib-cmp-maximals.tsv). These
calculations concern the groups represented in TomLib; the proof of the
general theorem uses the family arguments in the manuscript.
