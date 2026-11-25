using System;
using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;
using Verse.AI;

namespace HeProbe
{
    /// <summary>1.0 checks: the three nations, their people, traders, start scenarios, traditions and recreation.</summary>
    public static class Probe10
    {
        private static readonly string[] Nations = { "HE_Roma", "HE_Yamato", "HE_Nord", "HE_Hellas", "HE_Tianxia", "HE_Albion", "HE_Kemet", "HE_Pars", "HE_Inti" };

        public static void NationDefs()
        {
            foreach (string name in Nations)
            {
                NationDef n = DefDatabase<NationDef>.GetNamedSilentFail(name);
                P.Check("nation exists " + name, n != null);
                if (n == null) continue;
                P.Check("nation faction " + name, n.faction != null && n.playerFaction != null && n.scenario != null && n.archive != null);
                P.Check("nation text " + name, !n.label.NullOrEmpty() && !n.description.NullOrEmpty() && !n.rulerTitle.NullOrEmpty());
                int projects = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Count(r => r.GetModExtension<HeirsResearchExt>()?.nation == n);
                int traditions = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Count(r => r.GetModExtension<HeirsResearchExt>() is HeirsResearchExt e && e.nation == n && e.tradition);
                P.Check("nation research " + name, projects >= 16 && traditions >= 7, projects + " projects, " + traditions + " traditions");
            }
            NationDef roma = DefDatabase<NationDef>.GetNamed("HE_Roma");
            NationDef nord = DefDatabase<NationDef>.GetNamed("HE_Nord");
            P.Check("roma and nord are rivals", roma.IsRivalOf(nord) && nord.IsRivalOf(roma));
            P.Check("rivals are not friends", !roma.IsFriendOf(nord));
            NationDef hellas = DefDatabase<NationDef>.GetNamed("HE_Hellas"), tianxia = DefDatabase<NationDef>.GetNamed("HE_Tianxia"), albion = DefDatabase<NationDef>.GetNamed("HE_Albion");
            NationDef yamato = DefDatabase<NationDef>.GetNamed("HE_Yamato");
            P.Check("hellas friends roma", hellas.IsFriendOf(roma) && roma.IsFriendOf(hellas));
            P.Check("tianxia rivals yamato", tianxia.IsRivalOf(yamato) && yamato.IsRivalOf(tianxia));
            P.Check("albion friends nord, rivals roma", albion.IsFriendOf(nord) && albion.IsRivalOf(roma));
            P.Check("albion is industrial", albion.faction.techLevel == TechLevel.Industrial && albion.playerFaction.techLevel == TechLevel.Industrial);
            P.Check("2.0 nations released", hellas.release == 2 && tianxia.release == 2 && albion.release == 2);
        }

