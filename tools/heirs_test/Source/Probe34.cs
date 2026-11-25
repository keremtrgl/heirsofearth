using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using Verse;

namespace HeProbe
{
    /// <summary>3.4 checks: rulers and succession, treaties and their benefits, the embassy, titles and world events.</summary>
    public static class Probe34
    {
        internal static int savedTreaties = -1; // taken again at the moment of saving (ProbeRun.Save): a treaty can break before that
        private static string savedRuler;

        private static List<QueuedIncident> Queue()
        {
            var list = new List<QueuedIncident>();
            foreach (object q in Find.Storyteller.incidentQueue) list.Add((QueuedIncident)q);
            return list;
        }

        private static void SetGoodwill(Faction f, int value)
        {
            int now = f.GoodwillWith(Faction.OfPlayer);
            if (now != value) f.ChangeGoodwill_Debug(Faction.OfPlayer, value - now);
        }

        private static void Spawn(ThingDef def, int count, Map map)
        {
            Pawn near = P.Colonist(map);
            while (count > 0)
            {
                Thing t = ThingMaker.MakeThing(def);
                t.stackCount = System.Math.Min(count, def.stackLimit);
                count -= t.stackCount;
                GenPlace.TryPlaceThing(t, near.Position, map, ThingPlaceMode.Near);
                t.SetForbidden(false, false);
            }
        }

        public static void Data()
        {
            var bad = new List<string>();
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                if (n.temperamentBias.NullOrEmpty() || n.honoraryTitle.NullOrEmpty()) bad.Add(n.defName);
            }
            P.Check("every nation has a court: temperaments and an honorary title", bad.Count == 0, string.Join(" ", bad));
            ThingDef embassy = DefDatabase<ThingDef>.GetNamedSilentFail("HE_Embassy");
            P.Check("embassy and its research", embassy != null && embassy.researchPrerequisites.Any(r => r.HasModExtension<HeirsResearchExt>()) && P.HasTexture(embassy.graphicData.texPath));
            P.Check("event letter and thoughts", DefDatabase<LetterDef>.GetNamedSilentFail("HE_EventLetter")?.letterClass == typeof(ChoiceLetter_HeirsEvent)
                && DefDatabase<ThoughtDef>.GetNamedSilentFail("HE_GamesVictor") != null && DefDatabase<ThoughtDef>.GetNamedSilentFail("HE_GamesContender") != null);
            foreach (Temperament t in System.Enum.GetValues(typeof(Temperament)))
            {
                P.Check("temperament text " + t, ("HE_Temperament" + t).CanTranslate() && ("HE_Temperament" + t + "Desc").CanTranslate() && ("HE_Epithet" + t).CanTranslate());
            }
            foreach (TreatyKind k in HeirsTreaties.Kinds)
            {
                P.Check("treaty text " + k, ("HE_Treaty" + k).CanTranslate() && ("HE_Treaty" + k + "Desc").CanTranslate());
            }
        }

