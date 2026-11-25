"""Heirs of Earth 3.4 "Palace and Treaty": rulers with temperaments and succession, treaties with the nations, the embassy,
honorary titles and world events (the Games, a great fair, famine and plague)."""
from heirs_c_v32 import free_slot
from heirs_c_v33 import find
from heirs_data import add, key, tex
from heirs_kit import research
from heirs_xml import Def, T

# ------------------------------------------------------------------ courts: temperament leanings and honorary titles
COURTS = {
    "Roma": (["Warlike", "Mercantile"], ("honorary citizen of Nova Roma", "Nova Roma fahri yurttaşı")),
    "Yamato": (["Warlike", "Pious"], ("honoured guest of the shogun", "şogunun onurlu konuğu")),
    "Nord": (["Warlike"], ("sworn friend of the jarls", "jarlların yeminli dostu")),
    "Hellas": (["Scholarly", "Mercantile"], ("proxenos of the League", "Birliğin proksenosu")),
    "Tianxia": (["Scholarly", "Cautious"], ("marquis of the outer realm", "dış diyarın markisi")),
    "Albion": (["Mercantile", "Warlike"], ("knight of the Commonwealth", "Devletler Topluluğu şövalyesi")),
    "Kemet": (["Pious", "Scholarly"], ("friend of the Pharaoh", "Firavunun dostu")),
    "Pars": (["Mercantile", "Pious"], ("benefactor of the Satrap", "Satrabın velinimeti")),
    "Inti": (["Pious", "Cautious"], ("kin of the Sun", "Güneşin akrabası")),
}
for nation, (bias, title) in COURTS.items():
    nd = find("HeirsOfEarth.NationDef", f"HE_{nation}")
    nd.fields["temperamentBias"] = list(bias)
    nd.fields["honoraryTitle"] = T(*title)

