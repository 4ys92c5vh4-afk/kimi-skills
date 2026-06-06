---
name: office-toolkit
description: "Use this skill whenever the user wants to read, create, or convert Office files (Word, Excel, PowerPoint, PDF) in batch or programmatically. Triggers include: reading multiple Office files, batch converting between formats (e.g., Word to PDF, Excel to CSV, PDF to images), extracting text/tables from Office documents programmatically, or when the user mentions 'office files', 'batch process', 'convert documents', 'read docx/xlsx/pptx/pdf', or needs to handle multiple document formats in one task. Also activate when the user needs to create simple Office files quickly without advanced formatting, or when converting between Office formats. For advanced Word editing with tracked changes, use the docx skill. For advanced PowerPoint design with templates, use the pptx skill. For advanced Excel data analysis, use the xlsx skill."
license: MIT
---

# Office Toolkit

一站式 Office 文件处理工具箱，支持 **读取、创建、转换** Word、Excel、PDF、PowerPoint 文件。

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | Use example scripts or direct Python libraries |
| Create new document | Use python-docx / openpyxl / reportlab / python-pptx |
| Convert formats | Use `convert_files.py` or pandoc / LibreOffice |

---

## Reading Files

### Read Word (.docx)

```bash
cd examples
python3 read_docx.py your-file.docx
```

**Python:**
```python
from docx import Document

doc = Document("file.docx")
for para in doc.paragraphs:
    print(para.text)
```

**Command line (pandoc):**
```bash
pandoc --track-changes=all your-file.docx -t plain -o output.txt
```

### Read Excel (.xlsx)

```bash
python3 read_xlsx.py your-file.xlsx
```

**Python:**
```python
import pandas as pd

# Single sheet
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")
print(df.head())

# All sheets
all_sheets = pd.read_excel("file.xlsx", sheet_name=None)
for name, df in all_sheets.items():
    print(f"Sheet: {name}, Rows: {len(df)}")
```

### Read PDF

```bash
python3 read_pdf.py your-file.pdf
```

**Python (basic text):**
```python
from pypdf import PdfReader

reader = PdfReader("file.pdf")
for page in reader.pages:
    print(page.extract_text())
```

**Python (tables):**
```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### Read PowerPoint (.pptx)

```bash
python3 read_pptx.py your-file.pptx
```

**Python:**
```python
from pptx import Presentation

prs = Presentation("file.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            print(shape.text)
```

---

## Creating Files

### Create Word (.docx)

```bash
python3 create_docx.py output.docx
```

**Python:**
```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
doc.add_heading('标题', 0)
doc.add_paragraph('正文内容')
doc.add_paragraph('列表项', style='List Bullet')

# Table
table = doc.add_table(rows=3, cols=3)
table.style = 'Light Grid Accent 1'

doc.save('output.docx')
```

### Create Excel (.xlsx)

```bash
python3 create_xlsx.py output.xlsx
```

**Python:**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "数据"

ws['A1'] = '标题'
ws['A1'].font = Font(bold=True)
ws['B2'] = '=SUM(A1:A10)'

wb.save('output.xlsx')
```

### Create PDF

```bash
python3 create_pdf.py output.pdf
```

**Python:**
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("output.pdf", pagesize=A4)
c.drawString(100, 800, "Hello World")
c.save()
```

---

## Converting Files

Use `convert_files.py` for common conversions:

```bash
cd examples

# Word → PDF
python3 convert_files.py docx2pdf input.docx

# Excel → CSV
python3 convert_files.py xlsx2csv input.xlsx ./output/

# PDF → Text
python3 convert_files.py pdf2txt input.pdf

# PDF → Images (PNG per page)
python3 convert_files.py pdf2img input.pdf ./images/

# PowerPoint → PDF
python3 convert_files.py pptx2pdf input.pptx
```

**Other conversions:**

```bash
# DOCX → PDF (via LibreOffice)
soffice --headless --convert-to pdf document.docx

# PPTX → PDF (via LibreOffice)
soffice --headless --convert-to pdf presentation.pptx

# PDF pages to images
pdftoppm -png input.pdf output/page
```

---

## Project Structure

```
office-toolkit/
├── README.md
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
├── scripts/
│   └── install.sh            # One-click install (macOS)
├── examples/
│   ├── read_docx.py          # Read Word
│   ├── read_xlsx.py          # Read Excel
│   ├── read_pdf.py           # Read PDF
│   ├── read_pptx.py          # Read PPT
│   ├── create_docx.py        # Create Word
│   ├── create_xlsx.py        # Create Excel
│   ├── create_pdf.py         # Create PDF
│   └── convert_files.py      # Format conversion
└── docs/
    └── usage.md              # Detailed documentation
```

---

## Dependencies

### Python Packages

```bash
pip3 install pandas openpyxl pypdf pdfplumber reportlab python-pptx markitdown Pillow pdf2image
```

| Package | Purpose |
|---------|---------|
| `pandas` | Excel data analysis |
| `openpyxl` | Excel read/write (formulas, formatting) |
| `pypdf` | PDF basic operations |
| `pdfplumber` | PDF text/table extraction |
| `reportlab` | Create PDF |
| `python-pptx` | PPT read/write |
| `markitdown` | PPT text extraction |
| `Pillow` | Image processing |
| `pdf2image` | PDF to images |

### System Tools

| Tool | Purpose | Install |
|------|---------|---------|
| `pandoc` | Document format conversion | `brew install pandoc` |
| `poppler` | PDF text extraction | `brew install poppler` |
| `qpdf` | PDF command-line operations | `brew install qpdf` |
| `LibreOffice` | Office → PDF conversion | `brew install --cask libreoffice` |
| `tesseract` | OCR text recognition | `brew install tesseract` |

### Node.js Packages

```bash
npm install -g docx pptxgenjs
```

| Package | Purpose |
|---------|---------|
| `docx` | Create Word documents |
| `pptxgenjs` | Create PPT presentations |

---

## Troubleshooting

### SSL Certificate Error

```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

### LibreOffice Conversion Fails

```bash
brew install --cask libreoffice
```

### pdf2image: poppler Not Found

```bash
brew install poppler
```

### Chinese PDF Garbled Text

Use `pdfplumber` instead of `pypdf`:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
