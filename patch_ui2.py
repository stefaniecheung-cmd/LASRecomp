# -*- coding: utf-8 -*-
"""第二遍：处理 TextColored(颜色, "文字") / Text(font, ...) 这类文本不在第一参数的情况。
只包裹"最后一个参数、后面紧跟右括号"的字面量，避免动到三元表达式里的片段。"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remaining_ui_zh import TRANS

CALL = re.compile(r'ImGui::(Text|TextDisabled|TextWrapped|TextColored)\s*\(')
ESC = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', '0': '\0'}


def unescape(raw):
    out, i = [], 0
    while i < len(raw):
        if raw[i] == '\\' and i + 1 < len(raw):
            out.append(ESC.get(raw[i + 1], raw[i + 1])); i += 2
        else:
            out.append(raw[i]); i += 1
    return ''.join(out)


def literals(src, start, end):
    """返回 [(run_start, run_end, raw, text)]，正确跳过字符串内部。"""
    out = []
    i = start
    while i < end:
        if src[i] == '"':
            rs = i
            raw = []
            i += 1
            cur = []
            while i < end:
                if src[i] == '\\':
                    cur.append(src[i]); cur.append(src[i + 1]); i += 2; continue
                if src[i] == '"':
                    break
                cur.append(src[i]); i += 1
            raw.append(''.join(cur))
            i += 1
            # 相邻字面量拼接
            while True:
                j = i
                while j < end and src[j] in ' \t\r\n':
                    j += 1
                if j < end and src[j] == '"':
                    i = j + 1
                    cur = []
                    while i < end:
                        if src[i] == '\\':
                            cur.append(src[i]); cur.append(src[i + 1]); i += 2; continue
                        if src[i] == '"':
                            break
                        cur.append(src[i]); i += 1
                    raw.append(''.join(cur))
                    i += 1
                    continue
                break
            out.append((rs, i, ''.join(raw), unescape(''.join(raw))))
        else:
            i += 1
    return out


def call_end(src, open_paren):
    depth = 0
    for i in range(open_paren, len(src)):
        if src[i] == '(':
            depth += 1
        elif src[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1


total = 0
for f in sorted(glob.glob('runtime/ui/*.mm')):
    if f.endswith('localization.mm'):
        continue
    src = open(f, encoding='utf-8').read()
    edits = []
    for m in CALL.finditer(src):
        op = m.end() - 1
        end = call_end(src, op)
        if end < 0:
            continue
        body = src[op:end + 1]
        if 'ui_tr' in body or 'ui_label' in body:
            continue
        runs = literals(src, op + 1, end)
        if not runs:
            continue
        rs, re_, raw, text = runs[-1]
        # 必须是整段最后一个参数
        j = re_
        while j < end and src[j] in ' \t\r\n':
            j += 1
        if j != end:
            continue
        if not text.strip() or text.startswith('%') or '##' in text:
            continue
        if text not in TRANS:
            continue
        edits.append((rs, re_, 'ui_tr("%s")' % raw))
    if not edits:
        continue
    for s, e, new in sorted(edits, reverse=True):
        src = src[:s] + new + src[e:]
    open(f, 'w', encoding='utf-8', newline='').write(src)
    print('%-28s %d 处' % (os.path.basename(f), len(edits)))
    total += len(edits)
print('合计:', total)
