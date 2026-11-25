"""Celestial Tianxia (2.0): nation, research branch, weapons, armour, buildings, floors and food."""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Tianxia"
FN = "Nations/HE_Tianxia.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Tianxia",
                 label=T("Celestial Tianxia", "Göksel Tianxia"),
                 description=T("The colony ship Kunlun carried the largest crew of all the heirs, and their descendants built the largest realm. An emperor rules all under heaven through scholar-officials chosen by examination, and the silk roads of Tianxia carry tea, porcelain and silk to every market. They are patient, numerous and proud, and they have never forgiven Yamato for an old war.",
                               "Kunlun koloni gemisi bütün mirasçıların en kalabalık mürettebatını taşıdı ve torunları en büyük ülkeyi kurdu. Bir imparator, sınavla seçilmiş âlim memurlar aracılığıyla göğün altındaki her şeyi yönetir; Tianxia'nın ipek yolları çayı, porseleni ve ipeği her pazara taşır. Sabırlı, kalabalık ve gururludurlar; Yamato'yu eski bir savaş için hiç affetmediler."),
                 color="(0.62, 0.14, 0.12)", iconPath="HeirsOfEarth/UI/HE_Tianxia",
                 rulerTitle=T("Emperor", "İmparator"), adjective=T("Tianxia", "Tianxia"), release=2,
                 rivals=["HE_Yamato"])
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Tianxia", "nation_icon", color="#9c2a20", emblem="dragon")

# ------------------------------------------------------------------ research: Neolithic
R_JIAN = research(NATION, "Jian", "jian", "jian",
                  "The straight double-edged sword, called the gentleman of weapons.",
                  "Silahların beyefendisi denen düz, çift ağızlı kılıç.",
                  500, "Neolithic", 0, 0)
R_SILK = research(NATION, "Silk", "silk weaving", "ipek dokuma",
                  "Raise silkworms on mulberry leaves and weave their thread into the softest cloth in the world.",
                  "İpek böceklerini dut yapraklarıyla besle ve ipliklerini dünyanın en yumuşak kumaşına doku.",
                  500, "Neolithic", 1, 0)
R_JADE = research(NATION, "JadeFloor", "jade courtyards", "yeşim avlular",
                  "Pave courtyards with polished green stone set in patterns of clouds.",
                  "Avluları bulut desenleriyle döşenmiş cilalı yeşil taşla kapla.",
                  550, "Neolithic", 2, 0)
R_HANFU = research(NATION, "Hanfu", "hanfu", "hanfu",
                   "Sew the flowing robes with crossed collars and wide sleeves worn by scholars and officials.",
                   "Âlimlerin ve memurların giydiği çapraz yakalı, geniş kollu dökümlü kaftanları dik.",
                   450, "Neolithic", 0, 1, prereqs=[R_SILK])
R_DUMPLINGS = research(NATION, "Dumplings", "dumplings", "mantı",
                       "Fold minced meat and greens into thin dough and steam them in bamboo baskets.",
                       "Kıyılmış eti ve yeşillikleri ince hamura sarıp bambu sepetlerde buharda pişir.",
                       400, "Neolithic", 1, 1)
R_LANTERN = research(NATION, "PaperLantern", "paper lanterns", "kâğıt fenerler",
                     "Stretch oiled paper over bamboo frames and hang red lanterns along every path.",
                     "Yağlı kâğıdı bambu çerçevelere ger ve her yol boyunca kırmızı fenerler as.",
                     450, "Neolithic", 2, 1, prereqs=[R_JADE])
R_TEA = research(NATION, "TeaCulture", "tea culture", "çay kültürü",
                 "A cup of tea before sleep, a cup on waking. The body rests better when the mind is calm.",
                 "Uyumadan önce bir fincan çay, uyanınca bir fincan. Zihin sakin olunca beden daha iyi dinlenir.",
                 700, "Neolithic", 0, 2, prereqs=[R_HANFU], knowledge=15, tradition=True,
                 stats=[("RestRateMultiplier", 0, 1.05, "Colonists")],
                 effect=T("Colonists rest 5% faster.", "Kolonistler %5 daha hızlı dinlenir."))
