"""Inti Empire (3.0): nation, research branch, weapons, armour, buildings, floors and food.

Inti is the mountain nation: terraces, storehouses, roads and records kept in knotted cords. Its signature pieces are
the sling, the star mace, the qullqa storehouse that slows rot, the quipu table that speeds research and stone
terraces that turn poor hillside ground into farmland.
"""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, culture, deco, floor, food, melee, projectile, ranged, research, tool
from heirs_xml import Def, T

NATION = "Inti"
FN = "Nations/HE_Inti.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Inti",
                 label=T("Inti Empire", "İnti İmparatorluğu"),
                 description=T("The colony ship Qhapaq came down among high mountains, on a world where the air was thin and the valleys were narrow. Its people cut the slopes into terraces, filled stone storehouses against the bad years and tied every count, census and tribute into knotted cords. The Inti Empire is orderly, hard-working and patient, and no one in it goes hungry. They have an old quarrel with Albion over the mountain mines.",
                               "Qhapaq koloni gemisi havanın ince, vadilerin dar olduğu bir dünyada yüksek dağların arasına indi. Halkı yamaçları teraslara böldü, taş ambarları kötü yıllara karşı doldurdu ve her sayımı, nüfus kaydını ve vergiyi düğümlü iplere bağladı. İnti İmparatorluğu düzenli, çalışkan ve sabırlıdır; içinde kimse aç kalmaz. Dağ madenleri yüzünden Albion'la eski bir kavgaları vardır."),
                 color="(0.78, 0.31, 0.16)", iconPath="HeirsOfEarth/UI/HE_Inti",
                 rulerTitle=T("Sapa Inti", "Sapa İnti"), adjective=T("Inti", "İnti"), release=3,
                 rivals=["HE_Albion"])
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Inti", "nation_icon", color="#c8502a", emblem="condor")

# ------------------------------------------------------------------ research: Neolithic
R_SLING = research(NATION, "Sling", "sling", "sapan",
                   "A braided wool sling and a pouch of river stones. A good slinger can break a helmet at a hundred paces.",
                   "Örgü yünden bir sapan ve bir kese dere taşı. İyi bir sapancı yüz adımdan bir miğferi kırabilir.",
                   450, "Neolithic", 0, 0)
R_UNKU = research(NATION, "Unku", "unku tunic", "unku tuniği",
                  "Weave the knee-length tunic of alpaca wool, its squares of tocapu patterns telling who the wearer is.",
                  "Alpaka yününden dize kadar uzun tuniği doku; tocapu desenli kareleri onu giyenin kim olduğunu anlatır.",
                  400, "Neolithic", 1, 0)
R_TERRACES = research(NATION, "Terraces", "terraces", "teraslar",
                      "Cut the hillside into steps, wall each one with stone and fill it with carried soil. A slope becomes a field.",
                      "Yamacı basamaklara böl, her birini taşla duvarla ve taşınan toprakla doldur. Bir yamaç tarlaya dönüşür.",
                      600, "Neolithic", 2, 0)
R_CHASKI = research(NATION, "Chaski", "chaski runners", "çaski koşucuları",
                    "Relay runners posted along every road, a conch to announce themselves and a quipu to carry. A message crosses the empire in days.",
                    "Her yol boyunca konuşlanmış bayrak koşucuları; kendilerini duyurmak için bir deniz kabuğu ve taşımak için bir quipu. Bir haber imparatorluğu günler içinde geçer.",
                    750, "Neolithic", 0, 1, prereqs=[R_SLING], knowledge=15, tradition=True,
                    stats=[("MoveSpeed", 0, 1.03, "Colonists")],
                    effect=T("Colonists move 3% faster.", "Kolonistler %3 daha hızlı yürür."))
R_PACHAMANCA = research(NATION, "Pachamanca", "pachamanca", "paçamanka",
                        "Heat stones in a pit, lay meat, potatoes and maize on them, cover everything with herbs and earth and wait.",
                        "Bir çukurda taşları ısıt, üzerlerine et, patates ve mısır koy, her şeyi otlar ve toprakla ört ve bekle.",
                        400, "Neolithic", 1, 1, prereqs=[R_UNKU])
R_AYNI = research(NATION, "Ayni", "ayni", "ayni",
                  "Today I help you dig your field, tomorrow you help me roof my house. Work is lent and always repaid.",
                  "Bugün ben senin tarlanı kazmana yardım ederim, yarın sen benim damımı örtmeme. İş ödünç verilir ve her zaman geri ödenir.",
                  750, "Neolithic", 2, 1, prereqs=[R_TERRACES], knowledge=15, tradition=True,
                  stats=[("WorkSpeedGlobal", 0, 1.03, "Colonists")],
                  effect=T("Colonists work 3% faster.", "Kolonistler %3 daha hızlı çalışır."))
