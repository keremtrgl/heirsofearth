# Changelog

Every release of Heirs of Earth, newest first. These are the same notes that appear on the [Steam Workshop change log](https://steamcommunity.com/sharedfiles/filedetails/changelog/3845334110).

## Heirs of Earth 4.3.0 - The Electric Age


- A fourth age. After the Age of Steam, each nation now goes on to the Electric Age. At the usual pace a nation reaches it after about 14 years; everything that speeds up or holds back the other ages works the same way here. A letter and a chronicle entry announce it, and a setback never takes the age away once it is reached.
- 9 new firearms, one per nation, all hand-drawn, each level with the closest vanilla gun and each with one strength of its own: the Roman self-loading rifle, the Yamato sniper rifle with a brass telescope, the Nordic trench gun (a pump shotgun with heavy shot), the Hellenic mountain carbine, the Tianxia box pistol (fires short bursts), the Albion light machine gun (pan-fed, six-round bursts, more steel and fewer components than most), the Nile carbine, the Persian long rifle (the longest reach of the age) and the Inti light carbine (the lightest and cheapest).
- 9 steel helmets, one per nation, each in the nation's colour and drawn for every side: the legion steel helmet, the Yamato, Nordic, Hellenic, Tianxia, Albion and Inti steel helmets, the Kemetic sun helmet and the Persian spiked helmet.
- 9 field uniforms, one per nation, in drab colours with the nation's own collar, buttons and pockets, drawn for all five body types and every side.
- Electric Age troops carry the new gun about two times in five, wear the field uniform about half the time and the steel helmet about half the time. Nothing they wear clashes. Leaders keep their own regalia.
- 9 powered buildings, one per nation, all hand-drawn:
  - Roman electric fountain: beauty 28, lit blue at night, colonists rest at it (150 W).
  - Yamato electric tea urn: colonists gather at it to share tea (150 W).
  - Nordic electric forge: makes everything a smithy makes, 25% faster, including bills from other mods (250 W).
  - Hellenic lamp-lit lectern: +6% research speed for a research bench nearby while powered (200 W).
  - Tianxia silk printing press: +12% work speed for a tailoring bench nearby while powered (250 W).
  - Albion telegraph office: while powered, +1 goodwill every quadrum with each heir nation that is not hostile. Only one office counts (200 W).
  - Kemetic irrigation pump: plants within 6 cells grow 15% faster while powered (300 W).
  - Persian electric carpet loom: every bill of the carpet loom, 40% faster (250 W).
  - Inti cold store: storage where food rots at a third of the normal speed while powered (400 W).
- 18 new research projects: each nation's electric army (3000) and its works (2600). Traders sell, and your colony may research, a nation's Electric Age items once that nation has reached the age; if it is your heritage, at any time.
- The World Fair. The first nation to reach the Electric Age holds a fair (if it is hostile to you, the next nation to get there that is not). You may send your colony's best art piece, weapon or book; it comes back by drop pod about ten days later with silver, goodwill with the hosts and every peaceful nation, and knowledge of the host, all growing with its quality (from 150 silver for a normal piece to 1200 for a legendary one). A masterwork or legendary exhibit wins the grand prize: more goodwill everywhere and a chronicle entry. Declining costs 3 goodwill with the hosts. It happens once per game and follows the world events setting.
- The Heirs tab and the encyclopedia show the fourth age.
- Fixed: the fourth game speed button could sit partly off the right edge of the screen. The speed row now grows to the left and always stays on screen.
- Save compatible. Nations already far along may reach the Electric Age soon after loading; each announces it once.

---

## Heirs of Earth 4.2.1 - Maintenance


### Performance
- Storehouses (the Inti qullqa): the slower rot used to look up every storehouse on the map for every rotting item on every tick. Each map's storehouse cells are now remembered and refreshed every 250 ticks (about four seconds), so a map without a storehouse costs almost nothing, and a storehouse you build or tear down takes effect within a few seconds.
- The Heirs tab no longer creates a new bar texture every frame for the knowledge and ages bars. Over a long session this slowly used up memory; the bars now share one texture per nation.
- The list of each nation's age arms and uniforms is worked out once and remembered, instead of on every trader visit and every soldier that is generated.
- The ages tooltip in the Heirs tab is only built when you actually hover over a nation.

### Ages of Progress: pace
- The ages came too fast. In a ten-year test world with the usual peace, allies and towns, most nations reached the Age of Steam in four to six years. The thresholds are now 3 years for the Age of Powder and 9 years for the Age of Steam (were 2.5 and 7) at the base pace. In the same test world the nations now reach the Age of Powder after 1.6 to 3 years and the Age of Steam after 4.8 to 9 years, depending on their rulers, wars and allies.
- Saves from 4.2.0 keep every age a nation has already reached; only the progress toward the next age follows the new thresholds.

### Ages of Progress: firearms
- Fairer costs and stats. Powder arms are cheaper (45 steel, 25 wood, no components) but slower to reload and less accurate at range than a bolt-action rifle. Steam rifles now stand level with the vanilla bolt-action rifle (warmup 1.7 s, range 37, cooldown 1.5 s) and cost 55 steel, 15 wood and 2 components.
- Every nation's gun now has its own strength:
  - Roman arquebus: the most accurate of the powder arms.
  - Nordic hook gun: fires a heavy ball (28 damage, 45% armour penetration), but reloads slowest.
  - Hellenic musket: a long bayonet that stabs well in melee.
  - Tianxia bird gun: the longest reach of the powder arms (31 tiles) and better at range.
  - Kemetic musket: a longer barrel (29 tiles).
  - Inti arquebus: light and quick to raise (warmup 1.5 s, 3.2 kg) and the cheapest (40 steel).
  - Yamato rifle: the most accurate at long range, with a long bayonet.
  - Nordic rifle: the fastest to work the bolt (cooldown 1.2 s).
  - Hellenic rifle: very accurate at every range, with a bayonet.
  - Tianxia rifle: made in workshops at scale: much quicker to make, 45 steel and one component.
  - Albion breech-loading rifle: the fastest to aim and to reload (warmup 1.2 s, cooldown 1.3 s).
  - Persian rifle: the longest range of all (42 tiles) and good at long range.
- The descriptions of the guns tell you their strength (in English and Turkish).

### Heirs tab
- The ten tabs of the Heirs tab now sit in two rows of five. In one row each tab was under 100 pixels wide and the longer names (Encyclopedia, Culture knowledge) ran into each other.

### Names
- In long wars the game could log "Could not get new name" for a nation's men or women. RimWorld keeps every living pawn's short name unique, and it takes a person's short name from either the first or the family name. Each nation now has more than 40 family names (were 12 to 18), and about 40 to 90 more first names per gender. Roman women now carry a feminine cognomen as their family name, as in "Cornelia Prisca", instead of a second nomen that was also a first name. Each nation now has room for roughly 140 to 230 distinct people per gender.

### Testing
- The automated test now also checks the storehouse cache, the shared bar textures, the name pools (50 men and 50 women per nation at once, all with distinct short names) and runs a ten-year world (wars, rulers, allies and ages) to watch the pace.
- Fixed three tests that could fail by chance: the lyceum test spot, the saved treaty count, and the troop test, whose 720 throwaway soldiers stayed among the world's dead and used up names that the name test then needed.
- The test now copies the mod's assembly into the game folder outright and checks it, after a run once kept an older copy.

Save compatible.

---

## Heirs of Earth 4.2.0 - Ages of Progress


- The nations now progress. Each one moves through three ages, the Age of Founding, the Age of Powder and the Age of Steam, as the years pass. At the usual pace a nation reaches the Age of Powder after about two and a half years and the Age of Steam after about seven; each nation starts a little ahead or behind the others.
- What sets the pace: peace and steady growth; a scholarly ruler (+50%); each ally (+15%); a science treaty with you (+25%); a trade road with you (+10%); many towns (up to +30%). War slows a nation down (-40%). A famine or plague costs it progress, less if you sent help. A setback never takes an age away once it is reached.
- A letter and a chronicle entry announce each new age, with the ruler and the new arms and uniforms.
- 12 new firearms, all hand-drawn. Age of Powder: the Roman arquebus, the Nordic hook gun, the Hellenic musket, the Tianxia bird gun, the Kemetic musket and the Inti arquebus. Age of Steam: the Yamato rifle, the Nordic rifle, the Hellenic rifle, the Tianxia rifle, the Albion breech-loading rifle and the Persian rifle inlaid in khatam. Seven existing guns (the Roman and Inti carbines, the tanegashima, the Albion musket and rifle, the Kemetic desert rifle and the jezail) now also belong to their nation's ages.
- 9 new uniform coats, one per nation, in the nation's own colour, drawn for all five body types and every side: the Roman legion field coat, the Yamato army coat, the Nordic greatcoat, the Greek evzone dress with fustanella, the Tianxia new army coat, the Albion rifle green jacket, the Kemetic field coat, the Persian chokha and the Inti field coat.
- Troops follow their nation's age. In the Age of Powder about half of a nation's gunmen carry its powder arms; in the Age of Steam most carry its rifles and about half wear the uniform. Leaders keep their own regalia.
- Traders sell a nation's new arms and uniforms only once it has reached their age. Your colony may research them then too (15 new research projects); if the nation is your heritage, you may research them at any time.
- The Heirs tab has a new "Ages of the nations" section showing each nation's age, its progress to the next and, on hover, what speeds it up or holds it back and what each age brings. The encyclopedia shows each nation's age as well.
- New: a fourth game speed button. RimWorld has a fastest speed (15x) that is normally hidden; it now has its own button next to the other three, its icon made from the game's own arrows, and its key (4 by default) can be changed in the keyboard settings. Like the third speed, it slows down by itself when something needs your attention.
- Mod settings: the fourth speed button, the ages and the pace of the ages (25% to 400%) can each be changed. With the ages turned off, nations keep their old arms and everything can be researched as before.
- Save compatible. In an existing save, every nation starts in the Age of Founding with a small random head start.

---

## Heirs of Earth 4.1.0 - Dress of the Nations


- Every heir tunic, robe, coat, cloak and suit of armour (26 pieces) now has its own hand-drawn look when worn, for all five body types and from every side. Before this they borrowed vanilla graphics such as the plate armour, duster and robe.
- Armour: the Roman lorica segmentata with shoulder guards and leather pteruges, the samurai do-maru with laced tassets, the Tianxia lamellar with its breast mirror, the Nordic mail byrnie, the Parsian and Kemetic scale, the Greek linothorax, the Inca quilted armour with its sun disc.
- Clothing: the redcoat with white crossbelts, the frock coat, toga with its purple border, tunica with clavi, chiton, himation, kimono with obi, kamishimo, hanfu, the dragon robe, kaftan, candys, kalasiris with its broad collar, the Nordic tunic and fur cloak, the unku with tocapu squares.
- The material still colours the cloth or metal; trims, gold, lacing and dyes keep their own colours.
- Fix: the Inca feather cape and the Kemet leopard mantle used the Royalty cape graphic, which a game without Royalty cannot show. They now have their own.
- Fix: hats, helmets and crowns (since 3.6) did not take the colour of their material in game, because their colour masks were misnamed. Steel helmets now look like steel, gold crowns like gold, and every new garment is tinted the same way. A test now checks the real material the game builds.
- New Steam screenshots: a close look at each nation's dress, and every older scene shot again in the new garments.
- Save compatible.

---

## Heirs of Earth 4.0.0 - the great update (everything since 3.2: Art of War, Palace and Treaty, Epics, Sound and Sight, Common Ground)


### Art of war
- Every nation raids with its own war doctrine and drill: the Roman testudo, the Greek phalanx, Nordic shore raids, Yamato bushido, Tianxia's art of war, Albion's siege train, the Kemet chariot vanguard, Pars cavalry wings and Inti mountain sappers. Each changes the raid plan and gives raiders a fitting bonus while they fight (formation armour, speed, aim, melee). Scripted and other mods' raids are untouched; a setting turns doctrines off.
- Nation pack animals: horses, donkeys, yaks, dromedaries and alpacas walk with each nation's caravans, and every heir start brings its nation's animal.
- New counterweight trebuchet for every heir: manned, fed with stone chunks, hurls boulders over walls at long range.
- Fix: on frozen maps heir soldiers no longer swap their uniform for random warm clothes.

### Palace and treaty
- Every nation has a ruler with a name, epithet and temperament (warlike, mercantile, scholarly, pious, cautious). Reigns end, crowns pass, and a new ruler may change course.
- Four treaties: peace, trade, science exchange and defensive alliance, each with a fee and a goodwill threshold; rulers sometimes offer one for free. Breaking a treaty costs goodwill everywhere.
- New embassy building, needed for the higher treaties.
- Titles of standing, up to each nation's own highest honour (honorary citizen of Nova Roma, friend of the Pharaoh, kin of the Sun and more).
- World events: the Games, great fairs, famine and plague.
- Fix: when a reign ends, the crown always passes to someone new (the game could hand it back to the old ruler).

### Epics
- 18 classic books (two per nation) and 9 legendary great books, in each nation's own form: codices, rune boards, scrolls, bamboo slips, khipu cords. Reading teaches culture knowledge; better copies teach faster.
- A second saga for every nation: five steps ending with a lost original to return or keep, and the nation's great book either way.
- Errands: friendly nations ask small favours by letter (goods, fine crafts, books) for silver, knowledge and goodwill.
- Fix: a story choice now takes a forbidden relic too.

### Sound and sight
- Every nation has its own music, made for this mod, and a short signature call that sounds with its news. Its music plays when its story ends, when it honours you or when you win its Games, and now and then among the usual songs (your heritage and nations that honoured you). A setting turns it off.
- 18 heir weapons got their own firing sounds (muskets, matchlock, flintlock, blunderbuss, cannon, scorpio, manuballista, trebuchet, sling, repeating crossbow, fire lance, naft, fire arrows, harpoon), and three artifacts their own calls.
- All 19 heir hats, helmets, crowns and wreaths now have their own look when worn, from all sides (five were invisible before). The stuff colours the main part; plumes, gold and jewels keep their colours.
- The laurel, olive wreath, circlet and mascaypacha now sit on the hair instead of hiding it, like the vanilla coronet.
- Fix: nation calls no longer go silent after loading an earlier save.

### Common ground
- Every nation can be switched off on its own in the settings: it keeps its faction and goods but leaves stories, errands, letters, music and world politics.
- A translation template folder with every text in English and a short guide, for anyone translating the mod.
- A world where an heir nation has fallen keeps running cleanly.
- The "Translation data for language Turkish has errors" warning comes from the official language pack, not from this mod.

### DLC extras
- Royalty: the khepresh, kidaris and mascaypacha count as a noble's crown (Baron to Consul); the laurel, nemes and circlet as a coronet (Baron and Count). Without Royalty nothing changes.

### Technical
- About 380 new automatic in-game checks since 3.2 (about 2,880 in all); the full suite passes.
- Save compatible: rulers are crowned and new systems start when an older save is loaded.

---

## Heirs of Earth 3.7.0 "Common Ground"


Playing alongside other mods and in other languages.

### Nations on and off (new)
- Every nation can be switched off in the mod settings, one by one. Useful with many faction mods.
- A nation switched off keeps its faction, towns, goods and research, but it is no longer added to saves that lack it, starts no stories, sends no errands or letters, plays no music and leaves the politics of the world (wars, alliances, envoys, the court, treaties, the council and world events). Switch it back on and it takes part again.
- The traditions of each nation can still be switched off on their own, as before.

### Translation template (new)
- The mod now ships a TranslationTemplate folder with every text of the mod in English (definitions and interface), laid out exactly as the game expects, and a short guide. The game does not load it.
- Translators copy it into Languages/<their language>, translate the text and are done. The complete Turkish translation is the example.

### Stability
- A world in which an heir nation has fallen, or was never created, keeps running cleanly: politics, errands, events, the court, treaties, the council and the stories all leave it out.

### Technical
- New automatic tests: switching a nation off (no politics, stories, music, errands or letters about it) and back on, a fallen nation over half a year of world events, and a check that none of the game's translation warnings come from this mod. (The "Translation data for language Turkish has errors" warning some players see comes from the official language pack's DLC entries, not from Heirs of Earth.)
- Two automatic tests (the trebuchet crew, the vanguard drill speed) no longer fail by chance.
- Save compatible.

