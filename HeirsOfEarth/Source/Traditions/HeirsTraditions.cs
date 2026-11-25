using System.Collections.Generic;
using System.Linq;
using System.Text;
using HarmonyLib;
using RimWorld;
using RimWorld.Planet;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>Traditions: finished heritage projects that change game rules.</summary>
    public static class HeirsTraditions
    {
        private static List<(ResearchProjectDef project, HeirsResearchExt ext)> active;
        private static Game cachedFor;

        public static void Dirty()
        {
            active = null;
        }

        public static bool Active(ResearchProjectDef project)
        {
            HeirsResearchExt ext = project.GetModExtension<HeirsResearchExt>();
            return ext != null && ext.tradition && Current.Game != null && project.IsFinished && HeirsMod.Settings.TraditionsEnabled(ext.nation);
        }

        public static List<(ResearchProjectDef project, HeirsResearchExt ext)> ActiveList
        {
            get
            {
                if (Current.Game == null)
                {
                    return new List<(ResearchProjectDef, HeirsResearchExt)>();
                }
                if (active == null || cachedFor != Current.Game)
                {
                    cachedFor = Current.Game;
                    active = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Where(Active).Select(p => (p, p.GetModExtension<HeirsResearchExt>())).ToList();
                }
                return active;
            }
        }

        public static float StudyBonus(NationDef nation)
        {
            return ActiveList.Where(a => a.ext.nation == nation || a.ext.nation == null).Sum(a => a.ext.studyFactor);
        }

        public static void InstallStatParts()
        {
            var stats = new HashSet<StatDef>();
            foreach (ResearchProjectDef project in DefDatabase<ResearchProjectDef>.AllDefsListForReading)
            {
                HeirsResearchExt ext = project.GetModExtension<HeirsResearchExt>();
                if (ext?.stats == null) continue;
                foreach (StatEffect effect in ext.stats)
                {
                    if (effect.stat != null) stats.Add(effect.stat);
                }
            }
            foreach (StatDef stat in stats)
            {
                if (stat.parts == null) stat.parts = new List<StatPart>();
                if (!stat.parts.Any(p => p is StatPart_HeirsTradition))
                {
                    stat.parts.Add(new StatPart_HeirsTradition { parentStat = stat });
                }
            }
        }

        public static bool InScope(Thing thing, EffectScope scope)
        {
            if (thing == null || thing.Faction != Faction.OfPlayerSilentFail || Faction.OfPlayerSilentFail == null)
            {
                return false;
            }
            return scope == EffectScope.Colonists ? thing is Pawn pawn && pawn.RaceProps.Humanlike : thing is Building;
        }

        public static QualityCategory RaiseQuality(Pawn pawn, QualityCategory quality)
        {
            if (pawn == null || pawn.Faction != Faction.OfPlayerSilentFail || quality >= QualityCategory.Masterwork)
            {
                return quality;
            }
            float chance = ActiveList.Sum(a => a.ext.qualityChance);
            return chance > 0f && Rand.Chance(chance) ? quality + 1 : quality;
        }

        public static int CaravanTicks(Caravan caravan, StringBuilder explanation, int ticks)
        {
            if (caravan == null || caravan.Faction != Faction.OfPlayerSilentFail)
            {
                return ticks;
            }
            float bonus = ActiveList.Sum(a => a.ext.caravanSpeed);
            if (bonus <= 0f)
            {
                return ticks;
            }
            explanation?.AppendLine().Append("  " + "HE_CaravanTradition".Translate(bonus.ToStringPercent()));
            return UnityEngine.Mathf.Max(1, UnityEngine.Mathf.RoundToInt(ticks / (1f + bonus)));
        }
    }

    public class StatPart_HeirsTradition : StatPart
    {
        public override void TransformValue(StatRequest req, ref float val)
        {
            if (!req.HasThing) return;
            foreach (var (_, ext) in HeirsTraditions.ActiveList)
            {
                foreach (StatEffect e in ext.stats)
                {
                    if (e.stat == parentStat && HeirsTraditions.InScope(req.Thing, e.scope))
                    {
                        val = (val + e.offset) * e.factor;
                    }
                }
            }
        }

        public override string ExplanationPart(StatRequest req)
        {
            if (!req.HasThing) return null;
            var sb = new StringBuilder();
            foreach (var (project, ext) in HeirsTraditions.ActiveList)
            {
                foreach (StatEffect e in ext.stats)
                {
                    if (e.stat != parentStat || !HeirsTraditions.InScope(req.Thing, e.scope)) continue;
                    string value = e.offset != 0f ? e.offset.ToStringByStyle(parentStat.toStringStyle, ToStringNumberSense.Offset) : "x" + e.factor.ToStringPercent();
                    sb.AppendLine("HE_TraditionStat".Translate(project.LabelCap) + ": " + value);
                }
            }
            return sb.Length > 0 ? sb.ToString().TrimEndNewlines() : null;
        }
    }

    public class Patch_Quality : HeirsPatch
    {
        public override string Id => "MasterCraft";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.Need(typeof(QualityUtility), "GenerateQualityCreatedByPawn", new[] { typeof(Pawn), typeof(SkillDef), typeof(bool) }), postfix: HeirsPatches.Hook("Quality_Postfix"));
        }
    }

    public class Patch_CaravanSpeed : HeirsPatch
    {
        public override string Id => "CaravanSpeed";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.Need(typeof(CaravanTicksPerMoveUtility), "GetTicksPerMove", new[] { typeof(Caravan), typeof(StringBuilder) }), postfix: HeirsPatches.Hook("CaravanTicks_Postfix"));
        }
    }
}
