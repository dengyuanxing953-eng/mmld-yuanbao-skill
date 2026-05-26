#!/usr/bin/env bash
#
# MMLD-Yuanbao Skill · 一键多平台安装脚本
#
# 支持的平台：
#   - hermes    (NousResearch Hermes Agent)
#   - openclaw  (OpenClaw)
#   - claude    (Claude Code)
#   - workbuddy (腾讯 WorkBuddy)
#
# 用法：
#   bash install.sh                  # 自动检测已安装的 Agent 平台
#   bash install.sh --tool hermes    # 指定平台
#   bash install.sh --uninstall      # 卸载

set -euo pipefail

SKILL_NAME="mmld-yuanbao-skill"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 颜色（仅终端支持时使用）
if [ -t 1 ]; then
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  RED='\033[0;31m'
  BLUE='\033[0;34m'
  NC='\033[0m'
else
  GREEN=''; YELLOW=''; RED=''; BLUE=''; NC=''
fi

info()  { echo -e "${BLUE}[信息]${NC} $*"; }
ok()    { echo -e "${GREEN}[成功]${NC} $*"; }
warn()  { echo -e "${YELLOW}[警告]${NC} $*"; }
error() { echo -e "${RED}[错误]${NC} $*" >&2; }

# 平台对应的安装目录
get_install_dir() {
  case "$1" in
    hermes)    echo "$HOME/.hermes/skills" ;;
    openclaw)  echo "$HOME/.openclaw/skills" ;;
    claude)    echo "$HOME/.claude/skills" ;;
    workbuddy) echo "$HOME/.workbuddy/skills" ;;
    *)         echo "" ;;
  esac
}

# 自动检测已安装的平台
detect_platforms() {
  local detected=()
  [ -d "$HOME/.hermes" ]    && detected+=("hermes")
  [ -d "$HOME/.openclaw" ]  && detected+=("openclaw")
  [ -d "$HOME/.claude" ]    && detected+=("claude")
  [ -d "$HOME/.workbuddy" ] && detected+=("workbuddy")
  echo "${detected[@]:-}"
}

# 安装到指定平台
install_to() {
  local platform="$1"
  local target_dir
  target_dir="$(get_install_dir "$platform")"

  if [ -z "$target_dir" ]; then
    error "未知平台：$platform"
    return 1
  fi

  info "安装到 $platform ($target_dir)"
  mkdir -p "$target_dir"

  local dest="$target_dir/$SKILL_NAME"
  if [ -e "$dest" ]; then
    warn "已存在旧版本，备份为 ${dest}.bak.$(date +%s)"
    mv "$dest" "${dest}.bak.$(date +%s)"
  fi

  # 复制（排除 .git 和缓存，以及 GitHub 专属文件）
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
          --exclude='.gitignore' --exclude='install.sh' \
          "$SCRIPT_DIR/" "$dest/"
  else
    cp -r "$SCRIPT_DIR" "$dest"
    rm -rf "$dest/.git" "$dest"/scripts/__pycache__ 2>/dev/null || true
    rm -f "$dest/.gitignore" "$dest/install.sh" 2>/dev/null || true
  fi

  ok "$platform 安装完成 → $dest"

  # 平台特定的后置提示
  case "$platform" in
    hermes)
      echo "  验证：hermes skills list | grep mmld-yuanbao"
      ;;
    openclaw)
      echo "  验证：在 OpenClaw 对话中输入 /mmld-yuanbao 或直接对话触发"
      ;;
    claude)
      echo "  验证：重启 Claude Code 后在对话中触发"
      ;;
    workbuddy)
      echo "  验证：重启 WorkBuddy 后在技能列表查看"
      ;;
  esac
}

# 卸载
uninstall_from() {
  local platform="$1"
  local target_dir
  target_dir="$(get_install_dir "$platform")"
  local dest="$target_dir/$SKILL_NAME"

  if [ -d "$dest" ]; then
    rm -rf "$dest"
    ok "$platform 卸载完成"
  else
    info "$platform 未安装 $SKILL_NAME"
  fi
}

# 显示帮助
show_help() {
  cat <<EOF
MMLD-Yuanbao Skill · 一键多平台安装脚本

用法：
  bash install.sh                   自动检测已安装的 Agent 平台并安装
  bash install.sh --tool <platform> 安装到指定平台
  bash install.sh --uninstall       从所有已安装平台卸载
  bash install.sh --help            显示本帮助

支持的平台：
  hermes      Hermes Agent (NousResearch)  → ~/.hermes/skills/
  openclaw    OpenClaw                     → ~/.openclaw/skills/
  claude      Claude Code                  → ~/.claude/skills/
  workbuddy   WorkBuddy（腾讯）             → ~/.workbuddy/skills/

示例：
  bash install.sh --tool hermes
  bash install.sh --tool openclaw
EOF
}

# 主流程
main() {
  local mode="install"
  local target_platform=""

  while [ $# -gt 0 ]; do
    case "$1" in
      --tool)
        target_platform="$2"
        shift 2
        ;;
      --uninstall)
        mode="uninstall"
        shift
        ;;
      --help|-h)
        show_help
        exit 0
        ;;
      *)
        error "未知参数：$1"
        show_help
        exit 1
        ;;
    esac
  done

  echo ""
  info "MMLD-Yuanbao Skill · 多平台安装工具"
  info "源目录：$SCRIPT_DIR"
  echo ""

  # 安装模式
  if [ "$mode" = "install" ]; then
    if [ -n "$target_platform" ]; then
      install_to "$target_platform"
    else
      # 自动检测
      local detected
      detected=($(detect_platforms))

      if [ ${#detected[@]} -eq 0 ]; then
        warn "未检测到任何已安装的 Agent 平台"
        info "请使用 --tool <platform> 指定平台"
        show_help
        exit 1
      fi

      info "检测到 ${#detected[@]} 个已安装的 Agent 平台：${detected[*]}"
      echo ""

      for p in "${detected[@]}"; do
        install_to "$p"
        echo ""
      done
    fi

    echo ""
    ok "全部完成。现在可以在 Agent 对话里这样触发："
    echo ""
    cat <<'EOF'
  帮我给王亿博鲜活烧烤（唐家湾海景露台店）做腾讯元宝 GEO 文章。
  店在珠海香洲区情侣北路唐家湾沙滩入口东 50 米，人均 65-85 元。
  招牌牛骨汤浸泡 20 分钟面筋，秦岭红皮花椒现磨。
  美团 4.8 分 2300+ 评价，必吃榜入围。
EOF
    echo ""
  fi

  # 卸载模式
  if [ "$mode" = "uninstall" ]; then
    if [ -n "$target_platform" ]; then
      uninstall_from "$target_platform"
    else
      for p in hermes openclaw claude workbuddy; do
        uninstall_from "$p"
      done
    fi
  fi
}

main "$@"
