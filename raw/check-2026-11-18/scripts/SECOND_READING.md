# Generating the correction rereading worklists

From the deliverable root:

```sh
python scripts/second_reading_worklist.py --root . --output ../work/second_reading
```

Run the same command again after ledger edits. The default destination, when
`--output` is omitted, is the sibling scratch directory `work/second_reading`.
An output directory inside the deliverable tree is rejected. Only generated
worklist files are replaced; edition sources, ledgers, page records, notes and
images are never modified.

The scratch output contains:

- `INDEX.md`: the ledger snapshot hash, counts and links to every worklist.
- `page_01.md` through `page_42.md`: complete per-page lists, including explicit
  empty lists where the ledger has no correction rows for that page.
- `global_and_preamble.md`: all main-file/preamble, build, page-range,
  non-page-source and unspecified/out-of-range rows.
- `row_manifest.tsv`: every original record and field, with its displayed unit,
  routing reason, logical row number and physical TSV line span.
- `unit_manifest.tsv`: the exact fields defining every displayed group, every
  member row number and the explicitly named evidence-image references.
- `evidence_manifest.tsv`: evidence filenames and sizes, filename-inferred
  printed pages and units explicitly naming the file.

## Exact grouping and complete text

Rows are grouped only within the same page/global bucket and only when `old`,
`new`, `evidence` and `kind` are exactly equal, including whitespace. The lists
retain each original row number, layer, file, printed-page field, line field,
statement and current confidence. Every old/new/evidence field is displayed
in full, with a safe-length Markdown code fence. The TSV manifests preserve
the exact original field values, including multiline contents.

A logical ledger-row number counts the header as row 1. The data-record number
starts at 1 after the header. Physical line spans are separate because one
quoted TSV record can occupy several lines.

Main preamble files remain in the separate global list even if their recorded
page field is numeric. Numeric pages outside 1–42, ranges and other page
labels also remain there. All routing reasons are explicit; no record is
dropped. The generator asserts that every input record appears exactly once.

## Evidence and verdicts

The generator reads image filenames and size metadata only. It does not open
an image, make a montage, decide a reading or assign a verdict. Explicit
image references are resolved against the evidence directory; missing and
ambiguous names are reported. Per-page evidence inventories use only filename
patterns such as `p01-...`; they do not assert that a particular image proves
a particular correction. Files with no page inferred from their names appear
in the global list.

Grouping is a display convenience. Every listed occurrence still requires the
primary reader's assessment. Make verdict changes in the editorial ledger;
annotations made directly in generated worklists would be replaced by the
next generation. The index records the precise source-ledger SHA-256 and
warns if the ledger changed during generation.

## Infrastructure validation

Synthetic tests verified preservation of all input fields, separate grouping
when evidence or whitespace differs, full display of a multiline field over
12,000 characters long, embedded backtick handling, physical line spans,
punctuation-adjacent image filenames, separate preamble/range routing, all
42 page files, and rejection of a destination inside the deliverable tree.
No verdicts were assigned during testing.

## Compact terminal supplement

The supplementary CLI prints the same exact-field grouping with much less
repeated scaffolding. It writes only to standard output:

```sh
python scripts/second_reading_compact.py --root . --pages 1-3,7
python scripts/second_reading_compact.py --root . --pages 39-42 --include-global
python scripts/second_reading_compact.py --root . --global-only
```

Omitting selection options prints all 42 pages and the separate global list.
`--pages` accepts comma-separated inclusive ranges and may be repeated.
Per-page evidence strings appear once in a local evidence dictionary; groups
refer to those exact strings by ID. `--repeat-evidence` prints the complete
evidence text in every group instead. Old/new text is always complete.

Data IDs `D1`, `D2`, and so on are one-based records after the header; their
header-counted ledger row numbers are respectively 2, 3, and so on. File aliases
provide the full layer/file mapping. Every data ID and printed-line locator is
listed, with statements where present and the raw page field for global/range
rows. The compact CLI neither filters by confidence nor assigns a judgment.
