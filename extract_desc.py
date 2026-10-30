import re, os, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, "runtime", "ui")

table_src = open(os.path.join(UI, "localization_strings.h"), encoding="utf-8").read()
lit = r'"(?:[^"\\]|\\.)*"'
run = r'%s(?:\s*%s)*' % (lit, lit)

def join_run(text):
    return "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', text))

existing = set()
for m in re.finditer(r'UI_TEXT\(\s*(%s)\s*,\s*(%s)\s*,\s*(%s)\)' % (run, run, run), table_src):
    existing.add(join_run(m.group(1)))

CALLS = r'\b(opt_toggle|opt_choice|opt_slider|opt_link|opt_button|opt_text|opt_section|opt_label|row|toggle|slider|choice)\s*\('

def strip_comments(src):
    src = re.sub(r'/\*.*?\*/', lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    return re.sub(r'//[^\n]*', "", src)

found = {}
for path in glob.glob(os.path.join(UI, "*.mm")) + glob.glob(os.path.join(UI, "*.h")):
    name = os.path.basename(path)
    if name in ("localization_strings.h", "localization.mm", "localization.h"):
        continue
    raw = open(path, encoding="utf-8", errors="replace").read()
    src = strip_comments(raw)
    for m in re.finditer(CALLS, src):
        start = m.end() - 1  # at '('
        depth = 0
        i = start
        while i < len(src):
            c = src[i]
            if c == '"':
                i += 1
                while i < len(src) and src[i] != '"':
                    i += 2 if src[i] == '\\' else 1
                i += 1
                continue
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        args = src[start:i + 1]
        runs = [join_run(r.group(0)) for r in re.finditer(run, args, re.S)]
        if not runs:
            continue
        # description: the last run that reads like prose
        cand = None
        for s in reversed(runs):
            if len(s) >= 12 and " " in s.strip() and re.search(r"[A-Za-z]", s):
                cand = s
                break
        if cand is None:
            continue
        if cand in existing:
            continue
        line = src[:m.start()].count("\n") + 1
        found.setdefault(cand, [name, line])

print("existing keys:", len(existing))
print("untranslated descriptions:", len(found))
out = os.path.join(os.path.dirname(ROOT), "missing_desc.json")
json.dump({k: v for k, v in sorted(found.items(), key=lambda kv: (kv[1][0], kv[1][1]))},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written:", out)
