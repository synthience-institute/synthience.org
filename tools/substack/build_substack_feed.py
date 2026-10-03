#!/usr/bin/env python3
"""Build an RSS 2.0 feed (full text in content:encoded) of every published Field Note
and Practitioner Guide, plus a short note on every published paper, for Substack's
"Import posts" tool.

Usage: build_substack_feed.py REPO OUTDIR [--no-papers] [--paper-image URL]
Writes OUTDIR/substack-all.xml (articles and paper notes, newest first),
OUTDIR/substack-articles.xml (articles only), OUTDIR/substack-pilot.xml (the PILOT pieces),
and OUTDIR/preview/<ID>.html (a paste file per post, 06_article_production_guide Section 1.12).
Paper notes come from paper_notes.json beside this script. With --paper-image, each note carries
that image after its "Read the full paper" line (the back catalog uses one Institute logo card,
so Substack's cards show the logo instead of an empty grey box; a new paper's note gets its own
announcement image instead).
"""
import sys, os, re, copy, html, json
from datetime import datetime
from email.utils import format_datetime
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

REPO, OUT = sys.argv[1], sys.argv[2]
WITH_PAPERS = "--no-papers" not in sys.argv[3:]
PAPER_IMAGE = sys.argv[sys.argv.index("--paper-image") + 1] if "--paper-image" in sys.argv else None
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://synthience.org"
PILOT = {"FN-018", "PG-003"}
ET = ZoneInfo("America/New_York")
LISTING_DATES, LISTING_ORDER = {}, {}
for _f in ("field-notes.html", "practitioner-guides.html"):
    _s = open(os.path.join(REPO, _f), encoding="utf-8").read()
    for _id, _d in re.findall(r'id:\s*"((?:FN|PG)-\d{3})",(?:(?!id:).)*?date:\s*"(\d{4}-\d{2}-\d{2})"', _s, re.S):
        LISTING_DATES.setdefault(_id, _d)
    for _b in re.findall(r"\{([^{}]*?id:\s*\"(?:FN|PG)-\d{3}\"[^{}]*?)\}", _s, re.S):
        _m = re.search(r'id:\s*"((?:FN|PG)-\d{3})"', _b); _o = re.search(r"dateOrder:\s*(\d+)", _b)
        if _o:
            LISTING_ORDER.setdefault(_m.group(1), int(_o.group(1)))

# Styled boxes on the site that become quotes on Substack
QUOTE_CLASSES = {"fn-callout", "fn-pullquote", "pg-callout", "response-block", "key-insight",
                 "try-this", "pg-rule", "operator-check", "warning", "shortcut"}
# Monospace boxes on the site that become code blocks (keeps line breaks, easy to copy)
PRE_CLASSES = {"prompt-block", "diff-example"}


def absolute(url, section):
    if not url or re.match(r"^(https?:|mailto:|#)", url):
        return url
    if url.startswith("../"):
        return f"{SITE}/{url[3:]}"
    if url.startswith("/"):
        return SITE + url
    return f"{SITE}/{section}/{url}"


def youtube_watch(src):
    m = re.search(r"youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]+)", src or "")
    return f"https://www.youtube.com/watch?v={m.group(1)}" if m else src


def text_lines(el):
    """Text of a monospace box, keeping its line breaks."""
    if el.find("div"):  # diff-example: one div per line
        lines = []
        for d in el.find_all("div", recursive=False):
            t = d.get_text().replace("\xa0", " ")
            lines.append(t.rstrip())
        return "\n".join(lines)
    return el.get_text().strip("\n")


