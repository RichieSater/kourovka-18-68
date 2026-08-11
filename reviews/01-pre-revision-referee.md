# Full initial-candidate referee pass

- **Frozen mathematical candidate reviewed:**
  `915e4c4487aa5ed4fcd753b51ea07916a9aaf3ea`
- **Freeze-marker commit:**
  `01cd302e9f993dae709debdee65ab66e19c086c9`
- **Review date:** 2026-08-11
- **Role boundary:** internal adversarial review; not external specialist peer
  review
- **Protocol status:** full pre-Revision 1 pass on the initial candidate; this
  report does not complete formal Referee 1
- **Verdict:** **major revision**
- **Recommendation:** **do not circulate for external specialist review until
  the open P1 item is repaired on a new frozen candidate and re-refereed**

## Executive finding

The quotient, chief-factor, monolithic, product-action, and prime-valuation
parts of the proof survived independent reconstruction.  The cited primitive
group theorem has the scope claimed, and the proof-critical finite
Table-of-Marks rows reproduced exactly.

The universal coordinate classification does not presently survive review.
The symplectic argument in lines 480--498 asserts, for every

\[
  S=\operatorname{PSp}_4(2^f)\leq X\leq\operatorname{Aut}(S),
\]

that \(H=N_X(\Omega_4^+(2^f))\) is maximal, supplements \(S\), and has the
displayed degree.  This is false when
\(S=\operatorname{PSp}_4(4)\) and
\(X=\operatorname{Aut}(S)=S_4(4).4\).
An exact GAP/AtlasRep calculation gives

\[
  \lvert X:H\rvert=272,
  \qquad \lvert X:\langle H,S\rangle\rvert=2,
\]

whereas the manuscript claims degree \(136\) and \(X=HS\).  Thus \(H\) is
not maximal in \(X\), and the constructed primitive action does not exist for
this coordinate group.  This is an acceptance-level gap in
Proposition 6.1 and therefore in the proof of the main theorem.  It is not a
counterexample to the theorem itself.

## Scope and method

This pass did not use the working tree as the mathematical candidate.  It
started from a fresh checkout of the exact commit above and covered:

1. the Notebook statement, complement convention, theorem scope, and status
   language;
2. every elementary reduction and the passage from an arbitrary composition
   factor to a self-centralizing monolithic quotient;
3. the product-action primitivity proof and the use of
   Liebeck--Praeger--Saxl Corollary 3(iv);
4. an independent CFSG family inventory and inspection of the available
   primary factorization sources;
5. all proof-path GAP and Python commands, regeneration, negative controls,
   and representative mutations;
6. a clean Tectonic build and visual inspection of all eleven pages; and
7. a dated ten-angle literature refresh.

The review treats CFSG and the cited exhaustive classification theorems as
published inputs.  It checks their stated scope and the manuscript's use of
them; it does not reprove those classifications.

## Independent proof reconstruction

### 1. Quotient and monolithic reductions

The quotient argument is correct.  If \(M/N\) is maximal in \(G/N\) and
\(K\) complements its full preimage \(M\), then \(K\cap N=1\), the image
\(KN/N\) is transitive on the quotient cosets, and its intersection with
\(M/N\) is trivial.

For a chief factor \(A/B\cong S^k\), the quotient by
\(C_{G/B}(A/B)\) has a minimal normal subgroup isomorphic to \(S^k\).
Centerlessness gives \(A\cap C=B\), and faithfulness of the conjugation
action gives \(C_L(S^k)=1\).  Any second minimal normal subgroup would
centralize \(S^k\), so the socle is unique.  No property of a normal subgroup
or arbitrary section is inferred.

### 2. Product-action lifting

The coordinate group

\[
  X=N_L(S_1)/C_L(S_1)
\]

is almost simple, and the standard wreath embedding is faithful.  For a
core-free maximal \(H<X\) with \(V=H\cap S\ne1\), the proof that the point
stabilizer in the action on \((X/H)^k\) is maximal is sound:

- projections of an intermediate normal subgroup are either \(V\) or \(S\);
- coordinate transitivity makes the alternative uniform;
- in the subdirect case, Scott's lemma gives full diagonal strips; and
- containment of \(V^k\) rules out every strip of length greater than one.

