using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>
    /// The World Council, the end goal of 3.0. It opens after three finished story chains or three trade roads kept for a year.
    /// With a Council Hall built, the player can call one meeting per quadrum. Two ways to win:
    /// unity (two thirds of the living nations vote yes) or dominion (every living nation has sworn fealty to the player).
    /// The game goes on after the victory.
    /// </summary>
    public static class HeirsCouncil
    {
        public const int ChainsToUnlock = 3;
        public const int RoutesToUnlock = 3;
        public const int MeetingIntervalDays = 15;
        public const int YesGoodwill = 60;
        public const int FealtyOfferIntervalDays = 30;
        public const int TributeIntervalDays = 30;
        public const int TributePerSettlement = 100;
        public const int FealtyGoodwill = 25;
        public const string HallDefName = "HE_CouncilHall";

        /// <summary>Test hook: when set, victory does not roll the credits.</summary>
        public static bool NoCredits;

        public static bool Enabled => HeirsMod.Settings.councilVictory;

        private static ThingDef hall;

        public static ThingDef Hall => hall ?? (hall = DefDatabase<ThingDef>.GetNamedSilentFail(HallDefName));

        public static int ChainsDone(HeirsGame game) => HeirsChains.All.Count(c => game.State(c).done);

        public static int OldRoutes(HeirsGame game)
        {
            int now = Find.TickManager.TicksGame;
            return game.routes.Count(r => now - r.openedTick >= GenDate.TicksPerYear);
        }

        public static bool UnlockReady(HeirsGame game) => ChainsDone(game) >= ChainsToUnlock || OldRoutes(game) >= RoutesToUnlock;

        public static bool HallBuilt()
        {
            return Hall != null && Find.Maps.Any(m => m.IsPlayerHome && m.listerThings.ThingsOfDef(Hall).Any(t => t.Faction == Faction.OfPlayer));
        }

        public static int DaysToNextMeeting(HeirsGame game)
        {
            int left = game.lastMeetingTick + MeetingIntervalDays * GenDate.TicksPerDay - Find.TickManager.TicksGame;
            return Mathf.Max(0, Mathf.CeilToInt(left / (float)GenDate.TicksPerDay));
        }

        public static bool CanMeet(HeirsGame game, out string reason)
        {
            reason = null;
            if (!Enabled) reason = "HE_CouncilDisabled".Translate();
            else if (game.councilWon != null) reason = "HE_CouncilAlreadyWon".Translate();
            else if (!game.councilUnlocked) reason = "HE_CouncilLocked".Translate();
            else if (!HallBuilt()) reason = "HE_CouncilNeedHall".Translate();
            else if (DaysToNextMeeting(game) > 0) reason = "HE_CouncilWait".Translate(DaysToNextMeeting(game));
            return reason == null;
        }

        public static bool IsVassal(HeirsGame game, NationDef nation) => game.vassals.Contains(nation);

        /// <summary>How a nation would vote for unity now, and why.</summary>
        public static bool Vote(HeirsGame game, NationDef nation, out string why)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            if (f == null)
            {
                why = "HE_VoteGone".Translate();
                return false;
            }
            if (IsVassal(game, nation))
            {
                why = "HE_VoteVassal".Translate();
                return true;
            }
            if (f.RelationKindWith(Faction.OfPlayer) == FactionRelationKind.Ally)
            {
                why = "HE_VoteAlly".Translate();
                return true;
            }
            if (!BaseYes(game, nation))
            {
                why = f.HostileTo(Faction.OfPlayer) ? "HE_VoteHostile".Translate().Resolve() : "HE_VoteGoodwill".Translate(YesGoodwill, f.GoodwillWith(Faction.OfPlayer)).Resolve();
                return false;
            }
            HeirsWorld world = HeirsWorld.Get;
            NationDef enemy = world == null ? null : HeirsWorld.LiveNations.FirstOrDefault(o => o != nation && world.AtWar(nation, o) && BaseYes(game, o));
            if (enemy != null)
            {
                why = "HE_VoteEnemyYes".Translate(enemy.LabelCap);
                return false;
            }
            why = "HE_VoteFriend".Translate(f.GoodwillWith(Faction.OfPlayer));
            return true;
        }

        private static bool BaseYes(HeirsGame game, NationDef nation)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            if (f == null || f.HostileTo(Faction.OfPlayer)) return false;
            return IsVassal(game, nation) || f.RelationKindWith(Faction.OfPlayer) == FactionRelationKind.Ally || f.GoodwillWith(Faction.OfPlayer) >= YesGoodwill;
        }

        public static int YesNeeded(int living) => Mathf.CeilToInt(living * 2f / 3f);

        public static bool AllSubdued(HeirsGame game) => HeirsWorld.LiveNations.All(n => IsVassal(game, n));

        /// <summary>Holds a council meeting: dominion if every nation has sworn fealty, else a unity vote. Returns the victory kind or null.</summary>
        public static string Meet(HeirsGame game, bool force = false)
        {
            if (!force && !CanMeet(game, out _))
            {
                return null;
            }
            game.lastMeetingTick = Find.TickManager.TicksGame;
            List<NationDef> living = HeirsWorld.LiveNations.ToList();
            if (AllSubdued(game))
            {
                Victory(game, "Dominion");
                return "Dominion";
            }
            var lines = new List<string>();
            int yes = 0;
            foreach (NationDef n in living)
            {
                bool v = Vote(game, n, out string why);
                if (v) yes++;
                lines.Add((v ? "HE_VoteYes" : "HE_VoteNo").Translate().Resolve() + "  " + n.LabelCap + ": " + why);
            }
            int need = YesNeeded(living.Count);
            if (living.Count > 0 && yes >= need)
            {
                Victory(game, "Unity");
                return "Unity";
            }
            string text = "HE_CouncilFailedText".Translate(yes, living.Count, need, string.Join("\n", lines), MeetingIntervalDays);
            game.AddChronicle("HE_CouncilFailedChronicle".Translate(yes, living.Count));
            Find.LetterStack.ReceiveLetter("HE_CouncilFailedLabel".Translate(), text, LetterDefOf.NeutralEvent);
            return null;
        }

        public static void Victory(HeirsGame game, string kind)
        {
            game.councilWon = kind;
            string text = ("HE_Victory" + kind + "Text").Translate(Faction.OfPlayer.Name);
            game.AddChronicle(("HE_Victory" + kind + "Chronicle").Translate());
            Find.LetterStack.ReceiveLetter(("HE_Victory" + kind + "Label").Translate(), text, LetterDefOf.PositiveEvent);
            if (!NoCredits)
            {
                GameVictoryUtility.ShowCredits(text, SongDefOf.EndCreditsSong, false, 5f);
            }
        }

        /// <summary>Called every 2500 ticks from HeirsGame: unlock, fealty offers, tributes and broken oaths.</summary>
        public static void TickRare(HeirsGame game)
        {
            if (!Enabled || Faction.OfPlayerSilentFail == null)
            {
                return;
            }
            if (!game.councilUnlocked && UnlockReady(game))
            {
                Unlock(game);
            }
            int now = Find.TickManager.TicksGame;
            foreach (NationDef nation in game.vassals.ToList())
            {
                Faction f = HeirsWorld.FactionOf(nation);
                if (f == null)
                {
                    game.vassals.Remove(nation);
                }
                else if (f.HostileTo(Faction.OfPlayer))
                {
                    game.vassals.Remove(nation);
                    string text = "HE_FealtyBrokenText".Translate(nation.LabelCap);
                    game.AddChronicle(text, nation);
                    Find.LetterStack.ReceiveLetter("HE_FealtyBrokenLabel".Translate(nation.LabelCap), text, LetterDefOf.ThreatSmall);
                }
            }
            if (game.vassals.Count > 0 && now - game.lastTributeTick >= TributeIntervalDays * GenDate.TicksPerDay)
            {
                game.lastTributeTick = now;
                PayTribute(game);
            }
            foreach (NationDef nation in HeirsWorld.LiveNations.ToList())
            {
                int count = Settlements(nation);
                int peak = game.peakSettlements.TryGetValue(nation, out int p) ? p : 0;
                if (count > peak)
                {
                    game.peakSettlements[nation] = peak = count;
                }
                if (IsVassal(game, nation) || peak < 2 || count * 2 > peak || !HeirsWorld.FactionOf(nation).HostileTo(Faction.OfPlayer))
                {
                    continue;
                }
                int last = game.fealtyOffers.TryGetValue(nation, out int t) ? t : -999999999;
                if (now - last >= FealtyOfferIntervalDays * GenDate.TicksPerDay)
                {
                    game.fealtyOffers[nation] = now;
                    OfferFealty(nation, count, peak);
                }
            }
        }

        public static int Settlements(NationDef nation)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            return f == null ? 0 : Find.WorldObjects.Settlements.Count(s => s.Faction == f);
        }

        public static void Unlock(HeirsGame game)
        {
            game.councilUnlocked = true;
            game.AddChronicle("HE_CouncilUnlockedChronicle".Translate());
            Find.LetterStack.ReceiveLetter("HE_CouncilUnlockedLabel".Translate(), "HE_CouncilUnlockedText".Translate(), LetterDefOf.PositiveEvent);
        }

        public static void OfferFealty(NationDef nation, int count, int peak)
        {
            var letter = (ChoiceLetter_HeirsFealty)LetterMaker.MakeLetter(DefDatabase<LetterDef>.GetNamed("HE_FealtyLetter"));
            letter.nation = nation;
            letter.Label = "HE_FealtyLabel".Translate(nation.LabelCap);
            letter.Text = "HE_FealtyText".Translate(nation.LabelCap, peak - count, peak, nation.rulerTitle ?? "", TributePerSettlement * Mathf.Max(1, count), TributeIntervalDays);
            Find.LetterStack.ReceiveLetter(letter);
        }

        public static void AcceptFealty(HeirsGame game, NationDef nation)
        {
            Faction f = HeirsWorld.FactionOf(nation);
            if (f == null || game.vassals.Contains(nation))
            {
                return;
            }
            if (game.vassals.Count == 0) game.lastTributeTick = Find.TickManager.TicksGame;
            game.vassals.Add(nation);
            // Heir factions use goodwill, so the relation follows the goodwill value; lifting it ends the war.
            int gw = f.GoodwillWith(Faction.OfPlayer);
            if (gw < FealtyGoodwill)
            {
                f.TryAffectGoodwillWith(Faction.OfPlayer, FealtyGoodwill - gw, false, false, null);
            }
            game.AddChronicle("HE_FealtyAcceptedChronicle".Translate(nation.LabelCap), nation);
        }

        public static void PayTribute(HeirsGame game)
        {
            Map map = Find.AnyPlayerHomeMap;
            if (map == null) return;
            var things = new List<Thing>();
            var names = new List<string>();
            int total = 0;
            foreach (NationDef nation in game.vassals)
            {
                int amount = TributePerSettlement * Mathf.Max(1, Settlements(nation));
                total += amount;
                names.Add(nation.LabelCap + " (" + amount + ")");
            }
            int left = total;
            while (left > 0)
            {
                Thing s = ThingMaker.MakeThing(ThingDefOf.Silver);
                s.stackCount = Mathf.Min(left, ThingDefOf.Silver.stackLimit);
                left -= s.stackCount;
                things.Add(s);
            }
            if (things.Count == 0) return;
            DropPodUtility.DropThingsNear(DropCellFinder.TradeDropSpot(map), map, things, 110, false, false, false, forbid: false);
            Find.LetterStack.ReceiveLetter("HE_TributeArrivesLabel".Translate(), "HE_TributeArrivesText".Translate(total, string.Join(", ", names)),
                LetterDefOf.PositiveEvent, new LookTargets(things.Where(t => t.Spawned)));
        }
    }

    public class ChoiceLetter_HeirsFealty : ChoiceLetter
    {
        public NationDef nation;
        public bool resolved;

        public override IEnumerable<DiaOption> Choices
        {
            get
            {
                if (resolved || ArchivedOnly || nation == null || HeirsWorld.FactionOf(nation) == null)
                {
                    yield return Option_Close;
                    yield break;
                }
                yield return new DiaOption("HE_FealtyAccept".Translate())
                {
                    action = () =>
                    {
                        resolved = true;
                        HeirsCouncil.AcceptFealty(HeirsGame.Get, nation);
                        Find.LetterStack.RemoveLetter(this);
                    },
                    resolveTree = true
                };
                yield return new DiaOption("HE_FealtyRefuse".Translate())
                {
                    action = () =>
                    {
                        resolved = true;
                        HeirsGame.Get?.AddChronicle("HE_FealtyRefusedChronicle".Translate(nation.LabelCap), nation);
                        Find.LetterStack.RemoveLetter(this);
                    },
                    resolveTree = true
                };
                yield return Option_Postpone;
            }
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Defs.Look(ref nation, "nation");
            Scribe_Values.Look(ref resolved, "resolved");
        }
    }
}
