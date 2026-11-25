"""Heirs of Earth 3.2 part two: two more buildings for Albion, Kemet, Pars and Inti, and a defensive structure for every
nation that did not have one (Tianxia already has its fire-arrow battery)."""
from heirs_c_v32 import free_slot
from heirs_data import add, tex
from heirs_kit import culture, deco, projectile, research
from heirs_xml import Def, T

LAMP_POWER = [{"@Class": "CompProperties_Power", "compClass": "CompPowerTrader", "basePowerConsumption": 30, "shortCircuitInRain": False},
              {"@Class": "CompProperties_Flickable"}]


def wood_fire(rate, capacity, size, offset, heat=None):
    comps = [{"@Class": "CompProperties_Refuelable", "fuelConsumptionRate": rate, "fuelCapacity": capacity, "fuelConsumptionPerTickInRain": 0.0006,
              "fuelFilter": {"thingDefs": ["WoodLog"]}, "initialFuelPercent": 1, "showAllowAutoRefuelToggle": True},
             {"@Class": "CompProperties_FireOverlay", "fireSize": size, "offset": offset}]
    if heat:
        comps.append({"@Class": "CompProperties_HeatPusher", "heatPerSecond": heat, "heatPushMaxTemperature": 26})
    return comps


# ------------------------------------------------------------------ buildings
deco("Albion", "GasLamp", "gas lamp", "gaz lambası",
     "A cast-iron street lamp with a glass lantern. In the cities gas from the works keeps it burning all night; here a small burner fed from the power grid does the same.",
     "Cam fenerli dökme demir bir sokak lambası. Şehirlerde gazhaneden gelen gaz onu bütün gece yakar; burada elektrik şebekesinden beslenen küçük bir brülör aynı işi görür.",
     "HE_Albion_SteamPower", (1, 1), "gas_lamp", 4, 1500, stuff=None, cost={"Steel": 45, "ComponentIndustrial": 1}, hp=120,
     fill=0.2, glow=(11, "(255,214,140,0)"), comps=LAMP_POWER, draw_size="(1,1.8)", category="Furniture",
     extra={"building": {"ai_chillDestination": False}})
deco("Albion", "GrandfatherClock", "grandfather clock", "dede saati",
     "A tall case clock of carved oak with a brass pendulum, wound once a week. Its slow tick is the sound of a well-run house.",
     "Pirinç sarkaçlı, oymalı meşeden uzun bir ayaklı saat; haftada bir kurulur. Yavaş tik takı düzenli bir evin sesidir.",
     "HE_Albion_JointStock", (1, 1), "grandfather_clock", 14, 3000, stuff=("Woody",), stuff_count=90,
     cost={"Steel": 20, "ComponentIndustrial": 1}, hp=140, fill=0.3, draw_size="(1,1.8)", category="Art")
deco("Kemet", "Sphinx", "sphinx", "sfenks",
     "A lion with the head of a king, wearing the striped royal headcloth, carved to keep watch over a gate or a tomb. Kemet says its builders still dream behind its eyes.",
     "Çizgili kraliyet başlığını takmış, kral başlı bir aslan; bir kapıyı ya da mezarı beklemek için yontulur. Kemet, yapanların hâlâ onun gözlerinin ardında rüya gördüğünü söyler.",
     "HE_Kemet_ChildrenOfSun", (2, 1), "sphinx", 34, 12000, stuff_count=240, hp=600, passability="Impassable", fill=0.6,
     draw_size="(2.2,1.55)", category="Art", minify=False)
