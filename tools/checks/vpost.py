# After vbuild/sf40b: sets suggested-citation titles ("Title (SFxxxx vX)") and head/og/twitter descriptions for SF0037-39. Run: python3 vpost.py. Edit VER/DESC per release.
"""Post-build fixes for the four verification-stack pages: citation titles and head descriptions.
Run after vbuild.py and sf40b.py."""
import re
R = '/home/user/synthience.org/research/'
VER = {'SF0037': 'v1.6', 'SF0038': 'v2.8', 'SF0039': 'v1.7'}
TITLE = {'SF0037': 'Citation Verification Protocol (CVP)', 'SF0038': 'Ingestion Verification Protocol (IVP)',
         'SF0039': 'Context Representation Drift (CRD)'}
DESC = {
 'SF0037': "The Citation Verification Protocol (CVP) is a domain-general method for verifying citations: each citation must be real, correctly identified and read to confirm it supports the specific claim it is used to justify, with foundational attributions that are identified but not read reported separately.",
 'SF0038': "The Ingestion Verification Protocol (IVP) defines a practical, platform-agnostic method for verifying, through an observable processing record and human adjudication, that an AI system has actively processed a document to a degree adequate for reliable downstream use.",
 'SF0039': "Context Representation Drift (CRD) names the progressive loss of fidelity to task-relevant information that AI systems show over extended interaction, with a detection procedure that needs no access to model internals and re-grounding practices that manage it.",
}
for pid in VER:
    s = open(R + pid + '.html').read()
    s = re.sub(r'(<div class="citation-label">Suggested Citation</div>\n  Gantz, T\. W\. \(\d{4}\)\. ).*?(<a href)',
               lambda m: m.group(1) + f'{TITLE[pid]} ({pid} {VER[pid]}). Synthience Institute. ' + m.group(2), s, count=1)
    d = DESC[pid]
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + d + ' Synthience Institute.', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + d, s, count=1)
    s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + d, s, count=1)
    open(R + pid + '.html', 'w').write(s)
    print(pid, re.search(r'Suggested Citation</div>\n  (.*)', s).group(1)[:140])
