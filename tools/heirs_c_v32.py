"""Heirs of Earth 3.2 "Equal Heritage": every nation brought up to the same depth.

Targets per nation: 5 buildings, 3 floors, 3 foods, 5 weapons, 5 clothes (with leader regalia) and one defensive structure.
Most new things hang on existing research of the nation; the defensive structures get one new project each.
"""
from heirs_data import FILES
from heirs_kit import ERA_Y, NATION_X, ROW, food

# ------------------------------------------------------------------ research grid helper


def free_slot(nation, tech, col=2.0):
    """First free (col, row) in a nation's research column for an age, so new projects never overlap old ones."""
    taken = set()
    for rel, defs in FILES.items():
        if not rel.startswith("Research/"):
            continue
        for d in defs:
            x, y = d.fields.get("researchViewX"), d.fields.get("researchViewY")
            if x is not None and y is not None:
                taken.add((round(float(x), 2), round(float(y), 2)))
    for c in (col, col - 1, col + 1, col - 2, 0.0, 3.0):
        for r in range(0, 5):
            if (round(NATION_X[nation] + c, 2), round(ERA_Y[tech] + r * ROW, 2)) not in taken:
                return c, r
    raise ValueError(f"no free research slot for {nation} {tech}")


# ------------------------------------------------------------------ foods: two per nation
# (nation, key, en, tr, description en, description tr, research, painter kind, ingredients, joy)
FOODS = [
    ("Roma", "Lucanica", "lucanica and bread", "lucanica ve ekmek",
     "A coil of smoked pork sausage spiced with pepper, cumin and rue, served with a round of bread. Legionaries carried it on the march.",
     "Biber, kimyon ve sedefotu ile baharatlanmış, bir yuvarlak ekmekle sunulan bir halka füme domuz sucuğu. Lejyonerler yürüyüşte yanlarında taşırdı.",
     "HE_Roma_Garum", "lucanica", ("MeatRaw", "PlantFoodRaw"), 0),
    ("Roma", "Libum", "libum", "libum",
     "A cheese cake baked on bay leaves and glazed with honey, offered at festivals and eaten with great ceremony afterwards.",
     "Defne yaprakları üstünde pişirilip balla parlatılan bir peynirli kek. Bayramlarda adak olarak sunulur, sonra büyük törenle yenir.",
     "HE_Roma_Forum", "libum", ("FoodRaw",), 0.08),
    ("Yamato", "Miso", "miso soup", "miso çorbası",
     "A lacquered bowl of fermented bean broth with tofu and spring onion. Every Yamato morning starts with one.",
     "Tofu ve taze soğanlı, fermente fasulye suyundan yapılmış bir lake kâse çorba. Her Yamato sabahı bununla başlar.",
     "HE_Yamato_Onigiri", "miso", ("FoodRaw",), 0),
    ("Yamato", "Mochi", "mochi", "moçi",
     "Pounded sweet rice cakes in three colours on a skewer, made for the tea ceremony and the new year.",
     "Şişe dizilmiş, üç renkli dövülmüş tatlı pirinç kekleri. Çay töreni ve yeni yıl için yapılır.",
     "HE_Yamato_TeaHouse", "mochi", ("PlantFoodRaw",), 0.08),
    ("Nord", "HunterStew", "hunter's stew", "avcı yahnisi",
     "Venison, roots and barley simmered all day in an iron pot over the long fire. It keeps a hall warm through the dark months.",
     "Uzun ateşin üstündeki demir kazanda bütün gün kaynayan geyik eti, kökler ve arpa. Karanlık aylar boyunca bir salonu sıcak tutar.",
     "HE_Nord_Hunting", "hunter_stew", ("MeatRaw", "PlantFoodRaw"), 0),
    ("Nord", "Flatbread", "honey flatbread", "ballı yassı ekmek",
     "Thin barley bread baked on a stone and spread with honey and butter, served with mead at every feast.",
     "Bir taşın üstünde pişirilip bal ve tereyağıyla sürülen ince arpa ekmeği. Her ziyafette bal şarabıyla sunulur.",
     "HE_Nord_MeadHall", "flatbread", ("PlantFoodRaw",), 0.08),
    ("Hellas", "Skewers", "obeliskos skewers", "obeliskos şişleri",
     "Lamb grilled on iron spits with peppers, served with olives. The smell of them drifts over every festival and every camp.",
     "Biberle birlikte demir şişlerde ızgara edilmiş, zeytinle sunulan kuzu eti. Kokusu her şenliğin ve her ordugâhın üstünde dolaşır.",
     "HE_Hellas_Maza", "skewers", ("MeatRaw",), 0),
    ("Hellas", "Plakous", "plakous", "plakous",
     "Layers of thin dough and soft cheese soaked in honey. Athletes are given it after the games, and nobody refuses.",
     "Balla ıslatılmış ince hamur ve yumuşak peynir katmanları. Oyunlardan sonra atletlere verilir ve kimse reddetmez.",
     "HE_Hellas_Olympic", "plakous", ("FoodRaw",), 0.08),
    ("Tianxia", "Congee", "congee", "pirinç lapası",
     "Rice simmered for hours into a smooth porridge, topped with ginger and spring onion. Easy on the sick and kind to the poor.",
     "Saatlerce pişirilip pürüzsüz bir lapaya dönüşen, zencefil ve taze soğanla süslenmiş pirinç. Hastaya hafif gelir, yoksula iyi gelir.",
     "HE_Tianxia_Dumplings", "congee", ("PlantFoodRaw",), 0),
    ("Tianxia", "Mooncake", "mooncakes", "ay kekleri",
     "Round pastries with a sweet bean and yolk filling, pressed with patterns. They are shared under the full moon of autumn.",
     "Tatlı fasulye ve yumurta sarısı dolgulu, desenli kalıplarla basılmış yuvarlak hamur işleri. Sonbaharın dolunayı altında paylaşılır.",
     "HE_Tianxia_TeaCulture", "mooncake", ("FoodRaw",), 0.08),
    ("Albion", "Roast", "Sunday roast", "pazar rostosu",
     "Roast meat with a risen batter pudding, greens and gravy. The whole household sits down to it once a week.",
     "Kabarmış hamur pudingi, yeşillik ve et suyu sosuyla rosto et. Bütün hane haftada bir kez bunun başına oturur.",
     "HE_Albion_MeatPie", "roast", ("MeatRaw", "PlantFoodRaw"), 0),
    ("Albion", "Scones", "tea and scones", "çay ve çörek",
     "Warm scones with clotted cream and jam and a pot of strong tea. In Albion this counts as a meal and a ceremony at once.",
     "Kaymak ve reçelli sıcak çörekler ve bir demlik koyu çay. Albion'da bu hem yemek hem de tören sayılır.",
     "HE_Albion_Pub", "scones", ("PlantFoodRaw",), 0.08),
    ("Kemet", "Ful", "ful", "ful",
     "Fava beans stewed slowly with oil, garlic and cumin, eaten with flat bread. The meal of every farmer and every pharaoh.",
     "Yağ, sarımsak ve kimyonla ağır ağır pişirilen bakla, yassı ekmekle yenir. Her çiftçinin ve her firavunun yemeği.",
     "HE_Kemet_Bread", "ful", ("PlantFoodRaw",), 0),
    ("Kemet", "DateCake", "date cakes", "hurma kekleri",
     "Small cakes of ground dates, honey and nuts, baked for temple feasts and given to children on festival days.",
     "Öğütülmüş hurma, bal ve cevizden yapılan küçük kekler. Tapınak şölenleri için pişirilir, bayram günlerinde çocuklara verilir.",
     "HE_Kemet_RoyalKitchens", "date_cake", ("PlantFoodRaw",), 0.08),
    ("Pars", "Kebab", "kebab and saffron rice", "kebap ve safranlı pilav",
     "Spiced minced meat grilled on flat swords of iron, laid on a mound of saffron rice. Served at every caravan inn.",
     "Yassı demir kılıçlarda ızgara edilmiş baharatlı kıyma, bir safranlı pilav tepesinin üstüne yatırılır. Her kervansarayda sunulur.",
     "HE_Pars_Pilaf", "kebab", ("MeatRaw", "PlantFoodRaw"), 0),
    ("Pars", "Sholeh", "sholeh zard", "şole zerd",
     "A golden rice pudding with saffron, rosewater and pistachios, drawn with a cinnamon pattern on top. Cooked for vows and blessings.",
     "Safran, gül suyu ve antep fıstıklı, üstüne tarçınla desen çizilmiş altın sarısı bir sütlaç. Adaklar ve dualar için pişirilir.",
     "HE_Pars_GardenCulture", "sholeh", ("PlantFoodRaw",), 0.08),
    ("Inti", "Locro", "locro", "locro",
     "A thick stew of corn, potato and squash, slow cooked in a clay pot. Every mountain village has its own way of making it.",
     "Mısır, patates ve kabaktan yapılan, toprak bir kapta ağır ağır pişirilen koyu bir yahni. Her dağ köyünün kendi tarifi vardır.",
     "HE_Inti_Pachamanca", "locro", ("PlantFoodRaw", "MeatRaw"), 0),
    ("Inti", "Humita", "humitas", "humita",
     "Fresh ground corn mixed with fat and spice, wrapped in husks and steamed. Shared by neighbours who worked the terraces together.",
     "Yağ ve baharatla karıştırılmış taze öğütülmüş mısır, kabuklara sarılıp buharda pişirilir. Teraslarda birlikte çalışan komşular paylaşır.",
     "HE_Inti_Ayni", "humita", ("PlantFoodRaw",), 0.08),
]

