using System.Collections.Generic;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    public class HeirsSettings : ModSettings
    {
        public float knowledgeGain = 1f;
        public float researchCost = 1f;
        public bool politics = true;
        public int politicsIntervalDays = 30;
        public bool interStateWar = true;
        public float raidStrength = 1f;
        public float tributeDemand = 1f;
        public bool addMissingNations = true;
        public bool tradeRoutes = true;
        public bool councilVictory = true;
        public bool raidDoctrines = true;
        public bool worldEvents = true;
        public bool nationMusic = true;
        public bool fourthSpeed = true;
        public bool ages = true;
        public float ageSpeed = 1f;
        public List<string> disabledTraditions = new List<string>();
        public List<string> disabledNations = new List<string>();

        public override void ExposeData()
        {
            Scribe_Values.Look(ref knowledgeGain, "knowledgeGain", 1f);
            Scribe_Values.Look(ref researchCost, "researchCost", 1f);
            Scribe_Values.Look(ref politics, "politics", true);
            Scribe_Values.Look(ref politicsIntervalDays, "politicsIntervalDays", 30);
            Scribe_Values.Look(ref interStateWar, "interStateWar", true);
            Scribe_Values.Look(ref raidStrength, "raidStrength", 1f);
            Scribe_Values.Look(ref tributeDemand, "tributeDemand", 1f);
            Scribe_Values.Look(ref addMissingNations, "addMissingNations", true);
            Scribe_Values.Look(ref tradeRoutes, "tradeRoutes", true);
            Scribe_Values.Look(ref councilVictory, "councilVictory", true);
            Scribe_Values.Look(ref raidDoctrines, "raidDoctrines", true);
            Scribe_Values.Look(ref worldEvents, "worldEvents", true);
            Scribe_Values.Look(ref nationMusic, "nationMusic", true);
            Scribe_Values.Look(ref fourthSpeed, "fourthSpeed", true);
            Scribe_Values.Look(ref ages, "ages", true);
            Scribe_Values.Look(ref ageSpeed, "ageSpeed", 1f);
            Scribe_Collections.Look(ref disabledTraditions, "disabledTraditions", LookMode.Value);
            Scribe_Collections.Look(ref disabledNations, "disabledNations", LookMode.Value);
            if (disabledTraditions == null)
            {
                disabledTraditions = new List<string>();
            }
            if (disabledNations == null)
            {
                disabledNations = new List<string>();
            }
        }

        /// <summary>Difficulty presets: 0 relaxed, 1 standard, 2 hard. Each sets the five tuning sliders at once.</summary>
        public void ApplyPreset(int preset)
        {
            float[][] values =
            {
                new[] { 1.5f, 0.75f, 0.75f, 0.5f, 45f },
                new[] { 1f, 1f, 1f, 1f, 30f },
                new[] { 0.75f, 1.25f, 1.35f, 1.5f, 20f },
            };
            float[] v = values[preset];
            knowledgeGain = v[0];
            researchCost = v[1];
            raidStrength = v[2];
            tributeDemand = v[3];
            politicsIntervalDays = (int)v[4];
        }

        /// <summary>
        /// A nation switched off stays where it is (faction, towns, goods, research) but no longer takes part: it is not added to saves
        /// that lack it, starts no stories, sends no errands or letters, plays no music and leaves the politics of the world.
        /// </summary>
        public bool NationActive(NationDef nation)
        {
            return nation == null || !disabledNations.Contains(nation.defName);
        }

        public bool TraditionsEnabled(NationDef nation)
        {
            return nation == null || !disabledTraditions.Contains(nation.defName);
        }
    }

    public class HeirsMod : Mod
    {
        public static HeirsSettings Settings;
        private Vector2 scroll;

        public HeirsMod(ModContentPack content) : base(content)
        {
            Settings = GetSettings<HeirsSettings>();
        }

        public override string SettingsCategory()
        {
            return Content.Name;
        }

        public override void DoSettingsWindowContents(Rect inRect)
        {
            var nations = DefDatabase<NationDef>.AllDefsListForReading;
            Rect view = new Rect(0f, 0f, inRect.width - 20f, 680f + nations.Count * 56f + HeirsPatches.Status.Count * 24f);
            Widgets.BeginScrollView(inRect, ref scroll, view);
            var list = new Listing_Standard();
            list.Begin(view);
            list.Label("HE_SettingsPresets".Translate());
            Rect presets = list.GetRect(32f);
            for (int i = 0; i < 3; i++)
            {
                if (Widgets.ButtonText(new Rect(presets.x + i * (presets.width / 3f), presets.y, presets.width / 3f - 6f, 30f), ("HE_SettingsPreset" + i).Translate()))
                {
                    Settings.ApplyPreset(i);
                }
            }
            list.Gap(6f);
            list.Label("HE_SettingsKnowledgeGain".Translate(Settings.knowledgeGain.ToStringPercent()));
            Settings.knowledgeGain = Mathf.Round(list.Slider(Settings.knowledgeGain, 0.25f, 4f) * 20f) / 20f;
            list.Label("HE_SettingsResearchCost".Translate(Settings.researchCost.ToStringPercent()));
            Settings.researchCost = Mathf.Round(list.Slider(Settings.researchCost, 0.25f, 3f) * 20f) / 20f;
            list.Label("HE_SettingsRaidStrength".Translate(Settings.raidStrength.ToStringPercent()));
            Settings.raidStrength = Mathf.Round(list.Slider(Settings.raidStrength, 0.25f, 2f) * 20f) / 20f;
            list.Label("HE_SettingsTributeDemand".Translate(Settings.tributeDemand.ToStringPercent()));
            Settings.tributeDemand = Mathf.Round(list.Slider(Settings.tributeDemand, 0.25f, 3f) * 20f) / 20f;
            list.GapLine();
            list.CheckboxLabeled("HE_SettingsPolitics".Translate(), ref Settings.politics);
            list.CheckboxLabeled("HE_SettingsInterStateWar".Translate(), ref Settings.interStateWar);
            list.CheckboxLabeled("HE_SettingsAddMissing".Translate(), ref Settings.addMissingNations, "HE_SettingsAddMissingTip".Translate());
            list.CheckboxLabeled("HE_SettingsTradeRoutes".Translate(), ref Settings.tradeRoutes, "HE_SettingsTradeRoutesTip".Translate());
            list.CheckboxLabeled("HE_SettingsCouncil".Translate(), ref Settings.councilVictory, "HE_SettingsCouncilTip".Translate());
            list.CheckboxLabeled("HE_SettingsDoctrines".Translate(), ref Settings.raidDoctrines, "HE_SettingsDoctrinesTip".Translate());
            list.CheckboxLabeled("HE_SettingsWorldEvents".Translate(), ref Settings.worldEvents, "HE_SettingsWorldEventsTip".Translate());
            list.CheckboxLabeled("HE_SettingsNationMusic".Translate(), ref Settings.nationMusic, "HE_SettingsNationMusicTip".Translate());
            list.CheckboxLabeled("HE_SettingsFourthSpeed".Translate(), ref Settings.fourthSpeed, "HE_SettingsFourthSpeedTip".Translate());
            list.CheckboxLabeled("HE_SettingsAges".Translate(), ref Settings.ages, "HE_SettingsAgesTip".Translate());
            if (Settings.ages)
            {
                list.Label("HE_SettingsAgeSpeed".Translate(Settings.ageSpeed.ToStringPercent()));
                Settings.ageSpeed = Mathf.Round(list.Slider(Settings.ageSpeed, 0.25f, 4f) * 20f) / 20f;
            }
            list.Label("HE_SettingsPoliticsInterval".Translate(Settings.politicsIntervalDays));
            Settings.politicsIntervalDays = Mathf.RoundToInt(list.Slider(Settings.politicsIntervalDays, 10f, 60f));
            list.GapLine();
            foreach (NationDef nation in nations)
            {
                bool active = Settings.NationActive(nation);
                bool wasActive = active;
                list.CheckboxLabeled("HE_SettingsNationActive".Translate(nation.LabelCap), ref active, "HE_SettingsNationActiveTip".Translate());
                if (active != wasActive)
                {
                    if (active) Settings.disabledNations.Remove(nation.defName);
                    else Settings.disabledNations.Add(nation.defName);
                }
                bool on = Settings.TraditionsEnabled(nation);
                bool was = on;
                list.CheckboxLabeled("HE_SettingsTraditions".Translate(nation.LabelCap), ref on);
                if (on != was)
                {
                    if (on) Settings.disabledTraditions.Remove(nation.defName);
                    else Settings.disabledTraditions.Add(nation.defName);
                    HeirsTraditions.Dirty();
                }
            }
            list.GapLine();
            list.Label("HE_SettingsPatches".Translate());
            foreach (var pair in HeirsPatches.Status)
            {
                list.Label("  " + pair.Key + ": " + (pair.Value ? "HE_PatchOn".Translate() : "HE_PatchOff".Translate()));
            }
            list.End();
            Widgets.EndScrollView();
        }

        public override void WriteSettings()
        {
            base.WriteSettings();
            HeirsTraditions.Dirty();
        }
    }
}