deco("Kemet", "LotusLamp", "lotus lamp", "nilüfer kandili",
     "A bronze stand crowned with an open lotus flower that holds an oil flame. The lotus closes at night and opens at dawn, and so does the light of Kemet.",
     "Tepesinde yağ alevi taşıyan açık bir nilüfer çiçeği olan bronz bir ayak. Nilüfer gece kapanır, şafakta açılır; Kemet'in ışığı da öyle.",
     "HE_Kemet_Scribes", (1, 1), "lotus_lamp", 6, 1200, stuff=("Metallic",), stuff_count=40, hp=100, fill=0.2,
     glow=(9, "(255,190,110,0)"), comps=wood_fire(1.2, 12, 0.22, "(0,0,0.5)"), draw_size="(1,1.56)", category="Furniture",
     extra={"tickerType": "Normal", "building": {"ai_chillDestination": False}})
deco("Pars", "FireAltar", "fire altar", "ateş sunağı",
     "A stepped altar of white stone whose fire must never go out. The priests feed it fragrant wood day and night, and the household gathers around its warmth.",
     "Ateşi asla sönmemesi gereken beyaz taştan basamaklı bir sunak. Rahipler onu gece gündüz kokulu odunla besler, ev halkı da sıcaklığının çevresinde toplanır.",
     "HE_Pars_SatrapLaw", (1, 1), "fire_altar", 10, 2600, stuff_count=70, hp=250, fill=0.4,
     glow=(10, "(252,180,100,0)"), comps=wood_fire(2.0, 20, 0.4, "(0,0,0.32)", heat=6), draw_size="(1,1.48)", category="Temperature",
     extra={"tickerType": "Normal", "building": {"ai_chillDestination": False}})
deco("Pars", "Lamassu", "lamassu", "lamassu",
     "A winged bull with a crowned human head, carved in stone to guard the gates of kings. It is carved with five legs, so that it stands still from the front and strides from the side.",
     "Kralların kapılarını korumak için taşa oyulmuş, taçlı insan başlı kanatlı bir boğa. Beş bacaklı yapılır; önden bakınca durur, yandan bakınca yürür.",
     "HE_Pars_TenThousand", (2, 1), "lamassu", 32, 12000, stuff_count=240, hp=600, passability="Impassable", fill=0.6,
     draw_size="(2,1.64)", category="Art", minify=False)
deco("Inti", "SunDisc", "sun disc", "güneş diski",
     "A face of the sun beaten from gold and raised on a stone stand. In the temple of the sun such discs caught the dawn and filled the hall with light.",
     "Altından dövülmüş ve taş bir ayağa yerleştirilmiş bir güneş yüzü. Güneş tapınağında bu diskler şafağı yakalar, salonu ışıkla doldururdu.",
     "HE_Inti_KnotKeepers", (1, 1), "sun_disc", 22, 4000, stuff_count=50, cost={"Gold": 25}, hp=200, fill=0.3,
     draw_size="(1,1.64)", category="Art")
deco("Inti", "PumaStone", "puma stone", "puma taşı",
     "A crouching puma carved from a single block. The puma guards the world of the living, between the condor above and the serpent below.",
     "Tek bir bloktan yontulmuş, çömelmiş bir puma. Puma, yukarıdaki kondor ile aşağıdaki yılanın arasında, yaşayanların dünyasını korur.",
     "HE_Inti_Mita", (2, 1), "puma_stone", 28, 10000, stuff_count=200, hp=550, passability="Impassable", fill=0.6,
     draw_size="(2,1.33)", category="Art", minify=False)


# ------------------------------------------------------------------ defensive structures
def ammo(label_en, label_tr, out_en, out_tr, things, capacity, multiplier):
    return {"@Class": "CompProperties_Refuelable", "fuelLabel": T(label_en, label_tr), "fuelGizmoLabel": T(label_en, label_tr),
            "outOfFuelMessage": T(out_en, out_tr), "fuelFilter": {"thingDefs": list(things)},
            "fuelCapacity": capacity, "fuelMultiplier": multiplier, "initialFuelPercent": 0, "autoRefuelPercent": 0.5, "showFuelGizmo": True,
            "minimumFueledThreshold": 1, "factorByDifficulty": True, "consumeFuelOnlyWhenUsed": True}


def arrows():
    return ammo("Arrows", "Oklar", "Needs wood for arrows", "Ok için odun gerekli", ["WoodLog"], 60, 2)


