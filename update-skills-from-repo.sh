#!/bin/bash
# 从 monorepo 更新本地 skills
# 用法: ./update-skills-from-repo.sh

set -e

REPO_DIR="$HOME/kimi-skills"
SKILLS_DIR="$HOME/.kimi/skills"
LOG_FILE="$HOME/.local/share/kimi-cli/monorepo-update.log"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$REPO_DIR"

log "开始从 monorepo 更新 skills..."

# 拉取最新代码
if git pull origin main 2>&1 | tee -a "$LOG_FILE" | grep -q "Already up to date"; then
    log "Monorepo 已是最新，无需更新"
    exit 0
fi

log "Monorepo 有更新，同步到本地 skills..."

# 同步每个 skill
for skill_dir in "$REPO_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    
    # 跳过非 skill 目录和脚本
    if [[ "$skill_name" == *.sh ]] || [[ "$skill_name" == install-guide.md ]]; then
        continue
    fi
    
    target_dir="$SKILLS_DIR/$skill_name"
    
    if [ -d "$target_dir" ]; then
        # 使用 rsync 同步（保留本地修改，但更新现有文件）
        rsync -av --exclude='.git' "$skill_dir" "$target_dir" 2>&1 | tail -3 | tee -a "$LOG_FILE"
        log "已更新: $skill_name"
    else
        log "跳过: $skill_name (本地不存在)"
    fi
done

log "同步完成"
