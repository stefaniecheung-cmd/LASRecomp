# -*- coding: utf-8 -*-
"""中文词表自检：提交前跑一遍，任何一项不为 0 都不要推。

检查项
  1. 条目数、重复键
  2. 占位符：数量与次序都必须和英文原文一致
  3. 换行转义：C 字符串里不允许出现「两个反斜杠 + n」（会显示成字面 \\n）
  4. 繁体列：不能还是简体（需要 opencc，没有就跳过）
  5. 空译文、译文里出现 ###（会截断 ImGui 的稳定 ID）
  6. 文件级：引号成对、括号平衡、每行都是 UI_TEXT(...) 形式

用法
  python scripts/check_zh.py            # 只读检查
  python scripts/check_zh.py --strict   # 有警告也算失败
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HDR = os.path.join(HERE, os.pardir, "runtime/ui/localization_strings.h")

LIT = r'"(?:[^"\\]|\\.)*"'
RUN = r"%s(?:\s*%s)*" % (LIT, LIT)
ESC = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "r": "\r"}
PH = re.compile(r"%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[diouxXeEfgGcsp]")


def unesc(t):
    out, i = [], 0
    while i < len(t):
        c = t[i]
        if c == "\\" and i + 1 < len(t):
            out.append(ESC.get(t[i + 1], "\\" + t[i + 1]))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def main():
    src = open(HDR, encoding="utf-8").read()
    rows = []
    for m in re.finditer(r"UI_TEXT\(\s*(%s)\s*,\s*(%s)\s*,\s*(%s)\)" % (RUN, RUN, RUN), src):
        g = lambda i: unesc("".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(i))))
        rows.append((g(1), g(2), g(3)))

    errors, warns = [], []

    # 1. 数量与重复
    keys = [r[0] for r in rows]
    dup = [k for k, n in collections.Counter(keys).items() if n > 1]
    if dup:
        errors.append("重复键 %d 条，例如：%r" % (len(dup), dup[:3]))

    # 2. 占位符
    pct = [(en, zh) for en, zh, _ in rows if en.count("%") != zh.count("%")]
    if pct:
        errors.append("百分号数量不一致 %d 条，例如：%r" % (len(pct), pct[:2]))
    bad_ph = [(en, zh) for en, zh, _ in rows if sorted(PH.findall(en)) != sorted(PH.findall(zh))]
    if bad_ph:
        errors.append("占位符不一致 %d 条，例如：%r" % (len(bad_ph), bad_ph[:2]))
    bad_order = [(en, zh) for en, zh, _ in rows
                 if PH.findall(en) and sorted(PH.findall(en)) == sorted(PH.findall(zh))
                 and PH.findall(en) != PH.findall(zh)]
    if bad_order:
        errors.append("占位符次序不一致 %d 条，例如：%r" % (len(bad_order), bad_order[:2]))

    # 3. 双重转义
    two = collections.Counter(1 for line in src.splitlines()
                             if line.startswith("UI_TEXT(") and (chr(92) * 2 + "n") in line)
    if two:
        errors.append("出现「两个反斜杠+n」的行 %d 条（会显示成字面 \\n）" % sum(two.values()))

    # 4. 繁体列
    try:
        from opencc import OpenCC
        t2s = OpenCC("t2s")
        s2t = OpenCC("s2twp")
        cjk = re.compile(r"[\u4e00-\u9fff]")
        simp_in_tw = [en for en, zh, tw in rows
                      if tw and cjk.search(tw) and t2s.convert(tw) == tw
                      and s2t.convert(zh) != tw]
        if simp_in_tw:
            warns.append("繁体列仍是简体 %d 条，例如：%r" % (len(simp_in_tw), simp_in_tw[:3]))
    except ImportError:
        warns.append("未安装 opencc，跳过繁体检查（pip install opencc-python-reimplemented）")

    # 5. 空译文 / ###
    empty = [en for en, zh, tw in rows if not zh.strip()]
    if empty:
        errors.append("空译文 %d 条，例如：%r" % (len(empty), empty[:3]))
    hash_id = [en for en, zh, tw in rows if "###" in zh or "###" in tw]
    if hash_id:
        errors.append("译文含 ###（会截断 ImGui ID）%d 条，例如：%r" % (len(hash_id), hash_id[:3]))

    # 6. 文件级
    if src.count('"') % 2:
        errors.append("引号数量为奇数，字符串没有闭合")
    if src.count("(") != src.count(")"):
        errors.append("括号不平衡：%d 个 ( / %d 个 )" % (src.count("("), src.count(")")))
    odd = [l for l in src.splitlines() if l.startswith("UI_TEXT(") and not l.rstrip().endswith(")")]
    if odd:
        errors.append("格式异常行 %d 条，例如：%r" % (len(odd), odd[:2]))

    print("条目：%d" % len(rows))
    for w in warns:
        print("警告：%s" % w)
    for e in errors:
        print("错误：%s" % e)
    if not errors and not warns:
        print("全部通过")
    if errors or ("--strict" in sys.argv and warns):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
