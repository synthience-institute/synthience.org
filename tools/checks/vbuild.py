# Rebuilds the CVP, IVP and CRD paper pages (research/SF0037-39.html) from their Word files, keeping head, meta block, citation and footer. Run: python3 vbuild.py <dir with the .docx> '{"SF0037":"file.docx",...}'. Needs python-docx, conv.py, dx.py. Handles IVP direct-formatted headings, typed numbered lists, Quick Start / cert / def / stack blocks. Hard-coded paths (R, sys.path) point at the old session: fix before use.
"""Rebuild the four verification-stack paper pages from their Word files.
Usage: vbuild.py <dir with the four .docx> <suffix map json>
Re-run on the final Word files at publication."""
import re, sys, json, html, docx
sys.path.insert(0, '/tmp/claude-0/-home-user-synthience-org/2fe82130-37f7-5981-8eac-48922e58d072/scratchpad')
from docx.text.paragraph import Paragraph
from conv import runs_html, autolink, numfmt, style, esc
from dx import blocks

R = '/home/user/synthience.org/research/'
LAST = ' style="margin-bottom:0;"'
QS_CSS = ("    .quickstart-block { background: #eef4f0; border: 1px solid #b8d4c0; padding: 0.85rem 1.1rem; margin: 1.2rem 0 1.5rem; border-radius: 4px; font-size: 0.9rem; color: #2d4a3a; }\n"
          "    .quickstart-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #5a8a6a; margin-bottom: 0.5rem; font-weight: bold; }\n")
REF_CSS = ("    .ref-list { list-style: none; padding: 0; font-size: 0.88rem; }\n"
           "    .ref-list li { margin-bottom: 0.8rem; padding-left: 1.5rem; text-indent: -1.5rem; }\n")

def rh(p):
    h = runs_html(p).replace('\n', '<br>\n')
    return autolink(h)

def ptext(b):
    return b.text.strip() if isinstance(b, Paragraph) else ''

def first_size(p):
    for r in p.runs:
        if r.text.strip():
            return (bool(r.bold), r.font.size.pt if r.font.size else None)
    return (False, None)

def cell_paras(t):
    return [p for p in t.cell(0, 0).paragraphs if p.text.strip()]

def table_block(t, pid):
    rows, cols = len(t.rows), len(t.columns)
    if rows == 1 and cols == 1:
        ps = cell_paras(t)
        first = ps[0].text.strip()
        if first.startswith('Abstract'):
            return ''
        if pid == 'SF0039' and first == 'Context Representation Drift (CRD)':
            inner = '\n'.join('  <p' + (LAST if i == len(ps) - 1 else '') + '>' + rh(p) + '</p>' for i, p in enumerate(ps))
            return f'<div class="def-block">\n{inner}\n</div>'
        if len(ps) == 1:
            return f'<div class="distinction-block">{rh(ps[0])}</div>'
        inner = '\n'.join('  <p' + (LAST if i == len(ps) - 1 else '') + '>' + rh(p) + '</p>' for i, p in enumerate(ps))
        return f'<div class="distinction-block">\n{inner}\n</div>'
    cls = 'obs-table' if pid == 'SF0039' else 'doc-table'
    out = []
    for i, r in enumerate(t.rows):
        seen, cells = set(), []
        for c in r.cells:
            if id(c._tc) in seen: continue
            seen.add(id(c._tc))
            inner = '<br>'.join(rh(p) for p in c.paragraphs if p.text.strip())
            tag = 'th' if i == 0 else 'td'
            cells.append(f'<{tag}>{inner}</{tag}>')
        out.append('  <tr>' + ''.join(cells) + '</tr>')
    return f'<table class="{cls}">\n' + '\n'.join(out) + '\n</table>'

