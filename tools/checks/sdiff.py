# Step A sentence diff between two Word files (sentences removed/added). Run: python3 sdiff.py old.docx new.docx [width].
import docx,re,sys
def paras(f):
    d=docx.Document(f); out=[]
    for p in d.element.body.iter():
        if p.tag.endswith('}p'):
            t=''.join(x.text or '' for x in p.iter() if x.tag.endswith('}t')).strip()
            if t: out.append(t)
    return out
def sents(ps):
    o=[]
    for p in ps:
        p=re.sub(r'\s+',' ',p.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"'))
        o+=[s for s in re.split(r'(?<=[.!?:])\s+(?=[A-Z"(])',p) if s.strip()]
    return o
key=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
A=sents(paras(sys.argv[1])); B=sents(paras(sys.argv[2])); w=int(sys.argv[3]) if len(sys.argv)>3 else 200
KA={key(s) for s in A}; KB={key(s) for s in B}
rem=[s for s in A if key(s) not in KB]; add=[s for s in B if key(s) not in KA]
print(f'{len(A)} -> {len(B)} sentences | removed {len(rem)} | added {len(add)}')
for s in rem: print('  -',s[:w])
for s in add: print('  +',s[:w])
