"""Heirs of Earth 2.1: the pieces the design promised that 2.0 left out.

- Industrial rows for Nova Roma, Yamato and Nordheim (a gun and a tradition each).
- Tianxia fire-arrow battery: an unpowered turret loaded with wood.
- Albion textile mill: a powered loom that weaves wool into tweed, now a real fabric.
- Hellas lyceum (research bench facility) and asclepion (bed facility). Their links to vanilla benches and beds
  are XML patches in HeirsOfEarth/Patches/HE_Facilities.xml.
- Signature sounds (horn, bugle, gong, drum) and the war letter that plays the horn.
"""
from heirs_data import add, tex
from heirs_kit import culture, deco, projectile, ranged, research, tool
from heirs_xml import Def, T

FS = "Core/HE_Sounds.xml"


# ------------------------------------------------------------------ sounds and the war letter
def sound(name, clip, volume):
    add(FS, Def("SoundDef", name, maxSimultaneous=1,
                subSounds=[{"onCamera": True, "grains": [{"@Class": "AudioGrain_Clip", "clipPath": "HeirsOfEarth/" + clip}],
                            "volumeRange": f"{volume}~{volume}"}]))
    return name


HORN = sound("HE_Sound_Horn", "HE_Horn", 45)
sound("HE_Sound_Bugle", "HE_Bugle", 40)
sound("HE_Sound_Gong", "HE_Gong", 42)
sound("HE_Sound_Drum", "HE_Drum", 42)
add(FS, Def("LetterDef", "HE_WarLetter", color="(196, 120, 96)", flashColor="(206, 110, 90)", flashInterval=90, arriveSound=HORN))

# ------------------------------------------------------------------ Nova Roma: industrial row
R_CARBINE = research("Roma", "Carbine", "legion carbine", "lejyon karabinası",
                     "A short breech-loading carbine for the new legions: quick to load, light to carry and easy to fire from behind a shield wall.",
                     "Yeni lejyonlar için kısa, kuyruktan dolma bir karabina: çabuk dolar, hafif taşınır ve kalkan duvarının arkasından kolayca ateşlenir.",
                     1500, "Industrial", 0, 0, prereqs=["Gunsmithing", "HE_Roma_Pilum"], knowledge=35)
R_CIVIL = research("Roma", "CivilCode", "civil code", "medeni kanun",
                   "Every right and duty written down in one book, from inheritance to the price of grain. Disputes end sooner, though every request now needs a form.",
                   "Mirastan tahıl fiyatına kadar her hak ve görev tek bir kitapta yazılı. Anlaşmazlıklar daha çabuk biter, ama artık her istek için bir dilekçe gerekir.",
                   1700, "Industrial", 2, 0, prereqs=["HE_Roma_Pax"], knowledge=45, tradition=True,
                   stats=[("NegotiationAbility", 0.06, 1, "Colonists"), ("SocialImpact", 0.06, 1, "Colonists"), ("WorkSpeedGlobal", 0, 0.98, "Colonists")],
                   effect=T("Colonists gain +6% negotiation ability and +6% social impact, but work 2% slower.",
                            "Kolonistler +%6 müzakere yeteneği ve +%6 sosyal etki kazanır, ama %2 daha yavaş çalışır."))
CARBINE_BULLET = projectile("HE_Bullet_Carbine", "carbine bullet", "karabina mermisi", "Bullet", 15, 70, "Things/Projectile/Bullet_Small", pen=0.22)
ranged("Roma", "Carbine", "legion carbine", "lejyon karabinası",
       "A short breech-loading carbine with a red-lacquered stock and a brass eagle on the lock plate. It loads fast and handles well at close range.",
       "Kırmızı cilalı dipçikli ve kilit plakasında pirinç bir kartal bulunan kısa, kuyruktan dolma bir karabina. Hızlı dolar ve yakın mesafede iyi kullanılır.",
       "Industrial", R_CARBINE, CARBINE_BULLET, 1.2, 23.9, 1.6, (0.65, 0.72, 0.55, 0.38), 3.0, 18000, "carbine",
       {"Steel": 55, "WoodLog": 15, "ComponentIndustrial": 1}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       klass=("Ranged", "RangedLight"), weapon_tags=["HE_RomaGuns"], tools=[tool("stock", "Blunt", 9, 2), tool("barrel", "Blunt", 8, 2)])

