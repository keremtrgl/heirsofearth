"""Nordheim: nation, research branch, weapons, armour, buildings, floors and food."""
import heirs_c_roma
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Nord"
FN = "Nations/HE_Nord.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Nord",
                 label=T("Jarldom of Nordheim", "Nordheim Jarllığı"),
                 description=T("The crew of the colony ship Yggdrasil landed on a cold coast and never asked for a warmer one. Their jarls are chosen at the Thing, the assembly of free people, and their longhouses stand in the snow like overturned ships. Hardy hunters and fierce raiders, they keep the old sagas alive around the hearth, and they remember every Roman insult.",
                               "Yggdrasil koloni gemisinin mürettebatı soğuk bir kıyıya indi ve hiçbir zaman daha sıcağını istemedi. Jarlları, özgür insanların meclisi Thing'de seçilir; uzun evleri karın içinde ters dönmüş gemiler gibi durur. Dayanıklı avcılar ve vahşi akıncılardır; eski destanları ocak başında yaşatırlar ve Romalıların her hakaretini hatırlarlar."),
                 color="(0.23, 0.33, 0.38)", iconPath="HeirsOfEarth/UI/HE_Nord",
                 rulerTitle=T("Jarl", "Jarl"), adjective=T("Nordheim", "Nordheim"), release=1,
                 rivals=["HE_Roma"])
add(FN, NATION_DEF)
heirs_c_roma.NATION_DEF.fields["rivals"] = ["HE_Nord"]
tex("HeirsOfEarth/UI/HE_Nord", "nation_icon", color="#3a5562", emblem="raven")

# ------------------------------------------------------------------ research: Neolithic
R_LONGHOUSE = research(NATION, "Longhouse", "longhouse hearth", "uzun ev ocağı",
                       "A long stone-lined fire pit that warms a whole hall and cooks the evening meal.",
                       "Bütün bir salonu ısıtan ve akşam yemeğini pişiren, taş kaplı uzun bir ateş çukuru.",
                       450, "Neolithic", 0, 0)
R_PLANKS = research(NATION, "Planks", "split planks", "yarma tahta",
                    "Split logs along the grain into wide planks for floors and benches.",
                    "Kütükleri lif yönünde yararak zemin ve sıralar için geniş tahtalar elde et.",
                    400, "Neolithic", 1, 0)
R_HUNTBOW = research(NATION, "HuntBow", "hunting bow", "av yayı",
                     "A simple elm bow for deer in the pine forests, quick to make and quick to draw.",
                     "Çam ormanlarındaki geyikler için basit bir karaağaç yay; yapması da çekmesi de çabuktur.",
                     450, "Neolithic", 2, 0)
R_FUR = research(NATION, "Fur", "fur and wool", "kürk ve yün",
                 "Sew heavy fur cloaks and thick woollen tunics for the long winters.",
                 "Uzun kışlar için ağır kürk pelerinler ve kalın yün tunikler dik.",
                 450, "Neolithic", 0, 1, prereqs=[R_LONGHOUSE])
R_SKYR = research(NATION, "Skyr", "skyr", "skyr",
                  "Curdle skimmed milk into skyr, a thick sour dairy that keeps through the winter.",
                  "Yağı alınmış sütü pıhtılaştırarak kışa dayanan koyu ve ekşi bir süt ürünü olan skyr yap.",
                  400, "Neolithic", 1, 1)
R_RUNES = research(NATION, "Runes", "rune stones", "run taşları",
                   "Carve runes into standing stones to remember the dead and boast of the living.",
                   "Ölüleri anmak ve yaşayanları övmek için dikili taşlara runlar kazı.",
                   600, "Neolithic", 2, 1, prereqs=[R_PLANKS])
R_BLOOD = research(NATION, "Blood", "northern blood", "kuzey kanı",
                   "Children who bathe in icy rivers grow into adults who do not notice the cold.",
                   "Buz gibi nehirlerde yıkanan çocuklar, soğuğu fark etmeyen yetişkinlere dönüşür.",
                   700, "Neolithic", 0, 2, prereqs=[R_FUR], knowledge=15, tradition=True,
                   stats=[("ComfyTemperatureMin", -8, 1, "Colonists")],
                   effect=T("Colonists are comfortable at temperatures 8°C colder.", "Kolonistler 8°C daha soğukta rahat eder."))
