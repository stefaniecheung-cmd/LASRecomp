# -*- coding: utf-8 -*-
"""把所有待翻译条目写成 UI_TEXT 行，追加到 localization_strings.h"""
import re, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from opencc import OpenCC
from translations_92 import TRANS
from names_dict import NAMES
from remaining_ui_zh import TRANS as UI_SECONDARY

ROOT = os.path.dirname(os.path.abspath(__file__))
HDR = os.path.join(ROOT, "runtime/ui/localization_strings.h")
cc = OpenCC("s2twp")

def cstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'

# 已有 key（按 C 语义还原转义后比较）
src = open(HDR, encoding="utf-8").read()
lit = r'"(?:[^"\\]|\\.)*"'
run = r'%s(?:\s*%s)*' % (lit, lit)
def unesc(t):
    return t.encode().decode("unicode_escape")

existing = set()
for m in re.finditer(r'UI_TEXT\(\s*(%s)\s*,\s*(%s)\s*,\s*(%s)\)' % (run, run, run), src):
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
    existing.add(unesc("".join(parts)))

# 1) 92 条说明文字（#23 改为“你的游戏文件”）
desc = json.load(open(os.path.join(os.path.dirname(ROOT), "missing_desc.json"), encoding="utf-8"))
keys = list(desc.keys())
assert len(keys) == len(TRANS)
# 抽取时保留的是转义文本（\\n 等），这里还原成真实字符再重新转义
pairs = { k.encode('utf-8').decode('unicode_escape'): v for k, v in zip(keys, TRANS) }

# 2) 传送点区域名与标签
warp = json.load(open(os.path.join(os.path.dirname(ROOT), "warp_zh.json"), encoding="utf-8"))
pairs.update(warp["areas"])
pairs.update(warp["labels"])

# 3) 道具名 / 追踪器 / 开始界面
pairs.update(NAMES)

# 4) 二级界面：软键盘、随机化、剧透、存档编辑、作弊、按键、宠物、弹窗、追踪器图例
pairs.update(UI_SECONDARY)

# 过滤：已有 key 跳过；空白翻译跳过
final = {k: v for k, v in pairs.items() if k not in existing and v.strip()}
lines = [
    "",
    "// ---- 以下为补充翻译（右栏说明、传送点、道具名、追踪器、开始界面），由社区补全 ----",
]
for k in sorted(final):
    lines.append("UI_TEXT(%s, %s, %s)" % (cstr(k), cstr(final[k]), cstr(cc.convert(final[k]))))

open(HDR, "a", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("新增条目:", len(final), " 跳过(已存在):", len(pairs) - len(final))
print("总计:", len(existing) + len(final))
json.dump(final, open(os.path.join(os.path.dirname(ROOT), "added_entries.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
