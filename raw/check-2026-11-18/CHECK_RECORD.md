# GAGA second-pass check

## Notation table

The table is initialized before page 1 and refined against the images. The printed typeface, not a modern notation convention, controls the diplomatic layer. `evidence/p03-notation.png` retains the alphabet distinctions used in this table and the recurring-font review.

| Printed sign or usage | LaTeX in the layers | Reading policy |
|---|---|---|
| Upright capital point-set letters | `\mathrm{X}`, `\mathrm{Y}`, `\mathrm{U}` | Follow each printed occurrence; do not silently turn upright letters into italic. |
| Italic variables | `x`, `f`, `n`, `p`, `q` | Preserve case, primes, indices and exponents; ordinary capital point-set, ring and module letters are upright where the print shows them. |
| Bold complex field | `\mathbf{C}` | Preserve bold, including in powers. |
| Script sheaves and ideals | `\mathcal{C}`, `\mathcal{H}`, `\mathcal{O}`, `\mathcal{F}`, `\mathcal{J}`, `\mathcal{A}` | Analytic vanishing ideal is script A (pp. 3, 5); distinguish it from algebraic J and from Gothic ideals. Compare each glyph in enlarged details. |
| Gothic ideals | `\mathfrak{m}`, `\mathfrak{p}`, `\mathfrak{a}` | Keep distinct from script ideals. |
| Cohomology / axioms | `\mathrm{H}`, `(\mathrm{H}_{\mathrm{I}})`, `(\mathrm{H}_{\mathrm{II}})` | Verify each context rather than normalizing. |
| Restriction homomorphism / maps | `\varepsilon`, `\varphi`, `\to`, `\longrightarrow` | Arrow length may reflow; direction, labels and endpoints must agree. |
| Direct sum, tensor, intersection | `\oplus`, `\otimes`, `\cap`, `\bigcap` | Check base rings, limits and any primes separately. |
| Emphasis / small capitals | `\emph`, `\textit`, `\textsc` | Printed emphasis and name typography are source facts. |
| Number and section abbreviations | `n\textsuperscript{o}`, `n\textsuperscript{os}`, `\S`, `cf.`, `resp.` | Preserve French spelling and printed abbreviation; English translates ordinary prose. |
| Printed page boundaries | `% printed page N` comment lines | Keep marker identities and lexical joins; do not create a paragraph at a page break. |

## Scope and evidential standard

The attached Numdam scan alone decides the French readings. Edition records are prior AI decisions, not authorities. No other GAGA edition or translation is consulted. Each page is read in printed order in one stream by GPT-6 Astra (ChatGPT Pro mode); no page collation is delegated. Working image strips overlap and preserve the 400-dpi render. Further crops are made where a reading needs closer inspection. Source line ranges below refer to the version at the time that page was completed; a final page map supplies final ranges.

Textual collation is not a proof check. CHECK_EVENTS.tsv distinguishes background statements from targeted mathematical reasoning; the effort setting is not exposed and is not invented. The printed running heads, page numbers, line endings and exact page geometry are not recreated as body text; the article text, typeface distinctions, punctuation, mathematical displays and page markers are collated.

## Totals

The ledger contains **2,396 data records**, of which **2,395 describe retained changes** and **1 is explicitly withdrawn**. A data record is one recorded source edit, often one formula-font restoration; it is not one mathematical error. The withdrawn English record remains to preserve the decision history. Inherited corrections already present in the supplied corrected layer are separately adjudicated in `INHERITED_VERDICTS.tsv`; they are not counted again as new edits.

| Layer | Reading | Misprint of the original | Translation | Typesetting | Structure | Ledger total | Retained changes |
|---|---:|---:|---:|---:|---:|---:|---:|
| as-printed | 15 | 0 | 0 | 715 | 3 | 733 | 733 |
| corrected | 13 | 3 | 0 | 715 | 3 | 734 | 734 |
| English | 3 | 0 | 52 | 870 | 2 | 927 | 926 |
| build | 0 | 0 | 0 | 2 | 0 | 2 | 2 |

### Pages with no newly found difference

These counts refer to retained page-text/typography/structure edits found against the supplied source layer. Build-only layout changes are excluded. An inherited correction that was confirmed is not a new difference found in this run. A repair spanning two printed pages affects both pages.

| Layer | Pages with no new difference | Printed pages |
|---|---:|---|
| as-printed | 5 | 10, 15, 28, 33, 42 |
| corrected | 5 | 10, 15, 28, 33, 42 |
| English | 5 | 1, 7, 10, 16, 42 |

### Changes to mathematical symbols, assertions or references

The following list separates substantive symbol/reference decisions from the much larger set of font and layout restorations. Each line identifies its place and the corresponding ledger data records or inherited verdict. No change in alphabet styling is claimed to be a new mathematical theorem.

