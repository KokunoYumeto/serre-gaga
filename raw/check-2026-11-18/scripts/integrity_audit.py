"""Mechanically audit source identity, protected credits and ledger coverage.

Run from the deliverable root after the sequential reading and second pass:
    python scripts/integrity_audit.py --original ../input/GAGA_sources --root .

No source or editorial record is changed. Reports go to the configurable
--output directory (default: integrity beneath the deliverable root).

An exact ledger reconstruction is a textual certificate: every reconstructed
byte comes from the supplied original or a recorded old/new substitution. The
final source is used only to disambiguate possible substitution positions; it
never supplies replacement text. This does not verify a scan reading, a reason
for emendation, a translation, or mathematical correctness.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import difflib
import hashlib
import io
from pathlib import Path
import re
import sys


sys.dont_write_bytecode = True
PAGE = re.compile(r"^.*%.*printed page\s+(\d+)[^\n]*$", re.MULTILINE)
CREDIT = re.compile(r"Jean-Pierre|Thomas\s+Waring|Waring|OpenAI|Codex|GPT[- ]?\d|NUMDAM|Numdam|copyright|rights|licen[cs]e|droits", re.IGNORECASE)
REQUIRED_COLUMNS = ("file", "layer", "printed_page", "line", "statement", "old", "new", "evidence", "kind", "confidence")
KINDS = {"reading", "misprint of the original", "translation", "typesetting", "structure"}
LAYERS = {"as-printed", "corrected", "English", "build"}
ANCHORS = {"label": 1, "hypertarget": 1, "GAGATarget": 1, "GAGASection": 2, "GAGASubsection": 2, "pdfbookmark": 2}
GENERATED_ENDINGS = (".aux", ".log", ".pdf", ".out", ".toc", ".fls", ".fdb_latexmk", ".xdv", ".dvi", ".synctex.gz")


@dataclass
class Check:
    category: str
    item: str
    status: str
    detail: str


def sha(text: str | bytes) -> str:
    return hashlib.sha256(text.encode("utf-8") if isinstance(text, str) else text).hexdigest()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def save_tsv(path: Path, header: tuple[str, ...], rows: list[tuple[object, ...]]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    path.write_text(stream.getvalue(), encoding="utf-8")


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def page_ranges(text: str) -> dict[int, tuple[int, int]]:
    matches = list(PAGE.finditer(text))
    return {int(m.group(1)): (m.start(), matches[i + 1].start() if i + 1 < len(matches) else len(text)) for i, m in enumerate(matches)}


def scope(text: str, filename: str, printed_page: str) -> tuple[int, int]:
    if filename.endswith("/gaga_body.tex") and printed_page.isdecimal():
        ranges = page_ranges(text)
        number = int(printed_page)
        if number not in ranges:
            raise ValueError("The declared printed-page marker is missing.")
        return ranges[number]
    return 0, len(text)


def occurrences(text: str, needle: str) -> list[int]:
    if not needle:
        return []
    found: list[int] = []
    start = 0
    while (at := text.find(needle, start)) != -1:
        found.append(at)
        start = at + len(needle)
    return found


def common_prefix(a: str, b: str) -> int:
    low, high = 0, min(len(a), len(b))
    while low < high:
        middle = (low + high + 1) // 2
        if a[:middle] == b[:middle]:
            low = middle
        else:
            high = middle - 1
    return low


def select_occurrence(current: str, target: str, old: str, new: str, positions: list[int]) -> tuple[int, str]:
    targets = occurrences(target, new)
    if not targets:
        return positions[0], "first occurrence; replacement not present verbatim in final target"
    window = 256
    target_contexts = [(target[max(0, p - window):p][::-1], target[p + len(new):p + len(new) + window]) for p in targets]
    scored: list[tuple[int, int]] = []
    for position in positions:
        left = current[max(0, position - window):position][::-1]
        right = current[position + len(old):position + len(old) + window]
        score = max(common_prefix(left, a) + common_prefix(right, b) for a, b in target_contexts)
        scored.append((score, position))
    best = max(score for score, _ in scored)
    winners = [position for score, position in scored if score == best]
    return winners[0], "final-context match; score=" + str(best) + "; tied positions=" + str(len(winners))


def replay(original: str, target: str, filename: str, rows: list[tuple[int, dict[str, str]]]) -> tuple[str, list[tuple[object, ...]], int]:
    current = original
    report: list[tuple[object, ...]] = []
    unresolved = 0
    for ordinal, (row_number, row) in enumerate(rows):
        old, new = row.get("old", ""), row.get("new", "")
        page = row.get("printed_page", "")
        if not old:
            report.append((row_number, filename, page, "unresolved insertion", 0, "", 0, "An empty old field does not locate an insertion."))
            unresolved += 1
            continue
        if old == new:
            report.append((row_number, filename, page, "recorded no-op", 0, "", 0, "Old and new are identical."))
            continue
        try:
            start, end = scope(current, filename, page)
            target_start, target_end = scope(target, filename, page)
        except ValueError as error:
            report.append((row_number, filename, page, "unresolved scope", 0, "", 0, str(error)))
            unresolved += 1
            continue
        part = current[start:end]
        desired = target[target_start:target_end]
        positions = occurrences(part, old)
        if not positions:
            report.append((row_number, filename, page, "old text not found", 0, "", 0, "No replacement was inferred or invented."))
            unresolved += 1
            continue
        multiplicity = 1
        if len(positions) == 1:
            position = positions[0]
            selection = "unique exact old-text match"
        else:
            future_same_scope = any(later.get("printed_page", "") == page for _, later in rows[ordinal + 1:]) if filename.endswith("/gaga_body.tex") else ordinal + 1 < len(rows)
            if not future_same_scope and part.replace(old, new) == desired:
                position = positions[0]
                multiplicity = len(positions)
                selection = "all exact occurrences; last row in scope and exact final-scope equality"
            else:
                position, selection = select_occurrence(part, desired, old, new, positions)
        line = current.count("\n", 0, start + position) + 1
        if multiplicity > 1:
            replacement = part.replace(old, new)
        else:
            replacement = part[:position] + new + part[position + len(old):]
        current = current[:start] + replacement + current[end:]
        report.append((row_number, filename, page, "applied", len(positions), line, multiplicity, selection))
    return current, report, unresolved


def without_comments(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines(keepends=True):
        cutoff = len(line)
        for index, character in enumerate(line):
            if character != "%":
                continue
            backslashes, before = 0, index - 1
            while before >= 0 and line[before] == "\\":
                backslashes += 1
                before -= 1
            if backslashes % 2 == 0:
                cutoff = index
                break
        kept.append(line[:cutoff] + ("\n" if cutoff < len(line) and line.endswith("\n") else ""))
    return "".join(kept)


def group(text: str, position: int, opener: str = "{", closer: str = "}") -> tuple[str, int] | None:
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != opener:
        return None
    start, level = position + 1, 1
    position += 1
    while position < len(text):
        if text[position] == "\\":
            position += 2
            continue
        if text[position] == opener:
            level += 1
        elif text[position] == closer:
            level -= 1
            if not level:
                return text[start:position], position + 1
        position += 1
    return None


def anchors(text: str) -> list[tuple[str, str]]:
    text = without_comments(text)
    result: list[tuple[str, str]] = []
    for match in re.finditer(r"\\([A-Za-z@]+)", text):
        command = match.group(1)
        if command not in ANCHORS:
            continue
        position = match.end()
        optional = group(text, position, "[", "]")
        if optional:
            position = optional[1]
        arguments: list[str] = []
        for _ in range(ANCHORS[command]):
            argument = group(text, position)
            if not argument:
                break
            arguments.append(argument[0])
            position = argument[1]
        if len(arguments) == ANCHORS[command] and "#" not in arguments[-1]:
            result.append((command, arguments[-1]))
    return result


def macros(text: str) -> Counter[tuple[str, str]]:
    text = without_comments(text)
    result: Counter[tuple[str, str]] = Counter()
    pattern = re.compile(r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|DeclareMathOperator|DeclareTextFontCommand)\*?\s*(?:\{\\([A-Za-z@]+)\}|\\([A-Za-z@]+))\s*(?:\[(\d+)\])?")
    for match in pattern.finditer(text):
        result[(match.group(1) or match.group(2), match.group(3) or "0")] += 1
    tex_slash = re.escape(chr(92))
    for match in re.finditer(tex_slash + r"def\s*" + tex_slash + r"([A-Za-z@]+)((?:\s*#[1-9])*)", text):
        result[(match.group(1), str(len(re.findall(r"#[1-9]", match.group(2)))))] += 1
    for match in re.finditer(tex_slash + r"let\s*" + tex_slash + r"([A-Za-z@]+)", text):
        result[(match.group(1), "alias")] += 1
    for match in re.finditer(tex_slash + r"DeclareUnicodeCharacter\s*\{([^{}]+)\}", text):
        result[("Unicode " + match.group(1), "declaration")] += 1
    for match in re.finditer(r"\\(?:newenvironment|renewenvironment|provideenvironment)\*?\s*\{([^{}]+)\}\s*(?:\[(\d+)\])?", text):
        result[("environment " + match.group(1), match.group(2) or "0")] += 1
    return result


def leading_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines(keepends=True):
        if not line.strip() or line.lstrip().startswith("%"):
            lines.append(line)
        else:
            break
    return "".join(lines)


def frontmatter(text: str, filename: str) -> str:
    if filename.endswith("/gaga_body.tex"):
        match = re.search(r"^.*INTRODUCTION.*$", text, re.MULTILINE)
        return text[:match.start()] if match else ""
    if filename.endswith("/00_title_and_introduction.tex"):
        at = text.find(r"\GAGASection")
        return text[:at] if at >= 0 else ""
    return text.split(r"\begin{document}", 1)[0] if r"\begin{document}" in text else ""


def article_author_typography_review(filename: str, original_line: str, current_front: str) -> bool:
    """Recognize only the recorded print-author styling case, never credits.

    This changes the diagnostic to REVIEW, not PASS. It does not apply to a
    README, preamble, rights notice, edition credit, model credit or source
    credit, and it never supplies the primary reader's scan/credit assessment.
    """
    if filename not in {"french-diplomatic/gaga_body.tex", "french-corrected/gaga_body.tex"}:
        return False
    before = r"par Jean-Pierre \textsc{Serre}."
    after = r"\begin{center}\bfseries par Jean-Pierre \MakeUppercase{Serre}.\end{center}"
    return original_line == before and any(line.strip() == after for line in current_front.splitlines())


def changes(a: str, b: str) -> list[tuple[int, int, int, int, str, str]]:
    if a == b:
        return []
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(i, j, k, l, a[i:j], b[k:l]) for tag, i, j, k, l in matcher.get_opcodes() if tag != "equal"]


def trimmed_pair(old: str, new: str) -> tuple[str, str]:
    prefix = common_prefix(old, new)
    old, new = old[prefix:], new[prefix:]
    suffix = common_prefix(old[::-1], new[::-1])
    return (old[:-suffix], new[:-suffix]) if suffix else (old, new)


def unified(a: str, b: str, left: str, right: str) -> str:
    return "".join(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True), fromfile=left, tofile=right, n=3))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("integrity"))
    args = parser.parse_args()
    root, original_root = args.root.resolve(), args.original.resolve()
    source_root = root / "sources"
    output = args.output if args.output.is_absolute() else root / args.output
    output.mkdir(parents=True, exist_ok=True)
    if not original_root.is_dir() or not source_root.is_dir():
        raise ValueError("Both the original source tree and the current sources tree must exist.")
    if original_root == source_root.resolve():
        raise ValueError("The original reference tree must be separate from the edited sources.")
    checks: list[Check] = []
    original_files = sorted(p.relative_to(original_root) for p in original_root.rglob("*") if p.is_file() and p.name != "MANIFEST.tsv" and not p.name.endswith(GENERATED_ENDINGS))
    originals: dict[str, str] = {}
    currents: dict[str, str] = {}
    for relative in original_files:
        name = relative.as_posix()
        destination = source_root / relative
        if not destination.is_file():
            checks.append(Check("required source", name, "FAIL", "Required supplied file is missing."))
            continue
        originals[name], currents[name] = read_text(original_root / relative), read_text(destination)
        checks.append(Check("required source", name, "PASS", "Required filename retained."))
    if (original_root / "MANIFEST.tsv").is_file():
        lines = [line for line in read_text(original_root / "MANIFEST.tsv").splitlines() if line and not line.startswith("#")]
        for row in csv.DictReader(lines, delimiter="\t"):
            name = row.get("path_in_zip", "")
            if name in originals:
                valid = sha((original_root / name).read_bytes()) == row.get("sha256")
                checks.append(Check("original manifest", name, "PASS" if valid else "FAIL", "Original reference SHA-256 " + ("matches." if valid else "does not match.")))
    header, ledger = load_rows(root / "CORRECTIONS.tsv")
    if tuple(header) != REQUIRED_COLUMNS:
        checks.append(Check("ledger schema", "CORRECTIONS.tsv", "FAIL", "Columns differ from the required ordered schema."))
    by_file: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    for number, row in enumerate(ledger, 2):
        name = row.get("file", "")
        by_file[name].append((number, row))
        issues: list[str] = []
        if name not in currents:
            issues.append("file is not a retained supplied source")
        if row.get("layer") not in LAYERS:
            issues.append("unknown layer")
        if row.get("kind") not in KINDS:
            issues.append("unknown kind")
        if not row.get("evidence", "").strip():
            issues.append("empty evidence")
        if not re.match(r"^(?:high|medium|low)\b", row.get("confidence", ""), re.IGNORECASE):
            issues.append("second-reading confidence is not final")
        if issues:
            checks.append(Check("ledger row", "row " + str(number), "REVIEW", "; ".join(issues)))
    source_inventory: list[tuple[object, ...]] = []
    replay_rows: list[tuple[object, ...]] = []
    source_diffs: list[str] = []
    frontmatter_diffs: list[str] = []
    for name in sorted(originals):
        old, new = originals[name], currents[name]
        source_inventory.append((name, len(old.encode()), sha(old), len(new.encode()), sha(new), len(by_file.get(name, []))))
        if Path(name).name in {"README.md", "README.fr.md"}:
            identical = old == new
            checks.append(Check("README rights and credits", name, "PASS" if identical else "FAIL", "Complete supplied README is " + ("byte-identical." if identical else "changed; credits and rights must not be silently repaired by this audit.")))
            count_old, count_new = old.count("Thomas Waring"), new.count("Thomas Waring")
            checks.append(Check("Thomas Waring credit", name, "PASS" if count_old == count_new and identical else "FAIL", "Exact name occurrences: original=" + str(count_old) + ", current=" + str(count_new) + "; full wording is covered by README equality."))
        if name.endswith(".tex"):
            old_markers, new_markers = [m.group(0) for m in PAGE.finditer(old)], [m.group(0) for m in PAGE.finditer(new)]
            checks.append(Check("page markers", name, "PASS" if old_markers == new_markers else "FAIL", "Exact marker lines and order: original=" + str(len(old_markers)) + ", current=" + str(len(new_markers)) + "."))
            if name.endswith("/gaga_body.tex"):
                numbers = [int(m.group(1)) for m in PAGE.finditer(new)]
                checks.append(Check("printed page sequence", name, "PASS" if numbers == list(range(1, 43)) else "FAIL", "Required sequence is exactly 1 through 42, once each."))
            old_anchors, new_anchors = anchors(old), anchors(new)
            missing = Counter(old_anchors) - Counter(new_anchors)
            added = Counter(new_anchors) - Counter(old_anchors)
            detail = "Targets: original=" + str(len(old_anchors)) + ", current=" + str(len(new_anchors)) + "; missing=" + str(sum(missing.values())) + "; added=" + str(sum(added.values())) + "."
            checks.append(Check("labels and anchors", name, "FAIL" if missing else "REVIEW" if added or old_anchors != new_anchors else "PASS", detail))
            for command, value in missing:
                checks.append(Check("missing anchor", name, "FAIL", command + " target " + value))
            missing_macros = macros(old) - macros(new)
            checks.append(Check("required macros", name, "FAIL" if missing_macros else "PASS", "Removed or changed macro signatures: " + str(sum(missing_macros.values())) + ". Added macros are allowed and remain subject to ledger replay."))
            old_inputs = re.findall(r"\\(?:input|include)\s*\{([^{}]+)\}", without_comments(old))
            new_inputs = re.findall(r"\\(?:input|include)\s*\{([^{}]+)\}", without_comments(new))
            missing_inputs = Counter(old_inputs) - Counter(new_inputs)
            checks.append(Check("source inclusions", name, "FAIL" if missing_inputs else "REVIEW" if old_inputs != new_inputs else "PASS", "Literal input/include targets: original=" + str(len(old_inputs)) + ", current=" + str(len(new_inputs)) + "; missing=" + str(sum(missing_inputs.values())) + "."))
            prefix = leading_comments(old)
            if prefix.strip():
                checks.append(Check("leading provenance comments", name, "PASS" if prefix in new else "REVIEW", "Original leading comment block " + ("retained verbatim." if prefix in new else "is not present as an exact block.")))
            old_front, new_front = frontmatter(old, name), frontmatter(new, name)
            if old_front:
                if name.endswith("/gaga_body.tex") or name.endswith("/00_title_and_introduction.tex"):
                    checks.append(Check("front-matter block", name, "PASS" if old_front == new_front else "REVIEW", "Exact block " + ("unchanged." if old_front == new_front else "differs; title/layout edits require assessment against their ledger rows, independently of protected credits.")))
                    if old_front != new_front:
                        frontmatter_diffs.append(unified(old_front, new_front, "original/" + name, "current/" + name))
                credit_lines = [line for line in old_front.splitlines() if CREDIT.search(line)]
                for index, line in enumerate(credit_lines, 1):
                    if line in new_front:
                        status, detail = "PASS", "retained verbatim."
                    elif article_author_typography_review(name, line, new_front):
                        status = "REVIEW"
                        detail = "exact article-author markup changed from the supplied small-caps line to the recognized centered/bold/uppercase line. The literal name tokens Jean-Pierre and Serre are retained. Primary-reader confirmation of printed-page-1 typography and unchanged attribution is required; no automatic clearance is given. Full original/current blocks remain in frontmatter_changes.diff."
                    else:
                        status, detail = "FAIL", "exact wording or markup is absent."
                    checks.append(Check("protected front-matter credit", name + " credit line " + str(index), status, "Original credit/provenance line SHA-256=" + sha(line) + "; " + detail))
        reconstructed, events, unresolved = replay(old, new, name, by_file.get(name, []))
        replay_rows.extend(events)
        equal = reconstructed == new
        status = "FAIL" if not equal else "REVIEW" if unresolved else "PASS"
        checks.append(Check("ledger reconstruction", name, status, "Exact final equality=" + str(equal).lower() + "; ledger rows=" + str(len(by_file.get(name, []))) + "; unresolved rows=" + str(unresolved) + "."))
        if not equal:
            source_diffs.append(unified(reconstructed, new, "ledger-reconstruction/" + name, "current/" + name))
    required_names = set(originals)
    for path in sorted(source_root.rglob("*")):
        if path.is_file() and path.suffix in {".tex", ".sty", ".cls"}:
            name = path.relative_to(source_root).as_posix()
            if name not in required_names:
                checks.append(Check("additional source", name, "REVIEW", "New source file; assess structural authorization and ledger coverage separately."))
    verdicts: list[dict[str, str]] = []
    if (root / "INHERITED_VERDICTS.tsv").is_file():
        _, verdicts = load_rows(root / "INHERITED_VERDICTS.tsv")
    verdicts_by_page: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in verdicts:
        verdicts_by_page[row.get("printed_page", "")].append(row)
    french_rows: list[tuple[object, ...]] = []
    inherited_rows: list[tuple[object, ...]] = []
    final_diff, initial_diff = [], []
    french_preambles = ("french-diplomatic/gaga.tex", "french-corrected/gaga.tex")
    if all(name in currents for name in french_preambles):
        first, second = (currents[name] for name in french_preambles)
        checks.append(Check("French preamble equality", "French main files", "PASS" if first == second else "REVIEW", "Preambles " + ("are byte-identical." if first == second else "differ; inspect their ledger coverage separately.")))
        if first != second:
            final_diff.append(unified(first, second, "final-diplomatic/gaga.tex", "final-corrected/gaga.tex"))
    french_pair = ("french-diplomatic/gaga_body.tex", "french-corrected/gaga_body.tex")
    if all(name in originals for name in french_pair):
        od, oc = (originals[name] for name in french_pair)
        nd, nc = (currents[name] for name in french_pair)
        od_ranges, oc_ranges, nd_ranges, nc_ranges = (page_ranges(t) for t in (od, oc, nd, nc))
        for page in range(1, 43):
            if not all(page in ranges for ranges in (od_ranges, oc_ranges, nd_ranges, nc_ranges)):
                continue
            pieces = [text[ranges[page][0]:ranges[page][1]] for text, ranges in ((od, od_ranges), (oc, oc_ranges), (nd, nd_ranges), (nc, nc_ranges))]
            initial, final = changes(pieces[0], pieces[1]), changes(pieces[2], pieces[3])
            ids = [row.get("id", "") for row in verdicts_by_page[str(page)]]
            if initial and not ids:
                checks.append(Check("inherited French differences", "printed page " + str(page), "REVIEW", str(len(initial)) + " original character-diff blocks; no inherited-verdict row on this page."))
            for index, (a, b, c, d, old, new) in enumerate(initial, 1):
                inherited_rows.append((page, index, pieces[0].count("\n", 0, a) + 1, pieces[1].count("\n", 0, c) + 1, sha(old), sha(new), "; ".join(ids), "page-level verdict association only; no semantic one-to-one verdict claim"))
            for index, (a, b, c, d, old, new) in enumerate(final, 1):
                candidate_rows = []
                for number, row in by_file.get(french_pair[1], []):
                    if row.get("printed_page") != str(page) or row.get("kind") != "misprint of the original":
                        continue
                    recorded_old, recorded_new = row.get("old", ""), row.get("new", "")
                    cores = {trimmed_pair(recorded_old, recorded_new)}
                    cores.update((item[4], item[5]) for item in changes(recorded_old, recorded_new))
                    if (old, new) in cores:
                        candidate_rows.append(number)
                inherited_candidates = [n for n, item in enumerate(initial, 1) if (item[4], item[5]) == (old, new)]
                if candidate_rows:
                    status = "exact changed-core match to corrected-layer misprint row"
                elif inherited_candidates and ids:
                    status = "original changed-core match with page-level verdict candidate"
                elif inherited_candidates:
                    status = "original changed-core match; verdict missing on page"
                else:
                    status = "no exact changed-core candidate; manual coverage review required"
                french_rows.append((page, index, pieces[2].count("\n", 0, a) + 1, pieces[3].count("\n", 0, c) + 1, sha(old), sha(new), "; ".join(map(str, candidate_rows)), "; ".join(map(str, inherited_candidates)), "; ".join(ids), status))
                if not candidate_rows and not (inherited_candidates and ids):
                    checks.append(Check("French residual coverage", "printed page " + str(page) + " diff " + str(index), "REVIEW", status))
            if initial:
                initial_diff.append(unified(pieces[0], pieces[1], "original-diplomatic/printed-page-" + str(page), "original-corrected/printed-page-" + str(page)))
            if final:
                final_diff.append(unified(pieces[2], pieces[3], "final-diplomatic/printed-page-" + str(page), "final-corrected/printed-page-" + str(page)))
    save_tsv(output / "checks.tsv", ("category", "item", "status", "detail"), [(c.category, c.item, c.status, c.detail) for c in checks])
    save_tsv(output / "source_inventory.tsv", ("relative_source", "original_bytes", "original_sha256", "current_bytes", "current_sha256", "ledger_rows"), source_inventory)
    save_tsv(output / "ledger_replay_rows.tsv", ("ledger_row_including_header", "file", "printed_page", "status", "old_matches_in_scope", "reconstruction_line", "replacement_multiplicity", "selection"), replay_rows)
    save_tsv(output / "original_french_differences.tsv", ("printed_page", "difference", "diplomatic_page_source_line", "corrected_page_source_line", "old_core_sha256", "new_core_sha256", "page_verdict_ids", "scope_of_association"), inherited_rows)
    save_tsv(output / "final_french_difference_coverage.tsv", ("printed_page", "difference", "diplomatic_page_source_line", "corrected_page_source_line", "old_core_sha256", "new_core_sha256", "misprint_ledger_rows", "original_difference_candidates", "page_verdict_ids", "status"), french_rows)
    (output / "unreconstructed_source_changes.diff").write_text("".join(source_diffs), encoding="utf-8")
    (output / "frontmatter_changes.diff").write_text("".join(frontmatter_diffs), encoding="utf-8")
    (output / "original_french_layers.diff").write_text("".join(initial_diff), encoding="utf-8")
    (output / "final_french_layers.diff").write_text("".join(final_diff), encoding="utf-8")
    totals = Counter(check.status for check in checks)
    summary = ["# Mechanical source-integrity audit\n\n", "PASS: " + str(totals["PASS"]) + "; REVIEW: " + str(totals["REVIEW"]) + "; FAIL: " + str(totals["FAIL"]) + ".\n\n"]
    summary.append("This audit does not read a scan, decide a reading, assess a translation, or prove a mathematical claim. Exact ledger reconstruction establishes a textual transformation from the supplied source to the final source using recorded replacement text only. Context-based occurrence choices are recorded; exact equality, not a heuristic score, is the certificate. A failed reconstruction is a coverage gap or an ambiguity to investigate, not by itself proof of an unrecorded edit.\n\n")
    summary.append("Complete README equality protects all supplied README credits and rights wording, including Thomas Waring. Provenance comments and credit-bearing front-matter lines are checked separately. Other front-matter changes are reported for assessment against the scan-supported ledger. Labels, anchor targets, existing macro signatures and exact printed-page marker lines are checked mechanically.\n\n")
    summary.append("French-layer residuals are all listed in the diff and coverage table. Exact changed-core matches identify candidate ledger coverage. Inherited verdicts are associated at page level only because their readings may be human notation rather than literal TeX. The audit cannot certify the mathematical justification of a correction or a one-to-one inherited-verdict match. An unmatched core may result from surrounding notation changes or multiple changes in one row and requires the primary reader's review.\n\n")
    summary.append("## Items requiring assessment\n\n")
    for check in checks:
        if check.status != "PASS":
            summary.append("- **" + check.status + "** " + check.category + " — `" + check.item + "`: " + check.detail + "\n")
    if not totals["FAIL"] and not totals["REVIEW"]:
        summary.append("No mechanical gaps were detected within the stated scope.\n")
    (output / "REPORT.md").write_text("".join(summary), encoding="utf-8")
    print("Integrity audit: PASS=" + str(totals["PASS"]) + ", REVIEW=" + str(totals["REVIEW"]) + ", FAIL=" + str(totals["FAIL"]))
    print("Reports written to the configured audit directory. No source or editorial record was modified.")
    return 2 if totals["FAIL"] else 1 if totals["REVIEW"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print("Integrity audit stopped: " + type(error).__name__ + ". Check the configured input files and report directory.", file=sys.stderr)
        sys.exit(2)