K = [
    # temperaments
    ("HE_TemperamentWarlike", "Warlike", "Savaşçı"),
    ("HE_TemperamentWarlikeDesc", "seeks quarrels with rivals, demands half again as much tribute and offers defensive alliances.",
     "rakipleriyle kavga arar, yarısı kadar daha fazla haraç ister ve savunma ittifakı önerir."),
    ("HE_TemperamentMercantile", "Mercantile", "Tüccar"),
    ("HE_TemperamentMercantileDesc", "warms to every nation, offers trade treaties and likes to host great fairs.",
     "her devlete ısınır, ticaret antlaşması önerir ve büyük panayırlar düzenlemeyi sever."),
    ("HE_TemperamentScholarly", "Scholarly", "Bilgin"),
    ("HE_TemperamentScholarlyDesc", "shares learning freely (a quarter more culture knowledge from this nation) and offers science exchanges.",
     "bilgisini cömertçe paylaşır (bu devletten dörtte bir daha fazla kültür bilgisi) ve bilim değişimi önerir."),
    ("HE_TemperamentPious", "Pious", "Dindar"),
    ("HE_TemperamentPiousDesc", "keeps the festivals, may host the Games and offers peace treaties.",
     "bayramları gözetir, Oyunlara ev sahipliği yapabilir ve barış antlaşması önerir."),
    ("HE_TemperamentCautious", "Cautious", "Temkinli"),
    ("HE_TemperamentCautiousDesc", "often holds back from war, warms slowly to others and offers peace treaties.",
     "çoğu zaman savaştan kaçınır, başkalarına yavaşça ısınır ve barış antlaşması önerir."),
    ("HE_EpithetWarlike", "the Bold", "Cesur"),
    ("HE_EpithetMercantile", "the Rich", "Zengin"),
    ("HE_EpithetScholarly", "the Wise", "Bilge"),
    ("HE_EpithetPious", "the Pious", "Dindar"),
    ("HE_EpithetCautious", "the Prudent", "Temkinli"),
    ("HE_RulerLine", "{0} {1}, {2}", "{0} {1}, {2}"),
    ("HE_ReignYears", "Reigning for {0} years.", "{0} yıldır hüküm sürüyor."),
    ("HE_AtlasRuler", "Ruler", "Hükümdar"),
    # succession
    ("HE_SuccessionLabel", "New ruler of {0}", "{0}: yeni hükümdar"),
    ("HE_SuccessionText",
     "The reign of {1} is over: the crown of {0} has passed to {2}.\n\nThe new ruler is {3}\n\nA new ruler may review the treaties made with you, and rivals may test the young reign.",
     "{1} saltanatı sona erdi: {0} tacı {2} adlı hükümdara geçti.\n\nYeni hükümdar {3}\n\nYeni bir hükümdar seninle yapılan antlaşmaları gözden geçirebilir, rakipler de genç saltanatı sınayabilir."),
    ("HE_SuccessionChronicle", "{0} now rules {1}.", "{1} artık {0} tarafından yönetiliyor."),
    ("HE_SuccessionMessage", "{0} now rules {1}.", "{1} artık {0} tarafından yönetiliyor."),
    # treaties
    ("HE_CourtsHeading", "Courts and treaties", "Saraylar ve antlaşmalar"),
    ("HE_CourtsIntro",
     "Every nation is ruled by a ruler with a temperament that shapes what the court offers and demands. Sign treaties for a gift of silver; a ruler may also offer one for free. Your title with a nation grows with goodwill and treaties.",
     "Her devleti, sarayın ne önerip ne isteyeceğini belirleyen bir mizaca sahip bir hükümdar yönetir. Antlaşmaları bir gümüş hediyesiyle imzala; bir hükümdar da bedava önerebilir. Bir devletteki unvanın iyi niyet ve antlaşmalarla büyür."),
    ("HE_EmbassyYes", "You have an embassy: science exchanges and defensive alliances are possible, and every nation you hold a treaty with grows a little fonder of you each month.",
     "Bir elçiliğin var: bilim değişimi ve savunma ittifakı mümkün, antlaşma yaptığın her devlet de her ay sana biraz daha ısınır."),
    ("HE_EmbassyNo", "Build an embassy (research: embassies) for science exchanges and defensive alliances.",
     "Bilim değişimi ve savunma ittifakı için bir elçilik inşa et (araştırma: elçilikler)."),
    ("HE_TreatyPeace", "Peace", "Barış"),
    ("HE_TreatyPeaceDesc", "The nation will not demand tribute from you, and its goodwill rises a little every month.",
     "Devlet senden haraç istemez ve iyi niyeti her ay biraz artar."),
    ("HE_TreatyTrade", "Trade", "Ticaret"),
    ("HE_TreatyTradeDesc", "A trade caravan of the nation visits your colony every twenty days or so.",
     "Devletin bir ticaret kervanı yaklaşık yirmi günde bir koloni ziyaret eder."),
    ("HE_TreatyScience", "Science", "Bilim"),
    ("HE_TreatyScienceDesc", "Scholars visit each other: you gain 8 culture knowledge of the nation every month.",
     "Bilginler birbirini ziyaret eder: her ay devletin kültür bilgisinden 8 kazanırsın."),
    ("HE_TreatyAlliance", "Alliance", "İttifak"),
    ("HE_TreatyAllianceDesc", "A defensive alliance: when raiders attack your home, the nation often sends warriors to help (at most every ten days).",
     "Savunma ittifakı: akıncılar evine saldırdığında devlet çoğu zaman yardıma savaşçı gönderir (en çok on günde bir)."),
    ("HE_TreatyFee", "A gift of {0} silver seals it. Needs at least {1} goodwill.", "{0} gümüşlük bir hediyeyle mühürlenir. En az {1} iyi niyet gerekir."),
    ("HE_TreatyNeedsEmbassy", "Needs an embassy in your colony.", "Kolonide bir elçilik gerekir."),
    ("HE_TreatyClickCancel", "Click to cancel this treaty.", "Bu antlaşmayı iptal etmek için tıkla."),
    ("HE_TreatyCancelConfirm",
     "Cancel the {0} treaty with {1}? They will lose {2} goodwill toward you, and every other nation {3}: word of a broken oath travels fast.",
     "{1} ile {0} antlaşmasını iptal etmek mi? Sana karşı {2} iyi niyet kaybederler, diğer her devlet de {3}: bozulan yeminin haberi çabuk yayılır."),
    ("HE_TreatyNoNation", "This nation is gone.", "Bu devlet yok oldu."),
    ("HE_TreatyAlready", "Already signed.", "Zaten imzalandı."),
    ("HE_TreatyHostile", "{0} is hostile to you.", "{0} sana düşman."),
    ("HE_TreatyGoodwill", "Needs at least {0} goodwill.", "En az {0} iyi niyet gerekir."),
    ("HE_TreatyEmbassy", "Needs an embassy in your colony.", "Kolonide bir elçilik gerekir."),
    ("HE_TreatySigned", "A {0} treaty was signed with {1}.", "{1} ile {0} antlaşması imzalandı."),
    ("HE_TreatyEnded", "The {0} treaty with {1} was cancelled.", "{1} ile {0} antlaşması iptal edildi."),
    ("HE_TreatyVoid", "The {0} treaty with {1} became void when they turned hostile.", "{1} düşmanlaşınca {0} antlaşması geçersiz oldu."),
    ("HE_TreatyRevoked", "The new ruler of {1} revoked the {0} treaty.", "{1} yeni hükümdarı {0} antlaşmasını feshetti."),
    ("HE_TreatyVoidLabel", "Treaties with {0} void", "{0} ile antlaşmalar geçersiz"),
    ("HE_TreatyVoidText", "{0} has turned hostile to you. Every treaty you held with them is void.",
     "{0} sana düşman oldu. Onlarla yaptığın bütün antlaşmalar geçersiz."),
    ("HE_TreatyRevokedLabel", "{0} revokes a treaty", "{0} bir antlaşmayı feshediyor"),
    ("HE_TreatyRevokedText", "{0} does not hold with the agreements of the old court: the {1} treaty with {2} is revoked.\n\nWin back their goodwill and you can sign it again.",
     "{0} eski sarayın anlaşmalarına bağlı değil: {2} ile {1} antlaşması feshedildi.\n\nİyi niyetlerini geri kazanırsan yeniden imzalayabilirsin."),
    ("HE_TreatyOfferLabel", "{0} offers a {1} treaty", "{0} {1} antlaşması öneriyor"),
    ("HE_TreatyOfferText", "{0} of {1} sends a sealed letter offering a {2} treaty, without the usual gifts.\n\n{3}",
     "{1} hükümdarı {0}, alışılmış hediyeler olmadan {2} antlaşması öneren mühürlü bir mektup gönderdi.\n\n{3}"),
    ("HE_TreatyOfferAccept", "Sign the {0} treaty", "{0} antlaşmasını imzala"),
    ("HE_TreatyOfferRefuse", "Decline", "Reddet"),
    ("HE_AllyAnswers", "{0} honours the alliance: its warriors are marching to help you.", "{0} ittifaka sadık kalıyor: savaşçıları yardımına geliyor."),
    # titles
    ("HE_YourTitle", "Your standing: {0}", "Konumun: {0}"),
    ("HE_Title0", "stranger", "yabancı"),
    ("HE_Title1", "guest", "konuk"),
    ("HE_Title2", "friend", "dost"),
    ("HE_Title3", "honoured friend", "onurlu dost"),
    ("HE_TitleTip",
     "Guest: goodwill 0 or more. Friend: 40 or more. Honoured friend: 60 or more and two treaties. The nation's own high honour ({0}): 80 or more, a defensive alliance and an embassy; it brings {1} culture knowledge every month.",
     "Konuk: 0 veya daha fazla iyi niyet. Dost: 40 veya daha fazla. Onurlu dost: 60 veya daha fazla ve iki antlaşma. Devletin kendi yüksek onuru ({0}): 80 veya daha fazla, bir savunma ittifakı ve bir elçilik; her ay {1} kültür bilgisi getirir."),
    ("HE_HonourLabel", "Honoured by {0}", "{0} tarafından onurlandırıldın"),
    ("HE_HonourText", "{0} of {1} proclaims your colony {2} before the whole court. From now on their scholars share {3} culture knowledge with you every month.",
     "{1} hükümdarı {0}, bütün sarayın önünde koloniyi {2} ilan etti. Bundan sonra bilginleri her ay seninle {3} kültür bilgisi paylaşacak."),
    ("HE_HonourChronicle", "The colony was named {0} by {1}.", "Koloni {1} tarafından {0} ilan edildi."),
    # world events
    ("HE_SettingsWorldEvents", "World events between the nations", "Devletler arası dünya olayları"),
    ("HE_SettingsWorldEventsTip", "The Games, great fairs, famines and plagues among the heir nations, some of which ask for your help.",
     "Mirasçı devletler arasında Oyunlar, büyük panayırlar, kıtlıklar ve salgınlar; bazıları senden yardım ister."),
    ("HE_GamesLabel", "The Games of {0}", "{0} Oyunları"),
    ("HE_GamesText",
     "{1} invites every nation to the Games of {0}: footraces, wrestling and the bow, before crowds from the whole world.\n\nYour best fighter, {2} (skill {3}), could compete for the colony. Chance to win: {4}.\n\nA victory makes every nation think better of you; even taking part pleases the hosts.",
     "{1}, bütün devletleri {0} Oyunlarına davet ediyor: bütün dünyadan gelen kalabalıklar önünde koşu, güreş ve okçuluk.\n\nEn iyi savaşçın {2} (beceri {3}) koloni adına yarışabilir. Kazanma şansı: {4}.\n\nBir zafer her devletin sana daha iyi bakmasını sağlar; katılmak bile ev sahiplerini memnun eder."),
    ("HE_GamesAccept", "Send {1} to compete", "{1} yarışmaya gitsin"),
    ("HE_GamesRefuse", "Stay home", "Evde kal"),
    ("HE_GamesMissing", "Cannot compete.", "Yarışamaz."),
    ("HE_GamesNoChampion", "The champion cannot travel.", "Şampiyon yola çıkamaz."),
    ("HE_GamesWonLabel", "{0} wins the Games", "{0} Oyunları kazandı"),
    ("HE_GamesWon", "{0} won the Games of {1}. The whole world now knows the name of your colony.",
     "{0}, {1} Oyunlarını kazandı. Bütün dünya artık koloninin adını biliyor."),
    ("HE_GamesLost", "{0} competed well at the Games of {1} but did not win.", "{0}, {1} Oyunlarında iyi yarıştı ama kazanamadı."),
    ("HE_FairLabel", "Great fair of {0}", "{0} büyük panayırı"),
    ("HE_FairText", "{1} opens a great fair, and merchants of the whole world take to the roads. Over the next days, caravans of {2} will pass by your colony.",
     "{1} büyük bir panayır açtı ve bütün dünyanın tüccarları yola çıktı. Önümüzdeki günlerde {2} kervanları kolonine uğrayacak."),
    ("HE_FairChronicle", "{0} held a great fair.", "{0} büyük bir panayır düzenledi."),
    ("HE_FamineLabel", "Famine in {0}", "{0}: kıtlık"),
    ("HE_FamineText", "The harvest has failed in {0}, and {1} asks every friend for food. Could you spare food worth {2} nutrition (about {2} simple meals)?",
     "{0} topraklarında hasat kötü gitti ve {1} her dosttan yiyecek istiyor. {2} besin değerinde (yaklaşık {2} basit yemek) yiyecek ayırabilir misin?"),
    ("HE_FamineAccept", "Send food worth {0} nutrition", "{0} besin değerinde yiyecek gönder"),
    ("HE_FamineRefuse", "We have none to spare", "Ayıracak yiyeceğimiz yok"),
    ("HE_FamineMissing", "You do not have {0} nutrition of food.", "{0} besin değerinde yiyeceğin yok."),
    ("HE_FamineHelped", "The colony sent food to {0} in a famine.", "Koloni kıtlık çeken {0} devletine yiyecek gönderdi."),
    ("HE_PlagueLabel", "Plague in {0}", "{0}: salgın"),
    ("HE_PlagueText", "A plague is spreading in {0}. {1} asks for {2} medicine.\n\nIf you trade with them, the sickness may travel your roads whatever you answer.",
     "{0} topraklarında bir salgın yayılıyor. {1} {2} ilaç istiyor.\n\nOnlarla ticaret yapıyorsan, cevabın ne olursa olsun hastalık yollarından sana gelebilir."),
    ("HE_PlagueAccept", "Send {0} medicine", "{0} ilaç gönder"),
    ("HE_PlagueRefuse", "Keep our medicine", "İlacımızı tut"),
    ("HE_PlagueMissing", "You do not have {0} medicine.", "{0} ilacın yok."),
    ("HE_PlagueHelped", "The colony sent medicine to {0} in a plague.", "Koloni salgın yaşayan {0} devletine ilaç gönderdi."),
    ("HE_PlagueSpreads", "The plague of {0} has travelled the trade roads: sickness may reach the colony within days.",
     "{0} salgını ticaret yollarından yayıldı: hastalık birkaç gün içinde koloniye ulaşabilir."),
]
for k, en, tr in K:
    key(k, en, tr)

