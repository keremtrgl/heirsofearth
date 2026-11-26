"""Heirs of Earth balance table and sanity checks.

Reads the generated Defs and vanilla Core Defs, prints a balance table and exits 1 on:
duplicate defNames, missing texture files, defs without a Turkish label, melee DPS above 1.25x the best
vanilla weapon of the same tech level, ranged DPS above 1.25x (heavy and advanced guns excluded; turrets against
the median vanilla turret), research cost outside 0.5x-3x of the
vanilla median for the same tech level.
"""
import glob
import os
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(os.path.dirname(HERE), "HeirsOfEarth")
CORE = r"C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Data\Core\Defs"
TURKISH = os.path.join(MOD, "Languages", "Turkish (Türkçe)", "DefInjected")
TEX = os.path.join(MOD, "Textures")

problems = []


def load(folder):
    defs = []
    for path in glob.glob(os.path.join(folder, "**", "*.xml"), recursive=True):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as e:
            problems.append(f"XML error {path}: {e}")
            continue
        for el in root:
            defs.append((el, path))
    return defs


def text(el, tag, default=None):
    x = el.find(tag)
    return x.text.strip() if x is not None and x.text else default


def resolve(defs):
    """Returns {defName: element} plus abstract parents so techLevel and tools can be inherited."""
    by_name, abstract = {}, {}
    for el, _ in defs:
        if el.get("Name"):
            abstract[el.get("Name")] = el
        n = text(el, "defName")
        if n:
            by_name[n] = el
    return by_name, abstract


def inherited(el, tag, abstract):
    seen = 0
    while el is not None and seen < 20:
        v = el.find(tag)
        if v is not None:
            return v
        el = abstract.get(el.get("ParentName"))
        seen += 1
    return None


def melee_dps(tools):
    best = 0.0
    for li in tools.findall("li"):
        power, cd = float(text(li, "power", 0)), float(text(li, "cooldownTime", 1))
        best = max(best, power / max(cd, 0.1))
    return best


def burst_of(el, abstract):
    verbs = inherited(el, "verbs", abstract)
    v = verbs.find("li") if verbs is not None else None
    return int(text(v, "burstShotCount", 1)) if v is not None else 1


def ranged_dps(el, abstract, by_name):
    verbs = inherited(el, "verbs", abstract)
    if verbs is None:
        return 0.0
    v = verbs.find("li")
    if v is None:
        return 0.0
    proj = by_name.get(text(v, "defaultProjectile", ""))
    if proj is None:
        return 0.0
    pr = inherited(proj, "projectile", abstract)
    dmg = float(text(pr, "damageAmountBase", 0)) if pr is not None else 0.0
    burst = int(text(v, "burstShotCount", 1))
    warm = float(text(v, "warmupTime", 1))
    stats = inherited(el, "statBases", abstract)
    cool = float(text(stats, "RangedWeapon_Cooldown", 1)) if stats is not None else 1.0
    return dmg * burst / max(warm + cool, 0.1)


# Vanilla guns that are a class of their own (minigun, LMG, assault rifle...) are not the yardstick for a nation's line weapon.
HEAVY_TAGS = {"GunHeavy", "IndustrialGunAdvanced", "Minigun"}


def weapon_tags(el, abstract):
    tags = inherited(el, "weaponTags", abstract)
    return {li.text for li in tags.findall("li")} if tags is not None else set()


def tech(el, abstract):
    t = inherited(el, "techLevel", abstract)
    return t.text.strip() if t is not None and t.text else "Undefined"


