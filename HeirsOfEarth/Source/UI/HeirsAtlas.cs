using System.Collections.Generic;
using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;
using Verse.Sound;

namespace HeirsOfEarth
{
    /// <summary>3.1: the research browser (filters by nation, age and state) and the nation encyclopedia of the Heirs tab.</summary>
    public static class HeirsAtlas
    {
        public enum ResearchState { All, Available, Locked, Finished }

        // Research browser filters; null nation with commonOnly false means "all".
        public static NationDef filterNation;
        public static bool filterCommon;
        public static TechLevel filterAge = TechLevel.Undefined;
        public static ResearchState filterState = ResearchState.All;

        public static NationDef encyclopediaNation;

        private static List<ResearchProjectDef> allProjects;

        public static List<ResearchProjectDef> AllProjects
        {
            get
            {
                if (allProjects == null)
                {
                    allProjects = DefDatabase<ResearchProjectDef>.AllDefsListForReading
                        .Where(p => p.HasModExtension<HeirsResearchExt>() || p.tab == HeirsDefOf.HE_WorldHeritage)
                        .OrderBy(p => p.GetModExtension<HeirsResearchExt>()?.nation?.index ?? -1)
                        .ThenBy(p => (int)p.techLevel)
                        .ThenBy(p => p.baseCost)
                        .ThenBy(p => p.label)
                        .ToList();
                }
                return allProjects;
            }
        }

        public static NationDef NationOf(ResearchProjectDef p)
        {
            return p.GetModExtension<HeirsResearchExt>()?.nation;
        }

        public static ResearchState StateOf(ResearchProjectDef p)
        {
            if (p.IsFinished) return ResearchState.Finished;
            return p.CanStartNow ? ResearchState.Available : ResearchState.Locked;
        }

        /// <summary>The projects that pass the current filters, in display order.</summary>
        public static List<ResearchProjectDef> Filtered()
        {
            return AllProjects.Where(p =>
            {
                NationDef n = NationOf(p);
                if (filterCommon && n != null) return false;
                if (!filterCommon && filterNation != null && n != filterNation) return false;
                if (filterAge != TechLevel.Undefined && p.techLevel != filterAge) return false;
                return filterState == ResearchState.All || StateOf(p) == filterState;
            }).ToList();
        }

        /// <summary>Why a project cannot start yet, in one line.</summary>
        public static string LockReason(ResearchProjectDef p)
        {
            HeirsGame game = HeirsGame.Get;
            if (game != null && !game.CanStart(p, out string why) && !why.NullOrEmpty())
            {
                return why;
            }
            List<ResearchProjectDef> missing = (p.prerequisites ?? new List<ResearchProjectDef>()).Concat(p.hiddenPrerequisites ?? new List<ResearchProjectDef>())
                .Where(q => !q.IsFinished).ToList();
            if (missing.Count > 0)
            {
                return "HE_AtlasNeeds".Translate(string.Join(", ", missing.Select(q => q.LabelCap.Resolve())));
            }
            if (p.requiredResearchBuilding != null)
            {
                return "HE_AtlasNeedsBench".Translate(p.requiredResearchBuilding.LabelCap);
            }
            return "HE_AtlasLocked".Translate();
        }

        private static string AgeLabel(TechLevel t)
        {
            return t == TechLevel.Undefined ? "HE_AtlasAllAges".Translate().Resolve() : t.ToStringHuman().CapitalizeFirst();
        }

        private static string NationFilterLabel()
        {
            if (filterCommon) return "HE_AtlasCommon".Translate();
            return filterNation == null ? "HE_AtlasAllNations".Translate().Resolve() : filterNation.LabelCap.Resolve();
        }

