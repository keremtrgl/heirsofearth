"""Heirs of Earth 3.0b: trade routes (HeirsRoutes.cs) - the texts of the Routes section, its letters and its setting."""
from heirs_data import key

for k, en, tr in [
    ("HE_TabRoutes", "Trade routes", "Ticaret yolları"),
    ("HE_RoutesIntro",
     "Open a trade road to a nation that likes you (goodwill {0} or more) by paying silver once. Every {1} days a route caravan "
     "brings that nation's goods and silver worth {2} of what the road cost, raises relations a little and teaches you something "
     "of their culture. A nation at war may lose a caravan to raiders. If the nation turns hostile or collapses, the road closes.",
     "Seni seven bir devlete (ilişki {0} ve üstü) bir kez gümüş ödeyerek ticaret yolu aç. Her {1} günde bir yol kervanı o devletin "
     "mallarını ve gümüşünü getirir; değeri yolun bedelinin {2} kadarıdır. Her sefer ilişkiyi biraz artırır ve o kültürden bir şeyler "
     "öğretir. Savaştaki bir devletin kervanı yolda yağmalanabilir. Devlet sana düşman olursa ya da çökerse yol kapanır."),
    ("HE_RoutesOpen", "Open roads: {0} / {1}", "Açık yollar: {0} / {1}"),
    ("HE_RoutesNone", "You have no trade roads yet.", "Henüz hiç ticaret yolun yok."),
    ("HE_RoutesAvailable", "Nations", "Devletler"),
    ("HE_RouteInfo", "next caravan in {0} days · worth {1} silver · {2} trips, {3} raided",
     "sonraki kervan {0} gün sonra · {1} gümüş değerinde · {2} sefer, {3} yağma"),
    ("HE_RouteWarRisk", "At war: caravans may be raided.", "Savaşta: kervanlar yağmalanabilir."),
    ("HE_RouteOffer", "costs {0} silver · {1} tiles away · relations {2}", "bedel {0} gümüş · {1} kare uzakta · ilişki {2}"),
    ("HE_RouteOpen", "Open the road", "Yolu aç"),
    ("HE_RouteClose", "Close the road", "Yolu kapat"),
    ("HE_RouteCloseConfirm", "Close the trade road to {0}? The silver you paid is not returned.",
     "{0} ile ticaret yolu kapatılsın mı? Ödediğin gümüş geri verilmez."),
    ("HE_RouteDisabled", "Trade routes are turned off in the mod settings.", "Ticaret yolları mod ayarlarında kapalı."),
    ("HE_RouteNoNation", "this nation is gone", "bu devlet artık yok"),
    ("HE_RouteAlreadyOpen", "already open", "zaten açık"),
    ("HE_RouteHostile", "hostile to you", "sana düşman"),
    ("HE_RouteGoodwill", "needs relations {0}", "{0} ilişki gerekir"),
    ("HE_RouteNoSettlement", "no settlement to trade with", "ticaret yapılacak yerleşim yok"),
    ("HE_RouteFull", "at most {0} roads", "en fazla {0} yol"),
    ("HE_RouteOpenedChronicle", "A trade road to {0} was opened for {1} silver.", "{0} ile {1} gümüşe bir ticaret yolu açıldı."),
    ("HE_RouteTripLabel", "Road caravan from {0}", "{0} yol kervanı"),
    ("HE_RouteTripText",
     "The road caravan from {0} has arrived and unloaded near your trade spot: {1}.\n\nRelations with them rise by {2}. "
     "The next caravan is due in {3} days.",
     "{0} yol kervanı geldi ve yükünü ticaret noktanın yanına indirdi: {1}.\n\nOnlarla ilişkin {2} arttı. "
     "Sonraki kervan {3} gün sonra gelecek."),
    ("HE_RouteTripChronicle", "Caravan number {1} arrived on the road from {0}.", "{0} yolundan {1}. kervan geldi."),
    ("HE_RouteRaidedLabel", "Road caravan of {0} raided", "{0} yol kervanı yağmalandı"),
    ("HE_RouteRaidedText",
     "{0} is at war, and raiders fell on its road caravan before it reached you. Nothing arrives this time. The road stays open.",
     "{0} savaşta ve yağmacılar yol kervanına sana ulaşmadan saldırdı. Bu sefer hiçbir şey gelmiyor. Yol açık kalıyor."),
    ("HE_RouteClosedLabel", "Road to {0} closed", "{0} yolu kapandı"),
    ("HE_RouteClosedHostile", "{0} has turned hostile and closed its trade road to you.", "{0} sana düşman oldu ve ticaret yolunu kapattı."),
    ("HE_RouteClosedCollapse", "{0} has collapsed. Its trade road falls silent.", "{0} çöktü. Ticaret yolu sessizliğe gömüldü."),
    ("HE_RouteClosedByPlayer", "You closed the trade road to {0}.", "{0} ile ticaret yolunu kapattın."),
    ("HE_SettingsTradeRoutes", "Trade routes", "Ticaret yolları"),
    ("HE_SettingsTradeRoutesTip", "Lets you open trade roads to friendly nations in the Heirs tab. When off, open roads send no caravans.",
     "Mirasçılar sekmesinden dost devletlere ticaret yolu açmanı sağlar. Kapalıyken açık yollar kervan göndermez."),
]:
    key(k, en, tr)