        public static void Court()
        {
            HeirsWorld world = HeirsWorld.Get;
            var live = HeirsWorld.LiveNations.ToList();
            P.Check("every living nation has a ruler", live.Count > 0 && live.All(n => HeirsCourt.ReignOf(n) != null && !HeirsCourt.RulerLine(n).NullOrEmpty()),
                string.Join("; ", live.Select(n => HeirsCourt.RulerLine(n))));
            NationDef nation = live.FirstOrDefault(n => HeirsWorld.FactionOf(n).leader != null) ?? live.First();
            Faction faction = HeirsWorld.FactionOf(nation);
            Reign before = HeirsCourt.ReignOf(nation);
            int oldLeader = faction.leader?.thingIDNumber ?? -1, number = before.number, chronicle = HeirsGame.Get.chronicle.Count;
            Reign after = HeirsCourt.Succeed(world, nation, true);
            P.Check("succession crowns a new ruler", after != before && after.number == number + 1 && (faction.leader?.thingIDNumber ?? -1) != oldLeader
                && after.leaderId == faction.leader?.thingIDNumber && HeirsGame.Get.chronicle.Count > chronicle,
                "ruler " + after.rulerName + " #" + after.number);
            after.leaderId = -5; // as if the leader died and vanilla chose another
            HeirsCourt.MonthlyTick(world);
            Reign third = HeirsCourt.ReignOf(nation);
            P.Check("a leader's death is noticed", third != after && third.number == after.number + 1 && third.leaderId == faction.leader?.thingIDNumber);
            third.endTick = Find.TickManager.TicksGame - 1;
            HeirsCourt.MonthlyTick(world);
            P.Check("a long reign ends", HeirsCourt.ReignOf(nation) != third);
            P.Check("reigns last years", HeirsCourt.ReignOf(nation).endTick - Find.TickManager.TicksGame >= HeirsCourt.MinReignYears * GenDate.DaysPerYear * GenDate.TicksPerDay - 10);

            // vanilla may hand the crown back to the old ruler; every heir nation, several times over, must crown someone new
            bool wars = HeirsMod.Settings.interStateWar;
            HeirsMod.Settings.interStateWar = false;
            var same = new List<string>();
            foreach (NationDef n in live)
            {
                for (int i = 0; i < 4; i++)
                {
                    Pawn old = HeirsWorld.FactionOf(n).leader;
                    Reign was = HeirsCourt.ReignOf(n);
                    Reign now = HeirsCourt.Succeed(world, n, true);
                    Pawn lead = HeirsWorld.FactionOf(n).leader;
                    if (lead == null || lead == old || now.leaderId != lead.thingIDNumber || (was != null && now.rulerName == was.rulerName))
                    {
                        same.Add(n.defName + ":" + now.rulerName);
                    }
                }
            }
            HeirsMod.Settings.interStateWar = wars;
            P.Check("every succession crowns someone new", same.Count == 0, string.Join(", ", same));
            Find.LetterStack.LettersListForReading.ToList().ForEach(l => Find.LetterStack.RemoveLetter(l));

            Reign r = HeirsCourt.ReignOf(nation);
            Temperament keep = r.temperament;
            r.temperament = Temperament.Scholarly;
            float k0 = HeirsGame.Get.Knowledge(nation);
            HeirsGame.Get.AddKnowledge(nation, 10f, null);
            P.Check("a scholarly court shares more knowledge", System.Math.Abs(HeirsGame.Get.Knowledge(nation) - k0 - 12.5f) < 0.01f, (HeirsGame.Get.Knowledge(nation) - k0).ToString("F2"));
            HeirsGame.Get.SetKnowledge(nation, k0);
            NationDef rival = nation.rivals.FirstOrDefault(x => HeirsCourt.ReignOf(x) != null);
            if (rival != null)
            {
                Temperament keepRival = HeirsCourt.ReignOf(rival).temperament;
                r.temperament = Temperament.Warlike;
                HeirsCourt.ReignOf(rival).temperament = Temperament.Warlike;
                P.Check("warlike rulers sour on rivals", HeirsCourt.Drift(nation, rival) < 0, HeirsCourt.Drift(nation, rival).ToString());
                HeirsCourt.ReignOf(rival).temperament = keepRival;
            }
            r.temperament = keep;
            int rolls = 0;
            for (int i = 0; i < 300; i++) if (nation.temperamentBias.Contains(HeirsCourt.RollTemperament(nation))) rolls++;
            P.Check("nations lean toward their temperaments", rolls > 300 * 0.4f, rolls + "/300");
            savedRuler = HeirsCourt.ReignOf(nation).rulerName;
        }

