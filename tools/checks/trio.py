# Word vs PDF vs markdown parity check. Run: UDIR=<dir>/ python3 trio.py file.docx file.pdf file.md <header-regex>.
import docx,re,sys,zipfile,difflib,pypdf
import os; U=os.environ.get('UDIR','./')
dx,pdf,md,hdrpat=sys.argv[1:5]
def paras(path):
    d=docx.Document(path); out=[]
    for p in d.element.body.iter():
        if p.tag.endswith('}p'):
            t=''.join(x.text or '' for x in p.iter() if x.tag.endswith('}t')).strip()
            if t: out.append(t)
    return out
z=zipfile.ZipFile(U+dx)
for n in sorted(z.namelist()):
    if re.search(r'word/(header|footer)\d*\.xml',n):
        t=re.sub(r'<[^>]+>','',z.read(n).decode()); print('  ',n,'|',t.strip()[:150])
print('  comments:',[n for n in z.namelist() if 'comment' in n], 'ins/del:', z.read('word/document.xml').decode().count('<w:ins '), z.read('word/document.xml').decode().count('<w:del '))
r=pypdf.PdfReader(U+pdf)
print('  pdf pages',len(r.pages), sorted({str(f.get_object().get('/BaseFont')).split('+')[-1] for p in r.pages for f in p['/Resources']['/Font'].values()}), r.metadata.get('/Producer'))
norm=lambda s: re.findall(r"[a-z0-9]+",re.sub(r'-\s*\n\s*','-',s.replace('’',"'").replace('‘',"'")).lower())
D=paras(U+dx); A=norm(' '.join(D))
P='\n'.join(p.extract_text() for p in r.pages); P=re.sub(hdrpat,' ',P); B=norm(P)
M=open(U+md).read().replace('\\',''); M=M.split('Version History')[0] if 'Version History' in M else M
C=norm(re.sub(r'[#*|+\-]{2,}|```\{=html\}|<!-- -->|```',' ',M))
def cmp(x,y,lab):
    sm=difflib.SequenceMatcher(None,x,y,autojunk=False); ops=[o for o in sm.get_opcodes() if o[0]!='equal']
    print(f'  {lab}: {len(ops)} diffs (words {len(x)} vs {len(y)})')
    for op,i1,i2,j1,j2 in ops[:15]: print('     ',op,'|',' '.join(x[max(0,i1-3):i2+3])[:110],'||',' '.join(y[max(0,j1-3):j2+3])[:110])
cmp(A,B,'docx vs pdf'); cmp(A,C,'docx vs md')
print('  "Version History" in docx:', any('Version History' in p for p in D), '| in pdf:', 'Version History' in P)