# ------------------------------------------------------------------ 3.0c: the World Council
from heirs_data import add, tex  # noqa: E402
from heirs_kit import ERA_Y, NATION_X  # noqa: E402
from heirs_xml import Def, T  # noqa: E402

R_COUNCIL = "HE_WorldCouncil"
add("Research/HE_Research_Common.xml", Def(
    "ResearchProjectDef", R_COUNCIL,
    label=T("world council", "dünya konseyi"),
    description=T("A standing council where every heir nation sends a voice: one hall, one table, nine banners. From here the heirs can be "
                  "united by vote, or a single power can call them to swear fealty.\n\nOpens after you finish 3 nation stories, or keep "
                  "3 trade roads open for a year.",
                  "Her mirasçı devletin bir temsilci gönderdiği kalıcı bir konsey: tek salon, tek masa, dokuz sancak. Buradan mirasçılar "
                  "oylamayla birleştirilebilir ya da tek bir güç onları biat etmeye çağırabilir.\n\n3 devlet hikâyesini bitirince ya da "
                  "3 ticaret yolunu bir yıl açık tutunca açılır."),
    baseCost=3000, techLevel="Industrial", tab="HE_WorldHeritage",
    researchViewX=round(NATION_X["Common"] + 0.0, 2), researchViewY=round(ERA_Y["Industrial"], 2),
    prerequisites=["HE_Academy"],
    modExtensions=[{"@Class": "HeirsOfEarth.HeirsResearchExt", "council": True}]))

HALL = "HE_CouncilHall"
add("Things/HE_Buildings_Common.xml", Def(
    "ThingDef", HALL, parent="BuildingBase",
    label=T("council hall of the heirs", "mirasçılar konsey salonu"),
    description=T("A great round table of polished stone under a ring of nine banners, one for every heir nation, with a seat for each "
                  "envoy. Once it stands, you can call the World Council from the Heirs tab once per quadrum.",
                  "Cilalı taştan büyük, yuvarlak bir masa; çevresinde her mirasçı devlet için bir sancak ve her elçi için bir koltuk. "
                  "İnşa edildiğinde Mirasçılar sekmesinden mevsimde bir kez Dünya Konseyi'ni toplayabilirsin."),
    thingClass="Building",
    graphicData={"texPath": "HeirsOfEarth/Buildings/" + HALL, "graphicClass": "Graphic_Single", "drawSize": "(5,5)"},
    altitudeLayer="Building", passability="PassThroughOnly", pathCost=60, fillPercent=0.5,
    rotatable=False, size="(5,5)",
    stuffCategories=["Stony"], costStuffCount=400,
    costList={"Steel": 150, "Gold": 60, "Cloth": 120},
    statBases={"MaxHitPoints": 1200, "WorkToBuild": 40000, "Beauty": 40, "Flammability": 0},
    designationCategory="HE_Heritage",
    researchPrerequisites=[R_COUNCIL],
    constructionSkillPrerequisite=8,
    building={"isInert": True}))
