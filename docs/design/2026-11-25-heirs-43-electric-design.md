# Heirs of Earth 4.3 "Electric Age": design

Approved by the user on 2026-11-25 ("uygun"), after the proposal in chat; the user chose a separate helmet and field uniform
for every nation ("Her ulusa ayrı").

## Why
4.3 is the next step on the roadmap after 4.2 "Ages of Progress" (Founding, Powder, Steam). In a long game the nations should
keep moving: a fourth age gives late-game nations a new look and new arms, gives the player late-game items to research
from each nation, and adds an event that rewards the player's colony for what it has made.

## Goals
- A fourth age, **IV Electric**, after the Age of Steam.
- Each nation gets one late-game gun with its own strength, one steel helmet and one field uniform, all with hand-made art
  (worn art on four sides and five body types, colour masks like 4.1/4.2).
- Each nation gets one powered industrial building with one small, useful effect that fits the nation.
- **World Fair**: the first nation to reach the Electric Age holds a fair; the player may send an exhibit and earn goodwill,
  knowledge and silver by its quality.
- Fix shipped with it: the fourth speed button no longer hangs off the right edge of the screen (done, `HeirsSpeed.Fit`).
- Everything works like 4.2: troops carry and wear the age's items, traders sell them, and the player may research them only
  once the nation has reached the age (or if it is the player's heritage).

## Non-goals
- No spacer tech; the Electric Age stays industrial (vanilla Industrial tech level, guns level with vanilla industrial guns).
- No change to faction tech level or other def-wide faction values.
- No new pawn kinds; melee troops keep their weapons.

## Anti-goals
- Breaking 4.2 saves (ages already reached must stay reached).
- Age IV coming so fast that most nations reach it in an ordinary game: it should be a late-game event.
- Art that looks flat or generated, or helmets/uniforms that do not read as the nation's.

## Approaches
- **Chosen: extend the 4.2 age system by one step.** Same tag swap for guns (`HE_<Nation>Age4`), same uniform kit patch,
  same `HeirsAgeExt` (age 4) for traders and the research gate, same letters, chronicle, Heirs tab and encyclopedia.
- Rejected: a separate "electric" system next to the ages (twice the code, two places for the same rules, more save risk).
- Rejected: new pawn kinds per age (27+ kinds, raid tables) and runtime faction def changes, as in 4.2.

## Numbers
- Age IV at **18.0** progress (Age II 3.0, Age III 9.0; same rate rules). With the usual peace bonuses (about 130%) that is
  about 14 years, so most games end before it, and a nation that rises (scholarly ruler, allies, science treaty) can get there.
- Setbacks (famine, plague) never drop a nation out of an age it reached; floor extends to 18.
- Ranged troops in Age IV: 40% Age IV gun, 30% Age III, 10% Age II, rest the usual weapon. Melee troops: 15% / 15% / 5%.
- Armed troops in Age IV: 55% wear the field uniform (in place of the steam coat) and, independently, 55% the steel helmet.
  Leaders keep their regalia.
- Research: one project per nation, "<Adj> electric army" (guns, helmet, uniform), 3200 research, 60 knowledge, prerequisites
  the nation's Age III project plus vanilla `Machining`; one more project per nation, "<Adj> works" (the building),
  2600 research, 50 knowledge, prerequisite vanilla `Electricity` and the Age III project. Both are Industrial and age-gated (4).

## Items
Guns (Industrial, balanced against vanilla industrial guns; each has one strength):
- Albion: light machine gun (burst, heavy, slow to aim; level with vanilla LMG but costs more steel, less components)
- Yamato: scoped sniper rifle (longest aim, best long-range accuracy)
- Nordheim: pump shotgun (close range, high damage, pellets as one heavy shot as in vanilla)
- Roma: self-loading rifle (fast cooldown, medium range)
- Tianxia: "box" pistol with a stock (short burst, quick to aim, cheap to make)
- Hellas: mountain carbine (light, good at medium range)
- Kemet: desert carbine (long barrel for a carbine, good in heat; text only, no heat stat)
- Pars: long-range rifle (longest range of the age)
- Inti: light carbine (lightest and cheapest)

Apparel per nation (18): a steel helmet (Overhead, covers FullHead or UpperHead like vanilla's simple helmet) and a field
uniform (Shell over torso/shoulders/arms, slightly better armour than the steam coat, worse than flak). Each in the nation's
colours and with its own detail (badge, crest, band, braid).

Buildings per nation (9), each powered (150-500 W), made of steel and components, one effect, preferring vanilla mechanics:
- Roma: electric fountain (beauty, a little joy)
- Yamato: electric tea kettle (tea-house joy, fast)
- Nordheim: electric forge (a faster smithy; builder's call: Nordheim already has a sauna since 1.x, so not a sauna stove)
- Hellas: electric lamp-lit lecture hall lectern (research speed facility for research benches)
- Tianxia: printing press (prints silk: a facility that speeds tailoring benches; builder's call, vanilla has no book-printing job)
- Albion: telegraph office (small monthly goodwill with friendly nations; builder's call: no raid warning, to keep it simple)
- Kemet: electric irrigation pump (raises growth on nearby fields)
- Pars: electric carpet loom (fast cloth work table for carpets/textiles)
- Inti: cold store (storage that slows rot, like the qullqa but powered and stronger)
The exact effect numbers and which vanilla comps are used are left to the builder; at most a few buildings may need custom code.

## World Fair
- Fires once per game, when the first nation reaches the Electric Age. If that nation is hostile to the player then, the next
  nation to reach the age that is not hostile hosts it instead.
- A choice letter: "send an exhibit" or "decline". The exhibit is chosen automatically: the colony's best art piece, weapon
  or book by quality, then market value (shown in the letter). Declining costs a little goodwill with the host.
- The exhibit travels to the fair and comes back by drop pod about 10 days later; the result letter arrives then.
- Reward by quality: goodwill with the host and with every peaceful nation, knowledge of the host, silver. Legendary and
  masterwork exhibits can win the fair's grand prize (extra goodwill everywhere and a chronicle entry).
- A setting is not added; it follows the existing "world events" setting.

## Save compatibility
- 4.2 saves: progress and shown ages carry on; nations already past 18 progress announce the Electric Age once.
- With ages off nothing changes (everything researchable as before, as in 4.2).

## Tests (probes)
Age thresholds and `AgeFor` up to 4, setback floor at 18, Age IV items per nation (gun, helmet, uniform, building), tags
and HeirsAgeExt on each, troops in Age IV get Age IV guns/uniforms/helmets in the expected range, traders and research
gated, worn art and masks present for every new apparel (all sides, all bodies), each building's effect works, the World
Fair letter, exhibit return and rewards, the fourth speed row stays on screen, plus the full existing suite.

## Left to the builder
Exact stats, building effect numbers, art, text (English and Turkish), and the names of the research projects.
