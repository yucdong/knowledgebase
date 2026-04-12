"""
Generate a formatted PDF from the 街头摄影 (Street Photography) knowledge base.
Uses reportlab as specified by the .claude/pdf skill.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# --- Font Registration ---
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD_PATH = "C:/Windows/Fonts/msyhbd.ttc"

pdfmetrics.registerFont(TTFont("MSYH", FONT_PATH, subfontIndex=0))
pdfmetrics.registerFont(TTFont("MSYH-Bold", FONT_BOLD_PATH, subfontIndex=0))

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(BASE_DIR, "dongyuchen", "街头摄影")
ATTACH_DIR = os.path.join(PHOTO_DIR, "attachments")
OUTPUT_PDF = os.path.join(PHOTO_DIR, "街头摄影知识库.pdf")

# --- Colors ---
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
LIGHT_BG = HexColor("#f5f5f5")
TABLE_HEADER_BG = HexColor("#16213e")
TABLE_HEADER_FG = HexColor("#ffffff")
TABLE_ROW_ALT = HexColor("#eef1f6")

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
    textColor=HexColor("#333333"), spaceBefore=12, spaceAfter=6
)
style_body = ParagraphStyle(
    "CNBody", parent=styles["Normal"],
    fontName="MSYH", fontSize=10.5, leading=16,
    textColor=HexColor("#333333"), spaceAfter=6
)
style_bullet = ParagraphStyle(
    "CNBullet", parent=style_body,
    leftIndent=18, bulletIndent=6, spaceAfter=4,
    bulletFontName="MSYH", bulletFontSize=10.5
)
style_quote = ParagraphStyle(
    "CNQuote", parent=style_body,
    fontName="MSYH", fontSize=11, leading=17,
    leftIndent=20, textColor=HexColor("#555555"),
    borderColor=ACCENT, borderWidth=2, borderPadding=8,
    spaceBefore=8, spaceAfter=8
)
style_keyword = ParagraphStyle(
    "CNKeyword", parent=style_body,
    fontName="MSYH-Bold", fontSize=10, leading=14,
    textColor=ACCENT, spaceAfter=10
)
style_table_header = ParagraphStyle(
    "TableHeader", parent=style_body,
    fontName="MSYH-Bold", fontSize=9.5, leading=13,
    textColor=TABLE_HEADER_FG, alignment=TA_CENTER
)
style_table_cell = ParagraphStyle(
    "TableCell", parent=style_body,
    fontName="MSYH", fontSize=9.5, leading=13,
    textColor=HexColor("#333333")
)
style_caption = ParagraphStyle(
    "CNCaption", parent=style_body,
    fontName="MSYH", fontSize=9, leading=13,
    textColor=HexColor("#888888"), alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=12
)


def make_table(headers, rows, col_widths=None):
    """Create a styled table with headers and rows."""
    page_width = A4[0] - 50 * mm
    if col_widths is None:
        n = len(headers)
        col_widths = [page_width / n] * n

    data = [[Paragraph(h, style_table_header) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), style_table_cell) for c in row])

    table = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), TABLE_HEADER_FG),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ROW_ALT))

    table.setStyle(TableStyle(style_cmds))
    return table


def add_image(story, filename, caption, max_width=120*mm, max_height=80*mm):
    """Add an image with caption if the file exists."""
    filepath = os.path.join(ATTACH_DIR, filename)
    if not os.path.exists(filepath):
        story.append(Paragraph(f"[图片缺失: {filename}]", style_caption))
        return
    try:
        img = Image(filepath)
        ratio = min(max_width / img.drawWidth, max_height / img.drawHeight, 1.0)
        img.drawWidth *= ratio
        img.drawHeight *= ratio
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph(caption, style_caption))
    except Exception as e:
        story.append(Paragraph(f"[图片加载失败: {filename} - {e}]", style_caption))


def build_cover(story):
    """Build title page."""
    story.append(Spacer(1, 60 * mm))
    story.append(Paragraph("街头摄影知识库", style_title))
    story.append(Paragraph("Street Photography Knowledge Base", style_subtitle))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(
        "基于街拍笔记和视频学习整理<br/>"
        "聚焦拍摄地点、晴天与夜晚的街拍思路<br/>"
        "以及现场快速复用的观察方法",
        ParagraphStyle("CoverDesc", parent=style_body,
                       fontName="MSYH", fontSize=12, leading=20,
                       textColor=HexColor("#666666"), alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph(
        "参考来源：郭城安街拍笔记",
        ParagraphStyle("CoverRef", parent=style_body,
                       fontName="MSYH", fontSize=10,
                       textColor=HexColor("#999999"), alignment=TA_CENTER)
    ))
    story.append(PageBreak())


def build_toc(story):
    """Build table of contents."""
    story.append(Paragraph("目录", style_h1))
    story.append(Spacer(1, 5 * mm))
    toc_items = [
        ("一、街拍核心思路", "基本理念、观察优先级与关键原则"),
        ("二、晴天街拍", "曝光、景深与 8 种常见拍法"),
        ("三、夜晚街拍", "找光要领与 8 种夜拍技巧"),
        ("四、现场拍摄流程", "到达现场后的三步操作"),
        ("五、拍摄地点", "推荐街拍地点清单"),
        ("六、常见问题与避坑", "常见错误与自检清单"),
        ("七、夜拍示例图集", "11 张夜拍示例及分析"),
    ]
    for title, desc in toc_items:
        story.append(Paragraph(
            f"<b>{title}</b> — {desc}", style_body
        ))
        story.append(Spacer(1, 2 * mm))
    story.append(PageBreak())


def build_core_concept(story):
    """Section 1: 街拍核心思路."""
    story.append(Paragraph("一、街拍核心思路", style_h1))

    story.append(Paragraph("基本理念", style_h2))
    for item in [
        "街拍强调<b>环境中的人</b>，而不是强肖像感的照片",
        "与其追着人拍，不如先找到合适的光位和构图，再等人物走进画面",
        "重点不是人物本身，而是人物与环境的关系",
    ]:
        story.append(Paragraph(item, style_bullet, bulletText="•"))

    story.append(Paragraph("观察优先级", style_h2))
    for num, item in [
        ("1.", "<b>先观察光</b> — 判断主光源方向和质量"),
        ("2.", "<b>再看构图</b> — 寻找线条、边框、镜面、前景和背景关系"),
        ("3.", "<b>最后等人</b> — 等待人物走入预设的画面中"),
    ]:
        story.append(Paragraph(item, style_bullet, bulletText=num))

    story.append(Paragraph("关键原则", style_h2))
    principles = [
        ("<b>逆光优先</b>：逆光有利于拉开人物和背景的层次，也更容易形成剪影"),
        ("<b>黑包白</b>：让深色区域包裹亮部主体，形成视觉聚焦"),
        ("<b>等待大于追拍</b>：先选好位置，再等人物进入"),
        ("<b>环境工具</b>：前景、边框、镜面、立柱、楼梯、玻璃反射都可以成为画面的组织工具"),
    ]
    for p in principles:
        story.append(Paragraph(p, style_bullet, bulletText="•"))

    story.append(PageBreak())


def build_sunny(story):
    """Section 2: 晴天街拍."""
    story.append(Paragraph("二、晴天街拍", style_h1))

    story.append(Paragraph("曝光与景深", style_h2))
    story.append(Paragraph("晴天不必把光圈开得太大。推荐使用类似 <b>F5.6</b> 的设置，让画面保留一定环境信息，同时让主体与背景产生适度分离。", style_body))

    story.append(Paragraph("常见拍法", style_h2))
    pw = A4[0] - 50 * mm
    table = make_table(
        ["#", "拍法", "要点"],
        [
            ["1", "逆光 + 框架构图", "拍出剪影和明确的明暗对比"],
            ["2", "顺光 + 前景", "利用被照亮的建筑色彩，加入芦苇、花等前景"],
            ["3", "线条构图", "把柱子、栏杆等线条当作构图元素，等待人物进入"],
            ["4", "纵深感", "寻找有透视感的街道、走廊、通道，让人物处在透视线中"],
            ["5", "黑包白", "让深色区域包裹亮部主体，形成视觉聚焦（黄金分割构图）"],
            ["6", "镜面反射", "利用镜子或反射面制造画面层次与陌生感"],
            ["7", "低角度向上拍", "在地下车库等位置拍摄，适合中心构图和高反差画面"],
            ["8", "自然前景", "用树叶等自然元素做前景，让阳光和人物剪影一起进入画面"],
        ],
        col_widths=[pw * 0.06, pw * 0.22, pw * 0.72]
    )
    story.append(table)

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "关键词：<b>剪影 | 框架构图 | 黑包白 | 线条 | 前景遮挡 | 纵深感 | 镜面反射</b>",
        style_keyword
    ))
    story.append(PageBreak())


def build_night(story):
    """Section 3: 夜晚街拍."""
    story.append(Paragraph("三、夜晚街拍", style_h1))

    story.append(Paragraph("核心观察点", style_h2))
    for item in [
        "夜晚同样可以沿用<b>黑包白</b>的思路，把亮部当作视觉中心",
        "主动找光源：店铺、窗户、楼道、广告牌、路灯、车灯",
        "优先拍<b>逆光和侧逆光</b>，让人物从背景里跳出来",
        "雨夜、玻璃、水面、车窗都能增强光线层次",
    ]:
        story.append(Paragraph(item, style_bullet, bulletText="•"))

    story.append(Paragraph("常见拍法", style_h2))
    pw = A4[0] - 50 * mm
    table = make_table(
        ["#", "拍法", "要点"],
        [
            ["1", "室内透光", "从室内向外透出的光源适合做画面中心"],
            ["2", "高饱和色彩", "很暗的环境中，红色、暖色招牌和服装更显眼"],
            ["3", "雨夜叙事", "雨夜车窗后的人影和倒影是很好的叙事元素"],
            ["4", "找光等人", "先找到灯光，再等待人走进光区"],
            ["5", "暖光温馨", "暖光适合拍温馨场景（家庭、亲子互动）"],
            ["6", "冷暖对比", "冷暖双侧光适合等待两个方向的人同时进入"],
            ["7", "建筑分界", "楼梯、墙边、建筑边缘都可以做分界线或剪影背景"],
            ["8", "反射与低角度", "玻璃反射、灯光反射和低角度广角建筑画面适合夜景氛围"],
        ],
        col_widths=[pw * 0.06, pw * 0.22, pw * 0.72]
    )
    story.append(table)

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "关键词：<b>主动找光 | 逆光 | 冷暖对比 | 玻璃反射 | 低角度 | 分界线 | 剪影层次</b>",
        style_keyword
    ))
    story.append(PageBreak())


def build_workflow(story):
    """Section 4: 现场拍摄流程."""
    story.append(Paragraph("四、现场拍摄流程", style_h1))
    story.append(Paragraph("到达拍摄地点后的三步操作流程。", style_body))

    story.append(Paragraph("1. 先看环境", style_h2))
    for item in [
        "判断<b>主光源位置</b>（太阳方向 / 灯光来源）",
        "判断背景是否干净",
        "观察是否有<b>线条、框架、前景</b>可利用",
    ]:
        story.append(Paragraph(item, style_bullet, bulletText="•"))

    story.append(Paragraph("2. 再定机位", style_h2))
    pw = A4[0] - 50 * mm
    table = make_table(
        ["角度", "适用场景"],
        [
            ["低角度", "夸张空间关系"],
            ["正面等待", "中心构图"],
            ["侧面等待", "利用墙面、楼梯、玻璃和柱子"],
        ],
        col_widths=[pw * 0.3, pw * 0.7]
    )
    story.append(table)

    story.append(Paragraph("3. 最后等人物", style_h2))
    for item in [
        "等人物进入<b>亮部</b>",
        "等人物走到<b>透视中心</b>或边界位置",
        "等动作、姿态、人与人的关系形成<b>画面张力</b>",
    ]:
        story.append(Paragraph(item, style_bullet, bulletText="•"))

    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("简要口诀", style_h2))
    story.append(Paragraph("光 → 位 → 人<br/>先看光，再选位，最后等人。", style_quote))
    story.append(PageBreak())


def build_locations(story):
    """Section 5: 拍摄地点."""
    story.append(Paragraph("五、拍摄地点", style_h1))
    story.append(Paragraph("推荐的街拍拍摄地点清单。", style_body))

    story.append(Paragraph("上海", style_h2))
    for item in ["徐汇滨江公园", "龙美术馆"]:
        story.append(Paragraph(item, style_bullet, bulletText="•"))

    story.append(Paragraph("南京", style_h2))
    story.append(Paragraph("待补充", style_body))

    story.append(Paragraph("苏州", style_h2))
    story.append(Paragraph("待补充", style_body))
    story.append(PageBreak())


def build_faq(story):
    """Section 6: 常见问题与避坑."""
    story.append(Paragraph("六、常见问题与避坑", style_h1))
    story.append(Paragraph("街拍中容易犯的错误，拍摄前和回看时都可以对照检查。", style_body))

    story.append(Paragraph("常见问题", style_h2))
    pw = A4[0] - 50 * mm
    table = make_table(
        ["问题", "说明"],
        [
            ["只拍到人，没有环境", "没有拍到人与环境的关系，画面缺乏街拍语境"],
            ["缺乏层次分离", "光线虽强，但人物和背景没有形成层次"],
            ["元素过多", "前景、反射、线条堆叠过多，导致主体不明确"],
            ["过度靠近", "画面变成单纯肖像，失去街拍感"],
        ],
        col_widths=[pw * 0.3, pw * 0.7]
    )
    story.append(table)

    story.append(Paragraph("自检清单", style_h2))
    checklist = [
        "画面中是否有明确的<b>环境关系</b>？",
        "人物与背景是否有<b>层次分离</b>？",
        "前景和构图元素是否<b>服务于主体</b>？",
        "拍摄距离是否保持了<b>街拍而非肖像</b>的感觉？",
    ]
    for item in checklist:
        story.append(Paragraph(item, style_bullet, bulletText="☐"))
    story.append(PageBreak())


def build_gallery(story):
    """Section 7: 夜拍示例图集."""
    story.append(Paragraph("七、夜拍示例图集", style_h1))
    story.append(Paragraph("以下示例图来自郭城安街拍笔记中的夜拍素材。", style_body))
    story.append(Spacer(1, 5 * mm))

    examples = [
        ("image.png", "示例 1：亮部作为视觉中心"),
        ("image-1.png", "示例 2：暗环境中的高饱和色彩"),
        ("image-2.png", "示例 3：雨夜、车窗与人物关系"),
        ("image-3.png", "示例 4：主动找光，等待人物进入"),
        ("image-4.png", "示例 5：暖光适合温馨场景"),
        ("image-5.png", "示例 6：环境中的人，避免强肖像感"),
        ("image-6.png", "示例 7：楼梯和建筑光源形成剪影"),
        ("image-7.png", "示例 8：前景遮挡增加层次"),
        ("image-8.png", "示例 9：低角度拍建筑与空间"),
        ("image-9.png", "示例 10：玻璃与灯光反射作为前景"),
        ("image-10.png", "示例 11：墙边与边界线组织画面"),
    ]
    for filename, caption in examples:
        add_image(story, filename, caption, max_width=140 * mm, max_height=90 * mm)
        story.append(Spacer(1, 3 * mm))


def add_page_number(canvas_obj, doc):
    """Add page number footer."""
    canvas_obj.saveState()
    canvas_obj.setFont("MSYH", 8)
    canvas_obj.setFillColor(HexColor("#999999"))
    page_num = canvas_obj.getPageNumber()
    text = f"— {page_num} —"
    canvas_obj.drawCentredString(A4[0] / 2, 15 * mm, text)
    canvas_obj.restoreState()


def main():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=25 * mm,
        title="街头摄影知识库",
        author="dongyuchen",
    )

    story = []
    build_cover(story)
    build_toc(story)
    build_core_concept(story)
    build_sunny(story)
    build_night(story)
    build_workflow(story)
    build_locations(story)
    build_faq(story)
    build_gallery(story)

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
