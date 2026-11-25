using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>Hooks the log before any XML loads, so load-time errors are counted too.</summary>
    public class ProbeMod : Mod
    {
        public ProbeMod(ModContentPack content) : base(content)
        {
            P.Hook();
        }
    }

    /// <summary>A patch whose target does not exist: used to prove a broken patch only switches off its own feature.</summary>
    public class BrokenTestPatch : HeirsPatch
    {
        public override string Id => "BrokenTest";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.Need(typeof(ResearchManager), "ThisMethodDoesNotExist_HeirsProbe"), postfix: HeirsPatches.Hook("FinishProject_Postfix"));
        }
    }

    public static class P
    {
        public const BindingFlags Any = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static;
        public static int fails;
        public static int passes;
        public static int brokenWarnings;
        public static bool inGame;
        public static bool finished;
        public static readonly List<string> Errors = new List<string>();
        public static readonly List<string> OtherLoad = new List<string>();
        private static bool hooked;

        public static void Hook()
        {
            if (hooked)
            {
                return;
            }
            hooked = true;
            Application.logMessageReceived += (message, trace, type) =>
            {
                if (message == null || message.StartsWith("HETEST"))
                {
                    return;
                }
                if (message.Contains("[Heirs] feature 'BrokenTest'"))
                {
                    brokenWarnings++;
                    return;
                }
                string line = message.Split('\n')[0];
                bool ours = message.Contains("HE_") || message.Contains("Heirs") || (trace ?? "").Contains("HeirsOfEarth");
                if (type == LogType.Error || type == LogType.Exception || type == LogType.Assert)
                {
                    if (inGame || ours)
                    {
                        if (Errors.Count < 400) Errors.Add(line);
                    }
                    else if (OtherLoad.Count < 50)
                    {
                        OtherLoad.Add(line);
                    }
                }
                else if (type == LogType.Warning && (message.Contains("[Heirs]") || (ours && !inGame)) && Errors.Count < 400)
                {
                    Errors.Add("WARNING " + line);
                }
            };
        }

        public static void Say(string text)
        {
            Debug.Log("HETEST " + text);
        }

        public static void Check(string name, bool ok, string detail = "")
        {
            if (ok)
            {
                passes++;
                return;
            }
            fails++;
            Say("FAIL " + name + (detail.Length > 0 ? " : " + detail : ""));
        }

        public static void Fail(string name, Exception e)
        {
            while (e is TargetInvocationException && e.InnerException != null)
            {
                e = e.InnerException;
            }
            fails++;
            Say("FAIL " + name + ": " + e.GetType().Name + " " + e.Message + "\n" + e.StackTrace);
        }

        public static void Run(string name, Action action)
        {
            try
            {
                action();
            }
            catch (Exception e)
            {
                Fail(name, e);
            }
        }

        public static FieldInfo Field(Type type, string name)
        {
            for (Type t = type; t != null; t = t.BaseType)
            {
                FieldInfo f = t.GetField(name, Any | BindingFlags.DeclaredOnly);
                if (f != null) return f;
            }
            throw new Exception("no field " + name + " on " + type.Name);
        }

        public static object Get(object o, string name) => Field(o.GetType(), name).GetValue(o);

        public static void Set(object o, string name, object value) => Field(o.GetType(), name).SetValue(o, value);

        public static void Ticks(int n)
        {
            for (int i = 0; i < n; i++)
            {
                Find.TickManager.DoSingleTick();
            }
        }

        public static Map Home => Find.Maps.Where(m => m.IsPlayerHome).OrderByDescending(m => m.mapPawns.FreeColonistsSpawnedCount).First();

        public static HeirsGame Game => HeirsGame.Get;

        public static Pawn Colonist(Map map) => map.mapPawns.FreeColonistsSpawned.FirstOrDefault(p => !p.Downed) ?? map.mapPawns.FreeColonistsSpawned.FirstOrDefault();

        public static Pawn Builder(Map map) => map.mapPawns.FreeColonistsSpawned.FirstOrDefault(p => !p.Downed && !StatDefOf.ConstructionSpeed.Worker.IsDisabledFor(p)) ?? Colonist(map);

        public static ResearchProjectDef R(string name) => DefDatabase<ResearchProjectDef>.GetNamed(name);

        public static void CloseWindows()
        {
            foreach (Window w in Find.WindowStack.Windows.ToList())
            {
                string ns = w.GetType().Namespace ?? "";
                if (ns.StartsWith("HeirsOfEarth") || w is Dialog_MessageBox || w is Dialog_NodeTree || w is Dialog_ModSettings)
                {
                    w.Close(false);
                }
            }
        }

        /// <summary>Removes leftover enemies so later steps start from a calm colony.</summary>
        /// <summary>Clear sky and no weather events, so building tests do not depend on the random map's weather.</summary>
        public static void FairWeather(Map map)
        {
            map.weatherManager.curWeather = WeatherDefOf.Clear;
            map.weatherManager.lastWeather = WeatherDefOf.Clear;
            foreach (GameCondition c in map.gameConditionManager.ActiveConditions.ToList())
            {
                c.End();
            }
        }

        /// <summary>Why a joy giver found no job: the facts vanilla checks.</summary>
        public static string JoyWhy(Pawn pawn, Thing building)
        {
            return "no job; outside ok " + JoyUtility.EnjoyableOutsideNow(pawn) + ", weather " + pawn.Map.weatherManager.curWeather.defName
                + ", temp " + pawn.Map.mapTemperature.OutdoorTemp.ToString("F0") + ", hour " + GenLocalDate.HourOfDay(pawn.Map)
                + ", reach " + pawn.CanReach(building, Verse.AI.PathEndMode.Touch, Danger.None) + ", reserve " + Verse.AI.ReservationUtility.CanReserve(pawn, building)
                + ", conditions " + string.Join("/", pawn.Map.gameConditionManager.ActiveConditions.Select(c => c.def.defName))
                + ", pawn " + (pawn.MentalStateDef?.defName ?? "ok") + (pawn.Drafted ? " drafted" : "") + (pawn.Downed ? " downed" : "");
        }

        /// <summary>Removes a test pawn the way the game discards one: destroyed, and every relation to it cleared, so saves stay clean.</summary>
        /// <summary>A scholarly ruler adds a quarter to all knowledge; exact knowledge checks run without one.</summary>
        public static void NotScholarly(NationDef nation)
        {
            Reign r = HeirsCourt.ReignOf(nation);
            if (r != null && r.temperament == Temperament.Scholarly) r.temperament = Temperament.Cautious;
        }

        public static void Gone(Pawn p)
        {
            if (p == null) return;
            if (!p.Destroyed) p.Destroy(DestroyMode.Vanish);
            if (Find.WorldPawns.Contains(p)) Find.WorldPawns.RemoveAndDiscardPawnViaGC(p);
            else if (!p.Discarded) p.Discard(true);
        }

        public static void Calm()
        {
            CloseWindows();
            foreach (Map map in Find.Maps)
            {
                foreach (Pawn p in map.mapPawns.AllPawnsSpawned.ToList())
                {
                    if (!p.Dead && !p.Destroyed && p.HostileTo(Faction.OfPlayer) && !p.IsPrisoner)
                    {
                        Gone(p);
                    }
                }
            }
        }

        public static IntVec3 FreeSpot(Map map, IntVec2 size)
        {
            // Open, reachable ground near the colonists first: on mountain maps the map centre can be a sealed cave,
            // where colonists cannot reach a building and a turret cannot see any raider.
            Pawn colonist = Colonist(map);
            if (colonist != null)
            {
                foreach (IntVec3 c in GenRadial.RadialCellsAround(colonist.Position, 56f, false))
                {
                    if (!c.InBounds(map) || c.DistanceTo(colonist.Position) < 6f) continue;
                    CellRect rect = GenAdj.OccupiedRect(c, Rot4.North, size).ExpandedBy(1);
                    if (rect.InBounds(map) && rect.Cells.All(x => x.Standable(map) && !x.Roofed(map) && !x.Fogged(map) && x.GetFirstBuilding(map) == null && x.GetThingList(map).Count == 0)
                        && colonist.CanReach(c, Verse.AI.PathEndMode.Touch, Danger.Deadly))
                    {
                        return c;
                    }
                }
            }
            foreach (IntVec3 c in GenRadial.RadialCellsAround(map.Center, 50f, true))
            {
                CellRect rect = GenAdj.OccupiedRect(c, Rot4.North, size).ExpandedBy(1);
                if (rect.InBounds(map) && rect.Cells.All(x => x.Standable(map) && x.GetFirstBuilding(map) == null && x.GetThingList(map).Count == 0))
                {
                    return c;
                }
            }
            foreach (IntVec3 c in map.AllCells.OrderBy(x => x.DistanceToSquared(map.Center)))
            {
                CellRect rect = GenAdj.OccupiedRect(c, Rot4.North, size).ExpandedBy(1);
                if (!rect.InBounds(map) || rect.Cells.Any(x => x.GetThingList(map).Any(t => t is Pawn || t.Faction == Faction.OfPlayer)))
                {
                    continue;
                }
                foreach (IntVec3 x in rect.Cells)
                {
                    foreach (Thing t in x.GetThingList(map).ToList())
                    {
                        if (!t.Destroyed) t.Destroy();
                    }
                    map.terrainGrid.SetTerrain(x, TerrainDefOf.Soil);
                    map.roofGrid.SetRoof(x, null);
                }
                return c;
            }
            return IntVec3.Invalid;
        }

        public static Thing SpawnBuilding(ThingDef def, Map map)
        {
            Thing thing = ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
            if (def.CanHaveFaction) thing.SetFaction(Faction.OfPlayer);
            IntVec3 spot = FreeSpot(map, def.size);
            if (!spot.IsValid) throw new Exception("no spot for " + def.defName);
            return GenSpawn.Spawn(thing, spot, map, Rot4.South);
        }

        public static bool HasTexture(string path) => !path.NullOrEmpty() && ContentFinder<Texture2D>.Get(path, false) != null;
    }
}
