"""Build article (लेख) pages for ankurx.in.

Each article lives in lekh/<slug>/article_body.html (an <article> block). This script wraps it in the
main site's head/CSS, header and footer (taken from index.html) and writes lekh/<slug>/index.html,
plus the list page lekh/index.html. Article list = ARTICLES below (newest first).

Usage: python3 tools/build_lekh.py      (then: python3 tools/publish.py push "message")
"""
import os, re, html

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES = [  # slug, title, date (display), one-line summary
    ("chhath-puja", "हमारी छठ पूजा: इसका इतिहास, वर्तमान स्वरूप और आध्यात्मिक महत्त्व", "13 नवंबर 2026",
     "न मूर्ति, न मंदिर, न पंडित: सूरज, नदी और व्रती के संयम का महापर्व। इसका इतिहास, आज की तस्वीर और बाकी पूजाओं से इसका फ़र्क।"),
]

EXTRA_CSS = """
/* ---- लेख (articles) ---- */
.lekh{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:22px 20px 26px;margin:18px 0 28px}
.lekh .ltitle{font-family:var(--display);font-size:clamp(1.6rem,4.6vw,2.3rem);line-height:1.25;margin:.2em 0 .3em;color:var(--ink)}
.lekh .byline{color:var(--ink2);margin:0 0 1em;font-size:.95rem}
.lekh .lede{font-size:1.12rem;font-weight:500;border-left:4px solid var(--turmeric);padding:.2em 0 .2em .8em}
.lekh h2{font-family:var(--display);font-size:1.45rem;margin:1.5em 0 .4em;color:var(--leaf)}
.lekh p,.lekh li{font-size:1.06rem;line-height:1.85}
.lekh ul,.lekh ol{padding-left:1.3em}
.lekh li{margin:.45em 0}
.compare{display:grid;gap:10px;margin:14px 0}
.crow{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--ground)}
.crow > div{line-height:1.7}
.ctopic{font-weight:700;color:var(--vermilion)}
.clab{font-weight:700;color:var(--ink2)}
@media (min-width:720px){.crow{display:grid;grid-template-columns:9rem 1fr 1.4fr;gap:12px;align-items:start}}
.lekh .wish{font-weight:700;color:var(--leaf);text-align:center;margin-top:1.4em}
.sources{font-size:.92rem}
.sources li{font-size:.92rem;line-height:1.6;word-break:break-word}
.llist{display:grid;gap:12px;margin:18px 0 28px}
.lcard{display:block;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;color:var(--ink)}
.lcard h3{font-family:var(--display);font-size:1.3rem;margin:0 0 .3em;color:var(--leaf)}
.lcard small{color:var(--ink2)}
.lcard p{margin:.4em 0 0;line-height:1.7}
"""


def parts():
    src = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    head = src[:src.index("</style>")] + EXTRA_CSS + "</style>\n</head>\n<body>\n"
    sprite = src[src.index("<svg width=\"0\""):src.index("</svg>", src.index("<svg width=\"0\"")) + 6]
    header = src[src.index('<div class="band"'):src.index("</header>") + 9]
    footer = src[src.index('<footer class="wrap">'):src.index("</footer>") + 9]
    # links in header/footer must go back to the main page
    header = header.replace('href="#"', 'href="/"').replace('href="#', 'href="/#').replace('href="/lekh/"', 'href="/lekh/"')
    header = re.sub(r'<a href="/lekh/" data-nav="lekh">', '<a href="/lekh/" data-nav="lekh" aria-current="page">', header)
    footer = footer.replace('href="#', 'href="/#')
    return head, sprite, header, footer


def page(head, sprite, header, footer, title, desc, url, body):
    h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | AnkurX</title>", head, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + html.escape(desc), h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + html.escape(title), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + html.escape(desc), h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url, h)
    return f"{h}{sprite}\n{header}\n<main><div class=\"wrap\">\n{body}\n</div></main>\n{footer}\n</body>\n</html>\n"


def main():
    head, sprite, header, footer = parts()
    for slug, title, date, summary in ARTICLES:
        d = os.path.join(SITE, "lekh", slug)
        body = open(os.path.join(d, "article_body.html"), encoding="utf-8").read()
        out = page(head, sprite, header, footer, title, summary, f"https://ankurx.in/lekh/{slug}/", body)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
        print("built lekh/%s/index.html" % slug)
    cards = "\n".join(
        f'<a class="lcard" href="/lekh/{s}/"><h3>{html.escape(t)}</h3><small>{html.escape(dt)}</small><p>{html.escape(sm)}</p></a>'
        for s, t, dt, sm in ARTICLES)
    body = f'<section><h2>लेख</h2><p class="sub">खबर के पीछे की समझ: इतिहास, समाज और संस्कृति पर लेख।</p><div class="llist">{cards}</div></section>'
    out = page(head, sprite, header, footer, "लेख", "AnkurX के लेख: इतिहास, समाज और संस्कृति", "https://ankurx.in/lekh/", body)
    open(os.path.join(SITE, "lekh", "index.html"), "w", encoding="utf-8").write(out)
    print("built lekh/index.html")


if __name__ == "__main__":
    main()
