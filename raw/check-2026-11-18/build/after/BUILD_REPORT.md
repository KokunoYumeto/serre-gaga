# French after-build audit

The two French layers were rebuilt from an isolated snapshot after the primary reader added the Babel `FrenchFootnotes=false` setting. The snapshot contains four French files and was taken when the correction ledger contained 2396 records. English was not rebuilt; its final four-pass evidence remains in `build/before`.

All six requested pdfLaTeX passes completed with exit status 0, 24 PDF pages, zero errors, zero warning headings, zero missing-glyph diagnostics and zero overfull boxes. The maximum overfull excess is 0pt in every pass, satisfying the no-overflow-beyond-2pt gate for every requested pass.

Each pass has the same two underfull horizontal boxes: badness 1881 at `gaga_body.tex` lines 724–726 and badness 1715 at lines 863–864. Output pages are estimated as 15 and 18 from line-initial shipout markers. These are inferred associations, not layout judgments. `underfull.tsv` and `all_diagnostics.tsv` retain the complete details.

All four current French source hashes match their isolated snapshot before and after the build. The actual commands did not alter current sources or the correction ledger. `passes.tsv` records every pass; `pass_details.tsv` adds underfull and missing-glyph counts. Each pass has a separate sanitized log and stdout capture. Per-pass PDFs and all TeX intermediates remain in the scratch build tree; only text evidence is copied here.

The last-pass French PDFs replace the French reader copies in `pdf`. The baseline PDFs remain in the earlier scratch build tree. Both final French PDFs contain 24 A4 pages and all font records are embedded. Their exact hashes, sizes, page counts and font totals are in `reader_pdfs.tsv`; `font_embedding.tsv` and the per-layer `pdfinfo.txt` / `pdffonts.txt` retain the checks. The primary reader performs the visual review separately; this build task did not render or inspect page images.

## Reproduction

From the workspace root, with the supplied isolated French source snapshot and repaired toolchain:

```text
python GAGA_CHECK/scripts/build_audit.py --sources work/build-after/sources --output work/build-after/audit --texmf toolchain/texmf --formats toolchain/formats --layer french-diplomatic --layer french-corrected --keep-going
```
