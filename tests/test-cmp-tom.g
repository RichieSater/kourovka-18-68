#############################################################################
## Regression tests for gap/cmp_tom.g
##
## Run from problem-18-68/ with:
##     gap --quitonbreak -q tests/test-cmp-tom.g
#############################################################################

Read("gap/cmp_tom.g");

CMPAssert := function(condition, message)
    if not condition then
        Print("TEST FAILURE: ", message, "\n");
        QUIT_GAP(1);
    fi;
end;


# Published positive simple fixtures.
for name in ["L2(7)", "L2(11)", "L5(2)"] do
    certificate := CMPTableOfMarksCertificate(name);
    CMPAssert(certificate.cmp,
              Concatenation(name, " should be CMP-positive"));
    CMPAssert(certificate.nonabelian_simple,
              Concatenation(name, " should be detected as nonabelian simple"));
    CMPAssert(ForAll(certificate.maximal_rows,
                     row -> row.complemented
                            and row.witness_class <> fail),
              Concatenation(name,
                            " must have a witness for every maximal class"));
od;


# Source-backed and structural negative controls.
for name in ["A5", "S5", "L2(7).2", "(A5xA5):2"] do
    certificate := CMPTableOfMarksCertificate(name);
    CMPAssert(not certificate.cmp,
              Concatenation(name, " should be CMP-negative"));
    CMPAssert(Length(certificate.failed_maximal_classes) > 0,
              Concatenation(name, " must expose a failed maximal class"));
od;

CMPAssert(CMPTableOfMarksCertificate("A5").nonabelian_simple,
          "A5 should be detected as nonabelian simple");
CMPAssert(not CMPTableOfMarksCertificate("S5").nonabelian_simple,
          "S5 should not be detected as simple");


# PGL_2(7) = L2(7).2 has a maximal subgroup of order 12 and index 28,
# while its table of marks has no subgroup class of order 28.  This tests the
# exhaustive zero-candidate branch rather than only a failed intersection.
certificate := CMPTableOfMarksCertificate("L2(7).2");
rows := Filtered(certificate.maximal_rows,
                 row -> row.maximal_order = 12 and row.index = 28);
CMPAssert(Length(rows) = 1,
          "L2(7).2 should have one maximal-class row of order 12/index 28");
CMPAssert(not rows[1].complemented and Length(rows[1].candidates) = 0,
          "the order-12 maximal of L2(7).2 must have no order-28 candidate");


# A positive control with more than one subgroup class at some relevant
# orders guards against replacing the intersection test by order alone.
certificate := CMPTableOfMarksCertificate("L2(7)");
CMPAssert(certificate.maximal_class_count = 3,
          "L2(7) should have three maximal subgroup classes in TomLib");
CMPAssert(ForAll(certificate.maximal_rows,
                 row -> ForAny(row.candidates,
                               c -> c.trivial_intersection_multiplicity > 0)),
          "L2(7) witnesses must use a positive trivial-intersection count");


# Soluble sanity checks: S4 is a TomLib positive.  We compute complete tables
# directly for cyclic order 4 (negative) and dihedral order 8 (positive).
# The latter pair supports the hand-checked warning that CMP is not inherited
# by normal subgroups: C4 is normal in D8.
certificate := CMPTableOfMarksCertificate("S4");
CMPAssert(certificate.cmp, "S4 should be CMP-positive");

certificate := CMPTableOfMarksCertificateFromTable(
                   TableOfMarks(CyclicGroup(4)), "C4-computed");
CMPAssert(not certificate.cmp, "C4 should be CMP-negative");

certificate := CMPTableOfMarksCertificateFromTable(
                   TableOfMarks(DihedralGroup(IsPermGroup, 8)),
                   "D8-computed");
CMPAssert(certificate.cmp, "D8 should be CMP-positive");

Print("ALL CMP TABLE-OF-MARKS TESTS PASSED\n");
Print("GAP ", GAPInfo.Version, "; TomLib ",
      CMPPackageVersion("tomlib"), "\n");
QUIT_GAP(0);
