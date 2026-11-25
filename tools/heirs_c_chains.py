"""1.0 story chains: The Lost Eagle (Nova Roma), The Broken Dynasty (Yamato) and Winter Rite (Nordheim).

Each chain has five steps, a lost relic found at a story site, a final choice, an artifact and a capstone
tradition that only opens when the story is finished.
"""
from heirs_data import add, key, tex
from heirs_kit import culture, research, tool
from heirs_xml import Def, T

F = "Chains/HE_Chains.xml"
FI = "Chains/HE_ChainItems.xml"

key("HE_ArtifactCooldown", "Resting: ready again in {0}.", "Dinleniyor: {0} sonra yeniden hazır.")
key("HE_ArtifactReady", "Ready to use.", "Kullanıma hazır.")
key("HE_ArtifactUsed", "{0} used {1}: {2} allies rallied, {3} enemies fled.", "{0}, {1} kullandı: {2} müttefik coştu, {3} düşman kaçtı.")

add(FI, Def("HediffDef", "HE_Rallied", label=T("rallied", "coşkulu"),
            description=T("Inspired by an ancient artifact. Fights harder, feels less pain and keeps a steadier mind.",
                          "Kadim bir eserden ilham almış. Daha sert dövüşür, daha az acı duyar ve zihnini daha sağlam tutar."),
            hediffClass="HediffWithComps", isBad=False, defaultLabelColor="(0.95, 0.80, 0.40)",
            comps=[{"@Class": "HediffCompProperties_Disappears", "disappearsAfterTicks": "60000~60000", "showRemainingTime": True}],
            stages=[{"painFactor": 0.8, "statOffsets": {"MeleeHitChance": 3, "ShootingAccuracyPawn": 3, "MentalBreakThreshold": -0.05}}]))


def item(name, en, tr, den, dtr, painter, value, mass, nation, comps=None, pargs=None, beauty=0):
    add(FI, Def("ThingDef", name, label=T(en, tr), description=T(den, dtr),
                thingClass="ThingWithComps", category="Item", drawerType="MapMeshOnly", altitudeLayer="Item",
                useHitPoints=True, selectable=True, alwaysHaulable=True, rotatable=False, pathCost=14, stackLimit=1,
                tradeability="None", healthAffectsPrice=False,
                graphicData={"texPath": f"HeirsOfEarth/Items/{name}", "graphicClass": "Graphic_Single"},
                statBases={"MaxHitPoints": 250, "MarketValue": value, "Mass": mass, "Flammability": 0, "DeteriorationRate": 0, "Beauty": beauty},
                thingCategories=["Manufactured"],
                comps=[{"@Class": "CompProperties_Forbiddable"}] + list(comps or [])))
    tex(f"HeirsOfEarth/Items/{name}", painter, **(pargs or {}))
    return name


def usable(label_en, label_tr, weather=None, flee=0.0, cooldown=10, sound=None, goodwill=0, caravan=False):
    return [{"@Class": "CompProperties_Usable", "useJob": "UseItem", "useLabel": T(label_en, label_tr), "useDuration": 180},
            {"@Class": "HeirsOfEarth.CompProperties_HeirsArtifact", "allyHediff": "HE_Rallied", "fleeChance": flee or None,
             "weather": weather, "cooldownDays": cooldown, "sound": sound, "goodwill": goodwill or None, "callCaravan": True if caravan else None}]


# ------------------------------------------------------------------ relics found at the story sites
LOST_EAGLE = item("HE_Roma_LostEagle", "tarnished eagle", "kararmış kartal",
                  "The bronze eagle of the Ninth Legion, lost with its cohort generations ago. One wing is cracked, the gilding is almost gone, but every Nova Roman would know it at a glance.",
                  "Kuşaklar önce kohortuyla birlikte kaybolan Dokuzuncu Lejyon'un bronz kartalı. Bir kanadı çatlak, yaldızı neredeyse silinmiş, ama her Nova Romalı onu bir bakışta tanır.",
                  "relic", 800, 3, "HE_Roma", pargs={"kind": "eagle"}, beauty=10)
REGALIA = item("HE_Yamato_Regalia", "sacred mirror", "kutsal ayna",
               "A bronze mirror on a silk cushion, one of the regalia of the lost imperial line. Whoever holds it may name the true heir.",
               "İpek bir yastık üzerinde duran bronz bir ayna; kayıp imparatorluk soyunun hükümranlık eşyalarından biri. Onu elinde tutan, gerçek varisi ilan edebilir.",
               "relic", 800, 2, "HE_Yamato", pargs={"kind": "regalia"}, beauty=12)
