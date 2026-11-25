"""Heirs of Earth 3.3 "Art of War": every nation raids with its own doctrine (a preferred raid plan and arrival, and a drill that
its raiders fight with), each nation keeps its own pack and herd animals, and every heir can build a manned trebuchet."""
from heirs_c_v32 import free_slot
from heirs_data import FILES, add, key, tex
from heirs_kit import research
from heirs_xml import Def, T

NATIONS = ("Roma", "Yamato", "Nord", "Hellas", "Tianxia", "Albion", "Kemet", "Pars", "Inti")


def find(cls, name):
    for defs in FILES.values():
        for d in defs:
            if d.cls == cls and d.name == name:
                return d
    raise KeyError(f"{cls} {name} not found")


# ------------------------------------------------------------------ doctrines
# (nation, label en/tr, description en/tr, strategy, arrival, chance, formation radius, stages)
# A stage is (min severity, label en, label tr, statOffsets, statFactors, pain factor). Formation drills grow with the comrades
# standing close by: alone (0), in a loose line (a quarter of a full rank), in full formation (four comrades or more).
DOCTRINES = [
    ("Roma", ("testudo", "testudo"),
     ("Legionaries close ranks and lock their shields into a roof. Packed together they shrug off arrows and blows, but they march slowly.",
      "Lejyonerler saflarını sıklaştırır ve kalkanlarını bir çatı gibi birbirine kilitler. Sık durdukça oklara ve darbelere aldırmazlar ama yavaş yürürler."),
     "StageThenAttack", "EdgeWalkIn", 0.75, 2.9,
     [(0.0, "broken ranks", "dağınık saf", {}, {}, None),
      (0.24, "loose line", "gevşek saf", {"ArmorRating_Sharp": 0.10, "ArmorRating_Blunt": 0.05, "MoveSpeed": -0.2}, {}, None),
      (0.74, "shield roof", "kalkan çatısı", {"ArmorRating_Sharp": 0.20, "ArmorRating_Blunt": 0.10, "MoveSpeed": -0.4}, {}, None)]),
    ("Hellas", ("phalanx", "falanks"),
     ("Hoplites fight shoulder to shoulder, each shield covering the man to the left. In the line they are hard to hit and hard to escape; alone they are ordinary men.",
      "Hoplitler omuz omuza dövüşür, her kalkan soldakini korur. Safta vurulmaları da kaçılmaları da zordur; yalnız kaldıklarında sıradan adamlardır."),
     "ImmediateAttack", "EdgeWalkIn", 0.75, 2.9,
     [(0.0, "broken line", "dağılmış saf", {}, {}, None),
      (0.24, "loose phalanx", "gevşek falanks", {"ArmorRating_Sharp": 0.06, "MeleeHitChance": 2, "MeleeDodgeChance": 2}, {}, None),
      (0.74, "closed phalanx", "kapalı falanks", {"ArmorRating_Sharp": 0.12, "MeleeHitChance": 4, "MeleeDodgeChance": 4}, {}, None)]),
    ("Nord", ("strandhogg", "strandhogg"),
     ("The shore raid: no siege and no waiting. Raiders cut through walls with axes and run at the enemy, fast, fierce and hard to stop with pain.",
      "Kıyı baskını: kuşatma yok, bekleme yok. Akıncılar duvarları baltayla yarar ve düşmana koşar; hızlı, öfkeli ve acıyla durdurulması zor."),
     "ImmediateAttackBreaching", None, 0.6, 0,
     [(0.0, "raider's fury", "akıncı öfkesi", {"MoveSpeed": 0.3, "MeleeHitChance": 3}, {}, 0.85)]),
    ("Yamato", ("bushido", "bushido"),
     ("Samurai attack in small bands from several sides at once and pick their targets with care. Calm in the face of death, they fight on through wounds.",
      "Samuraylar aynı anda birkaç yandan küçük gruplar halinde saldırır ve hedeflerini dikkatle seçer. Ölüm karşısında sakindirler, yaralarına rağmen dövüşmeyi sürdürürler."),
     "ImmediateAttackSmart", "EdgeWalkInGroups", 0.75, 0,
     [(0.0, "way of the warrior", "savaşçının yolu", {"MeleeHitChance": 3, "MeleeDodgeChance": 3}, {}, 0.85)]),
    ("Tianxia", ("art of war", "savaş sanatı"),
     ("Every battle is won before it is fought. Tianxia armies gather out of reach, wait for the right moment and then strike with drilled crossbow volleys.",
      "Her savaş, yapılmadan önce kazanılır. Tianxia orduları menzil dışında toplanır, doğru anı bekler ve sonra talimli arbalet yaylımlarıyla vurur."),
     "StageThenAttack", None, 0.75, 0,
     [(0.0, "drilled volleys", "talimli yaylım", {"ShootingAccuracyPawn": 3}, {"AimingDelayFactor": 0.85}, None)]),
    ("Albion", ("siege train", "kuşatma kolu"),
     ("Albion comes with spades and guns. Its armies often dig in and build a battery before they attack, and its riflemen fire steady, measured volleys.",
      "Albion kürek ve topla gelir. Orduları çoğu zaman saldırmadan önce siper kazar ve bir batarya kurar; tüfekçileri sakin, ölçülü yaylımlar atar."),
     "Siege", None, 0.4, 0,
     [(0.0, "volley fire", "yaylım ateşi", {"ShootingAccuracyPawn": 3, "MoveSpeed": -0.1}, {"AimingDelayFactor": 0.8}, None)]),
    ("Kemet", ("chariot vanguard", "savaş arabası öncüsü"),
     ("Kemet's attack opens with speed: the vanguard runs ahead as the chariots once did and is on the walls before the defenders are ready.",
      "Kemet'in saldırısı hızla başlar: öncü birlik bir zamanlar savaş arabalarının yaptığı gibi öne koşar ve savunanlar hazır olmadan surlara varır."),
     "ImmediateAttack", "EdgeWalkIn", 0.75, 0,
     [(0.0, "vanguard's speed", "öncü hızı", {"MoveSpeed": 0.8}, {}, None)]),
    ("Pars", ("cavalry wings", "süvari kanatları"),
     ("The armies of Pars attack on the wings: several swift groups at once, used to fighting from the saddle and closing in fast.",
      "Pars orduları kanatlardan saldırır: aynı anda birkaç hızlı grup, eyerden dövüşmeye ve hızla yaklaşmaya alışkın."),
     "ImmediateAttack", "EdgeWalkInGroups", 0.75, 0,
     [(0.0, "rider's charge", "atlı hücumu", {"MoveSpeed": 0.6, "MeleeHitChance": 2}, {}, None)]),
    ("Inti", ("mountain sappers", "dağ lağımcıları"),
     ("The road builders of the Andes go through rock rather than around it. Inti raiders dig toward your walls and throw stones with mountain-trained aim.",
      "And Dağları'nın yol yapıcıları kayanın etrafından değil içinden geçer. Inti akıncıları surlarına doğru tünel kazar ve dağda eğitilmiş bir nişanla taş atar."),
     "ImmediateAttackSappers", "EdgeWalkIn", 0.75, 0,
     [(0.0, "mountain stride", "dağ adımı", {"ShootingAccuracyPawn": 2, "MoveSpeed": 0.3}, {}, None)]),
]

