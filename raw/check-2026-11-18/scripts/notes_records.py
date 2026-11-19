"""Search the supplied context for every note and append truthful check events.

Run from the deliverable root. The context stays an external input; it is not
copied into the deliverable. Re-running refreshes search results but does not
duplicate existing note/map event identifiers.
"""
from pathlib import Path
import argparse,csv,json,re,subprocess
from datetime import datetime,timezone
from package_deliverable import PRIVATE_PATTERNS

ap=argparse.ArgumentParser()
ap.add_argument('--context',type=Path,default=Path('../input/GAGA_context'))
args=ap.parse_args()
root=Path('.');ctx=args.context
text=(root/'NOTES.md').read_text()
parts=list(re.finditer(r'^### (N\d{3}[A-Z]?) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)',text,re.M|re.S))
assert parts
stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
who='GPT-6 Astra (ChatGPT Pro mode); effort not exposed; GAGA_CHECK_20261118 root'
allowed=['targeted proof check','independent re-proof','computation or formal certificate','used and rechecked in this run','carried as background without fault found','refuted']
def clean(s):
 for _,pat in PRIVATE_PATTERNS:s=pat.sub('<local>',s)
 return s.replace('\t',' ').replace('\n',' ')
search_rows=[];note_rows=[]
for m in parts:
 ident,title,body=m.groups()
 q=re.search(r'\*\*Context search:\*\* `([^`]+)`',body)
 assert q,ident
 pattern=q[1]
 proc=subprocess.run(['rg','--json','--text','-i','-e',pattern,str(ctx)],capture_output=True,text=True)
 assert proc.returncode in (0,1),(ident,proc.stderr)
 hits=[]
 for line in proc.stdout.splitlines():
  item=json.loads(line)
  if item['type']!='match':continue
  d=item['data'];path=Path(d['path']['text']).relative_to(ctx).as_posix()
  source=d['lines']['text'];pos=d['submatches'][0]['start'] if d['submatches'] else 0
  # rg offsets are bytes. Convert before taking a readable Unicode excerpt.
  charpos=len(source.encode()[:pos].decode(errors='ignore'))
  excerpt=source[max(0,charpos-70):charpos+240].strip()
  hits.append((path,d['line_number'],clean(excerpt)))
 counts={}
 for path,line,excerpt in hits:counts[path]=counts.get(path,0)+1
 for path,count in sorted(counts.items()):
  example=next(h for h in hits if h[0]==path)
  search_rows.append([ident,pattern,path,count,example[1],example[2]])
 if not hits:search_rows.append([ident,pattern,'NO MATCH',0,'','No literal regex hit; see the note for the scope of the comparison.'])
 kindmatch=re.search(r'\*\*Event:\*\* (.+)',body)
 assert kindmatch,ident
 typ=next((a for a in allowed if kindmatch[1].startswith(a)),None)
 assert typ,(ident,kindmatch[1])
 conf=re.search(r'\*\*Confidence:\*\* (.+?)(?:\*\*Event:|\n\n)',body,re.S)
 note_rows.append([f'GAGA-NOTE:{ident}',stamp,who,typ,clean(f'NOTES.md {ident}: {title}. Scope and dependencies are those explicitly stated in the note. Confidence: '+(conf[1].strip() if conf else 'see note'))])
