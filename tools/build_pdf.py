# -*- coding: utf-8 -*-
"""ARAÇ SAHİPLERİ EL KİTABI — markdown bölümlerinden PDF dizgisi.

Kullanım:  python tools/build_pdf.py
Çıktı:     output/pdf/ARAC-SAHIPLERI-EL-KITABI-v0.1.pdf
"""
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, NextPageTemplate, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "01-arac-sahipleri"
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT / "ARAC-SAHIPLERI-EL-KITABI-v0.1.pdf"

# ---------------------------------------------------------------- renkler
RED = colors.HexColor("#C41220")
NAVY = colors.HexColor("#1E2C47")
MUTED = colors.HexColor("#49597A")
FAINT = colors.HexColor("#8A93A5")
MIST = colors.HexColor("#ECF1F7")
BOX_BLUE = colors.HexColor("#EEF3FA")
BOX_RED = colors.HexColor("#FBEFEF")
BOX_GRAY = colors.HexColor("#F2F3F5")
BOX_AMBER = colors.HexColor("#FBF4E4")

# ---------------------------------------------------------------- fontlar
FONTS = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("Segoe", f"{FONTS}/segoeui.ttf"))
pdfmetrics.registerFont(TTFont("Segoe-B", f"{FONTS}/segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("Segoe-I", f"{FONTS}/segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("Segoe-BI", f"{FONTS}/segoeuiz.ttf"))
pdfmetrics.registerFont(TTFont("SegoeSym", f"{FONTS}/seguisym.ttf"))
pdfmetrics.registerFontFamily(
    "Segoe", normal="Segoe", bold="Segoe-B", italic="Segoe-I", boldItalic="Segoe-BI")

# pyphen'de Türkçe heceleme sözlüğü bulunmuyor; heceleme kapalı.
HYPH = None


def style(name, **kw):
    base = dict(fontName="Segoe", fontSize=10.5, leading=15.5,
                textColor=colors.HexColor("#1B2333"), alignment=TA_JUSTIFY,
                spaceAfter=6)
    if HYPH:
        base["hyphenationLang"] = HYPH
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "body": style("body"),
    "chap_no": style("chap_no", fontName="Segoe-B", fontSize=11, leading=14,
                     textColor=RED, alignment=TA_LEFT, spaceAfter=2),
    "chap_title": style("chap_title", fontName="Segoe-B", fontSize=21,
                        leading=26, textColor=NAVY, alignment=TA_LEFT,
                        spaceAfter=4),
    "motto": style("motto", fontName="Segoe-I", fontSize=11, leading=15,
                   textColor=MUTED, alignment=TA_LEFT, spaceAfter=14),
    "h2": style("h2", fontName="Segoe-B", fontSize=14, leading=18,
                textColor=NAVY, alignment=TA_LEFT, spaceBefore=14,
                spaceAfter=6),
    "h3": style("h3", fontName="Segoe-B", fontSize=11.5, leading=15,
                textColor=RED, alignment=TA_LEFT, spaceBefore=10,
                spaceAfter=4),
    "bullet": style("bullet", leftIndent=16, bulletIndent=4, spaceAfter=4),
    "check": style("check", leftIndent=20, firstLineIndent=-14, spaceAfter=4),
    "boxlabel": style("boxlabel", fontName="Segoe-B", fontSize=9.5,
                      leading=12, alignment=TA_LEFT, spaceAfter=3),
    "boxbody": style("boxbody", fontSize=10, leading=14.5, spaceAfter=3),
    "toc_h": style("toc_h", fontName="Segoe-B", fontSize=21, leading=26,
                   textColor=NAVY, alignment=TA_LEFT, spaceAfter=14),
}

BOX_KINDS = {
    "NEDEN": ("NEDEN?", BOX_BLUE, NAVY),
    "UZMAN": ("KUŞCU SİGORTA UZMAN GÖRÜŞÜ", BOX_RED, RED),
    "MEVZUAT": ("MEVZUAT KUTUSU", BOX_GRAY, MUTED),
    "GERCEK": ("GERÇEK HAYATTAN", MIST, MUTED),
    "DIKKAT": ("DİKKAT", BOX_AMBER, colors.HexColor("#8A6D1A")),
    "BILGI": ("BİLMENİZ GEREKEN", BOX_BLUE, NAVY),
}

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF☀-⛿✀-➿⬀-⯿"
    "️‍⁉‼ℹ↩↪⌚⌛Ⓜ]")


