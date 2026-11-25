using System.Collections.Generic;
using System.Linq;
using RimWorld;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>The character of a ruler. It shapes what the court offers, demands and fights for.</summary>
    public enum Temperament
    {
        Warlike,
        Mercantile,
        Scholarly,
        Pious,
        Cautious
    }

    /// <summary>One nation's current reign: who rules (the faction leader), with which temperament, since when and until when.</summary>
    public class Reign : IExposable
    {
        public NationDef nation;
        public int leaderId = -1;
        public string rulerName;
        public Temperament temperament;
        public int crownedTick;
        public int endTick;
        public int number = 1;

        public void ExposeData()
        {
            Scribe_Defs.Look(ref nation, "nation");
            Scribe_Values.Look(ref leaderId, "leaderId", -1);
            Scribe_Values.Look(ref rulerName, "rulerName");
            Scribe_Values.Look(ref temperament, "temperament");
            Scribe_Values.Look(ref crownedTick, "crownedTick");
            Scribe_Values.Look(ref endTick, "endTick");
            Scribe_Values.Look(ref number, "number", 1);
        }
    }

    /// <summary>
    /// 3.4: every heir nation is ruled by its faction leader, who has a temperament. Reigns last four to ten years; then the crown
    /// passes on (a leader who dies or is killed is followed at once). A new ruler may review the treaties with you, and a warlike
    /// rival may use the change of crown to start a war.
    /// </summary>
    public static class HeirsCourt
    {
        public const int MinReignYears = 4;
        public const int MaxReignYears = 10;
        public const float SuccessionWarChance = 0.2f;
        public const float ScholarlyKnowledgeFactor = 1.25f;
        public const float WarlikeTributeFactor = 1.5f;

        public static Reign ReignOf(NationDef nation)
        {
            HeirsWorld world = HeirsWorld.Get;
            if (world == null || nation == null)
            {
                return null;
            }
            Reign reign = world.reigns.FirstOrDefault(r => r.nation == nation);
            if (reign == null && HeirsWorld.FactionOf(nation) != null)
            {
                reign = NewReign(nation, null);
                world.reigns.Add(reign);
            }
            return reign;
        }

        public static Temperament? TemperamentOf(NationDef nation)
        {
            return HeirsMod.Settings.politics ? ReignOf(nation)?.temperament : null;
        }

        public static bool Is(NationDef nation, Temperament t) => TemperamentOf(nation) == t;

        public static Temperament RollTemperament(NationDef nation)
        {
            return System.Enum.GetValues(typeof(Temperament)).Cast<Temperament>()
                .RandomElementByWeight(t => nation.temperamentBias != null && nation.temperamentBias.Contains(t) ? 3f : 1f);
        }

        private static Reign NewReign(NationDef nation, Reign before)
        {
            Faction faction = HeirsWorld.FactionOf(nation);
            Pawn leader = faction?.leader;
            int now = Find.TickManager?.TicksGame ?? 0;
            return new Reign
            {
                nation = nation,
                leaderId = leader?.thingIDNumber ?? -1,
                rulerName = leader?.Name?.ToStringFull ?? faction?.Name ?? nation.LabelCap.Resolve(),
                temperament = RollTemperament(nation),
                crownedTick = now,
                endTick = now + Rand.RangeInclusive(MinReignYears * GenDate.DaysPerYear, MaxReignYears * GenDate.DaysPerYear) * GenDate.TicksPerDay,
                number = (before?.number ?? 0) + 1
            };
        }

        /// <summary>"Imperator Gaius Valerius, the Bold".</summary>
        public static string RulerLine(NationDef nation)
        {
            Reign r = ReignOf(nation);
            if (r == null)
            {
                return "";
            }
            return "HE_RulerLine".Translate(nation.rulerTitle.CapitalizeFirst(), r.rulerName, ("HE_Epithet" + r.temperament).Translate()).Resolve();
        }

        public static string TemperamentText(Temperament t) => ("HE_Temperament" + t).Translate().Resolve() + ": " + ("HE_Temperament" + t + "Desc").Translate().Resolve();

        public static int ReignYears(Reign r) => (Find.TickManager.TicksGame - r.crownedTick) / (GenDate.DaysPerYear * GenDate.TicksPerDay);

        /// <summary>Monthly: notices leaders who died, ends long reigns and starts new ones.</summary>
        public static void MonthlyTick(HeirsWorld world)
        {
            world.reigns.RemoveAll(r => r.nation == null || HeirsWorld.FactionOf(r.nation) == null);
            foreach (NationDef nation in HeirsWorld.LiveNations.ToList())
            {
                Reign reign = ReignOf(nation);
                Faction faction = HeirsWorld.FactionOf(nation);
                if (reign == null || faction == null)
                {
                    continue;
                }
                if (faction.leader == null)
                {
                    faction.TryGenerateNewLeader();
                }
                int id = faction.leader?.thingIDNumber ?? -1;
                if (reign.leaderId == -1 && id != -1)
                {
                    reign.leaderId = id;
                    reign.rulerName = faction.leader.Name?.ToStringFull ?? reign.rulerName;
                }
                else if (id != reign.leaderId)
                {
                    Succeed(world, nation, false);
                }
                else if (Find.TickManager.TicksGame >= reign.endTick)
                {
                    Succeed(world, nation, true);
                }
            }
        }

        /// <summary>
        /// The crown passes. natural: the old ruler's reign ended (a new leader is chosen and a letter tells of it); otherwise the leader
        /// died or was replaced and vanilla already sent its own letter, so only the chronicle and a message tell of the new temperament.
        /// </summary>
        public static Reign Succeed(HeirsWorld world, NationDef nation, bool natural)
        {
            Faction faction = HeirsWorld.FactionOf(nation);
            Reign old = world.reigns.FirstOrDefault(r => r.nation == nation);
            if (faction == null)
            {
                return old;
            }
            string oldName = old?.rulerName ?? "";
            if (natural)
            {
                CrownHeir(faction);
            }
            world.reigns.RemoveAll(r => r.nation == nation);
            Reign reign = NewReign(nation, old);
            world.reigns.Add(reign);
            string text = "HE_SuccessionText".Translate(nation.LabelCap, oldName, RulerLine(nation), TemperamentText(reign.temperament)).Resolve();
            HeirsGame.Get?.AddChronicle("HE_SuccessionChronicle".Translate(RulerLine(nation), nation.LabelCap), nation);
            if (natural)
            {
                HeirsMusic.Sting(nation);
                Find.LetterStack.ReceiveLetter("HE_SuccessionLabel".Translate(nation.LabelCap), text, LetterDefOf.NeutralEvent);
            }
            else
            {
                Messages.Message("HE_SuccessionMessage".Translate(RulerLine(nation), nation.LabelCap), MessageTypeDefOf.NeutralEvent, false);
            }
            HeirsTreaties.ReviewAfterSuccession(nation);
            SuccessionWar(world, nation);
            return reign;
        }

        /// <summary>
        /// A new leader who is not the old one. Vanilla may hand the crown back to an existing world pawn, the old ruler included,
        /// and leaves the faction leaderless when it finds no leader kind; either way a freshly made heir of the old ruler's kind takes it.
        /// </summary>
        private static void CrownHeir(Faction faction)
        {
            Pawn previous = faction.leader;
            for (int i = 0; i < 3; i++)
            {
                if (faction.TryGenerateNewLeader() && faction.leader != previous)
                {
                    return;
                }
            }
            PawnKindDef kind = previous?.kindDef ?? faction.def.fixedLeaderKinds?.FirstOrDefault();
            if (kind == null)
            {
                faction.leader = previous;
                return;
            }
            Pawn heir = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, faction, PawnGenerationContext.NonPlayer, null, true));
            if (heir.RaceProps.IsFlesh)
            {
                heir.relations.everSeenByPlayer = true;
            }
            if (!Find.WorldPawns.Contains(heir))
            {
                Find.WorldPawns.PassToWorld(heir, RimWorld.Planet.PawnDiscardDecideMode.KeepForever);
            }
            faction.leader = heir;
        }

        /// <summary>A warlike rival may strike while the court is busy with the new ruler.</summary>
        private static void SuccessionWar(HeirsWorld world, NationDef nation)
        {
            if (!HeirsMod.Settings.interStateWar)
            {
                return;
            }
            NationDef rival = nation.rivals.Where(r => HeirsWorld.FactionOf(r) != null && !world.AtWar(r, nation) && Is(r, Temperament.Warlike)).RandomElementWithFallback();
            if (rival != null && Rand.Chance(SuccessionWarChance))
            {
                world.DeclareWar(rival, nation);
            }
        }

        /// <summary>Monthly goodwill drift between two nations from their rulers: warlike rulers sour on rivals, mercantile ones warm to everyone.</summary>
        public static int Drift(NationDef a, NationDef b)
        {
            int d = 0;
            foreach ((NationDef x, NationDef y) in new[] { (a, b), (b, a) })
            {
                Temperament? t = TemperamentOf(x);
                if (t == Temperament.Warlike && x.IsRivalOf(y)) d -= 4;
                if (t == Temperament.Mercantile) d += 2;
                if (t == Temperament.Cautious) d += 1;
            }
            return d;
        }

        /// <summary>A cautious ruler on either side usually holds back from war.</summary>
        public static bool HoldsBackFromWar(NationDef a, NationDef b)
        {
            return (Is(a, Temperament.Cautious) || Is(b, Temperament.Cautious)) && Rand.Chance(0.5f);
        }
    }
}
