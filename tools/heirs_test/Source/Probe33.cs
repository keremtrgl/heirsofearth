using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using RimWorld.Planet;
using Verse;
using Verse.AI;
using Verse.AI.Group;

namespace HeProbe
{
    /// <summary>3.3 checks: war doctrines (data, drill, formation, raid plan, a real heir raid), nation animals and the trebuchet.</summary>
    public static class Probe33
    {
        public static void Data()
        {
            var bad = new List<string>();
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                RaidDoctrine d = n.doctrine;
                if (d == null || d.label.NullOrEmpty() || d.description.NullOrEmpty() || d.hediff == null || d.strategy == null) { bad.Add(n.defName + " incomplete"); continue; }
                if (d.arrival != null && (d.strategy.arriveModes == null || !d.strategy.arriveModes.Contains(d.arrival))) bad.Add(n.defName + " arrival not allowed by " + d.strategy.defName);
                if (!d.hediff.HasComp(typeof(HediffComp_HeirsDoctrine))) bad.Add(n.defName + " drill without comp");
                if (d.chance <= 0f || d.chance > 1f) bad.Add(n.defName + " chance " + d.chance);
                if (HeirsAtlas.WarText(n).NullOrEmpty() || !HeirsAtlas.WarText(n).Contains(d.label.CapitalizeFirst())) bad.Add(n.defName + " encyclopedia");
            }
            P.Check("every nation has a complete war doctrine", bad.Count == 0, string.Join("; ", bad));
            P.Check("doctrines differ", DefDatabase<NationDef>.AllDefsListForReading.Select(n => n.doctrine?.hediff).Distinct().Count() == 9);
            P.Check("letter key exists", "HE_DoctrineLetter".CanTranslate() && "HE_SettingsDoctrines".CanTranslate() && "HE_AtlasDoctrine".CanTranslate());
        }

