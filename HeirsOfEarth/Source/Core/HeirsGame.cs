using System.Collections.Generic;
using RimWorld;
using Verse;

namespace HeirsOfEarth
{
    public class ChronicleEntry : IExposable
    {
        public int tick;
        public string text;
        public NationDef nation;

        public void ExposeData()
        {
            Scribe_Values.Look(ref tick, "tick");
            Scribe_Values.Look(ref text, "text");
            Scribe_Defs.Look(ref nation, "nation");
        }
    }

    /// <summary>Per-save state: heritage, Culture Knowledge, chronicle and story chains.</summary>
    public class HeirsGame : GameComponent, IThingHolder
    {
        public const int ChronicleLimit = 200;

        public NationDef heritage;
        public bool heritageChosen;
        public bool reminded;
        private int remindAt = -1;
        public List<ChronicleEntry> chronicle = new List<ChronicleEntry>();
        public List<TradeRoute> routes = new List<TradeRoute>();
        public bool councilUnlocked;
        public string councilWon;
        public int lastMeetingTick = -9999999;
        public int lastTributeTick;
        public int lastTelegramTick;
        // 4.3 World Fair: held once; the exhibit is kept here while it is away
        public bool worldFairHeld;
        public ThingOwner<Thing> fairExhibit;
        public int fairReturnTick;
        public NationDef fairHost;

        public IThingHolder ParentHolder => null;

        public ThingOwner GetDirectlyHeldThings() => fairExhibit;

        public void GetChildHolders(List<IThingHolder> outChildren)
        {
            ThingOwnerUtility.AppendThingHoldersFromThings(outChildren, GetDirectlyHeldThings());
        }
        public List<NationDef> vassals = new List<NationDef>();
        public Dictionary<NationDef, int> peakSettlements = new Dictionary<NationDef, int>();
        public Dictionary<NationDef, int> fealtyOffers = new Dictionary<NationDef, int>();
        public List<Treaty> treaties = new List<Treaty>();
        public List<NationDef> honours = new List<NationDef>();
        public List<Errand> errands = new List<Errand>();
        public int errandsDone;
        private Dictionary<NationDef, float> knowledge = new Dictionary<NationDef, float>();
        private Dictionary<NationDef, float> ageProgress = new Dictionary<NationDef, float>();
        private Dictionary<NationDef, int> ageShown = new Dictionary<NationDef, int>();
        private Dictionary<ChainDef, ChainState> chains = new Dictionary<ChainDef, ChainState>();
        private List<ChainDef> tmpChainKeys;
        private List<ChainState> tmpChainValues;

        public HeirsGame(Game game)
        {
            fairExhibit = new ThingOwner<Thing>(this);
        }

        public static HeirsGame Get => Current.Game?.GetComponent<HeirsGame>();

        public float Knowledge(NationDef nation)
        {
            return nation != null && knowledge.TryGetValue(nation, out float v) ? v : 0f;
        }

        public void AddKnowledge(NationDef nation, float amount, string reasonKey)
        {
            if (nation == null || amount == 0f)
            {
                return;
            }
            if (amount > 0f && HeirsCourt.Is(nation, Temperament.Scholarly))
            {
                amount *= HeirsCourt.ScholarlyKnowledgeFactor; // a scholarly court shares its learning more freely
            }
            float before = Knowledge(nation);
            knowledge[nation] = UnityEngine.Mathf.Max(0f, before + amount);
            if (reasonKey != null && amount >= 10f)
            {
                AddChronicle(reasonKey.Translate(nation.adjective, amount.ToString("0")), nation);
            }
        }

        public bool HasAgeProgress(NationDef nation) => nation != null && ageProgress.ContainsKey(nation);

        public float AgeProgress(NationDef nation) => nation != null && ageProgress.TryGetValue(nation, out float v) ? v : 0f;

        public void SetAgeProgress(NationDef nation, float value)
        {
            if (nation != null) ageProgress[nation] = UnityEngine.Mathf.Max(0f, value);
        }

        public int AgeShown(NationDef nation) => nation != null && ageShown.TryGetValue(nation, out int v) ? v : 0;

