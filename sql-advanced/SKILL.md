---
name: sql-advanced
description: 高级 SQL 查询与分析指南。覆盖复杂 JOIN、窗口函数、CTE、透视表、性能优化、递归查询等。适用于 PostgreSQL、MySQL、DuckDB、SQLite。当用户需要"复杂SQL查询"、"数据分析报表"、"窗口函数"、"CTE"、"SQL性能优化"时触发。
---

# 高级 SQL 查询指南

## 何时使用

- 复杂多表关联分析与报表生成
- 时间序列分析（同比、环比、累计）
- 数据去重、分组聚合、排名
- 递归查询（层级结构、树形数据）
- SQL 性能优化与执行计划分析

## 核心技巧

### CTE（公用表表达式）
```sql
WITH monthly_stats AS (
    SELECT 
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS total,
        SUM(amount) AS revenue
    FROM orders
    WHERE created_at >= '2024-01-01'
    GROUP BY 1
),
growth AS (
    SELECT 
        month,
        total,
        revenue,
        LAG(total) OVER (ORDER BY month) AS prev_total,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly_stats
)
SELECT 
    month,
    total,
    revenue,
    ROUND((total - prev_total)::NUMERIC / NULLIF(prev_total, 0) * 100, 2) AS growth_pct
FROM growth
ORDER BY month;
```

### 窗口函数
```sql
-- 排名
SELECT 
    department,
    employee,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS overall_rank
FROM employees;

-- 累计求和 / 移动平均
SELECT 
    date,
    sales,
    SUM(sales) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS cumulative,
    AVG(sales) OVER (ORDER BY date ROWS 6 PRECEDING) AS ma7
FROM daily_sales;

-- 首尾值
SELECT 
    product,
    price,
    FIRST_VALUE(price) OVER (PARTITION BY product ORDER BY date) AS first_price,
    LAST_VALUE(price) OVER (PARTITION BY product ORDER BY date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS latest_price
FROM prices;
```

### 透视表（行转列）
```sql
-- PostgreSQL
SELECT *
FROM CROSSTAB(
    'SELECT department, quarter, SUM(amount) 
     FROM sales GROUP BY 1,2 ORDER BY 1,2'
) AS ct(department TEXT, Q1 NUMERIC, Q2 NUMERIC, Q3 NUMERIC, Q4 NUMERIC);

-- DuckDB / 标准 SQL
SELECT 
    department,
    SUM(CASE WHEN quarter = 'Q1' THEN amount END) AS Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN amount END) AS Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN amount END) AS Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN amount END) AS Q4
FROM sales
GROUP BY department;
```

### 递归 CTE（树形结构）
```sql
WITH RECURSIVE org_tree AS (
    -- 锚点：顶层节点
    SELECT id, name, parent_id, 0 AS level
    FROM organizations
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- 递归：子节点
    SELECT o.id, o.name, o.parent_id, ot.level + 1
    FROM organizations o
    JOIN org_tree ot ON o.parent_id = ot.id
)
SELECT REPEAT('  ', level) || name AS org_hierarchy
FROM org_tree
ORDER BY level, id;
```

## 性能优化

```sql
-- 查看执行计划
EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE created_at > '2024-01-01' AND status = 'completed';

-- 索引建议
CREATE INDEX CONCURRENTLY idx_orders_created_status 
ON orders(created_at, status) 
INCLUDE (amount, customer_id);

-- 分区表示例（PostgreSQL）
CREATE TABLE measurements (
    logdate DATE,
    peaktemp INT
) PARTITION BY RANGE (logdate);

CREATE TABLE measurements_y2024m01 
PARTITION OF measurements
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## 最佳实践

1. **先过滤后聚合**：WHERE 子句尽早过滤数据
2. **避免 SELECT ***：只取需要的列
3. **索引策略**：高基数列建 B-tree，JSON 查询用 GIN，地理数据用 GiST
4. **批量插入**：使用 `INSERT ... VALUES (), (), ()` 而非逐条插入
5. **分析表统计**：定期执行 `ANALYZE table_name`