def stones():
    return ammo("Stones", "Taşlar", "Needs stone chunks", "Taş yığını gerekli",
                ["ChunkGranite", "ChunkLimestone", "ChunkMarble", "ChunkSandstone", "ChunkSlate"], 40, 10)


def turret_research(nation, key, en, tr, den, dtr, cost, tech, prereq):
    col, row = free_slot(nation, tech)
    return research(nation, key, en, tr, den, dtr, cost, tech, col, row, prereqs=[prereq], knowledge=40)


def turret(nation, key, en, tr, den, dtr, gun_en, gun_tr, research_name, base_style, top_kind, bullet, burst, cooldown, rng, acc,
           cost, work, hp, ammo_comp, sound, min_range=0, skill=5, flammability=1.0, miss=0):
    name = f"HE_{nation}_{key}"
    gun = name + "_Gun"
    top = f"HeirsOfEarth/Buildings/{name}_Top"
    verb = {"verbClass": "Verb_Shoot", "defaultProjectile": bullet, "warmupTime": 0, "range": rng, "minRange": min_range or None,
            "ticksBetweenBurstShots": 9 if burst > 1 else None, "burstShotCount": burst, "soundCast": sound, "consumeFuelPerShot": 1,
            "forcedMissRadius": miss or None}
    add(f"Things/HE_Buildings_{nation}.xml", Def(
        "ThingDef", gun, parent="BaseWeaponTurret", label=T(gun_en, gun_tr),
        description=T(f"The turning top of the {en}.", f"{tr} yapısının dönen üst kısmı."),
        graphicData={"texPath": top, "graphicClass": "Graphic_Single"},
        statBases={"AccuracyTouch": acc[0], "AccuracyShort": acc[1], "AccuracyMedium": acc[2], "AccuracyLong": acc[3],
                   "RangedWeapon_Cooldown": cooldown, "DeteriorationRate": 0, "Mass": 30, "Flammability": 0.5},
        verbs=[verb]))
    tex(top, "turret_top", kind=top_kind)
    add(f"Things/HE_Buildings_{nation}.xml", Def(
        "ThingDef", name, parent="BuildingBase", label=T(en, tr), description=T(den, dtr),
        thingClass="Building_TurretGun", drawerType="MapMeshAndRealTime", drawHighlight=True, drawHighlightOnlyForHostile=True,
        graphicData={"texPath": f"HeirsOfEarth/Buildings/{name}", "graphicClass": "Graphic_Single", "drawSize": "(2,2)",
                     "damageData": {"rect": "(0.2,0.2,0.6,0.6)"}, "shadowData": {"volume": "(1.5,0.35,1.4)", "offset": "(0,0,-0.05)"}},
        altitudeLayer="Building", stealable=False, rotatable=False, size="(2,2)",
        statBases={"MaxHitPoints": hp, "Flammability": flammability, "WorkToBuild": work, "Mass": 60, "Beauty": -4, "ShootingAccuracyTurret": 0.9},
        tickerType="Normal", passability="PassThroughOnly", pathCost=50, fillPercent=0.5, hasTooltip=True,
        costList=cost, terrainAffordanceNeeded="Light", designationCategory="Security", constructionSkillPrerequisite=skill,
        building={"ai_combatDangerous": True, "turretGunDef": gun, "turretBurstCooldownTime": cooldown, "turretTopDrawSize": 2.0,
                  "turretTopOffset": "(0, 0.05)"},
        placeWorkers=["PlaceWorker_TurretTop", "PlaceWorker_ShowTurretRadius"],
        researchPrerequisites=[research_name],
        comps=[{"@Class": "CompProperties_Forbiddable"}, ammo_comp],
        modExtensions=[culture(nation)]))
    tex(f"HeirsOfEarth/Buildings/{name}", "turret_base", size=(2, 2), style=base_style)
    return name


