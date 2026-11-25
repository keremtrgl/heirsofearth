"""Heirs of Earth 3.1 balance report.

Compares every heir weapon, apparel, food and building with vanilla Core things of the same tech level (median and best)
and writes docs/heirs_balance.md. Flags:
  weapons    DPS below 0.6x the vanilla median or above 1.25x the vanilla best (artifacts excluded)
  apparel    sharp armour above 1.25x the best vanilla piece of the same layer and tech, or market value off by 3x
  food       nutrition per silver off the vanilla median by 2x
  buildings  market value off the vanilla median for the same tech by 4x
It also prints the per-nation content counts so gaps between nations stay visible.
Usage: python -I tools/heirs_balance.py   (exit 1 if anything is flagged)
"""
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heirs_check as hc  # noqa: E402

OUT = os.path.join(os.path.dirname(hc.HERE), "docs", "heirs_balance.md")
NATIONS = ("Roma", "Yamato", "Nord", "Hellas", "Tianxia", "Albion", "Kemet", "Pars", "Inti")


def stats(el, abstract):
    """statBases merged down the parent chain, child values winning."""
    chain, seen = [], 0
    while el is not None and seen < 20:
        chain.append(el)
        el = abstract.get(el.get("ParentName"))
        seen += 1
    out = {}
    for e in reversed(chain):
        sb = e.find("statBases")
        if sb is not None:
            for s in sb:
                try:
                    out[s.tag] = float(s.text)
                except (TypeError, ValueError):
                    pass
    return out


def child(el, abstract, path):
    """First match of a nested path (a/b) down the parent chain."""
    seen = 0
    while el is not None and seen < 20:
        x = el.find(path)
        if x is not None:
            return x
        el = abstract.get(el.get("ParentName"))
        seen += 1
    return None


def kind_of(el, abstract):
    if child(el, abstract, "apparel") is not None:
        return "apparel"
    if child(el, abstract, "ingestible") is not None:
        return "food"
    if (hc.text(el, "category") or (child(el, abstract, "category").text if child(el, abstract, "category") is not None else "")) == "Building" \
            or child(el, abstract, "building") is not None:
        return "building"
    if hc.inherited(el, "verbs", abstract) is not None and el.find("verbs") is not None:
        return "ranged"
    if el.find("tools") is not None and "Weapon" in (el.get("ParentName") or ""):
        return "melee"
    return None


def layer(el, abstract):
    """Apparel slot: head (Overhead), body armour (any Middle layer, as vanilla plate armour), or clothes."""
    layers = child(el, abstract, "apparel/layers")
    names = [li.text for li in layers.findall("li")] if layers is not None else []
    if "Overhead" in names:
        return "head"
    if "Middle" in names:
        return "body armour"
    return "clothes"


def armour(s, el=None, abstract=None):
    """Stuffed apparel is rated by its stuff multiplier (fabric and metal apart, since hyperweave makes a fabric multiplier
    worth far more), the rest by flat sharp armour; they are compared only within kind."""
    if "StuffEffectMultiplierArmor" in s:
        cats = child(el, abstract, "stuffCategories") if el is not None else None
        names = {li.text for li in cats.findall("li")} if cats is not None else set()
        kind = "fabric" if names and names <= {"Fabric", "Leathery"} else "metal"
        return "stuff-" + kind, s["StuffEffectMultiplierArmor"]
    return "flat", s.get("ArmorRating_Sharp", 0.0)


def nation_of(name):
    for n in NATIONS:
        if name.startswith(f"HE_{n}_"):
            return n
    return "Shared"