The nontrivial, nonsubdirect socle stabilizer \(V^k\) places the action in
product-action type.  Corollary 3(iv) of Liebeck--Praeger--Saxl then has the
stated consequence for \(k\geq2\): a regular subgroup would force a
core-free transitive subgroup in the almost-simple component action.

For \(k=1\), the manuscript needs the local repair recorded as
`R186-PR1-02` below.  The conclusion is true, but the sentence currently
given is not a valid general implication about regular subgroups.

### 3. Factor screen and prime lifting

The factor-screen lemma is correct.  Automorphism invariance of the
\(S\)-class of \(V\) gives \(N_X(V)S=X\); the modular law restricts a
hypothetical factorization to \(CS\), and maximal overgroups remain
core-free because both original factors supplement the socle.

Both prime-lifting lemmas are correct.  The fixed-tuple equations close on a
\(p\)-cycle because its cycle product is trivial.  In the valuation lemma,
for a hypothetical regular subgroup \(R\), the estimate

\[
  v_p(\lvert R\cap S^k\rvert)
  \geq k(a-o)-v_p(k!)>0
\]

does force an order-\(p\) element in the base socle, which fixes a tuple.

### 4. Family audit apart from the open symplectic branch

I reconstructed the family partition without using the manuscript's summary
as an exhaustive premise.

- The alternating actions through degree \(12\) have the claimed elementary
  elusive witnesses; the five factor-free small rows reproduce.  The
  six-subset screen for degree at least \(13\) has the required separation
  from the intransitive factors in the LPS list.
- Xia--Li Theorem 2.15 and Tables A.1--A.7 do restate the maximal
  factorizations for classical socles.  The rank-one order checks, the
  \(L_3(q)\) split-torus calculation, the low-rank isomorphisms, and the ten
  \(L_3(4)\) finite rows were checked.  The two corrected
  \(\mathrm P\Omega_8^+(4)\) and
  \(\mathrm P\Omega_8^+(16)\) rows do not contain the central-node
  parabolic.
- Hering--Liebeck--Saxl has the exceptional-family scope used in the paper.
  The defining-characteristic order comparison excludes its displayed
  factors.
- Giudici's theorems and tables have the claimed sporadic scope.  The
  selected maximal subgroups for \(M_{11}\), \(He\), \(Ru\), \(Suz\),
  \(Fi_{22}\), and \(Co_1\) were also checked against the official online
  ATLAS lists.  No additional sporadic survivor was found; the \(M_{24}\)
  two-subset action is 2-elusive.

This audit found no second missing CFSG family, but it cannot close the
classification proposition while the graph-outer symplectic case below is
open.

## Acceptance-level defect: the graph-outer symplectic case

Let

\[
  X=S_4(4).4=\operatorname{Aut}(S_4(4)),
  \qquad S=X'=S_4(4),
\]

and let \(U\cong\Omega_4^+(4)\cong A_5\times A_5\).  The following uses
GAP 4.15.1 and AtlasRep 2.1.11.

```gap
LoadPackage("atlasrep");;
G := AtlasGroup("S4(4).4", IsPermGroup, true);;
S := DerivedSubgroup(G);;
O := First(MaximalSubgroups(S), u -> Size(u) = 7200);;
U := DerivedSubgroup(O);;
H := Normalizer(G, U);;
Y := ClosureGroup(H, S);;

Print(Size(G), " ", Size(S), " ", Size(U), " ", Size(H), " ",
      Size(Intersection(H, S)), " ", Size(Y), "\n");
Print(Index(G, H), " ", Index(G, Y), "\n");
```

The output is

```text
3916800 979200 3600 14400 7200 1958400
272 2
```

There are two \(S\)-classes of maximal subgroups of order \(7200\), each of
shape \((A_5\times A_5):2\) and each with orbit length \(136\); repeating the
normalizer calculation for either class gives the same result.  Consequently

\[
  H\cap S=O_4^+(4),\qquad
  \lvert X:H\rvert=272,
  \qquad HS=Y<X.
\]

