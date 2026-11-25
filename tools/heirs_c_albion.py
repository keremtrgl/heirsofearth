"""Commonwealth of Albion (2.0): the industrial heir nation. Research, weapons, uniforms, steam power, floors and food."""
from heirs_data import add, tex
from heirs_kit import SMITHY, apparel, deco, floor, food, melee, projectile, ranged, research, resource, tool
from heirs_xml import Def, T

NATION = "Albion"
FN = "Nations/HE_Albion.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Albion",
                 label=T("Commonwealth of Albion", "Albion Topluluğu"),
                 description=T("The colony ship Avalon landed on a rainy island rich in coal and iron, and its people did what their ancestors had done: they dug, built and invented. Albion is the only heir nation with steam engines and rifles, ruled by a Lord Protector and a quarrelsome parliament. Its redcoats are disciplined, its merchants ambitious, and it has been at odds with Nova Roma for as long as anyone can remember.",
                               "Avalon koloni gemisi kömür ve demir bakımından zengin, yağmurlu bir adaya indi; halkı atalarının yaptığını yaptı: kazdı, inşa etti ve icat etti. Albion, buhar makineleri ve tüfekleri olan tek mirasçı devlettir; bir Lord Koruyucu ve kavgacı bir parlamento tarafından yönetilir. Kızılceketlileri disiplinli, tüccarları hırslıdır ve kimsenin hatırlayabildiği kadar uzun zamandır Nova Roma ile arası açıktır."),
                 color="(0.55, 0.10, 0.12)", iconPath="HeirsOfEarth/UI/HE_Albion",
                 rulerTitle=T("Lord Protector", "Lord Koruyucu"), adjective=T("Albion", "Albion"), release=2,
                 friends=["HE_Nord"], rivals=["HE_Roma"])
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Albion", "nation_icon", color="#8c1c22", emblem="lion")

# ------------------------------------------------------------------ research: Medieval
R_SABRE = research(NATION, "Sabre", "cavalry sabre", "süvari kılıcı",
                   "A curved, single-edged sword with a basket guard, made for cutting from the saddle.",
                   "Eyerden kesmek için yapılmış, sepet siperli, eğri, tek ağızlı bir kılıç.",
                   800, "Medieval", 0, 0, prereqs=["Smithing"], knowledge=10)
R_TWEED = research(NATION, "Tweed", "tweed mills", "tüvit dokuma",
                   "Weave rough, warm wool cloth in muted checks that shrugs off rain.",
                   "Yağmuru sırtından atan, sönük kareli, kaba ve sıcak yün kumaş doku.",
                   600, "Medieval", 1, 0)
R_BRICK = research(NATION, "Brick", "bricks and cobbles", "tuğla ve arnavut kaldırımı",
                   "Fire red bricks for courtyards and set rounded cobbles into the streets.",
                   "Avlular için kırmızı tuğla pişir ve sokaklara yuvarlak arnavut taşları döşe.",
                   600, "Medieval", 2, 0)
R_PIE = research(NATION, "MeatPie", "meat pie", "etli börek",
                 "Seal meat and gravy into a thick pastry crust that keeps for days and travels well.",
                 "Eti ve sosu günlerce dayanan ve yolda iyi taşınan kalın bir hamur kabuğuna kapat.",
                 500, "Medieval", 0, 1)
R_PUB = research(NATION, "Pub", "public house", "meyhane",
                 "A long oak table, a barrel of ale and a dartboard: the true parliament of Albion.",
                 "Uzun bir meşe masa, bir fıçı bira ve bir dart tahtası: Albion'un gerçek parlamentosu.",
                 700, "Medieval", 1, 1, prereqs=[R_TWEED])
