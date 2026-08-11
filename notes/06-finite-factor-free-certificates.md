# Finite factor-free certificates

**Evidence label:** **computationally certified**, conditional on the complete
tables in GAP 4.15.1 / TomLib 1.2.11.  These calculations close five named
small alternating cases and all ten almost-simple coordinate groups with
socle (L_3(4)), and independently cross-check nine sporadic rows;
they are not used as an infinite-family classification.

## Predicate

Let (X) be almost simple with socle (S), and let (H<X) be maximal and
core-free.  A subgroup (C<X) is transitive on (X/H) exactly when

\[
X=HC.
\]

For subgroup classes (h,c,i) in a complete table of marks, a conjugate
pair can have intersection in class (i) precisely when
`IntersectionsTom(tom,h,c)[i]` is positive.  Such a pair factors (X) if
and only if

\[
|H|\,|C|=|X|\,|H\cap C|.
\]

The factor (C) is core-free exactly when its class does not contain the
socle class.  The producer exhausts every such class (c) and every
intersection class (i).  Missing table, maximal, containment, or
intersection data raise an error.

The producer also records and checks

\[
|H\cap S|=|H|\,|S|/|X|>1,
\]

so every proof row satisfies the nontrivial-socle-stabilizer hypothesis in
the product-action lemma.

## Pinned witnesses

| (X) | (|H|) | (\lvert X:H\rvert) | Role |
|---|---:|---:|---|
| (A_6.2_2) | 16 | 45 | small alternating closeout |
| (A_6.2_3) | 20 | 36 | small alternating closeout |
| (A_6.2^2) | 32 | 45 | small alternating closeout |
| (A_7) | 72 | 35 | small alternating closeout |
| (S_7) | 144 | 35 | small alternating closeout |
| (L_3(4)) | 960 | 21 | small linear closeout |
| (L_3(4).2_1) | 384 | 105 | small linear closeout |
| (L_3(4).2_2) | 1920 | 21 | small linear closeout |
| (L_3(4).2_3) | 720 | 56 | small linear closeout |
| (L_3(4).3) | 216 | 280 | small linear closeout |
| (L_3(4).2^2) | 768 | 105 | small linear closeout |
| (L_3(4).3.2_2) | 432 | 280 | small linear closeout |
| (L_3(4).3.2_3) | 1152 | 105 | small linear closeout |
| (L_3(4).6) | 1152 | 105 | small linear closeout |
| (L_3(4).D_{12}) | 2304 | 105 | small linear closeout |
| (M_{11}) | 120 | 66 | sporadic cross-check |
| (M_{12}) | 192 | 495 | sporadic cross-check |
| (M_{12}.2) | 216 | 880 | sporadic cross-check |
| (M_{22}.2) | 1440 | 616 | sporadic cross-check |
| (M_{23}) | 20160 | 506 | sporadic cross-check |
| (J_2) | 2160 | 280 | sporadic cross-check |
| (J_2.2) | 4320 | 280 | sporadic cross-check |
| (HS) | 40320 | 1100 | sporadic cross-check |
| (HS.2) | 80640 | 1100 | sporadic cross-check |

Every row has zero core-free transitive factor classes.

## Reproduction

From the repository root run:

```sh
gap -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
```

The committed output is
[`../data/tomlib-factor-free.tsv`](../data/tomlib-factor-free.tsv), SHA-256

```text
82bcf695617014f0124839c5a01983a6c8904fc5bc92e0893c9c2601c43bd3a0
```

The GAP producer checks the group, socle, maximal-class position, core-free
condition, order arithmetic, and every possible factor/intersection class.
The Python checker independently validates the pinned rows, metadata,
arithmetic, and file hash.
