"""Nova Roma: nation, research branch, weapons, buildings and floors."""
from heirs_data import add, tex
from heirs_kit import N, deco, floor, melee, research, tool
from heirs_xml import Def, T

NATION = "Roma"
FN = "Nations/HE_Roma.xml"

NATION_DEF = Def("HeirsOfEarth.NationDef", "HE_Roma",
            label=T("Nova Roma Republic", "Nova Roma Cumhuriyeti"),
            description=T("Heirs of the colony ship Aeternitas, the citizens of Nova Roma rebuilt the republic of their ancestors on a new world: a senate, two consuls, roads that run straight across any land and legions that march in step. They are master builders and disciplined soldiers, proud of their law and slow to forgive.",
                          "Aeternitas koloni gemisinin torunları olan Nova Roma yurttaşları, atalarının cumhuriyetini yeni bir dünyada yeniden kurdu: bir senato, iki konsül, her toprağı dümdüz kesen yollar ve adım adım yürüyen lejyonlar. Usta inşaatçı ve disiplinli askerdirler; hukuklarıyla gurur duyar, kolay affetmezler."),
            color="(0.56, 0.16, 0.14)", iconPath="HeirsOfEarth/UI/HE_Roma",
            rulerTitle=T("Consul", "Konsül"), adjective=T("Nova Roman", "Nova Roma"), release=1)
add(FN, NATION_DEF)
tex("HeirsOfEarth/UI/HE_Roma", "nation_icon", color="#8e2a24", emblem="eagle")

# ------------------------------------------------------------------ research (0.1 core of the branch)
R_STANDARD = research(NATION, "Standard", "legion standards", "lejyon sancakları",
                      "Weave the red standards of the legions and raise them over your halls.",
                      "Lejyonların kırmızı sancaklarını doku ve salonlarının üzerine dik.",
                      400, "Neolithic", 0, 0)
R_CONCRETE = research(NATION, "Concrete", "Roman concrete", "Roma betonu",
                      "Mix lime, volcanic ash and rubble into a concrete that hardens even under water. Unlocks concrete floors.",
                      "Kireç, volkanik kül ve molozu su altında bile sertleşen bir betona dönüştür. Beton zemini açar.",
                      500, "Neolithic", 1, 0)
R_SMITHING = research(NATION, "Smithing", "legion smithing", "lejyon demirciliği",
                      "Forge the gladius, the short sword of the legions.",
                      "Lejyonların kısa kılıcı gladiusu döv.",
                      700, "Medieval", 0, 0, prereqs=["Smithing"])
R_PILUM = research(NATION, "Pilum", "pilum", "pilum",
                   "Make the pilum, a heavy spear with a long iron shank that punches through shields and armor.",
                   "Kalkan ve zırhı delen uzun demir saplı ağır mızrak pilumu yap.",
                   800, "Medieval", 0, 1, prereqs=[R_SMITHING], knowledge=10)
R_ROADS = research(NATION, "Roads", "Roman roads", "Roma yolları",
                   "Build paved roads that let people walk quickly and caravans travel far.",
                   "İnsanların hızlı yürümesini ve kervanların uzağa gitmesini sağlayan taş döşeli yollar yap.",
                   900, "Medieval", 1, 1, prereqs=[R_CONCRETE], knowledge=20, tradition=True, caravan=0.10,
                   effect=T("Unlocks Roman road floors. Your caravans travel 10% faster.",
                            "Roma yolu zeminini açar. Kervanların %10 daha hızlı yolculuk eder."))
R_ENGINEERS = research(NATION, "Engineers", "castrum engineers", "castrum mühendisleri",
                       "Every legionary is also a builder. Each night the legion raises a fortified camp; your colonists learn to build just as quickly.",
                       "Her lejyoner aynı zamanda bir inşaatçıdır. Lejyon her gece tahkimatlı bir kamp kurar; kolonistlerin de o hızla inşa etmeyi öğrenir.",
                       1200, "Medieval", 2, 1, prereqs=[R_CONCRETE], knowledge=30, tradition=True,
                       stats=[("ConstructionSpeed", 0, 1.15, "Colonists"), ("MiningSpeed", 0, 0.95, "Colonists")],
                       effect=T("Colonists build 15% faster but mine 5% slower: the legion's tools are made for building, not digging. Unlocks the legion brazier.",
                                "Kolonistler %15 daha hızlı inşa eder ama %5 daha yavaş kazar: lejyonun aletleri kazmak için değil, inşa için yapılmıştır. Lejyon mangalını açar."))
R_AQUEDUCT = research(NATION, "Aqueduct", "aqueducts", "su kemerleri",
                      "Raise arched aqueducts, the pride of every Roman town.",
                      "Her Roma kentinin gururu olan kemerli su kemerlerini yükselt.",
                      1400, "Medieval", 1, 2, prereqs=[R_ROADS], knowledge=40)