R_HUNTING = research(NATION, "Hunting", "hunting lore", "av bilgisi",
                     "Read tracks in snow and move downwind: the hunters' lore is passed from parent to child.",
                     "Kardaki izleri oku ve rüzgârın altından ilerle: avcıların bilgisi ebeveynden çocuğa geçer.",
                     750, "Neolithic", 1, 2, prereqs=[R_HUNTBOW], knowledge=15, tradition=True,
                     stats=[("HuntingStealth", 0.10, 1, "Colonists"), ("ShootingAccuracyPawn", 1, 1, "Colonists")],
                     effect=T("Colonists gain +10% hunting stealth and +1 shooting accuracy.",
                              "Kolonistler +%10 av gizliliği ve +1 atış isabeti kazanır."))
R_SAGA = research(NATION, "Saga", "saga telling", "destan anlatımı",
                  "On winter nights the skalds recite the deeds of the ancestors. Everyone listens, and everyone learns.",
                  "Kış gecelerinde ozanlar ataların kahramanlıklarını anlatır. Herkes dinler, herkes öğrenir.",
                  850, "Neolithic", 2, 2, prereqs=[R_RUNES], knowledge=20, tradition=True,
                  stats=[("GlobalLearningFactor", 0.05, 1, "Colonists"), ("SocialImpact", 0.05, 1, "Colonists")],
                  effect=T("Colonists learn 5% faster and gain +5% social impact.", "Kolonistler %5 daha hızlı öğrenir ve +%5 sosyal etki kazanır."))
