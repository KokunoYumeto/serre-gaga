# Mechanical source-integrity audit

After the sequential page reading and the second reading of corrections, run
from the deliverable root:

```sh
python scripts/integrity_audit.py --original ../input/GAGA_sources --root .
```

The original-source directory is configurable and must be a separate copy of
the supplied source archive. `--output` changes the report directory; its
default is `integrity/` beneath the deliverable root. The script never modifies
edition sources, correction rows, page records, notes or the progress log. It
does not invoke a TeX engine or read scan images.

## What is checked

- Every supplied source filename is retained. Original-source SHA-256 values
  are verified against the supplied manifest when it is present.
- The complete supplied README files remain byte-identical, protecting their
  rights notices and all credits, including the Thomas Waring credit and its
  wording. The root delivery README is a separate document and is not treated
  as a supplied README.
- Original leading provenance-comment blocks and credit-bearing lines in
  preambles/title matter are retained verbatim. Other changes to title matter
  are listed separately, because scan-supported typography or structural
  corrections can change that layout without changing the credits.
- Exact printed-page marker lines and their order are retained; each French
  body must contain printed pages 1 through 42 exactly once.
- Explicit labels, anchor targets and literal input/include targets remain
  present in their original sequence. Additions or order changes are reported.
- Existing signatures of common explicit command, alias, environment and
  Unicode declarations remain present. Added macros are permitted and remain
  subject to the correction-ledger comparison.
- Correction columns, kinds, layers, evidence presence and final confidence
  labels are checked mechanically.
- Each current source is reconstructed from its supplied original by applying
  its ledger's old/new substitutions in record order. Final byte equality is
  the decisive comparison.
- All original and final differences between the French bodies are listed.
  French preambles are also compared directly. Exact changed-core matches
  identify candidate corrected-layer misprint rows or original differences,
  with inherited verdict IDs associated by printed page.

## Ledger reconstruction

One narrowly recognized article-author case is reported as REVIEW rather than
FAIL: the original French body line crediting Jean-Pierre Serre in small caps
has the recorded centered/bold/uppercase markup. The exact markup change and
the full original/current front-matter diff remain reported, and the primary
reader must confirm both the printed-page-1 typography and the unchanged
attribution. This does not clear the item automatically. The exception applies
only to that exact author-line pair in the two French bodies; verbatim
protection of README, rights, edition, model and source-credit notices is
unchanged.

For a French body, substitutions are confined to the printed page named by
the row. The English files have no printed-page markers, so their entire
component is the mechanical search scope. Printed line descriptions and the
English printed-page assignment cannot be certified from substring mechanics.

A unique exact old-text occurrence is replaced directly. Where the same old
text occurs several times, the final text supplies surrounding context to
choose a candidate location. Replacement bytes always come from the ledger;
the final file never supplies missing replacement text. Every choice, match
count and multiplicity is recorded. Consequently, exact final equality is a
textual witness that the recorded substitutions can produce the current file,
even when an occurrence choice was not unique.

The algorithm is deterministic and conservative about failure. It does not
search every possible edit-history branch. A failure can reflect ambiguous
repeated text, amended rows, overlapping substitutions, insertion rows without
an old-text locator, or an unrecorded change. `unreconstructed_source_changes.diff`
shows the residual for the primary reader; a failure alone is not a claim that
the edit is unrecorded. Rows that could not be replayed are identified even if
other rows happen to produce the final bytes.

## French-layer coverage

`final_french_layers.diff` contains every remaining difference between the two
French layers. The coverage table provides exact changed-core candidates; it
does not decide whether an original reading is a mathematical misprint. A
candidate may match a part of a row containing several changes.

Inherited verdict readings may use human mathematical notation rather than
literal TeX. Their association is therefore explicitly page-level. This script
cannot certify a one-to-one correspondence between an inherited correction
and its verdict, or assess the reason for confirming or reverting it. Missing
exact candidates are flagged for review; notation changes around a correction
can prevent a literal core match.

## Reports and exit status

- `REPORT.md` and `checks.tsv`: summary and individual results.
- `source_inventory.tsv`: original/current hashes and ledger-row counts.
- `ledger_replay_rows.tsv`: the disposition of every recorded substitution.
- `unreconstructed_source_changes.diff`: any residual after ledger replay.
- `frontmatter_changes.diff`: nonidentical title/front-matter blocks.
- `original_french_layers.diff` and `original_french_differences.tsv`: supplied
  inter-layer differences and page-level verdict associations.
- `final_french_layers.diff` and `final_french_difference_coverage.tsv`: final
  inter-layer differences and candidate coverage.

Exit status 0 means no mechanical gap was detected within this scope; status 1
means review items remain; status 2 means at least one mechanical failure or an
input error. None of these statuses certifies a visual reading, translation,
mathematical proof, complete historical-verdict matching or final PDF quality.
The TeX syntax checks recognize common literal declarations and do not execute
arbitrary macro expansion or conditional code.

## Infrastructure validation

The audit was tested on separate synthetic 42-marker French bodies. It
correctly reconstructed a change at the intended one of two repeated old-text
occurrences, retained an inherited difference with a page-level verdict,
matched a new recorded inter-layer correction, and returned no gaps for the
valid fixture. Separate deliberately unledgered text, altered README credit
and removed-anchor variants each produced failures. These tests did not run
the audit against the live edition or alter any actual editorial record.
