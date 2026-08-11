# Manuscript

`kourovka-18-68.tex` is the peer-review draft proving the three-factor
answer to Kourovka Problem 18.68.

Build from this directory with:

```sh
SOURCE_DATE_EPOCH=1786406400 tectonic kourovka-18-68.tex
```

The proof depends on the published exhaustive factorization classifications
listed in the bibliography.  The proof-critical computation consists of
five named small alternating coordinate groups and the ten almost-simple
groups with socle \(L_3(4)\), and is reproduced by:

```sh
cd ..
gap -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
```
