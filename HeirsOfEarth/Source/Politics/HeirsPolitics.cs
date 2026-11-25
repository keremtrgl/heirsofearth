using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>Events the politics bring to the player, and settlement changes during wars.</summary>
    public static class HeirsPolitics
    {
        public const int SilverTributeMin = 300;
        public const int SilverTributeMax = 800;
        public const int MediationCost = 500;

        public static Faction Player => Faction.OfPlayerSilentFail;

        public static int PlayerGoodwill(NationDef nation)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            return f != null && Player != null ? f.GoodwillWith(Player) : 0;
        }

        public static void Affect(NationDef nation, int amount)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            if (f != null && f.HasGoodwill && amount != 0)
            {
                f.TryAffectGoodwillWith(Player, amount, true, true, null);
            }
        }

        public static void MonthlyEvents(HeirsWorld world)
        {
            if (Find.AnyPlayerHomeMap == null || Player == null)
            {
                return;
            }
            var options = new List<System.Func<bool>> { TryEnvoy, TryTribute, () => TryWarCall(world), () => TryMarriage(), () => TryMediation(world), TryTreatyOffer };
            if (world.updates % 2 == 0)
            {
                TryAllianceGift();
            }
            if (Rand.Chance(0.6f))
            {
                foreach (System.Func<bool> pick in options.InRandomOrder())
                {
                    if (pick()) break;
                }
            }
        }

        private static IEnumerable<NationDef> Friendly(int min) => HeirsWorld.LiveNations.Where(n => !HeirsWorld.FactionOf(n).HostileTo(Player) && PlayerGoodwill(n) >= min);

        public static bool TryEnvoy()
        {
            NationDef nation = Friendly(-20).RandomElementWithFallback();
            if (nation == null) return false;
            int gift = Rand.RangeInclusive(150, 400);
            return Send("Envoy", nation, null, gift);
        }

        public static bool TryTribute()
        {
            NationDef nation = HeirsWorld.LiveNations.Where(n => !HeirsWorld.FactionOf(n).HostileTo(Player) && PlayerGoodwill(n) < 10 && PlayerGoodwill(n) > -75
                && !HeirsTreaties.Has(n, TreatyKind.Peace)).RandomElementWithFallback();
            if (nation == null) return false;
            int amount = TributeAmount(Find.AnyPlayerHomeMap.wealthWatcher.WealthTotal);
            if (HeirsCourt.Is(nation, Temperament.Warlike)) amount = Mathf.RoundToInt(amount * HeirsCourt.WarlikeTributeFactor / 50f) * 50; // a warlike ruler asks more
            return Send("Tribute", nation, null, amount);
        }

        /// <summary>Silver a nation demands: 1% of colony wealth within 300-800, times the tribute setting, in steps of 50.</summary>
        public static int TributeAmount(float wealth)
        {
            return Mathf.Max(50, Mathf.RoundToInt(Mathf.Clamp(wealth * 0.01f, SilverTributeMin, SilverTributeMax) * HeirsMod.Settings.tributeDemand / 50f) * 50);
        }

        public static bool TryWarCall(HeirsWorld world)
        {
            foreach (NationPair war in world.wars.InRandomOrder())
            {
                foreach ((NationDef ally, NationDef enemy) in new[] { (war.a, war.b), (war.b, war.a) })
                {
                    if (PlayerGoodwill(ally) >= 60 && !HeirsWorld.FactionOf(enemy).HostileTo(Player))
                    {
                        return Send("WarCall", ally, enemy, 0);
                    }
                }
            }
            return false;
        }

        public static bool TryMarriage()
        {
            NationDef nation = Friendly(40).Where(n => n.release >= 2 || n.faction != null).RandomElementWithFallback();
            return nation != null && Send("Marriage", nation, null, 0);
        }

        public static bool TryMediation(HeirsWorld world)
        {
            NationPair war = world.wars.Where(w => PlayerGoodwill(w.a) >= 0 && PlayerGoodwill(w.b) >= 0).RandomElementWithFallback();
            return war != null && Send("Mediation", war.a, war.b, MediationCost);
        }

        /// <summary>A ruler offers the treaty that suits their temperament, without the usual gift of silver.</summary>
        public static bool TryTreatyOffer()
        {
            foreach (NationDef nation in Friendly(0).InRandomOrder())
            {
                Temperament? t = HeirsCourt.TemperamentOf(nation);
                TreatyKind kind = t == Temperament.Mercantile ? TreatyKind.Trade : t == Temperament.Scholarly ? TreatyKind.Science
                    : t == Temperament.Warlike ? TreatyKind.Alliance : TreatyKind.Peace;
                if (HeirsTreaties.CanSign(nation, kind, true, out _))
                {
                    return Send("TreatyOffer", nation, null, (int)kind);
                }
            }
            return false;
        }

        public static bool TryAllianceGift()
        {
            NationDef nation = Friendly(75).Where(n => n.archive != null).RandomElementWithFallback();
            if (nation == null) return false;
            HeirsChains.Give(nation.archive, 1);
            HeirsMusic.Sting(nation);
            Find.LetterStack.ReceiveLetter("HE_GiftLabel".Translate(nation.LabelCap), "HE_GiftText".Translate(nation.LabelCap, nation.archive.label), LetterDefOf.PositiveEvent);
            return true;
        }

        private static bool Send(string kind, NationDef a, NationDef b, int amount)
        {
            var letter = (ChoiceLetter_HeirsPolitics)LetterMaker.MakeLetter(DefDatabase<LetterDef>.GetNamed("HE_PoliticsLetter"));
            letter.kind = kind;
            letter.a = a;
            letter.b = b;
            letter.amount = amount;
            string ruler = a.rulerTitle ?? "";
            letter.Label = ("HE_" + kind + "Label").Translate(a.LabelCap, kind == "TreatyOffer" ? HeirsTreaties.Label((TreatyKind)amount) : b?.LabelCap ?? "");
            letter.Text = kind == "TreatyOffer"
                ? "HE_TreatyOfferText".Translate(HeirsCourt.RulerLine(a), a.LabelCap, HeirsTreaties.Label((TreatyKind)amount), HeirsTreaties.Description((TreatyKind)amount))
                : ("HE_" + kind + "Text").Translate(a.LabelCap, b?.LabelCap ?? "", amount, ruler);
            HeirsMusic.Sting(a);
            Find.LetterStack.ReceiveLetter(letter);
            return true;
        }

        /// <summary>Applies a choice. option 0 = accept, 1 = refuse.</summary>
        public static void Resolve(string kind, NationDef a, NationDef b, int amount, int option)
        {
            HeirsWorld world = HeirsWorld.Get;
            HeirsGame game = HeirsGame.Get;
            bool accept = option == 0;
            switch (kind)
            {
                case "Envoy":
                    Affect(a, accept ? 15 : -5);
                    if (accept) HeirsChains.Give(ThingDefOf.Silver, amount);
                    break;
                case "Tribute":
                    if (accept && HeirsChains.CountAvailable(ThingDefOf.Silver) >= amount)
                    {
                        HeirsChains.TakeFromColony(ThingDefOf.Silver, amount);
                        Affect(a, 10);
                    }
                    else
                    {
                        Affect(a, -25);
                        Map map = Find.AnyPlayerHomeMap;
                        Faction raider = HeirsChains.HostileFaction(a);
                        if (map != null && raider != null)
                        {
                            IncidentParms parms = StorytellerUtility.DefaultParmsNow(IncidentCategoryDefOf.ThreatBig, map);
                            parms.faction = raider;
                            parms.points *= HeirsMod.Settings.raidStrength;
                            parms.forced = true;
                            Find.Storyteller.incidentQueue.Add(IncidentDefOf.RaidEnemy, Find.TickManager.TicksGame + 2 * GenDate.TicksPerDay, parms);
                        }
                    }
                    break;
                case "WarCall":
                    if (accept)
                    {
                        Faction enemy = HeirsWorld.FactionOf(b);
                        if (enemy != null && enemy.HasGoodwill)
                        {
                            enemy.TryAffectGoodwillWith(Player, -200, true, true, null);
                        }
                        Affect(a, 25);
                        if (a.archive != null) HeirsChains.Give(a.archive, 2);
                    }
                    else
                    {
                        Affect(a, -20);
                    }
                    break;
                case "Marriage":
                    if (accept)
                    {
                        Faction faction = HeirsWorld.FactionOf(a);
                        Map map = Find.AnyPlayerHomeMap;
                        if (faction != null && map != null)
                        {
                            Pawn pawn = PawnGenerator.GeneratePawn(new PawnGenerationRequest(faction.def.basicMemberKind, faction, PawnGenerationContext.NonPlayer, map.Tile, mustBeCapableOfViolence: false));
                            pawn.SetFaction(Player);
                            GenSpawn.Spawn(pawn, CellFinder.RandomClosewalkCellNear(DropCellFinder.TradeDropSpot(map), map, 5), map);
                            game?.AddChronicle("HE_MarriageChronicle".Translate(pawn.LabelShort, a.LabelCap), a);
                        }
                        Affect(a, 20);
                    }
                    else
                    {
                        Affect(a, -5);
                    }
                    break;
                case "TreatyOffer":
                    if (accept) HeirsTreaties.Sign(a, (TreatyKind)amount, true);
                    else Affect(a, -3);
                    break;
                case "Mediation":
                    if (accept && HeirsChains.CountAvailable(ThingDefOf.Silver) >= amount)
                    {
                        HeirsChains.TakeFromColony(ThingDefOf.Silver, amount);
                        world?.MakePeace(a, b);
                        Affect(a, 15);
                        Affect(b, 15);
                    }
                    break;
            }
        }

        /// <summary>During a war the stronger side may take a nearby settlement; a nation with none left collapses.</summary>
        public static void WarSkirmish(HeirsWorld world, NationDef a, NationDef b)
        {
            Faction fa = HeirsWorld.FactionOf(a), fb = HeirsWorld.FactionOf(b);
            if (fa == null || fb == null) return;
            List<Settlement> sa = Find.WorldObjects.Settlements.Where(s => s.Faction == fa).ToList();
            List<Settlement> sb = Find.WorldObjects.Settlements.Where(s => s.Faction == fb).ToList();
            bool aStronger = sa.Count > sb.Count || (sa.Count == sb.Count && Rand.Bool);
            NationDef winner = aStronger ? a : b, loser = aStronger ? b : a;
            List<Settlement> winners = aStronger ? sa : sb, losers = aStronger ? sb : sa;
            CaptureNearest(world, winner, loser, winners, losers);
        }

        public static bool CaptureNearest(HeirsWorld world, NationDef winner, NationDef loser, List<Settlement> winners, List<Settlement> losers)
        {
            if (winners.Count == 0 || losers.Count == 0) return false;
            Settlement target = losers.Where(l => winners.Any(w => Find.WorldGrid.ApproxDistanceInTiles(w.Tile, l.Tile) <= 15f)).RandomElementWithFallback();
            if (target == null) return false;
            target.SetFaction(HeirsWorld.FactionOf(winner));
            string text = "HE_CaptureText".Translate(winner.LabelCap, target.LabelCap, loser.LabelCap);
            HeirsGame.Get?.AddChronicle(text, winner);
            Find.LetterStack.ReceiveLetter("HE_CaptureLabel".Translate(target.LabelCap), text, LetterDefOf.NeutralEvent, target);
            if (losers.Count == 1)
            {
                Collapse(world, loser);
            }
            return true;
        }

        public static void Collapse(HeirsWorld world, NationDef nation)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            if (f == null) return;
            f.defeated = true;
            world.wars.RemoveAll(w => w.a == nation || w.b == nation);
            world.alliances.RemoveAll(w => w.a == nation || w.b == nation);
            string text = "HE_CollapseText".Translate(nation.LabelCap);
            HeirsGame.Get?.AddChronicle(text, nation);
            Find.LetterStack.ReceiveLetter("HE_CollapseLabel".Translate(nation.LabelCap), text, LetterDefOf.NegativeEvent);
        }
    }

    public class ChoiceLetter_HeirsPolitics : ChoiceLetter
    {
        public string kind;
        public NationDef a;
        public NationDef b;
        public int amount;
        public bool resolved;

        public override IEnumerable<DiaOption> Choices
        {
            get
            {
                if (resolved || ArchivedOnly)
                {
                    yield return Option_Close;
                    yield break;
                }
                for (int i = 0; i < 2; i++)
                {
                    int option = i;
                    var dia = new DiaOption(("HE_" + kind + (i == 0 ? "Accept" : "Refuse")).Translate(kind == "TreatyOffer" ? HeirsTreaties.Label((TreatyKind)amount) : amount.ToString()))
                    {
                        action = () =>
                        {
                            resolved = true;
                            HeirsPolitics.Resolve(kind, a, b, amount, option);
                            Find.LetterStack.RemoveLetter(this);
                        },
                        resolveTree = true
                    };
                    if (i == 0 && (kind == "Tribute" || kind == "Mediation") && HeirsChains.CountAvailable(ThingDefOf.Silver) < amount)
                    {
                        dia.Disable("HE_NotEnoughSilver".Translate(amount));
                    }
                    yield return dia;
                }
            }
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Values.Look(ref kind, "kind");
            Scribe_Defs.Look(ref a, "a");
            Scribe_Defs.Look(ref b, "b");
            Scribe_Values.Look(ref amount, "amount");
            Scribe_Values.Look(ref resolved, "resolved");
        }
    }
}
