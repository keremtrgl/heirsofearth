using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;
using Verse.AI.Group;

namespace HeirsOfEarth
{
    /// <summary>World-map places that story chain steps send caravans to.</summary>
    public static class HeirsSites
    {
        private const int Radius = 13;
        private const int HoldTicks = 60000 * 60;

        public static HeirsSite Reveal(ChainDef chain, ChainStep step)
        {
            if (!TryFindTile(out PlanetTile tile))
            {
                return null;
            }
            var site = (HeirsSite)WorldObjectMaker.MakeWorldObject(DefDatabase<WorldObjectDef>.GetNamed("HE_ChainSite"));
            site.chain = chain;
            site.stepIndex = chain.steps.IndexOf(step);
            site.Tile = tile;
            site.SetFaction(HeirsChains.HostileFaction(step.enemy));
            Find.WorldObjects.Add(site);
            return site;
        }

        private static bool TryFindTile(out PlanetTile tile)
        {
            PlanetTile fallback = PlanetTile.Invalid;
            for (int i = 0; i < 14; i++)
            {
                if (!TileFinder.TryFindNewSiteTile(out PlanetTile candidate, 5, 22))
                {
                    continue;
                }
                fallback = candidate;
                if (Find.WorldGrid[candidate].hilliness <= Hilliness.LargeHills)
                {
                    tile = candidate;
                    return true;
                }
            }
            tile = fallback;
            return fallback.Valid;
        }

        public static void Build(Map map, ChainStep step, Faction faction)
        {
            IntVec3 center = map.Center;
            int yard = Radius + 8;
            foreach (IntVec3 cell in CellRect.CenteredOn(center, yard).ClipInsideMap(map))
            {
                if (!cell.InHorDistOf(center, yard)) continue;
                foreach (Thing thing in cell.GetThingList(map).ToList())
                {
                    if (!(thing is Pawn) && !thing.Destroyed && thing.def.destroyable)
                    {
                        thing.Destroy(DestroyMode.Vanish);
                    }
                }
                map.roofGrid.SetRoof(cell, null);
                TerrainDef terrain = map.terrainGrid.TerrainAt(cell);
                if (terrain.passability == Traversability.Impassable || terrain.IsWater)
                {
                    map.terrainGrid.SetTerrain(cell, TerrainDefOf.Gravel);
                }
            }
            ThingDef wallStuff = step.siteWall ?? ThingDefOf.BlocksGranite;
            switch (step.siteLayout)
            {
                case "Hall":
                    for (int x = -Radius; x <= Radius; x++)
                    {
                        for (int z = -9; z <= 9; z++)
                        {
                            bool edge = Mathf.Abs(x) == Radius || Mathf.Abs(z) == 9;
                            if (edge && Mathf.Abs(x) > 1 && Mathf.Abs(z) > 1) Wall(map, center + new IntVec3(x, 0, z), wallStuff, faction);
                        }
                    }
                    break;
                case "Ruin":
                    foreach (IntVec3 cell in GenRadial.RadialCellsAround(center, Radius + 1f, true))
                    {
                        if (cell.InBounds(map) && cell.DistanceTo(center) > Radius - 1.5f && Rand.Chance(0.45f) && Mathf.Abs(cell.x - center.x) > 2 && Mathf.Abs(cell.z - center.z) > 2)
                        {
                            Wall(map, cell, wallStuff, faction);
                        }
                    }
                    break;
                default:
                    foreach (IntVec3 cell in GenRadial.RadialCellsAround(center, Radius + 1f, true))
                    {
                        int dx = cell.x - center.x, dz = cell.z - center.z;
                        if (Mathf.Abs(Mathf.Sqrt(dx * dx + dz * dz) - Radius) < 0.75f && Mathf.Abs(dx) > 1 && Mathf.Abs(dz) > 1)
                        {
                            Wall(map, cell, wallStuff, faction);
                        }
                    }
                    break;
            }
            if (step.siteProp != null)
            {
                for (int i = 0; i < 6; i++)
                {
                    float a = i * 60f * Mathf.Deg2Rad;
                    Place(map, center + new IntVec3(Mathf.RoundToInt(Mathf.Cos(a) * 6), 0, Mathf.RoundToInt(Mathf.Sin(a) * 6)), step.siteProp, faction);
                }
            }
            if (step.siteReward != null)
            {
                Thing reward = ThingMaker.MakeThing(step.siteReward, step.siteReward.MadeFromStuff ? GenStuff.DefaultStuffFor(step.siteReward) : null);
                GenPlace.TryPlaceThing(reward, center, map, ThingPlaceMode.Near);
            }
            SpawnDefenders(map, center, step, faction);
        }

        private static void Wall(Map map, IntVec3 cell, ThingDef stuff, Faction faction)
        {
            if (!cell.InBounds(map) || cell.GetEdifice(map) != null) return;
            Thing wall = ThingMaker.MakeThing(ThingDefOf.Wall, stuff);
            wall.SetFaction(faction);
            GenSpawn.Spawn(wall, cell, map, WipeMode.Vanish);
        }

