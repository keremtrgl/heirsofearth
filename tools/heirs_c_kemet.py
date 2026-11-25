"""Kingdom of New Kemet (3.0): nation, research branch, weapons, armour, buildings, floors and food.

Kemet is the river nation: farming, stonework and hot climates. Its signature pieces are the khopesh, the composite
bow, the obelisk, the papyrus workshop and irrigated silt, a floor that turns plain soil into better farmland.
"""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, culture, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Kemet"
FN = "Nations/HE_Kemet.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Kemet",
                 label=T("Kingdom of New Kemet", "Yeni Kemet Krallığı"),
                 description=T("The colony ship Iteru came down beside a great river in a land of red sand, and its people did what their ancestors had done: they measured the flood, dug canals and built in stone. New Kemet is an old-fashioned kingdom of farmers, scribes and stonemasons, proud, patient and very hard to starve. They count the Hellenes as friends and trade with everyone who brings timber.",
                               "Iteru koloni gemisi kızıl kumlu bir ülkede büyük bir nehrin kıyısına indi ve halkı atalarının yaptığını yaptı: taşkını ölçtü, kanallar kazdı ve taştan inşa etti. Yeni Kemet; çiftçilerin, kâtiplerin ve taş ustalarının gururlu, sabırlı ve aç bırakılması çok zor, eski usul bir krallığıdır. Hellenleri dost sayar ve kereste getiren herkesle ticaret yaparlar."),
                 color="(0.80, 0.62, 0.24)", iconPath="HeirsOfEarth/UI/HE_Kemet",
                 rulerTitle=T("Pharaoh", "Firavun"), adjective=T("Kemetic", "Kemet"), release=3,
                 friends=["HE_Hellas"])
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Kemet", "nation_icon", color="#c99e3c", emblem="falcon")

# ------------------------------------------------------------------ research: Neolithic
R_SPEAR = research(NATION, "Spear", "river spear", "nehir mızrağı",
                   "A light spear with a socketed bronze head, carried by every levy that marches out when the flood is low.",
                   "Taşkın çekildiğinde yola çıkan her askerin taşıdığı, soketli bronz uçlu hafif bir mızrak.",
                   450, "Neolithic", 0, 0)
R_KALASIRIS = research(NATION, "Kalasiris", "kalasiris", "kalasiris",
                       "Weave fine linen into the long sheath dress worn in the heat of the river valley.",
                       "İnce keteni nehir vadisinin sıcağında giyilen uzun, dar elbiseye doku.",
                       400, "Neolithic", 1, 0)
R_IRRIGATION = research(NATION, "Irrigation", "irrigation", "sulama",
                        "Dig shallow canals, carry the river's black silt onto the fields and let the water do the rest.",
                        "Sığ kanallar kaz, nehrin kara balçığını tarlalara taşı ve gerisini suya bırak.",
                        550, "Neolithic", 2, 0)
R_BOW = research(NATION, "CompositeBow", "composite bow", "kompozit yay",
                 "Glue horn, wood and sinew into a short, angled bow that shoots further than a plain stave.",
                 "Boynuz, ahşap ve siniri yapıştırarak düz bir yaydan daha uzağa atan kısa, köşeli bir yay yap.",
                 550, "Neolithic", 0, 1, prereqs=[R_SPEAR])
R_BREAD = research(NATION, "Bread", "date bread", "hurmalı ekmek",
                   "Bake round loaves of emmer and dates in clay moulds, with onions and soft cheese on the side.",
                   "Kızıl buğday ve hurmadan yuvarlak somunları kil kalıplarda pişir; yanına soğan ve yumuşak peynir koy.",
                   400, "Neolithic", 1, 1, prereqs=[R_KALASIRIS])
R_RIVER = research(NATION, "RiverSoil", "gift of the river", "nehrin armağanı",
                   "Every field is measured after the flood and planted in the same week. Nothing grows by luck in Kemet.",
                   "Her tarla taşkından sonra ölçülür ve aynı hafta ekilir. Kemet'te hiçbir şey şans eseri yetişmez.",
                   750, "Neolithic", 2, 1, prereqs=[R_IRRIGATION], knowledge=15, tradition=True,
                   stats=[("PlantHarvestYield", 0, 1.08, "Colonists")],
                   effect=T("Colonists harvest 8% more from every plant.", "Kolonistler her bitkiden %8 daha fazla ürün toplar."))
