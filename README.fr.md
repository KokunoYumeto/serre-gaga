# Jean-Pierre Serre, *Géométrie algébrique et géométrie analytique* (GAGA, 1956)

[English](README.md)

« GAGA » de Serre, *Annales de l'Institut Fourier* 6 (1956), p. 1–42 : la comparaison de la géométrie algébrique et
de la géométrie analytique des variétés projectives complexes, par leurs faisceaux cohérents et leur cohomologie.
Cette édition donne l'article en LaTeX, en français et en traduction anglaise.

| | |
|---|---|
| [Français tel qu'imprimé (PDF, 24 pages)][dip] | coquilles de l'impression comprises |
| [Français corrigé (PDF, 24 pages)][cor] | coquilles évidentes corrigées |
| [Traduction anglaise (PDF, 26 pages)][en] | |
| [Sources LaTeX (ZIP)][zip] | aussi consultables dans ce dépôt |

Compiler le français avec pdfLaTeX, trois passes sur `gaga.tex` dans `french-diplomatic/` ou `french-corrected/` ;
l'anglais avec XeLaTeX, quatre passes sur `english/GAGA_English_source_aligned.tex`.

## Comment elle a été faite

Transcription et traduction produites par IA, juillet–août 2026, à partir de la numérisation sur Numdam
([AIF_1956__6__1_0](https://www.numdam.org/item/AIF_1956__6__1_0/)) : une première transcription, puis la vérification
sur la numérisation, la couche corrigée et la traduction anglaise par OpenAI Codex (surtout GPT-5.6 Sol, avec des
parties par GPT-6 Astra, tous deux en effort Ultra). La traduction anglaise de GAGA par Thomas Waring (2021,
[thomaskwaring.github.io/gaga.pdf](https://thomaskwaring.github.io/gaga.pdf)) a été consultée pour comparaison ;
l'anglais de cette édition est traduit du français de Serre.

## Qualité

Un contrôle ponctuel par Claude (Anthropic), novembre 2026, a comparé la p. 20 imprimée à la numérisation : le
français correspond exactement à l'imprimé. L'anglais n'a pas été contrôlé. D'autres contrôles sont prévus ; d'ici là,
citer l'article imprimé.

## Droits

Les droits sur l'œuvre originale appartiennent à son auteur ou à ses représentants ou ayants droit. Dans la mesure
où nous détenons des droits sur la transcription, la traduction, les corrections et la composition produites par IA,
ils sont dédiés au domaine public sous CC0 1.0. Cette édition est publiée à des fins éducatives et non lucratives, et
nous ne revendiquons aucun droit que nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez
à sa publication ici, ouvrez une issue GitHub et nous la retirerons.

[dip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-fr-diplomatic.pdf
[cor]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-fr-corrected.pdf
[en]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-en.pdf
[zip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-06/gaga-sources.zip