- Printed p. 5, Proposition 1 and preceding definition: restore the analytic vanishing ideal `A(Y)` at all six places in each layer (data records 19–36); the scan does not print `J(Y)`.
- Printed p. 6, Proposition 1 proof: restore the same analytic ideal `A(X)` at both places in each layer (39–44).
- Printed p. 11, Proposition 5 proof: restore the printed capital `X` only in diplomatic French; corrected French and English retain the mathematically required point `x` (55; SRC-006/SRC-023).
- Printed p. 18, Proposition 11: restore tensoring over `A` in corrected French and English (716–717); both factors are `A/a`-modules, so the printed expression is canonically valid.
- Printed p. 23, no. 15: restore algebraic ideal `J=J(Y)` and its fiber `J_x` in all layers (840–843, 846–847).
- Printed p. 24, no. 15: restore `J.G=0` in all layers (866–867, 871).
- Printed p. 24, no. 15: correct the printed reference `[8]` to FAC `[18]`, no. 65, Proposition 7, only in corrected French and English (870, 872).
- Printed p. 26, equation (8): restore the printed `M(n)` in corrected French and English (951–952); the repeated equality is true and sufficient, so an editorial `M(n−1)` is not required.
- Printed p. 36, Proposition 21 diagram: reproduce the visibly missing closing parenthesis only in diplomatic French; corrected French and English retain it (1770; UNC-067).
- Inherited correction retained: p. 5 chart axiom `H_II` → `H_I` (SRC-022).
- Inherited correction retained: p. 6 conclusion `H_U` → `H_X` (SRC-003).
- Inherited correction retained: p. 14 missing component index `K′` → `K′_i` (SRC-008).
- Inherited correction retained: p. 17 inverse-image sequence `F_3` → `F′_3` (SRC-009).
- Inherited correction retained: p. 23 algebraic global sections `H^0(X^h,A)` → `H^0(X,A)` (SRC-012).
- Inherited correction retained: p. 28 source of the semilinear cohomology map uses `Ω^p(X)`, not `Ω^p(X^σ)` (SRC-014).

All other retained French-layer differences are grammatical or punctuation repairs recorded with reasons. There are 16 local differences between the final French bodies on 15 printed pages; the original spelling conventions and unsupported proposed corrections are retained or restored as documented.

### Review coverage

All 2,396 ledger records have a second-reading disposition: 2,394 high-confidence records and 2 medium-confidence records. `SECOND_READING.tsv` maps data records to the actual review sessions. `RECURRENCE_CHECK.md` records the full-work follow-up searches. The inherited-record crosswalk covers all 134 source-correction, transcription-repair, page-join, English-check and uncertain-reading identifiers. The final page map is in `FINAL_PAGE_MAP.tsv`.

## Printed page 1

- Scan: PDF page 2, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 2-17; `sources/french-corrected/gaga_body.tex`, lines 2-17. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/00_title_and_introduction.tex`, lines 1-19 (line 19 through the page-ending “we”), paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 1, as-printed/typesetting: 3, corrected/reading: 1, corrected/typesetting: 3. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: All three prose paragraphs checked, including the absent full stop after “etc.)”, upright X, italic “algébrique”, “analytique” and “faisceaux cohérents”, small-capital Chow and the “nous | montrons” page join. Three heading typography repairs in each French layer. No English change on this page.
- Completed: 2026-11-18 12:32:48 UTC.
- Second-reading/recurrence result: Second reading: a detached baseline mark after the title is transcribed as a period in both French layers, with medium confidence. The physical origin remains uncertain.

## Printed page 2

- Scan: PDF page 3, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 18-27; `sources/french-corrected/gaga_body.tex`, lines 18-27. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/00_title_and_introduction.tex`, lines 19-25, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 1, corrected/typesetting: 1, English/translation: 2. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference. GAGA-SRC-001: retain printed W-L. Chow; punctuation is not a mathematical defect.
- Observations: Checked introductory equivalence, section descriptions, ring subscripts and completion claim, the semisimple-group limitation, and footnote 1. French words and punctuation match. French parenthesized footnote markers restored through the preamble; English “fibre spaces” changed to glossary “bundles” at the two occurrences.
- Completed: 2026-11-18 12:34:11 UTC.

## Printed page 3

- Scan: PDF page 4, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 28-51; `sources/french-corrected/gaga_body.tex`, lines 28-51. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/00_title_and_introduction.tex`, line 27; `sources/english/components/01_analytic_spaces.tex`, lines 1-17, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 2, as-printed/structure: 1, corrected/typesetting: 2, corrected/structure: 1, English/structure: 1. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Checked the analytic-subset quantifiers, n≥0, exponents r/s/n, the restriction display, both kernel expressions, the entire sheaf-definition emphasis, and the map-composition condition. Kernel A is script, not Gothic. Two heading typography repairs per French layer; English matches the corrected French.
- Completed: 2026-11-18 12:35:08 UTC.
- Second-reading/recurrence result: Recurrence review: removed the added paragraph break at pp. 3–4 in both French layers and English; both page-edge crops were reread.

## Printed page 4

- Scan: PDF page 5, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 52-76; `sources/french-corrected/gaga_body.tex`, lines 52-76. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/01_analytic_spaces.tex`, lines 19-39, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 1, as-printed/structure: 1, corrected/typesetting: 1, corrected/structure: 1, English/translation: 2, English/structure: 1. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: GAGA-SRC-002 confirmed: the print lacks est, while grammar and the parallel p. 3 definition require it; retained solely in corrected French and English.
- Observations: Checked composition/inverse and product maps, every prime and exponent, the two axioms and the terminal morphism paragraph. No French wording change. Bold heading restored. English covering and separated follow the supplied glossary; separated here has its ordinary topological meaning Hausdorff.
- Completed: 2026-11-18 12:35:59 UTC.
- Second-reading/recurrence result: Recurrence review: the opening coordinate criterion continues the p. 3 definition without a new paragraph in the print.

