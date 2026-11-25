"""League of Hellas (2.0): nation, research branch, weapons, armour, buildings, floors and food."""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Hellas"
FN = "Nations/HE_Hellas.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Hellas",
                 label=T("League of Hellas", "Hellas Birliği"),
                 description=T("The colony ship Argo carried teachers, doctors and philosophers, and their children never stopped arguing. The city-states of Hellas are a quarrelsome league held together by a common tongue, the games and a deep love of learning. Their hoplites fight shoulder to shoulder, their physicians are sought by every nation, and they count the Nova Romans as old friends.",
                               "Argo koloni gemisi öğretmenler, hekimler ve filozoflar taşıdı; çocukları tartışmayı hiç bırakmadı. Hellas şehir devletleri ortak bir dil, oyunlar ve derin bir öğrenme sevgisiyle bir arada duran kavgacı bir birliktir. Hoplitleri omuz omuza dövüşür, hekimleri her devletçe aranır ve Nova Romalıları eski dostları sayarlar."),
                 color="(0.18, 0.36, 0.55)", iconPath="HeirsOfEarth/UI/HE_Hellas",
                 rulerTitle=T("Archon", "Arkon"), adjective=T("Hellenic", "Hellas"), release=2,
                 friends=["HE_Roma"])
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Hellas", "nation_icon", color="#2e5c8c", emblem="owl")

# ------------------------------------------------------------------ research: Neolithic
R_DORY = research(NATION, "Dory", "dory", "dory",
                  "The long thrusting spear of the hoplite, with a leaf-shaped head and a bronze butt-spike.",
                  "Hoplitin uzun saplı mızrağı: yaprak biçimli bir ucu ve bronz bir dip çivisi vardır.",
                  450, "Neolithic", 0, 0)
R_TOXON = research(NATION, "Toxon", "toxon", "toxon",
                   "The Scythian-style recurve bow, short enough to use behind a shield wall.",
                   "Bir kalkan duvarının arkasında kullanılacak kadar kısa, İskit tarzı çift kavisli yay.",
                   500, "Neolithic", 1, 0)
R_MEANDER = research(NATION, "Meander", "meander floors", "menderes zeminler",
                     "Lay pale stone floors bordered with the endless key pattern of the old temples.",
                     "Eski tapınakların sonsuz anahtar deseniyle çevrili açık renkli taş zeminler döşe.",
                     500, "Neolithic", 2, 0)
R_CHITON = research(NATION, "Chiton", "chiton", "khiton",
                    "Sew the light pinned tunic worn by every citizen from the agora to the gymnasium.",
                    "Agoradan gymnasiuma kadar her yurttaşın giydiği hafif, iğneli tuniği dik.",
                    400, "Neolithic", 0, 1, prereqs=[R_DORY])
R_MAZA = research(NATION, "Maza", "maza", "maza",
                  "Barley cakes kneaded with olive oil and honey: plain food that keeps a hoplite marching.",
                  "Zeytinyağı ve balla yoğrulmuş arpa çörekleri: bir hoplitin yürümesini sağlayan sade yiyecek.",
                  400, "Neolithic", 1, 1)
R_COLUMNS = research(NATION, "Columns", "fluted columns", "yivli sütunlar",
                     "Carve fluted columns and crown them with statues of the city's heroes.",
                     "Yivli sütunlar oy ve onları şehrin kahramanlarının heykelleriyle taçlandır.",
                     600, "Neolithic", 2, 1, prereqs=[R_MEANDER])
R_OLYMPIC = research(NATION, "Olympic", "olympic games", "olimpiyat oyunları",
                     "Every fourth summer the cities stop their wars and race each other instead.",
                     "Her dördüncü yaz şehirler savaşlarını durdurur ve onun yerine birbirleriyle yarışır.",
                     700, "Neolithic", 0, 2, prereqs=[R_CHITON], knowledge=15, tradition=True,
                     stats=[("MoveSpeed", 0, 1.03, "Colonists")],
                     effect=T("Colonists move 3% faster.", "Kolonistler %3 daha hızlı yürür."))
R_RHETORIC = research(NATION, "Rhetoric", "rhetoric", "retorik",
                      "In the assembly a good argument is worth more than a good spear.",
                      "Mecliste iyi bir argüman iyi bir mızraktan daha değerlidir.",
                      750, "Neolithic", 1, 2, prereqs=[R_MAZA], knowledge=15, tradition=True,
                      stats=[("NegotiationAbility", 0.12, 1, "Colonists")],
                      effect=T("Colonists gain +12% negotiation ability.", "Kolonistler +%12 müzakere yeteneği kazanır."))
