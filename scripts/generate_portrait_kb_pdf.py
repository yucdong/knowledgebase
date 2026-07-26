"""
Generate a single combined PDF for the 人像摄影 (portrait photography) knowledge base.

Reads the organized Obsidian notes under dongyuchen/人像摄影/ in reading order and
renders headings, paragraphs, bullet/ordered lists, tables, blockquotes and inline
images (from attachments/) into one PDF. Uses reportlab per the .claude/pdf skill.
"""
import io
import os
import re

from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether, Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Font Registration ---
pdfmetrics.registerFont(TTFont("MSYH", "C:/Windows/Fonts/msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYH-Bold", "C:/Windows/Fonts/msyhbd.ttc", subfontIndex=0))

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "dongyuchen", "人像摄影")
OUTPUT_PDF = os.path.join(SRC_DIR, "人像摄影知识库.pdf")

# Reading order of the notes (chapter order in the PDF).
DOC_ORDER = [
    "拍摄核心思路.md",
    "焦段运用.md",
    "视角与构图.md",
    "动作引导.md",
    "后期调色.md",
    "拍摄地点-上生新所.md",
    "拍摄地点-118广场.md",
    "南京街拍示例.md",
]

# --- Colors ---
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
DARK = HexColor("#16213e")

# --- Styles ---
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "CNTitle", parent=styles["Title"], fontName="MSYH-Bold",
    fontSize=30, leading=40, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=20)
style_subtitle = ParagraphStyle(
    "CNSubtitle", parent=styles["Normal"], fontName="MSYH",
    fontSize=12, leading=16, textColor=HexColor("#666666"),
    alignment=TA_CENTER, spaceAfter=30)
style_h1 = ParagraphStyle(
    "CNH1", parent=styles["Heading1"], fontName="MSYH-Bold",
    fontSize=22, leading=30, textColor=PRIMARY, spaceBefore=6, spaceAfter=14)
style_h2 = ParagraphStyle(
    "CNH2", parent=styles["Heading2"], fontName="MSYH-Bold",
    fontSize=16, leading=22, textColor=DARK, spaceBefore=16, spaceAfter=8)
style_h3 = ParagraphStyle(
    "CNH3", parent=styles["Heading3"], fontName="MSYH-Bold",
    fontSize=13, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=6)
style_body = ParagraphStyle(
    "CNBody", parent=styles["Normal"], fontName="MSYH",
    fontSize=11, leading=17, textColor=HexColor("#333333"), spaceAfter=6)
style_bullet = ParagraphStyle(
    "CNBullet", parent=style_body, leftIndent=10 * mm, spaceAfter=3)
style_quote = ParagraphStyle(
    "CNQuote", parent=style_body, leftIndent=8 * mm, textColor=HexColor("#555555"),
    backColor=HexColor("#f4f4f8"), borderColor=ACCENT, borderWidth=0,
    spaceBefore=4, spaceAfter=8)
