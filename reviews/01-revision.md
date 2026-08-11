# Revision 1 response to the initial-candidate referee

- **Response date:** 2026-08-11
- **Responds to:** [`01-pre-revision-referee.md`](01-pre-revision-referee.md)
- **Initial candidate:** `915e4c4487aa5ed4fcd753b51ea07916a9aaf3ea`
- **Referee verdict answered:** major revision
- **Revision status:** all six recorded issues answered in the working
  candidate; exact frozen commit to be recorded in the subsequent freeze
  marker
- **Role boundary:** author revision response, not a referee verdict and not
  external specialist review

## Summary of the mathematical change

The report's countercalculation is accepted without qualification.  The
initial manuscript's assertion that
\(N_X(\Omega_4^+(2^f))\) is maximal and supplements the socle for every
\(S\le X\le\operatorname{Aut}(S)\) was false.  It has been removed from the
proof.

Revision 1 uses a different subgroup.  For
\(S=\operatorname{Sp}_4(2^f)\), choose a prime \(r\mid f\), put
\(d=f/r\), and take the standard subfield subgroup

\[
V=\operatorname{Sp}_4(2^d).
\]

Bray--Holt--Roney-Dougal, Table 8.14, gives maximality of \(V<S\) because the
field-extension degree is prime.  If \(\varphi\) is Frobenius and \(\rho\) is
the exceptional graph-field endomorphism, Harper's Lemma 2.1 gives
\(\rho^2=\varphi\) and
\(\operatorname{Aut}(S)=\langle S,\rho\rangle\).  Hence \(\rho\) normalizes
the \(\varphi^d\)-fixed subgroup \(V\), so the \(S\)-class of \(V\) is
invariant under the full automorphism group, not just under the field-only
part.

For every coordinate group \(S\le X\le\operatorname{Aut}(S)\), put
\(H=N_X(V)\).  Then

\[
X=SH,\qquad H\cap S=V,
\]

and \(H\) is maximal: for \(H<K<X\), maximality of \(V\) gives
\(K\cap S=V\) or \(S\); the first alternative makes \(V\trianglelefteq K\)
and forces \(K\le H\), while the second forces \(K=X\).  The subgroup is
core-free because every nontrivial normal subgroup of an almost-simple group
contains the socle.

LPS (2010), Lemmas 2.1--2.2 and Corollary 2.3, show that the three involution
classes meet \(O_4^+(q)\), with conjugacy there agreeing with symplectic
conjugacy.  Under

\[
O_4^+(q)\cong(SL_2(q)\times SL_2(q))\rtimes\langle\tau\rangle,
\]

the three classes have representatives \((u,1),(u,u),\tau\), which may all
be chosen in \(O_4^+(2)\le Sp_4(2)\le V\).  Thus \(S\) is 2-elusive in the
corrected action.  Finally,

\[
 a=v_2(|X:H|)=v_2(|S:V|)=4(f-d),
 \qquad
 o=v_2(|X:S|)\le1+v_2(f)<2f\le4(f-d)=a.
\]

The existing socle-valuation lemma now applies for every socle exponent.  The
argument explicitly includes every field-only and graph-outer image in the
cyclic group \(\operatorname{Out}(S)\) of order \(2f\).

At the report's test point
\(X=\operatorname{Aut}(Sp_4(4))=S_4(4).4\), the new subgroup has

\[
|H|=2880,\qquad |H\cap S|=720,\qquad |X:H|=1360,
\]

and does supplement the socle.  This finite calculation is a regression test,
not the proof of the uniform statement.

## Point-by-point response

