# Notes on Serre, GAGA (1956)

These notes were begun only after the page readings, every correction's second reading, recurrence searches, builds and final PDF inspection were complete (PDF gate: 18 November 2026, 14:16 UTC). They do not supply evidence for a printed reading: the supplied scan alone decided those readings. Pages below are Serre's printed pp. 1–42, not the new PDFs' pagination.

Author: GPT-6 Astra (ChatGPT Pro mode; effort setting not exposed). A proof check is a bounded check of the stated implication, with its inputs named, not a certification of every external theorem. The supplied Montpellier notes and Stacks-style chapter are leads and comparison material, not independent authorities. Release status is not a proof verdict. `CHECK_EVENTS.tsv` records the actual kind of work on each note and contextual statement used.

Context paths are relative to the supplied context archive. Labels in `stacks/gaga.tex` are exact; mapping IDs refer to `stacks/gaga_r3/map.csv` and `dec.csv`. `NOTE_CONTEXT_SEARCH.tsv` records searches for every note. Input files and research PDFs are not redistributed. Primary sources [P1] onward are identified at the end; a bibliography-only lead is explicitly distinguished from a verified statement.

## I. Misprints, justified repairs and rejected emendations

### N001 — The missing copula

**Place:** p. 4, no. 2, Definition 1, following paragraph. **Kind:** grammatical misprint.

Printed *si elle continue* becomes *si elle est continue* in corrected French. Continuity is a property of the map, coordinated with the following condition. The parallel definition on p. 3 supplies the copula. No hypothesis is added. SRC-002 is confirmed; diplomatic French retains the omission.

**Confidence:** high, from the image and parallel sentence. **Event:** carried as background without fault found; grammatical collation only.

**Context search:** `continue|holomorphic-map-analytic-subsets|definition-serre-analytic-space`. **Relation:** adds a textual repair to the continuity condition in `stacks/gaga.tex`, `definition-holomorphic-map-analytic-subsets` and `definition-serre-analytic-space`, D000020–D000021.

### N002 — Chart compatibility invokes the first axiom

**Place:** p. 5, no. 2, first paragraph. **Kind:** wrong reference.

Replace printed `(H_II)` by `(H_I)` in the corrected layer. The sentence asserts existence of analytic charts, the first axiom on p. 4. The second asserts separatedness. SRC-022 is confirmed; the definition itself is unchanged.

**Confidence:** high; the two axioms have distinct explicit content. **Event:** targeted proof check.

**Context search:** `Hausdorff|charts|definition-serre-analytic-space`. **Relation:** restates the distinction in `stacks/gaga.tex`, `definition-serre-analytic-space`, D000021; adds the source slip.

### N003 — The coherence conclusion concerns the quotient

**Place:** p. 6, no. 3, Proposition 1 proof. **Kind:** wrong subscript.

The conclusion is coherence of `H_X`, not printed `H_U`. Coherence of `H_U` is already the open-subset input. The quotient `H_X=H_U/A(X)` and coherence of its defining ideal imply the required conclusion on `X`. SRC-003 is confirmed. The analytic vanishing ideal is the printed script `A`, independently of this repair.

**Confidence:** high; quotient and proposition determine the subscript. **Event:** targeted proof check.

**Context search:** `oka-cartan-coherence|quotient|vanishing ideal`. **Relation:** restates the reduction in `stacks/gaga.tex`, `theorem-oka-cartan-coherence`, D000023; adds the exact source defect.

### N004 — Duplicated colon in a chart declaration

**Place:** p. 8, no. 5, Proposition 2 proof. **Kind:** punctuation misprint.

Printed `φ′ : V′ : → U′` becomes `φ′ : V′ → U′`. The second colon has no role between domain and arrow; surrounding declarations use one colon. SRC-005 is confirmed.

**Confidence:** high, from image and syntax. **Event:** carried as background without fault found; punctuation collation only.

**Context search:** `transition maps|proposition-analytification|charts`. **Relation:** adds a source diagnosis to `stacks/gaga.tex`, `proposition-analytification`, D000027, which already uses the intended chart.

### N005 — A neighbourhood of the point

**Place:** p. 11, no. 7, Proposition 5 proof. **Kind:** capital/point-variable misprint.

The image prints *Z-voisinage de X*. Corrected French and English use `x`: vanishing of an ideal stalk gives equality on a neighbourhood of that point, not on the entire variety. The diplomatic capital was restored in this run; the earlier record asserting a printed lowercase letter was reversed (SRC-006/SRC-023).

**Confidence:** high for image and local argument. **Event:** targeted proof check.

**Context search:** `zariski-dense-open-analytically-dense|neighbourhood|stalk`. **Relation:** restates the local step in `stacks/gaga.tex`, `lemma-zariski-dense-open-analytically-dense`, D000035; differs from the earlier transcription verdict.

### N006 — Missing component index on a fraction field

**Place:** p. 14, no. 8, Proposition 9 proof. **Kind:** omitted index.

The factors of the total fraction ring of `A′` are `K′_i`, not unindexed `K′`. Each was defined as the fraction field of `A′/p′_i`; the next argument compares `K_i` and `K′_i` component by component. SRC-008 is confirmed.

**Confidence:** high; definition, product and degree calculation agree. **Event:** targeted proof check.

**Context search:** `K'_i|total-fractions-reduced|analytic-isomorphism-algebraic`. **Relation:** restates the indexed product in `stacks/gaga.tex`, `proposition-analytic-isomorphism-algebraic` and `lemma-total-fractions-reduced`, D000041–D000042.

### N007 — The third inverse-image sheaf needs its prime

**Place:** p. 17, no. 9, Proposition 10 proof. **Kind:** omitted prime.

The final sheaf in the inverse-image sequence on `X^h` is `F′_3`, not `F_3`. All terms are inverse images before tensoring with the analytic structure sheaf. The next tensor sequence confirms the prime. SRC-009 is confirmed.

**Confidence:** high; base space and parallel terms determine it. **Event:** targeted proof check.

**Context search:** `inverse image|analytification-exact-faithful-coherent|module-stalks`. **Relation:** restates `stacks/gaga.tex`, `lemma-analytification-exact-faithful-coherent`, D000045; adds the source diagnosis.

### N008 — Tensoring over A is already correct

**Place:** p. 18, no. 10, Proposition 11. **Kind:** rejected emendation, SRC-024.

Restore printed `E⊗_A B′` in corrected French and English. Here `A′=A/a` and both factors are `A′`-modules. An `A`-balanced bilinear map from `E×B′` is automatically `A′`-balanced: lift an element of `A′` to `A`; different lifts act identically. The converse is immediate. Hence `E⊗_A B′ ≅ E⊗_{A′} B′` canonically. The inherited change made a valid expression more explicit; it did not repair an error.

**Confidence:** high; established by the universal property. **Event:** targeted proof check.

**Context search:** `pushforward-closed-immersion|Associativity of tensor|quotient`. **Relation:** restates the tensor identifications in `stacks/gaga.tex`, `lemma-analytification-pushforward-closed-immersion`, D000047; differs from the inherited necessity claim.

### N009 — Closing a participial parenthesis

**Place:** p. 22, no. 13, final paragraph of Theorem 1 proof. **Kind:** punctuation repair.

Corrected French adds the closing comma after `F` in *Ce résultat, étant valable pour tout faisceau algébrique cohérent F, s'applique…*. The first comma opens that participial phrase. Diplomatic French retains the omission; SRC-011 is confirmed. The mathematical content is unchanged.

**Confidence:** high for image and syntax. **Event:** carried as background without fault found; punctuation collation only.

**Context search:** `descending induction|cohomology|surjective`. **Relation:** adds a textual repair to the proof of `theorem-gaga-cohomology` in `stacks/gaga.tex`, D000050/D000053.

### N010 — Algebraic global sections live on X

**Place:** p. 23, no. 14, Theorem 2 proof. **Kind:** wrong base space.

The first inline group is `H^0(X,A)`, with `A` the algebraic internal-Hom sheaf. Printed `H^0(X^h,A)` mixes an algebraic sheaf with the analytic space and contradicts the preceding display. The later analytic group is `H^0(X^h,A^h)`. SRC-012 is confirmed.

**Confidence:** high; domain and comparison map fix the expression. **Event:** targeted proof check.

**Context search:** `proof-gaga-fully-faithful|internal-hom|H^0`. **Relation:** restates the identifications in `stacks/gaga.tex`, proof of `theorem-gaga-fully-faithful`, D000051/D000056.

### N011 — The vanishing reference is FAC

**Place:** p. 24, no. 16, Lemma 7 proof. **Kind:** wrong bibliography number.

Correct `[8]` to `[18]` before *no. 65, proposition 7*. Reference 8 is Dolbeault's note; reference 18 is FAC. Its primary scan was opened and printed p. 258 inspected: no. 65, Proposition 7 states finite dimensionality of coherent cohomology for `q≥0` and vanishing after a sufficiently large twist for `q>0`. This is the input used here. [P1]

**Confidence:** high; exact primary statement and page verified, including the image's `≥`. **Event:** targeted proof check of reference and application, not a re-proof of FAC vanishing.

**Context search:** `hyperplane-analytic-serre-vanishing|coherent-projective|lemma:7`. **Relation:** restates the input in `stacks/gaga.tex`, `lemma-hyperplane-analytic-serre-vanishing`, D000060; adds the reference repair.

### N012 — Equation (8) is redundant but true

**Place:** p. 26, no. 16, Lemma 8 proof, equation (8). **Kind:** rejected emendation, SRC-013.

The print has `dim H^1(M(n))` at both ends. The inherited correction substituted `M(n−1)` at the left; this run restores the print in corrected French and English. The dimensions have stabilized, and the middle dimension is squeezed between equal consecutive values. The printed equality is true and gives exactly the equality needed to turn the next surjection into an isomorphism. A stronger display is not a necessary correction.

**Confidence:** high, after tracing (5)–(9). **Event:** targeted proof check.

**Context search:** `stabilize|projective-analytic-global-generation|L_n`. **Relation:** restates the argument in `stacks/gaga.tex`, `lemma-projective-analytic-global-generation`, D000061; differs from the inherited error diagnosis.

### N013 — The semilinear map starts with differentials on X

**Place:** p. 28, no. 18, Proposition 12 proof. **Kind:** wrong coefficient sheaf.

The source of the Čech cohomology map is `H^q(U,Ω^p(X))`. The print inserts `X^σ` in that source once although `U` covers `X`; the target is on the conjugated covering with `Ω^p(X^σ)`. Applying `σ` to coefficients defines a semilinear cochain map between precisely these objects. SRC-014 is confirmed.

**Confidence:** high; the preceding cochain map determines both coefficients. **Event:** targeted proof check.

**Context search:** `semilinear|conjugate-smooth-projective-betti-numbers|Omega`. **Relation:** restates `stacks/gaga.tex`, `proposition-conjugate-smooth-projective-betti-numbers`, D000064; adds the misplaced-superscript diagnosis.

### N014 — A damaged word in Chow's theorem

**Place:** p. 29, no. 19, Proposition 13. **Kind:** defective word.

The enlarged image reads *sous-ense.nble*; corrected French uses *sous-ensemble*. The diplomatic layer preserves the visible defect. SRC-015 is confirmed, without deciding whether type, ink or scanning caused it.

**Confidence:** high for visible reading and intended word; physical cause unresolved. **Event:** carried as background without fault found; textual collation only.

**Context search:** `chow-closed-analytic-projective|closed reduced|prop:13`. **Relation:** adds a textual diagnosis to `stacks/gaga.tex`, `theorem-chow-closed-analytic-projective`, D000068.

### N015 — A stop interrupts an associated-bundle construction

**Place:** p. 33, no. 20, Proposition 19 proof. **Kind:** extraneous punctuation.

Remove the stop after `P×_H G` before `(resp. P_0)`. The alternative and following fiber-type clause belong to the same sentence. SRC-016 is confirmed; the construction is unchanged.

**Confidence:** high for the image and sentence structure. **Event:** carried as background without fault found; punctuation collation only.

**Context search:** `algebraize-reduction-structure-group|associated bundle|P_0`. **Relation:** adds a textual repair to `stacks/gaga.tex`, `proposition-algebraize-reduction-structure-group`, D000077.

### N016 — The diagram node lacks a closing parenthesis

**Place:** p. 36, no. 21, Proposition 21 diagram. **Kind:** incomplete mathematical punctuation.

The top-right printed node is `T(L_1`; the corrected node is `T(L_1)`, paired with `T′(L_1)` below. Diplomatic French now reproduces the absence; corrected French and English retain the closure. UNC-067 is resolved as an observed defect without assigning its physical cause.

**Confidence:** high for image and required syntax. **Event:** targeted proof check of the diagram's node identification.

**Context search:** `gaga:prop:21|pseudo-coherence-and-base-change-ext|D000003`. **Relation:** adds a source diagnosis to map unit `gaga:prop:21`, D000003. The contextual chapter delegates this appendix result to the mapped algebra statement.

### N017 — Both closing parentheses are legitimate

**Place:** p. 36, no. 22, Proposition 22(a), (a′). **Kind:** rejected normalization, SRC-017.

Retain both closing parentheses in `(resp. a′))`: one closes the enumerator `a′)`, the other the parenthetic phrase. This is independent of the genuinely missing parenthesis in N016.

**Confidence:** high, from parsing the two levels. **Event:** carried as background without fault found; syntactic collation only.

**Context search:** `gaga:prop:22|universally-injective|D000006`. **Relation:** adds a negative textual verdict to map unit `gaga:prop:22`, D000006; the flat-pair criterion is unchanged.

### N018 — The dot inside Kodaira's title

**Place:** p. 41, bibliography [11]. **Kind:** anomalous punctuation.

The image has a small baseline dot after *restricted type*. Corrected French removes it before the lower-case explanatory parenthesis; diplomatic French retains it. SRC-018 is confirmed as a repair of the visible title, without diagnosing how the mark arose. N068 distinguishes this title check from verification of the cited Theorems 7 and 8.

**Confidence:** high for visible mark and title syntax; physical origin unresolved. **Event:** carried as background without fault found.