        public static void Treaties()
        {
            Map map = P.Home;
            HeirsGame game = HeirsGame.Get;
            NationDef nation = HeirsWorld.LiveNations.FirstOrDefault(n => !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer)) ?? HeirsWorld.LiveNations.First();
            Faction faction = HeirsWorld.FactionOf(nation);
            int goodwill = faction.GoodwillWith(Faction.OfPlayer);
            Find.Storyteller.incidentQueue.Clear();
            game.treaties.Clear();
            SetGoodwill(faction, 90);
            Spawn(ThingDefOf.Silver, 3000, map);
            int silver = HeirsChains.CountAvailable(ThingDefOf.Silver);
            P.Check("science exchange needs an embassy", HeirsTreaties.HasEmbassy() || (!HeirsTreaties.CanSign(nation, TreatyKind.Science, false, out string why) && why.Length > 0));
            Thing embassy = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Embassy"), map);
            P.Check("embassy counts", HeirsTreaties.HasEmbassy());
            foreach (TreatyKind k in HeirsTreaties.Kinds) HeirsTreaties.Sign(nation, k, false);
            int paid = silver - HeirsChains.CountAvailable(ThingDefOf.Silver);
            P.Check("all four treaties signed", HeirsTreaties.Kinds.All(k => HeirsTreaties.Has(nation, k)), string.Join(",", game.treaties.Select(t => t.kind)));
            P.Check("treaties cost their gifts", paid == HeirsTreaties.Kinds.Sum(HeirsTreaties.Fee), paid.ToString());
            P.Check("a second copy cannot be signed", !HeirsTreaties.Sign(nation, TreatyKind.Peace, true));
            P.Check("high honour with alliance, embassy and goodwill", HeirsTreaties.TitleRank(nation) == 4 && game.honours.Contains(nation) && HeirsTreaties.TitleLabel(nation) == nation.honoraryTitle.CapitalizeFirst(),
                HeirsTreaties.TitleRank(nation) + " " + HeirsTreaties.TitleLabel(nation));

            float k0 = game.Knowledge(nation);
            foreach (Treaty t in game.treaties) t.lastBenefitTick = Find.TickManager.TicksGame - 30 * GenDate.TicksPerDay;
            HeirsTreaties.MonthlyTick(game);
            float gained = game.Knowledge(nation) - k0;
            P.Check("science treaty and honour bring knowledge", gained >= HeirsTreaties.ScienceKnowledge + HeirsTreaties.HonourKnowledge - 0.01f, gained.ToString("F1"));
            P.Check("trade treaty sends a caravan", Queue().Any(q => q.FiringIncident.def == IncidentDefOf.TraderCaravanArrival && q.FiringIncident.parms.faction == faction));

            Faction enemy = Find.FactionManager.AllFactions.FirstOrDefault(f => !f.IsPlayer && f != faction && f.HostileTo(Faction.OfPlayer) && f.def.humanlikeFaction);
            if (enemy != null)
            {
                Treaty alliance = game.treaties.First(t => t.kind == TreatyKind.Alliance);
                NationDef answered = null;
                for (int i = 0; i < 10 && answered == null; i++)
                {
                    alliance.lastBenefitTick = -999999;
                    answered = HeirsTreaties.AnswerRaid(new IncidentParms { target = map, faction = enemy, points = 1000f });
                }
                P.Check("an ally answers a raid", answered == nation && Queue().Any(q => q.FiringIncident.def == IncidentDefOf.RaidFriendly && q.FiringIncident.parms.faction == faction));
                P.Check("an ally does not answer twice in ten days", HeirsTreaties.AnswerRaid(new IncidentParms { target = map, faction = enemy, points = 1000f }) == null);
            }
            Find.Storyteller.incidentQueue.Clear();

