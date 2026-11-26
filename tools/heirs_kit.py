"""Heirs of Earth: builders for the def kinds the content modules use."""
from heirs_data import add, tex
from heirs_xml import Def, Raw, T

NATIONS = {
    # key: (defName, English adjective, Turkish adjective)
    "Roma": ("HE_Roma", "Nova Roman", "Nova Roma"),
    "Yamato": ("HE_Yamato", "Yamato", "Yamato"),
    "Nord": ("HE_Nord", "Nordheim", "Nordheim"),
    "Hellas": ("HE_Hellas", "Hellenic", "Hellas"),
    "Tianxia": ("HE_Tianxia", "Tianxia", "Tianxia"),
    "Albion": ("HE_Albion", "Albion", "Albion"),
    "Kemet": ("HE_Kemet", "Kemetic", "Kemet"),
    "Pars": ("HE_Pars", "Parsian", "Pars"),
    "Inti": ("HE_Inti", "Inti", "İnti"),
}
NATION_X = {"Common": 0.0, "Roma": 2.4, "Yamato": 5.6, "Nord": 8.8, "Hellas": 12.0, "Tianxia": 15.2, "Albion": 18.4,
            "Kemet": 21.6, "Pars": 24.8, "Inti": 28.0}
ERA_Y = {"Neolithic": 0.0, "Medieval": 3.6, "Industrial": 7.2}
ROW = 0.72
ENTRY_KNOWLEDGE = 5

TOOL_TR = {"handle": "kabza", "point": "uç", "edge": "ağız", "blade": "ağız", "haft": "sap", "head": "baş", "shaft": "gövde",
           "limb": "kol", "stock": "dipçik", "barrel": "namlu", "bayonet": "süngü", "pommel": "topuz", "spike": "çivi",
           "beard": "sakal", "rim": "kenar", "boss": "umbo", "grip": "kavrama", "guard": "siper", "butt": "dip"}

SMITHY = ["FueledSmithy", "ElectricSmithy"]
TAILOR = ["HandTailoringBench", "ElectricTailoringBench"]
CRAFT = ["CraftingSpot"]
STOVES = ["FueledStove", "ElectricStove"]


def N(nation):
    return NATIONS[nation][0]


def culture(nation, knowledge=None):
    return {"@Class": "HeirsOfEarth.HeirsCultureExt", "nation": N(nation), "knowledge": knowledge}


def tool(label, caps, power, cool, pen=None):
    return {"label": T(label, TOOL_TR[label]), "capacities": caps if isinstance(caps, list) else [caps], "power": power,
            "cooldownTime": cool, "armorPenetration": pen}


def counts(d):
    return {k: v for k, v in d.items()} if d else None


def recipe_maker(research, skill, users=None, order=None, unfinished=None, skill_name="Crafting", extra=None):
    r = {}
    if unfinished:
        r["unfinishedThingDef"] = unfinished
    r["researchPrerequisite"] = research
    r["skillRequirements"] = {skill_name: skill}
    if users:
        r["recipeUsers"] = {"@Inherit": "False", "#items": users}
    if order:
        r["displayPriority"] = order
    if extra:
        r.update(extra)
    return r


