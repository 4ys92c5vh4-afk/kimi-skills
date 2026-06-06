# 详细使用文档

## 目录

- [读取文件](#读取文件)
- [创建文件](#创建文件)
- [转换格式](#转换格式)
- [常见问题](#常见问题)

---

## 读取文件

### 读取 Word (.docx)

```bash
cd examples

# 方法1: 使用示例脚本
python3 read_docx.py your-file.docx

# 方法2: 使用 pandoc (命令行)
pandoc --track-changes=all your-file.docx -t plain -o output.txt
```

**Python 代码:**
```python
from docx import Document

doc = Document("file.docx")
for para in doc.paragraphs:
    print(para.text)
```

### 读取 Excel (.xlsx)

```bash
python3 read_xlsx.py your-file.xlsx
```

**Python 代码:**
```python
import pandas as pd

# 读取单个 Sheet
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")
print(df.head())

# 读取所有 Sheet
all_sheets = pd.read_excel("file.xlsx", sheet_name=None)
for name, df in all_sheets.items():
    print(f"Sheet: {name}, Rows: {len(df)}")
```

### 读取 PDF

```bash
python3 read_pdf.py your-file.pdf
```

**Python 代码:**
```python
from pypdf import PdfReader

reader = PdfReader("file.pdf")
for page in reader.pages:
    print(page.extract_text())
```

**提取表格:**
```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### 读取 PPT (.pptx)

```bash
python3 read_pptx.py your-file.pptx
```

**Python 代码:**
```python
from pptx import Presentation

prs = Presentation("file.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            print(shape.text)
```

---

## 创建文件

### 创建 Word

```bash
python3 create_docx.py output.docx
```

**关键代码:**
```python
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
doc.add_heading('标题', 0)
doc.add_paragraph('正文内容')
doc.add_paragraph('列表项', style='List Bullet')

# 表格
table = doc.add_table(rows=3, cols=3)
table.style = 'Light Grid Accent 1'

doc.save('output.docx')
```

### 创建 Excel

```bash
python3 create_xlsx.py output.xlsx
```

**关键代码:**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "数据"

# 写入数据
ws['A1'] = '标题'
ws['A1'].font = Font(bold=True)

# 公式
ws['B2'] = '=SUM(A1:A10)'

wb.save('output.xlsx')
```

### 创建 PDF

```bash
python3 create_pdf.py output.pdf
```

**关键代码:**
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("output.pdf", pagesize=A4)
c.drawString(100, 800, "Hello World")
c.save()
```

---

## 转换格式

### 转换命令速查

```bash
cd examples

# Word → PDF
python3 convert_files.py docx2pdf input.docx

# Excel → CSV
python3 convert_files.py xlsx2csv input.xlsx ./output/

# PDF → 文本
python3 convert_files.py pdf2txt input.pdf

# PDF → 图片 (每页一张 PNG)
python3 convert_files.py pdf2img input.pdf ./images/

# PPT → PDF
python3 convert_files.py pptx2pdf input.pptx
```

---

## 常见问题

### Q: 安装时提示 SSL 证书错误

**A:** 运行以下命令修复 macOS Python 证书：
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

或使用 `--trusted-host`：
```bash
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas
```

### Q: LibreOffice 转换失败

**A:** 安装 LibreOffice：
```bash
brew install --cask libreoffice
```

### Q: pdf2image 报错 poppler 未找到

**A:** 安装 poppler：
```bash
brew install poppler
```

### Q: 读取中文 PDF 乱码

**A:** 尝试使用 pdfplumber 代替 pypdf：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