R_SCRIBES = research(NATION, "Scribes", "house of scribes", "kâtipler evi",
                     "Children who can write are taught to write well, to count grain and to copy the old books without a single error.",
                     "Yazabilen çocuklara iyi yazmak, tahıl saymak ve eski kitapları tek bir hata yapmadan kopyalamak öğretilir.",
                     750, "Neolithic", 0, 2, prereqs=[R_BOW], knowledge=15, tradition=True,
                     stats=[("GlobalLearningFactor", 0.07, 1, "Colonists")],
                     effect=T("Colonists learn 7% faster.", "Kolonistler %7 daha hızlı öğrenir."))
R_CALENDAR = research(NATION, "SunCalendar", "sun calendar", "güneş takvimi",
                      "Three seasons of four months, read from the rising of one bright star. Sowing and reaping happen on the right day.",
                      "Parlak bir yıldızın doğuşundan okunan, dörder aylık üç mevsim. Ekim ve hasat doğru günde yapılır.",
                      800, "Neolithic", 1, 2, prereqs=[R_BREAD], knowledge=20, tradition=True,
                      stats=[("PlantWorkSpeed", 0, 1.07, "Colonists")],
                      effect=T("Colonists sow and harvest 7% faster.", "Kolonistler %7 daha hızlı eker ve hasat eder."))
R_OBELISK = research(NATION, "Obelisk", "obelisks", "dikili taşlar",
                     "Quarry a single needle of stone, raise it with ramps and ropes and cap it with gold that catches the first light.",
                     "Tek parça bir taş iğnesi çıkar, rampalar ve halatlarla dik ve ilk ışığı yakalayan altınla taçlandır.",
                     700, "Neolithic", 2, 2, prereqs=[R_RIVER], knowledge=10)
