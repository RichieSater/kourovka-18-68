# Revision 4 — hard-final release candidate

- **Revision date:** 2026-08-11
- **Predecessor:** Referee 3 pass at `reviews/03-referee.md`
- **Role boundary:** author-side hard-final revision; not a referee verdict
  and not external peer review

## Final theorem-scope audit

The theorem quantifies over every finite `CMP` group and every one of its
nonabelian composition factors. The proof chooses an arbitrary nonabelian
chief factor $A/B\cong S^k$, constructs a quotient with unique
self-centralizing socle $S^k$, and excludes the simple type $S$ unless it
is $L_2(7)$, $L_2(11)$, or $L_5(2)$. It does not stop after identifying
the socle of the original group, assume a minimal counterexample, or require
`CMP` to pass to sections.

The positive direction asks only whether each listed simple group can occur.
Levchuk--Likharev's theorem says that each simple group itself has `CMP`, so
no extension-existence or cohomology assertion is needed.

## Consistency and notation audit

The abstract, Theorem 1.1, proof conclusion, README, problem statement, and
claim ledger all state the same three groups and the same CFSG-conditional
scope. The complement convention is consistently the exact factorization
$G=MK$ with $M\cap K=1$. Coordinate groups are always almost simple;
$k$ is the chief-factor multiplicity; $f,r,d$ are used only in the even
symplectic subfield argument.

A repository-wide scan found no acceptance-critical `TODO`, `PENDING`, bare
Python `assert`, obsolete degree 136 claim, or live use of the withdrawn
$O_4^+$-normalizer. Historical reports containing the old claim remain for
provenance and are now explicitly marked superseded.

## Closure of earlier P3 items

- The missing backslash in one `reviews/01-revision.md` display was restored
  with an explicit editorial note.
- The BHRD access boundary remains disclosed; the exact row is triangulated by
  Burness and Harper and is flagged for an external referee with book access.
- The host-based fresh-clone environment records and enforces all
  acceptance-critical versions plus the Tectonic bundle hash.
- The README and manuscript distinguish a claimed complete proof from an
  externally established result.
- The manuscript now carries an explicit AI-use disclosure. AI tools are not
  listed as authors or referees, and the named author remains solely
  responsible for verification and submission.

## Release-artifact audit

The pinned build wrapper was rerun after the disclosure change and recorded
two byte-identical clean builds. The final artifact hashes are:

```text
TeX  d01d3a0212eaf1b965f25d5076254b6500933c13c2bb95665b5f4aeedf7d81f4
PDF  9fa44095bcfde9c0592b6bdd7529f86da7e31ed59d875cf5a63a72eadc3948fb
```

All three data certificates are unchanged from Referee 3. The 12-page PDF was
rendered after rebuilding; the disclosure and bibliography fit without
clipping or overflow.

The standalone release will be version 1.0.2. Its release notes and Zenodo
description must state prominently that versions 1.0.0 and 1.0.1 contained a
proof gap: the claimed $N_X(\Omega_4^+(4))$ action for
$X=\operatorname{Aut}(Sp_4(4))$ had degree 272 and did not supplement the
socle. Version 1.0.2 replaces it with the prime-degree subfield action of
degree 1360. The earlier records are preserved, not silently overwritten.

## Remaining boundary

No internal P0--P2 issue is open. CFSG and the cited exhaustive
classifications remain published inputs, and the BHRD table should be checked
by a referee with direct access. No independent external finite-group
specialist has yet reviewed the proof. The next step is a frozen hard-final
Referee 4 pass; only that pass may recommend external circulation.
