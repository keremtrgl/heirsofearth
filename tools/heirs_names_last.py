"""Heirs of Earth 4.2.1: family names.
RimWorld gives a two-part name ("First Last") a short name of either its first or its last part, and keeps short names unique among
living and world pawns. With only 12-18 family names a nation shared, half of all new names fell on that small set and a long war
ran the pool dry ("Could not get new name"). Each nation now has some forty more. heirs_people._names merges these and drops any
family name that is also a first name of that nation, since that would halve the pool again.
"last" extends the men's list (and the women's when the nation has no "last_female"); "last_female" extends the women's list.
"female_replace" swaps the women's list out: Roman women were named Nomen + Cognomen (Cornelia Prisca), so their family part is
a feminine cognomen, not a nomen that is already a first name.
"""

LAST = {
    "Roma": {
        "last": ["Aquilius", "Atilius", "Caelius", "Cassius", "Curtius", "Decius", "Didius", "Duilius", "Fannius", "Furius",
                 "Gabinius", "Genucius", "Hostilius", "Iulius", "Laelius", "Livius", "Lollius", "Lucilius", "Maenius", "Manlius",
                 "Minucius", "Nonius", "Numicius", "Oppius", "Petronius", "Pinarius", "Plautius", "Pompeius", "Porcius",
                 "Postumius", "Quinctius", "Rutilius", "Scribonius", "Sergius", "Sextius", "Statilius", "Terentius", "Titius",
                 "Ulpius", "Vibius", "Vipsanius", "Volumnius", "Acilius", "Afranius", "Annius", "Appuleius", "Arruntius", "Aufidius", "Caesennius", "Calidius", "Cestius", "Cocceius", "Egnatius", "Fonteius", "Gellius", "Helvius", "Horatius", "Memmius", "Mummius", "Pomponius", "Sestius", "Vettius"],
        "female_replace": True,
        "last_female": ["Prisca", "Secunda", "Tertia", "Quarta", "Quinta", "Maxima", "Paulina", "Lucilla",
                        "Marcella", "Severa", "Rufina", "Faustina", "Agrippina", "Drusilla", "Procula", "Vera", "Longina",
                        "Saturnina", "Sabina", "Galla", "Crispina", "Celsa", "Firma", "Iusta", "Modesta", "Placida", "Prima",
                        "Pulchra", "Serena", "Vitalis", "Felicula", "Honorata", "Benigna", "Clementina", "Constantia",
                        "Tertulla", "Fortunata", "Iucunda", "Lepida", "Nobilis", "Optata", "Plotina", "Pudentilla", "Rustica",
                        "Sancta", "Superba", "Venusta", "Victorina", "Aeliana", "Amoena", "Aurea", "Bona", "Candida", "Castula", "Concessa", "Exuperia", "Fidelis", "Ianuaria", "Ingenua", "Laeta", "Lupula", "Marciana", "Matidia", "Nigrina", "Perpetua", "Potita", "Quieta", "Sexta", "Successa", "Urbana", "Verecunda", "Severina", "Tacita"],
    },
    "Yamato": {
        "last": ["Abe", "Akechi", "Aoki", "Asano", "Chosokabe", "Endo", "Fukuda", "Goto", "Hasegawa", "Hayashi", "Honda",
                 "Imagawa", "Ishikawa", "Kikuchi", "Kimura", "Kondo", "Maeda", "Matsudaira", "Miyamoto", "Mogami", "Murakami",
                 "Nabeshima", "Nagao", "Niwa", "Oda", "Ogawa", "Otomo", "Ouchi", "Saito", "Sakai", "Sasaki", "Shibata",
                 "Suzuki", "Takahashi", "Tanaka", "Toda", "Tokugawa", "Ukita", "Watanabe", "Yamada", "Yamamoto", "Yoshida"],
    },
    "Nord": {
        "last": ["Asgeirsson", "Bardsson", "Dagsson", "Einarsson", "Finnsson", "Geirsson", "Grimsson", "Hakonsson", "Hallsson",
                 "Hauksson", "Helgason", "Hrafnsson", "Ingvarsson", "Jonsson", "Ketilsson", "Kolbeinsson", "Leifsson",
                 "Magnusson", "Njalsson", "Oddsson", "Ormsson", "Ragnarsson", "Runolfsson", "Sigmundsson", "Snorrason",
                 "Steinsson", "Sveinsson", "Thorgeirsson", "Thorkelsson", "Torfason", "Vigfusson", "Ottarsson", "Hjaltason",
                 "Bersason", "Skeggjason", "Gizurarson", "Brandsson", "Hrolfsson", "Ulfarsson", "Vemundsson"],
        "last_female": ["Asgeirsdottir", "Bardsdottir", "Dagsdottir", "Einarsdottir", "Finnsdottir", "Geirsdottir",
                        "Grimsdottir", "Hakonardottir", "Hallsdottir", "Hauksdottir", "Helgadottir", "Hrafnsdottir",
                        "Ingvarsdottir", "Jonsdottir", "Ketilsdottir", "Kolbeinsdottir", "Leifsdottir", "Magnusdottir",
                        "Njalsdottir", "Oddsdottir", "Ormsdottir", "Ragnarsdottir", "Runolfsdottir", "Sigmundsdottir",
                        "Snorradottir", "Steinsdottir", "Sveinsdottir", "Thorgeirsdottir", "Thorkelsdottir", "Torfadottir",
                        "Vigfusdottir", "Ottarsdottir", "Hjaltadottir", "Bersadottir", "Skeggjadottir", "Gizurardottir",
                        "Brandsdottir", "Hrolfsdottir", "Ulfarsdottir", "Vemundardottir"],
    },
    "Hellas": {
        "last": ["Alexiou", "Antoniou", "Argyros", "Bouras", "Chatzis", "Christodoulou", "Dimitriou", "Economou", "Fotiou",
                 "Georgiou", "Giannakis", "Ioannou", "Kalogeros", "Karamanlis", "Komnenos", "Konstantinou", "Kouris",
                 "Lambrou", "Makris", "Manolis", "Markou", "Melissinos", "Michailidis", "Notaras", "Oikonomou",
                 "Palaiologos", "Panagiotou", "Petrakis", "Phokas", "Raptis", "Sarris", "Skleros", "Spanos", "Stathis",
                 "Tsakalos", "Vasileiou", "Vrienios", "Xenakis", "Zervas", "Zografos"],
    },
    "Tianxia": {
        "last": ["Bai", "Cai", "Cao", "Cheng", "Cui", "Deng", "Ding", "Dong", "Du", "Fan", "Fang", "Feng", "Gao", "Gong",
                 "Han", "Jiang", "Jin", "Kong", "Lu", "Luo", "Meng", "Pan", "Peng", "Qian", "Qin", "Ren", "Shen", "Shi",
                 "Song", "Su", "Tang", "Tian", "Wei", "Xiao", "Xie", "Xiong", "Yan", "Ye", "Yu", "Yuan", "Zeng", "Zheng",
                 "Zhong", "Ouyang", "Sima", "Zhuge", "Shangguan", "Murong"],
    },
    "Albion": {
        "last": ["Abbott", "Ainsworth", "Arkwright", "Bainbridge", "Barlow", "Beckett", "Bramwell", "Carlisle", "Chadwick",
                 "Crompton", "Dalton", "Davenport", "Ellsworth", "Fenwick", "Garside", "Greenhalgh", "Hartley", "Holloway",
                 "Kendrick", "Lockwood", "Marsden", "Montague", "Northcote", "Oldham", "Pickering", "Radcliffe", "Rowntree",
                 "Sedgwick", "Shackleton", "Stanhope", "Sutcliffe", "Tennant", "Trevithick", "Wainwright", "Wedgwood",
                 "Whitworth", "Wilberforce", "Winslow", "Woodhouse", "Yardley"],
    },
    "Kemet": {
        "last": ["son of Amenemhat", "son of Djehuty", "son of Khaemwaset", "son of Ptahmose", "son of Userhat", "son of Neferhotep",
                 "son of Sennefer", "son of Nakht", "of Abydos", "of Iunu", "of Men-nefer", "of Khmun", "of Swenett", "of Nekhen",
                 "of Djeba", "of Ta-senet", "of the Fayum", "of the Cataract", "Amenemope", "Djeserkare", "Hapuseneb",
                 "Ineni", "Kenamun", "Maya", "Nakhtmin", "Paheri", "Ramose", "Senenmut", "Tjanuni", "Userkaf", "Wennefer",
                 "Khnumhotep", "Intef", "Mentuhotep", "Senusret", "Ahmose", "Panehesy", "Ipuwer", "Dedi", "Weni", "of Behdet", "of Tjebu", "of Per-Bastet", "of Zau", "of Djedu", "of Iunet", "of Gebtu", "of Akhetaten", "of the Oasis", "of the Red Land"],
        "last_female": ["daughter of Amenemhat", "daughter of Djehuty", "daughter of Khaemwaset", "daughter of Ptahmose",
                        "daughter of Userhat", "daughter of Neferhotep", "daughter of Sennefer", "daughter of Nakht",
                        "of Abydos", "of Iunu", "of Men-nefer", "of Khmun", "of Swenett", "of Nekhen", "of Djeba",
                        "of Ta-senet", "of the Fayum", "of the Cataract", "Amenemope", "Djeserkare", "Hapuseneb", "Ineni",
                        "Kenamun", "Maya", "Nakhtmin", "Paheri", "Ramose", "Senenmut", "Tjanuni", "Userkaf", "Wennefer",
                        "Khnumhotep", "Intef", "Mentuhotep", "Senusret", "Ahmose", "Panehesy", "Ipuwer", "Dedi", "Weni", "of Behdet", "of Tjebu", "of Per-Bastet", "of Zau", "of Djedu", "of Iunet", "of Gebtu", "of Akhetaten", "of the Oasis", "of the Red Land"],
    },
    "Pars": {
        "last": ["son of Artabanus", "son of Bahram", "son of Hormozd", "son of Mithradates", "son of Peroz", "son of Tiridates",
                 "son of Vologases", "son of Narseh", "of Ctesiphon", "of Persepolis", "of Bactra", "of Rhagae", "of Marv",
                 "of Nishapur", "of Istakhr", "of Gundeshapur", "Aspahbad", "Ispahbudhan", "Kanarang", "Zik", "Mehran",
                 "Spahbed", "Bavand", "Dabuy", "Gushnasp", "Khosrowan", "Nakhwar", "Paduspan", "Razmi", "Shahrvaraz",
                 "Tahmasp", "Vahriz", "Yazdegerdi", "Zarmihr", "Arsacid", "Kayanid", "Pishdad", "Ardashiri", "Mazdaki", "Babakan"],
        "last_female": ["daughter of Artabanus", "daughter of Bahram", "daughter of Hormozd", "daughter of Mithradates",
                        "daughter of Peroz", "daughter of Tiridates", "daughter of Vologases", "daughter of Narseh",
                        "of Ctesiphon", "of Persepolis", "of Bactra", "of Rhagae", "of Marv", "of Nishapur", "of Istakhr",
                        "of Gundeshapur", "Aspahbad", "Ispahbudhan", "Kanarang", "Zik", "Mehran", "Spahbed", "Bavand",
                        "Dabuy", "Gushnasp", "Khosrowan", "Nakhwar", "Paduspan", "Razmi", "Shahrvaraz", "Tahmasp", "Vahriz",
                        "Yazdegerdi", "Zarmihr", "Arsacid", "Kayanid", "Pishdad", "Ardashiri", "Mazdaki", "Babakan"],
    },
    "Inti": {
        "last": ["Amaru", "Apu-Rimaq", "Kusi-Yupanki", "Inka-Roka", "Mamani", "Kunturi", "Chuqi", "Wamani", "Paukar",
                 "Sinchi", "Tupaq", "Wari", "Ayar", "Kanchi", "Qispe", "Rumi", "Urqu", "Wayna", "Pachakuti", "Kuri",
                 "of Saqsaywaman", "of Willkapampa", "of Machu Pikchu", "of Titiqaqa", "of Pisaq", "of Ollantaytampu",
                 "of Kashamarka", "of Chan Chan", "of Kitu", "of Arequipa", "of Hatun Xauxa", "of Tumipampa", "of Wanuku",
                 "of the Sun Gate", "of the Salt Pans", "of the High Puna", "of the Cloud Forest", "of the Rope Bridge", "of Pachakamaq", "of Limaq", "of Qullasuyu", "of Chinchaysuyu", "of Antisuyu", "of Kuntisuyu", "of Wanakawri", "of the Terraces", "of the Quipu House", "of the Long Road",
                 "Allqa", "Antawaylla"],
    },
}
