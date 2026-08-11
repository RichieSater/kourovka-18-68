#############################################################################
## Generate deterministic exact CMP certificates for every TomLib table.
##
## Producer command (from the repository root):
##     gap -q gap/generate-tomlib-scan.g
#############################################################################

Read("gap/cmp_tom.g");

names := ShallowCopy(AllLibTomNames());;
Sort(names);

summaryPath := "data/tomlib-cmp-scan.tsv";;
maximalPath := "data/tomlib-cmp-maximals.tsv";;

summaryStream := OutputTextFile(summaryPath, false);;
maximalStream := OutputTextFile(maximalPath, false);;
if summaryStream = fail or maximalStream = fail then
    Error("CMP: could not open output TSV files");
fi;
SetPrintFormattingStatus(summaryStream, false);
SetPrintFormattingStatus(maximalStream, false);

PrintTo(summaryStream,
    "# producer\tgap -q gap/generate-tomlib-scan.g\n",
    "# gap_version\t", GAPInfo.Version, "\n",
    "# tomlib_version\t", CMPPackageVersion("tomlib"), "\n",
    "# semantics\texact relative to the complete subgroup-class and ",
    "intersection data in each supplied TomLib table\n",
    "table_name\tgroup_order\tsubgroup_classes\tmaximal_classes\t",
    "normal_classes\tnonabelian_simple\tsolvable\tchief_factor_orders\t",
    "cmp\tfailed_maximal_classes\n");

PrintTo(maximalStream,
    "# producer\tgap -q gap/generate-tomlib-scan.g\n",
    "# gap_version\t", GAPInfo.Version, "\n",
    "# tomlib_version\t", CMPPackageVersion("tomlib"), "\n",
    "# candidate_field\tclass_position:trivial_intersection_multiplicity; ",
    "none means that no subgroup class has the required order\n",
    "table_name\tgroup_order\tmaximal_class\tmaximal_label\t",
    "maximal_order\tindex\tcomplemented\twitness_class\tcandidates\n");

positiveCount := 0;;
for name in names do
    certificate := CMPTableOfMarksCertificate(name);
    if certificate.cmp then
        positiveCount := positiveCount + 1;
    fi;

    if Length(certificate.chief_factor_orders) = 0 then
        chiefText := "not_computed";
    else
        chiefText := CMPJoinIntegers(certificate.chief_factor_orders, ",");
    fi;
    if Length(certificate.failed_maximal_classes) = 0 then
        failedText := "none";
    else
        failedText := CMPJoinIntegers(certificate.failed_maximal_classes, ",");
    fi;

    PrintTo(summaryStream,
        certificate.table_name, "\t",
        certificate.group_order, "\t",
        certificate.subgroup_class_count, "\t",
        certificate.maximal_class_count, "\t",
        certificate.normal_class_count, "\t",
        certificate.nonabelian_simple, "\t",
        certificate.solvable, "\t",
        chiefText, "\t",
        certificate.cmp, "\t",
        failedText, "\n");

    for row in certificate.maximal_rows do
        if row.witness_class = fail then
            witnessText := "none";
        else
            witnessText := String(row.witness_class);
        fi;
        PrintTo(maximalStream,
            certificate.table_name, "\t",
            certificate.group_order, "\t",
            row.maximal_class, "\t",
            row.maximal_label, "\t",
            row.maximal_order, "\t",
            row.index, "\t",
            row.complemented, "\t",
            witnessText, "\t",
            CMPFormatCandidateRows(row.candidates), "\n");
    od;
od;

CloseStream(summaryStream);
CloseStream(maximalStream);

Print("WROTE ", summaryPath, " and ", maximalPath, "\n");
Print("TABLES ", Length(names), "; CMP-positive ", positiveCount,
      "; CMP-negative ", Length(names) - positiveCount, "\n");

QUIT_GAP(0);
