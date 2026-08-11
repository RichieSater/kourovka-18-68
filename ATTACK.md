# Planned attack

This plan refines Stage 2 of the root attack order. Deliverable A and the
quotient/normal-subgroup parts of B are complete; C has an exact bounded
TomLib audit; D has a proved chief-factor reduction.  The product-action,
family-screen, and prime-divisibility closeouts have now passed, yielding the
complete manuscript in `paper/`.

## Deliverable A — exact property and fixtures

- Read Levchuk--Likharev and the Maslova/Revin papers in full.
- Fix the complement convention and identify any equivalent factorization
  test.
- Implement a maximal-class loop that returns an explicit complement for every
  positive class or one maximal subgroup with a certified failure.
- Validate the simple positive groups
  \(L_2(7),L_2(11),L_5(2)\) and source-backed negative simple controls.

**Gate A: passed (2026-08-11).** Exact source pinpoints, tested
product/intersection witnesses, and fail-closed Table-of-Marks behavior are in
the notes, code, and tests.

## Deliverable B — inheritance audit

Treat separately:

1. quotients by arbitrary normal subgroups;
2. quotients by subgroups inside the Frattini subgroup;
3. normal subgroups and arbitrary sections;
4. direct products;
5. split and nonsplit extensions.

Every positive inheritance statement needs a construction of the required
complement; every failure needs a smallest practical counterexample.

**Gate B: partly passed.** Quotients are proved and normal inheritance is
disproved. Direct products, Frattini extensions, and arbitrary nonsplit
extensions remain open as general closure questions. The chief-factor
reduction does not depend on positive answers to those questions.

## Deliverable C — bounded reconnaissance

- Scan a declared SmallGroups/perfect-groups range.
- Scan a declared set of primitive groups with abelian and nonabelian socles.
- Record `CMP`, maximal-class witnesses, composition factors, socle, soluble
  radical, and primitive action type.
- Test the three-factor conjecture and actively search for an extension that
  violates it.

Positive verdicts require exhaustive maximal-class coverage and exhaustive
complement search within the declared group. Negative verdicts require one
verified maximal subgroup with no complement, plus a transparent completeness
argument for the candidate complement orders/classes.

**Bounded result:** all 414 TomLib 1.2.11 tables and all 2,395 of their maximal
classes have exact certificates. This is not CFSG-wide coverage.

## Deliverable D — primitive/monolithic reduction

- Use the inheritance audit to choose the correct minimal object.
- Separate affine primitive groups from groups with socle \(S^k\).
- For nonabelian socle, classify maximal subgroups by top, product, and
  diagonal behavior only after checking whether the 10.34 trichotomy applies
  to the exact ambient group.
- Track how an arbitrary nonabelian composition factor appears through the
  normal series; do not replace composition-factor control with socle control.

**Gate D: passed.** Every nonabelian composition factor \(S\) yields a
`CMP` monolithic quotient with unique self-centralizing socle \(S^t\) and a
faithful primitive action.  For every suitable coordinate action, the same
group has a primitive product action on \((X/H)^t\).  LPS Corollary 3(iv)
reduces the arbitrary exponent \(t\) to an almost-simple factor screen.

## Deliverable E — extension and cohomology layer

- Identify the precise complement theorem required in each primitive case.
- If using \(H^1\), specify module, acting group, and whether the result proves
  existence, conjugacy, or counts complements.
- Treat nonsplit extensions explicitly; a scan of split semidirect products is
  not exhaustive evidence.

**Gate E: rendered unnecessary for the composition-factor question.**  The
quotient and product-action construction treats split and nonsplit ambient
groups uniformly; no complement-conjugacy or cohomology assertion is used.

## Deliverable F — classification closeout

If the working conjecture survives, produce a section-safe proof that every
nonabelian composition factor is one of the three simple groups. If it fails,
record the smallest explicit counterexample and revise the target before any
CFSG-wide campaign.

**Gate F: passed through internal Referee 4 (2026-08-11).**  The CFSG family screen
is in `notes/05-family-factor-screen.md`, with an exact row audit in
`notes/07-classification-containment-ledger.md`.  The sole infinite survivor
\(\operatorname{PSp}_4(2^f)\) is eliminated for every \(t\) and every
field-only or graph-outer coordinate group by the corrected prime-degree
subfield action and 2-adic socle-valuation lemma.  Fifteen named small cases
have complete Table-of-Marks certificates. Structural, source,
fresh-clone reproducibility, and hard-final referee passes are complete. The
hard-final recommendation is to circulate; external specialist review remains
pending.