add("Core/HE_Letters.xml", Def("LetterDef", "HE_EventLetter", letterClass="HeirsOfEarth.ChoiceLetter_HeirsEvent",
                               color="(170, 140, 90)", flashInterval=-1))

THOUGHTS = "Core/HE_Thoughts34.xml"
add(THOUGHTS, Def("ThoughtDef", "HE_GamesVictor", thoughtClass="Thought_Memory", durationDays=15, stackLimit=1,
                  stages=[{"label": T("victor of the Games", "Oyunların galibi"),
                           "description": T("I won the Games before the whole world. They will sing of it.",
                                            "Oyunları bütün dünyanın önünde kazandım. Bunun şarkısını söyleyecekler."),
                           "baseMoodEffect": 12}]))
add(THOUGHTS, Def("ThoughtDef", "HE_GamesContender", thoughtClass="Thought_Memory", durationDays=6, stackLimit=1,
                  stages=[{"label": T("competed at the Games", "Oyunlarda yarıştı"),
                           "description": T("I did not win, but I stood among the best of the world.",
                                            "Kazanamadım ama dünyanın en iyileri arasında durdum."),
                           "baseMoodEffect": 4}]))

# ------------------------------------------------------------------ the embassy (shared)
col, row = free_slot("Common", "Medieval")
R_EMB = research("Common", "Embassies", "embassies", "elçilikler",
                 "Permanent envoys, sealed letters and a house where foreign guests are received with honour. Opens the embassy, which makes science exchanges and defensive alliances possible.",
                 "Kalıcı elçiler, mühürlü mektuplar ve yabancı konukların onurla karşılandığı bir ev. Bilim değişimini ve savunma ittifakını mümkün kılan elçiliği açar.",
                 900, "Medieval", col, row, prereqs=["Smithing"])
