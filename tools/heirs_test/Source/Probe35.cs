using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using Verse;

namespace HeProbe
{
    /// <summary>3.5 checks: the nations' books, the second sagas with their great books, and errands.</summary>
    public static class Probe35
    {
        private static int savedErrands = -1;
        private static int savedErrandsDone = -1;

        private static NationDef N(string name) => DefDatabase<NationDef>.GetNamed("HE_" + name);

        private static BookOutcomeProperties_HeirsKnowledge Doer(ThingDef def) =>
            def.GetCompProperties<CompProperties_Book>()?.doers?.OfType<BookOutcomeProperties_HeirsKnowledge>().FirstOrDefault();

        private static IEnumerable<ThingDef> Books => DefDatabase<ThingDef>.AllDefsListForReading.Where(d => Doer(d) != null);

        private static Thing Place(Thing t, Map map)
        {
            GenPlace.TryPlaceThing(t, P.Colonist(map).Position, map, ThingPlaceMode.Near);
            t.SetForbidden(false, false);
            return t;
        }

        private static void Spawn(ThingDef def, int count, Map map)
        {
            while (count > 0)
            {
                Thing t = ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                t.stackCount = System.Math.Min(count, def.stackLimit);
                count -= t.stackCount;
                Place(t, map);
            }
        }

        private static void Clear(ThingDef def)
        {
            foreach (Map m in Find.Maps)
            {
                foreach (Thing t in m.listerThings.ThingsOfDef(def).ToList()) t.Destroy();
            }
        }

        public static void Data()
        {
            List<ThingDef> books = Books.ToList();
            P.Check("27 heir books", books.Count == 27, books.Count.ToString());
            var bad = new List<string>();
            foreach (ThingDef d in books)
            {
                BookOutcomeProperties_HeirsKnowledge doer = Doer(d);
                CompProperties_Book props = d.GetCompProperties<CompProperties_Book>();
                bool epic = d.tradeability == Tradeability.None;
                if (doer.nation == null || !doer.titleKey.CanTranslate() || !doer.descKey.CanTranslate() || !P.HasTexture(d.graphicData.texPath)
                    || props.nameMaker?.defName != "HE_BookNamer" || props.descriptionMaker?.defName != "HE_BookDescriber" || d.thingClass != typeof(Book)
                    || (!epic && (d.tradeTags == null || !d.tradeTags.Contains("HE_Books_" + doer.nation.defName.Substring(3))))
                    || (epic && (d.thingSetMakerTags?.Count ?? 0) != 0))
                {
                    bad.Add(d.defName);
                }
            }
            P.Check("books: nation, title, blurb, cover, namer, trade tags", bad.Count == 0, string.Join(" ", bad));
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                P.Check("two classic books and a great book " + n.defName, books.Count(b => Doer(b).nation == n && b.tradeability != Tradeability.None) == 2
                                                                       && books.Count(b => Doer(b).nation == n && b.tradeability == Tradeability.None) == 1);
                foreach (string kind in new[] { "Caravan", "Settlement" })
                {
                    TraderKindDef trader = DefDatabase<TraderKindDef>.GetNamedSilentFail(n.defName + "_" + kind);
                    P.Check("books sold by " + n.defName + " " + kind, trader != null
                        && trader.stockGenerators.OfType<StockGenerator_Tag>().Any(g => (string)P.Get(g, "tradeTag") == "HE_Books_" + n.defName.Substring(3)));
                }
                ChainDef saga = DefDatabase<ChainDef>.GetNamedSilentFail("HE_Saga_" + n.defName.Substring(3));
                ChainDef first = DefDatabase<ChainDef>.GetNamedSilentFail("HE_Chain_" + n.defName.Substring(3));
                ChainStep research = saga?.steps.FirstOrDefault(s => s.kind == StepKind.Research);
                ChainStep build = saga?.steps.FirstOrDefault(s => s.kind == StepKind.Build);
                ChainStep site = saga?.steps.FirstOrDefault(s => s.kind == StepKind.Site);
                ChainStep deliver = saga?.steps.FirstOrDefault(s => s.kind == StepKind.Deliver);
                P.Check("saga " + n.defName, saga != null && saga.nation == n && saga.after == first && saga.steps.Count == 5
                    && saga.artifact != null && saga.artifact.tradeability == Tradeability.None && Doer(saga.artifact)?.nation == n
                    && research?.project?.GetModExtension<HeirsResearchExt>()?.requiresChain == first
                    && build?.building?.designationCategory != null && site?.siteReward != null && P.HasTexture(site.siteReward.graphicData.texPath)
                    && deliver != null && deliver.things.Count > 0 && deliver.things.All(t => t.thingDef != null)
                    && saga.steps.All(s => !s.label.NullOrEmpty() && !s.text.NullOrEmpty())
                    && saga.steps.Last().options.Count == 2 && saga.steps.Last().options[0].takes.Any(t => t.thingDef == site.siteReward));
            }
            P.Check("errand letter", DefDatabase<LetterDef>.GetNamedSilentFail("HE_ErrandLetter")?.letterClass == typeof(ChoiceLetter_HeirsErrand));
            foreach (string k in new[] { "HE_ErrandSupplyText", "HE_ErrandCraftText", "HE_ErrandLoreText", "HE_ChainAfter", "HE_BookBenefit", "HE_ErrandLine" })
            {
                P.Check("text " + k, k.CanTranslate());
            }
        }