R_ENCLOSURE = research(NATION, "Enclosure", "enclosure", "çitleme",
                       "Hedge the common fields and farm them for profit. The harvest grows; the neighbours grumble.",
                       "Ortak tarlaları çitle ve kâr için işle. Hasat büyür; komşular homurdanır.",
                       900, "Medieval", 2, 1, prereqs=[R_BRICK], knowledge=20, tradition=True,
                       stats=[("PlantHarvestYield", 0, 1.05, "Colonists"), ("NegotiationAbility", -0.05, 1, "Colonists")],
                       effect=T("Colonists harvest 5% more from plants but lose 5% negotiation ability.",
                                "Kolonistler bitkilerden %5 daha fazla hasat alır ama %5 müzakere yeteneği kaybeder."))
R_SANITATION = research(NATION, "Sanitation", "sanitation", "sağlık düzeni",
                        "Boil the water, drain the streets, wash the hands. Fevers pass faster in a clean town.",
                        "Suyu kaynat, sokakları kurut, elleri yıka. Temiz bir kasabada ateşli hastalıklar daha çabuk geçer.",
                        1000, "Medieval", 0, 2, prereqs=[R_PIE], knowledge=25, tradition=True,
                        stats=[("ImmunityGainSpeed", 0, 1.10, "Colonists")],
                        effect=T("Colonists gain immunity 10% faster.", "Kolonistler %10 daha hızlı bağışıklık kazanır."))
R_JOINTSTOCK = research(NATION, "JointStock", "joint-stock company", "anonim şirket",
                        "Pool the money of many, share the risk of every voyage and the profit of every bargain.",
                        "Birçok kişinin parasını birleştir, her seferin riskini ve her pazarlığın kârını paylaş.",
                        1100, "Medieval", 1, 2, prereqs=[R_PUB], knowledge=25, tradition=True,
                        stats=[("TradePriceImprovement", 0.05, 1, "Colonists")],
                        effect=T("Colonists get 5% better trade prices.", "Kolonistler %5 daha iyi ticaret fiyatı alır."))
R_CHARTS = research(NATION, "Charts", "Royal Navy charts", "kraliyet donanması haritaları",
                    "Surveyed coasts, measured rivers and well-kept roads: Albion's caravans never lose their way.",
                    "Ölçülmüş kıyılar, haritalanmış nehirler ve bakımlı yollar: Albion kervanları yolunu hiç kaybetmez.",
                    1100, "Medieval", 2, 2, prereqs=[R_ENCLOSURE], knowledge=30, tradition=True, caravan=0.10,
                    effect=T("Caravans travel 10% faster.", "Kervanlar %10 daha hızlı yol alır."))
# ------------------------------------------------------------------ research: Industrial
R_MUSKET = research(NATION, "Musket", "flintlock musket", "çakmaklı tüfek",
                    "A smoothbore flintlock: slow to load, loud, inaccurate past fifty paces and terrifying in a volley.",
                    "Yivsiz bir çakmaklı tüfek: doldurması yavaş, gürültülü, elli adımdan sonra isabetsiz ve yaylım ateşinde dehşet verici.",
                    1200, "Industrial", 0, 0, prereqs=[R_SABRE], knowledge=20)
R_REDCOAT = research(NATION, "Redcoat", "redcoat uniform", "kızılceket üniforması",
                     "A red wool coat with white facings and a tall shako. A line of them is seen from a mile away, and meant to be.",
                     "Beyaz yakalı kırmızı yün bir ceket ve uzun bir şako. Bir sıra kızılceketli bir milden görülür; amaç da budur.",
                     900, "Industrial", 1, 0, prereqs=[R_TWEED], knowledge=15)
R_STEAM = research(NATION, "SteamEngine", "steam engine", "buhar makinesi",
                   "Boil water with wood, push a piston with the steam and turn a dynamo with the piston.",
                   "Suyu odunla kaynat, buharla bir pistonu it ve pistonla bir dinamoyu döndür.",
                   1400, "Industrial", 2, 0, prereqs=["Electricity"], knowledge=25)
