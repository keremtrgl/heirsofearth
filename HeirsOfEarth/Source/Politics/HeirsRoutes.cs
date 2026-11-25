using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>One open trade route between the player and a heir nation.</summary>
    public class TradeRoute : IExposable
    {
        public NationDef nation;
        public int cost;
        public int openedTick;
        public int nextTick;
        public int trips;
        public int raids;

        public void ExposeData()
        {
            Scribe_Defs.Look(ref nation, "nation");
            Scribe_Values.Look(ref cost, "cost");
            Scribe_Values.Look(ref openedTick, "openedTick");
            Scribe_Values.Look(ref nextTick, "nextTick");
            Scribe_Values.Look(ref trips, "trips");
            Scribe_Values.Look(ref raids, "raids");
        }
    }

    /// <summary>
    /// Trade routes: the player pays silver once to open a road to a friendly nation; every 15 days a route caravan
    /// brings that nation's goods and silver. Wars put caravans at risk, hostility closes the road.
    /// </summary>
    public static class HeirsRoutes
    {
        public const int MinGoodwill = 25;
        public const int BaseRoutes = 3;
        public const int IntervalDays = 15;
        public const float RaidChance = 0.25f;
        public const float BaseShare = 0.35f;
        public const float PostShare = 0.5f;
        public const int GoodwillPerTrip = 2;
        public const float KnowledgePerTrip = 3f;
        public const int MinCost = 400;
        public const int MaxCost = 900;

        private static ResearchProjectDef royalPost;

        private static ResearchProjectDef RoyalPost => royalPost ?? (royalPost = DefDatabase<ResearchProjectDef>.GetNamedSilentFail("HE_Pars_RoyalPost"));

        public static bool Enabled => HeirsMod.Settings.tradeRoutes;

        public static bool HasRoyalPost => RoyalPost != null && RoyalPost.IsFinished && HeirsTraditions.Active(RoyalPost);

        public static int MaxRoutes => BaseRoutes + (HasRoyalPost ? 1 : 0);

        public static float Share => HasRoyalPost ? PostShare : BaseShare;

        public static int CaravanValue(TradeRoute route) => Mathf.RoundToInt(route.cost * Share);

        /// <summary>Distance in world tiles from the player's home to the nation's nearest settlement, or -1.</summary>
        public static float Distance(NationDef nation)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            Map home = Find.AnyPlayerHomeMap;
            if (f == null || home == null)
            {
                return -1f;
            }
            float best = -1f;
            foreach (Settlement s in Find.WorldObjects.Settlements)
            {
                if (s.Faction != f) continue;
                float d = Find.WorldGrid.ApproxDistanceInTiles(home.Tile, s.Tile);
                if (best < 0f || d < best) best = d;
            }
            return best;
        }

        /// <summary>Silver to open a route: 400 near, rising 5 per tile, at most 900, rounded to 50.</summary>
        public static int Cost(NationDef nation)
        {
            float d = Distance(nation);
            if (d < 0f) d = 100f;
            return Mathf.Clamp(Mathf.RoundToInt((MinCost + d * 5f) / 50f) * 50, MinCost, MaxCost);
        }

        public static TradeRoute RouteTo(HeirsGame game, NationDef nation) => game.routes.FirstOrDefault(r => r.nation == nation);

        public static bool CanOpen(HeirsGame game, NationDef nation, out string reason)
        {
            reason = null;
            Faction f = HeirsWorld.FactionOf(nation);
            if (!Enabled) reason = "HE_RouteDisabled".Translate();
            else if (f == null) reason = "HE_RouteNoNation".Translate();
            else if (RouteTo(game, nation) != null) reason = "HE_RouteAlreadyOpen".Translate();
            else if (f.HostileTo(Faction.OfPlayer)) reason = "HE_RouteHostile".Translate();
            else if (HeirsPolitics.PlayerGoodwill(nation) < MinGoodwill) reason = "HE_RouteGoodwill".Translate(MinGoodwill);
            else if (Distance(nation) < 0f) reason = "HE_RouteNoSettlement".Translate();
            else if (game.routes.Count >= MaxRoutes) reason = "HE_RouteFull".Translate(MaxRoutes);
            else if (HeirsChains.CountAvailable(ThingDefOf.Silver) < Cost(nation)) reason = "HE_NotEnoughSilver".Translate(Cost(nation));
            return reason == null;
        }

        public static bool Open(HeirsGame game, NationDef nation, bool pay = true)
        {
            if (!CanOpen(game, nation, out _) && pay)
            {
                return false;
            }
            int cost = Cost(nation);
            if (pay)
            {
                HeirsChains.TakeFromColony(ThingDefOf.Silver, cost);
            }
            int now = Find.TickManager.TicksGame;
            game.routes.Add(new TradeRoute { nation = nation, cost = cost, openedTick = now, nextTick = now + IntervalDays * GenDate.TicksPerDay });
            game.AddChronicle("HE_RouteOpenedChronicle".Translate(nation.LabelCap, cost), nation);
            return true;
        }

        public static void Close(HeirsGame game, TradeRoute route, string reasonKey)
        {
            if (!game.routes.Remove(route))
            {
                return;
            }
            string text = reasonKey.Translate(route.nation.LabelCap);
            game.AddChronicle(text, route.nation);
            if (reasonKey != "HE_RouteClosedByPlayer")
            {
                Find.LetterStack.ReceiveLetter("HE_RouteClosedLabel".Translate(route.nation.LabelCap), text, LetterDefOf.NegativeEvent);
            }
        }

        /// <summary>Called every 2500 ticks from HeirsGame.</summary>
        public static void TickRare(HeirsGame game)
        {
            if (game.routes.Count == 0)
            {
                return;
            }
            int now = Find.TickManager.TicksGame;
            foreach (TradeRoute route in game.routes.ToList())
            {
                Faction f = HeirsWorld.FactionOf(route.nation);
                if (f == null)
                {
                    Close(game, route, "HE_RouteClosedCollapse");
                    continue;
                }
                if (f.HostileTo(Faction.OfPlayer))
                {
                    Close(game, route, "HE_RouteClosedHostile");
                    continue;
                }
                if (!Enabled || now < route.nextTick)
                {
                    continue;
                }
                route.nextTick = now + IntervalDays * GenDate.TicksPerDay;
                Trip(game, route, null);
            }
        }

        public static bool AtWar(NationDef nation)
        {
            HeirsWorld world = HeirsWorld.Get;
            return world != null && world.wars.Any(w => w.a == nation || w.b == nation);
        }

        /// <summary>One caravan run. forceRaid: null = roll the dice, true/false = test hook.</summary>
        public static bool Trip(HeirsGame game, TradeRoute route, bool? forceRaid)
        {
            Map map = Find.AnyPlayerHomeMap;
            if (map == null)
            {
                return false;
            }
            bool raided = forceRaid ?? (AtWar(route.nation) && Rand.Chance(RaidChance));
            if (raided)
            {
                route.raids++;
                string text = "HE_RouteRaidedText".Translate(route.nation.LabelCap);
                game.AddChronicle(text, route.nation);
                Find.LetterStack.ReceiveLetter("HE_RouteRaidedLabel".Translate(route.nation.LabelCap), text, LetterDefOf.NegativeEvent);
                return false;
            }
            route.trips++;
            List<Thing> things = Goods(route.nation, CaravanValue(route), out string summary);
            DropPodUtility.DropThingsNear(DropCellFinder.TradeDropSpot(map), map, things, 110, false, false, false, forbid: false);
            HeirsPolitics.Affect(route.nation, GoodwillPerTrip);
            game.AddKnowledge(route.nation, KnowledgePerTrip * HeirsMod.Settings.knowledgeGain, null);
            game.AddChronicle("HE_RouteTripChronicle".Translate(route.nation.LabelCap, route.trips), route.nation);
            Find.LetterStack.ReceiveLetter("HE_RouteTripLabel".Translate(route.nation.LabelCap),
                "HE_RouteTripText".Translate(route.nation.LabelCap, summary, GoodwillPerTrip, IntervalDays),
                LetterDefOf.PositiveEvent, new LookTargets(things.Where(t => t.Spawned)));
            return true;
        }

        /// <summary>Items a nation trades on its road: everything tradeable that carries its culture, except the story relics.</summary>
        public static List<ThingDef> GoodsOf(NationDef nation)
        {
            return DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.category == ThingCategory.Item && d.tradeability.TraderCanSell()
                    && d.BaseMarketValue > 0f && !d.IsCorpse && d.GetModExtension<HeirsCultureExt>()?.nation == nation
                    && d.GetCompProperties<CompProperties_HeirsArtifact>() == null).ToList();
        }

        /// <summary>About 60% of the value in the nation's goods (up to three kinds), the rest in silver.</summary>
        public static List<Thing> Goods(NationDef nation, int value, out string summary)
        {
            var things = new List<Thing>();
            var parts = new List<string>();
            float goodsBudget = value * 0.6f;
            List<ThingDef> pool = GoodsOf(nation);
            foreach (ThingDef def in pool.InRandomOrder().Take(3))
            {
                if (goodsBudget <= 0f) break;
                ThingDef stuff = def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null;
                float unit = def.GetStatValueAbstract(StatDefOf.MarketValue, stuff);
                if (unit <= 0f || unit > goodsBudget) continue;
                int count = Mathf.Clamp(Mathf.FloorToInt(goodsBudget / 2f / unit), 1, def.stackLimit);
                if (count * unit > goodsBudget) count = Mathf.Max(1, Mathf.FloorToInt(goodsBudget / unit));
                Thing thing = ThingMaker.MakeThing(def, stuff);
                thing.stackCount = count;
                thing.TryGetComp<CompQuality>()?.SetQuality(QualityCategory.Normal, ArtGenerationContext.Outsider);
                things.Add(thing);
                parts.Add(thing.LabelCap);
                goodsBudget -= count * unit;
                value -= Mathf.RoundToInt(count * unit);
            }
            int silver = Mathf.Max(0, value);
            while (silver > 0)
            {
                Thing s = ThingMaker.MakeThing(ThingDefOf.Silver);
                s.stackCount = Mathf.Min(silver, ThingDefOf.Silver.stackLimit);
                silver -= s.stackCount;
                things.Add(s);
                parts.Add(s.LabelCap);
            }
            summary = string.Join(", ", parts);
            return things;
        }
    }
}
