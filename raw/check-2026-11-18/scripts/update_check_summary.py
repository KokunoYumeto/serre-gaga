"""Refresh derived final ledger counts and page map, preserving reading timestamps.

Run from the directory containing GAGA_CHECK. No edition source is modified.
"""
from pathlib import Path
import csv,re,collections
root=Path('GAGA_CHECK')
rows=list(csv.DictReader((root/'CORRECTIONS.tsv').open(),delimiter='\t'))
active=[r for r in rows if r['old']!=r['new']]
confidence_counts=collections.Counter(r['confidence'].split(';',1)[0].strip().casefold() for r in rows)
review_sessions=list(csv.DictReader((root/'SECOND_READING.tsv').open(),delimiter='\t'))
reviewed_ids=set()
for session in review_sessions:
 for part in re.split(r'[,;]',session['ledger_rows']):
  part=part.strip()
  if not part or part.casefold()=='none':continue
  match=re.fullmatch(r'(\d+)(?:\s*[-–]\s*(\d+))?',part)
  if not match:raise ValueError('Unrecognized second-reading record range: '+part)
  first=int(match.group(1));last=int(match.group(2) or first)
  if last<first:raise ValueError('Reversed second-reading record range: '+part)
  reviewed_ids.update(range(first,last+1))
expected_ids=set(range(1,len(rows)+1))
if reviewed_ids-expected_ids:raise ValueError('Second-reading records refer beyond the current ledger.')
missing_reviews=sorted(expected_ids-reviewed_ids)
confidence_parts=[f'{confidence_counts[level]:,} {level}-confidence records' for level in ['high','medium','low'] if confidence_counts[level]]
confidence_parts.extend(f'{count:,} records marked "{level}"' for level,count in sorted(confidence_counts.items()) if level not in {'high','medium','low'})
confidence_text=' and '.join(confidence_parts) if len(confidence_parts)<3 else ', '.join(confidence_parts[:-1])+', and '+confidence_parts[-1]
review_coverage=(f'All {len(rows):,} ledger records have a second-reading disposition: ' if not missing_reviews else f'{len(reviewed_ids):,} of {len(rows):,} ledger records are mapped to second-reading sessions. Current confidence labels: ')+confidence_text+'.'
if missing_reviews:review_coverage+=' Records without a mapped review: '+', '.join(map(str,missing_reviews))+'.'
layers=['as-printed','corrected','English','build']
kinds=['reading','misprint of the original','translation','typesetting','structure']
def pages(r):
 s=r['printed_page']; nums=[int(v) for v in re.findall(r'\d+',s)]
 if len(nums)==2 and re.search(r'[–-]',s):return set(range(nums[0],nums[1]+1))
 return set(nums)
p=root/'CHECK_RECORD.md';t=p.read_text()
for n in range(1,43):
 pattern=r'(## Printed page '+str(n)+r'\n)(.*?)(?=\n## |\Z)'
 m=re.search(pattern,t,re.S);assert m,n
 block=m.group(2)
 counts=collections.Counter((r['layer'],r['kind']) for r in active if r['layer']!='build' and n in pages(r))
 line=', '.join(f'{layer}/{kind}: {counts[layer,kind]}' for layer in layers for kind in kinds if counts[layer,kind]) or '0 in all layers'
 block=re.sub(r'^- Changes:.*$', '- Changes: '+line+'. Counts include the second reading and recurrence review; page-range repairs are counted on each affected page.',block,flags=re.M)
 updates={
 1:'Second reading: a detached baseline mark after the title is transcribed as a period in both French layers, with medium confidence. The physical origin remains uncertain.',
 3:'Recurrence review: removed the added paragraph break at pp. 3–4 in both French layers and English; both page-edge crops were reread.',
 4:'Recurrence review: the opening coordinate criterion continues the p. 3 definition without a new paragraph in the print.',
 8:'Recurrence review: the final Remark continues into p. 9 without a paragraph break; all three layers were repaired and reread.',
 9:'Recurrence review: “On définit” continues the p. 8 Remark flush left; the following “Dans la suite” starts a separate indented paragraph.',
 12:'Second reading: restored the first union as a large union sign as well as the second; the second union retains its printed below-sign limit.',
 19:'Second reading: the proposed English addition “new” was withdrawn as unnecessary. Data record 809 is retained with identical old/new text; the original English wording remains.',
 26:'Recurrence review: “Ceci étant…” continues into the flush-left p. 27 “En effet…”; both French layers were joined. English was already one paragraph.',
 27:'Recurrence review: removed the added page-boundary paragraph break in both French layers; no English change was needed.',
 38:'Second reading: amended three display-font records to remove accidental math-font commands from the ordinary words “Artin” and “Exposé”; nested formulas remain correctly styled.'
 }
 if n in updates and '- Second-reading/recurrence result:' not in block:
  block=block.rstrip()+'\n- Second-reading/recurrence result: '+updates[n]+'\n'
 if n==19:block=block.replace('Restored the omitted adjective “new”; no paraphrase or stylistic rewriting.','The initial addition of “new” was subsequently withdrawn; see the second-reading result below.')
 t=t[:m.start(2)]+block+t[m.end(2):]
