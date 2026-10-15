# Claim-language check (09_instance_briefing Section 2.3, "Say whose claim it is"): lists every empirical-sounding word in the site's own pages, with its context, for a person to judge; it changes nothing. Run from the repository root: python3 tools/checks/claimcheck.py [page.html ...]. With no arguments it checks the site pages that summarize the papers (not the paper or article pages, whose wording follows their published text, and not the article index pages).
import html, re, sys

PAGES = ["index.html", "about.html", "founder.html", "faq.html", "glossary.html", "research.html", "updates.html"]
# Common verbs such as "shows" and "finding" are left out: on these pages they almost always describe
# outside work or an article's argument, and listing them buries the hits that matter.
WORDS = ["empirical", "empirically", "observed", "documented", "documenting", "demonstrates", "demonstrated",
         "reproducible", "measurable", "longitudinal", "systematically", "proven"]
# Phrases that are correct by design and would only add noise.
ALLOW = ["pre-empirical", "not empirical", "no empirical", "empirical testing by", "independent empirical",
         "documented in", "documented revisions"]

pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in WORDS) + r")\b", re.I)

def text_lines(path):
    raw = open(path, encoding="utf-8").read()
    for n, line in enumerate(raw.split("\n"), 1):
        # Keep text in scripts too: research.html and updates.html hold their entries in JS arrays.
        t = html.unescape(re.sub(r"<[^>]+>", " ", line))
        yield n, re.sub(r"\s+", " ", t)

total = 0
for page in sys.argv[1:] or PAGES:
    for n, t in text_lines(page):
        low = t.lower()
        for m in pattern.finditer(t):
            window = low[max(0, m.start() - 40):m.end() + 40]
            if any(a in window for a in ALLOW):
                continue
            total += 1
            print(f"{page}:{n}: ...{t[max(0, m.start() - 70):m.end() + 70].strip()}...")
print(f"{total} hits to review. Each is fine where it describes cited outside work or a definition in observable terms.")