---

## Heirs of Earth 3.6.0 "Sound and Sight"


The nine nations now sound and look like themselves.

### Music and calls (new)
- Every nation has its own piece of music, about one and a half to two and a half minutes long, made for this mod: brass and lyre over frame drums for Nova Roma, shakuhachi, koto and taiko for Yamato, fiddle and horn over deep drums for Nordheim, aulos and kithara for Hellas, dizi flute, guzheng and gong for Tianxia, fife, fiddle, lute and a marching drum for Albion, ney, harp and sistrum for Kemet, ney, santur and daf for Pars, and siku panpipes, charango and bombo for the Inti.
- Every nation also has a short signature call. It sounds when that nation's news reaches you: a story starting or moving on, an errand, a succession, a gift, a political event, the Games or a fair.
- A nation's music plays when one of its stories ends, when it honours you, and when your colonist wins its Games.
- Now and then the music of your heritage, and of nations that have made you one of their own, plays among the usual songs. Never the music of a stranger, and never during danger.
- A new setting turns all of it off.

### Weapon and artifact sounds (new)
- Eighteen heir weapons got their own firing sounds instead of borrowed vanilla ones: the musket and jezail, the tanegashima matchlock, the flintlock pistol, the blunderbuss, the field cannon, the scorpio and gastraphetes, the manuballista, the trebuchet and lithobolos, the sling and sling stand, the repeating crossbow, the fire lance, the naft thrower, the fire arrow battery and the harpoon gun.
- Three artifacts that used another nation's call now have their own: the Sun Disc (a sistrum), the King's Eye (a karnay horn) and the Golden Thread (a pututu shell trumpet).