ARROW_TEX = "Things/Projectile/Arrow_Small"
STONE_TEX = "HeirsOfEarth/Projectiles/HE_Stone_Inti"

# Nova Roma
turret("Roma", "Scorpio", "scorpio", "skorpio",
       "A torsion bolt thrower on a stone platform. Twisted sinew springs send a heavy iron-tipped bolt through a shield and the man behind it. It shoots one bolt at a time, slowly, but very far and very hard. Wood is cut into new bolts: one log makes two.",
       "Taş bir platform üzerinde burulmalı bir ok atıcı. Bükülmüş sinir yaylar ağır, demir uçlu bir oku kalkanın ve arkasındaki adamın içinden geçirir. Tek tek ve yavaş atar ama çok uzağa ve çok sert. Odun yeni oklara dönüşür: bir kütük iki ok eder.",
       "scorpio", "skorpio",
       turret_research("Roma", "Scorpio", "scorpio", "skorpio",
                       "The legion's artillery: a bolt thrower small enough to set on a wall, strong enough to pin a man to a tree at three hundred paces.",
                       "Lejyonun topçusu: bir surun üstüne konacak kadar küçük, üç yüz adımdan bir adamı ağaca çivileyecek kadar güçlü bir ok atıcı.",
                       1400, "Medieval", "HE_Roma_Manuballista"),
       "stone", "scorpio", projectile("HE_Bolt_Scorpio", "scorpio bolt", "skorpio oku", "Arrow", 36, 60, ARROW_TEX, pen=0.38),
       1, 4.0, 32.9, (0.6, 0.8, 0.82, 0.7), {"WoodLog": 80, "Steel": 60, "BlocksGranite": 40}, 9000, 320,
       arrows(), "Bow_Large", flammability=0.6)

# Yamato
turret("Yamato", "Yagura", "yagura", "yagura",
       "A small timber watchtower with white plaster walls. Three bows set on a turning frame loose a short volley at once. Wood for new arrows: one log makes two.",
       "Beyaz sıvalı küçük bir ahşap gözcü kulesi. Dönen bir çerçeveye kurulu üç yay aynı anda kısa bir yaylım atar. Yeni oklar için odun: bir kütük iki ok eder.",
       "tower bows", "kule yayları",
       turret_research("Yamato", "Yagura", "yagura", "yagura",
                       "Castle builders learn to raise arrow towers at the corners of the walls, where archers can shoot along them.",
                       "Kale ustaları surların köşelerine, okçuların sur boyunca atabileceği ok kuleleri dikmeyi öğrenir.",
                       1300, "Medieval", "HE_Yamato_Kyudo"),
       "yagura", "multibow", projectile("HE_Arrow_Yagura", "tower arrow", "kule oku", "Arrow", 12, 50, ARROW_TEX, pen=0.16),
       3, 4.2, 30.9, (0.5, 0.66, 0.58, 0.42), {"WoodLog": 140, "Steel": 30}, 8000, 260, arrows(), "Bow_Recurve")

# Nordheim
turret("Nord", "BowLoft", "bow loft", "yay çardağı",
       "A log platform with a huge twin bow on a pivot, the kind that once guarded the fjord gates. It shoots two great arrows at a time over long range. Wood for new arrows: one log makes two.",
       "Bir mil üzerinde dev bir çift yay taşıyan kütük platform; bir zamanlar fiyort kapılarını koruyanlardan. Uzun menzile ikişer büyük ok atar. Yeni oklar için odun: bir kütük iki ok eder.",
       "twin bow", "çift yay",
       turret_research("Nord", "BowLoft", "bow loft", "yay çardağı",
                       "Hunters and shipwrights put their skills together: a bow too big to draw by hand, spanned with a winch.",
                       "Avcılar ve gemi ustaları becerilerini birleştirir: elle gerilemeyecek kadar büyük, bir vinçle gerilen bir yay.",
                       1300, "Medieval", "HE_Nord_HuntBow"),
       "loft", "longbow", projectile("HE_Arrow_BowLoft", "great arrow", "büyük ok", "Arrow", 14, 55, ARROW_TEX, pen=0.20),
       2, 3.6, 34.9, (0.5, 0.68, 0.62, 0.5), {"WoodLog": 150, "Steel": 40}, 8500, 280, arrows(), "Bow_Large")

