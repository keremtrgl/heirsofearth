using System.Collections.Generic;
using System.Linq;
using HarmonyLib;
using RimWorld;
using Verse;
using Verse.Sound;

namespace HeirsOfEarth
{
    /// <summary>
    /// 3.6: every nation has its own music and a short signature call. The call sounds when that nation's news arrives; the music
    /// plays when one of its stories ends or it honours you, and now and then among the usual songs: your heritage's music, and the
    /// music of nations that have made you one of their own. The heir songs have no weight of their own in the vanilla rotation.
    /// </summary>
    public static class HeirsMusic
    {
        public const float RotationChance = 0.3f;
        private static int lastStingTick = -9999;

        public static string Key(NationDef nation) => nation?.defName.Length > 3 ? nation.defName.Substring(3) : null;

        public static SongDef SongOf(NationDef nation) => nation == null ? null : DefDatabase<SongDef>.GetNamedSilentFail("HE_Song_" + Key(nation));

        public static SoundDef StingOf(NationDef nation) => nation == null ? null : DefDatabase<SoundDef>.GetNamedSilentFail("HE_Sound_Sting_" + Key(nation));

        /// <summary>The nation's call, at most once every few seconds so a burst of letters does not become a din.</summary>
        public static void Sting(NationDef nation)
        {
            if (!HeirsMod.Settings.nationMusic || !HeirsMod.Settings.NationActive(nation) || Find.TickManager == null)
            {
                return;
            }
            // the last call may belong to another game (a later save): only a call earlier in this game's time holds the next one back
            int now = Find.TickManager.TicksGame;
            if (now >= lastStingTick && now - lastStingTick < 300)
            {
                return;
            }
            SoundDef sound = StingOf(nation);
            if (sound == null)
            {
                return;
            }
            lastStingTick = now;
            sound.PlayOneShotOnCamera();
        }

        /// <summary>Plays the nation's music now, unless the colony is in danger.</summary>
        public static bool Play(NationDef nation)
        {
            SongDef song = SongOf(nation);
            MusicManagerPlay music = Find.MusicManagerPlay;
            if (!HeirsMod.Settings.nationMusic || !HeirsMod.Settings.NationActive(nation) || song == null || music == null || music.DangerMusicMode)
            {
                return false;
            }
            music.ForcePlaySong(song, false);
            return true;
        }

        /// <summary>Nations whose music may join the rotation: your heritage, and nations that have honoured you.</summary>
        public static IEnumerable<NationDef> Patrons(HeirsGame game)
        {
            if (game == null) yield break;
            if (game.heritage != null && HeirsMod.Settings.NationActive(game.heritage)) yield return game.heritage;
            foreach (NationDef n in game.honours.Where(n => n != game.heritage && HeirsMod.Settings.NationActive(n))) yield return n;
        }

        public class Patch_Rotation : HeirsPatch
        {
            public override string Id => "NationMusic";

            public override void Apply(Harmony harmony)
            {
                harmony.Patch(HeirsPatches.Need(typeof(MusicManagerPlay), "ChooseNextSong"), postfix: new HarmonyMethod(typeof(Patch_Rotation), nameof(Postfix)));
            }

            public static void Postfix(MusicManagerPlay __instance, ref SongDef __result, Queue<SongDef> ___recentSongs)
            {
                if (!HeirsMod.Settings.nationMusic || __instance.DangerMusicMode || Current.ProgramState != ProgramState.Playing || !Rand.Chance(RotationChance))
                {
                    return;
                }
                SongDef pick = Patrons(HeirsGame.Get).Select(SongOf).Where(s => s != null && (___recentSongs == null || !___recentSongs.Contains(s))).RandomElementWithFallback();
                if (pick != null)
                {
                    __result = pick;
                }
            }
        }
    }
}
