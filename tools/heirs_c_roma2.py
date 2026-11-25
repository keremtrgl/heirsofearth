"""Nova Roma 1.0: the remaining traditions, armour, ranged weapon, bath, forum, dining and food."""
from heirs_c_roma import NATION, R_AQUEDUCT, R_CONCRETE, R_ENGINEERS, R_PILUM, R_ROADS, R_SENATE, R_SMITHING, R_STANDARD
from heirs_data import add
from heirs_kit import SMITHY, apparel, deco, floor, food, projectile, ranged, research, resource, tool
from heirs_xml import T

# ------------------------------------------------------------------ research
R_GARUM = research(NATION, "Garum", "garum and puls", "garum ve puls",
                   "Learn the kitchen of the legions: thick puls porridge and the fermented fish sauce garum that every Roman table expects.",
                   "Lejyonların mutfağını öğren: koyu puls lapası ve her Roma sofrasının beklediği fermente balık sosu garum.",
                   450, "Neolithic", 2, 0)
R_CURSUS = research(NATION, "Cursus", "cursus honorum", "cursus honorum",
                    "The ladder of public offices: every citizen who wants to lead must first serve, learn and be judged.",
                    "Kamu görevlerinin merdiveni: yönetmek isteyen her yurttaş önce hizmet etmeli, öğrenmeli ve yargılanmalıdır.",
                    600, "Neolithic", 0, 1, prereqs=[R_STANDARD], knowledge=10, tradition=True,
                    stats=[("GlobalLearningFactor", 0.08, 1, "Colonists"), ("MentalBreakThreshold", 0.02, 1, "Colonists")],
                    effect=T("Colonists learn 8% faster, but the pressure of office raises their mental break threshold by 2%.",
                             "Kolonistler %8 daha hızlı öğrenir, ama görev baskısı zihinsel çöküş eşiklerini %2 yükseltir."))
R_FORUM = research(NATION, "Forum", "the forum", "forum",
                   "Raise marble statues of great citizens around an open forum.",
                   "Açık bir forumun çevresine büyük yurttaşların mermer heykellerini dik.",
                   800, "Medieval", 1, 0, prereqs=[R_CONCRETE], knowledge=10)
R_LORICA = research(NATION, "Lorica", "lorica segmentata", "lorica segmentata",
                    "Forge the banded plate armour of the legions and the bronze galea helmet with its red crest. Also teaches the simple wool tunic.",
                    "Lejyonların şeritli plaka zırhını ve kırmızı sorguçlu bronz galea miğferini döv. Basit yün tunikayı da öğretir.",
                    1100, "Medieval", 0, 2, prereqs=[R_SMITHING], knowledge=20)
R_THERMAE = research(NATION, "Thermae", "thermae", "thermae",
                     "Heated public baths fed by the aqueducts, where citizens wash, gossip and forget their troubles. Also teaches mosaic floors.",
                     "Su kemerlerinden beslenen, yurttaşların yıkandığı, dedikodu yaptığı ve dertlerini unuttuğu ısıtmalı hamamlar. Mozaik zemini de öğretir.",
                     1300, "Medieval", 2, 2, prereqs=[R_AQUEDUCT], knowledge=35)
R_TESTUDO = research(NATION, "Testudo", "testudo", "testudo",
                     "The tortoise formation: shields locked above and around, the legion advances slowly but almost nothing gets through.",
                     "Kaplumbağa düzeni: kalkanlar üstte ve çevrede kenetlenir, lejyon yavaş ilerler ama neredeyse hiçbir şey içeri giremez.",
                     1400, "Medieval", 0, 3, prereqs=[R_LORICA, R_PILUM], knowledge=40, tradition=True,
                     stats=[("ArmorRating_Sharp", 0.05, 1, "Colonists"), ("MoveSpeed", 0, 0.97, "Colonists")],
                     effect=T("Colonists gain +5% sharp armour but move 3% slower. Unlocks the scutum display.",
                              "Kolonistler +%5 kesici zırh kazanır ama %3 daha yavaş yürür. Scutum sergisini açar."))
R_MANUBALLISTA = research(NATION, "Manuballista", "manuballista", "manuballista",
                          "A hand-held torsion crossbow that throws heavy iron bolts.",
                          "Ağır demir oklar fırlatan, elde taşınan burulmalı arbalet.",
                          1200, "Medieval", 1, 3, prereqs=[R_PILUM], knowledge=30)
