# Computational verification of the finite cases

The calculation uses the complete subgroup and intersection data in GAP
4.15.1 and TomLib 1.2.11. It treats five small alternating coordinate groups
and all ten almost-simple coordinate groups with socle \(L_3(4)\), and also
checks nine sporadic rows from the published classification.

## Property checked

Let \(X\) be almost simple with socle \(S\), and let \(H<X\) be maximal and
core-free.  A subgroup \(C<X\) is transitive on \(X/H\) exactly when

\[
X=HC.
\]

For subgroup classes \(h,c,i\) in a complete table of marks, a conjugate
pair can have intersection in class \(i\) precisely when
`IntersectionsTom(tom,h,c)[i]` is positive.  Such a pair factors \(X\) if
and only if

\[
\lvert H\rvert\,\lvert C\rvert=\lvert X\rvert\,\lvert H\cap C\rvert.
\]

The factor \(C\) is core-free exactly when its class does not contain the
socle class. The program examines every such class \(c\) and every
intersection class \(i\).

For each listed subgroup it also checks

\[
\lvert H\cap S\rvert=\lvert H\rvert\,\lvert S\rvert/\lvert X\rvert>1,
\]

so every proof row satisfies the nontrivial-socle-stabilizer hypothesis in
the product-action lemma.

## Groups and subgroups checked

| \(X\) | \(\lvert H\rvert\) | \(\lvert X:H\rvert\) | Role |
|---|---:|---:|---|
| \(A_6.2_2\) | 16 | 45 | alternating case |
| \(A_6.2_3\) | 20 | 36 | alternating case |
| \(A_6.2^2\) | 32 | 45 | alternating case |
| \(A_7\) | 72 | 35 | alternating case |
| \(S_7\) | 144 | 35 | alternating case |
| \(L_3(4)\) | 960 | 21 | linear case |
| \(L_3(4).2_1\) | 384 | 105 | linear case |
| \(L_3(4).2_2\) | 1920 | 21 | linear case |
| \(L_3(4).2_3\) | 720 | 56 | linear case |
| \(L_3(4).3\) | 216 | 280 | linear case |
| \(L_3(4).2^2\) | 768 | 105 | linear case |
| \(L_3(4).3.2_2\) | 432 | 280 | linear case |
| \(L_3(4).3.2_3\) | 1152 | 105 | linear case |
| \(L_3(4).6\) | 1152 | 105 | linear case |
| \(L_3(4).D_{12}\) | 2304 | 105 | linear case |
| \(M_{11}\) | 120 | 66 | sporadic cross-check |
| \(M_{12}\) | 192 | 495 | sporadic cross-check |
| \(M_{12}.2\) | 216 | 880 | sporadic cross-check |
| \(M_{22}.2\) | 1440 | 616 | sporadic cross-check |
| \(M_{23}\) | 20160 | 506 | sporadic cross-check |
| \(J_2\) | 2160 | 280 | sporadic cross-check |
| \(J_2.2\) | 4320 | 280 | sporadic cross-check |
| \(HS\) | 40320 | 1100 | sporadic cross-check |
| \(HS.2\) | 80640 | 1100 | sporadic cross-check |

Every row has zero core-free transitive factor classes.

## Reproduction

From the repository root, run:

```sh
gap --quitonbreak -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
```

The output is
[`../data/tomlib-factor-free.tsv`](../data/tomlib-factor-free.tsv). The
program is part of the
[accompanying repository](https://github.com/RichieSater/kourovka-18-68).
For every named group it checks maximality, the socle class, core-freeness,
the order identity, and all possible factor and intersection classes.