            NationDef other = HeirsWorld.LiveNations.FirstOrDefault(n => n != nation && !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer));
            int otherBefore = other == null ? 0 : HeirsPolitics.PlayerGoodwill(other);
            int gw = HeirsPolitics.PlayerGoodwill(nation);
            HeirsTreaties.Cancel(nation, TreatyKind.Trade, true);
            P.Check("cancelling costs goodwill", !HeirsTreaties.Has(nation, TreatyKind.Trade) && HeirsPolitics.PlayerGoodwill(nation) <= gw - HeirsTreaties.CancelPenalty + 1
                && (other == null || HeirsPolitics.PlayerGoodwill(other) < otherBefore), gw + " -> " + HeirsPolitics.PlayerGoodwill(nation));

            SetGoodwill(faction, -90);
            HeirsTreaties.MonthlyTick(game);
            P.Check("a hostile nation voids its treaties", HeirsTreaties.Count(nation) == 0);
            SetGoodwill(faction, 50);
            P.Check("peace treaty can be signed again", HeirsTreaties.Sign(nation, TreatyKind.Peace, true));

            // a ruler's offer
            Find.LetterStack.LettersListForReading.OfType<ChoiceLetter_HeirsPolitics>().ToList().ForEach(l => Find.LetterStack.RemoveLetter(l));
            bool offered = HeirsPolitics.TryTreatyOffer();
            var offer = Find.LetterStack.LettersListForReading.OfType<ChoiceLetter_HeirsPolitics>().FirstOrDefault(l => l.kind == "TreatyOffer");
            P.Check("a ruler offers a treaty", !offered || offer != null);
            if (offer != null)
            {
                HeirsPolitics.Resolve(offer.kind, offer.a, offer.b, offer.amount, 0);
                P.Check("accepting the offer signs it for free", HeirsTreaties.Has(offer.a, (TreatyKind)offer.amount), offer.a.defName + " " + (TreatyKind)offer.amount);
                Find.LetterStack.RemoveLetter(offer);
            }
            savedTreaties = game.treaties.Count;
            embassy.Destroy();
            SetGoodwill(faction, goodwill > -80 ? System.Math.Max(goodwill, 10) : goodwill);
            P.Calm();
        }

        public static void Events()
        {
            Map map = P.Home;
            HeirsGame game = HeirsGame.Get;
            Find.Storyteller.incidentQueue.Clear();
            int letters = Find.LetterStack.LettersListForReading.Count;
            foreach (string kind in HeirsEvents.Kinds)
            {
                P.Check("world event " + kind, HeirsEvents.Try(kind), kind);
            }
            P.Check("world events send letters", Find.LetterStack.LettersListForReading.Count > letters);
            P.Check("a great fair brings caravans", Queue().Count(q => q.FiringIncident.def == IncidentDefOf.TraderCaravanArrival) >= 1);
            Find.Storyteller.incidentQueue.Clear();

            NationDef nation = HeirsWorld.LiveNations.FirstOrDefault(n => !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer));
            if (nation == null) { P.Say("no peaceful nation"); return; }
            Spawn(ThingDefOf.MealSimple, 40, map);
            float food = HeirsEvents.NutritionAvailable();
            int gw = HeirsPolitics.PlayerGoodwill(nation);
            HeirsEvents.Resolve("Famine", nation, 20, null, 0);
            P.Check("famine aid takes the food", food - HeirsEvents.NutritionAvailable() >= 19.9f && HeirsPolitics.PlayerGoodwill(nation) > gw,
                food.ToString("F1") + " -> " + HeirsEvents.NutritionAvailable().ToString("F1"));
            Spawn(ThingDefOf.MedicineHerbal, 20, map);
            int med = HeirsEvents.MedicineAvailable();
            HeirsEvents.Resolve("Plague", nation, 10, null, 0);
            P.Check("plague aid takes the medicine", med - HeirsEvents.MedicineAvailable() == 10, med + " -> " + HeirsEvents.MedicineAvailable());
            P.Check("a plague can travel the roads", HeirsEvents.SpreadPlague(nation) && Find.Storyteller.incidentQueue.Count > 0);
            Find.Storyteller.incidentQueue.Clear();
            Pawn champion = HeirsEvents.Champion(map);
            if (champion != null)
            {
                HeirsEvents.Resolve("Games", nation, 0, champion, 0);
                P.Check("the champion remembers the Games", champion.needs.mood.thoughts.memories.Memories.Any(m => m.def.defName == "HE_GamesVictor" || m.def.defName == "HE_GamesContender"));
                P.Check("win chance follows skill", HeirsEvents.WinChance(champion) >= 0.15f && HeirsEvents.WinChance(champion) <= 0.85f);
            }
            foreach (var l in Find.LetterStack.LettersListForReading.OfType<ChoiceLetter_HeirsEvent>().ToList())
            {
                Find.LetterStack.RemoveLetter(l);
            }
            HeirsMod.Settings.worldEvents = false;
            int before = Find.LetterStack.LettersListForReading.Count;
            for (int i = 0; i < 20; i++) HeirsEvents.MonthlyTick();
            P.Check("world events can be switched off", Find.LetterStack.LettersListForReading.Count == before);
            HeirsMod.Settings.worldEvents = true;
            P.Calm();
        }

        public static void AfterLoad()
        {
            P.Check("treaties saved", HeirsGame.Get.treaties.Count == savedTreaties, HeirsGame.Get.treaties.Count + "/" + savedTreaties);
            P.Check("rulers saved", savedRuler == null || HeirsWorld.Get.reigns.Any(r => r.rulerName == savedRuler), savedRuler);
        }
    }
}
