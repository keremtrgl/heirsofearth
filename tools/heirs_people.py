"""Nation framework: factions, names, pawn kinds, backstories, traders, archive and start scenario.

nation_people(nation_key, nation_def, spec) writes everything one nation needs to exist in a world.
"""
from heirs_data import add, key, tex
from heirs_kit import N, culture
from heirs_names_more import EXTRA as EXTRA_NAMES
from heirs_names_more2 import EXTRA2 as EXTRA_NAMES2
from heirs_names_last import LAST as LAST_NAMES
from heirs_xml import Def, Raw, T

def BS(key, slot, title, short, desc, skills, disables=None, requires=None, body=None):
    return {"key": key, "slot": slot, "title": title, "short": short, "desc": desc, "skills": skills,
            "disables": disables, "requires": requires, "body": body}


POINTS_CURVE = {"points": ["(0,35)", "(70,50)", "(700,100)", "(1300,150)", "(100000,10000)"]}


def _names(nation, spec):
    f = f"Nations/HE_Names_{nation}.xml"
    def pack(name, firsts, lasts, extra=()):
        rules = ["r_name(p=3)->[first] [last]"] + list(extra)
        rules += [f"first->{x}" for x in firsts] + [f"last->{x}" for x in lasts]
        add(f, Def("RulePackDef", name, rulePack={"rulesStrings": rules}))
        return name
    nick = [f"r_name->[first] '[nick]' [last]"] + [f"nick->{x}" for x in spec.get("nicks", [])] if spec.get("nicks") else []
    more = EXTRA_NAMES.get(nation, {})
    more2 = EXTRA_NAMES2.get(nation, {})
    # A first name must be one word: RimWorld reads "A B C" as first "A" and last "B C". Two-part names are hyphenated.
    males = list(dict.fromkeys(x.replace(" ", "-") for x in spec["male"] + more.get("male", []) + more2.get("male", [])))
    females = list(dict.fromkeys(x.replace(" ", "-") for x in spec["female"] + more.get("female", []) + more2.get("female", [])))
    # 4.2.1: family names. A family name that is also one of the nation's first names would share its short name, so it is dropped.
    fam = LAST_NAMES.get(nation, {})
    firsts = set(males) | set(females)
    def lasts_of(*lists):
        out = list(dict.fromkeys(x for xs in lists for x in xs if x not in firsts))
        assert len(out) >= 40, f"{nation}: only {len(out)} family names"
        return out
    male_last = lasts_of(spec["last"], fam.get("last", []))
    if fam.get("female_replace"):
        female_last = lasts_of(fam["last_female"])
    elif "last_female" in spec:
        female_last = lasts_of(spec["last_female"], fam.get("last_female", fam.get("last", [])))
    else:
        female_last = male_last
    male = pack(f"HE_Names_{nation}_Male", males, male_last, nick)
    female = pack(f"HE_Names_{nation}_Female", females, female_last, nick)
    town = f"HE_Names_{nation}_Settlement"
    rules = [f"r_name->{x}" for x in spec["towns"]]
    if spec.get("town_parts"):
        a, b = spec["town_parts"]
        rules += ["r_name(p=2)->[ta][tb]"] + [f"ta->{x}" for x in a] + [f"tb->{x}" for x in b]
    add(f, Def("RulePackDef", town, rulePack={"rulesStrings": rules}))
    return male, female, town


# Each nation's signature clothes: (everyday garment, body armour, helmet). 3.0.1: pawns are dressed from these instead of
# the shared vanilla tags, which had given heir soldiers cowboy hats, parkas and the armour of other nations.
KITS = {
    "Roma": ("HE_Roma_Tunica", "HE_Roma_Lorica", "HE_Roma_Galea"),
    "Yamato": ("HE_Yamato_Kimono", "HE_Yamato_Domaru", "HE_Yamato_Kabuto"),
    "Nord": ("HE_Nord_Tunic", "HE_Nord_Byrnie", "HE_Nord_Helm"),
    "Hellas": ("HE_Hellas_Chiton", "HE_Hellas_Linothorax", "HE_Hellas_Corinthian"),
    "Tianxia": ("HE_Tianxia_Hanfu", "HE_Tianxia_Lamellar", "HE_Tianxia_Helmet"),
    "Albion": ("Apparel_CollarShirt", "HE_Albion_Redcoat", "HE_Albion_Shako"),
    "Kemet": ("HE_Kemet_Kalasiris", "HE_Kemet_Corselet", "HE_Kemet_Khepresh"),
    "Pars": ("HE_Pars_Kaftan", "HE_Pars_ScaleCoat", "HE_Pars_WingedHelm"),
    "Inti": ("HE_Inti_Unku", "HE_Inti_QuiltedTunic", "HE_Inti_PlumedHelm"),
}
# Shared vanilla tags that let other kits in; plain shirts and trousers come back through HE_Base (Patches/HE_BaseClothes.xml).
FOREIGN_TAGS = {"IndustrialBasic", "MedievalMilitary", "IndustrialMilitaryBasic", "Western", "Neolithic"}


