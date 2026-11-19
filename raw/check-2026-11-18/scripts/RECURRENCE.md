# Mechanical recurrence tools

These generators support the primary reader's recurrence review. They neither read scans nor assign reading, translation, font, or mathematical verdicts. They write their own reports and never alter edition sources or the corrections ledger.

Run from the directory containing `CORRECTIONS.tsv` and `sources/`:

```bash
python scripts/recurrence_math_inventory.py
python scripts/recurrence_terminology_inventory.py
```

All input and output paths are configurable. The default compact destinations are `recurrence/math` and `recurrence/terminology`. Terminology uses the supplied glossary at the relative default `../input/GAGA_context/glossary/GLOSSARY_SGA_EN_UNIFIED.tsv`; use `--glossary` when that input is stored elsewhere. The glossary is not bundled in full.

## Compact evidence

The math inventory includes source SHA-256 hashes, per-source and per-printed-page lexical counts, exact candidate and parser-uncertainty tables, a table of math-font commands in textual wrappers without detected explicit nested math, and aggregate counts for legitimate nested formulas. Empty candidate tables retain their headers, so zero findings are explicit.
Math and locator source filenames are relative to `sources/`; terminology source filenames include the `sources/` prefix and are relative to the deliverable root.

The locator tables preserve the original one-based data-record ID, file, layer, printed page, exact line locator, statement, kind and confidence. They omit duplicated old/new/evidence fields, which remain in `CORRECTIONS.tsv`. The page-28/29 table includes every ledger row on those two pages, not only candidates. A broad range is a review lead; it is not automatically inadequate.

The terminology inventory preserves every exact source match event and complete matching source line. Selected glossary rows appear once, accompanied by an index to their original data-record IDs and physical line ranges. Count tables retain search terms with zero hits. Word and phrase families overlap intentionally, so event totals are not counts of distinct mathematical usages.

The primary reader's `recurrence/page_pattern_counts.tsv` accompanies the parser's own page-count table. It records the original recurrence pass's literal typography patterns. The late paragraph joins and the two build-only French preamble changes do not change those counted command tokens.

## Optional verbose regeneration

Duplicate full-wrapper and full-span tables are excluded from the compact deliverable. They can be regenerated in scratch when a location needs investigation:

```bash
python scripts/recurrence_math_inventory.py --verbose --output ../work/recurrence_math_verbose
python scripts/recurrence_terminology_inventory.py --verbose --output ../work/recurrence_terminology_verbose
```

Verbose output is refused inside the deliverable tree. Within the deliverable, each tool permits only its own inventory directory. Source directories, the deliverable root, and other records are not valid output destinations.

## Lexical limits

The math lexer recognizes literal dollar, bracket and parenthesis math delimiters, common math environments and `ensuremath`. It parses the configured text wrappers and math alphabet arguments with balanced braces. Explicit math nested within a text wrapper is scanned in its own mode. It preserves control-sequence names and known non-glyph arguments. Unknown macro expansion, conditional execution, verbatim syntax, and custom TeX grammars are not interpreted. Uncertain arrow-option labels and malformed known syntax are reported separately. A zero candidate count is a lexical result, not proof of every rendered glyph.

French printed pages come from source page markers. English locations use exact component file, line and column positions; printed-page numbers remain blank where the source does not encode them. The generator does not infer printed pages from the page layout.

Terminology matching is case-insensitive and bounded by word characters, while exact spelling and capitalization are retained. Spaces and hyphens are literal. TeX spacing commands, nonbreaking spaces, line breaks within a phrase, macro expansion, and alternative hyphen characters are not normalized. Raw comments, commands and anchors are included. Glossary selection searches all fields and provides lexical leads, not a replacement recommendation.

Each generator hashes its inputs and checks they remain unchanged during generation. Regenerate a ledger-based inventory after ledger edits, including confidence-only changes, so its snapshot hash remains current.