BARROW_HORN = item("HE_Nord_BarrowHorn", "barrow horn", "höyük boynuzu",
                   "An iron-bound horn taken from a frozen grave mound. Frost never melts from it, and the old songs say it can call the storm.",
                   "Donmuş bir mezar höyüğünden alınmış, demir bilezikli bir boynuz. Üzerindeki kırağı hiç erimez; eski şarkılar onun fırtınayı çağırabildiğini söyler.",
                   "relic", 800, 2, "HE_Nord", pargs={"kind": "horn"}, beauty=6)

# ------------------------------------------------------------------ artifacts
EAGLE = item("HE_Roma_Artifact_Eagle", "Eagle Standard", "Kartal Sancağı",
             "The restored eagle of the Ninth Legion on a red standard. When it is raised, every colonist nearby fights as if the whole legion stood behind them. It must rest for ten days between uses.",
             "Kırmızı bir sancağın tepesinde, onarılmış Dokuzuncu Lejyon kartalı. Kaldırıldığında yakındaki her kolonist sanki bütün lejyon arkasındaymış gibi dövüşür. Her kullanımdan sonra on gün dinlenmesi gerekir.",
             "eagle_standard", 3500, 4, "HE_Roma", comps=usable("Raise the eagle", "Kartalı kaldır", flee=0.15, cooldown=10, sound="HE_Sound_Bugle"), beauty=30)
HORN = item("HE_Nord_Artifact_StormHorn", "Storm Horn", "Fırtına Boynuzu",
            "The barrow horn, awakened. Its call rallies your people, sends many enemies running and pulls a thunderstorm out of a clear sky. It must rest for twelve days between uses.",
            "Uyanmış höyük boynuzu. Sesi halkını coşturur, birçok düşmanı kaçırır ve açık gökten bir gök gürültülü fırtına çeker. Her kullanımdan sonra on iki gün dinlenmesi gerekir.",
            "storm_horn", 3500, 2, "HE_Nord", comps=usable("Blow the horn", "Boynuzu üfle", weather="RainyThunderstorm", flee=0.5, cooldown=12, sound="HE_Sound_Horn"), beauty=15)
SKY_SWORD = "HE_Yamato_Artifact_SkySword"
add(FI, Def("ThingDef", SKY_SWORD, parent="BaseMeleeWeapon_Sharp_Quality",
            label=T("Sky Sword", "Gök Kılıcı"),
            description=T("The sword of the first shogun, forged, it is said, from iron that fell from the sky. Its blade is faintly blue and never dulls. In any hand it is a masterpiece; in a trained hand it is a legend.",
                          "Söylendiğine göre gökten düşen demirden dövülmüş ilk şogunun kılıcı. Ağzı belli belirsiz mavidir ve hiç körelmez. Her elde bir şaheserdir; eğitimli bir elde ise bir efsane."),
            techLevel="Medieval", tradeability="None", smeltable=False, relicChance=0, recipeMaker={"@IsNull": "True"},
            graphicData={"texPath": f"HeirsOfEarth/Weapons/{SKY_SWORD}", "graphicClass": "Graphic_Single"},
            uiIconScale=1.1, equippedAngleOffset=-45,
            statBases={"Mass": 1.1, "MarketValue": 4000, "MaxHitPoints": 400, "DeteriorationRate": 0},
            equippedStatOffsets={"MeleeHitChance": 4, "MeleeDodgeChance": 4},
            tools=[tool("handle", "Blunt", 9, 2), tool("point", "Stab", 20, 1.8, 0.40), tool("edge", "Cut", 24, 1.7, 0.45)]))
tex(f"HeirsOfEarth/Weapons/{SKY_SWORD}", "sky_sword")


# ------------------------------------------------------------------ chains
def things(**kw):
    """ThingDefCountClass lists load from the short form <Steel>200</Steel>."""
    return dict(kw)


def step(kind, en, tr, ten, ttr, den=None, dtr=None, **fields):
    s = {"kind": kind, "label": T(en, tr), "text": T(ten, ttr)}
    if den:
        s["doneText"] = T(den, dtr)
    s.update(fields)
    return s