def main():
    core = load(CORE)
    ours = load(os.path.join(MOD, "Defs"))
    core_by, core_abs = resolve(core)
    our_by, our_abs = resolve(ours)
    abstract = dict(core_abs)
    abstract.update(our_abs)
    by_name = dict(core_by)
    by_name.update(our_by)

    # duplicates
    seen = defaultdict(list)
    for el, path in ours:
        n = text(el, "defName")
        if n:
            seen[(el.tag, n)].append(os.path.basename(path))
    for (tag, n), files in seen.items():
        if len(files) > 1:
            problems.append(f"duplicate {tag} {n} in {files}")

    # textures
    for el, path in ours:
        for tag in ("texPath", "texturePath", "iconPath", "expandingIconTexture", "uiIconPath"):
            for x in el.iter(tag):
                p = (x.text or "").strip()
                if p.startswith("HeirsOfEarth/") and not os.path.exists(os.path.join(TEX, p + ".png")):
                    problems.append(f"{text(el, 'defName')}: missing texture {p}")

    # Turkish labels
    injected = set()
    for path in glob.glob(os.path.join(TURKISH, "**", "*.xml"), recursive=True):
        for el in ET.parse(path).getroot():
            injected.add(el.tag)
    for el, _ in ours:
        n = text(el, "defName")
        if n and el.find("label") is not None and f"{n}.label" not in injected:
            problems.append(f"{n}: no Turkish label")

    # vanilla reference tables
    v_melee, v_ranged, v_research = defaultdict(float), defaultdict(float), defaultdict(list)
    v_heavy = defaultdict(float)
    for el, _ in core:
        if el.tag == "ThingDef" and el.get("Abstract") != "True" and text(el, "defName"):
            cats = inherited(el, "thingCategories", abstract)
            is_weapon = cats is not None and any("Weapons" in (li.text or "") for li in cats.findall("li"))
            if not is_weapon:
                continue
            lvl = tech(el, abstract)
            if inherited(el, "verbs", abstract) is not None:
                if not HEAVY_TAGS & weapon_tags(el, abstract):
                    v_ranged[lvl] = max(v_ranged[lvl], ranged_dps(el, abstract, by_name))
                else:
                    v_heavy[lvl] = max(v_heavy[lvl], ranged_dps(el, abstract, by_name))
            else:
                tools = inherited(el, "tools", abstract)
                if tools is not None:
                    v_melee[lvl] = max(v_melee[lvl], melee_dps(tools))
        elif el.tag == "ResearchProjectDef" and text(el, "baseCost"):
            v_research[tech(el, abstract)].append(float(text(el, "baseCost")))
    turret_dps = sorted(d for d in (ranged_dps(el, abstract, by_name) for el, _ in core
                                    if el.tag == "ThingDef" and el.get("Abstract") != "True" and "TurretGun" in weapon_tags(el, abstract))
                        if 0 < d < 1000)
    v_turret = turret_dps[len(turret_dps) // 2] if turret_dps else 0.0

    print(f"{'def':34} {'tech':11} {'kind':8} {'value':>8} {'vanilla':>8} {'ratio':>6}")
    for el, _ in ours:
        n = text(el, "defName")
        if not n:
            continue
        lvl = tech(el, abstract)
        if el.tag == "ThingDef" and el.get("Abstract") != "True":
            if inherited(el, "verbs", abstract) is not None and el.find("verbs") is not None:
                dps = ranged_dps(el, abstract, by_name)
                if "TurretGun" in weapon_tags(el, abstract):
                    ref, kind, lvl = v_turret, "turret", "Turret"
                elif burst_of(el, abstract) >= 5 and v_heavy.get(lvl):
                    # 4.3: a machine gun is measured against the vanilla heavy guns of its age (the light machine gun)
                    ref, kind = v_heavy[lvl], "heavy"
                else:
                    ref, kind = v_ranged.get(lvl) or v_ranged.get("Neolithic", 0), "ranged"
            elif el.find("tools") is not None and "Weapon" in (el.get("ParentName") or ""):
                dps, ref = melee_dps(el.find("tools")), v_melee.get(lvl, 0)
                kind = "melee"
            else:
                continue
            ratio = dps / ref if ref else 0
            print(f"{n:34} {lvl:11} {kind:8} {dps:8.2f} {ref:8.2f} {ratio:6.2f}")
            if ref and ratio > 1.25 and "_Artifact_" not in n:
                problems.append(f"{n}: {kind} DPS {dps:.2f} > 1.25x best vanilla {lvl} {ref:.2f}")
        elif el.tag == "ResearchProjectDef":
            cost = float(text(el, "baseCost", 0))
            pool = v_research.get(lvl) or v_research.get("Medieval")
            med = statistics.median(pool) if pool else 0
            ratio = cost / med if med else 0
            print(f"{n:34} {lvl:11} {'research':8} {cost:8.0f} {med:8.0f} {ratio:6.2f}")
            if med and not 0.5 <= ratio <= 3.0:
                problems.append(f"{n}: research cost {cost:.0f} outside 0.5x-3x of vanilla {lvl} median {med:.0f}")

    counts = defaultdict(int)
    for el, _ in ours:
        if text(el, "defName"):
            counts[el.tag] += 1
    print("counts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print(f"problems: {len(problems)}")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
