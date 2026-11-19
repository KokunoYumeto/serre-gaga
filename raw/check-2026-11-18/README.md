# GAGA: complete second-pass check

Jean-Pierre Serre, *Géométrie algébrique et géométrie analytique*, Annales de l'Institut Fourier 6 (1956), printed pp. 1–42. Checked on 18 November 2026 by GPT-6 Astra in ChatGPT Pro mode; the reasoning-effort setting was not exposed.

All 42 printed pages were read in order against the supplied Numdam scan in a single primary-reader stream: French as printed, corrected French, then English. Every correction received a second reading; recurring error classes were searched across the work. All three layers build and passed the recorded PDF inspection. The notes were written only after that gate closed, at 14:16 UTC. The page readings were not delegated. Assistance with tooling, record inventories and later-source research did not decide printed readings.

The input edition is repository main `6306315`, release `edition-2026-11-06`. The scan alone controlled this check; no other edition or translation of GAGA was consulted. Both supplied READMEs remain byte-identical, including all rights statements and the Thomas Waring credit. The provenance and credit text in the source trees is retained. This delivery README supplements those notices.

## Results and counts

There are **2,396 correction-ledger records: 2,395 retained changes and one withdrawn change**. These are individual source edits, predominantly restorations of mathematical typefaces. They are not 2,396 mathematical errors. Existing corrected-layer emendations were adjudicated separately and are not counted again as newly made edits.

| Layer | Reading | Original misprint | Translation | Typesetting | Structure | Ledger records | Retained changes |
|---|---:|---:|---:|---:|---:|---:|---:|
| French as printed | 15 | 0 | 0 | 715 | 3 | 733 | 733 |
| Corrected French | 13 | 3 | 0 | 715 | 3 | 734 | 734 |
| English | 3 | 0 | 52 | 870 | 2 | 927 | 926 |
| Build preambles | 0 | 0 | 0 | 2 | 0 | 2 | 2 |
| Total | 31 | 3 | 52 | 2,302 | 8 | 2,396 | 2,395 |

All 2,396 records have second-reading dispositions. Confidence is high for 2,394 and medium for two: the terminal mark following the title, transcribed as a period in both French layers. Its physical origin remains uncertain. The withdrawn English record is retained as a documented no-op, not silently removed from the history.

The final French bodies differ at 16 local places on 15 printed pages, each with a retained misprint justification. The inherited-record crosswalk covers all 134 identifiers. Five printed pages in each layer required no newly found retained change: French as printed and corrected, 10, 15, 28, 33, 42; English, 1, 7, 10, 16, 42. A confirmed inherited emendation is not counted as a new change.

Substantive decisions include restoring the printed analytic ideal letter A and algebraic ideal letter J at their respective places; retaining the printed capital X in diplomatic French at p. 11 while correcting it to the point x in the other layers; correcting the p. 24 FAC reference to [18]; and withdrawing unsupported emendations of the tensor base on p. 18 and equation (8) on p. 26. `CHECK_RECORD.md` lists all mathematical-symbol and reference decisions individually, with ledger or inherited-verdict identifiers. `NOTES.md` explains their reasons.

## What the files contain

| File or directory | Purpose |
|---|---|
| `sources/` | Complete three-layer TeX edition in the supplied directory layout, with the two original READMEs. |
| `pdf/` | Final reader PDFs: French diplomatic, corrected French and English. |
| `CORRECTIONS.tsv` | Required old/new/evidence ledger. Data-record numbers start at 1 after the header; a quoted multiline record can occupy several physical TSV lines. |
| `CHECK_RECORD.md` | Notation table, totals, substantive decisions and all 42 page records, including source ranges, comparisons, counts and completion times. |
| `SECOND_READING.tsv` | Every ledger record's confirmation, amendment or withdrawal and its second-reading evidence. |
| `INHERITED_VERDICTS.tsv` | Decisions on pre-existing French corrections and selected inherited uncertainties or joins. |
| `INHERITED_RECORD_CROSSWALK.tsv` | All 134 inherited IDs connected to their current disposition or page record. |
| `FINAL_PAGE_MAP.tsv` | Final source-line ranges for each printed page in both French bodies; English ranges are in the page records. |
| `RECURRENCE_CHECK.md`, `recurrence/` | Full-work recurrence conclusions and reproducible inventories of mathematical alphabets, terminology, locators and page joins. |
| `PDF_CHECK.md`, `build/` | Commands, pass results, warnings, font information, hashes, sanitized logs and the final visual inspection. |
| `NOTES.md` | 106 individually identified notes: source slips, proof obligations and checks, later results, programme connections and explicitly labelled proposals. |
| `NOTE_CONTEXT_SEARCH.tsv` | Context queries for every note, matching files and excerpts; searches are leads, not proof certificates. |
| `NOTE_CLAIM_COVERAGE.tsv`, `scripts/NOTE_COVERAGE.md` | Supplementary source-prose coverage map, including terse assertions and examples that a proof-status keyword search alone can miss. |
| `CHECK_EVENTS.tsv` | Statement-level events distinguishing textual background, targeted proof work, use of external results and refutations. |
| `integrity/` | Source/credit/marker protection, ledger reconstruction, French-layer differences, manual dispositions and final completion audit. |
| `evidence/` | Only retained problem-specific scan crops and the footnote-formatting before/after details. Full working page renders are excluded. |
| `progress.log`, `CHECKPOINTS.tsv` | UTC work record and observed successful hourly saves. |
| `scripts/` | Audit, build, recurrence, second-reading, note-record and packaging tools, with scope and usage documentation. |
| `PACKAGE_FILES.tsv` | File sizes and SHA-256 hashes for the archive's included deliverables. |
| `PACKAGE_EXCLUSIONS.tsv`, `PACKAGE_INFO.md` | Packaging scope, exclusions and snapshot information. Every current deliverable is included; there is no dependency on an earlier checkpoint. |

