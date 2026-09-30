# Library: iterates a docx body as paragraphs and tables in order (blocks()); U comes from UDIR; FILES lists the old session's file names, override them.
import re,sys,glob
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
import os; U=os.environ.get('UDIR','./')  # folder holding the uploaded .docx files
FILES={'SF0038':'eacadb0c-SF0038_IVP_v2_7.docx','SF0040':'4dab8647-SF0040_TCAP_v3_1.docx','SF0037':'c305df11-SF0037_CVP_v1_5.docx','SM-021':'a6159133-SM-021_Institutional_Continuity_Substrate_v2_7.docx','SR001-VR1':'634a7c1a-SR001-VR1_RICO_Citation_Verification_Report_v1_2.docx','SI-WP-007':'fdc92877-SI-WP-007_Human_Accountability_Problem_v1_8.docx','SM-011':'de4bae62-SM-011_Delegated_Coherence_Monitoring_v1_9.docx'}
def blocks(d):
    body=d.element.body
    for ch in body.iterchildren():
        tag=ch.tag.split('}')[1]
        if tag=='p': yield Paragraph(ch,d)
        elif tag=='tbl': yield Table(ch,d)
def doctext(pid):
    d=docx.Document(U+FILES[pid]); out=[]
    for b in blocks(d):
        if isinstance(b,Paragraph): out.append(b.text)
        else:
            for r in b.rows:
                for c in r.cells: out.append(c.text)
    return '\n'.join(out)
