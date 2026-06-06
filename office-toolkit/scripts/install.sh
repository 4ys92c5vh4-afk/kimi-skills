#!/bin/bash
# Office Toolkit - 一键安装脚本 (macOS)

set -e

echo "🚀 Office Toolkit 安装脚本"
echo "================================"

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi
echo "✅ Python3 已安装: $(python3 --version)"

# 检查 pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，正在安装..."
    python3 -m ensurepip --upgrade
fi
echo "✅ pip3 已安装: $(pip3 --version)"

# 安装 Python 包
echo ""
echo "📦 安装 Python 依赖..."
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    pandas openpyxl \
    pypdf pdfplumber reportlab pdf2image \
    python-pptx Pillow

# 尝试安装 markitdown（可能网络受限）
echo ""
echo "📦 尝试安装 markitdown..."
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org "markitdown[pptx]" || echo "⚠️ markitdown 安装失败，PPT 文本提取功能将使用 python-pptx"

# 检查 Node.js
if ! command -v npm &> /dev/null; then
    echo ""
    echo "⚠️ Node.js/npm 未安装，跳过 Node 包安装"
    echo "   如需创建 Word/PPT，请安装 Node.js: https://nodejs.org"
else
    echo ""
    echo "📦 安装 Node.js 依赖..."
    npm install -g docx pptxgenjs || echo "⚠️ Node 包安装失败"
fi

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo ""
    echo "⚠️ Homebrew 未安装，跳过系统工具安装"
    echo "   如需完整功能，请安装 Homebrew: https://brew.sh"
else
    echo ""
    echo "📦 安装系统工具..."
    
    # 检查并安装各工具
    for tool in pandoc poppler qpdf tesseract; do
        if ! command -v $tool &> /dev/null; then
            echo "   安装 $tool..."
            brew install $tool || echo "   ⚠️ $tool 安装失败"
        else
            echo "   ✅ $tool 已安装"
        fi
    done
    
    # LibreOffice
    if ! command -v soffice &> /dev/null; then
        echo "   安装 LibreOffice..."
        brew install --cask libreoffice || echo "   ⚠️ LibreOffice 安装失败"
    else
        echo "   ✅ LibreOffice 已安装"
    fi
fi

echo ""
echo "================================"
echo "✅ 安装完成！"
echo ""
echo "验证安装:"
echo "  python3 -c \"import pandas, openpyxl, pypdf, pdfplumber; print('Python OK')\""
echo ""
echo "使用示例:"
echo "  cd examples && python3 read_pdf.py your-file.pdf"
