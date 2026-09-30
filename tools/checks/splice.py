# Older generic page rebuild (splices converted Word body into a paper page). Superseded by vbuild.py for the stack; kept for other papers.
import re,html,sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from conv import *
from pypdf import PdfReader
R='/home/user/synthience.org/research/'
def splice(pid, start_heading, end_marker='<div class="dep-block">'):
    p=open(R+pid+'.html').read()
    a=p.index('<div class="doc-body">')+len('<div class="doc-body">')
    b=p.index(end_marker,a)
    body=body_html(pid,start_heading=start_heading)
    p=p[:a]+'\n\n'+body+'\n\n'+p[b:]
    open(R+pid+'.html','w').write(p)
norm=lambda x: re.sub(r'[^a-z0-9]','',x.lower())
def check(pid, show=4):
    s=open(R+pid+'.html').read(); m=re.search(r'<main.*?</main>',s,re.S)
    Hn=norm(html.unescape(re.sub(r'<[^>]+>',' ',m.group(0))))
    L=[]
    for pg in PdfReader(R+'pdf/'+pid+'.pdf').pages:
        for ln in (pg.extract_text() or '').split('\n'):
            if re.search(r'Page \d+|synthience\.org \||\| synthience\.org|v\d+(\.\d+)+ \| \w+ (\d+, )?\d{4}|© 20\d\d',ln): continue
            L.append(ln)
    P=re.sub(r'\s+',' ',re.sub(r'-\n','',' '.join(L)))
    sents=[x for x in re.split(r'(?<=[.!?])\s+(?=[A-Z])',P) if len(x.split())>=10]
    miss=[x for x in sents if sum(norm(' '.join(x.split()[k:k+8])) not in Hn for k in range(0,len(x.split())-7,4))>=max(2,len(x.split())//6)]
    print(f'{pid}: {len(sents)} PDF sentences, {len(miss)} not on page')
    for x in miss[:show]: print('    -',x[:170])
    return miss