# ------------------------------------------------------------------ Yamato: industrial row
R_TANE = research("Yamato", "Tanegashima", "tanegashima", "tanegaşima",
                  "Matchlocks copied from a stranded merchant's gun and improved in the forges of Sakai until they outshot the original.",
                  "Karaya oturmuş bir tüccarın tüfeğinden kopyalanan ve Sakai ocaklarında aslını geçene dek geliştirilen fitilli tüfekler.",
                  1500, "Industrial", 0, 0, prereqs=["Gunsmithing", "HE_Yamato_Bushido"], knowledge=35)
R_SAKAI = research("Yamato", "Sakai", "Sakai gunsmiths", "Sakai tüfekçileri",
                   "Three ranks of gunners, one firing, one ramming, one priming. Every man knows his breath and his count.",
                   "Üç sıra tüfekçi: biri ateş eder, biri sıkıştırır, biri barut koyar. Her adam nefesini ve sayısını bilir.",
                   1700, "Industrial", 0, 1, prereqs=[R_TANE], knowledge=45, tradition=True,
                   stats=[("AimingDelayFactor", 0, 0.92, "Colonists")],
                   effect=T("Colonists aim 8% faster.", "Kolonistler %8 daha hızlı nişan alır."))
TANE_BALL = projectile("HE_Bullet_Tanegashima", "matchlock ball", "fitilli tüfek bilyesi", "Bullet", 21, 68, "Things/Projectile/Bullet_Small", pen=0.28)
ranged("Yamato", "Tanegashima", "tanegashima", "tanegaşima",
       "A long matchlock with a black-lacquered stock and brass fittings. The glowing cord must be kept dry, but a trained gunner hits a man at a hundred paces.",
       "Siyah cilalı dipçikli ve pirinç donanımlı uzun bir fitilli tüfek. Yanan fitil kuru tutulmalıdır, ama eğitimli bir tüfekçi yüz adımda bir adamı vurur.",
       "Industrial", R_TANE, TANE_BALL, 2.0, 27.9, 2.3, (0.48, 0.66, 0.54, 0.36), 4.0, 17000, "tanegashima",
       {"Steel": 55, "WoodLog": 30}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       klass=("Ranged", "RangedHeavy", "LongShots"), weapon_tags=["HE_YamatoGuns"], tools=[tool("stock", "Blunt", 9, 2), tool("barrel", "Blunt", 8, 2)])

# ------------------------------------------------------------------ Nordheim: industrial row
R_HARPOON = research("Nord", "HarpoonGun", "harpoon gun", "zıpkın tüfeği",
                     "A whaler's gun that throws a barbed iron harpoon on a line. It was made for whales; it works on raiders too.",
                     "Halata bağlı, dikenli bir demir zıpkın fırlatan bir balinacı tüfeği. Balinalar için yapıldı; akıncılarda da işe yarar.",
                     1500, "Industrial", 0, 0, prereqs=["Gunsmithing", "HE_Nord_Berserk"], knowledge=35)
R_FOLK = research("Nord", "FolkSchools", "folk high schools", "halk yüksekokulları",
                  "Schools without exams where farmers, fishers and smiths learn history, song and the law of the Thing together.",
                  "Çiftçilerin, balıkçıların ve demircilerin tarihi, türküleri ve Thing yasasını birlikte öğrendiği sınavsız okullar.",
                  1600, "Industrial", 2, 0, prereqs=["HE_Nord_Longships"], knowledge=45, tradition=True,
                  stats=[("GlobalLearningFactor", 0.08, 1, "Colonists"), ("ResearchSpeed", 0, 1.04, "Colonists")],
                  effect=T("Colonists learn 8% faster and research 4% faster.", "Kolonistler %8 daha hızlı öğrenir ve %4 daha hızlı araştırma yapar."))