def convert(path, section, kind):
    s = open(path, encoding="utf-8").read()
    soup = BeautifulSoup(s, "html.parser")
    main = soup.find("main")
    title = main.find("h1").get_text(" ", strip=True)
    meta = main.find(class_="article-meta")
    spans = [x.get_text(strip=True) for x in meta.find_all("span")]
    doc_id = spans[0]
    # Publication date: the listing page's date (exact for every piece); the page's own date is cross-checked
    iso = LISTING_DATES[doc_id]
    dt = datetime.strptime(iso, "%Y-%m-%d").replace(hour=9, tzinfo=ET)
    date_txt = dt.strftime("%B %-d, %Y")
    page_date = next((x for x in spans if re.match(r"[A-Z][a-z]+ \d{1,2}, \d{4}$", x)), None)
    if page_date != date_txt:
        print(f"NOTE {doc_id}: page shows {spans[1:2]}, listing date {date_txt} used", file=sys.stderr)
    url = f"{SITE}/{section}/{os.path.basename(path)}"

    for sel in ["back-link", "article-meta", "article-footer", "subscribe-box"]:
        for x in main.find_all(class_=sel):
            x.decompose()
    main.find("h1").decompose()
    for x in main.find_all(["script", "style"]):
        x.decompose()
    for x in main.find_all(string=lambda t: isinstance(t, Comment)):
        x.extract()

    # Dek: the first paragraph when it is wholly italic
    # Dek: the first wholly italic paragraph near the top (after any "This guide expands..." orientation line)
    dek, first_p = "", None
    for cand in main.find_all("p", limit=3):
        if "pg-orient" in (cand.get("class") or []):
            continue
        if cand.find("em") and cand.get_text(strip=True) == cand.find("em").get_text(strip=True):
            dek, first_p = cand.get_text(" ", strip=True), cand
        break
    md = soup.find("meta", attrs={"name": "description"})
    subtitle = dek or (md["content"].strip() if md else "")

    # Videos -> a link line
    for vc in main.find_all(class_="video-container"):
        ifr = vc.find("iframe")
        w = youtube_watch(ifr.get("src")) if ifr else ""
        # Substack drops embedded players: show the video's YouTube thumbnail, linked to the video, plus a text link
        vid = re.search(r"v=([A-Za-z0-9_-]+)", w or "")
        fig = soup.new_tag("p")
        if vid:
            la = soup.new_tag("a", href=w)
            la.append(soup.new_tag("img", src=f"https://img.youtube.com/vi/{vid.group(1)}/maxresdefault.jpg", alt="Video thumbnail: " + title))
            fig.append(la)
        p = soup.new_tag("p")
        p.append("Watch the video: ")
        a = soup.new_tag("a", href=w); a.string = w
        p.append(a)
        vc.replace_with(fig)
        fig.insert_after(p)
    for x in main.find_all(class_="media-tag"):
        x.decompose()

    # Tables -> caption line plus one list item per row
    for tw in main.find_all("table"):
        heads = [th.get_text(" ", strip=True) for th in tw.find("thead").find_all("th")] if tw.find("thead") else []
        frag = []
        cap = tw.find("caption")
        if cap:
            p = soup.new_tag("p"); em = soup.new_tag("em"); em.string = cap.get_text(" ", strip=True); p.append(em)
            frag.append(p)
        ul = soup.new_tag("ul")
        rows = tw.find("tbody").find_all("tr") if tw.find("tbody") else tw.find_all("tr")[1:]
        for tr in rows:
            cells = tr.find_all(["th", "td"])
            li = soup.new_tag("li")
            for i, c in enumerate(cells):
                h = heads[i] if i < len(heads) else ""
                if i > 0:
                    li.append(soup.new_tag("br"))
                if h:
                    em = soup.new_tag("em"); em.string = h + ":"; li.append(em); li.append(" ")
                if i == 0:
                    st = soup.new_tag("strong"); st.string = c.get_text(" ", strip=True); li.append(st)
                else:
                    for ch in list(c.contents):
                        li.append(copy.copy(ch))
            ul.append(li)
        frag.append(ul)
        target = tw.parent if tw.parent.name == "div" and "table-scroll" in (tw.parent.get("class") or []) else tw
        for f in frag:
            target.insert_before(f)
        target.decompose()

    # Monospace boxes -> code blocks, with any "YOU SAY:" style label as a bold line above
    for cls in PRE_CLASSES:
        for box in main.find_all(class_=cls):
            label = box.find(class_="label", recursive=False)
            out = []
            if label and cls == "prompt-block":
                p = soup.new_tag("p"); st = soup.new_tag("strong"); st.string = label.get_text(strip=True); p.append(st)
                out.append(p)
                label.decompose()
            pre = soup.new_tag("pre"); code = soup.new_tag("code"); code.string = text_lines(box).strip("\n")
            pre.append(code); out.append(pre)
            for o in out:
                box.insert_before(o)
            box.decompose()

    # Labels inside text -> bold with a space after
    for lab in main.find_all("span", class_=["label", "shortcut-label", "practice-num"]):
        st = soup.new_tag("strong"); st.string = lab.get_text(strip=True)
        lab.replace_with(st)
        nxt = st.next_sibling
        if not (isinstance(nxt, NavigableString) and nxt.startswith((" ", "\n"))):
            st.insert_after(" ")

    # Series box header -> bold paragraph
    for h in main.find_all(class_="core-series-header"):
        h.name = "p"; inner = h.get_text(strip=True); h.clear()
        st = soup.new_tag("strong"); st.string = inner; h.append(st)

    # Quote boxes -> blockquote; text sitting directly inside is wrapped in paragraphs
    for cls in QUOTE_CLASSES:
        for box in main.find_all(class_=cls):
            box.name = "blockquote"

    for bq in main.find_all("blockquote"):
        wrap_loose_text(soup, bq)

    # Links absolute, images absolute; strip presentation attributes
    for a in main.find_all("a"):
        href = absolute(a.get("href"), section)
        a.attrs = {"href": href} if href else {}
    for img in main.find_all("img"):
        img.attrs = {"src": absolute(img.get("src"), section), "alt": img.get("alt", "")}

    # Unwrap divs and spans (after quotes are blockquotes), wrapping loose text first
    for d in main.find_all("div"):
        wrap_loose_text(soup, d)
        d.unwrap()
    for sp in main.find_all("span"):
        sp.unwrap()
    for t in main.find_all(True):
        if t.name not in ("a", "img"):
            t.attrs = {}

    # Site-first line (06 Section 1.10), right after the dek, or at the top if there is none
    site = soup.new_tag("p"); site.append("Originally published at synthience.org: ")
    a = soup.new_tag("a", href=url); a.string = url; site.append(a)
    if dek:
        # Substack previews a post by its first paragraph, so the summary line goes first
        # (on guides it follows the "This guide expands..." orientation line on the site)
        if main.find("p") is not first_p:
            first_p.extract()
            main.insert(0, first_p)
        first_p.insert_after(site)
    else:
        main.insert(0, site)

    body = "".join(str(c) for c in main.contents)
    # PG-003 points to colored placeholder text; Substack drops the color, and the placeholders are bracketed
    body = body.replace("Text in this color is a placeholder", "Text in [square brackets] is a placeholder")
    body = re.sub(r"\n\s*\n+", "\n\n", body).strip()
    return dict(id=doc_id, title=title, dek=subtitle, date=dt, date_txt=date_txt, url=url, body=body, kind=kind,
                dateOrder=LISTING_ORDER.get(doc_id), type=None)


