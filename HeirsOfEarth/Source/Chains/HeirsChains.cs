using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    public enum StepKind
    {
        Deliver,
        Build,
        Research,
        Raid,
        Site,
        Choice
    }

    public class ChainOption
    {
        public string label;
        public string text;
        public int goodwill;
        public float knowledge;
        public bool keepArtifact = true;
        public List<ThingDefCountClass> rewards = new List<ThingDefCountClass>();
        public List<ThingDefCountClass> takes = new List<ThingDefCountClass>();
    }

    public class ChainStep
    {
        public StepKind kind;
        public string label;
        public string text;
        public string doneText;
        public List<ThingDefCountClass> things = new List<ThingDefCountClass>();
        public ThingDef building;
        public ResearchProjectDef project;
        public NationDef enemy;
        public float points = 600f;
        public string siteLayout = "Ring";
        public ThingDef siteWall;
        public ThingDef siteProp;
        public ThingDef siteReward;
        public float siteThreat = 1f;
        public GameConditionDef condition;
        public float conditionDays = 3f;
        public List<ChainOption> options = new List<ChainOption>();
    }

    /// <summary>A nation's story: 4-5 steps ending in its legendary artifact.</summary>
    public class ChainDef : Def
    {
        public NationDef nation;
        public float startKnowledge = 60f;
        public List<ChainStep> steps = new List<ChainStep>();
        public ThingDef artifact;
        /// <summary>3.5: a later chapter of a nation's saga only begins once this chain is done.</summary>
        public ChainDef after;
        public string startText;
        public string endText;
    }

    public class ChainState : IExposable
    {
        public bool started;
        public bool done;
        public int step;
        public int stepTick;
        public bool raidSpawned;
        public int raidMapId = -1;
        public Faction raidFaction;
        public HeirsSite site;
        public int choice = -1;

        public void ExposeData()
        {
            Scribe_Values.Look(ref started, "started");
            Scribe_Values.Look(ref done, "done");
            Scribe_Values.Look(ref step, "step");
            Scribe_Values.Look(ref stepTick, "stepTick");
            Scribe_Values.Look(ref raidSpawned, "raidSpawned");
            Scribe_Values.Look(ref raidMapId, "raidMapId", -1);
            Scribe_References.Look(ref raidFaction, "raidFaction");
            Scribe_References.Look(ref site, "site");
            Scribe_Values.Look(ref choice, "choice", -1);
        }
    }

    public static class HeirsChains
    {
        public const int RaidDelayTicks = 60000;

        public static IEnumerable<ChainDef> All => DefDatabase<ChainDef>.AllDefsListForReading;

        public static ChainStep Current(ChainDef chain, ChainState state)
        {
            return state.started && !state.done && state.step < chain.steps.Count ? chain.steps[state.step] : null;
        }

        public static void TickRare(HeirsGame game)
        {
            foreach (ChainDef chain in All)
            {
                ChainState state = game.State(chain);
                if (state.done)
                {
                    continue;
                }
                if (!state.started)
                {
                    if (CanStart(game, chain))
                    {
                        Start(game, chain);
                    }
                    continue;
                }
                ChainStep step = Current(chain, state);
                if (step != null && Check(chain, state, step))
                {
                    Advance(game, chain);
                }
            }
        }

        public static bool CanStart(HeirsGame game, ChainDef chain)
        {
            if (chain.nation == null || !HeirsMod.Settings.NationActive(chain.nation) || (chain.after != null && !game.State(chain.after).done))
            {
                return false;
            }
            return game.heritage == chain.nation || game.Knowledge(chain.nation) >= chain.startKnowledge;
        }

        public static void Start(HeirsGame game, ChainDef chain)
        {
            ChainState state = game.State(chain);
            if (state.started)
            {
                return;
            }
            state.started = true;
            state.step = 0;
            game.AddChronicle("HE_ChainStartedChronicle".Translate(chain.LabelCap), chain.nation);
            HeirsMusic.Sting(chain.nation);
            Find.LetterStack.ReceiveLetter("HE_ChainStartedLabel".Translate(chain.LabelCap), chain.startText + "\n\n" + Goal(chain, state), LetterDefOf.PositiveEvent);
            BeginStep(game, chain);
        }

        public static string Goal(ChainDef chain, ChainState state)
        {
            ChainStep step = Current(chain, state);
            if (step == null)
            {
                return "";
            }
            string goal = "HE_ChainGoal".Translate(state.step + 1, chain.steps.Count, step.label) + "\n" + step.text;
            if (step.kind == StepKind.Deliver)
            {
                goal += "\n" + string.Join("\n", step.things.Where(t => t?.thingDef != null).Select(t => "  - " + t.thingDef.LabelCap + " x" + t.count + " (" + CountAvailable(t.thingDef) + ")"));
            }
            return goal;
        }

        private static void BeginStep(HeirsGame game, ChainDef chain)
        {
            ChainState state = game.State(chain);
            ChainStep step = Current(chain, state);
            state.stepTick = Find.TickManager.TicksGame;
            state.raidSpawned = false;
            state.raidMapId = -1;
            state.raidFaction = null;
            state.choice = -1;
            if (step == null)
            {
                return;
            }
            if (step.condition != null && Find.AnyPlayerHomeMap != null)
            {
                Find.AnyPlayerHomeMap.gameConditionManager.RegisterCondition(GameConditionMaker.MakeCondition(step.condition, Mathf.RoundToInt(step.conditionDays * GenDate.TicksPerDay)));
            }
            if (step.kind == StepKind.Site)
            {
                state.site = HeirsSites.Reveal(chain, step);
            }
            else if (step.kind == StepKind.Choice)
            {
                var letter = (ChoiceLetter_HeirsChain)LetterMaker.MakeLetter(DefDatabase<LetterDef>.GetNamed("HE_ChainChoiceLetter"));
                letter.Label = chain.LabelCap + ": " + step.label;
                letter.Text = step.text;
                letter.chain = chain;
                letter.stepIndex = state.step;
                Find.LetterStack.ReceiveLetter(letter);
            }
        }

        /// <summary>True when the current step's goal is met.</summary>
        public static bool Check(ChainDef chain, ChainState state, ChainStep step)
        {
            switch (step.kind)
            {
                case StepKind.Build:
                    return Find.Maps.Any(m => m.IsPlayerHome && m.listerBuildings.ColonistsHaveBuilding(step.building));
                case StepKind.Research:
                    return step.project != null && step.project.IsFinished;
                case StepKind.Raid:
                    return CheckRaid(chain, state, step);
                case StepKind.Site:
                    return step.siteReward != null && PlayerHas(step.siteReward);
                default:
                    return false;
            }
        }

        private static bool CheckRaid(ChainDef chain, ChainState state, ChainStep step)
        {
            if (!state.raidSpawned)
            {
                if (Find.TickManager.TicksGame - state.stepTick < RaidDelayTicks)
                {
                    return false;
                }
                SpawnRaid(state, step);
                return false;
            }
            Map map = Find.Maps.FirstOrDefault(m => m.uniqueID == state.raidMapId);
            if (map == null || state.raidFaction == null)
            {
                return true;
            }
            return !map.mapPawns.SpawnedPawnsInFaction(state.raidFaction).Any(p => !p.Downed && !p.Dead && !p.IsPrisoner);
        }

        public static void SpawnRaid(ChainState state, ChainStep step)
        {
            Map map = Find.AnyPlayerHomeMap;
            if (map == null)
            {
                return;
            }
            Faction faction = HostileFaction(step.enemy);
            if (faction == null)
            {
                state.raidSpawned = true;
                return;
            }
            IncidentParms parms = StorytellerUtility.DefaultParmsNow(IncidentCategoryDefOf.ThreatBig, map);
            parms.faction = faction;
            parms.points = Mathf.Max(step.points, parms.points * 0.8f) * HeirsMod.Settings.raidStrength;
            parms.raidStrategy = RaidStrategyDefOf.ImmediateAttack;
            parms.raidArrivalMode = PawnsArrivalModeDefOf.EdgeWalkIn;
            parms.forced = true;
            IncidentDefOf.RaidEnemy.Worker.TryExecute(parms);
            state.raidSpawned = true;
            state.raidMapId = map.uniqueID;
            state.raidFaction = faction;
        }

        /// <summary>The enemy nation's faction if it is hostile, otherwise the renegades.</summary>
        public static Faction HostileFaction(NationDef enemy)
        {
            Faction faction = enemy != null ? HeirsWorld.FactionOf(enemy) : null;
            if (faction != null && !faction.defeated && faction.HostileTo(Faction.OfPlayer))
            {
                return faction;
            }
            FactionDef renegades = DefDatabase<FactionDef>.GetNamedSilentFail("HE_Renegades");
            Faction r = renegades != null ? Find.FactionManager.FirstFactionOfDef(renegades) : null;
            return r ?? Find.FactionManager.RandomEnemyFaction(false, false, true, TechLevel.Undefined);
        }

        public static int CountAvailable(ThingDef def)
        {
            return Find.Maps.Where(m => m.IsPlayerHome).Sum(m => m.listerThings.ThingsOfDef(def).Where(t => t.Spawned && !t.IsForbidden(Faction.OfPlayer)).Sum(t => t.stackCount));
        }

        public static bool PlayerHas(ThingDef def)
        {
            if (Find.Maps.Where(m => m.IsPlayerHome).Any(m => m.listerThings.ThingsOfDef(def).Any()))
            {
                return true;
            }
            return Find.WorldObjects.Caravans.Any(c => c.IsPlayerControlled && CaravanInventoryUtility.AllInventoryItems(c).Any(t => t.def == def));
        }

        public static bool CanDeliver(ChainDef chain, ChainState state)
        {
            ChainStep step = Current(chain, state);
            return step != null && step.kind == StepKind.Deliver && step.things.All(t => t?.thingDef == null || CountAvailable(t.thingDef) >= t.count);
        }

        public static void Deliver(HeirsGame game, ChainDef chain)
        {
            ChainState state = game.State(chain);
            if (!CanDeliver(chain, state))
            {
                return;
            }
            foreach (ThingDefCountClass need in Current(chain, state).things)
            {
                TakeFromColony(need.thingDef, need.count);
            }
            Advance(game, chain);
        }

        /// <summary>Removes up to count of def from unforbidden stacks on player home maps; returns how many were taken.</summary>
        public static int TakeFromColony(ThingDef def, int count, bool includeForbidden = false)
        {
            if (def == null || count <= 0)
            {
                return 0;
            }
            int left = count;
            foreach (Map map in Find.Maps.Where(m => m.IsPlayerHome))
            {
                foreach (Thing thing in map.listerThings.ThingsOfDef(def).Where(t => t.Spawned && (includeForbidden || !t.IsForbidden(Faction.OfPlayer))).ToList())
                {
                    if (left <= 0) break;
                    int take = Mathf.Min(left, thing.stackCount);
                    thing.SplitOff(take).Destroy(DestroyMode.Vanish);
                    left -= take;
                }
            }
            return count - left;
        }

        /// <summary>Like TakeFromColony, but also takes forbidden ones and looks in the player's caravans (used for story relics, which may still be on the road).</summary>
        public static int TakeAnywhere(ThingDef def, int count)
        {
            int taken = TakeFromColony(def, count, true);
            foreach (Caravan caravan in Find.WorldObjects.Caravans.Where(c => c.IsPlayerControlled).ToList())
            {
                foreach (Thing thing in CaravanInventoryUtility.AllInventoryItems(caravan).Where(t => t.def == def).ToList())
                {
                    if (taken >= count) return taken;
                    int take = Mathf.Min(count - taken, thing.stackCount);
                    thing.SplitOff(take).Destroy(DestroyMode.Vanish);
                    taken += take;
                }
            }
            return taken;
        }

        public static void Choose(HeirsGame game, ChainDef chain, int stepIndex, int option)
        {
            ChainState state = game.State(chain);
            ChainStep step = Current(chain, state);
            if (step == null || step.kind != StepKind.Choice || state.step != stepIndex || option < 0 || option >= step.options.Count)
            {
                return;
            }
            state.choice = option;
            ChainOption chosen = step.options[option];
            Faction faction = HeirsWorld.FactionOf(chain.nation);
            if (faction != null && chosen.goodwill != 0 && faction.HasGoodwill)
            {
                faction.TryAffectGoodwillWith(Faction.OfPlayer, chosen.goodwill, true, true, HistoryEventDefOf.QuestGoodwillReward);
            }
            if (chosen.knowledge != 0f)
            {
                game.AddKnowledge(chain.nation, chosen.knowledge, null);
            }
            foreach (ThingDefCountClass take in chosen.takes)
            {
                TakeAnywhere(take.thingDef, take.count);
            }
            foreach (ThingDefCountClass reward in chosen.rewards)
            {
                Give(reward.thingDef, reward.count);
            }
            game.AddChronicle(chain.LabelCap + ": " + chosen.label, chain.nation);
            Advance(game, chain, chosen.keepArtifact);
        }

        /// <summary>Test and debug hook.</summary>
        public static void ForceCompleteStep(HeirsGame game, ChainDef chain)
        {
            ChainState state = game.State(chain);
            ChainStep step = Current(chain, state);
            if (step == null) return;
            if (step.kind == StepKind.Choice)
            {
                Choose(game, chain, state.step, 0);
            }
            else
            {
                Advance(game, chain);
            }
        }

        public static void Advance(HeirsGame game, ChainDef chain, bool keepArtifact = true)
        {
            ChainState state = game.State(chain);
            ChainStep step = Current(chain, state);
            if (step == null)
            {
                return;
            }
            if (state.site != null && !state.site.Destroyed && !state.site.HasMap)
            {
                state.site.Destroy();
            }
            state.site = null;
            state.step++;
            if (state.step >= chain.steps.Count)
            {
                Finish(game, chain, keepArtifact);
                return;
            }
            if (!step.doneText.NullOrEmpty())
            {
                HeirsMusic.Sting(chain.nation);
                Find.LetterStack.ReceiveLetter("HE_ChainStepLabel".Translate(chain.LabelCap), step.doneText + "\n\n" + Goal(chain, state), LetterDefOf.PositiveEvent);
            }
            BeginStep(game, chain);
        }

        private static void Finish(HeirsGame game, ChainDef chain, bool keepArtifact)
        {
            ChainState state = game.State(chain);
            state.done = true;
            if (keepArtifact && chain.artifact != null)
            {
                Give(chain.artifact, 1, QualityCategory.Legendary);
            }
            game.AddChronicle("HE_ChainDoneChronicle".Translate(chain.LabelCap), chain.nation);
            Find.LetterStack.ReceiveLetter("HE_ChainDoneLabel".Translate(chain.LabelCap), chain.endText, LetterDefOf.PositiveEvent);
            HeirsMusic.Play(chain.nation);
        }

        public static void Give(ThingDef def, int count, QualityCategory? quality = null)
        {
            Map map = Find.AnyPlayerHomeMap;
            if (map == null || def == null || count <= 0)
            {
                return;
            }
            var things = new List<Thing>();
            while (count > 0)
            {
                Thing thing = ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                thing.stackCount = Mathf.Min(count, def.stackLimit);
                if (quality.HasValue)
                {
                    thing.TryGetComp<CompQuality>()?.SetQuality(quality.Value, ArtGenerationContext.Outsider);
                }
                count -= thing.stackCount;
                things.Add(thing);
            }
            DropPodUtility.DropThingsNear(DropCellFinder.TradeDropSpot(map), map, things, 110, false, false, false);
        }
    }

    public class ChoiceLetter_HeirsChain : ChoiceLetter
    {
        public ChainDef chain;
        public int stepIndex;

        public override IEnumerable<DiaOption> Choices
        {
            get
            {
                ChainStep step = chain != null && stepIndex < chain.steps.Count ? chain.steps[stepIndex] : null;
                if (step == null || ArchivedOnly || Stale)
                {
                    yield return Option_Close;
                    yield break;
                }
                for (int i = 0; i < step.options.Count; i++)
                {
                    int index = i;
                    ChainOption option = step.options[i];
                    yield return new DiaOption(option.label)
                    {
                        action = () =>
                        {
                            HeirsChains.Choose(HeirsGame.Get, chain, stepIndex, index);
                            Find.LetterStack.RemoveLetter(this);
                        },
                        resolveTree = true
                    };
                }
                yield return Option_Postpone;
            }
        }

        private bool Stale => HeirsGame.Get == null || HeirsGame.Get.State(chain).step != stepIndex;

        public override void ExposeData()
        {
            base.ExposeData();
            Scribe_Defs.Look(ref chain, "chain");
            Scribe_Values.Look(ref stepIndex, "stepIndex");
        }
    }
}