In fact, an intermediate-subgroup calculation finds \(Y\) as the unique
proper intermediate subgroup between \(H\) and \(X\).  Hence \(H\) is not
maximal in \(X\), and its only maximal overgroup contains the socle.

This directly contradicts manuscript lines 481--485 for an allowed
coordinate group \(X\).  The cited LPS Section 10 begins with a point
stabilizer already assumed core-free and maximal; case (10.1) cannot be used
in reverse to assert that this normalizer is maximal for every intermediate
almost-simple group.

Revision must not patch only \(q=4\).  It must inventory every
\(S\leq X\leq\operatorname{Aut}(S)\) for
\(S=\operatorname{PSp}_4(2^f)\), distinguish field-only from graph-outer
images in \(\operatorname{Out}(S)\cong C_{2f}\), and supply a valid maximal
coordinate action and obstruction in every case.

## Source and literature audit

Freshly obtained copies of the following proof inputs matched the SHA-256
values in `references/README.md`:

| Input | Hash check and scope result |
|---|---|
| Liebeck--Praeger--Saxl (2000) | matched; Corollary 3(iv) has the claimed product-action conclusion |
| Xia--Li (2022) | matched; Theorem 2.15 and Tables A.1--A.7 have the claimed exhaustive classical scope |
| Gill--Giudici--Spiga (2024) | matched; the two corrected plus-orthogonal rows were inspected |
| Hering--Liebeck--Saxl (1987) | matched; Theorems 1--2 have the claimed exceptional scope |
| Giudici (2006) | matched; Theorems 1.1--1.3 and Tables 1--3 were inspected |
| Liebeck--Praeger--Saxl (2010) | matched; Corollary 2.3 and Section 10 were inspected |
| Levchuk--Likharev (2006) | matched; the stated simple-group classification was checked |

The original 1990 LPS memoir and the Kleidman--Liebeck book were not
available as searchable local PDFs.  For the classical family inventory I
used the Xia--Li restatement and the 2024 correction.  This limitation is
one reason the revised paper should add exact row and proposition pinpoints
rather than broad chapter references.

The literature refresh used the following ten query angles:

1. exact searches for “Kourovka 18.68”;
2. the exact English property and composition-factor question;
3. the Russian formulation of complemented maximal subgroups;
4. citations to Levchuk--Likharev;
5. citations to Maslova--Revin;
6. regular subgroups in primitive product action;
7. corrections to maximal-factorization classifications;
8. exact factorizations of almost-simple groups;
9. claimed solutions or preprints for Problem 18.68; and
10. 2025--2026 work on complemented maximals and regular subgroups.

The July 2026 Notebook still prints Problem 18.68 without a solution note.
No complete solution was found in the search.  This is dated reconnaissance,
not proof of novelty, priority, or the absence of unindexed work.

## Computational and artifact reproduction

From a fresh checkout of the frozen candidate, all documented proof-path
commands succeeded:

```sh
make check
cd problem-18-68
gap -q tests/test-cmp-tom.g
gap -q gap/generate-tomlib-scan.g
python3 tests/check-tomlib-scan.py
gap -q tests/test-factor-free-tom.g
gap -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
cd paper && tectonic kourovka-18-68.tex
```

The regenerated bounded scan again contained 414 tables, 2,395 maximal
classes, and 73 positive tables.  The proof/cross-check certificate again
contained 24 rows.  The regenerated hashes were

```text
e8057a728dca589e6c431cc9779ce02b37f8a5daac83a0be879e98ba8bc6f9b4
adbd9590e769136eab7fea84139de0bec2f068252a68228e454066cc7f473c55
82bcf695617014f0124839c5a01983a6c8904fc5bc92e0893c9c2601c43bd3a0
```

Corrupting either committed TSV made the Python checker reject it.  A
different failure control exposed an executable-contract weakness: plain
`gap -q` prints a GAP `Error` but returns process status zero at end of
input.  For example, requesting nonmaximal class 1 in the \(A_5\) test
prints “the requested class is not maximal” and exits zero.  If a version
check fails before an output file is opened, a stale committed output can
therefore remain and its checker can still pass.  The producer command must
use `--quitonbreak` or an equivalent explicit nonzero exit discipline.

