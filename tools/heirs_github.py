"""Builds a clean copy of Heirs of Earth for the GitHub repository (keremtrgl/heirsofearth).

Usage: python -I heirs_github.py <repo clone folder> <release zip path>
README.md, LICENSE, LICENSE-ASSETS, .gitignore, .gitattributes and .git in the clone are kept; everything else is rebuilt.
"""
import glob
import os
import re
import shutil
import sys
import zipfile

SRC = r"C:\Genel Oyun Dosyası\özel\Claude\RimMod"
OUT = sys.argv[1]
ZIP = sys.argv[2]

if os.path.exists(OUT):
    keep = {os.path.join(OUT, n) for n in (".git", "README.md", ".gitignore", ".gitattributes", "LICENSE", "LICENSE-ASSETS")}
    for name in os.listdir(OUT):
        p = os.path.join(OUT, name)
        if p in keep:
            continue
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(OUT, exist_ok=True)


def copy(rel_src, rel_dst=None):
    s = os.path.join(SRC, rel_src)
    d = os.path.join(OUT, rel_dst or rel_src)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if os.path.isdir(s):
        shutil.copytree(s, d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "bin", "obj"))
    else:
        shutil.copy2(s, d)


# The mod itself, exactly as it ships.
copy("HeirsOfEarth")

# Build and test tools for this mod only.
for f in sorted(glob.glob(os.path.join(SRC, "tools", "heirs_*.py"))):
    copy(os.path.relpath(f, SRC))
for f in ["kut_render.py", "heirs_compile.ps1", "heirs_validate.ps1",
          "heirs_test/run.ps1", "heirs_test/Source"]:
    copy("tools/" + f)

# Design documents.
for f in glob.glob(os.path.join(SRC, "docs", "superpowers", "*", "*heirs*")):
    copy(os.path.relpath(f, SRC), "docs/design/" + os.path.basename(f))
copy("docs/heirs_balance.md", "docs/balance.md")
for n in ["kemet", "pars", "inti"]:
    copy(f"docs/{n}_gorseller.png", f"docs/art/{n}_art_sheet.png")

# Steam Workshop texts and screenshots (the uploader reads them from here).
copy("workshop/Heirs_Steam")


# CHANGELOG.md from the Steam change notes, newest first.
def vkey(path):
    v = re.search(r"change_note_([\d.]+)\.txt", path).group(1)
    return tuple(int(x) for x in v.split("."))


notes = sorted(glob.glob(os.path.join(SRC, "workshop", "Heirs_Steam", "change_note_*.txt")), key=vkey, reverse=True)
out = ["# Changelog", "",
       "Every release of Heirs of Earth, newest first. These are the same notes that appear on the "
       "[Steam Workshop change log](https://steamcommunity.com/sharedfiles/filedetails/changelog/3845334110).", ""]
for path in notes:
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().strip().splitlines()
    out.append("## " + lines[0].strip())
    out.append("")
    for line in lines[1:]:
        s = line.rstrip()
        bare = s.strip()
        if bare and not bare.startswith("-") and len(bare) < 80 and (bare.isupper() or (
                not bare.endswith(".") and not bare.endswith(":") and not line.startswith(" ")
                and len(bare.split()) <= 8 and bare[0].isupper() and not re.search(r"[.!?]\s", bare))):
            head = bare.capitalize() if bare.isupper() else bare
            head = re.sub(r"\bDlc\b|\bdlc\b", "DLC", head).replace("(new)", "(new)")
            for word in ["albion", "roma", "rome", "kemet", "pars", "inti", "hellas", "yamato", "nordheim",
                         "tianxia", "nova", "new kemet", "world council", "harmony", "royalty", "steam"]:
                head = re.sub(r"\b" + word + r"\b", lambda m: m.group(0).title(), head)
            out.append("### " + head)
        else:
            out.append(s)
    out.append("")
    out.append("---")
    out.append("")
with open(os.path.join(OUT, "CHANGELOG.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out[:-2]) + "\n")

# Ready-to-install release archive: the mod without its C# sources.
mod = os.path.join(SRC, "HeirsOfEarth")
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(mod):
        rel = os.path.relpath(root, mod)
        if rel.split(os.sep)[0] == "Source":
            continue
        for f in files:
            full = os.path.join(root, f)
            z.write(full, os.path.join("HeirsOfEarth", os.path.relpath(full, mod)))

total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) if ".git" not in r for f in fs)
count = sum(len(fs) for r, _, fs in os.walk(OUT) if ".git" not in r)
print(f"staged {count} files, {total / 1e6:.1f} MB; zip {os.path.getsize(ZIP) / 1e6:.1f} MB")
