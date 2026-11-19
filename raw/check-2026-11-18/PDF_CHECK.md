# Build and PDF inspection

## Commands and initial result

The baseline audit uses an isolated byte-identical copy of the three checked source trees. The build runner invokes pdfLaTeX three times for each French main file and XeLaTeX four times for the English main file. A complete TeX Live installation can use these direct commands from each respective source directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error gaga.tex
pdflatex -interaction=nonstopmode -halt-on-error gaga.tex
pdflatex -interaction=nonstopmode -halt-on-error gaga.tex
```

```sh
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
```

For the supplied audit runner, from the deliverable root:

```sh
python scripts/build_audit.py --sources sources --output build/after --texmf ../toolchain/texmf --formats ../toolchain/formats
```

The last two options are only needed for this runtime's repaired TeX cache; see `scripts/TOOLCHAIN.md`. No package substitution or dependency omission was made in the edition to accommodate this runtime.

| Layer | Required passes | Baseline errors, all passes | Baseline overfull boxes, all passes | Baseline pages |
|---|---:|---:|---:|---:|
| French as printed | 3 | 0 | 0 | 24 |
| Corrected French | 3 | 0 | 0 | 24 |
| English | 4 | 0 | 0 | 26 |

Every baseline pass exits 0. There are no boxes exceeding 2pt and therefore no pages with overflow above 10pt requiring a before/after overflow inspection. The French logs have no warnings. English pass 1 has the expected unresolved-reference/rerun warnings from a clean build; subsequent passes resolve them. XeLaTeX reports that `inputenc` is ignored by its Unicode engine; this harmless warning remains. Complete per-pass warnings and sanitized logs are retained in `build/before/`.

## Final visual check and disposition

Primary reader: GPT-6 Astra (ChatGPT Pro mode). PDF pages here mean output-PDF page numbers, not the 1956 printed-page numbers. Working renders use Poppler at 140 dpi; details were enlarged where needed. Full-page working images are excluded from the deliverable.

The baseline diplomatic French pages 1, 4 and 7 were inspected. The footnote-text marker on PDF p. 1 appeared as a baseline `1.` instead of the parenthesized raised number visible on printed p. 2. Babel's begin-document setup overrode the existing custom formatter. Ledger data records 2395–2396 add `\frenchsetup{FrenchFootnotes=false}` to the two French preambles. The formatter, article text and numbering stay unchanged. Compare `evidence/p02-bundles-footnote.png`, `evidence/build-french-footnote-before.png` and `evidence/build-french-footnote-after.png`.

Both French layers were then rebuilt for all three passes from the final sources. Every one of those six passes exits 0, has zero errors, zero warning headings, zero missing glyphs and zero overfull boxes. The largest overflow is therefore 0pt both before and after. Final English is the unchanged, four-pass baseline PDF. No pass in any layer had an overflow over 10pt, so there are no overflow pages requiring a separate before/after image pair.

| Final layer | PDF pages rendered and visually inspected | Result |
|---|---|---|
| French as printed | 1, 4, 7, 8, 11, 12, 15, 18, 19, 21, 22, 23, 24 | Clear text and formulas, separated diagram nodes/arrows, all six corrected footnote markers, no clipping or overlap |
| Corrected French | 1, 4, 7, 8, 11, 12, 15, 18, 19, 21, 22, 23, 24 | Same checks passed; all six footnote markers inspected |
| English | 1, 4, 7, 10, 11, 12, 13, 14, 17, 20, 22, 23, 24, 26 | Title and contents through bibliography; every diagram and all footnotes clear; no clipping or overlap |

The French spread includes every diagram (output pp. 11, 12, 19, 21, 23), both paragraphs producing underfull-box diagnostics (pp. 15, 18), the local-algebra appendix and the bibliography. The English spread includes every diagram (pp. 11, 12, 13, 20, 22, 24). An apparent paragraph join on French p. 7 was checked in enlarged rendering and by coordinates: the new paragraph is indented and on its own baseline. An apparent crowded arrow on corrected French p. 19 was enlarged: its symbols are correctly separated. Neither needed a source change.

## Warnings and remaining diagnostics

The two French underfull boxes recur on each before/after pass: badness 1881 at body lines 724–726, output p. 15, and badness 1715 at lines 863–864, output p. 18. Both paragraphs were visually inspected and are readable; they have no protrusion. Underfull badness is not an overflow size. No line-breaking adjustment was needed.

English pass 1 has 250 warning headings, chiefly 245 undefined hyperreferences from a clean build plus summaries/rerun notices and the Unicode-engine `inputenc` notice. Pass 2 has two warnings (rerun and `inputenc`); passes 3 and 4 have only `inputenc`. All references settle. The package is harmlessly ignored under XeLaTeX; retained to preserve the supplied preamble.

Final French PDFs each have 24 pages and embed all 25 fonts. English has 26 pages and embeds all 28 fonts. Hashes, metadata, fonts and complete sanitized per-pass diagnostics are in `build/after/` for the final French and `build/before/` for English. The baseline English source hashes are unchanged. There are no raw source paths in the returned logs, and no intermediate PDFs or auxiliary TeX products are included.

**Gate closed: 2026-11-18 14:16:00 UTC.** Every required pass and the final visual spread pass. The programme, notes and Stacks context may now be read for `NOTES.md`.