R_GRANARY = research(NATION, "Granary", "ever-normal granary", "dengeli ambar",
                     "Buy grain when it is cheap and store it against bad years: the harvest is worked with care.",
                     "Ucuzken tahıl al ve kötü yıllar için sakla: hasat özenle yapılır.",
                     750, "Neolithic", 1, 2, prereqs=[R_DUMPLINGS], knowledge=15, tradition=True,
                     stats=[("PlantHarvestYield", 0, 1.06, "Colonists")],
                     effect=T("Colonists harvest 6% more from plants.", "Kolonistler bitkilerden %6 daha fazla hasat alır."))
R_SILKROAD = research(NATION, "SilkRoad", "silk road", "ipek yolu",
                      "From oasis to oasis the caravans of Tianxia carry silk west and silver east, and they know every price.",
                      "Tianxia kervanları vahadan vahaya ipeği batıya, gümüşü doğuya taşır ve her fiyatı bilirler.",
                      850, "Neolithic", 2, 2, prereqs=[R_LANTERN], knowledge=20, tradition=True,
                      stats=[("TradePriceImprovement", 0.06, 1, "Colonists")],
                      effect=T("Colonists get 6% better trade prices.", "Kolonistler %6 daha iyi ticaret fiyatı alır."))
# ------------------------------------------------------------------ research: Medieval
R_FORGE = research(NATION, "Guandao", "imperial armoury", "imparatorluk cephaneliği",
                   "Forge the heavy guandao glaive and lamellar armour for the imperial guard.",
                   "İmparatorluk muhafızları için ağır guandao palasını ve lameller zırhı döv.",
                   1000, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_REPEATER = research(NATION, "Repeater", "repeating crossbow", "tekrarlı arbalet",
                      "A crossbow with a magazine of bolts on top: pull the lever, loose, pull again.",
                      "Üstünde cıvata şarjörü olan bir arbalet: kolu çek, bırak, yine çek.",
                      1100, "Medieval", 1, 0, prereqs=[R_JIAN], knowledge=15)
R_PORCELAIN_R = research(NATION, "PorcelainKiln", "porcelain kiln", "porselen fırını",
                         "Fire white clay hotter than any potter in the world and paint it in cobalt blue.",
                         "Beyaz kili dünyadaki her çömlekçiden daha sıcak pişir ve kobalt maviyle boya.",
                         900, "Medieval", 2, 0, prereqs=[R_LANTERN], knowledge=15)
R_FIRELANCE = research(NATION, "FireLance", "fire lance", "ateş mızrağı",
                       "A tube of black powder tied to a spear. When it is lit, it spits fire and shrapnel at the enemy.",
                       "Bir mızrağa bağlanmış kara barut tüpü. Ateşlendiğinde düşmana ateş ve şarapnel püskürtür.",
                       1300, "Medieval", 1, 1, prereqs=[R_REPEATER], knowledge=30)
R_PHYSICIANS = research(NATION, "Physicians", "imperial physicians", "saray hekimleri",
                        "Needles, herbs and pulse-reading: the court physicians know a cure for nearly everything.",
                        "İğneler, otlar ve nabız okuma: saray hekimlerinin neredeyse her şeye bir çaresi vardır.",
                        1000, "Medieval", 2, 1, prereqs=[R_PORCELAIN_R], knowledge=25, tradition=True,
                        stats=[("MedicalTendQuality", 0.10, 1, "Colonists"), ("ImmunityGainSpeed", 0, 1.08, "Colonists")],
                        effect=T("Colonists tend wounds with +10% quality and gain immunity 8% faster.",
                                 "Kolonistler yaraları +%10 kaliteyle tedavi eder ve %8 daha hızlı bağışıklık kazanır."))
R_EXAM = research(NATION, "Examination", "imperial examination", "imparatorluk sınavı",
                  "Anyone may sit the examination, and anyone who passes may rule. So everyone studies.",
                  "Herkes sınava girebilir ve geçen herkes yönetebilir. Bu yüzden herkes çalışır.",
                  1300, "Medieval", 0, 1, prereqs=[R_FORGE], knowledge=35, tradition=True,
                  stats=[("GlobalLearningFactor", 0.10, 1, "Colonists")],
                  effect=T("Colonists learn 10% faster.", "Kolonistler %10 daha hızlı öğrenir."))
R_FIREARROWS = research(NATION, "FireArrows", "fire arrows", "ateş okları",
                        "Archers drill until the volley lands as one. The enemy line burns before it reaches the wall.",
                        "Okçular yaylım tek bir ok gibi düşene dek talim yapar. Düşman hattı surlara ulaşmadan yanar.",
                        1300, "Medieval", 1, 2, prereqs=[R_FIRELANCE], knowledge=35, tradition=True,
                        stats=[("ShootingAccuracyPawn", 2, 1, "Colonists")],
                        effect=T("Colonists gain +2 shooting accuracy.", "Kolonistler +2 atış isabeti kazanır."))
R_PORCELAIN = research(NATION, "Porcelain", "porcelain mastery", "porselen ustalığı",
                       "The kilns of Jingdezhen fire a thousand pieces to keep one. Every craftsman learns that patience.",
                       "Jingdezhen fırınları bir tanesini saklamak için bin parça pişirir. Her zanaatkâr bu sabrı öğrenir.",
                       1500, "Medieval", 2, 2, prereqs=[R_PHYSICIANS], knowledge=40, tradition=True, quality=0.06,
                       effect=T("Crafted items have a 6% chance to come out one quality level higher.",
                                "Üretilen eşyaların %6 ihtimalle bir kalite üstü çıkar."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Jian", "jian", "jian",
      "A straight double-edged sword, light and quick, used with precise thrusts and flicks of the wrist.",
      "Hafif ve çabuk, düz, çift ağızlı bir kılıç; kesin hamlelerle ve bilek hareketleriyle kullanılır.",
      "Neolithic", R_JIAN, [tool("handle", "Blunt", 7, 2), tool("point", "Stab", 17, 1.7, 0.24), tool("edge", "Cut", 15, 1.7, 0.20)],
      mass=1.0, work=10000, painter="jian", stuff_count=50, skill=4, angle=-45, extra_tags=["MedievalMeleeDecent"])
melee(NATION, "Guandao", "guandao", "guandao",
      "A heavy curved blade on a long pole with a dragon-head guard, swung in great sweeping arcs.",
      "Ejder başlı siperi olan uzun bir sapın ucunda ağır, eğri bir ağız; büyük süpürücü yaylarla savrulur.",
      "Medieval", R_FORGE, [tool("shaft", "Blunt", 10, 2.2), tool("edge", "Cut", 25, 2.5, 0.34)],
      mass=3.2, work=18000, painter="spear_long", stuff_count=75, skill=6, angle=-45, extra_tags=["MedievalMeleeAdvanced"],
      pargs={"head": "guandao", "shaft": "#5a1e18"})
BOLT = projectile("HE_Bolt_Repeater", "repeater bolt", "tekrarlı arbalet oku", "Arrow", 8, 50, "Things/Projectile/Arrow_Small", pen=0.10)
ranged(NATION, "Repeater", "repeating crossbow", "tekrarlı arbalet",
       "A crossbow with a box of ten bolts mounted on top. It throws three light bolts in quick succession, then must be reloaded.",
       "Üstüne on cıvatalık bir kutu takılmış bir arbalet. Üç hafif cıvatayı art arda fırlatır, sonra yeniden doldurulmalıdır.",
       "Medieval", R_REPEATER, BOLT, 1.4, 22.9, 3.0, (0.65, 0.6, 0.45, 0.3), 3.0, 14000, "repeater",
       {"WoodLog": 50, "Steel": 30}, sound="Bow_Large", interact="Bow_Large", burst=3, ticks=12, extra_tags=["MedievalRangedAdvanced"])
FLAME = projectile("HE_Bullet_FireLance", "fire lance blast", "ateş mızrağı püskürtüsü", "Flame", 12, 40, "Things/Projectile/Spark", pen=0.10)
ranged(NATION, "FireLance", "fire lance", "ateş mızrağı",
       "A spear with a bamboo tube of black powder lashed behind the head. Lit, it spits a short jet of fire that sets targets alight; then it is only a spear again.",
       "Ucunun arkasına kara barutlu bir bambu tüp bağlanmış bir mızrak. Ateşlendiğinde hedefleri tutuşturan kısa bir alev püskürtür; sonra yeniden yalnızca bir mızraktır.",
       "Medieval", R_FIRELANCE, FLAME, 1.2, 9.9, 3.5, (0.7, 0.55, 0.2, 0.05), 2.6, 12000, "fire_lance",
       {"WoodLog": 40, "Steel": 35}, sound="Shot_IncendiaryLauncher", interact="Interact_Rifle",
       tools=[tool("shaft", "Blunt", 9, 2), tool("point", "Stab", 15, 2.2, 0.22)], extra_tags=["MedievalRangedAdvanced"])

# ------------------------------------------------------------------ apparel
apparel(NATION, "Helmet", "lamellar helmet", "lameller miğfer",
        "A rounded iron helmet with a tall plume tube and a curtain of small plates hanging over the neck.",
        "Uzun bir sorguç borusu ve enseye sarkan küçük plakalardan bir perdesi olan yuvarlak demir bir miğfer.",
        "Medieval", R_FORGE, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 120, "StuffEffectMultiplierArmor": 0.58, "StuffEffectMultiplierInsulation_Cold": 0.2, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet2", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=50, work=4200, mass=2.2, users=SMITHY, skill=6, head=True,
        pargs={"kind": "tianxia"})
apparel(NATION, "Lamellar", "lamellar armour", "lameller zırh",
        "Hundreds of small iron plates laced into overlapping rows, with a lacquered breast mirror. Flexible and strong.",
        "Üst üste binen sıralara bağlanmış yüzlerce küçük demir plaka ve lake bir göğüs aynası. Esnek ve güçlü.",
        "Medieval", R_FORGE, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders", "Arms", "Legs"],
        {"MaxHitPoints": 240, "StuffEffectMultiplierArmor": 0.8, "StuffEffectMultiplierInsulation_Cold": 0.4, "StuffEffectMultiplierInsulation_Heat": 0.05},
        "torso2", parent="ArmorSmithableBase", stuff=("Metallic",), stuff_count=130, cost={"Cloth": 25}, work=30000, mass=9,
        users=SMITHY, skill=7, equipped={"MoveSpeed": -0.18}, tags=["MedievalMilitary"], pargs={"kind": "lamellar"})
apparel(NATION, "Hanfu", "hanfu", "hanfu",
        "A long flowing robe with a crossed collar and wide sleeves, tied with a sash. It marks a person of learning.",
        "Çapraz yakalı ve geniş kollu, kuşakla bağlanan uzun dökümlü bir kaftan. Bilgili bir kişiyi belli eder.",
        "Neolithic", R_HANFU, "Robe/Robe", ["Shell"], ["Torso", "Shoulders", "Arms", "Legs"],
        {"MaxHitPoints": 110, "StuffEffectMultiplierArmor": 0.2, "StuffEffectMultiplierInsulation_Cold": 0.75, "StuffEffectMultiplierInsulation_Heat": 0.4},
        "torso2", stuff=("Fabric",), stuff_count=75, work=5500, mass=0.9, equipped={"SocialImpact": 0.04}, pargs={"kind": "hanfu"})

# ------------------------------------------------------------------ buildings and floors
deco(NATION, "Vase", "porcelain vase", "porselen vazo",
     "A tall white vase painted in cobalt blue with dragons among clouds. Merchants travel half the world to buy one.",
     "Bulutlar arasında ejderlerle kobalt maviye boyanmış uzun beyaz bir vazo. Tüccarlar bir tane almak için dünyanın yarısını dolaşır.",
     R_PORCELAIN_R, (1, 1), "vase", beauty=16, work=4000, stuff=None, cost={"BlocksMarble": 20, "Silver": 15}, hp=60,
     category="Art", draw_size="(1,1.5)")
deco(NATION, "MoonGate", "moon gate", "ay kapısı",
     "A perfectly round opening in a garden wall. Stepping through it is said to bring luck.",
     "Bir bahçe duvarında kusursuz yuvarlak bir açıklık. İçinden geçmenin şans getirdiğine inanılır.",
     R_JADE, (3, 1), "moon_gate", beauty=18, work=7000, stuff=("Stony",), stuff_count=180, hp=500,
     passability="Standable", fill=0.0, minify=False, category="Art", draw_size="(3,2.25)")
deco(NATION, "Lantern", "paper lantern", "kâğıt fener",
     "A red paper lantern on a lacquered post, with a small oil lamp inside.",
     "Lake bir direğin üzerinde, içinde küçük bir kandil olan kırmızı bir kâğıt fener.",
     R_LANTERN, (1, 1), "paper_lantern", beauty=5, work=1600, stuff=("Woody",), stuff_count=25, cost={"Cloth": 10}, hp=80,
     glow=(6, "(255,120,90,0)"), category="Art", draw_size="(1,1.5)", extra={"tickerType": "Normal"},
     comps=[{"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": 1.0, "fuelCapacity": 10, "fuelFilter": {"thingDefs": ["WoodLog"]},
             "initialFuelPercent": 1, "showAllowAutoRefuelToggle": True}])
deco(NATION, "TeaTable", "gongfu tea table", "gongfu çay masası",
     "A carved wooden tray table with a clay teapot and tiny cups. Tea is brewed again and again, a little stronger each time.",
     "Kil bir demlik ve minik fincanlarla donatılmış oymalı ahşap bir tepsi masa. Çay her seferinde biraz daha koyu olarak tekrar tekrar demlenir.",
     R_TEA, (2, 2), "table", beauty=5, work=2800, stuff=("Woody",), stuff_count=60, hp=140, joy="Social", pargs={"kind": "gongfu"})
floor(NATION, "Jade", "jade tiles", "yeşim karolar",
      "Polished green stone tiles set in a pattern of interlocking clouds.",
      "Birbirine geçen bulut deseninde döşenmiş cilalı yeşil taş karolar.",
      R_JADE, "floor_jade", beauty=4, cost={"BlocksMarble": 4, "Silver": 2}, work=1400)

# ------------------------------------------------------------------ food and trade goods
food(NATION, "Dumplings", "dumplings", "mantı",
     "Thin dough folded around minced meat and greens, steamed in a bamboo basket and served with vinegar.",
     "Kıyılmış et ve yeşilliklerin etrafına katlanmış ince hamur; bambu sepette buharda pişirilip sirkeyle sunulur.",
     R_DUMPLINGS, "food2", nutrition=0.9, value=22, rot_days=4, pargs={"kind": "dumplings"})
resource(NATION, "TeaBrick", "tea brick", "çay tuğlası",
         "Black tea leaves steamed and pressed into a hard brick stamped with a dragon. It keeps for years and is used as money on the silk road.",
         "Buharda pişirilip ejder damgalı sert bir tuğlaya preslenmiş siyah çay yaprakları. Yıllarca dayanır ve ipek yolunda para olarak kullanılır.",
         12, "goods", mass=0.4, stack=50, pargs={"kind": "teabrick"})
resource(NATION, "Silk", "silk bolt", "ipek top",
         "A bolt of heavy red silk embroidered with golden cranes. Worth its weight in silver anywhere.",
         "Altın turnalarla işlenmiş ağır kırmızı ipekten bir top. Her yerde ağırlığınca gümüş eder.",
         20, "goods", mass=0.3, stack=30, pargs={"kind": "silk"})