**Context search:** `Kodaira|line-bundles-gaga|gaga:bib:11`. **Relation:** adds a bibliographic repair to map unit `gaga:bib:11`; contextual `remark-line-bundles-gaga` does not verify the physical defect.

### N019 — An abbreviation point in Rosenlicht's citation

**Place:** p. 41, bibliography [13]. **Kind:** abbreviation punctuation.

Corrected French restores `Amer.` in *Amer. J. of Maths.*; diplomatic French retains the missing point. Reference [6] supplies the same journal abbreviation as an internal comparator. SRC-019 is confirmed without modernizing the title.

**Confidence:** high from the two printed entries. **Event:** carried as background without fault found; bibliographic collation only.

**Context search:** `Rosenlicht|gaga:bib:13|rational-section-condition-examples`. **Relation:** adds a textual diagnosis to map unit `gaga:bib:13`; N073 treats the theorem-level connection.

### N020 — The title's terminal mark remains uncertain

**Place:** p. 1, title. **Kind:** uncertain physical reading.

A detached baseline mark after the last word is transcribed as a period in both French titles. It is visible, but one scan cannot establish whether it belongs to the type, stray ink or reproduction. The two ledger records remain medium confidence. No mathematical claim depends on it.

**Confidence:** medium; an isolated physical mark is ambiguous. **Event:** carried as background without fault found; image reading only.

**Context search:** `title|Géométrie algébrique|second pass`. **Relation:** adds a residual uncertainty to the edition records; neither the programme nor the Stacks mapping resolves a physical mark on the supplied scan.

## II. Proof obligations and bounded checks, in printed order

### N021 — The introductory comparison of differential forms

**Place:** p. 1, Introduction. **Kind:** announced background claim.

For smooth projective `X`, the regular differential sheaf `Ω_X^p` is coherent and its analytification is the sheaf of holomorphic p-forms: this can be checked in smooth coordinates, with the differential of the coordinate changes giving the same transition matrices. Theorem 1 in degree zero then identifies global regular and holomorphic forms. The traditional phrase “everywhere of the first kind” must refer to regularity at every point. The introduction is announcing a consequence, so using the later theorem here explains the claim without inserting it as an input to that theorem. This argument does not identify arbitrary meromorphic forms with regular forms on singular spaces.

**Confidence:** high, conditional on Theorem 1 and the smooth-coordinate identification. **Event:** targeted proof check.

**Context search:** `holomorphic.*forms|Omega|conjugate-smooth-projective`. **Relation:** restates the differential-sheaf identification in `stacks/gaga.tex`, `proposition-conjugate-smooth-projective-betti-numbers`; adds the explicit restriction on the introductory language.

### N022 — Local closedness and local compactness

**Place:** p. 3, no. 1, basic analytic-subset properties. **Kind:** omitted elementary proof.

At each point of an analytic subset choose the neighbourhood on which finitely many holomorphic functions define it. Their common zero set is closed in that neighbourhood. A smaller relatively compact Euclidean neighbourhood gives local compactness of the subset. The definition does not require the subset to be globally closed in affine space. For a product, concatenate defining equations in the two coordinate blocks; the subspace topology is the product topology. These arguments prove the properties directly from the local definition, without invoking coherence.

**Confidence:** high; explicit local equations suffice. **Event:** targeted proof check.

**Context search:** `locally closed|locally compact|analytic-subset-basic-properties`. **Relation:** restates `stacks/gaga.tex`, `lemma-analytic-subset-basic-properties`, D000019.

### N023 — The coordinate test for holomorphic maps

**Place:** pp. 3–4, no. 1, definition of a holomorphic map. **Kind:** implicit equivalence.

If pullback preserves holomorphic germs, apply it to the target's finitely many coordinate functions. Conversely, lift the holomorphic coordinate germs on the source to ambient holomorphic functions on one common neighbourhood. A target holomorphic germ is the restriction of an ambient holomorphic germ; its composition with those lifts is holomorphic after shrinking. This proves the pullback condition and also continuity. The same construction proves closure under composition and holomorphicity of product maps. It explains the coordinate criterion but does not justify removing the printed continuity condition.

**Confidence:** high; finitely many lifts and composition give both implications. **Event:** targeted proof check.

**Context search:** `coordinate criterion|holomorphic-map-analytic-subsets|composition`. **Relation:** restates `stacks/gaga.tex`, `definition-holomorphic-map-analytic-subsets` and `lemma-serre-analytic-subspaces-products`, D000019–D000020.

### N024 — Reducedness and the instruction to transpose FAC

**Place:** pp. 4–5, no. 2, Definition 1 and final instruction. **Kind:** scope and omitted constructions.

The structure sheaf is a sheaf of actual complex-valued functions. A germ whose power is zero vanishes pointwise and is zero, so the local rings are reduced. Analytic subspaces inherit the restriction-and-image sheaf in charts, and chart changes identify it; products use product charts and the preceding coordinate criterion. Those are the constructions required to transpose the elementary FAC statements cited in nos. 34–35. Nilpotent thickenings cannot be inserted into this definition merely by replacing “subset” by a modern ringed-space word. Their later inclusion is a separate extension (N084).

**Confidence:** high for reducedness and these constructions; no assertion that every uncited FAC consequence has been reproved. **Event:** targeted proof check.

**Context search:** `reduced|serre-analytic-subspaces-products|definition-serre-analytic-space`. **Relation:** restates the explicit reduced-scope warning and product lemma in `stacks/gaga.tex`, D000020–D000021.

### N025 — What the Oka–Cartan reduction actually uses

**Place:** pp. 5–6, no. 3, Proposition 1. **Kind:** cited analytic input and short reduction.

The open-subset theorem supplies coherence of holomorphic functions and of vanishing ideals in an open subset of affine complex space. For closed analytic subsets `Y⊂X⊂U`, use `H_X=H_U/A(X)` and `A_X(Y)=A_U(Y)/A_U(X)`. Coherent kernels, cokernels and change of coefficient ring then give both assertions on `X`. This reduction is checked here; Oka–Cartan coherence itself is an external analytic theorem, cited by Serre as [1], Theorems 1–2 and [2], Exposés XV–XVI. Finite locally free sheaves are consequently coherent. The automorphic-function example needs the specific construction in the cited seminar; it is not a consequence of the word “automorphic” alone.

**Confidence:** high for the reduction; the named analytic theorem is carried as an explicit dependency. **Event:** targeted proof check.

**Context search:** `oka-cartan-coherence|automorphic|coherent-analytic-modules`. **Relation:** restates `stacks/gaga.tex`, `theorem-oka-cartan-coherence` and `remark-examples-coherent-analytic-modules`, D000022–D000023.

### N026 — Reconstructing a germ from its local analytic algebra

**Place:** p. 6, no. 4. **Kind:** “easily seen” assertion.

Use local complex-algebra maps, preserving the complex scalars. Present the rings as quotients of convergent power-series rings. The images of coordinate germs give a holomorphic map germ in the opposite direction; finitely many defining relations force its image into the target analytic subset. A local homomorphism is continuous for maximal-ideal powers. Its agreement with substitution on polynomials therefore extends to the completed series rings, and injectivity into completion identifies the convergent germs. Applying the construction to an inverse algebra map gives inverse analytic germs. Specifying the scalar structure and continuity argument prevents an abstract-ring interpretation from silently entering the claim.

**Confidence:** high, using Noetherianity, finite equations and separated completion. **Event:** targeted proof check.

**Context search:** `analytic-germ-local-algebra|convergent|local homomorphism`. **Relation:** adds the scalar and continuity justification to the shorter proof in `stacks/gaga.tex`, `lemma-analytic-germ-local-algebra`, D000024.

### N027 — Regular local rings and simple analytic points

**Place:** p. 6, no. 4, simple-point criterion. **Kind:** cited analytic theorem.

The easy direction identifies the local ring at a smooth point with a convergent power-series ring, whose embedding dimension and Krull dimension agree. For the converse, one must use the analytic implicit-function theorem: a basis of the cotangent space gives minimal coordinates, and regularity forces enough independent equations to eliminate the remaining coordinates. The conclusion is an analytic germ isomorphic to affine complex space of the stated dimension. Merely knowing an abstract Noetherian local ring is regular would not construct such a complex-analytic germ; the convergent presentation is essential.

**Confidence:** high for the dependency analysis; the analytic implicit-function theorem is not reproved here. **Event:** carried as background without fault found.

**Context search:** `simple-point-regular-local|implicit function|regular analytic`. **Relation:** restates the explicit external dependency in `stacks/gaga.tex`, `lemma-simple-point-regular-local`, D000024.

### N028 — Components and analytic dimension

**Place:** pp. 6–7, no. 4. **Kind:** cited local structure results.

Reduced Noetherian local algebra gives finitely many minimal primes with intersection zero. Identifying those primes with irreducible analytic germs requires the local analytic Nullstellensatz. For an irreducible germ, a finite analytic projection gives a finite extension of a convergent power-series ring in `r` variables; dimension invariance under integral finite extension then gives Krull dimension `r`. Identifying this `r` with half the local topological dimension is another analytic dimension theorem. The algebraic minimal-prime calculation alone does not prove that topological assertion.

**Confidence:** high for the separation of dependencies; the analytic projection and dimension theorems are background. **Event:** carried as background without fault found.

**Context search:** `components-dimension-analytic-space|topological dimension|parameter theorem`. **Relation:** restates `stacks/gaga.tex`, `lemma-components-dimension-analytic-space`, D000024; highlights which part cannot be supplied by an algebra-only citation.

### N029 — Analytic charts glue, but separatedness must be checked

**Place:** pp. 8–9, no. 5, Lemma 1 and Proposition 2. **Kind:** gluing proof.

A regular map is locally a tuple of polynomial quotients with nonvanishing denominators, hence holomorphic. The algebraic transition maps and their inverses therefore identify analytic structures on overlaps and satisfy the cocycle relation. To obtain a Hausdorff space, check the diagonal: on each product of chart domains its inverse image is the algebraic overlap graph, closed by the separatedness axiom for the algebraic variety. A Zariski-closed set is analytically closed. The chart products cover the product space, so the diagonal is closed. This is the missing step if one says only “glue the charts.”

**Confidence:** high; chart transitions and the local diagonal test prove the assertion. **Event:** targeted proof check.

**Context search:** `Hausdorff axiom|diagonal|proposition-analytification`. **Relation:** restates the explicit diagonal argument in `stacks/gaga.tex`, `proposition-analytification`, D000025–D000027.

### N030 — The intrinsic definition on p. 9

**Place:** p. 9, no. 5, Remark. **Kind:** equivalence left to the reader.

Interpret the topology as generated on Zariski-open chart domains by regular functions, with those domains open. On an affine chart, the coordinate functions are regular; their inverse images of Euclidean opens generate the usual subspace topology. Every regular function is continuous for that topology, proving equality of the two topologies. For germs, the analytic closure of the regular coordinate algebra consists of restrictions of convergent holomorphic expressions in the coordinates; these are precisely the holomorphic germs of the chart. Finite many charts also give local compactness and a countable compact exhaustion. Product compatibility and locally closed subvariety compatibility follow in the same charts.

**Confidence:** high with the stated interpretation of the local topology and analytic closure. **Event:** targeted proof check.

**Context search:** `analytification-properties|countable|analytic charts`. **Relation:** adds a direct proof of the intrinsic-definition equivalence to `stacks/gaga.tex`, `lemma-analytification-properties`, D000025; the supplied chapter states the chart construction instead.

### N031 — The radical-ideal step in the local comparison

**Place:** pp. 9–10, no. 6, Propositions 3–4. **Kind:** nontrivial dependency.