        public static float DrawResearch(Rect view)
        {
            float y = Para(view, 0f, "HE_AtlasIntro".Translate());
            float x = 0f;
            if (Widgets.ButtonText(new Rect(x, y, 220f, 30f), NationFilterLabel()))
            {
                var opts = new List<FloatMenuOption>
                {
                    new FloatMenuOption("HE_AtlasAllNations".Translate(), () => { filterNation = null; filterCommon = false; }),
                    new FloatMenuOption("HE_AtlasCommon".Translate(), () => { filterNation = null; filterCommon = true; }),
                };
                foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
                {
                    NationDef local = n;
                    opts.Add(new FloatMenuOption(n.LabelCap, () => { filterNation = local; filterCommon = false; }, n.Icon, Color.white));
                }
                Find.WindowStack.Add(new FloatMenu(opts));
            }
            x += 228f;
            if (Widgets.ButtonText(new Rect(x, y, 170f, 30f), AgeLabel(filterAge)))
            {
                var opts = new List<FloatMenuOption>();
                foreach (TechLevel t in new[] { TechLevel.Undefined, TechLevel.Neolithic, TechLevel.Medieval, TechLevel.Industrial, TechLevel.Spacer })
                {
                    if (t != TechLevel.Undefined && !AllProjects.Any(p => p.techLevel == t)) continue;
                    TechLevel local = t;
                    opts.Add(new FloatMenuOption(AgeLabel(t), () => filterAge = local));
                }
                Find.WindowStack.Add(new FloatMenu(opts));
            }
            x += 178f;
            foreach (ResearchState s in System.Enum.GetValues(typeof(ResearchState)))
            {
                Rect r = new Rect(x, y, 112f, 30f);
                if (filterState == s) Widgets.DrawBoxSolid(r, new Color(1f, 1f, 1f, 0.12f));
                if (Widgets.ButtonText(r, ("HE_AtlasState" + s).Translate(), drawBackground: filterState != s))
                {
                    filterState = s;
                }
                x += 116f;
            }
            y += 38f;

            List<ResearchProjectDef> list = Filtered();
            int done = list.Count(p => p.IsFinished);
            GUI.color = Color.gray;
            Widgets.Label(new Rect(0f, y, view.width, 24f), "HE_AtlasCount".Translate(list.Count, done));
            GUI.color = Color.white;
            y += 26f;
            if (list.Count == 0)
            {
                return Para(view, y, "HE_AtlasEmpty".Translate());
            }
            foreach (ResearchProjectDef p in list)
            {
                y = DrawProjectRow(view, y, p);
            }
            return y;
        }

        private static float DrawProjectRow(Rect view, float y, ResearchProjectDef p)
        {
            const float h = 44f;
            Rect row = new Rect(0f, y, view.width, h);
            NationDef nation = NationOf(p);
            ResearchState state = StateOf(p);
            bool current = Find.ResearchManager.IsCurrentProject(p);
            if (nation != null)
            {
                Widgets.DrawBoxSolid(new Rect(0f, y + 2f, 4f, h - 4f), nation.color);
            }
            if (current) Widgets.DrawHighlightSelected(row);
            else Widgets.DrawHighlightIfMouseover(row);
            if (nation != null)
            {
                GUI.DrawTexture(new Rect(10f, y + 8f, 28f, 28f), nation.Icon);
            }
            HeirsResearchExt ext = p.GetModExtension<HeirsResearchExt>();
            string title = p.LabelCap + (ext != null && ext.tradition ? "  · " + "HE_AtlasTradition".Translate().Resolve() : "");
            GUI.color = state == ResearchState.Locked ? Color.gray : Color.white;
            Widgets.Label(new Rect(46f, y + 2f, 330f, 22f), title);
            Text.Font = GameFont.Tiny;
            string sub = AgeLabel(p.techLevel) + " · " + p.CostApparent.ToString("0");
            if (ext != null && ext.nation != null && ext.knowledge > 0f) sub += " · " + "HE_AtlasKnowledge".Translate(ext.knowledge.ToString("0")).Resolve();
            Widgets.Label(new Rect(46f, y + 23f, 330f, 20f), sub);
            GUI.color = Color.white;

            Rect info = new Rect(384f, y + 4f, view.width - 384f - 160f, h - 8f);
            if (state == ResearchState.Finished)
            {
                GUI.color = ColorLibrary.Green;
                Widgets.Label(info, "HE_AtlasDone".Translate());
            }
            else if (state == ResearchState.Locked)
            {
                GUI.color = ColorLibrary.RedReadable;
                Widgets.Label(info, LockReason(p));
            }
            else
            {
                Widgets.FillableBar(new Rect(info.x, info.y + 10f, Mathf.Min(220f, info.width), 14f), p.ProgressPercent);
                string effect = MainTabWindow_Heirs.EffectText(p);
                if (!effect.NullOrEmpty())
                {
                    Widgets.Label(new Rect(info.x + 230f, info.y, info.width - 230f, info.height), effect);
                }
            }
            GUI.color = Color.white;
            Text.Font = GameFont.Small;

            Rect button = new Rect(view.width - 150f, y + 7f, 150f, 30f);
            if (current)
            {
                Widgets.Label(new Rect(button.x + 10f, button.y + 5f, button.width, 24f), "HE_AtlasCurrent".Translate());
            }
            else if (state == ResearchState.Available && Widgets.ButtonText(button, "HE_AtlasResearch".Translate()))
            {
                Find.ResearchManager.SetCurrentProject(p);
                SoundDefOf.ResearchStart.PlayOneShotOnCamera();
            }
            TooltipHandler.TipRegion(row, p.description + (ext != null && !MainTabWindow_Heirs.EffectText(p).NullOrEmpty() ? "\n\n" + MainTabWindow_Heirs.EffectText(p) : ""));
            return y + h + 2f;
        }

