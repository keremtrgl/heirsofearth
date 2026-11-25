using System;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using Verse;

namespace HeProbe
{
    /// <summary>3.7 checks: switching a nation off and on, and a world in which a nation has fallen.</summary>
    public static class Probe37
    {
        public static void Toggle()
        {
            HeirsGame game = P.Game;
            HeirsSettings s = HeirsMod.Settings;
            NationDef nation = HeirsWorld.LiveNations.FirstOrDefault(n => n != game.heritage);
            if (nation == null) { P.Say("no live nation to switch off"); return; }
            ChainDef chain = DefDatabase<ChainDef>.AllDefsListForReading.FirstOrDefault(c => c.nation == nation && c.after == null);
            NationDef heritage = game.heritage;
            var honours = game.honours.ToList();
            P.Check("text for the nation switch", "HE_SettingsNationActive".CanTranslate() && "HE_SettingsNationActiveTip".CanTranslate());

            s.disabledNations.Add(nation.defName);
            try
            {
                game.heritage = nation;
                if (!game.honours.Contains(nation)) game.honours.Add(nation);
                P.Check("switched off: out of the world's politics", !HeirsWorld.LiveNations.Contains(nation) && HeirsWorld.FactionOf(nation) != null);
                P.Check("switched off: starts no story", chain == null || !HeirsChains.CanStart(game, chain), chain?.defName);
                P.Check("switched off: no music", !HeirsMusic.Play(nation) && !HeirsMusic.Patrons(game).Contains(nation));
                int letters = Find.LetterStack.LettersListForReading.Count;
                for (int i = 0; i < 12; i++)
                {
                    HeirsErrands.MonthlyTick();
                    HeirsEvents.MonthlyTick();
                    HeirsWorld.Get?.MonthlyTick();
                }
                P.Check("switched off: no errands from it", game.errands.All(e => e.nation != nation));
                P.Check("switched off: no letters about it",
                        Find.LetterStack.LettersListForReading.Skip(letters).All(l => l is ChoiceLetter_HeirsErrand ce ? ce.errand?.nation != nation : true),
                        (Find.LetterStack.LettersListForReading.Count - letters) + " new letters");
                P.Check("the setting is saved", s.disabledNations.Contains(nation.defName));
            }
            catch (Exception e)
            {
                P.Check("switched-off nation runs without errors", false, e.ToString());
            }
            finally
            {
                s.disabledNations.Remove(nation.defName);
                game.heritage = heritage;
                game.honours.Clear();
                game.honours.AddRange(honours);
            }
            P.Check("switched back on: takes part again", HeirsWorld.LiveNations.Contains(nation) && (chain == null || game.heritage != nation || HeirsChains.CanStart(game, chain)));
        }

        public static void FallenNation()
        {
            NationDef nation = HeirsWorld.LiveNations.LastOrDefault(n => n != P.Game.heritage);
            if (nation == null) { P.Say("no nation to fall"); return; }
            Faction faction = HeirsWorld.FactionOf(nation);
            faction.defeated = true;
            try
            {
                P.Check("a fallen nation leaves the world's politics", !HeirsWorld.LiveNations.Contains(nation));
                HeirsGame game = P.Game;
                for (int i = 0; i < 6; i++)
                {
                    HeirsWorld.Get?.MonthlyTick();
                    HeirsErrands.MonthlyTick();
                    HeirsEvents.MonthlyTick();
                    HeirsCourt.MonthlyTick(HeirsWorld.Get);
                    HeirsTreaties.MonthlyTick(game);
                    HeirsCouncil.TickRare(game);
                    HeirsChains.TickRare(game);
                }
                P.Check("the world runs on without it", true);
            }
            catch (Exception e)
            {
                P.Check("the world runs on without it", false, e.ToString());
            }
            finally
            {
                faction.defeated = false;
            }
        }
    }
}
