"""Heirs of Earth 3.2 part four: clothes and leader regalia, so every nation has at least five pieces of apparel.

Regalia (the laurel wreath, the jarl's circlet, the dragon robe, the bicorne, the nemes, the kidaris and the mascaypacha)
raise social impact noticeably; everyday clothes only a little. Circlets and wreaths have no worn graphic of their own,
so they show on the pawn only in the gear tab, like vanilla rings of office would.
"""
from heirs_kit import SMITHY, apparel

BODY = ["Torso", "Shoulders", "Arms", "Legs"]
DRAPE = ["Torso", "Shoulders", "Legs"]
HEAD = ["UpperHead"]


def clothes(nation, key, en, tr, den, dtr, tech, research_name, worn, groups, kind, cold, heat, social, stuff=("Fabric",), count=70,
            work=5000, mass=1.0, hp=120):
    return apparel(nation, key, en, tr, den, dtr, tech, research_name, worn, ["Shell"], groups,
                   {"MaxHitPoints": hp, "StuffEffectMultiplierArmor": 0.15, "StuffEffectMultiplierInsulation_Cold": cold,
                    "StuffEffectMultiplierInsulation_Heat": heat},
                   "garment", stuff=stuff, stuff_count=count, work=work, mass=mass, equipped={"SocialImpact": social}, pargs={"kind": kind})


def headgear(nation, key, en, tr, den, dtr, tech, research_name, worn, kind, social, stuff=("Fabric", "Leathery"), count=25, work=2400,
             cold=0.15, metal=False, cost=None):
    return apparel(nation, key, en, tr, den, dtr, tech, research_name, worn, ["Overhead"], HEAD,
                   {"MaxHitPoints": 60, "StuffEffectMultiplierArmor": 0.05, "StuffEffectMultiplierInsulation_Cold": cold,
                    "StuffEffectMultiplierInsulation_Heat": 0.05},
                   "headwear", stuff=stuff, stuff_count=count, cost=cost, work=work, mass=0.3, head=True,
                   users=SMITHY if metal else None, equipped={"SocialImpact": social}, pargs={"kind": kind})


GOLD_ONLY = ("Metallic",)

# ------------------------------------------------------------------ Nova Roma
clothes("Roma", "Toga", "toga", "toga",
        "A great half-circle of white wool wrapped around the body and over the left shoulder. Only citizens may wear it; a purple border marks a magistrate.",
        "Vücuda ve sol omzun üstüne sarılan büyük, yarım daire biçiminde beyaz bir yün. Sadece yurttaşlar giyebilir; mor kenar bir yargıcı belli eder.",
        "Medieval", "HE_Roma_Senate", "Robe/Robe", DRAPE, "toga", 0.45, 0.4, 0.10, count=80, work=5500, mass=1.2)
headgear("Roma", "Laurel", "laurel wreath", "defne tacı",
         "A wreath of laurel leaves beaten from gold, the crown of a general in triumph. A slave once stood behind him whispering that he was only a man.",
         "Altından dövülmüş defne yapraklarından bir taç; zafer alayındaki bir komutanın tacı. Bir zamanlar arkasında bir köle durur, ona yalnızca bir insan olduğunu fısıldardı.",
         "Medieval", "HE_Roma_Aquila", None, "laurel", 0.12, stuff=GOLD_ONLY, count=20, work=6000, cold=0, metal=True)

# ------------------------------------------------------------------ Yamato
clothes("Yamato", "Kamishimo", "kamishimo", "kamişimo",
        "The formal dress of a retainer: a sleeveless jacket with stiff wide shoulders over pleated hakama trousers, marked with the house crest.",
        "Bir maiyet adamının resmî kıyafeti: pileli hakama pantolonun üstüne giyilen, sert ve geniş omuzlu kolsuz bir ceket; hanedan armasıyla işaretlidir.",
        "Medieval", "HE_Yamato_Ceremony", "Jacket/Jacket", ["Torso", "Shoulders", "Legs"], "kamishimo", 0.4, 0.4, 0.07, count=70, work=6000)
