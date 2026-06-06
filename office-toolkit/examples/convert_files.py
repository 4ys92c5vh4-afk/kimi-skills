#!/usr/bin/env python3
"""
文件格式转换工具
支持: DOCX↔PDF, XLSX↔CSV, PDF→图片, PPTX→PDF
"""

import sys
import subprocess
import shutil
from pathlib import Path


def docx_to_pdf(input_path, output_path=None):
    """Word → PDF (使用 LibreOffice)"""
    input_path = Path(input_path)
    output_path = output_path or input_path.with_suffix('.pdf')

    if shutil.which("soffice"):
        cmd = [
            "soffice", "--headless", "--convert-to", "pdf",
            "--outdir", str(input_path.parent), str(input_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        # LibreOffice 输出文件名可能不同
        generated = input_path.with_suffix('.pdf')
        if generated != output_path:
            generated.rename(output_path)
        print(f"✅ DOCX → PDF: {output_path}")
    else:
        print("❌ LibreOffice (soffice) 未安装")
        print("   安装: brew install --cask libreoffice")


def xlsx_to_csv(input_path, output_dir=None):
    """Excel → CSV (每个 Sheet 一个 CSV)"""
    import pandas as pd

    input_path = Path(input_path)
    output_dir = Path(output_dir) if output_dir else input_path.parent
    output_dir.mkdir(exist_ok=True)

    sheets = pd.read_excel(input_path, sheet_name=None)
    for sheet_name, df in sheets.items():
        safe_name = "".join(c if c.isalnum() else "_" for c in sheet_name)
        output_file = output_dir / f"{input_path.stem}_{safe_name}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"✅ Sheet '{sheet_name}' → {output_file}")


def pdf_to_text(input_path, output_path=None):
    """PDF → 文本"""
    from pypdf import PdfReader

    input_path = Path(input_path)
    output_path = output_path or input_path.with_suffix('.txt')

    reader = PdfReader(input_path)
    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"\n--- 第 {i+1} 页 ---\n{page_text}"

    output_path.write_text(text, encoding='utf-8')
    print(f"✅ PDF → TXT: {output_path}")


def pdf_to_images(input_path, output_dir=None, dpi=200):
    """PDF → 图片 (每页一张 PNG)"""
    try:
        from pdf2image import convert_from_path

        input_path = Path(input_path)
        output_dir = Path(output_dir) if output_dir else input_path.parent / "pdf_images"
        output_dir.mkdir(exist_ok=True)

        images = convert_from_path(input_path, dpi=dpi)
        for i, image in enumerate(images):
            img_path = output_dir / f"page_{i+1:03d}.png"
            image.save(img_path, "PNG")
            print(f"✅ 第 {i+1} 页 → {img_path}")

        print(f"\n📁 图片保存在: {output_dir}")
    except ImportError:
        print("❌ pdf2image 未安装: pip3 install pdf2image")
    except Exception as e:
        print(f"❌ 转换失败: {e}")


def pptx_to_pdf(input_path, output_path=None):
    """PPT → PDF (使用 LibreOffice)"""
    input_path = Path(input_path)
    output_path = output_path or input_path.with_suffix('.pdf')

    if shutil.which("soffice"):
        cmd = [
            "soffice", "--headless", "--convert-to", "pdf",
            "--outdir", str(input_path.parent), str(input_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        generated = input_path.with_suffix('.pdf')
        if generated != output_path:
            generated.rename(output_path)
        print(f"✅ PPTX → PDF: {output_path}")
    else:
        print("❌ LibreOffice (soffice) 未安装")


def print_usage():
    print("""
文件格式转换工具

用法: python3 convert_files.py <操作> <输入文件> [输出路径]

操作:
    docx2pdf    Word → PDF
    xlsx2csv    Excel → CSV (每个 Sheet 一个文件)
    pdf2txt     PDF → 文本
    pdf2img     PDF → 图片 (每页一张 PNG)
    pptx2pdf    PPT → PDF

示例:
    python3 convert_files.py docx2pdf document.docx
    python3 convert_files.py xlsx2csv data.xlsx ./output/
    python3 convert_files.py pdf2img report.pdf ./images/
""")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    action = sys.argv[1]
    input_file = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    if not Path(input_file).exists():
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)

    actions = {
        'docx2pdf': docx_to_pdf,
        'xlsx2csv': xlsx_to_csv,
        'pdf2txt': pdf_to_text,
        'pdf2img': pdf_to_images,
        'pptx2pdf': pptx_to_pdf,
    }

    if action in actions:
        actions[action](input_file, output)
    else:
        print(f"❌ 未知操作: {action}")
        print_usage()
