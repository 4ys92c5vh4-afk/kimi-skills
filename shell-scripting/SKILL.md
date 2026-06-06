---
name: shell-scripting
description: Shell/Bash 脚本编写指南。覆盖文件批量处理、文本处理、系统运维、定时任务、日志分析、管道组合。适用于 macOS/Linux 日常自动化。当用户需要"写个shell脚本"、"批量处理文件"、"定时任务"、"日志分析"、"系统运维"时触发。
---

# Shell 脚本编写指南

## 何时使用

- 批量文件处理（重命名、移动、删除、压缩）
- 文本日志分析与提取
- 系统运维监控（磁盘、内存、进程）
- 定时任务（crontab）
- 快速原型，比 Python 更轻量

## 基础语法

### 变量与引用
```bash
name=" incubator "
echo "${name}"      # 推荐: 带花括号
echo "$name"        # 双引号: 变量展开
echo '$name'        # 单引号: 原样输出
echo "${name// /}"  # 删除所有空格
```

### 条件判断
```bash
if [ -f "file.txt" ]; then
    echo "文件存在"
elif [ -d "dir" ]; then
    echo "目录存在"
else
    echo "不存在"
fi

# 常用测试
[ -z "$var" ]       # 字符串为空
[ -n "$var" ]       # 字符串非空
[ "$a" = "$b" ]     # 字符串相等
[ "$a" -eq "$b" ]   # 数字相等
[ -f "file" ]       # 是普通文件
[ -d "dir" ]        # 是目录
[ -e "path" ]       # 存在
```

### 循环
```bash
# for 循环
for file in *.txt; do
    echo "处理: $file"
done

# 读取文件行
while IFS= read -r line; do
    echo "$line"
done < "input.txt"

# C 风格
for ((i=0; i<10; i++)); do
    echo $i
done
```

## 实用脚本

### 批量重命名（添加前缀/后缀）
```bash
#!/bin/bash
# add_prefix.sh prefix_ *.txt
prefix="$1"
shift
for file in "$@"; do
    [ -f "$file" ] && mv "$file" "${prefix}${file}"
done
echo "完成"
```

### 批量压缩旧日志
```bash
#!/bin/bash
# 压缩 7 天前的日志文件
find /var/log -name "*.log" -mtime +7 -exec gzip {} \;
echo "旧日志已压缩"
```

### 监控系统资源
```bash
#!/bin/bash
# monitor.sh - 监控磁盘和内存

disk_usage=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
mem_usage=$(vm_stat | awk '/Pages active/ {gsub(/\./,""); print $3}')

if [ "$disk_usage" -gt 80 ]; then
    echo "警告: 磁盘使用率 ${disk_usage}%" | mail -s "磁盘告警" admin@example.com
fi

if [ "$mem_usage" -gt 1000000 ]; then
    echo "警告: 内存使用过高"
fi
```

### 日志分析（提取错误）
```bash
#!/bin/bash
# extract_errors.sh logfile
logfile="$1"
output="errors_$(date +%Y%m%d).txt"

grep -i "error\|exception\|failed" "$logfile" | \
    awk '{print $1 " " $2 ": " $0}' | \
    sort | uniq -c | sort -rn | \
    head -20 > "$output"

echo "错误统计已保存到 $output"
```

### 定时备份脚本
```bash
#!/bin/bash
# backup.sh - 每日备份

backup_dir="/backup/$(date +%Y%m%d)"
source_dir="/data/incubator"

mkdir -p "$backup_dir"

tar -czf "${backup_dir}/incubator_$(date +%H%M).tar.gz" \
    -C "$(dirname $source_dir)" \
    "$(basename $source_dir)"

# 保留最近 7 天
find /backup -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;

echo "备份完成: $backup_dir"
```

## 文本处理三板斧

### grep - 搜索
```bash
grep "关键词" file.txt              # 基础搜索
grep -i "关键词" file.txt           # 忽略大小写
grep -r "关键词" ./dir/             # 递归搜索
grep -E "正则表达式" file.txt       # 扩展正则
grep -v "排除词" file.txt           # 反向匹配
grep -n "关键词" file.txt           # 显示行号
grep -C 3 "关键词" file.txt         # 显示前后3行上下文
```

### sed - 流编辑
```bash
sed 's/old/new/g' file.txt          # 替换所有
sed -i 's/old/new/g' file.txt       # 直接修改文件
sed '1,10d' file.txt                # 删除1-10行
sed -n '5,20p' file.txt             # 只打印5-20行
sed '/pattern/d' file.txt           # 删除匹配行
```

### awk - 列处理
```bash
awk '{print $1, $3}' file.txt       # 打印第1、3列
awk -F',' '{print $2}' file.csv     # 指定逗号分隔符
awk '$3 > 100 {print $0}' file.txt  # 条件过滤
awk '{sum+=$2} END {print sum}' f   # 求和
awk '!seen[$1]++' file.txt          # 按第一列去重
```

## 定时任务（crontab）

```bash
# 编辑定时任务
crontab -e

# 格式: 分 时 日 月 周 命令
0 2 * * * /scripts/backup.sh        # 每天凌晨2点备份
0 9 * * 1-5 /scripts/report.sh      # 工作日上午9点生成报表
*/30 * * * * /scripts/monitor.sh    # 每30分钟监控一次
0 0 1 * * /scripts/monthly.sh       # 每月1号执行

# 查看定时任务
crontab -l
```

## 最佳实践

1. **Shebang**：脚本首行必须是 `#!/bin/bash` 或 `#!/bin/sh`
2. **set 选项**：开头添加 `set -euo pipefail` 让脚本更健壮
   - `-e`：遇到错误立即退出
   - `-u`：使用未定义变量报错
   - `-o pipefail`：管道中任一命令失败即退出
3. **变量引用**：始终用 `"${var}"` 包裹，防止空格问题
4. **路径处理**：使用 `$(dirname "$0")` 获取脚本所在目录
5. **日志输出**：`exec > >(tee -a logfile.txt) 2>&1` 同时输出到终端和日志