find("ResearchProjectDef", R_EMB).fields["modExtensions"] = [{"@Class": "HeirsOfEarth.HeirsResearchExt"}]

add("Things/HE_Buildings_Common.xml", Def(
    "ThingDef", "HE_Embassy", parent="BuildingBase", label=T("embassy", "elçilik"),
    description=T("A hall to receive the envoys of the heir nations: a desk for letters and seals, chairs for guests and a banner stand "
                  "for every nation. With an embassy you can sign science exchanges and defensive alliances, and every nation you hold "
                  "a treaty with grows a little fonder of you each month. One is enough.",
                  "Mirasçı devletlerin elçilerini karşılamak için bir salon: mektuplar ve mühürler için bir masa, konuklar için "
                  "sandalyeler ve her devlet için bir sancak ayağı. Bir elçilikle bilim değişimi ve savunma ittifakı imzalayabilirsin, "
                  "antlaşma yaptığın her devlet de her ay sana biraz daha ısınır. Bir tane yeter."),
    thingClass="Building",
    graphicData={"texPath": "HeirsOfEarth/Buildings/HE_Embassy", "graphicClass": "Graphic_Single", "drawSize": "(3,3)",
                 "shadowData": {"volume": "(2.6,0.4,2.6)"}},
    altitudeLayer="Building", passability="PassThroughOnly", pathCost=40, fillPercent=0.3, rotatable=False, size="(3,3)",
    stuffCategories=["Stony", "Woody"], costStuffCount=180, costList={"Cloth": 60, "Gold": 10, "Silver": 200},
    statBases={"MaxHitPoints": 400, "WorkToBuild": 12000, "Beauty": 12, "Flammability": 0.6, "Mass": 120},
    designationCategory="HE_Heritage", researchPrerequisites=[R_EMB], constructionSkillPrerequisite=5,
    building={"isInert": True}))
tex("HeirsOfEarth/Buildings/HE_Embassy", "embassy", size=(3, 3))
