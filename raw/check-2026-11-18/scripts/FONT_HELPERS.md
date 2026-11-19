# Balanced font helper behavior

The `font_inline` and `font_display` functions in `audit.py` are manual collation helpers. They are called only after the primary reader has individually verified the intended capital-font changes against the scan. The helper update itself did not change edition sources or ledger entries.

`upright_math_capitals(text, letters, implicit_math=False)` is the pure transformation used by both writers. It uses the adjacent `recurrence_math_inventory.py` lexer. It changes only selected ordinary ASCII capital tokens in recognized math mode, retaining all other characters exactly.

Balanced arguments of textual wrappers such as `text`, `mbox`, `textrm`, `textit`, `emph`, `parbox` and `footnote` remain text. Explicit nested formulas inside those arguments are parsed independently. For example, in a display containing `\text{(Artin--Rees; Exposé~2), $A$}`, the names remain unchanged and the nested formula can become `$\mathrm{A}$`. Nested braces in the textual argument do not end that protection early.

Existing math alphabet arguments, control-sequence names, comments and known metadata arguments are preserved. A selected capital already inside `\mathrm`, `\mathcal` or another recognized math alphabet is not wrapped again. The transformation is idempotent for the tested cases. Arbitrary macro expansion is not attempted.

`font_inline` records one ledger row for each changed outer inline formula, including changes in its nested explicit math. A nested formula inside that outer formula does not create a second overlapping ledger row. Dollar and parenthesized inline math delimiters are recognized. The writer preserves the paragraph's remaining characters and the existing line ending.

`font_display` expects the selected lines to include the display's math delimiters. For a manually inspected formula fragment without delimiters, the caller must explicitly supply `implicit_math=True`. This avoids treating an incidental textual fragment as math merely because it was passed to a display helper.

Malformed known wrapper syntax, unbalanced braces, unmatched math delimiters, and reported ambiguous option tokens raise an exception before either writer changes a source or appends to the ledger. This protection does not replace review of custom macro syntax or a visual font judgment.

## Synthetic verification

Seven exact transformation fixtures covered nested braces, Artin/Exposé textual material, nested math inside nested text wrappers, command names, existing math alphabets, font declarations, metadata targets, multi-argument text wrappers, escaped dollars, comments, and the four unbraced-subscript patterns. The resulting strings matched the expected strings exactly, and applying the transformation a second time made no change in all seven cases.

Four ambiguous-input fixtures were refused. Separate scratch-only writer fixtures verified inline ledger grouping, the display writer, and preservation of both source and ledger after refusal. Hashes of the actual edition source files and `CORRECTIONS.tsv` were identical before and after these tests. No actual edition font helper was executed.