        // ------------------------------------------------------------------ encyclopedia

        public enum EntryKind { Building, Weapon, Apparel, Food, Item, Floor }

        private static Dictionary<NationDef, Dictionary<EntryKind, List<Def>>> entries;

        /// <summary>Everything a nation brings, grouped for the encyclopedia. Things carry HeirsCultureExt; floors use the nation's defName prefix.</summary>
        public static Dictionary<EntryKind, List<Def>> EntriesOf(NationDef nation)
        {
            if (entries == null)
            {
                entries = new Dictionary<NationDef, Dictionary<EntryKind, List<Def>>>();
            }
            if (!entries.TryGetValue(nation, out var groups))
            {
                groups = new Dictionary<EntryKind, List<Def>>();
                foreach (EntryKind k in System.Enum.GetValues(typeof(EntryKind)))
                {
                    groups[k] = new List<Def>();
                }
                string prefix = nation.defName + "_";
                foreach (ThingDef t in DefDatabase<ThingDef>.AllDefsListForReading)
                {
                    if (t.GetModExtension<HeirsCultureExt>()?.nation != nation || t.IsBlueprint || t.IsFrame) continue;
                    EntryKind k = t.category == ThingCategory.Building ? EntryKind.Building
                        : t.IsWeapon ? EntryKind.Weapon
                        : t.IsApparel ? EntryKind.Apparel
                        : t.IsIngestible ? EntryKind.Food
                        : EntryKind.Item;
                    groups[k].Add(t);
                }
                foreach (TerrainDef t in DefDatabase<TerrainDef>.AllDefsListForReading)
                {
                    if (t.defName.StartsWith(prefix)) groups[EntryKind.Floor].Add(t);
                }
                foreach (var list in groups.Values)
                {
                    list.SortBy(d => d.label);
                }
                entries[nation] = groups;
            }
            return groups;
        }

        public static float DrawEncyclopedia(Rect view)
        {
            List<NationDef> nations = DefDatabase<NationDef>.AllDefsListForReading;
            if (encyclopediaNation == null)
            {
                encyclopediaNation = HeirsGame.Get?.heritage ?? nations.FirstOrDefault();
            }
            float y = Para(view, 0f, "HE_EncyclopediaIntro".Translate());
            float cell = Mathf.Min(96f, view.width / nations.Count);
            for (int i = 0; i < nations.Count; i++)
            {
                NationDef n = nations[i];
                Rect r = new Rect(i * cell, y, cell - 4f, 62f);
                if (n == encyclopediaNation) Widgets.DrawHighlightSelected(r);
                else Widgets.DrawHighlightIfMouseover(r);
                GUI.DrawTexture(new Rect(r.center.x - 18f, r.y + 3f, 36f, 36f), n.Icon);
                Text.Font = GameFont.Tiny;
                Text.Anchor = TextAnchor.UpperCenter;
                Widgets.Label(new Rect(r.x, r.y + 41f, r.width, 20f), n.LabelCap.Resolve().Truncate(r.width));
                Text.Anchor = TextAnchor.UpperLeft;
                Text.Font = GameFont.Small;
                if (Widgets.ButtonInvisible(r))
                {
                    encyclopediaNation = n;
                    SoundDefOf.Tick_High.PlayOneShotOnCamera();
                }
            }
            y += 72f;
            return DrawNation(view, y, encyclopediaNation);
        }

