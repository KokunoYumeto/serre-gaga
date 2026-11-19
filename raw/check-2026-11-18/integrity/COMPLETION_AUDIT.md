# Final completion audit

Generated 2026-11-18 15:01:24 UTC.

**PASS: 41; REVIEW: 0; FAIL: 0.**

This is a mechanical completion and snapshot audit. It checks recorded coverage, exact IDs and hashes, prior reconstruction evidence, accepted pass logs, note metadata, context-search reproduction, evidence filenames and packaging privacy preflight. It does not read scans, inspect images again, redo mathematical arguments, rebuild TeX or create an archive. Sources, ledgers, notes, events, READMEs and existing integrity classifications are read only.

The final accepted build consists of the two French three-pass sequences in `build/after` and the English four-pass sequence in `build/before`. The earlier French baseline is not confused with the final French reader files.

The existing source-integrity result remains **110 PASS / 6 REVIEW / 0 FAIL** when its check below passes. Those six review classifications retain the primary reader's rationale in `integrity/MANUAL_REVIEW.md`; this completion audit does not turn them into automatic passes.

## Results

| Check | Status | Result |
|---|---|---|
| `pages.progress` | PASS | Recorded page sequence has 42 entries; timestamps are nondecreasing=True. |
| `pages.sections` | PASS | Found 42 page sections. |
| `pages.layers` | PASS | French pair=42; English=42; printed-to-scan mapping=42; matching completion timestamps=42. |
| `pages.source_map` | PASS | Final map contains 84 rows; line ranges checked against current source bytes. |
| `pages.visual_record` | PASS | Checks presence of the final gate and PDF report; it does not repeat or certify image reading. |
| `ledger.count` | PASS | Records=2396; retained=2395; no-op=1. |
| `ledger.confidence` | PASS | high=2394; medium=2 |
| `ledger.second_reading` | PASS | Review sessions=46; covered=2396; missing=0; outside ledger=0; repeated=0. |
| `crosswalk.ids` | PASS | Crosswalk=134; unique IDs=134; supplied IDs=134; nonempty dispositions and bases=True. |
| `integrity.classifications` | PASS | PASS=110; REVIEW=6; FAIL=0. The six review classifications are not changed or automatically cleared. |
| `integrity.snapshot` | PASS | Ledger and manual-review hashes checked against FINAL_TOTALS.tsv; manual assessment remains the primary reader's responsibility. |
| `integrity.sources` | PASS | Inventory rows=14; source files=14; source reconstruction PASS rows=14. |
| `integrity.credits` | PASS | README byte equality=True; protected README/name checks=4. Other protected front matter remains covered by the unchanged integrity classifications and manual rationale. |
| `integrity.replay` | PASS | Replay states={'applied': 2395, 'recorded no-op': 1}; unreconstructed diff empty=True. |
| `build.passes.french-diplomatic` | PASS | Pass rows=3; flagged passes=none. Every accepted pass log was inspected mechanically; underfull boxes and benign warnings are not silently reclassified as errors. |
| `build.overfull_table.french-diplomatic` | PASS | Overfull rows=0. |
| `build.source_hashes.french-diplomatic` | PASS | Current source files=2; manifest entries=2; after-build entries=2. |
| `build.reader_pdf.french-diplomatic` | PASS | Reader=pdf/GAGA_french_diplomatic.pdf; pages=24; bytes=421792; SHA-256=51a2d7f611ad4d77c0f2ef05c20c17401d285eb874fcc38b864e21d2fe59b272; recorded embedded fonts=25. |
| `build.passes.french-corrected` | PASS | Pass rows=3; flagged passes=none. Every accepted pass log was inspected mechanically; underfull boxes and benign warnings are not silently reclassified as errors. |
| `build.overfull_table.french-corrected` | PASS | Overfull rows=0. |
| `build.source_hashes.french-corrected` | PASS | Current source files=2; manifest entries=2; after-build entries=2. |
| `build.reader_pdf.french-corrected` | PASS | Reader=pdf/GAGA_french_corrected.pdf; pages=24; bytes=421802; SHA-256=96c47e601e442b02b5d5fa5bcca50d9a792b18663376d4da49b6b952f1b5d7a8; recorded embedded fonts=25. |
| `build.passes.english` | PASS | Pass rows=4; flagged passes=none. Every accepted pass log was inspected mechanically; underfull boxes and benign warnings are not silently reclassified as errors. |
| `build.overfull_table.english` | PASS | Overfull rows=0. |
| `build.source_hashes.english` | PASS | Current source files=8; manifest entries=8; after-build entries=8. |
| `build.reader_pdf.english` | PASS | Reader=pdf/GAGA_English.pdf; pages=26; bytes=213400; SHA-256=bf44add18c864f5c757a28c4e0658b68a0c8dc71433a5a7fd857b229162f4b85; recorded embedded fonts=28. |
| `build.reader_set` | PASS | PDF files under deliverable=3. |
| `notes.ids` | PASS | Notes=106; base IDs=95; suffixed IDs=11; duplicate or malformed IDs=False. The expected event/query set is derived from the current headings. |
| `notes.event_schema` | PASS | Total events=328; invalid type count=0; complete event fields=True. |
| `notes.metadata` | PASS | Malformed note IDs=none. |
| `notes.events` | PASS | Mismatched note IDs=none. |
| `notes.sections` | PASS | Placement mismatches=none. This limited label check is not a semantic review of every section heading. |
| `notes.query_coverage` | PASS | Query-covered notes=106; file-level rows=794. |
| `notes.query_replay` | PASS | Replayed queries=106; mismatches=none. Literal matches do not independently prove the note's claim or relation. |
| `notes.mapping_events` | PASS | Mapping decisions=79; background records=79; separately typed follow-up checks=1. |
| `notes.readme` | PASS | README UTF-8 characters=10694; original source READMEs are audited separately. |
| `notes.claim_coverage` | PASS | Rows=65; lexical marker lines=59; trigger occurrences=70; additional prose lines=6; addressed=63; introductory nonproof=2; valid note/source links=True; source hash matches=True. Editorial mappings are checked for traceability, not independently certified as complete proof coverage. |
| `evidence.paths` | PASS | Referenced image filenames=130; evidence files=130; missing=none. Bare filenames in evidence fields are resolved beneath evidence/. Images are not opened or judged. |
| `package.preflight` | PASS | Exit=0; UTC now: 2026-11-18T15:01:25Z Final package: no checkpoint interval applies. Included deliverables: 290 Excluded generated, raw or temporary files: 4 Owned deliverables omitted because unchanged: 0 (complete snapshot). Preflight only: no archive created. |
| `snapshot.stability` | PASS | Included deliverables checked=288; changed deliverables=none; changed direct inputs=none. The two completion-audit output files are excluded from their own snapshot. |
| `package.audit_output_privacy` | PASS | Findings=0. |