## Printed page 5

- Scan: PDF page 6, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 77-94; `sources/french-corrected/gaga_body.tex`, lines 77-94. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/01_analytic_spaces.tex`, lines 41-53, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 6, as-printed/typesetting: 1, corrected/reading: 6, corrected/typesetting: 1, English/translation: 6. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: GAGA-SRC-022 confirmed: printed H_II retained diplomatically; corrected H_I is the chart-cover axiom, not the separatedness axiom.
- Observations: Charts, induced analytic structure, product uniqueness, the deferred FAC analogues, analytic sheaves and both parts of Proposition 1 checked. Six analytic-ideal A/J transcription repairs in each French layer and their six English formula repairs. The analytic ideal is A, consistently with p. 3; algebraic J will be checked where introduced. Bold heading restored. Procedural exception: an assertion in the page-5 edit helper stopped before any change, but the shell continued to render/show page 6 before this completion entry. Page 5 was then completed; page 6 is re-read next before any page-6 edit.
- Completed: 2026-11-18 12:38:06 UTC.

## Printed page 6

- Scan: PDF page 7, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 95-112; `sources/french-corrected/gaga_body.tex`, lines 95-112. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/01_analytic_spaces.tex`, lines 55-69, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 2, as-printed/typesetting: 1, corrected/reading: 2, corrected/typesetting: 1, English/translation: 3. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: GAGA-SRC-003 confirmed (H_U to H_X in corrected French); quotient coherence gives the required conclusion. GAGA-SRC-004 retained as printed.
- Observations: Checked the quotient/coherence proof, two analytic-ideal symbols, examples, local algebra, residue field, convergent power-series rings, the regularity criterion, and the reduced-ring intersection. Two A/J repairs per French layer and in English; English bundle terminology and the French bold heading corrected. The displayed intersection retains its comma and joins the first words of p. 7 without a new paragraph.
- Completed: 2026-11-18 12:39:10 UTC.

## Printed page 7

