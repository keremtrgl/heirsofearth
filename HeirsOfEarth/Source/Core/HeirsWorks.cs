using System.Collections.Generic;
using System.Linq;
using HarmonyLib;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>4.3 Albion telegraph office: while powered it sends greetings every quadrum, +goodwill with each heir nation that is not
    /// hostile. Only one telegraph counts per game, however many are built.</summary>
    public class CompProperties_HeirsTelegraph : CompProperties
    {
        public int goodwill = 1;
        public float intervalDays = 15f;

        public CompProperties_HeirsTelegraph()
        {
            compClass = typeof(CompHeirsTelegraph);
        }
    }

    public class CompHeirsTelegraph : ThingComp
    {
        public CompProperties_HeirsTelegraph Props => (CompProperties_HeirsTelegraph)props;

        public bool Working => parent.Spawned && (parent.TryGetComp<CompPowerTrader>()?.PowerOn ?? true);

        public override string CompInspectStringExtra()
        {
            HeirsGame g = HeirsGame.Get;
            if (g == null || !Working)
            {
                return null;
            }
            int left = HeirsWorks.NextTelegramTick(g, Props) - Find.TickManager.TicksGame;
            return "HE_TelegraphNext".Translate(Mathf.Max(0, left).ToStringTicksToPeriod());
        }
    }

    /// <summary>4.3 Kemet irrigation pump: while powered, plants within the radius grow faster.</summary>
    public class CompProperties_HeirsIrrigation : CompProperties
    {
        public float radius = 6f;
        public float growthFactor = 1.15f;

        public CompProperties_HeirsIrrigation()
        {
            compClass = typeof(CompHeirsIrrigation);
        }
    }

    public class CompHeirsIrrigation : ThingComp
    {
        public CompProperties_HeirsIrrigation Props => (CompProperties_HeirsIrrigation)props;

        public override void PostDrawExtraSelectionOverlays()
        {
            GenDraw.DrawRadiusRing(parent.Position, Props.radius);
        }
    }

    /// <summary>A work table that also takes every bill of other tables (the Nord electric forge and the Pars electric carpet loom).
    /// Copied once at startup, after the implied recipes exist, so modded recipes for those tables come along too.</summary>
    public class HeirsCopyRecipesExt : DefModExtension
    {
        public List<ThingDef> from = new List<ThingDef>();
    }

    public static class HeirsWorks
    {
        // ------------------------------------------------------------------ recipes
        public static void CopyRecipes()
        {
            foreach (ThingDef table in DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.GetModExtension<HeirsCopyRecipesExt>() != null).ToList())
            {
                List<ThingDef> from = table.GetModExtension<HeirsCopyRecipesExt>().from.Where(f => f != null).ToList();
                foreach (RecipeDef recipe in DefDatabase<RecipeDef>.AllDefsListForReading)
                {
                    if (recipe.recipeUsers != null && recipe.recipeUsers.Any(from.Contains) && !recipe.recipeUsers.Contains(table))
                    {
                        recipe.recipeUsers.Add(table);
                    }
                }
                foreach (ThingDef source in from)
                {
                    if (source.recipes == null)
                    {
                        continue;
                    }
                    table.recipes ??= new List<RecipeDef>();
                    foreach (RecipeDef recipe in source.recipes.Where(r => !table.recipes.Contains(r)))
                    {
                        table.recipes.Add(recipe);
                    }
                }
                Traverse.Create(table).Field("allRecipesCached").SetValue(null);
            }
        }

        // ------------------------------------------------------------------ telegraph
        private static List<ThingDef> telegraphDefs;

        private static List<ThingDef> TelegraphDefs =>
            telegraphDefs ??= DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.HasComp(typeof(CompHeirsTelegraph))).ToList();

        public static int NextTelegramTick(HeirsGame g, CompProperties_HeirsTelegraph props) =>
            g.lastTelegramTick + (int)(props.intervalDays * GenDate.TicksPerDay);

        /// <summary>The first powered telegraph office on any player map, or null.</summary>
        public static CompHeirsTelegraph WorkingTelegraph()
        {
            if (TelegraphDefs.Count == 0)
            {
                return null;
            }
            foreach (Map map in Find.Maps.Where(m => m.IsPlayerHome))
            {
                foreach (ThingDef def in TelegraphDefs)
                {
                    foreach (Thing t in map.listerThings.ThingsOfDef(def))
                    {
                        CompHeirsTelegraph comp = t.TryGetComp<CompHeirsTelegraph>();
                        if (comp != null && comp.Working && t.Faction == Faction.OfPlayer)
                        {
                            return comp;
                        }
                    }
                }
            }
            return null;
        }

        /// <summary>Called every 2500 ticks: sends the telegrams once the interval has passed.</summary>
        public static void TickRare(HeirsGame g)
        {
            CompHeirsTelegraph telegraph = WorkingTelegraph();
            if (telegraph == null)
            {
                return;
            }
            if (g.lastTelegramTick <= 0)
            {
                // the first office starts the clock; it does not pay out the moment it is switched on
                g.lastTelegramTick = Find.TickManager.TicksGame;
                return;
            }
            if (Find.TickManager.TicksGame >= NextTelegramTick(g, telegraph.Props))
            {
                SendTelegrams(g, telegraph);
            }
        }

        /// <summary>Raises goodwill with each heir nation that is not hostile; returns how many were raised. Does nothing without a
        /// powered office.</summary>
        public static int SendTelegrams(HeirsGame g, CompHeirsTelegraph telegraph = null)
        {
            telegraph ??= WorkingTelegraph();
            if (telegraph == null)
            {
                return 0;
            }
            g.lastTelegramTick = Find.TickManager.TicksGame;
            List<string> names = new List<string>();
            foreach (NationDef n in HeirsWorld.LiveNations.ToList())
            {
                Faction f = HeirsWorld.FactionOf(n);
                if (f == null || f.IsPlayer || f.HostileTo(Faction.OfPlayer))
                {
                    continue;
                }
                if (f.TryAffectGoodwillWith(Faction.OfPlayer, telegraph.Props.goodwill, false, false, null))
                {
                    names.Add(f.Name);
                }
            }
            if (names.Count > 0)
            {
                Messages.Message("HE_TelegraphSent".Translate(telegraph.Props.goodwill, names.ToCommaList(true)), telegraph.parent,
                    MessageTypeDefOf.PositiveEvent, false);
            }
            return names.Count;
        }

        // ------------------------------------------------------------------ irrigation
        private static List<ThingDef> pumpDefs;
        private static readonly Dictionary<Map, Irrigated> irrigated = new Dictionary<Map, Irrigated>();
        public const int RefreshTicks = 250;

        private class Irrigated
        {
            public bool built;
            public int builtAt;
            public readonly Dictionary<IntVec3, float> factor = new Dictionary<IntVec3, float>();
        }

        private static List<ThingDef> PumpDefs =>
            pumpDefs ??= DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.HasComp(typeof(CompHeirsIrrigation))).ToList();

        public static void ResetIrrigation() => irrigated.Clear();

        /// <summary>The cells a map's powered pumps water, with their growth factor; rebuilt every 250 ticks.</summary>
        public static Dictionary<IntVec3, float> IrrigatedCells(Map map)
        {
            int now = Find.TickManager?.TicksGame ?? 0;
            if (!irrigated.TryGetValue(map, out Irrigated c))
            {
                foreach (Map gone in irrigated.Keys.Where(m => !Find.Maps.Contains(m)).ToList())
                {
                    irrigated.Remove(gone);
                }
                c = new Irrigated();
                irrigated[map] = c;
            }
            if (!c.built || now - c.builtAt >= RefreshTicks || now < c.builtAt)
            {
                c.built = true;
                c.builtAt = now;
                c.factor.Clear();
                foreach (ThingDef def in PumpDefs)
                {
                    foreach (Thing pump in map.listerThings.ThingsOfDef(def))
                    {
                        if (!(pump.TryGetComp<CompPowerTrader>()?.PowerOn ?? true))
                        {
                            continue;
                        }
                        CompProperties_HeirsIrrigation props = pump.TryGetComp<CompHeirsIrrigation>().Props;
                        foreach (IntVec3 cell in GenRadial.RadialCellsAround(pump.Position, props.radius, true))
                        {
                            if (cell.InBounds(map) && (!c.factor.TryGetValue(cell, out float old) || props.growthFactor > old))
                            {
                                c.factor[cell] = props.growthFactor;
                            }
                        }
                    }
                }
            }
            return c.factor;
        }

        public static float GrowthFactorFor(Plant plant)
        {
            if (plant == null || !plant.Spawned || PumpDefs.Count == 0)
            {
                return 1f;
            }
            Dictionary<IntVec3, float> cells = IrrigatedCells(plant.Map);
            return cells.Count > 0 && cells.TryGetValue(plant.Position, out float f) ? f : 1f;
        }
    }

    /// <summary>Plants on irrigated cells grow faster (the growth rate is what Plant.TickLong adds up, so the readout agrees).</summary>
    public class HeirsIrrigationPatch : HeirsPatch
    {
        public override string Id => "irrigation";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.NeedGetter(typeof(Plant), "GrowthRate"),
                postfix: new HarmonyMethod(typeof(HeirsIrrigationPatch), nameof(GrowthRatePostfix)));
        }

        public static void GrowthRatePostfix(Plant __instance, ref float __result)
        {
            if (__result > 0f)
            {
                __result *= HeirsWorks.GrowthFactorFor(__instance);
            }
        }
    }
}
