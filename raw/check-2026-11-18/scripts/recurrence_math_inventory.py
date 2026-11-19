"""Read-only lexical recurrence support; no image reading or adjudication.

From the deliverable root:
    python scripts/recurrence_math_inventory.py

All paths are configurable. Compact output defaults to recurrence/math.
Full duplicate source-span tables require --verbose and an external scratch
destination. This script never modifies its source or ledger inputs.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path
import re
import sys


MATH_ENVS = {"math", "displaymath", "equation", "equation*", "align", "align*", "alignat", "alignat*", "flalign", "flalign*", "gather", "gather*", "multline", "multline*", "eqnarray", "eqnarray*", "aligned", "alignedat", "gathered", "split", "array", "matrix", "pmatrix", "bmatrix", "Bmatrix", "vmatrix", "Vmatrix", "smallmatrix", "cases", "tikzcd", "CD"}
FONT_ARGS = {"mathrm", "mathcal", "mathfrak", "mathbf", "mathbb", "mathsf", "mathit", "mathscr", "mathnormal", "operatorname"}
FONT_DECLARATIONS = {"rm", "bf", "it", "sf", "tt", "cal", "frak", "rmfamily", "sffamily", "ttfamily", "normalfont", "bfseries", "itshape", "slshape", "scshape", "upshape"}
TEXT_ARGS = {"text": 1, "mbox": 1, "textrm": 1, "textsf": 1, "texttt": 1, "textnormal": 1, "textbf": 1, "textit": 1, "textsl": 1, "textsc": 1, "textup": 1, "emph": 1, "hbox": 1, "vbox": 1, "fbox": 1, "makebox": 1, "parbox": 2, "raisebox": 2, "shortstack": 1, "textcolor": 2, "colorbox": 2, "fcolorbox": 3, "footnote": 1, "footnotetext": 1, "caption": 1, "uline": 1}
NON_GLYPH_ARGS = {"label": 1, "ref": 1, "eqref": 1, "pageref": 1, "cite": 1, "GAGACite": 1, "GAGATarget": 1, "tag": 1, "color": 1, "hspace": 1, "vspace": 1}


@dataclass
class Wrapper:
    start: int
    arg_start: int
    arg_end: int
    end: int
    name: str


@dataclass
class Span:
    start: int
    content_start: int
    content_end: int
    end: int
    kind: str
    complete: bool = True


def mask_comments(text: str) -> str:
    chars = list(text)
    for match in re.finditer("%", text):
        before, count = match.start() - 1, 0
        while before >= 0 and text[before] == chr(92):
            count += 1
            before -= 1
        if count % 2:
            continue
        end = text.find("\n", match.start())
        if end < 0:
            end = len(text)
        chars[match.start():end] = " " * (end - match.start())
    return "".join(chars)


def command(text: str, position: int) -> tuple[str, int]:
    end = position + 1
    if end >= len(text):
        return "", end
    if text[end].isalpha() or text[end] == "@":
        while end < len(text) and (text[end].isalpha() or text[end] == "@"):
            end += 1
        return text[position + 1:end], end
    return text[end], end + 1


def commands(text: str):
    position = 0
    while position < len(text):
        if text[position] == chr(92):
            name, end = command(text, position)
            yield position, name, end
            position = end
        else:
            position += 1


def group(text: str, position: int, opener: str = "{", closer: str = "}") -> tuple[int, int, int] | None:
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != opener:
        return None
    start, level = position + 1, 1
    position += 1
    while position < len(text):
        if text[position] == chr(92):
            _, position = command(text, position)
            continue
        if text[position] == opener:
            level += 1
        elif text[position] == closer:
            level -= 1
            if not level:
                return start, position, position + 1
        position += 1
    return None


def arguments(text: str, position: int, count: int) -> list[tuple[int, int, int]]:
    if position < len(text) and text[position] == "*":
        position += 1
    result: list[tuple[int, int, int]] = []
    while True:
        optional = group(text, position, "[", "]")
        if not optional:
            break
        position = optional[2]
    for _ in range(count):
        arg = group(text, position)
        if not arg:
            return []
        result.append(arg)
        position = arg[2]
        while True:
            optional = group(text, position, "[", "]")
            if not optional:
                break
            position = optional[2]
    return result


def wrappers(text: str) -> tuple[list[Wrapper], list[tuple[int, str]]]:
    result, warnings = [], []
    for position, name, end in commands(text):
        if name not in TEXT_ARGS:
            continue
        args = arguments(text, end, TEXT_ARGS[name])
        if args:
            start, stop, finish = args[-1]
            result.append(Wrapper(position, start, stop, finish, name))
        else:
            warnings.append((position, "Text-wrapper arguments could not be parsed: " + name))
    return result, warnings


def math_spans(text: str, wrapper_list: list[Wrapper], *, implicit_math: bool = False) -> tuple[list[Span], list[tuple[int, str]]]:
    found: list[Span] = []
    warnings: list[tuple[int, str]] = []
    wrapper_at = {wrapper.start: wrapper for wrapper in wrapper_list}

    def scan(low: int, high: int, forced: Span | None = None, depth: int = 0) -> None:
        if depth > 30:
            warnings.append((low, "Math/text nesting exceeds parser depth; region not expanded."))
            return
        active: dict[str, object] | None = {"span": forced, "closing": "forced", "level": 1} if forced else None
        position = low
        while position < high:
            if text[position] == "$":
                token = "$$" if text.startswith("$$", position) else "$"
                if active is None:
                    active = {"span": Span(position, position + len(token), high, high, token), "closing": token, "level": 1}
                elif active["closing"] == token:
                    span = active["span"]
                    span.content_end, span.end = position, position + len(token)
                    found.append(span)
                    active = None
                else:
                    warnings.append((position, "Unexpected dollar delimiter inside " + str(active["closing"]) + " math; no mode judgment made."))
                position += len(token)
                continue
            if text[position] != chr(92):
                position += 1
                continue
            name, end = command(text, position)
            if active is not None and position in wrapper_at:
                wrapper = wrapper_at[position]
                scan(wrapper.arg_start, min(wrapper.arg_end, high), depth=depth + 1)
                position = min(wrapper.end, high)
                continue
            if name == "ensuremath":
                args = arguments(text, end, 1)
                if args:
                    start, stop, finish = args[0]
                    scan(start, min(stop, high), Span(position, start, stop, finish, "ensuremath"), depth + 1)
                    position = min(finish, high)
                    continue
            if name in {"[", "("} and active is None:
                active = {"span": Span(position, end, high, high, "display bracket" if name == "[" else "math parenthesis"), "closing": "]" if name == "[" else ")", "level": 1}
                position = end
                continue
            if active is not None and name == active["closing"]:
                span = active["span"]
                span.content_end, span.end = position, end
                found.append(span)
                active = None
                position = end
                continue
            if name in {"begin", "end"}:
                arg = group(text, end)
                if arg:
                    environment = text[arg[0]:arg[1]].strip()
                    if name == "begin" and environment in MATH_ENVS:
                        if active is None:
                            active = {"span": Span(position, arg[2], high, high, "environment " + environment), "closing": "env:" + environment, "level": 1}
                        elif active["closing"] == "env:" + environment:
                            active["level"] += 1
                    elif name == "end" and active is not None and active["closing"] == "env:" + environment:
                        active["level"] -= 1
                        if not active["level"]:
                            span = active["span"]
                            span.content_end, span.end = position, arg[2]
                            found.append(span)
                            active = None
                    position = arg[2]
                    continue
            position = end
        if active is not None:
            span = active["span"]
            if active["closing"] == "forced":
                found.append(span)
            else:
                span.content_end, span.end, span.complete = high, high, False
                found.append(span)
                warnings.append((span.start, "Unterminated math span; candidates in it are uncertain."))

    initial = Span(0, 0, len(text), len(text), "implicit math") if implicit_math else None
    scan(0, len(text), initial)
    return sorted(found, key=lambda span: (span.start, span.end)), warnings


def capital_tokens(text: str, span: Span, spans: list[Span], wrapper_list: list[Wrapper]) -> tuple[list[int], list[tuple[int, str]]]:
    tokens, warnings = [], []
    wrappers_at = {wrapper.start: wrapper for wrapper in wrapper_list}
    child_at = {child.start: child for child in spans if child is not span and span.content_start <= child.start < child.end <= span.content_end}
    fonts = [False]
    position = span.content_start
    # Initial optional/array-format arguments are environment metadata.
    if span.kind.startswith("environment "):
        optional = group(text, position, "[", "]")
        if optional:
            if re.search(r"[A-Z]", text[optional[0]:optional[1]]):
                warnings.append((optional[0], "Capital(s) in initial environment options; metadata or labels require manual inspection."))
            position = optional[2]
        if span.kind == "environment array":
            fmt = group(text, position)
            if fmt:
                position = fmt[2]
    while position < span.content_end:
        if position in child_at:
            position = child_at[position].end
            continue
        char = text[position]
        if char == "{":
            fonts.append(fonts[-1])
            position += 1
            continue
        if char == "}":
            if len(fonts) > 1:
                fonts.pop()
            position += 1
            continue
        if char == chr(92):
            name, end = command(text, position)
            if position in wrappers_at:
                position = wrappers_at[position].end
                continue
            if name in FONT_ARGS:
                cursor = end + (1 if end < len(text) and text[end] == "*" else 0)
                arg = group(text, cursor)
                if arg:
                    position = arg[2]
                    continue
                while cursor < span.content_end and text[cursor].isspace():
                    cursor += 1
                if cursor < span.content_end and text[cursor] == chr(92):
                    _, position = command(text, cursor)
                    warnings.append((cursor, "Non-braced command token used as a math-font argument; macro expansion not evaluated."))
                else:
                    position = min(cursor + 1, span.content_end)
                continue
            if name in FONT_DECLARATIONS:
                fonts[-1] = True
                position = end
                continue
            if name in NON_GLYPH_ARGS:
                args = arguments(text, end, NON_GLYPH_ARGS[name])
                position = args[-1][2] if args else end
                continue
            if name in {"GAGAInternalRef", "href"}:
                target = group(text, end)
                position = target[2] if target else end
                continue
            if name == "hyperref":
                target = group(text, end, "[", "]")
                position = target[2] if target else end
                continue
            if name in {"begin", "end"}:
                arg = group(text, end)
                if arg:
                    environment = text[arg[0]:arg[1]].strip()
                    position = arg[2]
                    optional = group(text, position, "[", "]")
                    if optional:
                        if re.search(r"[A-Z]", text[optional[0]:optional[1]]):
                            warnings.append((optional[0], "Capital(s) in nested environment options; manual inspection required."))
                        position = optional[2]
                    if name == "begin" and environment in {"array", "alignat", "alignat*", "alignedat"}:
                        fmt = group(text, position)
                        if fmt:
                            position = fmt[2]
                    continue
            if name in {"arrow", "ar"}:
                optional = group(text, end, "[", "]")
                if optional:
                    if re.search(r"[A-Z]", text[optional[0]:optional[1]]):
                        warnings.append((optional[0], "Capital(s) in arrow options/labels; exact option text is reported but not classified as glyphs."))
                    position = optional[2]
                    continue
            position = end
            continue
        if "A" <= char <= "Z" and not fonts[-1]:
            tokens.append(position)
        position += 1
    return tokens, warnings


def locations(text: str):
    starts = [0] + [match.end() for match in re.finditer("\n", text)]
    def locate(position: int) -> tuple[int, int, str]:
        index = bisect_right(starts, position) - 1
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        return index + 1, position - starts[index] + 1, text[starts[index]:end].rstrip("\r\n")
    return locate


def printed_page(text: str, position: int) -> str:
    prior = [match for match in re.finditer(r"^.*printed page\s+(\d+).*$", text, re.MULTILINE) if match.start() <= position]
    return prior[-1].group(1) if prior else ""


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def fenced(text: str) -> str:
    fence = "`" * max(3, max((len(match.group()) for match in re.finditer(r"`+", text)), default=0) + 1)
    return fence + "tex\n" + text + ("" if text.endswith("\n") else "\n") + fence + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("recurrence/math"))
    parser.add_argument("--verbose", action="store_true", help="Include duplicate full-span tables; destination must be outside the deliverable.")
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    if output == root or output == root / "sources" or root / "sources" in output.parents:
        raise ValueError("The inventory destination must not be the deliverable root or a source directory.")
    if root in output.parents and (root / "recurrence" / "math") not in (output, *output.parents):
        raise ValueError("Output inside the deliverable must be under recurrence/math.")
    if args.verbose and root in output.parents:
        raise ValueError("Verbose output must stay outside the deliverable tree.")
    output.mkdir(parents=True, exist_ok=True)
    source_root = root / "sources"
    paths = [source_root / "french-diplomatic/gaga_body.tex", source_root / "french-corrected/gaga_body.tex"] + sorted((source_root / "english/components").glob("*.tex"))
    token_rows, span_rows, wrapper_rows, warning_rows, snapshots = [], [], [], [], []
    page_counts = defaultdict(Counter)
    span_markdown = ["# Lexical capital-token candidates\n\nNo reading or correction judgment is made. These are source tokens outside recognized explicit alphabet wrappers in parsed math spans. Unknown macro expansion and option-label syntax remain limitations.\n\n"]
    wrapper_markdown = ["# Math-font commands inside textual wrappers\n\nEvery occurrence is listed without an error judgment. Explicit nested math is identified where the lexical parser can do so.\n\n"]
    for path in paths:
        data = path.read_bytes()
        raw = data.decode("utf-8")
        text = mask_comments(raw)
        relative = path.relative_to(source_root).as_posix()
        encoded_pages = re.findall(r"printed page\s+(\d+)", raw)
        for page in encoded_pages or [""]:
            page_counts[(relative, page)]
        locate = locations(raw)
        wrapper_list, warnings = wrappers(text)
        spans, span_warnings = math_spans(text, wrapper_list)
        warnings.extend(span_warnings)
        token_count = 0
        for index, span in enumerate(spans, 1):
            tokens, more_warnings = capital_tokens(text, span, spans, wrapper_list)
            warnings.extend(more_warnings)
            page = printed_page(raw, span.start)
            page_counts[(relative, page)]["math_spans"] += 1
            page_counts[(relative, page)]["capital_candidates"] += len(tokens)
            if not tokens:
                continue
            identifier = relative + ":M" + f"{index:04d}"
            start_line, start_column, _ = locate(span.start)
            end_line, end_column, _ = locate(max(span.start, span.end - 1))
            exact = raw[span.start:span.end]
            positions = []
            for position in tokens:
                line, column, source_line = locate(position)
                positions.append(str(line) + ":" + str(column) + "=" + raw[position])
                token_rows.append([relative, page, line, column, position, raw[position], identifier, span.kind, span.complete, source_line, exact])
            token_count += len(tokens)
            span_rows.append([identifier, relative, page, span.kind, span.complete, start_line, start_column, end_line, end_column, len(tokens), "; ".join(positions), exact])
            span_markdown.append("## " + identifier + "\n\nPrinted page: " + (page or "not encoded in this source") + "; source " + str(start_line) + ":" + str(start_column) + "–" + str(end_line) + ":" + str(end_column) + "; mode: " + span.kind + ".\n\nTokens: " + "; ".join(positions) + ".\n\n" + fenced(exact) + "\n")
        for position, name, end in commands(text):
            if name not in FONT_ARGS:
                continue
            containing = [wrapper for wrapper in wrapper_list if wrapper.arg_start <= position < wrapper.arg_end]
            if not containing:
                continue
            containing.sort(key=lambda wrapper: wrapper.arg_end - wrapper.arg_start)
            nearest = containing[0]
            nested = [span for span in spans if nearest.arg_start <= span.start <= position < span.end <= nearest.arg_end and span.complete]
            explicit = "yes" if nested else "no explicit nested math detected"
            line, column, source_line = locate(position)
            wrapper_line, wrapper_column, _ = locate(nearest.start)
            page = printed_page(raw, position)
            page_counts[(relative, page)]["math_font_commands_in_text"] += 1
            page_counts[(relative, page)]["without_nested_math"] += int(not nested)
            exact = raw[nearest.start:nearest.end]
            chain = "; ".join(wrapper.name + "@" + str(locate(wrapper.start)[0]) + ":" + str(locate(wrapper.start)[1]) for wrapper in containing)
            wrapper_rows.append([relative, page, line, column, name, nearest.name, wrapper_line, wrapper_column, explicit, chain, source_line, exact])
            wrapper_markdown.append("## " + relative + ":" + str(line) + ":" + str(column) + "\n\nCommand: `" + chr(92) + name + "`; nearest textual wrapper: `" + chr(92) + nearest.name + "` at " + str(wrapper_line) + ":" + str(wrapper_column) + "; explicit nested math: " + explicit + "; printed page: " + (page or "not encoded") + ".\n\n" + fenced(exact) + "\n")
        for position, warning in sorted(set(warnings)):
            line, column, source_line = locate(position)
            exact_region = source_line
            if "option" in warning.lower() and position > 0 and text[position - 1] == "[":
                optional = group(text, position - 1, "[", "]")
                if optional:
                    exact_region = raw[position - 1:optional[2]]
            warning_rows.append([relative, printed_page(raw, position), line, column, warning, source_line, exact_region])
            page_counts[(relative, printed_page(raw, position))]["parser_uncertainties"] += 1
        snapshots.append([relative, len(data), hashlib.sha256(data).hexdigest(), len(spans), token_count, len(warnings)])
    write_tsv(output / "capital_tokens.tsv", ["file", "printed_page_if_encoded", "source_line", "source_column", "character_offset", "capital", "span_id", "math_mode", "complete_span", "full_source_line", "full_math_span"], token_rows)
    write_tsv(output / "capital_spans.tsv", ["span_id", "file", "printed_page_if_encoded", "math_mode", "complete_span", "start_line", "start_column", "end_line", "end_column", "candidate_count", "candidate_locations", "full_math_span"], span_rows)
    wrapper_fields = ["file", "printed_page_if_encoded", "command_line", "command_column", "math_font_command", "nearest_text_wrapper", "wrapper_line", "wrapper_column", "explicit_nested_math", "wrapper_chain", "full_source_line", "full_nearest_wrapper"]
    write_tsv(output / "math_fonts_without_nested_math.tsv", wrapper_fields, [row for row in wrapper_rows if row[8] != "yes"])
    wrapper_counts = Counter((row[0], row[1], row[4], row[5], row[8]) for row in wrapper_rows)
    write_tsv(output / "math_font_wrapper_counts.tsv", ["file", "printed_page_if_encoded", "math_font_command", "nearest_text_wrapper", "explicit_nested_math", "count"], [[*key, count] for key, count in sorted(wrapper_counts.items())])
    page_fields = ["math_spans", "capital_candidates", "parser_uncertainties", "math_font_commands_in_text", "without_nested_math"]
    write_tsv(output / "math_page_counts.tsv", ["file", "printed_page_if_encoded", *page_fields], [[filename, page, *[counts[field] for field in page_fields]] for (filename, page), counts in sorted(page_counts.items(), key=lambda pair: (pair[0][0], int(pair[0][1] or 0)))])
    write_tsv(output / "parser_uncertainties.tsv", ["file", "printed_page_if_encoded", "source_line", "source_column", "uncertainty", "full_source_line", "full_option_or_source_line"], warning_rows)
    write_tsv(output / "math_source_snapshots.tsv", ["file", "bytes", "sha256", "parsed_math_spans", "capital_candidates", "parser_warning_events"], snapshots)
    if args.verbose:
        write_tsv(output / "math_fonts_in_text_wrappers.tsv", wrapper_fields, wrapper_rows)
        (output / "capital_spans.md").write_text("".join(span_markdown), encoding="utf-8")
        (output / "math_fonts_in_text_wrappers.md").write_text("".join(wrapper_markdown), encoding="utf-8")
    ledger_data = (root / "CORRECTIONS.tsv").read_bytes()
    reader = csv.DictReader(io.StringIO(ledger_data.decode("utf-8"), newline=""), delimiter="\t")
    ledger_fields = list(reader.fieldnames or []) if args.verbose else ["file", "layer", "printed_page", "line", "statement", "kind", "confidence"]
    generic_rows, broad_rows, priority_rows = [], [], []
    for index, row in enumerate(reader, 1):
        locator = row.get("line", "")
        reasons = []
        if re.search(r"\bcorresponding\b", locator, re.IGNORECASE):
            reasons.append("corresponding paragraph/formula is not an individual printed-line locator")
        if re.search(r"\bsource(?:\s+(?:line|position|paragraph|formula))?\b", locator, re.IGNORECASE):
            reasons.append("locator explicitly refers to source position")
        if locator.strip().casefold() in {"body", "formula", "display", "paragraph", "text", "source"}:
            reasons.append("generic unnumbered position label")
        if re.search(r"\b(?:displays|formulas|paragraphs)\b", locator, re.IGNORECASE) and not re.search(r"\d", locator):
            reasons.append("unnumbered multiple-display/formula/paragraph label")
        values = [index, index + 1, "; ".join(reasons), *[row.get(field, "") for field in ledger_fields]]
        if reasons:
            generic_rows.append(values)
        broad = []
        for match in re.finditer(r"\b(lines?|paragraphs?)\s+(\d+)\s*[-–]\s*(\d+)", locator, re.IGNORECASE):
            size = int(match.group(3)) - int(match.group(2)) + 1
            if size >= 8 or match.group(1).lower().startswith("paragraph") and size > 1:
                broad.append("broad " + match.group(1) + " range " + match.group(2) + "–" + match.group(3) + "; not itself a proof of inadequacy")
        if broad:
            broad_rows.append([index, index + 1, "; ".join(broad), *[row.get(field, "") for field in ledger_fields]])
        if row.get("printed_page") in {"28", "29"}:
            priority_rows.append(values)
    headers = ["data_record_1_based", "ledger_row_header_is_1", "mechanical_reason", *ledger_fields]
    write_tsv(output / "generic_locator_candidates.tsv", headers, generic_rows)
    write_tsv(output / "broad_locator_ranges.tsv", headers, broad_rows)
    write_tsv(output / "pp28_29_all_locator_rows.tsv", headers, priority_rows)
    no_nested = sum(row[8] != "yes" for row in wrapper_rows)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = "# Mechanical math and locator recurrence inventory\n\nGenerated " + now + ". No source, ledger, image or editorial record was modified. No reading, translation or mathematical judgment is made.\n\n"
    report += "- Capital-token candidates: " + str(len(token_rows)) + " in " + str(len(span_rows)) + " math spans.\n- Math-font command occurrences inside textual wrappers: " + str(len(wrapper_rows)) + "; without an explicit nested math span detected: " + str(no_nested) + ".\n- Parser uncertainty locations: " + str(len(warning_rows)) + ".\n- Generic-locator candidates: " + str(len(generic_rows)) + "; broad-range rows separately listed: " + str(len(broad_rows)) + ".\n- Every page-28/29 ledger row retained in the priority table: " + str(len(priority_rows)) + ".\n\n"
    report += "## Scope and limitations\n\nMath spans use literal dollar, bracket and parenthesis delimiters, common math environments, and ensuremath. Text wrappers are parsed with balanced braces; nested explicit math in those wrappers is scanned separately. Recognized math alphabet arguments and font declarations are excluded from ordinary-capital candidates. Arrow-option capitals, unparsable wrappers and delimiter anomalies are reported separately. Arbitrary macro expansion, conditional TeX execution, verbatim environments and custom syntax are not evaluated; this is a lexical candidate inventory, not a certificate of every rendered glyph. Printed-page numbers are supplied only where source markers encode them; English component locations remain exact source line/column positions.\n\n"
    report += "Compact output retains full exact source text only for capital candidates, parser uncertainties, and math-font commands without detected explicit nested math. Valid nested text-wrapper formulas are represented by counts, not duplicate full-source extracts. Page counts are lexical event counts; English printed pages are blank where they are not encoded. Locator tables retain original data-row IDs, file/layer, exact locators, statement, kind and confidence; old/new/evidence text remains in the authoritative ledger. Generic-locator reasons are lexical signals; only the primary reader can refine them against the print. Verbose duplicate tables can be regenerated outside the deliverable with --verbose.\n\nCORRECTIONS.tsv snapshot SHA-256: `" + hashlib.sha256(ledger_data).hexdigest() + "`.\n"
    source_changed = any(hashlib.sha256((source_root / row[0]).read_bytes()).hexdigest() != row[2] for row in snapshots)
    ledger_changed = (root / "CORRECTIONS.tsv").read_bytes() != ledger_data
    report += "\nInputs unchanged during generation: " + ("no; regenerate this snapshot" if source_changed or ledger_changed else "yes") + ".\n"
    (output / "MATH_AND_LOCATORS_REPORT.md").write_text(report, encoding="utf-8")
    print("Capital candidates=" + str(len(token_rows)) + "; candidate spans=" + str(len(span_rows)) + "; parser uncertainties=" + str(len(warning_rows)))
    print("Math-font commands in text wrappers=" + str(len(wrapper_rows)) + "; without explicit nested math detected=" + str(no_nested))
    print("Generic locator candidates=" + str(len(generic_rows)) + "; page-28/29 rows=" + str(len(priority_rows)))
    print("Read-only inventory written to configured destination; no judgments assigned.")
    return 1 if source_changed or ledger_changed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print("Inventory stopped: " + type(error).__name__ + ". Check source/ledger inputs and scratch destination.", file=sys.stderr)
        sys.exit(2)