For affine space, polynomial-local and convergent local rings have the same formal-power-series completion. The analytic Nullstellensatz identifies the ideal vanishing on the germ with the radical of the extended algebraic ideal. Removing that radical needs more: the completion of the reduced algebraic local quotient is reduced (Serre's cited Chevalley input). If a germ's power lies in the extended ideal, reducedness of the completed quotient places the germ in the completed ideal; contraction from the faithfully flat completion then places it in the original analytic ideal. Only after this affine-space step may one pass to quotients to prove the general completion isomorphism. Flatness alone does not preserve arbitrary reduced quotients.

**Confidence:** high for the implication chain; analytic Nullstellensatz and reducedness of the algebraic completion are named inputs. **Event:** targeted proof check.

**Context search:** `analytification-closed-ideal|excellent|completion-reduced`. **Relation:** restates the proof in `stacks/gaga.tex`, `proposition-analytification-closed-ideal`, D000028/D000030. That chapter supplies a modern excellence/Nagata route for the reduced-completion input; it is an extension of the dependency explanation, not evidence for a reading.

### N032 — Equal completions imply faithful flatness here

**Place:** p. 11, no. 6, Corollaries 1–3. **Kind:** use of the appendix.

The rings are Noetherian local and the map is local. Their common completion is faithfully flat over each. To test injectivity after tensoring a module map with the analytic ring, tensor again with that completion; injectivity there follows from its flatness over the algebraic ring, and faithful flatness over the analytic ring detects the kernel. This proves flatness, and a flat local map is faithfully flat. Dimension equality uses invariance of the dimension of a Noetherian local ring under completion. For an irreducible variety over `C`, the local ring at every classical point has the variety's dimension, giving Corollary 3. These conclusions depend on locality and Noetherian hypotheses, not just a bare ring isomorphism somewhere between completions.

**Confidence:** high; the descent argument is explicit. **Event:** targeted proof check.

**Context search:** `analytification-local-faithfully-flat|analytification-local-dimension|completed-local-rings`. **Relation:** restates `stacks/gaga.tex`, those three local-comparison labels, D000029/D000031–D000033; see also N080–N082.

### N033 — Density and injectivity of regular germs

**Place:** p. 11, no. 7, Proposition 5 and Remark. **Kind:** equivalence left implicit.

Injectivity of regular germs into holomorphic germs gives the printed proof: an analytic neighbourhood contained in a proper algebraic closed subset would force its algebraic ideal stalk to vanish, contradicting density. Conversely, if a nonzero regular germ vanished analytically near `x`, choose an irreducible component through `x` on which it is not identically zero. Its nonvanishing locus is Zariski open and dense on that component, so Proposition 5 applied to the component forces it to meet every analytic neighbourhood of `x`, a contradiction. The reduction-to-a-curve suggestion needs an algebraic curve through `x` not contained in the zero locus, followed by normalization and the one-variable identity theorem; it is a separate route, not established merely by naming curves.

**Confidence:** high for the two implications; the curve route is a specified proof requirement. **Event:** targeted proof check.

**Context search:** `zariski-dense-open-analytically-dense|injective|curve`. **Relation:** adds the converse and the curve-route obligations to `stacks/gaga.tex`, `lemma-zariski-dense-open-analytically-dense`, D000035.

### N034 — Completeness versus analytic compactness

**Place:** pp. 11–12, no. 7, Proposition 6. **Kind:** cited Chow-lemma argument.

Chow's lemma supplies a proper surjective quasi-projective modification. Its projective closure provides a compact ambient analytic space. If the original variety is complete, the quasi-projective source is proper, so its immersion in projective space is closed and its compact image covers the original space. Conversely, compactness of the original space makes the modification's closed graph compact in the product with the projective closure; its projection is both closed and dense in that closure, hence the whole closure. The modification is then projective and proper surjectivity descends completeness. The essential inputs are the precise proper version of Chow's lemma, separatedness and N033, not an assumption that every complete variety is projective.

**Confidence:** high for the reduction, with Chow's lemma as an external algebraic input. **Event:** targeted proof check.

**Context search:** `proper-if-and-only-if-compact|Chow|closed graph`. **Relation:** restates `stacks/gaga.tex`, `proposition-proper-if-and-only-if-compact-analytification`, D000036; the contextual scheme formulation makes the properness steps explicit.

### N035 — A dense image contains a dense open set

**Place:** pp. 12–13, no. 7, Lemma 2 and Proposition 7. **Kind:** constructibility input.

For each component of the target met densely by an image component, the generic-image theorem gives a nonempty open contained in that image. Remove other target components and take the union of these opens. This produces an open dense subset of the full image closure; finiteness of the component set matters. Analytic density of that open by Proposition 5 then identifies analytic and Zariski closures of the image. A modern equivalent proof uses constructibility of a finite-type image and the fact that a dense constructible subset of a Noetherian space contains a dense open subset. An arbitrary dense subset need not contain an open set.

**Confidence:** high for the finite-component and closure arguments; constructibility is the named input. **Event:** targeted proof check.

**Context search:** `dense-image-contains-open|proposition-image-closure|chevalley`. **Relation:** restates `stacks/gaga.tex`, `lemma-dense-image-contains-open` and `proposition-image-closure`, D000037–D000038.

### N036 — Why an analytic inverse is algebraic

**Place:** pp. 13–15, no. 8, Propositions 8–9. **Kind:** proof dependency check.

An algebraic graph of a holomorphic map projects bijectively to the source with holomorphic inverse. Proposition 7 makes that projection a Zariski homeomorphism. At corresponding points, embed both algebraic local rings `A⊂A′` in the common analytic local ring `B`. The componentwise degree argument in N037 identifies their total fraction rings. For `h∈A′`, write `h=g/s` with `g,s∈A` and `s` a nonzerodivisor. Since `g=sh` in `B`, faithful flatness gives `g∈sB∩A=sA`; cancel `s` in `A′` to get `h∈A`. This proves equality of local rings and hence algebraicity of the inverse in Serre's classical variety category. Bijectivity alone would not suffice, as the normalization of a cusp shows.

**Confidence:** high, with N037 and the flat contraction property explicit. **Event:** targeted proof check.

**Context search:** `analytic-isomorphism-algebraic|algebraic-graph-holomorphic-regular|sB`. **Relation:** restates `stacks/gaga.tex`, the two corresponding propositions, D000040–D000041. Its extra scheme-point argument is beyond the classical-point step checked here.

### N037 — Generic fiber size equals the field degree

**Place:** p. 14, no. 8, Proposition 9, footnote (3). **Kind:** unproved generic-degree assertion.

For a dominant map of irreducible varieties of equal dimension, the function-field extension is finite. Shrink the target so the map is finite, then shrink again to make the finite algebra free and its discriminant invertible. In characteristic zero the field extension is separable, so this yields a finite étale map of rank equal to the field degree. Every closed fiber over `C` has exactly that many reduced points. A bijection of classical points therefore forces degree one. The separability step is indispensable: in positive characteristic Frobenius is bijective on algebraically closed points and can have larger purely inseparable function-field degree.

**Confidence:** high; the necessary finite and étale shrinkings are identified. **Event:** targeted proof check.

**Context search:** `finite-degree|generic-flatness|separable`. **Relation:** restates the expanded argument in `stacks/gaga.tex`, proof of `proposition-analytic-isomorphism-algebraic`, D000041; makes the characteristic-zero boundary explicit.

### N038 — Total fractions of a reduced ring with finitely many components

**Place:** pp. 14–15, no. 8, Lemma 3. **Kind:** algebraic proof check.

Let the minimal primes be the finite family `p_i`, with intersection zero, and invert the complement `S` of their union. A prime disjoint from `S` is contained in the finite union of the `p_i`; prime avoidance puts it in one of them, hence it equals that minimal prime. Thus the localized ring has exactly the maximal ideals `p_i A_S`. Their intersection is zero, and distinct maximal ideals are comaximal. The Chinese remainder theorem gives the product of the quotients. Each quotient is a field containing `A/p_i` and contained in its fraction field, and every nonzero element of `A/p_i` becomes invertible there; it is `K_i`. The finite-prime assumption, rather than Noetherianity by itself, is the operative hypothesis of this lemma.

**Confidence:** high; localization, prime avoidance and CRT prove the statement. **Event:** targeted proof check.

**Context search:** `total-fractions-reduced|minimal primes|total-ring-fractions`. **Relation:** restates `stacks/gaga.tex`, `lemma-total-fractions-reduced`, D000042, with its algebraic steps written out.

### N039 — The topology on the inverse-image sheaf

**Place:** p. 16, no. 9, construction preceding Definition 2. **Kind:** verification left to the reader.

Regard a sheaf as its étalé space. Above a Zariski open set, a local section is an open chart on which the projection is a homeomorphism. Pulling that chart back along the continuous identity from the finer analytic topology makes it a local homeomorphism over the analytic open set. These pulled-back charts are precisely the topology induced by the graph embedding into `X^h×F`. Consequently the new object is a sheaf, its stalk at each classical point is the old stalk, and it is the inverse-image sheaf. The later tensor product changes the coefficient ring; the topology change alone does not do so.

**Confidence:** high, by the étalé-space chart description. **Event:** targeted proof check.

**Context search:** `inverse image|analytification-module|module-stalks`. **Relation:** adds the topological construction behind `stacks/gaga.tex`, `definition-analytification-module` and `lemma-analytification-module-stalks`, D000043–D000044.

### N040 — Exactness, injectivity and coherence of analytification

**Place:** pp. 16–17, no. 9, Proposition 10. **Kind:** local-to-global check.

The stalk formula is `F_x⊗_{O_x} H_x`. Flatness makes short exact sequences remain exact; the flat-pair property makes the natural map from each original stalk injective. A coherent algebraic sheaf has a finite local presentation, whose analytification is a finite presentation over the coherent analytic structure sheaf, hence coherent. In the modern scheme formulation, detection of zero for coherent sheaves follows because a nonzero coherent support contains a closed point. This last argument should not be silently applied to arbitrary sheaves on all scheme points; Serre's underlying space consists of classical points.

**Confidence:** high; stalkwise flatness and finite presentations give the assertions. **Event:** targeted proof check.

**Context search:** `analytification-exact-faithful-coherent|finitely presented|closed point`. **Relation:** restates `stacks/gaga.tex`, `lemma-analytification-exact-faithful-coherent`, D000045; adds the distinction between the classical and scheme-point formulations of faithfulness.

### N041 — Closed extension by zero and its coefficients

**Place:** pp. 17–18, no. 10, Proposition 11. **Kind:** implicit sheaf-theoretic steps.

For a closed inclusion `i:Y→X`, direct image is extension by zero: its stalks are the original stalks on `Y` and zero off `Y`. It is exact, and modules on `Y` identify with modules on `X` annihilated by the defining ideal. Coherence follows from the coherent quotient structure sheaf. At a point of `Y`, put `A′=A/a` and `B′=B/aB`. The two analytifications of the extended sheaf have stalks canonically identified through `E⊗_A B ≅ E⊗_{A′} B′`; the ideal kills `E`. These stalk maps come from the natural sheaf map, so they glue, rather than merely giving noncanonical abstract isomorphisms. N008 explains the harmless alternate base in the print.

**Confidence:** high, using the closed-inclusion stalk description and tensor universal property. **Event:** targeted proof check.

**Context search:** `pushforward-closed-immersion|coherent-analytic-closed-immersion|annihilated`. **Relation:** restates the two closed-immersion lemmas in `stacks/gaga.tex`, D000046–D000047/D000058.

### N041A — Closed extension by zero preserves cohomology

**Place:** p. 20, no. 13, opening reduction to projective space. **Kind:** implicit cohomological bridge.

For a closed inclusion `i:Y→X`, direct image on sheaves of abelian groups is exact: its stalks are the original stalks on Y and zero off Y. It also preserves flasque sheaves, since restrictions of its sections are restrictions on intersections with Y. Apply `i_*` to a flasque resolution and use `Γ(X,i_*F)=Γ(Y,F)`. This gives `H^q(X,i_*F)=H^q(Y,F)` in every degree. The argument works for both the Zariski and analytic topologies. Combined with N041's compatibility of analytification and closed direct image, it justifies the comparison theorem's projective-space reduction.

**Confidence:** high; the same flasque resolution computes the two groups. **Event:** targeted proof check.

**Context search:** `cohomology-and-closed-immersions|closed-immersion|projective reduction`. **Relation:** expands the cohomology step explicitly invoked in `stacks/gaga.tex`, proof of `theorem-gaga-cohomology`, D000050, rather than deriving it from coherence alone.

### N042 — Compatibility with the connecting homomorphism

**Place:** pp. 18–19, no. 11, comparison map and square. **Kind:** abbreviated naturality proof.

For a short exact sequence, choose a representative cocycle in the quotient sheaf, lift it locally to the middle sheaf, and apply the Čech differential; the result is a cocycle in the kernel sheaf representing the boundary. Analytification carries the lifts, restrictions and differentials to their analytic counterparts. Refining the cover if necessary does not change the class. This proves commutativity of the boundary square, including its sign, when the same Čech convention is used on both sides. Affine acyclicity computes the algebraic groups from suitable covers; alternatively naturality of derived adjunction yields the same comparison. An abstract vector-space isomorphism would not be enough for the later five-lemma arguments.

**Confidence:** high for the cocycle calculation; sheaf-cohomology/Čech comparison is an explicit input. **Event:** targeted proof check.

**Context search:** `cohomology-map-functorial|connecting maps|derived adjunction`. **Relation:** restates `stacks/gaga.tex`, `lemma-analytification-cohomology-map-functorial`, D000048, with the elementary calculation behind its derived formulation.

### N043 — What fails without a global hypothesis

**Place:** pp. 19–20, no. 12, Theorems 1–3 and Remark 1. **Kind:** scope test.

On affine one-space, degree-zero comparison for the structure sheaf is the inclusion of polynomials into entire functions. The entire function `e^z` is not a polynomial, as its derivatives never become zero. Thus the comparison and full faithfulness already fail in this elementary nonproper example. This proves that one cannot discard the global hypothesis; it does not prove that projectivity is the sharp hypothesis. Proper schemes are covered by the later extension in N084. Coherence also matters: the theorem is not an equivalence of arbitrary sheaves of functions or of all analytic spaces.

**Confidence:** high; explicit non-surjective map. **Event:** targeted proof check.

**Context search:** `projectivity-essential|entire functions|proper-projective`. **Relation:** restates `stacks/gaga.tex`, `remark-gaga-projectivity-essential`, D000049; adds the distinction between a necessary global restriction and the sharp proper formulation.

### N044 — Why the intermediate inverse-image comparison is different

**Place:** p. 20, no. 12, Remark 2. **Kind:** obstruction and hidden limit input.

On irreducible `X`, the sheaf of rational functions `K` is flasque for the Zariski topology, so its higher cohomology vanishes. Its inverse image on `X^h` is the constant sheaf with value `K`. On a compact triangulable analytic variety, that sheaf has cohomology equal to ordinary cohomology with those coefficients, of `K`-dimension the Betti number. A projective example with positive higher Betti number therefore separates the two theories. To deduce the existence of a coherent counterexample from the hypothetical assertion for every coherent sheaf, one also needs the expression of `K` as a filtered union of coherent subsheaves and the relevant compatibility of cohomology with that limit. Serre cites [19], §2 for this bridge; it is not proved simply by the constant-sheaf calculation.

**Confidence:** high for the obstruction; the filtered-limit bridge is a named dependency. **Event:** targeted proof check.

**Context search:** `comparison-factorization|flasque|Betti`. **Relation:** adds the limit requirement to `stacks/gaga.tex`, `remark-gaga-comparison-factorization`, D000049, which records the rational-function obstruction.

### N045 — The analytic starting calculation on projective space

**Place:** pp. 20–21, no. 13, Lemma 4 and footnote (4). **Kind:** analytic input left to references.

For projective space, algebraic cohomology of `O` is computed by FAC. Analytically, constants give `H^0`, while Dolbeault plus the projective-space Hodge calculation gives `H^{0,q}=0` for `q>0`. This analytic calculation must be established independently of GAGA to avoid circularity. The footnote sketches an alternative: use the standard coordinate cover, Laurent expansions and an explicit Čech calculation. To carry it out one must prove cover/intersection acyclicity and the convergence of the decomposition of Laurent series. Its `H^q(X,O)` notation is read in that analytic calculation's context; it was not silently emended in the edition.

**Confidence:** high for identifying the required inputs; neither full Dolbeault theory nor the unpublished Laurent calculation is reproved here. **Event:** carried as background without fault found.

**Context search:** `projective-structure-sheaf-comparison|Dolbeault|cohomological-dimension`. **Relation:** restates the explicit analytic input in `stacks/gaga.tex`, `lemma-projective-structure-sheaf-comparison`, D000054.

### N046 — The five-lemma step works for all integer twists

**Place:** p. 21, no. 13, Lemma 5. **Kind:** abbreviated diagram argument.

The hyperplane sequence relates `O(n−1)`, `O(n)` and `O_E(n)` and remains exact after analytification. Induction on the projective dimension supplies comparison for the hyperplane in every degree and every twist. In the two long exact sequences, a five-term window then shows that comparison for `O(n)` in all degrees is equivalent to comparison for `O(n−1)` in all degrees. Start at `n=0` and move in both directions. At degree zero, the sequences start with zero, so the same argument handles the boundary. Induction only upwards would miss negative twists, which are used in presentations later.

**Confidence:** high; the two directions and degree-zero boundary are explicit. **Event:** targeted proof check.

**Context search:** `projective-twist-comparison|five-lemma|upward and downward`. **Relation:** restates `stacks/gaga.tex`, `lemma-projective-twist-comparison`, D000055.

### N047 — Descending induction must range over all coherent sheaves

**Place:** pp. 21–22, no. 13, Theorem 1 proof. **Kind:** logical dependency check.

Fix a degree and assume comparison in the next degree for every coherent sheaf. Choose a surjection from a finite sum of twists onto `F`, with coherent kernel `R`. In the diagram, the next-degree maps for `R` and the sum of twists are isomorphisms, and comparison for the twists in the current degree is known. Exactness first gives surjectivity for `F`. Because this works for every coherent sheaf, it also gives surjectivity for `R`; another diagram chase then gives injectivity for `F`. The induction starts beyond real dimension `2r` on the analytic side, using the topological cohomological-dimension theorem, and an algebraic vanishing bound. Applying surjectivity only to the initially chosen `F` would leave a gap.

**Confidence:** high for the diagram argument; cohomological-dimension bounds are explicit external inputs. **Event:** targeted proof check.

**Context search:** `descending induction|projective-analytic-cohomological-dimension|theorem-gaga-cohomology`. **Relation:** restates the simultaneous induction in `stacks/gaga.tex`, proof of `theorem-gaga-cohomology`, D000050/D000053.

### N048 — Internal Hom needs finite presentation and flatness

**Place:** pp. 22–23, no. 14, Lemma 6. **Kind:** local base-change check.

Take a finite presentation `A^m→A^n→E→0`. Applying `Hom_A(−,F)` writes `Hom_A(E,F)` as the kernel of `F^n→F^m`. A flat extension preserves that kernel, and finite sums commute with tensor product. The resulting kernel is precisely `Hom_B(E⊗B,F⊗B)`. Applied locally, this proves the internal-Hom comparison. Finite presentation is the essential finiteness assumption; a Noetherian base and a finite module imply it, but are stronger than necessary. The modern ringed-space statement is exactly Stacks Lemma 17.22.5, Tag 0C6I. [P4]

**Confidence:** high; the finite-presentation proof and the current primary statement were checked. **Event:** targeted proof check.

**Context search:** `analytification-internal-hom|pullback-internal-hom|pseudo-coherence-and-base-change-ext`. **Relation:** restates `stacks/gaga.tex`, `lemma-analytification-internal-hom`, D000057; adds the explicit weaker hypothesis and verified modern locator.

### N049 — Uniqueness means lifting the isomorphism and its inverse

**Place:** p. 23, no. 15, beginning of Theorem 3 proof. **Kind:** categorical implication.

Fullness lifts an analytic isomorphism and its inverse to algebraic maps. Faithfulness shows that the two algebraic composites are identities, since their analytifications are. Thus the algebraization is unique up to isomorphism. There is not a unique isomorphism between the bare algebraic objects if the analytic object has automorphisms; uniqueness of the lift is relative to a specified analytic isomorphism. This distinction matters when transporting the result into a moduli category.

**Confidence:** high; the two composite identities prove the claim. **Event:** targeted proof check.

**Context search:** `essential-surjectivity-projective-reduction|uniqueness|fully faithful`. **Relation:** restates the uniqueness proof in `stacks/gaga.tex`, `lemma-gaga-essential-surjectivity-projective-reduction`, D000058; adds the automorphism qualification.

### N050 — Descending the annihilator in the projective reduction

**Place:** pp. 23–24, no. 15. **Kind:** faithful local comparison.

Algebraize the analytic extension by zero to a coherent sheaf `G` on projective space. Every element of the algebraic ideal `J(Y)` acts as zero after analytification, because the analytic sheaf is supported as a module on `Y^h`. Stalkwise injectivity `G_x→G_x⊗H_x` then shows that each product `fg` was already zero. Hence `J(Y)G=0`, so `G` is the pushforward of a coherent module on `Y`. Proposition 11 recovers its original analytic sheaf. This uses annihilation by the ideal, a stronger property than merely set-theoretic support on `Y`; the latter alone would allow nilpotent thickening data.

**Confidence:** high; injectivity detects every product and quotient-module descent is explicit. **Event:** targeted proof check.

**Context search:** `annihilated|essential-surjectivity-projective-reduction|ideal sheaf`. **Relation:** restates `stacks/gaga.tex`, `lemma-gaga-essential-surjectivity-projective-reduction`, D000058; makes the distinction between support and annihilator explicit.

### N051 — The twist cocycle and its direction

**Place:** p. 24, no. 16, definition of `M(n)`. **Kind:** gluing verification.

On `U_i∩U_j`, the map from the j-copy to the i-copy multiplies by `(t_j/t_i)^n`. On a triple overlap, the product of the j-to-i and k-to-j factors is the k-to-i factor. The inverse is obtained by interchanging i and j. These units therefore glue the local copies. Tensoring with the corresponding rank-one sheaf gives `M(n)=M⊗H(n)`, and the same transition factors on the algebraic side prove `F^h(n)=F(n)^h`. The orientation of the transition maps is what fixes the sign of the twist; it cannot be guessed from the exponent alone.

**Confidence:** high; explicit cocycle multiplication. **Event:** targeted proof check.

**Context search:** `coherent-analytic-twist|tensor compatibility|twist`. **Relation:** adds the printed cocycle calculation to `stacks/gaga.tex`, `definition-coherent-analytic-twist`, D000059.

### N052 — Hyperplane vanishing is an induction input, not a circular theorem

**Place:** p. 24, no. 16, Lemma 7. **Kind:** induction dependency.

The hyperplane has one lower projective dimension. The induction hypothesis for Theorem 3 algebraizes its coherent analytic sheaf; Theorem 1, already proved in all dimensions, identifies the twisted cohomology; FAC vanishing then kills it in positive degrees for large twist. Only finitely many cohomological degrees can be nonzero, so a common lower bound on the twist can be chosen. Theorem 3 in the ambient dimension is not used. N011 supplies the corrected exact FAC reference.

**Confidence:** high; ordering of the three inputs prevents circularity. **Event:** targeted proof check.

**Context search:** `hyperplane-analytic-serre-vanishing|induction hypothesis|finitely many`. **Relation:** restates `stacks/gaga.tex`, `lemma-hyperplane-analytic-serre-vanishing`, D000060.

### N053 — From generation at each point to one uniform twist

**Place:** p. 25, no. 16, Lemma 8, opening observations. **Kind:** compactness argument.

At a point where one homogeneous coordinate is nonzero, multiplication by a suitable power of that coordinate raises the twist and is an isomorphism on the stalk. Thus generation persists for larger twists. Choose finitely many global sections generating a given stalk; the cokernel of their evaluation map is coherent and has zero stalk there, so it vanishes on a neighbourhood. Pointwise generation is therefore open. Compactness supplies finitely many such neighbourhoods, and the maximum of their twists works everywhere by persistence. Compactness by itself does not produce a single twist unless these two preliminary properties have been proved.

**Confidence:** high; finite generation, support and compactness provide the uniform bound. **Event:** targeted proof check.

**Context search:** `generation at a point|projective-analytic-global-generation|compactness`. **Relation:** restates the first paragraph of `stacks/gaga.tex`, `lemma-projective-analytic-global-generation`, D000061.

### N054 — The hyperplane kernel must be retained

**Place:** pp. 25–26, no. 16, Lemma 8, sequences (1)–(4). **Kind:** tensor-exactness check.

Tensoring the hyperplane sequence with an arbitrary coherent analytic module need not preserve injectivity on the left. The sheaf `C` is the kernel of multiplication by the hyperplane equation on `M(−1)`; it is a Tor contribution and must be included. The cokernel `B=M/tM` and that kernel are both annihilated by `t`, hence are coherent modules on the hyperplane. Their twists give the two short exact sequences through `L_n`. No flatness of `M` has been assumed. Dropping `C` would make the proof apply only to a restricted class of modules and would break its induction.

**Confidence:** high; local multiplication by `t` identifies kernel, cokernel and annihilators. **Event:** targeted proof check.

**Context search:** `both are annihilated|projective-analytic-global-generation|kernel`. **Relation:** restates the hyperplane-kernel step in `stacks/gaga.tex`, `lemma-projective-analytic-global-generation`, D000061.

### N055 — Why finite-dimensionality is needed for stabilization

**Place:** p. 26, no. 16, Lemma 8, (5)–(9). **Kind:** numerical argument.

Hyperplane vanishing gives `dim H^1(M(n−1)) ≥ dim H^1(L_n) ≥ dim H^1(M(n))`. The outer sequence consists of finite nonnegative integers, so it eventually stabilizes. In that range the surjection `H^1(L_n)→H^1(M(n))` is injective as well, forcing the preceding boundary map from `H^0(B(n))` to vanish and allowing sections to lift. Without finite-dimensionality, a surjective map between equally infinite-dimensional spaces need not be injective. Serre cites the compact coherent-cohomology finiteness theorem [5] and seminar [3]; that analytic finiteness input is essential, not an incidental convenience.

**Confidence:** high for the finite-dimensional argument; compact analytic finiteness remains an external theorem. **Event:** targeted proof check.

**Context search:** `finite dimensional|stabilize|Grauert-direct-image`. **Relation:** restates `stacks/gaga.tex`, `lemma-projective-analytic-global-generation`, D000061. Its later Grauert citation is a different source for the analytic input; it has not been independently verified in this run.

### N056 — The last local step is exactly Nakayama

**Place:** pp. 26–27, no. 16, Lemma 8 conclusion. **Kind:** local algebra check.

Let `N` be the submodule of the finite stalk `M` generated by global sections. Lifted generators of the hyperplane quotient yield `M=N+pM`, with `p=(t)` contained in the maximal ideal because the hyperplane passes through the chosen point. The finite quotient `Q=M/N` satisfies `Q=pQ`, hence `Q=mQ`; Nakayama gives `Q=0`. The finite-generation and containment hypotheses are both used. This proves generation at the point; N053 then gives global generation with a common twist.

**Confidence:** high; the quotient meets the precise Nakayama hypotheses. **Event:** targeted proof check.

**Context search:** `M=N|Nakayama|projective-analytic-global-generation`. **Relation:** restates the final stalk argument in `stacks/gaga.tex`, `lemma-projective-analytic-global-generation`, D000061.

### N057 — Two finite presentations finish algebraization

**Place:** p. 27, no. 17, end of Theorem 3. **Kind:** exactness and fullness check.

Global generation gives a surjection from an analytified finite sum of twists to `M`. Its kernel is coherent; applying global generation again gives another finite sum of twists mapping onto that kernel. The resulting analytic map between the two sums is algebraic by Theorem 2. Its algebraic cokernel is coherent, and exactness of analytification identifies its analytic cokernel with `M`. A finite set of generating sections is obtained by compactness or finite-dimensionality of global sections; one must not replace it silently by an infinite free sum. No infinite resolution is needed.

**Confidence:** high; each of the two finite steps and the final cokernel is accounted for. **Event:** targeted proof check.

**Context search:** `completion-gaga-essential-surjectivity|Coker|finite set`. **Relation:** restates `stacks/gaga.tex`, completion of `theorem-gaga-essential-surjectivity`, D000062.

### N058 — Semilinear cohomology preserves dimensions, not a topology

**Place:** pp. 27–28, no. 18, Proposition 12. **Kind:** comparison proof and scope.

Applying a field automorphism to coefficients identifies the algebraic differential Čech complexes semilinearly; kernels and images correspond, so the cohomology vector spaces have equal dimensions. Smoothness identifies analytic differential forms with analytified algebraic differentials. Projectivity gives a compact Kähler manifold, where Hodge decomposition expresses each Betti number as the sum of the relevant Hodge dimensions. These steps prove equality of Betti numbers and even of the individual Hodge numbers in this setting. They do not produce a continuous map between the conjugate analytic spaces; an arbitrary automorphism of `C` need not be continuous.

**Confidence:** high for the semilinear argument, conditional on Hodge decomposition. **Event:** targeted proof check.

**Context search:** `semilinear|Kahler|conjugate-smooth-projective-betti-numbers`. **Relation:** restates `stacks/gaga.tex`, `proposition-conjugate-smooth-projective-betti-numbers`, D000064; the topological limitation connects to N086.

### N059 — Extending embeddings of an algebraic field

**Place:** p. 28, no. 18, corollary to Proposition 12. **Kind:** field-theoretic assertion left implicit.

Two embeddings of a field algebraic over `Q` into `C` extend to embeddings of its algebraic closure. Inside `C`, the algebraic closure of `Q` is an algebraic closure of either image, so an isomorphism extending the prescribed embedding is obtained there. Choose a transcendence basis of `C` over that algebraic closure, fix its elements, extend to the rational-function field and then to its algebraic closure `C`. The resulting automorphism has the required restriction. Proposition 12 applies to the two base changes. The corollary concerns this algebraic field hypothesis, not an unspecified continuity property of embeddings.

**Confidence:** high, using the algebraic-closure extension theorem and a transcendence basis. **Event:** targeted proof check.

**Context search:** `number-field-embeddings-betti-numbers|field embeddings|algebraic over`. **Relation:** expands the one-line extension argument in `stacks/gaga.tex`, `corollary-number-field-embeddings-betti-numbers`, D000065.

### N059A — An explicit genus-one pair of nonisomorphic conjugates

**Place:** p. 29, no. 18, Remark following Proposition 12 and its corollary. **Kind:** example asserted without construction.

Take the smooth projective cubic `E: Y²Z=X³+XZ²+(1+i)Z³` and its complex conjugate. The short-Weierstrass discriminant factor is `4+27(1+i)²=4+54i`, which is nonzero. The formula `j=1728·4a³/(4a³+27b²)` gives `j(E)=6912/(4+54i)`, a nonreal number, while `j(Ē)` is its distinct complex conjugate. The formula and its isomorphism invariance are verified in [P9, II §2, Theorem 2.1(a)–(c), author-PDF pp. 50–51].

An unpointed algebraic curve isomorphism can be followed by a translation on the target to preserve the origins, so unequal j-invariants exclude it as well. An analytic isomorphism would be algebraic by the independently proved Proposition 15 (N062). This proves the printed genus-one assertion. Complex conjugation itself is an antiholomorphic homeomorphism here: this example does not answer the subsequent homeomorphism question, for which N086 gives a later result.

**Confidence:** high; the discriminant and invariant are explicit, with the classification input inspected. **Event:** targeted proof check.

**Context search:** `elliptic|genus|conjugate-varieties-historical`. **Relation:** supplies the missing example behind the parenthetical elliptic-curve assertion in `stacks/gaga.tex`, `remark-conjugate-varieties-historical`, D000066, and separates it from the topological question.

### N060 — Chow's theorem follows from coherent support

**Place:** p. 29, no. 19, Proposition 13. **Kind:** proof check.

The analytic structure sheaf of a closed analytic subset, extended by zero, is coherent. Algebraize it by Theorem 3. Faithful local comparison says the algebraic sheaf and its analytification have the same classical support; the support of a coherent algebraic sheaf is Zariski closed. This proves the printed set-theoretic Chow assertion without choosing an algebra structure on the algebraized sheaf. For a stronger reduced-subscheme identification, algebraize the inclusion of the coherent analytic ideal into the structure sheaf using full faithfulness. Its image is an algebraic ideal, and faithful flat contraction detects radicality and uniqueness. The extra ideal argument proves more structure than the original support argument requires.

**Confidence:** high; support detection and the stronger ideal variant are distinguished. **Event:** targeted proof check.

**Context search:** `chow-closed-analytic-projective|radicality|support`. **Relation:** the first argument restates Serre; the ideal variant restates `stacks/gaga.tex`, `theorem-chow-closed-analytic-projective`, D000068, which adds the unique reduced-subscheme formulation.

### N061 — Compact analytic subsets in a nonprojective variety

**Place:** p. 29, no. 19, Proposition 14. **Kind:** abbreviated closure argument.

Use the proper modification with source an open subset `U` of a projective variety `Y` and closed graph in `X×Y`. The inverse image of the compact analytic subset is compact, hence closed in `Y`. It is analytic on `U`; at every point outside it, including the boundary of `U`, a neighbourhood disjoint from the compact closed set gives the empty analytic subset. Thus it is analytic on all of `Y`, not merely on `U`. Chow makes it algebraic, and Proposition 7 plus closedness of its image makes the original subset algebraic. The phrase “analytic in U, hence in Y” requires precisely this boundary justification.

**Confidence:** high; compactness supplies the missing boundary neighbourhoods. **Event:** targeted proof check.

**Context search:** `compact-analytic-subspace-algebraic|empty closed analytic|compactification`. **Relation:** restates the substance of `stacks/gaga.tex`, `proposition-compact-analytic-subspace-algebraic`, D000069; the chapter uses a later compactification route, while this note fills the original graph argument.

### N062 — Algebraicity of maps from a compact source

**Place:** pp. 29–30, no. 19, Proposition 15. **Kind:** graph argument.

The graph of a holomorphic map is analytic by local holomorphic equations. It is compact because it is the continuous image of the compact source, and it is closed because the target is Hausdorff. Proposition 14 algebraizes that graph; Proposition 8 then makes the map regular. One should not infer regularity from the graph's pointwise bijection with the source without the analytic-inverse input used in Proposition 8.

**Confidence:** high; all graph hypotheses are present. **Event:** targeted proof check.

**Context search:** `holomorphic-map-from-proper-is-regular|graph|proper`. **Relation:** restates `stacks/gaga.tex`, `proposition-holomorphic-map-from-proper-is-regular`, D000070.

### N062A — Uniqueness of an algebraic structure is not existence

**Place:** p. 30, no. 19, corollary to Proposition 15. **Kind:** interpretation.

If a compact analytic space has two algebraizations, Proposition 6 makes both algebraic varieties complete. Apply Proposition 15 to an analytic isomorphism between them and to its inverse; the results are inverse algebraic maps. This is the precise sense of “at most one structure.” It supplies neither an algebraization of every compact analytic space nor a preferred presentation of an existing one. Those would be stronger and generally different questions.

**Confidence:** high, from the two applications to inverse maps. **Event:** targeted proof check.

**Context search:** `compact-analytic-space-unique-algebraization|at most one|cor:15`. **Relation:** restates `stacks/gaga.tex`, `corollary-compact-analytic-space-unique-algebraization`, D000071, with the existence/uniqueness distinction explicit.

### N063 — Nonabelian H1 classifies locally trivial torsors

**Place:** p. 30, no. 20, opening paragraph. **Kind:** background construction.

Choose local trivializations of a principal bundle. Transition maps on overlaps are sections of the group sheaf and satisfy the cocycle identity. Changing trivializations changes the cocycle by a coboundary; conversely a cocycle glues trivial bundles. This gives a pointed set of isomorphism classes, with the trivial bundle as base point. It is a group only in the abelian case. The algebraic cover here is Zariski open, whereas the analytic cover is open in the analytic topology. The choice of topology is part of the statement, not implicit notation to be changed when comparing later results.

**Confidence:** high for the cocycle/gluing correspondence. **Event:** targeted proof check.

**Context search:** `principal-bundle-analytification-map|Zariski locally trivial|torsors`. **Relation:** restates the explicit topology conventions in `stacks/gaga.tex`, `definition-principal-bundle-analytification-map`, D000072.

### N064 — The isomorphism bundle proves injectivity

**Place:** p. 31, no. 20, Proposition 16. **Kind:** omitted associated-bundle identification.

For two principal `G`-bundles, local trivializations identify an equivariant isomorphism with multiplication by an element of `G`. Changing the two frames acts by `(g,g′)·h=ghg′^{-1}`, exactly the printed action. The resulting associated bundle therefore represents equivariant isomorphisms. An analytic isomorphism is an analytic section of this algebraic bundle. Since the base is compact, Proposition 15 makes the section regular, proving injectivity and algebraicity of the specified isomorphism. The total principal-bundle space need not itself be compact; compactness is used on the section's domain.

**Confidence:** high; the frame-change calculation identifies the associated bundle. **Event:** targeted proof check.

**Context search:** `principal-bundle-analytification-injective|Isom|sections`. **Relation:** restates `stacks/gaga.tex`, `proposition-principal-bundle-analytification-injective`, D000073; supplies its local action calculation.

### N065 — The finite-group warning concerns Zariski triviality

**Place:** p. 31, no. 20, paragraph after Proposition 16. **Kind:** explicit scope example.

On an irreducible variety, a regular map from a nonempty open set to a finite constant group is constant. Every intersection in a nonempty Zariski cover is nonempty; its constant transition cocycle can be trivialized by choosing one reference index. Thus a Zariski locally trivial torsor under a finite constant group is trivial. A complex elliptic curve has nontrivial finite analytic covers: for example the inclusion of lattices `2Z+τZ⊂Z+τZ` gives a connected double cover of complex tori. It cannot be the analytification of a Zariski locally trivial constant-group torsor. It can be algebraized as a finite étale cover; N085 explains why that does not contradict Serre's warning.

**Confidence:** high for the cocycle argument and lattice cover; the usual algebraicity of elliptic complex tori is background. **Event:** targeted proof check.

**Context search:** `finite|Zar|principal-bundle-analytification-map`. **Relation:** adds an explicit test case to `stacks/gaga.tex`, `definition-principal-bundle-analytification-map`, D000072, making its topology convention operational.

### N065A — An abelian-variety counterexample over the projective line

**Place:** p. 31, no. 20, paragraph following Proposition 16. **Kind:** second counterexample asserted without proof.

Let the group be an elliptic curve `E=C/Λ`, with its rank-two period lattice, and let the base be `P¹`. Analytically, the local lifting property of the covering `C→E` gives an exact sequence of sheaves `0→Λ→O→E_hol→0`. Since `H¹(P¹,O)=H²(P¹,O)=0`, its cohomology sequence identifies `H¹(P¹,E_hol)` with `H²(P¹,Λ)=Λ`. Nonzero classes give nontrivial analytic principal E-bundles by the torsor classification in N063.

Algebraically, any regular map from a nonempty open subset of `P¹` to E extends over the omitted points by properness. It is constant: a nonconstant map from a genus-zero curve to a genus-one curve contradicts Riemann–Hurwitz. Thus the Zariski sheaf of such maps is the constant sheaf `E(C)`, whose transition cocycles on the irreducible base trivialize exactly as in N065. All Zariski locally trivial algebraic principal E-bundles on this base are trivial. This proves the abelian-variety warning in the specified topology. Inputs are elliptic uniformization, the projective-line calculation in N045, and Riemann–Hurwitz; it is not an assertion that every analytic torsor fails algebraization in every algebraic topology.

**Confidence:** high, with the classical curve and cohomology inputs explicitly identified. **Event:** targeted proof check.

**Context search:** `abelian|principal-bundle-analytification-map|torsors-h1`. **Relation:** adds the abelian-variety example missing from the supplied chapter's discussion near `definition-principal-bundle-analytification-map`, D000072, alongside rather than in place of its finite-group boundary.

### N066 — Additive bundles are the degree-one comparison

**Place:** p. 31, no. 20, Proposition 17. **Kind:** reduction to Theorem 1.

For the additive group, transition functions are additive sections of the structure sheaf. Their cocycle classes are `H^1(X,O_X)` and, analytically, `H^1(X^h,H_X)`. The comparison in Theorem 1 is induced by the same inclusion of functions and therefore is the bundle comparison map itself. It gives surjectivity as well as injectivity; an unrelated isomorphism between the two cohomology groups would not identify the torsor map.

**Confidence:** high, from the explicit cocycles. **Event:** targeted proof check.

**Context search:** `additive-principal-bundles-gaga|additive sheaf|torsors-h1`. **Relation:** restates `stacks/gaga.tex`, `proposition-additive-principal-bundles-gaga`, D000074.

### N067 — Local freeness must descend after algebraization

**Place:** pp. 31–32, no. 20, Proposition 18. **Kind:** essential local step.

An analytic vector bundle gives a coherent analytic module, which Theorem 3 algebraizes. It remains to prove that the algebraic module is locally free. At a point its analytic scalar extension is free of rank n. Proposition 30 descends that freeness to the algebraic local ring; finite presentation then makes the chosen basis valid on a neighbourhood. The resulting frame bundle algebraizes the original principal `GL_n`-bundle. This step cannot be replaced by saying that every coherent sheaf is a vector bundle. N083 checks the local algebra used here.

**Confidence:** high, conditional on the explicitly checked descent lemma. **Event:** targeted proof check.

**Context search:** `general-linear-principal-bundles-gaga|finite-projectivity|frame bundle`. **Relation:** restates `stacks/gaga.tex`, `proposition-general-linear-principal-bundles-gaga`, D000075; its modern finite-projectivity descent is an alternative to Serre's completion-based proof.

### N067A — Line bundles and divisors on a normal variety

**Place:** p. 32, no. 20, Remark 1 after Proposition 18. **Kind:** divisor interpretation.

The rank-one case identifies algebraic and analytic Picard groups. A line bundle on an integral variety admits a nonzero rational section by trivializing at the generic point; its local ratios define a Cartier divisor, and changing the rational section adds a principal divisor. Conversely local equations of a Cartier divisor glue an invertible sheaf. On a normal variety Cartier divisors map to Weil divisors, and “locally linearly equivalent to zero” selects the Cartier condition. It must not be replaced by the group of all Weil divisor classes on a singular normal variety. Smoothness makes that distinction disappear locally.

**Confidence:** high for the rational-section/Cartier-divisor construction. **Event:** targeted proof check.

**Context search:** `line-bundles-gaga|divisor classes|Pic`. **Relation:** adds the Cartier-versus-Weil qualification to `stacks/gaga.tex`, `remark-line-bundles-gaga`, D000076.

### N067B — The precise bridge to Lefschetz's divisor-class theorem

**Place:** p. 32, no. 20, Remark 1 after Proposition 18. **Kind:** claimed essential equivalence.

On a smooth projective complex variety, the analytic exponential sequence gives `im(c₁:Pic_an(X)→H²(X,Z))=ker(H²(X,Z)→H²(X,O))`. Hodge decomposition identifies the latter with the integral classes whose complexification has type (1,1): an integral class is real, so vanishing of its (0,2) component also kills its (2,0) component. This includes torsion classes, whose complexification is zero. Algebraization of every analytic line bundle, followed by the divisor construction in N067A, therefore gives Lefschetz's assertion that those classes arise from divisors. Poincaré duality translates this cohomology formulation to the homology language in the print.

For the converse, equality of first Chern classes is insufficient by itself. Lefschetz gives an algebraic divisor with the same class as an analytic line bundle; their quotient is topologically trivial. One must additionally know that these `Pic⁰_an` classes are algebraic, from the classical Picard-variety theory. The exponential sequence, Hodge decomposition, Poincaré duality and this Picard-theoretic input explain the word “essentially”; no equivalence is inferred from first Chern classes alone. This is the smooth case asserted in the remark, not a claim about Hodge decomposition on arbitrary singular varieties.

**Confidence:** high for the forward implication and the isolated converse dependency; full Picard-variety theory is an external input. **Event:** targeted proof check.

**Context search:** `Lefschetz|Pic|divisor classes|remark-line-bundles-gaga`. **Relation:** adds the omitted equivalence argument to the historical summary in `stacks/gaga.tex`, `remark-line-bundles-gaga`, D000076; it is separate from the two Kodaira applications in N068.

### N068 — Kodaira's Theorems 7 and 8 need an exact source check

**Place:** p. 32, no. 20, Remark 2 after Proposition 18. **Kind:** historical extension claim.

Serre says that Proposition 18 extends Theorems 7 and 8 of his bibliography [11] to arbitrary projective varieties, possibly singular. The supplied Stacks-style remark repeats that statement without carrying out the applications. A proof must first recover the exact two theorem statements from the Annals paper, distinguish them from the preliminary PNAS announcement, and identify which steps are merely algebraization of a line or vector bundle and which use smooth analytic geometry. The bibliographic title correction in N018 does not accomplish that mathematical verification. The primary-source access result and the precise unresolved part are recorded in the source register below; no replacement theorem is attributed to Kodaira from memory.

**Confidence:** high about what the printed remark and supplied context assert; verification of the two original statements is explicitly limited by source access. **Event:** carried as background without fault found.

**Context search:** `Kodaira|Theorems 7 and 8|line-bundles-gaga`. **Relation:** restates the historical lead in `stacks/gaga.tex`, `remark-line-bundles-gaga`, D000076; adds the unfulfilled source-level proof obligation instead of treating the repetition as verification.

### N069 — A rational section gives local trivializations of the homogeneous quotient

**Place:** pp. 32–33, no. 20, before Proposition 19. **Kind:** equivalence asserted in passing.

A rational section is regular on a nonempty open subset of `G/H`. Over that open, multiplication identifies its inverse image with the product of the open and `H`; the inverse sends a point to its quotient point and its unique relative group element. Translate the open and the section by elements of `G`. Transitivity covers the homogeneous space, giving Zariski local triviality. Conversely a Zariski local trivialization supplies a section on a nonempty open. Existence of the algebraic quotient is a separate theorem and is not proved by this argument. The rational-section hypothesis cannot be omitted for an arbitrary subgroup.

**Confidence:** high for the section/trivialization equivalence, given the quotient and torsor action. **Event:** targeted proof check.

**Context search:** `rational section|algebraize-reduction-structure-group|translates`. **Relation:** restates the first step of `stacks/gaga.tex`, `proposition-algebraize-reduction-structure-group`, D000077.

### N070 — A reduction of structure group is a section

**Place:** p. 33, no. 20, Proposition 19. **Kind:** local bundle identification.

For an algebraic principal `G`-bundle `Q`, the associated bundle `E=Q×^G(G/H)` is locally `U×G/H`. Under N069, `Q→E` is locally the principal `H`-bundle `G→G/H`. An analytic reduction to `H` is a section of `E^h`; Proposition 15 algebraizes it because the base is compact. Pulling `Q→E` back along that section gives the required algebraic `H`-bundle. In each trivialization the pullback consists exactly of the coset chosen by the section, which identifies its analytification with the original reduction. This verifies the printed square and its claimed pullback, not just the existence of an associated bundle.

**Confidence:** high, from the local coset description. **Event:** targeted proof check.

**Context search:** `algebraize-reduction-structure-group|pulling|section`. **Relation:** restates `stacks/gaga.tex`, `proposition-algebraize-reduction-structure-group`, D000077; supplies the local explanation of the pullback square.

### N071 — The determinant section for SLn

**Place:** p. 34, no. 20, Example (b). **Kind:** “evident” section.

The determinant identifies `GL_n/SL_n` with `G_m`. The matrix `diag(t,1,…,1)` has determinant t and defines a regular section. It is stronger than a rational section. Together with Propositions 18 and 19 it proves the asserted comparison for `SL_n`. This construction fixes the embedding under consideration; no general statement about all semisimple groups follows from it.

**Confidence:** high; direct matrix calculation. **Event:** targeted proof check.

**Context search:** `determinant section|SL|rational-section-condition-examples`. **Relation:** expands the determinant reference in `stacks/gaga.tex`, `remark-rational-section-condition-examples`, D000078.

### N072 — Rational symplectic Gram–Schmidt

**Place:** p. 34, no. 20, Example (c). **Kind:** generic linear algebra.

Over the rational-function field in the entries of a generic nondegenerate alternating matrix, choose two basis vectors with nonzero pairing, divide one by that pairing, and project the remaining vectors to their common symplectic orthogonal complement. Repeat on the complement. Every operation uses rational expressions, with denominators nonzero on a nonempty open subset. The resulting basis transforms the form to the standard block alternating form, giving the rational section of `GL_{2m}/Sp_{2m}`. Alternating forms are essential: no square roots are required. Diagonal normalization of a symmetric form generally requires square roots; that observation alone does not prove the absence of a rational section (N095).

**Confidence:** high; the finite elimination constructs the rational matrix. **Event:** targeted proof check.

**Context search:** `symplectic|Gram|rational-section-condition-examples`. **Relation:** expands the rational symplectic calculation in `stacks/gaga.tex`, `remark-rational-section-condition-examples`, D000078.

### N073 — The solvable-group example needs a connectedness convention

**Place:** p. 34, no. 20, Example (a). **Kind:** conditional scope correction, not a textual emendation.

Under the modern convention allowing disconnected solvable algebraic groups, the unqualified assertion is false. Take `μ_2⊂GL_1`. Its quotient map is `x↦x²` on `G_m`. A rational section would give `r(t)²=t` in `C(t)`, impossible because the valuation at zero would satisfy `2v_0(r)=1`. That valuation is legitimate in the function field even though zero is not a point of `G_m`. The positive statement is for connected solvable linear groups over `C`; Grothendieck's 1958 discussion explicitly includes connectedness in this example. [P3, §3, p. 5-11]

The supplied modern `remark-rational-section-condition-examples` omits that qualification and is refuted as written. Its refined statement is **N073-connected**: connected solvable subgroups satisfy (R). In characteristic zero such a group is split solvable; a split series and additive/multiplicative Hilbert 90 trivialize its generic torsor, yielding the section. Recovering Serre's and Rosenlicht's historical convention would be needed before calling the original wording a typographical omission. The edition therefore retains it and records this mathematical limitation separately.

**Confidence:** high for the explicit counterexample and required qualification; historical convention unresolved. **Event:** targeted proof check; the separate context event is `refuted`, with refined ID N073-connected.

**Context search:** `solvable subgroups|rational-section-condition-examples|Rosenlicht`. **Relation:** differs from and refines the unqualified assertion in `stacks/gaga.tex`, `remark-rational-section-condition-examples`, D000078; it adds a concrete obstruction rather than changing the scanned words.

### N073A — The ordinary-flatness test on cyclic modules

**Place:** p. 35, no. 21, opening paragraph after Definition 3. **Kind:** compressed Tor argument.

The long Tor sequence for an arbitrary short exact sequence shows that tensoring with B preserves injections exactly when `Tor₁(B,Q)=0` for every Q; right exactness supplies the remaining flatness condition. Any finite module has a finite filtration with cyclic quotients, obtained by adjoining one generator at a time. If Tor₁ vanishes on all `A/I`, its exact sequence and induction make it vanish on all finite modules. Arbitrary modules are filtered unions of finite submodules, and Tor commutes with those filtered colimits. Finally, `0→I→A→A/I→0` identifies `Tor₁(B,A/I)` with the kernel of `I⊗B→B`. This proves the printed ideal test without a Noetherian assumption, and is distinct from N075's additional test for a flat pair.

**Confidence:** high; the filtration and exact sequence supply both reductions. **Event:** targeted proof check.

**Context search:** `gaga:no:21|algebra-section-flat|Tor`. **Relation:** supplies an explicit proof of a preliminary assertion subsumed under the broad subsection mapping D000001; a mapped section title by itself does not verify this reduction.

### N073B — Torsion freedom over a principal ideal domain

**Place:** p. 35, no. 21, Example 1. **Kind:** asserted consequence of the ideal test.

Over a principal ideal domain, each nonzero ideal `(a)` is a free module with basis a. Under that identification the ideal-test map `(a)⊗B→B` is multiplication by a. All such maps are injective exactly when B is torsion free; the zero ideal gives no condition. N073A therefore proves the equivalence with flatness. “Principal” is used in its integral-domain sense here; a definition allowing zero divisors would require a different torsion convention and does not follow from this argument.

**Confidence:** high; each test map is explicit. **Event:** targeted proof check.

**Context search:** `principal|torsion|gaga:no:21|algebra-section-flat`. **Relation:** expands the first example within subsection mapping D000001. N076 uses one direction of this phenomenon, but its counterexample is a separate claim.

### N073C — Localization is flat

**Place:** p. 35, no. 21, Example 2. **Kind:** referenced elementary example.

Identify `M⊗_A S⁻¹A` with `S⁻¹M`. If `M′→M` is injective and the image of `m/s` from `S⁻¹M′` is zero, some t in S kills m in M. Injectivity says t already kills m in M′, so `m/s` was zero there. Localization thus preserves every injection; with right exactness of tensor this proves flatness. No Noetherian hypothesis is needed, and no faithfulness conclusion follows unless extra conditions are imposed on S.

**Confidence:** high; the zero-fraction criterion proves injectivity directly. **Event:** targeted proof check.

**Context search:** `localization|fractions|gaga:no:21|algebra-section-flat`. **Relation:** supplies the direct proof of the FAC-referenced example covered only generally by D000001. It is also the elementary flatness input in local-ring passages, with faithfulness handled separately.

### N074 — Flat Hom base change in the appendix

**Place:** pp. 35–36, no. 21, Proposition 21. **Kind:** hypothesis check.

The finite free presentation of `E` makes the comparison a map between kernels of two maps of finite sums of `F`. Flatness of `B` preserves the first kernel; Hom's left exactness gives the second. The comparison on finite free modules is the tautological identification with finite sums, so the kernels agree. This is the same calculation as N048. The proof uses no finiteness of `F`; it uses finite presentation of `E`, obtained here from finite generation over a Noetherian ring. Infinite free presentations would lead to infinite products, which tensor need not preserve.

**Confidence:** high, with the exact finiteness dependency isolated. **Event:** targeted proof check.

**Context search:** `gaga:prop:21|pseudo-coherence-and-base-change-ext|D000003`. **Relation:** restates the weaker finite-presentation scope described in mapping decision D000003; adds the explicit warning about infinite products.

### N075 — The flat-pair criterion and the cyclic test

**Place:** p. 36, no. 22, Definition 4 and Proposition 22. **Kind:** abbreviated implication.

The Tor sequence for `0→A→B→B/A→0` proves that flatness of `B/A` is equivalent to flatness of `B` plus injectivity of `M→M⊗B` for every module. It is enough to test finite modules because arbitrary modules are filtered unions of finite submodules and tensor and filtered colimits preserve the relevant maps. To obtain the ideal criterion, assume `B` flat and `IB∩A=I` for every ideal I. If `m∈M` is nonzero, its cyclic submodule is `A/I`; contraction says its element `1 mod I` remains nonzero in `B/IB`, and flatness embeds this tensor product into `M⊗B`. Thus no nonzero m dies. This fills the otherwise compressed passage from cyclic modules to all modules.

**Confidence:** high; the cyclic-submodule argument proves the missing implication. **Event:** targeted proof check.

**Context search:** `gaga:prop:22|check-universally-injective-into-flat|flat-ses`. **Relation:** restates the flat/universally-injective criteria in map decision D000006; the full proof of the mapped algebra files is not supplied, so this note provides the needed local argument itself.

### N076 — Flat pairs do not satisfy unrestricted two-out-of-three

**Place:** p. 37, no. 22, Proposition 23 and Remark. **Kind:** example left unstated.

Set `A=k`, `B=k[x]`, `C=k(x)`. Both `B/A` and `C/A` are vector spaces over k, hence flat, so `(A,B)` and `(A,C)` are flat pairs. But `C/B` has the nonzero class of `1/x`, killed by x. A flat module over the domain `k[x]` is torsion free, because tensoring the injection given by multiplication by x preserves injectivity. Hence `(B,C)` is not a flat pair. This verifies the printed non-converse. For the positive direction of Proposition 23, tensor the kernel over B with C; flatness over A kills it, and the flat-pair injection into its C-extension detects that the kernel was zero.

**Confidence:** high; explicit torsion and the kernel argument. **Event:** targeted proof check.

**Context search:** `flat-pairs-not-two-out-of-three|gaga:prop:23:remark|D000008`. **Relation:** restates the counterexample role of mapping decision D000008. Its referenced algebra remark is not present in this context archive; the example is checked here directly.

### N076A — The valid composition direction for flat pairs

**Place:** p. 37, no. 22, Remark after Proposition 23, first sentence. **Kind:** “analogous reasoning” left unwritten.

If `(A,B)` and `(B,C)` are flat pairs, the two scalar-extension functors are exact, so their composite `−⊗_A C` is exact. For every A-module M, the injection `M→M⊗_A B` is followed by the injection `M⊗_A B→(M⊗_A B)⊗_B C`. Associativity identifies the composite with the unit map to `M⊗_A C`. Proposition 22 now gives the flat pair `(A,C)`. This is a different valid direction from Proposition 23's descent implication; N076 records the third, false direction separately.

**Confidence:** high; both parts of the flat-pair criterion compose. **Event:** targeted proof check.

**Context search:** `composition-flat|composition-universally-injective|gaga:prop:23:remark`. **Relation:** restates the composition proof described in D000008, with the two exact inputs written out rather than inferred from the failed converse.

### N077 — Nakayama's lemma does not need Noetherianity in this form

**Place:** pp. 37–38, no. 23, Proposition 24 and corollary. **Kind:** direct proof and scope.

For a nonzero finite module over a local ring, take a generating set of least positive cardinality. If the module equals its maximal-ideal multiple, express the last generator with coefficients in that ideal. Move its own term to the left; its coefficient becomes a unit `1−a`, allowing that generator to be eliminated, a contradiction. Apply this to the finite quotient `E/F` for the corollary. Noetherianity is not needed for these two statements; finite generation and locality are. It is needed in subsequent assertions about submodules and completion, so removing it from the whole section would be unjustified.

**Confidence:** high; the minimal-generator argument is complete. **Event:** targeted proof check.

**Context search:** `gaga:prop:24|NAK|nakayama`. **Relation:** restates the general Nakayama result mapped in D000010–D000011 and identifies which later hypotheses cannot be removed.

### N077A — What the Zariski-ring footnote requires

**Place:** p. 37, no. 23, footnote (6), concerning nos. 23–24. **Kind:** blanket generalization with a topology to specify.

The relevant adic formulation uses a Noetherian ring A with an ideal of definition `I⊂Jac(A)`, rather than requiring I to be a maximal ideal. Nakayama applies to I; Artin–Rees and the same separatedness argument then give closed finite submodules, exact completion and `Ê=E⊗Â`. Completion is faithfully flat, as also verified in [P5]. For two such adic rings and a compatible homomorphism inducing an isomorphism of completions, the common-completion argument in N081 still gives the flat pair. Completing finite quotients gives N082 as well.

The free-module assertion deserves its own step. If a finite E becomes free after the second ring, its completion is free over Â. Since `E/IE=Ê/IÊ`, choose elements of E lifting a basis modulo I. Their completed map `Âⁿ→Ê` is a map between free modules of rank n and is invertible modulo `IÂ`. That ideal is in the Jacobson radical, so its determinant is a unit and the completed map is an isomorphism. Faithful flatness descends the isomorphism to `Aⁿ→E`. This replaces the local proof's residue-field basis by a basis over `A/I`; mere descent of projectivity would not alone prove freeness.

Thus all the indicated implications extend with the ideal and compatible completion maps made explicit. Calling a ring “Zariski” without specifying its topology would leave the statement incomplete. The historical definition and its exact source are recorded in [P10]; this is distinct from the unrelated term “Jacobson ring.”

**Confidence:** high for the stated Noetherian adic formulation and free-descent argument, using Artin–Rees and faithful completion as named inputs. **Event:** targeted proof check.

**Context search:** `Zariski ring|completion-faithfully-flat|gaga:no:23|gaga:no:24`. **Relation:** extends the local formulations in mapping decisions D000009 and D000014–D000018 and makes the scope of the printed footnote explicit; the subsection mapping alone did not establish this full generalization.

### N078 — Artin–Rees supplies both topology and closedness

**Place:** p. 38, no. 23, Proposition 25. **Kind:** cited theorem and compressed deduction.

Artin–Rees gives an r such that `F∩m^nE=m^{n−r}(F∩m^rE)` for `n≥r`. Together with `m^nF⊂F∩m^nE`, this shows that the induced and intrinsic filtrations define the same topology. For the closure `N=∩m^nE` of zero, apply Artin–Rees to N: at a sufficiently large stage the formula yields `N=mN`. Noetherianity makes N finite, and Nakayama gives N=0. Apply this to `E/F` to see every submodule is closed. The finite-generation step is why the same argument does not establish separatedness for every module over an arbitrary local ring.

**Confidence:** high for the deductions, conditional on Artin–Rees. **Event:** targeted proof check.

**Context search:** `gaga:prop:25|Artin-Rees|intersect-powers`. **Relation:** restates the dependencies in mapping decision D000012, with the closure-of-zero argument expanded.

### N079 — Exact completion requires compatible lifts

**Place:** pp. 38–39, no. 23, Proposition 26. **Kind:** completion argument.

For a short exact sequence of finite modules, Artin–Rees identifies the submodule topology with the induced one, and the quotient topology is the quotient-adic topology. Surjectivity after completion can be proved by choosing successively compatible lifts modulo increasing powers: correct each next lift by an element of the kernel so it agrees with the previous lift at the preceding level. The transition maps for the kernel quotients are surjective, which is the concrete Mittag–Leffler input. Kernel identification follows from the induced topology and separatedness. With a finite presentation, compare completed finite free modules with their tensor products with the completed ring; right exactness and this exact completion identify `E⊗Â` with `Ê`. Bare metrizability without these module-topology properties would not justify exactness.

**Confidence:** high for the lifting mechanism and presentation comparison, conditional on N078. **Event:** targeted proof check.

**Context search:** `gaga:prop:26|completion-tensor|completion-noetherian`. **Relation:** expands the argument behind map decision D000013; supplies the compatibility requirement hidden in the printed appeal to metrizable topologies.

### N080 — Faithful flatness of local completion

**Place:** p. 39, no. 24, Proposition 27. **Kind:** finite-to-arbitrary reduction.

For finite modules, N079 identifies tensoring with the completion with exact completion, so injections remain injections. To treat arbitrary modules, take filtered systems of finite submodules; over a Noetherian ring the required finite submodule relations remain finite, and filtered colimits are exact. This gives flatness. Separatedness gives the injection of each finite module into its completion, and the same passage to filtered colimits gives the flat-pair property. Modern Stacks Lemma 10.97.3, Tag 00MC, states a broader version: completion along an ideal contained in the Jacobson radical of a Noetherian ring is faithfully flat. [P5]

**Confidence:** high, with the finite-module reduction explicit and the primary modern statement checked. **Event:** targeted proof check.

**Context search:** `gaga:prop:27|completion-faithfully-flat|D000015`. **Relation:** restates map decision D000015 and extends its local formulation to the verified Jacobson-radical version.

### N081 — Descent from an isomorphism of completions

**Place:** pp. 39–40, no. 24, Proposition 28. **Kind:** transitivity check.

The local homomorphism sends the maximal ideal into the maximal ideal, hence extends continuously to completions. If that extension is an isomorphism, injectivity of A into its completion embeds A in B. Identify `Â` with `B̂`; both `(A,Â)` and `(B,B̂)` are flat pairs by Proposition 27. Proposition 23 then gives `(A,B)`. This proof uses the particular homomorphism-induced isomorphism, not merely an abstract isomorphism between two completed rings. The map of local rings and the commutative triangle are essential data.

**Confidence:** high; the diagram exactly matches Proposition 23. **Event:** targeted proof check.

**Context search:** `gaga:prop:28|flatness-descends|D000016`. **Relation:** restates mapping decision D000016, adding the distinction between an induced and an abstract completion isomorphism.

### N082 — Quotients preserve the completion comparison

**Place:** p. 40, no. 24, Proposition 29. **Kind:** quotient compatibility and boundary case.

For a proper ideal a of a Noetherian local A, completion of `A/a` is `Â/aÂ`; the corresponding formula holds for `B/aB`. The completion isomorphism identifies these quotients, so Proposition 28 applies to the quotient map. This proves its flat-pair conclusion. If a is the unit ideal, both quotients are zero and the flat-module assertion is trivial, but the phrase “local ring” requires either excluding that ideal or adopting the zero-ring convention. This is a boundary convention, not grounds to alter the printed universal wording silently.

**Confidence:** high for proper ideals and the explicit zero-ring qualification. **Event:** targeted proof check.

**Context search:** `gaga:prop:29|completion-tensor|D000017`. **Relation:** restates mapping decision D000017; adds the unit-ideal convention that its compressed mapping does not state.

### N083 — Descending a finite free module

**Place:** pp. 40–41, no. 24, Proposition 30. **Kind:** proof check.

The completion hypothesis identifies the residue fields and makes A→A′ faithfully flat. Choose n elements of E lifting a basis of the common residue vector space; Nakayama gives a surjection `A^n→E`. Its kernel N is finite by Noetherianity. After base change, the quotient E′ is free, so the exact sequence splits. Reducing that split sequence modulo the maximal ideal of A′ shows `N′/m′N′=0`, since the chosen n generators give a basis of the quotient. Nakayama gives N′=0, and faithful flatness gives N=0. Reduction modulo the maximal ideal would not preserve the kernel without the splitting; that is the reason for the printed direct-summand sentence.

**Confidence:** high; basis choice, splitting, finite kernel and faithful descent are all used. **Event:** targeted proof check.

**Context search:** `gaga:prop:30|finite-projective-descends|D000018`. **Relation:** restates the local free-descent content mapped in D000018 and connects it to the vector-bundle proof in N067.

## III. Later results and the supplied programme

### N084 — Proper and relative GAGA

**Place:** pp. 19–20, no. 12, Theorems 1–3. **Kind:** later extension.

SGA 1, Exposé XII, Theorem 4.2 gives coherent higher-direct-image comparison for a proper morphism of locally finite-type `C`-schemes. Corollary 4.3 gives cohomology comparison for a proper `C`-scheme, and Theorem 4.4 gives the coherent-category equivalence. The inspected SMF reissue pages are 248–249, with original pagination 327 and 329. These statements include nonreduced schemes and replace the projective-variety scope of the 1956 theorems. [P2]

**Confidence:** high for the verified statements and hypotheses; their full later proofs were not independently reproved. **Event:** carried as background without fault found.

**Context search:** `relative GAGA|proper-projective|formal comparison`. **Relation:** extends `stacks/gaga.tex`, `section-gaga-statements`, and `stacks/gaga_r3/topics.csv`, rows `proper-projective` and `formal`. It supplies a precise later locator relevant to the relative comparison lead in N088; formal existence and analytic GAGA remain different theorems.

### N085 — Finite étale comparison has a wider base scope

**Place:** pp. 30–31, no. 20, finite-group warning. **Kind:** later comparison with a different topology.

SGA 1 XII, Theorem 5.1, identifies finite étale covers of a locally finite-type `C`-scheme with finite analytic étale covers of its analytification. Properness and smoothness are not hypotheses. The exact inspected locator is reissue p. 251, original pp. 332–333. The preceding Corollary 4.6 concerns finite objects over a proper base. [P2] The distinction explains why N065's analytic cover may be algebraic without being Zariski locally trivial.

**Confidence:** high for the inspected theorem and its relation to N065. **Event:** targeted proof check of scope, not a re-proof of Riemann existence.

**Context search:** `finite locally constant|constructible|principal-bundle-analytification-map`. **Relation:** differs from the Zariski torsor comparison in `stacks/gaga.tex`, `definition-principal-bundle-analytification-map`; supplies a narrower, precisely verified comparison category for the cote 33 leads, without claiming equivalence for all analytic constructible sheaves.

### N086 — Equal Betti numbers do not force homeomorphism

**Place:** pp. 28–29, no. 18, question following Proposition 12. **Kind:** later negative answer and stronger invariant.

An accessible primary result is François Charles, *Conjugate varieties with distinct real cohomology algebras*, Theorem 1, author's proof PDF p. 2: there are smooth projective conjugate varieties whose real cohomology algebras are nonisomorphic. A homeomorphism would induce a cohomology-ring isomorphism, so these are nonhomeomorphic. That last implication is the deduction made here. The final publication is *J. reine angew. Math.* 630 (2009), 125–139; the inspected author proof retains placeholder publication metadata, so its own page 2 is specified. [P6]

The 1964 Serre paper with the nonhomeomorphic-conjugate title is a verified bibliographic lead [B2], but its primary body was not obtained; no theorem number or construction from it is certified here. Charles's inspected statement suffices to settle the 1956 question negatively while remaining compatible with N058: equality of vector-space dimensions is weaker than isomorphism of cohomology rings.

**Confidence:** high for Charles's statement and the nonhomeomorphism inference; not an independent proof of his construction. **Event:** targeted proof check of the inference, with the theorem carried as an inspected external input.

**Context search:** `conjugate-varieties-historical|homeomorphic|Betti`. **Relation:** extends the historical question recorded in `stacks/gaga.tex`, `remark-conjugate-varieties-historical`, D000066, with an exact accessible later theorem.

### N087 — The simply connected semisimple conjecture is too broad

**Place:** p. 34, no. 20, conjecture after Examples (b)–(c). **Kind:** later classification.

Grothendieck's 1958 *Torsion homologique et sections rationnelles*, §5, Theorem 3, p. 5-22, states that the special affine semisimple groups are precisely products of special linear and symplectic groups. This is narrower than all simply connected semisimple groups. His §3, p. 5-11 defines specialness through local triviality of principal bundles. The final remark on p. 5-29 explicitly acknowledges unfinished supporting arguments in that historical presentation; the theorem statement is verified here, not its complete proof. [P3]

To relate specialness to (R) over `C`, a rational section of `GL_n→GL_n/G` gives local sections everywhere by translation. Any étale-locally trivial G-torsor extends to a `GL_n`-torsor, a vector bundle, which is Zariski locally trivial. In such a trivialization its reduction is a map to `GL_n/G`; pull back the quotient's local sections. Thus it is Zariski locally trivial. The converse applies specialness to the quotient torsor itself. This explains why the classification addresses Serre's condition, rather than merely sharing its examples.

**Confidence:** high for the primary statement and the conditional comparison of notions; full classification proof is background. **Event:** targeted proof check of the bridge to (R).

**Context search:** `simply connected|semisimple conjecture|rational-section-condition-examples`. **Relation:** extends and limits the historical conjecture repeated in `stacks/gaga.tex`, `remark-rational-section-condition-examples`, D000078; it does not alter a historical conjecture into a theorem in the source text.

### N088 — The relative-group GAGA lead requires its missing hypotheses

**Place:** pp. 19–23, nos. 12–15, compared with Montpellier cote 136, scan 242, typed p. 182, §13.5. **Kind:** programme connection and scope test.

The supplied `notes/MPL_136_235-281__N62.md` points to an unproved full-faithfulness claim for a specified category of relative group schemes, with an unidentified reference [10]. N084 supplies a precise proper coherent-sheaf comparison, but it does not identify that missing reference or establish the manuscript's full-faithfulness assertion. One must recover the base, properness or other finiteness conditions, and how group morphisms are represented by coherent algebraic data.

The unrestricted generalization to all algebraic groups is false already over a point: `z↦e^z` is a holomorphic group homomorphism `G_a^an→G_m^an`, whereas a regular map `A^1→G_m` is an invertible polynomial and hence constant; a group homomorphism of this kind is therefore trivial. This example rejects an overbroad reconstruction, not the unseen manuscript's actual assertion.

**Confidence:** high for the counterexample; the intended relative category remains unresolved. **Event:** targeted proof check.

**Context search:** `relative GAGA|136|full faithfulness`. **Relation:** adds an explicit boundary test to `notes/MPL_136_235-281__N62.md`, N62, and connects it to programme Book II, chapter II.9, as identified by the cote 136 entry in `programme/montpellier_manuscripts.html`. It does not turn that archive lead into an established result.

### N089 — The exponential-graph constructibility test survives connected strata

**Place:** pp. 19–20, no. 12, comparison-category boundary; cote 33, scan 006. **Kind:** rechecked contextual example.

Let `Z={(z,w):w=e^z}⊂C²` and extend a nonzero finite constant sheaf on Z by zero. The holomorphic change of coordinates `(z,w)↦(z,w−e^z)` identifies the two strata with `C×{0}` and `C×C*`; both are smooth and connected. Thus even a finite connected analytic stratification allows this sheaf.

If a polynomial `Σ p_j(z)w^j` vanished on Z, divide the identity along positive real x by the largest exponential `e^{mx}` with nonzero coefficient. It would force the nonzero polynomial `p_m(x)` to tend to zero, impossible. Hence Z is Zariski dense. It contains no nonempty Euclidean open set and therefore no nonempty Zariski open set; a dense algebraically constructible subset of irreducible affine space would contain one. Its support is not algebraically constructible. On these affine spaces the algebraic definition uses a finite algebraic stratification; see Stacks Definition 59.71.1, Tag 03RW. [P7]

**Confidence:** high for this conditional support obstruction, independently checked in this run; the manuscript's intended constructibility convention is unresolved. **Event:** targeted proof check.

**Context search:** `exponential|graph|MPL_33_002-049|constructible`. **Relation:** restates and strengthens `notes/MPL_33_002-049__N05.md`, N05: requiring connected strata alone does not remove the example. It differs from coherent GAGA, since the sheaf is a finite-coefficient sheaf on a nonproper base.

### N090 — The integer-support example has a different finiteness boundary

**Place:** pp. 19–20, no. 12, comparison-category boundary; cote 33, scan 006. **Kind:** rechecked contextual example.

The zeros of `sin(πz)` are the integers and are simple, so `Z⊂C` is a closed discrete analytic subset. Extend a nonzero finite constant sheaf on Z by zero. With disconnected strata allowed, Z and its complement are two analytic strata. With connected strata and local finiteness allowed, use the individual integer points and the complement; compact subsets meet only finitely many points. A requirement of finitely many connected strata excludes this example, since a connected stratum carrying nonzero stalks must be a single point. Every algebraically constructible subset of affine one-space is finite or cofinite, while the integers are neither. This proves the support obstruction with the convention explicitly fixed.

**Confidence:** high for the example and the three distinctions; no claim about the unseen historical convention. **Event:** targeted proof check.

**Context search:** `sin|integer|MPL_33_002-049_chatB|constructible`. **Relation:** restates `notes/MPL_33_002-049_chatB__N06.md`, N06, and clarifies its locally finite versus finite connected-stratum cases. N089 is a stronger test against the latter convention.

### N091 — What this pass contributes to the programme

**Place:** pp. 1–42, whole edition; no single statement number. **Kind:** programme and provenance.

The supplied programme snapshot of 17 November places the French-school editions' full scan pass among the remaining edition tasks; its HTML reference page assigns one whole work to GPT-6 Astra. This run supplies that bounded GAGA text-and-build audit and a record of its decisions. It does not validate the programme's other project counts or research claims. The supplied Stacks release claims 126 classified units and 79 mapping decisions; those are traceability records, not 79 independent proof certificates. Here the main comparison argument and the appendix implications have been checked in the bounded senses recorded above, and N073 identifies one qualification needed in the supplied modern chapter.

**Confidence:** high for what the supplied records say and what this run delivers; no audit of other projects is claimed. **Event:** carried as background without fault found.

**Context search:** `French-school|second pass|126|79`. **Relation:** adds completed GAGA-specific evidence to `programme/PROGRAMME_STATUS_20261117.md`, the French-school row and “The record”; `programme/montpellier_manuscripts.html`, French-school paragraph; `stacks/gaga_r3/STATUS.md` and `stacks/output/publication/GAGA_STACKS_R3_README.md`. It differs from treating publication/build status as mathematical verification.

## IV. Ideas proposed in this run

### N092 — A small dependency certificate for the three GAGA theorems

**Place:** pp. 19–27, nos. 12–17, Theorems 1–3. **Kind:** own organizational idea, with a checked formal implication.

I propose recording separately: local faithful flatness; coherent finite presentations; comparison for twists; naturality with connecting maps; a cohomological bound; compact coherent finiteness; and eventual analytic global generation. The proof above then exposes exactly where each is used. An elementary categorical kernel of the last step is worth extracting: if a right-exact fully faithful functor has the property that every target object admits a finite presentation by two objects in its image, then it is essentially surjective. Lift the presentation map by fullness and take its source cokernel; right exactness gives the target object. This is a repackaging of N057, not a claim of a new GAGA theorem.

**Confidence:** high for that elementary implication; medium for the usefulness of the proposed record format until used on further texts. **Event:** targeted proof check of the implication; proposal otherwise.

**Context search:** `external analytic input|proof-gaga|substantive statement gaps`. **Relation:** adds a dependency-level certificate to the unit mapping in `stacks/gaga_r3/map.csv` and the explicit input comments in `stacks/gaga.tex`. It would help the programme distinguish an expanded proof from a matched label.

### N093 — Record the topology alongside every torsor comparison

**Place:** pp. 30–34, no. 20, Propositions 16–20. **Kind:** own methodological proposal.

I propose a comparison record with explicit fields for the base, field, group and connectedness, algebraic topology, analytic topology, object class, and conclusion (faithful, full, or essentially surjective). Apply it first to N065, N073 and N085. The same finite cover is a counterexample to a Zariski-local-triviality assertion and an instance of a finite-étale comparison theorem. The record should therefore prohibit a match based only on “principal bundle” or “GAGA.” This is a way to prevent a documented category error, not a new classification result.

**Confidence:** high that these fields distinguish the examples; medium that the proposed format will be effective across the larger archive. **Event:** carried as background without fault found; proposal only.

**Context search:** `principal-bundle|constructible|tmap|topic`. **Relation:** adds a hypothesis-level refinement to `stacks/gaga_r3/topics.csv` and `tmap.csv`, and to the constructibility scope questions of the two cote 33 notes.

### N094 — Start any formal certificate with the appendix's small implications

**Place:** pp. 35–41, nos. 21–24, Propositions 21–30. **Kind:** own proposed verification project.

I propose formalizing the finite-presentation Hom argument, the cyclic test for a flat pair, the explicit failure of two-out-of-three, and free descent first. These have short algebraic interfaces and no analytic geometry hidden in their statements. Completion exactness should expose Artin–Rees and compatible inverse-limit lifting as inputs. Only after those interfaces are fixed should the analytic comparison proof use them. The present TSV events and executable text/build checks are not a formal mathematical certificate, and no proof-assistant verification is claimed.

**Confidence:** high that these are bounded dependency interfaces, from N074–N083; medium about effort or coverage of a future implementation. **Event:** carried as background without fault found; proposal only.

**Context search:** `gaga:prop:21|gaga:prop:30|Formalization result|deterministic`. **Relation:** adds a concrete distinction between replay/build validation and formal proof to the supplied release README and mapping decisions D000001–D000018.

## V. Historical boundary

### N095 — The orthogonal non-section assertion and the remaining question

**Place:** p. 34, no. 20, last paragraph. **Kind:** unproved assertion and boundary of later input.

For `SO_n` with `n≥3`, the later special-group classification in N087 supplies a route to the failure of (R): `SO_n` has a nontrivial central double covering by its spin group and is not a product of the simply connected special linear and symplectic groups. The exact covering input is Milne, *Algebraic Groups*, §24i, pp. 532–533: diagram (162), its quotient formula, and the following kernel calculation. [P8] The argument needs that structure fact, the classification and the (R)/specialness bridge. It does not follow merely from unsuccessful attempts to orthogonalize a generic form rationally.

The separate question in the print asks whether the Zariski principal-bundle comparison is bijective for this group. Failure of (R) means Serre's sufficient criterion does not apply; it is not by itself a proof of non-surjectivity for every projective base. The present notes do not settle that separate question, and do not substitute an étale-torsor theorem for it.

**Confidence:** high for the logical separation; the classification and spin-cover facts are external inputs, not independently reproved here. **Event:** carried as background without fault found.

**Context search:** `orthogonal|unimodular|rational-section-condition-examples`. **Relation:** restates the historical boundary in `stacks/gaga.tex`, `remark-rational-section-condition-examples`, D000078, and adds the precise limit of what the later classification proves.

## Primary-source register and explicit access limits

All online items below were retrieved on 18 November 2026. Only the stated passages are claimed to have been checked. No other edition or translation of GAGA (1956) was consulted. Source screenshots used during research are working files, not included in the ZIP.

| ID | Source and exact locator | What was verified |
|---|---|---|
| P1 | J.-P. Serre, *Faisceaux algébriques cohérents*, Ann. of Math. (2) 61 (1955), 197–278; chapter III, §3, no. 65, Proposition 7, printed p. 258. [Primary scan](https://www.college-de-france.fr/sites/default/files/media/document/2023-11/Jean-Pierre%20Serre_Faisceaux%20alg%C3%A9briques%20coh%C3%A9rents.pdf) | Root inspected the page image and statement; the OCR's first inequality is wrong, while the image reads q≥0. Used to verify GAGA's reference correction. |
| P2 | *SGA 1*, Exposé XII, Theorem 4.2, Corollary 4.3, Theorem 4.4, Corollary 4.6 and Theorem 5.1. [SMF reissue PDF](https://pi.math.cornell.edu/~dkmiller/bin/sga1.pdf), reissue pp. 248–249 and 251; original pp. 327, 329, 332–333 | Root inspected the exact page images and hypotheses; p≥0 in 4.2–4.3, despite extraction errors. Statement verification, not a full re-proof. |
| P3 | A. Grothendieck, *Torsion homologique et sections rationnelles*, Séminaire Claude Chevalley 3 (1958), exposé 5; §3 p. 5-11, §5 Theorem 3 p. 5-22, final remark p. 5-29. [Numdam primary scan](https://www.numdam.org/item/SCC_1958__3__A5_0.pdf) | Definition, connected solvable example, semisimple classification statement, and the author's explicit proof-completeness caveat visually checked. The full classification was not independently proved. |
| P4 | Stacks Project, Lemma 17.22.5, [Tag 0C6I](https://stacks.math.columbia.edu/tag/0C6I) | Flat pullback commutes with internal Hom from a finitely presented module; exact current statement and proof read. |
| P5 | Stacks Project, Lemma 10.97.3, [Tag 00MC](https://stacks.math.columbia.edu/tag/00MC) | Faithful flatness of Noetherian completion for an ideal in the Jacobson radical; exact current statement and proof read. |
| P6 | F. Charles, *Conjugate varieties with distinct real cohomology algebras*, J. reine angew. Math. 630 (2009), 125–139, [DOI 10.1515/CRELLE.2009.036](https://doi.org/10.1515/CRELLE.2009.036); Theorem 1, [author proof PDF](https://www.imo.universite-paris-saclay.fr/~francois.charles/crll5855.pdf), p. 2 | Root inspected Theorem 1's page image. Final metadata checked on the publisher page; proof-PDF placeholder metadata is not used. Nonhomeomorphism is the elementary inference stated in N086. |
| P7 | Stacks Project, Definition 59.71.1, [Tag 03RW](https://stacks.math.columbia.edu/tag/03RW) | Exact algebraic constructibility definition read; used only to fix the finite algebraic stratification convention in N089–N090. |
| P8 | J. S. Milne, *Algebraic Groups*, Cambridge University Press (2017), §24i, printed pp. 532–533, diagram (162), quotient formula and the following two paragraphs; [author PDF](https://www.jmilne.org/math/Books/iAG2017.pdf) | Root inspected the page images: the central kernel is μ₂ and Spin is the simply connected twofold covering of SO. Used over C in N095; the separate dimension restriction in §24j is not imposed on this covering statement. |
| P9 | J. S. Milne, *Elliptic Curves*, second-edition [author PDF](https://www.jmilne.org/math/Books/EC2.pdf), chapter II, §2, Theorem 2.1(a)–(c), author-PDF pp. 50–51 | Root inspected the nonsingularity criterion, short-Weierstrass j formula and isomorphism invariant. The explicit curve arithmetic and unpointed-isomorphism reduction are checked in N059A. The locator uses this PDF's pagination. |
| P10 | M. Yoshida, *A theorem on Zariski rings*, Canadian Journal of Mathematics 8 (1956), 3–4; [primary publisher PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/EAAFBF537DB1750547F01ECD5220AD1C/S0008414X00036464a.pdf/theorem_on_zariski_rings.pdf), opening paragraph, printed p. 3; [DOI 10.4153/CJM-1956-002-6](https://doi.org/10.4153/CJM-1956-002-6) | The contemporaneous definition and its Jacobson-radical characterization were read. GAGA [15] is Samuel's *Commutative Algebra*, Cornell notes (1953), p. 157; that cited page was not obtained. Yoshida independently supplies the terminology used in N077A. |
| B1 | K. Kodaira, *On Kähler varieties of restricted type (an intrinsic characterization of algebraic varieties)*, Ann. of Math. (2) 60 (1954), 28–48, DOI 10.2307/1969701; [official works list](https://www.mathsoc.jp/en/meeting/kodaira100/works.html), item (38) | Bibliographic identity verified. Actual Theorems 7 and 8 and their individual pages were **not** obtained. Original/publisher PDF attempts gave empty or access-limited responses. The distinct PNAS preliminary note, item (37), was not substituted. N068 remains a specified historical proof obligation. |
| B2 | J.-P. Serre, *Exemples de variétés projectives conjuguées non homéomorphes*, C. R. Acad. Sci. Paris 258 (1964), 4194–4196; [official Abel publication bibliography](https://abelprize.no/sites/default/files/2021-09/The%20Abel%20Prize%202003-2007%20The%20first%20years%202003_jean_pierre_serre.pdf), item 107, p. 87 | Bibliographic entry inspected. The primary 1964 article was not obtained; Gallica and preview access failed. No internal theorem locator or construction is asserted from it. N086 instead uses the inspected Charles theorem. |

The original article's references to Oka–Cartan, Weierstrass, the local analytic Nullstellensatz, analytic dimension, Dolbeault, Hodge decomposition, Chow's lemma, Artin–Rees and coherent-cohomology finiteness remain explicitly named inputs where used. This report does not imply that each of those foundational works was reread in full. The unresolved historical access items do not affect the scan collation, the two rejected emendations, the verified FAC repair, or the completed build gate.