tex("HeirsOfEarth/Buildings/" + HALL, "council_hall", size=(5, 5))

add("Core/HE_Letters.xml", Def("LetterDef", "HE_FealtyLetter", letterClass="HeirsOfEarth.ChoiceLetter_HeirsFealty",
                                color="(196, 160, 72)", flashColor="(220, 180, 80)", flashInterval=90))

for k, en, tr in [
    ("HE_TabCouncil", "World Council", "Dünya Konseyi"),
    ("HE_CouncilIntro",
     "The end goal of the heirs. The council opens after you finish {0} nation stories or keep {1} trade roads open for a full year. "
     "Then research the World Council and build its hall. Once per {3} days you can call a meeting.\n\n"
     "Unity: two thirds of the living nations vote yes. A nation votes yes if it is your ally, has sworn you fealty or likes you "
     "({2} relations or more), but says no if a nation it is at war with votes yes.\n"
     "Dominion: every living nation has sworn you fealty. A nation hostile to you that has lost half of its settlements offers fealty; "
     "a nation you wipe out collapses.\n\nAfter the victory the game goes on.",
     "Mirasçıların son hedefi. Konsey, {0} devlet hikâyesini bitirince ya da {1} ticaret yolunu tam bir yıl açık tutunca açılır. "
     "Sonra Dünya Konseyi'ni araştır ve salonunu inşa et. Her {3} günde bir toplantı çağırabilirsin.\n\n"
     "Birlik: yaşayan devletlerin üçte ikisi evet der. Bir devlet müttefikinse, sana biat ettiyse ya da seni seviyorsa ({2} ilişki ve üstü) "
     "evet der; ama savaşta olduğu bir devlet evet diyorsa hayır der.\n"
     "Hükümranlık: yaşayan her devlet sana biat etmiştir. Sana düşman olup yerleşimlerinin yarısını kaybeden bir devlet biat teklif eder; "
     "tamamen yok ettiğin bir devlet çöker.\n\nZaferden sonra oyun devam eder."),
    ("HE_CouncilDisabled", "The World Council is turned off in the mod settings.", "Dünya Konseyi mod ayarlarında kapalı."),
    ("HE_CouncilAlreadyWon", "the council has already decided", "konsey kararını çoktan verdi"),
    ("HE_CouncilLocked", "the council has not opened yet", "konsey henüz açılmadı"),
    ("HE_CouncilNeedHall", "build the council hall first", "önce konsey salonunu inşa et"),
    ("HE_CouncilWait", "next meeting possible in {0} days", "sonraki toplantı {0} gün sonra yapılabilir"),
    ("HE_CouncilProgress", "Road to the council", "Konseye giden yol"),
    ("HE_CouncilStepUnlock", "Council opened: {0}/{1} stories finished or {2}/{3} trade roads open for a year",
     "Konsey açıldı: {0}/{1} hikâye bitti ya da {2}/{3} ticaret yolu bir yıldır açık"),
    ("HE_CouncilStepHall", "Council hall built (research the World Council first)", "Konsey salonu inşa edildi (önce Dünya Konseyi'ni araştır)"),
    ("HE_CouncilCall", "Call the World Council", "Dünya Konseyi'ni topla"),
    ("HE_CouncilVotes", "How the nations would vote today", "Devletler bugün nasıl oy verirdi"),
    ("HE_CouncilSettlements", "{0} settlements", "{0} yerleşim"),
    ("HE_CouncilTally", "Yes votes: {0} of {1}. Unity needs {2}.", "Evet oyu: {0} / {1}. Birlik için {2} gerekir."),
    ("HE_CouncilDominion", "Nations sworn to you: {0} of {1}. Dominion needs all of them.",
     "Sana biat eden devletler: {0} / {1}. Hükümranlık için hepsi gerekir."),
    ("HE_CouncilWonNote", "The heirs of Earth have their answer. Your colony goes on; the world remembers.",
     "Dünya'nın mirasçıları cevabını buldu. Kolonin yaşamaya devam ediyor; dünya bunu unutmayacak."),
    ("HE_VoteYes", "Yes", "Evet"),
    ("HE_VoteNo", "No", "Hayır"),
    ("HE_VoteGone", "gone", "artık yok"),
    ("HE_VoteVassal", "has sworn you fealty", "sana biat etti"),
    ("HE_VoteAlly", "your ally", "müttefikin"),
    ("HE_VoteHostile", "hostile to you", "sana düşman"),
    ("HE_VoteGoodwill", "needs relations {0}, has {1}", "{0} ilişki gerekir, şu an {1}"),
    ("HE_VoteEnemyYes", "will not sit beside {0}, its enemy in war", "savaştaki düşmanı {0} ile aynı masaya oturmaz"),
    ("HE_VoteFriend", "trusts you (relations {0})", "sana güveniyor (ilişki {0})"),
    ("HE_NeedCouncil", "The World Council opens after {0} finished nation stories or {1} trade roads kept open for a year.",
     "Dünya Konseyi, {0} devlet hikâyesi bitince ya da {1} ticaret yolu bir yıl açık kalınca açılır."),
    ("HE_CouncilUnlockedLabel", "The World Council can gather", "Dünya Konseyi toplanabilir"),
    ("HE_CouncilUnlockedText",
     "Word of your colony has travelled along every road of this world. The heir nations now speak of a council where all of them would "
     "have a voice, and many expect you to call it.\n\nResearch the World Council, build the council hall and call the meeting from the "
     "Heirs tab. You can unite the heirs by vote, or make them swear fealty to you.",
     "Kolonin adı bu dünyanın bütün yollarında duyuldu. Mirasçı devletler artık hepsinin söz sahibi olacağı bir konseyden söz ediyor "
     "ve birçoğu onu senin toplamanı bekliyor.\n\nDünya Konseyi'ni araştır, konsey salonunu inşa et ve toplantıyı Mirasçılar sekmesinden "
     "çağır. Mirasçıları oylamayla birleştirebilir ya da sana biat ettirebilirsin."),
    ("HE_CouncilUnlockedChronicle", "The nations began to speak of a World Council.", "Devletler bir Dünya Konseyi'nden söz etmeye başladı."),
    ("HE_CouncilFailedLabel", "The council did not agree", "Konsey anlaşamadı"),
    ("HE_CouncilFailedText",
     "The envoys sat around the great table, argued long into the night and voted. {0} of {1} said yes; unity needs {2}.\n\n{3}\n\n"
     "You can call the council again in {4} days.",
     "Elçiler büyük masanın çevresine oturdu, gece geç saatlere kadar tartıştı ve oy verdi. {1} devletten {0} tanesi evet dedi; birlik için {2} gerekir.\n\n{3}\n\n"
     "Konseyi {4} gün sonra yeniden toplayabilirsin."),
    ("HE_CouncilFailedChronicle", "The World Council met: {0} of {1} voted for unity, not enough.",
     "Dünya Konseyi toplandı: {1} devletten {0} tanesi birliğe evet dedi, yetmedi."),
    ("HE_VictoryUnityLabel", "Victory: the heirs united", "Zafer: mirasçılar birleşti"),
    ("HE_VictoryUnityText",
     "The envoys rose one by one and laid their banners on the great table. Centuries after the ships left Earth, its heirs have chosen "
     "to stand together, and it was {0} that brought them to the table.\n\nThe old quarrels are not gone, but from today they are settled "
     "in council, not on the battlefield. Your colony lives on, and the world will tell its story for a long time.",
     "Elçiler birer birer ayağa kalktı ve sancaklarını büyük masaya bıraktı. Gemiler Dünya'dan kalkalı yüzyıllar oldu; mirasçıları "
     "sonunda birlikte durmayı seçti ve onları bu masaya getiren {0} oldu.\n\nEski kavgalar bitmedi, ama bugünden sonra savaş alanında "
     "değil konseyde çözülecek. Kolonin yaşamaya devam ediyor ve dünya onun hikâyesini uzun süre anlatacak."),
    ("HE_VictoryUnityChronicle", "The World Council voted for unity. The heirs of Earth stand together.",
     "Dünya Konseyi birliğe oy verdi. Dünya'nın mirasçıları artık birlikte."),
    ("HE_VictoryDominionLabel", "Victory: dominion over the heirs", "Zafer: mirasçılar üzerinde hükümranlık"),
    ("HE_VictoryDominionText",
     "Every nation still standing has knelt. Their envoys came to the council hall not to vote but to swear, and the banners of the heirs "
     "now hang beneath the banner of {0}.\n\nIt was not won gently, and some will not forget. But no one on this world now doubts who "
     "leads it. Your colony lives on.",
     "Ayakta kalan her devlet diz çöktü. Elçileri konsey salonuna oy vermeye değil, biat etmeye geldi; mirasçıların sancakları artık "
     "{0} sancağının altında asılı.\n\nBu zafer kolay kazanılmadı ve bazıları bunu unutmayacak. Ama artık bu dünyada kimin önde "
     "olduğundan kimse şüphe etmiyor. Kolonin yaşamaya devam ediyor."),
    ("HE_VictoryDominionChronicle", "Every living nation swore fealty. The World Council bowed to one power.",
     "Yaşayan her devlet biat etti. Dünya Konseyi tek bir güce boyun eğdi."),
    ("HE_FealtyLabel", "{0} offers fealty", "{0} biat teklif ediyor"),
    ("HE_FealtyText",
     "{0} has lost {1} of its {2} settlements to its wars, and it is still at war with you. The {3} sends an envoy under a white banner: they will swear fealty to "
     "you, end the war and pay a tribute of {4} silver every {5} days.\n\nA nation sworn to you counts toward dominion over the heirs "
     "and always votes yes in the World Council. If it ever turns hostile again, the oath is broken.",
     "{0} savaşlarında {2} yerleşiminden {1} tanesini kaybetti ve hâlâ seninle savaşta. {3} beyaz sancakla bir elçi gönderiyor: sana biat edecek, savaşı "
     "bitirecek ve her {5} günde {4} gümüş haraç ödeyecekler.\n\nSana biat eden bir devlet mirasçılar üzerindeki hükümranlığa sayılır ve "
     "Dünya Konseyi'nde hep evet der. Bir gün yeniden düşman olursa yemin bozulur."),
    ("HE_FealtyAccept", "Accept their fealty", "Biatlarını kabul et"),
    ("HE_FealtyRefuse", "Refuse: the war goes on", "Reddet: savaş sürsün"),
    ("HE_FealtyAcceptedChronicle", "{0} swore fealty to your colony.", "{0} kolonine biat etti."),
    ("HE_FealtyRefusedChronicle", "You refused the fealty of {0}. The war goes on.", "{0} devletinin biatını reddettin. Savaş sürüyor."),
    ("HE_FealtyBrokenLabel", "{0} broke its oath", "{0} yeminini bozdu"),
    ("HE_FealtyBrokenText", "{0} has turned hostile and broken its oath of fealty to you. It no longer pays tribute.",
     "{0} sana düşman oldu ve biat yeminini bozdu. Artık haraç ödemiyor."),
    ("HE_TributeArrivesLabel", "Tribute from your vassals", "Biat edenlerden haraç"),
    ("HE_TributeArrivesText", "The nations sworn to you have sent their tribute: {0} silver ({1}).",
     "Sana biat eden devletler haraçlarını gönderdi: {0} gümüş ({1})."),
    ("HE_SettingsCouncil", "World Council (end goal)", "Dünya Konseyi (oyun sonu)"),
    ("HE_SettingsCouncilTip", "The World Council, fealty offers and the two victories. When off, none of them happen.",
     "Dünya Konseyi, biat teklifleri ve iki zafer yolu. Kapalıyken hiçbiri olmaz."),
]:
    key(k, en, tr)