def option(en, tr, ten, ttr, goodwill=0, knowledge=0, keep=True, rewards=None, takes=None):
    return {"label": T(en, tr), "text": T(ten, ttr), "goodwill": goodwill or None, "knowledge": knowledge or None,
            "keepArtifact": keep, "rewards": rewards, "takes": takes}


add(F, Def("HeirsOfEarth.ChainDef", "HE_Chain_Roma", nation="HE_Roma", artifact=EAGLE, startKnowledge=60,
           label=T("The Lost Eagle", "Kayıp Kartal"),
           description=T("The eagle of the Ninth Legion was lost in the north generations ago. Find it, and decide whose glory it serves.",
                         "Dokuzuncu Lejyon'un kartalı kuşaklar önce kuzeyde kayboldu. Onu bul ve kimin şanına hizmet edeceğine karar ver."),
           startText=T("A dying veteran reaches your colony with a map scratched on a shield. He swears he knows where the eagle of the Ninth Legion fell. The senate would pay dearly for it, and so would its enemies.",
                       "Ölmek üzere olan bir kıdemli asker, bir kalkanın üzerine kazınmış haritayla kolonine ulaşır. Dokuzuncu Lejyon'un kartalının nerede düştüğünü bildiğine yemin eder. Senato onun için çok para öder; düşmanları da öyle."),
           endText=T("The story of the lost eagle is told in every forum of Nova Roma, and your colony's name is part of it.",
                     "Kayıp kartalın hikâyesi Nova Roma'nın her forumunda anlatılıyor ve koloninin adı da bu hikâyenin bir parçası."),
           steps=[
               step("Deliver", "Arm an expedition", "Bir sefer donat",
                    "An expedition into the north needs iron and good swords. Gather 200 steel and 4 gladii, then deliver them from the Stories page.",
                    "Kuzeye bir sefer demir ve iyi kılıçlar ister. 200 çelik ve 4 gladius topla, sonra Hikâyeler sayfasından teslim et.",
                    "The smiths have done their work. Now the expedition needs a standard to march under.",
                    "Demirciler işini yaptı. Şimdi seferin altında yürüyeceği bir sancak gerekiyor.",
                    things=things(Steel=200, HE_Roma_Gladius=4)),
               step("Build", "Raise a standard", "Bir sancak dik",
                    "No legion marches without its colours. Build a legion standard in your colony.",
                    "Hiçbir lejyon sancağı olmadan yürümez. Kolonine bir lejyon sancağı inşa et.",
                    "The standard flies, and word of your expedition spreads. Not everyone is pleased.",
                    "Sancak dalgalanıyor ve seferinin haberi yayılıyor. Herkes bundan hoşnut değil.",
                    building="HE_Roma_Standard"),
               step("Raid", "Hold the colony", "Koloniyi savun",
                    "The northern clans would rather see the eagle stay buried. Expect an attack within a day and drive it off.",
                    "Kuzey klanları kartalın gömülü kalmasını yeğler. Bir gün içinde bir saldırı bekle ve onu püskürt.",
                    "The attackers are beaten. Among their dead you find a sketch of a ruined fort: the eagle is there.",
                    "Saldırganlar yenildi. Ölülerinin arasında yıkık bir kalenin çizimini buluyorsun: kartal orada.",
                    enemy="HE_Nord", points=700),
               step("Site", "The ruined fort", "Yıkık kale",
                    "Send a caravan to the ruined fort marked on the world map, defeat its guards and bring the tarnished eagle home.",
                    "Dünya haritasında işaretli yıkık kaleye bir kervan gönder, muhafızlarını yen ve kararmış kartalı eve getir.",
                    "The eagle is in your hands. Broken, tarnished, and still the most valuable thing your colony owns.",
                    "Kartal artık senin elinde. Kırık, kararmış ve yine de koloninin sahip olduğu en değerli şey.",
                    enemy="HE_Nord", siteLayout="Ruin", siteWall="BlocksSandstone", siteProp="HE_Roma_ScutumDisplay",
                    siteReward=LOST_EAGLE, siteThreat=1.0),
               step("Choice", "The fate of the eagle", "Kartalın kaderi",
                    "Messengers of the senate ask for the eagle to be returned to the capital, where it belongs. Your colonists would rather restore it and keep it here, under your own banner.",
                    "Senatonun habercileri kartalın ait olduğu başkente geri verilmesini istiyor. Kolonistlerin ise onu onarıp burada, kendi sancağının altında tutmayı yeğliyor.",
                    options=[
                        option("Return it to the senate", "Senatoya geri ver",
                               "The senate honours your colony and opens its archives to you.", "Senato koloniyi onurlandırır ve arşivlerini sana açar.",
                               goodwill=40, knowledge=40, keep=False, rewards=things(Silver=600), takes=things(HE_Roma_LostEagle=1)),
                        option("Restore it and keep it", "Onar ve sakla",
                               "Your smiths restore the eagle on a new standard. The senate will not forget this.", "Demircilerin kartalı yeni bir sancak üzerinde onarır. Senato bunu unutmayacak.",
                               goodwill=-30, keep=True, takes=things(HE_Roma_LostEagle=1)),
                    ]),
           ]))