        public void SetAgeShown(NationDef nation, int age)
        {
            if (nation != null) ageShown[nation] = age;
        }

        /// <summary>Test hook: sets knowledge directly.</summary>
        public void SetKnowledge(NationDef nation, float amount)
        {
            knowledge[nation] = amount;
        }

        public bool CanStart(ResearchProjectDef project, out string reason)
        {
            reason = null;
            HeirsResearchExt ext = project.GetModExtension<HeirsResearchExt>();
            if (ext == null)
            {
                return true;
            }
            if (ext.council && !councilUnlocked)
            {
                reason = "HE_NeedCouncil".Translate(HeirsCouncil.ChainsToUnlock, HeirsCouncil.RoutesToUnlock);
                return false;
            }
            if (ext.age > 1 && ext.nation != null && ext.nation != heritage && HeirsAges.AgeOf(ext.nation) < ext.age && HeirsAges.On)
            {
                reason = "HE_NeedAge".Translate(ext.nation.LabelCap, HeirsAges.AgeLabel(ext.age));
                return false;
            }
            if (ext.requiresChain != null && !State(ext.requiresChain).done)
            {
                reason = "HE_NeedChain".Translate(ext.requiresChain.LabelCap);
                return false;
            }
            if (ext.nation == null || ext.nation == heritage || ext.knowledge <= 0f)
            {
                return true;
            }
            float have = Knowledge(ext.nation);
            if (have >= ext.knowledge)
            {
                return true;
            }
            reason = "HE_NeedKnowledge".Translate(ext.knowledge.ToString("0"), ext.nation.adjective, have.ToString("0"));
            return false;
        }

        public void SetHeritage(NationDef nation)
        {
            if (heritageChosen)
            {
                return;
            }
            heritageChosen = true;
            heritage = nation;
            AddChronicle(nation == null ? "HE_ChronicleIndependent".Translate() : "HE_ChronicleHeritage".Translate(nation.LabelCap), nation);
            HeirsTraditions.Dirty();
            HeirsWorldHooks.OnHeritageChosen(nation);
        }

        public void AddChronicle(string text, NationDef nation = null)
        {
            chronicle.Add(new ChronicleEntry { tick = Find.TickManager?.TicksAbs ?? 0, text = text, nation = nation });
            if (chronicle.Count > ChronicleLimit)
            {
                chronicle.RemoveRange(0, chronicle.Count - ChronicleLimit);
            }
        }

        public ChainState State(ChainDef chain)
        {
            if (!chains.TryGetValue(chain, out ChainState state))
            {
                state = new ChainState();
                chains[chain] = state;
            }
            return state;
        }

        public override void StartedNewGame()
        {
            remindAt = Find.TickManager.TicksGame + 2500;
        }

        public override void LoadedGame()
        {
            HeirsWorldHooks.AddMissingNations();
            if (!heritageChosen && !reminded)
            {
                remindAt = Find.TickManager.TicksGame + 600;
            }
        }

        /// <summary>One letter, once per save, pointing new players to the heritage choice in the Heirs tab.</summary>
        private void Remind()
        {
            if (reminded || heritageChosen || remindAt < 0 || Find.TickManager.TicksGame < remindAt)
            {
                return;
            }
            reminded = true;
            Find.LetterStack.ReceiveLetter("HE_HeritageReminderLabel".Translate(), "HE_HeritageReminderText".Translate(), LetterDefOf.NeutralEvent);
        }

        public override void GameComponentTick()
        {
            if (Find.TickManager.TicksGame % 250 == 0)
            {
                Remind();
            }
            if (Find.TickManager.TicksGame % 2500 == 0)
            {
                HeirsChains.TickRare(this);
                HeirsRoutes.TickRare(this);
                HeirsCouncil.TickRare(this);
                HeirsErrands.TickRare(this);
                HeirsWorks.TickRare(this);
                HeirsEvents.FairTick(this);
            }
            if (Find.TickManager.TicksGame % GenDate.TicksPerDay == 1234)
            {
                HeirsAges.DailyTick(this);
            }
        }