R_RIFLE = research(NATION, "Rifle", "rifled musket", "yivli tüfek",
                   "Cut spiral grooves into the barrel and fix a bayonet: longer range, better aim and a spear at the end.",
                   "Namluya sarmal yivler aç ve bir süngü tak: daha uzun menzil, daha iyi nişan ve ucunda bir mızrak.",
                   1600, "Industrial", 0, 1, prereqs=[R_MUSKET], knowledge=35)
R_DRILL = research(NATION, "Drill", "drill sergeant", "talim çavuşu",
                   "Load, present, fire. Again. Again. Until it is done without thinking.",
                   "Doldur, nişan al, ateş. Yine. Yine. Düşünmeden yapılana kadar.",
                   1300, "Industrial", 1, 1, prereqs=[R_REDCOAT], knowledge=35, tradition=True,
                   stats=[("ShootingAccuracyPawn", 2, 1, "Colonists")],
                   effect=T("Colonists gain +2 shooting accuracy.", "Kolonistler +2 atış isabeti kazanır."))
R_STEAMPOWER = research(NATION, "SteamPower", "steam power", "buhar gücü",
                        "Belts and shafts carry the engine's power to every bench. Less waste, more work.",
                        "Kayışlar ve miller makinenin gücünü her tezgâha taşır. Daha az israf, daha çok iş.",
                        1500, "Industrial", 2, 1, prereqs=[R_STEAM], knowledge=40, tradition=True,
                        stats=[("WorkTableEfficiencyFactor", 0, 1.05, "PlayerBuildings")],
                        effect=T("Your work tables use 5% fewer resources.", "Çalışma tezgâhların %5 daha az malzeme kullanır."))
R_FACTORY = research(NATION, "FactoryOrder", "factory order", "fabrika düzeni",
                     "The whistle at dawn, the shift, the quota. Benches never stand idle, and neither do the workers.",
                     "Şafakta düdük, vardiya, kota. Tezgâhlar hiç boş durmaz, işçiler de.",
                     1800, "Industrial", 2, 2, prereqs=[R_STEAMPOWER], knowledge=45, tradition=True,
                     stats=[("WorkTableWorkSpeedFactor", 0, 1.12, "PlayerBuildings"), ("MentalBreakThreshold", 0.02, 1, "Colonists")],
                     effect=T("Your work tables work 12% faster, but colonists' mental break threshold rises by 2%.",
                              "Çalışma tezgâhların %12 daha hızlı çalışır, ama kolonistlerin zihinsel çöküş eşiği %2 yükselir."))

# ------------------------------------------------------------------ weapons
melee(NATION, "Sabre", "cavalry sabre", "süvari kılıcı",
      "A curved single-edged blade with a steel basket guard. It cuts fast and keeps the hand safe.",
      "Çelik sepet siperli, eğri, tek ağızlı bir kılıç. Hızlı keser ve eli güvende tutar.",
      "Medieval", R_SABRE, [tool("guard", "Blunt", 9, 2), tool("point", "Stab", 14, 1.9, 0.20), tool("edge", "Cut", 19, 1.9, 0.26)],
      mass=1.3, work=14000, painter="sabre", stuff_count=60, skill=5, angle=-45, extra_tags=["MedievalMeleeDecent"])
BALL = projectile("HE_Bullet_Musket", "musket ball", "tüfek mermisi", "Bullet", 20, 70, "Things/Projectile/Bullet_Small", pen=0.30)
ranged(NATION, "Musket", "flintlock musket", "çakmaklı tüfek",
       "A long smoothbore flintlock. Slow to reload and wild at range, but a heavy lead ball stops anything it hits.",
       "Uzun, yivsiz bir çakmaklı tüfek. Yeniden doldurması yavaş ve uzakta isabetsizdir, ama ağır kurşun bilye vurduğu her şeyi durdurur.",
       "Industrial", R_MUSKET, BALL, 1.8, 25.9, 2.8, (0.45, 0.6, 0.45, 0.28), 4.6, 16000, "musket",
       {"Steel": 60, "WoodLog": 30}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True, klass=("Ranged", "RangedHeavy", "LongShots"),
       tools=[tool("stock", "Blunt", 10, 2.1), tool("barrel", "Blunt", 9, 2.0)])