R_DRILL = research(NATION, "Drill", "legion drill", "lejyon talimi",
                   "Endless practice with wooden swords twice as heavy as real ones. When the real fight comes, every thrust lands.",
                   "Gerçeklerinin iki katı ağır tahta kılıçlarla bitmeyen talim. Gerçek dövüş geldiğinde her hamle yerini bulur.",
                   1300, "Medieval", 2, 3, prereqs=[R_ENGINEERS], knowledge=35, tradition=True,
                   stats=[("MeleeHitChance", 2, 1, "Colonists")],
                   effect=T("Colonists gain +2 melee hit chance.", "Kolonistler +2 yakın dövüş isabeti kazanır."))
R_PAX = research(NATION, "Pax", "pax romana", "pax romana",
                 "Peace through law, trade and the quiet threat of the legions. Nova Roma's envoys are listened to.",
                 "Hukuk, ticaret ve lejyonların sessiz tehdidiyle gelen barış. Nova Roma elçileri dinlenir.",
                 1600, "Medieval", 1, 4, prereqs=[R_SENATE, R_ROADS], knowledge=45, tradition=True,
                 stats=[("NegotiationAbility", 0.10, 1, "Colonists"), ("SocialImpact", 0.05, 1, "Colonists")],
                 effect=T("Colonists gain +10% negotiation ability and +5% social impact.",
                          "Kolonistler +%10 müzakere yeteneği ve +%5 sosyal etki kazanır."))

# ------------------------------------------------------------------ weapons and armour
BOLT = projectile("HE_Bolt_Manuballista", "manuballista bolt", "manuballista oku", "Arrow", 17, 52, "Things/Projectile/Arrow_Small", pen=0.32)
ranged(NATION, "Manuballista", "manuballista", "manuballista",
       "A torsion crossbow small enough for one soldier. It is slow to wind but its iron bolt hits like a thrown pilum.",
       "Tek bir askerin taşıyabileceği kadar küçük bir burulmalı arbalet. Kurması yavaştır ama demir oku fırlatılmış bir pilum gibi çarpar.",
       "Medieval", R_MANUBALLISTA, BOLT, 2.0, 26.9, 2.2, (0.7, 0.8, 0.74, 0.6), 3.2, 16000, "crossbow",
       {"WoodLog": 40, "Steel": 30}, users=SMITHY, skill=5)
apparel(NATION, "Lorica", "lorica segmentata", "lorica segmentata",
        "Overlapping iron bands laced over a leather harness. It turns blades well, though the wearer walks a little slower.",
        "Deri bir koşum üzerine bağlanmış, üst üste binen demir şeritler. Kılıçları iyi savuşturur, ama giyen biraz daha yavaş yürür.",
        "Medieval", R_LORICA, "PlateArmor/PlateArmor", ["Middle"], ["Torso", "Neck", "Shoulders", "Arms"],
        {"MaxHitPoints": 240, "StuffEffectMultiplierArmor": 0.82, "StuffEffectMultiplierInsulation_Cold": 0.5, "StuffEffectMultiplierInsulation_Heat": 0},
        "torso", parent="ArmorSmithableBase", stuff=("Metallic",), stuff_count=120, work=24000, mass=9, users=SMITHY, skill=6,
        equipped={"MoveSpeed": -0.3}, tags=["MedievalMilitary"], pargs={"kind": "lorica"})
apparel(NATION, "Galea", "galea", "galea",
        "A bronze-trimmed legionary helmet with wide cheek guards and a red horsehair crest.",
        "Geniş yanak siperlikli, kırmızı at kılı sorguçlu, bronz süslü bir lejyoner miğferi.",
        "Medieval", R_LORICA, "SimpleHelmet/SimpleHelmet", ["Overhead"], ["UpperHead"],
        {"MaxHitPoints": 110, "StuffEffectMultiplierArmor": 0.55, "StuffEffectMultiplierInsulation_Cold": 0.15, "StuffEffectMultiplierInsulation_Heat": 0},
        "helmet", parent="ArmorHelmetMakeableBase", stuff=("Metallic",), stuff_count=45, work=3600, mass=2, users=SMITHY, skill=5, head=True,
        equipped={"SocialImpact": 0.02}, pargs={"kind": "galea"})
