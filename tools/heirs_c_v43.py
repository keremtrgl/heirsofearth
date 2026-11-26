"""Heirs of Earth 4.3 "Electric Age": a fourth age after the Age of Steam (HeirsAges.cs, threshold 18). Each nation gets one
late-game gun with a strength of its own, a steel helmet and a field uniform (art in heirs_art21), and one powered building
(heirs_c_v43 works section, HeirsWorks.cs). Items of the age carry HeirsAgeExt age 4 and guns the weapon tag HE_<Nation>Age4,
exactly like the ages of 4.2 (see heirs_c_v42)."""
import heirs_art21  # noqa: F401  (registers the painters)
from heirs_art19 import BODIES, ROTS
from heirs_art21 import HELMETS, UNIFORMS_E
from heirs_c_v32 import free_slot
from heirs_c_v33 import find
from heirs_c_v42 import ADJ_EN, ADJ_TR, AGE_EN, AGE_TR, CARTRIDGE, NATION_EN, NATION_TR, NATION_TR_GEN, RESEARCH as RESEARCH42, age_tag, mark
from heirs_data import add, key, tex
from heirs_kit import apparel, culture, deco, projectile, ranged, research, tool
from heirs_xml import Def, T

AGE_EN[4] = "Electric Age"
AGE_TR[4] = "Elektrik Çağı'na"
NATIONS = ["Roma", "Yamato", "Nord", "Hellas", "Tianxia", "Albion", "Kemet", "Pars", "Inti"]


def age4_research(nation, k, en, tr, den, dtr, cost, prereqs, knowledge):
    col, row = free_slot(nation, "Industrial", 3.0)
    name = research(nation, k, en, tr,
                    den + f"\n\nOutside your heritage, this can be researched only once {NATION_EN[nation]} has reached the Electric Age.",
                    dtr + f"\n\nMirasın bu değilse, ancak {NATION_TR[nation]} Elektrik Çağı'na ulaştığında araştırılabilir.",
                    cost, "Industrial", col, row, prereqs=prereqs, knowledge=knowledge)
    find("ResearchProjectDef", name).fields["modExtensions"][0]["age"] = 4
    return name


RESEARCH = {}
WORKS_RESEARCH = {}
for nation in NATIONS:
    steam = RESEARCH42[(nation, 3)]
    RESEARCH[nation] = age4_research(
        nation, "ElectricArmy", f"{ADJ_EN[nation]} electric army", f"{ADJ_TR[nation]} elektrik ordusu",
        f"Machine-made arms, a steel helmet and a field uniform in drab: the army {NATION_EN[nation]} raised when the wires came.",
        f"Makinede yapılmış silahlar, bir çelik miğfer ve soluk renkli bir sahra üniforması: teller geldiğinde {NATION_TR_GEN[nation]} kurduğu ordu.",
        3000, [steam, "Machining"], 60)
    WORKS_RESEARCH[nation] = age4_research(
        nation, "Works", f"{ADJ_EN[nation]} works", f"{ADJ_TR[nation]} işleri",
        f"The first electric works of {NATION_EN[nation]}: one machine the nation is proud of, built to its own taste.",
        f"{NATION_TR_GEN[nation]} ilk elektrikli işleri: devletin gurur duyduğu, kendi zevkine göre kurulmuş bir makine.",
        2600, [steam, "Electricity"], 50)

# ------------------------------------------------------------------ guns
# Stats stand level with the closest vanilla gun (game data, RimWorld 1.6) and each has one strength of its own.
TRENCH_SHOT = projectile("HE_Bullet_TrenchShot", "trench shot", "siper saçması", "Bullet", 20, 55, "Things/Projectile/Bullet_Small", pen=0.15)
GUN = dict(sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True)