START_SUPPLIES = {"Pemmican", "RawRice", "MealSurvivalPack", "MedicineHerbal", "MedicineIndustrial"}


def _kit(nation, tags, required=None, fighter=False, money="0~0", headgear=0.0):
    """Apparel tags without the shared vanilla tags, and the nation clothes a kind always wears."""
    garment, armour, helm = KITS[nation]
    low = float(str(money).split("~")[0])
    tags = ["HE_Base"] + [t for t in tags if t not in FOREIGN_TAGS and t != "HE_Base"]
    need = list(required or [])
    if garment:
        need.append(garment)
    if (fighter and low >= 450) or low >= 1000:
        need.append(armour)
    if fighter and headgear >= 0.6:
        need.append(helm)
    return tags, list(dict.fromkeys(need)) or None


def _kinds(nation, spec, faction, male, female, player):
    f = f"Nations/HE_People_{nation}.xml"
    base = f"HE_{nation}_KindBase"
    add(f, Def("PawnKindDef", None, abstract_name=base, abstract=True,
               race="Human", defaultFactionDef=faction, chemicalAddictionChance=0.02, backstoryCryptosleepCommonality=0,
               invNutrition=2.5, initialResistanceRange="10~18", initialWillRange="1~3",
               nameMaker=male, nameMakerFemale=female,
               backstoryFiltersOverride=[{"categories": [f"HE_{nation}"]}]))
    colonist = f"HE_{nation}_Colonist"
    ctags, creq = _kit(nation, [f"HE_{nation}Apparel"])
    add(f, Def("PawnKindDef", colonist, parent="BasePlayerPawnKind", label=T("colonist", "kolonist"),
               defaultFactionDef=player, nameMaker=male, nameMakerFemale=female, chemicalAddictionChance=0.02,
               apparelTags=ctags, apparelRequired=creq, apparelAllowHeadgearChance=0, apparelMoney="350~600",
               backstoryCryptosleepCommonality=0, initialResistanceRange="13~21"))
    names = {"Colonist": colonist}
    for k in spec["kinds"]:
        name = f"HE_{nation}_{k['key']}"
        names[k["key"]] = name
        atags, areq = _kit(nation, k["apparel"], k.get("required"), k.get("fighter", True), k["amoney"], k.get("headgear", 0.6))
        fields = dict(label=T(*k["label"]), combatPower=k["power"], isFighter=k.get("fighter", True),
                      itemQuality=k.get("quality"), gearHealthRange=k.get("gear", "0.7~1.6"),
                      weaponTags=k["weapons"], weaponMoney=k["wmoney"], apparelTags=atags, apparelMoney=k["amoney"],
                      apparelAllowHeadgearChance=k.get("headgear", 0.6), apparelRequired=areq,
                      factionLeader=k.get("leader"), trader=k.get("trader"), minGenerationAge=k.get("min_age"), maxGenerationAge=k.get("max_age"),
                      skills=k.get("skills"))
        if k.get("plural"):
            fields["labelPlural"] = T(*k["plural"])
        add(f, Def("PawnKindDef", name, parent=base, **fields))
    return names


def _backstories(nation, spec):
    f = f"Nations/HE_Backstories_{nation}.xml"
    out = []
    for b in spec["backstories"]:
        name = f"HE_{nation}_BS_{b['key']}"
        out.append(name)
        add(f, Def("BackstoryDef", name,
                   title=T(*b["title"]), titleShort=T(*b["short"]),
                   description=T(*b["desc"]),
                   slot=b["slot"], spawnCategories=[f"HE_{nation}"],
                   skillGains=b.get("skills"), workDisables=b.get("disables"), requiredWorkTags=b.get("requires"),
                   bodyTypeGlobal=b.get("body"),
                   bodyTypeMale=None if b.get("body") or b["slot"] != "Adulthood" else "Male",
                   bodyTypeFemale=None if b.get("body") or b["slot"] != "Adulthood" else "Female",
                   modExtensions=[culture(nation)]))
    return out