        public static void Reading()
        {
            Map map = P.Home;
            HeirsGame game = P.Game;
            NationDef hellas = N("Hellas");
            // a scholarly ruler adds a quarter to all knowledge; the reading rates are checked without one
            if (HeirsCourt.Is(hellas, Temperament.Scholarly)) HeirsCourt.ReignOf(hellas).temperament = Temperament.Cautious;
            ThingDef def = DefDatabase<ThingDef>.GetNamed("HE_Book_Hellas_Elements");
            var book = (Book)ThingMaker.MakeThing(def);
            book.TryGetComp<CompQuality>().SetQuality(QualityCategory.Normal, ArtGenerationContext.Outsider);
            P.Check("book title is its own", book.Title == "HE_Book_Hellas_Elements_Title".Translate().Resolve().CapitalizeFirst() || book.Title.ToLower() == "HE_Book_Hellas_Elements_Title".Translate().Resolve().ToLower(), book.Title);
            P.Check("book blurb and benefit", book.DescriptionDetailed.Contains("HE_Book_Hellas_Elements_Desc".Translate().Resolve().Substring(0, 20))
                                              && book.DescriptionDetailed.Contains(hellas.adjective), book.DescriptionDetailed);
            Place(book, map);
            var doer = book.BookComp.Doers.OfType<BookOutcomeDoer_HeirsKnowledge>().Single();
            Pawn reader = P.Colonist(map);
            float before = game.Knowledge(hellas);
            if (before >= 130f) game.AddKnowledge(hellas, 100f - before, null);
            before = game.Knowledge(hellas);
            doer.OnReadingTick(reader, GenDate.TicksPerHour);
            float gain = game.Knowledge(hellas) - before;
            P.Check("an hour of reading teaches 0.8 x quality", System.Math.Abs(gain - 0.8f * 1.0f) < 0.01f, gain.ToString("0.000"));
            P.Check("book still has something to teach", doer.DoesProvidesOutcome(reader));
            game.AddKnowledge(hellas, 140f - game.Knowledge(hellas) + 1f, null);
            before = game.Knowledge(hellas);
            doer.OnReadingTick(reader, GenDate.TicksPerHour);
            P.Check("book teaches nothing past its cap", game.Knowledge(hellas) == before && !doer.DoesProvidesOutcome(reader), game.Knowledge(hellas).ToString("0.0"));
            P.Check("learned books say so", doer.GetBenefitsString(reader).Contains("HE_BookLearned".Translate().Resolve()));

            // a real reading job on a fresh book of another nation
            NationDef kemet = N("Kemet");
            var scroll = (Book)ThingMaker.MakeThing(DefDatabase<ThingDef>.GetNamed("HE_Book_Kemet_Instructions"));
            scroll.TryGetComp<CompQuality>().SetQuality(QualityCategory.Excellent, ArtGenerationContext.Outsider);
            Place(scroll, map);
            float k0 = game.Knowledge(kemet);
            if (k0 >= 75f)
            {
                game.AddKnowledge(kemet, 20f - k0, null);
                k0 = game.Knowledge(kemet);
            }
            reader.drafter.Drafted = false;
            reader.jobs.TryTakeOrderedJob(JobMaker.MakeJob(JobDefOf.Reading, scroll), Verse.AI.JobTag.Misc);
            P.Ticks(3000);
            P.Check("reading the scroll teaches Kemet", game.Knowledge(kemet) > k0, k0.ToString("0.00") + " -> " + game.Knowledge(kemet).ToString("0.00") + " job " + reader.CurJobDef?.defName);
            reader.jobs.EndCurrentJob(Verse.AI.JobCondition.InterruptForced);
            book.Destroy();
            if (!scroll.Destroyed) scroll.Destroy();

            // the traders carry them
            TraderKindDef trader = DefDatabase<TraderKindDef>.GetNamed("HE_Pars_Caravan");
            StockGenerator gen = trader.stockGenerators.OfType<StockGenerator_Tag>().First(g => (string)P.Get(g, "tradeTag") == "HE_Books_Pars");
            List<Thing> stock = gen.GenerateThings(map.Tile).ToList();
            foreach (Thing t in stock) t.PostGeneratedForTrader(trader, map.Tile, HeirsWorld.FactionOf(N("Pars")));
            P.Check("a Pars caravan carries a Pars book", stock.Count > 0 && stock.All(t => Doer(t.def)?.nation == N("Pars")), string.Join(", ", stock.Select(t => t.LabelCap)));
            P.Check("trade stock books have titles", stock.All(t => t is Book b && !b.Title.NullOrEmpty() && b.Title == b.Title.Trim()),
                string.Join(" | ", stock.Select(t => (t as Book)?.Title ?? "null")));
            foreach (Thing t in stock) t.Destroy();
            P.Calm();
        }

