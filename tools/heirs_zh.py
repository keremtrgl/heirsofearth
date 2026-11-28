"""Heirs of Earth 4.3.2: Simplified Chinese.

The mod's text is written as T(en, tr) pairs in the generators. Chinese is kept apart, in tools/zh/*.json files that map each English
text to its Chinese text, so the generators do not need a third language. heirs_build.py writes
Languages/ChineseSimplified (简体中文) from them; a text with no Chinese yet is left out, and the game shows the English instead.

    python heirs_zh.py export   writes tools/zh/_todo/NNN.json, batches of texts that still need Chinese, with where each is used
    python heirs_zh.py merge N  reads tools/zh/_answers/NNN.json (a list of Chinese texts in the batch's order) into tools/zh/NNN.json
    python heirs_zh.py show N   prints batch N with numbered lines, the texts in full
    python heirs_zh.py check    counts missing texts and checks every translation keeps the placeholders and line breaks

Batches stay fixed while they are being translated: export again only when every batch has been merged.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ZH_DIR = os.path.join(HERE, "zh")
CHINESE = "ChineseSimplified (简体中文)"
BATCH = 90

# {0}, {PAWN_labelShort}, [PAWN_nameDef] and the like must survive translation unchanged.
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}|\[[A-Za-z0-9_]+\]")


def load():
    """All Chinese translations, English text -> Chinese text."""
    out = {}
    for path in sorted(glob.glob(os.path.join(ZH_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            for en, zh in json.load(f).items():
                if zh:
                    out[en] = zh
    return out


def texts():
    """Every English text of the mod with the places it is used, in build order."""
    import heirs_data as data
    from heirs_xml import render
    data.load_all()
    seen = {}
    for defs in data.FILES.values():
        _, tr = render(defs)
        for def_type, path, t in tr:
            seen.setdefault(t.en, []).append(f"{def_type}:{path}")
    for k, v in data.KEYED.items():
        seen.setdefault(v.en, []).append("Keyed:" + k)
    return seen


def problems(en, zh):
    """What is wrong with one translation (empty list if nothing)."""
    out = []
    if sorted(PLACEHOLDER.findall(en)) != sorted(PLACEHOLDER.findall(zh)):
        out.append(f"placeholders {sorted(PLACEHOLDER.findall(en))} != {sorted(PLACEHOLDER.findall(zh))}")
    if en.count("\n") != zh.count("\n"):
        out.append(f"line breaks {en.count(chr(10))} != {zh.count(chr(10))}")
    if "->" in en and en.count("->") != zh.count("->"):
        out.append("rule arrows differ")
    return out


def export():
    have = load()
    todo = [(en, where) for en, where in texts().items() if en not in have]
    folder = os.path.join(ZH_DIR, "_todo")
    os.makedirs(folder, exist_ok=True)
    for f in glob.glob(os.path.join(folder, "*.json")):
        os.remove(f)
    for i in range(0, len(todo), BATCH):
        batch = [{"en": en, "where": where[:2]} for en, where in todo[i:i + BATCH]]
        with open(os.path.join(folder, f"{i // BATCH:03d}.json"), "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=1)
    print(f"to translate: {len(todo)} texts in {(len(todo) + BATCH - 1) // BATCH} batches")


def check(strict=False):
    have = load()
    all_texts = texts()
    missing = [en for en in all_texts if en not in have]
    bad = [(en, p) for en in all_texts if en in have for p in problems(en, have[en])]
    unused = [en for en in have if en not in all_texts]
    print(f"chinese: {len(all_texts) - len(missing)}/{len(all_texts)} translated, {len(bad)} problems, {len(unused)} unused")
    for en, p in bad[:20]:
        print("  PROBLEM", p, "|", en[:80])
    if strict and (missing or bad):
        raise SystemExit(1)
    return len(missing), len(bad)


def batch(n):
    with open(os.path.join(ZH_DIR, "_todo", f"{n:03d}.json"), encoding="utf-8") as f:
        return json.load(f)


def show(n):
    for i, item in enumerate(batch(n)):
        print(f"#{i} [{item['where'][0]}] {json.dumps(item['en'], ensure_ascii=False)}")


def merge(n):
    items = batch(n)
    with open(os.path.join(ZH_DIR, "_answers", f"{n:03d}.json"), encoding="utf-8") as f:
        answers = json.load(f)
    if len(answers) != len(items):
        raise SystemExit(f"batch {n}: {len(items)} texts but {len(answers)} answers")
    out, bad = {}, 0
    for item, zh in zip(items, answers):
        for p in problems(item["en"], zh):
            bad += 1
            print(f"  PROBLEM {p} | {item['en'][:70]}")
        out[item["en"]] = zh
    with open(os.path.join(ZH_DIR, f"{n:03d}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"batch {n}: {len(out)} merged, {bad} problems")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "export":
        export()
    elif cmd == "show":
        show(int(sys.argv[2]))
    elif cmd == "merge":
        for n in sys.argv[2:]:
            merge(int(n))
    else:
        check(strict=cmd == "strict")
