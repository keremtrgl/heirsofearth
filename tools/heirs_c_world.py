"""World-level content shared by every nation: the Renegades, the independent start and the heritage reminder."""
from heirs_data import add, key, tex
from heirs_people import POINTS_CURVE
from heirs_xml import Def, T

F = "Nations/HE_World.xml"

key("HE_HeritageReminderLabel", "Choose your heritage", "Mirasını seç")
key("HE_HeritageReminderText",
    "Your colony has not yet chosen which old nation it descends from.\n\nOpen the Heirs tab at the bottom of the screen and pick a heritage: its research needs no Culture Knowledge, its people start friendly and its traditions are yours from the start. You can also stay independent and learn a little of every culture.\n\nThe choice can be made only once.",
    "Kolonin henüz hangi eski ulusun soyundan geldiğini seçmedi.\n\nEkranın altındaki Mirasçılar sekmesini aç ve bir miras seç: o ulusun araştırmaları Kültür Bilgisi gerektirmez, halkı sana dostça başlar ve gelenekleri baştan senindir. İstersen bağımsız kalıp her kültürden biraz öğrenebilirsin.\n\nBu seçim yalnızca bir kez yapılabilir.")

# ------------------------------------------------------------------ Renegades: outlaws from every nation
tex("HeirsOfEarth/UI/HE_Renegades", "nation_icon", color="#3a3632", emblem="blades")
add(F, Def("PawnKindDef", None, abstract_name="HE_RenegadeBase", abstract=True,
           race="Human", defaultFactionDef="HE_Renegades", chemicalAddictionChance=0.12, backstoryCryptosleepCommonality=0,
           invNutrition=2.0, initialResistanceRange="14~22", initialWillRange="1~3", gearHealthRange="0.4~1.2"))
RENEGADE_KINDS = {
    "Cutthroat": (("cutthroat", "gırtlakkesen"), 45, ["MedievalMeleeBasic", "NeolithicMeleeBasic"], "80~200", ["IndustrialBasic", "Neolithic"], "150~350", None),
    "Brigand": (("brigand", "eşkıya"), 70, ["MedievalMeleeDecent", "NeolithicMeleeDecent"], "200~380", ["IndustrialBasic", "Neolithic"], "250~500", None),
    "Bowman": (("renegade bowman", "dönek okçu"), 60, ["NeolithicRangedDecent", "NeolithicRangedBasic"], "150~300", ["IndustrialBasic", "Neolithic"], "200~450", None),
    "Warlord": (("warlord", "savaş ağası"), 140, ["MedievalMeleeAdvanced"], "400~700", ["MedievalMilitary", "IndustrialBasic"], "900~1600", True),
}
for k, (label, power, weapons, wm, apparel, am, leader) in RENEGADE_KINDS.items():
    add(F, Def("PawnKindDef", f"HE_Renegade_{k}", parent="HE_RenegadeBase", label=T(*label), combatPower=power,
               weaponTags=weapons, weaponMoney=wm, apparelTags=apparel, apparelMoney=am, apparelAllowHeadgearChance=0.5,
               factionLeader=leader, minGenerationAge=30 if leader else None, itemQuality="Good" if leader else None))