headgear("Yamato", "Jingasa", "jingasa", "jingasa",
         "A wide, shallow cone hat of lacquered hardened leather, worn by foot soldiers and officials on the road. It keeps off sun, rain and a falling blow.",
         "Piyadelerin ve yoldaki memurların taktığı, cilalı sertleştirilmiş deriden geniş, basık konik bir şapka. Güneşi, yağmuru ve inen bir darbeyi uzak tutar.",
         "Medieval", "HE_Yamato_Levy", "CowboyHat/CowboyHat", "jingasa", 0.02, stuff=("Leathery", "Woody"), count=25)

# ------------------------------------------------------------------ Nordheim
headgear("Nord", "Circlet", "jarl's circlet", "jarl tacı",
         "A plain silver band worked with knotwork and set with one red stone. A jarl needs no grander crown: his word at the Thing is enough.",
         "Düğüm işlemeli, tek bir kırmızı taş kakılmış sade bir gümüş bant. Bir jarlın daha görkemli bir taca ihtiyacı yoktur: Thing'deki sözü yeter.",
         "Medieval", "HE_Nord_Thing", None, "circlet", 0.12, stuff=GOLD_ONLY, count=20, work=5000, cold=0, metal=True)

# ------------------------------------------------------------------ Hellas
clothes("Hellas", "Himation", "himation", "himation",
        "A large wool mantle worn over the chiton, wrapped around the body and thrown over the shoulder. Philosophers wear nothing else.",
        "Khitonun üstüne giyilen, vücuda sarılıp omuzdan atılan büyük bir yün manto. Filozoflar başka bir şey giymez.",
        "Neolithic", "HE_Hellas_Chiton", "Robe/Robe", DRAPE, "himation", 0.55, 0.35, 0.05, count=70, work=4000)
headgear("Hellas", "OliveWreath", "olive wreath", "zeytin tacı",
         "A wreath cut from the sacred olive tree, the only prize of the games. It is worth nothing and everyone wants it.",
         "Kutsal zeytin ağacından kesilmiş bir taç, oyunların tek ödülü. Hiçbir değeri yoktur ve herkes onu ister.",
         "Neolithic", "HE_Hellas_Olympic", None, "olive", 0.10, stuff=None, count=0, work=1200, cold=0, cost={"WoodLog": 2})

# ------------------------------------------------------------------ Tianxia
clothes("Tianxia", "DragonRobe", "dragon robe", "ejderha kaftanı",
        "A robe of imperial yellow silk embroidered with a five-clawed dragon above the waves. Only the ruler and those he honours may wear it.",
        "Dalgaların üstünde beş pençeli bir ejderhayla işlenmiş, imparatorluk sarısı ipekten bir kaftan. Sadece hükümdar ve onurlandırdıkları giyebilir.",
        "Medieval", "HE_Tianxia_Harmony", "Robe/Robe", BODY, "dragon_robe", 0.7, 0.35, 0.14, count=90, work=9000, mass=1.4)
headgear("Tianxia", "Futou", "futou cap", "futou başlığı",
         "A black gauze cap with two long stiff wings at the back, worn by officials who passed the examinations. The wings stop them whispering to each other at court.",
         "Arkasında iki uzun sert kanadı olan siyah tül bir başlık; sınavları geçen memurlar takar. Kanatlar sarayda birbirlerine fısıldamalarını engeller.",
         "Medieval", "HE_Tianxia_Examination", "BowlerHat/BowlerHat", "futou", 0.06, stuff=("Fabric",), count=25)

# ------------------------------------------------------------------ Albion
clothes("Albion", "FrockCoat", "frock coat", "redingot",
        "A knee-length black wool coat with tails, silk lapels and brass buttons. Bankers, engineers and members of parliament all wear one.",
        "Kuyruklu, ipek yakalı ve pirinç düğmeli diz boyu siyah yün bir ceket. Bankacılar, mühendisler ve milletvekilleri hep bir tane giyer.",
        "Industrial", "HE_Albion_Tweed", "Duster/Duster", BODY, "frock_coat", 0.6, 0.25, 0.07, count=75, work=7000, mass=1.3)