The companion TSV gives each requirement and its relative evidence locators. A clean result applies only to the audited snapshot. Rerun after any later source, ledger, note, event, README or other deliverable change.

## Core snapshot hashes

| Relative file | SHA-256 |
|---|---|
| `CHECK_EVENTS.tsv` | `9ba3d3eaa76f2b52dd8621a0364a75616f2d0bb067bb64b669d4f6a61ae7f1b6` |
| `CHECK_RECORD.md` | `3119b9a53eef0ae8f0d7b93a2818e41112cabd066711ae8e2ad0d205eb6e187d` |
| `CORRECTIONS.tsv` | `419dcc496216b22ad62fca5b84dcc5e7f99905a5e4eec9284129d0aa6ffdfb5d` |
| `INHERITED_RECORD_CROSSWALK.tsv` | `263db2d0280fe3a9b6439f1904880c9fd75d088ecb2178342f31daed5ffd2d85` |
| `NOTES.md` | `eccea23e311595fcb2e43438a1854eb6599e20906e511a1daf8651757601b297` |
| `NOTE_CLAIM_COVERAGE.tsv` | `3eceda60404600cd1f4e11d4fa4e0135896006dd4bec705b14a241a6d7fe55a0` |
| `NOTE_CONTEXT_SEARCH.tsv` | `8c5c949cd565244ef4781b53f5bcfa8a054846eca5a95320128b53926d3fa76a` |
| `README.md` | `7aa0d5d70345dcf65e41573c7fe6f699a017ca728cd450c121b6ed452b26404c` |
| `SECOND_READING.tsv` | `1ea2534f50454307aa0b4ae76d89bea888a818caabb1f7000f25139ece060e18` |
| `integrity/MANUAL_REVIEW.md` | `d7f429d6662818226f85ea058f72830f01825585383caa9226baf9367196d343` |
| `pdf/GAGA_English.pdf` | `bf44add18c864f5c757a28c4e0658b68a0c8dc71433a5a7fd857b229162f4b85` |
| `pdf/GAGA_french_corrected.pdf` | `96c47e601e442b02b5d5fa5bcca50d9a792b18663376d4da49b6b952f1b5d7a8` |
| `pdf/GAGA_french_diplomatic.pdf` | `51a2d7f611ad4d77c0f2ef05c20c17401d285eb874fcc38b864e21d2fe59b272` |
| `scripts/NOTE_COVERAGE.md` | `fd28054b540728269b06d7881d30a332b2f2bb6630136f469392a90bbfab72c5` |
| `scripts/final_completion_audit.py` | `0c9cfca6081a4945ca44ea112863a56adad1f9f0715d65ea92ee4748594d5674` |

Aggregate SHA-256 of the included-file names, sizes and SHA-256 values, excluding only this audit's two self-referential outputs: `9d39bc9a1eb5eabf6e0758e3d8d06161ed25a32b937bc0fdb241ed0aa002d147`.

## Packaging boundary

The package preflight creates no ZIP. The final packager must still enforce its strict compressed-size limit, complete member inventory, SHA-256 manifest and CRC verification when the final archive is actually created. Binary PDF and image content is outside the returned-text privacy scanner; existing PDF metadata/font reports and the primary reader's visual record remain the evidence for those artifacts.
