"""Create an immutable complete GAGA checkpoint or final ZIP.

This script does nothing until invoked. Use --preflight to inspect eligibility,
privacy findings and the candidate file list without creating an archive.

Examples, run from the deliverable root:
    python scripts/package_deliverable.py --root . --output-dir .. --kind checkpoint --number 1 --preflight
    python scripts/package_deliverable.py --root . --output-dir .. --kind checkpoint --number 2 --previous-save-utc 2026-11-18T13:30:00Z
    python scripts/package_deliverable.py --root . --output-dir .. --kind final

The first checkpoint is gated by the first timestamp in progress.log unless
--work-start-utc is supplied. Later checkpoints require the actual successful
save time of the previous checkpoint. Library upload is deliberately separate:
creation of a local archive is not evidence that it was saved persistently.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import io
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import zipfile


MAX_BYTES = 500_000_000
CHUNK = 1024 * 1024
RESERVED = {"PACKAGE_FILES.tsv", "PACKAGE_EXCLUSIONS.tsv", "PACKAGE_INFO.md"}
EXCLUDED_DIRECTORIES = {
    ".git", ".cache", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "__pycache__", "node_modules", "input", "inputs", "upload",
    "uploads", "toolchain", "tmp", "temp", "renders", "render", "rendered",
    "checkpoints", "archives", "backup", "backups", "snapshots",
}
ARCHIVE_ENDINGS = (".zip", ".7z", ".tar", ".tar.gz", ".tgz", ".tar.xz", ".txz", ".xz", ".bz2")
INTERMEDIATE_ENDINGS = (
    ".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".out", ".toc",
    ".synctex", ".synctex.gz", ".xdv", ".dvi", ".nav", ".snm", ".vrb",
    ".loa", ".lof", ".lot", ".bcf", ".run.xml", ".pyc", ".pyo",
)
TEMPORARY_ENDINGS = (".tmp", ".temp", ".partial", ".bak", ".orig", ".swp", "~")
IMAGE_ENDINGS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff", ".bmp", ".svg", ".avif", ".heic", ".jp2", ".ppm", ".pgm", ".pbm"}
TEXT_ENDINGS = {
    ".md", ".tex", ".tsv", ".csv", ".txt", ".log", ".py", ".sh",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sty", ".cls",
    ".html", ".htm", ".css", ".js", ".ts", ".tsx", ".jsx", ".bib",
    ".rst", ".xml", ".map", ".def", ".ldf", ".lua", ".pl", ".bat",
}
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
LOCAL_POSIX = re.compile(
    r"(?<![\w:/])/(?:home|Users|workspace|workspaces|scratch|tmp|var|opt|usr|mnt|media|private|Volumes|root|etc|run|srv|dev|sys|bin|sbin|lib|lib64|Applications|app|data|Library)(?:/)[^\s<>\]\)\"']*"
)
TEX_MATH_COMMAND = r"(?:mathrm|mathcal|mathfrak|mathbf|mathbb|mathsf|mathit|mathscr|operatorname|text)"
TEX_TEXT_COMMAND = r"(?:textsc|textbf|textit|textrm|textsf|texttt|emph|ref|pageref|cite|hyperref|GAGAInternalRef|GAGACite|GAGATarget)"
# A map's one-letter name and colon followed by a braced TeX command is
# mathematical syntax. It must not be classified as a Windows drive path.
LOCAL_WINDOWS = re.compile(r"(?<![\w\\])(?:[A-Za-z]:(?:/|\\(?!" + TEX_MATH_COMMAND + r"\s*\{))|\\\\[A-Za-z0-9_-]+[\\/])[^\s<>\]\)\"']*")
LOCAL_PERSONAL = re.compile(r"(?<![\w/])(?:Documents|Downloads|Desktop|AppData)[\\/][^\s<>\]\)\"']*")
# TeX's unbreakable space before a formatting/reference command is distinct
# from a home-relative path; actual slash and ordinary directory forms remain.
LOCAL_TILDE = re.compile(r"(?<![\w])~(?:/|\\(?!" + TEX_TEXT_COMMAND + r"\s*(?:\{|\[)))[^\s<>\]\)\"']*")
FILE_URI = re.compile(r"file:[/]{2}[^\s<>\]\)\"']+", re.IGNORECASE)
PRIVATE_PATTERNS = (
    ("email address", EMAIL),
    ("absolute POSIX local path", LOCAL_POSIX),
    ("absolute Windows or network local path", LOCAL_WINDOWS),
    ("personal local-directory path", LOCAL_PERSONAL),
    ("home-relative local path", LOCAL_TILDE),
    ("local file URI", FILE_URI),
)


class PackagingError(RuntimeError):
    pass


def utc(value: str) -> datetime:
    value = value.strip().removesuffix(" UTC")
    value = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise PackagingError("Use an ISO date and time in UTC.") from error
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def stamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_label(value: str) -> str:
    """Do not echo a sensitive filename as part of a privacy finding."""
    for _, pattern in PRIVATE_PATTERNS:
        value = pattern.sub("<redacted>", value)
    return value


def exclusion(relative: Path) -> str | None:
    parts = relative.parts
    if any(part in EXCLUDED_DIRECTORIES for part in parts[:-1]):
        return "raw input, dependency cache, render work, prior snapshot or temporary directory"
    name = relative.name
    lower = name.lower()
    if name in RESERVED and len(parts) == 1:
        return "package-generated inventory from an earlier local extraction; regenerated for this ZIP"
    if lower.endswith(ARCHIVE_ENDINGS):
        return "archive; earlier checkpoints and attached archives are never nested"
    if lower.endswith(INTERMEDIATE_ENDINGS):
        return "generated TeX or Python intermediate"
    if lower.endswith(TEMPORARY_ENDINGS):
        return "temporary or backup file"
    if name.startswith("."):
        return "hidden runtime or temporary file"
    if parts[0] == "sources" and relative.suffix.lower() in {".log", ".pdf"}:
        return "raw generated TeX build file; use sanitized audit logs and the designated PDF deliverables"
    if relative.suffix.lower() in IMAGE_ENDINGS and parts[0] != "evidence":
        return "rendered work image outside the explicit evidence directory"
    if lower.startswith("gaga_aif_1956") and relative.suffix.lower() == ".pdf":
        return "supplied original scan"
    return None


def gather(root: Path) -> tuple[list[Path], list[tuple[str, str]]]:
    included: list[Path] = []
    excluded: list[tuple[str, str]] = []
    for directory, subdirectories, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for dirname in sorted(subdirectories):
            candidate = directory_path / dirname
            if candidate.is_symlink():
                relative = candidate.relative_to(root)
                excluded.append((relative.as_posix() + "/", "symlinked directory is not followed"))
        subdirectories[:] = sorted(name for name in subdirectories if not (directory_path / name).is_symlink())
        for name in sorted(filenames):
            path = directory_path / name
            relative = path.relative_to(root)
            reason = exclusion(relative)
            if reason:
                excluded.append((relative.as_posix(), reason))
            elif path.is_symlink():
                raise PackagingError("Included deliverable is a symlink: " + safe_label(relative.as_posix()))
            elif path.is_file():
                included.append(relative)
            else:
                raise PackagingError("Unsupported included filesystem item: " + safe_label(relative.as_posix()))
    return sorted(included), sorted(excluded)


def digest_file(path: Path) -> tuple[int, str, tuple[int, int]]:
    before = path.stat()
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while data := handle.read(CHUNK):
            size += len(data)
            digest.update(data)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) or size != after.st_size:
        raise PackagingError("A deliverable changed during inventory; pause writes and retry.")
    return size, digest.hexdigest(), (after.st_size, after.st_mtime_ns)


def privacy_findings(root: Path, included: list[Path]) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for relative in included:
        label = relative.as_posix()
        for kind, pattern in PRIVATE_PATTERNS:
            if pattern.search(label):
                findings.append((safe_label(label), 0, "filename contains " + kind))
        path = root / relative
        if path.suffix.lower() not in TEXT_ENDINGS:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as error:
            raise PackagingError("Cannot scan text file as UTF-8: " + safe_label(label)) from error
        for number, line in enumerate(text.splitlines(), 1):
            for kind, pattern in PRIVATE_PATTERNS:
                if pattern.search(line):
                    findings.append((safe_label(label), number, kind))
    return findings


def tsv(header: tuple[str, ...], rows: list[tuple[object, ...]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def zip_info(name: str, now: datetime, mode: int = 0o644) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, now.timetuple()[:6])
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | mode) << 16
    return info


def expected_name(kind: str, number: int | None) -> str:
    if kind == "final":
        if number is not None:
            raise PackagingError("The final package has no checkpoint number.")
        return "GAGA_CHECK.zip"
    if number is None or number < 1:
        raise PackagingError("A checkpoint requires a positive --number.")
    return f"GAGA_CHECK_checkpoint_{number:02d}.zip"


def eligibility(args: argparse.Namespace, root: Path, now: datetime) -> tuple[bool, str]:
    if args.kind == "final":
        return True, "Final package: no checkpoint interval applies."
    if args.number > 1:
        if not args.previous_save_utc:
            raise PackagingError("Later checkpoints require --previous-save-utc, the previous successful persistent save time.")
        reference = utc(args.previous_save_utc)
        basis = "previous successful persistent save"
    else:
        if args.previous_save_utc:
            raise PackagingError("Checkpoint 1 uses the work start, not a previous save.")
        if args.work_start_utc:
            reference = utc(args.work_start_utc)
        else:
            progress = root / "progress.log"
            if not progress.is_file():
                raise PackagingError("Checkpoint 1 requires progress.log or --work-start-utc.")
            with progress.open(encoding="utf-8") as handle:
                first_line = handle.readline()
            reference = utc(first_line)
        basis = "work start"
    due = reference + timedelta(hours=1)
    return now >= due, "Next eligible time: " + stamp(due) + " (one hour after " + basis + ")."


def make_archive(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    if not root.is_dir():
        raise PackagingError("The deliverable root does not exist.")
    if not 0 < args.max_bytes <= MAX_BYTES:
        raise PackagingError("--max-bytes must be positive and no greater than 500000000.")
    now = datetime.now(timezone.utc)
    name = expected_name(args.kind, args.number)
    eligible, timing = eligibility(args, root, now)
    output_dir = args.output_dir.resolve()
    if output_dir == root or root in output_dir.parents:
        raise PackagingError("Place the archive output directory outside the deliverable root.")
    destination = output_dir / name
    if destination.exists():
        raise PackagingError("Refusing to replace existing archive " + name + ".")
    included, excluded = gather(root)
    if not included:
        raise PackagingError("No deliverable files found.")
    findings = privacy_findings(root, included)
    print("UTC now: " + stamp(now))
    print(timing)
    print("Included deliverables: " + str(len(included)))
    print("Excluded generated, raw or temporary files: " + str(len(excluded)))
    print("Owned deliverables omitted because unchanged: 0 (complete snapshot).")
    for filename, line, kind in findings:
        location = filename + (":" + str(line) if line else "")
        print("PRIVACY " + location + ": " + kind)
    if args.list_files:
        for relative in included:
            print("INCLUDE " + safe_label(relative.as_posix()))
        for relative, reason in excluded:
            print("EXCLUDE " + safe_label(relative) + ": " + reason)
    if findings:
        raise PackagingError("Privacy preflight found " + str(len(findings)) + " location(s). No text, credit, rights notice or archive was changed.")
    if args.preflight:
        print("Preflight only: no archive created.")
        return 0 if eligible else 3
    if not eligible:
        raise PackagingError("Checkpoint is not yet due. No archive created.")
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory: list[tuple[object, ...]] = []
    snapshots: dict[Path, tuple[int, str, tuple[int, int]]] = {}
    for relative in included:
        size, digest, status = digest_file(root / relative)
        snapshots[relative] = (size, digest, status)
        inventory.append((relative.as_posix(), size, digest, "deliverable"))
    exclusion_bytes = tsv(("relative_path", "reason", "unchanged_file_checkpoint"), [(safe_label(p), reason, "") for p, reason in excluded])
    info_text = (
        "# GAGA package inventory\n\n"
        + "Archive: `" + name + "`. Created " + stamp(now) + ".\n\n"
        + "This is a complete snapshot of the current deliverables. No owned deliverable "
        + "was omitted because it was unchanged; therefore no earlier checkpoint is needed "
        + "to supply an unchanged deliverable.\n\n"
        + "`PACKAGE_FILES.tsv` gives the byte size and SHA-256 of every other archive member. "
        + "The inventory excludes its own hash to avoid a circular checksum. "
        + "`PACKAGE_EXCLUSIONS.tsv` lists generated files, temporary files and raw inputs "
        + "excluded by policy; its unchanged-file checkpoint column is empty. Any recognizable "
        + "private address or local-path fragment in an exclusion label is redacted in this "
        + "generated metadata, without changing the excluded file.\n\n"
        + "Supplied archives and scans, dependencies, rendered work images outside `evidence/`, "
        + "generated TeX intermediates and earlier ZIPs are excluded. Evidence images already "
        + "present in the explicit evidence directory are retained.\n\n"
        + "The privacy preflight checked returned UTF-8 text files for email addresses and "
        + "recognizable machine-local paths. It reports findings and never edits text, "
        + "credits or rights notices. Binary file content is not a text privacy scan.\n\n"
        + "A locally created checkpoint still requires a successful persistent save. "
        + "Its filename must never be reused, overwritten, renamed or deleted.\n"
    ).encode("utf-8")
    generated = {"PACKAGE_EXCLUSIONS.tsv": exclusion_bytes, "PACKAGE_INFO.md": info_text}
    for generated_name, data in generated.items():
        inventory.append((generated_name, len(data), hashlib.sha256(data).hexdigest(), "package metadata"))
    inventory_bytes = tsv(("relative_path", "bytes", "sha256", "role"), sorted(inventory))
    temporary: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(prefix=".gaga-package-", suffix=".tmp", dir=output_dir)
        os.close(descriptor)
        temporary = Path(temporary_name)
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as bundle:
            bundle.writestr(zip_info("PACKAGE_FILES.tsv", now), inventory_bytes)
            for generated_name, data in generated.items():
                bundle.writestr(zip_info(generated_name, now), data)
            for relative in included:
                path = root / relative
                size, expected, expected_status = snapshots[relative]
                current = path.stat()
                if (current.st_size, current.st_mtime_ns) != expected_status:
                    raise PackagingError("A deliverable changed before archiving; pause writes and retry.")
                mode = stat.S_IMODE(current.st_mode) & 0o777
                digest = hashlib.sha256()
                count = 0
                with path.open("rb") as source, bundle.open(zip_info(relative.as_posix(), now, mode), "w") as target:
                    while data := source.read(CHUNK):
                        target.write(data)
                        digest.update(data)
                        count += len(data)
                if count != size or digest.hexdigest() != expected:
                    raise PackagingError("A deliverable changed while archiving; pause writes and retry.")
        size = temporary.stat().st_size
        if size >= args.max_bytes:
            raise PackagingError("Compressed package is " + str(size) + " bytes, exceeding the strict limit of " + str(args.max_bytes) + ". No archive published; separate independent ZIP parts are required.")
        with zipfile.ZipFile(temporary) as check:
            damaged = check.testzip()
            if damaged:
                raise PackagingError("ZIP CRC verification failed; no archive published.")
            expected_members = {p.as_posix() for p in included} | RESERVED
            if set(check.namelist()) != expected_members:
                raise PackagingError("ZIP member inventory mismatch; no archive published.")
        _, archive_digest, _ = digest_file(temporary)
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        # Atomic, same-filesystem publication without replacement. An existing
        # destination makes link() fail; no earlier archive can be overwritten.
        os.link(temporary, destination)
        print("Created " + name)
        print("Bytes: " + str(size) + " (strictly below " + str(args.max_bytes) + ")")
        print("SHA-256: " + archive_digest)
        print("ZIP CRC and complete member inventory verified.")
        print("Persistent upload is still required; this script does not claim a saved checkpoint.")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path(".."))
    parser.add_argument("--kind", choices=("checkpoint", "final"), required=True)
    parser.add_argument("--number", type=int)
    parser.add_argument("--work-start-utc")
    parser.add_argument("--previous-save-utc")
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--list-files", action="store_true")
    args = parser.parse_args()
    try:
        return make_archive(args)
    except (PackagingError, OSError, zipfile.BadZipFile) as error:
        print("Packaging stopped: " + safe_label(str(error)), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
