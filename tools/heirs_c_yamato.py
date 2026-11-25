"""Yamato Shogunate: nation, research branch, weapons, armour, buildings, floors and food."""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Yamato"
FN = "Nations/HE_Yamato.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Yamato",
                 label=T("Yamato Shogunate", "Yamato Şogunluğu"),
                 description=T("Descendants of the colony ship Takamagahara, the clans of Yamato rebuilt the old order of their islands: an emperor who reigns in silence, a shogun who rules in his name and warrior houses bound by duty. They value craft above wealth and patience above speed, and their swordsmiths are the finest in the world.",
                               "Takamagahara koloni gemisinin torunları olan Yamato klanları, adalarının eski düzenini yeniden kurdu: sessizce hüküm süren bir imparator, onun adına yöneten bir şogun ve göreve bağlı savaşçı haneleri. Zanaatı servetten, sabrı hızdan üstün tutarlar; kılıç ustaları dünyanın en iyileridir."),
                 color="(0.20, 0.22, 0.33)", iconPath="HeirsOfEarth/UI/HE_Yamato",
                 rulerTitle=T("Shogun", "Şogun"), adjective=T("Yamato", "Yamato"), release=1)
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Yamato", "nation_icon", color="#2b3654", emblem="mon")

# ------------------------------------------------------------------ research: Neolithic
R_YARI = research(NATION, "Yari", "yari", "yari",
                  "The straight-bladed spear of the foot soldiers, long enough to keep a horseman at bay.",
                  "Piyadelerin düz ağızlı mızrağı; bir atlıyı uzakta tutacak kadar uzundur.",
                  450, "Neolithic", 0, 0)
R_YUMI = research(NATION, "Yumi", "yumi", "yumi",
                  "The tall asymmetric bow of Yamato, gripped below its middle and drawn to the ear.",
                  "Ortasının altından tutulan ve kulağa kadar çekilen, Yamato'nun uzun asimetrik yayı.",
                  550, "Neolithic", 1, 0)
R_TATAMI = research(NATION, "Tatami", "tatami and gravel gardens", "tatami ve çakıl bahçeleri",
                    "Lay woven straw tatami mats and rake white gravel into the patterns of still water.",
                    "Örülmüş saman tatami hasırları ser ve beyaz çakılı durgun su desenlerine tırmıkla.",
                    500, "Neolithic", 2, 0)
R_KIMONO = research(NATION, "Kimono", "kimono", "kimono",
                    "Sew the wrapped and belted robe worn by every class of Yamato.",
                    "Yamato'nun her sınıfının giydiği sarmalı ve kuşaklı giysiyi dik.",
                    400, "Neolithic", 0, 1, prereqs=[R_YARI])
R_ONIGIRI = research(NATION, "Onigiri", "onigiri", "onigiri",
                     "Rice pressed into triangles and wrapped in seaweed: the travelling food of soldiers and pilgrims.",
                     "Üçgen biçiminde sıkıştırılıp yosuna sarılmış pirinç: askerlerin ve hacıların yol yemeği.",
                     400, "Neolithic", 1, 1)
R_TORII = research(NATION, "Torii", "torii gates", "torii kapıları",
                   "Raise the red gates that mark the passage from the everyday world into a sacred place.",
                   "Gündelik dünyadan kutsal bir yere geçişi işaret eden kırmızı kapıları dik.",
                   600, "Neolithic", 2, 1, prereqs=[R_TATAMI])
R_LEVY = research(NATION, "Levy", "ashigaru levy", "ashigaru seferberliği",
                  "Every farmer keeps a spear by the door and knows where to run when the drum sounds.",
                  "Her çiftçi kapısının yanında bir mızrak tutar ve davul çaldığında nereye koşacağını bilir.",
                  700, "Neolithic", 0, 2, prereqs=[R_KIMONO], knowledge=15, tradition=True,
                  stats=[("MoveSpeed", 0, 1.03, "Colonists")],
                  effect=T("Colonists move 3% faster.", "Kolonistler %3 daha hızlı yürür."))
