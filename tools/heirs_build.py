"""Writes every generated file of the Heirs of Earth mod from heirs_data.

Usage: python -I tools/heirs_build.py
Generated (and wiped before writing): HeirsOfEarth/Defs, Languages/*/Keyed/Heirs.xml,
Languages/Turkish (Türkçe)/DefInjected, About/About.xml, LoadFolders.xml.
"""
import os
import shutil
import sys
from collections import defaultdict
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heirs_data as data  # noqa: E402
from heirs_xml import injection_xml, keyed_xml, render  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "HeirsOfEarth")
TURKISH = "Turkish (Türkçe)"
import heirs_zh
CHINESE = heirs_zh.CHINESE


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


PARA = chr(10) * 2


def about():
    m = data.MOD
    desc = ("Centuries ago, nine colony ships left Earth. Their descendants founded nine heir nations that carry the "
            "heritage of real cultures: Nova Roma, the Yamato Shogunate, the Jarldom of Nordheim, the League of Hellas, "
            "Celestial Tianxia, the industrial Commonwealth of Albion, the river kingdom of New Kemet, the Satrapy of Pars "
            "and the mountain empire of Inti." + PARA +
            "Start as the heir of one nation or as an independent colony. Learn the knowledge of the others through trade, "
            "study, alliances and war: each nation has its own research branch with seven or more traditions, weapons, "
            "armour, buildings, floors, food, people, traders and a start scenario. Every nation has a story chain that "
            "ends with a lost relic, a hard choice and a legendary artifact." + PARA +
            "The nations live their own politics: they ally, declare war, capture each other's towns, send envoys, ask "
            "for tribute, offer marriages and can collapse." + PARA +
            "Requires Harmony. Core only; no DLC needed (with Royalty, the heir crowns count as noble headwear). English and Turkish, with a translation template for other languages.")
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ModMetaData>
  <name>{m['name']}</name>
  <author>{m['author']}</author>
  <packageId>{m['packageId']}</packageId>
  <modVersion>{m['version']}</modVersion>
  <supportedVersions>
    <li>1.6</li>
  </supportedVersions>
  <modDependencies>
    <li>
      <packageId>{m['harmony']}</packageId>
      <displayName>Harmony</displayName>
      <steamWorkshopUrl>steam://url/CommunityFilePage/2009463077</steamWorkshopUrl>
      <downloadUrl>{m['harmonyUrl']}</downloadUrl>
    </li>
  </modDependencies>
  <loadAfter>
    <li>{m['harmony']}</li>
  </loadAfter>
  <description>{escape(desc)}</description>
</ModMetaData>
"""


TEMPLATE_README = """Heirs of Earth - translation template

This folder holds every text of the mod in English, ready to translate. The game does not load it.

1. Copy the folders DefInjected and Keyed into HeirsOfEarth/Languages/<YourLanguage>/, using the language folder name the game
   uses (for example "French (Français)" or "German (Deutsch)"; see RimWorld/Data/Core/Languages).
2. Translate the text between the tags. Keep the tags, the keys and anything in curly braces such as {0} or {PAWN_nameDef}.
3. Start the game in your language. Dev mode -> "Translation report" lists anything missing.

The Turkish translation in Languages/Turkish (Türkçe) is a complete example. Translations are welcome as separate mods.
"""


LOAD_FOLDERS = """<?xml version="1.0" encoding="utf-8"?>
<loadFolders>
  <v1.6>
    <li>/</li>
    <li>1.6</li>
  </v1.6>
</loadFolders>
"""


def main():
    data.load_all()
    for sub in ("Defs", os.path.join("Languages", TURKISH, "DefInjected"), os.path.join("Languages", CHINESE), "TranslationTemplate"):
        shutil.rmtree(os.path.join(ROOT, sub), ignore_errors=True)
    write(os.path.join(ROOT, "About", "About.xml"), about())
    write(os.path.join(ROOT, "LoadFolders.xml"), LOAD_FOLDERS)

    injections = defaultdict(list)  # (DefType, file stem) -> [(path, tr)]
    names = set()
    count = 0
    for rel, defs in data.FILES.items():
        for d in defs:
            if d.name:
                k = (d.cls, d.name)
                if k in names:
                    raise SystemExit(f"duplicate def {d.cls} {d.name}")
                names.add(k)
        xml, tr = render(defs)
        write(os.path.join(ROOT, "Defs", rel), xml)
        stem = os.path.splitext(os.path.basename(rel))[0]
        for def_type, path, text in tr:
            injections[(def_type, stem)].append((path, text))
        count += len(defs)
    zh = heirs_zh.load()  # 4.3.2: Simplified Chinese from tools/zh; a text with no Chinese yet stays English in game
    for (def_type, stem), entries in injections.items():
        write(os.path.join(ROOT, "Languages", TURKISH, "DefInjected", def_type, stem + ".xml"), injection_xml([(p, t.tr) for p, t in entries]))
        zh_entries = [(p, zh[t.en]) for p, t in entries if t.en in zh]
        if zh_entries:
            write(os.path.join(ROOT, "Languages", CHINESE, "DefInjected", def_type, stem + ".xml"), injection_xml(zh_entries))
        write(os.path.join(ROOT, "TranslationTemplate", "DefInjected", def_type, stem + ".xml"), injection_xml([(p, t.en) for p, t in entries]))

    write(os.path.join(ROOT, "Languages", "English", "Keyed", "Heirs.xml"), keyed_xml([(k, v.en) for k, v in data.KEYED.items()]))
    write(os.path.join(ROOT, "Languages", TURKISH, "Keyed", "Heirs.xml"), keyed_xml([(k, v.tr) for k, v in data.KEYED.items()]))
    zh_keys = [(k, zh[v.en]) for k, v in data.KEYED.items() if v.en in zh]
    if zh_keys:
        write(os.path.join(ROOT, "Languages", CHINESE, "Keyed", "Heirs.xml"), keyed_xml(zh_keys))
    write(os.path.join(ROOT, "TranslationTemplate", "Keyed", "Heirs.xml"), keyed_xml([(k, v.en) for k, v in data.KEYED.items()]))
    write(os.path.join(ROOT, "TranslationTemplate", "HOW_TO_TRANSLATE.txt"), TEMPLATE_README)
    print(f"defs: {count}, files: {len(data.FILES)}, keys: {len(data.KEYED)}, injections: {sum(len(v) for v in injections.values())}, "
          f"chinese: {len(zh)} texts")


if __name__ == "__main__":
    main()