RIFLE_BALL = projectile("HE_Bullet_Rifle", "rifle bullet", "tüfek kurşunu", "Bullet", 18, 80, "Things/Projectile/Bullet_Small", pen=0.34)
ranged(NATION, "Rifle", "rifled musket", "yivli tüfek",
       "A muzzle-loading rifle with a socket bayonet. It hits a man at three hundred paces and still fights when the powder runs out.",
       "Soket süngülü, ağızdan dolma bir tüfek. Üç yüz adımda bir adamı vurur ve barut bittiğinde de dövüşmeye devam eder.",
       "Industrial", R_RIFLE, RIFLE_BALL, 1.6, 33.9, 2.0, (0.5, 0.7, 0.66, 0.52), 4.4, 22000, "bayonet_rifle",
       {"Steel": 70, "WoodLog": 25, "ComponentIndustrial": 1}, sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True,
       tools=[tool("stock", "Blunt", 10, 2.1), tool("bayonet", "Stab", 16, 2.0, 0.28)])

# ------------------------------------------------------------------ apparel
apparel(NATION, "Shako", "shako", "şako",
        "A tall stiff cap with a brass plate and a short plume. It makes a soldier look half a head taller.",
        "Pirinç plakalı ve kısa sorguçlu, uzun, sert bir başlık. Bir askeri yarım baş daha uzun gösterir.",
        "Industrial", R_REDCOAT, "BowlerHat/BowlerHat", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 80, "StuffEffectMultiplierArmor": 0.2, "StuffEffectMultiplierInsulation_Cold": 0.25, "StuffEffectMultiplierInsulation_Heat": 0.1},
        "helmet2", stuff=("Fabric", "Leathery"), stuff_count=30, cost={"Steel": 5}, work=2400, mass=0.4, head=True,
        equipped={"SocialImpact": 0.03}, pargs={"kind": "shako"})
apparel(NATION, "Redcoat", "redcoat", "kızılceket",
        "A red wool coat with white facings, brass buttons and crossed white belts. Warm, sturdy and impossible to miss.",
        "Beyaz yakalı, pirinç düğmeli ve çapraz beyaz kemerli kırmızı yün bir ceket. Sıcak, sağlam ve gözden kaçması imkânsız.",
        "Industrial", R_REDCOAT, "Jacket/Jacket", ["Shell"], ["Torso", "Neck", "Shoulders", "Arms"],
        {"MaxHitPoints": 160, "ArmorRating_Sharp": 0.12, "ArmorRating_Blunt": 0.08, "Insulation_Cold": 18, "Insulation_Heat": 4},
        "torso2", stuff=None, cost={"Cloth": 70, "Steel": 5}, work=9000, mass=1.6, color="(0.66, 0.12, 0.12)",
        equipped={"SocialImpact": 0.04}, tags=["IndustrialMilitaryBasic"], pargs={"kind": "redcoat"})

# ------------------------------------------------------------------ buildings and floors
deco(NATION, "SteamEngine", "steam engine", "buhar makinesi",
     "A wood-fired boiler driving a beam engine and a dynamo. It produces more power than a simple generator, and plenty of noise and smoke.",
     "Bir kiriş makinesini ve bir dinamoyu çalıştıran odunla ısıtılan bir kazan. Basit bir jeneratörden daha fazla güç ve bolca gürültü ve duman üretir.",
     R_STEAM, (2, 2), "steam_engine", beauty=-10, work=4500, stuff=None, cost={"Steel": 160, "ComponentIndustrial": 3, "BlocksGranite": 30},
     hp=400, fill=0.9, minify=False, category="Temperature", designation="Power",
     extra={"tickerType": "Normal", "drawerType": "MapMeshAndRealTime", "blockWind": True, "castEdgeShadows": False,
            "building": {"destroySound": "BuildingDestroyed_Metal_Medium"}},
     comps=[{"@Class": "CompProperties_Power", "compClass": "CompPowerPlant", "basePowerConsumption": -1400, "transmitsPower": True,
             "soundAmbientProducingPower": "WoodFiredGenerator_Ambience"},
            {"@Class": "CompProperties_Flickable"},
            {"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": 26, "fuelCapacity": 90, "fuelFilter": {"thingDefs": ["WoodLog"]},
             "showAllowAutoRefuelToggle": True, "canEjectFuel": True},
            {"@Class": "CompProperties_Glower", "glowRadius": 5, "glowColor": "(217,112,33,0)"},
            {"@Class": "CompProperties_HeatPusher", "compClass": "CompHeatPusherPowered", "heatPerSecond": 6}])
