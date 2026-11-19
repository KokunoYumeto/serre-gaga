"""Audit final completion records without modifying sources or other records.

From the deliverable root:
    python scripts/final_completion_audit.py

The optional --root, --original and --context paths are configurable. By
default the external inputs are found beside the deliverable in input/.
Only integrity/COMPLETION_AUDIT.md and COMPLETION_AUDIT.tsv are written.
No TeX build, scan reading, mathematical test or archive creation is performed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True

ALLOWED_EVENTS = (
    "targeted proof check", "independent re-proof",
    "computation or formal certificate", "used and rechecked in this run",
    "carried as background without fault found", "refuted",
)
MINIMUM_NOTE_BASES = {f"N{number:03d}" for number in range(1, 96)}
OWN_OUTPUTS = {"integrity/COMPLETION_AUDIT.md", "integrity/COMPLETION_AUDIT.tsv"}
FINAL_LAYERS = (
    ("french-diplomatic", "after", 3),
    ("french-corrected", "after", 3),
    ("english", "before", 4),
)
ORIGINAL_LEDGERS = (
    ("SOURCE_CORRECTION_LEDGER.csv", "correction_id"),
    ("TRANSCRIPTION_REPAIR_LEDGER.csv", "repair_id"),
    ("PAGE_JOIN_LEDGER.csv", "join_id"),
    ("ENGLISH_TRANSLATION_LEDGER.csv", "translation_id"),
    ("UNCERTAIN_READING_LEDGER.csv", "reading_id"),
)
NOTE_PATTERN = re.compile(r"^### (N\d{3}[A-Z]?) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)", re.M | re.S)
IMAGE_TOKEN = re.compile(r"(?<![\w./-])(?:evidence/)?([A-Za-z0-9][A-Za-z0-9_.-]*\.(?:png|jpe?g|webp))\b", re.I)
ERROR_HEADING = re.compile(r"^(?:!|(?:\./)?[^\s:]+\.tex:\d+(?::\d+)?:)|(?:LaTeX|Package [^\n]+) Error:|Emergency stop|Fatal error occurred", re.M)


@dataclass
class Check:
    check_id: str
    status: str
    requirement: str
    result: str
    evidence: str


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def record_ids(value: str) -> list[int]:
    result = []
    for token in re.split(r"[,;]", value):
        token = token.strip()
        if not token or token.casefold() == "none":
            continue
        match = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", token)
        if not match:
            raise ValueError("Unrecognized review range.")
        first, last = int(match[1]), int(match[2] or match[1])
        if last < first:
            raise ValueError("Reversed review range.")
        result.extend(range(first, last + 1))
    return result


class Audit:
    def __init__(self, root: Path, original: Path, context: Path):
        self.root, self.original, self.context = root, original, context
        self.checks: list[Check] = []
        self.cache: dict[Path, bytes] = {}
        self.inputs: dict[Path, tuple[str, str]] = {}
        self.package = load_module("completion_packaging", root / "scripts/package_deliverable.py")
        self.build = load_module("completion_build", root / "scripts/build_audit.py")
        self.started = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.before = self.deliverable_snapshot()

    def safe(self, value: object) -> str:
        text = str(value)
        for _, pattern in self.package.PRIVATE_PATTERNS:
            text = pattern.sub("<local>", text)
        return text.replace("\t", " ").replace("\n", " ")

    def label(self, path: Path) -> str:
        for base, prefix in ((self.root, ""), (self.original, "original/"), (self.context, "context/")):
            try:
                return prefix + path.relative_to(base).as_posix()
            except ValueError:
                pass
        return "configured external input"

    def data(self, path: Path) -> bytes:
        if path not in self.cache:
            value = path.read_bytes()
            self.cache[path] = value
            self.inputs[path] = (self.label(path), hashlib.sha256(value).hexdigest())
        return self.cache[path]

    def text(self, name: str) -> str:
        return self.data(self.root / name).decode("utf-8-sig")

    def table(self, name: str, *, external: Path | None = None, delimiter: str = "\t") -> list[dict[str, str]]:
        path = external if external is not None else self.root / name
        return list(csv.DictReader(io.StringIO(self.data(path).decode("utf-8-sig"), newline=""), delimiter=delimiter))

    def add(self, ident: str, ok: bool, requirement: str, result: str, evidence: str = "", *, review: bool = False):
        self.checks.append(Check(ident, "PASS" if ok else "REVIEW" if review else "FAIL", requirement, self.safe(result), evidence))

    def run(self, name: str, function):
        try:
            function()
        except Exception as error:
            self.add(name + ".execution", False, "Complete this audit section", type(error).__name__ + "; inspect the section's required inputs. No source or other record was changed.")

    def deliverable_snapshot(self) -> dict[str, tuple[int, str]]:
        included, _ = self.package.gather(self.root)
        return {path.as_posix(): ((self.root / path).stat().st_size, digest(self.root / path)) for path in included if path.as_posix() not in OWN_OUTPUTS}

    def pages(self):
        progress = self.text("progress.log")
        done = re.findall(r"^page (\d+) done (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC)$", progress, re.M)
        sequence = [int(page) for page, _ in done]
        dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S UTC") for _, date in done]
        self.add("pages.progress", sequence == list(range(1, 43)) and dates == sorted(dates), "42 page completions in uninterrupted printed order", f"Recorded page sequence has {len(sequence)} entries; timestamps are nondecreasing={dates == sorted(dates)}.", "progress.log")
        document = self.text("CHECK_RECORD.md")
        blocks = list(re.finditer(r"^## Printed page (\d+)\n(.*?)(?=^## |\Z)", document, re.M | re.S))
        expected = list(range(1, 43))
        self.add("pages.sections", [int(item[1]) for item in blocks] == expected, "One check-record section for every printed page", f"Found {len(blocks)} page sections.", "CHECK_RECORD.md")
        french, english, scan, dated = [], [], [], []
        done_map = dict(done)
        for item in blocks:
            number, body = int(item[1]), item[2]
            if all(f"sources/{folder}/gaga_body.tex" in body for folder in ("french-diplomatic", "french-corrected")):
                french.append(number)
            entry = re.search(r"^- English comparison: (.+)$", body, re.M)
            if entry and ".tex" in entry[1] and not re.search(r"not (?:yet )?(?:checked|read)|pending", entry[1], re.I):
                english.append(number)
            if re.search(r"^- Scan: PDF page " + str(number + 1) + r"\b", body, re.M):
                scan.append(number)
            completion = re.search(r"^- Completed: ([^\n]+)", body, re.M)
            if completion and completion[1].rstrip(".") == done_map.get(str(number)):
                dated.append(number)
        self.add("pages.layers", french == expected and english == expected and scan == expected and dated == expected, "All 42 pages have both French comparisons, an English comparison, scan mapping and matching completion time", f"French pair={len(french)}; English={len(english)}; printed-to-scan mapping={len(scan)}; matching completion timestamps={len(dated)}.", "CHECK_RECORD.md; progress.log")
        page_map = self.table("FINAL_PAGE_MAP.tsv")
        actual = {(row["layer"], int(row["printed_page"])): row for row in page_map}
        valid = len(page_map) == len(actual) == 84
        for folder, layer in (("french-diplomatic", "as-printed"), ("french-corrected", "corrected")):
            filename = f"sources/{folder}/gaga_body.tex"
            lines = self.text(filename).splitlines()
            markers = [(int(match[1]), index + 1) for index, line in enumerate(lines) if (match := re.search(r"printed page (\d+)", line))]
            valid = valid and [number for number, _ in markers] == expected
            for index, (number, first) in enumerate(markers):
                last = markers[index + 1][1] - 1 if index + 1 < len(markers) else len(lines)
                row = actual.get((layer, number), {})
                valid = valid and row.get("file") == filename and row.get("first_source_line") == str(first) and row.get("last_source_line") == str(last) and row.get("scan_pdf_page") == str(number + 1)
        self.add("pages.source_map", valid, "84 exact French page-marker ranges", f"Final map contains {len(page_map)} rows; line ranges checked against current source bytes.", "FINAL_PAGE_MAP.tsv; sources/french-diplomatic/gaga_body.tex; sources/french-corrected/gaga_body.tex")
        self.add("pages.visual_record", "final PDF gate passed" in progress and len(self.text("PDF_CHECK.md")) > 500, "Final visual inspection has a primary-reader record", "Checks presence of the final gate and PDF report; it does not repeat or certify image reading.", "progress.log; PDF_CHECK.md")

    def ledger(self):
        rows = self.table("CORRECTIONS.tsv")
        retained = sum(row["old"] != row["new"] for row in rows)
        self.add("ledger.count", len(rows) == 2396 and retained == 2395, "2,396 correction records, with one explicitly withdrawn no-op", f"Records={len(rows)}; retained={retained}; no-op={len(rows) - retained}.", "CORRECTIONS.tsv")
        confidence = Counter(row["confidence"].split(";", 1)[0].strip().casefold() for row in rows)
        self.add("ledger.confidence", confidence == {"high": 2394, "medium": 2} and not any("pending" in row["confidence"].casefold() for row in rows), "All correction confidence dispositions are final", "; ".join(f"{key}={value}" for key, value in sorted(confidence.items())), "CORRECTIONS.tsv")
        reviews = self.table("SECOND_READING.tsv")
        covered = Counter()
        complete_metadata = True
        for row in reviews:
            identifiers = record_ids(row["ledger_rows"])
            covered.update(identifiers)
            if identifiers:
                complete_metadata = complete_metadata and bool(row["review"].strip()) and bool(row["utc"].strip())
        expected = set(range(1, len(rows) + 1))
        missing = expected - set(covered)
        extra = set(covered) - expected
        duplicates = [number for number, count in covered.items() if count != 1]
        self.add("ledger.second_reading", not missing and not extra and not duplicates and complete_metadata, "Each ledger data record occurs exactly once in the second-reading map", f"Review sessions={len(reviews)}; covered={len(covered)}; missing={len(missing)}; outside ledger={len(extra)}; repeated={len(duplicates)}.", "SECOND_READING.tsv; CORRECTIONS.tsv")

    def crosswalk(self):
        rows = self.table("INHERITED_RECORD_CROSSWALK.tsv")
        supplied = []
        control = self.context / "edition_records/terminal_package/05_EVIDENCE_CONTROLS"
        for filename, field in ORIGINAL_LEDGERS:
            supplied.extend(row[field] for row in self.table("", external=control / filename, delimiter=","))
        actual = [row["inherited_id"] for row in rows]
        complete = all(row["disposition"].strip() and row["basis_in_this_run"].strip() and row["utc"].strip() for row in rows)
        self.add("crosswalk.ids", len(rows) == len(set(actual)) == len(supplied) == len(set(supplied)) == 134 and set(actual) == set(supplied) and complete, "One disposition for each of the 134 supplied inherited record IDs", f"Crosswalk={len(rows)}; unique IDs={len(set(actual))}; supplied IDs={len(supplied)}; nonempty dispositions and bases={complete}.", "INHERITED_RECORD_CROSSWALK.tsv; context/edition_records/terminal_package/05_EVIDENCE_CONTROLS")

    def integrity(self):
        checks = self.table("integrity/checks.tsv")
        statuses = Counter(row["status"] for row in checks)
        self.add("integrity.classifications", statuses == {"PASS": 110, "REVIEW": 6}, "Preserve the existing 110 PASS / 6 REVIEW / 0 FAIL result", f"PASS={statuses['PASS']}; REVIEW={statuses['REVIEW']}; FAIL={statuses['FAIL']}. The six review classifications are not changed or automatically cleared.", "integrity/checks.tsv; integrity/REPORT.md")
        manual = self.data(self.root / "integrity/MANUAL_REVIEW.md")
        totals = {row["mechanical_metric"]: row["value"] for row in self.table("integrity/FINAL_TOTALS.tsv")}
        ledger_hash = hashlib.sha256(self.data(self.root / "CORRECTIONS.tsv")).hexdigest()
        manual_hash = hashlib.sha256(manual).hexdigest()
        self.add("integrity.snapshot", totals.get("CORRECTIONS_sha256") == ledger_hash and totals.get("MANUAL_REVIEW_sha256") == manual_hash and bool(manual.strip()), "The prior exact-replay certificate and manual rationale match the current ledger and manual file", "Ledger and manual-review hashes checked against FINAL_TOTALS.tsv; manual assessment remains the primary reader's responsibility.", "integrity/FINAL_TOTALS.tsv; integrity/MANUAL_REVIEW.md; CORRECTIONS.tsv")
        inventory = self.table("integrity/source_inventory.tsv")
        source_root = self.root / "sources"
        actual_files = {path.relative_to(source_root).as_posix() for path in source_root.rglob("*") if path.is_file() and path.suffix in {".tex", ".md"}}
        valid = len(inventory) == 14 and {row["relative_source"] for row in inventory} == actual_files
        for row in inventory:
            relative = row["relative_source"]
            current, original = self.data(source_root / relative), self.data(self.original / relative)
            valid = valid and len(current) == int(row["current_bytes"]) and len(original) == int(row["original_bytes"])
            valid = valid and hashlib.sha256(current).hexdigest() == row["current_sha256"] and hashlib.sha256(original).hexdigest() == row["original_sha256"]
        reconstruction = [row for row in checks if row["category"] == "ledger reconstruction"]
        self.add("integrity.sources", valid and len(reconstruction) == 14 and all(row["status"] == "PASS" for row in reconstruction), "The 14 original/current source hashes and exact reconstruction results remain current", f"Inventory rows={len(inventory)}; source files={len(actual_files)}; source reconstruction PASS rows={sum(row['status'] == 'PASS' for row in reconstruction)}.", "integrity/source_inventory.tsv; integrity/checks.tsv; sources")
        protected = [row for row in checks if row["category"] in {"README rights and credits", "Thomas Waring credit"}]
        readmes = all(self.data(source_root / filename) == self.data(self.original / filename) for filename in ("README.md", "README.fr.md"))
        self.add("integrity.credits", readmes and len(protected) == 4 and all(row["status"] == "PASS" for row in protected), "Both supplied READMEs and their rights/credits remain byte-identical, including Thomas Waring", f"README byte equality={readmes}; protected README/name checks={len(protected)}. Other protected front matter remains covered by the unchanged integrity classifications and manual rationale.", "sources/README.md; sources/README.fr.md; integrity/checks.tsv")
        replay = self.table("integrity/ledger_replay_rows.tsv")
        replay_ids = [int(row["ledger_row_including_header"]) for row in replay]
        replay_states = Counter(row["status"] for row in replay)
        empty_diff = not self.data(self.root / "integrity/unreconstructed_source_changes.diff")
        self.add("integrity.replay", sorted(replay_ids) == list(range(2, 2398)) and replay_states == {"applied": 2395, "recorded no-op": 1} and empty_diff, "All ledger rows are exactly reconstructed, with no unreconstructed source diff", f"Replay states={dict(replay_states)}; unreconstructed diff empty={empty_diff}.", "integrity/ledger_replay_rows.tsv; integrity/unreconstructed_source_changes.diff")

    def builds(self):
        for layer, stage, passes in FINAL_LAYERS:
            base = f"build/{stage}"
            rows = [row for row in self.table(base + "/passes.tsv") if row["layer"] == layer]
            valid = sorted(int(row["pass"]) for row in rows) == list(range(1, passes + 1))
            findings = []
            for row in rows:
                number = int(row["pass"])
                overfull = row.get("overfull_count", row.get("overfull_boxes", ""))
                clean = row["exit_status"] == row["errors"] == overfull == row["over_2pt"] == row["over_10pt"] == "0" and float(row["maximum_overfull_pt"]) == 0
                clean = clean and row.get("missing_glyph_diagnostics", "0") == "0" and row.get("pdf_created", "yes") == "yes"
                log = self.text(f"{base}/{layer}/pass-{number:02d}.log")
                self.text(f"{base}/{layer}/pass-{number:02d}.stdout.txt")
                clean = clean and not self.build.BOX.search(log) and not ERROR_HEADING.search(log) and "Missing character:" not in log
                valid = valid and clean
                if not clean:
                    findings.append(str(number))
            self.add("build.passes." + layer, valid, f"All {passes} accepted {layer} passes have no errors, missing glyphs or overfull boxes", f"Pass rows={len(rows)}; flagged passes={','.join(findings) or 'none'}. Every accepted pass log was inspected mechanically; underfull boxes and benign warnings are not silently reclassified as errors.", base + "/passes.tsv; " + base + "/" + layer)
            overflow = [row for row in self.table(base + "/overfull.tsv") if row["layer"] == layer]
            self.add("build.overfull_table." + layer, not overflow, "The accepted all-pass overflow table is empty for this layer", f"Overfull rows={len(overflow)}.", base + "/overfull.tsv")
            snapshot = self.table(base + "/source_snapshot.tsv")
            after_hashes = self.table(base + "/source_hashes_after_build.tsv")
            selected = [row for row in snapshot if row.get("relative_source", row.get("source_file", "")).startswith(layer + "/")]
            source_files = {path.relative_to(self.root / "sources").as_posix() for path in (self.root / "sources" / layer).rglob("*.tex")}
            hashed = {row["relative_source"]: row for row in after_hashes if row["relative_source"].startswith(layer + "/")}
            valid_hashes = {row.get("relative_source", row.get("source_file")) for row in selected} == source_files == set(hashed)
            for row in selected:
                filename = row.get("relative_source", row.get("source_file"))
                expected = row.get("snapshot_sha256", row.get("copied_sha256"))
                current = hashlib.sha256(self.data(self.root / "sources" / filename)).hexdigest()
                hashes = hashed.get(filename, {})
                valid_hashes = valid_hashes and current == expected == row.get("current_source_sha256", row.get("sha256"))
                valid_hashes = valid_hashes and all(hashes.get(field) == current for field in ("snapshot_sha256", "current_source_sha256", "isolated_source_sha256"))
            self.add("build.source_hashes." + layer, valid_hashes, "Current TeX sources match the verified isolated final-build snapshot", f"Current source files={len(source_files)}; manifest entries={len(selected)}; after-build entries={len(hashed)}.", base + "/source_snapshot.tsv; " + base + "/source_hashes_after_build.tsv")
            readers = [row for row in self.table(base + "/reader_pdfs.tsv") if row["layer"] == layer]
            valid_pdf = len(readers) == 1
            detail = "Reader manifest entry missing or duplicated."
            if valid_pdf:
                reader = readers[0]
                pdf = self.root / reader["relative_pdf"]
                valid_pdf = pdf.is_file() and pdf.stat().st_size == int(reader["bytes"]) and digest(pdf) == reader["sha256"] and reader["all_fonts_embedded"] == "yes"
                final_pass = next((row for row in rows if int(row["pass"]) == passes), {})
                valid_pdf = valid_pdf and reader["pdf_pages"] == final_pass.get("pdf_pages")
                detail = f"Reader={reader['relative_pdf']}; pages={reader['pdf_pages']}; bytes={reader['bytes']}; SHA-256={reader['sha256']}; recorded embedded fonts={reader['font_count']}."
            self.add("build.reader_pdf." + layer, valid_pdf, "Final reader PDF bytes match the previously inspected reader and font report", detail, base + "/reader_pdfs.tsv; pdf")
        delivered_pdfs = {path.relative_to(self.root).as_posix() for path in self.root.rglob("*.pdf")}
        intended = {"pdf/GAGA_french_diplomatic.pdf", "pdf/GAGA_french_corrected.pdf", "pdf/GAGA_English.pdf"}
        self.add("build.reader_set", delivered_pdfs == intended, "Only the three final reader PDFs are returned", f"PDF files under deliverable={len(delivered_pdfs)}.", "pdf")

    def notes(self):
        document = self.text("NOTES.md")
        parts = list(NOTE_PATTERN.finditer(document))
        identifiers = [match[1] for match in parts]
        expected_notes = set(identifiers)
        all_note_headings = re.findall(r"^### (N\S*)", document, re.M)
        bases = {ident for ident in identifiers if re.fullmatch(r"N\d{3}", ident)}
        highest = max((int(ident[1:]) for ident in bases), default=0)
        continuous_bases = bases == {f"N{number:03d}" for number in range(1, highest + 1)}
        suffixes = defaultdict(set)
        for ident in identifiers:
            if ident[-1:].isalpha():
                suffixes[ident[:-1]].add(ident[-1])
        valid_suffixes = all(base in bases and letters == {chr(number) for number in range(ord("A"), ord(max(letters)) + 1)} for base, letters in suffixes.items())
        valid_ids = len(identifiers) == len(expected_notes) and all_note_headings == identifiers and MINIMUM_NOTE_BASES <= bases and continuous_bases and valid_suffixes
        self.add("notes.ids", valid_ids, "Unique note headings with continuous base IDs and valid consecutive letter suffixes", f"Notes={len(identifiers)}; base IDs={len(bases)}; suffixed IDs={sum(len(letters) for letters in suffixes.values())}; duplicate or malformed IDs={not valid_ids}. The expected event/query set is derived from the current headings.", "NOTES.md")
        events = self.table("CHECK_EVENTS.tsv")
        bad_types = Counter(row["type"] for row in events if row["type"] not in ALLOWED_EVENTS)
        complete_events = all(row["statement_id"].strip() and row["who"].strip() and row["outcome"].strip() and re.fullmatch(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", row["date"]) for row in events)
        self.add("notes.event_schema", not bad_types and complete_events, "Every check event uses one of the six allowed types and complete metadata", f"Total events={len(events)}; invalid type count={sum(bad_types.values())}; complete event fields={complete_events}.", "CHECK_EVENTS.tsv")
        note_events = defaultdict(list)
        for row in events:
            if row["statement_id"].startswith("GAGA-NOTE:"):
                note_events[row["statement_id"][len("GAGA-NOTE:"):]].append(row)
        queries = {}
        metadata_bad, event_bad, placement_bad = [], [], []
        for match in parts:
            ident, title, body = match.groups()
            metadata = all(len(re.findall(r"\*\*" + label + r":\*\*", body)) == 1 for label in ("Place", "Kind", "Confidence", "Event", "Context search", "Relation"))
            query = re.search(r"\*\*Context search:\*\* `([^`]+)`", body)
            confidence = re.search(r"\*\*Confidence:\*\* (.+?)(?:\*\*Event:|\n\n)", body, re.S)
            event = re.search(r"\*\*Event:\*\* ([^\n]+)", body)
            kind = next((value for value in ALLOWED_EVENTS if event and event[1].startswith(value)), None)
            if not metadata or not query or not confidence or kind is None:
                metadata_bad.append(ident)
                continue
            queries[ident] = query[1]
            expected = self.safe(f"NOTES.md {ident}: {title}. Scope and dependencies are those explicitly stated in the note. Confidence: " + confidence[1].strip())
            associated = note_events[ident]
            if len(associated) != 1 or associated[0]["type"] != kind or associated[0]["outcome"] != expected:
                event_bad.append(ident)
            preceding = re.findall(r"^## ([^\n]+)", document[:match.start()], re.M)
            section = preceding[-1] if preceding else ""
            own_idea = bool(re.search(r"\*\*Kind:\*\* own\b", body))
            if own_idea != ("Ideas proposed in this run" in section):
                placement_bad.append(ident)
        self.add("notes.metadata", not metadata_bad, "Every note has confidence, allowed event type and context-query metadata", "Malformed note IDs=" + (", ".join(metadata_bad) or "none") + ".", "NOTES.md")
        self.add("notes.events", set(note_events) == expected_notes and not event_bad and all(len(rows) == 1 for rows in note_events.values()), "One current, matching check event per note", "Mismatched note IDs=" + (", ".join(event_bad) or "none") + ".", "NOTES.md; CHECK_EVENTS.tsv")
        self.add("notes.sections", not placement_bad, "The own-idea section contains the notes explicitly labelled as own proposals", "Placement mismatches=" + (", ".join(placement_bad) or "none") + ". This limited label check is not a semantic review of every section heading.", "NOTES.md")
        search = self.table("NOTE_CONTEXT_SEARCH.tsv")
        by_note = defaultdict(list)
        for row in search:
            by_note[row["note_id"]].append(row)
        recorded_valid = set(by_note) == expected_notes and len({(row["note_id"], row["context_file"]) for row in search}) == len(search)
        for ident, rows in by_note.items():
            recorded_valid = recorded_valid and all(row["regex_query"] == queries.get(ident) for row in rows)
            for row in rows:
                filename = row["context_file"]
                recorded_valid = recorded_valid and (filename == "NO MATCH" and row["matching_lines"] == "0" or filename != "NO MATCH" and not Path(filename).is_absolute() and ".." not in Path(filename).parts and (self.context / filename).is_file() and int(row["matching_lines"]) > 0)
        self.add("notes.query_coverage", recorded_valid, "Each note's exact query has a unique file-level search record", f"Query-covered notes={len(by_note)}; file-level rows={len(search)}.", "NOTES.md; NOTE_CONTEXT_SEARCH.tsv")
        def replay(item):
            ident, query = item
            process = subprocess.run(["rg", "--json", "--text", "-i", "-e", query, str(self.context)], capture_output=True, text=True)
            if process.returncode not in (0, 1):
                return ident
            hits = []
            import json
            for line in process.stdout.splitlines():
                entry = json.loads(line)
                if entry["type"] != "match":
                    continue
                data = entry["data"]
                filename = Path(data["path"]["text"]).relative_to(self.context).as_posix()
                source = data["lines"]["text"]
                offset = data["submatches"][0]["start"] if data["submatches"] else 0
                character = len(source.encode()[:offset].decode(errors="ignore"))
                excerpt = self.safe(source[max(0, character - 70):character + 240].strip())
                hits.append((filename, data["line_number"], excerpt))
            actual = {row["context_file"]: row for row in by_note[ident]}
            if not hits:
                return None if set(actual) == {"NO MATCH"} else ident
            counts = Counter(hit[0] for hit in hits)
            if set(actual) != set(counts):
                return ident
            for filename, count in counts.items():
                first = next(hit for hit in hits if hit[0] == filename)
                row = actual[filename]
                if int(row["matching_lines"]) != count or int(row["example_line"]) != first[1] or row["example_excerpt"] != first[2]:
                    return ident
            return None
        with ThreadPoolExecutor(max_workers=4) as pool:
            mismatched = [ident for ident in pool.map(replay, queries.items()) if ident]
        self.add("notes.query_replay", len(queries) == len(expected_notes) and not mismatched, "Recorded context-search file sets, counts and examples reproduce exactly", "Replayed queries=" + str(len(queries)) + "; mismatches=" + (", ".join(mismatched) or "none") + ". Literal matches do not independently prove the note's claim or relation.", "NOTE_CONTEXT_SEARCH.tsv; configured context input")
        decisions = self.table("", external=self.context / "stacks/gaga_r3/dec.csv", delimiter=",")
        expected_decisions = {row["decision_id"] for row in decisions}
        prefix = "CONTEXT:GAGA-R3:"
        mapped = [row for row in events if row["statement_id"].startswith(prefix)]
        counts = Counter(row["statement_id"][len(prefix):] for row in mapped)
        background = Counter(row["statement_id"][len(prefix):] for row in mapped if row["type"] == "carried as background without fault found")
        valid_mapping = set(counts) == expected_decisions and set(background) == expected_decisions and all(count == 1 for count in background.values())
        self.add("notes.mapping_events", valid_mapping, "Each supplied mapping decision has one background record, with separately typed follow-up checks permitted", f"Mapping decisions={len(expected_decisions)}; background records={sum(background.values())}; separately typed follow-up checks={len(mapped) - sum(background.values())}.", "CHECK_EVENTS.tsv; context/stacks/gaga_r3/dec.csv")
        readme = self.text("README.md")
        self.add("notes.readme", len(readme) > 500 and "Work in progress." not in readme, "The root README is a completion guide rather than the initial placeholder", f"README UTF-8 characters={len(readme)}; original source READMEs are audited separately.", "README.md")

    def evidence(self):
        references = defaultdict(set)
        for filename in ("CORRECTIONS.tsv", "SECOND_READING.tsv", "INHERITED_VERDICTS.tsv"):
            for number, row in enumerate(self.table(filename), 1):
                for match in IMAGE_TOKEN.finditer(row.get("evidence", "")):
                    references[match[1]].add(filename + ":data-record-" + str(number))
        for filename in ("CHECK_RECORD.md", "PDF_CHECK.md", "RECURRENCE_CHECK.md", "NOTES.md", "README.md"):
            for match in re.finditer(r"\bevidence/([A-Za-z0-9][A-Za-z0-9_.-]*\.(?:png|jpe?g|webp))\b", self.text(filename), re.I):
                references[match[1]].add(filename)
        missing = [filename for filename in sorted(references) if not (self.root / "evidence" / filename).is_file()]
        images = [path for path in (self.root / "evidence").rglob("*") if path.is_file()]
        self.add("evidence.paths", not missing, "Every explicit returned evidence-image filename resolves in evidence/", f"Referenced image filenames={len(references)}; evidence files={len(images)}; missing=" + (", ".join(missing) or "none") + ". Bare filenames in evidence fields are resolved beneath evidence/. Images are not opened or judged.", "CORRECTIONS.tsv; SECOND_READING.tsv; INHERITED_VERDICTS.tsv; evidence")

    def claim_coverage(self):
        document = self.text("scripts/NOTE_COVERAGE.md")
        expression = re.search(r"```regex\n([^\n]+)\n```", document)
        recorded_hash = re.search(r"Source snapshot:.*?SHA-256 `([0-9a-f]{64})`", document)
        if not expression or not recorded_hash:
            raise ValueError("Coverage method lacks its exact expression or source hash.")
        filename = "sources/french-corrected/gaga_body.tex"
        source = self.text(filename)
        source_hash = hashlib.sha256(self.data(self.root / filename)).hexdigest()
        pattern = re.compile(expression[1], re.I)
        lexical, page_by_line = {}, {}
        page = ""
        lines = source.splitlines()
        for number, line in enumerate(lines, 1):
            marker = re.search(r"printed page (\d+)", line)
            if marker:
                page = marker[1]
            page_by_line[number] = page
            if line.lstrip().startswith("%"):
                continue
            count = len(pattern.findall(line))
            if count:
                lexical[number] = count
        rows = self.table("NOTE_CLAIM_COVERAGE.tsv")
        declared_notes = {match[1] for match in NOTE_PATTERN.finditer(self.text("NOTES.md"))}
        recorded_lexical = {int(row["source_line"]): int(row["lexical_occurrences"]) for row in rows if row["lead_kind"] == "lexical_marker"}
        additional = {int(row["source_line"]) for row in rows if row["lead_kind"] == "additional_prose"}
        statuses = Counter(row["coverage_status"] for row in rows)
        valid_links = True
        for row in rows:
            number = int(row["source_line"])
            links = [token.strip() for token in re.split(r"[,;]", row["note_ids"]) if token.strip()]
            valid_links = valid_links and bool(links) and len(links) == len(set(links)) and set(links) <= declared_notes
            valid_links = valid_links and row["source_file"] == filename and 1 <= number <= len(lines) and row["printed_page"] == page_by_line.get(number) and bool(row["coverage_focus"].strip())
            if row["lead_kind"] == "additional_prose":
                valid_links = valid_links and row["lexical_occurrences"] == "0" and number not in lexical
        valid = recorded_hash[1] == source_hash and len(rows) == len({row['source_line'] for row in rows}) == 65
        valid = valid and recorded_lexical == lexical and len(lexical) == 59 and sum(lexical.values()) == 70
        valid = valid and additional == {810, 880, 971, 973, 975, 1084} and statuses == {"addressed": 63, "introductory_nonproof": 2} and valid_links
        self.add("notes.claim_coverage", valid, "The claim-coverage table matches its source hash, exact documented regex, declared counts and current note IDs", f"Rows={len(rows)}; lexical marker lines={len(lexical)}; trigger occurrences={sum(lexical.values())}; additional prose lines={len(additional)}; addressed={statuses['addressed']}; introductory nonproof={statuses['introductory_nonproof']}; valid note/source links={valid_links}; source hash matches={recorded_hash[1] == source_hash}. Editorial mappings are checked for traceability, not independently certified as complete proof coverage.", "NOTE_CLAIM_COVERAGE.tsv; scripts/NOTE_COVERAGE.md; NOTES.md; " + filename)

    def report(self):
        output = self.root / "integrity"
        output.mkdir(parents=True, exist_ok=True)
        with (output / "COMPLETION_AUDIT.tsv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
            writer.writerow(["check_id", "status", "requirement", "result", "evidence"])
            writer.writerows((row.check_id, row.status, row.requirement, row.result, row.evidence) for row in self.checks)
        counts = Counter(row.status for row in self.checks)
        text = ["# Final completion audit\n\n", "Generated " + self.started + ".\n\n", f"**PASS: {counts['PASS']}; REVIEW: {counts['REVIEW']}; FAIL: {counts['FAIL']}.**\n\n", "This is a mechanical completion and snapshot audit. It checks recorded coverage, exact IDs and hashes, prior reconstruction evidence, accepted pass logs, note metadata, context-search reproduction, evidence filenames and packaging privacy preflight. It does not read scans, inspect images again, redo mathematical arguments, rebuild TeX or create an archive. Sources, ledgers, notes, events, READMEs and existing integrity classifications are read only.\n\n", "The final accepted build consists of the two French three-pass sequences in `build/after` and the English four-pass sequence in `build/before`. The earlier French baseline is not confused with the final French reader files.\n\n", "The existing source-integrity result remains **110 PASS / 6 REVIEW / 0 FAIL** when its check below passes. Those six review classifications retain the primary reader's rationale in `integrity/MANUAL_REVIEW.md`; this completion audit does not turn them into automatic passes.\n\n", "## Results\n\n| Check | Status | Result |\n|---|---|---|\n"]
        for row in self.checks:
            text.append("| `" + row.check_id + "` | " + row.status + " | " + row.result.replace("|", "\\|") + " |\n")
        text.append("\nThe companion TSV gives each requirement and its relative evidence locators. A clean result applies only to the audited snapshot. Rerun after any later source, ledger, note, event, README or other deliverable change.\n\n")
        text.append("## Core snapshot hashes\n\n| Relative file | SHA-256 |\n|---|---|\n")
        selected = {"CORRECTIONS.tsv", "SECOND_READING.tsv", "CHECK_RECORD.md", "CHECK_EVENTS.tsv", "NOTES.md", "NOTE_CONTEXT_SEARCH.tsv", "NOTE_CLAIM_COVERAGE.tsv", "scripts/NOTE_COVERAGE.md", "README.md", "INHERITED_RECORD_CROSSWALK.tsv", "integrity/MANUAL_REVIEW.md", "scripts/final_completion_audit.py"}
        for filename, (_, value) in sorted(self.before.items()):
            if filename in selected or filename.startswith("pdf/"):
                text.append("| `" + filename + "` | `" + value + "` |\n")
        combined = hashlib.sha256("".join(filename + "\t" + str(size) + "\t" + value + "\n" for filename, (size, value) in sorted(self.before.items())).encode()).hexdigest()
        text.append("\nAggregate SHA-256 of the included-file names, sizes and SHA-256 values, excluding only this audit's two self-referential outputs: `" + combined + "`.\n\n")
        text.append("## Packaging boundary\n\nThe package preflight creates no ZIP. The final packager must still enforce its strict compressed-size limit, complete member inventory, SHA-256 manifest and CRC verification when the final archive is actually created. Binary PDF and image content is outside the returned-text privacy scanner; existing PDF metadata/font reports and the primary reader's visual record remain the evidence for those artifacts.\n")
        (output / "COMPLETION_AUDIT.md").write_text("".join(text), encoding="utf-8")

    def finish(self):
        # Write provisional audit outputs so the actual packaging preflight can
        # include these deliverables in its ordinary text/privacy scan.
        self.report()
        prospective = self.root.parent / "work" / "completion-preflight"
        process = subprocess.run([sys.executable, "-B", "scripts/package_deliverable.py", "--root", ".", "--output-dir", str(prospective), "--kind", "final", "--preflight"], cwd=self.root, capture_output=True, text=True)
        message = self.safe((process.stdout + process.stderr).strip())
        self.add("package.preflight", process.returncode == 0, "The actual final-package privacy preflight succeeds without creating an archive", "Exit=" + str(process.returncode) + "; " + message, "scripts/package_deliverable.py --kind final --preflight")
        after = self.deliverable_snapshot()
        changed = sorted(filename for filename in set(self.before) | set(after) if self.before.get(filename) != after.get(filename))
        external_changed = [label for path, (label, value) in self.inputs.items() if not path.is_file() or digest(path) != value]
        self.add("snapshot.stability", not changed and not external_changed, "All audited deliverables and directly read external inputs remain unchanged during this run", f"Included deliverables checked={len(self.before)}; changed deliverables=" + (", ".join(changed) or "none") + "; changed direct inputs=" + (", ".join(external_changed) or "none") + ". The two completion-audit output files are excluded from their own snapshot.")
        self.report()
        findings = self.package.privacy_findings(self.root, [Path(name) for name in sorted(OWN_OUTPUTS)])
        self.add("package.audit_output_privacy", not findings, "The final rewritten completion reports contain no detected local paths or email addresses", "Findings=" + str(len(findings)) + ".", "integrity/COMPLETION_AUDIT.md; integrity/COMPLETION_AUDIT.tsv")
        self.report()
        counts = Counter(row.status for row in self.checks)
        print(f"Completion audit: PASS={counts['PASS']}, REVIEW={counts['REVIEW']}, FAIL={counts['FAIL']}")
        for row in self.checks:
            if row.status != "PASS":
                print(row.status + " " + row.check_id + ": " + row.result)
        print("Wrote only integrity/COMPLETION_AUDIT.md and integrity/COMPLETION_AUDIT.tsv. No archive created.")
        return 2 if counts["FAIL"] else 1 if counts["REVIEW"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--original", type=Path, help="Original extracted GAGA_sources directory.")
    parser.add_argument("--context", type=Path, help="Supplied GAGA_context directory.")
    args = parser.parse_args()
    root = args.root.resolve()
    original = args.original.resolve() if args.original else root.parent / "input/GAGA_sources"
    context = args.context.resolve() if args.context else root.parent / "input/GAGA_context"
    audit = Audit(root, original, context)
    for name in ("pages", "ledger", "crosswalk", "integrity", "builds", "notes", "claim_coverage", "evidence"):
        audit.run(name, getattr(audit, name))
    return audit.finish()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, csv.Error) as error:
        print("Completion audit stopped: " + type(error).__name__ + ". Check the configured paths and required inputs; no archive was created.", file=sys.stderr)
        raise SystemExit(2)
