# Office Toolkit

一站式 Office 文件处理工具箱，支持 **读取、创建、转换** Word、Excel、PDF、PowerPoint 文件。

## 功能概览

| 格式 | 读取 | 创建 | 转换 |
|------|------|------|------|
| **DOCX** (Word) | ✅ pandoc / python-docx | ✅ docx-js / python-docx | ✅ → PDF |
| **XLSX** (Excel) | ✅ pandas / openpyxl | ✅ openpyxl | ✅ → CSV/JSON |
| **PDF** | ✅ pypdf / pdfplumber | ✅ reportlab | ✅ → 图片/文本 |
| **PPTX** (PPT) | ✅ markitdown / python-pptx | ✅ pptxgenjs / python-pptx | ✅ → PDF/图片 |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/huangtianyu/office-toolkit.git
cd office-toolkit
```

### 2. 一键安装依赖

```bash
# macOS
bash scripts/install.sh

# 或手动安装
pip3 install -r requirements.txt
npm install -g docx pptxgenjs
brew install pandoc poppler qpdf libreoffice
```

### 3. 运行示例

```bash
# 读取 Word
cd examples && python3 read_docx.py ../test.docx

# 读取 Excel
python3 read_xlsx.py ../test.xlsx

# 读取 PDF
python3 read_pdf.py ../test.pdf

# 读取 PPT
python3 read_pptx.py ../test.pptx
```

## 项目结构

```
office-toolkit/
├── README.md
├── requirements.txt          # Python 依赖
├── package.json              # Node.js 依赖
├── scripts/
│   └── install.sh            # 一键安装脚本
├── examples/
│   ├── read_docx.py          # 读取 Word
│   ├── read_xlsx.py          # 读取 Excel
│   ├── read_pdf.py           # 读取 PDF
│   ├── read_pptx.py          # 读取 PPT
│   ├── create_docx.py        # 创建 Word
│   ├── create_xlsx.py        # 创建 Excel
│   ├── create_pdf.py         # 创建 PDF
│   └── convert_files.py      # 格式转换示例
└── docs/
    └── usage.md              # 详细使用文档
```

## 依赖清单

### Python 包

| 包名 | 用途 |
|------|------|
| `pandas` | Excel 数据分析 |
| `openpyxl` | Excel 读写（公式、格式） |
| `pypdf` | PDF 基础操作 |
| `pdfplumber` | PDF 文本/表格提取 |
| `reportlab` | 创建 PDF |
| `python-pptx` | PPT 读写 |
| `markitdown` | PPT 文本提取 |
| `Pillow` | 图片处理 |
| `pdf2image` | PDF 转图片 |

### 系统工具

| 工具 | 用途 |
|------|------|
| `pandoc` | 文档格式转换 |
| `poppler` (pdftotext) | PDF 文本提取 |
| `qpdf` | PDF 命令行操作 |
| `LibreOffice` | Office → PDF 转换 |
| `tesseract` | OCR 文字识别 |

### Node.js 包

| 包名 | 用途 |
|------|------|
| `docx` | 创建 Word 文档 |
| `pptxgenjs` | 创建 PPT 演示文稿 |

## License

MIT