def wrap_loose_text(soup, el):
    """Put bare text and inline elements directly inside a block into <p> tags."""
    BLOCK = {"p", "ul", "ol", "pre", "blockquote", "h2", "h3", "h4", "figure", "div", "hr", "table", "img"}
    run = []

    def flush(before):
        if any((isinstance(x, NavigableString) and x.strip()) or isinstance(x, Tag) for x in run):
            p = soup.new_tag("p")
            for x in run:
                p.append(x.extract())
            if before is None:
                el.append(p)
            else:
                before.insert_before(p)
        else:
            for x in run:
                x.extract()
        run.clear()

    for ch in list(el.contents):
        if isinstance(ch, Tag) and ch.name in BLOCK:
            flush(ch)
        elif isinstance(ch, Comment):
            continue
        else:
            run.append(ch)
    flush(None)


def js_blocks(path, key):
    s = open(path, encoding="utf-8").read()
    return re.findall(r"\{([^{}]*?" + key + r"[^{}]*?)\}", s, re.S)


def js_field(b, k):
    m = re.search(k + r':\s*"([^"]*)"', b)
    return m.group(1) if m else None


def js_num(b, k):
    m = re.search(k + r":\s*(\d+)", b)
    return int(m.group(1)) if m else None


TYPE_ORDER = {"whitepaper": 0, "mortar": 1, "framework": 2, "protocol": 2, "research": 3, "definitions": 4}


def paper_items():
    notes = json.load(open(os.path.join(HERE, "paper_notes.json"), encoding="utf-8"))
    items = []
    for b in js_blocks(os.path.join(REPO, "research.html"), "read:"):
        pid = js_field(b, "id")
        d = datetime.strptime(js_field(b, "date"), "%B %d, %Y")
        n = notes[pid]
        url = f"{SITE}/research/{pid}.html"
        paras = [x.strip() for x in n["text"].split("\n\n") if x.strip()]
        body = []
        for para in paras:
            h = html.escape(para, quote=False)
            h = re.sub(r"(https://[^\s<]+?)([.,;:)]?)(?=\s|$)", r'<a href="\1">\1</a>\2', h)
            if h.startswith("*") and h.endswith("*"):
                h = "<em>" + h[1:-1] + "</em>"
            body.append(f"<p>{h}</p>")
            if PAPER_IMAGE and para.startswith("Read the full paper"):
                body.append(f'<p><img src="{PAPER_IMAGE}" alt="Synthience Institute logo"></p>')
        dek = re.sub(r"^\*|\*$", "", paras[0])
        # Post title: the paper's exact title as on research.html (and in its citation tags)
        items.append(dict(id=pid, title=html.unescape(js_field(b, "title")), dek=dek, date=d.replace(hour=9, tzinfo=ET),
                          date_txt=d.strftime("%B %-d, %Y"), url=url, body="\n".join(body), kind="PAPER",
                          dateOrder=js_num(b, "dateOrder"), type=js_field(b, "type")))
    return items


