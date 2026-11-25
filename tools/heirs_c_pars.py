"""Satrapy of Pars (3.0): nation, research branch, weapons, armour, buildings, floors and food.

Pars is the road-and-garden nation: caravans, diplomacy, horses and fine goods. Its signature pieces are the akinakes,
the scale coat of the Immortals, the jezail, the walled paradise garden and the carpet loom, whose carpets are
the most valuable trade good any heir nation makes.
"""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, culture, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Pars"
FN = "Nations/HE_Pars.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Pars",
                 label=T("Satrapy of Pars", "Pars Satraplığı"),
                 description=T("The colony ship Pasargad came down on a high plateau ringed by mountains, and its people built roads before they built walls. Pars is a patchwork of provinces held together by a royal road, a post that never stops and a court that remembers every favour. Its satraps love gardens, horses and good carpets, keep their word and expect others to keep theirs. They are old friends of Tianxia and old rivals of Nova Roma.",
                               "Pasargad koloni gemisi dağlarla çevrili yüksek bir yaylaya indi ve halkı surlardan önce yollar yaptı. Pars; bir kraliyet yolu, hiç durmayan bir posta ve her iyiliği hatırlayan bir sarayla bir arada tutulan eyaletlerden oluşur. Satrapları bahçeleri, atları ve iyi halıları sever, sözlerini tutar ve başkalarının da tutmasını bekler. Tianxia'nın eski dostu, Nova Roma'nın eski rakibidir."),
                 color="(0.62, 0.12, 0.17)", iconPath="HeirsOfEarth/UI/HE_Pars",
                 rulerTitle=T("Satrap", "Satrap"), adjective=T("Parsian", "Pars"), release=3,
                 friends=["HE_Tianxia"], rivals=["HE_Roma"])
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Pars", "nation_icon", color="#9e1f2b", emblem="griffin")

# ------------------------------------------------------------------ research: Neolithic
R_SPEAR = research(NATION, "Spear", "immortal's spear", "ölümsüz mızrağı",
                   "A long spear with a leaf blade at one end and a silver pomegranate at the other, the weapon of the royal guard.",
                   "Bir ucunda yaprak biçimli bir ağız, öbür ucunda gümüş bir nar bulunan uzun bir mızrak; kraliyet muhafızlarının silahı.",
                   450, "Neolithic", 0, 0)
R_KAFTAN = research(NATION, "Kaftan", "silk kaftan", "ipek kaftan",
                    "Cut the long open coat of the court, lined, embroidered and belted with a sash.",
                    "Sarayın astarlı, nakışlı ve kuşakla bağlanan uzun, önü açık ceketini dik.",
                    450, "Neolithic", 1, 0)
R_GARDEN = research(NATION, "Garden", "paradise garden", "cennet bahçesi",
                    "Wall a square of ground, split it in four with water channels and plant it with roses, cypress and fruit trees. The old word for it was paradise.",
                    "Bir toprak karesini duvarla çevir, su kanallarıyla dörde böl ve güller, serviler ve meyve ağaçlarıyla doldur. Eski dilde adı cennetti.",
                    550, "Neolithic", 2, 0)
R_BOW = research(NATION, "Bow", "recurve bow", "çift kavisli yay",
                 "A short recurve bow carried in a combined case with its arrows, light enough to shoot from the saddle.",
                 "Oklarıyla birlikte tek bir kılıfta taşınan, eyerden atılacak kadar hafif, kısa ve çift kavisli bir yay.",
                 550, "Neolithic", 0, 1, prereqs=[R_SPEAR])
R_PILAF = research(NATION, "Pilaf", "saffron pilaf", "safranlı pilav",
                   "Rice steamed with saffron, barberries and butter until the bottom turns to a golden crust, the best part.",
                   "Altı en güzel kısmı olan altın bir kabuk tutana dek safran, kızamık üzümü ve tereyağıyla demlenmiş pirinç.",
                   400, "Neolithic", 1, 1, prereqs=[R_KAFTAN])