        public static void Animals()
        {
            var bad = new List<string>();
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                if (n.animal == null || !n.animal.RaceProps.Animal) { bad.Add(n.defName + " no animal"); continue; }
                ScenPart_StartingAnimal part = n.scenario?.scenario.AllParts.OfType<ScenPart_StartingAnimal>().FirstOrDefault();
                PawnKindDef kind = part == null ? null : (PawnKindDef)P.Get(part, "animalKind");
                if (kind != n.animal) bad.Add(n.defName + " start " + kind?.defName);
                PawnGroupMaker trader = n.faction.pawnGroupMakers.FirstOrDefault(g => g.kindDef == PawnGroupKindDefOf.Trader);
                if (trader == null || trader.carriers.Count == 0 || trader.carriers.Any(c => !c.kind.RaceProps.packAnimal)) bad.Add(n.defName + " carriers");
            }
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                PawnGroupMaker trader = n.faction.pawnGroupMakers.FirstOrDefault(g => g.kindDef == PawnGroupKindDefOf.Trader);
                if (trader == null) continue;
                foreach (BiomeDef b in DefDatabase<BiomeDef>.AllDefsListForReading.Where(b => b.canBuildBase && !((List<ThingDef>)P.Get(b, "allowedPackAnimals")).NullOrEmpty()))
                {
                    if (!trader.carriers.Any(c => b.IsPackAnimalAllowed(c.kind.race))) bad.Add(n.defName + " no carrier in " + b.defName);
                }
            }
            ThingDef horse = ThingDef.Named("Horse"), yak = ThingDef.Named("Yak");
            if (!BiomeDef.Named("TemperateForest").IsPackAnimalAllowed(horse) || !BiomeDef.Named("Tundra").IsPackAnimalAllowed(yak)) bad.Add("pack animal patch");
            P.Check("nations keep their own animals", bad.Count == 0, string.Join("; ", bad));
            NationDef inti = DefDatabase<NationDef>.GetNamed("HE_Inti");
            P.Check("Inti caravans walk with alpacas", inti.faction.pawnGroupMakers.First(g => g.kindDef == PawnGroupKindDefOf.Trader).carriers.Max(c => c.selectionWeight) == inti.faction.pawnGroupMakers.First(g => g.kindDef == PawnGroupKindDefOf.Trader).carriers.First(c => c.kind.defName == "Alpaca").selectionWeight);
        }

        /// <summary>The drill: added to raiders, follows the formation, and leaves when the raider falls.</summary>
        public static void Drill()
        {
            Map map = P.Home;
            Faction enemy = Find.FactionManager.AllFactions.FirstOrDefault(f => !f.IsPlayer && f.HostileTo(Faction.OfPlayer) && f.def.humanlikeFaction);
            if (enemy == null) { P.Say("no hostile faction"); return; }
            P.Calm();
            RaidDoctrine roma = DefDatabase<NationDef>.GetNamed("HE_Roma").doctrine;
            IntVec3 spot = P.FreeSpot(map, new IntVec2(5, 5));
            var pawns = new List<Pawn>();
            for (int i = 0; i < 5; i++)
            {
                Pawn p = PawnGenerator.GeneratePawn(PawnKindDefOf.Villager, enemy);
                GenSpawn.Spawn(p, CellFinder.RandomClosewalkCellNear(spot, map, 1), map);
                pawns.Add(p);
            }
            LordMaker.MakeNewLord(enemy, new LordJob_DefendPoint(spot), map, pawns);
            Pawn lead = pawns[0];
            float before = lead.GetStatValue(StatDefOf.ArmorRating_Sharp);
            foreach (Pawn p in pawns) HeirsDoctrine.Drill(p, roma);
            Hediff h = lead.health.hediffSet.GetFirstHediffOfDef(roma.hediff);
            P.Check("drill added to raider", h != null && pawns.All(p => p.health.hediffSet.HasHediff(roma.hediff)));
            if (h == null) { P.Calm(); return; }
            HediffComp_HeirsDoctrine comp = ((HediffWithComps)h).TryGetComp<HediffComp_HeirsDoctrine>();
            int near = HediffComp_HeirsDoctrine.Comrades(lead, 2.9f);
            comp.Refresh();
            lead.health.hediffSet.DirtyCache();
            float packed = lead.GetStatValue(StatDefOf.ArmorRating_Sharp);
            P.Check("formation strengthens with comrades", h.Severity >= System.Math.Min(1f, near / 4f) - 0.01f && (near < 1 || packed > before),
                "comrades " + near + ", severity " + h.Severity.ToString("F2") + ", armour " + before.ToString("F2") + " -> " + packed.ToString("F2"));
            foreach (Pawn p in pawns.Skip(1)) P.Gone(p);
            comp.Refresh();
            P.Check("formation breaks when alone", h.Severity < 0.25f && h.CurStageIndex == 0, h.Severity.ToString("F2"));
            HealthUtility.DamageUntilDowned(lead, false);
            comp.Refresh();
            P.Check("drill leaves a downed raider", h.ShouldRemove || !lead.health.hediffSet.HasHediff(roma.hediff));
            P.Calm();
        }

        /// <summary>The raid plan: a heir faction prefers its plan and arrival; with the setting off nothing changes.</summary>
        public static void Plans()
        {
            Map map = P.Home;
            NationDef roma = DefDatabase<NationDef>.GetNamed("HE_Roma");
            Faction faction = HeirsWorld.FactionOf(roma);
            if (faction == null) { P.Say("no Roma faction"); return; }
            int strat = 0, arrive = 0;
            for (int i = 0; i < 20; i++)
            {
                var parms = new IncidentParms { target = map, faction = faction, points = 1200f, raidStrategy = RaidStrategyDefOf.ImmediateAttack };
                HeirsDoctrine.StrategyPostfix(parms, PawnGroupKindDefOf.Combat, true);
                if (parms.raidStrategy == roma.doctrine.strategy) strat++;
                parms.raidArrivalMode = PawnsArrivalModeDefOf.EdgeDrop;
                parms.raidStrategy = roma.doctrine.strategy;
                HeirsDoctrine.ArrivalPostfix(parms, true);
                if (parms.raidArrivalMode == roma.doctrine.arrival) arrive++;
            }
            P.Check("doctrine picks the nation's raid plan", strat >= 8, strat + "/20");
            P.Check("doctrine picks the nation's arrival", arrive >= 8, arrive + "/20");
            var forced = new IncidentParms { target = map, faction = faction, points = 1200f, raidStrategy = RaidStrategyDefOf.ImmediateAttack };
            HeirsDoctrine.StrategyPostfix(forced, PawnGroupKindDefOf.Combat, false);
            P.Check("a forced raid plan is kept", forced.raidStrategy == RaidStrategyDefOf.ImmediateAttack);
            HeirsMod.Settings.raidDoctrines = false;
            int off = 0;
            for (int i = 0; i < 10; i++)
            {
                var parms = new IncidentParms { target = map, faction = faction, points = 1200f, raidStrategy = RaidStrategyDefOf.ImmediateAttack };
                HeirsDoctrine.StrategyPostfix(parms, PawnGroupKindDefOf.Combat, true);
                if (parms.raidStrategy != RaidStrategyDefOf.ImmediateAttack) off++;
            }
            HeirsMod.Settings.raidDoctrines = true;
            P.Check("setting off: no doctrine", off == 0 && HeirsDoctrine.DoctrineOf(faction) != null, off.ToString());
            string text = "raid";
            HeirsDoctrine.LetterPostfix(new IncidentParms { faction = faction }, ref text);
            P.Check("raid letter names the doctrine", text.Contains(roma.doctrine.label.CapitalizeFirst()), text);
        }

        /// <summary>A real raid by an heir nation through the vanilla raid incident: its raiders arrive drilled and keep the drill while fighting.</summary>
        public static void RealRaid()
        {
            Map map = P.Home;
            P.Calm();
            NationDef nation = DefDatabase<NationDef>.GetNamed("HE_Kemet");
            Faction faction = HeirsWorld.FactionOf(nation);
            if (faction == null) { P.Say("no Kemet faction"); return; }
            int goodwill = faction.GoodwillWith(Faction.OfPlayer);
            try
            {
                // friendly Kemet traders or visitors already on the map turn hostile too; only the raid itself is drilled
                var present = new HashSet<Pawn>(map.mapPawns.SpawnedPawnsInFaction(faction));
                if (!faction.HostileTo(Faction.OfPlayer)) faction.ChangeGoodwill_Debug(Faction.OfPlayer, -100 - goodwill);
                var parms = new IncidentParms { target = map, faction = faction, points = 600f, forced = true };
                bool ok = IncidentDefOf.RaidEnemy.Worker.TryExecute(parms);
                List<Pawn> raiders = map.mapPawns.SpawnedPawnsInFaction(faction).Where(p => p.RaceProps.Humanlike && !present.Contains(p)).ToList();
                P.Check("heir raid arrives", ok && raiders.Count > 0, ok + " " + raiders.Count);
                int drilled = raiders.Count(p => p.health.hediffSet.HasHediff(nation.doctrine.hediff));
                P.Check("heir raiders arrive drilled", raiders.Count > 0 && drilled == raiders.Count, drilled + "/" + raiders.Count + " plan " + parms.raidStrategy?.defName + " arrival " + parms.raidArrivalMode?.defName);
                P.Ticks(400);
                int still = raiders.Count(p => p.Spawned && !p.Downed && p.health.hediffSet.HasHediff(nation.doctrine.hediff));
                int fighting = raiders.Count(p => p.Spawned && !p.Downed);
                P.Check("drill lasts while they fight", fighting == 0 || still == fighting, still + "/" + fighting);
                Pawn one = raiders.FirstOrDefault(p => p.Spawned && !p.Downed && p.health.hediffSet.HasHediff(nation.doctrine.hediff));
                if (one != null)
                {
                    float drilledSpeed = one.GetStatValue(StatDefOf.MoveSpeed, true, 0);
                    one.health.RemoveHediff(one.health.hediffSet.GetFirstHediffOfDef(nation.doctrine.hediff));
                    float plain = one.GetStatValue(StatDefOf.MoveSpeed, true, 0);
                    // the bonus is added before armour and wounds scale the speed, so compare the ratio: (4.6 + 0.8) / 4.6 = 1.17
                    P.Check("vanguard drill makes raiders faster", drilledSpeed > plain * 1.12f, drilledSpeed.ToString("F2") + " vs " + plain.ToString("F2"));
                }
            }
            finally
            {
                P.Calm();
                int now = faction.GoodwillWith(Faction.OfPlayer);
                if (now != goodwill) faction.ChangeGoodwill_Debug(Faction.OfPlayer, goodwill - now);
            }
        }

        /// <summary>On a frozen tile vanilla adds free warm clothes; heir pawns must take them from their own nation's wardrobe.</summary>
        public static void ColdKits()
        {
            PlanetTile cold = PlanetTile.Invalid;
            for (int i = 0; i < Find.WorldGrid.TilesCount; i += 7)
            {
                PlanetTile t = i;
                if (t.Valid && GenTemperature.MinTemperatureAtTile(t) < -30f) { cold = t; break; }
            }
            if (!cold.Valid) { P.Say("no frozen tile in this world"); return; }
            string[] vanilla = { "Apparel_CowboyHat", "Apparel_BowlerHat", "Apparel_Tuque", "Apparel_Parka" };
            int pawns = 0, bad = 0, missing = 0;
            var notes = new List<string>();
            foreach (PawnKindDef kind in DefDatabase<PawnKindDef>.AllDefs.Where(k => HeirsKits.NationOfKind(k) != null && k.defName != null && !k.defName.EndsWith("Colonist")))
            {
                string nation = kind.defName.Split('_')[1];
                for (int i = 0; i < 3; i++)
                {
                    Pawn pawn = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, null, tile: cold, canGeneratePawnRelations: false, forceAddFreeWarmLayerIfNeeded: true));
                    pawns++;
                    List<ThingDef> worn = pawn.apparel.WornApparel.Select(a => a.def).ToList();
                    List<ThingDef> wrong = worn.Where(d => vanilla.Contains(d.defName) || (d.defName.StartsWith("HE_") && !d.defName.StartsWith("HE_" + nation + "_"))).ToList();
                    if (wrong.Count > 0) { bad++; if (notes.Count < 6) notes.Add(kind.defName + ":" + string.Join("+", wrong.Select(d => d.defName))); }
                    if (kind.apparelRequired != null && kind.apparelRequired.Any(r => !worn.Contains(r))) { missing++; if (notes.Count < 6) notes.Add(kind.defName + ":missing " + string.Join("+", kind.apparelRequired.Where(r => !worn.Contains(r)).Select(r => r.defName)) + " wore " + string.Join("+", worn.Select(d => d.defName))); }
                    P.Gone(pawn);
                }
            }
            P.Check("frozen tile: heir pawns keep their own kit", pawns > 100 && bad == 0 && missing == 0, pawns + " pawns, " + bad + " foreign, " + missing + " missing " + string.Join(" ", notes));
        }

        public static void Trebuchet()
        {
            Map map = P.Home;
            Faction enemy = Find.FactionManager.AllFactions.FirstOrDefault(f => !f.IsPlayer && f.HostileTo(Faction.OfPlayer) && f.def.humanlikeFaction);
            ThingDef def = DefDatabase<ThingDef>.GetNamed("HE_Trebuchet");
            P.Check("trebuchet is manned and loaded with stones", def.HasComp(typeof(CompMannable)) && def.GetCompProperties<CompProperties_Refuelable>()?.fuelFilter.Allows(ThingDef.Named("ChunkGranite")) == true
                && def.building.turretGunDef.Verbs[0].defaultProjectile.projectile.flyOverhead && !def.building.turretGunDef.Verbs[0].requireLineOfSight);
            if (enemy == null) { P.Say("no hostile faction"); return; }
            P.Calm();
            P.FairWeather(map);
            var treb = (Building_TurretGun)P.SpawnBuilding(def, map);
            CompRefuelable fuel = treb.TryGetComp<CompRefuelable>();
            fuel.Refuel(fuel.Props.fuelCapacity / fuel.Props.FuelMultiplierCurrentDifficulty);
            float full = fuel.Fuel;
            Pawn crew = map.mapPawns.FreeColonistsSpawned.FirstOrDefault(p => !p.Downed && !p.WorkTagIsDisabled(WorkTags.Violent));
            if (crew == null) { P.Say("no colonist can man"); treb.Destroy(); return; }
            crew.jobs.StartJob(JobMaker.MakeJob(JobDefOf.ManTurret, treb), JobCondition.InterruptForced);
            bool manned = false;
            for (int i = 0; i < 40 && !manned; i++)
            {
                P.Ticks(100);
                manned = treb.TryGetComp<CompMannable>().MannedNow;
            }
            Pawn target = PawnGenerator.GeneratePawn(PawnKindDefOf.Villager, enemy);
            VerbProperties verb = def.building.turretGunDef.Verbs[0];
            IntVec3 cell = GenRadial.RadialCellsAround(treb.Position, 34f, false)
                .Where(x => x.InBounds(map) && x.DistanceTo(treb.Position) >= verb.minRange + 3f && x.Standable(map) && !x.Fogged(map) && !x.Roofed(map))
                .OrderByDescending(x => x.DistanceTo(treb.Position)).FirstOrDefault();
            if (!cell.IsValid) { P.Say("no cell for the trebuchet target"); treb.Destroy(); return; }
            GenSpawn.Spawn(target, cell, map);
            LordMaker.MakeNewLord(enemy, new LordJob_DefendPoint(cell), map, new[] { target });
            P.Ticks(1500);
            P.Check("crew mans the trebuchet", manned, crew.CurJobDef?.defName ?? "none");
            P.Check("manned trebuchet hurls boulders", fuel.Fuel < full, "fuel " + fuel.Fuel.ToString("F0") + "/" + full.ToString("F0") + ", distance " + treb.Position.DistanceTo(target.Position).ToString("F0")
                + ", target " + (target.Spawned ? "standing" : "gone"));
            crew.jobs.EndCurrentJob(JobCondition.InterruptForced);
            P.Gone(target);
            treb.Destroy();
            P.Calm();
        }
    }
}
