---
name: python-scripting
description: Python 自动化脚本编写指南。覆盖批量处理文本/CSV/JSON/Excel文件、目录遍历、正则匹配、日志处理、定时任务等日常办公自动化场景。当用户需要"批量处理文件"、"写个Python脚本"、"自动化处理数据"、"遍历文件夹"、"批量重命名"、"合并Excel"时触发。
---

# Python 脚本编写指南

## 何时使用

- 批量处理文本、CSV、JSON、Excel 文件
- 目录遍历、文件搜索、批量重命名
- 数据清洗、格式转换、日志分析
- 简单的自动化办公任务
- 需要比 Shell 更强大的数据处理能力时

## 核心库速查

### 文件与路径
```python
from pathlib import Path
import os
import shutil

# 遍历目录
for file in Path("/path").rglob("*.txt"):
    print(file.name)

# 批量重命名
for i, file in enumerate(Path(".").glob("*.jpg")):
    file.rename(f"img_{i:03d}.jpg")

# 复制/移动
shutil.copy("src.txt", "dst.txt")
shutil.move("old.txt", "new_dir/")
```

### CSV / Excel
```python
import pandas as pd

# 读取并合并多个 Excel
files = Path("data").glob("*.xlsx")
df = pd.concat([pd.read_excel(f) for f in files])
df.to_excel("merged.xlsx", index=False)

# CSV 处理
df = pd.read_csv("data.csv", encoding="utf-8")
df = df.dropna(subset=["关键列"])
df.to_csv("cleaned.csv", index=False, encoding="utf-8-sig")
```

### JSON / 文本
```python
import json

# 读取 JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 批量替换文本内容
for file in Path("docs").rglob("*.md"):
    content = file.read_text(encoding="utf-8")
    content = content.replace("旧文本", "新文本")
    file.write_text(content, encoding="utf-8")
```

### 正则表达式
```python
import re

# 提取电话号码
text = "联系：138-1234-5678 或 13987654321"
phones = re.findall(r"1[3-9]\d{9}", text.replace("-", ""))

# 批量替换
def replace_dates(text):
    return re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\1年\2月\3日", text)
```

## 完整示例

### 示例1：批量合并Excel并去重
```python
import pandas as pd
from pathlib import Path

def merge_excel_files(input_dir, output_file, key_column=None):
    files = list(Path(input_dir).glob("*.xlsx")) + list(Path(input_dir).glob("*.xls"))
    if not files:
        print("未找到 Excel 文件")
        return
    
    dfs = []
    for f in files:
        print(f"处理: {f.name}")
        df = pd.read_excel(f)
        df["来源文件"] = f.name
        dfs.append(df)
    
    result = pd.concat(dfs, ignore_index=True)
    if key_column:
        result = result.drop_duplicates(subset=[key_column], keep="last")
    
    result.to_excel(output_file, index=False)
    print(f"合并完成: {output_file} ({len(result)} 行)")

merge_excel_files("./数据", "合并结果.xlsx", key_column="企业名称")
```

### 示例2：批量处理Word文档提取信息
```python
from docx import Document
from pathlib import Path

def extract_from_docs(input_dir, output_csv):
    rows = []
    for file in Path(input_dir).glob("*.docx"):
        doc = Document(file)
        # 提取第一段作为标题
        title = doc.paragraphs[0].text if doc.paragraphs else ""
        # 统计字数
        text = "\n".join([p.text for p in doc.paragraphs])
        rows.append({"文件名": file.name, "标题": title, "字数": len(text)})
    
    pd.DataFrame(rows).to_csv(output_csv, index=False, encoding="utf-8-sig")

extract_from_docs("./文档", "文档统计.csv")
```

## 最佳实践

1. **编码处理**：始终显式指定 `encoding="utf-8"` 或 `utf-8-sig`（带BOM，兼容Excel）
2. **路径处理**：优先使用 `pathlib.Path` 而非字符串拼接
3. **错误处理**：批量操作中使用 try/except 防止单文件错误中断整个流程
4. **日志记录**：使用 `logging` 模块替代 `print`，便于排查问题
5. **备份原文件**：批量修改前先备份，或在输出到新目录