R_KYUDO = research(NATION, "Kyudo", "kyudo", "kyudo",
                   "The way of the bow: a calm breath, a perfect posture and an arrow that is released rather than shot.",
                   "Yayın yolu: sakin bir nefes, kusursuz bir duruş ve atılmaktan çok bırakılan bir ok.",
                   800, "Neolithic", 1, 2, prereqs=[R_YUMI], knowledge=20, tradition=True,
                   stats=[("ShootingAccuracyPawn", 2, 1, "Colonists")],
                   effect=T("Colonists gain +2 shooting accuracy.", "Kolonistler +2 atış isabeti kazanır."))
R_ZEN = research(NATION, "Zen", "zen garden", "zen bahçesi",
                 "Raking gravel around a few stones every morning teaches the mind to settle like the sand.",
                 "Her sabah birkaç taşın çevresindeki çakılı tırmıklamak, zihne kum gibi durulmayı öğretir.",
                 900, "Neolithic", 2, 2, prereqs=[R_TORII], knowledge=20, tradition=True,
                 stats=[("MentalBreakThreshold", -0.03, 1, "Colonists")],
                 effect=T("Colonists' mental break threshold drops by 3%.", "Kolonistlerin zihinsel çöküş eşiği %3 düşer."))
# ------------------------------------------------------------------ research: Medieval
R_STEEL = research(NATION, "Tamahagane", "tamahagane steel", "tamahagane çeliği",
                   "Smelt jewel steel in a clay furnace and fold it again and again into blades with a soft spine and a hard edge.",
                   "Kil bir fırında mücevher çeliği erit ve onu tekrar tekrar katlayarak sırtı yumuşak, ağzı sert bıçaklara dönüştür.",
                   900, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_TEA = research(NATION, "TeaHouse", "tea house", "çay evi",
                 "Build a low table for the tea ceremony and stone lanterns to light the garden path.",
                 "Çay töreni için alçak bir masa ve bahçe yolunu aydınlatacak taş fenerler yap.",
                 800, "Medieval", 1, 0, prereqs=[R_TORII], knowledge=15)
R_DOJO = research(NATION, "Dojo", "dojo", "dojo",
                  "A training hall with straw posts and racks for practice swords.",
                  "Saman kazıklı ve talim kılıçları için raflı bir eğitim salonu.",
                  900, "Medieval", 2, 0, prereqs=[R_YARI], knowledge=15)
R_YOROI = research(NATION, "Yoroi", "yoroi armour", "yoroi zırhı",
                   "Lacquered lamellar armour laced with silk, and the horned kabuto helmet of the samurai.",
                   "İpekle bağlanmış lake lameller zırh ve samurayın boynuzlu kabuto miğferi.",
                   1200, "Medieval", 0, 1, prereqs=[R_STEEL], knowledge=25)
R_CEREMONY = research(NATION, "Ceremony", "tea ceremony", "çay töreni",
                      "Every movement of the host is fixed and unhurried. Guests leave lighter than they came.",
                      "Ev sahibinin her hareketi belirli ve acelesizdir. Misafirler geldiklerinden daha hafif ayrılır.",
                      1000, "Medieval", 1, 1, prereqs=[R_TEA], knowledge=25, tradition=True,
                      stats=[("JoyGainFactor", 0, 1.15, "Colonists")],
                      effect=T("Colonists gain recreation 15% faster.", "Kolonistler eğlenceyi %15 daha hızlı kazanır."))
R_FOLDS = research(NATION, "Folds", "forged folds", "katlanmış dövme",
                   "The smith's patience becomes the whole colony's habit: measure twice, strike once.",
                   "Demircinin sabrı bütün koloninin alışkanlığı olur: iki kez ölç, bir kez vur.",
                   1200, "Medieval", 0, 2, prereqs=[R_STEEL], knowledge=30, tradition=True,
                   stats=[("GeneralLaborSpeed", 0, 1.10, "Colonists")],
                   effect=T("Colonists do general labour (smithing, crafting, butchering, cutting stone) 10% faster.",
                            "Kolonistler genel işleri (demircilik, zanaat, kasaplık, taş kesme) %10 daha hızlı yapar."))
R_BUSHIDO = research(NATION, "Bushido", "bushido", "bushido",
                     "The way of the warrior: duty before life, calm before pain.",
                     "Savaşçının yolu: hayattan önce görev, acıdan önce sükûnet.",
                     1400, "Medieval", 0, 3, prereqs=[R_YOROI], knowledge=40, tradition=True,
                     stats=[("MeleeDodgeChance", 3, 1, "Colonists"), ("PainShockThreshold", 0.05, 1, "Colonists")],
                     effect=T("Colonists gain +3 melee dodge chance and +5% pain shock threshold.",
                              "Kolonistler +3 yakın dövüşte kaçınma ve +%5 acı şoku eşiği kazanır."))
R_MASTER = research(NATION, "MasterCraft", "master craft", "usta zanaat",
                    "A Yamato craftsman would rather make one perfect thing than ten good ones.",
                    "Bir Yamato zanaatkârı on iyi şey yerine tek bir kusursuz şey yapmayı yeğler.",
                    1600, "Medieval", 1, 3, prereqs=[R_FOLDS], knowledge=45, tradition=True, quality=0.12,
                    stats=[("WorkSpeedGlobal", 0, 0.95, "Colonists")],
                    effect=T("Crafted items have a 12% chance to come out one quality level higher, but colonists work 5% slower.",
                             "Üretilen eşyaların %12 ihtimalle bir kalite üstü çıkar, ama kolonistler %5 daha yavaş çalışır."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Katana", "katana", "katana",
      "A curved single-edged sword of folded steel with a hard, wavy temper line. It cuts cleanly and quickly.",
      "Sert, dalgalı bir su verme çizgisi olan, katlanmış çelikten eğri, tek ağızlı kılıç. Temiz ve hızlı keser.",
      "Medieval", R_STEEL, [tool("handle", "Blunt", 8, 2), tool("point", "Stab", 16, 1.9, 0.28), tool("edge", "Cut", 19, 1.9, 0.30)],
      mass=1.2, work=18000, painter="katana_blade", stuff_count=70, skill=6, angle=-45, extra_tags=["MedievalMeleeAdvanced"])
melee(NATION, "Yari", "yari", "yari",
      "A long spear with a straight, triangular blade. Simple, cheap and deadly in a disciplined line.",
      "Düz, üçgen ağızlı uzun bir mızrak. Basit, ucuz ve disiplinli bir hatta ölümcül.",
      "Neolithic", R_YARI, [tool("shaft", "Blunt", 9, 2.1), tool("point", "Stab", 21, 2.3, 0.36)],
      mass=2.2, work=9000, painter="spear_long", stuff=("Metallic", "Woody"), stuff_count=50, skill=3, angle=-45,
      extra_tags=["MedievalMeleeDecent"], pargs={"head": "yari", "shaft": "#3a2418"})
melee(NATION, "Naginata", "naginata", "naginata",
      "A curved blade on a long lacquered pole, swung in wide arcs to keep many foes at a distance.",
      "Uzun, lake bir sapın ucunda eğri bir ağız; birçok düşmanı uzakta tutmak için geniş yaylarla savrulur.",
      "Medieval", R_STEEL, [tool("shaft", "Blunt", 9, 2.0), tool("point", "Stab", 17, 2.2, 0.25), tool("edge", "Cut", 22, 2.3, 0.30)],
      mass=2.6, work=16000, painter="spear_long", stuff_count=60, skill=5, angle=-45, extra_tags=["MedievalMeleeAdvanced"],
      pargs={"head": "naginata", "shaft": "#2a1a14"})
ARROW = projectile("HE_Arrow_Yumi", "yumi arrow", "yumi oku", "Arrow", 15, 46, "Things/Projectile/Arrow_Small", pen=0.22)
ranged(NATION, "Yumi", "yumi", "yumi",
       "A tall bow of laminated bamboo, longer than its archer. It shoots far and true in trained hands.",
       "Okçusundan uzun, lamine bambudan bir yay. Eğitimli ellerde uzağa ve isabetle atar.",
       "Neolithic", R_YUMI, ARROW, 1.35, 30.9, 1.6, (0.6, 0.72, 0.68, 0.56), 1.4, 9000, "long_bow",
       {"WoodLog": 50}, extra_tags=["NeolithicRangedDecent"], pargs={"kind": "yumi"})

# ------------------------------------------------------------------ apparel
apparel(NATION, "Kabuto", "kabuto", "kabuto",
        "A lacquered iron helmet with a flared neck guard of laced plates and gilded horns.",
        "Bağlı plakalardan geniş bir ense korumalı ve yaldızlı boynuzlu, lake demir bir miğfer.",
        "Medieval", R_YOROI, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 120, "StuffEffectMultiplierArmor": 0.58, "StuffEffectMultiplierInsulation_Cold": 0.18, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=50, work=4200, mass=2.2, users=SMITHY, skill=6, head=True,
        equipped={"SocialImpact": 0.03}, pargs={"kind": "kabuto"})
apparel(NATION, "Domaru", "do-maru", "do-maru",
        "Rows of small lacquered scales laced together with silk cord. Lighter than plate, it lets a warrior move freely.",
        "İpek kordonla birbirine bağlanmış sıra sıra küçük lake pullar. Plakadan hafiftir, savaşçının rahat hareket etmesini sağlar.",
        "Medieval", R_YOROI, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders", "Arms"],
        {"MaxHitPoints": 220, "StuffEffectMultiplierArmor": 0.76, "StuffEffectMultiplierInsulation_Cold": 0.45, "StuffEffectMultiplierInsulation_Heat": 0.05},
        "torso", parent="ArmorSmithableBase", stuff=("Metallic",), stuff_count=110, cost={"Cloth": 20}, work=26000, mass=7,
        users=SMITHY, skill=6, equipped={"MoveSpeed": -0.15}, tags=["MedievalMilitary"], pargs={"kind": "domaru"})
apparel(NATION, "Kimono", "kimono", "kimono",
        "A wrapped robe tied with a broad sash. Comfortable in summer and handsome at any ceremony.",
        "Geniş bir kuşakla bağlanan sarmal bir giysi. Yazın rahattır, her törende yakışıklı durur.",
        "Neolithic", R_KIMONO, "Duster/Duster", ["Shell"], ["Torso", "Shoulders", "Arms", "Legs"],
        {"MaxHitPoints": 110, "StuffEffectMultiplierArmor": 0.2, "StuffEffectMultiplierInsulation_Cold": 0.7, "StuffEffectMultiplierInsulation_Heat": 0.35},
        "torso", stuff=("Fabric",), stuff_count=70, work=5000, mass=0.8, equipped={"SocialImpact": 0.03}, pargs={"kind": "kimono"})

# ------------------------------------------------------------------ buildings and floors
deco(NATION, "Torii", "torii gate", "torii kapısı",
     "A tall red gate of two pillars and two lintels. Walking beneath it, people lower their voices.",
     "İki direk ve iki lentodan oluşan uzun kırmızı bir kapı. Altından geçerken insanlar seslerini alçaltır.",
     R_TORII, (3, 1), "torii", beauty=20, work=7000, stuff=("Woody", "Stony"), stuff_count=160, hp=400,
     passability="Standable", fill=0.0, minify=False, category="Art", draw_size="(3,2.25)")
deco(NATION, "Lantern", "stone lantern", "taş fener",
     "A carved stone lantern with a small flame inside. It lights a garden path softly through the night.",
     "İçinde küçük bir alev olan oyma taş fener. Gece boyunca bir bahçe yolunu yumuşakça aydınlatır.",
     R_TEA, (1, 1), "stone_lantern", beauty=6, work=2600, stuff=("Stony",), stuff_count=60, hp=200,
     glow=(7, "(252,197,133,0)"), category="Art", draw_size="(1,1.5)", extra={"tickerType": "Normal"},
     comps=[{"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": 1.2, "fuelCapacity": 10, "fuelFilter": {"thingDefs": ["WoodLog"]},
             "initialFuelPercent": 1, "showAllowAutoRefuelToggle": True}])
deco(NATION, "TeaTable", "tea table", "çay masası",
     "A low dark table set with an iron kettle and four cups. Colonists kneel around it for a quiet cup of tea.",
     "Demir bir çaydanlık ve dört fincanla kurulmuş alçak, koyu bir masa. Kolonistler sessiz bir fincan çay için çevresine diz çöker.",
     R_TEA, (2, 2), "table", beauty=4, work=2600, stuff=("Woody",), stuff_count=60, hp=140, joy="Social", pargs={"kind": "tea"})
deco(NATION, "Dojo", "dojo training post", "dojo talim direği",
     "A post wrapped in straw bundles. Colonists strike it again and again to train their sword arm.",
     "Saman demetlerine sarılmış bir direk. Kolonistler kılıç kollarını eğitmek için ona tekrar tekrar vurur.",
     R_DOJO, (1, 1), "training_post", beauty=0, work=1600, stuff=("Woody",), stuff_count=40, cost={"Hay": 20}, hp=150,
     joy="Gaming_Dexterity", draw_size="(1,1.5)")
deco(NATION, "Rack", "katana rack", "katana rafı",
     "A lacquered rack holding swords in their scabbards. A proud display of a house's blades.",
     "Kınlarındaki kılıçları tutan lake bir raf. Bir hanenin kılıçlarının gururlu bir sergisi.",
     R_DOJO, (2, 1), "weapon_rack", beauty=8, work=2400, stuff=("Woody",), stuff_count=50, cost={"Steel": 20}, hp=120,
     category="Art", draw_size="(2,1.25)")
floor(NATION, "Tatami", "tatami", "tatami",
      "Woven rush mats with dark cloth borders, soft underfoot and pleasant to sit on.",
      "Koyu kumaş kenarlı, ayak altında yumuşak ve oturması hoş örme hasır minderler.",
      R_TATAMI, "floor_tatami", beauty=2, cost={"Hay": 4, "Cloth": 1}, work=700)
floor(NATION, "Gravel", "raked gravel", "tırmıklanmış çakıl",
      "White gravel raked into gentle waves. Calming to look at, a little slow to walk across.",
      "Hafif dalgalar halinde tırmıklanmış beyaz çakıl. Bakması huzur verir, üzerinden yürümek biraz yavaştır.",
      R_TATAMI, "floor_gravel", beauty=3, cost={"BlocksGranite": 1}, work=600, path_cost=2)

# ------------------------------------------------------------------ food and trade goods
food(NATION, "Onigiri", "onigiri", "onigiri",
     "Triangles of pressed rice wrapped in seaweed, with a sour plum in the middle. Keeps well on the road.",
     "Ortasında ekşi bir erik olan, yosuna sarılı üçgen sıkıştırılmış pirinç. Yolda iyi dayanır.",
     R_ONIGIRI, "bowl", nutrition=0.9, value=20, rot_days=6, pargs={"kind": "onigiri"})
resource(NATION, "Sake", "sake flask", "sake şişesi",
         "A white porcelain flask of rice wine, sealed with wax. Sought after by traders everywhere.",
         "Mumla mühürlenmiş, pirinç şarabıyla dolu beyaz porselen bir şişe. Her yerde tüccarlar tarafından aranır.",
         16, "jar", mass=0.6, stack=25, pargs={"kind": "tokkuri"})
