"""Print compact, complete, unjudged correction groups to standard output.

From the deliverable root:
    python scripts/second_reading_compact.py --root . --pages 1-3,7
    python scripts/second_reading_compact.py --root . --pages 39-42 --include-global
    python scripts/second_reading_compact.py --root . --global-only

With no selection options, all 42 pages and the global/preamble list are shown.
Evidence strings are printed once per page and referenced by exact local IDs.
Use --repeat-evidence to repeat their complete text in each group instead.
There is no truncation, confidence filtering or automatic judgment. This tool
reads only CORRECTIONS.tsv and never changes a file or opens an image.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import sys


sys.dont_write_bytecode = True
from second_reading_worklist import GROUP_FIELDS, read_ledger


def page_selection(values: list[str] | None) -> list[int]:
    if values is None:
        return list(range(1, 43))
    pages: set[int] = set()
    for value in values:
        for token in value.split(","):
            token = token.strip()
            if token.casefold() == "all":
                pages.update(range(1, 43))
                continue
            match = re.fullmatch(r"(\d+)(?:[-–](\d+))?", token)
            if not match:
                raise ValueError("Use page numbers or inclusive ranges, for example 1-3,7,39-42.")
            first, last = int(match.group(1)), int(match.group(2) or match.group(1))
            if first < 1 or last > 42 or first > last:
                raise ValueError("Page ranges must be increasing and stay within 1 through 42.")
            pages.update(range(first, last + 1))
    return sorted(pages)


def field(label: str, value: str) -> None:
    """Keep every character of the field; delimiters are outside its text."""
    if "\n" not in value and "\r" not in value:
        print(label + ": " + value)
    else:
        print(label + " <<<")
        sys.stdout.write(value)
        if not value.endswith("\n"):
            sys.stdout.write("\n")
        print(">>> " + label)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--pages", action="append", help="Comma-separated page numbers/ranges; may be repeated.")
    parser.add_argument("--include-global", action="store_true")
    parser.add_argument("--global-only", action="store_true")
    parser.add_argument("--repeat-evidence", action="store_true")
    args = parser.parse_args()
    if args.global_only and (args.pages is not None or args.include_global):
        raise ValueError("Use --global-only without a page selection or --include-global.")
    pages = [] if args.global_only else page_selection(args.pages)
    include_global = args.global_only or args.include_global or args.pages is None
    buckets = [f"p{page:02d}" for page in pages] + (["global"] if include_global else [])
    data = (args.root / "CORRECTIONS.tsv").read_bytes()
    _, records = read_ledger(data)
    selected = [record for record in records if record["bucket"] in buckets]
    file_pairs = sorted({(record["row"]["layer"], record["row"]["file"]) for record in records})
    aliases = {pair: f"F{index:02d}" for index, pair in enumerate(file_pairs, 1)}
    used = {(record["row"]["layer"], record["row"]["file"]) for record in selected}
    print("COMPACT SECOND-READING INVENTORY — NO VERDICTS ASSIGNED")
    print("Data IDs D1... count records after the header; physical TSV line numbers can differ.")
    print("Selected records=" + str(len(selected)) + "/" + str(len(records)) + "; SHA-256=" + hashlib.sha256(data).hexdigest())
    print("FILE / LAYER MAP")
    for pair in file_pairs:
        if pair in used:
            print(aliases[pair] + " = " + pair[0] + " | " + pair[1])
    grouped: dict[str, dict[tuple[str, ...], list[dict[str, object]]]] = {bucket: {} for bucket in buckets}
    for record in selected:
        row = record["row"]
        key = tuple(row[name] for name in GROUP_FIELDS)
        grouped[str(record["bucket"])].setdefault(key, []).append(record)
    for bucket in buckets:
        units = list(grouped[bucket].values())
        count = sum(len(unit) for unit in units)
        heading = "GLOBAL / PREAMBLE / PAGE RANGES" if bucket == "global" else "PRINTED PAGE " + str(int(bucket[1:]))
        print("\n=== " + heading + " | " + str(count) + " records | " + str(len(units)) + " exact groups ===")
        if not units:
            print("No correction records in this bucket.")
            continue
        evidence_ids: dict[str, str] = {}
        for unit in units:
            evidence = unit[0]["row"]["evidence"]
            if evidence not in evidence_ids:
                evidence_ids[evidence] = f"E{len(evidence_ids) + 1:02d}"
        if not args.repeat_evidence:
            print("EVIDENCE TEXTS (IDs local to this page/bucket)")
            for evidence, identifier in evidence_ids.items():
                field(identifier, evidence)
        for index, unit in enumerate(units, 1):
            first = unit[0]["row"]
            identifier = (bucket.upper() if bucket != "global" else "GLOBAL") + f"-U{index:03d}"
            print("\n" + identifier + " | " + first["kind"] + " | " + evidence_ids[first["evidence"]])
            locations: dict[tuple[str, str, str, str], list[int]] = defaultdict(list)
            for record in unit:
                row = record["row"]
                alias = aliases[(row["layer"], row["file"])]
                locations[(alias, row["printed_page"], row["line"], row["statement"])].append(int(record["data_record"]))
            for (alias, page, line, statement), ids in locations.items():
                text = ",".join("D" + str(number) for number in ids) + " " + alias
                if bucket == "global":
                    text += " page=" + json.dumps(page, ensure_ascii=False)
                text += " line=" + json.dumps(line, ensure_ascii=False)
                if statement:
                    text += " statement=" + json.dumps(statement, ensure_ascii=False)
                print(text)
            field("OLD", first["old"])
            field("NEW", first["new"])
            if args.repeat_evidence:
                field("EVIDENCE " + evidence_ids[first["evidence"]], first["evidence"])
    assert sum(len(unit) for bucket in grouped.values() for unit in bucket.values()) == len(selected)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print("Compact worklist stopped: " + type(error).__name__ + ". Check the page selection and configured ledger.", file=sys.stderr)
        sys.exit(2)
