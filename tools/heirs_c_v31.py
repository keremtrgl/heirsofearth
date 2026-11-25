"""Heirs of Earth 3.1 "Polish and Balance": settlement icons, research browser, encyclopedia, difficulty presets."""
from heirs_data import key, tex

for nation in ("Roma", "Yamato", "Nord", "Hellas", "Tianxia", "Albion", "Kemet", "Pars", "Inti"):
    tex(f"HeirsOfEarth/World/HE_Settlement_{nation}", f"settlement_{nation.lower()}")

for k, en, tr in [
    # Research browser
    ("HE_TabResearch", "Research", "Araştırmalar"),
    ("HE_AtlasIntro",
     "Every research project of the heir nations in one list. Filter by nation, age and state, see why a project is locked, "
     "and start one with a single click. Hover over a row for its description and effects.",
     "Mirasçı devletlerin tüm araştırmaları tek listede. Devlete, çağa ve duruma göre süz, bir projenin neden kilitli olduğunu gör "
     "ve tek tıkla başlat. Açıklama ve etkiler için fareyi bir satırın üstüne getir."),
    ("HE_AtlasAllNations", "All nations", "Tüm devletler"),
    ("HE_AtlasCommon", "Shared (no nation)", "Ortak (devletsiz)"),
    ("HE_AtlasAllAges", "All ages", "Tüm çağlar"),
    ("HE_AtlasStateAll", "All", "Hepsi"),
    ("HE_AtlasStateAvailable", "Can start", "Başlatılabilir"),
    ("HE_AtlasStateLocked", "Locked", "Kilitli"),
    ("HE_AtlasStateFinished", "Finished", "Bitti"),
    ("HE_AtlasCount", "{0} projects, {1} finished", "{0} proje, {1} tanesi bitti"),
    ("HE_AtlasEmpty", "No project matches these filters.", "Bu filtrelere uyan proje yok."),
    ("HE_AtlasTradition", "tradition", "gelenek"),
    ("HE_AtlasKnowledge", "needs {0} knowledge", "{0} bilgi gerekir"),
    ("HE_AtlasDone", "Finished", "Bitti"),
    ("HE_AtlasCurrent", "Researching", "Araştırılıyor"),
    ("HE_AtlasResearch", "Research", "Araştır"),
    ("HE_AtlasNeeds", "Needs: {0}", "Gerekenler: {0}"),
    ("HE_AtlasNeedsBench", "Needs a {0}", "Gerekli yapı: {0}"),
    ("HE_AtlasLocked", "Not available yet", "Henüz açılmadı"),
    # Encyclopedia
    ("HE_TabEncyclopedia", "Encyclopedia", "Ansiklopedi"),
    ("HE_EncyclopediaIntro",
     "Everything about each heir nation on one page: its story, neighbours, buildings, weapons, clothes, food, traditions and tales. "
     "Click any entry to open its full information card.",
     "Her mirasçı devlet hakkında her şey tek sayfada: tarihi, komşuları, binaları, silahları, kıyafetleri, yemekleri, gelenekleri ve hikâyeleri. "
     "Tam bilgi kartını açmak için herhangi bir öğeye tıkla."),
    ("HE_EncyclopediaGone", "this nation has fallen", "bu devlet yıkıldı"),
    ("HE_EncyclopediaRelations", "relations with you {0} ({1})", "seninle ilişkisi {0} ({1})"),
    ("HE_EncyclopediaProgress", "Your knowledge: {0} · research {1} / {2} finished {3}", "Bilgin: {0} · araştırma {1} / {2} bitti {3}"),
    ("HE_EncyclopediaNeighbours", "Friends and rivals", "Dostlar ve rakipler"),
    ("HE_EncyclopediaFriends", "Natural friends: {0}\nOld rivals: {1}", "Doğal dostları: {0}\nEski rakipleri: {1}"),
    ("HE_EncyclopediaHowTo",
     "How to learn from them: trade with their caravans and visit their towns, open a trade road, study {0} goods at a culture table, "
     "take in {0} colonists as teachers, answer their envoys, and follow their story once your knowledge is high enough. "
     "Their friends think better of you when you help them; their rivals do not.",
     "Onlardan nasıl öğrenilir: kervanlarıyla ve kasabalarıyla ticaret yap, bir ticaret yolu aç, {0} mallarını kültür masasında incele, "
     "{0} kolonistleri öğretmen olarak al, elçilerine cevap ver ve bilgin yeterince yükselince hikâyelerini takip et. "
     "Onlara yardım edersen dostları seni daha çok sever; rakipleri sevmez."),
    ("HE_EncyclopediaBuilding", "Buildings ({0})", "Binalar ({0})"),
    ("HE_EncyclopediaWeapon", "Weapons ({0})", "Silahlar ({0})"),
    ("HE_EncyclopediaApparel", "Clothes and armour ({0})", "Kıyafet ve zırhlar ({0})"),
    ("HE_EncyclopediaFood", "Food and drink ({0})", "Yiyecek ve içecekler ({0})"),
    ("HE_EncyclopediaItem", "Goods and treasures ({0})", "Mallar ve hazineler ({0})"),
    ("HE_EncyclopediaFloor", "Floors ({0})", "Zeminler ({0})"),
    ("HE_EncyclopediaTraditions", "Traditions ({0})", "Gelenekler ({0})"),
    ("HE_EncyclopediaStories", "Story and legendary work", "Hikâye ve efsanevi eser"),
    ("HE_EncyclopediaChainOn", "in progress (see Stories)", "devam ediyor (Hikâyeler bölümüne bak)"),
    ("HE_EncyclopediaInfoTip", "Click for the full information card.", "Tam bilgi kartı için tıkla."),
    # Settings
    ("HE_SettingsPresets", "Difficulty presets (set the sliders below at once):", "Zorluk hazır ayarları (aşağıdaki kaydırıcıları birlikte ayarlar):"),
    ("HE_SettingsPreset0", "Relaxed", "Rahat"),
    ("HE_SettingsPreset1", "Standard", "Standart"),
    ("HE_SettingsPreset2", "Hard", "Zor"),
    ("HE_SettingsTributeDemand", "Silver demanded by nations: {0}", "Devletlerin istediği gümüş: {0}"),
]:
    key(k, en, tr)