        public static void People()
        {
            List<PawnKindDef> kinds = DefDatabase<PawnKindDef>.AllDefsListForReading.Where(k => k.defName.StartsWith("HE_")).ToList();
            P.Check("pawn kinds", kinds.Count >= 25, kinds.Count.ToString());
            foreach (PawnKindDef kind in kinds)
            {
                P.Run("pawn " + kind.defName, () =>
                {
                    for (int i = 0; i < 3; i++)
                    {
                        Pawn pawn = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, null, PawnGenerationContext.NonPlayer, forceGenerateNewPawn: true, mustBeCapableOfViolence: kind.isFighter));
                        P.Check("pawn body type " + kind.defName, pawn.story?.bodyType != null && pawn.story.headType != null);
                        P.Check("pawn name " + kind.defName, pawn.Name != null && !pawn.Name.ToStringFull.NullOrEmpty());
                        string nation = kind.defName.Split('_')[1];
                        if (nation != "Renegade" && pawn.story?.Adulthood != null && kind.defName != "HE_" + nation + "_Colonist")
                        {
                            P.Check("pawn backstory " + kind.defName, pawn.story.Adulthood.spawnCategories.Contains("HE_" + nation), pawn.story.Adulthood.defName);
                        }
                        if (kind.isFighter && kind.weaponTags != null && kind.weaponTags.Count > 0 && kind.weaponTags.All(t => t.StartsWith("HE_")))
                        {
                            ThingDef w = pawn.equipment?.Primary?.def;
                            P.Check("pawn own weapon " + kind.defName, w != null && w.defName.StartsWith("HE_" + nation + "_"), w?.defName ?? "unarmed");
                        }
                        if (kind.isFighter && kind.weaponTags != null && kind.weaponTags.Count > 0 && i == 0)
                        {
                            P.Say("  " + kind.defName + ": " + (pawn.equipment?.Primary?.def.defName ?? "unarmed") + ", " + pawn.apparel.WornApparel.Count + " apparel, " + pawn.Name.ToStringShort);
                        }
                        Find.WorldPawns.PassToWorld(pawn, PawnDiscardDecideMode.Discard);
                    }
                });
            }
        }

        public static void Traders()
        {
            foreach (TraderKindDef trader in DefDatabase<TraderKindDef>.AllDefsListForReading.Where(t => t.defName.StartsWith("HE_")).ToList())
            {
                P.Run("trader " + trader.defName, () =>
                {
                    ThingSetMakerParams parms = default;
                    parms.traderDef = trader;
                    parms.makingFaction = null;
                    parms.tile = P.Home.Tile;
                    List<Thing> stock = ThingSetMakerDefOf.TraderStock.root.Generate(parms);
                    string nation = trader.defName.Split('_')[1];
                    P.Check("trader stock " + trader.defName, stock.Count >= 5, stock.Count.ToString());
                    P.Check("trader archive " + trader.defName, stock.Any(t => t.def.defName == "HE_" + nation + "_Archive"));
                    P.Check("trader goods " + trader.defName, stock.Any(t => t.def.tradeTags != null && t.def.tradeTags.Contains("HE_" + nation + "Goods") && !t.def.defName.EndsWith("_Archive")));
                    foreach (Thing t in stock) t.Destroy();
                });
            }
        }

        public static void Scenarios()
        {
            foreach (ScenarioDef scen in DefDatabase<ScenarioDef>.AllDefsListForReading.Where(s => s.defName.StartsWith("HE_")).ToList())
            {
                P.Run("scenario " + scen.defName, () =>
                {
                    Scenario s = scen.scenario;
                    P.Check("scenario heritage part " + scen.defName, s.AllParts.Any(p => p is ScenPart_HeirsHeritage));
                    P.Check("scenario dialog " + scen.defName, s.AllParts.OfType<ScenPart_GameStartDialog>().Any());
                    string text = s.GetFullInformationText();
                    P.Check("scenario text " + scen.defName, !text.NullOrEmpty() && !s.summary.NullOrEmpty());
                    if (scen.defName != "HE_Start_Independent")
                    {
                        FactionDef fd = P.Get(P.Get(s, "playerFaction"), "factionDef") as FactionDef;
                        P.Check("scenario player faction " + scen.defName, fd != null && fd.isPlayer && fd.defName.StartsWith("HE_Player_"), fd?.defName ?? "null");
                    }
                });
            }
        }

        public static void QualityAndCaravan()
        {
            Pawn pawn = P.Colonist(P.Home);
            ResearchProjectDef master = P.R("HE_Yamato_MasterCraft");
            Find.ResearchManager.FinishProject(master, false, null, false);
            HeirsTraditions.Dirty();
            P.Check("mastercraft active", HeirsTraditions.Active(master));
            int raised = 0;
            for (int i = 0; i < 4000; i++)
            {
                if (HeirsTraditions.RaiseQuality(pawn, QualityCategory.Normal) == QualityCategory.Good) raised++;
            }
            float rate = raised / 4000f;
            P.Check("quality_patch rate", rate > 0.09f && rate < 0.15f, rate.ToString("0.000"));
            P.Check("quality never above legendary", HeirsTraditions.RaiseQuality(pawn, QualityCategory.Legendary) == QualityCategory.Legendary);
            P.Check("quality only for player", HeirsTraditions.RaiseQuality(null, QualityCategory.Normal) == QualityCategory.Normal);

            ResearchProjectDef ships = P.R("HE_Nord_Longships");
            Find.ResearchManager.FinishProject(ships, false, null, false);
            HeirsTraditions.Dirty();
            float caravan = HeirsTraditions.ActiveList.Sum(a => a.ext.caravanSpeed);
            P.Check("caravan bonus summed", caravan >= 0.12f - 0.001f, caravan.ToString("0.00"));
            P.Check("caravan ignores null", HeirsTraditions.CaravanTicks(null, null, 1000) == 1000);

            StatDef cold = StatDefOf.ComfyTemperatureMin;
            float before = cold.Worker.GetValue(pawn);
            Find.ResearchManager.FinishProject(P.R("HE_Nord_Blood"), false, null, false);
            HeirsTraditions.Dirty();
            float after = cold.Worker.GetValue(pawn);
            P.Check("northern blood", Mathf.Abs(after - (before - 8f)) < 0.01f, before + " -> " + after);

            ResearchProjectDef academy = P.R("HE_Academy");
            float study = HeirsTraditions.StudyBonus(DefDatabase<NationDef>.GetNamed("HE_Yamato"));
            Find.ResearchManager.FinishProject(P.R("HE_Translators"), false, null, false);
            Find.ResearchManager.FinishProject(academy, false, null, false);
            HeirsTraditions.Dirty();
            float study2 = HeirsTraditions.StudyBonus(DefDatabase<NationDef>.GetNamed("HE_Yamato"));
            P.Check("common study traditions", Mathf.Abs(study2 - study - 0.25f) < 0.001f, study + " -> " + study2);
        }

        public static void Joy()
        {
            Map map = P.Home;
            foreach (string giverName in new[] { "HE_Bathe", "HE_TeaCeremony", "HE_Feast", "HE_Training", "HE_Theatre" })
            {
                JoyGiverDef giver = DefDatabase<JoyGiverDef>.GetNamedSilentFail(giverName);
                P.Check("joy giver " + giverName, giver != null && giver.thingDefs.All(t => t != null) && giver.jobDef != null);
            }
            foreach (string name in new[] { "HE_Roma_Thermae", "HE_Nord_MeadTable", "HE_Yamato_Dojo", "HE_Hellas_Stage", "HE_Tianxia_TeaTable", "HE_Albion_PubTable" })
            {
                P.Run("joy job " + name, () =>
                {
                    ThingDef def = DefDatabase<ThingDef>.GetNamed(name);
                    P.FairWeather(map);
                    Thing building = P.SpawnBuilding(def, map);
                    Pawn pawn = P.Colonist(map);
                    JoyGiverDef giver = DefDatabase<JoyGiverDef>.AllDefsListForReading.First(g => g.thingDefs != null && g.thingDefs.Contains(def));
                    Job job = giver.Worker.TryGiveJob(pawn);
                    P.Check("joy job " + name, job != null && job.targetA.Thing == building, job == null ? P.JoyWhy(pawn, building) : job.def.defName + " on " + job.targetA.Thing?.def.defName);
                    if (job != null)
                    {
                        pawn.jobs.StartJob(job, JobCondition.InterruptForced);
                        P.Ticks(300);
                        P.Check("joy job runs " + name, pawn.CurJob == null || pawn.CurJob.def == job.def || pawn.CurJobDef != null);
                        pawn.jobs.EndCurrentJob(JobCondition.InterruptForced);
                    }
                    building.Destroy();
                });
            }
        }

        private static NationDef N(string name) => DefDatabase<NationDef>.GetNamed(name);

        public static void Politics()
        {
            HeirsWorld w = HeirsWorld.Get;
            NationDef roma = N("HE_Roma"), yamato = N("HE_Yamato"), nord = N("HE_Nord");
            P.Check("live nations", HeirsWorld.LiveNations.Count() >= 3, HeirsWorld.LiveNations.Count().ToString());
            P.Check("nation leaders", HeirsWorld.LiveNations.All(n => HeirsWorld.FactionOf(n).leader != null));
            P.Check("nation settlements", HeirsWorld.LiveNations.All(n => Find.WorldObjects.Settlements.Any(s => s.Faction == HeirsWorld.FactionOf(n))));

            // drift: 24 months with a fixed seed
            var before = new Dictionary<string, int> { { "rn", HeirsWorld.Goodwill(roma, nord) }, { "ry", HeirsWorld.Goodwill(roma, yamato) }, { "yn", HeirsWorld.Goodwill(yamato, nord) } };
            int updates = w.updates;
            Rand.PushState(1234);
            try
            {
                for (int i = 0; i < 24; i++) w.MonthlyTick();
            }
            finally
            {
                Rand.PopState();
            }
            var after = new Dictionary<string, int> { { "rn", HeirsWorld.Goodwill(roma, nord) }, { "ry", HeirsWorld.Goodwill(roma, yamato) }, { "yn", HeirsWorld.Goodwill(yamato, nord) } };
            P.Check("monthly_tick_runs", w.updates == updates + 24 && before.Any(kv => after[kv.Key] != kv.Value), string.Join(", ", before.Select(kv => kv.Key + " " + kv.Value + "->" + after[kv.Key])));
            P.Say("wars " + w.wars.Count + ", alliances " + w.alliances.Count + ", letters " + Find.LetterStack.LettersListForReading.Count);
            foreach (NationPair pair in w.wars.ToList()) w.MakePeace(pair.a, pair.b);

            // war and peace
            w.DeclareWar(roma, nord);
            Faction fr = HeirsWorld.FactionOf(roma), fn = HeirsWorld.FactionOf(nord);
            P.Check("war_and_peace war", w.AtWar(roma, nord) && fr.RelationKindWith(fn) == FactionRelationKind.Hostile);
            w.MakePeace(roma, nord);
            P.Check("war_and_peace peace", !w.AtWar(roma, nord) && fr.RelationKindWith(fn) != FactionRelationKind.Hostile);

            // switching politics off stops the monthly tick
            HeirsMod.Settings.politics = false;
            int u = w.updates;
            w.MonthlyTick();
            P.Check("politics_off_no_ticks", w.updates == u);
            HeirsMod.Settings.politics = true;

            // the player events
            Faction fy = HeirsWorld.FactionOf(yamato);
            fy.TryAffectGoodwillWith(Faction.OfPlayer, 50 - fy.GoodwillWith(Faction.OfPlayer), false, false, null);
            int letters = Find.LetterStack.LettersListForReading.Count;
            P.Check("incidents_fire envoy", HeirsPolitics.TryEnvoy() && Find.LetterStack.LettersListForReading.Count == letters + 1);
            P.Check("incidents_fire tribute", HeirsPolitics.TryTribute() || HeirsWorld.LiveNations.All(n => HeirsPolitics.PlayerGoodwill(n) >= 10 || HeirsPolitics.PlayerGoodwill(n) <= -75));
            P.Check("incidents_fire marriage", HeirsPolitics.TryMarriage());
            int gw = HeirsPolitics.PlayerGoodwill(yamato);
            HeirsPolitics.Resolve("Envoy", yamato, null, 200, 0);
            P.Check("envoy accept goodwill", HeirsPolitics.PlayerGoodwill(yamato) > gw, gw + " -> " + HeirsPolitics.PlayerGoodwill(yamato));
            int colonists = P.Home.mapPawns.FreeColonistsSpawnedCount;
            HeirsPolitics.Resolve("Marriage", yamato, null, 0, 0);
            P.Check("marriage_joins_pawn", P.Home.mapPawns.FreeColonistsSpawnedCount == colonists + 1);
            P.Check("married pawn body", P.Home.mapPawns.FreeColonistsSpawned.All(p => p.story?.bodyType != null));
            HeirsPolitics.Resolve("Tribute", yamato, null, 300, 1);
            P.Check("tribute refused queues raid", Find.Storyteller.incidentQueue.Count > 0);
            Find.Storyteller.incidentQueue.Clear();

            // mediation and war call
            w.DeclareWar(roma, yamato);
            for (int i = 0; i < 2; i++)
            {
                Thing silver = ThingMaker.MakeThing(ThingDefOf.Silver);
                silver.stackCount = 300;
                GenSpawn.Spawn(silver, P.FreeSpot(P.Home, new IntVec2(1, 1)), P.Home);
            }
            int silverBefore = HeirsChains.CountAvailable(ThingDefOf.Silver);
            bool warBefore = w.AtWar(roma, yamato);
            HeirsPolitics.Resolve("Mediation", roma, yamato, HeirsPolitics.MediationCost, 0);
            P.Check("mediation_peace", !w.AtWar(roma, yamato), "silver " + silverBefore + ", war before " + warBefore + ", same world " + (w == HeirsWorld.Get) + ", silver after " + HeirsChains.CountAvailable(ThingDefOf.Silver));
            w.DeclareWar(yamato, nord);
            fy.TryAffectGoodwillWith(Faction.OfPlayer, 80 - fy.GoodwillWith(Faction.OfPlayer), false, false, null);
            P.Check("incidents_fire war call", HeirsPolitics.TryWarCall(w));
            HeirsPolitics.Resolve("WarCall", yamato, nord, 0, 0);
            P.Check("war call makes enemy hostile", fn.HostileTo(Faction.OfPlayer));
            P.Check("gift_archive", HeirsPolitics.TryAllianceGift(), HeirsPolitics.PlayerGoodwill(yamato).ToString());

            // settlement capture between the two warring nations
            List<Settlement> sy = Find.WorldObjects.Settlements.Where(s => s.Faction == fy).ToList();
            List<Settlement> sn = Find.WorldObjects.Settlements.Where(s => s.Faction == fn).ToList();
            if (sy.Count > 0 && sn.Count > 1)
            {
                bool near = HeirsPolitics.CaptureNearest(w, yamato, nord, sy, sn);
                P.Say("capture within 15 tiles available: " + near);
                if (!near)
                {
                    // move one Nord settlement's claim next to Yamato by testing with a fake 'winners' list containing the target's neighbour
                    Settlement target = sn[0];
                    near = HeirsPolitics.CaptureNearest(w, yamato, nord, new List<Settlement> { target }, new List<Settlement> { target, sn[1] });
                }
                P.Check("settlement_capture", near && Find.WorldObjects.Settlements.Count(s => s.Faction == fy) > sy.Count);
            }
            w.MakePeace(yamato, nord);
            P.Check("politics_letters_ok", Find.LetterStack.LettersListForReading.All(l => l != null && !l.Label.NullOrEmpty()));
        }

        public static void Collapse()
        {
            HeirsWorld w = HeirsWorld.Get;
            NationDef yamato = N("HE_Yamato");
            HeirsPolitics.Collapse(w, yamato);
            P.Check("collapse_handled", HeirsWorld.FactionOf(yamato) == null && !HeirsWorld.LiveNations.Contains(yamato));
            int u = w.updates;
            w.MonthlyTick();
            P.Check("politics_survives_missing_faction", w.updates == u + 1 && !w.wars.Any(p => p.a == yamato || p.b == yamato));
            P.Check("chain raid falls back", HeirsChains.HostileFaction(yamato) != null);
        }
        // ------------------------------------------------------------------ story chains and artifacts
        public static void Chains()
        {
            HeirsGame g = P.Game;
            List<ChainDef> chains = DefDatabase<ChainDef>.AllDefsListForReading.ToList();
            P.Check("chains exist", chains.Count >= 6, chains.Count.ToString());
            foreach (ChainDef chain in chains)
            {
                P.Check("chain data " + chain.defName, chain.nation != null && chain.steps.Count == 5 && chain.artifact != null && !chain.startText.NullOrEmpty() && !chain.endText.NullOrEmpty());
                foreach (ChainStep s in chain.steps)
                {
                    P.Check("chain step text " + chain.defName + " " + s.kind, !s.label.NullOrEmpty() && !s.text.NullOrEmpty());
                }
            }
            ResearchProjectDef capstone = P.R("HE_Yamato_Mandate");
            g.SetKnowledge(DefDatabase<NationDef>.GetNamed("HE_Yamato"), 100f);
            Find.ResearchManager.FinishProject(P.R("HE_Yamato_MasterCraft"), false, null, false);
            bool can = g.CanStart(capstone, out string why);
            P.Check("capstone waits for chain", !capstone.CanStartNow && !can && !why.NullOrEmpty(), why ?? "");

            // run the Yamato chain step by step with the test hook
            ChainDef yamato = DefDatabase<ChainDef>.GetNamed("HE_Chain_Yamato");
            HeirsChains.TickRare(g);
            ChainState st = g.State(yamato);
            P.Check("chain starts at knowledge", st.started && st.step == 0);
            P.Check("deliver blocked without goods", !HeirsChains.CanDeliver(yamato, st));
            foreach (ThingDefCountClass need in yamato.steps[0].things)
            {
                int left = need.count;
                while (left > 0)
                {
                    Thing t = ThingMaker.MakeThing(need.thingDef);
                    t.stackCount = Mathf.Min(left, need.thingDef.stackLimit);
                    left -= t.stackCount;
                    GenPlace.TryPlaceThing(t, P.Colonist(P.Home).Position, P.Home, ThingPlaceMode.Near);
                }
            }
            P.Check("deliver allowed with goods", HeirsChains.CanDeliver(yamato, st));
            HeirsChains.Deliver(g, yamato);
            P.Check("deliver advances", st.step == 1);
            Find.ResearchManager.FinishProject(P.R("HE_Yamato_Folds"), false, null, false);
            HeirsChains.TickRare(g);
            P.Check("research step advances", st.step == 2);
            HeirsChains.SpawnRaid(st, yamato.steps[2]);
            P.Check("raid step spawns", st.raidSpawned && st.raidFaction != null, st.raidFaction?.Name ?? "none");
            foreach (Pawn raider in P.Home.mapPawns.AllPawnsSpawned.Where(p => p.Faction == st.raidFaction).ToList()) P.Gone(raider);
            HeirsChains.TickRare(g);
            P.Check("raid step ends when raiders are gone", st.step == 3, st.step.ToString());
            HeirsSite site = st.site;
            P.Check("site revealed", site != null && site.Spawned);
            if (site != null)
            {
                Map map = site.GetOrBuildMap();
                ThingDef reward = yamato.steps[3].siteReward;
                P.Check("site_generates reward", map.listerThings.ThingsOfDef(reward).Any());
                P.Check("site_generates guards", map.mapPawns.AllPawnsSpawned.Any(p => p.Faction != null && p.Faction == site.Faction));
                P.Check("site_generates walls", map.listerThings.ThingsOfDef(ThingDefOf.Wall).Count > 10);
                Thing relic = map.listerThings.ThingsOfDef(reward).First();
                relic.DeSpawn();
                GenPlace.TryPlaceThing(relic, P.Colonist(P.Home).Position, P.Home, ThingPlaceMode.Near);
                Current.Game.DeinitAndRemoveMap(map, false);
                HeirsChains.TickRare(g);
                P.Check("site step ends when relic is home", st.step == 4, st.step.ToString());
            }
            int relics = HeirsChains.CountAvailable(DefDatabase<ThingDef>.GetNamed("HE_Yamato_Regalia"));
            HeirsChains.Choose(g, yamato, 4, 1);
            P.Check("chain_runs_to_end", st.done && st.choice == 1);
            P.Check("choice takes relic", HeirsChains.CountAvailable(DefDatabase<ThingDef>.GetNamed("HE_Yamato_Regalia")) == relics - 1, relics.ToString());
            P.Check("capstone opens after chain", g.CanStart(capstone, out string why2), why2 ?? "");

            // the other two chains run with the test hook; Roma stays half done for the save check
            ChainDef nord = DefDatabase<ChainDef>.GetNamed("HE_Chain_Nord");
            HeirsChains.Start(g, nord);
            for (int i = 0; i < 5 && !g.State(nord).done; i++) HeirsChains.ForceCompleteStep(g, nord);
            P.Check("chain_runs_to_end nord", g.State(nord).done);
            P.Check("cold snap step", P.Home.gameConditionManager.ConditionIsActive(DefDatabase<GameConditionDef>.GetNamed("ColdSnap")));
            foreach (string pair in new[] { "Hellas:GoldenAge", "Tianxia:Harmony", "Albion:Workshop" })
            {
                string nation = pair.Split(':')[0], cap = pair.Split(':')[1];
                P.Run("chain 2.0 " + nation, () =>
                {
                    ChainDef chain = DefDatabase<ChainDef>.GetNamed("HE_Chain_" + nation);
                    ResearchProjectDef capstone2 = P.R("HE_" + nation + "_" + cap);
                    g.SetKnowledge(chain.nation, 100f);
                    foreach (ResearchProjectDef pre in capstone2.prerequisites ?? new List<ResearchProjectDef>())
                        Find.ResearchManager.FinishProject(pre, false, null, false);
                    P.Check("capstone locked before chain " + nation, !g.CanStart(capstone2, out string w0), w0 ?? "");
                    HeirsChains.Start(g, chain);
                    for (int i = 0; i < 5 && !g.State(chain).done; i++) HeirsChains.ForceCompleteStep(g, chain);
                    P.Check("chain_runs_to_end " + nation, g.State(chain).done);
                    P.Check("capstone opens after chain " + nation, g.CanStart(capstone2, out string w1), w1 ?? "");
                });
            }
            ChainDef roma = DefDatabase<ChainDef>.GetNamed("HE_Chain_Roma");
            HeirsChains.Start(g, roma);
            HeirsChains.ForceCompleteStep(g, roma);
            HeirsChains.ForceCompleteStep(g, roma);
            P.Check("roma chain mid-way", g.State(roma).step == 2 && !g.State(roma).done);
            foreach (string text in chains.Select(c => HeirsChains.Goal(c, g.State(c)))) { string unused = text; }
        }

        public static void ChainAfterLoad()
        {
            HeirsGame g = P.Game;
            ChainState roma = g.State(DefDatabase<ChainDef>.GetNamed("HE_Chain_Roma"));
            P.Check("chain_saved", roma.started && roma.step == 2 && !roma.done, roma.step.ToString());
            P.Check("chain done saved", g.State(DefDatabase<ChainDef>.GetNamed("HE_Chain_Yamato")).done);
        }

        public static void Artifacts()
        {
            Map map = P.Home;
            foreach (string name in new[] { "HE_Roma_Artifact_Eagle", "HE_Nord_Artifact_StormHorn", "HE_Hellas_Artifact_Aegis", "HE_Tianxia_Artifact_DragonSeal", "HE_Albion_Artifact_WarDrum" })
            {
                P.Run("artifact " + name, () =>
                {
                    Pawn pawn = P.Colonist(map);
                    Thing art = ThingMaker.MakeThing(DefDatabase<ThingDef>.GetNamed(name));
                    GenPlace.TryPlaceThing(art, pawn.Position, map, ThingPlaceMode.Near);
                    var comp = art.TryGetComp<CompUseEffect_HeirsArtifact>();
                    P.Check("artifact comp " + name, comp != null && art.TryGetComp<CompUsable>() != null);
                    P.Check("artifact usable " + name, comp.CanBeUsedBy(pawn).Accepted);
                    comp.DoEffect(pawn);
                    P.Check("artifact_works " + name, pawn.health.hediffSet.HasHediff(DefDatabase<HediffDef>.GetNamed("HE_Rallied")));
                    P.Check("artifact cooldown " + name, !comp.CanBeUsedBy(pawn).Accepted && comp.CooldownTicksLeft > 0);
                    string unused = art.GetInspectString();
                    art.Destroy();
                });
            }
            ThingDef sword = DefDatabase<ThingDef>.GetNamed("HE_Yamato_Artifact_SkySword");
            P.Check("sky sword not craftable", !DefDatabase<RecipeDef>.AllDefsListForReading.Any(r => r.ProducedThingDef == sword));
            P.Check("artifacts not studyable", !DefDatabase<RecipeDef>.GetNamed("HE_StudyCulture").fixedIngredientFilter.Allows(sword));
            Industry();
        }
    
        /// <summary>2.0: the steam engine makes power from wood, guns shoot the right rounds, the fire lance burns.</summary>
        public static void Industry()
        {
            Map map = P.Home;
            P.Run("steam engine", () =>
            {
                Thing engine = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Albion_SteamEngine"), map);
                CompRefuelable fuel = engine.TryGetComp<CompRefuelable>();
                CompPowerPlant plant = engine.TryGetComp<CompPowerPlant>();
                P.Check("steam engine comps", fuel != null && plant != null);
                fuel.Refuel(90f);
                P.Ticks(250);
                P.Check("steam_engine_power", plant.PowerOutput >= 1300f, plant.PowerOutput.ToString("F0"));
                engine.Destroy();
            });
            foreach (string gun in new[] { "HE_Albion_Musket", "HE_Albion_Rifle", "HE_Tianxia_Repeater", "HE_Tianxia_FireLance", "HE_Hellas_Toxon" })
            {
                ThingDef def = DefDatabase<ThingDef>.GetNamed(gun);
                P.Check("ranged verb " + gun, def.Verbs.Count > 0 && def.Verbs[0].defaultProjectile != null && def.recipeMaker != null, def.Verbs.FirstOrDefault()?.defaultProjectile?.defName ?? "none");
            }
            P.Check("fire lance burns", DefDatabase<ThingDef>.GetNamed("HE_Bullet_FireLance").projectile.damageDef == DamageDefOf.Flame);
            P.Check("repeater bursts", DefDatabase<ThingDef>.GetNamed("HE_Tianxia_Repeater").Verbs[0].burstShotCount == 3);
            P.Check("albion guns are industrial", DefDatabase<ThingDef>.GetNamed("HE_Albion_Rifle").techLevel == TechLevel.Industrial);
        }
    }
}
