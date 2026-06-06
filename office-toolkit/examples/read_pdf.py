#!/usr/bin/env python3
"""
读取 PDF 文件
支持：文本提取、表格提取、元数据读取
"""

import sys
from pathlib import Path


def read_pdf_with_pypdf(filepath):
    """使用 pypdf 提取文本"""
    from pypdf import PdfReader

    reader = PdfReader(filepath)
    print(f"📄 页数: {len(reader.pages)}")

    # 元数据
    if reader.metadata:
        print("\n📋 元数据:")
        meta = reader.metadata
        for key in ["/Title", "/Author", "/Subject", "/Creator", "/Producer"]:
            if key in meta:
                print(f"   {key}: {meta[key]}")

    # 提取文本
    full_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n--- 第 {i+1} 页 ---\n{text}"

    return full_text


def extract_tables_with_pdfplumber(filepath):
    """使用 pdfplumber 提取表格"""
    import pdfplumber

    print("\n📊 表格提取 (pdfplumber):")
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                print(f"\n   第 {i+1} 页 - 发现 {len(tables)} 个表格:")
                for j, table in enumerate(tables):
                    print(f"   表格 {j+1} ({len(table)} 行 x {len(table[0]) if table else 0} 列):")
                    for row in table[:5]:  # 只显示前 5 行
                        print(f"      {row}")
                    if len(table) > 5:
                        print(f"      ... (还有 {len(table)-5} 行)")


def extract_images_with_pdf2image(filepath):
    """将 PDF 页面转为图片"""
    try:
        from pdf2image import convert_from_path

        print("\n🖼️  转换页面为图片...")
        images = convert_from_path(filepath, first_page=1, last_page=1)
        output_dir = Path(filepath).parent / "pdf_images"
        output_dir.mkdir(exist_ok=True)

        for i, image in enumerate(images[:3]):  # 最多转 3 页
            img_path = output_dir / f"page_{i+1}.png"
            image.save(img_path)
            print(f"   已保存: {img_path}")
    except Exception as e:
        print(f"   ⚠️ 图片转换失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 read_pdf.py <文件路径>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)

    print(f"📑 读取 PDF 文件: {filepath}")
    print("=" * 60)

    text = read_pdf_with_pypdf(filepath)
    if text:
        print("\n📝 内容预览 (前 1500 字符):")
        print(text[:1500])
        if len(text) > 1500:
            print(f"\n... (共 {len(text)} 字符)")

    extract_tables_with_pdfplumber(filepath)
    extract_images_with_pdf2image(filepath)
