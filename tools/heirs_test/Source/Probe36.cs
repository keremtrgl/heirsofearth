using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using Verse;

namespace HeProbe
{
    /// <summary>3.6 checks: the nations' music and calls, weapon and artifact sounds, the music rotation.</summary>
    public static class Probe36
    {
        private static bool HasClip(SoundDef sound) =>
            sound != null && sound.subSounds.Count > 0 && sound.subSounds.All(s => s.grains.Count > 0 && s.grains.All(g => g.GetResolvedGrains().Any()));

        public static void Data()
        {
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                SongDef song = HeirsMusic.SongOf(n);
                P.Check("music " + n.defName, song != null && song.clip != null && song.clip.length > 60f && !song.playOnMap, song?.clip?.length.ToString("0"));
                P.Check("call " + n.defName, HasClip(HeirsMusic.StingOf(n)));
            }
            var weapons = new Dictionary<string, string>
            {
                { "HE_Albion_Musket", "HE_Shot_Musket" }, { "HE_Pars_Jezail", "HE_Shot_Musket" }, { "HE_Yamato_Tanegashima", "HE_Shot_Matchlock" },
                { "HE_Albion_FlintlockPistol", "HE_Shot_Flintlock" }, { "HE_Albion_Blunderbuss", "HE_Shot_Blunderbuss" }, { "HE_Albion_FieldCannon_Gun", "HE_Shot_Cannon" },
                { "HE_Roma_Scorpio_Gun", "HE_Shot_Scorpio" }, { "HE_Hellas_Gastraphetes", "HE_Shot_Scorpio" }, { "HE_Roma_Manuballista", "HE_Shot_Manuballista" },
                { "HE_Trebuchet_Gun", "HE_Shot_Trebuchet" }, { "HE_Hellas_Lithobolos_Gun", "HE_Shot_Trebuchet" }, { "HE_Inti_Sling", "HE_Shot_Sling" },
                { "HE_Inti_SlingStand_Gun", "HE_Shot_Sling" }, { "HE_Tianxia_Repeater", "HE_Shot_Repeater" }, { "HE_Tianxia_FireLance", "HE_Shot_FireLance" },
                { "HE_Pars_NaftThrower_Gun", "HE_Shot_Naft" }, { "HE_Tianxia_FireArrowBattery_Gun", "HE_Shot_FireArrows" }, { "HE_Nord_HarpoonGun", "HE_Shot_Harpoon" },
            };
            foreach (var kv in weapons)
            {
                ThingDef w = DefDatabase<ThingDef>.GetNamedSilentFail(kv.Key);
                SoundDef s = w?.Verbs.FirstOrDefault()?.soundCast;
                P.Check("weapon sound " + kv.Key, s != null && s.defName == kv.Value && HasClip(s), s?.defName);
            }
            foreach (var kv in new Dictionary<string, string> { { "HE_Kemet_Artifact_SunDisc", "HE_Sound_Sistrum" }, { "HE_Pars_Artifact_KingsEye", "HE_Sound_Karnay" }, { "HE_Inti_Artifact_GoldenThread", "HE_Sound_Pututu" } })
            {
                SoundDef s = DefDatabase<ThingDef>.GetNamed(kv.Key).GetCompProperties<CompProperties_HeirsArtifact>()?.sound;
                P.Check("artifact sound " + kv.Key, s?.defName == kv.Value && HasClip(s), s?.defName);
            }
            foreach (ThingDef hat in DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.IsApparel && d.defName.StartsWith("HE_") && d.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.UpperHead)))
            {
                string path = hat.apparel.wornGraphicPath;
                bool own = path != null && path.StartsWith("HeirsOfEarth/Apparel/Worn/");
                bool sides = own && new[] { "_south", "_east", "_north" }.All(r => ContentFinder<UnityEngine.Texture2D>.Get(path + r, false) != null
                    && (!hat.apparel.useWornGraphicMask || ContentFinder<UnityEngine.Texture2D>.Get(path + r + "m", false) != null));
                P.Check("worn look " + hat.defName, sides && (hat.MadeFromStuff == hat.apparel.useWornGraphicMask), path);
            }
            // wreaths and bands sit on the hair; vanilla would hide the hair under any head apparel without skip flags
            foreach (string band in new[] { "HE_Roma_Laurel", "HE_Hellas_OliveWreath", "HE_Nord_Circlet", "HE_Inti_Mascaypacha" })
            {
                ThingDef d = DefDatabase<ThingDef>.GetNamed(band);
                P.Check("hair shows under " + band, d.apparel.renderSkipFlags != null && d.apparel.renderSkipFlags.All(f => f == RenderSkipFlagDefOf.None));
            }
            P.Check("music setting text", "HE_SettingsNationMusic".CanTranslate() && "HE_SettingsNationMusicTip".CanTranslate());
        }

        public static void Music()
        {
            HeirsGame game = P.Game;
            MusicManagerPlay music = Find.MusicManagerPlay;
            NationDef kemet = DefDatabase<NationDef>.GetNamed("HE_Kemet");
            bool before = HeirsMod.Settings.nationMusic;
            HeirsMod.Settings.nationMusic = false;
            P.Check("music off plays nothing", !HeirsMusic.Play(kemet));
            HeirsMusic.Sting(kemet);
            HeirsMod.Settings.nationMusic = true;
            bool danger = music.DangerMusicMode;
            bool played = HeirsMusic.Play(kemet);
            P.Check("a nation's music plays", danger || (played && P.Get(music, "currentSong") == HeirsMusic.SongOf(kemet)), danger ? "danger" : (P.Get(music, "currentSong") as SongDef)?.defName);
            HeirsMusic.Sting(kemet);

            // the rotation: with a heritage, heir music turns up now and then, and never the music of a stranger
            NationDef heritage = game.heritage;
            var recent = (Queue<SongDef>)P.Get(music, "recentSongs");
            recent.Clear();
            game.heritage = DefDatabase<NationDef>.GetNamed("HE_Yamato");
            var choose = typeof(MusicManagerPlay).GetMethod("ChooseNextSong", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
            var picks = new List<SongDef>();
            for (int i = 0; i < 60; i++) picks.Add((SongDef)choose.Invoke(music, null));
            var allowed = new HashSet<SongDef>(HeirsMusic.Patrons(game).Select(HeirsMusic.SongOf));
            var heir = picks.Where(s => s.defName.StartsWith("HE_Song_")).ToList();
            P.Check("heritage music joins the rotation", danger || heir.Count > 0, heir.Count + "/60");
            P.Check("only patrons' music", heir.All(allowed.Contains), string.Join(",", heir.Select(s => s.defName).Distinct()));
            P.Check("heir music is not chosen without the rotation", DefDatabase<SongDef>.AllDefs.Where(s => s.defName.StartsWith("HE_Song_")).All(s => !s.playOnMap));
            game.heritage = heritage;

            // a call remembered from a later game (loading an older save) must not silence this one
            var last = typeof(HeirsMusic).GetField("lastStingTick", System.Reflection.BindingFlags.Static | System.Reflection.BindingFlags.NonPublic);
            int now = Find.TickManager.TicksGame;
            last.SetValue(null, now + 5000000);
            HeirsMusic.Sting(kemet);
            P.Check("calls play after loading an older save", (int)last.GetValue(null) == now, last.GetValue(null).ToString());
            HeirsMod.Settings.nationMusic = before;
        }
        /// <summary>Which translation load errors are ours (the game counts the official language pack's own too).</summary>
        public static void TranslationErrors()
        {
            LoadedLanguage lang = LanguageDatabase.activeLanguage;
            var errors = new List<string>(lang.loadErrors);
            foreach (var pack in lang.defInjections) errors.AddRange(pack.loadErrors);
            var ours = errors.Where(e => e.Contains("HeirsOfEarth") || e.Contains("HE_") || e.Contains("heirs")).ToList();
            foreach (string e in errors.Take(40)) P.Say("translation: " + (ours.Contains(e) ? "OURS " : "core ") + e);
            P.Check("no translation errors of ours", ours.Count == 0, ours.Count + "/" + errors.Count);
        }
    }
}