# ------------------------------------------------------------------ research: Medieval
R_SMITH = research(NATION, "Smithing", "Nordheim smithing", "Nordheim demirciliği",
                   "Pattern-welded swords and the long-hafted Dane axe, forged from bog iron.",
                   "Bataklık demirinden dövülmüş desenli kılıçlar ve uzun saplı Dane baltası.",
                   850, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_BYRNIE = research(NATION, "Byrnie", "byrnie and round shield", "zırh gömleği ve yuvarlak kalkan",
                    "Thousands of riveted rings make a byrnie. With a spangenhelm and a painted round shield, a warrior is ready for the shield wall.",
                    "Binlerce perçinli halka bir zırh gömleği eder. Bir miğfer ve boyalı bir yuvarlak kalkanla savaşçı kalkan duvarına hazırdır.",
                    1100, "Medieval", 0, 1, prereqs=[R_SMITH], knowledge=25)
R_MEAD = research(NATION, "MeadHall", "mead hall", "bal şarabı salonu",
                  "Long tables, drinking horns and a jarl's seat: the mead hall is where the people of Nordheim feast, boast and make peace.",
                  "Uzun masalar, içki boynuzları ve bir jarl koltuğu: bal şarabı salonu, Nordheim halkının ziyafet çektiği, övündüğü ve barıştığı yerdir.",
                  800, "Medieval", 1, 0, prereqs=[R_LONGHOUSE], knowledge=15)
R_SAUNA = research(NATION, "Sauna", "sauna", "sauna",
                   "A small log house with a stone stove. Steam, birch branches and a roll in the snow keep the body strong.",
                   "Taş sobalı küçük bir kütük ev. Buhar, huş dalları ve karda yuvarlanmak bedeni güçlü tutar.",
                   1000, "Medieval", 2, 0, prereqs=[R_PLANKS], knowledge=20, tradition=True,
                   stats=[("ImmunityGainSpeed", 0, 1.10, "Colonists")],
                   effect=T("Unlocks the sauna. Colonists gain immunity 10% faster.", "Saunayı açar. Kolonistler %10 daha hızlı bağışıklık kazanır."))
R_THING = research(NATION, "Thing", "the Thing", "Thing meclisi",
                   "Free people gather to settle disputes by law instead of the axe. Their voices carry far.",
                   "Özgür insanlar anlaşmazlıkları balta yerine yasayla çözmek için toplanır. Sesleri uzağa ulaşır.",
                   1000, "Medieval", 1, 1, prereqs=[R_MEAD], knowledge=25, tradition=True,
                   stats=[("NegotiationAbility", 0.08, 1, "Colonists")],
                   effect=T("Colonists gain +8% negotiation ability.", "Kolonistler +%8 müzakere yeteneği kazanır."))
R_LONGSHIPS = research(NATION, "Longships", "longship crews", "uzun gemi tayfaları",
                       "Rowing crews learn to travel light and fast, whether over waves or over land.",
                       "Kürek tayfaları dalgaların ya da karanın üzerinde hafif ve hızlı yolculuk etmeyi öğrenir.",
                       1100, "Medieval", 2, 1, prereqs=[R_SAUNA], knowledge=30, tradition=True, caravan=0.12,
                       effect=T("Your caravans travel 12% faster.", "Kervanların %12 daha hızlı yolculuk eder."))
R_BERSERK = research(NATION, "Berserk", "berserkergang", "berserkergang",
                     "Some warriors fight in a fury that ignores wounds and caution alike.",
                     "Bazı savaşçılar hem yaraları hem de temkini yok sayan bir öfkeyle dövüşür.",
                     1400, "Medieval", 0, 2, prereqs=[R_BYRNIE], knowledge=40, tradition=True,
                     stats=[("MeleeDamageFactor", 0, 1.10, "Colonists"), ("MeleeDodgeChance", -2, 1, "Colonists")],
                     effect=T("Colonists deal 10% more melee damage but have -2 melee dodge chance.",
                              "Kolonistler %10 daha fazla yakın dövüş hasarı verir ama yakın dövüşte kaçınmaları -2 olur."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Sword", "Nordheim sword", "Nordheim kılıcı",
      "A broad double-edged sword with a pattern-welded blade and a lobed pommel. A jarl's gift to a loyal warrior.",
      "Desenli kaynaklı ağzı ve dilimli topuzu olan geniş, iki ağızlı bir kılıç. Bir jarlın sadık bir savaşçıya hediyesi.",
      "Medieval", R_SMITH, [tool("pommel", "Blunt", 9, 2), tool("point", "Stab", 15, 2.0, 0.22), tool("edge", "Cut", 18, 2.0, 0.27)],
      mass=1.6, work=16000, painter="nordic_sword", stuff_count=75, skill=5, angle=-45, extra_tags=["MedievalMeleeDecent"])
melee(NATION, "DaneAxe", "Dane axe", "Dane baltası",
      "A thin, wide axe head on a haft as long as a man. Swung with both hands, it splits shields and helmets.",
      "Bir insan boyu uzunluğunda bir sapın ucunda ince, geniş bir balta başı. İki elle savrulduğunda kalkanları ve miğferleri yarar.",
      "Medieval", R_SMITH, [tool("haft", "Blunt", 10, 2.2), tool("edge", "Cut", 24, 2.5, 0.38)],
      mass=2.4, work=14000, painter="dane_axe", stuff_count=60, skill=5, angle=-55, extra_tags=["MedievalMeleeAdvanced"])
ARROW = projectile("HE_Arrow_HuntBow", "hunting arrow", "av oku", "Arrow", 13, 44, "Things/Projectile/Arrow_Small", pen=0.18)
ranged(NATION, "HuntBow", "hunting bow", "av yayı",
       "A plain elm bow strung with sinew. Light, quiet and accurate at hunting distances.",
       "Sinirle kirişlenmiş sade bir karaağaç yay. Hafif, sessiz ve av mesafelerinde isabetli.",
       "Neolithic", R_HUNTBOW, ARROW, 1.2, 26.9, 1.5, (0.65, 0.74, 0.64, 0.5), 1.0, 6000, "long_bow",
       {"WoodLog": 40}, extra_tags=["NeolithicRangedDecent"], pargs={"kind": "elm"})

# ------------------------------------------------------------------ apparel
apparel(NATION, "Helm", "spangenhelm", "spangenhelm",
        "A rounded iron helmet of riveted plates with a broad nose guard and spectacle-shaped eye guards.",
        "Geniş bir burun siperliği ve gözlük biçimli göz siperleri olan, perçinli plakalardan yuvarlak demir bir miğfer.",
        "Medieval", R_BYRNIE, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 110, "StuffEffectMultiplierArmor": 0.55, "StuffEffectMultiplierInsulation_Cold": 0.2, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=45, work=3600, mass=2, users=SMITHY, skill=5, head=True,
        pargs={"kind": "norse"})
apparel(NATION, "Byrnie", "byrnie", "zırh gömleği",
        "A knee-length shirt of riveted iron rings over a padded tunic. Heavy, but it stops most cuts.",
        "Dolgulu bir tunik üzerine giyilen, perçinli demir halkalardan diz boyu bir gömlek. Ağırdır ama çoğu kesiği durdurur.",
        "Medieval", R_BYRNIE, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders", "Arms", "Legs"],
        {"MaxHitPoints": 230, "StuffEffectMultiplierArmor": 0.78, "StuffEffectMultiplierInsulation_Cold": 0.4, "StuffEffectMultiplierInsulation_Heat": 0},
        "torso", parent="ArmorSmithableBase", stuff=("Metallic",), stuff_count=115, work=25000, mass=9, users=SMITHY, skill=6,
        equipped={"MoveSpeed": -0.25}, tags=["MedievalMilitary"], pargs={"kind": "byrnie"})
apparel(NATION, "FurCloak", "fur cloak", "kürk pelerin",
        "A heavy cloak of thick pelts fastened with a bronze brooch. Nothing keeps out the northern wind better.",
        "Bronz bir broşla tutturulmuş, kalın postlardan ağır bir pelerin. Kuzey rüzgârını hiçbir şey daha iyi kesmez.",
        "Neolithic", R_FUR, "Parka/Parka", ["Shell"], ["Torso", "Neck", "Shoulders", "Arms"],
        {"MaxHitPoints": 160, "StuffEffectMultiplierArmor": 0.25, "StuffEffectMultiplierInsulation_Cold": 1.2, "StuffEffectMultiplierInsulation_Heat": 0.1},
        "torso", stuff=("Leathery",), stuff_count=90, work=6000, mass=2.4, equipped={"MoveSpeed": -0.05}, pargs={"kind": "furcloak"})
apparel(NATION, "Tunic", "wool tunic", "yün tunik",
        "A thick woollen tunic with woven bands at the cuffs and hem. Warm, sturdy and itchy.",
        "Kol ağızlarında ve eteğinde dokuma şeritler olan kalın yün bir tunik. Sıcak, sağlam ve kaşındırıcı.",
        "Neolithic", R_FUR, "ShirtBasic/ShirtBasic", ["OnSkin"], ["Torso", "Shoulders", "Arms"],
        {"MaxHitPoints": 120, "StuffEffectMultiplierArmor": 0.2, "StuffEffectMultiplierInsulation_Cold": 0.55, "StuffEffectMultiplierInsulation_Heat": 0.1},
        "torso", stuff_count=55, work=2200, mass=0.4, pargs={"kind": "woolshirt"})

# ------------------------------------------------------------------ buildings and floors
deco(NATION, "Hearth", "longhouse hearth", "uzun ev ocağı",
     "A long fire pit lined with stones. It heats a large hall, lights it, and keeps a pot of stew warm.",
     "Taşlarla çevrili uzun bir ateş çukuru. Büyük bir salonu ısıtır, aydınlatır ve bir tencere yahniyi sıcak tutar.",
     R_LONGHOUSE, (2, 1), "hearth", beauty=4, work=1800, stuff=("Stony",), stuff_count=60, hp=200,
     passability="PassThroughOnly", fill=0.2, minify=False, category="Temperature", glow=(9, "(252,180,100,0)"),
     extra={"tickerType": "Normal"},
     comps=[{"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": 3.5, "fuelCapacity": 30, "fuelConsumptionPerTickInRain": 0.0006,
             "fuelFilter": {"thingDefs": ["WoodLog"]}, "initialFuelPercent": 1, "showAllowAutoRefuelToggle": True},
            {"@Class": "CompProperties_HeatPusher", "heatPerSecond": 26, "heatPushMaxTemperature": 26},
            {"@Class": "CompProperties_FireOverlay", "fireSize": 0.7, "offset": "(0,0,0.05)"}])
deco(NATION, "RuneStone", "rune stone", "run taşı",
     "A tall grey stone carved with a serpent of runes that tells of a hero's deeds.",
     "Bir kahramanın yaptıklarını anlatan runlardan bir yılanla oyulmuş, uzun, gri bir taş.",
     R_RUNES, (1, 1), "rune_stone", beauty=22, work=8000, stuff=("Stony",), stuff_count=130, hp=320, fill=0.5,
     category="Art", draw_size="(1,1.5)")
deco(NATION, "ShieldWall", "round shield display", "yuvarlak kalkan sergisi",
     "A painted round shield with an iron boss, hung where everyone can see it.",
     "Herkesin görebileceği bir yere asılmış, demir umbolu, boyalı yuvarlak bir kalkan.",
     R_BYRNIE, (1, 1), "wall_shield", beauty=6, work=1800, stuff=("Woody",), stuff_count=35, cost={"Steel": 10}, hp=100,
     category="Art", pargs={"kind": "round"})
deco(NATION, "MeadTable", "mead table", "bal şarabı masası",
     "A long oak table set with drinking horns and a bowl of mead. Colonists gather here to drink and boast.",
     "İçki boynuzları ve bir kâse bal şarabıyla kurulmuş uzun bir meşe masa. Kolonistler içmek ve övünmek için burada toplanır.",
     R_MEAD, (2, 2), "table", beauty=3, work=2400, stuff=("Woody",), stuff_count=70, hp=160, joy="Social", pargs={"kind": "mead"})
deco(NATION, "Sauna", "sauna", "sauna",
     "A small pine bath house with a stone stove and benches. Colonists sweat out their worries here.",
     "Taş sobası ve sıraları olan küçük, çam bir yıkanma evi. Kolonistler dertlerini burada terleyerek atar.",
     R_SAUNA, (3, 2), "bath", beauty=8, work=9000, stuff=("Woody",), stuff_count=180, cost={"BlocksGranite": 30}, hp=400,
     passability="PassThroughOnly", fill=0.3, minify=False, joy="Meditative", pargs={"kind": "sauna"})
floor(NATION, "Planks", "split plank floor", "yarma tahta zemin",
      "Wide planks split from pine logs and fitted together. Warm underfoot.",
      "Çam kütüklerinden yarılıp birbirine geçirilmiş geniş tahtalar. Ayak altında sıcaktır.",
      R_PLANKS, "floor_planks", beauty=1, cost={"WoodLog": 3}, work=600)

# ------------------------------------------------------------------ food and trade goods
food(NATION, "Skyr", "skyr bowl", "skyr kâsesi",
     "A bowl of thick, sour skyr with berries and a drizzle of honey. Filling and good for the bones.",
     "Böğürtlenli ve üzerine bal gezdirilmiş koyu, ekşi bir kâse skyr. Doyurucudur ve kemiklere iyi gelir.",
     R_SKYR, "bowl", nutrition=0.9, value=21, ingredients=("AnimalProductRaw",), count=0.5, rot_days=5, pargs={"kind": "skyr"})
resource(NATION, "Amber", "raw amber", "ham kehribar",
         "Golden lumps of amber gathered from the northern shores. Traders pay well for it.",
         "Kuzey kıyılarından toplanmış altın renkli kehribar parçaları. Tüccarlar ona iyi para öder.",
         18, "jar", mass=0.2, stack=50, pargs={"kind": "amber"})