HARPOON = projectile("HE_Projectile_Harpoon", "harpoon", "zıpkın", "Arrow", 30, 45, "HeirsOfEarth/Things/HE_Projectile_Harpoon", pen=0.45)
tex("HeirsOfEarth/Things/HE_Projectile_Harpoon", "harpoon")
ranged("Nord", "HarpoonGun", "harpoon gun", "zıpkın tüfeği",
       "A heavy short-barrelled gun that fires a barbed iron harpoon. Slow and short-ranged, but whatever it hits stays hit.",
       "Dikenli bir demir zıpkın fırlatan ağır, kısa namlulu bir tüfek. Yavaş ve kısa menzilli, ama vurduğu şey vurulmuş kalır.",
       "Industrial", R_HARPOON, HARPOON, 2.4, 19.9, 3.4, (0.6, 0.72, 0.5, 0.25), 6.0, 20000, "harpoon_gun",
       {"Steel": 80, "WoodLog": 30, "ComponentIndustrial": 1}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       klass=("Ranged", "RangedHeavy", "ShortShots"), weapon_tags=["HE_NordGuns"], tools=[tool("stock", "Blunt", 11, 2.2), tool("barrel", "Blunt", 10, 2.1)])

# ------------------------------------------------------------------ Tianxia: fire-arrow battery
R_BATTERY = research("Tianxia", "FireArrowBattery", "fire-arrow battery", "ateşli ok bataryası",
                     "A wheeled box of tubes, each holding a rocket arrow. Light one fuse and the whole nest of bees leaves at once.",
                     "Her biri bir roket ok taşıyan tüplerden oluşan tekerlekli bir sandık. Tek bir fitili yak, bütün arı kovanı aynı anda yola çıkar.",
                     1400, "Medieval", 2, 3, prereqs=["HE_Tianxia_FireArrows"], knowledge=40)
FIRE_ARROW = projectile("HE_Arrow_Fire", "fire arrow", "ateşli ok", "Flame", 8, 40, "Things/Projectile/Arrow_Small", pen=0.10)
BATTERY_GUN = "HE_Tianxia_FireArrowBattery_Gun"
add("Things/HE_Buildings_Tianxia.xml", Def(
    "ThingDef", BATTERY_GUN, parent="BaseWeaponTurret",
    label=T("fire-arrow rack", "ateşli ok rafı"),
    description=T("A hexagonal box of rocket arrows mounted on a turning cart.", "Dönen bir arabaya oturtulmuş altıgen bir roket ok sandığı."),
    graphicData={"texPath": "HeirsOfEarth/Buildings/HE_Tianxia_FireArrowBattery_Top", "graphicClass": "Graphic_Single"},
    statBases={"AccuracyTouch": 0.30, "AccuracyShort": 0.45, "AccuracyMedium": 0.38, "AccuracyLong": 0.26,
               "RangedWeapon_Cooldown": 6.5, "DeteriorationRate": 0, "Mass": 30, "Flammability": 0.5},
    verbs=[{"verbClass": "Verb_Shoot", "defaultProjectile": FIRE_ARROW, "warmupTime": 0, "minRange": 4.9, "range": 27.9,
            "ticksBetweenBurstShots": 5, "burstShotCount": 8, "soundCast": "Bow_Recurve", "consumeFuelPerShot": 1}]))
