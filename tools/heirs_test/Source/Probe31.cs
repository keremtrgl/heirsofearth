using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>3.1 checks: settlement icons, research browser filters, encyclopedia entries, difficulty presets and tribute setting.</summary>
    public static class Probe31
    {
        public static void Settlements()
        {
            int ok = 0;
            var bad = new List<string>();
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                string want = "HeirsOfEarth/World/HE_Settlement_" + nation.defName.Substring(3);
                FactionDef f = nation.faction;
                bool good = f != null && f.settlementTexturePath == want && ContentFinder<Texture2D>.Get(want, false) != null && f.SettlementTexture != BaseContent.BadTex;
                if (good) ok++;
                else bad.Add(nation.defName + ":" + f?.settlementTexturePath);
            }
            P.Check("every nation has its own settlement icon", ok == DefDatabase<NationDef>.DefCount && ok == 9, ok + " " + string.Join(" ", bad));
            int distinct = DefDatabase<NationDef>.AllDefsListForReading.Select(n => n.faction.settlementTexturePath).Distinct().Count();
            P.Check("settlement icons are all different", distinct == 9, distinct.ToString());
            Settlement s = Find.WorldObjects.Settlements.FirstOrDefault(x => x.Faction?.def.defName.StartsWith("HE_Faction_") == true);
            P.Check("a heir settlement on the world map uses its nation's icon", s == null || s.Faction.def.SettlementTexture.name.Contains("HE_Settlement_"),
                s == null ? "no heir settlement" : s.Faction.def.defName + " " + s.Faction.def.SettlementTexture.name);
        }

        public static void Atlas()
        {
            List<ResearchProjectDef> all = HeirsAtlas.AllProjects;
            int withExt = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Count(p => p.HasModExtension<HeirsResearchExt>());
            P.Check("research browser lists every heir project", all.Count >= withExt && withExt >= 175, all.Count + "/" + withExt);
            P.Check("research browser has no duplicates", all.Distinct().Count() == all.Count);

            NationDef roma = HeirsDefOf.HE_Roma;
            Reset();
            HeirsAtlas.filterNation = roma;
            List<ResearchProjectDef> romaList = HeirsAtlas.Filtered();
            P.Check("nation filter keeps only that nation", romaList.Count >= 15 && romaList.All(p => HeirsAtlas.NationOf(p) == roma), romaList.Count.ToString());

            Reset();
            HeirsAtlas.filterCommon = true;
            List<ResearchProjectDef> common = HeirsAtlas.Filtered();
            P.Check("shared filter keeps only projects without a nation", common.Count >= 3 && common.All(p => HeirsAtlas.NationOf(p) == null), common.Count.ToString());

            Reset();
            HeirsAtlas.filterAge = TechLevel.Industrial;
            List<ResearchProjectDef> industrial = HeirsAtlas.Filtered();
            P.Check("age filter keeps only that age", industrial.Count > 0 && industrial.All(p => p.techLevel == TechLevel.Industrial), industrial.Count.ToString());

            int sum = 0;
            foreach (HeirsAtlas.ResearchState s in new[] { HeirsAtlas.ResearchState.Available, HeirsAtlas.ResearchState.Locked, HeirsAtlas.ResearchState.Finished })
            {
                Reset();
                HeirsAtlas.filterState = s;
                List<ResearchProjectDef> list = HeirsAtlas.Filtered();
                sum += list.Count;
                bool consistent = s == HeirsAtlas.ResearchState.Finished ? list.All(p => p.IsFinished)
                    : s == HeirsAtlas.ResearchState.Available ? list.All(p => p.CanStartNow && !p.IsFinished)
                    : list.All(p => !p.CanStartNow && !p.IsFinished);
                P.Check("state filter " + s, consistent, list.Count.ToString());
            }
            P.Check("state filters cover every project once", sum == all.Count, sum + "/" + all.Count);

            Reset();
            HeirsAtlas.filterState = HeirsAtlas.ResearchState.Locked;
            List<ResearchProjectDef> locked = HeirsAtlas.Filtered();
            int noReason = locked.Count(p => HeirsAtlas.LockReason(p).NullOrEmpty());
            P.Check("every locked project says why", locked.Count > 0 && noReason == 0, locked.Count + " locked, " + noReason + " without reason");
            ResearchProjectDef gated = locked.FirstOrDefault(p => HeirsAtlas.NationOf(p) != null && HeirsAtlas.NationOf(p) != HeirsGame.Get.heritage
                && p.PrerequisitesCompleted && p.GetModExtension<HeirsResearchExt>().knowledge > HeirsGame.Get.Knowledge(HeirsAtlas.NationOf(p)));
            P.Check("knowledge-locked project names the knowledge it needs", gated == null || HeirsAtlas.LockReason(gated).Length > 5, gated == null ? "none" : HeirsAtlas.LockReason(gated));

            Reset();
            HeirsAtlas.filterState = HeirsAtlas.ResearchState.Available;
            ResearchProjectDef pick = HeirsAtlas.Filtered().FirstOrDefault();
            ResearchProjectDef before = Find.ResearchManager.GetProject();
            if (pick != null)
            {
                Find.ResearchManager.SetCurrentProject(pick);
                P.Check("browser can set the current project", Find.ResearchManager.IsCurrentProject(pick), pick.defName);
                // SetCurrentProject(null) throws in 1.6; with nothing chosen before, stop the picked project instead.
                if (before != null) Find.ResearchManager.SetCurrentProject(before);
                else Find.ResearchManager.StopProject(pick);
                P.Check("browser restores the previous project", before == null ? !Find.ResearchManager.IsCurrentProject(pick) : Find.ResearchManager.IsCurrentProject(before));
            }
            Reset();
        }

        /// <summary>Opens the research browser with several filter sets so the drawing code runs on each.</summary>
        public static void AtlasFilterVariant(int variant)
        {
            Reset();
            switch (variant)
            {
                case 0: HeirsAtlas.filterNation = HeirsDefOf.HE_Roma; HeirsAtlas.filterState = HeirsAtlas.ResearchState.Locked; break;
                case 1: HeirsAtlas.filterCommon = true; break;
                case 2: HeirsAtlas.filterAge = TechLevel.Spacer; break; // usually empty: draws the empty-list text
                default: HeirsAtlas.filterState = HeirsAtlas.ResearchState.Finished; break;
            }
        }

        public static void Reset()
        {
            HeirsAtlas.filterNation = null;
            HeirsAtlas.filterCommon = false;
            HeirsAtlas.filterAge = TechLevel.Undefined;
            HeirsAtlas.filterState = HeirsAtlas.ResearchState.All;
        }

        public static void Encyclopedia()
        {
            var thin = new List<string>();
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                var g = HeirsAtlas.EntriesOf(nation);
                int b = g[HeirsAtlas.EntryKind.Building].Count, w = g[HeirsAtlas.EntryKind.Weapon].Count, a = g[HeirsAtlas.EntryKind.Apparel].Count,
                    f = g[HeirsAtlas.EntryKind.Food].Count, fl = g[HeirsAtlas.EntryKind.Floor].Count;
                if (b < 3 || w < 3 || a < 2 || f < 1 || fl < 1) thin.Add(nation.defName + " b" + b + " w" + w + " a" + a + " f" + f + " fl" + fl);
                bool foreign = g.Values.SelectMany(x => x).Any(d => d is ThingDef td && td.GetModExtension<HeirsCultureExt>()?.nation != nation);
                if (foreign) thin.Add(nation.defName + " foreign entry");
            }
            P.Check("encyclopedia lists each nation's buildings, weapons, clothes, food and floors", thin.Count == 0, string.Join("; ", thin));
        }

        /// <summary>3.1: every heir start (nine nations and the independent one) begins with five colonists chosen from ten.</summary>
        public static void Starts()
        {
            var bad = new List<string>();
            int seen = 0;
            foreach (ScenarioDef def in DefDatabase<ScenarioDef>.AllDefsListForReading.Where(d => d.defName.StartsWith("HE_")))
            {
                seen++;
                var part = def.scenario.AllParts.OfType<ScenPart_ConfigPage_ConfigureStartingPawns>().FirstOrDefault();
                if (part == null || part.pawnCount != 5 || part.pawnChoiceCount != 10) bad.Add(def.defName + ":" + (part == null ? "none" : part.pawnCount + "/" + part.pawnChoiceCount));
            }
            P.Check("heir starts have five colonists out of ten", seen == 10 && bad.Count == 0, seen + " " + string.Join(" ", bad));
        }

        public static void Settings()
        {
            HeirsSettings s = HeirsMod.Settings;
            float k = s.knowledgeGain, r = s.researchCost, raid = s.raidStrength, t = s.tributeDemand;
            int days = s.politicsIntervalDays;
            s.ApplyPreset(2);
            P.Check("hard preset", s.raidStrength > 1f && s.tributeDemand > 1f && s.knowledgeGain < 1f && s.politicsIntervalDays < 30);
            s.ApplyPreset(0);
            P.Check("relaxed preset", s.raidStrength < 1f && s.tributeDemand < 1f && s.knowledgeGain > 1f && s.politicsIntervalDays > 30);
            s.ApplyPreset(1);
            P.Check("standard preset is the default", s.raidStrength == 1f && s.tributeDemand == 1f && s.knowledgeGain == 1f && s.researchCost == 1f && s.politicsIntervalDays == 30);
            int normal = HeirsPolitics.TributeAmount(50000f);
            s.tributeDemand = 2f;
            int doubled = HeirsPolitics.TributeAmount(50000f);
            s.tributeDemand = 0.25f;
            int quarter = HeirsPolitics.TributeAmount(50000f);
            P.Check("tribute setting scales the silver demanded", normal == 500 && doubled == 1000 && quarter >= 50 && quarter < normal && quarter % 50 == 0, normal + "/" + doubled + "/" + quarter);
            s.knowledgeGain = k;
            s.researchCost = r;
            s.raidStrength = raid;
            s.tributeDemand = t;
            s.politicsIntervalDays = days;
        }
    }
}
