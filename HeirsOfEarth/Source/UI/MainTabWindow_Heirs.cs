using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>The "Heirs" main tab: heritage, knowledge, diplomacy, traditions, stories and chronicle.</summary>
    public class MainTabWindow_Heirs : MainTabWindow
    {
        public enum Section { Heritage, Encyclopedia, Knowledge, Research, Diplomacy, Routes, Council, Traditions, Stories, Chronicle }

        private const float Row = 30f;
        private Section section = Section.Heritage;
        private Vector2 scroll;
        private float viewHeight = 600f;

        public override Vector2 RequestedTabSize => new Vector2(960f, 712f);

        public void Show(Section s)
        {
            section = s;
        }

        public override void DoWindowContents(Rect inRect)
        {
            var tabs = new List<TabRecord>();
            foreach (Section s in System.Enum.GetValues(typeof(Section)))
            {
                Section local = s;
                tabs.Add(new TabRecord(("HE_Tab" + s).Translate(), () => { section = local; scroll = Vector2.zero; }, section == s));
            }
            // 4.2.1: ten tabs in one row left each under 96 px and the longer names (Encyclopedia, Culture knowledge) ran into
            // each other, so the tabs sit in two rows of five.
            Rect body = new Rect(inRect.x, inRect.y + 63f, inRect.width, inRect.height - 63f);
            Widgets.DrawMenuSection(body);
            TabDrawer.DrawTabs(body, tabs, 2, null);
            Rect inner = body.ContractedBy(12f);
            HeirsGame game = HeirsGame.Get;
            if (game == null)
            {
                return;
            }
            Rect view = new Rect(0f, 0f, inner.width - 18f, Mathf.Max(viewHeight, inner.height));
            Widgets.BeginScrollView(inner, ref scroll, view);
            float y = 0f;
            switch (section)
            {
                case Section.Heritage: y = DrawHeritage(view, game); break;
                case Section.Encyclopedia: y = HeirsAtlas.DrawEncyclopedia(view); break;
                case Section.Knowledge: y = DrawKnowledge(view, game); break;
                case Section.Research: y = HeirsAtlas.DrawResearch(view); break;
                case Section.Diplomacy: y = DrawDiplomacy(view); break;
                case Section.Routes: y = DrawRoutes(view, game); break;
                case Section.Council: y = DrawCouncil(view, game); break;
                case Section.Traditions: y = DrawTraditions(view); break;
                case Section.Stories: y = DrawStories(view, game); break;
                case Section.Chronicle: y = DrawChronicle(view, game); break;
            }
            viewHeight = y + 20f;
            Widgets.EndScrollView();
        }

        private static float Para(Rect view, float y, string text, GameFont font = GameFont.Small)
        {
            Text.Font = font;
            float h = Text.CalcHeight(text, view.width);
            Widgets.Label(new Rect(0f, y, view.width, h), text);
            Text.Font = GameFont.Small;
            return y + h + 6f;
        }

        private static void Icon(Rect r, NationDef nation)
        {
            if (nation == null) return;
            GUI.color = Color.white;
            GUI.DrawTexture(r, nation.Icon);
        }

        private float DrawHeritage(Rect view, HeirsGame game)
        {
            float y = Para(view, 0f, "HE_HeritageIntro".Translate());
            if (!game.heritageChosen)
            {
                y = Para(view, y, "HE_HeritageNotChosen".Translate());
                if (Widgets.ButtonText(new Rect(0f, y, 260f, 36f), "HE_ChooseHeritage".Translate()))
                {
                    Find.WindowStack.Add(new Dialog_ChooseHeritage());
                }
                return y + 44f;
            }
            if (game.heritage == null)
            {
                return Para(view, y, "HE_HeritageIndependent".Translate(), GameFont.Medium);
            }
            Icon(new Rect(0f, y, 64f, 64f), game.heritage);
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(76f, y + 4f, view.width - 76f, 32f), game.heritage.LabelCap);
            Text.Font = GameFont.Small;
            Widgets.Label(new Rect(76f, y + 36f, view.width - 76f, 24f), "HE_RulerTitle".Translate(game.heritage.rulerTitle));
            y += 72f;
            return Para(view, y, game.heritage.description);
        }

        private float DrawKnowledge(Rect view, HeirsGame game)
        {
            float y = Para(view, 0f, "HE_KnowledgeIntro".Translate());
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                float have = game.Knowledge(nation);
                List<ResearchProjectDef> locked = DefDatabase<ResearchProjectDef>.AllDefsListForReading
                    .Where(p => p.GetModExtension<HeirsResearchExt>()?.nation == nation && !p.IsFinished && p.GetModExtension<HeirsResearchExt>().knowledge > have)
                    .OrderBy(p => p.GetModExtension<HeirsResearchExt>().knowledge).ToList();
                float next = locked.Count > 0 ? locked[0].GetModExtension<HeirsResearchExt>().knowledge : Mathf.Max(have, 1f);
                Icon(new Rect(0f, y, 32f, 32f), nation);
                Widgets.Label(new Rect(40f, y + 5f, 220f, 24f), nation.LabelCap + (nation == game.heritage ? " (" + "HE_YourHeritage".Translate().Resolve() + ")" : ""));
                Rect bar = new Rect(270f, y + 6f, view.width - 520f, 20f);
                Widgets.FillableBar(bar, Mathf.Clamp01(have / next), BarTex(nation));
                Widgets.Label(new Rect(bar.xMax + 10f, y + 5f, 240f, 24f), locked.Count > 0 ? "HE_KnowledgeNext".Translate(have.ToString("0"), next.ToString("0"), locked[0].LabelCap) : "HE_KnowledgeAll".Translate(have.ToString("0")));
                y += 38f;
            }
            y = Para(view, y + 8f, "HE_KnowledgeSources".Translate());
            return DrawAges(view, y + 12f);
        }

        /// <summary>4.2: each nation's age, how far it is to the next, and (as a tooltip) what makes its pace.</summary>
        private float DrawAges(Rect view, float y)
        {
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_AgesHeading".Translate());
            Text.Font = GameFont.Small;
            Widgets.DrawLineHorizontal(0f, y + 30f, view.width);
            y = Para(view, y + 36f, HeirsAges.On ? "HE_AgesIntro".Translate() : "HE_AgesOff".Translate());
            if (!HeirsAges.On)
            {
                return y;
            }
            foreach (NationDef nation in HeirsWorld.LiveNations.ToList())
            {
                int age = HeirsAges.AgeOf(nation);
                Rect row = new Rect(0f, y, view.width, 34f);
                Widgets.DrawHighlightIfMouseover(row);
                Icon(new Rect(0f, y, 32f, 32f), nation);
                Widgets.Label(new Rect(40f, y + 5f, 220f, 24f), nation.LabelCap);
                Widgets.Label(new Rect(270f, y + 5f, 190f, 24f), HeirsAges.AgeLabel(age));
                Rect bar = new Rect(470f, y + 6f, view.width - 720f, 20f);
                Widgets.FillableBar(bar, HeirsAges.ToNext(nation), BarTex(nation));
                Widgets.Label(new Rect(bar.xMax + 10f, y + 5f, 240f, 24f),
                    age >= HeirsAges.LastAge ? "HE_AgesLast".Translate().Resolve() : "HE_AgesToward".Translate(HeirsAges.AgeLabel(age + 1), HeirsAges.ToNext(nation).ToStringPercent()).Resolve());
                // the tooltip is put together only while the mouse is over the row
                NationDef n = nation;
                TooltipHandler.TipRegion(row, new TipSignal(() => AgeTip(n), n.shortHash));
                y += 38f;
            }
            return y;
        }

        public static string AgeTip(NationDef nation)
        {
            var parts = new List<string>();
            float rate = HeirsAges.Rate(nation, parts);
            return "HE_AgesPace".Translate((rate * HeirsMod.Settings.ageSpeed).ToStringPercent()) + "\n\n" + string.Join("\n", parts)
                + "\n\n" + "HE_AgesItems".Translate(string.Join(", ", Enumerable.Range(2, HeirsAges.LastAge - 1).SelectMany(a => HeirsAges.AgeItems(nation, a)).Select(d => d.LabelCap.Resolve())));
        }

        private static readonly Dictionary<NationDef, Texture2D> barTex = new Dictionary<NationDef, Texture2D>();

        /// <summary>A nation's bar colour, made once. (Before 4.2.1 a new texture was made for every bar on every frame.)</summary>
        public static Texture2D BarTex(NationDef nation)
        {
            if (!barTex.TryGetValue(nation, out Texture2D tex) || tex == null)
            {
                tex = SolidColorMaterials.NewSolidColorTexture(nation.color);
                barTex[nation] = tex;
            }
            return tex;
        }

        private float DrawDiplomacy(Rect view)
        {
            HeirsWorld world = HeirsWorld.Get;
            float y = Para(view, 0f, HeirsMod.Settings.politics ? "HE_DiplomacyIntro".Translate() : "HE_DiplomacyOff".Translate());
            List<NationDef> nations = HeirsWorld.LiveNations.ToList();
            if (world == null || nations.Count == 0)
            {
                return Para(view, y, "HE_NoNations".Translate());
            }
            float cell = Mathf.Min(110f, (view.width - 220f) / (nations.Count + 1));
            Widgets.Label(new Rect(220f, y, cell, 24f), "HE_You".Translate());
            for (int i = 0; i < nations.Count; i++)
            {
                Icon(new Rect(220f + cell * (i + 1) + cell / 2f - 12f, y, 24f, 24f), nations[i]);
            }
            y += 30f;
            foreach (NationDef row in nations)
            {
                Icon(new Rect(0f, y, 24f, 24f), row);
                Widgets.Label(new Rect(30f, y + 2f, 190f, 24f), row.LabelCap);
                int pg = HeirsPolitics.PlayerGoodwill(row);
                GUI.color = HeirsWorld.FactionOf(row).HostileTo(Faction.OfPlayer) ? ColorLibrary.RedReadable : Color.white;
                Widgets.Label(new Rect(220f, y + 2f, cell, 24f), pg.ToStringWithSign());
                GUI.color = Color.white;
                for (int i = 0; i < nations.Count; i++)
                {
                    NationDef col = nations[i];
                    if (col == row) continue;
                    string text = world.AtWar(row, col) ? "HE_AtWar".Translate().Resolve() : world.Allied(row, col) ? "HE_Allied".Translate().Resolve() : HeirsWorld.Goodwill(row, col).ToStringWithSign();
                    GUI.color = world.AtWar(row, col) ? ColorLibrary.RedReadable : world.Allied(row, col) ? ColorLibrary.Green : Color.white;
                    Widgets.Label(new Rect(220f + cell * (i + 1), y + 2f, cell, 24f), text);
                    GUI.color = Color.white;
                }
                y += 30f;
            }
            return DrawCourts(view, y + 10f);
        }

        /// <summary>3.4: each nation's ruler, your title there and the treaties you hold or can sign.</summary>
        public static float DrawCourts(Rect view, float y)
        {
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_CourtsHeading".Translate());
            Text.Font = GameFont.Small;
            Widgets.DrawLineHorizontal(0f, y + 30f, view.width);
            y = Para(view, y + 36f, "HE_CourtsIntro".Translate() + "\n" + (HeirsTreaties.HasEmbassy() ? "HE_EmbassyYes" : "HE_EmbassyNo").Translate());
            float buttonW = Mathf.Min(150f, (view.width - 320f) / 4f - 6f);
            foreach (NationDef nation in HeirsWorld.LiveNations.ToList())
            {
                Reign reign = HeirsCourt.ReignOf(nation);
                Rect row = new Rect(0f, y, view.width, 64f);
                Widgets.DrawHighlightIfMouseover(row);
                Icon(new Rect(0f, y + 4f, 40f, 40f), nation);
                Widgets.Label(new Rect(48f, y + 2f, 270f, 24f), nation.LabelCap);
                Text.Font = GameFont.Tiny;
                Rect rulerRect = new Rect(48f, y + 24f, 270f, 20f);
                Widgets.Label(rulerRect, HeirsCourt.RulerLine(nation));
                if (reign != null)
                {
                    TooltipHandler.TipRegion(rulerRect, HeirsCourt.TemperamentText(reign.temperament) + "\n\n" + "HE_ReignYears".Translate(HeirsCourt.ReignYears(reign)));
                }
                Rect titleRect = new Rect(48f, y + 42f, 270f, 20f);
                GUI.color = HeirsTreaties.TitleRank(nation) >= 4 ? new Color(1f, 0.85f, 0.4f) : Color.gray;
                Widgets.Label(titleRect, "HE_YourTitle".Translate(HeirsTreaties.TitleLabel(nation)));
                GUI.color = Color.white;
                TooltipHandler.TipRegion(titleRect, "HE_TitleTip".Translate(nation.honoraryTitle ?? "", HeirsTreaties.HonourKnowledge));
                Text.Font = GameFont.Small;
                for (int i = 0; i < HeirsTreaties.Kinds.Length; i++)
                {
                    TreatyKind kind = HeirsTreaties.Kinds[i];
                    Rect b = new Rect(320f + i * (buttonW + 6f), y + 14f, buttonW, 32f);
                    string tip = HeirsTreaties.Label(kind) + "\n\n" + HeirsTreaties.Description(kind);
                    if (HeirsTreaties.Has(nation, kind))
                    {
                        GUI.color = new Color(0.6f, 1f, 0.6f);
                        if (Widgets.ButtonText(b, "✓ " + HeirsTreaties.Label(kind)))
                        {
                            NationDef n = nation;
                            Find.WindowStack.Add(Dialog_MessageBox.CreateConfirmation("HE_TreatyCancelConfirm".Translate(HeirsTreaties.Label(kind), n.LabelCap, HeirsTreaties.CancelPenalty, HeirsTreaties.OathBreakerPenalty),
                                () => HeirsTreaties.Cancel(n, kind, true), true));
                        }
                        GUI.color = Color.white;
                        tip += "\n\n" + "HE_TreatyClickCancel".Translate();
                    }
                    else
                    {
                        bool can = HeirsTreaties.CanSign(nation, kind, false, out string reason);
                        GUI.color = can ? Color.white : Color.gray;
                        if (Widgets.ButtonText(b, HeirsTreaties.Label(kind) + " (" + HeirsTreaties.Fee(kind) + ")") )
                        {
                            if (can) HeirsTreaties.Sign(nation, kind, false);
                            else Messages.Message(reason, MessageTypeDefOf.RejectInput, false);
                        }
                        GUI.color = Color.white;
                        tip += "\n\n" + "HE_TreatyFee".Translate(HeirsTreaties.Fee(kind), HeirsTreaties.MinGoodwill(kind))
                            + (HeirsTreaties.NeedsEmbassy(kind) ? "\n" + "HE_TreatyNeedsEmbassy".Translate().Resolve() : "")
                            + (can ? "" : "\n\n" + reason);
                    }
                    TooltipHandler.TipRegion(b, tip);
                }
                y += 70f;
            }
            return y;
        }

        private float DrawRoutes(Rect view, HeirsGame game)
        {
            float y = Para(view, 0f, "HE_RoutesIntro".Translate(HeirsRoutes.MinGoodwill, HeirsRoutes.IntervalDays, HeirsRoutes.Share.ToStringPercent()));
            if (!HeirsRoutes.Enabled)
            {
                return Para(view, y, "HE_RouteDisabled".Translate());
            }
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_RoutesOpen".Translate(game.routes.Count, HeirsRoutes.MaxRoutes));
            Text.Font = GameFont.Small;
            y += 34f;
            if (game.routes.Count == 0)
            {
                y = Para(view, y, "HE_RoutesNone".Translate());
            }
            foreach (TradeRoute route in game.routes.ToList())
            {
                Rect row = new Rect(0f, y, view.width, 34f);
                Widgets.DrawHighlightIfMouseover(row);
                Icon(new Rect(0f, y + 3f, 28f, 28f), route.nation);
                Widgets.Label(new Rect(36f, y + 6f, 200f, 24f), route.nation.LabelCap);
                float days = Mathf.Max(0f, (route.nextTick - Find.TickManager.TicksGame) / (float)GenDate.TicksPerDay);
                string info = "HE_RouteInfo".Translate(days.ToString("0.0"), HeirsRoutes.CaravanValue(route), route.trips, route.raids);
                if (HeirsRoutes.AtWar(route.nation)) info += "  " + "HE_RouteWarRisk".Translate().Resolve();
                Widgets.Label(new Rect(240f, y + 6f, view.width - 400f, 24f), info);
                if (Widgets.ButtonText(new Rect(view.width - 150f, y + 2f, 150f, 30f), "HE_RouteClose".Translate()))
                {
                    TradeRoute local = route;
                    Find.WindowStack.Add(Dialog_MessageBox.CreateConfirmation("HE_RouteCloseConfirm".Translate(route.nation.LabelCap),
                        () => HeirsRoutes.Close(game, local, "HE_RouteClosedByPlayer"), destructive: true));
                }
                y += 38f;
            }
            y += 10f;
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_RoutesAvailable".Translate());
            Text.Font = GameFont.Small;
            y += 34f;
            foreach (NationDef nation in HeirsWorld.LiveNations.Where(n => HeirsRoutes.RouteTo(game, n) == null))
            {
                Rect row = new Rect(0f, y, view.width, 34f);
                Widgets.DrawHighlightIfMouseover(row);
                Icon(new Rect(0f, y + 3f, 28f, 28f), nation);
                Widgets.Label(new Rect(36f, y + 6f, 200f, 24f), nation.LabelCap);
                bool can = HeirsRoutes.CanOpen(game, nation, out string why);
                float dist = HeirsRoutes.Distance(nation);
                string info = "HE_RouteOffer".Translate(HeirsRoutes.Cost(nation), dist < 0f ? "?" : dist.ToString("0"), HeirsPolitics.PlayerGoodwill(nation).ToStringWithSign());
                GUI.color = can ? Color.white : Color.gray;
                Widgets.Label(new Rect(240f, y + 6f, view.width - 400f, 24f), can ? info : info + "  (" + why + ")");
                GUI.color = Color.white;
                if (Widgets.ButtonText(new Rect(view.width - 150f, y + 2f, 150f, 30f), "HE_RouteOpen".Translate(), active: can) && can)
                {
                    HeirsRoutes.Open(game, nation);
                }
                y += 38f;
            }
            return y;
        }

        private float DrawCouncil(Rect view, HeirsGame game)
        {
            float y = Para(view, 0f, "HE_CouncilIntro".Translate(HeirsCouncil.ChainsToUnlock, HeirsCouncil.RoutesToUnlock, HeirsCouncil.YesGoodwill, HeirsCouncil.MeetingIntervalDays));
            if (!HeirsCouncil.Enabled)
            {
                return Para(view, y, "HE_CouncilDisabled".Translate());
            }
            if (game.councilWon != null)
            {
                y = Para(view, y, ("HE_Victory" + game.councilWon + "Label").Translate(), GameFont.Medium);
                return Para(view, y, "HE_CouncilWonNote".Translate());
            }
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_CouncilProgress".Translate());
            Text.Font = GameFont.Small;
            y += 34f;
            y = Para(view, y, (game.councilUnlocked ? "✓ " : "· ") + "HE_CouncilStepUnlock".Translate(HeirsCouncil.ChainsDone(game), HeirsCouncil.ChainsToUnlock, HeirsCouncil.OldRoutes(game), HeirsCouncil.RoutesToUnlock).Resolve());
            bool hallBuilt = HeirsCouncil.HallBuilt();
            y = Para(view, y, (hallBuilt ? "✓ " : "· ") + "HE_CouncilStepHall".Translate().Resolve());
            bool can = HeirsCouncil.CanMeet(game, out string why);
            if (Widgets.ButtonText(new Rect(0f, y, 300f, 36f), "HE_CouncilCall".Translate(), active: can) && can)
            {
                HeirsCouncil.Meet(game);
            }
            if (!can)
            {
                GUI.color = Color.gray;
                Widgets.Label(new Rect(312f, y + 8f, view.width - 312f, 24f), why);
                GUI.color = Color.white;
            }
            y += 46f;
            List<NationDef> living = HeirsWorld.LiveNations.ToList();
            int yes = 0;
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_CouncilVotes".Translate());
            Text.Font = GameFont.Small;
            y += 34f;
            foreach (NationDef nation in living)
            {
                bool v = HeirsCouncil.Vote(game, nation, out string reason);
                if (v) yes++;
                Icon(new Rect(0f, y + 2f, 24f, 24f), nation);
                Widgets.Label(new Rect(32f, y + 3f, 200f, 24f), nation.LabelCap);
                GUI.color = v ? ColorLibrary.Green : ColorLibrary.RedReadable;
                Widgets.Label(new Rect(236f, y + 3f, 80f, 24f), (v ? "HE_VoteYes" : "HE_VoteNo").Translate());
                GUI.color = Color.white;
                Text.Font = GameFont.Tiny;
                Widgets.Label(new Rect(320f, y + 5f, view.width - 320f, 24f), reason + (HeirsCouncil.IsVassal(game, nation) ? "" : "  · " + "HE_CouncilSettlements".Translate(HeirsCouncil.Settlements(nation)).Resolve()));
                Text.Font = GameFont.Small;
                y += 30f;
            }
            y += 6f;
            y = Para(view, y, "HE_CouncilTally".Translate(yes, living.Count, HeirsCouncil.YesNeeded(living.Count)));
            return Para(view, y, "HE_CouncilDominion".Translate(game.vassals.Count, living.Count));
        }

        private float DrawTraditions(Rect view)
        {
            float y = Para(view, 0f, "HE_TraditionsIntro".Translate());
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                List<ResearchProjectDef> list = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Where(p => p.GetModExtension<HeirsResearchExt>() is HeirsResearchExt e && e.tradition && e.nation == nation).ToList();
                if (list.Count == 0) continue;
                Icon(new Rect(0f, y, 28f, 28f), nation);
                Text.Font = GameFont.Medium;
                Widgets.Label(new Rect(36f, y, view.width, 30f), nation.LabelCap + (HeirsMod.Settings.TraditionsEnabled(nation) ? "" : " (" + "HE_PatchOff".Translate().Resolve() + ")"));
                Text.Font = GameFont.Small;
                y += 34f;
                foreach (ResearchProjectDef p in list)
                {
                    bool on = HeirsTraditions.Active(p);
                    GUI.color = on ? Color.white : Color.gray;
                    Widgets.Label(new Rect(16f, y, 260f, 24f), (on ? "✓ " : "· ") + p.LabelCap);
                    string effect = p.GetModExtension<HeirsResearchExt>().stats.Count > 0 || on ? EffectText(p) : "";
                    Text.Font = GameFont.Tiny;
                    float h = Mathf.Max(24f, Text.CalcHeight(effect, view.width - 290f));
                    Widgets.Label(new Rect(280f, y + 3f, view.width - 290f, h), effect);
                    Text.Font = GameFont.Small;
                    GUI.color = Color.white;
                    y += h + 2f;
                }
                y += 8f;
            }
            return y;
        }

        public static string EffectText(ResearchProjectDef p)
        {
            HeirsResearchExt e = p?.GetModExtension<HeirsResearchExt>();
            if (e == null)
            {
                return string.Empty;
            }
            var parts = new List<string>();
            foreach (StatEffect s in e.stats)
            {
                string v = s.offset != 0f ? s.offset.ToStringByStyle(s.stat.toStringStyle, ToStringNumberSense.Offset) : "x" + s.factor.ToStringPercent();
                parts.Add(s.stat.LabelCap + " " + v + (s.scope == EffectScope.PlayerBuildings ? " (" + "HE_ScopeBuildings".Translate().Resolve() + ")" : ""));
            }
            if (e.qualityChance > 0f) parts.Add("HE_EffectQuality".Translate(e.qualityChance.ToStringPercent()));
            if (e.caravanSpeed > 0f) parts.Add("HE_EffectCaravan".Translate(e.caravanSpeed.ToStringPercent()));
            if (e.studyFactor > 0f) parts.Add("HE_EffectStudy".Translate(e.studyFactor.ToStringPercent()));
            return string.Join(", ", parts);
        }

        private float DrawStories(Rect view, HeirsGame game)
        {
            float y = Para(view, 0f, "HE_StoriesIntro".Translate());
            y = DrawErrands(view, game, y);
            foreach (ChainDef chain in HeirsChains.All)
            {
                ChainState state = game.State(chain);
                Icon(new Rect(0f, y, 28f, 28f), chain.nation);
                Text.Font = GameFont.Medium;
                Widgets.Label(new Rect(36f, y, view.width, 30f), chain.LabelCap);
                Text.Font = GameFont.Small;
                y += 34f;
                string text = state.done ? "HE_ChainDone".Translate().Resolve()
                    : !state.started && chain.after != null && !game.State(chain.after).done ? "HE_ChainAfter".Translate(chain.after.LabelCap).Resolve()
                    : !state.started ? "HE_ChainLocked".Translate(chain.startKnowledge.ToString("0"), chain.nation.adjective).Resolve()
                    : HeirsChains.Goal(chain, state);
                y = Para(new Rect(16f, 0f, view.width - 16f, 0f), y, text);
                ChainStep step = HeirsChains.Current(chain, state);
                if (step != null && step.kind == StepKind.Deliver)
                {
                    bool can = HeirsChains.CanDeliver(chain, state);
                    if (Widgets.ButtonText(new Rect(16f, y, 220f, 32f), "HE_Deliver".Translate(), active: can) && can)
                    {
                        HeirsChains.Deliver(game, chain);
                    }
                    y += 40f;
                }
                y += 10f;
            }
            return y;
        }

        /// <summary>3.5: the favours you promised, each with its reward, time left and a deliver button.</summary>
        public static float DrawErrands(Rect view, HeirsGame game, float y)
        {
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), "HE_ErrandsHeading".Translate());
            Text.Font = GameFont.Small;
            y += 32f;
            if (game.errands.Count == 0)
            {
                return Para(view, y, "HE_ErrandsNone".Translate(game.errandsDone)) + 10f;
            }
            foreach (Errand e in game.errands.ToList())
            {
                Icon(new Rect(0f, y, 28f, 28f), e.nation);
                string line = "HE_ErrandLine".Translate(e.nation.LabelCap, e.Want, e.DaysLeft, e.silver, e.knowledge.ToString("0")).Resolve();
                Widgets.Label(new Rect(36f, y + 4f, view.width - 270f, 28f), line);
                bool can = HeirsErrands.CanDeliver(e);
                Rect button = new Rect(view.width - 220f, y, 210f, 30f);
                TooltipHandler.TipRegion(button, can ? "HE_ErrandReady".Translate() : "HE_ErrandMissing".Translate());
                if (Widgets.ButtonText(button, "HE_Deliver".Translate(), active: can) && can)
                {
                    HeirsErrands.Deliver(e);
                }
                y += 36f;
            }
            return y + 14f;
        }

        private float DrawChronicle(Rect view, HeirsGame game)
        {
            float y = Para(view, 0f, "HE_ChronicleIntro".Translate());
            Vector2 longLat = Find.WorldGrid.LongLatOf(Find.AnyPlayerHomeMap?.Tile ?? 0);
            for (int i = game.chronicle.Count - 1; i >= 0; i--)
            {
                ChronicleEntry e = game.chronicle[i];
                string date = GenDate.DateFullStringAt(e.tick, longLat);
                Text.Font = GameFont.Tiny;
                GUI.color = Color.gray;
                Widgets.Label(new Rect(0f, y, 200f, 22f), date);
                GUI.color = Color.white;
                Text.Font = GameFont.Small;
                float h = Mathf.Max(22f, Text.CalcHeight(e.text, view.width - 210f));
                Widgets.Label(new Rect(210f, y, view.width - 210f, h), e.text);
                y += h + 4f;
            }
            return y;
        }
    }

    public class Dialog_ChooseHeritage : Window
    {
        public override Vector2 InitialSize => new Vector2(620f, 640f);

        public Dialog_ChooseHeritage()
        {
            doCloseX = true;
            forcePause = true;
            absorbInputAroundWindow = true;
        }

        public override void DoWindowContents(Rect inRect)
        {
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, 0f, inRect.width, 34f), "HE_ChooseHeritage".Translate());
            Text.Font = GameFont.Small;
            Widgets.Label(new Rect(0f, 36f, inRect.width, 44f), "HE_ChooseHeritageWarn".Translate());
            float y = 86f;
            foreach (NationDef nation in DefDatabase<NationDef>.AllDefsListForReading)
            {
                Rect row = new Rect(0f, y, inRect.width, 48f);
                Widgets.DrawHighlightIfMouseover(row);
                GUI.DrawTexture(new Rect(4f, y + 4f, 40f, 40f), nation.Icon);
                Widgets.Label(new Rect(54f, y + 4f, inRect.width - 180f, 40f), nation.LabelCap + "\n" + "HE_RulerTitle".Translate(nation.rulerTitle));
                if (Widgets.ButtonText(new Rect(inRect.width - 120f, y + 8f, 116f, 32f), "HE_Choose".Translate()))
                {
                    HeirsGame.Get?.SetHeritage(nation);
                    Close();
                }
                y += 52f;
            }
            if (Widgets.ButtonText(new Rect(0f, y + 8f, inRect.width, 36f), "HE_ChooseIndependent".Translate()))
            {
                HeirsGame.Get?.SetHeritage(null);
                HeirsStart.IndependentBonus();
                Close();
            }
        }
    }
}