headgear("Albion", "TopHat", "top hat", "silindir şapka",
         "A tall hat of black silk plush. It adds a head of height and a great deal of respectability.",
         "Siyah ipek peluştan uzun bir şapka. Bir baş boyu uzunluk ve epey saygınlık katar.",
         "Industrial", "HE_Albion_JointStock", "BowlerHat/BowlerHat", "top_hat", 0.06, stuff=("Fabric",), count=25)
headgear("Albion", "Bicorne", "bicorne", "bikorn",
         "A two-cornered officer's hat trimmed with gold lace and the national cockade. Admirals and generals wear it sideways; everyone salutes.",
         "Altın şeritle ve ulusal kokartla süslü, iki köşeli bir subay şapkası. Amiraller ve generaller onu yan giyer; herkes selam verir.",
         "Industrial", "HE_Albion_Redcoat", "CowboyHat/CowboyHat", "bicorne", 0.12, stuff=("Fabric",), count=30, work=3500)

# ------------------------------------------------------------------ New Kemet
headgear("Kemet", "Nemes", "nemes", "nemes",
         "The striped royal headcloth with lappets falling to the chest and a gold cobra at the brow. Only the king and his heir may wear it.",
         "Göğse dökülen uçları ve alında altın bir kobrası olan çizgili kraliyet başlığı. Yalnızca kral ve varisi takabilir.",
         "Medieval", "HE_Kemet_ChildrenOfSun", "Hood/Hood", "nemes", 0.12, stuff=("Fabric",), count=35, work=4000, cold=0.2)
clothes("Kemet", "LeopardMantle", "leopard mantle", "leopar postu",
        "A leopard skin worn over a white linen robe, the mark of the high priest who reads the stars and the sun calendar.",
        "Beyaz keten bir kaftanın üstüne giyilen leopar postu; yıldızları ve güneş takvimini okuyan baş rahibin işareti.",
        "Medieval", "HE_Kemet_SunCalendar", "Cape/Cape", ["Torso", "Shoulders"], "leopard_mantle", 0.3, 0.2, 0.08, stuff=("Leathery",), count=60, work=4500)

# ------------------------------------------------------------------ Pars
headgear("Pars", "Kidaris", "kidaris", "kidaris",
         "The tall fluted tiara of the King of Kings, banded with gold and turquoise. To wear it upright is the king's right alone.",
         "Kralların Kralı'nın altın ve turkuvazla şeritlenmiş, uzun yivli tacı. Onu dik takmak yalnızca kralın hakkıdır.",
         "Medieval", "HE_Pars_SatrapLaw", None, "kidaris", 0.14, stuff=GOLD_ONLY, count=25, work=7000, cold=0, metal=True)
clothes("Pars", "Candys", "candys", "kandys",
        "A long crimson robe with hanging sleeves worn over the shoulders, given by the king to those he wishes to honour.",
        "Omuzlara asılan sarkık kollu uzun, kırmızı bir kaftan; kralın onurlandırmak istediklerine verdiği bir armağan.",
        "Medieval", "HE_Pars_CarpetLoom", "Robe/Robe", BODY, "candys", 0.6, 0.45, 0.08, count=80, work=6500, mass=1.3)

# ------------------------------------------------------------------ Inti
headgear("Inti", "Mascaypacha", "mascaypacha", "maskaypaça",
         "A braided band wound around the head with a fringe of red wool over the brow and three feathers above. It is the crown of the Sapa Inca.",
         "Başa sarılan, alnın üstünde kırmızı yün saçaklı ve tepesinde üç tüy olan örgülü bir bant. Sapa İnka'nın tacıdır.",
         "Medieval", "HE_Inti_KnotKeepers", None, "mascay", 0.14, stuff=("Fabric",), count=25, work=5000, cold=0.05)
clothes("Inti", "FeatherCape", "feather cape", "tüy pelerin",
        "Thousands of red, yellow, green and blue feathers knotted onto cotton in rows. It takes the weavers of a whole village a season to make one.",
        "Sıra sıra pamuğa düğümlenmiş binlerce kırmızı, sarı, yeşil ve mavi tüy. Bir köyün bütün dokumacılarının birini yapması bir mevsim sürer.",
        "Medieval", "HE_Inti_Qullqa", "Cape/Cape", ["Torso", "Shoulders"], "feather", 0.35, 0.3, 0.08, count=60, work=8000)