        private static float Heading(Rect view, float y, string text)
        {
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(0f, y, view.width, 30f), text);
            Text.Font = GameFont.Small;
            Widgets.DrawLineHorizontal(0f, y + 30f, view.width);
            return y + 36f;
        }

        /// <summary>3.3: how the nation makes war and the animals it keeps, for its encyclopedia page.</summary>
        public static string WarText(NationDef nation)
        {
            var lines = new List<string>();
            RaidDoctrine d = nation.doctrine;
            if (d != null && !d.label.NullOrEmpty())
            {
                string drill = d.hediff?.stages == null ? "" : string.Join("; ", d.hediff.stages.Select(st => st.SpecialDisplayStats().Select(e => e.LabelCap + " " + e.ValueString))
                    .Where(x => x.Any()).Select(x => string.Join(", ", x)).DefaultIfEmpty("").Last());
                lines.Add(d.label.CapitalizeFirst() + ": " + d.description + (drill.NullOrEmpty() ? "" : " (" + drill + ")"));
            }
            Reign reign = HeirsCourt.ReignOf(nation);
            if (reign != null)
            {
                lines.Add("HE_AtlasRuler".Translate() + ": " + HeirsCourt.RulerLine(nation) + " (" + HeirsCourt.TemperamentText(reign.temperament) + ")");
            }
            if (nation.animal != null)
            {
                lines.Add("HE_AtlasAnimal".Translate() + ": " + nation.animal.LabelCap);
            }
            if (HeirsAges.On && HeirsWorld.FactionOf(nation) != null)
            {
                int age = HeirsAges.AgeOf(nation);
                lines.Add("HE_AtlasAge".Translate() + ": " + HeirsAges.AgeLabel(age)
                          + (age < 3 ? " (" + "HE_AgesToward".Translate(HeirsAges.AgeLabel(age + 1), HeirsAges.ToNext(nation).ToStringPercent()).Resolve() + ")" : ""));
            }
            return string.Join("\n", lines);
        }