### Worn headgear (new)
- All 19 heir hats, helmets, crowns and wreaths have their own look when worn, from three sides. Before, they borrowed vanilla helmets and hats, and five of them (the laurel, the olive wreath, the circlet, the mascaypacha and the kidaris) were invisible when worn.
- The shako, top hat and bicorne; the Corinthian helmet with its crest; the olive wreath and the golden laurel; the plumed helmet and the mascaypacha with its red fringe; the khepresh and the striped nemes; the spectacled Nordic helmet and the circlet; the winged helmet and the crenellated kidaris; the galea with cheek guards and crest; the Tianxia helmet with its tassel and curtain, and the winged futou; the kabuto with its gilded horns and the jingasa.
- The stuff an item is made of colours its main part, while plumes, crests, gold, cords and jewels keep their own colours.

### Fixes
- An automatic test of the trebuchet no longer fails when the crew needs longer to reach it.

### Technical
- New automatic tests: every nation's music and call, every weapon and artifact sound, the setting, playing a nation's music, heir music joining the rotation only for your patrons, and every worn headgear texture from all three sides with its colour mask.
- Save compatible.

---

## Heirs of Earth 3.5.0 "Epics"


The nations now have books, a second great story each, and small favours to ask of you.

### Books (new)
- 18 classic books, two for every nation, each with its own title and story: the Annals of Nova Roma, Ten Books on Building, The Brush and the Blade, the Diary of the Sakai Tea Masters, the Saga of the First Jarl, the Lay of the Long Winter, the Dialogues of the Academy, the Elements of the Geometers, the Analects of the Examination Hall, Thirteen Chapters on Strategy, the Commonwealth Almanac, A Treatise on the Steam Engine, the Instructions of the Scribe, the Book of the Second Sunrise, Verses of the Garden, the Book of the King's Road, and two khipu of the Inti.
- Every nation writes in its own way: leather codices, stitched books, rune boards, scrolls, bamboo slips and knotted khipu cords.
- Reading one teaches your colony that nation's culture knowledge every hour, up to what the book can teach (80 for the first book, 140 for the second). Better copies teach faster (an excellent copy teaches 40% more than a normal one, a legendary copy 80% more). Reading them is also a pleasure.
- Every nation's caravans and settlements sell its books. They can also turn up as quest rewards.