combat = {"HE_Renegade_Cutthroat": 10, "HE_Renegade_Brigand": 8, "HE_Renegade_Bowman": 7, "HE_Renegade_Warlord": 1}
add(F, Def("FactionDef", "HE_Renegades", parent="FactionBase",
           label=T("renegade bands", "dönek çeteler"),
           description=T("Deserters, exiles and oath-breakers from every old nation, bound together by nothing but plunder. They honor no treaty and speak for no people. When an old nation has no army to send, it is often the renegades who answer for it.",
                         "Her eski ulustan kaçaklar, sürgünler ve yemin bozanlar; onları bir arada tutan tek şey yağma. Hiçbir antlaşmayı tanımaz, hiçbir halk adına konuşmazlar. Bir eski ulusun gönderecek ordusu olmadığında, onun yerine çoğu zaman dönekler gelir."),
           pawnSingular=T("renegade", "dönek"), pawnsPlural=T("renegades", "dönekler"), leaderTitle=T("warlord", "savaş ağası"),
           categoryTag="HE_Renegades", listOrderPriority=34, settlementGenerationWeight=0.6, requiredCountAtGameStart=1,
           maxConfigurableAtWorldCreation=2, configurationListOrderPriority=70, canSiege=True, canStageAttacks=True,
           humanlikeFaction=True, permanentEnemy=True, techLevel="Medieval", basicMemberKind="HE_Renegade_Cutthroat", fixedLeaderKinds=["HE_Renegade_Warlord"],
           factionNameMaker="NamerFactionPirate", settlementNameMaker="NamerSettlementPirate",
           factionIconPath="HeirsOfEarth/UI/HE_Renegades", settlementTexturePath="World/WorldObjects/DefaultSettlement",
           colorSpectrum=["(0.25, 0.23, 0.21)", "(0.40, 0.34, 0.28)"],
           backstoryFilters=[{"categories": ["Pirate", "Offworld"], "commonality": 1}],
           allowedArrivalTemperatureRange="-40~45", raidLootMaker="PirateRaidLootMaker", earliestRaidDays=20,
           maxPawnCostPerTotalPointsCurve=POINTS_CURVE,
           pawnGroupMakers=[{"kindDef": "Combat", "options": combat},
                            {"kindDef": "Settlement", "options": combat}]))

# ------------------------------------------------------------------ independent start
add(F, Def("ScenarioDef", "HE_Start_Independent", parent="ScenarioBase",
           label=T("Heirs of no one", "Kimsenin Mirasçısı"),
           description=T("Five settlers who owe nothing to any old nation. They start neutral with everyone and know a little of every culture (15 knowledge of each nation), but no research comes for free.",
                         "Hiçbir eski ulusa borcu olmayan üç yerleşimci. Herkesle tarafsız başlarlar ve her kültürden biraz bilirler (her ulustan 15 bilgi), ama hiçbir araştırma bedava gelmez."),
           scenario={"summary": T("Five independent settlers. No heritage, a little knowledge of every nation.",
                                  "Beş bağımsız yerleşimci. Miras yok, her ulustan biraz bilgi."),
                     "parts": [
                         {"@Class": "ScenPart_ConfigPage_ConfigureStartingPawns", "def": "ConfigPage_ConfigureStartingPawns", "pawnCount": 5, "pawnChoiceCount": 10},
                         {"@Class": "ScenPart_PlayerPawnsArriveMethod", "def": "PlayerPawnsArriveMethod", "method": "Standing", "visible": False},
                         {"@Class": "HeirsOfEarth.ScenPart_HeirsHeritage", "def": "HE_Heritage"},
                         {"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": "Silver", "count": 600},
                         {"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": "Pemmican", "count": 200},
                         {"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": "MedicineHerbal", "count": 35},
                         {"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": "MeleeWeapon_Spear", "stuff": "Steel"},
                         {"@Class": "ScenPart_StartingThing_Defined", "def": "StartingThing_Defined", "thingDef": "Bow_Recurve"},
                         {"@Class": "ScenPart_StartingAnimal", "def": "StartingAnimal", "count": 1, "bondToRandomPlayerPawnChance": 0.5},
                         {"@Class": "ScenPart_ScatterThingsNearPlayerStart", "def": "ScatterThingsNearPlayerStart", "thingDef": "WoodLog", "count": 300},
                         {"@Class": "ScenPart_ScatterThingsNearPlayerStart", "def": "ScatterThingsNearPlayerStart", "thingDef": "Steel", "count": 250},
                         {"@Class": "ScenPart_GameStartDialog", "def": "GameStartDialog", "textKey": "HE_StartIndependentDialog", "closeSound": "GameStartSting"},
                     ]}))
key("HE_StartIndependentDialog",
    "No banner flies over your camp and no senate, shogun or jarl expects your tribute. The old nations will judge you by what you do, not by whose blood you carry. Learn from all of them, and owe none of them anything.",
    "Kampının üzerinde hiçbir sancak dalgalanmıyor; hiçbir senato, şogun ya da jarl senden haraç beklemiyor. Eski uluslar seni kimin kanını taşıdığına göre değil, ne yaptığına göre yargılayacak. Hepsinden öğren, hiçbirine borçlanma.")
