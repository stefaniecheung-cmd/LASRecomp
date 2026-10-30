#!/usr/bin/env bash
# 合并上游更新，并重新生成 / 自检中文词表。
#
#   ./scripts/sync-upstream.sh            # 默认合并 upstream/beta_5
#   ./scripts/sync-upstream.sh main       # 指定上游分支
#
# 它只做「拉取 + 合并 + 重新生成 + 自检」，不提交、不推送：
# 冲突和译文回归需要人看一眼再决定。
set -euo pipefail

UPSTREAM_URL="https://github.com/peiikai/LASRecomp.git"
BRANCH="${1:-beta_5}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! git remote get-url upstream >/dev/null 2>&1; then
  echo "== 添加 upstream 远端"
  git remote add upstream "$UPSTREAM_URL"
fi

echo "== 拉取 upstream"
git fetch upstream --prune

echo "== 合并 upstream/$BRANCH（有冲突就手动解决：词表交给生成器，.mm 保留 ui_tr）"
git merge "upstream/$BRANCH" || {
  echo
  echo "合并有冲突。处理建议："
  echo "  runtime/ui/localization_strings.h -> git checkout --theirs 之后跑 python gen_strings.py"
  echo "  runtime/ui/*.mm                   -> 保留 ui_tr(...)，把上游新文案包进去并记进 zh_table.py"
  exit 1
}

echo "== 重新生成词表"
python gen_strings.py

echo "== 自检"
python scripts/check_zh.py

echo
echo "下一步："
echo "  1) 看 runtime/ui/launcher.mm 的 LARECOMP_VERSION 是否变了（变了发布 tag 要跟着改）"
echo "  2) 跑一遍菜单，重点看上游新增的页面"
echo "  3) 构建：gh workflow run release.yml --ref zh-cn -f tag=<版本> -f ref=\$(git rev-parse HEAD)"