DRILL_FILE = "Core/HE_Doctrines.xml"


def stage(min_sev, en, tr, offsets, factors, pain):
    s = {"minSeverity": min_sev if min_sev else None, "label": T(en, tr)}
    if offsets:
        s["statOffsets"] = offsets
    if factors:
        s["statFactors"] = factors
    if pain:
        s["painFactor"] = pain
    return s


for nation, (en, tr), (den, dtr), strategy, arrival, chance, radius, stages in DOCTRINES:
    hediff = f"HE_Doctrine_{nation}"
    comp = {"@Class": "HeirsOfEarth.HediffCompProperties_HeirsDoctrine"}
    if radius:
        comp["formationRadius"] = radius
        comp["formationFull"] = 4
    add(DRILL_FILE, Def("HediffDef", hediff, label=T(f"{en} drill", f"{tr} talimi"),
                        description=T(den + ("\n\nThe more comrades stand within three cells, the stronger it is." if radius else
                                             "\n\nIt lasts while the raider fights for the raid."),
                                      dtr + ("\n\nÜç kare içinde ne kadar çok yoldaş durursa o kadar güçlüdür." if radius else
                                             "\n\nAkıncı baskın için dövüştüğü sürece sürer.")),
                        hediffClass="HediffWithComps", isBad=False, defaultLabelColor="(0.85, 0.66, 0.36)",
                        initialSeverity=0.01, minSeverity=0.001, maxSeverity=1, everCurableByItem=False,
                        comps=[comp], stages=[stage(*s) for s in stages]))
    nation_def = find("HeirsOfEarth.NationDef", f"HE_{nation}")
    nation_def.fields["doctrine"] = {"label": T(en, tr), "description": T(den, dtr), "hediff": hediff,
                                     "strategy": strategy, "arrival": arrival, "chance": chance}

