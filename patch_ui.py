# -*- coding: utf-8 -*-
"""把二级界面里直接写字面量的控件改成走 ui_tr / ui_label。"""
import glob, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remaining_ui_zh import TRANS

TEXTISH = {'Text', 'TextDisabled', 'TextWrapped', 'TextColored', 'SetTooltip', 'SetItemTooltip'}
LABELED = {'Button', 'SmallButton', 'Selectable', 'Checkbox', 'RadioButton', 'MenuItem',
           'CollapsingHeader', 'BeginMenu', 'BeginCombo', 'BeginTabItem'}

CALL = re.compile(r'ImGui::(Text|TextDisabled|TextWrapped|TextColored|SetTooltip|SetItemTooltip|'
                  r'Button|SmallButton|Selectable|Checkbox|RadioButton|MenuItem|CollapsingHeader|'
                  r'BeginMenu|BeginCombo|BeginTabItem)\s*\(')
ESC = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', '0': '\0'}


def unescape(raw):
    out, i = [], 0
    while i < len(raw):
        if raw[i] == '\\' and i + 1 < len(raw):
            out.append(ESC.get(raw[i + 1], raw[i + 1]))
            i += 2
        else:
            out.append(raw[i])
            i += 1
    return ''.join(out)


def parse_literal_run(src, pos):
    """从 pos（应为引号）开始，吃掉连续相邻的字符串字面量。返回 (end, raw, text)。"""
    raw = []
    n = len(src)
    while True:
        while pos < n and src[pos] in ' \t\r\n':
            pos += 1
        # 行注释/块注释
        if src.startswith('//', pos):
            pos = src.find('\n', pos)
            if pos < 0:
                return None
            continue
        if pos >= n or src[pos] != '"':
            break
        pos += 1
        start = pos
        while pos < n:
            if src[pos] == '\\':
                pos += 2
                continue
            if src[pos] == '"':
                break
            pos += 1
        raw.append(src[start:pos])
        pos += 1  # 跳过结尾引号
    if not raw:
        return None
    return pos, ''.join(raw), unescape(''.join(raw))


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


def patch_file(path):
    src = open(path, encoding='utf-8').read()
    edits = []
    for m in CALL.finditer(src):
        name = m.group(1)
        open_paren = m.end() - 1
        end = call_end(src, open_paren)
        if end < 0:
            continue
        body_start = open_paren + 1
        # 第一个参数是否是字面量？
        p = body_start
        while p < end and src[p] in ' \t\r\n':
            p += 1
        run = parse_literal_run(src, p) if p < end and src[p] == '"' else None
        if run is None:
            if name not in ('Text', 'TextDisabled', 'TextWrapped', 'TextColored'):
                continue
            # Text(font, size, pos, col, "text") 这类重载：取最后一个字面量
            last = None
            for mm in re.finditer(r'"', src[body_start:end]):
                cand = parse_literal_run(src, body_start + mm.start())
                if cand and (last is None or cand[0] > last[0]):
                    last = cand
            run = last
            if run is None:
                continue
        r_end, raw, text = run
        if '##' in text or '###' in text or not text.strip():
            continue
        if text not in TRANS:
            continue
        lit = '"%s"' % raw
        wrapped = ('ui_tr(%s)' % lit) if name in TEXTISH else ('ui_label(%s).c_str()' % lit)
        edits.append((p, r_end, wrapped))
    if not edits:
        return 0
    for start, stop, new in sorted(edits, reverse=True):
        src = src[:start] + new + src[stop:]
    if '#include "localization.h"' not in src:
        # 放在第一个 imgui 头之后
        idx = src.find('#include "imgui.h"')
        if idx >= 0:
            nl = src.find('\n', idx)
            src = src[:nl + 1] + '#include "localization.h"  // (ui_tr/ui_label: 二级界面文案)\n' + src[nl + 1:]
        else:
            return -1
    open(path, 'w', encoding='utf-8', newline='').write(src)
    return len(edits)


total = 0
for f in sorted(glob.glob('runtime/ui/*.mm')):
    if f.endswith('localization.mm'):
        continue
    n = patch_file(f)
    if n:
        print('%-32s %d 处' % (os.path.basename(f), n))
        total += n
print('合计替换:', total, '| 词条表:', len(TRANS))