def sym(ch):
    return f'<font name="SegoeSym">{ch}</font>'


def inline(text):
    t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # işaret karakterleri (emoji temizliğinden ÖNCE placeholder'a al)
    t = t.replace("✅", "\x01").replace("✔", "\x01")
    t = t.replace("❌", "\x02").replace("✘", "\x02")
    t = t.replace("☐", "\x03").replace("⬜", "\x03")
    t = EMOJI_RE.sub("", t)
    t = t.replace("\x01", sym("✔")).replace("\x02", sym("✘"))
    t = t.replace("\x03", sym("☐"))
    # markdown bağlantıları -> yalnızca metin
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", t)
    t = t.replace("`", "")
    return t.strip()


def box_kind(header):
    h = header.upper()
    if "NEDEN" in h:
        return "NEDEN"
    if "UZMAN" in h:
        return "UZMAN"
    if "MEVZUAT" in h:
        return "MEVZUAT"
    if "GERÇEK" in h or "GERCEK" in h:
        return "GERCEK"
    if "DİKKAT" in h or "DIKKAT" in h:
        return "DIKKAT"
    return "BILGI"


def make_box(lines):
    """'>' ile başlayan blok satırlarından renkli kutu üretir."""
    header, body = None, []
    for ln in lines:
        ln = ln.lstrip(">").strip()
        if not ln:
            body.append("")
            continue
        if ln.startswith("###"):
            header = ln.lstrip("#").strip()
        else:
            body.append(ln)
    kind = box_kind(header or "")
    label, bg, fg = BOX_KINDS[kind]
    if header:
        custom = EMOJI_RE.sub("", header).strip()
        if kind == "BILGI" and custom:
            label = custom.upper()
    flow = [Paragraph(label, ParagraphStyle(
        "bl", parent=S["boxlabel"], textColor=fg))]
    para_buf = []

    def flush():
        if para_buf:
            flow.append(Paragraph(inline(" ".join(para_buf)), S["boxbody"]))
            para_buf.clear()

    for ln in body:
        if not ln:
            flush()
        elif ln.startswith("- "):
            flush()
            flow.append(Paragraph(inline(ln[2:]), ParagraphStyle(
                "bb", parent=S["boxbody"], leftIndent=12, bulletIndent=2),
                bulletText="•"))
        else:
            para_buf.append(ln)
    flush()
    tbl = Table([[flow]], colWidths=[15.6 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.75, fg),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return [Spacer(1, 4), tbl, Spacer(1, 8)]


def chapter_flowables(md_text, front_title=None):
    """Bir bölüm dosyasını flowable listesine çevirir."""
    flows = []
    lines = md_text.splitlines()
    i, n = 0, len(lines)
    para_buf = []
    after_h1 = False

    def flush():
        nonlocal after_h1
        if para_buf:
            txt = inline(" ".join(para_buf))
            if txt:
                flows.append(Paragraph(txt, S["body"]))
            para_buf.clear()

    while i < n:
        raw = lines[i]
        ln = raw.rstrip()
        if not ln.strip():
            flush()
            i += 1
            continue
        if ln.startswith("> "):
            flush()
            block = []
            while i < n and lines[i].startswith(">"):
                block.append(lines[i])
                i += 1
            flows.extend(make_box(block))
            continue
        if ln.startswith("# "):  # H1
            flush()
            title = EMOJI_RE.sub("", ln[2:]).strip()
            m = re.match(r"Bölüm\s+(\d+)\s*[—-]\s*(.+)", title)
            if m:
                flows.append(Paragraph(f"BÖLÜM {m.group(1)}", S["chap_no"]))
                flows.append(Paragraph(inline(m.group(2)), S["chap_title"]))
                toc_text = f"Bölüm {m.group(1)} — {m.group(2)}"
            else:
                shown = front_title or title
                flows.append(Paragraph(inline(shown), S["chap_title"]))
                toc_text = shown
            flows[-1]._toc_entry = toc_text  # afterFlowable kancası için
            after_h1 = True
            i += 1
            continue
        if ln.startswith("## "):
            flush()
            flows.append(Paragraph(
                inline(EMOJI_RE.sub("", ln[3:]).strip()), S["h2"]))
            i += 1
            continue
        if ln.startswith("### "):
            flush()
            flows.append(Paragraph(
                inline(EMOJI_RE.sub("", ln[4:]).strip()), S["h3"]))
            i += 1
            continue
        if ln.strip() in ("---", "***"):
            flush()
            flows.append(Spacer(1, 10))
            i += 1
            continue
        stripped = ln.strip()
        # motto: H1'den hemen sonraki tek italik satır
        if after_h1 and re.fullmatch(r"\*[^*]+\*", stripped):
            flush()
            flows.append(Paragraph(inline(stripped[1:-1]), S["motto"]))
            after_h1 = False
            i += 1
            continue
        if re.match(r"^[-*] ", stripped) or re.match(r"^\d+\.\s", stripped) \
                or stripped.startswith(("☐", "✔", "✅", "❌")):
            flush()
            after_h1 = False
            # madde metni kaynakta satırlara bölünmüş olabilir; devamını topla
            j = i + 1
            parts = [stripped]
            while j < n:
                nxt = lines[j].strip()
                if (not nxt or nxt.startswith(("#", ">", "---", "***"))
                        or re.match(r"^[-*] ", nxt)
                        or re.match(r"^\d+\.\s", nxt)
                        or nxt.startswith(("☐", "✔", "✅", "❌"))):
                    break
                parts.append(nxt)
                j += 1
            stripped = " ".join(parts)
            i = j - 1
            m_num = re.match(r"^(\d+)\.\s+(.*)", stripped)
            if m_num:
                flows.append(Paragraph(inline(m_num.group(2)), S["bullet"],
                                       bulletText=f"{m_num.group(1)}."))
            else:
                content = re.sub(r"^[-*] ", "", stripped)
                if content.startswith(("☐", "✔", "✅", "❌", "[ ]")) or \
                        stripped.startswith(("☐", "✔", "✅", "❌")):
                    content = content.replace("[ ]", "☐", 1)
                    flows.append(Paragraph(inline(content), S["check"]))
                else:
                    flows.append(Paragraph(inline(content), S["bullet"],
                                           bulletText="•"))
            i += 1
            continue
        para_buf.append(stripped)
        after_h1 = False
        i += 1
    flush()
    return flows


# ---------------------------------------------------------------- sayfa süsleri
def draw_header_footer(canv, doc):
    canv.saveState()
    w, h = A4
    # üstbilgi
    canv.setFont("Segoe-B", 8.5)
    canv.setFillColor(RED)
    canv.drawString(2 * cm, h - 1.35 * cm, "KUŞCU")
    kus_w = canv.stringWidth("KUŞCU ", "Segoe-B", 8.5)
    canv.setFillColor(NAVY)
    canv.drawString(2 * cm + kus_w, h - 1.35 * cm, "SİGORTA")
    canv.setFont("Segoe", 8)
    canv.setFillColor(FAINT)
    canv.drawRightString(w - 2 * cm, h - 1.35 * cm, "ARAÇ SAHİPLERİ EL KİTABI")
    canv.setStrokeColor(MIST)
    canv.setLineWidth(0.7)
    canv.line(2 * cm, h - 1.55 * cm, w - 2 * cm, h - 1.55 * cm)
    # altbilgi
    canv.line(2 * cm, 1.55 * cm, w - 2 * cm, 1.55 * cm)
    canv.setFont("Segoe", 7.5)
    canv.setFillColor(FAINT)
    canv.drawString(2 * cm, 1.15 * cm,
                    "Hazırlayan: Abdurrahman KUŞCU — Sigorta Danışmanı")
    canv.drawCentredString(w / 2, 1.15 * cm, "www.kuscusigorta.com")
    canv.setFont("Segoe-B", 8.5)
    canv.setFillColor(NAVY)
    canv.drawRightString(w - 2 * cm, 1.15 * cm, str(canv.getPageNumber()))
    canv.restoreState()


class BookDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        entry = getattr(flowable, "_toc_entry", None)
        if entry:
            self.notify("TOCEntry", (0, entry, self.page))


def build():
    doc = BookDoc(str(PDF_PATH), pagesize=A4,
                  leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2.2 * cm, bottomMargin=2.1 * cm,
                  title="Araç Sahipleri El Kitabı",
                  author="Abdurrahman KUŞCU — Kuşcu Sigorta")
    frame = Frame(2 * cm, 2.1 * cm, A4[0] - 4 * cm, A4[1] - 4.3 * cm, id="f")
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[frame]),
        PageTemplate(id="Body", frames=[frame], onPage=draw_header_footer),
    ])

    story = []
    # ---------------------------------------------------------- kapak
    story.append(Spacer(1, 3.2 * cm))
    story.append(Paragraph("KUŞCU SİGORTA BİLGİ MERKEZİ", style(
        "c1", fontName="Segoe-B", fontSize=13, leading=17, textColor=RED,
        alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("Yayın No: 001", style(
        "c2", fontSize=10, textColor=FAINT, alignment=TA_CENTER,
        spaceAfter=34)))
    story.append(Paragraph("ARAÇ SAHİPLERİ<br/>EL KİTABI", style(
        "c3", fontName="Segoe-B", fontSize=34, leading=42, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=12)))
    story.append(Paragraph(
        "Kaza &bull; Hasar &bull; Acil Durumlar &bull; Sigorta Süreçleri",
        style("c4", fontSize=13, leading=17, textColor=MUTED,
              alignment=TA_CENTER, spaceAfter=40)))
    story.append(Paragraph(
        "<i>Bilgi, doğru zamanda kullanıldığında en güçlü güvencedir.</i>",
        style("c5", fontName="Segoe-I", fontSize=11.5, textColor=MUTED,
              alignment=TA_CENTER, spaceAfter=60)))
    story.append(Paragraph("Hazırlayan", style(
        "c6", fontSize=9.5, textColor=FAINT, alignment=TA_CENTER,
        spaceAfter=2)))
    story.append(Paragraph("<b>Abdurrahman KUŞCU</b>", style(
        "c7", fontSize=13, leading=17, textColor=NAVY, alignment=TA_CENTER,
        spaceAfter=1)))
    story.append(Paragraph("Sigorta Danışmanı", style(
        "c8", fontSize=10.5, textColor=MUTED, alignment=TA_CENTER,
        spaceAfter=26)))
    story.append(Paragraph(
        "Kuşcu Sigorta Aracılık Hizmetleri Ltd. Şti.<br/>"
        "www.kuscusigorta.com", style(
            "c9", fontSize=9.5, leading=13, textColor=FAINT,
            alignment=TA_CENTER, spaceAfter=22)))
    story.append(Paragraph("1. Baskı — 2026 &nbsp;|&nbsp; Sürüm v0.1 (taslak)",
                           style("c10", fontSize=9, textColor=FAINT,
                                 alignment=TA_CENTER)))
    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())

    # ---------------------------------------------------------- künye
    kapak_md = (SRC / "00-kapak-ve-kunye.md").read_text(encoding="utf-8")
    ic = kapak_md.split("## İç Kapak", 1)[1]
    story.append(Paragraph("Künye", S["chap_title"]))
    story[-1]._toc_entry = "Künye"
    story.append(Spacer(1, 6))
    story.extend(chapter_flowables(ic))
    story.append(PageBreak())

    # ---------------------------------------------------------- içindekiler
    story.append(Paragraph("İçindekiler", S["toc_h"]))
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(
        "toc0", fontName="Segoe", fontSize=10, leading=16,
        textColor=colors.HexColor("#1B2333"), leftIndent=6)]
    toc.dotsMinLevel = 0
    story.append(toc)
    story.append(PageBreak())

    # ---------------------------------------------------------- bölümler
    front = [("01-onsoz.md", "Önsöz"),
             ("02-rehber-nasil-kullanilir.md", "Bu Rehber Nasıl Kullanılır?"),
             ("03-acil-durumlarda-ilk-60-saniye.md",
              "Acil Durumlarda İlk 60 Saniye")]
    files = [(f, t) for f, t in front]
    for p in sorted(SRC.glob("*.md")):
        if p.name[:2] in ("00", "01", "02", "03", "04"):
            continue
        files.append((p.name, None))

    for idx, (fname, ftitle) in enumerate(files):
        md = (SRC / fname).read_text(encoding="utf-8")
        story.extend(chapter_flowables(md, front_title=ftitle))
        if idx < len(files) - 1:
            story.append(PageBreak())

    doc.multiBuild(story)
    print(f"OK: {PDF_PATH}")


if __name__ == "__main__":
    build()
