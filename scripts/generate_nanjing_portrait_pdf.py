"""
Generate a formatted PDF from 南京街拍.md (Nanjing portrait street shooting notes).
Parses the Markdown in order, rendering headings, text notes and inline images.
Uses reportlab as specified by the .claude/pdf skill.
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
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Font Registration ---
pdfmetrics.registerFont(TTFont("MSYH", "C:/Windows/Fonts/msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYH-Bold", "C:/Windows/Fonts/msyhbd.ttc", subfontIndex=0))

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "dongyuchen", "raw", "人像摄影")
SRC_MD = os.path.join(SRC_DIR, "南京街拍.md")
OUTPUT_PDF = os.path.join(SRC_DIR, "南京街拍.pdf")

# --- Colors ---
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")

# --- Styles ---
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "CNTitle", parent=styles["Title"],
    fontName="MSYH-Bold", fontSize=28, leading=36,
    textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=20
)
style_subtitle = ParagraphStyle(
    "CNSubtitle", parent=styles["Normal"],
    fontName="MSYH", fontSize=12, leading=16,
    textColor=HexColor("#666666"), alignment=TA_CENTER, spaceAfter=30
)
style_h1 = ParagraphStyle(
    "CNH1", parent=styles["Heading1"],
    fontName="MSYH-Bold", fontSize=20, leading=26,
    textColor=PRIMARY, spaceBefore=24, spaceAfter=12
)
style_h2 = ParagraphStyle(
    "CNH2", parent=styles["Heading2"],
    fontName="MSYH-Bold", fontSize=16, leading=22,
    textColor=HexColor("#16213e"), spaceBefore=18, spaceAfter=8
)
style_h3 = ParagraphStyle(
    "CNH3", parent=styles["Heading3"],
    fontName="MSYH-Bold", fontSize=13, leading=18,
    textColor=ACCENT, spaceBefore=12, spaceAfter=6
)
style_body = ParagraphStyle(
    "CNBody", parent=styles["Normal"],
    fontName="MSYH", fontSize=11, leading=17,
    textColor=HexColor("#333333"), spaceAfter=6
)
style_caption = ParagraphStyle(
    "CNCaption", parent=style_body,
    fontName="MSYH", fontSize=9, leading=13,
    textColor=HexColor("#888888"), alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=12
)

IMG_RE = re.compile(r"!\[(?P<alt>.*?)\]\((?P<src>.*?)\)")


def make_image(filename, caption, max_width=140 * mm, max_height=100 * mm):
    """Return a KeepTogether flowable for an image with an optional caption.

    Images are downscaled to ~150 DPI at their displayed size and re-encoded as
    JPEG to keep the output PDF a reasonable size.
    """
    filepath = os.path.join(SRC_DIR, filename)
    parts = []
    if not os.path.exists(filepath):
        parts.append(Paragraph(f"[图片缺失: {filename}]", style_caption))
        return KeepTogether(parts)
    try:
        pil = PILImage.open(filepath)
        if pil.mode in ("RGBA", "P", "LA"):
            pil = pil.convert("RGB")
        px_w, px_h = pil.size
        # Displayed size preserving aspect ratio within the max box.
        ratio = min(max_width / px_w, max_height / px_h, 1.0)
        disp_w = px_w * ratio
        disp_h = px_h * ratio
        # Downscale pixels to ~150 DPI of the displayed size.
        target_px_w = int(disp_w / mm * 150 / 25.4)
        if target_px_w and target_px_w < px_w:
            scale = target_px_w / px_w
            pil = pil.resize((target_px_w, max(1, int(px_h * scale))),
                             PILImage.LANCZOS)
        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=82, optimize=True)
        buf.seek(0)
        img = Image(buf, width=disp_w, height=disp_h)
        img.hAlign = "CENTER"
        parts.append(img)
        if caption:
            parts.append(Paragraph(caption, style_caption))
        else:
            parts.append(Spacer(1, 6 * mm))
    except Exception as e:  # noqa: BLE001
        parts.append(Paragraph(f"[图片加载失败: {filename} - {e}]", style_caption))
    return KeepTogether(parts)


def build_cover(story):
    story.append(Spacer(1, 70 * mm))
    story.append(Paragraph("南京街拍", style_title))
    story.append(Paragraph("Nanjing Portrait Street Photography", style_subtitle))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(
        "颐和路阴雨天街拍 · 喵喵街<br/>拍摄逻辑、姿势参考与机位示例",
        ParagraphStyle("CoverDesc", parent=style_body,
                       fontName="MSYH", fontSize=12, leading=20,
                       textColor=HexColor("#666666"), alignment=TA_CENTER)
    ))
    story.append(PageBreak())


def build_body(story):
    """Parse the Markdown line by line and render it in order."""
    with open(SRC_MD, encoding="utf-8") as f:
        lines = f.read().splitlines()

    pending_caption = None  # text note preceding an image acts as its caption

    def flush_caption():
        nonlocal pending_caption
        if pending_caption:
            story.append(Paragraph(pending_caption, style_body))
            pending_caption = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        img_match = IMG_RE.search(line)
        if img_match:
            src = img_match.group("src")
            # Use any immediately-preceding text note as the caption.
            caption = pending_caption
            pending_caption = None
            story.append(make_image(src, caption))
            continue

        if line.startswith("# "):
            flush_caption()
            story.append(Paragraph(line[2:].strip(), style_h1))
        elif line.startswith("## "):
            flush_caption()
            story.append(Paragraph(line[3:].strip(), style_h2))
        elif line.startswith("### "):
            flush_caption()
            story.append(Paragraph(line[4:].strip(), style_h3))
        else:
            # A plain text line: keep it as a candidate caption for a following
            # image, but also render it if the previous line was already text.
            flush_caption()
            pending_caption = line

    flush_caption()


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
        title="南京街拍", author="dongyuchen",
    )
    story = []
    build_cover(story)
    build_body(story)
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