R_GEOMETRY = research(NATION, "Geometry", "geometry", "geometri",
                      "Let no one ignorant of geometry build here: measured lines make faster, straighter walls.",
                      "Geometri bilmeyen burada inşa etmesin: ölçülü çizgiler daha hızlı ve daha düz duvarlar yapar.",
                      800, "Neolithic", 2, 2, prereqs=[R_COLUMNS], knowledge=20, tradition=True,
                      stats=[("ConstructionSpeed", 0, 1.08, "Colonists")],
                      effect=T("Colonists build 8% faster.", "Kolonistler %8 daha hızlı inşa eder."))
# ------------------------------------------------------------------ research: Medieval
R_BRONZE = research(NATION, "Bronze", "bronze smithing", "bronz demirciliği",
                    "Cast and hammer the short xiphos and the heavy, forward-curved kopis.",
                    "Kısa xiphos'u ve ağır, öne kıvrık kopis'i dök ve döv.",
                    900, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_THEATRON = research(NATION, "Theatron", "theatron", "theatron",
                      "Build a stage and a painted backdrop, and the whole colony will gather to watch the old plays.",
                      "Bir sahne ve boyalı bir dekor kur; bütün koloni eski oyunları izlemek için toplanacaktır.",
                      900, "Medieval", 1, 0, prereqs=[R_COLUMNS], knowledge=15)
R_HIPPOCRATIC = research(NATION, "Hippocratic", "hippocratic oath", "hipokrat yemini",
                         "First, do no harm. Hellenic physicians wash their hands, take their time and lose fewer patients.",
                         "Önce zarar verme. Hellas hekimleri ellerini yıkar, acele etmez ve daha az hasta kaybeder.",
                         1000, "Medieval", 2, 0, knowledge=25, tradition=True,
                         stats=[("MedicalSurgerySuccessChance", 0, 1.12, "Colonists"), ("MedicalTendSpeed", 0, 0.95, "Colonists")],
                         effect=T("Surgery success chance rises by 12%, but tending is 5% slower.",
                                  "Ameliyat başarı şansı %12 artar, ama tedavi %5 daha yavaştır."))
R_HOPLITE = research(NATION, "Hoplite", "hoplite panoply", "hoplit teçhizatı",
                     "The Corinthian helmet, the layered linen linothorax and the great round hoplon.",
                     "Korint miğferi, katmanlı keten linothoraks ve büyük yuvarlak hoplon.",
                     1200, "Medieval", 0, 1, prereqs=[R_BRONZE], knowledge=25)
R_THEATRE = research(NATION, "Theatre", "festival of plays", "oyunlar şenliği",
                     "Tragedy in the morning, comedy at night. People leave the theatre lighter and kinder.",
                     "Sabah tragedya, akşam komedi. İnsanlar tiyatrodan daha hafif ve daha nazik ayrılır.",
                     1000, "Medieval", 1, 1, prereqs=[R_THEATRON], knowledge=25, tradition=True,
                     stats=[("JoyGainFactor", 0, 1.10, "Colonists"), ("SocialImpact", 0.05, 1, "Colonists")],
                     effect=T("Colonists gain recreation 10% faster and +5% social impact.",
                              "Kolonistler eğlenceyi %10 daha hızlı kazanır ve +%5 sosyal etki kazanır."))
R_ACADEMY = research(NATION, "Academy", "the academy", "akademi",
                     "A grove where masters walk with their pupils and every question is followed to its end.",
                     "Ustaların öğrencileriyle yürüdüğü ve her sorunun sonuna kadar takip edildiği bir koru.",
                     1300, "Medieval", 2, 1, prereqs=[R_HIPPOCRATIC], knowledge=35, tradition=True,
                     stats=[("ResearchSpeed", 0, 1.10, "Colonists")],
                     effect=T("Colonists research 10% faster.", "Kolonistler %10 daha hızlı araştırma yapar."))
R_PHALANX = research(NATION, "Phalanx", "phalanx", "falanks",
                     "Shield overlapping shield, every man covers the one to his left. The line is slow, and almost unbreakable.",
                     "Kalkan kalkanın üstüne biner; her asker solundakini korur. Hat yavaştır ve neredeyse kırılmazdır.",
                     1400, "Medieval", 0, 2, prereqs=[R_HOPLITE], knowledge=40, tradition=True,
                     stats=[("ArmorRating_Blunt", 0.05, 1, "Colonists"), ("ArmorRating_Sharp", 0.03, 1, "Colonists"), ("MoveSpeed", 0, 0.97, "Colonists")],
                     effect=T("Colonists gain +5% blunt and +3% sharp armour but move 3% slower.",
                              "Kolonistler +%5 künt ve +%3 keskin zırh kazanır ama %3 daha yavaş yürür."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Dory", "dory", "dory",
      "A two-and-a-half metre ash spear with a leaf-shaped iron head. If the head breaks, the hoplite turns it round and fights with the bronze spike.",
      "Yaprak biçimli demir uçlu, iki buçuk metrelik dişbudak mızrak. Uç kırılırsa hoplit onu çevirir ve bronz çiviyle dövüşür.",
      "Neolithic", R_DORY, [tool("shaft", "Blunt", 9, 2.1), tool("point", "Stab", 20, 2.2, 0.34)],
      mass=2.0, work=8500, painter="spear_long", stuff=("Metallic", "Woody"), stuff_count=50, skill=3, angle=-45,
      extra_tags=["MedievalMeleeDecent"], pargs={"head": "leaf", "shaft": "#8a6a44"})
melee(NATION, "Xiphos", "xiphos", "xiphos",
      "A short double-edged sword with a leaf-shaped blade, carried as a sidearm when the spear is lost.",
      "Yaprak biçimli ağzı olan kısa, çift ağızlı bir kılıç; mızrak kaybolduğunda yedek silah olarak taşınır.",
      "Medieval", R_BRONZE, [tool("handle", "Blunt", 8, 2), tool("point", "Stab", 17, 1.8, 0.24), tool("edge", "Cut", 16, 1.8, 0.22)],
      mass=1.1, work=12000, painter="xiphos", stuff_count=55, skill=4, angle=-45, extra_tags=["MedievalMeleeDecent"])
melee(NATION, "Kopis", "kopis", "kopis",
      "A heavy single-edged blade that curves forward, so that every blow lands like an axe.",
      "Öne kıvrılan, ağır, tek ağızlı bir kılıç; her darbe bir balta gibi iner.",
      "Medieval", R_BRONZE, [tool("handle", "Blunt", 9, 2), tool("edge", "Cut", 22, 2.2, 0.32)],
      mass=1.6, work=15000, painter="kopis", stuff_count=65, skill=5, angle=-45, extra_tags=["MedievalMeleeAdvanced"])
ARROW = projectile("HE_Arrow_Toxon", "toxon arrow", "toxon oku", "Arrow", 13, 48, "Things/Projectile/Arrow_Small", pen=0.18)
ranged(NATION, "Toxon", "toxon", "toxon",
       "A short recurve bow of horn and sinew. It draws fast and shoots hard for its size.",
       "Boynuz ve sinirden yapılmış kısa, çift kavisli bir yay. Boyuna göre hızlı çekilir ve sert atar.",
       "Neolithic", R_TOXON, ARROW, 1.1, 26.9, 1.3, (0.65, 0.72, 0.6, 0.45), 1.1, 8000, "recurve_bow",
       {"WoodLog": 40}, extra_tags=["NeolithicRangedDecent"])

# ------------------------------------------------------------------ apparel
apparel(NATION, "Corinthian", "Corinthian helmet", "Korint miğferi",
        "A bronze helmet beaten from a single sheet, with a nose guard, long cheek pieces and a horsehair crest. It hides the face completely.",
        "Tek bir levhadan dövülmüş, burun korumalı, uzun yanak parçalı ve at kılı sorguçlu bronz bir miğfer. Yüzü tamamen gizler.",
        "Medieval", R_HOPLITE, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead", "FullHead"],
        {"MaxHitPoints": 120, "StuffEffectMultiplierArmor": 0.62, "StuffEffectMultiplierInsulation_Cold": 0.15, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet2", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=55, work=4600, mass=2.4, users=SMITHY, skill=6, head=True,
        equipped={"SocialImpact": 0.02}, pargs={"kind": "corinthian"})
apparel(NATION, "Linothorax", "linothorax", "linothoraks",
        "Many layers of linen glued and stitched together into a stiff cuirass, with hanging strips to guard the hips. Light, cool and surprisingly tough.",
        "Birbirine yapıştırılıp dikilmiş birçok keten katmanından sert bir göğüslük; kalçaları koruyan sarkık şeritleri vardır. Hafif, serin ve şaşırtıcı derecede dayanıklıdır.",
        "Medieval", R_HOPLITE, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders"],
        {"MaxHitPoints": 180, "StuffEffectMultiplierArmor": 0.5, "StuffEffectMultiplierInsulation_Cold": 0.25, "StuffEffectMultiplierInsulation_Heat": 0.20},
        "torso2", parent="ArmorSmithableBase", stuff=("Fabric", "Leathery"), stuff_count=120, cost={"Steel": 15}, work=18000, mass=4.5,
        users=SMITHY, skill=5, equipped={"MoveSpeed": -0.08}, tags=["MedievalMilitary"], pargs={"kind": "linothorax"})
apparel(NATION, "Chiton", "chiton", "khiton",
        "A light tunic pinned at the shoulders and belted at the waist. Comfortable in the heat and handsome in the agora.",
        "Omuzlardan iğnelenmiş, belden kuşaklanmış hafif bir tunik. Sıcakta rahattır, agorada yakışıklı durur.",
        "Neolithic", R_CHITON, "TribalA/TribalA", ["OnSkin"], ["Torso", "Shoulders", "Legs"],
        {"MaxHitPoints": 100, "StuffEffectMultiplierArmor": 0.15, "StuffEffectMultiplierInsulation_Cold": 0.35, "StuffEffectMultiplierInsulation_Heat": 0.6},
        "torso2", stuff=("Fabric",), stuff_count=55, work=3500, mass=0.5, equipped={"SocialImpact": 0.02}, pargs={"kind": "chiton"})

# ------------------------------------------------------------------ buildings and floors
deco(NATION, "Hoplon", "hoplon display", "hoplon sergisi",
     "A great bronze-faced round shield painted with the owl of the league, hung where guests can admire it.",
     "Birliğin baykuşuyla boyanmış, bronz yüzlü büyük yuvarlak bir kalkan; misafirlerin hayran kalabileceği bir yere asılır.",
     R_HOPLITE, (1, 1), "hoplon", beauty=10, work=3000, stuff=("Metallic",), stuff_count=50, cost={"WoodLog": 20}, hp=150,
     category="Art", passability="Standable", fill=0.0)
deco(NATION, "Column", "hero column", "kahraman sütunu",
     "A fluted marble column crowned with the bronze statue of a hero. Every city in Hellas has a forest of them.",
     "Bir kahramanın bronz heykeliyle taçlanmış yivli mermer bir sütun. Hellas'taki her şehirde bunlardan bir orman vardır.",
     R_COLUMNS, (1, 1), "column", beauty=18, work=6000, stuff=("Stony",), stuff_count=140, cost={"Steel": 15}, hp=300,
     category="Art", draw_size="(1,2)")
deco(NATION, "Stage", "theatre stage", "tiyatro sahnesi",
     "A raised wooden stage before a painted backdrop of columns, with the masks of comedy and tragedy above. Colonists gather in front of it to watch and to perform.",
     "Sütunlarla boyanmış bir dekorun önünde, üstünde komedi ve tragedya maskeleri bulunan yükseltilmiş ahşap bir sahne. Kolonistler izlemek ve oynamak için önünde toplanır.",
     R_THEATRON, (3, 2), "theatre", beauty=12, work=9000, stuff=("Woody", "Stony"), stuff_count=180, cost={"Cloth": 40}, hp=350,
     joy="Social", minify=False)
floor(NATION, "Meander", "meander floor", "menderes zemin",
      "Pale limestone slabs framed by a dark border of the endless key pattern.",
      "Sonsuz anahtar deseninden koyu bir kenarla çerçevelenmiş açık renkli kireçtaşı levhalar.",
      R_MEANDER, "floor_meander", beauty=3, cost={"BlocksLimestone": 4}, work=1100)

# ------------------------------------------------------------------ food and trade goods
food(NATION, "Maza", "maza", "maza",
     "Flat barley cakes kneaded with olive oil and honey, served with a few olives and a lump of cheese.",
     "Zeytinyağı ve balla yoğrulmuş yassı arpa çörekleri; birkaç zeytin ve bir parça peynirle sunulur.",
     R_MAZA, "food2", nutrition=0.9, value=21, rot_days=7, pargs={"kind": "maza"})
resource(NATION, "OliveOil", "olive oil", "zeytinyağı",
         "A sealed jar of green-gold oil pressed from the first olives of the season. Lamp fuel, medicine and luxury in one.",
         "Mevsimin ilk zeytinlerinden sıkılmış yeşil-altın yağla dolu mühürlü bir küp. Kandil yakıtı, ilaç ve lüks bir arada.",
         14, "goods", mass=0.7, stack=25, pargs={"kind": "oil"})