- Scan: PDF page 8, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 113-134; `sources/french-corrected/gaga_body.tex`, lines 113-134. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/01_analytic_spaces.tex`, line 71; `sources/english/components/02_associated_analytic_space.tex`, lines 1-15, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 2, corrected/typesetting: 2. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Checked minimal-prime subscripts, A_x(X_i), the convergent/formal series distinction, dimension r, the Krull comparison, Z-topology convention and all four assertions of Lemma 1. Two heading typography repairs per French layer. English is complete and mathematically aligned; no translation change.
- Completed: 2026-11-18 12:39:56 UTC.

## Printed page 8

- Scan: PDF page 9, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 135-154; `sources/french-corrected/gaga_body.tex`, lines 135-154. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 17-33, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/structure: 1, corrected/structure: 1, English/translation: 1, English/structure: 1. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: GAGA-SRC-005 confirmed: remove only the extraneous second colon in corrected French; the map and its endpoints are unchanged.
- Observations: Checked the proof of Lemma 1, chart display and comma, full statement of Proposition 2, gluing argument, all primed domains/codomains, axioms H_I/H_II/VA′_II, graph subscripts ij, and the opening remark. French matches the image, including the doubled colon in the diplomatic layer. One English glossary alignment: Hausdorff to separated.
- Completed: 2026-11-18 12:40:46 UTC.
- Second-reading/recurrence result: Recurrence review: the final Remark continues into p. 9 without a paragraph break; all three layers were repaired and reread.

## Printed page 9

- Scan: PDF page 10, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 155-176; `sources/french-corrected/gaga_body.tex`, lines 155-176. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 35–53 through the ideal of O_x, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 1, as-printed/structure: 1, corrected/typesetting: 1, corrected/structure: 1, English/structure: 1. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: All words, punctuation, italic emphasis, X^h superscripts, x,X subscripts, hats on theta/O/H, and the J algebraic-ideal glyph match. Restored the bold no. 6 heading. English preserves the two topology descriptions, countability at infinity, functoriality statements and Proposition 3 without a meaning difference.
- Completed: 2026-11-18 12:43:50 UTC.
- Second-reading/recurrence result: Recurrence review: “On définit” continues the p. 8 Remark flush left; the following “Dans la suite” starts a separate indented paragraph.

## Printed page 10

- Scan: PDF page 11, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 177-194; `sources/french-corrected/gaga_body.tex`, lines 177-194. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 53–75 through the image clause, paragraph by paragraph against the corrected French for this printed page.
- Changes: 0 in all layers. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: No differences found in the complete French page or its English meaning. Read both displayed equations, the Gothic a / script A / script J distinctions, r >= 0 and f^r, all completed-ring hats, citations, and the final quotient argument; enlarged completion and quotient details inspected. English juxtaposition for ideal products has the same formula meaning as the printed baseline multiplication points.
- Completed: 2026-11-18 12:44:22 UTC.

## Printed page 11

- Scan: PDF page 12, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 195-223; `sources/french-corrected/gaga_body.tex`, lines 195-223. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 75–99 from the canonical-image clause, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 1, as-printed/typesetting: 27, corrected/typesetting: 27, English/typesetting: 24. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-006 confirmed against the image; SRC-023 and the later lowercase transcription repair reversed. Corrected lowercase x is justified by the stalk argument.
- Observations: Read the three corollaries and Proposition 5 with proof and remark. Restored upright variety capitals formula by formula and the bold no. 7 heading. The printed capital X in the Z-neighbourhood clause is a genuine original misprint, contrary to the latest inherited ledger decision; restored only in the diplomatic layer. Earlier script-J repair is confirmed visually. English otherwise matches.
- Completed: 2026-11-18 12:45:56 UTC.

## Printed page 12

- Scan: PDF page 13, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 224-240; `sources/french-corrected/gaga_body.tex`, lines 224-240. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 101–115 through the subset U contained in f(X), paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 65, corrected/typesetting: 65, English/typesetting: 63. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Complete propositions 6 and 7 opening, Lemma 2 and its reduction to components compared. All variety capitals and I,J index sets are upright in print, restored formula by formula; lower-case indices unchanged. Restored the beneath-operator union limit in French. Words, hypotheses, arrows, subset signs and English meaning otherwise match. No bulk change made to the next-page part of the English paragraph.
- Completed: 2026-11-18 12:47:15 UTC.
- Second-reading/recurrence result: Second reading: restored the first union as a large union sign as well as the second; the second union retains its printed below-sign limit.

## Printed page 13

- Scan: PDF page 14, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 241-264; `sources/french-corrected/gaga_body.tex`, lines 241-264. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 115–135 from the Z-open/dense clause, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 39, corrected/typesetting: 39, English/typesetting: 38. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: All text, proposition hypotheses, inverse-map expression, star and negative exponent, stalk indices, displayed map, and footnote 2 with Samuel credit compared. Restored upright variety letters, including subscripts, and the bold heading. Print uses italic pr and an ordinary arrow x to (x,f(x)); these remain in French. English operator styling and mapsto express the same formula meaning and were left alone.
- Completed: 2026-11-18 12:48:03 UTC.

## Printed page 14

- Scan: PDF page 15, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 265-275; `sources/french-corrected/gaga_body.tex`, lines 265-275. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 137–145 through the first K_i in the final paragraph, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 60, corrected/typesetting: 60, English/translation: 2, English/typesetting: 60. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-007 retained as historical spelling; SRC-008 missing index correction confirmed. Earlier Gothic-to-script J transcription repair confirmed by the image.
- Observations: Read each prime/subscript in the component, fraction-ring and field-degree arguments and footnote 3. Restored upright capitals formula by formula. The original missing i on K prime is visible and the inherited correction is justified; historical considèrerons retained. Script J in the ideal definition is confirmed. English meaning agrees; fraction field terminology now follows the unified glossary.
- Completed: 2026-11-18 12:49:25 UTC.

## Printed page 15

- Scan: PDF page 16, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 276-297; `sources/french-corrected/gaga_body.tex`, lines 276-297. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/02_associated_analytic_space.tex`, lines 145–167 from the second parenthetical component field, paragraph by paragraph against the corrected French for this printed page.
- Changes: English/translation: 1, English/typesetting: 38. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: No French difference found: conclusion of Proposition 9 and complete Lemma 3 match, including primes, Gothic p/m/b, phi, product and sum operators, congruences and mod. punctuation. English mathematical alphabets restored to the corrected French; fraction field made consistent with glossary. Every sentence and formula meaning otherwise agrees.
- Completed: 2026-11-18 12:50:19 UTC.

## Printed page 16

