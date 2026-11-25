using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>A small, repeatable favour a nation asks of you: deliver goods, a fine piece of its own craft, or a book of another nation.</summary>
    public class Errand : IExposable
    {
        public NationDef nation;
        public string kind;
        public ThingDef thing;
        public int count = 1;
        public QualityCategory minQuality = QualityCategory.Awful;
        public int deadlineTick;
        public int silver;
        public float knowledge;
        public int goodwill;

        public void ExposeData()
        {
            Scribe_Defs.Look(ref nation, "nation");
            Scribe_Values.Look(ref kind, "kind");
            Scribe_Defs.Look(ref thing, "thing");
            Scribe_Values.Look(ref count, "count", 1);
            Scribe_Values.Look(ref minQuality, "minQuality");
            Scribe_Values.Look(ref deadlineTick, "deadlineTick");
            Scribe_Values.Look(ref silver, "silver");
            Scribe_Values.Look(ref knowledge, "knowledge");
            Scribe_Values.Look(ref goodwill, "goodwill");
        }

        public string Want => kind == "Craft" ? "HE_ErrandWantCraft".Translate(thing.LabelCap, minQuality.GetLabel()).Resolve() : thing.LabelCap + " x" + count;

        public int DaysLeft => Mathf.Max(0, (deadlineTick - Find.TickManager.TicksGame) / GenDate.TicksPerDay);
    }

    /// <summary>
    /// 3.5: errands. Now and then a friendly nation asks a favour by letter. Accepted errands wait on the Stories page until you deliver
    /// them (silver, knowledge and goodwill) or the time runs out (a little goodwill lost). At most three at once.
    /// </summary>
    public static class HeirsErrands
    {
        public const int MaxActive = 3;
        public const int Days = 15;
        public const float OfferChance = 0.5f;

        // Plain goods every nation may ask for: (thing, count).
        private static readonly (string, int)[] Supplies =
        {
            ("Steel", 150), ("WoodLog", 300), ("Cloth", 120), ("MedicineHerbal", 15), ("ComponentIndustrial", 6), ("Gold", 20),
            ("Leather_Plain", 80), ("Beer", 40), ("Pemmican", 80), ("BlocksGranite", 200), ("MealSimple", 30)
        };

        public static List<Errand> Active => HeirsGame.Get?.errands ?? new List<Errand>();

        public static void MonthlyTick()
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || Find.AnyPlayerHomeMap == null || game.errands.Count >= MaxActive || !Rand.Chance(OfferChance))
            {
                return;
            }
            Errand e = Make(HeirsWorld.LiveNations.Where(n => !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer) && HeirsPolitics.PlayerGoodwill(n) >= 0
                                                             && game.errands.All(x => x.nation != n)).RandomElementWithFallback());
            if (e != null)
            {
                Offer(e);
            }
        }

        /// <summary>Picks a favour for the nation: a book of another nation (if any exists), a piece of its own craft, or goods.</summary>
        public static Errand Make(NationDef nation, string kind = null)
        {
            if (nation == null)
            {
                return null;
            }
            kind = kind ?? new[] { "Supply", "Supply", "Craft", "Lore" }.RandomElement();
            var e = new Errand { nation = nation, kind = kind, deadlineTick = Find.TickManager.TicksGame + Days * GenDate.TicksPerDay };
            if (kind == "Lore")
            {
                ThingDef book = DefDatabase<ThingDef>.AllDefsListForReading.Where(d => BookNation(d) != null && BookNation(d) != nation
                                                                                     && d.tradeability != Tradeability.None).RandomElementWithFallback();
                if (book == null) return Make(nation, "Supply");
                e.thing = book;
                e.silver = 200;
                e.knowledge = 25f;
                e.goodwill = 15;
                return e;
            }
            if (kind == "Craft")
            {
                ThingDef craft = DefDatabase<ThingDef>.AllDefsListForReading.Where(d => (d.IsWeapon || d.IsApparel) && d.HasComp(typeof(CompQuality)) && d.recipeMaker != null
                                                                                      && d.GetModExtension<HeirsCultureExt>()?.nation == nation).RandomElementWithFallback();
                if (craft == null) return Make(nation, "Supply");
                e.thing = craft;
                e.minQuality = QualityCategory.Good;
                e.silver = Mathf.RoundToInt(craft.BaseMarketValue * 2.5f / 10f) * 10 + 100;
                e.knowledge = 15f;
                e.goodwill = 10;
                return e;
            }
            (string def, int count) = Supplies.Where(s => DefDatabase<ThingDef>.GetNamedSilentFail(s.Item1) != null).RandomElement();
            e.thing = DefDatabase<ThingDef>.GetNamed(def);
            e.count = count;
            e.silver = Mathf.RoundToInt(e.thing.BaseMarketValue * count * 1.4f / 10f) * 10;
            e.knowledge = 8f;
            e.goodwill = 8;
            return e;
        }

        public static NationDef BookNation(ThingDef def)
        {
            CompProperties_Book book = def.GetCompProperties<CompProperties_Book>();
            return book?.doers?.OfType<BookOutcomeProperties_HeirsKnowledge>().FirstOrDefault()?.nation;
        }

        public static void Offer(Errand e)
        {
            var letter = (ChoiceLetter_HeirsErrand)LetterMaker.MakeLetter(DefDatabase<LetterDef>.GetNamed("HE_ErrandLetter"));
            letter.errand = e;
            letter.Label = "HE_ErrandLabel".Translate(e.nation.LabelCap);
            letter.Text = ("HE_Errand" + e.kind + "Text").Translate(e.nation.LabelCap, HeirsCourt.RulerLine(e.nation), e.Want, Days, e.silver, e.knowledge.ToString("0"));
            HeirsMusic.Sting(e.nation);
            Find.LetterStack.ReceiveLetter(letter);
        }

        public static void Accept(Errand e)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || game.errands.Count >= MaxActive) return;
            e.deadlineTick = Find.TickManager.TicksGame + Days * GenDate.TicksPerDay;
            game.errands.Add(e);
        }

        private static IEnumerable<Thing> Matching(Errand e) => Find.Maps.Where(m => m.IsPlayerHome).SelectMany(m => m.listerThings.ThingsOfDef(e.thing))
            .Where(t => t.Spawned && !t.IsForbidden(Faction.OfPlayer) && (e.kind != "Craft" || (t.TryGetQuality(out QualityCategory q) && q >= e.minQuality)));

        public static bool CanDeliver(Errand e) => Matching(e).Sum(t => t.stackCount) >= e.count;

        public static bool Deliver(Errand e)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || !game.errands.Contains(e) || !CanDeliver(e)) return false;
            int left = e.count;
            foreach (Thing t in Matching(e).ToList())
            {
                if (left <= 0) break;
                int n = Mathf.Min(left, t.stackCount);
                left -= n;
                t.SplitOff(n).Destroy();
            }
            game.errands.Remove(e);
            if (e.silver > 0) HeirsChains.Give(ThingDefOf.Silver, e.silver);
            game.AddKnowledge(e.nation, e.knowledge, null);
            HeirsPolitics.Affect(e.nation, e.goodwill);
            game.errandsDone++;
            Messages.Message("HE_ErrandDone".Translate(e.nation.LabelCap, e.silver, e.knowledge.ToString("0")), MessageTypeDefOf.PositiveEvent, false);
            return true;
        }

        /// <summary>Every few hours: errands past their time are dropped, with a little goodwill lost.</summary>
        public static void TickRare(HeirsGame game)
        {
            int now = Find.TickManager.TicksGame;
            foreach (Errand e in game.errands.Where(x => x.nation == null || now > x.deadlineTick).ToList())
            {
                game.errands.Remove(e);
                if (e.nation == null) continue;
                HeirsPolitics.Affect(e.nation, -5);
                Messages.Message("HE_ErrandFailed".Translate(e.nation.LabelCap, e.Want), MessageTypeDefOf.NegativeEvent, false);
            }
        }
    }

    public class ChoiceLetter_HeirsErrand : ChoiceLetter
    {
        public Errand errand;
        public bool resolved;

        public override IEnumerable<DiaOption> Choices
        {
            get
            {
                if (resolved || ArchivedOnly || errand == null)
                {
                    yield return Option_Close;
                    yield break;
                }
                var accept = new DiaOption("HE_ErrandAccept".Translate())
                {
                    action = () => { resolved = true; HeirsErrands.Accept(errand); Find.LetterStack.RemoveLetter(this); },
                    resolveTree = true
                };
                if (HeirsErrands.Active.Count >= HeirsErrands.MaxActive)
                {
                    accept.Disable("HE_ErrandTooMany".Translate(HeirsErrands.MaxActive));
                }
                yield return accept;
                yield return new DiaOption("HE_ErrandRefuse".Translate())
                {
                    action = () => { resolved = true; Find.LetterStack.RemoveLetter(this); },
                    resolveTree = true
                };
            }
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Deep.Look(ref errand, "errand");
            Scribe_Values.Look(ref resolved, "resolved");
        }
    }
}
