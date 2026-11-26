using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>
    /// 4.3 World Fair: once per game the first nation to reach the Electric Age (or, if it is hostile then, the next one that is not)
    /// holds a fair. The colony may send its best art piece, weapon or book; it comes back by drop pod about ten days later with the
    /// prize, which grows with the exhibit's quality. Follows the "world events" setting and needs the ages to be on.
    /// </summary>
    public static partial class HeirsEvents
    {
        public const int FairDays = 10;
        public const int FairDeclineCost = 3;
        public const int GrandPrizeGoodwill = 5;

        public struct FairPrize
        {
            public int goodwillHost, goodwillOthers;
            public float knowledge;
            public int silver;
            public bool grandPrize;
        }

        public static FairPrize FairReward(QualityCategory q)
        {
            switch (q)
            {
                case QualityCategory.Legendary: return new FairPrize { goodwillHost = 22, goodwillOthers = 8, knowledge = 40, silver = 1200, grandPrize = true };
                case QualityCategory.Masterwork: return new FairPrize { goodwillHost = 16, goodwillOthers = 6, knowledge = 30, silver = 800, grandPrize = true };
                case QualityCategory.Excellent: return new FairPrize { goodwillHost = 12, goodwillOthers = 4, knowledge = 20, silver = 500 };
                case QualityCategory.Good: return new FairPrize { goodwillHost = 8, goodwillOthers = 3, knowledge = 15, silver = 300 };
                default: return new FairPrize { goodwillHost = 5, goodwillOthers = 2, knowledge = 10, silver = 150 };
            }
        }

        /// <summary>The thing inside a packed-up building, or the thing itself.</summary>
        public static Thing Inner(Thing t) => (t as MinifiedThing)?.InnerThing ?? t;

        public static QualityCategory QualityOf(Thing t) => Inner(t) != null && Inner(t).TryGetQuality(out QualityCategory q) ? q : QualityCategory.Normal;

        private static bool Exhibitable(Thing t)
        {
            Thing inner = Inner(t);
            if (inner == null || !t.Spawned || t.IsForbidden(Faction.OfPlayer) || !inner.TryGetQuality(out _))
            {
                return false;
            }
            if (t is Building && (t.Faction != Faction.OfPlayer || !t.def.Minifiable))
            {
                return false;
            }
            return inner.def.IsWeapon || inner is Book || inner.TryGetComp<CompArt>() != null;
        }

        /// <summary>The colony's best art piece, weapon or book on the map, by quality and then market value; null if there is none.</summary>
        public static Thing FairExhibit(Map map)
        {
            if (map == null)
            {
                return null;
            }
            return map.listerThings.AllThings.Where(Exhibitable)
                .OrderByDescending(QualityOf).ThenByDescending(t => t.MarketValue * t.stackCount).FirstOrDefault();
        }

        private static Thing AnyExhibit() => Find.Maps.Where(m => m.IsPlayerHome).Select(FairExhibit).Where(t => t != null)
            .OrderByDescending(QualityOf).ThenByDescending(t => t.MarketValue).FirstOrDefault();

        /// <summary>Hooked to HeirsAges.OnAgeReached.</summary>
        public static void OnAgeReached(NationDef nation, int age)
        {
            if (age == HeirsAges.LastAge)
            {
                TryWorldFair(nation);
            }
        }

        /// <summary>Sends the World Fair letter if the fair has not been held, the host is alive and not hostile, and the setting allows.</summary>
        public static bool TryWorldFair(NationDef host)
        {
            HeirsGame g = HeirsGame.Get;
            if (g == null || g.worldFairHeld || host == null || !HeirsMod.Settings.worldEvents || !HeirsMod.Settings.ages || Find.AnyPlayerHomeMap == null)
            {
                return false;
            }
            Faction f = HeirsWorld.FactionOf(host);
            if (f == null || f.HostileTo(Faction.OfPlayer))
            {
                return false;
            }
            g.worldFairHeld = true;
            Thing exhibit = AnyExhibit();
            ChoiceLetter_HeirsEvent letter = Make("WorldFair", host, 0, null);
            letter.exhibit = exhibit;
            letter.Label = "HE_WorldFairLabel".Translate(host.LabelCap);
            string shown = exhibit == null ? "HE_WorldFairNothing".Translate().Resolve()
                : "HE_WorldFairExhibit".Translate(Inner(exhibit).LabelCap, QualityOf(exhibit).GetLabel()).Resolve();
            letter.Text = "HE_WorldFairText".Translate(host.LabelCap, HeirsCourt.RulerLine(host), shown, FairDays);
            HeirsMusic.Sting(host);
            Find.LetterStack.ReceiveLetter(letter);
            return true;
        }

        /// <summary>The exhibit to send for a letter: the one it named if it is still at home, else the best one now.</summary>
        public static Thing ExhibitFor(Thing named) => named != null && !named.Destroyed && named.Spawned && named.Map.IsPlayerHome && Exhibitable(named) ? named : AnyExhibit();

        /// <summary>Takes the exhibit off the map and keeps it in the game until it comes back.</summary>
        public static bool SendExhibit(Thing exhibit, NationDef host)
        {
            HeirsGame g = HeirsGame.Get;
            if (g == null || exhibit == null || !exhibit.Spawned || g.fairExhibit.Any)
            {
                return false;
            }
            Thing travel = exhibit;
            if (exhibit is Building)
            {
                exhibit.DeSpawn(DestroyMode.Vanish);
                travel = exhibit.MakeMinified();
            }
            else
            {
                exhibit.DeSpawn(DestroyMode.Vanish);
            }
            if (!g.fairExhibit.TryAdd(travel, false))
            {
                return false;
            }
            g.fairHost = host;
            g.fairReturnTick = Find.TickManager.TicksGame + FairDays * GenDate.TicksPerDay;
            Messages.Message("HE_WorldFairSent".Translate(Inner(travel).LabelCap, host.LabelCap), MessageTypeDefOf.PositiveEvent, false);
            return true;
        }

        /// <summary>Called every 2500 ticks: brings the exhibit home once the fair is over.</summary>
        public static void FairTick(HeirsGame g)
        {
            if (g?.fairExhibit != null && g.fairExhibit.Any && Find.TickManager.TicksGame >= g.fairReturnTick)
            {
                ReturnExhibit(g);
            }
        }

        /// <summary>Drops the exhibit and the silver on a home map and pays the goodwill and knowledge. Returns the prize given.</summary>
        public static FairPrize? ReturnExhibit(HeirsGame g)
        {
            Map map = Find.AnyPlayerHomeMap;
            if (map == null || !g.fairExhibit.Any)
            {
                return null;
            }
            Thing exhibit = g.fairExhibit[0];
            QualityCategory q = QualityOf(exhibit);
            FairPrize prize = FairReward(q);
            NationDef host = g.fairHost;
            List<Thing> drop = new List<Thing>();
            g.fairExhibit.Remove(exhibit);
            drop.Add(exhibit);
            int silver = prize.silver;
            while (silver > 0)
            {
                Thing s = ThingMaker.MakeThing(ThingDefOf.Silver);
                s.stackCount = Mathf.Min(silver, ThingDefOf.Silver.stackLimit);
                silver -= s.stackCount;
                drop.Add(s);
            }
            IntVec3 at = DropCellFinder.TradeDropSpot(map);
            DropPodUtility.DropThingsNear(at, map, drop, 110, false, false, true);

            bool hostAlive = host != null && HeirsWorld.FactionOf(host) != null;
            foreach (NationDef n in Peaceful.ToList())
            {
                int amount = (n == host ? prize.goodwillHost : prize.goodwillOthers) + (prize.grandPrize ? GrandPrizeGoodwill : 0);
                HeirsPolitics.Affect(n, amount);
            }
            if (hostAlive)
            {
                g.AddKnowledge(host, prize.knowledge, null);
            }
            string hostLabel = host?.LabelCap.Resolve() ?? "?";
            string text = "HE_WorldFairBack".Translate(Inner(exhibit).LabelCap, hostLabel, q.GetLabel(), prize.goodwillHost, prize.goodwillOthers,
                prize.knowledge.ToString("0"), prize.silver).Resolve();
            if (prize.grandPrize)
            {
                string won = "HE_WorldFairGrandPrize".Translate(Inner(exhibit).LabelCap, hostLabel, GrandPrizeGoodwill).Resolve();
                g.AddChronicle(won, host);
                text += "\n\n" + won;
            }
            g.fairHost = null;
            g.fairReturnTick = 0;
            Find.LetterStack.ReceiveLetter("HE_WorldFairBackLabel".Translate(hostLabel), text, LetterDefOf.PositiveEvent, new LookTargets(at, map));
            return prize;
        }
    }
}
