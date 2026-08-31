#############################################################################
##
##  Produce the finite factor-free certificates used in the proof of 18.68.
##  Run from problem-18-68 with GAP 4.15.1 and TomLib 1.2.11:
##
##      gap --quitonbreak -q gap/generate-factor-free-scan.g
##
#############################################################################

# Delete the old certificate before any package or version check.  Together
# with --quitonbreak this prevents a failed producer run from leaving a stale
# file that a later checker could mistake for fresh output.
outputPath := "data/tomlib-factor-free.tsv";
if IsExistingFile(outputPath) and RemoveFile(outputPath) <> true then
    Error("factor-free producer: could not remove stale output");
fi;

Read("gap/factor_free_tom.g");

if GAPInfo.Version <> "4.15.1" then
    Error("factor-free producer: expected GAP 4.15.1");
fi;
if PackageInfo("tomlib")[1].Version <> "1.2.11" then
    Error("factor-free producer: expected TomLib 1.2.11");
fi;

# The class positions are part of the pinned TomLib certificate.  The first
# five rows close the small alternating cases not handled uniformly.  The
# next ten rows exhaust the almost-simple coordinate groups with socle
# L3(4), the one small linear parameter left by the uniform split-torus
# screen.  The remaining rows independently check selected sporadic
# factor-screen entries for which TomLib has complete tables.
targets := [
    ["A6.2_2", 18, 16, 45, "alternating-small"],
    ["A6.2_3", 17, 20, 36, "alternating-small"],
    ["A6.2^2", 49, 32, 45, "alternating-small"],
    ["A7", 35, 72, 35, "alternating-small"],
    ["S7", 90, 144, 35, "alternating-small"],
    ["L3(4)", 94, 960, 21, "linear-small"],
    ["L3(4).2_1", 145, 384, 105, "linear-small"],
    ["L3(4).2_2", 150, 1920, 21, "linear-small"],
    ["L3(4).2_3", 99, 720, 56, "linear-small"],
    ["L3(4).3", 86, 216, 280, "linear-small"],
    ["L3(4).2^2", 280, 768, 105, "linear-small"],
    ["L3(4).3.2_2", 205, 432, 280, "linear-small"],
    ["L3(4).3.2_3", 137, 1152, 105, "linear-small"],
    ["L3(4).6", 138, 1152, 105, "linear-small"],
    ["L3(4).D12", 397, 2304, 105, "linear-small"],
    ["M11", 34, 120, 66, "sporadic-cross-check"],
    ["M12", 127, 192, 495, "sporadic-cross-check"],
    ["M12.2", 194, 216, 880, "sporadic-cross-check"],
    ["M22.2", 476, 1440, 616, "sporadic-cross-check"],
    ["M23", 200, 20160, 506, "sporadic-cross-check"],
    ["J2", 144, 2160, 280, "sporadic-cross-check"],
    ["J2.2", 369, 4320, 280, "sporadic-cross-check"],
    ["HS", 583, 40320, 1100, "sporadic-cross-check"],
    ["HS.2", 2055, 80640, 1100, "sporadic-cross-check"]
];

out := OutputTextFile(outputPath, false);
if out = fail then
    Error("factor-free producer: could not open output TSV");
fi;
SetPrintFormattingStatus(out, false);
AppendTo(out,
    "# producer\tgap --quitonbreak -q gap/generate-factor-free-scan.g\n");
AppendTo(out, "# gap_version\t", GAPInfo.Version, "\n");
AppendTo(out, "# tomlib_version\t", PackageInfo("tomlib")[1].Version, "\n");
AppendTo(out,
    "table_name\tgroup_order\tsocle_class\tsocle_order\tmaximal_class",
    "\tmaximal_order\tsocle_intersection_order\tindex\tscope",
    "\tcorefree_factor_count\tfactor_free\n");

for target in targets do
    cert := FFCertificateTom(target[1], target[2]);
    if cert.maximal_order <> target[3] or cert.index <> target[4] then
        Error(Concatenation("factor-free producer: pinned row changed for ",
                            target[1]));
    fi;
    if not cert.factor_free then
        Error(Concatenation("factor-free producer: witness failed for ",
                            target[1]));
    fi;
    if cert.socle_intersection_order <= 1 then
        Error(Concatenation("factor-free producer: trivial socle intersection for ",
                            target[1]));
    fi;
    AppendTo(out,
        cert.table_name, "\t", cert.group_order, "\t",
        cert.socle_class, "\t", cert.socle_order, "\t",
        cert.maximal_class, "\t", cert.maximal_order, "\t",
        cert.socle_intersection_order, "\t", cert.index, "\t", target[5], "\t",
        Length(cert.corefree_factor_rows), "\t", cert.factor_free, "\n");
od;

CloseStream(out);
Print("FACTOR-FREE TOMLIB SCAN PASSED: ", Length(targets),
      " pinned maximal classes\n");
QUIT_GAP(0);
