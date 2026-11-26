"""Heirs of Earth 4.2 "Ages of Progress": every nation moves through three ages (Founding, Powder, Steam) as the years pass
(HeirsAges.cs). Each age brings the nation's own firearms and, in the Age of Steam, its uniform coat: its troops start carrying
them, its traders start selling them, and other colonies may research them only once the nation has reached that age.
Items of an age carry HeirsAgeExt (nation, age) and the weapon tag HE_<Nation>Age<n>, which is how troops are armed with them."""
from heirs_art19 import BODIES, ROTS
from heirs_art20 import COATS
from heirs_c_v32 import free_slot
from heirs_c_v33 import find
from heirs_data import key, tex
from heirs_kit import N, apparel, projectile, ranged, research, tool
from heirs_xml import T

ABILITY_SOUND = dict(sound="Shot_BoltActionRifle", interact="Interact_Rifle", gun=True)


def age_ext(nation, age):
    return {"@Class": "HeirsOfEarth.HeirsAgeExt", "nation": N(nation), "age": age}


def age_tag(nation, age):
    return f"HE_{nation}Age{age}"


def mark(defname, nation, age, extra_tag=True, ext=True):
    """Puts an item into a nation's age: the HeirsAgeExt (which holds it back from traders and research until the age) and, for
    guns, the weapon tag troops are armed by. Guns the nation already had keep selling as before and only get the tag."""
    d = find("ThingDef", defname)
    if ext:
        exts = d.fields.get("modExtensions") or []
        d.fields["modExtensions"] = [e for e in exts if e.get("@Class") != "HeirsOfEarth.HeirsAgeExt"] + [age_ext(nation, age)]
    if extra_tag and d.fields.get("weaponTags"):
        items = d.fields["weaponTags"]["#items"]
        if age_tag(nation, age) not in items:
            d.fields["weaponTags"]["#items"] = list(items) + [age_tag(nation, age)]


def age_research(nation, k, en, tr, den, dtr, age, cost, prereqs, knowledge):
    col, row = free_slot(nation, "Industrial", 2.0 if age == 2 else 3.0)
    name = research(nation, k, en, tr,
                    den + f"\n\nOutside your heritage, this can be researched only once {NATION_EN[nation]} has reached the {AGE_EN[age]}.",
                    dtr + f"\n\nMirasın bu değilse, ancak {NATION_TR[nation]} {AGE_TR[age]} ulaştığında araştırılabilir.",
                    cost, "Industrial", col, row, prereqs=prereqs, knowledge=knowledge)
    find("ResearchProjectDef", name).fields["modExtensions"][0]["age"] = age
    return name


NATION_EN = {"Roma": "Nova Roma", "Yamato": "Yamato", "Nord": "Nordheim", "Hellas": "Hellas", "Tianxia": "Tianxia", "Albion": "Albion",
             "Kemet": "New Kemet", "Pars": "Pars", "Inti": "Inti"}
NATION_TR = {"Roma": "Nova Roma", "Yamato": "Yamato", "Nord": "Nordheim", "Hellas": "Hellas", "Tianxia": "Tianxia", "Albion": "Albion",
             "Kemet": "Yeni Kemet", "Pars": "Pars", "Inti": "Inti"}
AGE_EN = {2: "Age of Powder", 3: "Age of Steam"}
AGE_TR = {2: "Barut Çağı'na", 3: "Buhar Çağı'na"}

BALL = "HE_Bullet_Musket"          # Albion's musket ball (heirs_c_albion)
CARTRIDGE = projectile("HE_Bullet_Cartridge", "rifle cartridge", "tüfek fişeği", "Bullet", 18, 90, "Things/Projectile/Bullet_Small", pen=0.38)

