CheckEnvironmentRequire := function(condition, message)
    if not condition then
        Error(Concatenation("environment check: ", message));
    fi;
end;

CheckEnvironmentRequire(GAPInfo.Version = "4.15.1", "expected GAP 4.15.1");
CheckEnvironmentRequire(LoadPackage("tomlib") = true, "TomLib unavailable");
CheckEnvironmentRequire(PackageInfo("tomlib")[1].Version = "1.2.11",
                        "expected TomLib 1.2.11");
CheckEnvironmentRequire(LoadPackage("atlasrep") = true, "AtlasRep unavailable");
CheckEnvironmentRequire(PackageInfo("atlasrep")[1].Version = "2.1.11",
                        "expected AtlasRep 2.1.11");
Print("PINNED GAP ENVIRONMENT PASSED: GAP 4.15.1, TomLib 1.2.11, ",
      "AtlasRep 2.1.11\n");
QUIT_GAP(0);