R_GARDENS = research(NATION, "GardenCulture", "culture of gardens", "bahçe kültürü",
                     "Every house has a courtyard, every courtyard a pool and every pool a bench beside it. Parsians go into the garden to cool their tempers.",
                     "Her evin bir avlusu, her avlunun bir havuzu, her havuzun yanında bir bankı vardır. Parslılar öfkelerini soğutmak için bahçeye çıkar.",
                     750, "Neolithic", 2, 1, prereqs=[R_GARDEN], knowledge=15, tradition=True,
                     stats=[("MentalBreakThreshold", -0.03, 1, "Colonists")],
                     effect=T("The mental break threshold of colonists drops by 3%.", "Kolonistlerin zihinsel çöküş eşiği %3 düşer."))
R_SATRAP = research(NATION, "SatrapLaw", "law of the satraps", "satraplar kanunu",
                    "One law for every province, written down, read aloud in the market and enforced by the satrap's own men. People know where they stand.",
                    "Her eyalet için tek bir kanun; yazılı, çarşıda yüksek sesle okunur ve satrabın kendi adamlarınca uygulanır. İnsanlar nerede durduklarını bilir.",
                    750, "Neolithic", 0, 2, prereqs=[R_BOW], knowledge=15, tradition=True,
                    stats=[("ArrestSuccessChance", 0.15, 1, "Colonists"), ("NegotiationAbility", 0.05, 1, "Colonists")],
                    effect=T("Colonists make arrests 15% more successfully and negotiate 5% better.",
                             "Kolonistler tutuklamalarda %15 daha başarılıdır ve %5 daha iyi pazarlık eder."))
R_POST = research(NATION, "RoyalPost", "royal post", "kraliyet postası",
                  "A station every day's ride, a fresh horse in every station and a rider who does not stop for snow, rain, heat or night.",
                  "Her günlük yolda bir menzil, her menzilde dinç bir at ve kar, yağmur, sıcak ya da gece için durmayan bir ulak.",
                  900, "Neolithic", 1, 2, prereqs=[R_PILAF], knowledge=20, tradition=True, caravan=0.10,
                  stats=[("TradePriceImprovement", 0.05, 1, "Colonists")],
                  effect=T("Caravans travel 10% faster and colonists get 5% better trade prices.",
                           "Kervanlar %10 daha hızlı gider ve kolonistler %5 daha iyi ticaret fiyatı alır."))
R_QANAT = research(NATION, "Qanats", "qanats", "kanatlar",
                   "Tunnels dug from the foot of the mountains to bring cold, clean water to every village without losing a drop to the sun.",
                   "Dağların eteğinden kazılan ve güneşe bir damla bile kaptırmadan her köye soğuk, temiz su getiren tüneller.",
                   800, "Neolithic", 2, 2, prereqs=[R_GARDENS], knowledge=20, tradition=True,
                   stats=[("ImmunityGainSpeed", 0, 1.06, "Colonists")],
                   effect=T("Colonists gain immunity 6% faster.", "Kolonistler %6 daha hızlı bağışıklık kazanır."))