        private static void Place(Map map, IntVec3 cell, ThingDef def, Faction faction)
        {
            if (!cell.InBounds(map) || cell.GetEdifice(map) != null || !GenSpawn.CanSpawnAt(def, cell, map)) return;
            Thing thing = ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
            if (thing.def.CanHaveFaction) thing.SetFaction(faction);
            GenSpawn.Spawn(thing, cell, map, WipeMode.Vanish);
        }

        private static void SpawnDefenders(Map map, IntVec3 center, ChainStep step, Faction faction)
        {
            if (faction == null) return;
            Map home = Find.AnyPlayerHomeMap ?? map;
            float points = Mathf.Clamp(StorytellerUtility.DefaultThreatPointsNow(home) * step.siteThreat, 400f, 4500f) * HeirsMod.Settings.raidStrength;
            var parms = new PawnGroupMakerParms { groupKind = PawnGroupKindDefOf.Combat, tile = map.Tile, faction = faction, points = points };
            List<Pawn> pawns = PawnGroupMakerUtility.GeneratePawns(parms, false).ToList();
            foreach (Pawn pawn in pawns)
            {
                GenSpawn.Spawn(pawn, CellFinder.RandomClosewalkCellNear(center, map, Radius - 3), map);
            }
            if (pawns.Count > 0)
            {
                LordMaker.MakeNewLord(faction, new LordJob_DefendBase(faction, center, HoldTicks), map, pawns);
            }
        }
    }

    public class HeirsSite : MapParent
    {
        private static readonly IntVec3 MapSize = new IntVec3(160, 1, 160);
        public ChainDef chain;
        public int stepIndex;
        private bool built;

        protected override bool UseGenericEnterMapFloatMenuOption => HasMap;

        public ChainStep Step => chain != null && stepIndex >= 0 && stepIndex < chain.steps.Count ? chain.steps[stepIndex] : null;

        public override string Label => Step != null ? Step.label : base.Label;

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Defs.Look(ref chain, "chain");
            Scribe_Values.Look(ref stepIndex, "stepIndex");
            Scribe_Values.Look(ref built, "built");
        }

        public override string GetInspectString()
        {
            string text = base.GetInspectString();
            string goal = Step?.text ?? "";
            return text.NullOrEmpty() ? goal : text + "\n" + goal;
        }

        public override IEnumerable<FloatMenuOption> GetFloatMenuOptions(Caravan caravan)
        {
            foreach (FloatMenuOption option in base.GetFloatMenuOptions(caravan))
            {
                yield return option;
            }
            if (HasMap)
            {
                yield break;
            }
            foreach (FloatMenuOption option in CaravanArrivalActionUtility.GetFloatMenuOptions(() => Spawned, () => new CaravanArrivalAction_HeirsSite(this), "HE_SiteEnter".Translate(Label), caravan, Tile, this))
            {
                yield return option;
            }
        }

        /// <summary>Generates the map (if needed). Also used by the probe.</summary>
        public Map GetOrBuildMap()
        {
            Map map = GetOrGenerateMapUtility.GetOrGenerateMap(Tile, MapSize, null);
            if (!built && Step != null)
            {
                built = true;
                HeirsSites.Build(map, Step, Faction);
            }
            return map;
        }

        public void Enter(Caravan caravan)
        {
            bool fresh = !HasMap;
            Map map = GetOrBuildMap();
            if (fresh)
            {
                Find.TickManager.Notify_GeneratedPotentiallyHostileMap();
            }
            CaravanEnterMapUtility.Enter(caravan, map, CaravanEnterMode.Edge, CaravanDropInventoryMode.DoNotDrop, true);
        }

        public override bool ShouldRemoveMapNow(out bool alsoRemoveWorldObject)
        {
            alsoRemoveWorldObject = false;
            Map map = Map;
            if (map.mapPawns.AnyPawnBlockingMapRemoval || map.AnyBuildingBlockingMapRemoval || TransporterUtility.IncomingTransporterPreventingMapRemoval(map))
            {
                return false;
            }
            HeirsGame game = HeirsGame.Get;
            alsoRemoveWorldObject = game == null || chain == null || game.State(chain).step != stepIndex || game.State(chain).done;
            return true;
        }

        public override void Notify_MyMapRemoved(Map map)
        {
            base.Notify_MyMapRemoved(map);
            built = false;
        }
    }

    public class CaravanArrivalAction_HeirsSite : CaravanArrivalAction
    {
        private HeirsSite site;

        public CaravanArrivalAction_HeirsSite()
        {
        }

        public CaravanArrivalAction_HeirsSite(HeirsSite site)
        {
            this.site = site;
        }

        public override string Label => "HE_SiteEnter".Translate(site?.Label ?? "");

        public override string ReportString => "HE_SiteEntering".Translate(site?.Label ?? "");

        public override FloatMenuAcceptanceReport StillValid(Caravan caravan, PlanetTile destinationTile)
        {
            FloatMenuAcceptanceReport report = base.StillValid(caravan, destinationTile);
            if (!report) return report;
            return site != null && site.Spawned && site.Tile == destinationTile;
        }

        public override void Arrived(Caravan caravan)
        {
            if (site.HasMap)
            {
                site.Enter(caravan);
                return;
            }
            LongEventHandler.QueueLongEvent(() => site.Enter(caravan), "GeneratingMapForNewEncounter", false, null);
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_References.Look(ref site, "site");
        }
    }
}
