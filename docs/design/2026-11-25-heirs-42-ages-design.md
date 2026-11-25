# Heirs of Earth 4.2 "Ages of Progress": design

Approved by the user on 2026-11-25 ("Tamam çok iyi bir şekilde hallet"), after the proposal in chat.

## Why
A player asked on Steam whether the nations stay medieval. The player's own colony can already research everything; the nine nations never change. In a long game a friend should be able to rise and a rival fall behind.

## Goals
- Each nation advances through three ages: I Founding (today's look), II Powder, III Steam.
- Each age shows: ranged troops carry the nation's own firearms (II: muzzle-loaders, III: rifles and carbines); in Age III soldiers often wear the nation's uniform coat.
- Progress depends on time and on the world: a scholarly ruler, wealth (settlements), alliances, a science or trade link with the player speed it up; war, famine and plague slow it.
- The player can only learn a nation's age items once that nation has reached that age (research gate), then pays knowledge and research as usual.
- Letters and chronicle entries on each new age; age and progress shown in the encyclopedia and Heirs tab.
- A setting: ages on/off and a speed slider.
- 4th time-speed button (vanilla's hidden Ultrafast speed, 15x), on by default, with its own icon and the key bound to it. A setting turns it off.

## Non-goals
- No spacer tech for nations; Age III stays industrial.
- Faction tech level (a def-wide value) is not changed.
- Melee troops keep their weapons.

## Approach (chosen)
Weapons through generation-time tag swaps (temporarily give a ranged kind the age tag and a wider weapon budget), uniforms through the existing nation wardrobe patch (temporarily add the uniform to the required list, dropping pieces it cannot be worn with). Rejected: new pawn kinds per age (27 extra kinds, raid tables) and changing faction defs at runtime (shared by every save).

## Numbers
- Progress per in-game year (60 days) at rate 1: Age II at 3.0, Age III at 9.0 (4.2.1; 4.2.0 had 2.5 and 7.0, which a ten-year run showed to be too fast: with real peace bonuses most nations reached steam in 4-6 years). A 4.2.0 save keeps the age each nation had reached. Rate = 1 + 0.5 scholarly ruler + 0.15 per ally + 0.25 science treaty with the player + 0.1 trade route/treaty with the player + 0.05 per settlement above 3 (max +0.3) - 0.4 at war; floor 0.2. Famine or plague costs 0.3 progress at once. Speed slider 0.25x-4x.
- Ranged troops: Age II 50% carry an Age II gun; Age III 45% Age III, 30% Age II.
- Age III uniform: 55% of armed troops.

## Items (new unless marked existing)
Age II / Age III guns per nation:
- Roma: legion arquebus / legion carbine (existing)
- Yamato: tanegashima (existing) / Yamato rifle
- Nordheim: hook gun / Nordic rifle
- Hellas: Hellenic musket / Hellenic rifle
- Tianxia: bird gun / Tianxia rifle
- Albion: rifle (existing) / breech-loader
- Kemet: Nile musket / desert rifle (existing)
- Pars: jezail (existing) / Pars rifle
- Inti: Inti arquebus / Inti carbine (existing)
Age III uniform coat per nation (9).

## Left to the builder
Exact stats (balanced against existing guns), art details, text.