# ---------------------------------------------------------------- research
def research(nation, key, en, tr, den, dtr, cost, tech, col, row, prereqs=(), knowledge=0, tradition=False, stats=(),
             quality=0.0, caravan=0.0, study=0.0, chain=None, effect=None, file=None, hidden=()):
    name = f"HE_{nation}_{key}" if nation != "Common" else f"HE_{key}"
    if nation != "Common" and not knowledge:
        # 4.3.1: every foreign project needs some knowledge of its nation (design: "a foreign nation's research cannot be started
        # without enough knowledge"); before, the 46 entry projects with no knowledge set were open to every colony.
        knowledge = ENTRY_KNOWLEDGE
    ext = None
    if nation != "Common" or tradition:
        ext = {"@Class": "HeirsOfEarth.HeirsResearchExt"}
        if nation != "Common":
            ext["nation"] = N(nation)
        if knowledge:
            ext["knowledge"] = knowledge
        if tradition:
            ext["tradition"] = True
        if stats:
            ext["stats"] = [{"stat": s[0], "offset": s[1] if len(s) > 1 and s[1] else None,
                             "factor": s[2] if len(s) > 2 and s[2] != 1 else None,
                             "scope": s[3] if len(s) > 3 else None} for s in stats]
        if quality:
            ext["qualityChance"] = quality
        if caravan:
            ext["caravanSpeed"] = caravan
        if study:
            ext["studyFactor"] = study
        if chain:
            ext["requiresChain"] = chain
    de, dt = den, dtr
    if effect:
        de += "\n\nTradition: " + effect.en
        dt += "\n\nGelenek: " + effect.tr
    if knowledge and nation != "Common":
        _, adj_en, adj_tr = NATIONS[nation]
        de += f"\n\nRequires {knowledge} {adj_en} knowledge unless this is your heritage."
        dt += f"\n\nMirasın bu değilse {knowledge} {adj_tr} bilgisi gerekir."
    if chain:
        de += "\n\nUnlocked by finishing the nation's story."
        dt += "\n\nDevletin hikâyesini bitirince açılır."
    d = Def("ResearchProjectDef", name,
            label=T(en, tr), description=T(de, dt), baseCost=cost, techLevel=tech,
            tab="HE_WorldHeritage",
            researchViewX=round(NATION_X[nation] + col, 2), researchViewY=round(ERA_Y[tech] + row * ROW, 2),
            prerequisites=list(prereqs) or None, hiddenPrerequisites=list(hidden) or None,
            modExtensions=[ext] if ext else None)
    add(file or f"Research/HE_Research_{nation}.xml", d)
    return name


# ---------------------------------------------------------------- weapons
def melee(nation, key, en, tr, den, dtr, tech, research_name, tools, mass, work, painter, stuff=("Metallic",), stuff_count=60,
          cost=None, blunt=False, angle=-65, skill=4, users=None, extra_tags=(), value_factor=None, order=None, knowledge=None, pargs=None):
    name = f"HE_{nation}_{key}"
    parent = "BaseMeleeWeapon_Blunt_Quality" if blunt else "BaseMeleeWeapon_Sharp_Quality"
    stats = {"WorkToMake": work, "Mass": mass}
    if value_factor:
        stats["MarketValue"] = value_factor
    d = Def("ThingDef", name, parent=parent,
            label=T(en, tr), description=T(den, dtr), techLevel=tech,
            graphicData={"texPath": f"HeirsOfEarth/Weapons/{name}", "graphicClass": "Graphic_Single"},
            uiIconScale=1.1, equippedAngleOffset=angle,
            costStuffCount=stuff_count if stuff else None,
            stuffCategories=list(stuff) if stuff else None,
            costList=counts(cost),
            statBases=stats,
            weaponTags={"@Inherit": "False", "#items": [f"HE_{nation}Melee"] + list(extra_tags)},
            tradeTags={"@Inherit": "False", "#items": [f"HE_{nation}Goods", "WeaponMelee"]},
            thingSetMakerTags=["RewardStandardQualitySuper"],
            relicChance=0,
            tools=tools,
            recipeMaker=recipe_maker(research_name, skill, users, order),
            modExtensions=[culture(nation, knowledge)])
    add(f"Things/HE_Weapons_{nation}.xml", d)
    tex(f"HeirsOfEarth/Weapons/{name}", painter, **(pargs or {}))
    return name


def projectile(name, label_en, label_tr, damage, amount, speed, tex_path, pen=None, explosive_radius=None, file="Things/HE_Projectiles.xml"):
    proj = {"damageDef": damage, "damageAmountBase": amount, "speed": speed, "armorPenetrationBase": pen}
    if explosive_radius:
        proj["explosionRadius"] = explosive_radius
    d = Def("ThingDef", name, parent="BaseBullet", label=T(label_en, label_tr),
            thingClass="Projectile_Explosive" if explosive_radius else None,
            graphicData={"texPath": tex_path, "graphicClass": "Graphic_Single"},
            projectile=proj)
    add(file, d)
    return name


