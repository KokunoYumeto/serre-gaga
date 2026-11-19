# Jean-Pierre Serre, *Géométrie algébrique et géométrie analytique* (GAGA, 1956)

[English](README.md)

Le « GAGA » de Serre, *Annales de l'Institut Fourier* 6 (1956), p. 1–42 : la comparaison des géométries algébrique et
analytique des variétés projectives complexes, par leurs faisceaux cohérents et leur cohomologie. Cette édition donne
l'article en LaTeX : le français tel qu'imprimé, le français corrigé et une traduction anglaise.

| | |
|---|---|
| [Français tel qu'imprimé (PDF, 25 pages)][dip] | le texte tel qu'imprimé, coquilles comprises |
| [Français corrigé (PDF, 25 pages)][cor] | coquilles évidentes de l'imprimé corrigées |
| [Traduction anglaise (PDF, 26 pages)][en] | anglais, traduit du français corrigé |
| [Sources LaTeX (ZIP)][zip] | les trois couches ci-dessous, aussi consultables dans ce dépôt |

- `french-diplomatic/` : le français tel qu'imprimé, coquilles comprises ;
- `french-corrected/` : le français où les coquilles évidentes sont corrigées ;
- `english/` : la traduction anglaise.

Compiler le français avec pdfLaTeX, trois passes sur `gaga.tex` dans `french-diplomatic/` ou `french-corrected/` ;
l'anglais avec XeLaTeX, quatre passes sur `english/GAGA_English_source_aligned.tex`.

## Comment elle a été faite

Transcription et traduction produites par IA, juillet–août 2026, à partir de la numérisation sur Numdam
([AIF_1956__6__1_0](https://www.numdam.org/item/AIF_1956__6__1_0/)) : une première transcription, puis la vérification
sur la numérisation, la couche corrigée et la traduction anglaise par OpenAI Codex (surtout GPT-5.6 Sol, avec des
parties par GPT-6 Astra, tous deux en effort de raisonnement ultra). La traduction anglaise de GAGA par Thomas Waring
(2021, [thomaskwaring.github.io/gaga.pdf](https://thomaskwaring.github.io/gaga.pdf)) a été consultée pour comparaison ;
l'anglais de cette édition est traduit du français de Serre.

Le 18 novembre 2026, GPT-6 Astra (mode Pro de ChatGPT) a contrôlé toute l'édition sur la numérisation de Numdam : les
42 pages imprimées, dans les trois couches, dans l'ordre de l'imprimé. Il a rendu la couche « tel qu'imprimé » conforme
à l'imprimé, justifié chaque correction de la couche corrigée ou rétabli la leçon imprimée, relu l'anglais sur le
français corrigé, soumis chaque modification à une seconde lecture, recherché dans tout l'article chaque type d'erreur
trouvé, recompilé les trois livres et écrit des notes sur les mathématiques. Les relevés de ce contrôle sont dans
[raw/check-2026-11-18](raw/check-2026-11-18/README.md), avec le prompt tel qu'envoyé ; le retour complet, avec ses
extraits de la numérisation, est joint à la publication (release).

## Qualité

Le contrôle du 18 novembre 2026 a relevé **2 396 modifications** ; 2 395 sont maintenues et une a été retirée à la
seconde lecture :

| Couche | Lecture de l'imprimé | Coquille de l'original | Traduction | Typographie | Structure | Modifications |
|---|---:|---:|---:|---:|---:|---:|
| Français tel qu'imprimé | 15 | 0 | 0 | 715 | 3 | 733 |
| Français corrigé | 13 | 3 | 0 | 715 | 3 | 734 |
| Anglais | 3 | 0 | 52 | 870 | 2 | 927 |
| Compilation | 0 | 0 | 0 | 2 | 0 | 2 |

La plupart rétablissent les caractères des lettres mathématiques (ronde, gothique, capitales droites) tels
qu'imprimés. Parmi les modifications de fond : le faisceau d'idéaux analytique est le A ronde imprimé et le faisceau
d'idéaux algébrique le J imprimé, chacun à sa place ; p. 24, le français corrigé renvoie à [18] (FAC), là où l'imprimé
porte [8] ; deux corrections antérieures que l'imprimé ne justifie pas ont été retirées, le produit tensoriel de la
p. 18 et l'égalité (8) de la p. 26. Le français corrigé diffère maintenant de l'imprimé en 16 endroits sur 15 pages,
chacun avec sa raison.

Les notes ([NOTES.md](raw/check-2026-11-18/NOTES.md), 106 entrées) donnent les lapsus de l'original, les étapes dont
l'article laisse la preuve au lecteur avec leurs vérifications, des résultats ultérieurs avec des références précises
(GAGA relatif et la comparaison étale dans SGA 1, entre autres) et les liens avec nos autres travaux ;
[CHECK_EVENTS.tsv](raw/check-2026-11-18/CHECK_EVENTS.tsv) consigne 328 événements de vérification, chacun avec ce qui a
réellement été fait. Les trois livres compilent sans erreur et sans ligne ni formule qui déborde dans la marge.

Avant cette publication, Claude (Claude Opus 5.5, effort high) a recompilé les trois livres (aucune erreur, aucune
boîte trop pleine), regardé des pages de chacun et comparé quatre des décisions ci-dessus à la numérisation : le A
ronde de la p. 5, le produit tensoriel de la p. 18, le renvoi de la p. 24 et l'égalité (8) de la p. 26. Toutes les
quatre sont conformes à l'imprimé.

Des erreurs peuvent subsister. Merci de les signaler par une issue GitHub.

## Droits

Les droits sur l'œuvre originale appartiennent à son auteur ou à ses représentants ou ayants droit. Notre
transcription, notre traduction, nos corrections et notre composition ont été produites par IA. Elles n'ont pas
d'auteur humain et, selon notre compréhension, ne sont pas protégées par le droit d'auteur ; là où un droit nous
appartiendrait malgré tout, il est versé au domaine public sous CC0 1.0. Tout ce travail reproduit ou traduit l'œuvre
originale : rien ici n'accorde de licence ni n'autorise une reproduction, une traduction ou un autre usage de cette
œuvre. Cette édition est publiée à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit que nous
ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez à sa publication ici, veuillez ouvrir une
issue GitHub et nous la retirerons.

[dip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-fr-diplomatic.pdf
[cor]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-fr-corrected.pdf
[en]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-en.pdf
[zip]: https://github.com/KokunoYumeto/serre-gaga/releases/download/edition-2026-11-19/gaga-sources.zip
