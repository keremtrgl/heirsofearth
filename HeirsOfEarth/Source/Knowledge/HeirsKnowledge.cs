using System.Collections.Generic;
using HarmonyLib;
using RimWorld;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>Culture Knowledge rules: the research gate, knowledge from finished projects, teachers and study.</summary>
    public static class HeirsKnowledge
    {
        public const float FinishBonus = 5f;
        public const float TeacherRate = 0.002f;

        public static bool Allowed(ResearchProjectDef project)
        {
            HeirsGame game = HeirsGame.Get;
            return game == null || game.CanStart(project, out _);
        }

        public static void OnProjectFinished(ResearchProjectDef project)
        {
            HeirsResearchExt ext = project?.GetModExtension<HeirsResearchExt>();
            if (ext == null)
            {
                return;
            }
            HeirsGame.Get?.AddKnowledge(ext.nation, FinishBonus, null);
            if (ext.tradition)
            {
                HeirsTraditions.Dirty();
                HeirsGame.Get?.AddChronicle("HE_ChronicleTradition".Translate(project.LabelCap), ext.nation);
            }
        }

        public static NationDef CultureOf(Pawn pawn)
        {
            if (pawn?.story == null)
            {
                return null;
            }
            return pawn.story.Adulthood?.GetModExtension<HeirsCultureExt>()?.nation ?? pawn.story.Childhood?.GetModExtension<HeirsCultureExt>()?.nation;
        }

        public static void OnResearchPerformed(float amount, Pawn researcher)
        {
            NationDef culture = CultureOf(researcher);
            if (culture == null || amount <= 0f)
            {
                return;
            }
            HeirsGame.Get?.AddKnowledge(culture, amount * TeacherRate * HeirsMod.Settings.knowledgeGain, null);
        }

        public static float StudyValue(Thing thing)
        {
            HeirsCultureExt ext = thing.def.GetModExtension<HeirsCultureExt>();
            if (ext == null || ext.nation == null)
            {
                return 0f;
            }
            float each = ext.knowledge > 0f ? ext.knowledge : thing.MarketValue / 20f;
            return each * thing.stackCount * HeirsMod.Settings.knowledgeGain * (1f + HeirsTraditions.StudyBonus(ext.nation));
        }

        public static void ApplyResearchCost()
        {
            float factor = HeirsMod.Settings.researchCost;
            if (factor == 1f)
            {
                return;
            }
            foreach (ResearchProjectDef project in DefDatabase<ResearchProjectDef>.AllDefsListForReading)
            {
                if (project.HasModExtension<HeirsResearchExt>())
                {
                    project.baseCost *= factor;
                }
            }
        }
    }

    public class RecipeWorker_HeirsStudy : RecipeWorker
    {
        public override void Notify_IterationCompleted(Pawn billDoer, List<Thing> ingredients)
        {
            base.Notify_IterationCompleted(billDoer, ingredients);
            HeirsGame game = HeirsGame.Get;
            if (game == null || ingredients == null)
            {
                return;
            }
            foreach (Thing thing in ingredients)
            {
                NationDef nation = thing.def.GetModExtension<HeirsCultureExt>()?.nation;
                float value = HeirsKnowledge.StudyValue(thing);
                if (nation != null && value > 0f)
                {
                    game.AddKnowledge(nation, value, "HE_ChronicleStudy");
                    Messages.Message("HE_StudyMessage".Translate(billDoer.LabelShort, value.ToString("0.#"), nation.adjective), billDoer, MessageTypeDefOf.PositiveEvent, false);
                }
            }
        }
    }

    public class Patch_ResearchGate : HeirsPatch
    {
        public override string Id => "ResearchGate";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.NeedGetter(typeof(ResearchProjectDef), "CanStartNow"), postfix: HeirsPatches.Hook("CanStartNow_Postfix"));
        }
    }

    public class Patch_ResearchKnowledge : HeirsPatch
    {
        public override string Id => "ResearchKnowledge";

        public override void Apply(Harmony harmony)
        {
            harmony.Patch(HeirsPatches.Need(typeof(ResearchManager), "FinishProject"), postfix: HeirsPatches.Hook("FinishProject_Postfix"));
            harmony.Patch(HeirsPatches.Need(typeof(ResearchManager), "ResearchPerformed"), postfix: HeirsPatches.Hook("ResearchPerformed_Postfix"));
        }
    }
}
