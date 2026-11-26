using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>One isolated game rule change. If it cannot be applied, only its feature switches off.</summary>
    public abstract class HeirsPatch
    {
        public abstract string Id { get; }

        public abstract void Apply(Harmony harmony);
    }

    public static class HeirsPatches
    {
        public const string HarmonyId = "kerem.heirs";
        private static readonly Dictionary<string, bool> status = new Dictionary<string, bool>();
        private static Harmony harmony;

        public static IReadOnlyDictionary<string, bool> Status => status;

        public static bool Active(string id)
        {
            return status.TryGetValue(id, out bool on) && on;
        }

        public static void ApplyAll()
        {
            foreach (Type type in typeof(HeirsPatches).Assembly.GetTypes().Where(t => t.IsSubclassOf(typeof(HeirsPatch)) && !t.IsAbstract).OrderBy(t => t.Name))
            {
                TryApply((HeirsPatch)Activator.CreateInstance(type));
            }
        }

        public static bool TryApply(HeirsPatch patch)
        {
            if (harmony == null)
            {
                harmony = new Harmony(HarmonyId);
            }
            try
            {
                patch.Apply(harmony);
                status[patch.Id] = true;
                return true;
            }
            catch (Exception e)
            {
                status[patch.Id] = false;
                string reason = e.Message;
                for (Exception inner = e.InnerException; inner != null; inner = inner.InnerException)
                {
                    reason += " -> " + inner.GetType().Name + ": " + inner.Message;
                }
                Log.Warning("[Heirs] feature '" + patch.Id + "' disabled: " + reason);
                return false;
            }
        }

        public static MethodInfo Need(Type type, string name, Type[] args = null)
        {
            MethodInfo method = AccessTools.Method(type, name, args);
            if (method == null)
            {
                throw new MissingMethodException(type.Name, name);
            }
            return method;
        }

        public static MethodInfo NeedGetter(Type type, string property)
        {
            MethodInfo method = AccessTools.PropertyGetter(type, property);
            if (method == null)
            {
                throw new MissingMethodException(type.Name, "get_" + property);
            }
            return method;
        }

        public static HarmonyMethod Hook(string name)
        {
            return new HarmonyMethod(AccessTools.Method(typeof(HeirsPatchHooks), name));
        }
    }

    [StaticConstructorOnStartup]
    public static class HeirsStartup
    {
        static HeirsStartup()
        {
            HeirsPatches.ApplyAll();
            HeirsTraditions.InstallStatParts();
            HeirsKnowledge.ApplyResearchCost();
            HeirsWorks.CopyRecipes();
            HeirsAges.OnAgeReached += HeirsEvents.OnAgeReached;
        }
    }

    /// <summary>All Harmony prefix and postfix bodies, kept thin: they forward to feature code.</summary>
    public static class HeirsPatchHooks
    {
        public static void CanStartNow_Postfix(ResearchProjectDef __instance, ref bool __result)
        {
            if (__result && !HeirsKnowledge.Allowed(__instance))
            {
                __result = false;
            }
        }

        public static void FinishProject_Postfix(ResearchProjectDef proj)
        {
            HeirsKnowledge.OnProjectFinished(proj);
        }

        public static void ResearchPerformed_Postfix(float amount, Pawn researcher)
        {
            HeirsKnowledge.OnResearchPerformed(amount, researcher);
        }

        public static void Quality_Postfix(Pawn pawn, ref RimWorld.QualityCategory __result)
        {
            __result = HeirsTraditions.RaiseQuality(pawn, __result);
        }

        public static void CaravanTicks_Postfix(RimWorld.Planet.Caravan caravan, System.Text.StringBuilder explanation, ref int __result)
        {
            __result = HeirsTraditions.CaravanTicks(caravan, explanation, __result);
        }
    }
}