# ------------------------------------------------------------------ research: Medieval
R_KHOPESH = research(NATION, "Khopesh", "khopesh", "hopeş",
                     "Forge the sickle-sword of the chariot corps, a blade that hooks shields aside and cuts like an axe.",
                     "Kalkanları yana çeken ve balta gibi kesen, savaş arabası birliğinin orak-kılıcını döv.",
                     900, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_PAPYRUS = research(NATION, "Papyrus", "papyrus workshop", "papirüs atölyesi",
                     "Split river reeds, lay them crosswise, beat them flat and dry them in the sun: the writing sheet of a whole civilisation.",
                     "Nehir sazlarını yar, çaprazlama diz, düzleşene kadar döv ve güneşte kurut: bütün bir uygarlığın yazı yaprağı.",
                     900, "Medieval", 1, 0, prereqs=[R_SCRIBES], knowledge=15)
R_MASONS = research(NATION, "Stonemasons", "royal stonemasons", "kraliyet taş ustaları",
                    "Copper saws, sand and patience. Kemetic masons dress a wall so smooth that a knife blade will not slide between the blocks.",
                    "Bakır testereler, kum ve sabır. Kemet ustaları bir duvarı o kadar düzgün yontar ki taşların arasına bıçak ağzı girmez.",
                    1100, "Medieval", 2, 0, prereqs=[R_OBELISK], knowledge=25, tradition=True,
                    stats=[("SmoothingSpeed", 0, 1.20, "Colonists"), ("MiningSpeed", 0, 1.05, "Colonists")],
                    effect=T("Colonists smooth stone 20% faster and mine 5% faster.", "Kolonistler taşı %20 daha hızlı düzler ve %5 daha hızlı kazı yapar."))
R_CHARIOT = research(NATION, "ChariotCorps", "chariot corps", "savaş arabası birliği",
                     "The war crown of blue leather and the scale corselet of the charioteers, made to turn arrows on the move.",
                     "Mavi deriden savaş tacı ve hareket halindeyken okları savuşturmak için yapılmış arabacı pullu göğüslüğü.",
                     1200, "Medieval", 0, 1, prereqs=[R_KHOPESH], knowledge=25)
R_SUN = research(NATION, "ChildrenOfSun", "children of the sun", "güneşin çocukları",
                 "Linen, shade at noon, water in the morning and a nap in the heat. Kemetians work where others faint.",
                 "Keten, öğlen gölge, sabah su ve sıcakta bir şekerleme. Kemetliler başkalarının bayıldığı yerde çalışır.",
                 1000, "Medieval", 1, 1, prereqs=[R_PAPYRUS], knowledge=25, tradition=True,
                 stats=[("ComfyTemperatureMax", 5, 1, "Colonists")],
                 effect=T("Colonists are comfortable in 5°C more heat.", "Kolonistler 5°C daha sıcakta rahat eder."))
R_KITCHENS = research(NATION, "RoyalKitchens", "royal kitchens", "kraliyet mutfakları",
                      "Clean water, covered jars and cooks who wash their hands. The palace kitchens feed a thousand and poison no one.",
                      "Temiz su, kapalı küpler ve ellerini yıkayan aşçılar. Saray mutfakları bin kişiyi doyurur ve kimseyi zehirlemez.",
                      1000, "Medieval", 2, 1, prereqs=[R_MASONS], knowledge=25, tradition=True,
                      stats=[("FoodPoisonChance", 0, 0.6, "Colonists"), ("CookSpeed", 0, 1.05, "Colonists")],
                      effect=T("Meals cooked by colonists are 40% less likely to cause food poisoning and colonists cook 5% faster.",
                               "Kolonistlerin pişirdiği yemeklerin zehirleme ihtimali %40 düşer ve kolonistler %5 daha hızlı pişirir."))
R_MEDJAY = research(NATION, "Medjay", "medjay patrols", "medjay devriyeleri",
                    "Desert scouts who run all day and shoot from the hip. They guard the tombs, the roads and the borders.",
                    "Bütün gün koşan ve belden ateş eden çöl izcileri. Mezarları, yolları ve sınırları korurlar.",
                    1300, "Medieval", 0, 2, prereqs=[R_CHARIOT], knowledge=35, tradition=True,
                    stats=[("MoveSpeed", 0, 1.02, "Colonists"), ("AimingDelayFactor", 0, 0.95, "Colonists")],
                    effect=T("Colonists move 2% faster and aim 5% faster.", "Kolonistler %2 daha hızlı yürür ve %5 daha hızlı nişan alır."))
R_SENET = research(NATION, "Senet", "senet", "senet",
                   "A board of thirty squares, five pieces each and four throwing sticks. Kings were buried with their sets.",
                   "Otuz kareli bir tahta, beşer taş ve dört atma çubuğu. Krallar setleriyle birlikte gömülürdü.",
                   700, "Medieval", 1, 2, prereqs=[R_SUN], knowledge=10)
# ------------------------------------------------------------------ research: Industrial
R_RIFLE = research(NATION, "DesertRifle", "desert rifle", "çöl tüfeği",
                   "A long rifle with a slim brass-bound stock, sighted for the open distances of the desert edge.",
                   "Çöl kenarının açık mesafelerine göre gez-arpacığı ayarlanmış, ince ve pirinç bağlı dipçikli uzun bir tüfek.",
                   1500, "Industrial", 0, 0, prereqs=["Gunsmithing", R_KHOPESH], knowledge=35)
R_ENGINEERING = research(NATION, "NileEngineering", "river engineering", "nehir mühendisliği",
                         "Dams, sluices and steam pumps. The old canals are rebuilt in iron and the flood answers to a timetable.",
                         "Barajlar, savaklar ve buharlı pompalar. Eski kanallar demirden yeniden yapılır ve taşkın bir tarifeye uyar.",
                         1700, "Industrial", 2, 0, prereqs=[R_KITCHENS], knowledge=45, tradition=True,
                         stats=[("ConstructionSpeed", 0, 1.05, "Colonists"), ("WorkSpeedGlobal", 0, 1.02, "Colonists")],
                         effect=T("Colonists build 5% faster and work 2% faster.", "Kolonistler %5 daha hızlı inşa eder ve %2 daha hızlı çalışır."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Spear", "river spear", "nehir mızrağı",
      "A light spear of acacia wood with a socketed bronze head shaped like a lotus leaf.",
      "Nilüfer yaprağı biçiminde soketli bronz bir ucu olan, akasya ağacından hafif bir mızrak.",
      "Neolithic", R_SPEAR, [tool("shaft", "Blunt", 8, 2.0), tool("point", "Stab", 18, 2.1, 0.30)],
      mass=1.6, work=7000, painter="spear_long", stuff=("Metallic", "Woody"), stuff_count=40, skill=3, angle=-45,
      extra_tags=["NeolithicMeleeDecent"], pargs={"head": "lotus", "shaft": "#8a6238"})
melee(NATION, "Khopesh", "khopesh", "hopeş",
      "A bronze-coloured sickle-sword whose curved outer edge bites like an axe and whose hook pulls shields and spears aside.",
      "Kıvrık dış ağzı balta gibi ısıran ve kancası kalkanları ve mızrakları yana çeken bronz renkli bir orak-kılıç.",
      "Medieval", R_KHOPESH, [tool("handle", "Blunt", 9, 2), tool("edge", "Cut", 21, 2.1, 0.30), tool("spike", "Blunt", 11, 2.0)],
      mass=1.5, work=14000, painter="khopesh", stuff_count=60, skill=5, angle=-45, extra_tags=["MedievalMeleeAdvanced"])
ARROW = projectile("HE_Arrow_Kemet", "reed arrow", "kamış ok", "Arrow", 12, 50, "Things/Projectile/Arrow_Small", pen=0.16)
ranged(NATION, "CompositeBow", "composite bow", "kompozit yay",
       "A short, angled bow of horn, wood and sinew, painted with lotus bands. Charioteers shoot it from a moving platform.",
       "Nilüfer şeritleriyle boyanmış, boynuz, ahşap ve sinirden kısa, köşeli bir yay. Arabacılar onu hareket eden bir platformdan atar.",
       "Neolithic", R_BOW, ARROW, 1.2, 28.9, 1.35, (0.6, 0.7, 0.62, 0.5), 1.0, 8500, "composite_bow",
       {"WoodLog": 40}, extra_tags=["NeolithicRangedDecent"])
RIFLE_BALL = projectile("HE_Bullet_DesertRifle", "desert rifle bullet", "çöl tüfeği mermisi", "Bullet", 17, 74, "Things/Projectile/Bullet_Small", pen=0.26)
ranged(NATION, "DesertRifle", "desert rifle", "çöl tüfeği",
       "A long, slim rifle with a brass-bound stock and a falcon engraved on the lock. Slow to aim, but deadly across open ground.",
       "Pirinç bağlı dipçikli ve kilidinde oyma bir şahin olan uzun, ince bir tüfek. Nişan alması yavaş, ama açık arazide ölümcül.",
       "Industrial", R_RIFLE, RIFLE_BALL, 1.8, 30.9, 2.2, (0.4, 0.62, 0.66, 0.5), 4.0, 18000, "desert_rifle",
       {"Steel": 60, "WoodLog": 25, "ComponentIndustrial": 1}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       klass=("Ranged", "RangedHeavy", "LongShots"), weapon_tags=["HE_KemetGuns"], tools=[tool("stock", "Blunt", 9, 2), tool("barrel", "Blunt", 8, 2)])

# ------------------------------------------------------------------ apparel
apparel(NATION, "Kalasiris", "kalasiris", "kalasiris",
        "A long sheath dress of pleated linen with a broad beaded collar. Cool in the worst heat and handsome at court.",
        "Geniş boncuklu yakalı, pliseli ketenden uzun ve dar bir elbise. En kötü sıcakta serin, sarayda yakışıklı.",
        "Neolithic", R_KALASIRIS, "TribalA/TribalA", ["OnSkin"], ["Torso", "Shoulders", "Legs"],
        {"MaxHitPoints": 100, "StuffEffectMultiplierArmor": 0.12, "StuffEffectMultiplierInsulation_Cold": 0.25, "StuffEffectMultiplierInsulation_Heat": 0.8},
        "torso3", stuff=("Fabric",), stuff_count=55, work=3600, mass=0.5, equipped={"SocialImpact": 0.02}, pargs={"kind": "kalasiris"})
apparel(NATION, "Corselet", "scale corselet", "pullu göğüslük",
        "A leather corselet covered in overlapping bronze scales, made for charioteers who need their arms free to shoot.",
        "Üst üste binen bronz pullarla kaplı deri bir göğüslük; ok atmak için kollarını serbest tutması gereken arabacılar için yapıldı.",
        "Medieval", R_CHARIOT, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck"],
        {"MaxHitPoints": 190, "StuffEffectMultiplierArmor": 0.5, "StuffEffectMultiplierInsulation_Cold": 0.15, "StuffEffectMultiplierInsulation_Heat": 0.1},
        "torso3", parent="ArmorSmithableBase", stuff=("Leathery",), stuff_count=90, cost={"Steel": 45}, work=19000, mass=5.0,
        users=SMITHY, skill=5, equipped={"MoveSpeed": -0.06}, tags=["MedievalMilitary"], pargs={"kind": "corselet"})
apparel(NATION, "Khepresh", "khepresh war crown", "hepreş savaş tacı",
        "A tall war crown of blue-dyed leather studded with bronze discs, worn by chariot captains. It turns a glancing blow and is seen across a battlefield.",
        "Bronz disklerle süslenmiş, maviye boyanmış deriden uzun bir savaş tacı; araba kaptanları giyer. Sıyıran bir darbeyi savuşturur ve savaş alanının öbür ucundan görülür.",
        "Medieval", R_CHARIOT, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 100, "StuffEffectMultiplierArmor": 0.35, "StuffEffectMultiplierInsulation_Cold": 0.1, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet3", parent="ArmorHelmetMakeableBase", stuff=("Leathery",), stuff_count=40, cost={"Steel": 10}, work=4200, mass=1.2,
        users=SMITHY, skill=5, head=True, equipped={"SocialImpact": 0.03}, pargs={"kind": "khepresh"})

# ------------------------------------------------------------------ buildings, floors and the senet table
deco(NATION, "Obelisk", "obelisk", "dikili taş",
     "A single needle of dressed stone covered in carved columns of signs and capped with a gilded point that shines at sunrise.",
     "Oyma işaret sütunlarıyla kaplı, gün doğumunda parlayan yaldızlı bir uçla taçlanmış tek parça yontulmuş bir taş iğnesi.",
     R_OBELISK, (1, 1), "obelisk", beauty=22, work=8000, stuff=("Stony",), stuff_count=160, cost={"Gold": 5}, hp=400,
     category="Art", draw_size="(1,2.4)")
deco(NATION, "SenetTable", "senet table", "senet masası",
     "A low table of ebony and ivory with a board of thirty squares and a drawer for the pieces. Two colonists sit at it to play.",
     "Otuz kareli bir tahtası ve taşlar için bir çekmecesi olan, abanoz ve fildişinden alçak bir masa. İki kolonist oynamak için başına oturur.",
     R_SENET, (2, 1), "senet_table", beauty=4, work=3000, stuff=("Woody", "Stony"), stuff_count=60, hp=120, joy="Gaming_Cerebral")
add("Things/HE_Buildings_Kemet.xml", Def("JobDef", "HE_PlaySenet", driverClass="JobDriver_SitFacingBuilding",
                                         reportString=T("playing senet.", "senet oynuyor."), joyDuration=4000, joyMaxParticipants=2,
                                         joyKind="Gaming_Cerebral", joySkill="Intellectual", joyXpPerTick=0.002, allowOpportunisticPrefix=True))
add("Things/HE_Buildings_Kemet.xml", Def("JoyGiverDef", "HE_Senet", giverClass="JoyGiver_InteractBuildingSitAdjacent", baseChance=3,
                                         requireChair=False, thingDefs=["HE_Kemet_SenetTable"], jobDef="HE_PlaySenet", joyKind="Gaming_Cerebral",
                                         requiredCapacities=["Sight", "Manipulation"]))

PAPYRUS = resource(NATION, "Papyrus", "papyrus", "papirüs",
                   "Sheets of pale writing paper made from river reeds. Scribes, traders and every culture table want it.",
                   "Nehir sazlarından yapılmış soluk yazı kâğıdı yaprakları. Kâtipler, tüccarlar ve her kültür masası onu ister.",
                   5, "goods3", mass=0.05, stack=100, knowledge=1, pargs={"kind": "papyrus"})
WORKSHOP = "HE_Kemet_PapyrusWorkshop"
add("Things/HE_Buildings_Kemet.xml", Def(
    "ThingDef", WORKSHOP, parent="BenchBase",
    label=T("papyrus workshop", "papirüs atölyesi"),
    description=T("A reed-splitting table, a beating stone and drying racks. It turns dried grass and reeds into papyrus sheets.",
                  "Bir saz yarma masası, bir dövme taşı ve kurutma rafları. Kurutulmuş otu ve sazı papirüs yapraklarına çevirir."),
    thingClass="Building_WorkTable",
    graphicData={"texPath": f"HeirsOfEarth/Buildings/{WORKSHOP}", "graphicClass": "Graphic_Single", "drawSize": "(2,1)",
                 "damageData": {"cornerTL": "Damage/Corner", "cornerTR": "Damage/Corner", "cornerBL": "Damage/Corner", "cornerBR": "Damage/Corner"}},
    castEdgeShadows=True, staticSunShadowHeight=0.15,
    costList={"WoodLog": 60},
    stuffCategories=["Stony", "Woody"], costStuffCount=40,
    altitudeLayer="Building", fillPercent=0.4, useHitPoints=True,
    statBases={"WorkToBuild": 2200, "MaxHitPoints": 140, "Flammability": 1.0, "Cleanliness": -2, "Mass": 25},
    size="(2,1)", designationCategory="Production", passability="PassThroughOnly", pathCost=50,
    hasInteractionCell=True, interactionCellOffset="(0,0,-1)", surfaceType="Item",
    researchPrerequisites=[R_PAPYRUS],
    inspectorTabs=["ITab_Bills"],
    building={"spawnedConceptLearnOpportunity": "BillsTab"},
    placeWorkers=["PlaceWorker_PreventInteractionSpotOverlap"],
    modExtensions=[culture(NATION)]))
tex(f"HeirsOfEarth/Buildings/{WORKSHOP}", "papyrus_bench", size=(2, 1))
add("Things/HE_Buildings_Kemet.xml", Def(
    "RecipeDef", "HE_Kemet_MakePapyrus",
    label=T("make papyrus", "papirüs yap"),
    description=T("Split, lay and beat 25 hay into 10 sheets of papyrus.", "25 kuru otu yarıp dizerek ve döverek 10 papirüs yaprağı yap."),
    jobString=T("Making papyrus.", "Papirüs yapıyor."),
    workAmount=1400, workSpeedStat="GeneralLaborSpeed", workSkill="Crafting", effectWorking="Tailor", soundWorking="Recipe_Tailor",
    ingredients=[{"filter": {"thingDefs": ["Hay"]}, "count": 25}],
    fixedIngredientFilter={"thingDefs": ["Hay"]},
    products={PAPYRUS: 10}, skillRequirements={"Crafting": 3},
    recipeUsers=[WORKSHOP], researchPrerequisite=R_PAPYRUS))

floor(NATION, "Silt", "irrigated silt", "sulanmış balçık",
      "Black river silt spread over soil and laced with small canals. Plants grow on it as on rich soil, a little less. It can only be laid on soil.",
      "Toprağın üstüne serilmiş ve küçük kanallarla örülmüş kara nehir balçığı. Bitkiler üzerinde neredeyse verimli toprakta olduğu gibi yetişir. Sadece toprağın üstüne serilebilir.",
      R_IRRIGATION, "floor_silt", beauty=0, cost={"WoodLog": 2}, work=1500, fertility=1.25, needs="GrowSoil", cleanliness=-0.5)
floor(NATION, "LotusTiles", "lotus tiles", "nilüfer çinileri",
      "Sandstone slabs painted with blue lotus flowers and a border of reeds.",
      "Mavi nilüfer çiçekleri ve saz bordürüyle boyanmış kumtaşı levhalar.",
      R_OBELISK, "floor_lotus", beauty=3, cost={"BlocksSandstone": 4}, work=1100)

# ------------------------------------------------------------------ food
food(NATION, "Bread", "date bread", "hurmalı ekmek",
     "A round loaf of emmer wheat baked with dates and honey, served with onions, a lump of soft cheese and a cup of thin beer.",
     "Hurma ve balla pişirilmiş yuvarlak bir kızıl buğday somunu; soğan, bir parça yumuşak peynir ve bir bardak hafif biranın yanında sunulur.",
     R_BREAD, "food3", nutrition=0.9, value=21, rot_days=6, pargs={"kind": "bread"})