key("HE_DoctrineLetter", "War doctrine: {0}. {1}", "Savaş öğretisi: {0}. {1}")
key("HE_SettingsDoctrines", "Nations raid with their war doctrines", "Devletler savaş öğretileriyle baskın yapar")
key("HE_SettingsDoctrinesTip",
    "Each heir nation prefers its own raid plan and way of arriving, and its raiders fight with a drill (for example the Roman testudo or the Hellenic phalanx). Off: heir raids behave like vanilla raids.",
    "Her mirasçı devlet kendi baskın planını ve geliş şeklini tercih eder, akıncıları da bir talimle dövüşür (örneğin Roma testudosu ya da Helen falanksı). Kapalı: mirasçı baskınları vanilya baskınları gibi davranır.")
key("HE_AtlasDoctrine", "War doctrine", "Savaş öğretisi")
key("HE_AtlasAnimal", "Pack and herd animal", "Yük ve sürü hayvanı")


# ------------------------------------------------------------------ animals
# Carriers that walk with each nation's caravans, and the animal every heir start brings along.
ANIMALS = {
# A biome only lets some animals carry caravan goods (Patches/HE_PackAnimals.xml adds horses, donkeys and yaks where they belong);
# a little muffalo in every list keeps caravans possible in any biome.
    "Roma": ({"Horse": 5, "Donkey": 2, "Muffalo": 1}, "Horse"),
    "Yamato": ({"Horse": 5, "Yak": 3, "Muffalo": 1}, "Horse"),
    "Nord": ({"Yak": 5, "Muffalo": 4}, "Husky"),
    "Hellas": ({"Donkey": 6, "Horse": 2, "Muffalo": 1}, "Donkey"),
    "Tianxia": ({"Yak": 4, "Horse": 4, "Muffalo": 1}, "Yak"),
    "Albion": ({"Horse": 6, "Muffalo": 2}, "Horse"),
    "Kemet": ({"Dromedary": 6, "Donkey": 2, "Muffalo": 1}, "Dromedary"),
    "Pars": ({"Dromedary": 5, "Horse": 3, "Muffalo": 1}, "Dromedary"),
    "Inti": ({"Alpaca": 7, "Muffalo": 1}, "Alpaca"),
}

for nation, (carriers, start) in ANIMALS.items():
    faction = find("FactionDef", f"HE_Faction_{nation}")
    traders = [g for g in faction.fields["pawnGroupMakers"] if g.get("kindDef") == "Trader"]
    assert traders, nation
    for g in traders:
        g["carriers"] = dict(carriers)
    scen = find("ScenarioDef", f"HE_Start_{nation}")
    parts = [p for p in scen.fields["scenario"]["parts"] if p.get("@Class") == "ScenPart_StartingAnimal"]
    assert len(parts) == 1, nation
    parts[0]["animalKind"] = start
    find("HeirsOfEarth.NationDef", f"HE_{nation}").fields["animal"] = start


# ------------------------------------------------------------------ trebuchet (shared, medieval)
STONES = ["ChunkGranite", "ChunkLimestone", "ChunkMarble", "ChunkSandstone", "ChunkSlate"]
col, row = free_slot("Common", "Medieval")
R_TREB = research("Common", "Trebuchet", "trebuchet", "mancınık",
                  "A long arm on an axle with a box of stones at the short end: when the box falls, the long end flings a boulder over any wall. Every heir nation built some kind of it.",
                  "Bir mil üzerinde uzun bir kol ve kısa ucunda taş dolu bir sandık: sandık düştüğünde uzun uç bir kaya parçasını her surun üzerinden fırlatır. Her mirasçı devlet bunun bir türünü yapmıştır.",
                  1600, "Medieval", col, row, prereqs=["Smithing"])
find("ResearchProjectDef", R_TREB).fields["modExtensions"] = [{"@Class": "HeirsOfEarth.HeirsResearchExt"}]  # listed in the research browser

PROJ = "HE_Boulder_Trebuchet"
add("Things/HE_Projectiles.xml", Def(
    "ThingDef", PROJ, parent="BaseBullet", label=T("trebuchet boulder", "mancınık kayası"), thingClass="Projectile_Explosive",
    graphicData={"texPath": "HeirsOfEarth/Projectiles/HE_Stone_Inti", "graphicClass": "Graphic_Single", "drawSize": "(1.3,1.3)"},
    projectile={"damageDef": "Bomb", "damageAmountBase": 32, "armorPenetrationBase": 0.3, "speed": 26, "explosionRadius": 1.9,
                "flyOverhead": True, "shadowSize": 0.8, "soundExplode": "MortarBomb_Explode"}))