| Issue | Disposition | Revision evidence |
|---|---|---|
| `R186-PR1-01` (P1) | **Answered.** The invalid \(O_4^+\)-normalizer is withdrawn.  The prime-degree subfield normalizer above is proved maximal, core-free, and socle-supplementing for every field-only and graph-outer coordinate group.  Involution coverage and the corrected degree/valuation are proved uniformly. | `paper/kourovka-18-68.tex`, even-symplectic part of Proposition 5.1; `notes/04-product-action-lifting.md`, §6; `notes/07-classification-containment-ledger.md`, §3.9; `tests/test-sp4-subfield.g` for the \(q=4\) regression. |
| `R186-PR1-02` (P2) | **Answered.** The text no longer says that regularity automatically implies core-freeness.  When \(k=1\), \(L=X\); a nontrivial core would contain \(S\), which contradicts \(R\cap H=1\) because \(H\cap S\ne1\). | Coordinate-obstruction proof in the manuscript; `notes/04-product-action-lifting.md`, §3. |
| `R186-PR1-03` (P2) | **Answered.** A 308-line ledger now gives exact Xia--Li row numbers A.1:1--10 through A.7:1--15, the GGS correction, containment rather than equality arguments, class invariance under outer automorphisms, maximality sources, low-parameter isomorphisms, exceptional-family divisibility, and Giudici Tables 1--4 group blocks. | `notes/07-classification-containment-ledger.md`; the manuscript's classical table now cites exact row ranges. |
| `R186-PR1-04` (P2) | **Answered.** Every documented GAP command uses `--quitonbreak`; both producers delete stale outputs before loading packages, enforce GAP 4.15.1 and TomLib 1.2.11, and regenerate version-stamped TSVs.  Python acceptance checks use explicit exceptions and pass under `python3 -O`.  A negative shell control verifies nonzero GAP error status. | `gap/generate-*.g`; `tests/check-*.py`; `tests/test-fail-closed.sh`; local `Makefile`. |
| `R186-PR1-05` (P3) | **Answered.** \(P_1\cap P_4\) is now called a graph-stable parabolic intersection containing a common Borel.  The \(L_2(q)\) text names the nonsplit-torus factor in A.1:1 rather than saying “either torus type.” | Exceptional and rank-one parts of the manuscript; `notes/05-family-factor-screen.md`; `notes/07-classification-containment-ledger.md`. |
| `R186-PR1-06` (P3) | **Answered.** The build wrapper requires Tectonic 0.17.0, bundle v33 content SHA-256 `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`, `SOURCE_DATE_EPOCH=1786406400`, UTC, and deterministic mode.  It compares two clean PDFs byte-for-byte and emits a checked receipt. | `scripts/build-paper.sh`; `scripts/check-release.py`; `paper/BUILD-RECEIPT.txt`; local `Makefile`. |

## Regenerated finite artifacts

The proof-critical factor-free TSV now records the fail-closed producer
command in its metadata and has SHA-256

```text
9b131720d41ef945a0696794c0493ae9c07e166d4d1f37b054a1d55f0c4837ae
```

The bounded CMP summary and maximal-row TSVs have SHA-256

```text
318ac4d55cde05e3e046497eba31b005ebe16832d1be59df98b5e48f9b951320
ed322a51f286f104c4adc057c0b06a6cdbf8c3300f71e9bab8d6950071882b16
```

Only producer metadata changed; the certified mathematical counts remain 414
TomLib tables, 2,395 maximal classes, 73 CMP-positive tables, and 24 pinned
factor-free rows.

The deterministic revised PDF receipt records SHA-256

```text
a48359e6d3be55e914216001cfddba33d316e79989a0aca02928f62f3de8f798
```

This is the receipt hash produced by two clean byte-identical builds before
the freeze check.

## Remaining boundary

This response asserts that the listed revisions have been made; it does not
supply the required fresh referee verdict.  CFSG and the cited exhaustive
classification theorems remain published inputs.  The BHRD book was not
locally audited page by page; its exact Table 8.14 subfield row is
cross-referenced by Burness (2007) and Harper (2024).  External
finite-group-specialist review remains pending.

## Revision 4 editorial note

On 2026-08-11 the two missing backslashes before `\qquad` in the
\(q=4\) display were restored. This changes only this response file; the
manuscript and its mathematical content were already correct.