counts=collections.Counter((r['layer'],r['kind']) for r in rows)
net=collections.Counter(r['layer'] for r in active)
summary=['## Totals','',f'The ledger contains **{len(rows):,} data records**, of which **{len(active):,} describe retained changes** and **{len(rows)-len(active)} is explicitly withdrawn**. A data record is one recorded source edit, often one formula-font restoration; it is not one mathematical error. The withdrawn English record remains to preserve the decision history. Inherited corrections already present in the supplied corrected layer are separately adjudicated in `INHERITED_VERDICTS.tsv`; they are not counted again as new edits.','', '| Layer | Reading | Misprint of the original | Translation | Typesetting | Structure | Ledger total | Retained changes |','|---|---:|---:|---:|---:|---:|---:|---:|']
for l in layers:
 if not any(counts[l,k] for k in kinds):continue
 summary.append('| '+l+' | '+' | '.join(str(counts[l,k]) for k in kinds)+' | '+str(sum(counts[l,k] for k in kinds))+' | '+str(net[l])+' |')
summary+=['','### Pages with no newly found difference','', 'These counts refer to retained page-text/typography/structure edits found against the supplied source layer. Build-only layout changes are excluded. An inherited correction that was confirmed is not a new difference found in this run. A repair spanning two printed pages affects both pages.','', '| Layer | Pages with no new difference | Printed pages |','|---|---:|---|']
for l in layers[:3]:
 changed=set().union(*(pages(r) for r in active if r['layer']==l))
 none=[n for n in range(1,43) if n not in changed]
 summary.append('| '+l+' | '+str(len(none))+' | '+', '.join(map(str,none))+' |')
summary+=['','### Changes to mathematical symbols, assertions or references','', 'The following list separates substantive symbol/reference decisions from the much larger set of font and layout restorations. Each line identifies its place and the corresponding ledger data records or inherited verdict. No change in alphabet styling is claimed to be a new mathematical theorem.','',
'- Printed p. 5, Proposition 1 and preceding definition: restore the analytic vanishing ideal `A(Y)` at all six places in each layer (data records 19–36); the scan does not print `J(Y)`.',
'- Printed p. 6, Proposition 1 proof: restore the same analytic ideal `A(X)` at both places in each layer (39–44).',
'- Printed p. 11, Proposition 5 proof: restore the printed capital `X` only in diplomatic French; corrected French and English retain the mathematically required point `x` (55; SRC-006/SRC-023).',
'- Printed p. 18, Proposition 11: restore tensoring over `A` in corrected French and English (716–717); both factors are `A/a`-modules, so the printed expression is canonically valid.',
'- Printed p. 23, no. 15: restore algebraic ideal `J=J(Y)` and its fiber `J_x` in all layers (840–843, 846–847).',
'- Printed p. 24, no. 15: restore `J.G=0` in all layers (866–867, 871).',
'- Printed p. 24, no. 15: correct the printed reference `[8]` to FAC `[18]`, no. 65, Proposition 7, only in corrected French and English (870, 872).',
'- Printed p. 26, equation (8): restore the printed `M(n)` in corrected French and English (951–952); the repeated equality is true and sufficient, so an editorial `M(n−1)` is not required.',
'- Printed p. 36, Proposition 21 diagram: reproduce the visibly missing closing parenthesis only in diplomatic French; corrected French and English retain it (1770; UNC-067).',
'- Inherited correction retained: p. 5 chart axiom `H_II` → `H_I` (SRC-022).',
'- Inherited correction retained: p. 6 conclusion `H_U` → `H_X` (SRC-003).',
'- Inherited correction retained: p. 14 missing component index `K′` → `K′_i` (SRC-008).',
'- Inherited correction retained: p. 17 inverse-image sequence `F_3` → `F′_3` (SRC-009).',
'- Inherited correction retained: p. 23 algebraic global sections `H^0(X^h,A)` → `H^0(X,A)` (SRC-012).',
'- Inherited correction retained: p. 28 source of the semilinear cohomology map uses `Ω^p(X)`, not `Ω^p(X^σ)` (SRC-014).',
'', 'All other retained French-layer differences are grammatical or punctuation repairs recorded with reasons. There are 16 local differences between the final French bodies on 15 printed pages; the original spelling conventions and unsupported proposed corrections are retained or restored as documented.','', '### Review coverage','', review_coverage+' `SECOND_READING.tsv` maps data records to the actual review sessions. `RECURRENCE_CHECK.md` records the full-work follow-up searches. The inherited-record crosswalk covers all 134 source-correction, transcription-repair, page-join, English-check and uncertain-reading identifiers. The final page map is in `FINAL_PAGE_MAP.tsv`.','']
t=re.sub(r'## Totals\n.*?(?=## Printed page 1\n)','\n'.join(summary)+'\n',t,flags=re.S)
p.write_text(t)
with (root/'FINAL_PAGE_MAP.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['printed_page','scan_pdf_page','layer','file','first_source_line','last_source_line'])
 for folder,layer in [('french-diplomatic','as-printed'),('french-corrected','corrected')]:
  file=f'sources/{folder}/gaga_body.tex';ls=(root/file).read_text().splitlines()
  marks=[(int(m.group(1)),i+1) for i,line in enumerate(ls) if (m:=re.search(r'printed page (\d+)',line))]
  for i,(n,start) in enumerate(marks):w.writerow([n,n+1,layer,file,start,marks[i+1][1]-1 if i+1<len(marks) else len(ls)])
print('Updated counts, final French page map, and second-reading/recurrence addenda.')
print(f'Review coverage: {len(reviewed_ids)}/{len(rows)} ledger records; '+confidence_text+'.')
