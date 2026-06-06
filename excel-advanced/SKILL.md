---
name: excel-advanced
description: 高级 Excel 操作指南。覆盖复杂公式、数据透视表、VLOOKUP/XLOOKUP、条件格式、宏与 VBA、批量操作。当用户需要"Excel公式"、"数据透视表"、"VLOOKUP"、"条件格式"、"Excel宏"、"批量处理Excel"时触发。
---

# 高级 Excel 操作指南

## 何时使用

- 复杂公式计算与多表关联
- 数据透视表汇总分析
- 条件格式高亮关键数据
- 批量数据处理（宏 / VBA / Python）
- 动态报表与仪表板

## 核心公式

### 查找匹配
```excel
=VLOOKUP(查找值, 区域, 列号, FALSE)     -- 基础查找（左→右）
=XLOOKUP(查找值, 查找列, 返回列)         -- 万能查找（推荐）
=INDEX(返回区域, MATCH(查找值, 查找列, 0)) -- 灵活组合
=IFERROR(XLOOKUP(...), "未找到")          -- 错误处理
```

### 条件统计
```excel
=SUMIF(条件区域, 条件, 求和区域)          -- 单条件求和
=SUMIFS(求和区域, 条件1区域, 条件1, ...)  -- 多条件求和
=COUNTIFS(区域1, 条件1, ...)              -- 多条件计数
=AVERAGEIF(区域, 条件, 平均区域)          -- 条件平均
```

### 文本处理
```excel
=TEXTJOIN(",", TRUE, 区域)               -- 合并文本（用逗号分隔）
=LEFT/RIGHT/MID(文本, 起始, 长度)        -- 截取文本
=TEXT(数值, "yyyy-mm-dd")                -- 格式化日期
=TRIM(CLEAN(文本))                       -- 清除多余空格和换行
```

### 数组公式
```excel
=FILTER(数据区域, 条件区域="条件")       -- 动态筛选（Office 365）
=UNIQUE(区域)                            -- 去重（Office 365）
=SORT(FILTER(数据, 条件), 2, -1)        -- 筛选后排序
=LET(a, 区域, b, a*2, SUM(b))           -- 定义变量（简化复杂公式）
```

## 数据透视表操作

### 创建步骤
1. 选中数据区域 → 插入 → 数据透视表
2. 行：拖拽分类字段（如"行业领域"）
3. 列：拖拽时间字段（如"入驻年月"）
4. 值：拖拽数值字段，选择聚合方式（求和/计数/平均）

### 透视表公式
```excel
=GETPIVOTDATA("求和项:注册资本", $A$3, "行业", "生物医药")
```

## VBA 常用脚本

### 批量合并多个工作簿
```vba
Sub MergeWorkbooks()
    Dim folderPath As String
    Dim fileName As String
    Dim wb As Workbook
    
    folderPath = "C:\数据\"
    fileName = Dir(folderPath & "*.xlsx")
    
    Do While fileName <> ""
        Set wb = Workbooks.Open(folderPath & fileName)
        wb.Sheets(1).UsedRange.Copy
        ThisWorkbook.Sheets("汇总").Cells(Rows.Count, 1).End(xlUp).Offset(1, 0).PasteSpecial
        wb.Close False
        fileName = Dir()
    Loop
End Sub
```

### 批量重命名工作表
```vba
Sub RenameSheets()
    Dim ws As Worksheet
    For Each ws In Worksheets
        ws.Name = "2024_" & ws.Name
    Next
End Sub
```

## Python + openpyxl 高级操作
```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

wb = load_workbook("报表模板.xlsx")
ws = wb.active

# 写入 DataFrame
for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
    for c_idx, value in enumerate(row, 1):
        ws.cell(row=r_idx, column=c_idx, value=value)

# 条件格式：高亮大于100的值
from openpyxl.formatting.rule import CellIsRule
red_fill = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")
ws.conditional_formatting.add("C2:C100", CellIsRule(operator="greaterThan", formula=["100"], fill=red_fill))

# 设置列宽
ws.column_dimensions["A"].width = 20
ws.column_dimensions["B"].width = 15

# 冻结首行
ws.freeze_panes = "A2"

wb.save("输出报表.xlsx")
```

## 最佳实践

1. **数据规范**：每列单一数据类型，第一行必须是标题，无合并单元格
2. **表格化**：使用 Ctrl+T 将区域转为"表格"，公式自动扩展
3. **命名区域**：给常用区域命名（公式 → 定义名称），公式更易读
4. **错误处理**：公式外套 IFERROR 防止 #N/A 扩散
5. **版本管理**：重要文件开启"自动保存"，或用 Git 管理 xlsx
