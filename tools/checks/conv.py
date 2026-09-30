# Library: python-docx runs/paragraphs to HTML (bold/italic/links, autolink, list numbering). Used by vbuild/sf40/splice.
import re, html
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.oxml.ns import qn
from dx import U, FILES, blocks

def esc(t): return html.escape(t, quote=True)

def style(p):
    try: return p.style.name
    except Exception: return 'Normal'

def numfmt(doc, p):
    pPr = p._p.pPr
    if pPr is None or pPr.numPr is None: return None
    numId = pPr.numPr.numId.val if pPr.numPr.numId is not None else None
    ilvl = pPr.numPr.ilvl.val if pPr.numPr.ilvl is not None else 0
    try:
        numbering = doc.part.numbering_part.element
        for num in numbering.findall(qn('w:num')):
            if num.get(qn('w:numId')) == str(numId):
                aid = num.find(qn('w:abstractNumId')).get(qn('w:val'))
                for an in numbering.findall(qn('w:abstractNum')):
                    if an.get(qn('w:abstractNumId')) == aid:
                        for lvl in an.findall(qn('w:lvl')):
                            if lvl.get(qn('w:ilvl')) == str(ilvl):
                                f = lvl.find(qn('w:numFmt'))
                                return f.get(qn('w:val')) if f is not None else 'bullet'
    except Exception: pass
    return 'bullet'

def runs_html(p):
    out = []
    for item in p.iter_inner_content():
        if isinstance(item, Run):
            out.append(run_html(item))
        else:  # Hyperlink
            inner = ''.join(run_html(r) for r in item.runs)
            url = item.url or ''
            if url and not url.startswith('#'):
                out.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{inner}</a>')
            else: out.append(inner)
    h = ''.join(out)
    # merge adjacent identical tags
    for t in ('strong','em'):
        h = h.replace(f'</{t}><{t}>', '')
    return h.strip()

def run_html(r):
    t = r.text
    if not t: return ''
    t = esc(t)
    if r.italic: t = f'<em>{t}</em>'
    if r.bold: t = f'<strong>{t}</strong>'
    return t

def autolink(h):
    # link bare URLs / DOIs not already inside an <a>
    if '<a ' in h: return h
    h = re.sub(r'(?<![">])(https?://[^\s<]+[^\s<.,;)])', r'<a href="\1" target="_blank" rel="noopener">\1</a>', h)
    return h

def table_html(t):
    rows = []
    for i, r in enumerate(t.rows):
        cells = []
        seen = set()
        for c in r.cells:
            if id(c._tc) in seen: continue
            seen.add(id(c._tc))
            inner = '<br>'.join(runs_html(p) for p in c.paragraphs if p.text.strip())
            tag = 'th' if i == 0 else 'td'
            cells.append(f'<{tag}>{autolink(inner)}</{tag}>')
        rows.append('<tr>' + ''.join(cells) + '</tr>')
    return '<table class="doc-table">\n' + '\n'.join(rows) + '\n</table>'

def body_html(pid, start_heading=None, stop_heading='Document Dependencies', hmap={'Heading 1':'h2','Heading 2':'h3','Heading 3':'h4'}):
    d = docx.Document(U + FILES[pid])
    out = []; on = start_heading is None; list_open = None
    started = False
    def close_list():
        nonlocal list_open
        if list_open: out.append(f'</{list_open}>'); list_open = None
    for b in blocks(d):
        if isinstance(b, Paragraph):
            s = style(b); txt = b.text.strip()
            if s in hmap:
                if stop_heading and txt.lower().startswith(stop_heading.lower()): break
                if not on and txt.lower().startswith(start_heading.lower()): on = True
            if not on: continue
            if not started:
                if s not in hmap: continue
                started = True
            if not txt: continue
            if s in hmap:
                close_list(); out.append(f'<{hmap[s]}>{esc(txt)}</{hmap[s]}>'); continue
            fmt = numfmt(d, b)
            if s.startswith('List') or fmt:
                kind = 'ol' if fmt in ('decimal','lowerLetter','upperLetter','lowerRoman','upperRoman') else 'ul'
                if list_open != kind:
                    close_list(); out.append(f'<{kind}>'); list_open = kind
                out.append(f'  <li>{autolink(runs_html(b))}</li>'); continue
            close_list()
            out.append(f'<p>{autolink(runs_html(b))}</p>')
        else:
            if not on or not started: continue
            close_list(); out.append(table_html(b))
    close_list()
    return '\n\n'.join(out)
