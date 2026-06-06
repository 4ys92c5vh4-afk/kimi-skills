#!/usr/bin/env python3
"""
创建 PDF 文件
使用 reportlab 创建带文本、表格、样式的 PDF
"""

import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors


def create_pdf(output_path):
    """创建示例 PDF"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    story = []

    # 标题
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E5090'),
        spaceAfter=30,
        alignment=1  # 居中
    )
    story.append(Paragraph("Office Toolkit", title_style))
    story.append(Paragraph("PDF 生成示例", styles['Heading2']))
    story.append(Spacer(1, 0.5*cm))

    # 正文
    story.append(Paragraph(
        "这是一个使用 <b>reportlab</b> 库生成的 PDF 示例文档。"
        "reportlab 是 Python 中最强大的 PDF 生成库之一，支持丰富的排版功能。",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.5*cm))

    # 特性列表
    story.append(Paragraph("<b>主要特性：</b>", styles['Heading3']))
    features = [
        "支持多种字体和文字样式（粗体、斜体、颜色）",
        "可插入表格并自定义样式",
        "支持分页和页眉页脚",
        "可嵌入图片和图形",
        "支持多栏布局和复杂排版",
    ]
    for feature in features:
        story.append(Paragraph(f"• {feature}", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))

    # 表格
    story.append(Paragraph("<b>示例数据表格：</b>", styles['Heading3']))
    data = [
        ["项目", "Q1", "Q2", "Q3", "Q4"],
        ["收入", "100万", "120万", "140万", "160万"],
        ["支出", "60万", "70万", "75万", "80万"],
        ["利润", "40万", "50万", "65万", "80万"],
    ]

    table = Table(data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#D5E8F0')),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

    # 第二页
    story.append(PageBreak())
    story.append(Paragraph("第二页内容", styles['Heading2']))
    story.append(Paragraph(
        "PDF 支持多页文档，可以自动处理分页。"
        "当内容超过一页时，reportlab 会自动创建新页面。",
        styles['Normal']
    ))

    doc.build(story)
    print(f"✅ PDF 已创建: {output_path}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "output.pdf"
    create_pdf(output)