### Second sagas (new)
- Every nation has a second story, which begins once its first story is done and you know enough of the nation (or it is your heritage): The Burned Archive, The Silent Chronicle, The Skald's Last Song, The Sunken Library, The Hidden Historian, The Lost Charter, The Sealed Tomb, The Poet's Road and The Knots of the Sun.
- Five steps each: gather materials, raise a monument, master the nation's highest tradition, recover a lost original from a story site, and decide its fate.
- Return the original to its nation (goodwill, knowledge and silver) or keep it in your own archive (a fine relic, but the nation will not like it).
- Either way your scribes keep a fair copy: the nation's great book, a legendary book that teaches up to 300 knowledge, fast. The Founders' Codex, Chronicle of the Eight Islands, the Edda of Nordheim, The Song of the Long Voyage, Records of the Heavenly Court, The Great Charter, The Book of Coming Forth, The Book of Kings and The Royal Khipu.
- The Stories page shows which story a sequel is waiting for.

### Errands (new)
- Now and then a friendly nation asks a small favour by letter: plain goods for its storehouses, a fine piece of its own craft (good quality or better), or a book of another nation.
- Accept and the errand waits on the Stories page with the time left and its reward. Deliver it there for silver, culture knowledge and goodwill. At most three at once; fifteen days each; a broken promise costs a little goodwill.

### Fixes
- A story choice that asks for a relic now takes it even if it is forbidden. Before, the reward was paid but the relic stayed.

### Technical
- New automatic tests: every book (title, blurb, cover, trade tags, traders selling it), reading speed by quality and the knowledge cap, a real reading job, books in trader stock, every saga's data, a saga from start to great book, all three kinds of errand, delivering, quality, running out of time, the limit of three, and errands and sagas surviving save and load.
- Save compatible.

---

## Heirs of Earth 3.4.0 "Palace and Treaty"


The nations now have courts. Every nation is ruled by a ruler with a temperament, crowns pass from ruler to ruler, you can sign treaties with them, earn their titles, and the world has its own events.

### Rulers and succession (new)
- Every heir nation is ruled by its faction leader, shown with title, name and epithet, for example "Consul Gaius Valerius, the Bold".
- Every ruler has a temperament. Each nation leans toward its own (Nordheim toward warlike rulers, Hellas toward scholarly and mercantile ones, the Inti toward pious and cautious ones), but any temperament is possible.
- Warlike: seeks quarrels with rivals, demands half again as much tribute, offers defensive alliances.
- Mercantile: warms to every nation, offers trade treaties, likes to host great fairs.
- Scholarly: shares learning freely (a quarter more culture knowledge from that nation), offers science exchanges.
- Pious: keeps the festivals, may host the Games, offers peace.
- Cautious: often holds back from war, warms slowly to others, offers peace.
- A reign lasts four to ten years, then the crown passes to a new ruler with a new temperament. If a leader dies or is killed, the successor is noticed at once.
- A new ruler may revoke treaties with you when relations are poor, and a warlike rival may use the change of crown to start a war.

### Treaties (new)
- The Diplomacy page now shows every nation's court: its ruler, your standing there and the treaties you hold or can sign. Hover for the details.
- Peace (200 silver, goodwill 0+): the nation demands no tribute from you, and its goodwill rises a little every month.
- Trade (300 silver, goodwill 20+): a trade caravan from the nation visits every twenty days or so.
- Science exchange (500 silver, goodwill 30+, needs an embassy): 8 culture knowledge of the nation every month.
- Defensive alliance (800 silver, goodwill 60+, needs an embassy): when raiders attack your home, the nation often sends warriors to help (at most every ten days).
- Rulers sometimes offer the treaty that suits their temperament for free.
- A treaty ends when the nation turns hostile, or when a new ruler revokes it. You can cancel a treaty yourself, but the nation loses 15 goodwill and every other nation 3: word of a broken oath travels fast.

### Embassy (new)
- New shared research "embassies" and a 3x3 embassy building: a hall with a desk for letters and seals, chairs for the envoys and a banner for every nation.
- Needed for science exchanges and defensive alliances. With an embassy, every nation you hold a treaty with grows a little fonder of you each month.

### Titles (new)
- Your standing with each nation: stranger, guest, friend (40 goodwill), honoured friend (60 goodwill and two treaties).
- The highest honour is the nation's own: honorary citizen of Nova Roma, honoured guest of the shogun, sworn friend of the jarls, proxenos of the League, marquis of the outer realm, knight of the Commonwealth, friend of the Pharaoh, benefactor of the Satrap, kin of the Sun. It needs 80 goodwill, a defensive alliance and an embassy, is proclaimed in a letter and brings 4 culture knowledge every month.

### World events (new)
- The Games: Hellas (or a pious court) holds the Games. Send your best fighter: a win (the chance follows their melee or shooting skill) raises your goodwill with every nation and gives the champion a strong good mood; even taking part pleases the hosts.
- Great fair: a nation, often one with a mercantile ruler, opens a great fair, and caravans of several nations pass by your colony over the next days.
- Famine: a nation asks for food. Sending it brings goodwill and some of their knowledge.
- Plague: a nation asks for medicine. If you trade with them (a trade treaty or trade road), the sickness may travel your roads whatever you answer.
- New setting: "World events between the nations" to turn them off.

