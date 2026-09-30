# Wrapper for sf40.py taking the docx path from env: TCAPDOCX=path/to/SF0040.docx python3 sf40b.py. Edit the version strings inside for the next release.
import re, docx
import dx, os; dx.FILES['SF0040']=os.path.relpath(os.path.abspath(os.environ['TCAPDOCX']), dx.U)
from conv import body_html, runs_html, autolink, esc
from dx import blocks, U
from docx.text.paragraph import Paragraph
P='/home/user/synthience.org/research/SF0040.html'
s=open(P).read()
d=docx.Document(dx.U+dx.FILES['SF0040']); B=list(blocks(d))
# body
body=body_html('SF0040',start_heading='Purpose',stop_heading='References')
stack='''<div class="stack-block">
  <div class="stack-label">The four integrity layers</div>
  <ul style="margin:0.4rem 0 0 1.2rem;">
    <li>CVP: citation integrity</li>
    <li>IVP: ingestion fidelity</li>
    <li>CRD: representation stability</li>
    <li>TCAP: theoretical coherence</li>
  </ul>
</div>'''
old_ul='<ul>\n\n  <li>CVP: citation integrity</li>\n\n  <li>IVP: ingestion fidelity</li>\n\n  <li>CRD: representation stability</li>\n\n  <li>TCAP: theoretical coherence</li>\n\n</ul>'
assert body.count(old_ul)==1, 'stack list not found'
body=body.replace(old_ul,stack)
a=s.index('<div class="doc-body">')+len('<div class="doc-body">'); b=s.index('<h2>References</h2>',a)
s=s[:a]+'\n\n'+body+'\n\n'+s[b:]
# references
i=[k for k,x in enumerate(B) if isinstance(x,Paragraph) and x.text.strip()=='References'][-1]
refs=[]
for x in B[i+1:]:
    t=x.text.strip()
    if not t: break
    refs.append('  <li>'+autolink(runs_html(x))+'</li>')
s=re.sub(r'<ul class="ref-list">.*?</ul>','<ul class="ref-list">\n'+'\n'.join(refs)+'\n</ul>',s,count=1,flags=re.S)
# abstract
ab=[x for x in B if isinstance(x,Paragraph) and x.text.startswith('The Theoretical Coherence Assurance Protocol (TCAP) defines')][0]
s=re.sub(r'(<div class="abstract-label">Abstract</div>\n  <p>).*?(</p>)',lambda m:m.group(1)+runs_html(ab)+m.group(2),s,count=1,flags=re.S)
# version fields
s=s.replace('<span class="meta-value">v3.2 | September 2026</span>','<span class="meta-value">v3.2.1 | September 2026</span>')
s=s.replace('(SF0040 v3.2)','(SF0040 v3.2.1)')
s=s.replace('Version: v3.2<br>','Version: v3.2.1<br>')
open(P,'w').write(s)
print(len(refs),'refs')
