# Primary-reader assessment of the six integrity review flags

The mechanical audit reports 110 PASS, 6 REVIEW and 0 FAIL. Its REVIEW flags are preserved; the following assessments supply the editorial evidence rather than changing the script to manufacture an automatic pass.

## French front matter: four flags

The original article title and author line are centered and bold in the printed page-1 image. Both French source bodies now reproduce that typography. The author line retains the literal name tokens `Jean-Pierre` and `Serre`, and the word `par`; `\MakeUppercase{Serre}` reproduces the printed surname capitals. The title and author typography are recorded in the opening correction rows and were checked again in the second reading against `evidence/p01-headings.png`. The subsequently added title period has its separate medium-confidence evidence in `evidence/p01-title-terminal-mark.png`.

These edits affect the article's printed heading typography. No edition provenance, rights statement, translation credit, model name or source attribution was edited. Both supplied READMEs remain byte-identical to the inputs, including their complete Thomas Waring credit. Main-file provenance comments are unchanged. The full markup differences remain in `frontmatter_changes.diff`, so the change is not represented as byte identity of the whole front-matter block.

## Printed page 11: one residual-difference flag

The final diplomatic body has `Z-voisinage de \mathrm{X}` and the corrected body has `Z-voisinage de x`. The earlier source-correction records contain conflicting decisions about this place. The primary reader inspected `evidence/p11-uppercase-neighbourhood.png` and confirmed the printed capital; it was restored diplomatically in data record 55. The mathematical stalk argument requires a neighbourhood of the point x in the corrected layer. `INHERITED_VERDICTS.tsv` and the SRC-006/SRC-023 crosswalk record both the reversal of the prior transcription decision and the retained original-misprint correction.

## Printed page 36: one residual-difference flag

The top-right node of the Proposition 21 diagram lacks its closing parenthesis in the scan. `evidence/p36-diagram-parenthesis.png` was enlarged and reread. Data record 1770 restores that visible absence in diplomatic French; corrected French and English keep the required closure. UNC-067 and its current verdict identify the reason. The scan does not establish whether the physical defect arose during setting, printing or scanning, and the edition makes no such claim.

## Reconstruction and coverage

Replaying all retained correction rows, with the explicitly withdrawn row as a no-op, exactly reconstructs the current source files from the supplied sources. No unreconstructed source difference remains. The final French residual difference inventory contains 16 local differences on 15 printed pages. The two flags above are covered by explicit manual verdicts; the remaining differences match inherited corrected readings or the newly recorded p. 24 reference repair. Labels, anchors, macros, file layout and the 42 printed-page marker identities pass the mechanical preservation checks.