# ------------------------------------------------------------------ research: Medieval
R_AKINAKES = research(NATION, "Akinakes", "akinakes", "akinakes",
                      "Forge the short straight sword of the guard, worn on the right hip in a gold-capped scabbard.",
                      "Muhafızların sağ kalçada, altın uçlu bir kında taşıdığı kısa, düz kılıcı döv.",
                      900, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_LOOM = research(NATION, "CarpetLoom", "carpet loom", "halı tezgâhı",
                  "An upright loom, a hundred colours of wool and a pattern held in the weaver's head. A good carpet takes a season and outlives its maker.",
                  "Dik bir tezgâh, yüz renk yün ve dokumacının kafasında tuttuğu bir desen. İyi bir halı bir mevsim sürer ve yapanından uzun yaşar.",
                  1000, "Medieval", 1, 0, prereqs=[R_POST], knowledge=15)
R_POLO = research(NATION, "Polo", "polo", "çevgen",
                  "Riders, mallets and a wooden ball on a long field. The princes play it to learn horsemanship, and the horses learn too.",
                  "Uzun bir sahada atlılar, sopalar ve tahta bir top. Prensler onu binicilik öğrenmek için oynar; atlar da öğrenir.",
                  1000, "Medieval", 2, 0, prereqs=[R_QANAT], knowledge=25, tradition=True,
                  stats=[("TrainAnimalChance", 0, 1.10, "Colonists"), ("TameAnimalChance", 0, 1.10, "Colonists")],
                  effect=T("Colonists train and tame animals 10% more successfully.", "Kolonistler hayvanları %10 daha başarılı eğitir ve evcilleştirir."))
R_IMMORTALS = research(NATION, "Immortals", "the Immortals", "Ölümsüzler",
                       "The scale coat and the winged helmet of the royal guard. Their number never drops: when one falls, another steps into the empty place.",
                       "Kraliyet muhafızlarının pullu zırhı ve kanatlı miğferi. Sayıları hiç azalmaz: biri düştüğünde yerine bir başkası geçer.",
                       1200, "Medieval", 0, 1, prereqs=[R_AKINAKES], knowledge=25)
R_EARS = research(NATION, "KingsEars", "ears of the king", "kralın kulakları",
                  "Officials who travel the provinces, listen to everyone and report only to the court. Envoys of Pars always know whom they are talking to.",
                  "Eyaletleri dolaşan, herkesi dinleyen ve yalnızca saraya rapor veren memurlar. Pars elçileri kiminle konuştuklarını her zaman bilir.",
                  1100, "Medieval", 1, 1, prereqs=[R_LOOM], knowledge=25, tradition=True,
                  stats=[("NegotiationAbility", 0.08, 1, "Colonists"), ("SocialImpact", 0.04, 1, "Colonists")],
                  effect=T("Colonists negotiate 8% better and have 4% more social impact.", "Kolonistler %8 daha iyi pazarlık eder ve %4 daha fazla sosyal etki yapar."))
R_GUARD = research(NATION, "TenThousand", "the ten thousand", "on binler",
                   "Drill until the line holds by itself. A wounded guard holds the line until the one behind can take the place.",
                   "Saf kendi kendine tutana dek talim. Yaralı bir muhafız arkasındaki adam yerini alana kadar yerinde kalır.",
                   1300, "Medieval", 0, 2, prereqs=[R_IMMORTALS], knowledge=35, tradition=True,
                   stats=[("PainShockThreshold", 0.05, 1, "Colonists"), ("MeleeHitChance", 1, 1, "Colonists")],
                   effect=T("Colonists withstand 5% more pain and hit 1 point more often in melee.",
                            "Kolonistler %5 daha fazla acıya dayanır ve yakın dövüşte 1 puan daha sık isabet ettirir."))
# ------------------------------------------------------------------ research: Industrial
R_JEZAIL = research(NATION, "Jezail", "jezail", "cezayir tüfeği",
                    "A long-barrelled flintlock with a sharply curved stock, inlaid with bone and brass. Mountain shots swear by it.",
                    "Kemik ve pirinç kakmalı, keskin kıvrımlı dipçikli, uzun namlulu çakmaklı bir tüfek. Dağ nişancıları ona yemin eder.",
                    1500, "Industrial", 0, 0, prereqs=["Gunsmithing", R_AKINAKES], knowledge=35)
R_BAZAAR = research(NATION, "GrandBazaar", "grand bazaar", "kapalı çarşı",
                    "A covered street of a thousand shops, its guilds, its money changers and its tea houses. Everything has a price and everyone knows it.",
                    "Bin dükkânlı kapalı bir cadde; loncaları, sarrafları ve çayhaneleriyle. Her şeyin bir fiyatı vardır ve herkes onu bilir.",
                    1700, "Industrial", 2, 0, prereqs=[R_POLO], knowledge=45, tradition=True,
                    stats=[("TradePriceImprovement", 0.04, 1, "Colonists"), ("NegotiationAbility", 0.03, 1, "Colonists")],
                    effect=T("Colonists get 4% better trade prices and negotiate 3% better.",
                             "Kolonistler %4 daha iyi ticaret fiyatı alır ve %3 daha iyi pazarlık eder."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Spear", "immortal's spear", "ölümsüz mızrağı",
      "A long spear of cornel wood with a broad leaf blade and a silver pomegranate on the butt, carried upright on parade and levelled in battle.",
      "Geniş yaprak biçimli bir ağzı ve dipte gümüş bir narı olan, kızılcık ağacından uzun bir mızrak; geçit töreninde dik taşınır, savaşta indirilir.",
      "Neolithic", R_SPEAR, [tool("butt", "Blunt", 9, 2.0), tool("point", "Stab", 18, 2.1, 0.30)],
      mass=1.7, work=7500, painter="spear_long", stuff=("Metallic", "Woody"), stuff_count=40, skill=3, angle=-45,
      extra_tags=["NeolithicMeleeDecent"], pargs={"head": "pomegranate", "shaft": "#7a4a2c"})
melee(NATION, "Akinakes", "akinakes", "akinakes",
      "A short straight sword with a heart-shaped guard and a pommel of two griffin heads. Quick in a press and worn by every guard officer.",
      "Kalp biçimli bir siperi ve iki grifon başından bir topuzu olan kısa, düz bir kılıç. Kalabalıkta çevik; her muhafız subayı taşır.",
      "Medieval", R_AKINAKES, [tool("pommel", "Blunt", 9, 2), tool("edge", "Cut", 16, 1.7, 0.24), tool("point", "Stab", 18, 1.8, 0.28)],
      mass=1.1, work=12500, painter="akinakes", stuff_count=50, skill=5, angle=-45, extra_tags=["MedievalMeleeDecent"])
ARROW = projectile("HE_Arrow_Pars", "cane arrow", "kamış ok", "Arrow", 12, 52, "Things/Projectile/Arrow_Small", pen=0.16)
ranged(NATION, "Bow", "recurve bow", "çift kavisli yay",
       "A short, deeply recurved bow of horn and sinew with lacquered red limbs. Fast to draw and light enough to shoot from a galloping horse.",
       "Boynuz ve sinirden, kırmızı cilalı kollu, kısa ve derin kavisli bir yay. Çabuk çekilir ve dörtnala giden bir attan atılacak kadar hafiftir.",
       "Neolithic", R_BOW, ARROW, 1.0, 26.9, 1.25, (0.62, 0.72, 0.6, 0.45), 0.9, 8500, "recurve_bow",
       {"WoodLog": 35}, extra_tags=["NeolithicRangedDecent"])
JEZAIL_BALL = projectile("HE_Bullet_Jezail", "jezail ball", "cezayir mermisi", "Bullet", 20, 70, "Things/Projectile/Bullet_Small", pen=0.25)
ranged(NATION, "Jezail", "jezail", "cezayir tüfeği",
       "A very long flintlock with a curved, bone-inlaid stock. It takes an age to reload, but a patient shooter can hit a man across a valley.",
       "Kemik kakmalı, kıvrık dipçikli çok uzun bir çakmaklı tüfek. Doldurması bir ömür sürer, ama sabırlı bir nişancı vadinin karşısındaki adamı vurabilir.",
       "Industrial", R_JEZAIL, JEZAIL_BALL, 2.0, 34.9, 2.2, (0.32, 0.6, 0.7, 0.58), 4.6, 18000, "jezail",
       {"Steel": 55, "WoodLog": 30, "ComponentIndustrial": 1}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       klass=("Ranged", "RangedHeavy", "LongShots"), weapon_tags=["HE_ParsGuns"], tools=[tool("stock", "Blunt", 9, 2), tool("barrel", "Blunt", 8, 2)])

# ------------------------------------------------------------------ apparel
apparel(NATION, "Kaftan", "silk kaftan", "ipek kaftan",
        "A long open coat of red silk lined with cotton, embroidered at the hems and closed with a gold sash. Warm on the plateau at night and splendid at court.",
        "Pamuk astarlı, etekleri nakışlı ve altın bir kuşakla kapanan kırmızı ipekten uzun, önü açık bir ceket. Yaylada geceleri sıcak, sarayda göz kamaştırıcı.",
        "Neolithic", R_KAFTAN, "Duster/Duster", ["Shell"], ["Torso", "Shoulders", "Arms", "Legs"],
        {"MaxHitPoints": 140, "StuffEffectMultiplierArmor": 0.15, "StuffEffectMultiplierInsulation_Cold": 0.55, "StuffEffectMultiplierInsulation_Heat": 0.45},
        "torso4", stuff=("Fabric",), stuff_count=75, work=5200, mass=1.4, equipped={"SocialImpact": 0.04}, pargs={"kind": "kaftan"})
apparel(NATION, "ScaleCoat", "immortal's scale coat", "ölümsüz pullu zırhı",
        "A knee-length coat of small iron scales sewn on leather, worn under the robe so that an enemy never knows who is armoured.",
        "Deriye dikilmiş küçük demir pullardan dizine kadar uzun bir zırh; düşman kimin zırhlı olduğunu bilmesin diye cübbenin altına giyilir.",
        "Medieval", R_IMMORTALS, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders", "Legs"],
        {"MaxHitPoints": 210, "StuffEffectMultiplierArmor": 0.72, "StuffEffectMultiplierInsulation_Cold": 0.2, "StuffEffectMultiplierInsulation_Heat": 0.05},
        "torso4", parent="ArmorSmithableBase", stuff=("Metallic",), stuff_count=110, cost={"Leather_Plain": 30}, work=22000, mass=8.0,
        users=SMITHY, skill=6, equipped={"MoveSpeed": -0.10}, tags=["MedievalMilitary"], pargs={"kind": "scalecoat"})
apparel(NATION, "WingedHelm", "winged helmet", "kanatlı miğfer",
        "A tall pointed helmet with a mail curtain over the neck and two gilded wings on the brow, the sign of a guard captain.",
        "Ensesine örme bir perde inen ve alnında iki yaldızlı kanat bulunan uzun, sivri bir miğfer; muhafız yüzbaşısının nişanı.",
        "Medieval", R_IMMORTALS, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 130, "StuffEffectMultiplierArmor": 0.7, "StuffEffectMultiplierInsulation_Cold": 0.12, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet4", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=55, cost={"Gold": 3}, work=6000, mass=1.8,
        users=SMITHY, skill=6, head=True, equipped={"SocialImpact": 0.03}, pargs={"kind": "winged"})

# ------------------------------------------------------------------ buildings, floors and goods
GARDEN = deco(NATION, "Garden", "paradise garden", "cennet bahçesi",
              "A small walled garden in four parts, split by water channels around a central pool and planted with roses and cypress. Colonists come to sit by the water and calm down.",
              "Ortadaki bir havuzun çevresinde su kanallarıyla dörde bölünmüş, güller ve servilerle dikili küçük, duvarlı bir bahçe. Kolonistler suyun kenarında oturup sakinleşmeye gelir.",
              R_GARDEN, (2, 2), "pars_garden", beauty=28, work=6000, stuff=("Stony",), stuff_count=120, cost={"WoodLog": 30}, hp=300,
              category="Art", joy="Meditative", minify=False)
add("Things/HE_Buildings_Pars.xml", Def("JobDef", "HE_SitInGarden", driverClass="JobDriver_SitFacingBuilding",
                                        reportString=T("resting in the garden.", "bahçede dinleniyor."), joyDuration=4000, joyMaxParticipants=4,
                                        joyKind="Meditative", allowOpportunisticPrefix=True))
add("Things/HE_Buildings_Pars.xml", Def("JoyGiverDef", "HE_Garden", giverClass="JoyGiver_InteractBuildingSitAdjacent", baseChance=3,
                                        requireChair=False, thingDefs=[GARDEN], jobDef="HE_SitInGarden", joyKind="Meditative",
                                        requiredCapacities=["Sight"]))

deco(NATION, "PostLamp", "post station lamp", "menzil feneri",
     "A pierced bronze lamp on a tall post, the kind hung at every royal post station so riders can find it in the dark.",
     "Uzun bir direğin üzerinde delikli bronz bir fener; ulaklar karanlıkta bulabilsin diye her kraliyet menziline asılanlardan.",
     R_POST, (1, 1), "post_lamp", beauty=5, work=1800, stuff=("Metallic",), stuff_count=25, cost={"WoodLog": 10}, hp=120,
     glow=(7, "(255,170,90,0)"), category="Art", draw_size="(1,1.6)", extra={"tickerType": "Normal"},
     comps=[{"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": 1.0, "fuelCapacity": 10, "fuelFilter": {"thingDefs": ["WoodLog"]},
             "initialFuelPercent": 1, "showAllowAutoRefuelToggle": True}])

CARPET = resource(NATION, "Carpet", "Parsian carpet", "Pars halısı",
                  "A thick hand-knotted carpet of wool in deep red, indigo and ivory, with a garden pattern in the middle. Every court in the world wants one.",
                  "Ortasında bahçe deseni olan, koyu kırmızı, çivit ve fildişi renklerinde, elle düğümlenmiş kalın bir yün halı. Dünyadaki her saray bir tane ister.",
                  240, "goods4", mass=3, stack=10, knowledge=2, pargs={"kind": "carpet"})
LOOM = "HE_Pars_CarpetLoom"
add("Things/HE_Buildings_Pars.xml", Def(
    "ThingDef", LOOM, parent="BenchBase",
    label=T("carpet loom", "halı tezgâhı"),
    description=T("An upright wooden loom strung with warp threads, with balls of dyed wool hanging from its beam. It knots cloth or wool into Parsian carpets.",
                  "Çözgü iplikleriyle gerilmiş, kirişinden boyalı yün yumakları sarkan dik, ahşap bir tezgâh. Kumaşı ya da yünü Pars halılarına düğümler."),
    thingClass="Building_WorkTable",
    graphicData={"texPath": f"HeirsOfEarth/Buildings/{LOOM}", "graphicClass": "Graphic_Single", "drawSize": "(2,1)",
                 "damageData": {"cornerTL": "Damage/Corner", "cornerTR": "Damage/Corner", "cornerBL": "Damage/Corner", "cornerBR": "Damage/Corner"}},
    castEdgeShadows=True, staticSunShadowHeight=0.25,
    costList={"WoodLog": 80},
    stuffCategories=["Woody"], costStuffCount=40,
    altitudeLayer="Building", fillPercent=0.5, useHitPoints=True,
    statBases={"WorkToBuild": 2600, "MaxHitPoints": 140, "Flammability": 1.0, "Cleanliness": -2, "Mass": 30},
    size="(2,1)", designationCategory="Production", passability="PassThroughOnly", pathCost=50,
    hasInteractionCell=True, interactionCellOffset="(0,0,-1)", surfaceType="Item",
    researchPrerequisites=[R_LOOM],
    inspectorTabs=["ITab_Bills"],
    building={"spawnedConceptLearnOpportunity": "BillsTab"},
    placeWorkers=["PlaceWorker_PreventInteractionSpotOverlap"],
    modExtensions=[culture(NATION)]))
tex(f"HeirsOfEarth/Buildings/{LOOM}", "carpet_loom", size=(2, 1))
WOOLS = ["Cloth", "WoolSheep", "WoolAlpaca", "WoolMuffalo", "WoolBison", "WoolMegasloth"]
add("Things/HE_Buildings_Pars.xml", Def(
    "RecipeDef", "HE_Pars_WeaveCarpet",
    label=T("weave a Parsian carpet", "Pars halısı doku"),
    description=T("Knot 60 cloth or wool into one Parsian carpet.", "60 kumaş ya da yünü düğümleyerek bir Pars halısı doku."),
    jobString=T("Weaving a carpet.", "Halı dokuyor."),
    workAmount=9000, workSpeedStat="GeneralLaborSpeed", workSkill="Crafting", effectWorking="Tailor", soundWorking="Recipe_Tailor",
    ingredients=[{"filter": {"thingDefs": WOOLS}, "count": 60}],
    fixedIngredientFilter={"thingDefs": WOOLS},
    products={CARPET: 1}, skillRequirements={"Crafting": 6}, workSkillLearnFactor=0.5,
    recipeUsers=[LOOM], researchPrerequisite=R_LOOM))

floor(NATION, "GirihTiles", "girih tiles", "girih çinileri",
      "Glazed tiles in turquoise, cobalt and white, laid in an endless pattern of ten-pointed stars.",
      "Turkuaz, kobalt ve beyaz sırlı çiniler; on köşeli yıldızlardan oluşan sonsuz bir desenle döşenmiş.",
      R_GARDEN, "floor_girih", beauty=4, cost={"BlocksSandstone": 4, "Silver": 2}, work=1400)

# ------------------------------------------------------------------ food
food(NATION, "Pilaf", "saffron pilaf", "safranlı pilav",
     "A mound of long-grain rice steamed with saffron and butter, topped with barberries, pistachios and a piece of its own golden crust.",
     "Safran ve tereyağıyla demlenmiş, üstü kızamık üzümü, antep fıstığı ve kendi altın kabuğundan bir parçayla süslenmiş uzun taneli pirinç tepesi.",
     R_PILAF, "food4", nutrition=0.9, value=22, rot_days=5, pargs={"kind": "pilaf"})
