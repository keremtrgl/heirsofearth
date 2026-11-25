using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>
    /// 3.4 world events between the nations: the Games (hosted by Hellas, or a pious court), a great fair (caravans from several
    /// nations), a famine (a nation asks for food) and a plague (a nation asks for medicine; the sickness can travel the trade roads).
    /// </summary>
    public static class HeirsEvents
    {
        public const float EventChance = 0.35f;
        public const float PlagueSpreadChance = 0.25f;

        public static readonly string[] Kinds = { "Games", "Fair", "Famine", "Plague" };

        private static IEnumerable<NationDef> Peaceful => HeirsWorld.LiveNations.Where(n => !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer));

        public static void MonthlyTick()
        {
            if (!HeirsMod.Settings.worldEvents || Find.AnyPlayerHomeMap == null || !Rand.Chance(EventChance))
            {
                return;
            }
            foreach (string kind in Kinds.InRandomOrder())
            {
                if (Try(kind)) return;
            }
        }

        public static bool Try(string kind)
        {
            switch (kind)
            {
                case "Games": return TryGames();
                case "Fair": return TryFair();
                case "Famine": return TryAsk("Famine", Rand.RangeInclusive(4, 8) * 5);
                case "Plague": return TryAsk("Plague", Rand.RangeInclusive(8, 15));
            }
            return false;
        }

        public static NationDef GamesHost()
        {
            NationDef hellas = DefDatabase<NationDef>.GetNamedSilentFail("HE_Hellas");
            if (hellas != null && Peaceful.Contains(hellas)) return hellas;
            return Peaceful.Where(n => HeirsCourt.Is(n, Temperament.Pious)).RandomElementWithFallback();
        }

        /// <summary>The colonist most likely to win: best at melee or shooting.</summary>
        public static Pawn Champion(Map map)
        {
            return map?.mapPawns.FreeColonistsSpawned.Where(p => !p.Downed && !p.WorkTagIsDisabled(WorkTags.Violent))
                .OrderByDescending(SkillOf).FirstOrDefault();
        }

        public static int SkillOf(Pawn p) => Mathf.Max(p.skills?.GetSkill(SkillDefOf.Melee)?.Level ?? 0, p.skills?.GetSkill(SkillDefOf.Shooting)?.Level ?? 0);

        public static float WinChance(Pawn p) => Mathf.Clamp(0.15f + SkillOf(p) * 0.035f, 0.15f, 0.85f);

        public static bool TryGames()
        {
            NationDef host = GamesHost();
            Pawn champion = Champion(Find.AnyPlayerHomeMap);
            if (host == null || champion == null) return false;
            ChoiceLetter_HeirsEvent letter = Make("Games", host, 0, champion);
            letter.Label = "HE_GamesLabel".Translate(host.LabelCap);
            HeirsMusic.Sting(host);
            letter.Text = "HE_GamesText".Translate(host.LabelCap, HeirsCourt.RulerLine(host), champion.LabelShort, SkillOf(champion), WinChance(champion).ToStringPercent(), champion.Named("PAWN"));
            Find.LetterStack.ReceiveLetter(letter);
            return true;
        }

        public static bool TryFair()
        {
            List<NationDef> peaceful = Peaceful.ToList();
            if (peaceful.Count == 0) return false;
            NationDef host = peaceful.Where(n => HeirsCourt.Is(n, Temperament.Mercantile)).RandomElementWithFallback() ?? peaceful.RandomElement();
            List<NationDef> guests = peaceful.Where(n => n != host).InRandomOrder().Take(2).ToList();
            Map map = Find.AnyPlayerHomeMap;
            int now = Find.TickManager.TicksGame;
            int day = 1;
            foreach (NationDef n in new[] { host }.Concat(guests))
            {
                Find.Storyteller.incidentQueue.Add(IncidentDefOf.TraderCaravanArrival, now + day * GenDate.TicksPerDay,
                    new IncidentParms { target = map, faction = HeirsWorld.FactionOf(n), forced = true });
                day += Rand.RangeInclusive(1, 2);
            }
            string names = new[] { host }.Concat(guests).Select(n => n.LabelCap.Resolve()).ToCommaList(true);
            string text = "HE_FairText".Translate(host.LabelCap, HeirsCourt.RulerLine(host), names);
            HeirsGame.Get?.AddChronicle("HE_FairChronicle".Translate(host.LabelCap), host);
            HeirsMusic.Sting(host);
            Find.LetterStack.ReceiveLetter("HE_FairLabel".Translate(host.LabelCap), text, LetterDefOf.PositiveEvent);
            return true;
        }

        public static bool TryAsk(string kind, int amount)
        {
            NationDef nation = Peaceful.Where(n => HeirsPolitics.PlayerGoodwill(n) > -50).RandomElementWithFallback();
            if (nation == null) return false;
            ChoiceLetter_HeirsEvent letter = Make(kind, nation, amount, null);
            letter.Label = ("HE_" + kind + "Label").Translate(nation.LabelCap);
            letter.Text = ("HE_" + kind + "Text").Translate(nation.LabelCap, HeirsCourt.RulerLine(nation), amount);
            Find.LetterStack.ReceiveLetter(letter);
            return true;
        }

        private static ChoiceLetter_HeirsEvent Make(string kind, NationDef nation, int amount, Pawn pawn)
        {
            var letter = (ChoiceLetter_HeirsEvent)LetterMaker.MakeLetter(DefDatabase<LetterDef>.GetNamed("HE_EventLetter"));
            letter.kind = kind;
            letter.nation = nation;
            letter.amount = amount;
            letter.pawn = pawn;
            return letter;
        }

        // ------------------------------------------------------------------ food and medicine in the colony
        private static IEnumerable<Thing> Food(Map map) => map.listerThings.ThingsInGroup(ThingRequestGroup.FoodSourceNotPlantOrTree)
            .Where(t => t.Spawned && !t.IsForbidden(Faction.OfPlayer) && t.def.IsNutritionGivingIngestible && t.def.ingestible.HumanEdible
                        && !t.def.IsCorpse && !t.def.IsDrug && t.def.ingestible.preferability >= FoodPreferability.RawBad && !(t is Pawn));

        private static IEnumerable<Thing> Medicine(Map map) => map.listerThings.ThingsInGroup(ThingRequestGroup.Medicine)
            .Where(t => t.Spawned && !t.IsForbidden(Faction.OfPlayer));

        private static IEnumerable<Map> Homes => Find.Maps.Where(m => m.IsPlayerHome);

        public static float NutritionAvailable() => Homes.SelectMany(Food).Sum(t => t.GetStatValue(StatDefOf.Nutrition) * t.stackCount);

        public static int MedicineAvailable() => Homes.SelectMany(Medicine).Sum(t => t.stackCount);

        /// <summary>Takes food worth the nutrition asked for, cheapest food first.</summary>
        public static void TakeNutrition(float nutrition)
        {
            foreach (Thing t in Homes.SelectMany(Food).OrderBy(x => x.MarketValue / Mathf.Max(0.01f, x.GetStatValue(StatDefOf.Nutrition))).ToList())
            {
                if (nutrition <= 0.001f) break;
                float each = t.GetStatValue(StatDefOf.Nutrition);
                if (each <= 0f) continue;
                int count = Mathf.Min(t.stackCount, Mathf.CeilToInt(nutrition / each));
                nutrition -= count * each;
                t.SplitOff(count).Destroy();
            }
        }

        /// <summary>Takes medicine, simplest kind first.</summary>
        public static void TakeMedicine(int count)
        {
            foreach (Thing t in Homes.SelectMany(Medicine).OrderBy(x => x.GetStatValue(StatDefOf.MedicalPotency)).ToList())
            {
                if (count <= 0) break;
                int n = Mathf.Min(t.stackCount, count);
                count -= n;
                t.SplitOff(n).Destroy();
            }
        }

        public static bool CanGive(string kind, int amount) => kind == "Famine" ? NutritionAvailable() >= amount : kind != "Plague" || MedicineAvailable() >= amount;

        /// <summary>Applies the answer to an event letter. option 0 = accept, 1 = refuse. Returns a line for the result message.</summary>
        public static string Resolve(string kind, NationDef nation, int amount, Pawn pawn, int option)
        {
            HeirsGame game = HeirsGame.Get;
            bool accept = option == 0;
            switch (kind)
            {
                case "Games":
                    if (!accept || pawn == null || pawn.Dead)
                    {
                        HeirsPolitics.Affect(nation, -3);
                        return null;
                    }
                    bool won = Rand.Chance(WinChance(pawn));
                    Thought(pawn, won ? "HE_GamesVictor" : "HE_GamesContender");
                    if (won)
                    {
                        foreach (NationDef n in Peaceful) HeirsPolitics.Affect(n, n == nation ? 15 : 6);
                        game?.AddKnowledge(nation, 20f, null);
                        string text = "HE_GamesWon".Translate(pawn.LabelShort, nation.LabelCap, pawn.Named("PAWN"));
                        game?.AddChronicle(text, nation);
                        Find.LetterStack.ReceiveLetter("HE_GamesWonLabel".Translate(pawn.LabelShort), text, LetterDefOf.PositiveEvent, pawn);
                        HeirsMusic.Play(nation);
                        return text;
                    }
                    HeirsPolitics.Affect(nation, 5);
                    Messages.Message("HE_GamesLost".Translate(pawn.LabelShort, nation.LabelCap, pawn.Named("PAWN")), pawn, MessageTypeDefOf.NeutralEvent, false);
                    return null;
                case "Famine":
                    if (accept && NutritionAvailable() >= amount)
                    {
                        TakeNutrition(amount);
                        HeirsPolitics.Affect(nation, 20);
                        game?.AddKnowledge(nation, 10f, null);
                        game?.AddChronicle("HE_FamineHelped".Translate(nation.LabelCap), nation);
                        HeirsAges.Setback(nation, true);
                    }
                    else
                    {
                        HeirsPolitics.Affect(nation, -5);
                        HeirsAges.Setback(nation, false);
                    }
                    return null;
                case "Plague":
                    if (accept && MedicineAvailable() >= amount)
                    {
                        TakeMedicine(amount);
                        HeirsPolitics.Affect(nation, 20);
                        game?.AddKnowledge(nation, 10f, null);
                        game?.AddChronicle("HE_PlagueHelped".Translate(nation.LabelCap), nation);
                        HeirsAges.Setback(nation, true);
                    }
                    else
                    {
                        HeirsPolitics.Affect(nation, -5);
                        HeirsAges.Setback(nation, false);
                    }
                    if (Linked(nation) && Rand.Chance(PlagueSpreadChance))
                    {
                        SpreadPlague(nation);
                    }
                    return null;
            }
            return null;
        }

        /// <summary>Trade treaties and open trade roads carry goods, and sometimes sickness.</summary>
        public static bool Linked(NationDef nation) => HeirsTreaties.Has(nation, TreatyKind.Trade) || (HeirsGame.Get?.routes.Any(r => r.nation == nation) ?? false);

        public static bool SpreadPlague(NationDef nation)
        {
            Map map = Find.AnyPlayerHomeMap;
            IncidentDef flu = DefDatabase<IncidentDef>.GetNamedSilentFail("Disease_Flu");
            if (map == null || flu == null) return false;
            Find.Storyteller.incidentQueue.Add(flu, Find.TickManager.TicksGame + Rand.RangeInclusive(2, 5) * GenDate.TicksPerDay,
                new IncidentParms { target = map, forced = true });
            Messages.Message("HE_PlagueSpreads".Translate(nation.LabelCap), MessageTypeDefOf.ThreatSmall, false);
            return true;
        }

        private static void Thought(Pawn pawn, string defName)
        {
            ThoughtDef def = DefDatabase<ThoughtDef>.GetNamedSilentFail(defName);
            if (def != null) pawn.needs?.mood?.thoughts?.memories?.TryGainMemory(def);
        }
    }

    public class ChoiceLetter_HeirsEvent : ChoiceLetter
    {
        public string kind;
        public NationDef nation;
        public int amount;
        public Pawn pawn;
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
                    var dia = new DiaOption(("HE_" + kind + (i == 0 ? "Accept" : "Refuse")).Translate(amount, pawn?.LabelShort ?? ""))
                    {
                        action = () =>
                        {
                            resolved = true;
                            HeirsEvents.Resolve(kind, nation, amount, pawn, option);
                            Find.LetterStack.RemoveLetter(this);
                        },
                        resolveTree = true
                    };
                    if (i == 0 && !HeirsEvents.CanGive(kind, amount))
                    {
                        dia.Disable(("HE_" + kind + "Missing").Translate(amount));
                    }
                    if (i == 0 && kind == "Games" && (pawn == null || pawn.Dead || pawn.Downed))
                    {
                        dia.Disable("HE_GamesNoChampion".Translate());
                    }
                    yield return dia;
                }
            }
        }

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Values.Look(ref kind, "kind");
            Scribe_Defs.Look(ref nation, "nation");
            Scribe_Values.Look(ref amount, "amount");
            Scribe_References.Look(ref pawn, "pawn");
            Scribe_Values.Look(ref resolved, "resolved");
        }
    }
}
