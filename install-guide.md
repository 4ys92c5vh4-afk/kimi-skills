# Kimi Skills 手动安装指南

由于网络限制无法自动下载，请按以下步骤手动安装：

## 方法一：浏览器下载后安装

### 1. 下载 Skills
打开浏览器访问：
- Anthropic Skills: https://github.com/anthropics/skills/archive/refs/heads/main.zip
- web-access Skill: https://github.com/eze-is/web-access/archive/refs/heads/main.zip

### 2. 解压到 Kimi Skills 目录

```bash
# 找到 Kimi skills 目录（通常是以下之一）
~/.local/share/uv/tools/kimi-code/lib/python3.13/site-packages/kimi_cli/skills/
~/.config/kimi/skills/
~/.kimi/skills/

# 解压下载的文件到该目录
unzip skills-main.zip -d ~/.kimi/skills/
```

## 方法二：使用代理/梯子后重试

如果你有代理工具，设置后可以重试：

```bash
export https_proxy=http://127.0.0.1:7890  # 根据你的代理端口调整
cd ~/.kimi/skills
git clone https://github.com/anthropics/skills.git
git clone https://github.com/eze-is/web-access.git
```

## 方法三：直接复制 skill 内容

1. 在浏览器中打开：
   - https://github.com/anthropics/skills/tree/main/skills/frontend-design
   - https://github.com/eze-is/web-access

2. 点击 "Code" → "Download ZIP" 或使用 GitHub 加速镜像

3. 解压后将文件夹放入 Kimi skills 目录

## Kimi Skills 目录位置

根据你的系统，可能是以下之一：

| 系统 | 路径 |
|------|------|
| macOS (uv) | `~/.local/share/uv/tools/kimi-code/lib/python3.13/site-packages/kimi_cli/skills/` |
| macOS (pip) | `~/.kimi/skills/` 或 `~/.config/kimi/skills/` |
| Linux | `~/.local/share/kimi/skills/` |

## 验证安装

安装后重启 Kimi Code，检查 skills：

```bash
kimi --list-skills
# 或
kimi /skills
```