- Scan: PDF page 17, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 298-331; `sources/french-corrected/gaga_body.tex`, lines 298-331. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/03_sheaf_correspondence_nos09_12.tex`, lines 1–31, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 2, corrected/typesetting: 2. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Read complete construction of F prime, Definition 2, tensor display over O prime, alpha and the two phi displays. Primes and h superscripts are distinct and correctly transcribed. Restored both bold headings and centered section heading. English is complete and its inverse-image term matches the glossary; no English change.
- Completed: 2026-11-18 12:50:48 UTC.

## Printed page 17

- Scan: PDF page 18, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 332-368; `sources/french-corrected/gaga_body.tex`, lines 332-368. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/03_sheaf_correspondence_nos09_12.tex`, lines 33–69, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 17, corrected/typesetting: 17, English/typesetting: 16. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-009 missing prime confirmed; all other differences from the diplomatic page are shared transcription/typography repairs.
- Observations: Read Proposition 10(a–c), all exact sequences, prime/h distinction, q/p exponents, the ideal-sheaf consequence, and extension by zero paragraph. Restored upright variety letters and bold no. 10 heading. Original missing prime on the third inverse-image term is visible and inherited correction confirmed. English mathematics and sentences otherwise agree.
- Completed: 2026-11-18 12:51:43 UTC.

## Printed page 18

- Scan: PDF page 19, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 369-414; `sources/french-corrected/gaga_body.tex`, lines 369-414. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/03_sheaf_correspondence_nos09_12.tex`, lines 71-122, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 28, corrected/misprint of the original: 1, corrected/typesetting: 28, English/translation: 1, English/typesetting: 27. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-024 reverted in corrected French and English: the printed tensor over A is valid; see INHERITED_VERDICTS.tsv.
- Observations: Read all of Proposition 11 and the section/cochain comparison construction; checked each tensor base, prime, stalk index, superscript h/X, intersection index, and Gothic covering symbol. Restored the upright mathematical alphabets and bold heading. The prose, reference [18], no.18, and all display boundaries otherwise agree.
- Completed: 2026-11-18 12:55:21 UTC.

## Printed page 19

- Scan: PDF page 20, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 415-467; `sources/french-corrected/gaga_body.tex`, lines 415-467. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/03_sheaf_correspondence_nos09_12.tex`, lines 124-175, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 3, corrected/typesetting: 3, English/typesetting: 2. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Collated the two induced cohomology maps, every node/arrow/label in the connecting-morphism square, the projectivity hypothesis, and Theorems 1 and 2. French arrow labels were on the wrong side despite an accurate source comment; moved both epsilon labels left. English formulas now retain upright X. The initial addition of “new” was subsequently withdrawn; see the second-reading result below.
- Completed: 2026-11-18 12:56:05 UTC.
- Second-reading/recurrence result: Second reading: the proposed English addition “new” was withdrawn as unnecessary. Data record 809 is retained with identical old/new text; the original English wording remains.

## Printed page 20

