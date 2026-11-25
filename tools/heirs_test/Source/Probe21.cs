using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>2.1 checks: nations added to old saves, the industrial rows, the battery, the mill, the Hellas facilities and the sounds.</summary>
    public static class Probe21
    {
        public static void Content()
        {
            foreach (string gun in new[] { "HE_Roma_Carbine", "HE_Yamato_Tanegashima", "HE_Nord_HarpoonGun" })
            {
                ThingDef def = DefDatabase<ThingDef>.GetNamed(gun);
                P.Check("industrial gun " + gun, def.techLevel == TechLevel.Industrial && def.Verbs[0].defaultProjectile != null && def.recipeMaker?.researchPrerequisite != null,
                        def.Verbs[0].defaultProjectile?.defName ?? "none");
                P.Check("gun not given to archers " + gun, !def.weaponTags.Any(t => t.EndsWith("Ranged")), string.Join(",", def.weaponTags));
                P.Check("gun texture " + gun, P.HasTexture(def.graphicData.texPath));
            }
            P.Check("harpoon texture", P.HasTexture(DefDatabase<ThingDef>.GetNamed("HE_Projectile_Harpoon").graphicData.texPath));
            foreach (string t in new[] { "HE_Roma_CivilCode", "HE_Yamato_Sakai", "HE_Nord_FolkSchools" })
            {
                ResearchProjectDef r = P.R(t);
                HeirsResearchExt ext = r.GetModExtension<HeirsResearchExt>();
                P.Check("industrial tradition " + t, r.techLevel == TechLevel.Industrial && ext != null && ext.tradition && ext.stats.Count > 0);
            }
            var spots = new Dictionary<Vector2, string>();
            bool overlap = false;
            string clash = "";
            foreach (ResearchProjectDef r in DefDatabase<ResearchProjectDef>.AllDefsListForReading.Where(x => x.tab?.defName == "HE_WorldHeritage"))
            {
                var key = new Vector2(Mathf.Round(r.ResearchViewX * 100f), Mathf.Round(r.ResearchViewY * 100f));
                if (spots.TryGetValue(key, out string other))
                {
                    overlap = true;
                    clash = other + " / " + r.defName;
                }
                spots[key] = r.defName;
            }
            P.Check("research nodes do not overlap", !overlap, clash);

            ThingDef tweed = DefDatabase<ThingDef>.GetNamed("HE_Albion_Tweed");
            P.Check("tweed is fabric", tweed.IsStuff && tweed.stuffProps.categories.Contains(StuffCategoryDefOf.Fabric));
            P.Check("tweed makes dusters", GenStuff.AllowedStuffsFor(DefDatabase<ThingDef>.GetNamed("Apparel_Duster")).Contains(tweed));
            ThingDef mill = DefDatabase<ThingDef>.GetNamed("HE_Albion_TextileMill");
            RecipeDef weave = DefDatabase<RecipeDef>.GetNamed("HE_Albion_WeaveTweed");
            P.Check("mill weaves tweed", mill.AllRecipes.Contains(weave) && weave.products[0].thingDef == tweed);
            P.Check("mill takes sheep wool", weave.fixedIngredientFilter.Allows(DefDatabase<ThingDef>.GetNamed("WoolSheep")));

            foreach (string s in new[] { "HE_Sound_Horn", "HE_Sound_Bugle", "HE_Sound_Gong", "HE_Sound_Drum" })
            {
                SoundDef sd = DefDatabase<SoundDef>.GetNamedSilentFail(s);
                string clip = (sd?.subSounds?.FirstOrDefault()?.grains?.FirstOrDefault() as Verse.Sound.AudioGrain_Clip)?.clipPath;
                P.Check("sound " + s, sd != null && clip != null && ContentFinder<AudioClip>.Get(clip, false) != null, clip ?? "no clip");
            }
            LetterDef war = DefDatabase<LetterDef>.GetNamedSilentFail("HE_WarLetter");
            P.Check("war letter plays the horn", war != null && war.arriveSound?.defName == "HE_Sound_Horn");
            int sounded = DefDatabase<ThingDef>.AllDefsListForReading.Count(d => d.GetCompProperties<CompProperties_HeirsArtifact>()?.sound != null);
            P.Check("artifact sounds", sounded >= 5, sounded.ToString());
            P.Run("play sounds", () =>
            {
                foreach (string s in new[] { "HE_Sound_Horn", "HE_Sound_Bugle", "HE_Sound_Gong", "HE_Sound_Drum" })
                {
                    Verse.Sound.SoundStarter.PlayOneShotOnCamera(DefDatabase<SoundDef>.GetNamed(s), P.Home);
                }
            });
        }

        public static void Buildings()
        {
            Map map = P.Home;
            P.Run("fire-arrow battery", () =>
            {
                P.FairWeather(map);
                var turret = (Building_TurretGun)P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Tianxia_FireArrowBattery"), map);
                CompRefuelable fuel = turret.TryGetComp<CompRefuelable>();
                P.Check("battery gun", turret.gun != null && turret.gun.def.defName == "HE_Tianxia_FireArrowBattery_Gun");
                P.Check("battery starts empty", fuel != null && fuel.Fuel == 0f);
                fuel.Refuel(32f);
                P.Check("battery loaded", fuel.Fuel >= 63.9f, fuel.Fuel.ToString("F0"));
                Faction enemy = Find.FactionManager.AllFactions.FirstOrDefault(f => !f.IsPlayer && f.HostileTo(Faction.OfPlayer) && f.def.humanlikeFaction);
                Pawn target = null;
                if (enemy != null)
                {
                    target = PawnGenerator.GeneratePawn(PawnKindDefOf.Villager, enemy);
                    // A raider the battery can see: open ground in range, in its line of sight, not fogged. A lone idle
                    // villager dropped behind a rock was not always a target, which made this check fail now and then.
                    IntVec3 cell = GenRadial.RadialCellsAround(turret.Position, 16f, false)
                        .Where(x => x.InBounds(map) && x.DistanceTo(turret.Position) >= 9f && x.Standable(map) && !x.Fogged(map)
                                    && GenSight.LineOfSight(turret.Position, x, map, true))
                        .OrderBy(x => x.Roofed(map) ? 1 : 0).FirstOrDefault();
                    if (!cell.IsValid)
                    {
                        cell = CellFinder.RandomClosewalkCellNear(turret.Position + new IntVec3(12, 0, 0), map, 3);
                    }
                    GenSpawn.Spawn(target, cell, map);
                    Verse.AI.Group.LordMaker.MakeNewLord(enemy, new LordJob_AssaultColony(enemy, false, false, false, false, false), map, new[] { target });
                    P.Ticks(900);
                    P.Check("battery fires", fuel.Fuel < 64f, "fuel " + fuel.Fuel.ToString("F0") + ", weather " + map.weatherManager.curWeather.defName + ", target " + (target.Dead ? "dead" : target.Downed ? "downed" : target.Spawned ? "standing" : "gone") + ", turret target " + (turret.CurrentTarget.Thing?.LabelShort ?? "none") + ", target hp " + target.health.summaryHealth.SummaryHealthPercent.ToString("F2") + ", sight " + GenSight.LineOfSight(turret.Position, target.Position, map, true) + ", distance " + turret.Position.DistanceTo(target.Position).ToString("F0") + ", roof " + (turret.Position.GetRoof(map)?.defName ?? "none"));
                    P.Gone(target);
                }
                else
                {
                    P.Say("no hostile faction for the battery shot test");
                }
                turret.Destroy();
            });
            P.Run("textile mill", () =>
            {
                Thing mill = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Albion_TextileMill"), map);
                P.Check("mill is a work table", mill is Building_WorkTable && mill.TryGetComp<CompPowerTrader>() != null && mill.def.hasInteractionCell);
                mill.Destroy();
            });
            P.Run("lyceum links to bench", () =>
            {
                // 4.2.1: both go into one cleared 10x10 patch, the lyceum 4 cells north of the bench (it links within 8), so the
                // test no longer depends on a random cell that could be out of reach or behind a wall.
                IntVec3 patch = P.FreeSpot(map, new IntVec2(10, 10));
                Thing bench = ThingMaker.MakeThing(ThingDefOf.SimpleResearchBench, GenStuff.DefaultStuffFor(ThingDefOf.SimpleResearchBench));
                bench.SetFaction(Faction.OfPlayer);
                GenSpawn.Spawn(bench, patch + new IntVec3(0, 0, -2), map, Rot4.South);
                float before = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                ThingDef lyceumDef = DefDatabase<ThingDef>.GetNamed("HE_Hellas_Lyceum");
                Thing lyceum = ThingMaker.MakeThing(lyceumDef, GenStuff.DefaultStuffFor(lyceumDef));
                lyceum.SetFaction(Faction.OfPlayer);
                GenSpawn.Spawn(lyceum, patch + new IntVec3(0, 0, 2), map, Rot4.North);
                P.Ticks(10);
                CompAffectedByFacilities links = bench.TryGetComp<CompAffectedByFacilities>();
                float after = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                P.Check("lyceum linked", links != null && links.LinkedFacilitiesListForReading.Contains(lyceum), links == null ? "bench has no facility comp" : links.LinkedFacilitiesListForReading.Count + " links");
                // The +6% offset is applied before the room, cleanliness and light factors, so on a bare test bench it shows smaller.
                float offset = links?.LinkedFacilitiesListForReading.Contains(lyceum) == true ? lyceumDef.GetCompProperties<CompProperties_Facility>().statOffsets.GetStatOffsetFromList(StatDefOf.ResearchSpeedFactor) : 0f;
                P.Check("lyceum speeds research", after > before + 0.005f && Mathf.Abs(offset - 0.06f) < 0.001f, before.ToString("F2") + " -> " + after.ToString("F2") + ", offset " + offset.ToString("F2"));
                lyceum.Destroy();
                bench.Destroy();
            });
            P.Run("asclepion links to bed", () =>
            {
                ThingDef bedDef = DefDatabase<ThingDef>.GetNamed("Bed");
                Thing bed = ThingMaker.MakeThing(bedDef, GenStuff.DefaultStuffFor(bedDef));
                bed.SetFaction(Faction.OfPlayer);
                IntVec3 spot = P.FreeSpot(map, new IntVec2(3, 3));
                GenSpawn.Spawn(bed, spot, map, Rot4.South);
                ThingDef shrineDef = DefDatabase<ThingDef>.GetNamed("HE_Hellas_Asclepion");
                Thing shrine = ThingMaker.MakeThing(shrineDef, GenStuff.DefaultStuffFor(shrineDef));
                shrine.SetFaction(Faction.OfPlayer);
                GenSpawn.Spawn(shrine, spot + new IntVec3(2, 0, 0), map, Rot4.North);
                P.Ticks(10);
                CompAffectedByFacilities links = bed.TryGetComp<CompAffectedByFacilities>();
                P.Check("asclepion linked", links != null && links.LinkedFacilitiesListForReading.Contains(shrine), links == null ? "no comp" : links.LinkedFacilitiesListForReading.Count + " links");
                P.Check("asclepion tend bonus", bed.GetStatValue(StatDefOf.MedicalTendQualityOffset) >= 0.039f, bed.GetStatValue(StatDefOf.MedicalTendQualityOffset).ToString("F3"));
                shrine.Destroy();
                bed.Destroy();
            });
        }

        public static void MissingNations()
        {
            int factions = Find.FactionManager.AllFactionsListForReading.Count;
            P.Check("no missing nations in a new world", HeirsWorldHooks.AddMissingNations().Count == 0 && Find.FactionManager.AllFactionsListForReading.Count == factions);
            NationDef hellas = DefDatabase<NationDef>.GetNamed("HE_Hellas");
            int settlements = Find.WorldObjects.Settlements.Count;
            Faction added = HeirsWorldHooks.AddNation(hellas, 3);
            int placed = Find.WorldObjects.Settlements.Count(s => s.Faction == added);
            P.Check("added nation faction", added != null && Find.FactionManager.AllFactionsListForReading.Contains(added) && added.leader != null, added?.Name ?? "null");
            P.Check("added nation settlements", placed >= 1 && Find.WorldObjects.Settlements.Count == settlements + placed, placed.ToString());
            P.Check("added nation relations", added.RelationWith(Faction.OfPlayer, true) != null
                    && Find.FactionManager.AllFactionsListForReading.Where(f => f != added && !f.def.hidden).All(f => added.RelationWith(f, true) != null));
            P.Check("added settlements named", Find.WorldObjects.Settlements.Where(s => s.Faction == added).All(s => !s.Name.NullOrEmpty()));
            P.Check("added nation chronicle", P.Game.chronicle.Any(c => c.text != null && c.text.Contains(hellas.LabelCap)));
            bool was = HeirsMod.Settings.addMissingNations;
            HeirsMod.Settings.addMissingNations = false;
            P.Check("add missing respects setting", HeirsWorldHooks.AddMissingNations().Count == 0);
            HeirsMod.Settings.addMissingNations = was;
        }
    }
}
