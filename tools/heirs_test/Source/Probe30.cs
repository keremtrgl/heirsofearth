using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;
using Verse.AI;

namespace HeProbe
{
    /// <summary>3.0a checks: Kemet, Pars and Inti content, their buildings, chains and artifacts.</summary>
    public static class Probe30
    {
        private static readonly string[] Nations = { "HE_Kemet", "HE_Pars", "HE_Inti" };

        /// <summary>3.0.1: every heir pawn kind wears its own nation's clothes, never another nation's kit, a vanilla hat or a parka.</summary>
        public static void Kits()
        {
            string[] vanilla = { "Apparel_CowboyHat", "Apparel_BowlerHat", "Apparel_Tuque", "Apparel_Parka" };
            int pawns = 0, bad = 0, bare = 0, missing = 0;
            List<string> notes = new List<string>();
            foreach (PawnKindDef kind in DefDatabase<PawnKindDef>.AllDefs.Where(k => k.defName.StartsWith("HE_") && !k.defName.StartsWith("HE_Renegade")))
            {
                string nation = kind.defName.Split('_')[1];
                for (int i = 0; i < 6; i++)
                {
                    Pawn pawn = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, null, canGeneratePawnRelations: false));
                    pawns++;
                    List<ThingDef> worn = pawn.apparel.WornApparel.Select(a => a.def).ToList();
                    List<ThingDef> wrong = worn.Where(d => vanilla.Contains(d.defName) || (d.defName.StartsWith("HE_") && !d.defName.StartsWith("HE_" + nation + "_"))).ToList();
                    if (wrong.Count > 0)
                    {
                        bad++;
                        if (notes.Count < 8) notes.Add(kind.defName + ":" + string.Join("+", wrong.Select(d => d.defName)));
                    }
                    if (!worn.Any(d => d.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.Torso)))
                    {
                        bare++;
                        if (notes.Count < 8) notes.Add(kind.defName + ":no torso");
                    }
                    if (kind.apparelRequired != null && kind.apparelRequired.Any(r => !worn.Contains(r)))
                    {
                        missing++;
                        if (notes.Count < 8) notes.Add(kind.defName + ":missing " + string.Join("+", kind.apparelRequired.Where(r => !worn.Contains(r)).Select(r => r.defName)));
                    }
                    P.Gone(pawn);
                }
            }
            P.Check("kits checked", pawns >= 400, pawns.ToString());
            P.Check("no foreign or vanilla kit on heir pawns", bad == 0, bad + " " + string.Join(" ", notes));
            P.Check("every heir pawn dressed", bare == 0, bare.ToString());
            P.Check("required nation clothes worn", missing == 0, missing.ToString());
        }

        public static void Content()
        {
            foreach (string name in Nations)
            {
                NationDef n = DefDatabase<NationDef>.GetNamedSilentFail(name);
                P.Check("3.0 nation " + name, n != null && n.release == 3, n == null ? "missing" : "release " + n.release);
                if (n == null) continue;
                Faction f = HeirsWorld.FactionOf(n);
                if (f != null)
                {
                    P.Check("3.0 nation settled " + name, Find.WorldObjects.Settlements.Any(s => s.Faction == f));
                }
                else
                {
                    P.Say("3.0 nation not in this world: " + name);
                }
            }
            NationDef kemet = DefDatabase<NationDef>.GetNamed("HE_Kemet");
            NationDef pars = DefDatabase<NationDef>.GetNamed("HE_Pars");
            NationDef inti = DefDatabase<NationDef>.GetNamed("HE_Inti");
            P.Check("kemet friend of hellas", kemet.IsFriendOf(DefDatabase<NationDef>.GetNamed("HE_Hellas")));
            P.Check("pars friend of tianxia", pars.IsFriendOf(DefDatabase<NationDef>.GetNamed("HE_Tianxia")));
            P.Check("pars rival of roma", pars.IsRivalOf(DefDatabase<NationDef>.GetNamed("HE_Roma")));
            P.Check("inti rival of albion", inti.IsRivalOf(DefDatabase<NationDef>.GetNamed("HE_Albion")));

            foreach (string t in new[] { "HE_Kemet_Silt", "HE_Inti_Terraces" })
            {
                TerrainDef def = DefDatabase<TerrainDef>.GetNamed(t);
                P.Check("farm floor fertile " + t, def.fertility > 0.5f && def.affordances.Contains(DefDatabase<TerrainAffordanceDef>.GetNamed("GrowSoil")), "fertility " + def.fertility);
            }
            P.Check("terraces need diggable ground", DefDatabase<TerrainDef>.GetNamed("HE_Inti_Terraces").terrainAffordanceNeeded == DefDatabase<TerrainAffordanceDef>.GetNamed("Diggable"));

            ThingDef workshop = DefDatabase<ThingDef>.GetNamed("HE_Kemet_PapyrusWorkshop");
            RecipeDef papyrus = DefDatabase<RecipeDef>.GetNamed("HE_Kemet_MakePapyrus");
            P.Check("workshop makes papyrus", workshop.AllRecipes.Contains(papyrus) && papyrus.products[0].thingDef.defName == "HE_Kemet_Papyrus");
            ThingDef loom = DefDatabase<ThingDef>.GetNamed("HE_Pars_CarpetLoom");
            RecipeDef carpet = DefDatabase<RecipeDef>.GetNamed("HE_Pars_WeaveCarpet");
            P.Check("loom weaves carpet", loom.AllRecipes.Contains(carpet) && carpet.products[0].thingDef.defName == "HE_Pars_Carpet");
            P.Check("loom takes sheep wool", carpet.fixedIngredientFilter.Allows(DefDatabase<ThingDef>.GetNamed("WoolSheep")));

            foreach (string gun in new[] { "HE_Kemet_CompositeBow", "HE_Pars_Bow", "HE_Pars_Jezail", "HE_Inti_Sling", "HE_Inti_Carbine", "HE_Kemet_DesertRifle" })
            {
                ThingDef def = DefDatabase<ThingDef>.GetNamedSilentFail(gun);
                ThingDef proj = def?.Verbs?.FirstOrDefault()?.defaultProjectile;
                P.Check("ranged weapon " + gun, def != null && proj != null && P.HasTexture(def.graphicData.texPath) && P.HasTexture(proj.graphicData.texPath),
                        proj?.defName ?? "no projectile");
            }
            P.Check("sling throws stones", DefDatabase<ThingDef>.GetNamed("HE_Inti_Sling").Verbs[0].defaultProjectile.defName == "HE_Stone_Inti");

            foreach (string giverName in new[] { "HE_Senet", "HE_Garden" })
            {
                JoyGiverDef giver = DefDatabase<JoyGiverDef>.GetNamedSilentFail(giverName);
                P.Check("joy giver " + giverName, giver != null && giver.thingDefs.All(t => t != null) && giver.jobDef != null);
            }
            P.Check("garden is meditative", DefDatabase<JoyGiverDef>.GetNamed("HE_Garden").joyKind?.defName == "Meditative");
            P.Check("food store patch active", HeirsPatches.Active("foodStore"));
        }

        public static void Buildings()
        {
            Map map = P.Home;
            foreach (string name in new[] { "HE_Kemet_SenetTable", "HE_Pars_Garden" })
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
                        P.Check("joy job runs " + name, pawn.CurJobDef != null);
                        pawn.jobs.EndCurrentJob(JobCondition.InterruptForced);
                    }
                    building.Destroy();
                });
            }
            P.Run("quipu table links to bench", () =>
            {
                Thing bench = P.SpawnBuilding(ThingDefOf.SimpleResearchBench, map);
                float before = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                ThingDef tableDef = DefDatabase<ThingDef>.GetNamed("HE_Inti_QuipuTable");
                Thing table = ThingMaker.MakeThing(tableDef, GenStuff.DefaultStuffFor(tableDef));
                table.SetFaction(Faction.OfPlayer);
                IntVec3 spot = CellFinder.RandomClosewalkCellNear(bench.Position + new IntVec3(0, 0, 4), map, 2, c => GenAdj.OccupiedRect(c, Rot4.North, tableDef.size).Cells.All(x => x.InBounds(map) && x.Standable(map) && x.GetFirstBuilding(map) == null));
                GenSpawn.Spawn(table, spot, map, Rot4.North);
                P.Ticks(10);
                CompAffectedByFacilities links = bench.TryGetComp<CompAffectedByFacilities>();
                float after = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                P.Check("quipu table linked", links != null && links.LinkedFacilitiesListForReading.Contains(table), links == null ? "no comp" : links.LinkedFacilitiesListForReading.Count + " links");
                P.Check("quipu table speeds research", after > before + 0.003f, before.ToString("F3") + " -> " + after.ToString("F3"));
                table.Destroy();
                bench.Destroy();
            });
            P.Run("qullqa slows rot", () =>
            {
                Thing store = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Inti_Qullqa"), map);
                P.Check("qullqa is storage", store is Building_Storage);
                HeirsFoodStorePatch.Reset(); // the store cells are cached per map; see the new store at once
                Thing inStore = ThingMaker.MakeThing(ThingDefOf.RawPotatoes);
                inStore.stackCount = 10;
                GenSpawn.Spawn(inStore, store.Position, map);
                Thing outside = ThingMaker.MakeThing(ThingDefOf.RawPotatoes);
                outside.stackCount = 10;
                GenSpawn.Spawn(outside, P.FreeSpot(map, new IntVec2(1, 1)), map);
                CompRottable rIn = inStore.TryGetComp<CompRottable>();
                CompRottable rOut = outside.TryGetComp<CompRottable>();
                P.Check("qullqa factor", Mathf.Abs(HeirsFoodStorePatch.FactorFor(inStore) - 0.5f) < 0.01f && HeirsFoodStorePatch.FactorFor(outside) == 1f);
                int tIn = rIn.TicksUntilRotAtTemp(20f), tOut = rOut.TicksUntilRotAtTemp(20f);
                P.Check("qullqa doubles rot time", tIn > tOut * 1.8f, tOut + " -> " + tIn);
                float a0 = rIn.RotProgress, b0 = rOut.RotProgress;
                rIn.CompTickInterval(2500);
                rOut.CompTickInterval(2500);
                float gIn = rIn.RotProgress - a0, gOut = rOut.RotProgress - b0;
                if (gOut > 0f)
                {
                    P.Check("qullqa rot ticks slower", gIn < gOut * 0.6f, gOut.ToString("F1") + " vs " + gIn.ToString("F1"));
                }
                else
                {
                    P.Say("no rot this cold, temp " + inStore.AmbientTemperature.ToString("F0"));
                }
                if (!inStore.Destroyed) inStore.Destroy();
                if (!outside.Destroyed) outside.Destroy();
                store.Destroy();
            });
            foreach (string name in new[] { "HE_Kemet_Obelisk", "HE_Pars_PostLamp", "HE_Inti_SunStone", "HE_Kemet_PapyrusWorkshop", "HE_Pars_CarpetLoom" })
            {
                P.Run("spawn " + name, () =>
                {
                    Thing b = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed(name), map);
                    P.Check("spawn " + name, b.Spawned && P.HasTexture(b.def.graphicData.texPath));
                    string unused = b.GetInspectString();
                    b.Destroy();
                });
            }
        }

        public static void Chains()
        {
            HeirsGame g = P.Game;
            foreach (string pair in new[] { "Kemet:SecondSunrise", "Pars:RoadOfKings", "Inti:CountedEmpire" })
            {
                string nation = pair.Split(':')[0], cap = pair.Split(':')[1];
                P.Run("chain 3.0 " + nation, () =>
                {
                    ChainDef chain = DefDatabase<ChainDef>.GetNamed("HE_Chain_" + nation);
                    ResearchProjectDef capstone = P.R("HE_" + nation + "_" + cap);
                    g.SetKnowledge(chain.nation, 100f);
                    foreach (ResearchProjectDef pre in capstone.prerequisites ?? new List<ResearchProjectDef>())
                        Find.ResearchManager.FinishProject(pre, false, null, false);
                    P.Check("capstone locked before chain " + nation, !g.CanStart(capstone, out string w0), w0 ?? "");
                    HeirsChains.Start(g, chain);
                    for (int i = 0; i < 6 && !g.State(chain).done; i++) HeirsChains.ForceCompleteStep(g, chain);
                    P.Check("chain_runs_to_end " + nation, g.State(chain).done, "step " + g.State(chain).step);
                    P.Check("capstone opens after chain " + nation, g.CanStart(capstone, out string w1), w1 ?? "");
                });
            }
        }

        public static void Artifacts()
        {
            Map map = P.Home;
            foreach (string name in new[] { "HE_Kemet_Artifact_SunDisc", "HE_Pars_Artifact_KingsEye", "HE_Inti_Artifact_GoldenThread" })
            {
                P.Run("artifact " + name, () =>
                {
                    Pawn pawn = P.Colonist(map);
                    Thing art = ThingMaker.MakeThing(DefDatabase<ThingDef>.GetNamed(name));
                    GenPlace.TryPlaceThing(art, pawn.Position, map, ThingPlaceMode.Near);
                    var comp = art.TryGetComp<CompUseEffect_HeirsArtifact>();
                    P.Check("artifact comp " + name, comp != null && art.TryGetComp<CompUsable>() != null);
                    P.Check("artifact usable " + name, comp.CanBeUsedBy(pawn).Accepted);
                    Dictionary<Faction, int> before = Find.FactionManager.AllFactions.Where(f => !f.IsPlayer).ToDictionary(f => f, f => f.PlayerGoodwill);
                    comp.DoEffect(pawn);
                    P.Check("artifact_works " + name, pawn.health.hediffSet.HasHediff(DefDatabase<HediffDef>.GetNamed("HE_Rallied")));
                    P.Check("artifact cooldown " + name, !comp.CanBeUsedBy(pawn).Accepted && comp.CooldownTicksLeft > 0);
                    if (name.Contains("KingsEye"))
                    {
                        bool raised = HeirsWorld.LiveNations.Select(HeirsWorld.FactionOf).Any(f => f != null && before.ContainsKey(f) && f.PlayerGoodwill > before[f]);
                        P.Check("kings eye raises goodwill", raised);
                    }
                    string unused = art.GetInspectString();
                    art.Destroy();
                });
            }
        }
            public static void Routes()
        {
            HeirsGame g = P.Game;
            Map map = P.Home;
            P.Check("routes setting on", HeirsRoutes.Enabled);
            P.Check("three roads without royal post", HeirsRoutes.MaxRoutes == 3 || HeirsRoutes.HasRoyalPost);
            List<NationDef> friendly = HeirsWorld.LiveNations.Where(n => !HeirsWorld.FactionOf(n).HostileTo(Faction.OfPlayer) && HeirsRoutes.Distance(n) >= 0f).ToList();
            P.Check("friendly nations for roads", friendly.Count >= 2, friendly.Count.ToString());
            if (friendly.Count < 2) return;
            NationDef a = friendly[0], b = friendly[1];
            foreach (NationDef n in new[] { a, b })
            {
                int cost = HeirsRoutes.Cost(n);
                P.Check("road cost in range " + n.defName, cost >= HeirsRoutes.MinCost && cost <= HeirsRoutes.MaxCost && cost % 50 == 0, cost.ToString());
                P.Check("road goods " + n.defName, HeirsRoutes.GoodsOf(n).Count > 0 && HeirsRoutes.GoodsOf(n).All(d => d.tradeability.TraderCanSell()), HeirsRoutes.GoodsOf(n).Count.ToString());
            }
            HeirsPolitics.Affect(a, 10 - HeirsPolitics.PlayerGoodwill(a));
            P.Check("low goodwill blocks road", !HeirsRoutes.CanOpen(g, a, out string w0), w0 ?? "");
            HeirsPolitics.Affect(a, 50 - HeirsPolitics.PlayerGoodwill(a));
            int cost0 = HeirsRoutes.Cost(a);
            Thing silver = ThingMaker.MakeThing(ThingDefOf.Silver);
            silver.stackCount = cost0 + 50;
            GenPlace.TryPlaceThing(silver, P.Colonist(map).Position, map, ThingPlaceMode.Near);
            int before = HeirsChains.CountAvailable(ThingDefOf.Silver);
            P.Check("road can open", HeirsRoutes.CanOpen(g, a, out string w1), w1 ?? "");
            P.Check("road opens", HeirsRoutes.Open(g, a));
            P.Check("road paid", HeirsChains.CountAvailable(ThingDefOf.Silver) == before - cost0, before + " -> " + HeirsChains.CountAvailable(ThingDefOf.Silver));
            TradeRoute route = HeirsRoutes.RouteTo(g, a);
            P.Check("road saved in game", route != null && route.cost == cost0 && route.nextTick > Find.TickManager.TicksGame);
            P.Check("no second road to the same nation", !HeirsRoutes.CanOpen(g, a, out _));

            int goodwill = HeirsPolitics.PlayerGoodwill(a);
            int silverBefore = HeirsChains.CountAvailable(ThingDefOf.Silver);
            P.Check("caravan trip", HeirsRoutes.Trip(g, route, false));
            P.Ticks(600);
            P.Check("caravan brought silver", HeirsChains.CountAvailable(ThingDefOf.Silver) > silverBefore, silverBefore + " -> " + HeirsChains.CountAvailable(ThingDefOf.Silver));
            P.Check("caravan raises goodwill", HeirsPolitics.PlayerGoodwill(a) > goodwill, goodwill + " -> " + HeirsPolitics.PlayerGoodwill(a));
            P.Check("trip counted", route.trips == 1);
            P.Check("raided caravan brings nothing", !HeirsRoutes.Trip(g, route, true) && route.raids == 1);
            List<Thing> goods = HeirsRoutes.Goods(a, 300, out string summary);
            float value = goods.Sum(t => t.MarketValue * t.stackCount);
            P.Check("caravan value near target", value >= 240f && value <= 330f, value.ToString("F0") + ": " + summary);
            foreach (Thing t in goods) t.Destroy();

            route.nextTick = Find.TickManager.TicksGame - 1;
            HeirsRoutes.TickRare(g);
            P.Check("due caravan leaves on tick", route.trips + route.raids == 3 && route.nextTick > Find.TickManager.TicksGame, route.trips + "/" + route.raids);

            HeirsRoutes.Open(g, b, false);
            Faction fb = HeirsWorld.FactionOf(b);
            int gwB = HeirsPolitics.PlayerGoodwill(b);
            fb.TryAffectGoodwillWith(Faction.OfPlayer, -200, false, false, null);
            HeirsRoutes.TickRare(g);
            P.Check("hostile nation closes road", HeirsRoutes.RouteTo(g, b) == null && HeirsRoutes.RouteTo(g, a) != null);
            fb.TryAffectGoodwillWith(Faction.OfPlayer, Mathf.Max(gwB, 25) - fb.GoodwillWith(Faction.OfPlayer), false, false, null);
            P.Check("relations restored after test", !fb.HostileTo(Faction.OfPlayer));
        }

        public static void RoutesAfterLoad()
        {
            HeirsGame g = P.Game;
            P.Check("road kept after load", g.routes.Count == 1 && g.routes[0].nation != null && g.routes[0].trips + g.routes[0].raids == 3,
                    g.routes.Count + " roads");
        }
            private static void SetGoodwill(NationDef n, int target)
        {
            Faction f = HeirsWorld.FactionOf(n);
            if (f == null) return;
            f.TryAffectGoodwillWith(Faction.OfPlayer, target - f.GoodwillWith(Faction.OfPlayer), false, false, null);
        }

        public static void Council()
        {
            HeirsGame g = P.Game;
            Map map = P.Home;
            HeirsCouncil.NoCredits = true;
            ResearchProjectDef research = P.R("HE_WorldCouncil");
            ThingDef hall = DefDatabase<ThingDef>.GetNamedSilentFail(HeirsCouncil.HallDefName);
            P.Check("council hall def", hall != null && hall.size == new IntVec2(5, 5) && P.HasTexture(hall.graphicData.texPath) && hall.researchPrerequisites.Contains(research));
            P.Check("council setting on", HeirsCouncil.Enabled);
            g.councilUnlocked = false;
            P.Check("council research locked", !g.CanStart(research, out string w0) && !w0.NullOrEmpty(), w0 ?? "");
            P.Check("council ready after three stories", HeirsCouncil.ChainsDone(g) >= 3 && HeirsCouncil.UnlockReady(g), HeirsCouncil.ChainsDone(g).ToString());
            HeirsCouncil.TickRare(g);
            P.Check("council unlocks on tick", g.councilUnlocked);
            P.Check("council research opens", g.CanStart(research, out string w1), w1 ?? "");
            P.Check("no meeting without hall", !HeirsCouncil.CanMeet(g, out string w2) && w2 == "HE_CouncilNeedHall".Translate().Resolve(), w2 ?? "");
            Thing built = P.SpawnBuilding(hall, map);
            P.Check("hall built", HeirsCouncil.HallBuilt());
            P.Check("meeting possible", HeirsCouncil.CanMeet(g, out string w3), w3 ?? "");

            List<NationDef> living = HeirsWorld.LiveNations.ToList();
            P.Check("living nations for council", living.Count >= 3, living.Count.ToString());
            if (living.Count < 3) return;
            foreach (NationDef n in living) SetGoodwill(n, 0);
            P.Check("cold council fails", HeirsCouncil.Meet(g) == null && g.councilWon == null);
            P.Check("one meeting per quadrum", !HeirsCouncil.CanMeet(g, out string w4) && HeirsCouncil.DaysToNextMeeting(g) > 0, w4 ?? "");

            HeirsWorld world = HeirsWorld.Get;
            NationDef a = living[0], b = living[1];
            world.wars.RemoveAll(w => w.Is(a, b));
            world.alliances.RemoveAll(w => w.Is(a, b));
            SetGoodwill(a, 65);
            P.Check("friend votes yes", HeirsCouncil.Vote(g, a, out string v0), v0);
            SetGoodwill(b, 65);
            world.wars.Add(new NationPair { a = a, b = b, startTick = Find.TickManager.TicksGame });
            P.Check("enemy of a yes votes no", !HeirsCouncil.Vote(g, a, out string v1) && !HeirsCouncil.Vote(g, b, out _), v1);
            world.wars.RemoveAll(w => w.Is(a, b));
            SetGoodwill(b, -100);
            P.Check("hostile votes no", !HeirsCouncil.Vote(g, b, out string v2), v2);
            P.Check("two thirds rule", HeirsCouncil.YesNeeded(9) == 6 && HeirsCouncil.YesNeeded(4) == 3 && HeirsCouncil.YesNeeded(3) == 2);

            foreach (NationDef n in living) SetGoodwill(n, 90);
            P.Check("allies vote yes", living.All(n => HeirsCouncil.Vote(g, n, out _)), string.Join(",", living.Select(n => HeirsWorld.FactionOf(n).RelationKindWith(Faction.OfPlayer).ToString())));
            P.Check("unity victory", HeirsCouncil.Meet(g, true) == "Unity" && g.councilWon == "Unity");
            P.Check("no meeting after victory", !HeirsCouncil.CanMeet(g, out _));
            g.councilWon = null;

            NationDef rebel = living[2];
            SetGoodwill(rebel, -100);
            int count = HeirsCouncil.Settlements(rebel);
            g.peakSettlements[rebel] = count * 2 + 1;
            g.fealtyOffers.Remove(rebel);
            int letters = Find.LetterStack.LettersListForReading.Count;
            HeirsCouncil.TickRare(g);
            ChoiceLetter_HeirsFealty offer = Find.LetterStack.LettersListForReading.OfType<ChoiceLetter_HeirsFealty>().LastOrDefault();
            P.Check("beaten nation offers fealty", offer != null && offer.nation == rebel && Find.LetterStack.LettersListForReading.Count > letters);
            HeirsCouncil.TickRare(g);
            P.Check("fealty offer not repeated at once", Find.LetterStack.LettersListForReading.OfType<ChoiceLetter_HeirsFealty>().Count(l => l.nation == rebel) == 1);
            HeirsCouncil.AcceptFealty(g, rebel);
            P.Check("fealty accepted", HeirsCouncil.IsVassal(g, rebel) && !HeirsWorld.FactionOf(rebel).HostileTo(Faction.OfPlayer));
            P.Check("vassal votes yes", HeirsCouncil.Vote(g, rebel, out string v3), v3);
            if (offer != null) Find.LetterStack.RemoveLetter(offer);

            int silver = HeirsChains.CountAvailable(ThingDefOf.Silver);
            g.lastTributeTick = Find.TickManager.TicksGame - (HeirsCouncil.TributeIntervalDays + 1) * GenDate.TicksPerDay;
            HeirsCouncil.TickRare(g);
            P.Ticks(600);
            P.Check("vassal pays tribute", HeirsChains.CountAvailable(ThingDefOf.Silver) >= silver + HeirsCouncil.TributePerSettlement, silver + " -> " + HeirsChains.CountAvailable(ThingDefOf.Silver));

            SetGoodwill(rebel, -100);
            HeirsCouncil.TickRare(g);
            P.Check("hostile vassal breaks oath", !HeirsCouncil.IsVassal(g, rebel));
            SetGoodwill(rebel, 20);

            P.Check("not subdued yet", !HeirsCouncil.AllSubdued(g));
            g.vassals.Clear();
            g.vassals.AddRange(HeirsWorld.LiveNations);
            P.Check("dominion victory", HeirsCouncil.Meet(g, true) == "Dominion" && g.councilWon == "Dominion");
            g.vassals.RemoveRange(1, g.vassals.Count - 1);
            built.Destroy();
            HeirsCouncil.NoCredits = false;
        }

        public static void CouncilAfterLoad()
        {
            HeirsGame g = P.Game;
            P.Check("council saved", g.councilUnlocked && g.councilWon == "Dominion" && g.vassals.Count == 1 && g.peakSettlements.Count > 0 && g.lastMeetingTick > 0,
                    g.councilUnlocked + " " + g.councilWon + " " + g.vassals.Count);
        }
    }
}
