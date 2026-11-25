using System.Collections.Generic;
using RimWorld;
using UnityEngine;
using Verse;
using Verse.Grammar;

namespace HeirsOfEarth
{
    /// <summary>
    /// 3.5: the classic books of the heir nations. Reading one teaches the reader's colony that nation's culture knowledge, by the hour,
    /// up to what the book can teach (its cap). Better copies teach faster. The title and blurb are the book's own, not generated.
    /// </summary>
    public class BookOutcomeProperties_HeirsKnowledge : BookOutcomeProperties
    {
        public NationDef nation;
        public float perHour = 0.5f;
        public float cap = 100f;
        public string titleKey;
        public string descKey;

        public override System.Type DoerClass => typeof(BookOutcomeDoer_HeirsKnowledge);
    }

    public class BookOutcomeDoer_HeirsKnowledge : BookOutcomeDoer
    {
        public new BookOutcomeProperties_HeirsKnowledge Props => (BookOutcomeProperties_HeirsKnowledge)props;

        /// <summary>Awful 0.6 ... legendary 1.8: a fine copy is easier to learn from.</summary>
        public float QualityFactor => 0.6f + 0.2f * (int)Quality;

        public float PerHour => Props.perHour * QualityFactor;

        public static float PerTick(float perHour) => perHour / GenDate.TicksPerHour;

        public bool Exhausted => HeirsGame.Get != null && HeirsGame.Get.Knowledge(Props.nation) >= Props.cap;

        public override bool DoesProvidesOutcome(Pawn reader) => Props.nation != null && HeirsGame.Get != null && !Exhausted;

        public override void OnReadingTick(Pawn reader, float factor)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || Props.nation == null || reader?.Faction == null || !reader.Faction.IsPlayer)
            {
                return;
            }
            float have = game.Knowledge(Props.nation);
            if (have >= Props.cap)
            {
                return;
            }
            game.AddKnowledge(Props.nation, Mathf.Min(PerTick(PerHour) * factor, Props.cap - have), null);
        }

        public override string GetBenefitsString(Pawn reader = null)
        {
            if (Props.nation == null)
            {
                return null;
            }
            string line = " - " + "HE_BookBenefit".Translate(Props.nation.adjective, PerHour.ToString("0.##"), Props.cap.ToString("0")).Resolve();
            return Exhausted ? (line + " (" + "HE_BookLearned".Translate().Resolve() + ")").Colorize(Color.gray) : line;
        }

        public override bool BenefitDetailsCanChange(Pawn reader = null) => true;

        public override IEnumerable<Rule_String> GetTopicRuleStrings()
        {
            yield return new Rule_String("heirs_title", Props.titleKey.NullOrEmpty() ? Parent.def.label : Props.titleKey.Translate().Resolve());
            yield return new Rule_String("heirs_desc", Props.descKey.NullOrEmpty() ? Parent.def.description : Props.descKey.Translate().Resolve());
        }
    }
}
