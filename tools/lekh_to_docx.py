"""Make an editable Word file from lekh/<slug>/article_body.html.
Usage: python3 tools/lekh_to_docx.py chhath-puja  -> ~/Desktop/AnkurX/lekh_drafts/<slug>.docx"""
import os, sys
from html.parser import HTMLParser
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "Kohinoor Devanagari"


class P(HTMLParser):
    """Collects blocks: (kind, runs) where runs = [(text, bold)]; compare rows; links."""
    def __init__(self):
        super().__init__(); self.blocks = []; self.cur = None; self.bold = 0; self.list = None
        self.cls = []; self.row = None; self.cell = None; self.href = None

    def start(self, kind):
        self.cur = (kind, []); self.blocks.append(self.cur)

    def handle_starttag(self, tag, a):
        a = dict(a); c = a.get("class", ""); self.cls.append(c)
        if tag == "h1": self.start("title")
        elif tag == "h2": self.start("h2")
        elif tag == "p": self.start({"lede": "lede", "byline": "byline", "wish": "wish"}.get(c, "p"))
        elif tag == "div" and c == "kicker": self.start("kicker")
        elif tag in ("ul", "ol"): self.list = "bullet" if tag == "ul" else "number"
        elif tag == "li": self.start(self.list)
        elif tag == "b": self.bold += 1
        elif tag == "a": self.href = a.get("href")
        elif tag == "img": self.start("photo"); self.cur[1].append(("[फ़ोटो: " + a.get("src", "") + "]  ", False))
        elif tag == "figcaption":
            if self.blocks and self.blocks[-1][0] == "photo": self.cur = self.blocks[-1]
        elif tag == "div" and c == "compare": self.blocks.append(("table", []))
        elif tag == "div" and c == "crow": self.row = []; self.blocks[-1][1].append(self.row) if self.blocks[-1][0] == "table" else None
        elif tag == "div" and self.row is not None: self.cell = []; self.row.append(self.cell)

    def handle_endtag(self, tag):
        c = self.cls.pop() if self.cls else ""
        if tag == "b": self.bold -= 1
        elif tag in ("p", "h1", "h2", "li", "figcaption"): self.cur = None
        elif tag == "a" and self.href and self.cur:
            self.cur[1].append(("  " + self.href, False)); self.href = None
        elif tag == "div":
            if c == "crow": self.row = None
            elif c == "compare": pass
            elif self.cell is not None: self.cell = None
            if c == "kicker": self.cur = None

    def handle_data(self, d):
        if not d.strip() and not (self.cur and self.cur[1]): return
        if d.strip():  # collapse inner whitespace, keep one space at an edge that had one
            d = (" " if d[0].isspace() else "") + " ".join(d.split()) + (" " if d[-1].isspace() else "")
        else:
            d = " "
        if self.cell is not None:
            self.cell.append(d)
        elif self.cur is not None:
            self.cur[1].append((d, self.bold > 0))


def fontify(run, size=None, bold=None, color=None):
    run.font.name = FONT
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:cs"), FONT)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)
    if size: run.font.size = Pt(size); run._element.get_or_add_rPr().append(
        run._element.makeelement(qn("w:szCs"), {qn("w:val"): str(int(size * 2))}))
    if bold is not None: run.bold = bold
    if color: run.font.color.rgb = RGBColor.from_string(color)


def main(slug):
    p = P(); p.feed(open(os.path.join(SITE, "lekh", slug, "article_body.html"), encoding="utf-8").read())
    d = Document()
    d.styles["Normal"].font.name = FONT; d.styles["Normal"].font.size = Pt(12)
    for kind, runs in p.blocks:
        if kind == "table":
            t = d.add_table(rows=1, cols=3); t.style = "Table Grid"
            for i, h in enumerate(("विषय", "आम पूजा", "छठ")):
                fontify(t.rows[0].cells[i].paragraphs[0].add_run(h), 12, True)
            for row in runs:
                cells = t.add_row().cells
                for i, parts in enumerate(row[:3]):
                    txt = "".join(parts).replace("आम पूजा:", "").replace("छठ:", "").strip()
                    fontify(cells[i].paragraphs[0].add_run(txt), 11, i == 0)
            continue
        style = {"bullet": "List Bullet", "number": "List Number"}.get(kind)
        para = d.add_paragraph(style=style) if style else d.add_paragraph()
        size = {"title": 20, "h2": 15, "kicker": 10, "byline": 10}.get(kind, 12)
        color = {"photo": "2F6BFF", "title": "16213A", "h2": "1E7F47", "kicker": "C2381F", "byline": "4A5468", "wish": "1E7F47"}.get(kind)
        for text, b in runs:
            fontify(para.add_run(text), size, b or kind in ("title", "h2", "lede", "wish"), color)
        if kind in ("h2",): para.paragraph_format.space_before = Pt(14)
    out_dir = os.path.expanduser("~/Desktop/AnkurX/lekh_drafts"); os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{slug}.docx"); d.save(out); print(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "chhath-puja")
