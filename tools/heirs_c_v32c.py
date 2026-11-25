"""Heirs of Earth 3.2 part three: weapons, so every nation has at least five."""
from heirs_kit import melee, projectile, ranged, tool

# ------------------------------------------------------------------ melee
melee("Roma", "Spatha", "spatha", "spatha",
      "The long sword of the cavalry and of the later legions. Longer than the gladius, it cuts well from horseback and still has a good point.",
      "Süvarilerin ve sonraki lejyonların uzun kılıcı. Gladiustan uzundur, at sırtından iyi keser ve ucu hâlâ iyi saplar.",
      "Medieval", "HE_Roma_Cursus",
      [tool("pommel", "Blunt", 9, 2), tool("point", "Stab", 16, 2.0, 0.26), tool("edge", "Cut", 19, 2.1, 0.28)],
      mass=1.5, work=15000, painter="spatha", stuff_count=70, skill=5, angle=-45, extra_tags=["MedievalMeleeDecent"])
melee("Nord", "Seax", "seax", "seaks",
      "A heavy single-edged knife with a broken back, carried by every free man. It is a tool at the table and a weapon in the shield wall.",
      "Her özgür adamın taşıdığı, sırtı kırık, ağır, tek ağızlı bir bıçak. Sofrada bir alet, kalkan duvarında bir silahtır.",
      "Medieval", "HE_Nord_Smithing",
      [tool("handle", "Blunt", 8, 1.8), tool("point", "Stab", 14, 1.6, 0.22), tool("edge", "Cut", 14, 1.7, 0.20)],
      mass=0.7, work=9000, painter="seax", stuff_count=40, skill=3)
melee("Tianxia", "Dao", "dao", "dao",
      "The broad sabre of the common soldier, with a disc guard and a red tassel. It cuts deep and is easy to learn.",
      "Disk siperli ve kırmızı püsküllü, sıradan askerin geniş kılıcı. Derin keser ve öğrenmesi kolaydır.",
      "Medieval", "HE_Tianxia_Jian",
      [tool("handle", "Blunt", 9, 2), tool("point", "Stab", 13, 1.9, 0.18), tool("edge", "Cut", 20, 2.0, 0.26)],
      mass=1.3, work=14000, painter="dao", stuff_count=60, skill=4, angle=-45, extra_tags=["MedievalMeleeDecent"])
melee("Kemet", "Hedj", "hedj mace", "hedj topuzu",
      "A pear-shaped mace head of white stone on a gold-bound haft. In the oldest carvings the king raises it over his enemies.",
      "Altınla sarılmış bir sap üzerinde beyaz taştan armut biçimli bir topuz başı. En eski kabartmalarda kral onu düşmanlarının üzerine kaldırır.",
      "Neolithic", "HE_Kemet_Spear",
      [tool("handle", "Blunt", 8, 2), tool("head", "Blunt", 15, 2.3, 0.20)],
      mass=1.8, work=8000, painter="hedj", stuff=("Metallic", "Stony"), stuff_count=50, cost={"WoodLog": 15}, blunt=True, skill=3, angle=-45)
melee("Pars", "Shamshir", "shamshir", "şimşir",
      "A deeply curved sabre of watered steel. It draws its cut through the target like a lion's claw and is the pride of every Parsian rider.",
      "Su çeliğinden derin eğimli bir kılıç. Kesiğini hedefin içinden bir aslan pençesi gibi çeker ve her Pars süvarisinin gururudur.",
      "Medieval", "HE_Pars_Akinakes",
      [tool("handle", "Blunt", 8, 2), tool("point", "Stab", 12, 1.9, 0.16), tool("edge", "Cut", 21, 1.95, 0.27)],
      mass=1.2, work=15000, painter="shamshir", stuff_count=60, skill=5, angle=-45, extra_tags=["MedievalMeleeDecent"])
melee("Inti", "Chuki", "chuki lance", "chuki mızrağı",
      "A long hardwood lance with a bronze leaf blade and a tuft of coloured wool. The royal guard holds the line with it on the mountain roads.",
      "Bronz yaprak biçimli uçlu ve renkli yün püsküllü uzun, sert ağaçtan bir mızrak. Kraliyet muhafızları dağ yollarında hattı onunla tutar.",
      "Medieval", "HE_Inti_RoyalGuard",
      [tool("shaft", "Blunt", 10, 2.2), tool("point", "Stab", 21, 2.5, 0.40)],
      mass=2.4, work=12000, painter="chuki", stuff_count=40, cost={"WoodLog": 25}, skill=4, angle=-45)