tex("HeirsOfEarth/Buildings/HE_Tianxia_FireArrowBattery_Top", "arrow_battery_top")
add("Things/HE_Buildings_Tianxia.xml", Def(
    "ThingDef", "HE_Tianxia_FireArrowBattery", parent="BuildingBase",
    label=T("fire-arrow battery", "ateşli ok bataryası"),
    description=T("A wheeled 'nest of bees' that looses eight fire arrows in one volley at anything hostile in range. It needs no power, only wood to make new arrows: one log becomes two arrows. The arrows are not accurate, but they set the enemy alight.",
                  "Menzildeki her düşmana tek yaylımda sekiz ateşli ok salan tekerlekli bir 'arı kovanı'. Elektrik istemez, sadece yeni oklar için odun ister: bir kütük iki ok olur. Oklar isabetli değildir ama düşmanı tutuşturur."),
    thingClass="Building_TurretGun", drawerType="MapMeshAndRealTime", drawHighlight=True, drawHighlightOnlyForHostile=True,
    graphicData={"texPath": "HeirsOfEarth/Buildings/HE_Tianxia_FireArrowBattery", "graphicClass": "Graphic_Single", "drawSize": "(2,2)",
                 "damageData": {"rect": "(0.2,0.2,0.6,0.6)"}, "shadowData": {"volume": "(1.5,0.35,1.4)", "offset": "(0,0,-0.05)"}},
    altitudeLayer="Building", stealable=False, rotatable=False, size="(2,2)",
    statBases={"MaxHitPoints": 260, "Flammability": 1.0, "WorkToBuild": 9000, "Mass": 60, "Beauty": -5, "ShootingAccuracyTurret": 0.9},
    tickerType="Normal", passability="PassThroughOnly", pathCost=50, fillPercent=0.5, hasTooltip=True,
    costList={"WoodLog": 120, "Steel": 40},
    terrainAffordanceNeeded="Light", designationCategory="Security", constructionSkillPrerequisite=5,
    building={"ai_combatDangerous": True, "turretGunDef": BATTERY_GUN, "turretBurstCooldownTime": 7, "turretTopDrawSize": 2.0, "turretTopOffset": "(0, 0.05)"},
    placeWorkers=["PlaceWorker_TurretTop", "PlaceWorker_ShowTurretRadius"],
    researchPrerequisites=[R_BATTERY],
    comps=[{"@Class": "CompProperties_Forbiddable"},
           {"@Class": "CompProperties_Refuelable", "fuelLabel": T("Fire arrows", "Ateşli oklar"), "fuelGizmoLabel": T("Arrows", "Oklar"),
            "outOfFuelMessage": T("Needs wood for arrows", "Ok için odun gerekli"), "fuelFilter": {"thingDefs": ["WoodLog"]},
            "fuelCapacity": 64, "fuelMultiplier": 2, "initialFuelPercent": 0, "autoRefuelPercent": 0.5, "showFuelGizmo": True,
            "minimumFueledThreshold": 1, "factorByDifficulty": True, "consumeFuelOnlyWhenUsed": True}],
    modExtensions=[culture("Tianxia")]))
tex("HeirsOfEarth/Buildings/HE_Tianxia_FireArrowBattery", "arrow_battery_base", size=(2, 2))

# ------------------------------------------------------------------ Albion: textile mill
R_MILL = research("Albion", "TextileMill", "textile mill", "dokuma fabrikası",
                  "A steam-driven power loom that weaves a bale of wool into tweed faster than ten hand weavers.",
                  "Bir balya yünü on el dokumacısından daha hızlı tüvite çeviren buharlı bir dokuma tezgâhı.",
                  1500, "Industrial", 2, 3, prereqs=["HE_Albion_FactoryOrder"], knowledge=40)
MILL = "HE_Albion_TextileMill"
add("Things/HE_Buildings_Albion.xml", Def(
    "ThingDef", MILL, parent="BenchBase",
    label=T("textile mill", "dokuma fabrikası"),
    description=T("A powered loom with an iron frame, a belt wheel and a roll of cloth. It weaves any wool into tweed, a warm and hard-wearing fabric.",
                  "Demir çerçeveli, kayış çarklı ve bir kumaş rulosu olan elektrikli bir dokuma tezgâhı. Her türlü yünü sıcak ve dayanıklı bir kumaş olan tüvite dokur."),
    thingClass="Building_WorkTable",
    graphicData={"texPath": f"HeirsOfEarth/Buildings/{MILL}", "graphicClass": "Graphic_Single", "drawSize": "(3,1)",
                 "damageData": {"cornerTL": "Damage/Corner", "cornerTR": "Damage/Corner", "cornerBL": "Damage/Corner", "cornerBR": "Damage/Corner"}},
    castEdgeShadows=True, staticSunShadowHeight=0.20,
    costList={"Steel": 120, "WoodLog": 60, "ComponentIndustrial": 2},
    altitudeLayer="Building", fillPercent=0.5, useHitPoints=True,
    statBases={"WorkToBuild": 3500, "MaxHitPoints": 200, "Flammability": 1.0, "Cleanliness": -2, "Mass": 40},
    size="(3,1)", designationCategory="Production", passability="PassThroughOnly", pathCost=50,
    hasInteractionCell=True, interactionCellOffset="(0,0,-1)", surfaceType="Item",
    researchPrerequisites=[R_MILL],
    inspectorTabs=["ITab_Bills"],
    building={"spawnedConceptLearnOpportunity": "BillsTab"},
    placeWorkers=["PlaceWorker_PreventInteractionSpotOverlap"],
    comps=[{"@Class": "CompProperties_Power", "compClass": "CompPowerTrader", "basePowerConsumption": 300, "shortCircuitInRain": True},
           {"@Class": "CompProperties_Flickable"},
           {"@Class": "CompProperties_Breakdownable"}],
    modExtensions=[culture("Albion")]))
