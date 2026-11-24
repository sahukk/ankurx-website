"""Build article (लेख) pages for ankurx.in.

Each article lives in lekh/<slug>/article_body.html (an <article> block). This script wraps it in the
main site's head/CSS, header and footer (taken from index.html) and writes lekh/<slug>/index.html,
plus the list page lekh/index.html. Article list = ARTICLES below (newest first).

Usage: python3 tools/build_lekh.py      (then: python3 tools/publish.py push "message")
"""
import os, re, html

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES = [  # slug, title, date (display), one-line summary
    ("saans-ka-vigyan", "आपकी नाक चुपके से शिफ्ट बदलती है! साँसों का विज्ञान और अध्यात्म", "24 नवंबर 2026",
     "रास्ता एक, तो नथुने दो क्यों? नासिका चक्र, वेगस नर्व, इड़ा-पिंगला-सुषुम्ना और प्राणायाम: साँसों की कहानी, विज्ञान और अध्यात्म दोनों की नजर से। दो आसान प्रयोगों के साथ।"),
    ("avsar-shuruaat", "मौका दरवाज़ा नहीं खटखटाता, बस तारीख़ निकल जाती है", "23 नवंबर 2026", "अवसर: नौकरी, छात्रवृत्ति, प्रतियोगिता और फ़ेलोशिप, हमेशा आधिकारिक लिंक के साथ। ठगी से बचने के 7 नियम और आज ही करने लायक 5 तैयारियाँ।"),
    ("vaibhav-suryavanshi", "वैभव सूर्यवंशी: ताजपुर से TIME की सूची तक, 15 साल का 'बॉस बेबी'", "22 नवंबर 2026",
     "प्रतिभा परिचय: समस्तीपुर के 15 साल के क्रिकेटर की कहानी: 12 की उम्र में रणजी, IPL 2026 में 776 रन, भारत के सबसे युवा पुरुष अंतरराष्ट्रीय खिलाड़ी, और अब TIME100 Next India में नाम।"),
    ("anokhi-2026-11-22-voyager", "वॉयजर-1: एक 'प्रकाश-दिन' दूर, 49 साल पुरानी मशीन जो आज भी घर पर चिट्ठी भेजती है", "22 नवंबर 2026",
     "अनोखी दुनिया: 1977 में छोड़ा गया वॉयजर-1 अब इतना दूर है कि रोशनी को भी एक दिन लगता है। इसकी शुरुआत, खोजें, सोने का रिकॉर्ड (हिंदी अभिवादन के साथ), 70 KB का कंप्यूटर, विवाद, और सवाल: क्या यह कल बदलेगा?"),
    ("ankurx-kahani", "उम्र नहीं, जिज्ञासा चाहिए: AnkurX कैसे बना", "16 नवंबर 2026",
     "मैंने करके देखा: 1980 के दशक से कंप्यूटर का शौक, और अब AI की मदद से एक हफ़्ते में खड़ा हुआ उत्तर बिहार का समाचार मंच।"),
    ("machhar-bomb", "मच्छरों का 'एटम बम': जब घर के कमरे को 'गैस चैंबर' बनाकर मच्छरों का सफाया होता था!", "15 नवंबर 2026",
     "यादों की अलमारी से: 1960 के दशक का 'एरोसोल बग बॉम्ब', लोहे का छोटा सिलेंडर जिसकी नोक तोड़ते ही मच्छरों पर 'सर्जिकल स्ट्राइक' होती थी। वीडियो के साथ।"),
    ("dr-s-siddharth", "डॉ. एस. सिद्धार्थ: अफ़सर, पायलट, चित्रकार, और दिल से एक विद्यार्थी", "14 नवंबर 2026",
     "प्रतिभा परिचय: IIT-IIM से पढ़े 1991 बैच के आईएएस, मुज़फ़्फ़रपुर के पूर्व डीएम, पायलट, फ़ोटोग्राफ़र और चित्रकार की कहानी।"),
    ("srilanka-diary", "श्री लंका डायरी: हाथी, मसाले, चाय और 30 मिनट में थाने की रिपोर्ट", "13 नवंबर 2026",
     "अगस्त 2023 की श्री लंका यात्रा: पिन्नावाला के हाथी, सिगिरिया, कैंडी, नुवारा एलिया की चाय, बेंटोटा का समुद्र और कोलंबो।"),
    ("chhath-puja", "हमारी छठ पूजा: इसका इतिहास, वर्तमान स्वरूप और आध्यात्मिक महत्त्व", "13 नवंबर 2026",
     "न मूर्ति, न मंदिर, न पंडित: सूरज, नदी और व्रती के संयम का महापर्व। इसका इतिहास, आज की तस्वीर और बाकी पूजाओं से इसका फ़र्क।"),
]