The Tectonic 0.17.0 build produced an eleven-page letter-size PDF.  All pages
were rendered and inspected; no clipping, collision, malformed display,
or unresolved-reference diagnostic was found.  The rebuilt PDF differed
only in creation metadata, as expected from the current unpinned build
wrapper.

## Issues

| ID | Severity | Observation | Required disposition | Status |
|---|---:|---|---|---|
| `R186-PR1-01` | P1 | The \(\operatorname{PSp}_4(2^f)\) argument falsely asserts that \(N_X(\Omega_4^+(2^f))\) is maximal and supplements the socle for every coordinate group.  \(X=S_4(4).4\) is an explicit counterexample to that assertion. | Give a uniform screen for every field and graph-outer coordinate group, with exact maximality, degree, and elusive/factor-free verification; then rerun the full family audit. | **Open** |
| `R186-PR1-02` | P2 | For \(k=1\), the proof says that a regular subgroup is automatically core-free.  That is false in general. | Use \(L=X\) and almost simplicity: a nontrivial core contains \(S\), but a regular complement cannot contain \(S\) because \(H\cap S\ne1\). | **Open** |
| `R186-PR1-03` | P2 | Several classical and sporadic containment exclusions are compressed to “absent from the table” with broad chapter citations. | Add a row-by-row source/containment ledger with exact table rows, maximality pinpoints, outer-automorphism behavior, and low-parameter routing. | **Open** |
| `R186-PR1-04` | P2 | GAP `Error` paths can exit with status zero under the documented commands; the general TomLib producer does not enforce its stated versions, and Python `assert` checks disappear under `python -O`. | Make proof-path commands fail closed, enforce every pinned version before retaining outputs, and replace acceptance-critical bare assertions with explicit checks. | **Open** |
| `R186-PR1-05` | P3 | The manuscript calls \(P_1\cap P_4\) in \(F_4(2^f)\) a Borel, although it is a graph-stable parabolic intersection containing a Borel.  The order argument remains valid. | Correct the terminology; also replace “either torus type” in the \(L_2(q)\) screen by the precise nonsplit factor that is actually being excluded. | **Open** |
| `R186-PR1-06` | P3 | The PDF build has no version-enforcing wrapper or metadata-stable receipt, and release metadata/disclosure fields are not yet submission-ready. | Add the pinned build/release checks in the later reproducibility and hard-final rounds. | **Open** |

Severity meanings are those of the repository workflow: P1 is
acceptance-level; P2 is important but locally repairable; P3 is editorial or
release-facing.  No P0 counterexample to the main theorem was found.

## Required major-revision gate

Before the candidate can receive a formal Referee 1 pass:

1. close `R186-PR1-01` uniformly, not by a single \(q=4\) computation;
2. answer every issue in a new append-only `01-revision.md` response matrix;
3. freeze a new exact candidate commit;
4. rerun the family, source, computation, mutation, notation, and rendering
   audits from that commit; and
5. obtain a fresh referee verdict on the full revised theorem rather than
   only on the response.

## What remains trusted or unchecked

- CFSG and the published classification theorems were not reproved.
- The original LPS 1990 memoir and the full Kleidman--Liebeck subgroup book
  were not inspected page by page in this pass.
- The AtlasRep calculation certifies the concrete \(S_4(4).4\) defect; it is
  not itself a classification of all graph-outer symplectic coordinates.
- No proof-assistant formalization, author correspondence, subscription-only
  citation-index search, or external finite-group-specialist review was
  performed.
- The clean computational reproduction certifies the named finite tables,
  not the truth of the infinite classification screen.

## Verdict rationale

The structural idea is strong and most of the proof is independently
checkable, but the main theorem is universal in the coordinate group \(X\).
One admissible almost-simple coordinate group already falsifies the subgroup
assertion used to close the sole surviving infinite classical family.  The
current manuscript therefore does not meet the no-open-P1 pass gate.  The
appropriate verdict is **major revision**, with external specialist
circulation deferred until a new frozen candidate closes the graph-outer
symplectic branch and passes a fresh full review.
