using Verse;
using RimWorld;

namespace HeirsOfEarth
{
    public static class HeirsStart
    {
        public const float IndependentKnowledge = 15f;

        /// <summary>Independent colonies start neutral with everyone but with a little knowledge of every culture.</summary>
        public static void IndependentBonus()
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null) return;
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                game.AddKnowledge(nation, IndependentKnowledge, null);
            }
        }
    }

    /// <summary>Scenario part: sets the colony's heritage when the game starts.</summary>
    public class ScenPart_HeirsHeritage : ScenPart
    {
        public NationDef nation;

        public override void PostGameStart()
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || game.heritageChosen) return;
            game.SetHeritage(nation);
            if (nation == null)
            {
                HeirsStart.IndependentBonus();
            }
        }

        public override string Summary(Scenario scen)
        {
            return nation == null ? "HE_ScenIndependent".Translate().Resolve() : "HE_ScenHeritage".Translate(nation.LabelCap).Resolve();
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Defs.Look(ref nation, "nation");
        }
    }
}