# ------------------------------------------------------------------ ranged
ranged("Hellas", "Gastraphetes", "gastraphetes", "gastraphetes",
       "The 'belly bow': a heavy bow on a long stock, spanned by leaning the belly on a curved rest. It shoots harder and further than any hand bow.",
       "'Karın yayı': uzun bir kundak üzerinde ağır bir yay; karnı kavisli bir dayanağa yaslayarak gerilir. Herhangi bir el yayından daha sert ve uzağa atar.",
       "Medieval", "HE_Hellas_Bronze",
       projectile("HE_Bolt_Gastraphetes", "gastraphetes bolt", "gastraphetes oku", "Arrow", 17, 52, "Things/Projectile/Arrow_Small", pen=0.30),
       1.9, 30.9, 2.2, (0.6, 0.72, 0.62, 0.46), 3.2, 14000, "gastraphetes", {"WoodLog": 50, "Steel": 30},
       sound="Bow_Large", interact="Bow_Large", skill=5)
ranged("Inti", "Bolas", "bolas", "bolas",
       "Three cord-wrapped stones on braided cords. Whirled and thrown, they wrap around the legs of man or llama and knock the wind out of them.",
       "Örgü iplere bağlı, iple sarılmış üç taş. Döndürülüp fırlatıldığında insanın ya da laması bacaklarına dolanır ve nefesini keser.",
       "Neolithic", "HE_Inti_Sling",
       projectile("HE_Bolas_Inti", "bolas", "bolas", "Blunt", 10, 30, "HeirsOfEarth/Projectiles/HE_Stone_Inti", pen=0.08),
       1.0, 17.9, 1.5, (0.75, 0.72, 0.5, 0.3), 0.6, 4000, "bolas", {"WoodLog": 10, "Cloth": 20},
       sound="ThrowGrenade", interact="Bow_Recurve", skill=2, klass=("Ranged", "ShortShots"))
ranged("Albion", "Blunderbuss", "blunderbuss", "blanderbas",
       "A short gun with a flared brass mouth, loaded with a handful of shot. Useless across a field, terrible across a room. Coachmen and ship's crews swear by it.",
       "Bir avuç saçmayla doldurulan, ağzı genişleyen pirinç namlulu kısa bir tüfek. Bir tarlanın öbür ucunda işe yaramaz, bir odanın öbür ucunda korkunçtur. Arabacılar ve gemi tayfaları ona yemin eder.",
       "Industrial", "HE_Albion_Musket",
       projectile("HE_Bullet_Blunderbuss", "blunderbuss shot", "blanderbas saçması", "Bullet", 24, 60, "Things/Projectile/Bullet_Small", pen=0.16),
       1.0, 13.9, 2.0, (0.85, 0.78, 0.42, 0.2), 3.8, 14000, "blunderbuss", {"Steel": 50, "WoodLog": 25},
       sound="Shot_Shotgun", interact="Interact_Shotgun", gun=True, klass=("Ranged", "ShortShots"),
       tools=[tool("stock", "Blunt", 10, 2.1), tool("barrel", "Blunt", 9, 2.0)])
ranged("Albion", "FlintlockPistol", "flintlock pistol", "çakmaklı tabanca",
       "A holster pistol with a brass butt cap: one shot, then a club. Officers carry a pair of them.",
       "Pirinç dipçik kapaklı bir kılıf tabancası: bir atış, sonra bir sopa. Subaylar bunlardan bir çift taşır.",
       "Industrial", "HE_Albion_Musket",
       projectile("HE_Bullet_FlintPistol", "pistol ball", "tabanca mermisi", "Bullet", 17, 55, "Things/Projectile/Bullet_Small", pen=0.20),
       0.6, 20.9, 2.0, (0.8, 0.66, 0.4, 0.22), 1.4, 9000, "flintlock_pistol", {"Steel": 35, "WoodLog": 10},
       sound="Shot_Revolver", interact="Interact_Revolver", gun=True, klass=("Ranged", "ShortShots"),
       tools=[tool("grip", "Blunt", 9, 1.6), tool("barrel", "Blunt", 8, 1.6)])