def heading_level(p, pid):
    s = style(p); t = p.text.strip()
    if s.startswith('Heading'):
        n = int(re.sub(r'\D', '', s) or 1)
        return {1: 'h2', 2: 'h3', 3: 'h4'}.get(n, 'h4')
    if pid == 'SF0038':
        b, sz = first_size(p)
        if b and sz == 13.0:
            return 'h3' if t.startswith('Phase ') else 'h2'
        if b and sz == 11.5:
            return 'strong'
    if pid == 'SF0039' and t in ('Quick Start', 'Practical Use'):
        return 'h2'
    return None

TYPED = re.compile(r'^\s*(\d+)\.\s*\t\s*')

def body(bl, pid, start, stop='References'):
    out = []; lst = None; on = False; qs = False; stack = False; last_h = ''
    def close():
        nonlocal lst
        if lst:
            out.append(f'</{lst}>'); lst = None
    def close_qs():
        nonlocal qs
        if qs:
            close(); out.append('</div>'); qs = False
    def close_stack():
        nonlocal stack
        if stack:
            out.append('</div>'); stack = False
    d = bl['doc']
    for b in bl['blocks']:
        t = ptext(b)
        if not on:
            if t == start: on = True
            else: continue
        if isinstance(b, Paragraph):
            if not t: continue
            if t == stop and heading_level(b, pid): break
            if pid == 'SF0039' and t == 'Position within the Synthience Verification Stack':
                out.append('<div class="stack-block">\n  <div class="stack-label">Position within the Synthience Verification Stack</div>')
                stack = True; continue
            lvl = heading_level(b, pid)
            if lvl in ('h2', 'h3', 'h4'):
                close(); close_qs(); close_stack()
                out.append(f'<{lvl}>{esc(t)}</{lvl}>'); last_h = t
                if t == 'Quick Start':
                    out.append('<div class="quickstart-block">\n  <div class="quickstart-label">Quick Start</div>'); qs = True
                continue
            if lvl == 'strong':
                close(); out.append(f'<p><strong>{esc(t)}</strong></p>'); continue
            m = TYPED.match(b.text)
            if m:
                if lst != 'ol':
                    close(); out.append('<ol style="margin-left:1.2rem;">' if qs else '<ol>'); lst = 'ol'
                h = rh(b)
                h = re.sub(r'^\s*<strong>\s*\d+\.\s*</strong>\s*', '', h)
                h = re.sub(r'^\s*<strong>\s*\d+\.\s*', '<strong>', h)
                h = re.sub(r'^\s*\d+\.\s*', '', h)
                if (qs or pid == 'SF0038') and h.startswith('<strong>') and h.endswith('</strong>') and h.count('<strong>') == 1:
                    h = h[8:-9]
                out.append(f'  <li>{h}</li>'); continue
            fmt = numfmt(d, b)
            if fmt:
                kind = 'ol' if fmt in ('decimal', 'lowerLetter', 'upperLetter', 'lowerRoman', 'upperRoman') else 'ul'
                if lst != kind:
                    close(); out.append(f'<{kind}>'); lst = kind
                out.append(f'  <li>{rh(b)}</li>'); continue
            close()
            if last_h == 'Certification Statement Template':
                out.append('<div class="cert-block">\n' + re.sub(r'</?em>', '', rh(b)) + '\n</div>'); continue
            if stack:
                out.append(f'  <p style="margin-bottom:0;">{rh(b)}</p>'); continue
            out.append(f'<p>{rh(b)}</p>')
        else:
            if not on: continue
            close(); close_stack()
            tb = table_block(b, pid)
            if tb: out.append(tb)
    close(); close_qs(); close_stack()
    return '\n\n'.join(x for x in out)

def merge_nested(h):
    # attach a bullet list that directly follows an ol item inside a quickstart block to that item
    return re.sub(r'</li>\n\n</ol>\n\n<ul>\n\n((?:  <li>.*?</li>\n\n)+)</ul>\n\n<ol style="margin-left:1.2rem;">',
                  lambda m: '\n    <ul>' + ''.join(re.findall(r'<li>.*?</li>', m.group(1))) + '</ul></li>\n\n', h)

