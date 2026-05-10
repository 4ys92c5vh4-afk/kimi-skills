#!/bin/bash
# 推送到 GitHub 仓库的脚本
# 运行前需要先执行: gh auth login

set -e

GITHUB_USER="4ys92c5vh4-afk"
REPO_NAME="kimi-skills"
REPO_URL="git@github.com:${GITHUB_USER}/${REPO_NAME}.git"

echo "检查 GitHub 认证状态..."
if ! gh auth status &>/dev/null; then
    echo "❌ 未登录 GitHub CLI"
    echo "请先运行: gh auth login"
    echo "选择: GitHub.com → SSH → 按提示完成认证"
    exit 1
fi

echo "✅ GitHub CLI 已登录"

# 检查仓库是否已存在
echo "检查远程仓库是否存在..."
if ! gh repo view "${GITHUB_USER}/${REPO_NAME}" &>/dev/null; then
    echo "创建远程仓库 ${REPO_NAME}..."
    gh repo create "${REPO_NAME}" --public --description "Personal Kimi CLI skills collection" --source=. --remote=origin --push
    echo "✅ 仓库创建并推送完成"
else
    echo "仓库已存在，设置 remote 并推送..."
    git remote add origin "${REPO_URL}" 2>/dev/null || git remote set-url origin "${REPO_URL}"
    git branch -M main
    git push -u origin main
    echo "✅ 推送完成"
fi

echo ""
echo "🎉 完成！仓库地址: https://github.com/${GITHUB_USER}/${REPO_NAME}"
