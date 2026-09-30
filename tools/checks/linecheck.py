# Page-vs-PDF check for ALL papers: every normalised line of research/pdf/<ID>.pdf (running headers/footers and list numbers stripped) must appear in research/<ID>.html. Run: python3 linecheck.py. Expected residue: cover labels such as "Affiliation Synthience Institute". Needs pypdf.
import re,html,glob,os,collections
from pypdf import PdfReader
norm=lambda x: re.sub(r'[^a-z0-9]','',html.unescape(x).lower().replace('&','and'))
R='/home/user/synthience.org/research/'
res={}
for pdf in sorted(glob.glob(R+'pdf/*.pdf')):
    pid=os.path.basename(pdf)[:-4]
    if not os.path.exists(R+pid+'.html'): continue
    s=open(R+pid+'.html').read()
    m=re.search(r'<main.*?</main>',s,re.S); body=m.group(0) if m else s
    Hn=norm(re.sub(r'<[^>]+>',' ',body))
    pages=[p.extract_text() or '' for p in PdfReader(pdf).pages]
    cnt=collections.Counter(l.strip() for p in pages for l in p.split('\n'))
    miss=[]
    for p in pages:
        for ln in p.split('\n'):
            l=ln.strip()
            if cnt[l]>2: continue                      # running headers/footers
            if re.search(r'synthience\.org|Page \d+|©',l): continue
            l=re.sub(r'^([●•▪◦\-–]|\d+\.|Step \d+\.|\d+\.\d+)\s*','',l)
            if len(l.split())<2 or re.search(r'Document ID|Version v?\d|DOI|doi\.org|Synthience Institute\. |END OF|Published by|Released under|ISBN|Report ID|Manuscript',l): continue
            if norm(l) not in Hn: miss.append(l)
    res[pid]=miss
    print(f'{pid:12} {len(miss):4} lines not on page  ({sum(len(x.split()) for x in miss)} words)')
import json; json.dump(res,open('linecheck.json','w'),indent=1)