def ranged(nation, key, en, tr, den, dtr, tech, research_name, bullet, warmup, rng, cooldown, acc, mass, work, painter, cost,
           sound="Bow_Recurve", interact="Bow_Recurve", burst=1, ticks=None, klass=("Ranged",), users=None, skill=5, gun=False,
           tools=None, extra_tags=(), stuff=None, stuff_count=None, order=None, knowledge=None, forced_miss=None, pargs=None,
           weapon_tags=None):
    name = f"HE_{nation}_{key}"
    parent = "BaseHumanMakeableGun" if gun else "BaseWeaponNeolithic"
    verb = {"verbClass": "Verb_Shoot", "hasStandardCommand": True, "defaultProjectile": bullet, "warmupTime": warmup,
            "range": rng, "soundCast": sound, "burstShotCount": burst if burst > 1 else None,
            "ticksBetweenBurstShots": ticks if burst > 1 else None, "forcedMissRadius": forced_miss}
    if gun:
        verb["soundCastTail"] = "GunTail_Medium"
        verb["muzzleFlashScale"] = 9
    d = Def("ThingDef", name, parent=parent,
            label=T(en, tr), description=T(den, dtr), techLevel=tech,
            graphicData={"texPath": f"HeirsOfEarth/Weapons/{name}", "graphicClass": "Graphic_Single"},
            soundInteract=interact,
            stuffCategories=list(stuff) if stuff else None, costStuffCount=stuff_count,
            costList=counts(cost),
            statBases={"WorkToMake": work, "Mass": mass, "AccuracyTouch": acc[0], "AccuracyShort": acc[1],
                       "AccuracyMedium": acc[2], "AccuracyLong": acc[3], "RangedWeapon_Cooldown": cooldown},
            weaponTags={"@Inherit": "False", "#items": list(weapon_tags) if weapon_tags else [f"HE_{nation}Ranged"] + list(extra_tags)},
            tradeTags={"@Inherit": "False", "#items": [f"HE_{nation}Goods", "WeaponRanged"]},
            weaponClasses=list(klass),
            relicChance=0,
            verbs=[verb],
            tools=tools or [tool("limb" if not gun else "stock", "Blunt", 9, 2)],
            recipeMaker=recipe_maker(research_name, skill, users or (SMITHY if gun else CRAFT), order),
            modExtensions=[culture(nation, knowledge)])
    add(f"Things/HE_Weapons_{nation}.xml", d)
    tex(f"HeirsOfEarth/Weapons/{name}", painter, **(pargs or {}))
    return name


# ---------------------------------------------------------------- apparel
def apparel(nation, key, en, tr, den, dtr, tech, research_name, worn, layers, groups, stats, painter, parent="ApparelMakeableBase",
            stuff=("Fabric", "Leathery"), stuff_count=60, cost=None, work=8000, mass=1.5, users=None, skill=4, head=False,
            tags=(), equipped=None, color=None, order=None, knowledge=None, pargs=None):
    name = f"HE_{nation}_{key}"
    base = {"WorkToMake": work, "Mass": mass, "EquipDelay": 2 if not head else 1}
    base.update(stats)
    app = {"bodyPartGroups": list(groups),
           "wornGraphicPath": f"Things/Pawn/Humanlike/Apparel/{worn}" if worn else None,
           "layers": list(layers),
           "tags": [f"HE_{nation}Apparel"] + list(tags),
           "defaultOutfitTags": ["Worker", "Soldier"] if not head else ["Soldier"]}
    if head:
        app["countsAsClothingForNudity"] = False
    d = Def("ThingDef", name, parent=parent,
            label=T(en, tr), description=T(den, dtr), techLevel=tech,
            graphicData={"texPath": f"HeirsOfEarth/Apparel/{name}", "graphicClass": "Graphic_Single"},
            stuffCategories=list(stuff) if stuff else None, costStuffCount=stuff_count if stuff else None,
            costList=counts(cost),
            statBases=base,
            equippedStatOffsets=equipped,
            thingCategories=["ApparelArmor" if "ArmorRating_Sharp" in stats and stats["ArmorRating_Sharp"] >= 0.3 else ("Headgear" if head else "Apparel")],
            tradeTags={"@Inherit": "False", "#items": [f"HE_{nation}Goods", "Clothing"]},
            apparel=app,
            colorGenerator={"@Class": "ColorGenerator_Single", "color": color} if color and not stuff else None,
            recipeMaker=recipe_maker(research_name, skill, users or TAILOR, order),
            modExtensions=[culture(nation, knowledge)])
    add(f"Things/HE_Apparel_{nation}.xml", d)
    tex(f"HeirsOfEarth/Apparel/{name}", painter, **(pargs or {}))
    return name