### Encyclopedia
- Each nation's page now shows its ruler and temperament.

### Technical
- New automatic tests: courts and honorary titles for every nation, succession (natural, after a death, after a long reign), temperament effects, signing all four treaties with their fees, the embassy requirement, monthly benefits (knowledge, caravans), allied help against a raid, cancelling and voiding treaties, a ruler's treaty offer, all four world events and their answers, and treaties and rulers surviving save and load.
- Save compatible. Rulers are crowned when an older save is first loaded.

---

## Heirs of Earth 3.3.0 "Art of War"


Every heir nation now makes war in its own way. Raids by a nation follow its war doctrine, its raiders fight with its drill, its caravans walk with its own animals, and every heir can build a manned trebuchet.

### War doctrines (new)
- Each nation prefers its own raid plan and way of arriving, and its raiders arrive with a drill that lasts while they fight for the raid. The drill leaves a raider who is downed, captured, recruited or goes home. The raid letter names the doctrine.
- Nova Roma, testudo: legions gather before they attack and walk in from the edge. Raiders close ranks: the more comrades stand within three cells, the more armour they gain (up to +20% sharp, +10% blunt), but packed together they march slowly.
- Hellas, phalanx: hoplites attack at once and fight shoulder to shoulder. Standing together they gain sharp armour, melee hit chance and dodge; alone they are ordinary soldiers.
- Nordheim, strandhogg: shore raiders breach walls with axes and run at you. Faster, hit harder in melee and feel less pain.
- Yamato, bushido: samurai attack in small bands from several sides and pick their targets with care. Better melee hit and dodge, less pain.
- Tianxia, art of war: armies gather out of reach, wait and then strike with drilled volleys. Better aim and faster aiming.
- Albion, siege train: often digs in and builds a battery before attacking (less often than the other doctrines take effect). Riflemen fire measured volleys: better aim, faster aiming, a little slower on foot.
- New Kemet, chariot vanguard: attacks at once from the edge, and its raiders run far faster than others.
- Pars, cavalry wings: several swift groups attack at once. Faster and better in melee.
- Inti, mountain sappers: diggers tunnel toward your walls. Better aim and surer feet.
- A doctrine only replaces a plan the game chose itself and only when it fits the raid, so scripted raids, quests and other mods' raids are not changed.
- The doctrine of each nation is shown on its encyclopedia page with its effects.
- New setting: "Nations raid with their war doctrines". Turn it off and heir raids behave like vanilla raids.

### Nation animals (new)
- Every nation's caravans walk with its own pack animals: horses and donkeys for Nova Roma, horses and yaks for Yamato, yaks for Nordheim, donkeys for Hellas, yaks and horses for Tianxia, horses for Albion, dromedaries for New Kemet and Pars, alpacas for the Inti. A few muffalo walk with every caravan so trade works in every biome.
- Vanilla only lets some animals carry caravan goods in each biome. Horses, donkeys and yaks are now allowed where they belong (horses and donkeys in temperate and arid lands, yaks in cold lands). Vanilla factions do not use them as carriers, so nothing changes for them.
- Every heir start brings the nation's own animal: a horse for Nova Roma, Yamato and Albion, a husky for Nordheim, a donkey for Hellas, a yak for Tianxia, a dromedary for New Kemet and Pars, an alpaca for the Inti.
- The encyclopedia names each nation's pack and herd animal.

### Trebuchet (new)
- New shared medieval research and defensive structure: the counterweight trebuchet (3x3). Any heir can build it, whatever their heritage.
- A colonist must man it, like a mortar. It hurls boulders over walls at enemies far out of bow range (57 cells), and they smash what they land on with a small blast.
- It cannot hit anything closer than twenty cells, misses often and reloads slowly. Fed with stone chunks: one chunk makes one boulder, twelve fit at a time.

### Fixes
- On frozen maps vanilla gave heir soldiers a "free" warm layer chosen from every piece of clothing in the game, which could replace their uniform: an Albion fusilier could lose his shako to a tuque and his shirt to a Nordic tunic. Heir pawns now take any extra warmth only from their own nation's wardrobe, and never lose a piece their uniform requires.

### Technical
- New automatic tests: every nation has a complete doctrine, the drill is added to raiders, grows with the formation, breaks when a raider stands alone and leaves a downed raider, the doctrine picks the raid plan and arrival (and does nothing when switched off or when the plan was forced), a real New Kemet raid arrives drilled and faster, nation animals and carriers in every biome, a manned trebuchet firing at a raider, and heir kits on a frozen tile.
- Save compatible. Caravans and starts made before the update keep their animals.

---

## Heirs of Earth 3.2.0 "Equal Heritage"


This update brings every nation up to the same depth and includes the 3.1 "Polish and Balance" changes, which were never released on their own. Every nation now has at least five weapons, five pieces of clothing and armour (with leader regalia), five buildings, three dishes, three floors and its own defensive structure.

### Defensive structures (new)
- Eight new unpowered defensive structures, one for every nation that had none. Each needs its own research (40 culture knowledge if it is not your heritage) and is loaded with simple ammunition, like the Tianxia fire-arrow battery.
- Nova Roma scorpio: a torsion bolt thrower. One heavy, armour-piercing bolt at a time over long range. Wood makes bolts.
- Yamato yagura: a timber watchtower whose three bows loose a short volley. Wood makes arrows.
- Nordheim bow loft: a log platform with a huge twin bow, two great arrows per volley at long range. Wood makes arrows.
- Hellenic lithobolos: a torsion stone thrower. Hard-hitting stones at very long range, but it cannot hit anything closer than six cells. Fed with stone chunks.
- Albion field cannon (industrial): bursting shells with a small blast radius at the longest range of all, slow to reload, nothing closer than eight cells. Steel is cast into shells.
- New Kemet archer pylon: four composite bows on a turning stand, a quick volley of light arrows. Wood makes arrows.
- Pars naft thrower: a bronze siphon that sprays burning naft in short bursts at close range and sets targets alight. Filled with chemfuel.
- Inti sling stand: a long sling arm that whirls three stones in a row. Fed with stone chunks.
- All of them are a little weaker than powered vanilla turrets, but need no power and are cheap to keep loaded.

