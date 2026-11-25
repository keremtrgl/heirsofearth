using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    public class NationPair : IExposable
    {
        public NationDef a;
        public NationDef b;
        public int startTick;

        public bool Is(NationDef x, NationDef y)
        {
            return (a == x && b == y) || (a == y && b == x);
        }

        public void ExposeData()
        {
            Scribe_Defs.Look(ref a, "a");
            Scribe_Defs.Look(ref b, "b");
            Scribe_Values.Look(ref startTick, "startTick");
        }
    }

    /// <summary>Living world politics between the heir nations.</summary>
    public class HeirsWorld : WorldComponent
    {
        public const int WarThreshold = -75;
        public const int AllianceThreshold = 80;
        public const int MinWarDays = 60;

        public List<NationPair> wars = new List<NationPair>();
        public List<NationPair> alliances = new List<NationPair>();
        public List<Reign> reigns = new List<Reign>();
        public int lastUpdateTick = -1;
        public int updates;

        public HeirsWorld(World world) : base(world)
        {
        }

        public static HeirsWorld Get => Find.World?.GetComponent<HeirsWorld>();

        public static Faction FactionOf(NationDef nation)
        {
            if (nation?.faction == null || Find.FactionManager == null)
            {
                return null;
            }
            Faction faction = Find.FactionManager.FirstFactionOfDef(nation.faction);
            return faction != null && !faction.defeated ? faction : null;
        }

        public static IEnumerable<NationDef> LiveNations => DefDatabase<NationDef>.AllDefsListForReading.Where(n => HeirsMod.Settings.NationActive(n) && FactionOf(n) != null);

        public bool AtWar(NationDef a, NationDef b)
        {
            return wars.Any(w => w.Is(a, b));
        }

        public bool Allied(NationDef a, NationDef b)
        {
            return alliances.Any(w => w.Is(a, b));
        }

        public static int Goodwill(NationDef a, NationDef b)
        {
            Faction fa = FactionOf(a), fb = FactionOf(b);
            FactionRelation r = fa != null && fb != null ? fa.RelationWith(fb, true) : null;
            return r?.baseGoodwill ?? 0;
        }

        public static void SetGoodwill(NationDef a, NationDef b, int value, FactionRelationKind? kind = null)
        {
            Faction fa = FactionOf(a), fb = FactionOf(b);
            if (fa == null || fb == null || fa == fb) return;
            FactionRelation r1 = fa.RelationWith(fb, true), r2 = fb.RelationWith(fa, true);
            if (r1 == null || r2 == null) return;
            value = Mathf.Clamp(value, -100, 100);
            r1.baseGoodwill = r2.baseGoodwill = value;
            if (kind.HasValue)
            {
                r1.kind = r2.kind = kind.Value;
            }
        }

        public void DeclareWar(NationDef a, NationDef b)
        {
            if (a == b || AtWar(a, b)) return;
            alliances.RemoveAll(p => p.Is(a, b));
            wars.Add(new NationPair { a = a, b = b, startTick = Find.TickManager.TicksGame });
            SetGoodwill(a, b, Mathf.Min(Goodwill(a, b), WarThreshold), FactionRelationKind.Hostile);
            string text = "HE_WarText".Translate(a.LabelCap, b.LabelCap);
            HeirsGame.Get?.AddChronicle(text, a);
            Find.LetterStack.ReceiveLetter("HE_WarLabel".Translate(a.LabelCap, b.LabelCap), text, DefDatabase<LetterDef>.GetNamedSilentFail("HE_WarLetter") ?? LetterDefOf.NeutralEvent);
        }

        public void MakePeace(NationDef a, NationDef b)
        {
            if (wars.RemoveAll(w => w.Is(a, b)) == 0) return;
            SetGoodwill(a, b, -40, FactionRelationKind.Neutral);
            string text = "HE_PeaceText".Translate(a.LabelCap, b.LabelCap);
            HeirsGame.Get?.AddChronicle(text, a);
            Find.LetterStack.ReceiveLetter("HE_PeaceLabel".Translate(a.LabelCap, b.LabelCap), text, LetterDefOf.NeutralEvent);
        }

        public override void WorldComponentTick()
        {
            if (!HeirsMod.Settings.politics)
            {
                return;
            }
            int now = Find.TickManager.TicksGame;
            if (lastUpdateTick < 0)
            {
                lastUpdateTick = now;
                return;
            }
            if (now - lastUpdateTick >= HeirsMod.Settings.politicsIntervalDays * GenDate.TicksPerDay)
            {
                lastUpdateTick = now;
                MonthlyTick();
            }
        }

        public void MonthlyTick()
        {
            if (!HeirsMod.Settings.politics)
            {
                return;
            }
            updates++;
            wars.RemoveAll(w => FactionOf(w.a) == null || FactionOf(w.b) == null);
            alliances.RemoveAll(w => FactionOf(w.a) == null || FactionOf(w.b) == null);
            HeirsCourt.MonthlyTick(this);
            List<NationDef> nations = LiveNations.ToList();
            for (int i = 0; i < nations.Count; i++)
            {
                for (int j = i + 1; j < nations.Count; j++)
                {
                    UpdatePair(nations[i], nations[j]);
                }
            }
            HeirsPolitics.MonthlyEvents(this);
            HeirsTreaties.MonthlyTick(HeirsGame.Get);
            HeirsEvents.MonthlyTick();
            HeirsErrands.MonthlyTick();
        }

        private void UpdatePair(NationDef a, NationDef b)
        {
            int drift = (a.IsFriendOf(b) ? 5 : 0) - (a.IsRivalOf(b) ? 5 : 0) + Rand.RangeInclusive(-10, 10) + HeirsCourt.Drift(a, b);
            int goodwill = Goodwill(a, b) + drift;
            bool atWar = AtWar(a, b);
            SetGoodwill(a, b, goodwill, atWar ? FactionRelationKind.Hostile : (Allied(a, b) ? FactionRelationKind.Ally : FactionRelationKind.Neutral));
            if (atWar)
            {
                NationPair war = wars.First(w => w.Is(a, b));
                if (Find.TickManager.TicksGame - war.startTick > MinWarDays * GenDate.TicksPerDay && Rand.Chance(0.25f))
                {
                    MakePeace(a, b);
                }
                else if (Rand.Chance(0.10f))
                {
                    HeirsPolitics.WarSkirmish(this, a, b);
                }
                return;
            }
            if (HeirsMod.Settings.interStateWar && goodwill <= WarThreshold && !HeirsCourt.HoldsBackFromWar(a, b))
            {
                DeclareWar(a, b);
                return;
            }
            if (!Allied(a, b) && goodwill >= AllianceThreshold && a.IsFriendOf(b))
            {
                alliances.Add(new NationPair { a = a, b = b, startTick = Find.TickManager.TicksGame });
                SetGoodwill(a, b, goodwill, FactionRelationKind.Ally);
                HeirsGame.Get?.AddChronicle("HE_AllianceText".Translate(a.LabelCap, b.LabelCap), a);
            }
            else if (Allied(a, b) && goodwill < 40)
            {
                alliances.RemoveAll(p => p.Is(a, b));
                SetGoodwill(a, b, goodwill, FactionRelationKind.Neutral);
                HeirsGame.Get?.AddChronicle("HE_AllianceEndText".Translate(a.LabelCap, b.LabelCap), a);
            }
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Collections.Look(ref wars, "wars", LookMode.Deep);
            Scribe_Collections.Look(ref alliances, "alliances", LookMode.Deep);
            Scribe_Collections.Look(ref reigns, "reigns", LookMode.Deep);
            Scribe_Values.Look(ref lastUpdateTick, "lastUpdateTick", -1);
            Scribe_Values.Look(ref updates, "updates");
            if (Scribe.mode == LoadSaveMode.PostLoadInit)
            {
                if (wars == null) wars = new List<NationPair>();
                if (alliances == null) alliances = new List<NationPair>();
                if (reigns == null) reigns = new List<Reign>();
                reigns.RemoveAll(r => r?.nation == null);
                wars.RemoveAll(w => w?.a == null || w.b == null);
                alliances.RemoveAll(w => w?.a == null || w.b == null);
            }
        }
    }

    public static class HeirsWorldHooks
    {
        public const int MinNewSettlements = 2;
        public const int MaxNewSettlements = 5;

        /// <summary>Generates a faction of the nation, its relations and up to count settlements. Returns the faction.</summary>
        public static Faction AddNation(NationDef nation, int count)
        {
            Faction faction = FactionGenerator.NewGeneratedFaction(new FactionGeneratorParms(nation.faction));
            Find.FactionManager.Add(faction);
            foreach (Faction other in Find.FactionManager.AllFactionsListForReading)
            {
                if (other != faction && faction.RelationWith(other, true) == null)
                {
                    faction.TryMakeInitialRelationsWith(other);
                }
            }
            int placed = 0;
            for (int i = 0; i < count; i++)
            {
                PlanetTile tile = TileFinder.RandomSettlementTileFor(faction);
                if (!tile.Valid)
                {
                    continue;
                }
                Settlement settlement = (Settlement)WorldObjectMaker.MakeWorldObject(WorldObjectDefOf.Settlement);
                settlement.SetFaction(faction);
                settlement.Tile = tile;
                settlement.Name = SettlementNameGenerator.GenerateSettlementName(settlement);
                Find.WorldObjects.Add(settlement);
                placed++;
            }
            if (placed == 0)
            {
                Log.Warning("[Heirs of Earth] No free tile for " + nation.defName + "; it has no settlements.");
            }
            HeirsGame.Get?.AddChronicle("HE_NationArrivedText".Translate(nation.LabelCap), nation);
            return faction;
        }

        /// <summary>A save made before a nation existed gets that nation, with settlements and relations, when it is loaded.</summary>
        public static List<NationDef> AddMissingNations()
        {
            var added = new List<NationDef>();
            if (!HeirsMod.Settings.addMissingNations || Find.World == null || Find.FactionManager == null || Find.WorldObjects == null)
            {
                return added;
            }
            List<int> sizes = HeirsWorld.LiveNations.Select(n => Find.WorldObjects.Settlements.Count(s => s.Faction == HeirsWorld.FactionOf(n))).ToList();
            int perNation = Mathf.Clamp(sizes.Count > 0 ? Mathf.RoundToInt((float)sizes.Average()) : 3, MinNewSettlements, MaxNewSettlements);
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                if (nation.faction == null || !HeirsMod.Settings.NationActive(nation) || Find.FactionManager.FirstFactionOfDef(nation.faction) != null)
                {
                    continue;
                }
                try
                {
                    AddNation(nation, perNation);
                    added.Add(nation);
                }
                catch (System.Exception e)
                {
                    Log.Error("[Heirs of Earth] Could not add " + nation.defName + " to this save: " + e);
                }
            }
            if (added.Count > 0)
            {
                string names = added.Select(n => n.LabelCap.ToString()).ToCommaList(true);
                Find.LetterStack.ReceiveLetter("HE_NationArrivedLabel".Translate(), "HE_NationArrivedLetter".Translate(names), LetterDefOf.NeutralEvent);
            }
            return added;
        }

        public static void OnHeritageChosen(NationDef nation)
        {
            if (nation == null || Faction.OfPlayerSilentFail == null)
            {
                return;
            }
            Faction own = HeirsWorld.FactionOf(nation);
            if (own != null && own.HasGoodwill)
            {
                int target = 60 - own.GoodwillWith(Faction.OfPlayer);
                own.TryAffectGoodwillWith(Faction.OfPlayer, target, false, false, null);
            }
            foreach (NationDef rival in nation.rivals)
            {
                Faction f = HeirsWorld.FactionOf(rival);
                if (f != null && f.HasGoodwill)
                {
                    f.TryAffectGoodwillWith(Faction.OfPlayer, -20, false, false, null);
                }
            }
        }
    }
}