- Scan: PDF page 21, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 468-500; `sources/french-corrected/gaga_body.tex`, lines 468-500. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/03_sheaf_correspondence_nos09_12.tex`, lines 177-191; `04_proofs_theorems1_3_nos13_17.tex`, lines 1-26 through the first Dolbeault cohomology expression, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 1, corrected/typesetting: 1, English/typesetting: 8. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-010 retained unchanged as printed.
- Observations: French wording, punctuation, indices, primes, bold projective-space/field symbols, and display boundaries agree. The no.13 heading required bold type. Read Theorem 3, both remarks, reduction to projective space, and the page-20 part of Lemma 4. Kept the printed hyphenated page join coho-/mologie and the absence of a full stop after Remarques. English corrections only restore mathematical alphabets.
- Completed: 2026-11-18 12:56:48 UTC.

## Printed page 21

- Scan: PDF page 22, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 501-558; `sources/french-corrected/gaga_body.tex`, lines 501-558. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, line 26 from “cohomology of type” including footnote (4), and lines 28-81, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 1, as-printed/typesetting: 1, corrected/reading: 1, corrected/typesetting: 1, English/typesetting: 12. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Read the entire first comparison ladder node by node: eight nonellipsis groups, all q/q+1 and n/n-1 indices, h superscripts, four downward epsilon labels on the left. The French formulas agree with print. Restored the spacing and final full stop at footnote (4). The footnote prints H^q(X,O), not H^q(X^h,O^h); retained this literal wording in all layers and reserved the likely analytic interpretation for an explicitly qualified note, since the intended reading is contextual. English changes restore X/E alphabets only.
- Completed: 2026-11-18 12:58:13 UTC.

## Printed page 22

- Scan: PDF page 23, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 559-620; `sources/french-corrected/gaga_body.tex`, lines 559-620. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, lines 83-152, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 1, corrected/typesetting: 1, English/typesetting: 2. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-011 confirmed: close the participial parenthesis with a comma in corrected French only.
- Observations: Collated the five-column comparison ladder, all epsilon indices 1-5, the two-stage diagram chase, internal-Hom construction and all stalk/base-ring distinctions in Lemma 6. No added or omitted English mathematical assertion found. The French heading lacked bold type; English X was italic in the diagram and one inline formula.
- Completed: 2026-11-18 12:58:52 UTC.

## Printed page 23

- Scan: PDF page 24, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 621-645; `sources/french-corrected/gaga_body.tex`, lines 621-645. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, lines 154-184, and line 186 through the formula for the analytified endomorphism, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 2, as-printed/typesetting: 1, corrected/reading: 2, corrected/typesetting: 1, English/reading: 2, English/typesetting: 18. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-012 confirmed: the first inline H^0 has an erroneous h on X in the original; corrected French and English already omit it.
- Observations: Read the proof of full faithfulness, uniqueness in Theorem 3, and beginning of the ambient projective-space reduction. Found the algebraic ideal sheaf misread as script I: the scan has script J in the definition and membership formula. Corrected both French layers and English; preserved X superscripts used for extension by zero. Bolded the numbered heading; restored upright English X/Y.
- Completed: 2026-11-18 12:59:47 UTC.

## Printed page 24

- Scan: PDF page 25, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 646-668; `sources/french-corrected/gaga_body.tex`, lines 646-668. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, line 186 from “coherent analytic sheaf on”, and lines 188-210, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 1, as-printed/typesetting: 1, corrected/reading: 1, corrected/misprint of the original: 1, corrected/typesetting: 1, English/reading: 1, English/translation: 1, English/typesetting: 21. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Completed the ideal-annihilator descent, twists and transition functions t_j^n/t_i^n, Lemma 7 with its proof, and Lemma 8 statement. Corrected the continuing script-I misreading to J. Found an original bibliographic slip [8] for [18] in the algebraic vanishing input; changed only corrected French and English. The diplomatic reference remains [8]. Restored numbered heading weight and English mathematical alphabets.
- Completed: 2026-11-18 13:00:43 UTC.

## Printed page 25

- Scan: PDF page 26, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 669-708; `sources/french-corrected/gaga_body.tex`, lines 669-708. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, lines 212-266, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 19, corrected/typesetting: 19, English/typesetting: 19. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: Earlier equation-(1) repair confirmed; no corrected-layer divergence on this page.
- Observations: Checked the generation-propagation exponent m-n, local indices k/i, all ideal and tensor terms, Tor_1, equation tags (1)-(4), n-1 twists and L_n kernels. The analytic ideal is script A here, in deliberate contrast with algebraic script J on pp.23-24. Restored upright H/X/U/E where sources used italic capitals. English “twisting by n” accurately expresses the functor in the French; no prose restyling.
- Completed: 2026-11-18 13:01:53 UTC.

## Printed page 26

- Scan: PDF page 27, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 709-738; `sources/french-corrected/gaga_body.tex`, lines 709-738. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, lines 268-345 through “required property”, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 19, as-printed/structure: 1, corrected/misprint of the original: 1, corrected/typesetting: 19, corrected/structure: 1, English/translation: 1, English/typesetting: 16. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-013 reverted: both outer terms in printed (8) are M(n); the repetition is true and adequate, so the stronger inherited variant is not a justified correction.
- Observations: Read sequences (5)-(9), the finite-dimensional stabilization argument, every n-1/n and cohomology index, and footnote (5). Restored upright alphabets and the space before the French footnote call. No English prose restyling.
- Completed: 2026-11-18 13:05:50 UTC.
- Second-reading/recurrence result: Recurrence review: “Ceci étant…” continues into the flush-left p. 27 “En effet…”; both French layers were joined. English was already one paragraph.

## Printed page 27

- Scan: PDF page 28, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 739-776; `sources/french-corrected/gaga_body.tex`, lines 739-776. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/04_proofs_theorems1_3_nos13_17.tex`, line 345 from “To simplify” through line 395; `sources/english/components/05_applications_nos18_20.tex`, lines 1-7 through the first x^sigma, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 3, as-printed/structure: 1, corrected/typesetting: 3, corrected/structure: 1, English/typesetting: 14. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Read the Nakayama step and all four exact-sequence displays; confirmed p/m Gothic, local-algebra capitals upright, sheaves script and projective space/complex field bold. Restored the three French headings and English formula alphabets.
- Completed: 2026-11-18 13:06:42 UTC.
- Second-reading/recurrence result: Recurrence review: removed the added page-boundary paragraph break in both French layers; no English change was needed.

## Printed page 28

- Scan: PDF page 29, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 777-807; `sources/french-corrected/gaga_body.tex`, lines 777-807. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/05_applications_nos18_20.tex`, lines 7-74 from “for the point”, paragraph by paragraph against the corrected French for this printed page.
- Changes: English/typesetting: 36. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-014 confirmed: remove sigma from X only in the source coefficient sheaf of the first H^q(U,-) term.
- Observations: All French words, punctuation, displays, Gothic covering U, upright C/H/X/U/V/K, and p,q,sigma exponents agree with the image. The English propositions, Hodge-number equalities, covering argument and corollary retain the meaning; formula alphabets were aligned.
- Completed: 2026-11-18 13:07:27 UTC.

## Printed page 29

- Scan: PDF page 30, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 808-829; `sources/french-corrected/gaga_body.tex`, lines 808-829. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/05_applications_nos18_20.tex`, lines 76-120, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 42, corrected/typesetting: 42, English/typesetting: 39. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-015 confirmed at the visible-text level; the scan does not establish whether the defect arose in typesetting or printing.
- Observations: Read the historical homeomorphism question without updating the text, the printed defect in “sous-ense.nble”, all support/sheaf subscripts and graph/projection formulas, and propositions 13-15. Restored upright alphabets and the no.19 bold heading.
- Completed: 2026-11-18 13:08:44 UTC.

