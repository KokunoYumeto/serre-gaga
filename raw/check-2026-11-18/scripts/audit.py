"""Sequential collation helpers. Run from the directory containing GAGA_CHECK.

Input archives are expected in upload/; extracted inputs in input/.
Rendered pages are working files and are excluded from delivery.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, csv, difflib, json, re, shutil, subprocess

ROOT = Path('GAGA_CHECK')
FIELDS = ['file','layer','printed_page','line','statement','old','new','evidence','kind','confidence']
EVENT_FIELDS = ['statement_id','date','who','type','outcome']
WHO = 'GPT-6 Astra (ChatGPT Pro mode); effort not exposed; GAGA_CHECK_20261118'

def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

def page_slice(text, page):
    lines=text.splitlines()
    starts=[(int(m.group(1)),i) for i,l in enumerate(lines) if (m:=re.search(r'printed page (\d+)',l))]
    a=next(i for n,i in starts if n==page)
    b=next((i for n,i in starts if n==page+1),len(lines))
    return a,b,lines[a:b]

def show(page):
    for layer in ['french-diplomatic','french-corrected']:
        p=ROOT/'sources'/layer/'gaga_body.tex'
        a,b,lines=page_slice(p.read_text(),page)
        if layer=='french-diplomatic':
            print(f'{p.relative_to(ROOT)} lines {a+1}-{b}')
            for n,l in enumerate(lines,a+1): print(f'{n}: {l}')
            base=lines
        else:
            print(f'Corrected French lines {a+1}-{b}:')
            diff=list(difflib.unified_diff(base,lines,fromfile='as-printed',tofile='corrected',lineterm=''))
            print('\n'.join(diff) if diff else 'Identical to as-printed page.')

def render(page):
    import fitz
    from PIL import Image
    dest=Path('work/render');dest.mkdir(parents=True,exist_ok=True)
    with fitz.open('input/GAGA_scans/GAGA_AIF_1956__6__1_0.pdf') as doc:
        pix=doc[page].get_pixmap(dpi=400,alpha=False)
        file=dest/f'p{page:02d}-400.png';pix.save(file)
    im=Image.open(file)
    # Trim empty borders, preserving the complete printed page, then make
    # overlapping strips whose small signs remain legible at native resolution.
    import PIL.ImageChops
    gray=im.convert('L'); ink=gray.point(lambda p: 255 if p<190 else 0)
    bbox=ink.getbbox()
    x0,y0,x1,y1=bbox
    x0=max(0,x0-45);y0=max(0,y0-35);x1=min(im.width,x1+45);y1=min(im.height,y1+35)
    box=(x0,y0,x1,y1)
    full=im.crop(box);full.save(dest/f'p{page:02d}-full.png')
    h=1050; step=990
    strips=[]
    for n,y in enumerate(range(y0,y1,step),1):
        end=min(y+h,y1)
        name=dest/f'p{page:02d}-s{n}.png'
        im.crop((x0,y,x1,end)).save(name)
        strips.append({'file':name.name,'box':[x0,y,x1,end]})
        if end==y1:break
    meta={'printed_page':page,'pdf_page':page+1,'dpi':400,'size':im.size,'content_box':box,'strips':strips}
    (dest/f'p{page:02d}.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta))

def change(file,layer,page,line,statement,old,new,evidence,kind,count=1):
    p=ROOT/'sources'/file
    t=p.read_text()
    if file.endswith('/gaga_body.tex') and isinstance(page,int):
        marker=re.search(r'^%+  printed page '+str(page)+r'  %+.*$',t,re.M)
        following=re.search(r'^%+  printed page '+str(page+1)+r'  %+.*$',t,re.M)
        a=marker.start(); b=following.start() if following else len(t)
    else:
        a,b=0,len(t)
    part=t[a:b]
    assert part.count(old)==count,(file,old,part.count(old),count)
    p.write_text(t[:a]+part.replace(old,new)+t[b:])
    with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
        csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t').writerow(dict(zip(FIELDS,[file,layer,page,line,statement,old,new,evidence,kind,'pending second reading'])))

def change_french(page,line,statement,old,new,evidence,kind='reading'):
    for folder,layer in [('french-diplomatic','as-printed'),('french-corrected','corrected')]:
        change(f'{folder}/gaga_body.tex',layer,page,line,statement,old,new,evidence,kind)

def _font_lexer():
    """Load the adjacent read-only lexer without depending on caller cwd."""
    import importlib.util, sys
    name = '_gaga_font_recurrence_lexer'
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name('recurrence_math_inventory.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            del sys.modules[name]
            raise
    return sys.modules[name]

def _font_parse(text, *, implicit_math=False):
    """Return balanced lexical math spans; refuse ambiguous input before writes."""
    lexer = _font_lexer()
    masked = lexer.mask_comments(text)
    wrappers, warnings = lexer.wrappers(masked)
    spans, more = lexer.math_spans(masked, wrappers, implicit_math=implicit_math)
    warnings.extend(more)
    level = 0
    position = 0
    while position < len(masked):
        if masked[position] == chr(92):
            _, position = lexer.command(masked, position)
            continue
        if masked[position] == '{':
            level += 1
        elif masked[position] == '}':
            level -= 1
            if level < 0:
                warnings.append((position, 'Unmatched closing brace.'))
                break
        position += 1
    if level > 0:
        warnings.append((len(masked), 'Unmatched opening brace.'))
    if warnings:
        raise ValueError('Font helper refused ambiguous syntax: ' + '; '.join(str(pos + 1) + ': ' + message for pos, message in warnings))
    return lexer, masked, wrappers, spans

def upright_math_capitals(text, letters, *, implicit_math=False):
    """Pure transformation of selected ordinary capital tokens in parsed math.

    Balanced textual arguments, existing math alphabet arguments, command names,
    comments and metadata are preserved. Explicit nested math in textual
    wrappers is scanned in its own math mode. Unknown macro expansion is not
    evaluated; reported parser ambiguities abort before any source write.
    implicit_math is for a caller-confirmed math fragment without delimiters.
    """
    if not letters or any(not ('A' <= letter <= 'Z') for letter in letters):
        raise ValueError('letters must contain only individually verified ASCII capitals.')
    lexer, masked, wrappers, spans = _font_parse(text, implicit_math=implicit_math)
    positions = set()
    warnings = []
    for span in spans:
        tokens, more = lexer.capital_tokens(masked, span, spans, wrappers)
        positions.update(position for position in tokens if text[position] in letters)
        warnings.extend(more)
    if warnings:
        raise ValueError('Font helper refused ambiguous tokens: ' + '; '.join(str(pos + 1) + ': ' + message for pos, message in warnings))
    return ''.join((chr(92) + 'mathrm{' + char + '}') if position in positions else char for position, char in enumerate(text))

def font_inline(file,layer,page,source_line,printed_line,statement,letters,evidence,stop=None):
    """Restore image-verified upright capitals, one ledger row per inline formula.

    source_line is the current source paragraph line, never inferred from OCR.
    Call only after individually inspecting every formula in that paragraph.
    """
    p=ROOT/'sources'/file
    lines=p.read_text().splitlines(keepends=True)
    line=lines[source_line-1]
    end=line.index(stop) if stop else len(line)
    prefix = line[:end]
    _, _, _, spans = _font_parse(prefix)
    inline = [span for span in spans if span.kind in {'$', 'math parenthesis'} and not any(other is not span and other.start <= span.start and span.end <= other.end for other in spans)]
    rows=[]; pieces=[]; cursor=0
    for ordinal, span in enumerate(inline, 1):
        old=prefix[span.start:span.end]
        new=upright_math_capitals(old, letters)
        if new!=old:
            rows.append([file,layer,page,f'{printed_line}; inline formula {ordinal}',statement,old,new,evidence,'typesetting','pending second reading'])
        pieces.extend([prefix[cursor:span.start], new])
        cursor=span.end
    pieces.append(prefix[cursor:])
    lines[source_line-1]=''.join(pieces)+line[end:]
    assert rows,(file,source_line)
    p.write_text(''.join(lines))
    with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
        csv.writer(f,delimiter='\t').writerows(rows)
    print(file,source_line,len(rows),'formula font changes')

def event(statement,kind,outcome):
    with (ROOT/'CHECK_EVENTS.tsv').open('a',newline='') as f:
        csv.DictWriter(f,fieldnames=EVENT_FIELDS,delimiter='\t').writerow(dict(zip(EVENT_FIELDS,[statement,now(),WHO,kind,outcome])))

def font_display(file,layer,page,source_first,source_last,printed_line,statement,letters,evidence,*,implicit_math=False):
    """Restore capitals in an inspected display, retaining lines and text mode.

    Include its math delimiters, or explicitly select implicit_math=True for an
    inspected formula fragment. This function does not infer a font judgment.
    """
    p=ROOT/'sources'/file
    lines=p.read_text().splitlines(keepends=True)
    old=''.join(lines[source_first-1:source_last])
    new=upright_math_capitals(old, letters, implicit_math=implicit_math)
    assert old!=new,(file,source_first,source_last)
    lines[source_first-1:source_last]=new.splitlines(keepends=True)
    p.write_text(''.join(lines))
    with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
        csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t').writerow(dict(zip(FIELDS,[file,layer,page,printed_line,statement,old,new,evidence,'typesetting','pending second reading'])))

def verdict(identifier,page,printed,corrected,decision,reason,evidence):
    p=ROOT/'INHERITED_VERDICTS.tsv'
    fields=['id','printed_page','printed_reading','corrected_reading','verdict','reason','evidence']
    exists=p.exists()
    with p.open('a',newline='') as f:
        w=csv.writer(f,delimiter='\t')
        if not exists:w.writerow(fields)
        w.writerow([identifier,page,printed,corrected,decision,reason,evidence])

def finish(page,english,observations,existing='No inherited French-layer difference on this page.',events=()):
    log=ROOT/'progress.log'
    completed=[int(m.group(1)) for m in re.finditer(r'^page (\d+) done',log.read_text(),re.M)]
    assert page==len(completed)+1,(page,completed)
    rows=list(csv.DictReader((ROOT/'CORRECTIONS.tsv').open(),delimiter='\t'))
    counts={}
    for r in rows:
        if r['printed_page']==str(page):
            k=r['layer']+'/'+r['kind'];counts[k]=counts.get(k,0)+1
    ranges=[]
    for folder in ['french-diplomatic','french-corrected']:
        a,b,_=page_slice((ROOT/'sources'/folder/'gaga_body.tex').read_text(),page)
        ranges.append(f'`sources/{folder}/gaga_body.tex`, lines {a+1}-{b}')
    stamp=now()
    text=f'\n## Printed page {page}\n\n- Scan: PDF page {page+1}, rendered at 400 dpi; complete page inspected through overlapping detail strips by GPT-6 Astra (ChatGPT Pro mode).\n- French comparison: '+ '; '.join(ranges)+'. The corrected page was compared against the diplomatic page and the image.\n'+f'- English comparison: {english}, paragraph by paragraph against the corrected French for this printed page.\n- Changes: '+(', '.join(f'{k}: {v}' for k,v in sorted(counts.items())) or '0 in all layers')+'.\n'+f'- Inherited correction verdicts: {existing}\n- Observations: {observations}\n- Completed: {stamp}.\n'
    with (ROOT/'CHECK_RECORD.md').open('a') as f:f.write(text)
    for statement,kind,outcome in events:event(statement,kind,outcome)
    with log.open('a') as f:f.write(f'page {page} done {stamp}\n')
    print(f'page {page} done {stamp}; changes {counts}')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['show','render']);ap.add_argument('page',type=int)
    args=ap.parse_args();globals()[args.action](args.page)