add(F, Def("HeirsOfEarth.ChainDef", "HE_Chain_Yamato", nation="HE_Yamato", artifact=SKY_SWORD, startKnowledge=60,
           label=T("The Broken Dynasty", "Kırık Hanedan"),
           description=T("The imperial line of Yamato ended in a night of fire. A sacred mirror and a sword survived. Find them, and decide who rules.",
                         "Yamato'nun imparatorluk soyu bir ateş gecesinde sona erdi. Kutsal bir ayna ve bir kılıç kurtuldu. Onları bul ve kimin yöneteceğine karar ver."),
           startText=T("A wandering monk arrives with news: the regalia of the old emperors are hidden in a mountain shrine, guarded by men who serve no lord. The clans whisper that whoever finds them will choose the next emperor.",
                       "Gezgin bir keşiş bir haberle gelir: eski imparatorların hükümranlık eşyaları, hiçbir efendiye hizmet etmeyen adamların koruduğu bir dağ tapınağında saklı. Klanlar, onları bulanın bir sonraki imparatoru seçeceğini fısıldıyor."),
           endText=T("Whatever you chose, the clans of Yamato now speak of your colony with respect, and with some fear.",
                     "Ne seçmiş olursan ol, Yamato klanları artık kolonin hakkında saygıyla ve biraz da korkuyla konuşuyor."),
           steps=[
               step("Deliver", "Gifts for the shrine", "Tapınak için armağanlar",
                    "A pilgrim does not arrive empty-handed. Gather 30 fine meals and 100 cloth for the shrine keepers, then deliver them from the Stories page.",
                    "Bir hacı eli boş gelmez. Tapınak bekçileri için 30 kaliteli yemek ve 100 kumaş topla, sonra Hikâyeler sayfasından teslim et.",
                    "The keepers accept your gifts and tell you more: the guards of the shrine can only be faced with a blade folded by your own smiths.",
                    "Bekçiler armağanlarını kabul eder ve sana daha fazlasını anlatır: tapınağın muhafızlarıyla ancak kendi demircilerinin katladığı bir kılıçla yüzleşilebilir.",
                    things=things(MealFine=30, Cloth=100)),
               step("Research", "Fold the steel", "Çeliği katla",
                    "Learn the forged folds tradition so your smiths can make blades worthy of the task.",
                    "Demircilerinin bu işe layık kılıçlar yapabilmesi için katlanmış dövme geleneğini öğren.",
                    "Your smiths have mastered the folds. A challenger has heard of it and is coming.",
                    "Demircilerin katlama sanatında ustalaştı. Bunu duyan bir meydan okuyucu geliyor.",
                    project="HE_Yamato_Folds"),
               step("Raid", "The challenger", "Meydan okuyan",
                    "A band of ronin led by a famous swordsman wants to test your colony. Defeat them.",
                    "Ünlü bir kılıç ustasının önderlik ettiği bir ronin çetesi kolonini sınamak istiyor. Onları yen.",
                    "The challenger falls. Before dying he tells you the way to the mountain shrine.",
                    "Meydan okuyan düşer. Ölmeden önce sana dağ tapınağının yolunu söyler.",
                    points=450),
               step("Site", "The mountain shrine", "Dağ tapınağı",
                    "Send a caravan to the mountain shrine marked on the world map, defeat its guards and bring the sacred mirror home.",
                    "Dünya haritasında işaretli dağ tapınağına bir kervan gönder, muhafızlarını yen ve kutsal aynayı eve getir.",
                    "The mirror is yours, and beneath it, wrapped in old silk, lies the Sky Sword of the first shogun.",
                    "Ayna artık senin; altında, eski ipeğe sarılı olarak ilk şogunun Gök Kılıcı yatıyor.",
                    siteLayout="Hall", siteWall="WoodLog", siteProp="HE_Yamato_Lantern", siteReward=REGALIA, siteThreat=1.0),
               step("Choice", "Who will rule?", "Kim yönetecek?",
                    "The clans wait for your word. You can give the mirror and the sword to the young heir the monks have hidden, or keep the sword for your own house.",
                    "Klanlar senin sözünü bekliyor. Aynayı ve kılıcı keşişlerin sakladığı genç varise verebilir ya da kılıcı kendi hanen için saklayabilirsin.",
                    options=[
                        option("Restore the heir", "Varisi tahta çıkar",
                               "The heir is crowned. The shogunate is grateful and shares the secrets of its scholars.", "Varis taç giyer. Şogunluk minnettardır ve âlimlerinin sırlarını seninle paylaşır.",
                               goodwill=40, knowledge=40, keep=False, rewards=things(Gold=40), takes=things(HE_Yamato_Regalia=1)),
                        option("Take the sword", "Kılıcı al",
                               "You return the mirror but keep the Sky Sword. The clans call it theft; your colonists call it fate.", "Aynayı geri verirsin ama Gök Kılıcı'nı saklarsın. Klanlar buna hırsızlık der; kolonistlerin ise kader.",
                               goodwill=-30, keep=True, takes=things(HE_Yamato_Regalia=1)),
                    ]),
           ]))