def main():
    core = hc.load(hc.CORE)
    ours = hc.load(os.path.join(hc.MOD, "Defs"))
    core_by, core_abs = hc.resolve(core)
    our_by, our_abs = hc.resolve(ours)
    abstract = dict(core_abs)
    abstract.update(our_abs)
    by_name = dict(core_by)
    by_name.update(our_by)

    def things(defs):
        for el, _ in defs:
            if el.tag == "ThingDef" and el.get("Abstract") != "True" and hc.text(el, "defName"):
                yield el

    def dps(el, k):
        return hc.ranged_dps(el, abstract, by_name) if k == "ranged" else hc.melee_dps(el.find("tools") if el.find("tools") is not None else hc.inherited(el, "tools", abstract))

    # vanilla pools
    v = defaultdict(list)
    for el in things(core):
        k = kind_of(el, abstract)
        if k is None:
            continue
        lvl = hc.tech(el, abstract)
        s = stats(el, abstract)
        if k in ("ranged", "melee"):
            cats = hc.inherited(el, "thingCategories", abstract)
            if cats is None or not any("Weapons" in (li.text or "") for li in cats.findall("li")):
                continue
            if k == "ranged" and hc.HEAVY_TAGS & hc.weapon_tags(el, abstract):
                continue
            d = dps(el, k)
            if d > 0:
                v[(k, lvl)].append(d)
        elif k == "apparel":
            mode, value = armour(s, el, abstract)
            v[("armour", mode, layer(el, abstract))].append(value)
            if s.get("WorkToMake"):
                v[("apparel_work", layer(el, abstract))].append(s["WorkToMake"])
        elif k == "food":
            nut, val = s.get("Nutrition", 0.0), s.get("MarketValue", 0.0)
            if nut > 0 and val > 0 and child(el, abstract, "ingestible/foodType") is not None:
                v["food"].append(nut / val)
        elif k == "building" and s.get("MarketValue"):
            v[("building", lvl)].append(s["MarketValue"])

    # strongest vanilla stuff per category, to rate stuffed apparel at its best (hyperweave, plasteel...)
    stuff_best = defaultdict(float)
    for el in things(core):
        props = child(el, abstract, "stuffProps/categories")
        power = stats(el, abstract).get("StuffPower_Armor_Sharp")
        if props is not None and power:
            for li in props.findall("li"):
                stuff_best[li.text] = max(stuff_best[li.text], power)

    def effective(el, mult):
        cats = child(el, abstract, "stuffCategories")
        names = [li.text for li in cats.findall("li")] if cats is not None else []
        return mult * max((stuff_best.get(c, 0.0) for c in names), default=0.0)

    v_eff = defaultdict(float)
    for el in things(core):
        if kind_of(el, abstract) == "apparel":
            s0 = stats(el, abstract)
            eff = effective(el, s0["StuffEffectMultiplierArmor"]) if "StuffEffectMultiplierArmor" in s0 else s0.get("ArmorRating_Sharp", 0.0)
            v_eff[layer(el, abstract)] = max(v_eff[layer(el, abstract)], eff)

    def med(key):
        pool = v.get(key) or []
        return statistics.median(pool) if pool else 0.0

    def best(key):
        pool = v.get(key) or []
        return max(pool) if pool else 0.0

    rows, flags = defaultdict(list), []
    counts = defaultdict(lambda: defaultdict(int))
    for el in things(ours):
        n = hc.text(el, "defName")
        k = kind_of(el, abstract)
        nation = nation_of(n)
        if k is None:
            cat = child(el, abstract, "category")
            if n.startswith("HE_") and cat is not None and cat.text == "Item":
                counts[nation]["items"] += 1
            continue
        lvl = hc.tech(el, abstract)
        s = stats(el, abstract)
        artifact = "_Artifact_" in n
        if k in ("ranged", "melee"):
            turret = "TurretGun" in hc.weapon_tags(el, abstract)
            if turret:
                continue
            counts[nation]["weapons"] += 1
            d = dps(el, k)
            pool_lvl = lvl if v.get((k, lvl)) else "Medieval"
            m, b = med((k, pool_lvl)), best((k, pool_lvl))
            note = ""
            if not artifact and m and d < 0.6 * m:
                note = "weak"
            if not artifact and b and d > 1.25 * b:
                note = "strong"
            rows["Weapons"].append((n, lvl, k, f"{d:.2f}", f"{m:.2f}", f"{b:.2f}", f"{d / m:.2f}" if m else "-", note))
            if note:
                flags.append(f"{n}: {k} DPS {d:.2f} is {note} (vanilla {pool_lvl} median {m:.2f}, best {b:.2f})")
        elif k == "apparel":
            counts[nation]["apparel"] += 1
            lay = layer(el, abstract)
            mode, val = armour(s, el, abstract)
            b = best(("armour", mode, lay))
            work, vw = s.get("WorkToMake", 0.0), med(("apparel_work", lay))
            eff = effective(el, val) if mode != "flat" else val
            cap = v_eff.get(lay, 0.0)
            note = ""
            if mode == "flat" and b and val > 1.25 * b:
                note = "armour high"
            if cap and eff > 1.05 * cap:
                note = (note + ", " if note else "") + f"best-stuff sharp {eff:.2f} > vanilla {cap:.2f}"
            if work and vw and not (vw / 3 <= work <= vw * 3):
                note = (note + ", " if note else "") + "work"
            rows["Apparel"].append((n, lvl, lay, f"{mode} {val:.2f}", f"{eff:.2f} / {cap:.2f}", f"{b:.2f}", f"{work:.0f}", f"{vw:.0f}", note))
            if note:
                flags.append(f"{n}: apparel {note} ({mode} {val:.2f} vs vanilla best {b:.2f}; work {work:.0f} vs median {vw:.0f})")
        elif k == "food":
            counts[nation]["food"] += 1
            nut, val = s.get("Nutrition", 0.0), s.get("MarketValue", 0.0)
            ratio = nut / val if nut and val else 0.0
            m = med("food")
            note = "" if not (ratio and m) or m / 2 <= ratio <= m * 2 else "nutrition/value"
            rows["Food"].append((n, lvl, "food", f"{nut:.2f}", f"{val:.1f}", f"{ratio:.3f}", f"{m:.3f}", note))
            if note:
                flags.append(f"{n}: nutrition per silver {ratio:.3f} vs vanilla median {m:.3f}")
        elif k == "building":
            counts[nation]["buildings"] += 1
            mv = s.get("MarketValue", 0.0)
            m = med(("building", lvl)) or med(("building", "Medieval"))
            note = "" if not (mv and m) or m / 4 <= mv <= m * 4 else "value"
            rows["Buildings"].append((n, lvl, "building", f"{mv:.0f}", f"{m:.0f}", f"{s.get('Beauty', 0):.0f}", f"{s.get('WorkToBuild', 0):.0f}", note))
            if note:
                flags.append(f"{n}: building value {mv:.0f} vs vanilla {lvl} median {m:.0f}")
    for el, _ in ours:
        n = hc.text(el, "defName") or ""
        if el.tag == "TerrainDef":
            counts[nation_of(n)]["floors"] += 1
        elif el.tag == "ResearchProjectDef":
            counts[nation_of(n)]["research"] += 1

    heads = {
        "Weapons": ("def", "tech", "kind", "DPS", "vanilla median", "vanilla best", "x median", "flag"),
        "Apparel": ("def", "tech", "slot", "armour", "best-stuff sharp / vanilla best", "vanilla best (same kind and slot)", "work", "vanilla median work (slot)", "flag"),
        "Food": ("def", "tech", "", "nutrition", "value", "nutrition/silver", "vanilla median", "flag"),
        "Buildings": ("def", "tech", "", "value", "vanilla median", "beauty", "work", "flag"),
    }
    lines = ["# Heirs of Earth balance report", "",
             "Generated by `tools/heirs_balance.py` from the built Defs and the vanilla Core Defs. "
             "Every heir thing is compared with vanilla things of the same tech level.", "",
             f"Flags: **{len(flags)}**", ""]
    for f in flags:
        lines.append(f"- {f}")
    lines += ["", "## Content per nation", "", "| nation | research | weapons | apparel | buildings | food | floors | items |", "|---|---|---|---|---|---|---|---|"]
    for n in NATIONS + ("Shared",):
        c = counts[n]
        lines.append(f"| {n} | {c['research']} | {c['weapons']} | {c['apparel']} | {c['buildings']} | {c['food']} | {c['floors']} | {c['items']} |")
    for section, data in rows.items():
        lines += ["", f"## {section}", "", "| " + " | ".join(heads[section]) + " |", "|" + "---|" * len(heads[section])]
        for r in sorted(data):
            lines.append("| " + " | ".join(r) + " |")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"balance report: {OUT}")
    print(f"flags: {len(flags)}")
    for f in flags:
        print("  " + f)
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
