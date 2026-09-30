# Word vs PDF check for one paper (text parity, headers/footers, comments, tracked changes, leftover Version History). Run: python3 duo.py file.docx file.pdf.
import docx,re,sys,zipfile,difflib,pypdf
dx,pdf=sys.argv[1:3]
def paras(path):
    d=docx.Document(path); out=[]
    for p in d.element.body.iter():
        if p.tag.endswith('}p'):
            t=''.join(x.text or '' for x in p.iter() if x.tag.endswith('}t')).strip()
            if t: out.append(t)
    return out
z=zipfile.ZipFile(dx)
hf=[re.sub(r'<[^>]+>','',z.read(n).decode()).strip() for n in sorted(z.namelist()) if re.search(r'word/(header|footer)\d*\.xml',n)]
doc=z.read('word/document.xml').decode()
com=z.read('word/comments.xml').decode().count('<w:comment ') if 'word/comments.xml' in z.namelist() else 0
print('  headers/footers:',[h[:70] for h in hf if h]); print('  comments',com,'ins/del',doc.count('<w:ins '),doc.count('<w:del '))
r=pypdf.PdfReader(pdf); print('  pages',len(r.pages))
norm=lambda s: re.findall(r"[a-z0-9]+",re.sub(r'-\s*\n\s*','-',s.replace('’',"'")).lower())
D=paras(dx); A=norm(' '.join(D)); P='\n'.join(p.extract_text() for p in r.pages)
for h in hf:
    if h: P=P.replace(h,' ')
B=norm(P)
ops=[o for o in difflib.SequenceMatcher(None,A,B,autojunk=False).get_opcodes() if o[0]!='equal']
bad=[o for o in ops if not (o[0]=='insert' and all(w.isdigit() or w in('page','synthience','org','institute','sf0037','sf0038','sf0039','sf0040','protocols','v2','8','v1','6','7','v3','2','1','cvp','ivp','crd','tcap','citation','verification','protocol','ingestion','context','representation','drift','theoretical','coherence','assurance','september','2026','|') for w in B[o[3]:o[4]]))]
print('  docx vs pdf: diffs',len(ops),'non-header diffs',len(bad))
for op,i1,i2,j1,j2 in bad[:6]: print('    ',op,' '.join(A[max(0,i1-4):i2+4])[:100],'||',' '.join(B[max(0,j1-4):j2+4])[:100])
print('  Version History in docx:',any('Version History' in p for p in D))