GUN = "HE_Trebuchet_Gun"
add("Things/HE_Buildings_Common.xml", Def(
    "ThingDef", GUN, parent="BaseWeaponTurret", label=T("trebuchet arm", "mancınık kolu"),
    description=T("The throwing arm and counterweight of a trebuchet.", "Bir mancınığın atış kolu ve karşı ağırlığı."),
    graphicData={"texPath": "HeirsOfEarth/Buildings/HE_Trebuchet_Top", "graphicClass": "Graphic_Single"},
    statBases={"AccuracyTouch": 0.1, "AccuracyShort": 0.3, "AccuracyMedium": 0.45, "AccuracyLong": 0.4,
               "RangedWeapon_Cooldown": 12, "DeteriorationRate": 0, "Mass": 60, "Flammability": 0.8},
    verbs=[{"verbClass": "Verb_Shoot", "defaultProjectile": PROJ, "warmupTime": 0, "range": 56.9, "minRange": 19.9,
            "requireLineOfSight": False, "forcedMissRadius": 4.9, "burstShotCount": 1, "soundCast": "Bow_Large",
            "consumeFuelPerShot": 1, "targetParams": {"canTargetLocations": True}}]))
tex("HeirsOfEarth/Buildings/HE_Trebuchet_Top", "turret_top", kind="trebuchet")

TREB = "HE_Trebuchet"
add("Things/HE_Buildings_Common.xml", Def(
    "ThingDef", TREB, parent="BuildingBase", label=T("trebuchet", "mancınık"),
    description=T("A counterweight trebuchet on a bed of rammed earth. A crew member must man it; it then hurls boulders over walls at enemies "
                  "far out of bow range, smashing what they land on. It cannot hit anything closer than twenty cells, misses often and "
                  "reloads slowly, but nothing an heir can build reaches further before the age of gunpowder. Fed with stone chunks: one chunk "
                  "makes one boulder.",
                  "Sıkıştırılmış toprak bir yatak üzerinde karşı ağırlıklı bir mancınık. Başına bir kişinin geçmesi gerekir; o zaman ok "
                  "menzilinin çok dışındaki düşmanlara surların üzerinden kayalar fırlatır ve düştüğü yeri ezer. Yirmi kareden yakını vuramaz, "
                  "sık ıskalar ve yavaş doldurulur ama barut çağından önce bir mirasçının yapabileceği hiçbir şey daha uzağa erişmez. Taş "
                  "yığınıyla beslenir: bir yığın bir kaya eder."),
    thingClass="Building_TurretGun", drawerType="MapMeshAndRealTime", drawHighlight=True, drawHighlightOnlyForHostile=True,
    graphicData={"texPath": "HeirsOfEarth/Buildings/" + TREB, "graphicClass": "Graphic_Single", "drawSize": "(3,3)",
                 "damageData": {"rect": "(0.2,0.2,0.6,0.6)"}, "shadowData": {"volume": "(2.4,0.5,2.2)", "offset": "(0,0,-0.1)"}},
    altitudeLayer="Building", stealable=False, rotatable=False, size="(3,3)", hasInteractionCell=True, interactionCellOffset="(0,0,-2)",
    statBases={"MaxHitPoints": 520, "Flammability": 1.0, "WorkToBuild": 14000, "Mass": 120, "Beauty": -6, "ShootingAccuracyTurret": 0.9},
    tickerType="Normal", passability="PassThroughOnly", pathCost=60, fillPercent=0.5, hasTooltip=True,
    costList={"WoodLog": 320, "Steel": 60}, terrainAffordanceNeeded="Medium", designationCategory="Security",
    constructionSkillPrerequisite=6,
    building={"ai_combatDangerous": True, "turretGunDef": GUN, "turretBurstWarmupTime": 3.0, "turretBurstCooldownTime": 12,
              "turretTopDrawSize": 3.6, "turretTopOffset": "(0, 0.05)"},
    placeWorkers=["PlaceWorker_NotUnderRoof", "PlaceWorker_TurretTop", "PlaceWorker_PreventInteractionSpotOverlap", "PlaceWorker_ShowTurretRadius"],
    researchPrerequisites=[R_TREB],
    comps=[{"@Class": "CompProperties_Forbiddable"},
           {"@Class": "CompProperties_Mannable", "manWorkType": "Violent"},
           {"@Class": "CompProperties_Refuelable", "fuelLabel": T("Boulders", "Kayalar"), "fuelGizmoLabel": T("Boulders", "Kayalar"),
            "outOfFuelMessage": T("Needs stone chunks", "Taş yığını gerekli"), "fuelFilter": {"thingDefs": STONES},
            "fuelCapacity": 12, "fuelMultiplier": 1, "initialFuelPercent": 0, "autoRefuelPercent": 0.5, "showFuelGizmo": True,
            "minimumFueledThreshold": 1, "factorByDifficulty": True, "consumeFuelOnlyWhenUsed": True}]))
tex("HeirsOfEarth/Buildings/" + TREB, "turret_base", size=(3, 3), style="earthwork")