        public override void ExposeData()
        {
            Scribe_Defs.Look(ref heritage, "heritage");
            Scribe_Values.Look(ref heritageChosen, "heritageChosen");
            Scribe_Values.Look(ref reminded, "reminded");
            Scribe_Collections.Look(ref knowledge, "knowledge", LookMode.Def, LookMode.Value);
            Scribe_Collections.Look(ref chronicle, "chronicle", LookMode.Deep);
            Scribe_Collections.Look(ref chains, "chains", LookMode.Def, LookMode.Deep, ref tmpChainKeys, ref tmpChainValues);
            Scribe_Collections.Look(ref routes, "routes", LookMode.Deep);
            Scribe_Values.Look(ref councilUnlocked, "councilUnlocked");
            Scribe_Values.Look(ref councilWon, "councilWon");
            Scribe_Values.Look(ref lastMeetingTick, "lastMeetingTick", -9999999);
            Scribe_Values.Look(ref lastTributeTick, "lastTributeTick");
            Scribe_Values.Look(ref lastTelegramTick, "lastTelegramTick");
            Scribe_Values.Look(ref worldFairHeld, "worldFairHeld");
            Scribe_Deep.Look(ref fairExhibit, "fairExhibit", this);
            Scribe_Values.Look(ref fairReturnTick, "fairReturnTick");
            Scribe_Defs.Look(ref fairHost, "fairHost");
            Scribe_Collections.Look(ref vassals, "vassals", LookMode.Def);
            Scribe_Collections.Look(ref peakSettlements, "peakSettlements", LookMode.Def, LookMode.Value);
            Scribe_Collections.Look(ref fealtyOffers, "fealtyOffers", LookMode.Def, LookMode.Value);
            Scribe_Collections.Look(ref treaties, "treaties", LookMode.Deep);
            Scribe_Collections.Look(ref honours, "honours", LookMode.Def);
            Scribe_Collections.Look(ref errands, "errands", LookMode.Deep);
            Scribe_Values.Look(ref errandsDone, "errandsDone");
            Scribe_Collections.Look(ref ageProgress, "ageProgress", LookMode.Def, LookMode.Value);
            Scribe_Collections.Look(ref ageShown, "ageShown", LookMode.Def, LookMode.Value);
            if (Scribe.mode == LoadSaveMode.PostLoadInit)
            {
                if (knowledge == null) knowledge = new Dictionary<NationDef, float>();
                if (fairExhibit == null) fairExhibit = new ThingOwner<Thing>(this);
                if (chronicle == null) chronicle = new List<ChronicleEntry>();
                if (chains == null) chains = new Dictionary<ChainDef, ChainState>();
                if (routes == null) routes = new List<TradeRoute>();
                if (vassals == null) vassals = new List<NationDef>();
                if (peakSettlements == null) peakSettlements = new Dictionary<NationDef, int>();
                if (fealtyOffers == null) fealtyOffers = new Dictionary<NationDef, int>();
                if (treaties == null) treaties = new List<Treaty>();
                if (honours == null) honours = new List<NationDef>();
                if (errands == null) errands = new List<Errand>();
                if (ageProgress == null) ageProgress = new Dictionary<NationDef, float>();
                if (ageShown == null) ageShown = new Dictionary<NationDef, int>();
                ageProgress.RemoveAll(p => p.Key == null);
                ageShown.RemoveAll(p => p.Key == null);
                errands.RemoveAll(e => e?.nation == null || e.thing == null);
                treaties.RemoveAll(t => t?.nation == null);
                honours.RemoveAll(n => n == null);
                vassals.RemoveAll(v => v == null);
                peakSettlements.RemoveAll(p => p.Key == null);
                fealtyOffers.RemoveAll(p => p.Key == null);
                routes.RemoveAll(r => r?.nation == null);
                knowledge.RemoveAll(p => p.Key == null);
                chains.RemoveAll(p => p.Key == null || p.Value == null);
                chronicle.RemoveAll(c => c == null);
                HeirsTraditions.Dirty();
            }
        }
    }
}
