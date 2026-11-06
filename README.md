# Jean-Pierre Serre, *Géométrie algébrique et géométrie analytique* (GAGA, 1956)

[Français](README.fr.md)

Serre's "GAGA", *Annales de l'Institut Fourier* 6 (1956), pp. 1–42: the comparison of the algebraic and the analytic
geometry of complex projective varieties, through their coherent sheaves and cohomology. This edition gives the paper
in LaTeX, in French and in an English translation.

| | |
|---|---|
| [French as printed (PDF, 24 pages)][dip] | including the printing's misprints |
| [French, corrected (PDF, 24 pages)][cor] | evident misprints corrected |
| [English translation (PDF, 26 pages)][en] | |
| [LaTeX sources (ZIP)][zip] | also browsable in this repository |

Build the French with pdfLaTeX, three passes on `gaga.tex` in `french-diplomatic/` or `french-corrected/`; the English
with XeLaTeX, four passes on `english/GAGA_English_source_aligned.tex`.

## How it was made

AI-transcribed and AI-translated, July–August 2026, from the scan on Numdam
([AIF_1956__6__1_0](https://www.numdam.org/item/AIF_1956__6__1_0/)): a first-pass transcription, then checking against
the scan, the corrected layer and the English translation by OpenAI Codex, mainly GPT-5.6 Sol, with parts by GPT-6
Astra, both at Ultra effort. Thomas Waring's English translation of GAGA (2021,
[thomaskwaring.github.io/gaga.pdf](https://thomaskwaring.github.io/gaga.pdf)) was consulted for comparison; the
English here was translated from Serre's French.

## Quality

A spot check by Claude (Anthropic), November 2026, compared printed p. 20 with the scan: the French matches the print
exactly. The English has not been spot-checked. More checking is planned; until then, cite the printed paper.

## Rights

The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights,
in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain
under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold.
If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it
down.

[dip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-fr-diplomatic.pdf
[cor]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-fr-corrected.pdf
[en]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-en.pdf
[zip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-sources.zip
