"""Repair the minimal TeX runtime used for this audit, without changing sources.

This helper is unnecessary on an ordinary complete TeX Live installation. It
uses installed TeX engines, base packages, and fonts; downloads four unmodified
packages from the frozen official TeX Live 2024 archive; creates local formats
with English and French hyphenation; and assembles a local PDF font map.

Run from the deliverable root:
    python scripts/prepare_toolchain.py --cache ../toolchain

Then use build_audit.py with --texmf ../toolchain/texmf and
--formats ../toolchain/formats. The cache is a runtime dependency, not part of
the edition or of the deliverable ZIP.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import urllib.request

sys.dont_write_bytecode = True
from build_audit import sanitize


ARCHIVE = "https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/archive/"
PACKAGES = {
    "babel-french": "9475bfc0f71e820c8e8de7d9e362062bec8f5e102ab11c9b4a4d6ff045951834",
    "hyphen-french": "77a89831bbda967aea80bd71c1e3809afaa9a37c4dba7ecc838ce89377ba1d78",
    "hyph-utf8": "ecf53abe0f4c00fee7c8931abeb626bd8ee1dcdc2877dba1ac9779590f348be9",
    "ulem": "cb1af29d7f2c9d9c08f8f5b065b3a78b0ffe25b32f8e2a833408c25e8b7b29d5",
}
MAPS = ("cm.map", "cmextra.map", "latxfont.map", "symbols.map", "euler.map", "rsfs.map", "lm.map")


def kpse(arguments: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(["kpsewhich", *arguments], env=env, capture_output=True, text=True)
    if result.returncode or not result.stdout.strip():
        raise RuntimeError("The installed TeX data lacks " + " ".join(arguments))
    return result.stdout.strip()


def configure(cache: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["TEXMFHOME"] = str(cache / "texmf")
    env["TEXMFVAR"] = str(cache / "texmf-var")
    env["TEXMFCONFIG"] = str(cache / "texmf-config")
    env["TEXMF"] = kpse(["-var-value=TEXMF"], env).replace("!!", "")
    env["TEXFORMATS"] = str(cache / "formats") + os.pathsep
    env["max_print_line"] = "1000"
    return env


def run(argv: list[str], cwd: Path, env: dict[str, str], cache: Path, log_name: str) -> None:
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, errors="replace")
    output = sanitize(result.stdout + result.stderr, (cache, Path.cwd(), Path.home()))
    (cache / "logs" / log_name).write_text(output, encoding="utf-8")
    if result.returncode:
        raise RuntimeError("Command failed: " + " ".join(argv) + "; inspect the corresponding cache log.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("..") / "toolchain")
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--skip-probes", action="store_true")
    args = parser.parse_args()
    cache = args.cache.resolve()
    for name in ("downloads", "texmf", "formats", "logs"):
        (cache / name).mkdir(parents=True, exist_ok=True)
    for engine in ("pdflatex", "xelatex", "kpsewhich"):
        if not shutil.which(engine):
            raise RuntimeError("Missing installed executable: " + engine)
    manifest = ["package\turl\tsha256\n"]
    for name, expected in PACKAGES.items():
        archive = cache / "downloads" / (name + "-2024.tar.xz")
        url = ARCHIVE + name + ".tar.xz"
        if not archive.exists():
            if args.no_download:
                raise RuntimeError("Missing cached archive: " + archive.name)
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != expected:
                raise RuntimeError("Archive checksum changed: " + name)
            archive.write_bytes(data)
        data = archive.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise RuntimeError("Cached archive checksum mismatch: " + name)
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as bundle:
            members = []
            for member in bundle.getmembers():
                path = Path(member.name)
                if path.is_absolute() or ".." in path.parts:
                    raise RuntimeError("Unexpected archive path in " + name)
                if member.isfile():
                    members.append(member)
            bundle.extractall(cache / "texmf", members=members, filter="data")
        manifest.append(name + "\t" + url + "\t" + expected + "\n")
        print(name + ": verified and extracted", flush=True)
    (cache / "package-sources.tsv").write_text("".join(manifest), encoding="utf-8")
    config = cache / "texmf" / "tex" / "generic" / "config"
    config.mkdir(parents=True, exist_ok=True)
    (config / "language.dat").write_text(
        "english hyphen.tex\n=usenglish\n=american\nfrench loadhyph-fr.tex\n=francais\n",
        encoding="utf-8",
    )
    env = configure(cache)
    for engine in ("pdflatex", "xelatex"):
        run([engine, "-ini", "-etex", "-interaction=nonstopmode", "-halt-on-error", "-jobname=" + engine, engine + ".ini"], cache / "formats", env, cache, engine + "-format.log")
        print(engine + ": format generated", flush=True)
    map_lines: list[str] = []
    seen: set[str] = set()
    for name in MAPS:
        source = Path(kpse(["--format=map", name], env))
        for line in source.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith(("%", "#", ";")):
                continue
            key = line.split()[0]
            if key not in seen:
                map_lines.append(line)
                seen.add(key)
    map_dir = cache / "texmf" / "fonts" / "map" / "pdftex" / "gaga"
    map_dir.mkdir(parents=True, exist_ok=True)
    (map_dir / "pdftex.map").write_text("\n".join(map_lines) + "\n", encoding="utf-8")
    print("Font map: " + str(len(map_lines)) + " unique entries", flush=True)
    if not args.skip_probes:
        for language, engine in (("french", "pdflatex"), ("english", "xelatex")):
            probe = cache / ("synthetic-" + language)
            probe.mkdir(exist_ok=True)
            preamble = r"""\documentclass[11pt,a4paper,leqno]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[LANGUAGE]{babel}
\usepackage{amsmath,amssymb,amsfonts,mathrsfs,mathtools,tikz,geometry,enumitem}
\usetikzlibrary{cd,arrows.meta}
\usepackage[normalem]{ulem}
\usepackage[hidelinks,unicode]{hyperref}
\begin{document}
Démonstration, théorie, Noël.
$\mathfrak m\subset\mathcal O_x$, $\mathscr F$, $\alpha_i^{n-1}$, $\mathbb C$.
\uline{A short sentence to check underlining.}
\[\begin{tikzcd}A\arrow[r]&B\end{tikzcd}\]
\end{document}
"""
            (probe / "probe.tex").write_text(preamble.replace("LANGUAGE", language), encoding="utf-8")
            run([engine, "-interaction=nonstopmode", "-halt-on-error", "probe.tex"], probe, env, cache, language + "-probe.log")
            print(language + ": synthetic preamble probe passed", flush=True)
    print("Toolchain ready. No edition sources were read or modified.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