R_MITA = research(NATION, "Mita", "mita labour", "mita emeği",
                  "Every household sends workers to the state for part of the year: roads, bridges, temples and storehouses rise as if by themselves.",
                  "Her hane yılın bir kısmında devlete işçi gönderir: yollar, köprüler, tapınaklar ve ambarlar kendiliğinden yükselir gibi.",
                  800, "Neolithic", 0, 2, prereqs=[R_CHASKI], knowledge=20, tradition=True,
                  stats=[("ConstructionSpeed", 0, 1.05, "Colonists"), ("MiningSpeed", 0, 1.05, "Colonists")],
                  effect=T("Colonists build 5% faster and mine 5% faster.", "Kolonistler %5 daha hızlı inşa eder ve %5 daha hızlı kazı yapar."))
R_QULLQA = research(NATION, "Qullqa", "qullqa storehouses", "qullqa ambarları",
                    "Round stone storehouses on windy slopes, vented at the floor and roofed with thatch. Grain and dried food keep in them for years.",
                    "Rüzgârlı yamaçlarda, tabandan havalandırılan ve sazla örtülen yuvarlak taş ambarlar. Tahıl ve kurutulmuş yiyecek içlerinde yıllarca dayanır.",
                    700, "Neolithic", 1, 2, prereqs=[R_PACHAMANCA], knowledge=10)
R_ALTITUDE = research(NATION, "HighAltitude", "children of the heights", "yükseklerin çocukları",
                      "Broad chests, coca tea, wool and the habit of cold mornings. Inti people work where lowlanders shiver.",
                      "Geniş göğüsler, koka çayı, yün ve soğuk sabahlara alışkanlık. İnti halkı ovalıların titrediği yerde çalışır.",
                      800, "Neolithic", 2, 2, prereqs=[R_AYNI], knowledge=20, tradition=True,
                      stats=[("ComfyTemperatureMin", -6, 1, "Colonists")],
                      effect=T("Colonists are comfortable in 6°C more cold.", "Kolonistler 6°C daha soğukta rahat eder."))
