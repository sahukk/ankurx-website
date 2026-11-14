"""Build article (लेख) pages for ankurx.in.

Each article lives in lekh/<slug>/article_body.html (an <article> block). This script wraps it in the
main site's head/CSS, header and footer (taken from index.html) and writes lekh/<slug>/index.html,
plus the list page lekh/index.html. Article list = ARTICLES below (newest first).

Usage: python3 tools/build_lekh.py      (then: python3 tools/publish.py push "message")
"""
import os, re, html

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES = [  # slug, title, date (display), one-line summary
    ("dr-s-siddharth", "डॉ. एस. सिद्धार्थ: अफ़सर, पायलट, चित्रकार, और दिल से एक विद्यार्थी", "14 नवंबर 2026",
     "प्रतिभा परिचय: IIT-IIM से पढ़े 1991 बैच के आईएएस, मुज़फ़्फ़रपुर के पूर्व डीएम, पायलट, फ़ोटोग्राफ़र और चित्रकार की कहानी।"),
    ("srilanka-diary", "श्री लंका डायरी: हाथी, मसाले, चाय और 30 मिनट में थाने की रिपोर्ट", "13 नवंबर 2026",
     "अगस्त 2023 की श्री लंका यात्रा: पिन्नावाला के हाथी, सिगिरिया, कैंडी, नुवारा एलिया की चाय, बेंटोटा का समुद्र और कोलंबो।"),
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
.lekh figure{margin:16px 0 20px}
.lekh figure img{display:block;width:100%;max-height:520px;object-fit:contain;background:var(--ground);border-radius:10px}
.lekh figcaption{font-size:.9rem;color:var(--ink2);text-align:center;margin-top:6px}
.lekh blockquote{margin:12px 0 16px;padding:12px 16px;border-left:4px solid var(--leaf);background:var(--ground);border-radius:8px;font-size:1.06rem;line-height:1.8}
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


SHARE_CSS = """
/* ---- like + share bar ---- */
.sbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0 18px}
.sbar .sb{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--paper);color:var(--ink);
  border-radius:999px;padding:7px 13px;font:600 .95rem var(--body);cursor:pointer;text-decoration:none;line-height:1}
.sbar .sb:hover{border-color:var(--leaf)}
.sbar .like[aria-pressed="true"]{background:var(--bad-bg);border-color:var(--vermilion);color:var(--vermilion)}
.sbar .like .n{min-width:1ch}
.sbar .wa{color:#128C4B}.sbar .fb{color:#1565D8}
.sbar .note{font-size:.85rem;color:var(--ink2)}
.sbar svg{width:18px;height:18px;fill:currentColor}
"""

SHARE_JS = """
<script>
(function(){
  var NS="ankurx.in", API="https://abacus.jasoncameron.dev";
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
  document.querySelectorAll(".sbar").forEach(function(bar){
    var key="likes-"+bar.dataset.slug, url=bar.dataset.url, title=bar.dataset.title;
    var like=bar.querySelector(".like"), n=bar.querySelector(".like .n");
    function show(v){document.querySelectorAll('.sbar[data-slug="'+bar.dataset.slug+'"] .like .n').forEach(function(x){x.textContent=v>0?v:""})}
    function mark(){document.querySelectorAll('.sbar[data-slug="'+bar.dataset.slug+'"] .like').forEach(function(x){x.setAttribute("aria-pressed","true")})}
    if(store("liked:"+key))mark();
    if(!window.__lk){window.__lk={}}
    if(!window.__lk[key]){window.__lk[key]=1;
      fetch(API+"/get/"+NS+"/"+key).then(function(r){return r.json()}).then(function(d){if(d&&d.value>=0)show(d.value)}).catch(function(){});}
    like.addEventListener("click",function(){
      if(store("liked:"+key))return;
      store("liked:"+key,"1");mark();
      fetch(API+"/hit/"+NS+"/"+key).then(function(r){return r.json()}).then(function(d){if(d&&d.value)show(d.value)}).catch(function(){});
    });
    var enc=encodeURIComponent;
    bar.querySelector(".wa").href="https://wa.me/?text="+enc(title+"\\n"+url);
    bar.querySelector(".fb").href="https://www.facebook.com/sharer/sharer.php?u="+enc(url);
    bar.querySelector(".tw").href="https://twitter.com/intent/tweet?text="+enc(title)+"&url="+enc(url);
    var cp=bar.querySelector(".cp");
    cp.addEventListener("click",function(){
      var done=function(){var o=cp.innerHTML;cp.textContent="लिंक कॉपी हो गया ✓";setTimeout(function(){cp.innerHTML=o},1800)};
      if(navigator.share&&/Mobi|Android/i.test(navigator.userAgent)){navigator.share({title:title,url:url}).catch(function(){});return}
      if(navigator.clipboard){navigator.clipboard.writeText(url).then(done,function(){prompt("यह लिंक कॉपी करें:",url)})}
      else{prompt("यह लिंक कॉपी करें:",url)}
    });
  });
})();
</script>
"""


def share_bar(slug, title, url):
    heart = '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.9 4.5c2.1 0 3.5 1.1 5.1 2.9 1.6-1.8 3-2.9 5.1-2.9 3.9 0 6 3.9 4.5 7.3C19.5 16.4 12 21 12 21z"/></svg>'
    return (f'<div class="sbar" data-slug="{slug}" data-url="{url}" data-title="{html.escape(title)}">'
            f'<button class="sb like" type="button" aria-pressed="false" aria-label="पसंद करें">{heart}<span>पसंद आया</span> <span class="n"></span></button>'
            '<a class="sb wa" target="_blank" rel="noopener">WhatsApp</a>'
            '<a class="sb fb" target="_blank" rel="noopener">Facebook</a>'
            '<a class="sb tw" target="_blank" rel="noopener">X</a>'
            '<button class="sb cp" type="button">🔗 लिंक कॉपी / शेयर</button>'
            '</div>')


def main():
    head, sprite, header, footer = parts()
    head = head.replace("</style>", SHARE_CSS + "</style>")
    for slug, title, date, summary in ARTICLES:
        d = os.path.join(SITE, "lekh", slug)
        url = f"https://ankurx.in/lekh/{slug}/"
        body = open(os.path.join(d, "article_body.html"), encoding="utf-8").read()
        bar = share_bar(slug, title, url)
        body = re.sub(r'(<p class="byline">.*?</p>)', lambda m: m.group(1) + "\n  " + bar, body, count=1, flags=re.S)
        end_bar = '<p class="note" style="margin-top:1.6em">लेख अच्छा लगा? पसंद करें और दोस्तों से शेयर करें:</p>' + bar
        if "<h2>स्रोत</h2>" in body:
            body = body.replace("<h2>स्रोत</h2>", end_bar + "\n  <h2>स्रोत</h2>", 1)
        else:
            body = body.replace("</article>", end_bar + "\n</article>", 1)
        body += SHARE_JS
        out = page(head, sprite, header, footer, title, summary, url, body)
        img = os.path.join(d, "share.jpg")
        if os.path.exists(img):
            og = (f'<meta property="og:image" content="{url}share.jpg">\n<meta property="og:image:width" content="1200">\n'
                  f'<meta property="og:image:height" content="630">\n<meta property="og:type" content="article">\n'
                  '<meta name="twitter:card" content="summary_large_image">\n')
            out = out.replace('<meta name="theme-color"', og + '<meta name="theme-color"', 1)
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