        private static float DrawNation(Rect view, float y, NationDef nation)
        {
            HeirsGame game = HeirsGame.Get;
            Widgets.DrawBoxSolid(new Rect(0f, y, view.width, 4f), nation.color);
            y += 10f;
            GUI.DrawTexture(new Rect(0f, y, 80f, 80f), nation.Icon);
            Text.Font = GameFont.Medium;
            Widgets.Label(new Rect(92f, y + 2f, view.width - 92f, 32f), nation.LabelCap);
            Text.Font = GameFont.Small;
            Faction faction = HeirsWorld.FactionOf(nation);
            string status = faction == null || faction.defeated ? "HE_EncyclopediaGone".Translate().Resolve()
                : "HE_EncyclopediaRelations".Translate(HeirsPolitics.PlayerGoodwill(nation).ToStringWithSign(), faction.PlayerRelationKind.GetLabelCap()).Resolve();
            Widgets.Label(new Rect(92f, y + 34f, view.width - 92f, 24f), "HE_RulerTitle".Translate(nation.rulerTitle) + "  ·  " + status);
            if (game != null)
            {
                List<ResearchProjectDef> own = AllProjects.Where(p => NationOf(p) == nation).ToList();
                Widgets.Label(new Rect(92f, y + 58f, view.width - 92f, 24f), "HE_EncyclopediaProgress".Translate(game.Knowledge(nation).ToString("0"), own.Count(p => p.IsFinished), own.Count,
                    nation == game.heritage ? "HE_YourHeritage".Translate().Resolve() : ""));
            }
            y += 92f;
            y = Para(view, y, nation.description);

            y = Heading(view, y, "HE_EncyclopediaNeighbours".Translate());
            string friends = nation.friends.Count == 0 ? "-" : string.Join(", ", DefDatabase<NationDef>.AllDefsListForReading.Where(o => o != nation && nation.IsFriendOf(o)).Select(o => o.LabelCap.Resolve()));
            string rivals = string.Join(", ", DefDatabase<NationDef>.AllDefsListForReading.Where(o => o != nation && nation.IsRivalOf(o)).Select(o => o.LabelCap.Resolve()));
            y = Para(view, y, "HE_EncyclopediaFriends".Translate(friends.NullOrEmpty() ? "-" : friends, rivals.NullOrEmpty() ? "-" : rivals));
            y = Para(view, y, "HE_EncyclopediaHowTo".Translate(nation.adjective));
            string war = WarText(nation);
            if (!war.NullOrEmpty())
            {
                y = Heading(view, y, "HE_AtlasDoctrine".Translate());
                y = Para(view, y, war);
            }

            var groups = EntriesOf(nation);
            foreach (EntryKind k in System.Enum.GetValues(typeof(EntryKind)))
            {
                List<Def> list = groups[k];
                if (list.Count == 0) continue;
                y = Heading(view, y, ("HE_Encyclopedia" + k).Translate(list.Count));
                y = DrawDefGrid(view, y, list);
            }

            List<ResearchProjectDef> traditions = AllProjects.Where(p => NationOf(p) == nation && p.GetModExtension<HeirsResearchExt>().tradition).ToList();
            if (traditions.Count > 0)
            {
                y = Heading(view, y, "HE_EncyclopediaTraditions".Translate(traditions.Count));
                foreach (ResearchProjectDef p in traditions)
                {
                    bool on = HeirsTraditions.Active(p);
                    GUI.color = on ? Color.white : Color.gray;
                    Widgets.Label(new Rect(8f, y, 270f, 24f), (on ? "✓ " : "· ") + p.LabelCap);
                    Text.Font = GameFont.Tiny;
                    string effect = MainTabWindow_Heirs.EffectText(p);
                    float h = Mathf.Max(24f, Text.CalcHeight(effect, view.width - 290f));
                    Widgets.Label(new Rect(280f, y + 3f, view.width - 290f, h), effect);
                    Text.Font = GameFont.Small;
                    GUI.color = Color.white;
                    y += h + 2f;
                }
                y += 6f;
            }

            List<ChainDef> chains = HeirsChains.All.Where(c => c.nation == nation).ToList();
            if (chains.Count > 0)
            {
                y = Heading(view, y, "HE_EncyclopediaStories".Translate());
                foreach (ChainDef chain in chains)
                {
                    ChainState state = game?.State(chain);
                    string line = chain.LabelCap + ": " + (state == null || !state.started ? "HE_ChainLocked".Translate(chain.startKnowledge.ToString("0"), nation.adjective).Resolve()
                        : state.done ? "HE_ChainDone".Translate().Resolve() : "HE_EncyclopediaChainOn".Translate().Resolve());
                    y = Para(view, y, line);
                    if (chain.artifact != null)
                    {
                        y = DrawDefGrid(view, y, new List<Def> { chain.artifact });
                    }
                }
            }
            return y;
        }

        private static float DrawDefGrid(Rect view, float y, List<Def> defs)
        {
            const float w = 210f, h = 40f;
            int per = Mathf.Max(1, (int)(view.width / w));
            for (int i = 0; i < defs.Count; i++)
            {
                Def d = defs[i];
                Rect r = new Rect((i % per) * w, y + (i / per) * h, w - 6f, h - 4f);
                Widgets.DrawHighlightIfMouseover(r);
                Rect iconRect = new Rect(r.x + 2f, r.y + 2f, 32f, 32f);
                if (d is ThingDef td) Widgets.ThingIcon(iconRect, td);
                else if (d is TerrainDef terrain) Widgets.DefIcon(iconRect, terrain);
                Text.Anchor = TextAnchor.MiddleLeft;
                Widgets.Label(new Rect(r.x + 40f, r.y, r.width - 40f, r.height), d.LabelCap.Resolve().Truncate(r.width - 44f));
                Text.Anchor = TextAnchor.UpperLeft;
                TooltipHandler.TipRegion(r, d.LabelCap + "\n\n" + d.description + "\n\n" + "HE_EncyclopediaInfoTip".Translate());
                if (Widgets.ButtonInvisible(r))
                {
                    Find.WindowStack.Add(new Dialog_InfoCard(d));
                }
            }
            return y + Mathf.CeilToInt(defs.Count / (float)per) * h + 8f;
        }

        private static float Para(Rect view, float y, string text)
        {
            float h = Text.CalcHeight(text, view.width);
            Widgets.Label(new Rect(0f, y, view.width, h), text);
            return y + h + 6f;
        }
    }
}