# ------------------------------------------------------------------ research: Medieval
R_CHAMPI = research(NATION, "Champi", "star mace", "yıldız topuz",
                    "Cast a bronze head with six points and set it on a hardwood staff: the champi of the imperial army.",
                    "Altı uçlu bronz bir baş dök ve sert ağaçtan bir sapa tak: imparatorluk ordusunun champisi.",
                    900, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_QUIPU = research(NATION, "Quipu", "quipu", "quipu",
                   "Cords of coloured wool knotted in tens, hundreds and thousands, hung from a main cord. Census, tribute and history in one bundle.",
                   "Onluk, yüzlük ve binlik düğümlerle bağlanmış, ana bir ipe asılı renkli yün iplikler. Nüfus, vergi ve tarih tek bir demette.",
                   1000, "Medieval", 1, 0, prereqs=[R_QULLQA], knowledge=15)
R_ANDEAN = research(NATION, "MountainFarming", "mountain farming", "dağ tarımı",
                    "A hundred kinds of potato, each for its own height and season, and fields rotated so the soil never tires.",
                    "Her biri kendi yüksekliği ve mevsimi için yüz çeşit patates ve toprak hiç yorulmasın diye nöbetleşe ekilen tarlalar.",
                    1100, "Medieval", 2, 0, prereqs=[R_ALTITUDE], knowledge=25, tradition=True,
                    stats=[("PlantHarvestYield", 0, 1.05, "Colonists"), ("PlantWorkSpeed", 0, 1.03, "Colonists")],
                    effect=T("Colonists harvest 5% more and sow and harvest 3% faster.", "Kolonistler %5 daha fazla hasat eder ve %3 daha hızlı eker ve hasat eder."))
R_GUARD = research(NATION, "RoyalGuard", "royal guard", "kraliyet muhafızları",
                   "The quilted war tunic and the plumed helmet of the guard who carry the emperor's litter.",
                   "İmparatorun tahtırevanını taşıyan muhafızların kapitone savaş tuniği ve tüylü miğferi.",
                   1200, "Medieval", 0, 1, prereqs=[R_CHAMPI], knowledge=25)
R_KEEPERS = research(NATION, "KnotKeepers", "keepers of the knots", "düğüm bekçileri",
                     "The khipukamayuq, trained from childhood to tie and read the cords. Nothing counted in the empire is ever forgotten.",
                     "Çocukluktan beri ipleri bağlamak ve okumak için yetiştirilen khipukamayuqlar. İmparatorlukta sayılan hiçbir şey asla unutulmaz.",
                     1100, "Medieval", 1, 1, prereqs=[R_QUIPU], knowledge=25, tradition=True,
                     stats=[("ResearchSpeed", 0, 1.06, "Colonists")],
                     effect=T("Colonists research 6% faster.", "Kolonistler %6 daha hızlı araştırma yapar."))
R_HEALERS = research(NATION, "Kallawaya", "kallawaya healers", "kallawaya şifacıları",
                     "Wandering herbalists who know a thousand plants of the mountains and the forest below them.",
                     "Dağların ve altlarındaki ormanın bin bitkisini bilen gezgin şifacılar.",
                     1100, "Medieval", 2, 1, prereqs=[R_ANDEAN], knowledge=25, tradition=True,
                     stats=[("MedicalTendQuality", 0.05, 1, "Colonists")],
                     effect=T("Colonists tend wounds and illness 5% better.", "Kolonistler yaraları ve hastalıkları %5 daha iyi tedavi eder."))
R_SLINGERS = research(NATION, "Slingers", "slingers of the heights", "yükseklerin sapancıları",
                      "Boys and girls of the mountains learn to sling before they learn to herd. In battle the stones come down like hail.",
                      "Dağların oğlanları ve kızları sürü gütmeyi öğrenmeden önce sapan atmayı öğrenir. Savaşta taşlar dolu gibi yağar.",
                      1300, "Medieval", 0, 2, prereqs=[R_GUARD], knowledge=35, tradition=True,
                      stats=[("ShootingAccuracyPawn", 1, 1, "Colonists"), ("AimingDelayFactor", 0, 0.96, "Colonists")],
                      effect=T("Colonists shoot 1 point more accurately and aim 4% faster.", "Kolonistler 1 puan daha isabetli ateş eder ve %4 daha hızlı nişan alır."))
# ------------------------------------------------------------------ research: Industrial
R_CARBINE = research(NATION, "Carbine", "mountain carbine", "dağ karabinası",
                     "A short, light carbine for steep ground, with a leather sling and a condor stamped on the lock.",
                     "Dik arazi için deri kayışlı ve kilidine kondor damgalı kısa, hafif bir karabina.",
                     1500, "Industrial", 0, 0, prereqs=["Gunsmithing", R_CHAMPI], knowledge=35)
R_ROADS = research(NATION, "QhapaqNan", "great road", "büyük yol",
                   "Paved roads along the ridges, rope bridges over the gorges and a resting house every day's walk. Caravans move as fast as runners.",
                   "Sırtlar boyunca taş döşeli yollar, geçitlerin üstünde halat köprüler ve her günlük yürüyüşte bir konak. Kervanlar koşucular kadar hızlı ilerler.",
                   1700, "Industrial", 2, 0, prereqs=[R_HEALERS], knowledge=45, tradition=True, caravan=0.08,
                   stats=[("ConstructionSpeed", 0, 1.03, "Colonists")],
                   effect=T("Caravans travel 8% faster and colonists build 3% faster.", "Kervanlar %8 daha hızlı gider ve kolonistler %3 daha hızlı inşa eder."))

# ------------------------------------------------------------------ weapons
STONE = projectile("HE_Stone_Inti", "sling stone", "sapan taşı", "Blunt", 10, 44, "HeirsOfEarth/Projectiles/HE_Stone_Inti", pen=0.10)
tex("HeirsOfEarth/Projectiles/HE_Stone_Inti", "sling_stone")
ranged(NATION, "Sling", "sling", "sapan",
       "A braided sling of black and white alpaca wool with a woven cradle. Cheap, light and dangerous in practised hands.",
       "Örülü bir beşiği olan, siyah ve beyaz alpaka yününden örgü bir sapan. Ucuz, hafif ve alışkın ellerde tehlikeli.",
       "Neolithic", R_SLING, STONE, 1.1, 24.9, 1.3, (0.6, 0.65, 0.5, 0.35), 0.3, 3500, "sling",
       {"Cloth": 15}, extra_tags=["NeolithicRangedBasic"])
melee(NATION, "Champi", "star mace", "yıldız topuz",
      "A six-pointed bronze star on a hardwood staff. It crushes helmets and quilted armour alike.",
      "Sert ağaçtan bir sapın ucunda altı köşeli bronz bir yıldız. Miğferleri de kapitone zırhları da ezer.",
      "Medieval", R_CHAMPI, [tool("haft", "Blunt", 9, 2), tool("head", "Blunt", 20, 2.2, 0.28)],
      mass=1.9, work=13000, painter="champi", stuff_count=60, skill=5, angle=-45, blunt=True, extra_tags=["MedievalMeleeDecent"])
CARBINE_BALL = projectile("HE_Bullet_MountainCarbine", "carbine bullet", "karabina mermisi", "Bullet", 15, 70, "Things/Projectile/Bullet_Small", pen=0.22)
ranged(NATION, "Carbine", "mountain carbine", "dağ karabinası",
       "A short, light carbine with a leather sling and a condor stamped on the lock. Quick to bring up on a narrow ledge.",
       "Deri kayışlı ve kilidine kondor damgalı kısa, hafif bir karabina. Dar bir kaya çıkıntısında çabucak omuza alınır.",
       "Industrial", R_CARBINE, CARBINE_BALL, 1.4, 27.9, 1.9, (0.55, 0.66, 0.58, 0.42), 3.0, 16000, "mountain_carbine",
       {"Steel": 50, "WoodLog": 20, "ComponentIndustrial": 1}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       klass=("Ranged", "RangedLight"), weapon_tags=["HE_IntiGuns"], tools=[tool("stock", "Blunt", 9, 2), tool("barrel", "Blunt", 8, 2)])

# ------------------------------------------------------------------ apparel
apparel(NATION, "Unku", "unku tunic", "unku tuniği",
        "A knee-length tunic of fine alpaca wool, woven with squares of tocapu patterns and a stepped band at the waist. Warm on cold mornings.",
        "İnce alpaka yününden, tocapu desenli karelerle ve belde basamaklı bir şeritle dokunmuş, dize kadar uzun bir tunik. Soğuk sabahlarda sıcak tutar.",
        "Neolithic", R_UNKU, "TribalA/TribalA", ["OnSkin"], ["Torso", "Shoulders", "Legs"],
        {"MaxHitPoints": 110, "StuffEffectMultiplierArmor": 0.15, "StuffEffectMultiplierInsulation_Cold": 0.6, "StuffEffectMultiplierInsulation_Heat": 0.25},
        "torso5", stuff=("Fabric",), stuff_count=60, work=3800, mass=0.6, equipped={"SocialImpact": 0.02}, pargs={"kind": "unku"})
apparel(NATION, "QuiltedTunic", "quilted war tunic", "kapitone savaş tuniği",
        "Layers of cotton quilted tight and soaked in brine until stiff, then faced with a chequered war pattern. Light, but it stops slings and arrows.",
        "Sıkıca kapitone edilip sertleşene kadar tuzlu suya batırılmış, sonra damalı bir savaş deseniyle kaplanmış pamuk katları. Hafif, ama sapan taşlarını ve okları durdurur.",
        "Medieval", R_GUARD, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders"],
        {"MaxHitPoints": 170, "StuffEffectMultiplierArmor": 0.52, "StuffEffectMultiplierInsulation_Cold": 0.5, "StuffEffectMultiplierInsulation_Heat": 0.2},
        "torso5", stuff=("Fabric",), stuff_count=140, work=16000, mass=3.0, skill=5, equipped={"MoveSpeed": -0.03},
        tags=["MedievalMilitary"], pargs={"kind": "quilted"})
apparel(NATION, "PlumedHelm", "plumed war helmet", "tüylü savaş miğferi",
        "A round helmet of woven cane faced with bronze, crowned with a fan of macaw feathers. Officers are seen and followed across the field.",
        "Bronzla kaplanmış örgü kamıştan, bir yelpaze ara papağanı tüyüyle taçlanmış yuvarlak bir miğfer. Subaylar savaş alanının öbür ucundan görülür ve izlenir.",
        "Medieval", R_GUARD, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 100, "StuffEffectMultiplierArmor": 0.55, "StuffEffectMultiplierInsulation_Cold": 0.15, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet5", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=35, cost={"WoodLog": 10}, work=4800, mass=1.3,
        users=SMITHY, skill=5, head=True, equipped={"SocialImpact": 0.03}, pargs={"kind": "plumed"})

# ------------------------------------------------------------------ buildings, floors
FB = "Things/HE_Buildings_Inti.xml"
QULLQA = "HE_Inti_Qullqa"
add(FB, Def(
    "ThingDef", QULLQA, parent="ShelfBase",
    label=T("qullqa storehouse", "qullqa ambarı"),
    description=T("A round stone storehouse with a thatched roof and vents at the floor, built where the wind blows. Food stored in it rots at half the normal speed. It holds three stacks per cell.",
                  "Rüzgârın estiği yere kurulmuş, sazdan çatılı ve tabanında havalandırma delikleri olan yuvarlak bir taş ambar. İçinde saklanan yiyecek normalin yarısı hızla bozulur. Her karede üç yığın tutar."),
    thingClass="Building_Storage",
    graphicData={"texPath": f"HeirsOfEarth/Buildings/{QULLQA}", "graphicClass": "Graphic_Single", "drawSize": "(2,2)"},
    size="(2,2)", rotatable=False, fillPercent=0.5,
    stuffCategories={"@Inherit": "False", "#items": ["Stony"]}, costStuffCount=90, costList={"WoodLog": 20, "Hay": 30},
    statBases={"MaxHitPoints": 300, "WorkToBuild": 4200, "Mass": 60, "Beauty": 1, "Flammability": 0.3},
    designationCategory="HE_Heritage",
    researchPrerequisites={"@Inherit": "False", "#items": [R_QULLQA]},
    building={"maxItemsInCell": 3, "preventDeteriorationOnTop": True, "ignoreStoredThingsBeauty": True,
              "blueprintClass": "Blueprint_Storage",
              "fixedStorageSettings": {"filter": {"disallowNotEverStorable": True, "categories": ["Foods", "PlantMatter"]}},
              "defaultStorageSettings": {"priority": "Important", "filter": {"categories": ["Foods"]}}},
    modExtensions=[culture(NATION), {"@Class": "HeirsOfEarth.HeirsFoodStoreExt", "rotFactor": 0.5}]))
tex(f"HeirsOfEarth/Buildings/{QULLQA}", "qullqa", size=(2, 2))
deco(NATION, "QuipuTable", "quipu table", "quipu masası",
     "A low table with a frame from which hang dozens of knotted cords in every colour, the counts of the colony. Placed near a research bench, it speeds up research by 5%.",
     "Her renkten düzinelerce düğümlü ipin, koloninin sayımlarının sarktığı bir çerçevesi olan alçak bir masa. Bir araştırma masasının yakınına konulunca araştırmayı %5 hızlandırır.",
     R_QUIPU, (2, 1), "quipu_table", beauty=5, work=2800, stuff=("Woody",), stuff_count=60, cost={"Cloth": 30}, hp=140,
     comps=[{"@Class": "CompProperties_Facility", "statOffsets": {"ResearchSpeedFactor": 0.05}, "maxSimultaneous": 1, "maxDistance": 8}],
     extra={"placeWorkers": ["PlaceWorker_ShowFacilitiesConnections"], "building": {"ai_chillDestination": False}}, file=FB)
deco(NATION, "SunStone", "sun stone", "güneş taşı",
     "A carved granite outcrop with a short post rising from it. On the two days of the year when the sun stands right above it, the post casts no shadow.",
     "Üzerinden kısa bir direk yükselen oyma bir granit kaya. Güneşin tam tepesinde durduğu yılın iki gününde direk hiç gölge düşürmez.",
     R_TERRACES, (1, 1), "sun_stone", beauty=12, work=4000, stuff=("Stony",), stuff_count=90, hp=400, category="Art", file=FB)

floor(NATION, "Terraces", "stone terraces", "taş teraslar",
      "Stepped beds of carried soil held up by dry-stone walls. Plants grow on them as on good soil. They can be laid on any diggable ground, so even gravel and stony slopes can be farmed.",
      "Kuru taş duvarlarla tutulan, taşınmış topraktan basamaklı yataklar. Bitkiler üzerlerinde iyi toprakta olduğu gibi yetişir. Kazılabilen her zemine döşenebilir, böylece çakıllı ve taşlı yamaçlar bile ekilebilir.",
      R_TERRACES, "floor_terraces", beauty=1, cost={"WoodLog": 2}, work=2200, fertility=1.0, needs="Diggable", cleanliness=-0.5)

# ------------------------------------------------------------------ food
food(NATION, "Pachamanca", "pachamanca", "paçamanka",
     "Meat, potatoes, sweet maize and broad beans cooked slowly under hot stones and herbs, served steaming with a sharp green pepper sauce.",
     "Sıcak taşlar ve otlar altında yavaşça pişirilmiş et, patates, tatlı mısır ve bakla; keskin yeşil biber sosuyla dumanı üstünde sunulur.",
     R_PACHAMANCA, "food5", nutrition=0.9, value=21, rot_days=5, pargs={"kind": "pachamanca"})
