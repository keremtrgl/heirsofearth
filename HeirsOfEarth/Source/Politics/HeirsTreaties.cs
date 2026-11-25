using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    public enum TreatyKind
    {
        Peace,
        Trade,
        Science,
        Alliance
    }

    /// <summary>A treaty between your colony and one nation.</summary>
    public class Treaty : IExposable
    {
        public NationDef nation;
        public TreatyKind kind;
        public int signedTick;
        public int lastBenefitTick;

        public void ExposeData()
        {
            Scribe_Defs.Look(ref nation, "nation");
            Scribe_Values.Look(ref kind, "kind");
            Scribe_Values.Look(ref signedTick, "signedTick");
            Scribe_Values.Look(ref lastBenefitTick, "lastBenefitTick");
        }
    }

    /// <summary>
    /// 3.4: treaties with the nations, signed from the Diplomacy page for a gift of silver (or offered by a ruler for free).
    /// Peace: no tribute demands and slowly rising goodwill. Trade: a trade caravan every twenty days. Science exchange: their
    /// knowledge each month (needs an embassy). Defensive alliance: their warriors come when you are raided (needs an embassy).
    /// A treaty ends when the nation turns hostile, when you cancel it (other nations hear of it) or when a new ruler revokes it.
    /// </summary>
    public static class HeirsTreaties
    {
        public const int CaravanDays = 20;
        public const int AidCooldownDays = 10;
        public const float AidChance = 0.6f;
        public const float AidPointsFactor = 0.6f;
        public const int ScienceKnowledge = 8;
        public const int HonourKnowledge = 4;
        public const int CancelPenalty = 15;
        public const int OathBreakerPenalty = 3;

        public static readonly TreatyKind[] Kinds = { TreatyKind.Peace, TreatyKind.Trade, TreatyKind.Science, TreatyKind.Alliance };

        public static int MinGoodwill(TreatyKind k) => k == TreatyKind.Peace ? 0 : k == TreatyKind.Trade ? 20 : k == TreatyKind.Science ? 30 : 60;

        public static int Fee(TreatyKind k) => k == TreatyKind.Peace ? 200 : k == TreatyKind.Trade ? 300 : k == TreatyKind.Science ? 500 : 800;

        public static bool NeedsEmbassy(TreatyKind k) => k == TreatyKind.Science || k == TreatyKind.Alliance;

        public static ThingDef EmbassyDef => DefDatabase<ThingDef>.GetNamedSilentFail("HE_Embassy");

        public static bool HasEmbassy()
        {
            ThingDef def = EmbassyDef;
            return def != null && Find.Maps.Any(m => m.IsPlayerHome && m.listerBuildings.ColonistsHaveBuilding(def));
        }

        public static List<Treaty> All => HeirsGame.Get?.treaties ?? new List<Treaty>();

        public static bool Has(NationDef nation, TreatyKind kind) => All.Any(t => t.nation == nation && t.kind == kind);

        public static int Count(NationDef nation) => All.Count(t => t.nation == nation);

        public static bool CanSign(NationDef nation, TreatyKind kind, bool free, out string reason)
        {
            reason = null;
            Faction faction = HeirsWorld.FactionOf(nation);
            if (faction == null || Faction.OfPlayerSilentFail == null)
            {
                reason = "HE_TreatyNoNation".Translate();
                return false;
            }
            if (Has(nation, kind))
            {
                reason = "HE_TreatyAlready".Translate();
                return false;
            }
            if (faction.HostileTo(Faction.OfPlayer))
            {
                reason = "HE_TreatyHostile".Translate(nation.LabelCap);
                return false;
            }
            if (HeirsPolitics.PlayerGoodwill(nation) < MinGoodwill(kind))
            {
                reason = "HE_TreatyGoodwill".Translate(MinGoodwill(kind));
                return false;
            }
            if (NeedsEmbassy(kind) && !HasEmbassy())
            {
                reason = "HE_TreatyEmbassy".Translate();
                return false;
            }
            if (!free && HeirsChains.CountAvailable(ThingDefOf.Silver) < Fee(kind))
            {
                reason = "HE_NotEnoughSilver".Translate(Fee(kind));
                return false;
            }
            return true;
        }

        public static bool Sign(NationDef nation, TreatyKind kind, bool free)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || !CanSign(nation, kind, free, out _))
            {
                return false;
            }
            if (!free)
            {
                HeirsChains.TakeFromColony(ThingDefOf.Silver, Fee(kind));
            }
            int now = Find.TickManager.TicksGame;
            game.treaties.Add(new Treaty { nation = nation, kind = kind, signedTick = now, lastBenefitTick = now });
            HeirsPolitics.Affect(nation, 5);
            game.AddChronicle("HE_TreatySigned".Translate(Label(kind), nation.LabelCap), nation);
            CheckHonour(game, nation);
            return true;
        }

        /// <summary>Ends a treaty. byPlayer: you broke your word, the nation and every other nation think less of you.</summary>
        public static void Cancel(NationDef nation, TreatyKind kind, bool byPlayer, string reasonKey = null)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || game.treaties.RemoveAll(t => t.nation == nation && t.kind == kind) == 0)
            {
                return;
            }
            if (byPlayer)
            {
                HeirsPolitics.Affect(nation, -CancelPenalty);
                foreach (NationDef other in HeirsWorld.LiveNations.Where(n => n != nation))
                {
                    HeirsPolitics.Affect(other, -OathBreakerPenalty);
                }
            }
            game.AddChronicle((reasonKey ?? "HE_TreatyEnded").Translate(Label(kind), nation.LabelCap), nation);
        }

        public static string Label(TreatyKind kind) => ("HE_Treaty" + kind).Translate().Resolve();

        public static string Description(TreatyKind kind) => ("HE_Treaty" + kind + "Desc").Translate().Resolve();

        /// <summary>A new ruler reviews the treaties: with low goodwill each one may be revoked.</summary>
        public static void ReviewAfterSuccession(NationDef nation)
        {
            if (HeirsPolitics.PlayerGoodwill(nation) >= 40)
            {
                return;
            }
            foreach (Treaty t in All.Where(x => x.nation == nation).ToList())
            {
                if (Rand.Chance(0.5f))
                {
                    Cancel(nation, t.kind, false, "HE_TreatyRevoked");
                    Find.LetterStack.ReceiveLetter("HE_TreatyRevokedLabel".Translate(nation.LabelCap),
                        "HE_TreatyRevokedText".Translate(HeirsCourt.RulerLine(nation), Label(t.kind), nation.LabelCap), LetterDefOf.NegativeEvent);
                }
            }
        }

        /// <summary>Monthly: hostile nations void their treaties, the others deliver their benefits.</summary>
        public static void MonthlyTick(HeirsGame game)
        {
            if (game == null || Faction.OfPlayerSilentFail == null)
            {
                return;
            }
            game.treaties.RemoveAll(t => t.nation == null || HeirsWorld.FactionOf(t.nation) == null);
            bool embassy = HasEmbassy();
            foreach (NationDef nation in game.treaties.Select(t => t.nation).Distinct().ToList())
            {
                Faction faction = HeirsWorld.FactionOf(nation);
                if (faction.HostileTo(Faction.OfPlayer))
                {
                    foreach (Treaty t in game.treaties.Where(x => x.nation == nation).ToList())
                    {
                        Cancel(nation, t.kind, false, "HE_TreatyVoid");
                    }
                    Find.LetterStack.ReceiveLetter("HE_TreatyVoidLabel".Translate(nation.LabelCap), "HE_TreatyVoidText".Translate(nation.LabelCap), LetterDefOf.NegativeEvent);
                    continue;
                }
                int goodwill = embassy ? 1 : 0;
                foreach (Treaty t in game.treaties.Where(x => x.nation == nation))
                {
                    switch (t.kind)
                    {
                        case TreatyKind.Peace: goodwill += 3; break;
                        case TreatyKind.Trade: goodwill += 1; break;
                        case TreatyKind.Science:
                            goodwill += 1;
                            game.AddKnowledge(nation, ScienceKnowledge, null);
                            break;
                        case TreatyKind.Alliance: goodwill += 2; break;
                    }
                }
                HeirsPolitics.Affect(nation, goodwill);
                if (TitleRank(nation) >= 4)
                {
                    game.AddKnowledge(nation, HonourKnowledge, null);
                }
                CheckHonour(game, nation);
            }
            SendCaravans(game);
        }

        /// <summary>Trade treaties: a caravan from the nation every twenty days or so.</summary>
        public static void SendCaravans(HeirsGame game)
        {
            Map map = Find.AnyPlayerHomeMap;
            if (map == null)
            {
                return;
            }
            int now = Find.TickManager.TicksGame;
            foreach (Treaty t in game.treaties.Where(x => x.kind == TreatyKind.Trade))
            {
                Faction faction = HeirsWorld.FactionOf(t.nation);
                if (faction == null || faction.HostileTo(Faction.OfPlayer) || now - t.lastBenefitTick < CaravanDays * GenDate.TicksPerDay)
                {
                    continue;
                }
                t.lastBenefitTick = now;
                var parms = new IncidentParms { target = map, faction = faction, forced = true };
                Find.Storyteller.incidentQueue.Add(IncidentDefOf.TraderCaravanArrival, now + Rand.RangeInclusive(1, 3) * GenDate.TicksPerDay, parms);
            }
        }

        /// <summary>Defensive alliance: after a raid on your home, an allied nation may send warriors. Returns the ally that answered.</summary>
        public static NationDef AnswerRaid(IncidentParms raid)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || !(raid?.target is Map map) || !map.IsPlayerHome || raid.faction == null || !raid.faction.HostileTo(Faction.OfPlayer))
            {
                return null;
            }
            int now = Find.TickManager.TicksGame;
            foreach (Treaty t in game.treaties.Where(x => x.kind == TreatyKind.Alliance).InRandomOrder())
            {
                Faction ally = HeirsWorld.FactionOf(t.nation);
                if (ally == null || ally == raid.faction || ally.HostileTo(Faction.OfPlayer) || now - t.lastBenefitTick < AidCooldownDays * GenDate.TicksPerDay
                    || !Rand.Chance(AidChance))
                {
                    continue;
                }
                t.lastBenefitTick = now;
                var parms = new IncidentParms
                {
                    target = map, faction = ally, forced = true, points = Mathf.Max(200f, raid.points * AidPointsFactor),
                    raidStrategy = RaidStrategyDefOf.ImmediateAttackFriendly, raidArrivalMode = PawnsArrivalModeDefOf.EdgeWalkIn
                };
                Find.Storyteller.incidentQueue.Add(IncidentDefOf.RaidFriendly, now + Rand.RangeInclusive(1000, 2500), parms);
                Messages.Message("HE_AllyAnswers".Translate(t.nation.LabelCap), MessageTypeDefOf.PositiveEvent, false);
                return t.nation;
            }
            return null;
        }

        public static void RaidPostfix(IncidentWorker_Raid __instance, IncidentParms parms, bool __result)
        {
            if (__result && __instance is IncidentWorker_RaidEnemy)
            {
                AnswerRaid(parms);
            }
        }

        // ------------------------------------------------------------------ titles
        /// <summary>Your standing with a nation: 0 stranger, 1 guest, 2 friend, 3 honoured friend, 4 the nation's own high honour.</summary>
        public static int TitleRank(NationDef nation)
        {
            Faction faction = HeirsWorld.FactionOf(nation);
            if (faction == null || Faction.OfPlayerSilentFail == null || faction.HostileTo(Faction.OfPlayer))
            {
                return 0;
            }
            int goodwill = HeirsPolitics.PlayerGoodwill(nation);
            if (goodwill >= 80 && Has(nation, TreatyKind.Alliance) && HasEmbassy()) return 4;
            if (goodwill >= 60 && Count(nation) >= 2) return 3;
            if (goodwill >= 40) return 2;
            return goodwill >= 0 ? 1 : 0;
        }

        public static string TitleLabel(NationDef nation)
        {
            int rank = TitleRank(nation);
            return rank == 4 && !nation.honoraryTitle.NullOrEmpty() ? nation.honoraryTitle.CapitalizeFirst() : ("HE_Title" + rank).Translate().Resolve();
        }

        /// <summary>The first time you earn a nation's high honour, it is proclaimed.</summary>
        public static void CheckHonour(HeirsGame game, NationDef nation)
        {
            if (TitleRank(nation) < 4 || game.honours.Contains(nation))
            {
                return;
            }
            game.honours.Add(nation);
            string text = "HE_HonourText".Translate(HeirsCourt.RulerLine(nation), nation.LabelCap, nation.honoraryTitle ?? "", HonourKnowledge);
            game.AddChronicle("HE_HonourChronicle".Translate(nation.honoraryTitle ?? "", nation.LabelCap), nation);
            Find.LetterStack.ReceiveLetter("HE_HonourLabel".Translate(nation.LabelCap), text, LetterDefOf.PositiveEvent);
            HeirsMusic.Play(nation);
        }
    }

    public class Patch_DefensiveAlliance : HeirsPatch
    {
        public override string Id => "DefensiveAlliance";

        public override void Apply(HarmonyLib.Harmony harmony)
        {
            harmony.Patch(HeirsPatches.Need(typeof(IncidentWorker_Raid), "TryExecuteWorker"),
                postfix: new HarmonyLib.HarmonyMethod(typeof(HeirsTreaties), nameof(HeirsTreaties.RaidPostfix)));
        }
    }
}