# ---------------------------------------------------------------- buildings
def deco(nation, key, en, tr, den, dtr, research_name, size, painter, beauty, work, stuff=("Stony",), stuff_count=80, cost=None,
         hp=200, passability="PassThroughOnly", fill=0.4, category="Furniture", designation="HE_Heritage", minify=True,
         glow=None, extra_stats=None, extra=None, comps=None, knowledge=None, draw_size=None, pargs=None, file=None, cls=None,
         parent="BuildingBase", joy=None):
    name = f"HE_{nation}_{key}"
    stats = {"MaxHitPoints": hp, "WorkToBuild": work, "Mass": 10 * size[0] * size[1], "Beauty": beauty, "Flammability": 0.5 if "Woody" in (stuff or ()) else 0}
    if extra_stats:
        stats.update(extra_stats)
    all_comps = list(comps or [])
    if glow:
        all_comps.append({"@Class": "CompProperties_Glower", "glowRadius": glow[0], "glowColor": glow[1]})
    gd = {"texPath": f"HeirsOfEarth/Buildings/{name}", "graphicClass": "Graphic_Single", "drawSize": draw_size or f"({size[0]},{size[1]})"}
    fields = dict(label=T(en, tr), description=T(den, dtr),
                  thingClass=cls or "Building",
                  graphicData=gd,
                  altitudeLayer="Building", passability=passability, fillPercent=fill, pathCost=42 if passability == "PassThroughOnly" else None,
                  rotatable=False, size=f"({size[0]},{size[1]})",
                  stuffCategories=list(stuff) if stuff else None, costStuffCount=stuff_count if stuff else None,
                  costList=counts(cost),
                  statBases=stats,
                  minifiedDef="MinifiedThing" if minify else None,
                  thingCategories=[{"Furniture": "BuildingsFurniture", "Art": "BuildingsArt", "Temperature": "BuildingsTemperature"}.get(category, "BuildingsArt")] if minify else None,
                  designationCategory=designation,
                  researchPrerequisites=[research_name] if research_name else None,
                  building=({"joyKind": joy} if joy else {"isInert": True}) if not extra or "building" not in extra else None,
                  comps=all_comps or None,
                  modExtensions=[culture(nation, knowledge)])
    if extra:
        fields.update(extra)
    d = Def("ThingDef", name, parent=parent, **fields)
    add(file or f"Things/HE_Buildings_{nation}.xml", d)
    tex(f"HeirsOfEarth/Buildings/{name}", painter, size=size, **(pargs or {}))
    return name


def floor(nation, key, en, tr, den, dtr, research_name, painter, beauty=1, cost=None, work=900, path_cost=0, stuffy=False, pargs=None,
          fertility=None, needs=None, cleanliness=0.2):
    """A buildable floor. With fertility it is farmland: plants grow on it and it can only be laid on `needs` ground."""
    name = f"HE_{nation}_{key}"
    extra = {}
    if fertility:
        extra = dict(fertility=fertility, terrainAffordanceNeeded=needs or "GrowSoil",
                     affordances={"@Inherit": "False", "#items": ["Light", "Medium", "Heavy", "Walkable", "GrowSoil", "Diggable"]},
                     generatedFilth="Filth_Dirt", takeFootprints=True)
    d = Def("TerrainDef", name, parent="FloorBase",
            label=T(en, tr), description=T(den, dtr),
            texturePath=f"HeirsOfEarth/Terrain/{name}",
            color=None,
            pathCost=path_cost,
            statBases={"WorkToBuild": work, "Beauty": beauty, "Cleanliness": cleanliness},
            costList=counts(cost),
            designationCategory="HE_Heritage",
            researchPrerequisites=[research_name],
            constructionSkillPrerequisite=3,
            uiOrder=2400, **extra)
    add(f"Things/HE_Floors_{nation}.xml", d)
    tex(f"HeirsOfEarth/Terrain/{name}", painter, **(pargs or {}))
    return name


