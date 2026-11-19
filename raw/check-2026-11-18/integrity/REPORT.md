# Mechanical source-integrity audit

PASS: 110; REVIEW: 6; FAIL: 0.

This audit does not read a scan, decide a reading, assess a translation, or prove a mathematical claim. Exact ledger reconstruction establishes a textual transformation from the supplied source to the final source using recorded replacement text only. Context-based occurrence choices are recorded; exact equality, not a heuristic score, is the certificate. A failed reconstruction is a coverage gap or an ambiguity to investigate, not by itself proof of an unrecorded edit.

Complete README equality protects all supplied README credits and rights wording, including Thomas Waring. Provenance comments and credit-bearing front-matter lines are checked separately. Other front-matter changes are reported for assessment against the scan-supported ledger. Labels, anchor targets, existing macro signatures and exact printed-page marker lines are checked mechanically.

French-layer residuals are all listed in the diff and coverage table. Exact changed-core matches identify candidate ledger coverage. Inherited verdicts are associated at page level only because their readings may be human notation rather than literal TeX. The audit cannot certify the mathematical justification of a correction or a one-to-one inherited-verdict match. An unmatched core may result from surrounding notation changes or multiple changes in one row and requires the primary reader's review.

## Items requiring assessment

- **REVIEW** front-matter block — `french-corrected/gaga_body.tex`: Exact block differs; title/layout edits require assessment against their ledger rows, independently of protected credits.
- **REVIEW** protected front-matter credit — `french-corrected/gaga_body.tex credit line 1`: Original credit/provenance line SHA-256=94d090c0eb5bfd4e7418e2ffd4138c67a85540abe71391f43aca3b05a8982127; exact article-author markup changed from the supplied small-caps line to the recognized centered/bold/uppercase line. The literal name tokens Jean-Pierre and Serre are retained. Primary-reader confirmation of printed-page-1 typography and unchanged attribution is required; no automatic clearance is given. Full original/current blocks remain in frontmatter_changes.diff.
- **REVIEW** front-matter block — `french-diplomatic/gaga_body.tex`: Exact block differs; title/layout edits require assessment against their ledger rows, independently of protected credits.
- **REVIEW** protected front-matter credit — `french-diplomatic/gaga_body.tex credit line 1`: Original credit/provenance line SHA-256=94d090c0eb5bfd4e7418e2ffd4138c67a85540abe71391f43aca3b05a8982127; exact article-author markup changed from the supplied small-caps line to the recognized centered/bold/uppercase line. The literal name tokens Jean-Pierre and Serre are retained. Primary-reader confirmation of printed-page-1 typography and unchanged attribution is required; no automatic clearance is given. Full original/current blocks remain in frontmatter_changes.diff.
- **REVIEW** French residual coverage — `printed page 11 diff 1`: no exact changed-core candidate; manual coverage review required
- **REVIEW** French residual coverage — `printed page 36 diff 1`: no exact changed-core candidate; manual coverage review required