def _traders(nation, spec, goods_tag, archive):
    f = f"Nations/HE_Traders_{nation}.xml"
    common = [
        {"@Class": "StockGenerator_SingleDef", "thingDef": "Silver", "countRange": "600~1100"},
        {"@Class": "StockGenerator_SingleDef", "thingDef": archive, "countRange": "1~2"},
        {"@Class": "StockGenerator_Tag", "tradeTag": goods_tag, "thingDefCountRange": "3~6", "countRange": "1~3"},
        {"@Class": "StockGenerator_SingleDef", "thingDef": "MedicineHerbal", "countRange": "5~12"},
        {"@Class": "StockGenerator_BuyExpensiveSimple"},
        {"@Class": "StockGenerator_BuyTradeTag", "tag": "Art"},
    ]
    caravan = f"HE_{nation}_Caravan"
    add(f, Def("TraderKindDef", caravan, label=T(*spec["caravan"]), commonality=1,
               stockGenerators=common + [
                   {"@Class": "StockGenerator_Category", "categoryDef": "WeaponsMelee", "thingDefCountRange": "2~4", "countRange": "1~1"},
                   {"@Class": "StockGenerator_Category", "categoryDef": "Textiles", "thingDefCountRange": "1~2", "countRange": "40~90"},
                   {"@Class": "StockGenerator_SingleDef", "thingDef": "Pemmican", "countRange": "30~60"},
               ]))
    base = f"HE_{nation}_Settlement"
    add(f, Def("TraderKindDef", base, label=T(*spec["settlement"]), commonality=1,
               stockGenerators=common + [
                   {"@Class": "StockGenerator_SingleDef", "thingDef": archive, "countRange": "1~3"},
                   {"@Class": "StockGenerator_Category", "categoryDef": "WeaponsMelee", "thingDefCountRange": "3~6", "countRange": "1~1"},
                   {"@Class": "StockGenerator_Category", "categoryDef": "Apparel", "thingDefCountRange": "4~8", "countRange": "1~1"},
                   {"@Class": "StockGenerator_Category", "categoryDef": "ResourcesRaw", "thingDefCountRange": "2~4", "countRange": "50~150"},
                   {"@Class": "StockGenerator_Category", "categoryDef": "FoodMeals", "thingDefCountRange": "1~2", "countRange": "8~20"},
                   {"@Class": "StockGenerator_Animals", "maxWildness": 0.6, "tradeTagsSell": ["AnimalFarm", "AnimalPet"],
                    "tradeTagsBuy": ["AnimalUncommon", "AnimalExotic"], "kindCountRange": "1~3", "countRange": "2~5"},
               ]))
    return caravan, base


def _archive(nation, spec, goods_tag):
    name = f"HE_{nation}_Archive"
    add(f"Things/HE_Goods_{nation}.xml", Def("ThingDef", name, parent="ResourceBase",
        label=T(*spec["archive"]), description=T(*spec["archive_desc"]),
        graphicData={"texPath": f"HeirsOfEarth/Items/{name}", "graphicClass": "Graphic_Single"},
        stackLimit=10, healthAffectsPrice=False,
        statBases={"MaxHitPoints": 60, "MarketValue": 220, "Mass": 0.6, "Flammability": 1.0, "DeteriorationRate": 2},
        thingCategories=["Manufactured"], tradeTags=[goods_tag],
        modExtensions=[culture(nation, 25)]))
    tex(f"HeirsOfEarth/Items/{name}", "archive", color=spec["color_hex"], emblem=spec["emblem"])
    return name


