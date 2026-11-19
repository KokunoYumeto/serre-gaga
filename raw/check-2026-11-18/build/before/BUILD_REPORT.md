# Actual baseline build audit

**Baseline status:** this directory records the pre-layout-fix snapshot. The reader PDF names identify the copies made at baseline time; subsequent reader replacements require their own after-build evidence. French footnote configuration is being handled separately by the primary reader.

All 10 requested passes completed with exit status 0. Every pass has zero errors, zero missing-glyph diagnostics and zero overfull boxes; the maximum overfull excess is 0pt throughout. No edition source or preamble was changed.

The isolated snapshot contains 14 source files, all checked against the current edition before and after building. The ledger contained 2394 correction records at snapshot time. See the source hashes and snapshot metadata.

## Every-pass results

| Layer | Pass | PDF pages | Errors | Warning headings | Underfull boxes | Overfull boxes | Maximum overflow |
|---|---:|---:|---:|---:|---:|---:|---:|
| french-diplomatic | 1 | 24 | 0 | 0 | 2 | 0 | 0pt |
| french-diplomatic | 2 | 24 | 0 | 0 | 2 | 0 | 0pt |
| french-diplomatic | 3 | 24 | 0 | 0 | 2 | 0 | 0pt |
| french-corrected | 1 | 24 | 0 | 0 | 2 | 0 | 0pt |
| french-corrected | 2 | 24 | 0 | 0 | 2 | 0 | 0pt |
| french-corrected | 3 | 24 | 0 | 0 | 2 | 0 | 0pt |
| english | 1 | 25 | 0 | 250 | 0 | 0 | 0pt |
| english | 2 | 26 | 0 | 2 | 0 | 0 | 0pt |
| english | 3 | 26 | 0 | 1 | 0 | 0 | 0pt |
| english | 4 | 26 | 0 | 1 | 0 | 0 | 0pt |

## Diagnostics

Both French layers report two underfull hboxes on every pass: badness 1881 at body-source lines 724–726 and badness 1715 at lines 863–864. These are underfull diagnostics, not positive overflow amounts. The inferred output pages are 15 and 18 respectively. Their source locations and inferred output pages are retained in `underfull.tsv`.

English first-pass reference and outline warnings resolve during the requested reruns. Pass 2 still asks for a label rerun; passes 3 and 4 retain only the warning that inputenc is ignored by the UTF-8 engine. Exact per-pass categories and complete diagnostic blocks are retained in `passes.tsv` and `all_diagnostics.tsv`. Package-description text describing warning/error facilities is not counted as a diagnostic.

No pass has an overflow greater than 10pt, so there are no overflow-triggered pages to render. The initial runner retained each pass log but only the last PDF per layer. Its lack of earlier-pass PDFs does not omit any required overflow preview, because every pass was overflow-free. English pagination changed from 25 pages on pass 1 to 26 on passes 2–4.

## Metadata and fonts

The last-pass baseline reader PDFs have 24 diplomatic-French pages, 24 corrected-French pages and 26 English pages. The PDF metadata and complete font tables are preserved per layer. Every listed font is embedded; the per-font table and reader checksums are in `font_embedding.tsv` and `reader_pdfs.tsv`.

## Visual review handoff

The specified representative pages were rendered at 140 dpi from the baseline reader copies into scratch for the primary reader. No rendered image was opened or assessed by this build worker. The primary reader must record its visual inspection separately.

French pages requested in each layer: 1, 4, 7, 10, 13, 16, 19, 22, 24. English pages: 1, 4, 7, 10, 14, 17, 20, 23, 26.