for nation, key_, en, tr, den, dtr, research_name, kind, ingredients, joy in FOODS:
    if joy:
        den += " A small treat: eating it is a little joy."
        dtr += " Küçük bir ikram: yemek biraz keyif verir."
    food(nation, key_, en, tr, den, dtr, research_name, "dish", ingredients=ingredients, joy=joy, pargs={"kind": kind})

# ------------------------------------------------------------------ floors: every nation reaches three
from heirs_kit import floor  # noqa: E402

FLOORS = [
    ("Yamato", "Ishidatami", "ishidatami paving", "ishidatami taş döşeme",
     "Grey stone slabs laid in courses, with moss allowed to grow in the joints. Temple paths and castle courts are paved this way.",
     "Sıra sıra döşenmiş, derzlerinde yosunun büyümesine izin verilen gri taş levhalar. Tapınak yolları ve kale avluları böyle döşenir.",
     "HE_Yamato_Torii", "floor_slabs", dict(base="#8e8a80", joint="#4a4640", cols=4, rows=6, moss="#5a6a3a", seed=11),
     2, {"BlocksGranite": 3}, 900),
    ("Nord", "Slate", "slate flagstones", "arduvaz döşeme",
     "Split slabs of dark slate fitted together like a puzzle. Cold underfoot, but they never rot and they shrug off mud.",
     "Bir yapboz gibi birbirine oturtulmuş, yarılmış koyu arduvaz levhalar. Ayak altında soğuktur ama asla çürümez ve çamuru üstünde tutmaz.",
     "HE_Nord_Longhouse", "floor_flags", dict(base="#5a6068", joint="#24262a", seed=12),
     1, {"BlocksSlate": 3}, 800),
    ("Nord", "CarvedBoards", "carved boards", "oymalı tahta",
     "Heavy oak boards with knotwork carved into them by the hall's craftsmen during the long winters.",
     "Uzun kışlarda salonun ustalarının düğüm desenleri oyduğu ağır meşe tahtalar.",
     "HE_Nord_Runes", "floor_boards", dict(base="#6a4a30", joint="#22160e", carve="#3a2416", seed=13),
     2, {"WoodLog": 4}, 1100),
    ("Hellas", "Marble", "marble slabs", "mermer levhalar",
     "Large slabs of white marble with grey veins, polished smooth. Every temple and every rich house in Hellas stands on them.",
     "Gri damarlı, pürüzsüz cilalanmış büyük beyaz mermer levhalar. Hellas'taki her tapınak ve her zengin ev bunların üstünde durur.",
     "HE_Hellas_Columns", "floor_slabs", dict(base="#e6e0d4", joint="#a8a296", cols=2, rows=4, vein="#b8b0a4", seed=14),
     3, {"BlocksMarble": 4}, 1400),
    ("Hellas", "Pebbles", "pebble mosaic", "çakıl mozaik",
     "Black and white river pebbles set in mortar in a running wave, the oldest kind of Hellenic mosaic.",
     "Harca dalga deseninde gömülmüş siyah ve beyaz dere çakılları; Hellas mozaiğinin en eski türü.",
     "HE_Hellas_Meander", "floor_pebbles", dict(ground="#bfb39a", colors=("#2a2826", "#ece6da"), pattern="wave", seed=15),
     2, {"BlocksLimestone": 2}, 1000),
    ("Tianxia", "GreyBrick", "grey brick paving", "gri tuğla döşeme",
     "Fired grey bricks laid in a herringbone. Granary yards and city streets of Tianxia are paved with them.",
     "Balık sırtı deseninde döşenmiş pişmiş gri tuğlalar. Tianxia'nın ambar avluları ve şehir sokakları bunlarla döşelidir.",
     "HE_Tianxia_Granary", "floor_herringbone", dict(base="#7a7a76", joint="#3a3a38", width=64, grain=False, seed=16),
     1, {"BlocksGranite": 2}, 800),
    ("Tianxia", "Lacquer", "red lacquer boards", "kırmızı lake tahta",
     "Boards coated in many layers of red lacquer until they shine like glass. Only halls of state and rich houses can afford them.",
     "Cam gibi parlayana kadar kat kat kırmızı lake sürülmüş tahtalar. Ancak devlet salonları ve zengin evler karşılayabilir.",
     "HE_Tianxia_PorcelainKiln", "floor_boards", dict(base="#8a2a1e", joint="#2a0c08", spec=True, seed=17),
     4, {"WoodLog": 3, "Silver": 2}, 1400),
    ("Albion", "Parquet", "parquet", "parke",
     "Oak blocks laid in a herringbone and waxed to a warm shine, the floor of every proper drawing room.",
     "Balık sırtı deseninde döşenip sıcak bir parlaklıkla cilalanmış meşe bloklar; her düzgün salonun zemini.",
     "HE_Albion_JointStock", "floor_herringbone", dict(base="#8a5a30", joint="#3a2414", width=64, seed=18),
     3, {"WoodLog": 4}, 1200),
    ("Kemet", "Sandstone", "sandstone slabs", "kum taşı levhalar",
     "Golden sandstone cut into even slabs by the royal masons. Temples, courts and tombs of Kemet are floored with it.",
     "Kraliyet taş ustalarının düzgün levhalara kestiği altın renkli kum taşı. Kemet'in tapınakları, avluları ve mezarları bununla döşenir.",
     "HE_Kemet_Stonemasons", "floor_slabs", dict(base="#d0a86a", joint="#8a6a3e", cols=4, rows=8, seed=19),
     2, {"BlocksSandstone": 3}, 900),
    ("Pars", "Glazed", "glazed star tiles", "sırlı yıldız çini",
     "Turquoise tiles glazed with eight-pointed stars, fired in the kilns of the royal cities. Cool underfoot even at noon.",
     "Kraliyet şehirlerinin fırınlarında pişirilmiş, sekiz köşeli yıldızlarla sırlanmış turkuaz çiniler. Öğle vakti bile ayak altında serindir.",
     "HE_Pars_SatrapLaw", "floor_glazed", dict(seed=20),
     4, {"BlocksSandstone": 3, "Silver": 3}, 1500),
    ("Pars", "GardenPath", "garden path", "bahçe yolu",
     "Terracotta and pale pebbles set in diamonds between brick borders, the walks of a Parsian paradise garden.",
     "Tuğla kenarlar arasında baklava deseninde dizilmiş pişmiş toprak ve açık renkli çakıllar; bir Pars cennet bahçesinin yürüyüş yolları.",
     "HE_Pars_GardenCulture", "floor_pebbles", dict(ground="#b8865a", colors=("#8a4a2a", "#e8d8b8"), pattern="quatrefoil", border="#7a3e22", seed=21),
     2, {"BlocksSandstone": 2}, 900),
    ("Inti", "FittedStone", "fitted stone", "geçme taş",
     "Many-sided stones cut to fit each other so tightly that no blade slips between them. Earthquakes cannot shake them loose.",
     "Aralarına hiçbir bıçak girmeyecek kadar sıkı birbirine oturtulmuş çok kenarlı taşlar. Depremler bile onları yerinden oynatamaz.",
     "HE_Inti_Mita", "floor_polygonal", dict(seed=22),
     3, {"BlocksGranite": 4}, 1600),
    ("Inti", "Adobe", "adobe tiles", "kerpiç karo",
     "Sun-dried tiles of clay and straw, warm in colour and cheap to make. Storehouses and village homes use them.",
     "Kil ve samandan yapılmış güneşte kurutulmuş karolar; rengi sıcak, yapımı ucuzdur. Ambarlarda ve köy evlerinde kullanılır.",
     "HE_Inti_Qullqa", "floor_slabs", dict(base="#b8875a", joint="#7a5636", cols=2, rows=4, stagger=False, speck="#d8b878", seed=23),
     1, {"WoodLog": 1}, 500),
]

for nation, key_, en, tr, den, dtr, research_name, painter_name, pargs, beauty, cost, work in FLOORS:
    floor(nation, key_, en, tr, den, dtr, research_name, painter_name, beauty=beauty, cost=cost, work=work, pargs=pargs)
