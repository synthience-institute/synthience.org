# ONE-OFF record (already applied in PR #39): the companion-page edits for the verification stack (research.html topic/stackOrder/deep link, about/faq/glossary lines, homepage row, updates entry). Kept as a worked example of edit-with-assert; do not re-run.
"""Companion-page edits for the verification-stack batch. Run once from a clean main checkout.
Usage: companion.py [YYYY-MM-DD publication date]"""
import sys, datetime
S = '/home/user/synthience.org/'
PUB = sys.argv[1] if len(sys.argv) > 1 else '2026-09-29'
d = datetime.date.fromisoformat(PUB)
PUBDISP = d.strftime('%B ') + str(d.day) + d.strftime(', %Y')

def edit(fn, pairs):
    s = open(S + fn).read()
    for old, new in pairs:
        assert s.count(old) == 1, (fn, old[:80], s.count(old))
        s = s.replace(old, new)
    open(S + fn, 'w').write(s)
    print(fn, len(pairs), 'edits')

def between(s, a, b):
    i = s.index(a); j = s.index(b, i); return s[i:j]

# ---------- research.html ----------
r = open(S + 'research.html').read()
def desc_of(pid):
    line = [l for l in r.split('\n') if l.startswith(f'  {{ id: "{pid}"')][0]
    return between(line, 'desc: "', '", read:')[len('desc: "'):]
edit('research.html', [
 (desc_of('SF0037'), "Domain-general method for verifying citations in any document whose claims rest on cited sources: each citation must be real, correctly identified, and read to confirm that it supports the specific claim it is used to justify. Defines a three-part verification method with support ratings, evidence anchors and verification tiers; a narrow class of foundational attributions that are identified but not read is reported separately. One of four published protocols forming the Synthience verification stack."),
 (desc_of('SF0038'), "Structured method for verifying, through an observable processing record and human adjudication, that an AI system has processed a supplied document to a degree adequate for the task, rather than answering from partial or superseded content. The system summarizes the document incrementally, with checkpoints tied to the source, and a person reviews that record before work that depends on the document proceeds. One of four published protocols forming the Synthience verification stack."),
 (desc_of('SF0039'), "Names the progressive loss of fidelity to task-relevant information that AI systems show over extended interaction: increasing abstraction, loss of detail, structural flattening and the quiet erosion of earlier constraints, often well before the context window is full. Gives a check a person can run by hand during a live session, without access to model internals, and re-grounding practices that manage drift. One of four published protocols forming the Synthience verification stack: it describes what can happen to a document&rsquo;s representation after ingestion."),
 ('link: "https://doi.org/10.5281/zenodo.18289391", date: "January 18, 2026", topic: "method"',
  'link: "https://doi.org/10.5281/zenodo.18289391", date: "January 18, 2026", topic: "verification", stackOrder: 4'),
 ('link: "https://doi.org/10.5281/zenodo.18075624", date: "December 23, 2025", topic: "verification"',
  'link: "https://doi.org/10.5281/zenodo.18075624", date: "December 23, 2025", topic: "verification", stackOrder: 1'),
 ('link: "https://doi.org/10.5281/zenodo.18289047", date: "January 18, 2026", topic: "verification"',
  'link: "https://doi.org/10.5281/zenodo.18289047", date: "January 18, 2026", topic: "verification", stackOrder: 2'),
 ('link: "https://doi.org/10.5281/zenodo.19151454", date: "March 21, 2026", topic: "verification"',
  'link: "https://doi.org/10.5281/zenodo.19151454", date: "March 21, 2026", topic: "verification", stackOrder: 3'),
 ('''var topicDefs = [
  { key: "foundations",''', '''var topicDefs = [
  { key: "verification", label: "The verification stack", blurb: "Four protocols for checking AI-assisted work: whether citations support their claims, whether a document was processed adequately, whether the theory holds together under review, and how detail erodes over a long session, with a worked verification report" },
  { key: "foundations",'''),
 ('''  { key: "verification", label: "Verification protocols", blurb: "How AI-assisted work is checked" },
''', ''),
 ('''        return td.key === "other" ? !known : d.topic === td.key;
      }).sort(publicationDateSort);''', '''        return td.key === "other" ? !known : d.topic === td.key;
      }).sort(function(a, b) {
        // The verification stack keeps its reading order (stackOrder); other groups sort by date.
        if (byTopic && (a.stackOrder || b.stackOrder)) return (a.stackOrder || 99) - (b.stackOrder || 99) || publicationDateSort(a, b);
        return publicationDateSort(a, b);
      });'''),
 ('''      html += '<div class="doc-section">';''', '''      html += '<div class="doc-section" id="' + (byTopic ? 'topic-' : 'type-') + td.key + '">';'''),
 ('''// === INIT ===
(function() {
''', '''// === INIT ===
(function() {
  // research.html#verification-stack opens the By Topic view at the verification stack.
  if (location.hash === "#verification-stack") activeResearchView = "topic";
'''),
 ('''  renderDocs();
})();''', '''  renderDocs();
  if (location.hash === "#verification-stack") {
    var el = document.getElementById("topic-verification");
    if (el) el.scrollIntoView();
  }
})();'''),
])

