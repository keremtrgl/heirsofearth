using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    public static partial class Probe43
    {
        private static int fairHostGoodwill;
        private static float fairHostKnowledge;
        private static NationDef fairHost;

        private static void ClearLetters()
        {
            while (Find.LetterStack.LettersListForReading.Count > 0) Find.LetterStack.RemoveLetter(Find.LetterStack.LettersListForReading[0]);
        }

        /// <summary>The World Fair: rewards, gates, once per game, the exhibit choice, declining, and sending (it comes back after the
        /// save and load, in FairAfterLoad).</summary>
        public static void Fair()
        {
            HeirsGame g = HeirsGame.Get;
            Map map = P.Home;
            bool held = g.worldFairHeld, ages = HeirsMod.Settings.ages, events = HeirsMod.Settings.worldEvents;

            HeirsEvents.FairPrize legendary = HeirsEvents.FairReward(QualityCategory.Legendary);
            HeirsEvents.FairPrize normal = HeirsEvents.FairReward(QualityCategory.Normal);
            HeirsEvents.FairPrize master = HeirsEvents.FairReward(QualityCategory.Masterwork);
            HeirsEvents.FairPrize excellent = HeirsEvents.FairReward(QualityCategory.Excellent);
            P.Check("fair reward table", legendary.goodwillHost == 22 && legendary.goodwillOthers == 8 && legendary.silver == 1200 && legendary.grandPrize
                && normal.goodwillHost == 5 && normal.silver == 150 && !normal.grandPrize && master.grandPrize && !excellent.grandPrize
                && Mathf.Approximately(master.knowledge, 30f) && HeirsEvents.FairReward(QualityCategory.Poor).silver == 150);

            NationDef host = HeirsWorld.LiveNations.FirstOrDefault(n => !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer));
            if (host == null)
            {
                P.Check("a peaceful nation for the fair", false);
                return;
            }
            ThingDef sculptureDef = DefDatabase<ThingDef>.GetNamed("SculptureSmall");
            Thing sculpture = ThingMaker.MakeThing(sculptureDef, ThingDefOf.WoodLog);
            sculpture.SetFaction(Faction.OfPlayer);
            sculpture.TryGetComp<CompQuality>().SetQuality(QualityCategory.Legendary, ArtGenerationContext.Colony);
            GenSpawn.Spawn(sculpture, P.FreeSpot(map, new IntVec2(1, 1)), map);
            try
            {
                P.Check("fair picks the legendary sculpture", HeirsEvents.FairExhibit(map) == sculpture, HeirsEvents.FairExhibit(map)?.LabelCap ?? "none");

                g.worldFairHeld = false;
                HeirsMod.Settings.ages = false;
                P.Check("ages off: no fair", !HeirsEvents.TryWorldFair(host));
                HeirsMod.Settings.ages = true;
                HeirsMod.Settings.worldEvents = false;
                P.Check("world events off: no fair", !HeirsEvents.TryWorldFair(host));
                HeirsMod.Settings.worldEvents = true;
                NationDef hostile = HeirsWorld.LiveNations.FirstOrDefault(n => HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer));
                if (hostile != null)
                {
                    P.Check("a hostile nation does not host and the honour stays open", !HeirsEvents.TryWorldFair(hostile) && !g.worldFairHeld);
                }
                else
                {
                    P.Say("no hostile nation to test the fair with");
                }
                NationDef fallen = DefDatabase<NationDef>.AllDefsListForReading.FirstOrDefault(n => HeirsWorld.FactionOf(n) == null);
                if (fallen != null)
                {
                    P.Check("a fallen nation does not host", !HeirsEvents.TryWorldFair(fallen) && !g.worldFairHeld);
                }

                int letters = Find.LetterStack.LettersListForReading.Count;
                P.Check("the fair fires", HeirsEvents.TryWorldFair(host) && g.worldFairHeld && Find.LetterStack.LettersListForReading.Count == letters + 1);
                P.Check("the fair fires once per game", !HeirsEvents.TryWorldFair(host));
                HeirsEvents.OnAgeReached(host, HeirsAges.LastAge);
                P.Check("a later Electric Age brings no second fair", Find.LetterStack.LettersListForReading.Count == letters + 1);

                Faction hf = HeirsWorld.FactionOf(host);
                int before = hf.PlayerGoodwill;
                HeirsEvents.Resolve("WorldFair", host, 0, null, 1, sculpture);
                // the game scales goodwill losses, so a 3 point penalty can show as 3 to 5
                P.Check("declining costs 3 goodwill", before - hf.PlayerGoodwill >= 3 && before - hf.PlayerGoodwill <= 5 && sculpture.Spawned, before + " -> " + hf.PlayerGoodwill);
                hf.TryAffectGoodwillWith(Faction.OfPlayer, before - hf.PlayerGoodwill, false, false, null);

                fairHostGoodwill = hf.PlayerGoodwill;
                fairHostKnowledge = g.Knowledge(host);
                fairHost = host;
                HeirsEvents.Resolve("WorldFair", host, 0, null, 0, sculpture);
                P.Check("accepting sends the exhibit away", !sculpture.Spawned && g.fairExhibit.Count == 1 && HeirsEvents.Inner(g.fairExhibit[0]) == sculpture
                    && g.fairHost == host && g.fairReturnTick > Find.TickManager.TicksGame + 9 * GenDate.TicksPerDay,
                    g.fairExhibit.Count + " held, back at " + g.fairReturnTick);
                HeirsEvents.FairTick(g);
                P.Check("the exhibit stays away until the fair is over", g.fairExhibit.Count == 1);
            }
            finally
            {
                HeirsMod.Settings.ages = ages;
                HeirsMod.Settings.worldEvents = events;
                if (sculpture.Spawned) sculpture.Destroy();
                ClearLetters();
                if (!g.fairExhibit.Any) g.worldFairHeld = held;
            }
        }

        /// <summary>After the save and load: the exhibit is still held, comes back by drop pod when the fair is over, and pays the prize.</summary>
        public static void FairAfterLoad()
        {
            HeirsGame g = HeirsGame.Get;
            Map map = P.Home;
            P.Check("fair exhibit survives the save", g.fairExhibit != null && g.fairExhibit.Count == 1 && g.fairHost == fairHost && g.worldFairHeld,
                (g.fairExhibit?.Count ?? -1) + " held, host " + g.fairHost?.defName);
            if (g.fairExhibit == null || g.fairExhibit.Count == 0) return;
            Thing exhibit = g.fairExhibit[0];
            int silver = map.resourceCounter.Silver;
            g.fairReturnTick = Find.TickManager.TicksGame;
            HeirsEvents.FairTick(g);
            P.Check("the exhibit leaves the fair", g.fairExhibit.Count == 0 && g.fairHost == null);
            P.Ticks(900);
            Thing inner = HeirsEvents.Inner(exhibit);
            P.Check("the exhibit is back home", exhibit.Spawned && exhibit.Map == map && inner.TryGetQuality(out QualityCategory q) && q == QualityCategory.Legendary,
                exhibit.Spawned + " " + exhibit.MapHeld);
            Faction hf = HeirsWorld.FactionOf(fairHost);
            if (hf != null)
            {
                int want = Mathf.Min(100, fairHostGoodwill + 22 + HeirsEvents.GrandPrizeGoodwill);
                P.Check("the host's goodwill rises by the legendary prize", hf.PlayerGoodwill >= want - 1, fairHostGoodwill + " -> " + hf.PlayerGoodwill);
                P.Check("knowledge of the host rises by 40", g.Knowledge(fairHost) >= fairHostKnowledge + 39.9f, fairHostKnowledge + " -> " + g.Knowledge(fairHost));
            }
            map.resourceCounter.UpdateResourceCounts();
            P.Check("the prize silver arrives", map.resourceCounter.Silver >= silver + 1200 || map.listerThings.ThingsOfDef(ThingDefOf.Silver).Sum(t => t.stackCount) >= 1200,
                silver + " -> " + map.resourceCounter.Silver);
            P.Check("the grand prize is in the chronicle", g.chronicle.Any(c => c.text.Contains(inner.LabelCap)));
            if (exhibit.Spawned) exhibit.Destroy();
            ClearLetters();
        }
    }
}