def resource(nation, key, en, tr, den, dtr, value, painter, mass=0.5, stack=75, category="Manufactured", knowledge=None, extra=None, pargs=None, file=None):
    name = f"HE_{nation}_{key}"
    fields = dict(label=T(en, tr), description=T(den, dtr),
                  graphicData={"texPath": f"HeirsOfEarth/Items/{name}", "graphicClass": "Graphic_Single"},
                  stackLimit=stack, soundInteract="Standard_Drop", soundDrop="Standard_Drop",
                  statBases={"MarketValue": value, "Mass": mass, "MaxHitPoints": 80, "Flammability": 1},
                  thingCategories=[category],
                  tradeTags=[f"HE_{nation}Goods"],
                  modExtensions=[culture(nation, knowledge)])
    if extra:
        fields.update(extra)
    d = Def("ThingDef", name, parent="ResourceBase", **fields)
    add(file or f"Things/HE_Items_{nation}.xml", d)
    tex(f"HeirsOfEarth/Items/{name}", painter, **(pargs or {}))
    return name


# ---------------------------------------------------------------- food
def food(nation, key, en, tr, den, dtr, research_name, painter, nutrition=0.9, value=22, fine=True, ingredients=("FoodRaw",),
         count=0.5, work=500, mass=0.44, knowledge=None, rot_days=4, joy=0.0, pargs=None):
    """A cooked meal of the nation plus its stove recipe. Fine meals carry the vanilla fine-meal mood."""
    name = f"HE_{nation}_{key}"
    ing = {"preferability": "MealFine" if fine else "MealSimple", "ingestEffect": "EatVegetarian", "ingestSound": "Meal_Eat",
           "tasteThought": "AteFineMeal" if fine else None, "optimalityOffsetFeedingAnimals": -25,
           "joy": joy or None, "joyKind": "Gluttonous" if joy else None}
    add(f"Things/HE_Food_{nation}.xml", Def("ThingDef", name, parent="MealCooked",
        label=T(en, tr), description=T(den, dtr),
        graphicData={"texPath": f"HeirsOfEarth/Items/{name}", "graphicClass": "Graphic_Single"},
        statBases={"MarketValue": value, "WorkToMake": work, "Nutrition": nutrition, "Mass": mass},
        ingestible=ing, tradeTags=[f"HE_{nation}Goods"],
        comps=[{"@Class": "CompProperties_Rottable", "daysToRotStart": rot_days, "rotDestroys": True}],
        modExtensions=[culture(nation, knowledge)]))
    add(f"Things/HE_Food_{nation}.xml", Def("RecipeDef", f"HE_Cook_{nation}_{key}", parent="CookMealBase",
        label=T("cook " + en, en + " pişir"), description=T("Cook " + en + ".", tr.capitalize() + " pişir."),
        jobString=T("Cooking " + en + ".", tr.capitalize() + " pişiriyor."),
        workAmount=work, workSpeedStat="CookSpeed", requiredGiverWorkType="Cooking", effectWorking="Cook", soundWorking="Recipe_CookMeal",
        allowMixingIngredients=True, ingredientValueGetterClass="IngredientValueGetter_Nutrition",
        ingredients=[{"filter": {"categories": list(ingredients)}, "count": count}],
        fixedIngredientFilter={"categories": ["FoodRaw"]},
        products={name: 1}, workSkill="Cooking", skillRequirements={"Cooking": 4},
        researchPrerequisite=research_name, recipeUsers=list(STOVES) + ["Campfire"]))
    tex(f"HeirsOfEarth/Items/{name}", painter, **(pargs or {}))
    return name