        public static void Saga()
        {
            HeirsGame game = P.Game;
            ChainDef first = DefDatabase<ChainDef>.GetNamed("HE_Chain_Albion");
            ChainDef saga = DefDatabase<ChainDef>.GetNamed("HE_Saga_Albion");
            NationDef albion = first.nation;
            ChainState fs = game.State(first);
            ChainState ss = game.State(saga);
            bool wasDone = fs.done;
            ss.started = false; ss.done = false; ss.step = 0;
            if (game.Knowledge(albion) < 200f) game.AddKnowledge(albion, 200f - game.Knowledge(albion), null);
            fs.done = false;
            P.Check("saga waits for the first story", !HeirsChains.CanStart(game, saga));
            fs.done = true;
            P.Check("saga opens after the first story", HeirsChains.CanStart(game, saga));
            HeirsChains.Start(game, saga);
            P.Check("saga started on its first step", ss.started && ss.step == 0 && HeirsChains.Current(saga, ss).kind == StepKind.Deliver);
            for (int i = 0; i < 4 && ss.step < 4; i++) HeirsChains.ForceCompleteStep(game, saga);
            ChainStep choice = HeirsChains.Current(saga, ss);
            P.Check("saga reaches its choice", choice != null && choice.kind == StepKind.Choice, ss.step.ToString());
            ThingDef relic = saga.steps[3].siteReward;
            if (!HeirsChains.PlayerHas(relic)) HeirsChains.Give(relic, 1);
            Clear(saga.artifact);
            P.Ticks(700);                                                   // rewards arrive by drop pod
            P.Check("the original is home before the choice", Find.Maps.Any(m => m.listerThings.ThingsOfDef(relic).Any()));
            float know = game.Knowledge(albion);
            HeirsChains.Choose(game, saga, 4, 0);
            P.Ticks(700);
            Thing great = Find.Maps.SelectMany(m => m.listerThings.ThingsOfDef(saga.artifact)).FirstOrDefault();
            P.Check("saga done, great book given", ss.done && great != null);
            P.Check("great book is legendary and teaches fast", great != null && great.TryGetQuality(out QualityCategory q) && q == QualityCategory.Legendary
                && ((Book)great).BookComp.Doers.OfType<BookOutcomeDoer_HeirsKnowledge>().Single().PerHour > 2.6f);
            P.Check("the original went home", !Find.Maps.Any(m => m.listerThings.ThingsOfDef(relic).Any()));
            P.Check("returning it taught knowledge", game.Knowledge(albion) >= know + 39f, know + " -> " + game.Knowledge(albion));
            if (!wasDone) fs.done = wasDone || fs.done;
            P.Calm();
        }

