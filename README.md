# Jean-Pierre Serre, *Géométrie algébrique et géométrie analytique* (GAGA, 1956)

[Français](README.fr.md)

Serre's "GAGA", *Annales de l'Institut Fourier* 6 (1956), pp. 1–42: the comparison of the algebraic and the analytic
geometry of complex projective varieties, through their coherent sheaves and cohomology. This edition gives the paper
in LaTeX: the French as printed, the corrected French and an English translation.

| | |
|---|---|
| [French as printed (PDF, 25 pages)][dip] | the text as printed, misprints included |
| [Corrected French (PDF, 25 pages)][cor] | evident misprints of the print corrected |
| [English translation (PDF, 26 pages)][en] | English, from the corrected French |
| [LaTeX sources (ZIP)][zip] | the three layers below, also browsable in this repository |

- `french-diplomatic/`: the French as printed, including its misprints;
- `french-corrected/`: the French with evident misprints corrected;
- `english/`: the English translation.

Build the French with pdfLaTeX, three passes on `gaga.tex` in `french-diplomatic/` or `french-corrected/`; the English
with XeLaTeX, four passes on `english/GAGA_English_source_aligned.tex`.

## How it was made

AI-transcribed and AI-translated, July–August 2026, from the scan on Numdam
([AIF_1956__6__1_0](https://www.numdam.org/item/AIF_1956__6__1_0/)): a first-pass transcription, then checking against
the scan, the corrected layer and the English translation by OpenAI Codex, mainly GPT-5.6 Sol, with parts by GPT-6
Astra, both at reasoning effort ultra. Thomas Waring's English translation of GAGA (2021,
[thomaskwaring.github.io/gaga.pdf](https://thomaskwaring.github.io/gaga.pdf)) was consulted for comparison; the
English here was translated from Serre's French.

On 18 November 2026 GPT-6 Astra (ChatGPT Pro mode) checked the whole edition against the Numdam scan: all 42 printed
pages, in all three layers, in printed order. It made the as-printed layer say what the print says, justified every
correction of the corrected layer or put the printed reading back, read the English against the corrected French,
gave every recorded change a second reading, searched the whole work for each kind of error it found, rebuilt the
three books, and wrote notes on the mathematics. The records of that check are in
[raw/check-2026-11-18](raw/check-2026-11-18/README.md), with the prompt as sent; the whole return, with its scan crops,
is a release asset.

## Quality

The check of 18 November 2026 recorded **2,396 changes**, of which 2,395 stand and one was withdrawn at the second
reading:

| Layer | Reading of the print | Misprint of the original | Translation | Typesetting | Structure | Changes |
|---|---:|---:|---:|---:|---:|---:|
| French as printed | 15 | 0 | 0 | 715 | 3 | 733 |
| Corrected French | 13 | 3 | 0 | 715 | 3 | 734 |
| English | 3 | 0 | 52 | 870 | 2 | 927 |
| Build | 0 | 0 | 0 | 2 | 0 | 2 |

Most of them restore the typefaces of mathematical letters (script, Gothic, upright capitals) as printed. Among the
changes of substance: the analytic ideal sheaf is the printed script A and the algebraic one the printed J, each at its
own places; on p. 24 the corrected French cites [18] (FAC), where the print has [8]; and two earlier emendations that
the print does not support were withdrawn, the tensor product on p. 18 and equation (8) on p. 26. The corrected French
now differs from the print at 16 places on 15 pages, each with its reason.

The notes ([NOTES.md](raw/check-2026-11-18/NOTES.md), 106 items) give the slips of the original, the steps whose proof
the paper leaves to the reader with their checks, later results with exact locators (relative GAGA and the étale
comparison in SGA 1, among others), and links to our other work;
[CHECK_EVENTS.tsv](raw/check-2026-11-18/CHECK_EVENTS.tsv) records 328 check events, each with what was actually done.
The three books build with no error and no line or formula running into the margin.

Before this release Claude (Claude Opus 5.5 at effort high) rebuilt the three books (no error, no overfull box), looked
at pages of each, and compared four of the decisions above with the scan: the script A on p. 5, the tensor product on
p. 18, the reference on p. 24 and equation (8) on p. 26. All four agree with the print.

Errors may remain. Please report them as GitHub issues.

## Rights

The rights in the original work belong to its author or the author's representatives or heirs. Our transcription,
translation, corrections and typesetting were produced by AI. They have no human author and, in our understanding, are
not protected by copyright; where any right of ours exists nonetheless, it is dedicated to the public domain under CC0
1.0. All of this work reproduces or translates the original work, so nothing here licenses or authorizes any
reproduction, translation or other use of that work. This edition is published for educational, non-profit purposes,
and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open
a GitHub issue and we will take it down.

[dip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-fr-diplomatic.pdf
[cor]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-fr-corrected.pdf
[en]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-en.pdf
[zip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-sources.zip
