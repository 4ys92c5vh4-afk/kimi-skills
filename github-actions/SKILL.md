---
name: github-actions
description: GitHub Actions 工作流编写指南。覆盖 CI/CD 流水线、自动化测试、自动部署、定时任务、Issue/PR 自动处理等场景。当用户需要"配置GitHub Actions"、"CI/CD流水线"、"自动部署"、"定时运行脚本"、"自动化工作流"时触发。
---

# GitHub Actions 工作流指南

## 何时使用

- 项目 CI/CD 自动化（测试、构建、部署）
- 定时任务（数据备份、报告生成、监控检查）
- PR/Issue 自动处理（标签、评论、合并）
- 多环境部署（开发、测试、生产）
- 代码质量检查（lint、format、security scan）

## 核心概念

```yaml
# .github/workflows/main.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * *"  # 每天凌晨2点

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
```

## 常用模式

### 模式1：多环境部署
```yaml
name: Deploy

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to ${{ vars.ENV_NAME }}
        run: |
          echo "Deploying to ${{ vars.ENV_NAME }}"
          # 部署脚本
```

### 模式2：矩阵构建（多版本测试）
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

### 模式3：缓存优化
```yaml
steps:
  - uses: actions/cache@v4
    with:
      path: |
        ~/.npm
        ~/.cache/pip
        node_modules
      key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

### 模式4：定时数据抓取任务
```yaml
name: Daily Data Scraper

on:
  schedule:
    - cron: "0 9 * * 1-5"  # 工作日早9点
  workflow_dispatch:  # 支持手动触发

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - run: pip install -r requirements.txt
      
      - name: Run scraper
        run: python scraper.py
        env:
          API_KEY: ${{ secrets.API_KEY }}
      
      - name: Commit results
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add data/
          git diff --staged --quiet || git commit -m "Update data $(date +%Y-%m-%d)"
          git push
```

## Secrets 与变量管理

```yaml
env:
  GLOBAL_VAR: "value"

jobs:
  deploy:
    steps:
      - name: Use secrets
        run: |
          echo "API Key: ${{ secrets.API_KEY }}"
          echo "Env var: ${{ vars.ENVIRONMENT_NAME }}"
```

## 最佳实践

1. **最小权限原则**：给 workflow 分配最小必要权限
   ```yaml
   permissions:
     contents: read
     issues: write
   ```
2. **固定 Action 版本**：使用 `@v4` 而非 `@main`，防止上游变更导致故障
3. **并发控制**：防止同时运行多个部署
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```
4. **超时设置**：防止任务挂起消耗资源
   ```yaml
   jobs:
     build:
       timeout-minutes: 10
   ```