# Hellas
turret("Hellas", "Lithobolos", "lithobolos", "lithobolos",
       "A torsion stone thrower on a marble platform. Its arm hurls a stone the size of a head that breaks bones and shields alike. It cannot hit anything closer than six cells and is slow, but it reaches very far. Feed it stone chunks: one chunk makes ten stones.",
       "Mermer bir platform üzerinde burulmalı bir taş atıcı. Kolu, kemiği de kalkanı da kıran kafa büyüklüğünde bir taş fırlatır. Altı kareden yakını vuramaz ve yavaştır ama çok uzağa erişir. Taş yığınıyla beslenir: bir yığın on taş eder.",
       "throwing arm", "atış kolu",
       turret_research("Hellas", "Lithobolos", "lithobolos", "lithobolos",
                       "The engineers of the city measure springs and angles until a machine throws stones further than any slinger.",
                       "Şehrin mühendisleri yayları ve açıları ölçer, ta ki bir makine taşı her sapancıdan daha uzağa atana kadar.",
                       1500, "Medieval", "HE_Hellas_Geometry"),
       "stone", "lithobolos", projectile("HE_Stone_Lithobolos", "hurled stone", "fırlatılmış taş", "Blunt", 34, 34, STONE_TEX, pen=0.32),
       1, 4.6, 36.9, (0.3, 0.6, 0.7, 0.6), {"WoodLog": 100, "Steel": 50, "BlocksMarble": 40}, 9500, 340,
       stones(), "Bow_Large", min_range=5.9, flammability=0.6)

# Albion
turret("Albion", "FieldCannon", "field cannon", "sahra topu",
       "A bronze cannon on a wooden carriage behind a ring of sandbags. Each shell bursts where it lands. It cannot fire at anything closer than eight cells, and the gunners need time to swab and reload. Steel is cast into shells: four steel make one shell.",
       "Bir kum torbası halkasının ardında, ahşap bir kızak üzerinde bronz bir top. Her mermi düştüğü yerde patlar. Sekiz kareden yakına ateş edemez ve topçuların temizleyip yeniden doldurması zaman alır. Çelik mermiye dökülür: dört çelik bir mermi eder.",
       "cannon", "top",
       turret_research("Albion", "FieldCannon", "field cannon", "sahra topu",
                       "Drilled gun crews and cast bronze barrels: the artillery that won the empire's battles.",
                       "Talimli top ekipleri ve dökme bronz namlular: imparatorluğun savaşlarını kazanan topçu.",
                       1800, "Industrial", "HE_Albion_Drill"),
       "gunpit", "cannon", projectile("HE_Shell_FieldCannon", "cannon shell", "top mermisi", "Bomb", 44, 46, STONE_TEX, pen=0.3, explosive_radius=2.1),
       1, 7.0, 40.9, (0.2, 0.5, 0.55, 0.45), {"Steel": 160, "WoodLog": 60, "ComponentIndustrial": 3}, 12000, 400,
       ammo("Shells", "Mermiler", "Needs steel for shells", "Mermi için çelik gerekli", ["Steel"], 20, 0.25),
       "Mortar_LaunchA", min_range=7.9, skill=6, flammability=0.4, miss=1.9)

