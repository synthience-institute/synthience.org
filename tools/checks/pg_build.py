# Builds practitioner-guides/PG-016.html from its markdown on the PG-015 template (head, Article JSON-LD, infographic, optional wide second figure, checklist, further reading, footer). Run: python3 pg_build.py text.md YYYY-MM-DD 1.0. Adapt names/captions/DESC for a new guide.
"""Build practitioner-guides/PG-016.html from the markdown text. Usage: build.py <md> <YYYY-MM-DD> <version>"""
import re, sys, html, datetime, json
md, PUB, VER = sys.argv[1], sys.argv[2], sys.argv[3]
d = datetime.date.fromisoformat(PUB); DISP = d.strftime('%B ') + str(d.day) + d.strftime(', %Y')
SHARE_OK = True
lines = open(md, encoding='utf-8').read().split('\n')

def typo(s):
    s = re.sub(r'(^|[\s(\[—–-])"', r'\1“', s); s = s.replace('"', '”')
    s = re.sub(r"(\w)'", r"\1’", s); s = re.sub(r"(^|\s)'", r"\1‘", s)
    return s
def inline(s):
    links = []
    def keep(m):
        links.append((m.group(1), m.group(2))); return f'\x00{len(links)-1}\x00'
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', keep, s)
    s = html.escape(typo(s), quote=False)
    s = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', s)
    s = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    for i, (t, u) in enumerate(links):
        s = s.replace(f'\x00{i}\x00', f'<a href="{u}">{html.escape(typo(t), quote=False)}</a>')
    return s

title = lines[0][2:].strip()
subtitle = lines[2].strip().strip('*')
body = lines[lines.index('---') + 1:]
out, lst, sec = [], None, None
CAPTION = 'The coordinating Claude instance (left) and the checking instance (right) during the final stage, with the founder relaying between them.'
FIG2 = ('<figure class="article-figure wide">\n  <a href="../assets/images/PG-016-two-instances.jpg" target="_blank" rel="noopener">'
        '<img src="../assets/images/PG-016-two-instances.jpg" width="2000" height="873" loading="lazy" decoding="async" '
        'alt="Screenshot of two browser windows side by side: on the left, the coordinating Claude instance finalizing the four protocol papers; on the right, the checking Claude instance building the website pages, with the outside reviewer&rsquo;s confirmation being relayed in."></a>\n'
        f'  <figcaption>{html.escape(CAPTION, quote=False)} Select the image to open it full size.</figcaption>\n</figure>')
def close():
    global lst
    if lst: out.append('</ul>'); lst = None
for l in body:
    if not l.strip():
        close(); continue
    if l.startswith('## '):
        close()
        if sec == 'What the Human Did': out.append(FIG2)
        sec = l[3:].strip()
        if sec == 'Further Reading':
            out.append('<div class="further-reading">\n<h3>Further reading</h3>')
        else:
            out.append(f'<h3>{inline(sec)}</h3>')
        continue
    if l.startswith('- '):
        item = l[2:]
        if 'chatgpt.com/share' in item and not SHARE_OK:
            out.append('  <!-- ChatGPT share link held until the PCP has skimmed the shared page -->'); continue
        if lst is None:
            out.append('<ul class="checklist">' if sec == 'Checklist' else '<ul>'); lst = 'ul'
        out.append(f'  <li>{inline(item)}</li>'); continue
    close(); out.append(f'<p>{inline(l.strip())}</p>')
close(); out.append('</div>')
bodyhtml = '\n\n'.join(x for x in out)

DESC = ('In September 2026 an outside reviewer found errors in the four protocols the Synthience Institute publishes for checking AI-assisted work. '
        'A worked example of how they were corrected in public: what each protocol caught, where errors hid, what the human decided, and what the run does and does not prove.')
e = lambda s: html.escape(s)
ht = e(typo(title))
tpl = open('/home/user/synthience.org/practitioner-guides/PG-015.html', encoding='utf-8').read()
head_start = tpl[:tpl.index('<meta charset="UTF-8">')]
ld = {"@context": "https://schema.org", "@type": "Article", "headline": typo(title), "description": DESC,
      "author": {"@type": "Person", "name": "Thomas W. Gantz", "url": "https://synthience.org/founder.html",
                 "sameAs": ["https://orcid.org/0009-0003-7168-493X", "https://scholar.google.com/citations?user=TA8Z2GYAAAAJ"]},
      "publisher": {"@type": "Organization", "name": "Synthience Institute", "url": "https://synthience.org/",
                    "logo": {"@type": "ImageObject", "url": "https://synthience.org/assets/images/synthience-logo-black-bg.png"}},
      "datePublished": PUB, "url": "https://synthience.org/practitioner-guides/PG-016.html",
      "mainEntityOfPage": "https://synthience.org/practitioner-guides/PG-016.html",
      "image": "https://synthience.org/assets/images/PG-016_Infographic.jpg", "inLanguage": "en"}