### New buildings
- Albion: gas lamp (a powered street lamp with a wide warm light) and grandfather clock (a fine oak clock with a brass pendulum).
- New Kemet: sphinx (a great 2x1 statue) and lotus lamp (a bronze lamp burning wood).
- Pars: fire altar (a stepped white altar whose fire warms the room) and lamassu (a winged guardian bull, 2x1).
- Inti: sun disc (a gold face of the sun on a stone stand) and puma stone (a crouching puma carved from one block, 2x1).

### New weapons
- Nova Roma spatha: the long cavalry sword.
- Nordheim seax: a heavy single-edged knife, cheap and quick to make.
- Hellenic gastraphetes: the belly bow, a heavy early crossbow.
- Tianxia dao: the broad soldier's sabre.
- Albion blunderbuss (a short, flared gun that is terrible at close range) and flintlock pistol.
- New Kemet hedj mace: a pear-shaped mace of stone or metal.
- Pars shamshir: a deeply curved sabre that cuts very well.
- Inti bolas (thrown cords and stones) and chuki lance.

### New clothes and regalia
- Leader regalia that raise social impact noticeably: Roman gold laurel wreath, Nordic jarl's circlet, Tianxia dragon robe, Albion bicorne, Kemet nemes, Parsian kidaris tiara and the Inca mascaypacha.
- Everyday and formal clothes: Roman toga, Yamato kamishimo and jingasa war hat, Hellenic himation and olive wreath, Tianxia futou cap, Albion frock coat and top hat, Kemet leopard mantle, Parsian candys robe and the Inca feather cape.
- Wreaths, circlets, the kidaris and the mascaypacha are shown in the gear tab but not drawn on the pawn.

### New food
- Two new dishes for every nation, including a dessert or festive dish that gives a little joy: Roman lucanica and bread and libum honey cake, Yamato miso soup and mochi, Nordic hunter's stew and honey flatbread, Hellenic obeliskos skewers and plakous, Tianxia congee and mooncakes, Albion Sunday roast and tea and scones, Kemet ful and date cakes, Parsian kebab with saffron rice and sholeh zard, Inca locro and humitas.

### New floors
- Thirteen new floors so every nation has three: Yamato ishidatami, Nordic slate and carved boards, Hellenic marble and pebble mosaic, Tianxia grey brick and red lacquer boards, Albion parquet, Kemet sandstone slabs, Parsian glazed star tiles and garden path, Inca fitted stone and adobe tiles.

### World map
- Every nation has its own settlement icon on the world map in its own colour: a basilica for Nova Roma, a castle keep for Yamato, a long hall for Nordheim, a hill temple for Hellas, a gate tower for Tianxia, a clock tower for Albion, a pyramid for New Kemet, a palace terrace for Pars and a sun temple for Inti.

### Research browser (new)
- New "Research" section in the Heirs tab that lists all heir research projects in one place.
- Filter by nation (or the shared projects that belong to no nation), by age (tribal, medieval, industrial) and by state (can start, locked, finished).
- Every locked project says why it is locked: the culture knowledge it needs, a story it needs, the World Council, missing prerequisites or a missing research bench.
- Start any available project with one click. Hover over a row for its full description and effects.

### Encyclopedia (new)
- New "Encyclopedia" section in the Heirs tab with one page per nation.
- Each page shows the nation's story, ruler, relations with you, your knowledge and research progress, its friends and rivals, and how to learn from it.
- Shows all its buildings, weapons, clothes and armour, food and drink, goods and floors with their icons. Click any entry to open its full information card.
- Also lists its traditions (with their effects and whether you have them) and its story and legendary work.

### Starts
- Every Heirs of Earth start (all nine nations and "Heirs of no one") now begins with five colonists instead of three, picked from ten candidates instead of eight.
- Starting food and medicine grow with the larger group (about two thirds more), so the first season is not a famine. Weapons, silver and the nation's goods stay the same.

### Difficulty
- New difficulty presets in the mod settings: Relaxed, Standard and Hard. Each sets knowledge gain, research cost, raid strength, tribute demands and how often political events happen in one click. You can still change every slider afterwards.
- New setting: how much silver the nations demand as tribute (25% to 300%).

### Balance
- New balance report tool compares every heir weapon, armour, food and building with vanilla things of the same tech level. Changes made from its findings:
- Fabric body armour could become stronger than marine armour when made from hyperweave. The Hellenic linothorax, the Kemet scale corselet and the Inti quilted war tunic now top out just under the best vanilla armour with the best fabric. With ordinary cloth and leather they are lighter, cheaper armour than metal.
- The Kemet khepresh war crown made from hyperweave was as strong as an advanced helmet. Its armour is lower now.
- The Yamato do-maru can now only be made from metal. Made from the best leathers it was stronger than any vanilla armour.
- The Yamato tanegashima and the Parsian jezail were far weaker than any other gun of their age. Both now hit a little harder (tanegashima 19 to 21 damage, jezail 18 to 20) and reload a little faster. They are still slow, long-range guns.

### Technical
- New automatic tests for content depth, all nine defensive structures firing at a raider, lamps and altars, worn graphics, regalia, settlement icons, the research browser, the encyclopedia and the difficulty settings.
- Save compatible. Existing armour keeps its material; newly made pieces use the new values.

---

## Heirs of Earth 3.0.1


### Nation clothes (fix)
- Heir pawns now always wear their own nation's clothes. Before this fix they could roll vanilla cowboy hats, bowler hats, tuques and parkas, and soldiers could wear another nation's armour (for example a Yamato samurai in a Roman lorica, or Parsian Immortals in Yamato do-maru).
- Every nation's people wear their everyday garment: the Roman tunica, the Yamato kimono, the Nordheim tunic, the Hellenic chiton, the Tianxia hanfu, the Kemet kalasiris, the Parsian kaftan and the Inti unku. Albion's civilians keep plain shirts and trousers.
- Soldiers with a good kit budget also wear their nation's body armour, and soldiers who usually wear helmets now always wear their nation's helmet.
- Some kinds could spawn with no clothes at all (the Kemet colonist, the Kemet charioteer and the Inti guard). They are now dressed.
- Plain shirts and trousers can still be worn under nation clothes. They now come from a mod tag instead of the shared vanilla clothing list, so no vanilla hats or coats get in.
- Some heir soldiers are a little tougher now that they always wear their armour.

### Names (fix)
- Every nation now has about 55 to 65 first names per gender instead of about 16. RimWorld keeps short names unique among living people, so in long games with many people of one nation (for example during long wars) the game ran out of names and logged "Could not get new name".
- Two-part first names such as Mama Ocllo are now written with a hyphen (Mama-Ocllo), so the game no longer reads the second part as a family name.

