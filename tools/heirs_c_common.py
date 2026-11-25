"""Shared 1.0 content: the common research line and the recreation jobs of the heritage buildings."""
from heirs_data import add
from heirs_kit import research
from heirs_xml import Def, T

F = "Core/HE_Joy.xml"

# ------------------------------------------------------------------ common research
R_TRANSLATORS = research("Common", "Translators", "translators", "tercümanlar",
                         "Train colonists to read the old languages of the heir nations, so every studied item teaches more.",
                         "Kolonistleri mirasçı devletlerin eski dillerini okuyacak şekilde eğit; böylece incelenen her eşya daha çok şey öğretir.",
                         600, "Neolithic", 0, 1, prereqs=["HE_CultureTable"], tradition=True, study=0.10,
                         effect=T("Studying culture items gives 10% more Culture Knowledge.",
                                  "Kültür eşyası incelemek %10 daha fazla Kültür Bilgisi verir."))
R_ENVOYS = research("Common", "Envoys", "envoys", "elçiler",
                    "Send envoys with gifts and letters to the old nations. Traders learn your name and treat you more fairly.",
                    "Eski devletlere hediyeler ve mektuplarla elçiler gönder. Tüccarlar adını öğrenir ve sana daha adil davranır.",
                    700, "Neolithic", 1, 1, prereqs=["HE_CultureTable"], tradition=True,
                    stats=[("TradePriceImprovement", 0.03, 1, "Colonists")],
                    effect=T("Colonists get 3% better trade prices.", "Kolonistler %3 daha iyi ticaret fiyatı alır."))
R_ACADEMY = research("Common", "Academy", "culture academy", "kültür akademisi",
                     "A school where the knowledge of every heir nation is copied, compared and taught.",
                     "Her mirasçı devletin bilgisinin kopyalandığı, karşılaştırıldığı ve öğretildiği bir okul.",
                     1200, "Medieval", 0, 0, prereqs=[R_TRANSLATORS], tradition=True, study=0.15,
                     stats=[("GlobalLearningFactor", 0.03, 1, "Colonists")],
                     effect=T("Studying culture items gives 15% more Culture Knowledge and colonists learn 3% faster.",
                              "Kültür eşyası incelemek %15 daha fazla Kültür Bilgisi verir ve kolonistler %3 daha hızlı öğrenir."))

# ------------------------------------------------------------------ recreation at heritage buildings
JOBS = {
    "HE_Relax": (("relaxing in the bath.", "banyoda dinleniyor."), "Meditative", None, 4),
    "HE_Tea": (("sharing tea.", "çay içiyor."), "Social", None, 4),
    "HE_Mead": (("drinking mead and boasting.", "bal şarabı içip övünüyor."), "Social", None, 4),
    "HE_Train": (("training at the post.", "direkte talim yapıyor."), "Gaming_Dexterity", "Melee", 1),
    "HE_WatchPlay": (("watching a play.", "bir oyun izliyor."), "Social", None, 6),
}
for name, (report, kind, skill, people) in JOBS.items():
    add(F, Def("JobDef", name, driverClass="JobDriver_SitFacingBuilding", reportString=T(*report),
               joyDuration=4000, joyMaxParticipants=people, joyKind=kind, joySkill=skill,
               joyXpPerTick=0.002 if skill else None, allowOpportunisticPrefix=True))

GIVERS = {
    "HE_Bathe": ("HE_Relax", ["HE_Roma_Thermae", "HE_Nord_Sauna"], "Meditative", 3, []),
    "HE_TeaCeremony": ("HE_Tea", ["HE_Yamato_TeaTable", "HE_Tianxia_TeaTable"], "Social", 3, ["Manipulation"]),
    "HE_Feast": ("HE_Mead", ["HE_Nord_MeadTable", "HE_Roma_Triclinium", "HE_Albion_PubTable"], "Social", 3, ["Manipulation"]),
    "HE_Theatre": ("HE_WatchPlay", ["HE_Hellas_Stage"], "Social", 3, ["Sight"]),
    "HE_Training": ("HE_Train", ["HE_Yamato_Dojo"], "Gaming_Dexterity", 2, ["Manipulation", "Moving"]),
}
for name, (job, things, kind, chance, caps) in GIVERS.items():
    add(F, Def("JoyGiverDef", name, giverClass="JoyGiver_InteractBuildingSitAdjacent", baseChance=chance,
               requireChair=False, thingDefs=things, jobDef=job, joyKind=kind, requiredCapacities=caps or None))
