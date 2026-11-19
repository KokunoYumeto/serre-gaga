"""Build the three GAGA layers and retain privacy-sanitized audit logs.

Run from the package root, for example:
    python scripts/build_audit.py --sources sources --output build/before

The script does not edit the sources. It invokes pdfLaTeX three times in each
French tree and XeLaTeX four times in the English tree. On an engine failure it
stops that layer unless --keep-going is supplied. It writes all box diagnostics,
all warning/error lines, and a final-pass summary as TSV files. Output-page and
input-file associations in box reports are explicitly marked as inferred.
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


LAYERS = (
    ("french-diplomatic", "pdflatex", "gaga.tex", 3),
    ("french-corrected", "pdflatex", "gaga.tex", 3),
    ("english", "xelatex", "GAGA_English_source_aligned.tex", 4),
)

BOX = re.compile(
    r"Overfull \\(?P<box>[hv])box \((?P<size>[0-9.]+)pt too "
    r"(?P<direction>wide|high)\)(?P<detail>[^\n]*)"
)
SOURCE = re.compile(r"\((?P<file>[^\s()]+\.tex)(?=[\s()]|$)")
# A box diagnostic may itself contain bracketed citations. Restrict estimated
# page markers to progress tokens at the beginning of a log line so such a
# citation cannot silently become a PDF-page estimate. Adjacent or wrapped
# shipout markers can be missed; estimates remain explicitly labelled.
PAGE = re.compile(r"(?m)^\s*\[(?P<page>\d+)(?=[\]{}\s])")
LINE_RANGE = re.compile(r"(?:at lines?|at line)\s+(\d+)(?:--(\d+))?")
FILE_LINE_ERROR = re.compile(r"^(?:\./)?[^\s:]+\.tex:\d+(?::\d+)?:")
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
# This matches absolute filesystem tokens, while leaving URLs and relative
# source filenames intact. Local identities are never part of an audit log.
ABSOLUTE_TOKEN = re.compile(r"(?<![A-Za-z0-9.:/])(?:[A-Za-z]:[\\/]|/)[^\s()\[\]<>\"']+")


def sanitize(text: str, roots: tuple[Path, ...]) -> str:
    for root in sorted({str(p.resolve()) for p in roots}, key=len, reverse=True):
        text = text.replace(root, "<local>")
    text = ABSOLUTE_TOKEN.sub("<local>", text)
    return EMAIL.sub("<redacted-email>", text)


def command_result(argv: list[str], env: dict[str, str]) -> str:
    proc = subprocess.run(argv, env=env, capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def runtime_environment(extra_texmf: Path | None, format_dir: Path | None) -> dict[str, str]:
    """Handle a runtime with unindexed but readable, installed TeX trees.

    Kpathsea's !! prefix forbids filesystem lookup. Removing it uses ordinary
    readable files when the runtime has omitted its generated filename index.
    A separately prepared local TeX tree and format directory may be supplied.
    """
    env = os.environ.copy()
    if shutil.which("kpsewhich"):
        if not command_result(["kpsewhich", "article.cls"], env):
            search = command_result(["kpsewhich", "-var-value=TEXMF"], env)
            if search:
                env["TEXMF"] = search.replace("!!", "")
        if extra_texmf:
            previous = env.get("TEXMF") or command_result(
                ["kpsewhich", "-var-value=TEXMF"], env
            )
            env["TEXMF"] = "{" + str(extra_texmf.resolve()) + "," + previous + "}"
    if format_dir:
        env["TEXFORMATS"] = str(format_dir.resolve()) + os.pathsep
    env["max_print_line"] = "1000"
    env["error_line"] = "254"
    env["half_error_line"] = "238"
    return env


def box_rows(log: str, layer: str, number: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    source_matches = list(SOURCE.finditer(log))
    page_matches = list(PAGE.finditer(log))
    for match in BOX.finditer(log):
        detail = match.group("detail").strip()
        lines = LINE_RANGE.search(detail)
        source_before = [m for m in source_matches if m.start() < match.start()]
        later_pages = [m for m in page_matches if m.start() > match.end()]
        prior_pages = [m for m in page_matches if m.start() < match.start()]
        if later_pages:
            page = later_pages[0].group("page")
            page_basis = "inferred: next line-initial output-page marker"
        elif prior_pages:
            page = str(int(prior_pages[-1].group("page")) + 1)
            page_basis = "inferred: previous line-initial output-page marker plus one"
        else:
            page = ""
            page_basis = "unavailable"
        rows.append({
            "layer": layer,
            "pass": str(number),
            "box": match.group("box"),
            "size_pt": match.group("size"),
            "direction": match.group("direction"),
            "source_file": source_before[-1].group("file") if source_before else "",
            "source_basis": "inferred: latest TeX input marker" if source_before else "unavailable",
            "source_lines": (lines.group(1) + ("--" + lines.group(2) if lines.group(2) else "")) if lines else "",
            "output_page": page,
            "page_basis": page_basis,
            "diagnostic": detail,
        })
    return rows


def write_tsv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=Path("sources"))
    parser.add_argument("--output", type=Path, default=Path("../work/build-audit"))
    parser.add_argument("--layer", action="append", choices=[r[0] for r in LAYERS])
    parser.add_argument("--texmf", type=Path, help="Optional additional prepared TeX tree.")
    parser.add_argument("--formats", type=Path, help="Optional directory containing engine format files.")
    parser.add_argument("--keep-going", action="store_true")
    args = parser.parse_args()
    source_root, output_root = args.sources.resolve(), args.output.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    roots = (Path.cwd(), source_root, output_root, Path.home())
    env = runtime_environment(args.texmf, args.formats)
    all_boxes: list[dict[str, str]] = []
    all_warnings: list[dict[str, str]] = []
    summaries: list[dict[str, str]] = []
    pass_summaries: list[dict[str, str]] = []
    failed = False
    for layer, engine, mainfile, passes in LAYERS:
        if args.layer and layer not in args.layer:
            continue
        layer_output = output_root / layer
        layer_output.mkdir(parents=True, exist_ok=True)
        if not shutil.which(engine):
            summaries.append({"layer": layer, "engine": engine, "passes_completed": "0", "exit_status": "missing engine", "errors": "1", "warnings": "0", "overfull_count": "0", "over_2pt": "0", "over_10pt": "0", "maximum_overfull_pt": "0", "pdf_created": "no"})
            failed = True
            continue
        version = subprocess.run([engine, "--version"], env=env, capture_output=True, text=True)
        (layer_output / "engine-version.txt").write_text(sanitize(version.stdout + version.stderr, roots), encoding="utf-8")
        current = source_root / layer
        if not (current / mainfile).is_file():
            raise SystemExit("Missing main source for " + layer)
        last_boxes: list[dict[str, str]] = []
        last_warnings: list[dict[str, str]] = []
        error_count = 0
        return_code = 0
        completed = 0
        for number in range(1, passes + 1):
            cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", mainfile]
            proc = subprocess.run(cmd, cwd=current, env=env, capture_output=True, text=True, errors="replace")
            completed = number
            return_code = proc.returncode
            stdout = sanitize(proc.stdout + proc.stderr, roots)
            (layer_output / f"pass-{number:02d}.stdout.txt").write_text(stdout, encoding="utf-8")
            raw_log_path = current / (Path(mainfile).stem + ".log")
            raw_log = raw_log_path.read_text(encoding="utf-8", errors="replace") if raw_log_path.exists() else proc.stdout + proc.stderr
            log = sanitize(raw_log, roots)
            (layer_output / f"pass-{number:02d}.log").write_text(log, encoding="utf-8")
            last_boxes = box_rows(log, layer, number)
            all_boxes.extend(last_boxes)
            last_warnings = []
            for log_line, line in enumerate(log.splitlines(), 1):
                if "Warning" in line or "Error" in line or line.startswith("!") or "Emergency stop" in line or FILE_LINE_ERROR.match(line):
                    last_warnings.append({"layer": layer, "pass": str(number), "log_line": str(log_line), "diagnostic": line})
            all_warnings.extend(last_warnings)
            error_count = sum(bool("Error" in r["diagnostic"] or r["diagnostic"].startswith("!") or "Emergency stop" in r["diagnostic"] or FILE_LINE_ERROR.match(r["diagnostic"])) for r in last_warnings)
            pass_pdf = current / (Path(mainfile).stem + ".pdf")
            if return_code == 0 and pass_pdf.exists():
                shutil.copy2(pass_pdf, layer_output / f"pass-{number:02d}.pdf")
            pass_sizes = [float(row["size_pt"]) for row in last_boxes]
            failed = failed or bool(return_code) or bool(error_count) or any(size > 2 for size in pass_sizes)
            page_counts = re.findall(r"Output written on .*? \((\d+) pages?", stdout)
            pass_summaries.append({
                "layer": layer, "pass": str(number), "engine": engine,
                "exit_status": str(return_code), "errors": str(error_count),
                "warnings": str(len(last_warnings) - error_count),
                "overfull_count": str(len(pass_sizes)),
                "over_2pt": str(sum(size > 2 for size in pass_sizes)),
                "over_10pt": str(sum(size > 10 for size in pass_sizes)),
                "maximum_overfull_pt": str(max(pass_sizes, default=0)),
                "pdf_created": "yes" if return_code == 0 and pass_pdf.exists() else "no",
                "pdf_pages": page_counts[-1] if page_counts else "",
            })
            print(f"{layer}: pass {number}/{passes}, exit {return_code}, overfull boxes {len(last_boxes)}", flush=True)
            if return_code and not args.keep_going:
                break
        pdf_path = current / (Path(mainfile).stem + ".pdf")
        if pdf_path.exists() and return_code == 0:
            shutil.copy2(pdf_path, layer_output / f"{layer}.pdf")
        sizes = [float(r["size_pt"]) for r in last_boxes]
        summaries.append({
            "layer": layer,
            "engine": engine,
            "passes_completed": str(completed),
            "exit_status": str(return_code),
            "errors": str(error_count),
            "warnings": str(len(last_warnings) - error_count),
            "overfull_count": str(len(sizes)),
            "over_2pt": str(sum(s > 2 for s in sizes)),
            "over_10pt": str(sum(s > 10 for s in sizes)),
            "maximum_overfull_pt": str(max(sizes, default=0)),
            "pdf_created": "yes" if pdf_path.exists() and return_code == 0 else "no",
        })
        failed = failed or bool(return_code) or completed != passes
    write_tsv(output_root / "overfull.tsv", ("layer", "pass", "box", "size_pt", "direction", "source_file", "source_basis", "source_lines", "output_page", "page_basis", "diagnostic"), all_boxes)
    write_tsv(output_root / "warnings.tsv", ("layer", "pass", "log_line", "diagnostic"), all_warnings)
    write_tsv(output_root / "summary.tsv", ("layer", "engine", "passes_completed", "exit_status", "errors", "warnings", "overfull_count", "over_2pt", "over_10pt", "maximum_overfull_pt", "pdf_created"), summaries)
    write_tsv(output_root / "passes.tsv", ("layer", "pass", "engine", "exit_status", "errors", "warnings", "overfull_count", "over_2pt", "over_10pt", "maximum_overfull_pt", "pdf_created", "pdf_pages"), pass_summaries)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
