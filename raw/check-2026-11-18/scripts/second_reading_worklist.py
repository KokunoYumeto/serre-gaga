"""Generate complete, unjudged correction worklists in scratch.

From the deliverable root:
    python scripts/second_reading_worklist.py --root . --output ../work/second_reading

Grouping is confined to each printed-page/global bucket and requires exact
equality of old, new, evidence and kind, including whitespace. Every original
logical TSV row, file, layer and line remains listed. No verdict is assigned.
The script reads ledger text and evidence filenames/stat metadata only; it does
not open images or alter sources, ledgers, page records or notes.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path
import re
import sys


REQUIRED = ("file", "layer", "printed_page", "line", "statement", "old", "new", "evidence", "kind", "confidence")
GROUP_FIELDS = ("old", "new", "evidence", "kind")
MAIN_FILES = {
    "french-diplomatic/gaga.tex", "french-corrected/gaga.tex",
    "english/GAGA_English_source_aligned.tex",
}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".gif", ".bmp", ".svg", ".avif", ".heic", ".jp2", ".ppm", ".pgm", ".pbm"}
IMAGE_REFERENCE = re.compile(r"(?<![\w./-])(?:[\w.-]+[/\\])*[\w.-]+\.(?:png|jpe?g|tiff?|webp|gif|bmp|svg|avif|heic|jp2|ppm|pgm|pbm)(?![\w-]|\.[\w-])", re.IGNORECASE)
FILENAME_PAGE = re.compile(r"(?:^|[-_])(?:p|page[-_]?)0*(\d{1,2})(?=[-_ .]|$)", re.IGNORECASE)


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def routing(row: dict[str, str]) -> tuple[str, str]:
    filename = row["file"].replace(chr(92), "/").removeprefix("sources/")
    raw_page = row["printed_page"].strip()
    if filename in MAIN_FILES:
        return "global", "main-file/preamble row"
    if row["layer"].strip().casefold() == "build":
        return "global", "build/global row"
    if row["line"].strip().casefold() in {"preamble", "global", "all pages", "whole file", "whole document", "shared preamble"}:
        return "global", "explicit preamble/global line field"
    is_page_source = filename in {"french-diplomatic/gaga_body.tex", "french-corrected/gaga_body.tex"} or filename.startswith("english/components/") and filename.endswith(".tex")
    if not is_page_source:
        return "global", "non-page source or metadata file"
    if not raw_page.isdecimal():
        return "global", "page range, global label or unspecified page"
    page = int(raw_page)
    if not 1 <= page <= 42:
        return "global", "numeric page outside printed pages 1–42"
    return f"p{page:02d}", "single printed page"


def read_ledger(data: bytes) -> tuple[list[str], list[dict[str, object]]]:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter="\t")
    fields = list(reader.fieldnames or [])
    missing = set(REQUIRED) - set(fields)
    if missing:
        raise ValueError("Missing required correction columns: " + ", ".join(sorted(missing)))
    records: list[dict[str, object]] = []
    previous_end = reader.line_num
    for index, row in enumerate(reader, 1):
        if None in row or any(row.get(field) is None for field in fields):
            raise ValueError("Malformed TSV record " + str(index) + ".")
        bucket, reason = routing(row)
        records.append({
            "data_record": index,
            "ledger_row": index + 1,
            "physical_start": previous_end + 1,
            "physical_end": reader.line_num,
            "bucket": bucket,
            "routing_reason": reason,
            "row": row,
        })
        previous_end = reader.line_num
    return fields, records


def image_inventory(root: Path) -> list[dict[str, object]]:
    folder = root / "evidence"
    result: list[dict[str, object]] = []
    if not folder.is_dir():
        return result
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        pages = sorted({int(match.group(1)) for match in FILENAME_PAGE.finditer(path.name) if 1 <= int(match.group(1)) <= 42})
        result.append({"path": path.relative_to(root).as_posix(), "name": path.name, "bytes": path.stat().st_size, "pages": pages})
    return result


def references(evidence: str, images: list[dict[str, object]]) -> list[dict[str, object]]:
    by_path = {image["path"]: image for image in images}
    by_name: dict[str, list[str]] = defaultdict(list)
    for image in images:
        by_name[str(image["name"])].append(str(image["path"]))
    result: list[dict[str, object]] = []
    seen: set[str] = set()
    for match in IMAGE_REFERENCE.finditer(evidence):
        token = match.group().replace(chr(92), "/").removeprefix("./")
        if token in seen:
            continue
        seen.add(token)
        if token in by_path:
            paths, status = [token], "present"
        else:
            paths = by_name.get(Path(token).name, [])
            status = "present by unique basename" if len(paths) == 1 else "ambiguous basename" if paths else "not found in evidence inventory"
        result.append({"reference": token, "paths": paths, "status": status})
    return result


def md_cell(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def fenced(value: str, language: str) -> str:
    longest = max((len(match.group()) for match in re.finditer(r"`+", value)), default=0)
    fence = "`" * max(3, longest + 1)
    return fence + language + "\n" + value + ("" if value.endswith("\n") else "\n") + fence + "\n"


def tsv(path: Path, fields: list[str], rows: list[list[object]]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(fields)
    writer.writerows(rows)
    path.write_text(stream.getvalue(), encoding="utf-8")


def unit_markdown(unit: dict[str, object]) -> str:
    rows = unit["records"]
    first = rows[0]["row"]
    row_numbers = ", ".join(str(record["ledger_row"]) for record in rows)
    output = ["## " + str(unit["id"]) + " — ledger rows " + row_numbers + "\n\n"]
    output.append("Kind: **" + md_cell(first["kind"]) + "**. Grouping is exact field equality, not a judgment that the occurrences are interchangeable.\n\n")
    output.append("| Ledger row (header = 1) | Data record | Physical TSV lines | Layer | File | Printed-page field | Printed-line field | Statement | Existing confidence | Routing |\n")
    output.append("|---|---|---|---|---|---|---|---|---|---|\n")
    for record in rows:
        row = record["row"]
        physical = str(record["physical_start"]) + "–" + str(record["physical_end"])
        values = [record["ledger_row"], record["data_record"], physical, row["layer"], row["file"], row["printed_page"], row["line"], row["statement"], row["confidence"], record["routing_reason"]]
        output.append("| " + " | ".join(md_cell(value) for value in values) + " |\n")
    output.append("\n### Old — complete field\n\n" + fenced(first["old"], "tex") + "\n")
    output.append("### New — complete field\n\n" + fenced(first["new"], "tex") + "\n")
    output.append("### Evidence — complete field\n\n" + fenced(first["evidence"], "text") + "\n")
    output.append("### Referenced evidence image filenames\n\n")
    if unit["references"]:
        for reference in unit["references"]:
            resolved = "; ".join("`" + str(path) + "`" for path in reference["paths"])
            output.append("- `" + str(reference["reference"]) + "`: " + str(reference["status"]) + ("; inventory path(s): " + resolved if resolved else "") + ".\n")
    else:
        output.append("No image filename is explicitly named in this evidence field. The per-page inventory below is only a filename inventory and does not assert correspondence to this unit.\n")
    output.append("\nNo second-reading verdict has been assigned by this generator. Every listed occurrence still requires the primary reader's assessment.\n\n")
    return "".join(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve() if args.output else root.parent / "work" / "second_reading"
    if output == root or root in output.parents:
        raise ValueError("Worklists must be outside the deliverable root.")
    ledger_path = root / "CORRECTIONS.tsv"
    data = ledger_path.read_bytes()
    source_hash = hashlib.sha256(data).hexdigest()
    generated = stamp()
    fields, records = read_ledger(data)
    images = image_inventory(root)
    buckets = [f"p{page:02d}" for page in range(1, 43)] + ["global"]
    groups: dict[str, dict[tuple[str, ...], dict[str, object]]] = {bucket: {} for bucket in buckets}
    all_units: list[dict[str, object]] = []
    for record in records:
        bucket = str(record["bucket"])
        row = record["row"]
        key = tuple(row[field] for field in GROUP_FIELDS)
        if key not in groups[bucket]:
            identifier = (bucket.upper() if bucket != "global" else "GLOBAL") + "-U" + f"{len(groups[bucket]) + 1:03d}"
            unit = {"id": identifier, "bucket": bucket, "records": [], "references": references(row["evidence"], images)}
            groups[bucket][key] = unit
            all_units.append(unit)
        unit = groups[bucket][key]
        unit["records"].append(record)
        record["unit"] = unit["id"]
    assert sum(len(unit["records"]) for unit in all_units) == len(records)
    assert sorted(record["ledger_row"] for unit in all_units for record in unit["records"]) == list(range(2, len(records) + 2))
    referenced_by: dict[str, list[str]] = defaultdict(list)
    for unit in all_units:
        for reference in unit["references"]:
            for path in reference["paths"]:
                referenced_by[str(path)].append(str(unit["id"]))
    output.mkdir(parents=True, exist_ok=True)
    snapshot_note = "Generated " + generated + " from `CORRECTIONS.tsv`, SHA-256 `" + source_hash + "`. This is an unjudged worklist snapshot. Regeneration replaces generated files; record verdicts in the editorial ledger, not in these generated lists.\n\n"
    index = ["# Correction second-reading worklists\n\n", snapshot_note]
    index.append("Ledger records: **" + str(len(records)) + "**; displayed units: **" + str(len(all_units)) + "**. Every original record appears exactly once in a page or global worklist. Grouping requires identical old/new/evidence/kind strings, including whitespace, within the same routing bucket.\n\n")
    index.append("A ledger-row number counts the header as row 1. A data-record number starts at 1 after the header. Physical TSV line spans are also supplied because quoted multiline fields occupy several physical lines. Old/new/evidence fields are shown in full; the manifests retain their exact TSV values.\n\n")
    index.append("| Worklist | Ledger records | Displayed units | Evidence files assigned by filename |\n|---|---|---|---|\n")
    for bucket in buckets:
        units = list(groups[bucket].values())
        count = sum(len(unit["records"]) for unit in units)
        if bucket == "global":
            filename, title = "global_and_preamble.md", "Preamble, global, page-range and other non-page rows"
            page_images = [image for image in images if not image["pages"]]
        else:
            page = int(bucket[1:])
            filename, title = f"page_{page:02d}.md", "Printed page " + str(page) + " (scan PDF page " + str(page + 1) + ")"
            page_images = [image for image in images if page in image["pages"]]
        index.append("| [" + title + "](" + filename + ") | " + str(count) + " | " + str(len(units)) + " | " + str(len(page_images)) + " |\n")
        page_text = ["# " + title + "\n\n", snapshot_note, "Ledger records: **" + str(count) + "**; displayed units: **" + str(len(units)) + "**.\n\n"]
        if units:
            page_text.extend(unit_markdown(unit) for unit in units)
        else:
            page_text.append("No correction rows are routed to this worklist. This statement concerns ledger inventory only.\n\n")
        page_text.append("## Evidence-file inventory\n\nFilename-based page assignment only; no image has been opened or assessed by this generator. An unreferenced file may still be needed for a row whose evidence field names no image.\n\n")
        if page_images:
            page_text.append("| Relative evidence filename | Bytes at inventory time | Units explicitly referencing it |\n|---|---|---|\n")
            for image in page_images:
                page_text.append("| " + md_cell(image["path"]) + " | " + str(image["bytes"]) + " | " + md_cell(", ".join(sorted(set(referenced_by[str(image["path"])]))) or "None explicitly") + " |\n")
        else:
            page_text.append("No evidence-image filename was assigned to this page/bucket by the filename rule.\n")
        (output / filename).write_text("".join(page_text), encoding="utf-8")
    index.append("\n## Machine-readable manifests\n\n- `row_manifest.tsv`: every original row and field, with logical and physical locations, routing reason and displayed unit.\n- `unit_manifest.tsv`: exact grouped fields, every member row number, and explicit evidence-image references.\n- `evidence_manifest.tsv`: evidence filenames, sizes, filename-inferred pages and referencing units; image contents are never read.\n")
    row_fields = ["ledger_row_header_is_1", "data_record", "physical_start_line", "physical_end_line", "bucket", "unit", "routing_reason", *fields]
    tsv(output / "row_manifest.tsv", row_fields, [[record["ledger_row"], record["data_record"], record["physical_start"], record["physical_end"], record["bucket"], record["unit"], record["routing_reason"], *[record["row"][field] for field in fields]] for record in records])
    tsv(output / "unit_manifest.tsv", ["unit", "bucket", "record_count", "ledger_rows_header_is_1", *GROUP_FIELDS, "explicit_image_references", "resolved_evidence_paths", "reference_statuses"], [[unit["id"], unit["bucket"], len(unit["records"]), ",".join(str(record["ledger_row"]) for record in unit["records"]), *[unit["records"][0]["row"][field] for field in GROUP_FIELDS], "; ".join(str(reference["reference"]) for reference in unit["references"]), "; ".join(sorted({str(path) for reference in unit["references"] for path in reference["paths"]})), "; ".join(str(reference["reference"]) + ": " + str(reference["status"]) for reference in unit["references"]) ] for unit in all_units])
    tsv(output / "evidence_manifest.tsv", ["relative_evidence_path", "bytes", "filename_inferred_printed_pages", "explicitly_referencing_units"], [[image["path"], image["bytes"], ",".join(map(str, image["pages"])), ",".join(sorted(set(referenced_by[str(image["path"])])))] for image in images])
    changed = hashlib.sha256(ledger_path.read_bytes()).hexdigest() != source_hash
    if changed:
        index.append("\n**Ledger changed during generation.** These files describe the initial snapshot hash above. Regenerate before beginning the second reading.\n")
    (output / "INDEX.md").write_text("".join(index), encoding="utf-8")
    print("Generated 42 page worklists, one separate global/preamble worklist, an index and three manifests.")
    print("Ledger records=" + str(len(records)) + "; exact-field groups=" + str(len(all_units)) + "; evidence filenames=" + str(len(images)) + ".")
    print("Ledger SHA-256=" + source_hash)
    print("No verdicts assigned. No sources, ledgers, page records, notes or images modified.")
    if changed:
        print("The ledger changed during generation; regenerate from the latest snapshot.")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print("Worklist generation stopped: " + type(error).__name__ + ". Check the configured scratch destination and ledger columns.", file=sys.stderr)
        sys.exit(2)