# The guns: (nation, key, en, tr, desc en, desc tr, age, painter, research en/tr + desc en/tr, stats)
# 4.2.1 balance. Powder arms need no components: a cheap early gun, weaker than a bolt-action rifle but far better than a bow.
# Steam rifles stand level with the vanilla bolt-action rifle (warmup 1.7, range 36.9, cooldown 1.5, accuracy .65/.80/.90/.80,
# 12000 work, 60 steel and 3 components) for 2 components and some wood, and each nation's rifle has one strength of its own.
POWDER = dict(warmup=1.8, rng=25.9, cool=2.7, acc=(0.45, 0.6, 0.46, 0.28), mass=4.6, work=9000, cost={"Steel": 45, "WoodLog": 25})
STEAM = dict(warmup=1.7, rng=36.9, cool=1.5, acc=(0.62, 0.78, 0.86, 0.76), mass=4.0, work=14000,
             cost={"Steel": 55, "WoodLog": 15, "ComponentIndustrial": 2})
HEAVY_BALL = projectile("HE_Bullet_HeavyBall", "heavy ball", "ağır bilye", "Bullet", 28, 60, "Things/Projectile/Bullet_Small", pen=0.45)

GUNS = [
    ("Roma", "Arquebus", "Roman arquebus", "Roma arkebüzü",
     "A matchlock arquebus with a red-lacquered stock and a brass eagle on the lock. The legions learned powder late and drilled it hard: it is the steadiest of the powder arms up close.",
     "Kırmızı cilalı dipçikli, kilidinde pirinç bir kartal olan fitilli bir arkebüz. Lejyonlar barutu geç öğrendi ve sıkı talim etti: yakında barutlu silahların en isabetlisidir.",
     2, "roma_arquebus", dict(POWDER, acc=(0.5, 0.68, 0.5, 0.3)), [tool("stock", "Blunt", 10, 2.1), tool("barrel", "Blunt", 9, 2.0)]),
    ("Nord", "HookGun", "hook gun", "kancalı tüfek",
     "A heavy matchlock with an iron hook under the barrel to brace it on a wall or a rail. It kicks like a horse and hits like one.",
     "Namlunun altında, bir duvara ya da korkuluğa dayamak için demir kancası olan ağır bir fitilli tüfek. At gibi teper, at gibi vurur.",
     2, "nord_hookgun", dict(POWDER, warmup=2.2, rng=27.9, cool=3.2, acc=(0.4, 0.58, 0.5, 0.32), mass=6.0, bullet="HE_Bullet_HeavyBall"),
     [tool("stock", "Blunt", 12, 2.2), tool("barrel", "Blunt", 10, 2.1)]),
    ("Hellas", "Musket", "Hellenic musket", "Helen tüfeği",
     "A flintlock musket with silver bands and a meander inlaid along the stock, carried by the volunteers who first marched under the blue and white. A socket bayonet makes it a spear when the powder runs out.",
     "Gümüş bilezikli, dipçiği boyunca menderes kakmalı, mavi beyazın altında ilk yürüyen gönüllülerin taşıdığı çakmaklı bir tüfek. Soket süngüsü, barut bitince onu bir mızrağa çevirir.",
     2, "hellas_musket", dict(POWDER), [tool("stock", "Blunt", 10, 2.1), tool("bayonet", "Stab", 15, 2.0, 0.22)]),
    ("Tianxia", "BirdGun", "bird gun", "kuş tüfeği",
     "The long, slender matchlock called the bird gun: accurate enough to hit a bird in flight, light enough to carry all day.",
     "Kuş tüfeği denen uzun, ince fitilli tüfek: uçan bir kuşu vuracak kadar isabetli, bütün gün taşınacak kadar hafif.",
     2, "tianxia_birdgun", dict(POWDER, rng=30.9, acc=(0.42, 0.62, 0.55, 0.42), mass=3.8, cool=2.9),
     [tool("stock", "Blunt", 9, 2.0), tool("barrel", "Blunt", 8, 2.0)]),
    ("Kemet", "Musket", "Kemetic musket", "Kemet tüfeği",
     "A long musket bound in brass, its stock inlaid with turquoise and a lotus on the butt. Made in the arsenals of the river, with a long barrel that reaches further than most muskets.",
     "Pirinçle sarılı, dipçiği turkuaz kakmalı ve dibinde bir nilüfer olan uzun bir tüfek. Nehrin cephaneliklerinde, çoğu tüfekten daha uzağa erişen uzun bir namluyla yapılır.",
     2, "kemet_musket", dict(POWDER, rng=28.9, acc=(0.45, 0.6, 0.52, 0.32)), [tool("stock", "Blunt", 10, 2.1), tool("barrel", "Blunt", 9, 2.0)]),
    ("Inti", "Arquebus", "Inti arquebus", "Inti arkebüzü",
     "An arquebus bound in gold, its stock inlaid with tocapu squares that name the workshop that made it and the sun it serves. Short and light, it comes up to aim faster than any other powder arm.",
     "Altınla sarılı, dipçiğindeki tokapu kareleri onu yapan atölyeyi ve hizmet ettiği güneşi söyleyen bir arkebüz. Kısa ve hafiftir; nişana her barutlu silahtan daha çabuk kalkar.",
     2, "inti_arquebus", dict(POWDER, warmup=1.5, rng=24.9, mass=3.2, cost={"Steel": 40, "WoodLog": 25}), [tool("stock", "Blunt", 10, 2.1), tool("barrel", "Blunt", 9, 2.0)]),
    ("Yamato", "Rifle", "Yamato rifle", "Yamato tüfeği",
     "A bolt-action rifle with a black-lacquered stock, a brass cherry blossom on the wrist and a sword bayonet. Very accurate at long range.",
     "Siyah cilalı dipçikli, bileğinde pirinç bir kiraz çiçeği ve kılıç süngüsü olan sürgülü bir tüfek. Uzak mesafede çok isabetlidir.",
     3, "yamato_rifle", dict(STEAM, acc=(0.62, 0.78, 0.88, 0.82)), [tool("stock", "Blunt", 10, 2.0), tool("bayonet", "Stab", 19, 2.0, 0.32)]),
    ("Nord", "Rifle", "Nordic rifle", "Nord tüfeği",
     "A bolt rifle with a pale birch stock and a box magazine on its side that is filled without opening the action, so it fires faster than other bolt rifles.",
     "Soluk huş dipçikli ve yan tarafında, mekanizma açılmadan doldurulan bir kutu şarjörü olan sürgülü bir tüfek; bu yüzden diğer sürgülü tüfeklerden hızlı ateş eder.",
     3, "nord_rifle", dict(STEAM, cool=1.2), [tool("stock", "Blunt", 11, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
    ("Hellas", "Rifle", "Hellenic rifle", "Helen tüfeği",
     "A single-shot bolt rifle with silver bands and a long sword bayonet. The evzones carried it into the mountains.",
     "Gümüş bilezikli ve uzun kılıç süngülü, tek atışlı sürgülü bir tüfek. Evzonlar onu dağlara taşıdı.",
     3, "hellas_rifle", dict(STEAM, acc=(0.62, 0.8, 0.9, 0.78)), [tool("stock", "Blunt", 10, 2.0), tool("bayonet", "Stab", 18, 2.0, 0.3)]),
    ("Tianxia", "Rifle", "Tianxia rifle", "Tianxia tüfeği",
     "A bolt rifle from the new arsenals, its dark red stock bound in brass and a red tassel at the muzzle for luck. Made by the thousand, it needs less work and fewer parts than any other rifle.",
     "Yeni cephaneliklerden çıkma, koyu kırmızı dipçiği pirinçle sarılı ve namlu ağzında uğur için kırmızı bir püskülü olan sürgülü bir tüfek. Binlercesi yapıldı; her tüfekten daha az emek ve parça ister.",
     3, "tianxia_rifle", dict(STEAM, work=9000, cost={"Steel": 45, "WoodLog": 15, "ComponentIndustrial": 1}), [tool("stock", "Blunt", 10, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
    ("Albion", "Breechloader", "breech-loading rifle", "kuyruktan dolma tüfek",
     "A falling-block rifle: pull the lever, drop in a cartridge, close it and fire. A trained man fires ten aimed rounds a minute.",
     "Düşen kamalı bir tüfek: manivelayı çek, bir fişek koy, kapat ve ateş et. Eğitimli bir asker dakikada on nişanlı atış yapar.",
     3, "albion_breechloader", dict(STEAM, warmup=1.2, cool=1.3), [tool("stock", "Blunt", 10, 2.0), tool("bayonet", "Stab", 17, 2.0, 0.3)]),
    ("Pars", "Rifle", "Persian rifle", "Pers tüfeği",
     "A bolt rifle whose stock is inlaid in khatam, thousands of tiny stars of bone, brass and wood. A treasure that also shoots, and the longest-ranged rifle of the nations.",
     "Dipçiği hatemle, kemikten, pirinçten ve tahtadan binlerce küçük yıldızla kakılmış sürgülü bir tüfek. Ateş de eden bir hazine ve devletlerin en uzun menzilli tüfeği.",
     3, "pars_rifle", dict(STEAM, rng=41.9, acc=(0.6, 0.76, 0.88, 0.84)), [tool("stock", "Blunt", 10, 2.0), tool("barrel", "Blunt", 9, 2.0)]),
]

# Guns that already existed and now belong to an age, so troops carry them from that age on.
EXISTING = [("Roma", "HE_Roma_Carbine", 3), ("Yamato", "HE_Yamato_Tanegashima", 2), ("Albion", "HE_Albion_Musket", 2),
            ("Albion", "HE_Albion_Rifle", 2), ("Kemet", "HE_Kemet_DesertRifle", 3), ("Pars", "HE_Pars_Jezail", 2),
            ("Inti", "HE_Inti_Carbine", 3)]

# The uniform coats: (nation, key, en, tr, desc en, desc tr, colour)
UNIFORMS = [
    ("Roma", "FieldCoat", "legion field coat", "lejyon sahra ceketi",
     "A long double-breasted coat in imperial crimson with bronze buttons and an eagle gorget at the throat.",
     "Bronz düğmeli ve boğazında kartallı bir boyunluk olan, imparatorluk kızılı, uzun, kruvaze bir ceket.", "(0.52, 0.10, 0.16)"),
    ("Yamato", "ArmyCoat", "Yamato army coat", "Yamato ordu ceketi",
     "A dark blue tunic with gold frogging across the chest and a red collar and hem.",
     "Göğsü boyunca altın kordonlu, kırmızı yakalı ve etekli koyu mavi bir ceket.", "(0.15, 0.18, 0.28)"),
    ("Nord", "FieldCoat", "Nordic greatcoat", "Nord kaputu",
     "A heavy grey-blue greatcoat with a fur collar and two rows of pewter buttons. Made for winters that do not end.",
     "Kürk yakalı ve iki sıra kalay düğmeli, ağır, gri mavi bir kaput. Bitmeyen kışlar için yapılmış.", "(0.34, 0.40, 0.48)"),
    ("Hellas", "Evzone", "evzone dress", "evzon kıyafeti",
     "A dark blue jacket embroidered in gold over the white pleated fustanella, with a red sash. The mountains' own uniform.",
     "Beyaz pilili fustanellanın üstünde altınla işlenmiş koyu mavi bir ceket ve kırmızı bir kuşak. Dağların kendi üniforması.",
     "(0.16, 0.22, 0.44)"),
    ("Tianxia", "ArmyCoat", "new army coat", "yeni ordu ceketi",
     "A short red coat with a dark border and the round placard of the new army on the chest and back.",
     "Koyu kenarlı ve göğsünde ve sırtında yeni ordunun yuvarlak levhası olan kısa, kırmızı bir ceket.", "(0.62, 0.20, 0.14)"),
    ("Albion", "RifleGreen", "rifle green jacket", "avcı yeşili ceket",
     "The dark green of the rifle regiments, with black facings, black buttons and a cross belt. It hides in a hedge; it is meant to.",
     "Siyah yakalı, siyah düğmeli ve çapraz kemerli avcı alaylarının koyu yeşili. Bir çalılıkta kaybolur; amaç da budur.",
     "(0.17, 0.28, 0.20)"),
    ("Kemet", "FieldCoat", "Kemetic field coat", "Kemet sahra ceketi",
     "A light khaki coat for the desert sun, a turquoise collar echoing the old broad collar and a leather shoulder strap.",
     "Çöl güneşi için açık haki bir ceket, eski geniş gerdanlığı anımsatan turkuaz bir yaka ve deri bir omuz kayışı.", "(0.68, 0.60, 0.42)"),
    ("Pars", "Chokha", "chokha", "çoha",
     "A long fitted coat with rows of silver cartridge loops across the chest and a narrow dark belt.",
     "Göğsü boyunca sıra sıra gümüş fişeklikleri ve dar, koyu bir kemeri olan uzun, bedene oturan bir ceket.", "(0.28, 0.22, 0.20)"),
    ("Inti", "FieldCoat", "Inti field coat", "Inti sahra ceketi",
     "An ochre field coat with a band of tocapu across the chest and a gold sun badge at the throat.",
     "Göğsü boyunca bir tokapu şeridi ve boğazında altın bir güneş rozeti olan hardal sarısı bir sahra ceketi.", "(0.72, 0.52, 0.20)"),
]

AGE_RESEARCH_EN = {
    2: ("{adj} powder arms", "The {nation} way of making a matchlock or a flintlock: the barrel, the lock, the stock and the drill to use them."),
    3: ("{adj} steam army", "Cartridges, rifled barrels and a uniform: the army {nation} raised when the factories came."),
}
AGE_RESEARCH_TR = {
    2: ("{adj} barutlu silahlar", "{nation} usulü bir fitilli ya da çakmaklı tüfek yapmak: namlu, kilit, dipçik ve kullanma talimi."),
    3: ("{adj} buhar ordusu", "Fişekler, yivli namlular ve bir üniforma: fabrikalar geldiğinde {nation} kurduğu ordu."),
}
ADJ_EN = {"Roma": "Roman", "Yamato": "Yamato", "Nord": "Nordic", "Hellas": "Hellenic", "Tianxia": "Tianxia", "Albion": "Albion",
          "Kemet": "Kemetic", "Pars": "Persian", "Inti": "Inti"}
ADJ_TR = {"Roma": "Roma", "Yamato": "Yamato", "Nord": "Nord", "Hellas": "Helen", "Tianxia": "Tianxia", "Albion": "Albion",
          "Kemet": "Kemet", "Pars": "Pers", "Inti": "Inti"}
NATION_TR_GEN = {"Roma": "Nova Roma'nın", "Yamato": "Yamato'nun", "Nord": "Nordheim'ın", "Hellas": "Hellas'ın", "Tianxia": "Tianxia'nın",
                 "Albion": "Albion'un", "Kemet": "Yeni Kemet'in", "Pars": "Pars'ın", "Inti": "Inti'nin"}

RESEARCH = {}
for nation in NATION_EN:
    for age in (2, 3):
        if age == 2 and not any(g[0] == nation and g[6] == 2 for g in GUNS):
            continue
        en, den = AGE_RESEARCH_EN[age]
        tr, dtr = AGE_RESEARCH_TR[age]
        prereqs = ["Gunsmithing"] if age == 2 else (["Gunsmithing", "ComplexClothing"] + ([RESEARCH[(nation, 2)]] if (nation, 2) in RESEARCH else []))
        RESEARCH[(nation, age)] = age_research(
            nation, "PowderArms" if age == 2 else "SteamArmy",
            en.format(adj=ADJ_EN[nation]), tr.format(adj=ADJ_TR[nation]),
            den.format(nation=NATION_EN[nation]), dtr.format(nation=NATION_TR_GEN[nation]),
            age, 1300 if age == 2 else 2200, prereqs, 30 if age == 2 else 45)

for nation, k, en, tr, den, dtr, age, painter, s, tools in GUNS:
    name = ranged(nation, k, en, tr, den, dtr, "Industrial", RESEARCH[(nation, age)], s.get("bullet") or (BALL if age == 2 else CARTRIDGE),
                  s["warmup"], s["rng"], s["cool"], s["acc"], s["mass"], s["work"], painter, s["cost"],
                  klass=("Ranged", "RangedHeavy", "LongShots"), tools=tools, weapon_tags=[age_tag(nation, age)], **ABILITY_SOUND)
    mark(name, nation, age)

for nation, defname, age in EXISTING:
    mark(defname, nation, age, ext=False)

for nation, k, en, tr, den, dtr, color in UNIFORMS:
    name = apparel(nation, k, en, tr, den, dtr, "Industrial", RESEARCH[(nation, 3)], None, ["Shell"], ["Torso", "Neck", "Shoulders", "Arms"],
                   {"MaxHitPoints": 180, "ArmorRating_Sharp": 0.16, "ArmorRating_Blunt": 0.1, "ArmorRating_Heat": 0.12,
                    "Insulation_Cold": 20, "Insulation_Heat": 6},
                   "heirs_coat_icon", stuff=None, cost={"Cloth": 70, "Steel": 5}, work=9500, mass=1.6, color=color,
                   equipped={"SocialImpact": 0.04}, pargs={"kind": f"HE_{nation}_{k}"})
    assert name in COATS, name
    d = find("ThingDef", name)
    d.fields["graphicData"]["shaderType"] = "CutoutComplex"
    tex(f"HeirsOfEarth/Apparel/{name}_m", "heirs_coat_icon", kind=name, mask=True)
    app = d.fields["apparel"]
    path = f"HeirsOfEarth/Apparel/Worn/Body/{name}"
    app["wornGraphicPath"] = path
    app["useWornGraphicMask"] = True
    for body in BODIES:
        for rot in ROTS:
            tex(f"{path}_{body}_{rot}", "heirs_body", kind=name, body=body, rot=rot)
            tex(f"{path}_{body}_{rot}m", "heirs_body", kind=name, body=body, rot=rot, mask=True)
    mark(name, nation, 3, extra_tag=False)

# ------------------------------------------------------------------ text
key("HE_Age1", "Age of Founding", "Kuruluş Çağı")
key("HE_Age2", "Age of Powder", "Barut Çağı")
key("HE_Age3", "Age of Steam", "Buhar Çağı")
key("HE_AgeLabel", "{0}: {1}", "{0}: {1}")
key("HE_AgeText2", "{0} has entered the Age of Powder.\n\n{1} has opened arsenals and gunpowder mills. From now on their troops carry firearms, "
    "their traders sell them, and your colony may research them even if {0} is not your heritage.\n\nNew: {2}.",
    "{0} Barut Çağı'na girdi.\n\n{1} cephaneler ve barut değirmenleri açtı. Bundan sonra askerleri ateşli silah taşıyor, tüccarları "
    "bunları satıyor ve mirasın {0} olmasa da kolonin bunları araştırabilir.\n\nYeni: {2}.")
key("HE_AgeText3", "{0} has entered the Age of Steam.\n\n{1} has built factories and raised a new army in uniform. Their troops now carry "
    "breech-loading rifles and wear the national coat, their traders sell both, and your colony may research them.\n\nNew: {2}.",
    "{0} Buhar Çağı'na girdi.\n\n{1} fabrikalar kurdu ve üniformalı yeni bir ordu topladı. Askerleri artık kuyruktan dolma tüfekler "
    "taşıyor ve ulusal ceketi giyiyor, tüccarları ikisini de satıyor ve kolonin bunları araştırabilir.\n\nYeni: {2}.")
key("HE_AgeChronicle", "{0} entered the {1}.", "{0}, {1}'na girdi.")
key("HE_AgeRateBase", "Steady progress", "Doğal ilerleme")
key("HE_AgeRateScholarly", "Scholarly ruler", "Bilgin hükümdar")
key("HE_AgeRateAllies", "Allies", "Müttefikler")
key("HE_AgeRateWar", "At war", "Savaşta")
key("HE_AgeRateScience", "Science treaty with you", "Seninle bilim antlaşması")
key("HE_AgeRateTrade", "Trade link with you", "Seninle ticaret bağı")
key("HE_AgeRateTowns", "Many towns", "Çok sayıda kasaba")
key("HE_AgesHeading", "Ages of the nations", "Devletlerin çağları")
key("HE_AgesIntro", "Every nation moves from the Age of Founding through the Age of Powder and the Age of Steam to the Electric Age as the years pass. "
    "Each new age arms its troops with its own guns and, from the Age of Steam on, dresses them in its uniform. Its traders sell these, "
    "and you may research them once the nation has reached that age. Peace, allies, treaties and trade with you speed a nation up; "
    "war, famine and plague hold it back. Hover over a nation to see why.",
    "Her devlet yıllar geçtikçe Kuruluş Çağı'ndan Barut ve Buhar çağlarından geçerek Elektrik Çağı'na ilerler. Her yeni çağ askerlerini kendi "
    "tüfekleriyle donatır ve Buhar Çağı'ndan itibaren onları kendi üniformasıyla giydirir. Tüccarları bunları satar ve devlet o çağa ulaştığında "
    "sen de bunları araştırabilirsin. Barış, müttefikler, antlaşmalar ve seninle ticaret bir devleti hızlandırır; savaş, kıtlık ve salgın "
    "onu geri tutar. Nedenini görmek için bir devletin üstüne gel.")
key("HE_AgesOff", "Ages are turned off in the mod settings: every nation keeps its old arms and every item can be researched as before.",
    "Çağlar mod ayarlarında kapalı: her devlet eski silahlarını korur ve her şey eskisi gibi araştırılabilir.")
key("HE_AgesLast", "the last age", "son çağ")
key("HE_AgesToward", "{1} toward the {0}", "{0} yolunda: {1}")
key("HE_AgesPace", "Pace: {0} of the usual speed.", "Hız: olağan hızın {0} kadarı.")
key("HE_AgesItems", "Arms and uniforms of its ages: {0}", "Çağlarının silahları ve üniformaları: {0}")
key("HE_AtlasAge", "Age", "Çağ")
key("HE_NeedAge", "{0} has not reached the {1} yet.", "{0} henüz {1}'na ulaşmadı.")
key("HE_SettingsFourthSpeed", "Fourth game speed button", "Dördüncü oyun hızı düğmesi")
key("HE_SettingsFourthSpeedTip", "Adds a fourth speed button (the game's fastest speed, normally hidden) next to the other three. "
    "Its key is 4 by default and can be changed in the keyboard settings.",
    "Diğer üçünün yanına dördüncü bir hız düğmesi (oyunun normalde gizli olan en yüksek hızı) ekler. Tuşu varsayılan olarak 4'tür ve "
    "klavye ayarlarından değiştirilebilir.")
key("HE_SpeedFourthTip", "Fastest speed. It slows down by itself when something needs your attention, like the third speed.",
    "En yüksek hız. Üçüncü hız gibi, ilgilenmen gereken bir şey olduğunda kendiliğinden yavaşlar.")
key("HE_SettingsAges", "Ages of progress", "İlerleme çağları")
key("HE_SettingsAgesTip", "Nations move through the Age of Founding, Powder, Steam and Electricity, getting new guns and uniforms. Turn off to keep the "
    "nations as they were before 4.2.",
    "Devletler Kuruluş, Barut, Buhar ve Elektrik çağlarından geçerek yeni tüfekler ve üniformalar kazanır. Devletleri 4.2 öncesindeki gibi tutmak için kapat.")
key("HE_SettingsAgeSpeed", "Pace of the ages: {0}", "Çağların hızı: {0}")