with (root/'NOTE_CONTEXT_SEARCH.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['note_id','regex_query','context_file','matching_lines','example_line','example_excerpt']);w.writerows(search_rows)
p=root/'CHECK_EVENTS.tsv'
with p.open(newline='') as f:r=csv.DictReader(f,delimiter='\t');fields=r.fieldnames;events=list(r)
existing={r['statement_id'] for r in events}
with p.open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for row in note_rows:
  if row[0] not in existing:w.writerow(row);existing.add(row[0])
 for row in csv.DictReader((ctx/'stacks/gaga_r3/dec.csv').open()):
  ident='CONTEXT:GAGA-R3:'+row['decision_id']
  if ident not in existing:
   w.writerow([ident,stamp,who,'carried as background without fault found',clean('Located and compared mapping decision for '+row['unit_id']+'. The record is a context lead, not an independently certified theorem or proof-assistant result. Bounded mathematical checks and any qualification are in NOTES.md; no blanket approval of the mapping release is inferred.')]);existing.add(ident)
# Additional events name the contextual statement or external input itself.
# A mapping decision can have a later bounded assessment without rewriting its
# earlier background/provenance event. Event type is never inferred from status.
supplement=[
 ('CONTEXT:stacks/gaga.tex:remark-rational-section-condition-examples:solvable','refuted','Refined statement ID N073-connected. With disconnected solvable groups allowed, mu_2 in GL_1 has quotient t -> t^2 and no rational section: a putative square root of t has impossible valuation 1/2. This refutes the supplied modern unqualified assertion, not an unresolved historical convention. See NOTES.md N073.'),
 ('N073-connected','targeted proof check','Refined statement: connected solvable linear groups over C satisfy (R). The deduction uses split solvability and additive/multiplicative Hilbert 90 on the generic torsor; these structural/cohomological inputs are named, not independently reproved. The precise connected-solvable statement was inspected in Grothendieck 1958, section 3, p. 5-11.'),
 ('CONTEXT:GAGA-R3:D000078','targeted proof check','The mapping records Proposition 20 and examples. The argument under (R) is checked in NOTES.md N069-N072; the unqualified modern solvable example needs the refined statement N073-connected. No blanket validation of every example or of the historic conjecture follows from this mapping record.'),
 ('CONTEXT:Montpellier:cote33:N05','targeted proof check','The exponential graph is analytic, connected and Zariski dense with no Zariski open subset. Its complement is also connected by the explicit holomorphic coordinate change. The support obstruction survives finite connected analytic strata; see NOTES.md N089. The manuscript convention remains unresolved.'),
 ('CONTEXT:Montpellier:cote33:chatB:N06','targeted proof check','The integer-support example and its finite/disconnected versus locally finite/connected distinctions are checked in NOTES.md N090. It does not by itself satisfy a requirement of finitely many connected strata. No assertion is made about the unseen manuscript convention.'),
 ('CONTEXT:Montpellier:cote136:N62','carried as background without fault found','Located the relative-group full-faithfulness lead and its missing reference/hypotheses. It remains unresolved. NOTES.md N088 does not promote it to a category equivalence or apply proper coherent GAGA without its hypotheses.'),
 ('PROPOSED:unrestricted-group-analytification-full-faithfulness','refuted','Refined scope record: GAGA-NOTE:N088. The unrestricted assertion for all algebraic groups is false: exp is a nonconstant holomorphic group map G_a^an -> G_m^an, whereas an algebraic A^1 -> G_m is constant. This tests an overbroad reconstruction and does not refute Montpellier N62.'),
 ('GAGA:p34:no20:simply-connected-semisimple-conjecture','refuted','Refined statement ID N087-special-classification. Conditional on the inspected later classification, simply connected semisimple groups outside products of SL and Sp do not satisfy (R). The bridge between (R) and specialness is checked in NOTES.md N087; the classification is an external input with its historical proof-completeness caveat.'),
 ('N087-special-classification','carried as background without fault found','Refined later statement: over C the special semisimple groups are products of special linear and symplectic groups. Grothendieck 1958, section 5, Theorem 3, p. 5-22, was inspected as a statement; the final caveat on p. 5-29 is retained. Full classification proof not independently checked.'),
 ('GAGA:p34:no20:orthogonal-comparison-question','carried as background without fault found','NOTES.md N095 separates the failure of condition (R) from surjectivity of the Zariski principal-bundle comparison. The latter question is not settled in this run.'),
 ('CONTEXT:programme:20261117:French-school-editions','carried as background without fault found','The supplied snapshot places full scan passes among edition tasks and assigns a whole work to the primary reader. This run supplies GAGA-specific text/build evidence only. Other programme counts, projects and mathematical claims are not audited; NOTES.md N091.'),
 ('EXTERNAL:FAC1955:III-3-65:Proposition7','used and rechecked in this run','Inspected printed p. 258 in the primary scan. Finiteness for q >= 0 and eventual higher-cohomology vanishing verify the precise FAC input and the correction of GAGA p. 24 reference [8] to [18]. This is a statement/reference check, not a re-proof of FAC.'),
 ('EXTERNAL:SGA1:XII:Theorem4.2','carried as background without fault found','Exact proper higher-direct-image comparison statement and hypotheses inspected on reissue p. 248, original p. 327. Used in NOTES.md N084; full SGA proof not independently checked.'),
 ('EXTERNAL:SGA1:XII:Corollary4.3','carried as background without fault found','Exact proper coherent-cohomology comparison statement inspected on reissue p. 249, original p. 329. Used in NOTES.md N084; full proof not independently checked.'),
 ('EXTERNAL:SGA1:XII:Theorem4.4','carried as background without fault found','Exact coherent-category equivalence over a proper C-scheme inspected on reissue p. 249, original p. 329. Used in NOTES.md N084; full proof not independently checked.'),
 ('EXTERNAL:SGA1:XII:Corollary4.6','carried as background without fault found','Finite-object equivalence over a proper base inspected on reissue p. 251, original p. 332. Its proper-base scope is distinguished from Theorem 5.1 in NOTES.md N085.'),
 ('EXTERNAL:SGA1:XII:Theorem5.1','carried as background without fault found','Finite etale comparison for locally finite-type C-schemes inspected on reissue p. 251, original pp. 332-333. Properness and smoothness are not hypotheses; NOTES.md N085. This is statement verification, not a re-proof of Riemann existence.'),
 ('EXTERNAL:Grothendieck1958:section3:special-groups','carried as background without fault found','Definition and explicitly connected solvable example inspected on p. 5-11. Used as named inputs in NOTES.md N073 and N087.'),
 ('EXTERNAL:Grothendieck1958:section5:Theorem3','carried as background without fault found','Semisimple special-group classification statement inspected on p. 5-22, with the author proof-completeness caveat on p. 5-29. The bridge to (R), rather than the classification proof, is checked in NOTES.md N087.'),
 ('EXTERNAL:Stacks:0C6I','used and rechecked in this run','Read Lemma 17.22.5 and its finite-presentation/flat-pullback proof. Its kernel calculation is checked locally in NOTES.md N048 and N074; no weaker finite-presentation hypothesis is silently omitted.'),
 ('EXTERNAL:Stacks:00MC','used and rechecked in this run','Read Lemma 10.97.3 and its proof. The Jacobson-radical hypothesis in the modern completion statement is retained; NOTES.md N080 checks the local finite-module argument with Artin-Rees as an explicit input.'),
 ('EXTERNAL:Stacks:03RW','used and rechecked in this run','Read Definition 59.71.1 to fix the finite algebraic stratification convention. NOTES.md N089-N090 check the nonalgebraically constructible supports under that convention.'),
 ('EXTERNAL:Charles2009:Theorem1','carried as background without fault found','Author proof PDF p. 2 inspected: smooth projective conjugates with nonisomorphic real cohomology algebras. Publisher metadata verified. NOTES.md N086 checks the elementary implication to nonhomeomorphism; the construction proof is external.'),
 ('BIBLIOGRAPHIC:Kodaira1954:Annals60:28-48','carried as background without fault found','Bibliographic identity verified against the official works list, item 38. The actual Theorems 7 and 8 and their pages were not obtained; no theorem-level check is claimed. NOTES.md N068 and source-register B1 retain the proof obligation.'),
 ('BIBLIOGRAPHIC:Serre1964:CR258:4194-4196','carried as background without fault found','Official Abel bibliography item 107, p. 87, inspected. The primary article body was not obtained; no internal theorem or construction is certified. NOTES.md N086 instead relies on Charles Theorem 1.'),
 ('EXTERNAL:Milne2017:24i:spin-cover','carried as background without fault found','Inspected the page images of Algebraic Groups, pp. 532-533, diagram (162), quotient formula and the following kernel calculation. Spin -> SO is a central twofold covering with kernel mu_2. Used over C for n >= 3 in NOTES.md N095; this structure theorem is an external input.'),
 ('EXTERNAL:MilneEC2:II-2:Theorem2.1','used and rechecked in this run','Inspected author-PDF pp. 50-51: short-Weierstrass nonsingularity and j-invariant formula/isomorphism criterion in characteristic not 2 or 3. NOTES.md N059A computes the explicit conjugate elliptic example and checks the unpointed reduction; the full elliptic-curve classification is an external input.'),
 ('EXTERNAL:Yoshida1956:p3:Zariski-definition','carried as background without fault found','Read the primary opening definition: Noetherian I-adic ring with all ideals closed, equivalently I inside the Jacobson radical. NOTES.md N077A checks the completion and free-descent extensions in this formulation. GAGA reference [15] is the distinct Samuel Cornell notes; its cited p. 157 was not obtained.')
]
with p.open(newline='') as f:events=list(csv.DictReader(f,delimiter='\t'))
event_keys={(r['statement_id'],r['type']) for r in events}
with p.open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for ident,typ,outcome in supplement:
  if (ident,typ) not in event_keys:
   w.writerow([ident,stamp,who,typ,clean(outcome)]);event_keys.add((ident,typ))
print(f'{len(parts)} notes; {len(search_rows)} file-level search records; all notes have confidence, event type and context search; supplemental context/source events recorded.')
