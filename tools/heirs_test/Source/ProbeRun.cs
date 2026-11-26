using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>Drives every Heirs of Earth system once, saves, reloads, strips the mod's data from the save, then reports and quits.</summary>
    public class GameComponent_HeProbe : GameComponent
    {
        private const string SaveName = "HeProbeSave";
        private const float WatchdogSeconds = 1200f;
        private static int phase;
        private static float savedRoma;
        private static int savedChronicle;
        private static NationDef savedHeritage;
        private static int missingTex;

        private List<KeyValuePair<string, Func<bool>>> steps;
        private int index;
        private int frames;
        private int tries;

        public GameComponent_HeProbe(Game game)
        {
            P.Hook();
            P.inGame = true;
        }

        private void Add(string name, Action action) => steps.Add(new KeyValuePair<string, Func<bool>>(name, () => { action(); return true; }));

        public override void GameComponentUpdate()
        {
            if (P.finished || Find.CurrentMap == null || LongEventHandler.AnyEventNowOrWaiting)
            {
                return;
            }
            if (Time.realtimeSinceStartup > WatchdogSeconds)
            {
                P.Check("watchdog", false, "test ran too long at step " + index);
                Finish();
                return;
            }
            if (steps == null)
            {
                steps = new List<KeyValuePair<string, Func<bool>>>();
                Build();
            }
            if (++frames < 10 || index >= steps.Count)
            {
                return;
            }
            frames = 0;
            KeyValuePair<string, Func<bool>> step = steps[index];
            bool done = true;
            try
            {
                done = step.Value();
            }
            catch (Exception e)
            {
                P.Fail(step.Key, e);
            }
            if (!done && ++tries > 60)
            {
                P.Check(step.Key, false, "never finished");
                done = true;
            }
            if (done)
            {
                tries = 0;
                index++;
            }
        }

        private void Build()
        {
            if (phase == 0)
            {
                Add("load", LoadReport);
                Add("patches", Patches);
                Add("research tab", ResearchTab);
                Add("things", Things);
                Add("floors", Floors);
                Add("gate", Gate);
                Add("gate keeps current", GateKeepsCurrent);
                Add("finish grants knowledge", FinishGrants);
                Add("study", Study);
                Add("traditions", Traditions);
                Add("heritage", Heritage);
                Add("politics without factions", Politics);
                Add("nations 1.0", Probe10.NationDefs);
                Add("people", Probe10.People);
                Add("traders", Probe10.Traders);
                Add("scenarios", Probe10.Scenarios);
                Add("quality and caravan", Probe10.QualityAndCaravan);
                Add("joy", Probe10.Joy);
                Add("chains", Probe10.Chains);
                Add("artifacts", Probe10.Artifacts);
                Add("2.1 content", Probe21.Content);
                Add("2.1 buildings", Probe21.Buildings);
                Add("3.0 content", Probe30.Content);
                Add("3.0 buildings", Probe30.Buildings);
                Add("3.0 chains", Probe30.Chains);
                Add("3.0 artifacts", Probe30.Artifacts);
                Add("3.0 routes", Probe30.Routes);
                Add("3.0 council", Probe30.Council);
                Add("3.0.1 kits", Probe30.Kits);
                Add("3.1 settlements", Probe31.Settlements);
                Add("3.1 research browser", Probe31.Atlas);
                Add("3.1 encyclopedia", Probe31.Encyclopedia);
                Add("3.1 settings", Probe31.Settings);
                Add("3.1 starts", Probe31.Starts);
                Add("3.2 content", Probe32.Content);
                Add("3.2 turrets", Probe32.Turrets);
                Add("3.2 lights", Probe32.Lights);
                Add("3.2 clothes", Probe32.Clothes);
                Add("3.3 doctrines", Probe33.Data);
                Add("3.3 animals", Probe33.Animals);
                Add("3.3 drill", Probe33.Drill);
                Add("3.3 raid plans", Probe33.Plans);
                Add("3.3 heir raid", Probe33.RealRaid);
                Add("3.3 trebuchet", Probe33.Trebuchet);
                Add("3.3 cold kits", Probe33.ColdKits);
                Add("3.4 data", Probe34.Data);
                Add("3.4 court", Probe34.Court);
                Add("3.4 treaties", Probe34.Treaties);
                Add("3.4 world events", Probe34.Events);
                Add("3.5 data", Probe35.Data);
                Add("3.5 reading", Probe35.Reading);
                Add("3.5 saga", Probe35.Saga);
                Add("3.5 errands", Probe35.Errands);
                Add("3.6 data", Probe36.Data);
                Add("3.6 music", Probe36.Music);
                Add("translation errors", Probe36.TranslationErrors);
                Add("3.7 nation switch", Probe37.Toggle);
                Add("3.7 fallen nation", Probe37.FallenNation);
                Add("4.0 royalty", Probe40.Royalty);
                Add("4.1 worn garments", Probe41.Garments);
                Add("4.2 fourth speed", Probe42.Speed);
                Add("4.2 ages data", Probe42.Data);
                Add("4.2 ages progress", Probe42.Progress);
                Add("4.2 ages troops", Probe42.Troops);
                Add("4.2 ages gates", Probe42.Gates);
                Add("4.2.1 storehouse speed", Probe42.StoreSpeed);
                Add("4.2.1 bar textures", Probe42.BarTextures);
                Add("4.2.1 name pools", Probe42.NamePools);
                Add("4.3 electric age", Probe43.Ages);
                Add("4.3 electric gates", Probe43.Gates);
                Add("4.3 electric troops", Probe43.Troops);
                Add("4.3 electric content", Probe43.Content);
                Add("4.3 works", Probe43.Works);
                Add("4.3 world fair", Probe43.Fair);
                Add("art references", ProbeArt.References);
                Add("art portraits", ProbeArt.Portraits);
                foreach (MainTabWindow_Heirs.Section s in Enum.GetValues(typeof(MainTabWindow_Heirs.Section)))
                {
                    MainTabWindow_Heirs.Section section = s;
                    Add("tab " + section, () => OpenTab(section));
                }
                for (int v = 0; v < 4; v++)
                {
                    int variant = v;
                    Add("research browser filters " + variant, () => { Probe31.AtlasFilterVariant(variant); OpenTab(MainTabWindow_Heirs.Section.Research); });
                }
                Add("research browser reset", Probe31.Reset);
                foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
                {
                    NationDef nation = n;
                    Add("encyclopedia " + nation.defName, () => { HeirsAtlas.encyclopediaNation = nation; OpenTab(MainTabWindow_Heirs.Section.Encyclopedia); });
                }
                Add("tab close", () => Find.MainTabsRoot.EscapeCurrentTab(false));
                Add("heritage dialog", () => Find.WindowStack.Add(new Dialog_ChooseHeritage()));
                Add("settings window", () => { P.CloseWindows(); Find.WindowStack.Add(new Dialog_ModSettings(LoadedModManager.GetMod<HeirsMod>())); });
                Add("2.1 missing nations", Probe21.MissingNations);
                Add("soak", () => { P.CloseWindows(); P.Ticks(5000); P.Calm(); });
                Add("save", Save);
                Add("load", () => { phase = 1; GameDataSaveLoader.LoadGame(SaveName); });
            }
            else if (phase == 1)
            {
                Add("after load", AfterLoad);
                Add("chain after load", Probe10.ChainAfterLoad);
                Add("3.0 routes after load", Probe30.RoutesAfterLoad);
                Add("3.0 council after load", Probe30.CouncilAfterLoad);
                Add("3.4 after load", Probe34.AfterLoad);
                Add("3.5 after load", Probe35.AfterLoad);
                Add("4.3 world fair after load", Probe43.FairAfterLoad);
                Add("soak after load", () => { P.Ticks(2500); P.Calm(); });
                Add("strip save", () => { GameDataSaveLoader.SaveGame(SaveName); StripSave(); });
                Add("load stripped", () => { phase = 2; GameDataSaveLoader.LoadGame(SaveName); });
            }
            else
            {
                Add("after stripped load", AfterStrippedLoad);
                Add("soak stripped", () => { P.Ticks(2500); P.Calm(); });
                Add("stripped tab", () => OpenTab(MainTabWindow_Heirs.Section.Heritage));
                Add("4.2.1 ten years", Probe42.TenYears);
                Add("collapse", Probe10.Collapse);
                Add("finish", () => { Find.MainTabsRoot.EscapeCurrentTab(false); Finish(); });
            }
        }

        // ------------------------------------------------------------------ load and patches
        private static void LoadReport()
        {
            P.Say("other load errors (not counted) " + P.OtherLoad.Count);
            foreach (string line in P.OtherLoad.Distinct().Take(20))
            {
                P.Say("  other: " + line);
            }
            P.Check("heirs game component", P.Game != null);
            P.Check("heirs world component", HeirsWorld.Get != null);
            P.Check("new game has no heritage", P.Game != null && !P.Game.heritageChosen && P.Game.heritage == null);
            P.Check("nation defs", DefDatabase<NationDef>.AllDefsListForReading.Count >= 1 && HeirsDefOf.HE_Roma != null);
        }

        private static void Patches()
        {
            P.Check("harmony_loaded", HeirsPatches.Status.Count > 0);
            foreach (KeyValuePair<string, bool> s in HeirsPatches.Status.ToList())
            {
                P.Check("all_patches_active " + s.Key, s.Value);
            }
            P.Say("patches: " + string.Join(", ", HeirsPatches.Status.Select(s => s.Key + "=" + s.Value)));
            int before = P.brokenWarnings;
            bool applied = HeirsPatches.TryApply(new BrokenTestPatch());
            P.Check("patch_failure_isolated returns false", !applied);
            P.Check("patch_failure_isolated one warning", P.brokenWarnings - before == 1, (P.brokenWarnings - before).ToString());
            P.Check("patch_failure_isolated inactive", !HeirsPatches.Active("BrokenTest"));
            P.Check("patch_failure_isolated others still on", HeirsPatches.Active("ResearchGate") && HeirsPatches.Active("ResearchKnowledge"));
        }

        // ------------------------------------------------------------------ content
        private static void ResearchTab()
        {
            List<ResearchProjectDef> ours = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Where(r => r.tab == HeirsDefOf.HE_WorldHeritage).ToList();
            P.Check("tab_has_projects", ours.Count >= 9, ours.Count.ToString());
            foreach (ResearchProjectDef r in ours)
            {
                P.Check("research text " + r.defName, !r.label.NullOrEmpty() && !r.description.NullOrEmpty());
                P.Check("research prereqs " + r.defName, r.prerequisites == null || r.prerequisites.All(x => x != null));
                HeirsResearchExt ext = r.GetModExtension<HeirsResearchExt>();
                P.Check("research ext " + r.defName, ext != null || r.defName == "HE_CultureTable");
                string unused = MainTabWindow_Heirs.EffectText(r);
            }
            ThingDef table = DefDatabase<ThingDef>.GetNamed("HE_CultureTable");
            P.Check("culture_table_bill", table.AllRecipes.Any(x => x.defName == "HE_StudyCulture"));
            RecipeDef study = DefDatabase<RecipeDef>.GetNamed("HE_StudyCulture");
            P.Check("study recipe worker", study.Worker is RecipeWorker_HeirsStudy);
            P.Check("study accepts gladius", study.fixedIngredientFilter.Allows(DefDatabase<ThingDef>.GetNamed("HE_Roma_Gladius")));
            foreach (RecipeDef recipe in DefDatabase<RecipeDef>.AllDefsListForReading.Where(x => x.ProducedThingDef != null && x.ProducedThingDef.defName.StartsWith("HE_")))
            {
                P.Check("roma_items_craftable " + recipe.defName, recipe.ProducedThingDef.uiIcon != null && recipe.ProducedThingDef.uiIcon != BaseContent.BadTex);
            }
        }

        private static void Things()
        {
            Map map = P.Home;
            foreach (ThingDef def in DefDatabase<ThingDef>.AllDefs.Where(d => d.defName.StartsWith("HE_") && (d.category == ThingCategory.Item || d.category == ThingCategory.Building)).ToList())
            {
                P.Run("thing " + def.defName, () =>
                {
                    bool building = def.category == ThingCategory.Building;
                    Thing thing;
                    if (building)
                    {
                        thing = P.SpawnBuilding(def, map);
                        thing.GetGizmos().ToList();
                    }
                    else
                    {
                        thing = ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                        GenPlace.TryPlaceThing(thing, map.Center, map, ThingPlaceMode.Near);
                    }
                    thing.GetInspectString();
                    string unused = thing.LabelCap + thing.DescriptionFlavor + thing.def.description;
                    bool iconOk = def.uiIcon != null && def.uiIcon != BaseContent.BadTex;
                    Material mat = thing.Graphic?.MatSingle;
                    bool texOk = mat != null && mat.mainTexture != null && mat.mainTexture != BaseContent.BadTex;
                    if (!iconOk || !texOk) missingTex++;
                    P.Check("icon " + def.defName, iconOk);
                    P.Check("texture " + def.defName, texOk);
                    if (building && def.building != null && def.researchPrerequisites.NullOrEmpty())
                    {
                        P.Check("building has research " + def.defName, false);
                    }
                    if (thing.Spawned) thing.Destroy();
                });
            }
        }

        private static void Floors()
        {
            Map map = P.Home;
            foreach (TerrainDef def in DefDatabase<TerrainDef>.AllDefs.Where(d => d.defName.StartsWith("HE_")).ToList())
            {
                P.Run("floor " + def.defName, () =>
                {
                    bool ok = P.HasTexture(def.texturePath) && def.uiIcon != null && def.uiIcon != BaseContent.BadTex;
                    if (!ok) missingTex++;
                    P.Check("floor texture " + def.defName, ok);
                    IntVec3 c = P.FreeSpot(map, new IntVec2(1, 1));
                    TerrainDef old = c.GetTerrain(map);
                    map.terrainGrid.SetTerrain(c, def);
                    P.Check("floor placed " + def.defName, c.GetTerrain(map) == def);
                    map.terrainGrid.SetTerrain(c, old);
                });
            }
            P.Check("road is fast", DefDatabase<TerrainDef>.GetNamed("HE_Roma_Road").pathCost == 0);
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                bool ok = n.Icon != null && n.Icon != BaseContent.BadTex;
                if (!ok) missingTex++;
                P.Check("nation icon " + n.defName, ok);
            }
            P.Check("site icon", P.HasTexture("HeirsOfEarth/World/HE_ChainSite"));
        }

        // ------------------------------------------------------------------ knowledge
        private static void Gate()
        {
            HeirsGame g = P.Game;
            ResearchManager rm = Find.ResearchManager;
            ResearchProjectDef roads = P.R("HE_Roma_Roads");
            rm.FinishProject(P.R("HE_Roma_Concrete"), false, null, false);
            P.Check("prerequisite finished", P.R("HE_Roma_Concrete").IsFinished);
            g.SetKnowledge(HeirsDefOf.HE_Roma, 0f);
            P.Check("gate_blocks_foreign", !roads.CanStartNow);
            P.Check("gate reason text", !g.CanStart(roads, out string reason) && !reason.NullOrEmpty() && reason.Contains("20"), reason ?? "null");
            g.SetKnowledge(HeirsDefOf.HE_Roma, 19.9f);
            P.Check("gate needs full amount", !roads.CanStartNow);
            g.AddKnowledge(HeirsDefOf.HE_Roma, 0.1f, null);
            P.Check("gate_opens_with_knowledge", roads.CanStartNow);
            P.Check("ungated project ok", P.R("HE_Roma_Standard").CanStartNow);
        }

        private static void GateKeepsCurrent()
        {
            HeirsGame g = P.Game;
            ResearchManager rm = Find.ResearchManager;
            ResearchProjectDef roads = P.R("HE_Roma_Roads");
            g.SetKnowledge(HeirsDefOf.HE_Roma, 25f);
            rm.SetCurrentProject(roads);
            P.Check("current set", rm.IsCurrentProject(roads));
            g.SetKnowledge(HeirsDefOf.HE_Roma, 0f);
            float before = rm.GetProgress(roads);
            rm.ResearchPerformed(100f, null);
            P.Check("gate_does_not_cancel_current progress", rm.GetProgress(roads) > before, before + " -> " + rm.GetProgress(roads));
            P.Check("gate_does_not_cancel_current still current", rm.IsCurrentProject(roads));
            rm.StopProject(roads);
        }

        private static void FinishGrants()
        {
            HeirsGame g = P.Game;
            P.NotScholarly(HeirsDefOf.HE_Roma);
            g.SetKnowledge(HeirsDefOf.HE_Roma, 30f);
            int chronicle = g.chronicle.Count;
            Find.ResearchManager.FinishProject(P.R("HE_Roma_Roads"), false, null, false);
            P.Check("finish_grants_knowledge", Mathf.Abs(g.Knowledge(HeirsDefOf.HE_Roma) - 35f) < 0.01f, g.Knowledge(HeirsDefOf.HE_Roma).ToString());
            P.Check("tradition chronicle", g.chronicle.Count == chronicle + 1);
            P.Check("roads tradition active", HeirsTraditions.Active(P.R("HE_Roma_Roads")));
            Find.ResearchManager.FinishProject(P.R("HE_CultureTable"), false, null, false);
            P.Check("common project gives no knowledge", Mathf.Abs(g.Knowledge(HeirsDefOf.HE_Roma) - 35f) < 0.01f);
        }

        private static void Study()
        {
            HeirsGame g = P.Game;
            P.NotScholarly(HeirsDefOf.HE_Roma);
            Map map = P.Home;
            Pawn pawn = P.Colonist(map);
            Thing gladius = ThingMaker.MakeThing(DefDatabase<ThingDef>.GetNamed("HE_Roma_Gladius"), ThingDefOf.Steel);
            float value = HeirsKnowledge.StudyValue(gladius);
            P.Check("study value positive", value > 0f, value.ToString());
            float before = g.Knowledge(HeirsDefOf.HE_Roma);
            DefDatabase<RecipeDef>.GetNamed("HE_StudyCulture").Worker.Notify_IterationCompleted(pawn, new List<Thing> { gladius });
            P.Check("study_grants_knowledge", Mathf.Abs(g.Knowledge(HeirsDefOf.HE_Roma) - before - value) < 0.01f, before + " + " + value + " = " + g.Knowledge(HeirsDefOf.HE_Roma));
            Thing steel = ThingMaker.MakeThing(ThingDefOf.Steel);
            P.Check("plain items give nothing", HeirsKnowledge.StudyValue(steel) == 0f);
            Find.ResearchManager.FinishProject(P.R("HE_Roma_Standard"), false, null, false);
            Find.ResearchManager.FinishProject(P.R("HE_Roma_Senate"), false, null, false);
            float boosted = HeirsKnowledge.StudyValue(gladius);
            P.Check("senate boosts study", Mathf.Abs(boosted - value * 1.25f) < 0.01f, value + " -> " + boosted);
        }

        // ------------------------------------------------------------------ traditions
        private static void Traditions()
        {
            // A colonist who can build: for one who cannot, construction speed is 0 and every check here passes or fails by chance.
            Pawn pawn = P.Builder(P.Home);
            StatDef build = StatDefOf.ConstructionSpeed;
            float before = build.Worker.GetValue(pawn);
            Find.ResearchManager.FinishProject(P.R("HE_Roma_Engineers"), false, null, false);
            float after = build.Worker.GetValue(pawn);
            P.Check("tradition_applies", before > 0f && Mathf.Abs(after - before * 1.15f) < 0.01f, before + " -> " + after);
            P.Check("tradition explanation", build.Worker.GetExplanationFull(StatRequest.For(pawn), ToStringNumberSense.Factor, after).Contains(P.R("HE_Roma_Engineers").LabelCap.RawText));
            HeirsMod.Settings.disabledTraditions.Add(HeirsDefOf.HE_Roma.defName);
            HeirsTraditions.Dirty();
            float off = build.Worker.GetValue(pawn);
            P.Check("tradition_toggle_clears_bonus", Mathf.Abs(off - before) < 0.01f, off + " vs " + before);
            HeirsMod.Settings.disabledTraditions.Remove(HeirsDefOf.HE_Roma.defName);
            HeirsTraditions.Dirty();
            P.Check("tradition back on", Mathf.Abs(build.Worker.GetValue(pawn) - after) < 0.01f);
        }

        // ------------------------------------------------------------------ heritage and politics
        private static void Heritage()
        {
            HeirsGame g = P.Game;
            int chronicle = g.chronicle.Count;
            g.SetHeritage(HeirsDefOf.HE_Roma);
            P.Check("heritage_once set", g.heritageChosen && g.heritage == HeirsDefOf.HE_Roma);
            g.SetHeritage(null);
            P.Check("heritage_once ignored second", g.heritage == HeirsDefOf.HE_Roma && g.chronicle.Count == chronicle + 1);
            g.SetKnowledge(HeirsDefOf.HE_Roma, 0f);
            P.Check("gate_allows_heritage", P.R("HE_Roma_Aqueduct").CanStartNow);
        }

        private static void Politics()
        {
            P.Check("goodwill missing faction", HeirsPolitics.PlayerGoodwill(null) == 0);
            Probe10.Politics();
        }

        private static void OpenTab(MainTabWindow_Heirs.Section section)
        {
            MainButtonDef def = DefDatabase<MainButtonDef>.GetNamed("HE_Heirs");
            if (Find.MainTabsRoot.OpenTab != def)
            {
                Find.MainTabsRoot.SetCurrentTab(def, false);
            }
            ((MainTabWindow_Heirs)def.TabWindow).Show(section);
        }

        // ------------------------------------------------------------------ save and load
        private static void Save()
        {
            HeirsGame g = P.Game;
            g.SetKnowledge(HeirsDefOf.HE_Roma, 42.5f);
            savedRoma = g.Knowledge(HeirsDefOf.HE_Roma);
            savedChronicle = g.chronicle.Count;
            savedHeritage = g.heritage;
            Probe34.savedTreaties = g.treaties.Count;
            GameDataSaveLoader.SaveGame(SaveName);
            P.Say("saved roma=" + savedRoma + " chronicle=" + savedChronicle + " heritage=" + savedHeritage);
        }

        private static void AfterLoad()
        {
            HeirsGame g = P.Game;
            P.Check("knowledge_saved", Mathf.Abs(g.Knowledge(HeirsDefOf.HE_Roma) - savedRoma) < 0.01f, g.Knowledge(HeirsDefOf.HE_Roma).ToString());
            P.Check("heritage saved", g.heritageChosen && g.heritage == savedHeritage);
            P.Check("chronicle saved", g.chronicle.Count == savedChronicle && g.chronicle.All(c => !c.text.NullOrEmpty()));
            P.Check("traditions after load", HeirsTraditions.Active(P.R("HE_Roma_Engineers")));
            Pawn pawn = P.Builder(P.Home);
            P.Check("tradition stat after load", StatDefOf.ConstructionSpeed.Worker.GetExplanationFull(StatRequest.For(pawn), ToStringNumberSense.Factor, 1f).Contains(P.R("HE_Roma_Engineers").LabelCap.RawText));
        }

        private static void StripSave()
        {
            string path = GenFilePaths.FilePathForSavedGame(SaveName);
            string text = System.IO.File.ReadAllText(path);
            RegexOptions mode = RegexOptions.Singleline | RegexOptions.Multiline;
            string stripped = Regex.Replace(text, "^([ \\t]*)<li Class=\"HeirsOfEarth\\.HeirsGame\">.*?^\\1</li>\\r?\\n", string.Empty, mode);
            stripped = Regex.Replace(stripped, "^([ \\t]*)<li Class=\"HeirsOfEarth\\.HeirsWorld\">.*?^\\1</li>\\r?\\n", string.Empty, mode);
            P.Check("strip removes heirs data", stripped.Length < text.Length && !stripped.Contains("HeirsOfEarth.HeirsGame"), text.Length + " -> " + stripped.Length);
            System.IO.File.WriteAllText(path, stripped);
        }

        private static void AfterStrippedLoad()
        {
            HeirsGame g = P.Game;
            P.Check("save_without_heirs_component recreated", g != null && HeirsWorld.Get != null);
            P.Check("save_without_heirs_component fresh", g != null && !g.heritageChosen && g.heritage == null && g.Knowledge(HeirsDefOf.HE_Roma) == 0f);
            P.Check("stripped research still finished", P.R("HE_Roma_Engineers").IsFinished);
            P.Check("stripped gate works", P.R("HE_Roma_Aqueduct").CanStartNow == false);
        }

        private static void Finish()
        {
            if (P.finished) return;
            P.finished = true;
            LoadedLanguage lang = LanguageDatabase.activeLanguage;
            List<string> missing = LanguageDatabase.defaultLanguage.keyedReplacements.Keys.Where(k => k.StartsWith("HE_") && !lang.keyedReplacements.ContainsKey(k)).ToList();
            P.Check("Turkish keyed complete", missing.Count == 0, string.Join(",", missing.Take(30)));
            int good = 0, bad = 0;
            foreach (DefInjectionPackage package in lang.defInjections)
            {
                foreach (KeyValuePair<string, DefInjectionPackage.DefInjection> entry in package.injections)
                {
                    if (!entry.Key.StartsWith("HE_")) continue;
                    if (entry.Value.injected) good++;
                    else { bad++; P.Say("untranslated " + package.defType.Name + " " + entry.Key); }
                }
            }
            int untranslatedDefs = 0;
            foreach (Def def in AllOurDefs())
            {
                if (!def.label.NullOrEmpty() && !lang.defInjections.Any(p => p.defType.IsInstanceOfType(def) && p.injections.ContainsKey(def.defName + ".label")))
                {
                    untranslatedDefs++;
                    P.Say("no Turkish label " + def.GetType().Name + " " + def.defName);
                }
            }
            List<string> langErrors = lang.loadErrors.Where(e => e.Contains("HE_") || e.Contains("Heirs")).ToList();
            langErrors.ForEach(e => P.Say("langerror " + e));
            P.Say("language=" + lang.folderName + " keys=" + lang.keyedReplacements.Keys.Count(k => k.StartsWith("HE_")) + " injected=" + good + " failed=" + bad);
            foreach (IGrouping<string, string> group in P.Errors.GroupBy(e => e))
            {
                P.Say("RUNTIME ERROR x" + group.Count() + " " + group.Key);
            }
            int untranslated = bad + langErrors.Count + untranslatedDefs;
            P.Say("SUMMARY pass=" + P.passes + " fail=" + P.fails + " errors=" + P.Errors.Count + " untranslated=" + untranslated + " missingTex=" + missingTex + " missingKeys=" + missing.Count);
            if (Uploader.TryStart(P.fails, P.Errors.Count, untranslated, missingTex, missing.Count))
            {
                return;
            }
            P.Say("COMPLETE");
            Root.Shutdown();
        }

        private static IEnumerable<Def> AllOurDefs()
        {
            foreach (Type t in GenDefDatabase.AllDefTypesWithDatabases())
            {
                foreach (Def d in GenDefDatabase.GetAllDefsInDatabaseForDef(t))
                {
                    if (d.defName.StartsWith("HE_") && d.modContentPack?.PackageId == "kerem.heirs") yield return d;
                }
            }
        }
    }
}
