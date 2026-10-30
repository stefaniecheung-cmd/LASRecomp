# -*- coding: utf-8 -*-
"""从 zh_table.py 生成 localization_strings.h 的「补充翻译」区块。

旧版（gen_strings_legacy.py）的两个坑，这里都堵住了：
  * 数据源按英文原文做键，不做「列表下标对齐」——下标一旦错位，整段译文会串行（#23 就是这么错的）。
  * 生成是「整块覆盖」，不是「只追加缺少的键」；改了译文重跑即可生效，不会留下旧版本。

用法：
  python gen_strings.py            # 重写区块
  python gen_strings.py --check    # 只比对，不写盘
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from zh_table import TABLE  # noqa: E402

HDR = os.path.join(HERE, "runtime/ui/localization_strings.h")
MARKER = "// ---- 以下为补充翻译（右栏说明、传送点、道具名、追踪器、开始界面），由社区补全 ----"


def cstr(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def render_block() -> str:
    lines = [MARKER]
    for en, (zh, tw) in TABLE.items():
        lines.append("UI_TEXT(%s, %s, %s)" % (cstr(en), cstr(zh), cstr(tw)))
    return "\n".join(lines) + "\n"


def main() -> int:
    src = open(HDR, encoding="utf-8").read()
    if MARKER not in src:
        print("错误：找不到补充翻译区块的标记行")
        return 2
    head = src[: src.index(MARKER)]
    new = head + render_block()

    if "--check" in sys.argv:
        if new == src:
            print("OK：%d 条，与 zh_table.py 一致" % len(TABLE))
            return 0
        a, b = src.splitlines(), new.splitlines()
        diff = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        print("不一致：%d 行不同（文件 %d 行 / 生成 %d 行）" % (len(diff), len(a), len(b)))
        for i, x, y in diff[:10]:
            print("  行%d\n    文件: %s\n    生成: %s" % (i, x[:120], y[:120]))
        return 1

    open(HDR, "w", encoding="utf-8", newline="\n").write(new)
    print("已写入：%d 条" % len(TABLE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