        public static void Errands()
        {
            Map map = P.Home;
            HeirsGame game = P.Game;
            game.errands.Clear();
            NationDef roma = N("Roma");
            Faction faction = HeirsWorld.FactionOf(roma);
            // friendly, with room for the errands' goodwill to show
            if (faction.HostileTo(Faction.OfPlayer) || faction.GoodwillWith(Faction.OfPlayer) < 20 || faction.GoodwillWith(Faction.OfPlayer) > 70)
            {
                faction.ChangeGoodwill_Debug(Faction.OfPlayer, 30 - faction.GoodwillWith(Faction.OfPlayer));
            }
            foreach (string kind in new[] { "Supply", "Craft", "Lore" })
            {
                Errand e = HeirsErrands.Make(roma, kind);
                P.Check("errand " + kind, e != null && e.kind == kind && e.thing != null && e.silver > 0 && e.knowledge > 0 && e.DaysLeft >= HeirsErrands.Days - 1
                    && !e.Want.NullOrEmpty(), e?.thing?.defName);
                if (kind == "Lore") P.Check("lore errand wants another nation's book", HeirsErrands.BookNation(e.thing) != null && HeirsErrands.BookNation(e.thing) != roma && e.thing.tradeability != Tradeability.None);
                if (kind == "Craft") P.Check("craft errand wants Roman craft", e.thing.GetModExtension<HeirsCultureExt>()?.nation == roma && e.minQuality == QualityCategory.Good);
            }

            // the letter
            int letters = Find.LetterStack.LettersListForReading.Count;
            HeirsErrands.Offer(HeirsErrands.Make(roma, "Supply"));
            var letter = Find.LetterStack.LettersListForReading.LastOrDefault() as ChoiceLetter_HeirsErrand;
            P.Check("errand letter arrives", letter != null && Find.LetterStack.LettersListForReading.Count == letters + 1 && letter.Choices.Count() == 2);
            letter.Choices.First().action();
            P.Check("accepting adds the errand", game.errands.Count == 1 && game.errands[0] == letter.errand);

            // deliver a supply errand
            Errand supply = game.errands[0];
            Clear(supply.thing);
            P.Check("cannot deliver without goods", !HeirsErrands.CanDeliver(supply));
            Spawn(supply.thing, supply.count, map);
            int silver = map.listerThings.ThingsOfDef(ThingDefOf.Silver).Sum(t => t.stackCount);
            float know = game.Knowledge(roma);
            int done = game.errandsDone;
            int goodwill = faction.GoodwillWith(Faction.OfPlayer);
            P.Check("supply errand delivered", HeirsErrands.Deliver(supply) && game.errands.Count == 0 && game.errandsDone == done + 1);
            P.Ticks(700);
            P.Check("supply errand paid", map.listerThings.ThingsOfDef(ThingDefOf.Silver).Sum(t => t.stackCount) >= silver + supply.silver && game.Knowledge(roma) >= know + supply.knowledge - 0.01f
                && faction.GoodwillWith(Faction.OfPlayer) > goodwill, silver + "->" + map.listerThings.ThingsOfDef(ThingDefOf.Silver).Sum(t => t.stackCount) + " (+" + supply.silver + ") " + know + "->" + game.Knowledge(roma) + " goodwill " + goodwill + "->" + faction.GoodwillWith(Faction.OfPlayer));
            P.Check("goods were taken", HeirsChains.CountAvailable(supply.thing) == 0 || supply.thing == ThingDefOf.Silver);

            // a craft errand needs good quality
            Errand craft = HeirsErrands.Make(roma, "Craft");
            HeirsErrands.Accept(craft);
            Clear(craft.thing);
            Thing poor = ThingMaker.MakeThing(craft.thing, craft.thing.MadeFromStuff ? GenStuff.DefaultStuffFor(craft.thing) : null);
            poor.TryGetComp<CompQuality>().SetQuality(QualityCategory.Normal, ArtGenerationContext.Colony);
            Place(poor, map);
            P.Check("normal craft is not enough", !HeirsErrands.CanDeliver(craft));
            Thing fine = ThingMaker.MakeThing(craft.thing, craft.thing.MadeFromStuff ? GenStuff.DefaultStuffFor(craft.thing) : null);
            fine.TryGetComp<CompQuality>().SetQuality(QualityCategory.Excellent, ArtGenerationContext.Colony);
            Place(fine, map);
            P.Check("excellent craft is", HeirsErrands.CanDeliver(craft) && HeirsErrands.Deliver(craft) && fine.Destroyed && !poor.Destroyed);
            poor.Destroy();

            // an errand that runs out of time
            Errand late = HeirsErrands.Make(roma, "Supply");
            HeirsErrands.Accept(late);
            late.deadlineTick = Find.TickManager.TicksGame - 1;
            goodwill = faction.GoodwillWith(Faction.OfPlayer);
            HeirsErrands.TickRare(game);
            P.Check("late errand dropped with goodwill lost", !game.errands.Contains(late) && faction.GoodwillWith(Faction.OfPlayer) < goodwill);

            // at most three
            for (int i = 0; i < HeirsErrands.MaxActive; i++) HeirsErrands.Accept(HeirsErrands.Make(N(i == 0 ? "Hellas" : i == 1 ? "Kemet" : "Pars"), "Supply"));
            HeirsErrands.Accept(HeirsErrands.Make(N("Inti"), "Supply"));
            P.Check("no more than three errands", game.errands.Count == HeirsErrands.MaxActive);
            HeirsErrands.Offer(HeirsErrands.Make(N("Inti"), "Lore"));
            var full = Find.LetterStack.LettersListForReading.LastOrDefault() as ChoiceLetter_HeirsErrand;
            P.Check("letter cannot be accepted when full", full != null && full.Choices.First().disabled);
            Find.LetterStack.RemoveLetter(full);
            game.errands.RemoveAt(0);
            savedErrands = game.errands.Count;
            savedErrandsDone = game.errandsDone;
            P.Calm();
        }

        public static void AfterLoad()
        {
            HeirsGame game = HeirsGame.Get;
            P.Check("errands saved", game.errands.Count == savedErrands && game.errands.All(e => e.nation != null && e.thing != null), game.errands.Count + "/" + savedErrands);
            P.Check("errands done saved", game.errandsDone == savedErrandsDone);
            P.Check("sagas saved", game.State(DefDatabase<ChainDef>.GetNamed("HE_Saga_Albion")).done);
        }
    }
}