# New Kemet
turret("Kemet", "ArcherPylon", "archer pylon", "okçu pilonu",
       "A sloped sandstone tower top painted with blue bands, where four composite bows on a turning stand shoot together. The volley is quick but the arrows are light. Wood for new arrows: one log makes two.",
       "Mavi şeritlerle boyanmış eğimli bir kum taşı kule tepesi; dönen bir ayaktaki dört kompozit yay birlikte atar. Yaylım hızlıdır ama oklar hafiftir. Yeni oklar için odun: bir kütük iki ok eder.",
       "pylon bows", "pilon yayları",
       turret_research("Kemet", "ArcherPylon", "archer pylon", "okçu pilonu",
                       "The temple gates become fortresses: archers on the pylons can cover the whole avenue of sphinxes.",
                       "Tapınak kapıları kaleye dönüşür: pilonların üstündeki okçular bütün sfenks yolunu kapsayabilir.",
                       1300, "Medieval", "HE_Kemet_CompositeBow"),
       "pylon", "pylonbows", projectile("HE_Arrow_Pylon", "pylon arrow", "pilon oku", "Arrow", 10, 48, ARROW_TEX, pen=0.14),
       4, 4.8, 28.9, (0.5, 0.62, 0.5, 0.34), {"WoodLog": 90, "BlocksSandstone": 60, "Steel": 30}, 8500, 300,
       arrows(), "Bow_Recurve", flammability=0.6)

# Pars
turret("Pars", "NaftThrower", "naft thrower", "neft atıcı",
       "A bronze tank of naft, the burning oil of the eastern wells, with a long siphon that sprays fire in short bursts. Its reach is short, but whatever it touches burns. Fill it with chemfuel: one unit makes one burst.",
       "Doğu kuyularının yanan yağı neftle dolu bronz bir tank ve kısa püskürtmelerle ateş saçan uzun bir sifon. Menzili kısadır ama dokunduğu her şey yanar. Kimyasal yakıtla doldurulur: bir birim bir püskürtme eder.",
       "naft siphon", "neft sifonu",
       turret_research("Pars", "NaftThrower", "naft thrower", "neft atıcı",
                       "The kings' engineers learn to pump naft through a bronze pipe and light it at the mouth.",
                       "Kralların mühendisleri nefti bronz bir borudan pompalayıp ağzında tutuşturmayı öğrenir.",
                       1500, "Medieval", "HE_Pars_Immortals"),
       "tiles", "naft", projectile("HE_Naft_Pars", "naft spray", "neft püskürtmesi", "Flame", 11, 30, "Things/Projectile/Bullet_Small", pen=0.05),
       4, 4.5, 18.9, (0.8, 0.7, 0.4, 0.2), {"Steel": 90, "BlocksSandstone": 40, "Chemfuel": 30}, 9000, 280,
       ammo("Naft", "Neft", "Needs chemfuel", "Kimyasal yakıt gerekli", ["Chemfuel"], 40, 1), "Bow_Recurve", flammability=0.4)

# Inti
turret("Inti", "SlingStand", "sling stand", "sapan kulesi",
       "A ring of fitted stones with a long sling arm on a pivot and a basket of round stones. It whirls three stones in a row at anyone who comes close. Feed it stone chunks: one chunk makes ten stones.",
       "Geçme taşlardan bir halka, bir mil üzerinde uzun bir sapan kolu ve bir sepet yuvarlak taş. Yaklaşan herkese art arda üç taş savurur. Taş yığınıyla beslenir: bir yığın on taş eder.",
       "sling arm", "sapan kolu",
       turret_research("Inti", "SlingStand", "sling stand", "sapan kulesi",
                       "The slingers of the empire teach the mountain forts to whirl stones without a hand on the cord.",
                       "İmparatorluğun sapancıları dağ kalelerine ipe el değmeden taş savurmayı öğretir.",
                       1300, "Medieval", "HE_Inti_Slingers"),
       "inti", "sling", projectile("HE_Stone_SlingStand", "sling stone", "sapan taşı", "Blunt", 11, 44, STONE_TEX, pen=0.12),
       3, 4.0, 30.9, (0.45, 0.62, 0.55, 0.4), {"WoodLog": 80, "BlocksGranite": 80}, 8000, 320, stones(), "Bow_Recurve", flammability=0.3)
