# Note coverage inventory

`../NOTE_CLAIM_COVERAGE.tsv` links source-text leads to the notes that address them. Paths inside the table are relative to `GAGA_CHECK/`. Printed page numbers come from the source's page markers; source-line numbers refer to the corrected French body.

## Scope and counts

- 59 noncomment source lines contain 70 lexical trigger occurrences.
- Six additional prose lines record claims found by reading the surrounding mathematical prose: 810, 880, 971, 973, 975 and 1084.
- The table has 65 rows: 63 addressed mathematical passages and two introductory rows marked `introductory_nonproof`.
- The two introductory rows point to related notes; they are not counted as omitted mathematical proofs.
- The nine additions N041A, N059A, N065A, N067B, N073A–N073C, N076A and N077A address all nine assertions identified in the preceding coverage review. No concrete coverage gap remained in this inventory when it was written.

## Method and limits

The lexical search is case-insensitive and skips comment-only lines. Repeated trigger words on one line increase `lexical_occurrences`; they are not separate theorem counts. The exact search expression is:

```regex
évid\w*|facil\w*|aisé\w*|on sait|bien connu|classique|il est clair|on v[ée]rif\w*|vérifie\w* (?:facilement|immédiatement)|laissons au lecteur|rappelons|immédiat\w*|on voit|admettr\w*|connu\w*|trivial\w*|cela se voit|on peut montrer|raisonnement analogue
```

The note mapping is a bounded editorial coverage judgment, not a conclusion produced by the regular expression. `addressed` means that the referenced note gives an argument, names its external inputs, or expressly preserves an unresolved obligation. It does not mean that every external theorem was independently proved. For example, the orthogonal-group row retains N095's named external inputs and separate unresolved question.

This pass read the already collated corrected French source and the notes. It did not inspect page images, make new source readings, compare another GAGA edition, or alter the source, NOTES, or event records. It is a compact traceability aid, not an image-proof or formal-proof certificate. The lexical inventory is not claimed to enumerate every mathematical assertion in the article.

Source snapshot: `sources/french-corrected/gaga_body.tex`, SHA-256 `8d5cea47090a2c775e7c15e5a744edc751b7b645a8060ad0a6790951be42ea72`. Regenerate line locators if that source changes. Notes retain their own statement of scope, confidence, dependencies and check-event status.
