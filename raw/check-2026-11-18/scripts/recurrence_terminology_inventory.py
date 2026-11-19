"""Inventory literal terminology occurrences without editorial judgments.

Run from GAGA_CHECK:
    python scripts/recurrence_terminology_inventory.py

Inputs and output directory are configurable. Source and glossary bytes are
read only. Compact outputs default to recurrence/terminology. Use --verbose
only with an output directory outside the deliverable for duplicate tables.
No image, scan, mathematical-context folder or TeX build is used.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path
import re
import subprocess
import sys


SOURCE_TERMS = {
    "fibre/fiber/stalk": ["fibre", "fibres", "fiber", "fibers", "stalk", "stalks"],
    "fibre-space/fibre space/fiber space/bundle": [
        "fibre-space", "fibre-spaces", "fibre space", "fibre spaces",
        "fiber-space", "fiber-spaces", "fiber space", "fiber spaces", "bundle", "bundles",
    ],
    "covering/cover": ["covering", "coverings", "cover", "covers"],
    "separated/Hausdorff": ["separated", "Hausdorff"],
    "quotient field/fraction field": ["quotient field", "quotient fields", "fraction field", "fraction fields"],
}
GLOSSARY_LOOKUPS = [
    "field of fractions", "fields of fractions", "corps des fractions",
    "corps de fractions", "corps quotient", "fibré", "fibrés", "fibrée", "fibrées",
    "recouvrement", "recouvrements", "séparé", "séparés", "séparée", "séparées",
]


def pattern(term: str) -> re.Pattern[str]:
    return re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    path.write_text(stream.getvalue(), encoding="utf-8")


def match_lines(text: str, expressions: list[tuple[str, str, re.Pattern[str]]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        for family, term, regex in expressions:
            for match in regex.finditer(line):
                result.append({
                    "family": family, "term": term, "match": match.group(),
                    "line": line_number, "column_start": match.start() + 1,
                    "column_end_exclusive": match.end() + 1,
                    "byte_start": len(line[:match.start()].encode("utf-8")),
                    "byte_end": len(line[:match.end()].encode("utf-8")),
                    "source_line": line,
                })
    return sorted(result, key=lambda item: (item["line"], item["column_start"], item["column_end_exclusive"], item["term"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--glossary", type=Path, default=Path("../input/GAGA_context/glossary/GLOSSARY_SGA_EN_UNIFIED.tsv"))
    parser.add_argument("--output", type=Path, default=Path("recurrence/terminology"))
    parser.add_argument("--verbose", action="store_true", help="Write duplicate full-source tables outside the deliverable only.")
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    inside_root = output == root or root in output.parents
    own_output = root / "recurrence" / "terminology"
    if inside_root and output != own_output and own_output not in output.parents:
        parser.error("Within the deliverable, output must be recurrence/terminology or its subdirectory; source, ledger, script and other record destinations are refused.")
    if args.verbose and inside_root:
        parser.error("Verbose duplicate tables require an output directory outside the deliverable tree.")
    if output == args.glossary.resolve() or args.glossary.resolve().is_relative_to(output):
        parser.error("The glossary input or a directory containing it cannot be the output destination.")
    source_folder = root / "sources" / "english" / "components"
    found = subprocess.run(["rg", "--files", str(source_folder), "-g", "*.tex"], capture_output=True, text=True, check=True)
    source_files = sorted(Path(line) for line in found.stdout.splitlines())
    expressions = [(family, term, pattern(term)) for family, terms in SOURCE_TERMS.items() for term in terms]
    source_matches: list[dict[str, object]] = []
    source_snapshots: list[list[object]] = []
    for path in source_files:
        data = path.read_bytes()
        relative = path.relative_to(root).as_posix()
        matches = match_lines(data.decode("utf-8"), expressions)
        for item in matches:
            item["file"] = relative
        source_matches.extend(matches)
        source_snapshots.append([relative, len(data), sha(data), len(matches)])
    glossary_data = args.glossary.read_bytes()
    glossary_text = glossary_data.decode("utf-8-sig")
    glossary_lines = glossary_text.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(glossary_text, newline=""), delimiter="\t")
    glossary_header = next(reader)
    header_end = reader.line_num
    previous_end = header_end
    glossary_records: list[tuple[int, int, int, list[str], str]] = []
    for index, row in enumerate(reader, 1):
        start, end = previous_end + 1, reader.line_num
        glossary_records.append((index, start, end, row, "".join(glossary_lines[start - 1:end])))
        previous_end = end
    glossary_expressions = expressions + [("additional glossary lookup", term, pattern(term)) for term in GLOSSARY_LOOKUPS]
    selected_glossary: list[tuple[int, int, int, list[str], str]] = []
    glossary_matches: list[list[object]] = []
    for index, start, end, row, raw in glossary_records:
        matches = match_lines(raw, glossary_expressions)
        if not matches:
            continue
        selected_glossary.append((index, start, end, row, raw))
        for match in matches:
            physical_line = start + int(match["line"]) - 1
            raw_line = match["source_line"]
            preceding = raw_line[:int(match["column_start"]) - 1]
            field_index = preceding.count("\t")
            field_name = glossary_header[field_index] if field_index < len(glossary_header) and len(row) == raw_line.rstrip("\r\n").count("\t") + 1 else "raw-row position"
            glossary_matches.append([index, start, end, physical_line, field_name, match["column_start"], match["column_end_exclusive"], match["family"], match["term"], match["match"], raw])
    output.mkdir(parents=True, exist_ok=True)
    source_fields = ["file", "line", "column_start_1based", "column_end_1based_exclusive", "byte_start_0based_in_line", "byte_end_0based_exclusive", "term_family", "literal_search_term", "exact_matched_text", "full_exact_source_line"]
    write_tsv(output / "source_occurrences.tsv", source_fields, [[m["file"], m["line"], m["column_start"], m["column_end_exclusive"], m["byte_start"], m["byte_end"], m["family"], m["term"], m["match"], m["source_line"]] for m in source_matches])
    unique_lines: dict[tuple[str, int], str] = {}
    locations_by_line: dict[tuple[str, int], list[str]] = defaultdict(list)
    for match in source_matches:
        key = (str(match["file"]), int(match["line"]))
        unique_lines[key] = str(match["source_line"])
        locations_by_line[key].append(str(match["column_start"]) + "–" + str(match["column_end_exclusive"]) + " " + str(match["term"]) + " = " + str(match["match"]))
    full_lines = []
    for (filename, line), content in sorted(unique_lines.items()):
        full_lines.append("=== " + filename + ":" + str(line) + " ===\n" + content + ("" if content.endswith("\n") else "\n") + "\n")
    if args.verbose:
        (output / "source_matching_lines.txt").write_text("".join(full_lines), encoding="utf-8")
        write_tsv(output / "source_line_index.tsv", ["file", "line", "literal_match_locations", "full_exact_source_line"], [[filename, line, "; ".join(locations_by_line[(filename, line)]), content] for (filename, line), content in sorted(unique_lines.items())])
    write_tsv(output / "source_snapshots.tsv", ["file", "bytes", "sha256", "match_count_including_overlap"], source_snapshots)
    glossary_header_raw = "".join(glossary_lines[:header_end])
    bom = bytes.fromhex("efbbbf") if glossary_data.startswith(bytes.fromhex("efbbbf")) else b""
    (output / "glossary_rows.tsv").write_bytes(bom + (glossary_header_raw + "".join(record[4] for record in selected_glossary)).encode("utf-8"))
    if args.verbose:
        write_tsv(output / "glossary_occurrences.tsv", ["data_record", "physical_start_line", "physical_end_line", "match_physical_line", "field", "column_start_1based", "column_end_1based_exclusive", "lookup_family", "literal_lookup_term", "exact_matched_text", "full_exact_original_row"], glossary_matches)
    write_tsv(output / "glossary_row_index.tsv", ["selected_row_1based", "data_record", "physical_start_line", "physical_end_line"], [[selected_index, index, start, end] for selected_index, (index, start, end, row, raw) in enumerate(selected_glossary, 1)])
    by_term = Counter(str(match["term"]) for match in source_matches)
    by_exact = Counter((str(match["term"]), str(match["match"])) for match in source_matches)
    by_family = Counter(str(match["family"]) for match in source_matches)
    by_file = Counter(str(match["file"]) for match in source_matches)
    write_tsv(output / "term_counts.tsv", ["term_family", "literal_search_term", "count_including_overlap"], [[family, term, by_term[term]] for family, terms in SOURCE_TERMS.items() for term in terms])
    write_tsv(output / "exact_spelling_counts.tsv", ["literal_search_term", "exact_matched_spelling", "count"], [[term, spelling, count] for (term, spelling), count in sorted(by_exact.items())])
    changed_sources = [relative for relative, _, digest, _ in source_snapshots if sha((root / relative).read_bytes()) != digest]
    glossary_changed = sha(args.glossary.read_bytes()) != sha(glossary_data)
    report = ["# Literal terminology recurrence inventory\n\n", "Generated " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + ". No reading, translation or replacement judgment is made.\n\n", "Source component files: " + str(len(source_files)) + "; lexical match events: " + str(len(source_matches)) + "; distinct matching source lines: " + str(len(unique_lines)) + "; selected glossary data rows: " + str(len(selected_glossary)) + ".\n\n", "Glossary snapshot SHA-256: `" + sha(glossary_data) + "`. Source snapshots are recorded separately.\n\n", "## Counts by requested family\n\n| Family | Match events |\n|---|---:|\n"]
    for family in SOURCE_TERMS:
        report.append("| " + family + " | " + str(by_family[family]) + " |\n")
    report.append("\n## Counts by source file\n\n| Source file | Match events |\n|---|---:|\n")
    for relative, _, _, _ in source_snapshots:
        report.append("| `" + str(relative) + "` | " + str(by_file[str(relative)]) + " |\n")
    report.append("\n## Scope and limitations\n\n- Matching is case-insensitive, with word boundaries; exact matched capitalization and spelling are preserved. Singular and ordinary plural forms are separate literal search terms.\n- Phrase spaces and hyphens are literal. TeX spacing commands, nonbreaking spaces, non-ASCII hyphens, macro expansion and line wrapping are not normalized. A phrase interrupted by such syntax is not counted as a literal phrase.\n- Families intentionally overlap: for example, the word fibre inside fibre space contributes a word event and a phrase event. Counts are lexical match events, not counts of distinct mathematical usages.\n- All raw source text is searched, including commands, anchors and comments; no semantic filtering is applied.\n- Glossary selection searches all fields. In addition to the requested English terms, explicit French lookup forms and field of fractions were searched as lexical leads. A selected row is not a recommended replacement or a verified mapping for this passage.\n- Full matching source lines and glossary rows are preserved without truncation. Character columns are one-based with exclusive ends; byte offsets are zero-based within the source line.\n- No scans, images, programme, research notes, Stacks context or GAGA build were used. No deliverable source, ledger or record was modified.\n")
    report.append("\n## Output and input verification\n\nThe compact inventory contains seven files: this report, exact source events, source hashes, selected exact glossary rows, their original row/line index, term counts, and exact spelling counts. Full-source line indexes and duplicate glossary-event tables are emitted only by the optional verbose mode outside the deliverable. The glossary subset preserves the original selected row text and header, including a byte-order mark if present.\n")
    if changed_sources or glossary_changed:
        report.append("\n**Inputs changed during generation. Regenerate before using this snapshot.**\n")
    else:
        report.append("\nAll " + str(len(source_snapshots)) + " source-component SHA-256 values and the glossary SHA-256 were unchanged when checked again at the end of generation.\n")
    (output / "REPORT.md").write_text("".join(report), encoding="utf-8")
    print("Source files=" + str(len(source_files)) + "; match events=" + str(len(source_matches)) + "; distinct source lines=" + str(len(unique_lines)) + "; glossary rows=" + str(len(selected_glossary)) + ".")
    print("Family counts: " + "; ".join(family + "=" + str(by_family[family]) for family in SOURCE_TERMS))
    print("No source, ledger, record or image modified; outputs are in the configured inventory directory.")
    return 1 if changed_sources or glossary_changed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, UnicodeError, ValueError, csv.Error, subprocess.CalledProcessError) as error:
        print("Inventory stopped: " + type(error).__name__ + ". Check configured relative input and output paths.", file=sys.stderr)
        raise SystemExit(2)
