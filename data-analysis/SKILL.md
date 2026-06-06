---
name: data-analysis
description: 数据分析全流程指南。覆盖 pandas 数据处理、matplotlib/seaborn 可视化、统计分析、数据清洗、报表生成。适用于孵化器运营数据、企业入驻统计、财务报表分析等场景。当用户需要"数据分析"、"画图表"、"统计报表"、"数据可视化"、"pandas处理"时触发。
---

# 数据分析指南

## 何时使用

- 孵化器运营数据统计分析
- 入驻企业信息汇总与可视化
- 财务报表、收支分析
- 问卷调查数据清洗与分析
- 任何需要"从数据中提取洞察"的场景

## 核心工作流

### 1. 数据加载与初探
```python
import pandas as pd
import numpy as np

# 读取数据
df = pd.read_excel("入驻企业数据.xlsx")

# 快速概览
print(df.shape)           # (行数, 列数)
print(df.columns)         # 列名
print(df.dtypes)          # 数据类型
print(df.describe())      # 统计摘要
print(df.head(10))        # 前10行
print(df.isnull().sum())  # 缺失值统计
```

### 2. 数据清洗
```python
# 处理缺失值
df["注册资本"] = df["注册资本"].fillna(0)
df["行业领域"] = df["行业领域"].fillna("未分类")

# 去重
df = df.drop_duplicates(subset=["统一社会信用代码"], keep="last")

# 类型转换
df["入驻日期"] = pd.to_datetime(df["入驻日期"])
df["注册资本"] = pd.to_numeric(df["注册资本"], errors="coerce")

# 异常值处理
df = df[df["注册资本"] >= 0]  # 过滤负数
```

### 3. 分组统计
```python
# 按行业统计企业数量
industry_stats = df.groupby("行业领域").agg({
    "企业名称": "count",
    "注册资本": ["sum", "mean"],
    "入驻日期": "max"
}).round(2)

# 按年月统计新增入驻
df["入驻年月"] = df["入驻日期"].dt.to_period("M")
monthly = df.groupby("入驻年月").size()
```

## 可视化模板

### 柱状图 / 条形图
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
df["行业领域"].value_counts().plot(kind="barh", ax=ax, color="steelblue")
ax.set_title("入驻企业行业分布", fontsize=14)
ax.set_xlabel("企业数量")
plt.tight_layout()
plt.savefig("行业分布.png", dpi=150)
```

### 折线图（时间趋势）
```python
monthly_counts = df.groupby(df["入驻日期"].dt.to_period("M")).size()
monthly_counts.index = monthly_counts.index.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 5))
monthly_counts.plot(ax=ax, marker="o", linewidth=2)
ax.set_title("月度入驻趋势", fontsize=14)
ax.set_ylabel("新增企业数")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("入驻趋势.png", dpi=150)
```

### 饼图
```python
fig, ax = plt.subplots(figsize=(8, 8))
df["孵化阶段"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_title("企业孵化阶段分布")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("孵化阶段.png", dpi=150)
```

## 完整示例：孵化器运营月报
```python
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def generate_monthly_report(data_file, output_dir="./报表"):
    df = pd.read_excel(data_file)
    df["入驻日期"] = pd.to_datetime(df["入驻日期"])
    
    report = {
        "统计月份": datetime.now().strftime("%Y年%m月"),
        "在孵企业总数": len(df),
        "本月新增": len(df[df["入驻日期"].dt.month == datetime.now().month]),
        "总注册资本(万元)": df["注册资本"].sum(),
        "平均注册资本(万元)": df["注册资本"].mean(),
        "行业分布": df["行业领域"].value_counts().to_dict()
    }
    
    # 生成可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    df["行业领域"].value_counts().plot(kind="bar", ax=axes[0,0], title="行业分布")
    df.groupby(df["入驻日期"].dt.year).size().plot(kind="bar", ax=axes[0,1], title="年度入驻")
    df["孵化阶段"].value_counts().plot(kind="pie", ax=axes[1,0], title="阶段分布")
    df["注册资本"].plot(kind="hist", bins=20, ax=axes[1,1], title="注册资本分布")
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/运营月报图表.png", dpi=150)
    
    return report

report = generate_monthly_report("入驻企业.xlsx")
print(report)
```

## 最佳实践

1. **数据备份**：分析前复制原始数据 `df_raw = df.copy()`
2. **版本记录**：用代码而非 Excel 操作，确保可复现
3. **图表规范**：始终添加标题、坐标轴标签、图例
4. **输出格式**：`plt.savefig()` 保存 PNG，同时导出 `df.to_excel()` 数据表
5. **中文显示**：设置字体 `plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']`
