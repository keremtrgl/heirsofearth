using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;
using Verse.AI.Group;

namespace HeirsOfEarth
{
    /// <summary>How a nation makes war: the raid plan and arrival it prefers and the drill its raiders fight with.</summary>
    public class RaidDoctrine
    {
        public string label;
        public string description;
        public HediffDef hediff;
        public RaidStrategyDef strategy;
        public PawnsArrivalModeDef arrival;
        public float chance = 0.75f;
    }

    /// <summary>
    /// The drill of a raiding nation. It lasts while the pawn fights for its raid and leaves when the pawn is downed,
    /// captured, recruited or goes home. With a formation radius, severity follows how many comrades stand close by.
    /// </summary>
    public class HediffCompProperties_HeirsDoctrine : HediffCompProperties
    {
        public float formationRadius;
        public int formationFull = 4;

        public HediffCompProperties_HeirsDoctrine()
        {
            compClass = typeof(HediffComp_HeirsDoctrine);
        }
    }

    public class HediffComp_HeirsDoctrine : HediffComp
    {
        private bool remove;

        public HediffCompProperties_HeirsDoctrine Props => (HediffCompProperties_HeirsDoctrine)props;

        public override bool CompShouldRemove => remove;

        public override void CompPostTickInterval(ref float severityAdjustment, int delta)
        {
            if (!Pawn.IsHashIntervalTick(120, delta))
            {
                return;
            }
            Refresh();
        }

        public void Refresh()
        {
            Pawn pawn = Pawn;
            if (!pawn.Dead && !pawn.Spawned && pawn.SpawnedOrAnyParentSpawned)
            {
                return; // still in a drop pod or being carried in: keep the drill until the raider lands
            }
            if (pawn.Dead || pawn.Downed || !pawn.Spawned || pawn.IsPrisoner || pawn.Faction == null || pawn.Faction.IsPlayer
                || !pawn.HostileTo(Faction.OfPlayer) || pawn.GetLord() == null)
            {
                remove = true;
                return;
            }
            if (Props.formationRadius > 0f)
            {
                parent.Severity = Mathf.Clamp(Comrades(pawn, Props.formationRadius) / (float)Props.formationFull, 0.01f, 1f);
            }
        }

        public static int Comrades(Pawn pawn, float radius)
        {
            int n = 0;
            float r2 = radius * radius;
            foreach (Pawn other in pawn.Map.mapPawns.SpawnedPawnsInFaction(pawn.Faction))
            {
                if (other != pawn && !other.Downed && other.RaceProps.Humanlike && (other.Position - pawn.Position).LengthHorizontalSquared <= r2)
                {
                    n++;
                }
            }
            return n;
        }
    }

    public static class HeirsDoctrine
    {
        private static Dictionary<FactionDef, NationDef> byFaction;

        public static NationDef NationOf(Faction faction)
        {
            if (faction == null)
            {
                return null;
            }
            if (byFaction == null)
            {
                byFaction = new Dictionary<FactionDef, NationDef>();
                foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
                {
                    if (n.faction != null) byFaction[n.faction] = n;
                }
            }
            return byFaction.TryGetValue(faction.def, out NationDef nation) ? nation : null;
        }

        public static RaidDoctrine DoctrineOf(Faction faction)
        {
            return HeirsMod.Settings.raidDoctrines ? NationOf(faction)?.doctrine : null;
        }

        public static void StrategyPrefix(IncidentParms parms, out bool __state)
        {
            __state = parms.raidStrategy == null;
        }

        /// <summary>Only when the game picked the plan itself (not a forced or scripted raid), and only if the plan fits.</summary>
        public static void StrategyPostfix(IncidentParms parms, PawnGroupKindDef groupKind, bool __state)
        {
            RaidDoctrine d = DoctrineOf(parms.faction);
            if (!__state || d?.strategy == null || parms.raidStrategy == d.strategy || !Rand.Chance(d.chance))
            {
                return;
            }
            if (d.strategy.Worker.CanUseWith(parms, groupKind))
            {
                parms.raidStrategy = d.strategy;
            }
        }

        public static void ArrivalPrefix(IncidentParms parms, out bool __state)
        {
            __state = parms.raidArrivalMode == null;
        }

        public static void ArrivalPostfix(IncidentParms parms, bool __state)
        {
            RaidDoctrine d = DoctrineOf(parms.faction);
            if (!__state || d?.arrival == null || parms.raidStrategy == null || parms.raidArrivalMode == d.arrival)
            {
                return;
            }
            if (parms.raidStrategy.arriveModes != null && parms.raidStrategy.arriveModes.Contains(d.arrival) && d.arrival.Worker.CanUseWith(parms) && Rand.Chance(d.chance))
            {
                parms.raidArrivalMode = d.arrival;
            }
        }

        public static void SpawnedPostfix(IncidentParms parms, List<Pawn> pawns)
        {
            RaidDoctrine d = DoctrineOf(parms.faction);
            if (d?.hediff == null || pawns == null || parms.faction == null || !parms.faction.HostileTo(Faction.OfPlayer))
            {
                return;
            }
            foreach (Pawn pawn in pawns)
            {
                Drill(pawn, d);
            }
        }

        public static void Drill(Pawn pawn, RaidDoctrine d)
        {
            if (pawn?.RaceProps == null || !pawn.RaceProps.Humanlike || pawn.health.hediffSet.HasHediff(d.hediff))
            {
                return;
            }
            Hediff h = pawn.health.AddHediff(d.hediff);
            h.Severity = 0.01f;
        }

        public static void LetterPostfix(IncidentParms parms, ref string __result)
        {
            RaidDoctrine d = DoctrineOf(parms.faction);
            if (d != null && !d.label.NullOrEmpty())
            {
                __result += "\n\n" + "HE_DoctrineLetter".Translate(d.label.CapitalizeFirst(), d.description);
            }
        }
    }

    public class Patch_RaidDoctrine : HeirsPatch
    {
        public override string Id => "RaidDoctrine";

        public override void Apply(HarmonyLib.Harmony harmony)
        {
            System.Type d = typeof(HeirsDoctrine);
            harmony.Patch(HeirsPatches.Need(typeof(IncidentWorker_RaidEnemy), "ResolveRaidStrategy"),
                prefix: new HarmonyLib.HarmonyMethod(d, nameof(HeirsDoctrine.StrategyPrefix)), postfix: new HarmonyLib.HarmonyMethod(d, nameof(HeirsDoctrine.StrategyPostfix)));
            harmony.Patch(HeirsPatches.Need(typeof(IncidentWorker_Raid), "ResolveRaidArriveMode"),
                prefix: new HarmonyLib.HarmonyMethod(d, nameof(HeirsDoctrine.ArrivalPrefix)), postfix: new HarmonyLib.HarmonyMethod(d, nameof(HeirsDoctrine.ArrivalPostfix)));
            harmony.Patch(HeirsPatches.Need(typeof(IncidentWorker_Raid), "PostProcessSpawnedPawns"),
                postfix: new HarmonyLib.HarmonyMethod(d, nameof(HeirsDoctrine.SpawnedPostfix)));
            harmony.Patch(HeirsPatches.Need(typeof(IncidentWorker_RaidEnemy), "GetLetterText"),
                postfix: new HarmonyLib.HarmonyMethod(d, nameof(HeirsDoctrine.LetterPostfix)));
        }
    }
}