deco(NATION, "PubTable", "pub table", "meyhane masası",
     "A long, scarred oak table with tankards of ale, a game of cards and a dartboard on the post. Colonists gather here to drink, argue and lose at darts.",
     "Bira maşrapaları, bir el kâğıt oyunu ve direkte bir dart tahtası olan uzun, çizik bir meşe masa. Kolonistler burada içmek, tartışmak ve dartta kaybetmek için toplanır.",
     R_PUB, (3, 2), "table", beauty=4, work=3000, stuff=("Woody",), stuff_count=90, hp=160, joy="Social", pargs={"kind": "pub"})
floor(NATION, "Cobble", "cobblestone street", "arnavut kaldırımı",
      "Rounded stones set close in sand. Hard-wearing and quick to walk on, if noisy under boots.",
      "Kumun içine sıkıca dizilmiş yuvarlak taşlar. Dayanıklı ve üzerinde yürümesi hızlı, ama çizme altında gürültülü.",
      R_BRICK, "floor_cobble", beauty=1, cost={"BlocksGranite": 3}, work=700)
floor(NATION, "Brick", "brick paving", "tuğla döşeme",
      "Red bricks laid in a herringbone pattern. Warm-looking and tidy.",
      "Balıksırtı deseninde döşenmiş kırmızı tuğlalar. Sıcak görünümlü ve düzenli.",
      R_BRICK, "floor_brick", beauty=2, cost={"BlocksSandstone": 3}, work=900)

# ------------------------------------------------------------------ food and trade goods
food(NATION, "MeatPie", "meat pie", "etli börek",
     "Chunks of meat and onion in thick gravy, sealed in a golden crust. Filling, warm and good for days.",
     "Koyu bir sosun içinde et ve soğan parçaları, altın rengi bir kabuğa kapatılmış. Doyurucu, sıcak ve günlerce iyi.",
     R_PIE, "food2", nutrition=0.9, value=21, rot_days=8, ingredients=("MeatRaw",), pargs={"kind": "pie"})
resource(NATION, "Tweed", "tweed", "tüvit",
         "Heavy checked wool woven on Albion's mills. A warm, rain-proof fabric that wears well; weave it from any wool at a textile mill.",
         "Albion değirmenlerinde dokunmuş ağır, kareli yün. Sıcak, yağmur geçirmez ve dayanıklı bir kumaş; dokuma fabrikasında her türlü yünden dokunur.",
         4, "goods", mass=0.03, stack=100, category="Textiles", pargs={"kind": "tweed"},
         extra={"statBases": {"MarketValue": 4, "Mass": 0.03, "MaxHitPoints": 90, "Flammability": 0.4, "DeteriorationRate": 2,
                              "StuffPower_Armor_Sharp": 0.45, "StuffPower_Armor_Blunt": 0.05, "StuffPower_Armor_Heat": 1.1,
                              "StuffPower_Insulation_Cold": 30, "StuffPower_Insulation_Heat": 14},
                "stuffProps": {"categories": ["Fabric"], "commonality": 0.05, "color": "(106,106,78)",
                               "statFactors": {"Flammability": 1.5, "Beauty": 1.6}, "canSuggestUseDefaultStuff": True},
                "burnableByRecipe": True, "healthAffectsPrice": False, "minRewardCount": 30})