PRATIBHA = {"dr-s-siddharth", "vaibhav-suryavanshi"}  # slugs shown on /pratibha/
ANOKHI = {"anokhi-2026-11-22-voyager"}  # weekly "Anokhi Duniya" articles (one per week, slugs like anokhi-2026-11-22-<topic>), shown on /anokhi/

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
.lekh .vidbox{position:relative;width:100%;aspect-ratio:16/9;border-radius:10px;overflow:hidden;background:#16213A}
.lekh .vidbox iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.lekh .vidwait{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
.lekh .tbl{overflow-x:auto;margin:12px 0 16px}
.lekh table{border-collapse:collapse;width:100%;font-size:1rem}
.lekh th,.lekh td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;line-height:1.6}
.lekh th{background:var(--ground);color:var(--leaf)}
/* ---- Anokhi Duniya weekly stories ---- */
.lekh .story{border-top:2px dashed var(--line);margin-top:1.6em;padding-top:.4em}
.lekh .story .tag{display:inline-block;font-size:.85rem;font-weight:700;color:#fff;background:var(--vermilion);border-radius:999px;padding:2px 12px;margin-top:.8em}
.lekh .story .sach{font-size:.95rem;color:var(--ink2);border-left:4px solid var(--leaf);padding-left:.7em}
.lekh .kal{background:var(--ground);border:1px solid var(--line);border-left:6px solid var(--turmeric);border-radius:10px;padding:10px 14px;margin:12px 0}
.lekh .kal b{color:var(--vermilion)}
.lekh .embed{display:flex;justify-content:center;margin:12px 0}
/* ---- infographic: distance bars + timeline ---- */
.infog{--bar:#1E7F47;--bar-hi:#2F6BFF;background:var(--ground);border:1px solid var(--line);border-radius:12px;padding:16px 14px;margin:18px 0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .infog{--bar:#3AA866;--bar-hi:#5A85E8}}
:root[data-theme="dark"] .infog{--bar:#3AA866;--bar-hi:#5A85E8}
.infog h3{font-family:var(--display);font-size:1.2rem;margin:0 0 .2em;color:var(--ink)}
.infog .isub{font-size:.9rem;color:var(--ink2);margin:0 0 12px;line-height:1.6}
.drow{display:grid;grid-template-columns:8.5rem 1fr 6.2rem;gap:8px;align-items:center;padding:5px 2px;border-radius:6px}
.drow:hover{background:var(--paper)}
.drow .dn{font-size:.95rem;line-height:1.3;color:var(--ink)}
.drow .dn small{display:block;color:var(--ink2);font-size:.78rem}
.drow .dt{height:14px;background:transparent;border-radius:4px}
.drow .db{height:14px;min-width:3px;background:var(--bar);border-radius:0 4px 4px 0}
.drow .dv{font-size:.88rem;color:var(--ink2);text-align:right;line-height:1.3}
.drow.hi .dn{font-weight:700}.drow.hi .db{background:var(--bar-hi)}.drow.hi .dv{color:var(--ink);font-weight:700}
.infog .inote{font-size:.85rem;color:var(--ink2);margin:10px 0 0;line-height:1.6}
@media (max-width:560px){.drow{grid-template-columns:1fr 7.6rem;row-gap:2px}.drow .dn{grid-column:1/-1}.drow .dt{grid-column:1}
  .drow .dv{font-size:.8rem;white-space:nowrap}}
/* ---- scale diagram: Sun, planets, Voyager ---- */
.sdiag{display:block;width:100%;height:auto;font-family:var(--body)}
.sd-tall{display:none;max-width:420px;margin:0 auto}
@media (max-width:640px){.sd-wide{display:none}.sd-tall{display:block}}
.sd-axis{stroke:var(--line);stroke-width:3}
.sd-axis2{stroke:var(--ink2);stroke-width:1.5}
.sd-lead{stroke:var(--ink2);stroke-width:1}
.sd-helio{fill:none;stroke:var(--ink2);stroke-width:2;stroke-dasharray:6 6}
.sd-sun{fill:var(--turmeric)}
.sd-pl{fill:var(--ink2)}
.sd-earth{fill:var(--bar)}
.sd-voy rect{fill:var(--bar-hi)}
.sd-arrow{stroke:var(--bar-hi);stroke-width:2.5}
.sd-head{fill:var(--bar-hi)}
.sd-box{fill:var(--paper);stroke:var(--line)}
.sd-pill{fill:var(--paper);stroke:var(--bar-hi);stroke-width:1.5}
.sd-lab{fill:var(--ink);font-size:20px}
.sd-sm{font-size:16px}.sd-xs{font-size:14px}.sd-xxs{font-size:12px}
.sd-mut{fill:var(--ink2)}.sd-strong{font-weight:700}
.tl{width:100%;border-collapse:collapse;font-size:.98rem}
.tl th,.tl td{border-bottom:1px solid var(--line);padding:8px 8px;text-align:left;vertical-align:top;line-height:1.6}
.tl th{color:var(--ink2);font-size:.85rem;font-weight:700}
.tl td:first-child{white-space:nowrap;font-weight:700;color:var(--leaf)}
.tl tr.hi td{background:var(--paper)}.tl tr.hi td:first-child{color:var(--vermilion)}
@media (max-width:560px){.tl{font-size:.92rem}.tl td:first-child{white-space:normal;width:32%}}
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


def contact_link():
    """The editor's contact link, copied from the first mailto: link on the home page (index.html)."""
    src = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    m = re.search(r'<a href="mailto:([^"]+)"[^>]*>', src)
    return f'<a href="mailto:{m.group(1)}">{m.group(1)}</a>' if m else '<a href="/#about">हमें बताएँ</a>'


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
    # प्रतिभा परिचय section page: lists profile articles (slugs in PRATIBHA)
    pcards = "\n".join(
        f'<a class="lcard" href="/lekh/{s}/"><h3>{html.escape(t)}</h3><small>{html.escape(dt)}</small><p>{html.escape(sm)}</p></a>'
        for s, t, dt, sm in ARTICLES if s in PRATIBHA)
    body = ('<section><h2>प्रतिभा परिचय</h2><p class="sub">उत्तर बिहार और बिहार के प्रेरक व्यक्तित्व: '
            'जिन्होंने अपनी मेहनत, हुनर और सेवा से नई राह दिखाई। आप भी किसी प्रतिभा की जानकारी भेज सकते हैं: '
            f'{contact_link()}</p>'
            f'<div class="llist">{pcards}</div></section>')
    out = page(head, sprite, header, footer, "प्रतिभा परिचय", "AnkurX प्रतिभा परिचय: बिहार के प्रेरक व्यक्तित्व",
               "https://ankurx.in/pratibha/", body)
    os.makedirs(os.path.join(SITE, "pratibha"), exist_ok=True)
    open(os.path.join(SITE, "pratibha", "index.html"), "w", encoding="utf-8").write(out)
    print("built pratibha/index.html")
    # अनोखी दुनिया, इस हफ़्ते: weekly section page (slugs in ANOKHI)
    acards = "\n".join(
        f'<a class="lcard" href="/lekh/{s}/"><h3>{html.escape(t)}</h3><small>{html.escape(dt)}</small><p>{html.escape(sm)}</p></a>'
        for s, t, dt, sm in ARTICLES if s in ANOKHI)
    if not acards:
        acards = ('<div class="lcard" style="border:2px solid var(--x)"><small style="color:var(--vermilion);font-weight:700">जल्द आ रहा है</small>'
                  '<h3>पहला लेख: इस रविवार, 22 नवंबर, सुबह 10 बजे! 🚀</h3>'
                  '<p>एक ऐसी मशीन की कहानी, जो 49 साल से लगातार सफ़र पर है, जिसका कंप्यूटर आपके फ़ोन की एक फ़ोटो से भी छोटा है, '
                  'और जो अब इतनी दूर पहुँच गई है कि वहाँ से रोशनी को भी हम तक आने में पूरा एक दिन लगता है। '
                  'साथ में चार्ट, सौरमंडल का नक़्शा और पूरी यात्रा की टाइमलाइन।</p>'
                  '<p><b>अंदाज़ा लगाइए, किसकी बात हो रही है?</b> रविवार सुबह 10 बजे यहीं मिलिए।</p></div>')
    body = ('<section><h2>अनोखी दुनिया, इस हफ़्ते</h2><p class="sub"><b>क्या यह कल बदलेगा?</b> '
            'हर रविवार सुबह 10 बजे: दुनिया भर से हफ़्ते की <b>एक</b> सबसे अनोखी, मज़ेदार या हैरान करने वाली खबर, '
            'विज्ञान, अंतरिक्ष, तकनीक, प्रकृति, कला या वायरल। दस खबरों में से छाँटी गई, जाँची-परखी, और पूरी गहराई से: '
            'इसकी शुरुआत, इसका असर, इससे जुड़े विवाद, और अंत में AnkurX की नज़र से: क्या यह हमारा कल बदलेगा? '
            'कोई अनोखी खबर दिखी? हमें भेजें: '
            f'{contact_link()}</p>'
            f'<div class="llist">{acards}</div></section>')
    out = page(head, sprite, header, footer, "अनोखी दुनिया, इस हफ़्ते",
               "AnkurX: हर रविवार हफ़्ते की एक अनोखी खबर की पूरी कहानी, क्या यह कल बदलेगा?", "https://ankurx.in/anokhi/", body)
    os.makedirs(os.path.join(SITE, "anokhi"), exist_ok=True)
    open(os.path.join(SITE, "anokhi", "index.html"), "w", encoding="utf-8").write(out)
    print("built anokhi/index.html")


if __name__ == "__main__":
    main()