## Printed page 30

- Scan: PDF page 31, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 830-854; `sources/french-corrected/gaga_body.tex`, lines 830-854. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/05_applications_nos18_20.tex`, lines 122-168 through “bundle”, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 33, corrected/typesetting: 33, English/translation: 8, English/typesetting: 32. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Read the graph proof and uniqueness corollary, the group/set distinction in nonabelian cohomology, additive-group example, comparison map, injectivity statement and its strengthened isomorphism formulation. Restored French bold heading and mathematical alphabets; applied the glossary rendering bundle in eight contextual English changes.
- Completed: 2026-11-18 13:09:55 UTC.

## Printed page 31

- Scan: PDF page 32, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 855-875; `sources/french-corrected/gaga_body.tex`, lines 855-875. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/05_applications_nos18_20.tex`, lines 168-219 from “with base”, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 25, corrected/typesetting: 25, English/translation: 9, English/typesetting: 25. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Read the associated Isom-bundle construction, its action g h g-prime inverse, the warning for abelian varieties and finite groups, propositions 17-18, and the local-freeness reduction. Restored upright alphabets and glossary terms bundle, vector bundle, fiber and fiber product. The glossary explicitly also specifies fiber for a sheaf at a point; all earlier stalk/fibre renderings are queued for the required whole-work recurrence sweep after p42.
- Completed: 2026-11-18 13:11:07 UTC.

## Printed page 32

