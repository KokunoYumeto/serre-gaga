# TeX toolchain and audit scripts

## Scope

Toolchain preparation used synthetic text and the two supplied preambles.
Actual edition builds were then run after the primary reader completed the
sequential page collation and second reading. The accepted final build evidence
is the English four-pass sequence in `build/before` and the two French
three-pass sequences in `build/after`. The earlier French baseline evidence is
retained in `build/before`. The primary reader performs all scan reading and
final visual PDF inspection.

## Runtime repair

The runtime supplies pdfTeX 3.141592653-2.6-1.40.26 and XeTeX
3.141592653-2.6-0.999996, both labelled TeX Live 2025/dev/Debian. Its installed
LaTeX kernel is LaTeX2e 2024-11-01, patch level 2. Poppler 26.05.0 provides the
PDF rendering and font-inspection utilities.

The installed TeX data initially lacked its generated filename database,
formats and PDF font map, and the Babel French and ulem packages were absent.
`prepare_toolchain.py` repairs these runtime omissions in a separate cache:

- It permits ordinary filesystem lookup of the existing readable TeX trees.
- It downloads and checks SHA-256 hashes for four unmodified packages from the
  [official frozen TeX Live 2024 archive](https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/archive/):
  babel-french, hyphen-french, hyph-utf8 and ulem.
- It creates pdfLaTeX and XeLaTeX formats with English and French hyphenation.
- It combines the installed CM, AMS, Euler, RSFS and Latin Modern font maps,
  retaining 755 distinct entries.

The frozen Babel French version is 3.6c, dated 2024-07-25; ulem identifies itself
as 2019/11/18. A trial with the moving 2026 Babel French package failed because
it requires a kernel command absent from this runtime. The frozen version is
compatible with the installed kernel. No edition preamble was changed to omit
or substitute a dependency.

Both unmodified edition preambles compiled synthetic specimens successfully.
The specimens exercised accented French, Gothic letters, calligraphic and
script letters, subscripts and superscripts, blackboard bold, underlining and a
commutative diagram. Font inspection found embedded Type 1 fonts in the
pdfLaTeX specimen and embedded Type 1C fonts in the XeLaTeX specimen.

## Reproduction in this minimal runtime

From the deliverable root:

```sh
python scripts/prepare_toolchain.py --cache ../toolchain
python scripts/build_audit.py --sources sources --output ../work/rebuild/audit --texmf ../toolchain/texmf --formats ../toolchain/formats
```

The first command is unnecessary on a complete TeX Live installation. In that
case the audit command can omit `--texmf` and `--formats`. Ordinary direct builds
are three pdfLaTeX passes on `gaga.tex` in each French directory and four XeLaTeX
passes on `GAGA_English_source_aligned.tex` in the English directory.

The package archives, unpacked dependency files, format binaries and synthetic
specimens are runtime caches and are not edition deliverables.
For an isolated build, first copy `sources` into a scratch directory and pass
that copy to `--sources`. The recorded builds used verified scratch copies;
their source hashes are included with the evidence. Use a new output directory
when preserving an earlier build is required.

## Build audit output

`build_audit.py` preserves a sanitized engine log and captured console output
for each pass. It also writes:

- `summary.tsv`: final-pass engine status, counts of errors and warnings,
  overfull-box counts, counts exceeding 2pt and 10pt, maximum excess and PDF
  creation status.
- `overfull.tsv`: every overfull hbox or vbox on every pass, including its exact
  excess, reported source line range and inferred source file and output page.
- `warnings.tsv`: every warning or error heading on every pass.
- `passes.tsv`: separate status and overflow totals for every pass. The final
  acceptance threshold applies to every requested pass, not merely the last.

The script returns a failure status if any requested pass fails, records an
error, or has an overfull box exceeding 2pt. An earlier failure remains a
failure even when `--keep-going` allows later passes to finish successfully.

The source-file association uses the latest TeX input marker; the output-page
association uses the next line-initial shipout marker. Bracketed citations
inside box diagnostic text are excluded from marker matching. Adjacent or
wrapped shipout tokens can be missed, so these associations are explicitly
labelled as inferred and must be verified against the relevant PDF for visual
review. Source-line ranges and excess sizes are reported directly by TeX.

A synthetic input containing a box exactly 12pt wider than the text measure
validated the reporting pipeline: all three pdfLaTeX passes reported one 12pt
overflow, assigned to the included source file at line 1 and output page 1.
The saved logs contained no workspace, system-installation or home-directory
prefixes.

The audit copies a successfully built PDF to its corresponding audit directory.
It also retains `pass-NN.pdf` for every successful pass, so an earlier-pass
overflow can be inspected against that pass's actual pagination. These PDFs
remain build-work artifacts; delivery copies of audit evidence should contain
the sanitized text logs and tables, with final reader PDFs in the designated
PDF directory only.
The engine also leaves ordinary generated files in the source directory. Those
raw generated files are not source deliverables; only sanitized audit logs
should be included in the final package. The script does not change any TeX
source file.