add(F, Def("HeirsOfEarth.ChainDef", "HE_Chain_Nord", nation="HE_Nord", artifact=HORN, startKnowledge=60,
           label=T("Winter Rite", "Kış Ayini"),
           description=T("Every hundred winters the jarls of Nordheim must open the ice barrow of their first king. This winter, the rite falls to you.",
                         "Her yüz kışta bir, Nordheim jarlları ilk krallarının buz höyüğünü açmak zorundadır. Bu kış ayin sana düşüyor."),
           startText=T("A skald arrives through the snow: the old jarl is dead, and the winter rite must be done before a new one can be chosen. The people of Nordheim ask your colony to prepare the feast and open the barrow.",
                       "Bir skald karın içinden gelir: yaşlı jarl öldü ve yenisi seçilmeden önce kış ayini yapılmalı. Nordheim halkı, kolonine şöleni hazırlamasını ve höyüğü açmasını rica ediyor."),
           endText=T("The rite is done. The skalds will sing of it for a hundred winters, until the barrow must be opened again.",
                     "Ayin tamamlandı. Skaldlar, höyüğün yeniden açılması gereken yüz kış boyunca onu şarkılarında anlatacak."),
           steps=[
               step("Deliver", "The winter feast", "Kış şöleni",
                    "The rite begins with a feast and warm gifts for the mourners. Gather 60 pemmican and 80 plain leather, then deliver them from the Stories page.",
                    "Ayin bir şölenle başlar. 60 pemmikan ve 80 düz deri topla, sonra Hikâyeler sayfasından teslim et.",
                    "The feast is ready. Now the dead need a stone to remember them by.",
                    "Şölen hazır. Şimdi ölülerin anılacağı bir taş gerekiyor.",
                    things=things(Pemmican=60, Leather_Plain=80)),
               step("Build", "Carve the stone", "Taşı oy",
                    "Build a rune stone in your colony to honour the dead king.",
                    "Ölü kralı onurlandırmak için kolonine bir run taşı inşa et.",
                    "The runes are cut. That night the wind turns, and the cold comes down from the mountains.",
                    "Runlar kazındı. O gece rüzgâr döner ve soğuk dağlardan iner.",
                    building="HE_Nord_RuneStone"),
               step("Raid", "Survive the long night", "Uzun geceyi atlat",
                    "A cold snap grips the land, and Roman scouts use it to strike before the rite is done. Survive the cold and drive off the attack.",
                    "Bir soğuk dalgası toprakları sarar ve Romalı keşifçiler bunu ayin bitmeden saldırmak için kullanır. Soğuğa dayan ve saldırıyı püskürt.",
                    "The long night is over. The way to the ice barrow is open.",
                    "Uzun gece sona erdi. Buz höyüğünün yolu açık.",
                    enemy="HE_Roma", points=650, condition="ColdSnap", conditionDays=4),
               step("Site", "The ice barrow", "Buz höyüğü",
                    "Send a caravan to the ice barrow marked on the world map, defeat the grave robbers and bring the barrow horn home.",
                    "Dünya haritasında işaretli buz höyüğüne bir kervan gönder, mezar soyguncularını yen ve höyük boynuzunu eve getir.",
                    "The horn is yours. Frost spreads across your fingers when you hold it.",
                    "Boynuz artık senin. Onu tuttuğunda kırağı parmaklarına yayılıyor.",
                    enemy="HE_Roma", siteLayout="Ring", siteWall="BlocksMarble", siteProp="HE_Nord_RuneStone", siteReward=BARROW_HORN, siteThreat=1.0),
               step("Choice", "The horn's voice", "Boynuzun sesi",
                    "The new jarl asks for the horn, as the rite demands. Your colonists want to blow it themselves and wake its power.",
                    "Yeni jarl, ayinin gerektirdiği gibi boynuzu istiyor. Kolonistlerin ise onu kendileri üfleyip gücünü uyandırmak istiyor.",
                    options=[
                        option("Give it to the jarl", "Jarla ver",
                               "The jarl takes the horn and names your colony a friend of Nordheim.", "Jarl boynuzu alır ve kolonini Nordheim'ın dostu ilan eder.",
                               goodwill=40, knowledge=40, keep=False, rewards=things(Silver=600), takes=things(HE_Nord_BarrowHorn=1)),
                        option("Blow it now", "Hemen üfle",
                               "Thunder answers the horn. It is yours now, and the jarl will not forget it.", "Boynuza gök gürültüsü cevap verir. Artık senin; jarl bunu unutmayacak.",
                               goodwill=-30, keep=True, takes=things(HE_Nord_BarrowHorn=1)),
                    ]),
           ]))