### Steam page
- Added in-game screenshots of all nine nations, the World Council, a battle, trade routes and the research tree.
- Harmony is now listed as a required item on this page. The mod has always needed it in game.

### Technical
- New automatic test: six pawns of every heir pawn kind are generated and checked for foreign kit, missing nation clothes and bare torsos.
- Save compatible. Pawns that already exist keep what they wear; new pawns use the fixed kits.

---

## Version 3.0.0 - Sand, Mountain and Road


### Three new nations
The last three colony ships have landed. Each new nation has the same depth as the first six: its own research branch (16+ projects, 7-9 traditions and an industrial row), weapons, armour, buildings, a floor, a food, a trade good, seven kinds of people, twelve backstories, a trader caravan, a start scenario, an archive item, a story chain and a legendary artifact. They appear in new worlds and join existing saves automatically (see "Add new nations to existing saves" in the mod settings).

NEW KEMET - the river kingdom (falcon, sand gold)
- Friends with Hellas. Farmers, scribes and stonemasons who are very hard to starve.
- Weapons: river spear, khopesh, composite bow, desert rifle (industrial).
- Apparel: linen kalasiris, scale corselet, khepresh war crown.
- Buildings: obelisk (beauty 22, needs a little gold), senet table (a two-player intellectual joy game that trains Intellectual), papyrus workshop (25 hay -> 10 papyrus, a light trade good with knowledge value).
- Floors: irrigated silt (fertility 125%, laid on soil) and lotus tiles.
- Food: date bread.
- Traditions: Gift of the River (+8% harvest yield), House of Scribes (+7% learning), Sun Calendar (+7% plant work speed), Royal Stonemasons (+20% smoothing, +5% mining), Children of the Sun (+5 C comfortable max temperature), Royal Kitchens (-40% food poisoning, +5% cooking speed), Medjay Patrols (+2% move speed, 5% faster aiming), River Engineering (industrial: +5% construction, +2% global work speed).
- Story chain "The City Beneath the Sand" ends with the Sun Disc of Iteru: it clears the sky, rallies your people and sends enemies fleeing. Capstone: Second Sunrise (+4% harvest, +5% construction, steadier minds).

THE SATRAPY OF PARS - the royal road (griffin, ruby and gold)
- Friends with Tianxia, rivals of Nova Roma. Gardeners, weavers and the Immortals.
- Weapons: Immortal's spear, akinakes short sword, recurve bow, jezail (industrial long gun).
- Apparel: silk kaftan, Immortal's scale coat, winged helmet.
- Buildings: paradise garden (2x2, beautiful, colonists sit in it for meditative joy), post station lamp (a fuelled lamp), carpet loom (60 cloth or wool -> one Parsian carpet worth 240 silver).
- Floor: girih tiles. Food: saffron pilaf.
- Traditions: Culture of Gardens (steadier minds), Law of the Satraps (+15% arrest success, +5% negotiation), Royal Post (+5% trade prices, +10% caravan speed), Qanats (+6% immunity gain), Polo (+10% taming and training), Ears of the King (+8% negotiation, +4% social impact), The Ten Thousand (+5% pain shock threshold, +1 melee hit), Grand Bazaar (industrial: +4% trade prices, +3% negotiation).
- Story chain "The Royal Road" ends with the King's Eye: it rallies your people, raises relations with every non-hostile heir nation (+6) and calls a friendly heir caravan to your colony. Capstone: Road of Kings (+5% negotiation, +5% social impact, +8% caravan speed).

THE INTI EMPIRE - the counted empire (condor, red-orange)
- Rivals of Albion. Terrace farmers, runners, slingers and the keepers of the knots.
- Weapons: sling (throws stones), star mace, mountain carbine (industrial).
- Apparel: unku tunic, quilted war tunic, plumed war helmet.
- Buildings: qullqa storehouse (a 2x2 stone store for food and plant matter; food stored in it rots at half speed, and the "rots in" readout shows the longer time), quipu table (links to a research bench, +5% research speed, like the Hellas lyceum), sun stone.
- Floor: stone terraces (fertility 100%, laid on any diggable ground, so rocky and poor soil can be farmed). Food: pachamanca.
- Traditions: Chaski Runners (+3% move speed), Ayni (+3% global work speed), Mita Labour (+5% construction and mining), Children of the Heights (-6 C comfortable min temperature), Mountain Farming (+5% harvest, +3% plant work), Keepers of the Knots (+6% research speed), Kallawaya Healers (+5% tend quality), Slingers of the Heights (+1 shooting accuracy, 4% faster aiming), Great Road (industrial: +3% construction, +8% caravan speed).
- Story chain "The Language of Knots" ends with the Golden Thread: it brings rain, rallies your people and drives enemies back. Capstone: The Counted Empire (+4% research, +5% learning, +2% work speed).

### Trade routes
- A new "Trade routes" section in the Heirs tab. Open a road to a nation that likes you (relations 25 or more, not hostile) by paying silver once: 400 for a close neighbour, up to 900 for a far one (5 silver per world tile).
- Up to 3 roads at a time; the Pars tradition Royal Post allows a 4th.
- Every 15 days a road caravan drops that nation's own goods and silver near your trade spot, worth 35% of what the road cost (50% with Royal Post). The goods are not forbidden, so your colonists can haul them right away.
- Each caravan raises relations with that nation by 2 and teaches your scholars a little of its culture (+3 Culture Knowledge).
- Danger on the road: if the nation is at war with anyone, each caravan has a 25% chance of being raided on the way. Nothing arrives that time, but the road stays open.
- A road closes on its own if the nation turns hostile or collapses (with a letter). You can also close a road yourself; the silver is not returned.
- Every opening, caravan, raid and closing is written into the Chronicle.
- Can be turned off in the mod settings ("Trade routes").

### The World Council (end goal)
- A new "World Council" section in the Heirs tab shows the road to the council and how every nation would vote today, with the reason.
- The council opens when you finish 3 nation stories, or keep 3 trade roads open for a full year (a letter tells you).
- Then research "World Council" (industrial, 3000) and build the Council Hall of the Heirs: a 5x5 stepped stone dais with a ring table, a mosaic of the world, nine envoy chairs and nine banners (400 stone, 150 steel, 60 gold, 120 cloth, Construction 8, beauty 40).
- With the hall standing you can call the council once every 15 days.
- Unity victory: two thirds of the living nations vote yes. A nation votes yes if it is your ally, has sworn you fealty or has 60+ relations with you, but votes no if a nation it is at war with votes yes. A failed vote sends a letter listing every nation's answer and reason.
- Dominion victory: every living nation has sworn fealty to you. A nation hostile to you that has lost half of its settlements offers fealty (at most once every 30 days). Accepting ends the war; the nation then pays 100 silver per settlement every 30 days and always votes yes. If it turns hostile again, the oath is broken. A nation whose last settlement you destroy collapses as before.
- Victory brings a final letter, a Chronicle entry and the end credits; the game goes on afterwards.
- Can be turned off in the mod settings ("World Council (end goal)"); fealty offers and tributes stop too.