# ---------- about.html ----------
a = open(S + 'about.html').read()
old_ver = between(a, '  <li><strong>Verification protocols.</strong>', '\n') + '\n'
edit('about.html', [
 (old_ver, ''),
 ('''<ul>
  <li><strong>Definitions and foundations.</strong>''', '''<ul>
  <li><strong>The verification stack.</strong> How AI-assisted work is checked: citation verification (<a href="research/SF0037.html">SF0037</a>), ingestion verification (<a href="research/SF0038.html">SF0038</a>) and multi-instance theoretical review (<a href="research/SF0040.html">SF0040</a>), with Context Representation Drift (<a href="research/SF0039.html">SF0039</a>), which describes how an AI system&rsquo;s hold on task-relevant detail erodes over extended interaction and how to detect and manage it. A published verification report (<a href="research/SR001-VR1.html">SR001-VR1</a>) is a worked example.</li>
  <li><strong>Definitions and foundations.</strong>'''),
 ('''the Continuity Anchoring Method (<a href="research/SF0005.html">SF0005</a>), Context Representation Drift (<a href="research/SF0039.html">SF0039</a>), the framework for detecting drift in an AI system&rsquo;s representation of the interaction, the Relational Pattern States''',
  '''the Continuity Anchoring Method (<a href="research/SF0005.html">SF0005</a>), the Relational Pattern States'''),
])

IVP_OLD = "when an AI system works from a document, it must demonstrate that it has actually processed it, through structured summaries checked against the source, rather than being taken at its word."
IVP_NEW = "when an AI system works from a document, it summarizes the document as it goes, with checkpoints tied to the source, and a person checks that record before work that depends on the document proceeds, rather than taking the system at its word."
CVP_OLD = "by retrieving and reading the source; long-established works whose full text was not obtained are rated as attributed rather than fully supported."
CVP_NEW = "by retrieving and reading the source; a narrow class of foundational works cited only for attribution, never for a load-bearing claim, is identified but not read, rated as attributed and reported separately."
edit('about.html', [(IVP_OLD, IVP_NEW), (CVP_OLD, CVP_NEW), ('for whether the source actually supports', 'for whether the source supports')])
edit('faq.html', [(IVP_OLD, IVP_NEW), (CVP_OLD, CVP_NEW)])

# ---------- glossary.html ----------
edit('glossary.html', [
 ("and, beyond ordinary citation checking, that the source actually supports the specific claim it is cited for: the verifier retrieves the source, reads the relevant portion and records the evidence found there. Documented in SF0037;",
  "and, beyond ordinary citation checking, that the source supports the specific claim it is cited for: the verifier retrieves the source, reads the relevant portion and records the evidence found there. A narrow class of foundational works cited only for attribution, never for a load-bearing claim, is identified but not read, and reported separately. Documented in SF0037;"),
 ("<p>The progressive degradation of task-relevant information within a system&rsquo;s effective working context during extended interaction. CRD describes degradation of representational fidelity: the quality of the system&rsquo;s access to prior interaction content. Documented in SF0039.</p>",
  "<p>The progressive loss of fidelity to task-relevant information that AI systems show over extended interaction: increasing abstraction, loss of detail, structural flattening, reduced precision and the quiet erosion of earlier constraints, often well before hard capacity limits are reached. CRD is detected from the system&rsquo;s behavior across a session, without access to model internals, and managed by re-grounding. Documented in SF0039.</p>"),
 ("<p>A protocol-governed procedure for confirming that a document or corpus has been successfully loaded into an AI system&rsquo;s working context and is accessible for retrieval and reasoning. Documented in the Ingestion Verification Protocol (SF0038).</p>",
  "<p>A protocol-governed procedure for verifying, through an observable processing record and human adjudication, that an AI system has processed a document to a degree adequate for a stated task. The system summarizes the document incrementally, with checkpoints tied to the source, and a person reviews that record before work that depends on the document proceeds. What is certified is the processing record at the time of review, not comprehension, correctness or later retention. Documented in the Ingestion Verification Protocol (SF0038).</p>"),
])

# ---------- index.html ----------
edit('index.html', [
 ('''  <p class="start-row"><span class="start-label">The research:</span>''',
  '''  <p class="start-row"><span class="start-label">Check AI-assisted work:</span> <a href="research.html#verification-stack">The Synthience verification stack &rarr;</a> <span class="sep">&middot;</span> <a href="research/SF0037.html">Citations (CVP)</a> <span class="sep">&middot;</span> <a href="research/SF0038.html">Ingestion (IVP)</a> <span class="sep">&middot;</span> <a href="research/SF0040.html">Theory review (TCAP)</a> <span class="sep">&middot;</span> <a href="research/SF0039.html">Drift (CRD)</a></p>
  <p class="start-row"><span class="start-label">The research:</span>'''),
])

# ---------- updates.html ----------
entry = f'''var allUpdates = [
  {{
    date: "{PUB}",
    dateDisplay: "{PUBDISP}",
    title: "The Synthience Verification Stack: Four Protocols Updated Together",
    link: "research.html#verification-stack",
    tag: "Revision",
    body: "The four protocols the Institute uses to check AI-assisted work have been revised together and published as new versions on Zenodo: the Citation Verification Protocol (CVP, SF0037), the Ingestion Verification Protocol (IVP, SF0038), the Theoretical Coherence Assurance Protocol (TCAP, SF0040) and Context Representation Drift (CRD, SF0039). Each now states more exactly what it establishes and what it does not. CVP separates citations read in full from a narrow class of foundational attributions that are identified but not read, and reports the two separately. IVP adds coverage evidence to every checkpoint, names the failure in which a revised document uploaded under the same filename is answered from the earlier version, and states that every valid result requires a person&rsquo;s judgment of the processing record. CRD adds a Quick Start, a check anyone can run by hand during a long session, and corrects how four external studies are reported. TCAP&rsquo;s account of the other three is aligned with them. The Research page now groups the four as the verification stack.",
    action: "See the verification stack",
    actionLink: "research.html#verification-stack"
  }},
'''
edit('updates.html', [('var allUpdates = [\n', entry)])
