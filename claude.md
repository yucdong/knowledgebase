# Claude 文档整理流程

从 `raw/` 目录中的原始素材整理为 Obsidian 知识库文档和 PDF 的标准流程。

## 整体流程

```
raw/ 原始素材 → 分析内容结构 → 拆分为 Obsidian 文档 → 生成 PDF
```

## 步骤详解

### 1. 分析原始内容

读取 `dongyuchen/raw/` 下的源文件（Markdown、HTML、图片等），识别：

- 主题与章节结构
- 图片资源
- 可复用的表格、清单、关键词

### 2. 规划 Obsidian 目录结构

按照已有知识库的惯例，创建主题文件夹：

```
dongyuchen/
  主题名/
    _Index.md          # 目录页，包含 [[wikilink]] 链接
    子主题1.md
    子主题2.md
    ...
    attachments/       # 图片附件
```

**命名规则：**
- 文件夹名 = 主题名（中文）
- `_Index.md` 作为入口文件
- 图片统一放入 `attachments/`
- 使用 `[[wikilink]]` 语法做页面间链接

### 3. 拆分与整理 Markdown

将原始大文件拆分为多个独立的 Obsidian 笔记，每个文件聚焦一个子主题：

| 原则 | 说明 |
|------|------|
| 单一关注 | 每个文件一个主题，方便独立引用 |
| 内部链接 | 使用 `[[页面名]]` 互相关联 |
| 表格化 | 对比性内容优先使用 Markdown 表格 |
| 图片引用 | 使用相对路径 `attachments/xxx.png` |
| 相关页面 | 每个文件末尾添加 `## 相关页面` 区域 |

### 4. 复制图片资源

将 `raw/` 中的图片复制到目标文件夹的 `attachments/` 目录：

```powershell
Copy-Item -Path "dongyuchen/raw/主题/图片源/*" -Destination "dongyuchen/主题/attachments/" -Recurse
```

### 5. 生成 PDF（使用 .claude/pdf skill）

使用 `.claude/pdf/SKILL.md` 中描述的 `reportlab` 库生成 PDF：

```bash
pip install reportlab Pillow
python scripts/generate_xxx_pdf.py
```

**PDF 生成脚本关键点：**

- **中文字体**：注册 `msyh.ttc`（微软雅黑）用于正文，`msyhbd.ttc` 用于标题加粗
- **页面布局**：A4 纸，左右 25mm 边距
- **内容构建**：使用 `reportlab.platypus` 的 `SimpleDocTemplate` + `story` 列表
- **表格样式**：交替行色、带表头背景色
- **图片处理**：按比例缩放，居中显示，带标题说明
- **页码**：底部居中显示

```python
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont("MSYH", "C:/Windows/Fonts/msyh.ttc", subfontIndex=0))
```

### 6. 验证

- 在 Obsidian 中打开文件夹，确认 `[[wikilink]]` 跳转正常
- 打开生成的 PDF 确认排版、字体、图片显示正确

## 文件清单示例

以街头摄影为例：

```
dongyuchen/街头摄影/
├── _Index.md              # 目录入口
├── 街拍核心思路.md
├── 晴天街拍.md
├── 夜晚街拍.md
├── 现场拍摄流程.md
├── 拍摄地点.md
├── 常见问题与避坑.md
├── 夜拍示例图集.md
├── 街头摄影知识库.pdf     # 生成的 PDF
└── attachments/           # 图片资源
    ├── image.png
    ├── image-1.png
    └── ...
```

## 依赖

- Python 3.x + `reportlab` + `Pillow`
- Windows 系统字体：微软雅黑（`msyh.ttc`）
- Obsidian（可选，用于浏览和编辑 Markdown）