## Build instructions and final status

Use a complete TeX Live installation with pdfLaTeX, XeLaTeX and the packages loaded by the supplied preambles. From each of `sources/french-diplomatic/` and `sources/french-corrected/`, run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error gaga.tex
pdflatex -interaction=nonstopmode -halt-on-error gaga.tex
pdflatex -interaction=nonstopmode -halt-on-error gaga.tex
```

From `sources/english/`, run:

```sh
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
xelatex -interaction=nonstopmode -halt-on-error GAGA_English_source_aligned.tex
```

| Final layer | Accepted sequence | Pages | Errors | Overfull boxes on any pass | Embedded fonts |
|---|---|---:|---:|---:|---:|
| French as printed | 3 pdfLaTeX passes, `build/after/` | 24 | 0 | 0 | 25 of 25 |
| Corrected French | 3 pdfLaTeX passes, `build/after/` | 24 | 0 | 0 | 25 of 25 |
| English | 4 XeLaTeX passes, `build/before/` | 26 | 0 | 0 | 28 of 28 |

The two French preambles now prevent Babel from overriding the edition's parenthesized raised footnote markers. This is the only build-stage source change. Both were rebuilt for three passes and their final PDFs inspected. The unchanged English PDF is its successful four-pass baseline build. Every accepted pass exits zero; maximum overflow is 0pt, below the required 2pt limit. No baseline pass had an overflow above 10pt.

The French logs retain two underfull-paragraph diagnostics per pass; the affected paragraphs were visually checked and are readable. English's initial cross-reference and rerun warnings settle by the final passes. The harmless warning that XeLaTeX ignores `inputenc` remains. Final inspection covered 13 pages in each French PDF and 14 in English, spread from the beginning through the bibliography, including every diagram and footnote. See `PDF_CHECK.md` for the exact pages and observations.

The minimal execution runtime required repair of its TeX cache and missing packages. `scripts/TOOLCHAIN.md` documents the versions and optional repair commands. The edition itself was not stripped of dependencies. Runtime caches and TeX auxiliary products are excluded from this archive.

## Evidence, interpretation and limits

The mechanical integrity audit reconstructed the final sources exactly from the supplied originals and retained ledger substitutions: 2,395 applied changes, one recorded no-op, and zero residual bytes. It reports 110 automatic PASS results, six REVIEW results and zero FAIL results. All six REVIEW flags have explicit primary-reader dispositions in `integrity/MANUAL_REVIEW.md`; the automatic status is preserved so that a manual judgment is not represented as a machine certificate. They concern title/front-matter typography and two deliberate French-layer differences, not unrecorded edits.

The notes distinguish a checked implication from its external inputs. They give exact locators for inspected later statements, including proper/relative GAGA and finite étale comparison in SGA 1, the special-group classification, and Charles's conjugate-variety theorem. They also identify the missing connectedness qualification in the supplied modern solvable-group remark and distinguish Zariski principal bundles from étale torsors. Explicit examples address the genus-one conjugates and the abelian-variety bundle warning; separate notes fill the preliminary flatness arguments and the Zariski-ring footnote. No proof-assistant certification or blanket validation of the supplied programme or Stacks-style release is claimed.

Historical access limits are explicit: the bodies of Kodaira's cited Theorems 7 and 8 and Serre's 1964 conjugate-variety note were not obtained. Their bibliographic identities are distinguished from verified theorem statements. The relevant proof obligations remain stated, and the homeomorphism question is addressed using Charles's inspected theorem. These limits do not affect the completed text, second-reading or PDF checks.

The archive excludes the attached inputs, the complete scan, full-page working rasters, temporary research downloads, dependency caches and previous checkpoint ZIPs. It contains the current deliverables in full. Local absolute paths and email addresses are excluded; records use `<local>` where a runtime path needed redaction. File hashes and ZIP CRCs provide transfer/integrity checks, not mathematical or visual certification.