- Scan: PDF page 33, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 876-888; `sources/french-corrected/gaga_body.tex`, lines 876-888. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/05_applications_nos18_20.tex`, lines 221-266, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 29, corrected/typesetting: 29, English/translation: 5, English/typesetting: 29. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Read the finite-module descent of local freeness, divisor remarks, Kodaira references, rational-section hypothesis, Grothendieck attribution and proposition 19 with its contracted-product subscript. The French has no new lexical or mathematical difference; restored capitals and aligned five English bundle terms.
- Completed: 2026-11-18 13:12:02 UTC.

## Printed page 33

- Scan: PDF page 34, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 889-926; `sources/french-corrected/gaga_body.tex`, lines 889-926. The corrected page was compared against the diplomatic page and the image.
- English comparison: `sources/english/components/05_applications_nos18_20.tex`, lines 268-321, paragraph by paragraph against the corrected French for this printed page.
- Changes: English/translation: 9, English/typesetting: 44. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: SRC-016 confirmed: remove the stop between the associated-bundle expression and its parenthetic alternative.
- Observations: Read every contracted product, H/G subscript, P0/P1 and E0 index, inverse image, the four-arrow square and condition (R). French agrees with the scan apart from the already justified corrected-layer stop removal. English bundle/fiber terminology and mathematical alphabets were aligned.
- Completed: 2026-11-18 13:13:09 UTC.

## Printed page 34

- Scan: PDF page 35, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 927-968; `sources/french-corrected/gaga_body.tex`, lines 927-968. The corrected page was compared against the diplomatic page and the image.
- English comparison: 05_applications_nos18_20.tex lines 323–376 and 06_appendix_nos21_24_bibliography.tex lines 1–23, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 2, corrected/typesetting: 2, English/typesetting: 17. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: The symplectic symbol has an upright S and italic p, retained in both French layers and restored in English. ANNEXE is centered in regular capitals, while the no. 21 heading is bold. The historical conjecture and the solvable-group convention are preserved for later discussion; no modern hypothesis has been silently inserted.
- Completed: 2026-11-18 13:17:15 UTC.

## Printed page 35

- Scan: PDF page 36, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 969-1003; `sources/french-corrected/gaga_body.tex`, lines 969-1003. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 25–84 (through “Consider the”), paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 56, corrected/typesetting: 56, English/typesetting: 54. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Every ring/module/functor capital on this page is upright in the scan. The cyclic-module flatness criterion and the stated noetherian finite-type hypotheses of Proposition 21 are retained exactly; no generalization is inserted.
- Completed: 2026-11-18 13:18:01 UTC.

## Printed page 36

- Scan: PDF page 37, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1004-1058; `sources/french-corrected/gaga_body.tex`, lines 1004-1058. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 85–147, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/reading: 1, as-printed/typesetting: 31, corrected/typesetting: 31, English/typesetting: 30. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: GAGA-SRC-017: confirmed rejection of the proposed punctuation change. GAGA-UNC-067: diplomatic normalization reversed, corrected reading retained.
- Observations: The alleged doubled-parenthesis error in Proposition 22(a) is not an error. In the earlier diagram, however, the top-right closing parenthesis is wholly absent in the scan; the diplomatic source now records its absence, while corrected French and English retain it. The damaged lower-right parenthesis remains legible as a parenthesis. Incidental ink marks after B in the proof and before “soit” have no defined mathematical role and are recorded as physical uncertainty, not promoted to prime notation.
- Completed: 2026-11-18 13:19:33 UTC.

## Printed page 37

- Scan: PDF page 38, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1059-1090; `sources/french-corrected/gaga_body.tex`, lines 1059-1090. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 149–203 (through “system of generators”, plus footnote 6), paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 45, corrected/typesetting: 45, English/typesetting: 44. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: The no. 23 heading was already correctly bold. Footnote 6 and its call were checked, including its Zariski-ring qualification. Ring/module capitals are upright throughout.
- Completed: 2026-11-18 13:20:21 UTC.

## Printed page 38

- Scan: PDF page 39, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1091-1127; `sources/french-corrected/gaga_body.tex`, lines 1091-1127. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex line 203 (from “of E”) through line 269, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 45, corrected/typesetting: 45, English/typesetting: 44. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: The full stop before the completion display is actually printed and is retained. The Artin–Rees exponent, the hats on both completions, and the hypotheses on all finite modules were checked. No mathematical emendation is warranted.
- Completed: 2026-11-18 13:21:06 UTC.
- Second-reading/recurrence result: Second reading: amended three display-font records to remove accidental math-font commands from the ordinary words “Artin” and “Exposé”; nested formulas remain correctly styled.

## Printed page 39

- Scan: PDF page 40, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1128-1167; `sources/french-corrected/gaga_body.tex`, lines 1128-1167. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 271–329 (through “the maximal ideal”), paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 40, corrected/typesetting: 40, English/typesetting: 35. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: The three downward-arrow labels in the French completion diagram were on the wrong side in the source code; all now match their printed left positions. Hats, double primes, the multiplication point, and the noetherian assumption were checked. No additional mathematical text change is needed.
- Completed: 2026-11-18 13:22:25 UTC.

## Printed page 40

- Scan: PDF page 41, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1168-1187; `sources/french-corrected/gaga_body.tex`, lines 1168-1187. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 329–386 (from “of A”), paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 56, corrected/typesetting: 56, English/typesetting: 52. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: The quotient ideals, completion hats, maximal-ideal primes and finite free ranks all agree with the scan. Proposition 30 has the stronger completion-isomorphism hypothesis actually stated by Serre; the edition does not replace it with a modern general descent theorem.
- Completed: 2026-11-18 13:23:06 UTC.

## Printed page 41

- Scan: PDF page 42, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1188-1236; `sources/french-corrected/gaga_body.tex`, lines 1188-1236. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 388–461, paragraph by paragraph against the corrected French for this printed page.
- Changes: as-printed/typesetting: 12, corrected/typesetting: 12, English/typesetting: 11. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: GAGA-SRC-018 and 019 confirmed; GAGA-SRC-020 and 021 confirmed as non-corrections.
- Observations: The end of Proposition 30 and bibliography entries 1–16 were read character by character. Titles remain in their original language, including the historical title “fibre spaces”. The anomalous dot in Kodaira’s title is visible, but its physical origin is uncertain. The printer’s signature 4 below the bibliography is page furniture, recorded here rather than inserted into the article body, consistently with the running-head/folio policy.
- Completed: 2026-11-18 13:24:30 UTC.

## Printed page 42

- Scan: PDF page 43, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).
- French comparison: `sources/french-diplomatic/gaga_body.tex`, lines 1237-1247; `sources/french-corrected/gaga_body.tex`, lines 1237-1247. The corrected page was compared against the diplomatic page and the image.
- English comparison: 06_appendix_nos21_24_bibliography.tex lines 463–476, paragraph by paragraph against the corrected French for this printed page.
- Changes: 0 in all layers. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.
- Inherited correction verdicts: No inherited French-layer difference on this page.
- Observations: Bibliography entries 17–20 and the terminal rule were checked, including the accents in Méthodes, algèbre and cohérents; the bold volumes 61 and 35; pp. 197–278; the proper title Fibre-spaces with its actual hyphen; and the Wallace attribution. All three layers agree. No change on this page.
- Completed: 2026-11-18 13:24:47 UTC.

## Numdam cover sheet

The additional PDF page 1 (not a printed article page) was rendered at 400 dpi and inspected in full after printed page 42. It identifies the article, journal, volume 6 (1956), pp. 1–42, and the Numdam source and rights notice. It is not an additional article page or a replacement for the unchanged edition rights and credit notices.

## Second reading

A separate row-level record is kept in SECOND_READING.tsv. Every reviewed CORRECTIONS row receives its decision and confidence. On p. 1 the enlarged title ending revealed a small detached baseline mark after the final E; it is transcribed as a terminal period in both French layers with medium confidence. Its physical origin is not certain.
