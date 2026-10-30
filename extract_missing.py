import re, sys, os, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, "runtime", "ui")

# 1) existing keys from the translation table
table_src = open(os.path.join(UI, "localization_strings.h"), encoding="utf-8").read()

def parse_ui_text(src):
    keys = {}
    # UI_TEXT("en", "hans", "hant")
    for m in re.finditer(r'UI_TEXT\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+),\s*((?:"(?:[^"\\]|\\.)*"\s*)+),\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)', src):
        def join(group):
            parts = re.findall(r'"((?:[^"\\]|\\.)*)"', group)
            return "".join(parts)
        keys[join(m.group(1))] = (join(m.group(2)), join(m.group(3)))
    return keys

existing = parse_ui_text(table_src)
print("existing keys:", len(existing))

# 2) extract every joined string literal from the UI sources
lit_re = re.compile(r'"((?:[^"\\]|\\.)*)"')
# a run of literals possibly separated by whitespace/newlines
run_re = re.compile(r'(?:"(?:[^"\\]|\\.)*")(?:\s*(?:"(?:[^"\\]|\\.)*"))*', re.S)

found = {}
for path in glob.glob(os.path.join(UI, "*.mm")) + glob.glob(os.path.join(UI, "*.h")):
    name = os.path.basename(path)
    if name in ("localization_strings.h",):
        continue
    src = open(path, encoding="utf-8", errors="replace").read()
    # strip comments (rough): // and /* */ - keep line structure
    src_nc = re.sub(r'/\*.*?\*/', lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    src_nc = re.sub(r'//[^\n]*', "", src_nc)
    for m in run_re.finditer(src_nc):
        parts = lit_re.findall(m.group(0))
        s = "".join(parts)
        if len(s) < 12:
            continue
        if s not in found:
            # context: line number
            line = src_nc[:m.start()].count("\n") + 1
            found[s] = (name, line)

# 3) which look like UI text
def looks_like_ui(s):
    if not re.search(r"[A-Za-z]", s):
        return False
    if s.startswith(("third_party/", "C:/", "/usr/", "/System/", "runtime/", "docs/", "http")):
        return False
    if re.match(r'^[a-z0-9_./-]+\.(ttf|ttc|otf|dll|so|exe|json|txt|ini|png|bin)$', s):
        return False
    if s in ("##rows", "##row", "##text", "###"):
        return False
    if len(s) < 12:
        return False
    # needs a space and at least 2 words to be prose
    if " " not in s.strip():
        return False
    # skip printf-only patterns? keep: keys can hold %s
    return True

missing = {s: ctx for s, ctx in found.items() if looks_like_ui(s) and s not in existing}
print("candidate strings scanned:", sum(1 for s in found if looks_like_ui(s)))
print("missing (untranslated):", len(missing))

out = os.path.join(ROOT, "..", "missing_strings.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump({s: list(ctx) for s, ctx in sorted(missing.items(), key=lambda kv: (kv[1][0], kv[1][1]))}, f, ensure_ascii=False, indent=1)
print("written:", os.path.abspath(out))
