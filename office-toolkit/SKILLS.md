# 我的 Claude Code Skills 清单

> 本清单记录了我安装的所有 Skills，方便换机器时快速恢复环境。
> 生成时间：2026-05-29

## 官方 Skills（Anthropic）

```bash
# 文档处理
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/docx"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/pptx"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/xlsx"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/pdf"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/internal-comms"

# 开发
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/claude-api"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/mcp-builder"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/frontend-design"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/webapp-testing"

# 设计
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/algorithmic-art"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/canvas-design"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/theme-factory"
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/anthropics/skills/tree/main/skills/brand-guidelines"
```

## 第三方精选 Skills

```bash
# 工程/DevOps
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/ci-cd-pipelines" --target ci-cd-pipelines
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/git-advanced" --target git-advanced
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/database-optimization" --target database-optimization
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/postgres-optimization" --target postgres-optimization
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/redis-patterns" --target redis-patterns
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/monitoring-observability" --target monitoring-observability
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/microservices-design" --target microservices-design
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/aws-cloud-patterns" --target aws-cloud-patterns

# 安全
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/security-hardening" --target security-hardening
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/authentication-patterns" --target authentication-patterns

# 测试
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/testing-strategies" --target testing-strategies

# AI/LLM
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/prompt-engineering" --target prompt-engineering
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/mcp-development" --target mcp-development
```

## 自定义 Skills

```bash
# 我的 Office 工具箱（本仓库）
~/.kimi/skills/skill-manager/scripts/install-skill.sh "https://github.com/4ys92c5vh4-afk/office-toolkit"
```

> 注：部分 skills 为系统预装（如 `skill-manager`、`a11y-check`、`api-design` 等），无需手动安装。

---

## 一键安装所有（批量脚本）

```bash
#!/bin/bash
# install-all-skills.sh

SKILLS=(
  "https://github.com/anthropics/skills/tree/main/skills/docx"
  "https://github.com/anthropics/skills/tree/main/skills/pptx"
  "https://github.com/anthropics/skills/tree/main/skills/xlsx"
  "https://github.com/anthropics/skills/tree/main/skills/pdf"
  "https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring"
  "https://github.com/anthropics/skills/tree/main/skills/internal-comms"
  "https://github.com/anthropics/skills/tree/main/skills/claude-api"
  "https://github.com/anthropics/skills/tree/main/skills/mcp-builder"
  "https://github.com/anthropics/skills/tree/main/skills/frontend-design"
  "https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder"
  "https://github.com/anthropics/skills/tree/main/skills/webapp-testing"
  "https://github.com/anthropics/skills/tree/main/skills/algorithmic-art"
  "https://github.com/anthropics/skills/tree/main/skills/canvas-design"
  "https://github.com/anthropics/skills/tree/main/skills/theme-factory"
  "https://github.com/anthropics/skills/tree/main/skills/brand-guidelines"
)

THIRD_PARTY=(
  "ci-cd-pipelines:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/ci-cd-pipelines"
  "git-advanced:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/git-advanced"
  "database-optimization:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/database-optimization"
  "postgres-optimization:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/postgres-optimization"
  "redis-patterns:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/redis-patterns"
  "monitoring-observability:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/monitoring-observability"
  "microservices-design:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/microservices-design"
  "aws-cloud-patterns:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/aws-cloud-patterns"
  "security-hardening:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/security-hardening"
  "authentication-patterns:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/authentication-patterns"
  "testing-strategies:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/testing-strategies"
  "prompt-engineering:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/prompt-engineering"
  "mcp-development:https://github.com/rohitg00/awesome-claude-code-toolkit/tree/main/skills/mcp-development"
)

INSTALLER="$HOME/.kimi/skills/skill-manager/scripts/install-skill.sh"

for url in "${SKILLS[@]}"; do
  "$INSTALLER" "$url"
done

for item in "${THIRD_PARTY[@]}"; do
  name="${item%%:*}"
  url="${item#*:}"
  "$INSTALLER" "$url" --target "$name"
done

# 自定义 skill
"$INSTALLER" "https://github.com/4ys92c5vh4-afk/office-toolkit"

echo "All skills installed!"
```