# ------------------------------------------------------------------ capstone traditions that open when the story ends
research("Roma", "Aquila", "the eagle's pride", "kartalın gururu",
         "With the eagle found, every citizen stands a little taller.",
         "Kartal bulunduğundan beri her yurttaş biraz daha dik duruyor.",
         1800, "Medieval", 1, 5, prereqs=["HE_Roma_Pax"], knowledge=50, tradition=True, chain="HE_Chain_Roma",
         stats=[("MeleeHitChance", 2, 1, "Colonists"), ("ShootingAccuracyPawn", 1, 1, "Colonists"), ("MentalBreakThreshold", -0.02, 1, "Colonists")],
         effect=T("Colonists gain +2 melee hit chance, +1 shooting accuracy and a 2% lower mental break threshold.",
                  "Kolonistler +2 yakın dövüş isabeti, +1 atış isabeti kazanır ve zihinsel çöküş eşikleri %2 düşer."))
research("Yamato", "Mandate", "mandate of heaven", "göğün buyruğu",
         "The rightful order is restored, and the people of Yamato work and study with calm hearts.",
         "Haklı düzen yeniden kuruldu; Yamato halkı sakin yüreklerle çalışıp öğreniyor.",
         1800, "Medieval", 1, 4, prereqs=["HE_Yamato_MasterCraft"], knowledge=50, tradition=True, chain="HE_Chain_Yamato",
         stats=[("GlobalLearningFactor", 0.05, 1, "Colonists"), ("MentalBreakThreshold", -0.03, 1, "Colonists")],
         effect=T("Colonists learn 5% faster and their mental break threshold drops by 3%.",
                  "Kolonistler %5 daha hızlı öğrenir ve zihinsel çöküş eşikleri %3 düşer."))
research("Nord", "Valhalla", "road to Valhalla", "Valhalla yolu",
         "Those who have seen the winter rite no longer fear death, only a dull one.",
         "Kış ayinini görenler artık ölümden korkmaz, yalnızca sıradan bir ölümden korkar.",
         1800, "Medieval", 1, 3, prereqs=["HE_Nord_Berserk"], knowledge=50, tradition=True, chain="HE_Chain_Nord",
         stats=[("PainShockThreshold", 0.08, 1, "Colonists"), ("MeleeHitChance", 1, 1, "Colonists")],
         effect=T("Colonists gain +8% pain shock threshold and +1 melee hit chance.",
                  "Kolonistler +%8 acı şoku eşiği ve +1 yakın dövüş isabeti kazanır."))