def nation_people(nation, nation_def, spec):
    """spec keys: color, color_hex, emblem, fixed, singular, plural, leader, desc, male, female, last, towns,
    kinds, backstories, caravan, settlement, archive, archive_desc, start, start_desc, start_summary, start_gear."""
    goods = f"HE_{nation}Goods"
    male, female, town = _names(nation, spec)
    faction = f"HE_Faction_{nation}"
    player = f"HE_Player_{nation}"
    archive = _archive(nation, spec, goods)
    kinds = _kinds(nation, spec, faction, male, female, player)
    _backstories(nation, spec)
    caravan, base = _traders(nation, spec, goods, archive)
    k = {x["key"]: kinds[x["key"]] for x in spec["kinds"]}
    roles = spec["roles"]
    fighters = {k[x]: w for x, w in roles["combat"].items()}
    add(f"Nations/HE_Factions_{nation}.xml", Def("FactionDef", faction, parent="FactionBase",
        label=T(*spec["fixed"]), description=T(*spec["desc"]), fixedName=T(*spec["fixed"]),
        pawnSingular=T(*spec["singular"]), pawnsPlural=T(*spec["plural"]), leaderTitle=T(*spec["leader"]),
        categoryTag=f"HE_{nation}", listOrderPriority=32, settlementGenerationWeight=1, requiredCountAtGameStart=1,
        maxConfigurableAtWorldCreation=3, configurationListOrderPriority=60, canSiege=True, canStageAttacks=True,
        humanlikeFaction=True, techLevel=spec.get("tech", "Medieval"),
        basicMemberKind=k[roles["basic"]],
        fixedLeaderKinds=[k[x["key"]] for x in spec["kinds"] if x.get("leader")],
        factionIconPath=f"HeirsOfEarth/UI/HE_{nation}", settlementTexturePath=f"HeirsOfEarth/World/HE_Settlement_{nation}",
        colorSpectrum=spec["spectrum"], settlementNameMaker=town,
        backstoryFilters=[{"categories": [f"HE_{nation}"], "commonality": 1}],
        caravanTraderKinds=[caravan], visitorTraderKinds=[caravan], baseTraderKinds=[base],
        allowedArrivalTemperatureRange=spec.get("temps", "-40~45"), raidLootMaker="OutlanderRaidLootMaker",
        maxPawnCostPerTotalPointsCurve=POINTS_CURVE, earliestRaidDays=spec.get("raid_days", 30),
        pawnGroupMakers=[
            {"kindDef": "Combat", "options": fighters},
            {"kindDef": "Peaceful", "options": {k[x]: w for x, w in roles["peaceful"].items()}},
            {"kindDef": "Trader", "traders": {k[roles["trader"]]: 1}, "carriers": {"Muffalo": 6, "Dromedary": 4},
             "guards": {k[x]: w for x, w in roles["guards"].items()}},
            {"kindDef": "Settlement", "options": {**{k[x]: w for x, w in roles["settlement"].items()}, **{k[x["key"]]: 1 for x in spec["kinds"] if x.get("leader")}}},
        ]))
    add(f"Nations/HE_Factions_{nation}.xml", Def("FactionDef", player, parent="PlayerFactionBase",
        label=T(*spec["player_label"]), description=T(*spec["player_desc"]), isPlayer=True,
        basicMemberKind=kinds["Colonist"], pawnSingular=T("colonist", "kolonist"), pawnsPlural=T("colonists", "kolonistler"),
        techLevel=spec.get("tech", "Medieval"), factionNameMaker="NamerFactionOutlander", settlementNameMaker=town,
        backstoryFilters=[{"categories": [f"HE_{nation}"], "commonality": 0.85}, {"categories": ["Offworld"], "commonality": 0.15}],
        factionIconPath=f"HeirsOfEarth/UI/HE_{nation}",
        startingResearchTags=spec.get("research_tags", ["TribalStart"]),
        colorSpectrum=[spec["spectrum"][0]]))
    scen = f"HE_Start_{nation}"
    key(f"HE_Start{nation}Dialog", *spec["start_dialog"])
    parts = [
        {"@Class": "ScenPart_ConfigPage_ConfigureStartingPawns", "def": "ConfigPage_ConfigureStartingPawns", "pawnCount": 5, "pawnChoiceCount": 10},
        {"@Class": "ScenPart_PlayerPawnsArriveMethod", "def": "PlayerPawnsArriveMethod", "method": "Standing", "visible": False},
        {"@Class": "HeirsOfEarth.ScenPart_HeirsHeritage", "def": "HE_Heritage", "nation": N(nation)},
    ]
    for thing, count, stuff in spec["start_gear"]:
        if thing in START_SUPPLIES:
            count = int(round(count * 5 / 3 / 5.0)) * 5  # five settlers instead of three: food and medicine scale with them
        parts.append({"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": thing, "count": count, "stuff": stuff})
    parts += [
        {"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": archive, "count": 1},
        {"@Class": "ScenPart_StartingAnimal", "def": "StartingAnimal", "count": 1, "bondToRandomPlayerPawnChance": 0.5},
        {"@Class": "ScenPart_ScatterThingsNearPlayerStart", "def": "ScatterThingsNearPlayerStart", "thingDef": "WoodLog", "count": 300},
        {"@Class": "ScenPart_ScatterThingsNearPlayerStart", "def": "ScatterThingsNearPlayerStart", "thingDef": "Steel", "count": 250},
        {"@Class": "ScenPart_GameStartDialog", "def": "GameStartDialog", "textKey": f"HE_Start{nation}Dialog", "closeSound": "GameStartSting"},
    ]
    add(f"Nations/HE_Factions_{nation}.xml", Def("ScenarioDef", scen, parent="ScenarioBase",
        label=T(*spec["start"]), description=T(*spec["start_desc"]),
        scenario={"summary": T(*spec["start_summary"]), "playerFaction": {"def": "PlayerFaction", "factionDef": player}, "parts": parts}))
    nation_def.fields.update(faction=faction, playerFaction=player, scenario=scen, archive=archive)
    return {"faction": faction, "player": player, "kinds": k, "archive": archive, "scenario": scen, "goods": goods}