style_caption = ParagraphStyle(
    "CNCaption", parent=style_body, fontName="MSYH", fontSize=9, leading=13,
    textColor=HexColor("#888888"), alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
style_cell = ParagraphStyle(
    "CNCell", parent=style_body, fontSize=10, leading=14, spaceAfter=0)
style_cell_head = ParagraphStyle(
    "CNCellHead", parent=style_cell, fontName="MSYH-Bold", textColor=HexColor("#ffffff"))

IMG_RE = re.compile(r"!\[(?P<alt>.*?)\]\((?P<src>.*?)\)")


def inline(text):
    """Escape XML and convert Markdown bold / wikilinks / inline code."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[\[(.+?)\]\]", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def make_image_flowable(src, max_width, max_height):
    """Return a single scaled Image flowable (or a placeholder Paragraph)."""
    filepath = os.path.join(SRC_DIR, src.replace("/", os.sep))
    if not os.path.exists(filepath):
        return Paragraph(f"[图片缺失: {src}]", style_caption)
    try:
        pil = PILImage.open(filepath)
        if pil.mode in ("RGBA", "P", "LA"):
            pil = pil.convert("RGB")
        px_w, px_h = pil.size
        ratio = min(max_width / px_w, max_height / px_h, 1.0)
        disp_w, disp_h = px_w * ratio, px_h * ratio
        target_px_w = int(disp_w / mm * 150 / 25.4)
        if target_px_w and target_px_w < px_w:
            scale = target_px_w / px_w
            pil = pil.resize((target_px_w, max(1, int(px_h * scale))), PILImage.LANCZOS)
        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=82, optimize=True)
        buf.seek(0)
        img = Image(buf, width=disp_w, height=disp_h)
        img.hAlign = "CENTER"
        return img
    except Exception as e:  # noqa: BLE001
        return Paragraph(f"[图片加载失败: {src} - {e}]", style_caption)


def make_image_grid(srcs, cols=4):
    """Lay out a run of images in a grid of `cols` per row to save space."""
    cell_w = 40 * mm
    img_w, img_h = 37 * mm, 46 * mm
    cells = [make_image_flowable(s, img_w, img_h) for s in srcs]
    rows = []
    for r in range(0, len(cells), cols):
        row = cells[r:r + cols]
        while len(row) < cols:
            row.append("")
        rows.append(row)
    t = Table(rows, colWidths=[cell_w] * cols, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return [t, Spacer(1, 4 * mm)]


def make_table(rows):
    """rows: list of list[str] (raw cell text). First row is the header."""
    data = []
    for i, r in enumerate(rows):
        style = style_cell_head if i == 0 else style_cell
        data.append([Paragraph(inline(c), style) for c in r])
    ncols = max(len(r) for r in rows)
    avail = 160 * mm
    col_w = [avail / ncols] * ncols
    t = Table(data, colWidths=col_w, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f4f4f8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def parse_table_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def build_cover(story):
    story.append(Spacer(1, 65 * mm))
    story.append(Paragraph("人像摄影知识库", style_title))
    story.append(Paragraph("Portrait &amp; Street Portrait Photography", style_subtitle))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        "拍摄思路 · 焦段运用 · 视角与构图 · 动作引导 · 后期调色<br/>"
        "上生新所 · 118 广场 · 南京颐和路 · 喵喵街",
        ParagraphStyle("CoverDesc", parent=style_body, fontName="MSYH",
                       fontSize=12, leading=22, textColor=HexColor("#666666"),
                       alignment=TA_CENTER)))
    story.append(PageBreak())


def render_doc(story, md_path):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.strip()

        if not line:
            i += 1
            continue

        # Skip the "相关页面" section entirely (Obsidian navigation, not for PDF).
        if line.startswith("## ") and "相关页面" in line:
            break

        # Table block
        if line.startswith("|") and i + 1 < n and set(lines[i + 1].strip()) <= set("|-: "):
            rows = [parse_table_row(line)]
            i += 2  # skip header + separator
            while i < n and lines[i].strip().startswith("|"):
                rows.append(parse_table_row(lines[i].strip()))
                i += 1
            story.append(make_table(rows))
            continue

        # Image run -> collect consecutive images and render as a 4-per-row grid.
        m = IMG_RE.search(line)
        if m and line.startswith("!["):
            srcs = []
            while i < n:
                l = lines[i].strip()
                if not l:
                    i += 1
                    continue
                mi = IMG_RE.search(l)
                if mi and l.startswith("!["):
                    srcs.append(mi.group("src"))
                    i += 1
                else:
                    break
            story.extend(make_image_grid(srcs))
            continue

        # Headings
        if line.startswith("### "):
            story.append(Paragraph(inline(line[4:].strip()), style_h3))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:].strip()), style_h2))
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:].strip()), style_h1))
        elif line.startswith(">"):
            story.append(Paragraph(inline(line.lstrip("> ").strip()), style_quote))
        elif re.match(r"^(-|\*)\s+", line):
            story.append(Paragraph("• " + inline(re.sub(r"^(-|\*)\s+", "", line)), style_bullet))
        elif re.match(r"^\d+\.\s+", line):
            story.append(Paragraph(inline(line), style_bullet))
        else:
            story.append(Paragraph(inline(line), style_body))
        i += 1


def add_page_number(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("MSYH", 8)
    canvas_obj.setFillColor(HexColor("#999999"))
    canvas_obj.drawCentredString(A4[0] / 2, 15 * mm, f"— {canvas_obj.getPageNumber()} —")
    canvas_obj.restoreState()


def main():
    doc = SimpleDocTemplate(
        OUTPUT_PDF, pagesize=A4,
        leftMargin=25 * mm, rightMargin=25 * mm,
        topMargin=20 * mm, bottomMargin=25 * mm,
        title="人像摄影知识库", author="dongyuchen")
    story = []
    build_cover(story)
    for idx, name in enumerate(DOC_ORDER):
        render_doc(story, os.path.join(SRC_DIR, name))
        if idx != len(DOC_ORDER) - 1:
            story.append(PageBreak())
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