apparel(NATION, "Tunica", "tunica", "tunica",
        "A knee-length wool tunic with a narrow border, belted at the waist. Every citizen owns two.",
        "Dar kenar şeritli, belden kuşaklı, diz boyu yün tunika. Her yurttaşın iki tane vardır.",
        "Neolithic", R_LORICA, "ShirtBasic/ShirtBasic", ["OnSkin"], ["Torso", "Shoulders"],
        {"MaxHitPoints": 110, "StuffEffectMultiplierArmor": 0.2, "StuffEffectMultiplierInsulation_Cold": 0.3, "StuffEffectMultiplierInsulation_Heat": 0.15},
        "torso", stuff_count=45, work=1800, mass=0.3, pargs={"kind": "tunica"})

# ------------------------------------------------------------------ buildings and floors
deco(NATION, "ScutumDisplay", "scutum display", "scutum sergisi",
     "A curved legionary shield painted with golden wings, hung on a stand. Veterans touch it for luck before a battle.",
     "Altın kanatlarla boyanmış, bir sehpaya asılmış kavisli lejyoner kalkanı. Kıdemliler savaştan önce şans için ona dokunur.",
     R_TESTUDO, (1, 1), "wall_shield", beauty=6, work=2000, stuff=("Woody",), stuff_count=35, cost={"Steel": 10}, hp=100,
     category="Art", pargs={"kind": "scutum"})
deco(NATION, "Statue", "forum statue", "forum heykeli",
     "A marble statue of a toga-clad citizen raising a golden laurel. It makes any square feel like a forum.",
     "Altın bir defne dalı kaldıran togalı bir yurttaşın mermer heykeli. Her meydanı bir forum gibi hissettirir.",
     R_FORUM, (1, 1), "statue", beauty=28, work=9000, stuff=("Stony",), stuff_count=140, hp=300, fill=0.5,
     category="Art", draw_size="(1.2,1.8)", pargs={"kind": "forum"})
deco(NATION, "Triclinium", "triclinium table", "triclinium masası",
     "A low marble dining table covered with a red cloth, set for wine, olives and long conversations.",
     "Kırmızı örtülü, şarap, zeytin ve uzun sohbetler için kurulmuş alçak bir mermer yemek masası.",
     R_FORUM, (2, 2), "table", beauty=4, work=2400, stuff=("Stony", "Woody"), stuff_count=70, hp=150,
     parent="TableGatherSpotBase", passability="PassThroughOnly", fill=0.4, extra={"building": None},
     pargs={"kind": "triclinium"})
deco(NATION, "Thermae", "thermae pool", "thermae havuzu",
     "A heated marble bathing pool. Colonists come here to soak, talk and let their worries drift away.",
     "Isıtmalı bir mermer yıkanma havuzu. Kolonistler buraya suya girmeye, sohbet etmeye ve dertlerini unutmaya gelir.",
     R_THERMAE, (3, 2), "bath", beauty=12, work=12000, stuff=("Stony",), stuff_count=220, hp=600,
     passability="PassThroughOnly", fill=0.2, minify=False, joy="Meditative", pargs={"kind": "thermae"})
floor(NATION, "Mosaic", "Roman mosaic", "Roma mozaiği",
      "Thousands of small stone tesserae set in a geometric pattern with a red border.",
      "Kırmızı bir kenarlıkla geometrik bir desene dizilmiş binlerce küçük taş tessera.",
      R_THERMAE, "floor_mosaic", beauty=3, cost={"BlocksMarble": 3}, work=1800)

# ------------------------------------------------------------------ food and trade goods
food(NATION, "Puls", "puls", "puls",
     "A thick porridge of grain and beans with olive oil and herbs. The legions marched on it for centuries.",
     "Zeytinyağı ve otlarla yapılmış koyu bir tahıl ve fasulye lapası. Lejyonlar yüzyıllarca onunla yürüdü.",
     R_GARUM, "bowl", nutrition=0.9, value=20, pargs={"kind": "puls"})
resource(NATION, "Garum", "garum amphora", "garum amforası",
         "A sealed clay amphora of garum, the fermented fish sauce of Nova Roma. Prized by traders and cooks across the world.",
         "Nova Roma'nın fermente balık sosu garumla dolu, mühürlü bir kil amfora. Dünyanın dört bir yanındaki tüccar ve aşçılar tarafından aranır.",
         14, "jar", mass=1.2, stack=25, pargs={"kind": "amphora"})