ldtxt = json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n  ')
page = f'''{head_start}<meta charset="UTF-8">
  <title>PG-016: {ht} &middot; Synthience Institute</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{e(DESC)}">
  <meta name="author" content="Thomas W. Gantz">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Synthience Institute">
  <meta property="og:title" content="{ht} &middot; Synthience Institute">
  <meta property="og:description" content="{e(DESC)}">
  <meta property="og:url" content="https://synthience.org/practitioner-guides/PG-016.html">
  <link rel="canonical" href="https://synthience.org/practitioner-guides/PG-016.html">
  <script type="application/ld+json">
  {ldtxt}
  </script>
  <meta property="og:image" content="https://synthience.org/assets/images/PG-016_Infographic.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@SynthienceInst">
  <meta name="twitter:title" content="{ht} &middot; Synthience Institute">
  <meta name="twitter:description" content="{e(DESC)}">
  <meta name="twitter:image" content="https://synthience.org/assets/images/PG-016_Infographic.jpg">
  <link rel="stylesheet" href="../assets/css/style.css">
  <style>
    .article-figure {{ margin: 1.5rem auto 2rem auto; max-width: 480px; }}
    .article-figure img {{ max-width: 100%; height: auto; border-radius: 4px; display: block; margin: 0 auto; }}
    .article-figure.wide {{ max-width: 100%; }}
    .article-figure.wide img {{ border: 1px solid #e0ddd4; }}
    .article-figure figcaption {{ font-size: 0.85rem; color: #8a7f72; margin-top: 0.5rem; font-style: italic; text-align: center; }}
    .article-meta {{ font-size: 0.88rem; color: #8a7f72; margin-bottom: 2rem; }}
    .article-meta span {{ margin-right: 1.2rem; }}
    .back-link {{ font-size: 0.9rem; margin-bottom: 1.5rem; }}
    .back-link a {{ color: #0645ad; text-decoration: none; }}
    .back-link a:hover {{ text-decoration: underline; }}
    .checklist li {{ margin-bottom: 0.55rem; }}
    .further-reading {{ margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e8e4dc; }}
  </style>
</head>
<body>

<header class="site-header">
  <div class="logo">
    <a href="../index.html">
      <img src="../assets/images/synthience-logo-black-bg.png" alt="Synthience Institute logo">
    </a>
  </div>
  <div class="header-text">
    <p class="site-title">Synthience Institute</p>
  </div>
  <nav class="main-nav" id="site-nav"></nav>
</header>
<script src="../assets/js/nav.js"></script>

<main class="content">

<div class="back-link"><a href="../practitioner-guides.html">&larr; All Practitioner Guides</a></div>

<h1 class="page-title">{ht}</h1>

<div class="article-meta">
  <span>PG-016</span>
  <span>{DISP}</span>
  <span>Thomas W. Gantz</span>
</div>

<p><em>{e(typo(subtitle))}</em></p>

<div class="article-figure">
  <img src="../assets/images/PG-016_Infographic.jpg" width="1254" height="1254" loading="lazy" decoding="async" alt="Infographic titled Checking the Checkers: how four verification protocols were corrected in public. Five numbered steps run top to bottom: 1, outside review, an AI reviewer from a different company found real errors; 2, read the sources, every questioned study opened and read in full; 3, check each other, a second AI instance checked every draft; 4, review again, a fresh review, then confirmation of every fix; 5, republish together, all four protocols live the same day, checksums verified. The closing line reads: check the artifact, not the account of it.">
</div>

{bodyhtml}

<div class="article-footer">
<p>Document: PG-016 Practitioner Guide<br>
Version: {VER}<br>
Author: Thomas W. Gantz<br>
Affiliation: Synthience Institute<br>
Date: {DISP}<br>
License: CC-BY 4.0</p>
</div>

</main>

<footer class="site-footer">
  <div id="site-footer"></div>
</footer>
<script src="../assets/js/footer.js"></script>

</body>
</html>
'''
open('/home/user/synthience.org/practitioner-guides/PG-016.html', 'w', encoding='utf-8').write(page)
print('built', len(page))