R_SENATE = research(NATION, "Senate", "senate records", "senato kayıtları",
                    "Keep careful records of everything your scholars learn about Nova Roma.",
                    "Âlimlerinin Nova Roma hakkında öğrendiği her şeyi titizlikle kaydet.",
                    1000, "Medieval", 2, 0, prereqs=[R_STANDARD], knowledge=25, tradition=True, study=0.25,
                    effect=T("Studying Nova Roman items gives 25% more knowledge.",
                             "Nova Roma eşyalarını incelemek %25 daha fazla bilgi verir."))

# ------------------------------------------------------------------ items
melee(NATION, "Gladius", "legion gladius", "lejyon gladiusu",
      "The short sword of the legions, forged with a broad stabbing point. Light and quick, it is made to strike from behind a shield wall.",
      "Lejyonların kısa kılıcı, geniş bir saplama ucuyla dövülmüş. Hafif ve hızlıdır, kalkan duvarının arkasından vurmak için yapılmıştır.",
      "Medieval", R_SMITHING,
      [tool("handle", "Blunt", 9, 2), tool("point", "Stab", 18, 1.9, 0.30), tool("edge", "Cut", 15, 2)],
      mass=0.9, work=13000, painter="gladius", stuff_count=55, skill=4)
melee(NATION, "Pilum", "pilum", "pilum",
      "A heavy javelin with a long soft-iron shank. In close fighting it is a spear whose point bends inside shields and armor and does not let go.",
      "Uzun yumuşak demir saplı ağır bir cirit. Yakın dövüşte, ucu kalkan ve zırhın içinde bükülüp bırakmayan bir mızraktır.",
      "Medieval", R_PILUM,
      [tool("shaft", "Blunt", 10, 2.2), tool("point", "Stab", 23, 2.6, 0.48)],
      mass=2.6, work=15000, painter="pilum", stuff=("Metallic",), stuff_count=45, cost={"WoodLog": 20}, skill=5, angle=-45)

deco(NATION, "Standard", "legion standard", "lejyon sancağı",
     "A red standard of the legions on a tall pole, crowned with a golden eagle. Soldiers stand straighter when they see it.",
     "Uzun bir direk üzerinde, altın bir kartalla taçlanmış kırmızı lejyon sancağı. Askerler onu görünce daha dik durur.",
     R_STANDARD, (1, 1), "roma_standard", beauty=8, work=2400, stuff=("Metallic", "Woody"), stuff_count=40,
     cost={"Cloth": 30}, hp=120, draw_size="(1.2,1.8)")
deco(NATION, "Aqueduct", "aqueduct span", "su kemeri",
     "A span of arched aqueduct in pale stone, carrying a channel of running water. Impressive, beautiful and very heavy.",
     "Açık renk taştan, akan su kanalı taşıyan kemerli bir su kemeri bölümü. Etkileyici, güzel ve çok ağır.",
     R_AQUEDUCT, (3, 1), "aqueduct", beauty=22, work=9000, stuff=("Stony",), stuff_count=240, hp=900,
     passability="Impassable", fill=0.9, minify=False, draw_size="(3.2,2.0)")
deco(NATION, "Brazier", "legion brazier", "lejyon mangalı",
     "A bronze brazier on iron legs. It lights the camp at night and warms the hands of the watch.",
     "Demir ayaklar üzerinde bronz bir mangal. Geceleri kampı aydınlatır ve nöbetçilerin ellerini ısıtır.",
     R_ENGINEERS, (1, 1), "brazier", beauty=3, work=1500, stuff=("Metallic",), stuff_count=40, hp=150,
     glow=(10, "(252,187,113,0)"), extra={"tickerType": "Normal"},
     comps=[{"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": 2.2, "fuelCapacity": 20, "fuelConsumptionPerTickInRain": 0.0006,
             "fuelFilter": {"thingDefs": ["WoodLog"]}, "initialFuelPercent": 1, "showAllowAutoRefuelToggle": True},
            {"@Class": "CompProperties_HeatPusher", "heatPerSecond": 8, "heatPushMaxTemperature": 28},
            {"@Class": "CompProperties_FireOverlay", "fireSize": 0.5, "offset": "(0,0,0.12)"}])

floor(NATION, "Concrete", "Roman concrete", "Roma betonu",
      "Pale concrete poured in square slabs. Durable and easy to clean.",
      "Kare levhalar halinde dökülmüş açık renk beton. Dayanıklı ve kolay temizlenir.",
      R_CONCRETE, "floor_concrete", beauty=1, cost={"Steel": 1}, work=600)
floor(NATION, "Road", "Roman road", "Roma yolu",
      "Fitted basalt slabs laid on a deep bed of gravel. Walking on it is fast and easy.",
      "Derin bir çakıl yatağı üzerine döşenmiş basalt levhalar. Üzerinde yürümek hızlı ve kolaydır.",
      R_ROADS, "floor_road", beauty=0, cost={"BlocksGranite": 2}, work=900)
