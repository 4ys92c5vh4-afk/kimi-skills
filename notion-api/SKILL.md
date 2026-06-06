---
name: notion-api
description: Notion API 集成指南。覆盖数据库操作、页面创建、内容同步、Webhook 自动化。适用于知识库管理、项目协作、文档同步。当用户需要"Notion API"、"同步到Notion"、"Notion数据库"、"知识库管理"时触发。
---

# Notion API 集成指南

## 何时使用

- 将数据同步到 Notion 数据库（企业信息、项目进度）
- 批量创建/更新 Notion 页面
- 从 Notion 导出数据进行分析
- 搭建项目看板、知识库
- 与其他工具（GitHub、Slack）联动

## 快速开始

### 1. 创建 Integration
1. 访问 https://www.notion.so/my-integrations
2. 创建 New integration，复制 Token
3. 在 Notion 页面/数据库 → Share → 添加 Integration

### 2. Python 客户端
```bash
pip install notion-client
```

```python
from notion_client import Client

notion = Client(auth="secret_xxxxxxxxxxxx")

# 查询数据库
database_id = "your-database-id"
response = notion.databases.query(database_id=database_id)
for page in response["results"]:
    print(page["properties"]["名称"]["title"][0]["text"]["content"])
```

## 核心操作

### 数据库查询与筛选
```python
# 带筛选条件的查询
response = notion.databases.query(
    database_id=database_id,
    filter={
        "property": "状态",
        "select": {"equals": "在孵"}
    },
    sorts=[{
        "property": "入驻日期",
        "direction": "descending"
    }]
)

# 分页获取全部
results = []
while response:
    results.extend(response["results"])
    if not response["has_more"]:
        break
    response = notion.databases.query(
        database_id=database_id,
        start_cursor=response["next_cursor"]
    )
```

### 创建页面（数据库条目）
```python
new_page = notion.pages.create(
    parent={"database_id": database_id},
    properties={
        "名称": {
            "title": [{"text": {"content": "新入驻企业"}}]
        },
        "行业": {
            "select": {"name": "生物医药"}
        },
        "注册资本": {
            "number": 500
        },
        "入驻日期": {
            "date": {"start": "2024-06-01"}
        },
        "状态": {
            "select": {"name": "在孵"}
        }
    }
)
```

### 更新页面
```python
notion.pages.update(
    page_id="page-id",
    properties={
        "状态": {"select": {"name": "毕业"}},
        "毕业日期": {"date": {"start": "2024-12-01"}}
    }
)
```

### 批量同步（Excel → Notion）
```python
import pandas as pd
from notion_client import Client

def sync_excel_to_notion(excel_file, database_id, notion_token):
    df = pd.read_excel(excel_file)
    notion = Client(auth=notion_token)
    
    for _, row in df.iterrows():
        # 检查是否已存在
        existing = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "名称",
                "title": {"equals": row["企业名称"]}
            }
        )
        
        properties = {
            "名称": {"title": [{"text": {"content": row["企业名称"]}}]},
            "行业": {"select": {"name": str(row["行业"])}},
            "注册资本": {"number": float(row["注册资本"])},
        }
        
        if existing["results"]:
            # 更新
            notion.pages.update(
                page_id=existing["results"][0]["id"],
                properties=properties
            )
            print(f"更新: {row['企业名称']}")
        else:
            # 创建
            notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            print(f"创建: {row['企业名称']}")
```

### 从 Notion 导出到 Excel
```python
def export_notion_to_excel(database_id, notion_token, output_file):
    notion = Client(auth=notion_token)
    
    response = notion.databases.query(database_id=database_id)
    rows = []
    
    for page in response["results"]:
        props = page["properties"]
        row = {
            "ID": page["id"],
            "名称": props.get("名称", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
            "行业": props.get("行业", {}).get("select", {}).get("name", ""),
            "状态": props.get("状态", {}).get("select", {}).get("name", ""),
            "注册资本": props.get("注册资本", {}).get("number"),
        }
        rows.append(row)
    
    pd.DataFrame(rows).to_excel(output_file, index=False)
    print(f"导出完成: {output_file}")
```

## 最佳实践

1. **Token 安全**：使用环境变量存储 `NOTION_TOKEN`，不要硬编码
2. **Rate Limit**：Notion API 限制 3 请求/秒，批量操作加 `time.sleep(0.35)`
3. **属性映射**：不同属性类型（title、rich_text、number、select、multi_select、date）结构不同
4. **错误重试**：使用 `tenacity` 库实现自动重试
5. **ID 管理**：保存 Notion page_id 到本地，避免重复创建