### Balance and fixes
- Inti warriors get a larger weapon budget, so they no longer sometimes spawn without their star mace.

### Art
- 51 new hand-painted textures for the three nations: weapons, apparel, buildings, floors, food, relics, artifacts and nation emblems.
- The Council Hall of the Heirs.

### Technical
- New mod feature "foodStore" (Harmony patch on CompRottable). If a future game update breaks it, it turns itself off with a log warning and nothing else is affected.
- Artifacts can now raise goodwill and call a caravan (new fields on the artifact comp).
- Trade routes, the council, fealty and victory are saved with the game; saves from 2.x load without them and start with no roads.

---

## Version 2.1.0 - Filling the gaps


### Existing saves
- New nations now join existing saves. When you load a save made with an older version, nations that did not exist yet arrive with their own settlements, relations and a letter telling you who came. You can turn this off in the mod settings ("Add new nations to existing saves").

### Industrial age for the first three nations
- Nova Roma: legion carbine (a light breech-loader with a brass eagle) and the Civil Code tradition (+6% negotiation, +6% social impact, but 2% slower work).
- Yamato: tanegashima matchlock and the Sakai Gunsmiths tradition (colonists aim 8% faster).
- Nordheim: harpoon gun (slow, short-ranged, hits hard) and the Folk High Schools tradition (+8% learning, +4% research speed).
- These guns are made at a smithy and sold by traders. Existing archers of these nations keep their bows.

### New signature buildings
- Tianxia fire-arrow battery: an unpowered "nest of bees" turret that looses eight fire arrows per volley. It is loaded with wood (one log makes two arrows). Inaccurate, but it sets enemies alight.
- Albion textile mill: a powered loom that weaves 50 wool of any kind into 50 tweed.
- Hellas lyceum scroll cabinet: links to a research bench and speeds up research by 6%.
- Hellas asclepion: a small healing altar that links to beds within six cells (+4% tend quality, +3% immunity gain speed). Works with modded beds that accept end tables.

### Tweed is now a fabric
- Tweed can be used to make clothes, like wool: warm, rain-proof and hard-wearing. Its price dropped to fit its new role.

### Sounds
- Four new signature sounds: a war horn when nations declare war and when the Storm Horn is blown, a brass call for the Eagle Standard and the Owl Aegis, a gong for the Dragon Seal and a drum roll for the War Drum.

### Fixes
- Mediation letters now show both nation names.

---

## Version 2.0.0 - Three new nations and full politics


### New nations
- League of Hellas (owl, led by an Archon). Hoplites, Ephebes, Toxotes archers, physicians and Strategoi. Weapons: dory spear, xiphos, kopis, toxon bow. Armour: Corinthian helmet, linothorax, chiton. Buildings: hoplon wall shield, marble column, theatre stage, meander floor. Food: maza barley cakes. Trade good: olive oil. Friendly toward Nova Roma.
- Celestial Tianxia (dragon, led by an Emperor). Militia, crossbowmen, palace guards, scholars and generals. Weapons: jian, guandao, repeating crossbow (3-bolt burst), fire lance (short-range flame shot). Armour: lamellar, Tianxia helmet, hanfu robe. Buildings: porcelain vase, moon gate, paper lantern, gongfu tea table, jade floor. Food: dumplings. Trade goods: tea bricks and silk. Rival of the Yamato Shogunate.
- Commonwealth of Albion (lion, led by a Lord Protector). The first Industrial heir nation: fusiliers, riflemen, dragoons, engineers and colonels. Weapons: cavalry sabre, musket, bayonet rifle. Apparel: shako and redcoat. Buildings: wood-fired steam engine (1400 W), pub table, cobblestone and brick floors. Food: meat pie. Trade good: tweed. Friendly toward Nordheim, rival of Nova Roma.

### Research and traditions
- Each new nation has its own research branch with seven traditions (21 new traditions in total).
- Hellas: Olympic Games, Rhetoric, Geometry, Hippocratic Oath, Theatre, Academy, Phalanx.
- Tianxia: Tea Culture, Ever-Normal Granary, Silk Road, Imperial Physicians, Imperial Examination, Fire Arrows, Porcelain Mastery.
- Albion: Enclosure, Sanitation, Joint-Stock Company, Admiralty Charts, Line Drill, Steam Power, Factory Order.
- Some traditions have a price (Phalanx slows movement, Enclosure hurts negotiation, Factory Order raises mental break risk).

### Story chains and artifacts
- Three new five-step story chains: "The Lost Library" (Hellas), "The Palace Examination" (Tianxia) and "Iron Revolution" (Albion).
- Each chain ends with a relic, a hard choice and a legendary artifact: the Aegis of the Owl, the Dragon Seal (calls fog and rain) and the War Drum.
- Finishing a chain unlocks the nation's capstone project: Golden Age (Hellas), Harmony Under Heaven (Tianxia) and the Workshop of the World (Albion).

### Politics
- All six nations now take part in the political simulation: alliances, wars, captured towns, envoys, tribute demands, marriages and collapse.
- New starting friendships and rivalries between the nations.
- Mediation letters now show both nation names correctly.

### People and joy
- 21 new pawn kinds and 36 new backstories.
- New joy activity: watching a play at the Hellas theatre stage (up to six spectators).
- Tianxia tea tables join the tea ceremony; Albion pub tables join feasts.
- Every new nation has a trader and a start scenario (Albion starts as an Industrial colony).

### Fixes and balance
- Nova Roma's Aquila research no longer overlaps Pax Romana in the research tab.
- Ranged weapons balanced against vanilla references (repeating crossbow and toxon stay close to vanilla bows; muskets and rifles close to vanilla guns).
- New preview image and mod icon with all six nation emblems.

All new text is in English and Turkish. Existing saves keep loading, but the three new nations only appear in newly generated worlds.