def order_same_day(items):
    """Posts that share a date get minutes after 09:00 ET so Substack's newest-first archive shows them in
    the order the site does: the pieces' own dateOrder (research.html or the listing pages) when every one
    carries it, else updates.html's order when it lists them all, else research.html's By Date rule."""
    upd = []
    for b in js_blocks(os.path.join(REPO, "updates.html"), "dateDisplay"):
        m = re.search(r"([A-Z][A-Z-]*\d+(?:-VR1)?)\.html", js_field(b, "link") or "")
        if m:
            upd.append(m.group(1))
    groups = {}
    for it in items:
        groups.setdefault(it["date"].date(), []).append(it)
    for g in groups.values():
        if len(g) == 1:
            continue
        if all(it.get("dateOrder") for it in g):
            shown = sorted(g, key=lambda it: -it["dateOrder"])
        elif all(it["id"] in upd for it in g):
            shown = sorted(g, key=lambda it: upd.index(it["id"]))
        else:  # research.html's fallback: typeOrder, then ID descending
            shown = sorted(g, key=lambda it: it["id"], reverse=True)
            shown = sorted(shown, key=lambda it: (-(it.get("dateOrder") or 0), TYPE_ORDER.get(it.get("type"), 5)))
        for pos, it in enumerate(shown):
            it["date"] = it["date"].replace(minute=len(shown) - 1 - pos)


def rss(items, title):
    def cdata(x):
        return "<![CDATA[" + x.replace("]]>", "]]]]><![CDATA[>") + "]]>"
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">',
           "<channel>",
           f"<title>{html.escape(title)}</title>",
           f"<link>{SITE}/</link>",
           "<description>Field Notes, Practitioner Guides and paper notes from the Synthience Institute.</description>",
           "<language>en-us</language>"]
    for it in items:
        out += ["<item>",
                f"<title>{html.escape(it['title'])}</title>",
                # Link without ".html" (the site serves both): Substack builds the post's address from it (/p/fn-018)
                f"<link>{it['url'][:-5]}</link>",
                f'<guid isPermaLink="true">{it["url"][:-5]}</guid>',
                f"<pubDate>{format_datetime(it['date'])}</pubDate>",
                "<dc:creator>Thomas W. Gantz</dc:creator>",
                f"<category>{ {'FN': 'Field Notes', 'PG': 'Practitioner Guides'}.get(it['kind'], 'Papers') }</category>",
                f"<description>{cdata(it['dek'])}</description>",
                f"<content:encoded>{cdata(it['body'])}</content:encoded>",
                "</item>"]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


def main():
    items = []
    for section, kind, pat in [("field-notes", "FN", r"FN-\d{3}\.html$"), ("practitioner-guides", "PG", r"PG-\d{3}\.html$")]:
        d = os.path.join(REPO, section)
        for f in sorted(os.listdir(d)):
            if re.match(pat, f):
                items.append(convert(os.path.join(d, f), section, kind))
    if WITH_PAPERS:
        items += paper_items()
    order_same_day(items)
    items.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
    open(os.path.join(OUT, "substack-all.xml"), "w").write(rss(items, "Synthience Institute"))
    open(os.path.join(OUT, "substack-articles.xml"), "w").write(rss([i for i in items if i["kind"] != "PAPER"], "Synthience Institute"))
    open(os.path.join(OUT, "substack-pilot.xml"), "w").write(rss([i for i in items if i["id"] in PILOT], "Synthience Institute"))
    for it in items:
        open(os.path.join(OUT, "preview", it["id"] + ".html"), "w").write(
            f"<!doctype html><meta charset='utf-8'><title>{html.escape(it['title'])}</title>"
            f"<body style='max-width:680px;margin:2rem auto;font-family:Georgia,serif;line-height:1.6;padding:0 16px'>"
            f"<h1>{html.escape(it['title'])}</h1><p style='color:#666'>{it['date_txt']} · Thomas W. Gantz</p>{it['body']}</body>")
    for it in items:
        print(f"{it['id']}\t{it['date'].strftime('%Y-%m-%d %H:%M')}\t{len(it['body']):>6}\t{it['title']}")
    print(len(items), "items")


main()