def refs(bl):
    out = []; on = False
    for b in bl['blocks']:
        t = ptext(b)
        if not on:
            if t == 'References' and isinstance(b, Paragraph): on = True
            continue
        if not t: continue
        if t.startswith('©') or t.startswith('END') or t.startswith('—') or t.startswith('License') or t == 'synthience.org': break
        out.append('  <li>' + rh(b) + '</li>')
    return '<h2>References</h2>\n\n<ul class="ref-list">\n' + '\n'.join(out) + '\n</ul>'

def abstract(bl, pid):
    for b in bl['blocks']:
        if not isinstance(b, Paragraph) and b.cell(0, 0).text.strip().startswith('Abstract'):
            return [rh(p) for p in cell_paras(b)[1:]]
    ps = []; on = False
    for b in bl['blocks']:
        t = ptext(b)
        if t == 'Abstract': on = True; continue
        if on:
            if isinstance(b, Paragraph) and heading_level(b, pid): break
            if t and not t.startswith('Keywords'): ps.append(rh(b))
    return ps

def keywords(bl):
    for b in bl['blocks']:
        t = ptext(b)
        if t.startswith('Keywords:'):
            return t.split(':', 1)[1].strip()

def build(pid, path, ver, date, start):
    d = docx.Document(path)
    bl = {'doc': d, 'blocks': list(blocks(d))}
    s = open(R + pid + '.html').read()
    bod = merge_nested(body(bl, pid, start))
    new = '\n\n' + bod + '\n\n' + refs(bl) + '\n\n'
    a = s.index('<div class="doc-body">') + len('<div class="doc-body">')
    e = s.index('</div>\n\n<div class="citation-block">', a) if '</div>\n\n<div class="citation-block">' in s else None
    assert e, 'doc-body end not found'
    s = s[:a] + new + s[e:]
    ab = abstract(bl, pid)
    s = re.sub(r'(<div class="abstract-label">Abstract</div>\n)(.*?)(</div>)',
               lambda m: m.group(1) + '\n'.join(f'  <p>{p}</p>' for p in ab) + '\n' + m.group(3), s, count=1, flags=re.S)
    kw = keywords(bl)
    if kw and '<span class="meta-label">Keywords</span>' in s:
        s = re.sub(r'(<span class="meta-label">Keywords</span><span class="meta-value">)[^<]*', lambda m: m.group(1) + esc(kw), s)
    s = re.sub(r'(<span class="meta-label">Version</span><span class="meta-value">)[^<]*', lambda m: m.group(1) + f'{ver} | {date}', s)
    s = re.sub(r'\((' + pid + r') v[\d.]+\)', lambda m: f'({pid} {ver})', s)
    s = re.sub(r'Version: v[\d.]+<br>', f'Version: {ver}<br>', s)
    s = re.sub(r'Date: [^<]*<br>', f'Date: {date}<br>', s)
    s = s.replace('<div class="doc-series">Framework Series</div>', '<div class="doc-series">Protocols</div>')
    s = s.replace(f'Document: {pid} Framework Series', f'Document: {pid} Protocols')
    if 'quickstart-block' in s and '.quickstart-block' not in s:
        s = s.replace('  </style>', QS_CSS + '  </style>', 1)
    if 'ref-list' in s and '.ref-list' not in s:
        s = s.replace('  </style>', REF_CSS + '  </style>', 1)
    open(R + pid + '.html', 'w').write(s)
    print(pid, 'built:', len(bod), 'chars body;', len(ab), 'abstract paras; keywords', bool(kw))

if __name__ == '__main__':
    D = sys.argv[1]
    for pid, fn, ver, start in [('SF0037', 'SF0037_CVP_v1_6_draft3.docx', 'v1.6', 'Quick Start'),
                                ('SF0038', 'SF0038_IVP_v2_8_draft5.docx', 'v2.8', 'The Problem'),
                                ('SF0039', 'SF0039_CRD_v1_7_draft3.docx', 'v1.7', 'Position within the Synthience Verification Stack')]:
        if len(sys.argv) > 2: fn = json.loads(sys.argv[2]).get(pid, fn)
        build(pid, D + '/' + fn, ver, 'September 2026', start)
