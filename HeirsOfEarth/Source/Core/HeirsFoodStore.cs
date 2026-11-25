using System.Collections.Generic;
using System.Linq;
using HarmonyLib;
using RimWorld;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>Marks a storage building whose cells slow down rot, like the Inti qullqa storehouse.</summary>
    public class HeirsFoodStoreExt : DefModExtension
    {
        public float rotFactor = 0.5f;
    }

    /// <summary>Rottable things lying in a food store rot at rotFactor of the normal speed, and their "rots in" readout agrees.</summary>
    public class HeirsFoodStorePatch : HeirsPatch
    {
        public override string Id => "foodStore";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.Need(typeof(CompRottable), "TickInterval", new[] { typeof(int) }),
                prefix: new HarmonyMethod(typeof(HeirsFoodStorePatch), nameof(TickPrefix)),
                postfix: new HarmonyMethod(typeof(HeirsFoodStorePatch), nameof(TickPostfix)));
            harmony.Patch(HeirsPatches.Need(typeof(CompRottable), "TicksUntilRotAtTemp", new[] { typeof(float) }),
                postfix: new HarmonyMethod(typeof(HeirsFoodStorePatch), nameof(TicksUntilPostfix)));
        }

        // 4.2.1: the patch runs for every rottable thing on every map, so the stores are looked up once per map and refreshed every
        // 250 ticks (a store built or torn down takes effect within a few seconds). A map without a store costs one dictionary lookup.
        private static List<ThingDef> storeDefs;
        private static readonly Dictionary<Map, StoreCells> cells = new Dictionary<Map, StoreCells>();
        public const int RefreshTicks = 250;

        private class StoreCells
        {
            public bool built;
            public int builtAt;
            public readonly Dictionary<IntVec3, float> factor = new Dictionary<IntVec3, float>();
        }

        private static List<ThingDef> StoreDefs =>
            storeDefs ??= DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.GetModExtension<HeirsFoodStoreExt>() != null).ToList();

        /// <summary>The store cells of a map with their rot factor.</summary>
        public static Dictionary<IntVec3, float> StoreCellsOf(Map map)
        {
            int now = Find.TickManager?.TicksGame ?? 0;
            if (!cells.TryGetValue(map, out StoreCells c))
            {
                if (cells.Count > 0)
                {
                    foreach (Map gone in cells.Keys.Where(m => !Find.Maps.Contains(m)).ToList())
                    {
                        cells.Remove(gone);
                    }
                }
                c = new StoreCells();
                cells[map] = c;
            }
            if (!c.built || now - c.builtAt >= RefreshTicks || now < c.builtAt)
            {
                c.built = true;
                c.builtAt = now;
                c.factor.Clear();
                foreach (ThingDef def in StoreDefs)
                {
                    float f = def.GetModExtension<HeirsFoodStoreExt>().rotFactor;
                    foreach (Thing store in map.listerThings.ThingsOfDef(def))
                    {
                        foreach (IntVec3 cell in store.OccupiedRect())
                        {
                            if (!c.factor.TryGetValue(cell, out float old) || f < old)
                            {
                                c.factor[cell] = f;
                            }
                        }
                    }
                }
            }
            return c.factor;
        }

        /// <summary>Forgets every map's stores (a new game, or a test that builds stores and wants them seen at once).</summary>
        public static void Reset() => cells.Clear();

        /// <summary>The rot speed factor for a thing, 1 when it is not lying in a food store.</summary>
        public static float FactorFor(Thing thing)
        {
            if (thing == null || !thing.Spawned || StoreDefs.Count == 0)
            {
                return 1f;
            }
            Dictionary<IntVec3, float> map = StoreCellsOf(thing.Map);
            return map.Count > 0 && map.TryGetValue(thing.Position, out float f) ? f : 1f;
        }

        public static void TickPrefix(CompRottable __instance, out float __state)
        {
            __state = __instance.RotProgress;
        }

        public static void TickPostfix(CompRottable __instance, float __state)
        {
            if (__instance.parent == null || __instance.parent.Destroyed)
            {
                return;
            }
            float gained = __instance.RotProgress - __state;
            if (gained <= 0f)
            {
                return;
            }
            float factor = FactorFor(__instance.parent);
            if (factor < 1f)
            {
                __instance.RotProgress = __state + gained * factor;
            }
        }

        public static void TicksUntilPostfix(CompRottable __instance, ref int __result)
        {
            if (__result <= 0 || __result >= int.MaxValue / 4)
            {
                return;
            }
            float factor = FactorFor(__instance.parent);
            if (factor > 0f && factor < 1f)
            {
                __result = (int)(__result / factor);
            }
        }
    }
}
