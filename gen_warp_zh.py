# -*- coding: utf-8 -*-
import re, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from warp_dict import PLACES, SUFFIX, DIR

ROOT = os.path.dirname(os.path.abspath(__file__))

def name(s):
    """Translate a place name (area or the X inside a label)."""
    if s in PLACES:
        return PLACES[s]
    m = re.match(r'^Level (\d+): (.+)$', s)
    if m:
        return "第 %s 迷宫：%s" % (m.group(1), name(m.group(2)))
    m = re.match(r'^(.+?) \(([^)]+)\)$', s)
    if m:
        base, q = m.group(1), m.group(2)
        if q in DIR:
            return "%s（%s）" % (name(base), DIR[q])
        if q in PLACES:
            return "%s（%s）" % (name(base), PLACES[q])
        return None
    # longest suffix match
    for suf in sorted(SUFFIX, key=len, reverse=True):
        if s.endswith(" " + suf):
            base = s[: -(len(suf) + 1)]
            b = name(base)
            return None if b is None else "%s%s" % (b, SUFFIX[suf])
    return None

def label(s):
    """Translate a warp label."""
    s = re.sub(r" \(Lv[0-9A-Za-z_]+\)$", "", s)  # (内部房间哈希后缀)
    s = re.sub(r"\s*/\s*[A-Za-z0-9_]+$", "", s)  # 去掉 "/ PanelLv10ClothesDungeon" 这类内部名
    m = re.match(r"^(.+) \(([0-9A-Z]{3}(?:_[a-z])?)\)( #\d)?$", s)
    core, code, dup = (m.group(1), m.group(2), m.group(3) or "") if m else (s, None, "")
    t = None
    if core == "Entrance":
        t = "入口"
    elif core == "Manbo's Mambo point":
        t = "曼波曼波曲传送点"
    elif re.match(r'^Room [0-9A-Z]{3}', core):
        m2 = re.match(r'^Room ([0-9A-Z]{3}[A-Z]?)(?: \(([a-z ]+)\))?$', core)
        if m2:
            extra = ""
            if m2.group(2):
                extra = "（%s）" % {"stairs": "楼梯", "ladder": "梯子", "drop in": "落入口", "entrance": "入口"}.get(m2.group(2), m2.group(2))
            t = "房间 %s%s" % (m2.group(1), extra)
    else:
        for pre, fmt in (("Manbo's Mambo: ", "曼波曼波曲：%s"), ("Warp hole: ", "传送洞：%s"),
                         ("Outside Level ", None), ("Outside ", "%s外"), ("Out of ", None)):
            if core.startswith(pre):
                rest = core[len(pre):]
                if pre == "Outside Level ":
                    m3 = re.match(r'^(\d+): (.+)$', rest)
                    if m3:
                        t = "第 %s 迷宫外：%s" % (m3.group(1), name(m3.group(2)))
                    break
                if pre == "Out of ":
                    n = name(rest.replace("the ", "", 1))
                    t = "%s出口" % n if n else None
                    break
                n = name(rest)
                t = fmt % n if n else None
                break
    if t is None:  # 无固定句式：整体按地名翻译（如 Beach path (09B)）
        t = name(core)
    if t is None:
        return None
    if code:
        t += "（%s）" % code
    if dup:  # " #2" -> "之二"，避免中文里出现 "#" 和多余空格
        n = int(dup.strip(" #"))
        t += "之" + "二三四五六七八九"[n - 2] if 2 <= n <= 9 else dup.strip()
    return t

if __name__ == "__main__":
    src = open(os.path.join(ROOT, "runtime/ui/warp_data.h"), encoding="utf-8").read()
    rows = re.findall(r'\{(\d+), "((?:[^"\\]|\\.)*)", "((?:[^"\\]|\\.)*)"', src)
    areas, labels = set(), []
    bad = set()
    for g, a, l in rows:
        areas.add(a)
        labels.append(l)
    out_a, out_l = {}, {}
    for a in sorted(areas):
        t = name(a)
        (out_a.__setitem__(a, t) if t else bad.add(a))
    for l in sorted(set(labels)):
        t = label(l)
        (out_l.__setitem__(l, t) if t else bad.add(l))
    print("areas:", len(out_a), "/", len(areas), " labels:", len(out_l), "/", len(set(labels)))
    print("unresolved:", len(bad))
    for b in sorted(bad)[:40]:
        print("   ?", b)
    json.dump({"areas": out_a, "labels": out_l}, open(os.path.join(os.path.dirname(ROOT), "warp_zh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