E_GUNS = [
    # (nation, key, en, tr, desc en, desc tr, bullet, warmup, range, cooldown, acc, mass, work, cost, burst, ticks, sound, tools)
    ("Albion", "LightMG", "Albion light machine gun", "Albion hafif makineli tüfeği",
     "A pan-fed light machine gun with a cooling jacket round the barrel and a bipod folded under it. Heavy and slow to bring up, it "
     "puts six rounds where one would go. The works of Albion make it with more steel and fewer fine parts than most such guns.",
     "Namlusunu saran bir soğutma ceketi ve altında katlanmış bir iki ayağı olan, tava şarjörlü bir hafif makineli tüfek. Ağırdır ve "
     "nişana yavaş kalkar, ama bir merminin gideceği yere altı mermi yollar. Albion'un fabrikaları onu benzerlerinden daha çok çelik ve "
     "daha az ince parçayla yapar.",
     "Bullet_LMG", 1.8, 25.9, 1.6, (0.40, 0.48, 0.35, 0.26), 8.5, 34000, {"Steel": 90, "ComponentIndustrial": 4}, 6, 7, "Shot_Minigun",
     [tool("stock", "Blunt", 11, 2.2), tool("barrel", "Blunt", 10, 2.2)]),
    ("Yamato", "Sniper", "Yamato sniper rifle", "Yamato keskin nişancı tüfeği",
     "A long bolt rifle with a black-lacquered stock, a brass telescope and a cherry blossom on the scope ring. Slow to aim, but at the "
     "end of its reach it is the most accurate gun of the nations.",
     "Siyah cilalı dipçikli, pirinç bir dürbünü ve dürbün halkasında bir kiraz çiçeği olan uzun, sürgülü bir tüfek. Nişan alması yavaştır, "
     "ama menzilinin sonunda devletlerin en isabetli silahıdır.",
     "Bullet_SniperRifle", 3.5, 44.9, 1.5, (0.50, 0.70, 0.88, 0.94), 4.2, 42000, {"Steel": 60, "WoodLog": 10, "ComponentIndustrial": 7}, 1, None,
     "Shot_SniperRifle", [tool("stock", "Blunt", 10, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
    ("Nord", "TrenchGun", "Nordic trench gun", "Nord siper tüfeği",
     "A pump-action shotgun with a birch stock, a heat shield over the barrel and a raven on the receiver. Its heavy shot hits harder "
     "than other shotguns at the few paces it is meant for.",
     "Huş dipçikli, namlusunun üstünde bir ısı kalkanı ve gövdesinde bir kuzgun olan pompalı bir av tüfeği. Ağır saçması, yapıldığı "
     "birkaç adımlık mesafede diğer av tüfeklerinden daha sert vurur.",
     "HE_Bullet_TrenchShot", 0.9, 15.9, 1.25, (0.80, 0.87, 0.77, 0.64), 3.6, 12000, {"Steel": 60, "WoodLog": 10, "ComponentIndustrial": 3}, 1, None,
     "Shot_Shotgun", [tool("stock", "Blunt", 11, 2.0), tool("barrel", "Blunt", 10, 2.0)]),
    ("Roma", "Autoloader", "Roman self-loading rifle", "Roma yarı otomatik tüfeği",
     "A self-loading rifle with a red-lacquered stock and a bronze eagle on the receiver. The gas of each shot works the bolt, so the "
     "legionary fires again as soon as he has his aim.",
     "Kırmızı cilalı dipçikli, gövdesinde bronz bir kartal olan yarı otomatik bir tüfek. Her atışın gazı sürgüyü çalıştırır; böylece "
     "lejyoner nişanını bulur bulmaz yeniden ateş eder.",
     CARTRIDGE, 1.3, 33.9, 1.0, (0.60, 0.74, 0.80, 0.68), 4.2, 20000, {"Steel": 60, "WoodLog": 10, "ComponentIndustrial": 4}, 1, None,
     "Shot_BoltActionRifle", [tool("stock", "Blunt", 10, 2.0), tool("bayonet", "Stab", 16, 2.0, 0.28)]),
    ("Tianxia", "BoxPistol", "Tianxia box pistol", "Tianxia kutu tabancası",
     "A broom-handled pistol that rides in a wooden box, and the box clips on as a stock. It fires short bursts, comes up fast and is "
     "made by the thousand with little work. A red tassel hangs from the grip.",
     "Tahta bir kutuda taşınan, süpürge saplı bir tabanca; kutu takılınca dipçik olur. Kısa seriler atar, çabuk kalkar ve az emekle "
     "binlercesi yapılır. Kabzasından kırmızı bir püskül sarkar.",
     "Bullet_MachinePistol", 0.6, 21.9, 1.1, (0.85, 0.68, 0.40, 0.20), 1.6, 7000, {"Steel": 35, "WoodLog": 5, "ComponentIndustrial": 2}, 3, 8,
     "Shot_Autopistol", [tool("grip", "Blunt", 8, 1.8), tool("barrel", "Blunt", 8, 1.8)]),
    ("Hellas", "MountainCarbine", "Hellenic mountain carbine", "Helen dağ karabinası",
     "A short, light carbine with silver bands, made for the mountain troops who carry everything up the slopes themselves. Best at the "
     "middle distances of the hills.",
     "Her şeyi yamaçlara kendi sırtında taşıyan dağ birlikleri için yapılmış, gümüş bilezikli, kısa ve hafif bir karabina. Tepelerin "
     "orta mesafelerinde en iyisidir.",
     CARTRIDGE, 1.4, 31.9, 1.4, (0.62, 0.80, 0.86, 0.60), 2.8, 13000, {"Steel": 50, "WoodLog": 10, "ComponentIndustrial": 2}, 1, None,
     "Shot_BoltActionRifle", [tool("stock", "Blunt", 10, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
    ("Kemet", "NileCarbine", "Nile carbine", "Nil karabinası",
     "A carbine with a long barrel for its kind, a brass-bound stock and a lotus on the butt plate. It reaches further than other carbines, "
     "and it is cut to stay clean in the sand.",
     "Türüne göre uzun namlulu, pirinçle sarılı dipçikli ve dipçik plakasında bir nilüfer olan bir karabina. Diğer karabinalardan daha "
     "uzağa erişir ve kumda temiz kalacak şekilde yapılmıştır.",
     CARTRIDGE, 1.3, 33.9, 1.4, (0.62, 0.78, 0.82, 0.66), 3.2, 13000, {"Steel": 50, "WoodLog": 10, "ComponentIndustrial": 2}, 1, None,
     "Shot_BoltActionRifle", [tool("stock", "Blunt", 10, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
    ("Pars", "LongRifle", "Persian long rifle", "Pers uzun tüfeği",
     "A very long rifle with a khatam-inlaid stock and a fine brass sight. It is slow to aim, and it reaches further than any other gun "
     "of the nations.",
     "Hatem kakmalı dipçikli ve ince pirinç bir nişangâhı olan çok uzun bir tüfek. Nişan alması yavaştır ve devletlerin her silahından "
     "daha uzağa erişir.",
     CARTRIDGE, 2.0, 45.9, 1.6, (0.55, 0.72, 0.88, 0.88), 4.6, 22000, {"Steel": 60, "WoodLog": 15, "ComponentIndustrial": 4}, 1, None,
     "Shot_BoltActionRifle", [tool("stock", "Blunt", 10, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
    ("Inti", "LightCarbine", "Inti light carbine", "Inti hafif karabinası",
     "A short carbine with a gold sun on the stock, the lightest and cheapest gun of the age. It comes up fast and is easy to carry over "
     "the passes.",
     "Dipçiğinde altın bir güneş olan kısa bir karabina; çağın en hafif ve en ucuz silahı. Çabuk kalkar ve geçitlerde kolay taşınır.",
     CARTRIDGE, 1.1, 29.9, 1.3, (0.66, 0.78, 0.74, 0.55), 2.6, 9000, {"Steel": 40, "WoodLog": 10, "ComponentIndustrial": 1}, 1, None,
     "Shot_BoltActionRifle", [tool("stock", "Blunt", 9, 1.9), tool("barrel", "Blunt", 8, 1.9)]),
]

GUNS = {}
for (nation, k, en, tr, den, dtr, bullet, warmup, rng, cool, acc, mass, work, cost, burst, ticks, sound, tools) in E_GUNS:
    name = ranged(nation, k, en, tr, den, dtr, "Industrial", RESEARCH[nation], bullet, warmup, rng, cool, acc, mass, work,
                  "heirs_e_gun", cost, sound=sound, interact="Interact_Rifle", gun=True, burst=burst, ticks=ticks,
                  klass=("Ranged", "RangedHeavy", "LongShots") if mass >= 4 else ("Ranged", "ShortShots") if rng < 25 else ("Ranged", "LongShots"),
                  tools=tools, weapon_tags=[age_tag(nation, 4)], pargs={"kind": f"HE_{nation}_{k}"}, skill=6)
    mark(name, nation, 4)
    GUNS[nation] = name

# ------------------------------------------------------------------ steel helmets and field uniforms
APPAREL = {}
for nation in NATIONS:
    hk, hen, htr, hden, hdtr, hcol = HELMETS[nation]
    helmet = apparel(nation, hk, hen, htr, hden, hdtr, "Industrial", RESEARCH[nation], None, ["Overhead"], ["UpperHead"],
                     {"MaxHitPoints": 120, "ArmorRating_Sharp": 0.4, "ArmorRating_Blunt": 0.18, "ArmorRating_Heat": 0.2,
                      "Insulation_Cold": 2},
                     "heirs_e_helmet_icon", stuff=None, cost={"Steel": 50}, work=6000, mass=1.4, head=True, color=hcol,
                     pargs={"kind": f"HE_{nation}_{hk}"})
    d = find("ThingDef", helmet)
    d.fields["graphicData"]["shaderType"] = "CutoutComplex"
    tex(f"HeirsOfEarth/Apparel/{helmet}_m", "heirs_e_helmet_icon", kind=helmet, mask=True)
    app = d.fields["apparel"]
    app["wornGraphicPath"] = f"HeirsOfEarth/Apparel/Worn/{helmet}"
    app["useWornGraphicMask"] = True
    for rot in ("south", "east", "north"):
        tex(f"HeirsOfEarth/Apparel/Worn/{helmet}_{rot}", "heirs_worn", kind=helmet, rot=rot)
        tex(f"HeirsOfEarth/Apparel/Worn/{helmet}_{rot}m", "heirs_worn", kind=helmet, rot=rot, mask=True)
    mark(helmet, nation, 4, extra_tag=False)

    uk, uen, utr, uden, udtr, ucol = UNIFORMS_E[nation]
    uniform = apparel(nation, uk, uen, utr, uden, udtr, "Industrial", RESEARCH[nation], None, ["Shell"], ["Torso", "Neck", "Shoulders", "Arms"],
                      {"MaxHitPoints": 200, "ArmorRating_Sharp": 0.22, "ArmorRating_Blunt": 0.14, "ArmorRating_Heat": 0.15,
                       "Insulation_Cold": 22, "Insulation_Heat": 6},
                      "heirs_coat_icon", stuff=None, cost={"Cloth": 60, "Steel": 10}, work=10000, mass=1.8, color=ucol,
                      pargs={"kind": f"HE_{nation}_{uk}"})
    d = find("ThingDef", uniform)
    d.fields["graphicData"]["shaderType"] = "CutoutComplex"
    tex(f"HeirsOfEarth/Apparel/{uniform}_m", "heirs_coat_icon", kind=uniform, mask=True)
    app = d.fields["apparel"]
    path = f"HeirsOfEarth/Apparel/Worn/Body/{uniform}"
    app["wornGraphicPath"] = path
    app["useWornGraphicMask"] = True
    for body in BODIES:
        for rot in ROTS:
            tex(f"{path}_{body}_{rot}", "heirs_body", kind=uniform, body=body, rot=rot)
            tex(f"{path}_{body}_{rot}m", "heirs_body", kind=uniform, body=body, rot=rot, mask=True)
    mark(uniform, nation, 4, extra_tag=False)
    APPAREL[nation] = (helmet, uniform)

# ------------------------------------------------------------------ text
key("HE_Age4", "Electric Age", "Elektrik Çağı")
key("HE_AgeText4", "{0} has entered the Electric Age.\n\n{1} has strung wires across its lands and lit its cities. Its new army "
    "carries machine-made guns and wears the steel helmet and the field uniform, its traders sell them, and your colony may research "
    "them and the nation's electric works.\n\nNew: {2}.",
    "{0} Elektrik Çağı'na girdi.\n\n{1} topraklarına teller çekti ve şehirlerini aydınlattı. Yeni ordusu makinede yapılmış silahlar "
    "taşıyor, çelik miğferi ve sahra üniformasını giyiyor, tüccarları bunları satıyor ve kolonin bunları ve devletin elektrikli işlerini "
    "araştırabilir.\n\nYeni: {2}.")


# ------------------------------------------------------------------ works: one powered building per nation
def power(watts, rain=False):
    return [{"@Class": "CompProperties_Power", "compClass": "CompPowerTrader", "basePowerConsumption": watts, "shortCircuitInRain": rain},
            {"@Class": "CompProperties_Flickable"}]


FACILITY = ["PlaceWorker_ShowFacilitiesConnections"]
WORKS = {}


def work_deco(nation, k, en, tr, den, dtr, size, painter, watts, beauty, cost, work=4000, hp=200, comps=None, joy=None, glow=None,
              place=None, passability="PassThroughOnly", fill=0.4):
    ext = {"building": {"joyKind": joy} if joy else {}, "tickerType": "Normal"}
    if place:
        ext["placeWorkers"] = place
    name = deco(nation, k, en, tr, den, dtr, WORKS_RESEARCH[nation], size, painter, beauty, work, stuff=None, cost=cost, hp=hp,
                comps=power(watts) + list(comps or []), glow=glow, extra=ext, designation="HE_Heritage",
                category="Furniture", passability=passability, fill=fill)
    mark(name, nation, 4, extra_tag=False)
    WORKS[nation] = name
    return name


def work_table(nation, k, en, tr, den, dtr, size, painter, watts, cost, speed, copy_from, work=3500, hp=200, effect=None):
    name = f"HE_{nation}_{k}"
    add(f"Things/HE_Buildings_{nation}.xml", Def(
        "ThingDef", name, parent="BenchBase",
        label=T(en, tr), description=T(den, dtr),
        thingClass="Building_WorkTable",
        graphicData={"texPath": f"HeirsOfEarth/Buildings/{name}", "graphicClass": "Graphic_Single", "drawSize": f"({size[0]},{size[1]})",
                     "damageData": {"cornerTL": "Damage/Corner", "cornerTR": "Damage/Corner", "cornerBL": "Damage/Corner", "cornerBR": "Damage/Corner"}},
        castEdgeShadows=True, staticSunShadowHeight=0.20,
        costList=cost,
        altitudeLayer="Building", fillPercent=0.5, useHitPoints=True,
        statBases={"WorkToBuild": work, "MaxHitPoints": hp, "Flammability": 0.5, "Cleanliness": -2, "Mass": 50,
                   "WorkTableWorkSpeedFactor": speed},
        size=f"({size[0]},{size[1]})", designationCategory="Production", passability="PassThroughOnly", pathCost=50,
        hasInteractionCell=True, interactionCellOffset="(0,0,-1)", surfaceType="Item", constructionSkillPrerequisite=5,
        researchPrerequisites=[WORKS_RESEARCH[nation]],
        inspectorTabs=["ITab_Bills"],
        building={"spawnedConceptLearnOpportunity": "BillsTab"},
        placeWorkers=["PlaceWorker_ShowFacilitiesConnections", "PlaceWorker_PreventInteractionSpotOverlap"],
        comps=power(watts, rain=True) + [{"@Class": "CompProperties_AffectedByFacilities", "linkableFacilities": ["ToolCabinet"]}]
              + ([effect] if effect else []),
        modExtensions=[culture(nation), {"@Class": "HeirsOfEarth.HeirsCopyRecipesExt", "from": copy_from}]))
    tex(f"HeirsOfEarth/Buildings/{name}", painter, size=size)
    mark(name, nation, 4, extra_tag=False)
    WORKS[nation] = name
    return name


# Roma: a fountain that sits in the forum and lights up at night; colonists sit by it to rest.
work_deco("Roma", "ElectricFountain", "electric fountain", "elektrikli çeşme",
          "A round marble basin with a bronze she-wolf in the middle and an electric pump that throws a crown of water into the air. "
          "Lamps under the water light it blue at night. Colonists sit at its rim to rest.",
          "Ortasında tunçtan bir dişi kurt olan yuvarlak mermer bir havuz ve suyu havaya taç gibi fışkırtan elektrikli bir pompa. "
          "Suyun altındaki lambalar onu geceleri maviye boyar. Kolonistler dinlenmek için kenarına oturur.",
          (2, 2), "e_fountain", 150, 28, {"Steel": 60, "ComponentIndustrial": 2, "BlocksMarble": 80}, work=6000, hp=300,
          joy="Meditative", glow=(6, "(120,190,255,0)"), passability="Impassable", fill=0.5)
# Yamato: a tea urn that keeps water hot all day; colonists share tea at it.
work_deco("Yamato", "TeaUrn", "electric tea urn", "elektrikli çay kazanı",
          "A tall urn of black-lacquered copper on a stand, heated by a coil and kept just below the boil all day, with a tray of cups "
          "beside it. Colonists gather at it to share tea.",
          "Bir ayak üstünde, siyah cilalı bakırdan uzun bir kazan. Bir rezistansla ısıtılır ve gün boyu kaynamanın hemen altında tutulur; "
          "yanında bir fincan tepsisi durur. Kolonistler çay paylaşmak için başında toplanır.",
          (1, 1), "e_tea_urn", 150, 8, {"Steel": 40, "ComponentIndustrial": 1}, work=2400, hp=120, joy="Social")
# Hellas: a lit lectern that links to research benches.
work_deco("Hellas", "Lectern", "lamp-lit lectern", "lambalı kürsü",
          "A tall lectern of olive wood with an electric reading lamp, where one reads aloud and the others take notes. "
          "Placed near a research bench and powered, it speeds up research by 6%.",
          "Bir kişinin yüksek sesle okuyup ötekilerin not tuttuğu, elektrikli bir okuma lambası olan zeytin ağacından uzun bir kürsü. "
          "Bir araştırma masasının yakınına konulup elektrik verilince araştırmayı %6 hızlandırır.",
          (1, 1), "e_lectern", 200, 6, {"Steel": 30, "WoodLog": 40, "ComponentIndustrial": 2}, work=3000, hp=120,
          comps=[{"@Class": "CompProperties_Facility", "statOffsets": {"ResearchSpeedFactor": 0.06}, "maxSimultaneous": 1, "maxDistance": 8}],
          place=FACILITY)
# Tianxia: a printing press that prints patterns on silk; it links to tailoring benches.
work_deco("Tianxia", "PrintingPress", "silk printing press", "ipek baskı makinesi",
          "An electric press with carved rollers that print patterns on silk and cotton in one pass. Placed near a tailoring bench "
          "and powered, it speeds up tailoring by 12%.",
          "İpeğe ve pamuğa desenleri tek geçişte basan oymalı silindirleri olan elektrikli bir baskı makinesi. Bir terzi tezgâhının "
          "yakınına konulup elektrik verilince terziliği %12 hızlandırır.",
          (2, 1), "e_press", 250, 2, {"Steel": 90, "ComponentIndustrial": 3}, work=4000, hp=200,
          comps=[{"@Class": "CompProperties_Facility", "statOffsets": {"WorkTableWorkSpeedFactor": 0.12}, "maxSimultaneous": 1, "maxDistance": 6}],
          place=FACILITY)
# Albion: a telegraph office that keeps in touch with the other nations.
work_deco("Albion", "TelegraphOffice", "telegraph office", "telgraf ofisi",
          "A desk with a brass telegraph key, a sounder and a battery of cells, wired to a mast outside. While it has power it sends "
          "greetings to the other nations every quadrum: +1 goodwill with each heir nation that is not hostile. Only one office counts.",
          "Pirinç bir telgraf anahtarı, bir alıcı ve bir pil dizisi olan, dışarıdaki bir direğe bağlı bir masa. Elektriği olduğu sürece "
          "her mevsim öteki devletlere selam gönderir: düşman olmayan her mirasçı devletle +1 iyi niyet. Yalnızca bir ofis sayılır.",
          (2, 1), "e_telegraph", 200, 2, {"Steel": 70, "ComponentIndustrial": 4}, work=3600, hp=160,
          comps=[{"@Class": "HeirsOfEarth.CompProperties_HeirsTelegraph", "goodwill": 1, "intervalDays": 15}])
# Kemet: an irrigation pump that waters the fields round it.
work_deco("Kemet", "IrrigationPump", "irrigation pump", "sulama pompası",
          "An electric pump that lifts water from below and sends it through clay channels to the fields around it. While it has "
          "power, plants within 6 cells grow 15% faster.",
          "Suyu aşağıdan çekip kil kanallardan çevresindeki tarlalara gönderen elektrikli bir pompa. Elektriği olduğu sürece 6 kare "
          "içindeki bitkiler %15 daha hızlı büyür.",
          (1, 1), "e_pump", 300, 0, {"Steel": 60, "ComponentIndustrial": 2}, work=3000, hp=180,
          comps=[{"@Class": "HeirsOfEarth.CompProperties_HeirsIrrigation", "radius": 6, "growthFactor": 1.15}],
          passability="Impassable", fill=0.6)
# Nord: an electric forge, a faster smithy.
work_table("Nord", "ElectricForge", "electric forge", "elektrikli demirhane",
           "A forge with an electric blower, a power hammer and an anvil worn smooth by generations. It makes everything a smithy "
           "makes, 25% faster.",
           "Elektrikli bir körüğü, bir şahmerdanı ve nesillerdir dövülmekten pürüzsüzleşmiş bir örsü olan bir demirhane. Bir demircinin "
           "yaptığı her şeyi %25 daha hızlı yapar.",
           (3, 1), "e_forge", 250, {"Steel": 140, "ComponentIndustrial": 4}, 1.25, ["ElectricSmithy", "FueledSmithy"],
           effect={"@Class": "CompProperties_HeatPusher", "compClass": "CompHeatPusherPowered", "heatPerSecond": 4})
# Pars: an electric carpet loom.
work_table("Pars", "ElectricLoom", "electric carpet loom", "elektrikli halı tezgâhı",
           "A carpet loom whose shuttle and beater are driven by a small motor while the weaver ties the knots. It takes every bill "
           "of the carpet loom and works 40% faster.",
           "Dokumacı düğümleri atarken mekiği ve tarağı küçük bir motorla çalışan bir halı tezgâhı. Halı tezgâhının her işini alır ve "
           "%40 daha hızlı çalışır.",
           (2, 1), "e_loom", 250, {"Steel": 80, "WoodLog": 40, "ComponentIndustrial": 3}, 1.4, ["HE_Pars_CarpetLoom"])

# Inti: a cold store, the powered heir of the qullqa.
COLD = "HE_Inti_ColdStore"
add("Things/HE_Buildings_Inti.xml", Def(
    "ThingDef", COLD, parent="ShelfBase",
    label=T("cold store", "soğuk depo"),
    description=T("A stone storehouse with thick walls, a cork-lined door and an electric cooler humming in the roof. While it has power, "
                  "food stored in it rots at a third of the normal speed. It holds three stacks per cell.",
                  "Kalın duvarlı, mantar kaplı kapılı ve çatısında vızıldayan elektrikli bir soğutucusu olan bir taş ambar. Elektriği olduğu "
                  "sürece içinde saklanan yiyecek normal hızın üçte birinde bozulur. Her karede üç yığın tutar."),
    thingClass="Building_Storage",
    graphicData={"texPath": f"HeirsOfEarth/Buildings/{COLD}", "graphicClass": "Graphic_Single", "drawSize": "(2,2)"},
    size="(2,2)", rotatable=False, fillPercent=0.5, tickerType="Normal",
    stuffCategories={"@Inherit": "False", "#items": ["Stony"]}, costStuffCount=80, costList={"Steel": 60, "ComponentIndustrial": 3},
    statBases={"MaxHitPoints": 320, "WorkToBuild": 5000, "Mass": 70, "Beauty": 0, "Flammability": 0.2},
    designationCategory="HE_Heritage",
    researchPrerequisites={"@Inherit": "False", "#items": [WORKS_RESEARCH["Inti"]]},
    building={"maxItemsInCell": 3, "preventDeteriorationOnTop": True, "ignoreStoredThingsBeauty": True,
              "blueprintClass": "Blueprint_Storage",
              "fixedStorageSettings": {"filter": {"disallowNotEverStorable": True, "categories": ["Foods", "PlantMatter"]}},
              "defaultStorageSettings": {"priority": "Important", "filter": {"categories": ["Foods"]}}},
    comps=power(400),
    modExtensions=[culture("Inti"), {"@Class": "HeirsOfEarth.HeirsFoodStoreExt", "rotFactor": 0.35, "needsPower": True}]))
tex(f"HeirsOfEarth/Buildings/{COLD}", "e_cold_store", size=(2, 2))
mark(COLD, "Inti", 4, extra_tag=False)
WORKS["Inti"] = COLD

# Recreation: colonists rest at the fountain and share tea at the urn.
add("Core/HE_Joy.xml", Def("JobDef", "HE_Fountain", driverClass="JobDriver_SitFacingBuilding",
                                    reportString=T("resting by the fountain.", "çeşmenin başında dinleniyor."),
                                    joyDuration=4000, joyMaxParticipants=6, joyKind="Meditative", allowOpportunisticPrefix=True))
add("Core/HE_Joy.xml", Def("JoyGiverDef", "HE_FountainRest", giverClass="JoyGiver_InteractBuildingSitAdjacent", baseChance=3,
                                    requireChair=False, thingDefs=[WORKS["Roma"]], jobDef="HE_Fountain", joyKind="Meditative"))
tea = find("JoyGiverDef", "HE_TeaCeremony")
tea.fields["thingDefs"] = list(tea.fields["thingDefs"]) + [WORKS["Yamato"]]

key("HE_TelegraphNext", "Next telegrams in {0}.", "Sonraki telgraflar {0} içinde.")
key("HE_TelegraphSent", "The telegraph office sent greetings: +{0} goodwill with {1}.",
    "Telgraf ofisi selam gönderdi: {1} ile +{0} iyi niyet.")

# ------------------------------------------------------------------ World Fair (HeirsWorldFair.cs)
for k, en, tr in [
    ("HE_WorldFairLabel", "World Fair of {0}", "{0} Dünya Fuarı"),
    ("HE_WorldFairText",
     "{1} celebrates the Electric Age with a World Fair: halls of glass and iron lit by thousands of bulbs, where every nation shows "
     "the best it can make.\n\nYour colony is invited to send one exhibit. {2}\n\nThe exhibit travels to the fair and comes back by drop "
     "pod in about {3} days, with a prize that grows with its quality. A masterwork or legendary piece can win the grand prize. "
     "Declining offends the hosts a little.",
     "{1}, Elektrik Çağı'nı bir Dünya Fuarı ile kutluyor: binlerce ampulle aydınlatılmış camdan ve demirden salonlar, her devletin "
     "yapabildiğinin en iyisini sergilediği yerler.\n\nKolonin bir eser göndermeye davet edildi. {2}\n\nEser fuara gider ve yaklaşık "
     "{3} gün sonra, niteliğiyle büyüyen bir ödülle birlikte bir iniş kapsülüyle geri döner. Ustalık ya da efsanevi bir eser büyük "
     "ödülü kazanabilir. Daveti geri çevirmek ev sahiplerini biraz kırar."),
    ("HE_WorldFairExhibit", "Your best piece is {0} ({1}).", "En iyi eserin: {0} ({1})."),
    ("HE_WorldFairNothing", "The colony has no art, weapon or book of quality to send yet.",
     "Kolonide henüz gönderilecek nitelikli bir sanat eseri, silah ya da kitap yok."),
    ("HE_WorldFairAccept", "Send {1}", "{1} gönderilsin"),
    ("HE_WorldFairRefuse", "Decline", "Geri çevir"),
    ("HE_WorldFairMissing", "Nothing to exhibit.", "Sergilenecek bir şey yok."),
    ("HE_WorldFairSent", "{0} is on its way to the World Fair of {1}.", "{0}, {1} Dünya Fuarı'na yola çıktı."),
    ("HE_WorldFairBackLabel", "Back from the World Fair of {0}", "{0} Dünya Fuarı'ndan dönüş"),
    ("HE_WorldFairBack",
     "{0} is back from the World Fair of {1}. Judged {2}, it brings home {6} silver, +{3} goodwill with the hosts, +{4} with every "
     "other peaceful nation and {5} knowledge of {1}.",
     "{0}, {1} Dünya Fuarı'ndan döndü. {2} bulunan eser eve {6} gümüş, ev sahipleriyle +{3}, öteki her barışçı devletle +{4} iyi "
     "niyet ve {5} {1} bilgisi getiriyor."),
    ("HE_WorldFairGrandPrize", "{0} won the grand prize of the World Fair of {1}: +{2} goodwill more with every peaceful nation.",
     "{0}, {1} Dünya Fuarı'nın büyük ödülünü kazandı: her barışçı devletle +{2} iyi niyet daha."),
]:
    key(k, en, tr)