tex(f"HeirsOfEarth/Buildings/{MILL}", "loom", size=(3, 1))
add("Things/HE_Buildings_Albion.xml", Def(
    "RecipeDef", "HE_Albion_WeaveTweed",
    label=T("weave tweed", "tüvit doku"),
    description=T("Weave 50 wool of any kind into 50 tweed.", "Herhangi bir türden 50 yünü 50 tüvite dokur."),
    jobString=T("Weaving tweed.", "Tüvit dokuyor."),
    workAmount=1600, workSpeedStat="GeneralLaborSpeed", workSkill="Crafting", effectWorking="Tailor", soundWorking="Recipe_Tailor",
    ingredients=[{"filter": {"categories": ["Wools"]}, "count": 50}],
    fixedIngredientFilter={"categories": ["Wools"]},
    products={"HE_Albion_Tweed": 50}, skillRequirements={"Crafting": 4},
    recipeUsers=[MILL], researchPrerequisite=R_MILL))

# ------------------------------------------------------------------ Hellas: lyceum and asclepion
FACILITY_PLACE = ["PlaceWorker_ShowFacilitiesConnections"]
deco("Hellas", "Lyceum", "lyceum scroll cabinet", "Lykeion parşömen dolabı",
     "A cedar cabinet full of scrolls with a marble bust of a philosopher on top. Placed near a research bench, it speeds up research by 6%.",
     "Parşömenlerle dolu, üstünde bir filozofun mermer büstü olan sedir bir dolap. Bir araştırma masasının yakınına konulunca araştırmayı %6 hızlandırır.",
     "HE_Hellas_Academy", (2, 1), "lyceum", beauty=6, work=3000, stuff=("Woody",), stuff_count=80, hp=150,
     comps=[{"@Class": "CompProperties_Facility", "statOffsets": {"ResearchSpeedFactor": 0.06}, "maxSimultaneous": 1, "maxDistance": 8}],
     extra={"placeWorkers": FACILITY_PLACE, "building": {"ai_chillDestination": False}})
deco("Hellas", "Asclepion", "asclepion", "Asklepion sunağı",
     "A small marble altar to the healer god, with herbs smouldering in a bronze bowl and the snake-wound rod beside it. Beds within six cells get +4% tend quality and +3% immunity gain speed.",
     "Şifa tanrısına adanmış küçük bir mermer sunak: bronz bir kâsede tüten otlar ve yanında yılan sarılı asa. Altı kare içindeki yataklar +%4 tedavi kalitesi ve +%3 bağışıklık kazanma hızı kazanır.",
     "HE_Hellas_Hippocratic", (1, 1), "asclepion", beauty=6, work=2400, stuff=("Stony",), stuff_count=60, hp=180, draw_size="(1,1.25)",
     glow=(2.5, "(255,176,96,0)"),
     comps=[{"@Class": "CompProperties_Facility", "statOffsets": {"MedicalTendQualityOffset": 0.04, "ImmunityGainSpeedFactor": 0.03},
             "maxSimultaneous": 1, "maxDistance": 6}],
     extra={"placeWorkers": FACILITY_PLACE, "building": {"ai_chillDestination": False}})
