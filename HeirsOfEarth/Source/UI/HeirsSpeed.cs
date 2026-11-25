using System;
using RimWorld;
using UnityEngine;
using Verse;
using Verse.Sound;

namespace HeirsOfEarth
{
    /// <summary>
    /// 4.2: a fourth time-speed button. The game already has this speed (Ultrafast, 15x) but only shows it in developer mode.
    /// The button and its key (the game's own "ultrafast" binding, 4 by default) work in a normal game; the icon is built from
    /// the game's own arrows, so it matches the other three buttons.
    /// </summary>
    public static class HeirsSpeed
    {
        private static readonly TimeSpeed[] Speeds = { TimeSpeed.Paused, TimeSpeed.Normal, TimeSpeed.Fast, TimeSpeed.Superfast, TimeSpeed.Ultrafast };
        private static Texture2D icon;
        private static bool iconTried;

        public static bool Enabled => HeirsMod.Settings.fourthSpeed;

        public static Texture2D Icon
        {
            get
            {
                if (!iconTried)
                {
                    iconTried = true;
                    try
                    {
                        icon = BuildIcon();
                    }
                    catch (Exception e)
                    {
                        Log.Warning("[Heirs] could not build the fourth speed icon, using the third: " + e.Message);
                    }
                }
                return icon ?? TexButton.SpeedButtonTextures[(int)TimeSpeed.Superfast];
            }
        }

        private static Texture2D TextureFor(TimeSpeed speed) => speed == TimeSpeed.Ultrafast ? Icon : TexButton.SpeedButtonTextures[(int)speed];

        private static KeyBindingDef BindingFor(TimeSpeed speed)
        {
            switch (speed)
            {
                case TimeSpeed.Paused: return KeyBindingDefOf.TogglePause;
                case TimeSpeed.Normal: return KeyBindingDefOf.TimeSpeed_Normal;
                case TimeSpeed.Fast: return KeyBindingDefOf.TimeSpeed_Fast;
                case TimeSpeed.Superfast: return KeyBindingDefOf.TimeSpeed_Superfast;
                default: return KeyBindingDefOf.TimeSpeed_Ultrafast;
            }
        }

        private static void PlaySound(TimeSpeed speed)
        {
            SoundDef sound = speed == TimeSpeed.Paused ? SoundDefOf.Clock_Stop
                : speed == TimeSpeed.Normal ? SoundDefOf.Clock_Normal
                : speed == TimeSpeed.Fast ? SoundDefOf.Clock_Fast
                : SoundDefOf.Clock_Superfast;
            sound?.PlayOneShotOnCamera();
        }

        private static void SetSpeed(TimeSpeed speed)
        {
            Find.TickManager.CurTimeSpeed = speed;
            PlaySound(speed);
            PlayerKnowledgeDatabase.KnowledgeDemonstrated(ConceptDefOf.TimeControls, KnowledgeAmount.SpecificInteraction);
        }

        /// <summary>The game's time controls with the fourth button; the rest behaves exactly like the original.</summary>
        public static bool Prefix(Rect timerRect)
        {
            if (!Enabled)
            {
                return true;
            }
            TickManager tickManager = Find.TickManager;
            Vector2 size = TimeControls.TimeButSize;
            timerRect.width = Mathf.Max(timerRect.width, size.x * Speeds.Length);
            Widgets.BeginGroup(timerRect);
            Rect rect = new Rect(0f, 0f, size.x, size.y);
            foreach (TimeSpeed speed in Speeds)
            {
                string key = KeyPrefs.KeyPrefsData.GetBoundKeyCode(BindingFor(speed), KeyPrefs.BindingSlot.A).ToStringReadable();
                string tip = "HotKeyTip".Translate() + ": " + key;
                if (speed == TimeSpeed.Ultrafast)
                {
                    tip = "HE_SpeedFourthTip".Translate() + "\n\n" + tip;
                }
                if (Widgets.ButtonImage(rect, TextureFor(speed), true, tip) && !tickManager.ForcePaused)
                {
                    if (speed == TimeSpeed.Paused)
                    {
                        tickManager.TogglePaused();
                        PlayerKnowledgeDatabase.KnowledgeDemonstrated(ConceptDefOf.Pause, KnowledgeAmount.SpecificInteraction);
                        PlaySound(tickManager.CurTimeSpeed);
                    }
                    else
                    {
                        SetSpeed(speed);
                    }
                }
                if ((tickManager.ForcePaused ? TimeSpeed.Paused : tickManager.CurTimeSpeed) == speed)
                {
                    GUI.DrawTexture(rect, TexUI.HighlightTex);
                }
                rect.x += rect.width;
            }
            if (tickManager.slower.ForcedNormalSpeed)
            {
                Widgets.DrawLineHorizontal(rect.width * 2f, rect.height / 2f, rect.width * 3f);
            }
            if (tickManager.ForcePaused)
            {
                Widgets.DrawLineHorizontal(rect.width, rect.height / 2f, rect.width * 4f);
            }
            Widgets.EndGroup();
            GenUI.AbsorbClicksInRect(timerRect);
            UIHighlighter.HighlightOpportunity(timerRect, "TimeControls");
            if (Event.current.type == EventType.KeyDown)
            {
                Keys(tickManager);
            }
            return false;
        }

        private static void Keys(TickManager tickManager)
        {
            if (KeyBindingDefOf.TogglePause.KeyDownEvent)
            {
                tickManager.TogglePaused();
                PlaySound(tickManager.CurTimeSpeed);
                PlayerKnowledgeDatabase.KnowledgeDemonstrated(ConceptDefOf.Pause, KnowledgeAmount.SpecificInteraction);
                Event.current.Use();
            }
            if (Find.WindowStack.WindowsForcePause)
            {
                return;
            }
            foreach (TimeSpeed speed in new[] { TimeSpeed.Normal, TimeSpeed.Fast, TimeSpeed.Superfast, TimeSpeed.Ultrafast })
            {
                if (BindingFor(speed).KeyDownEvent)
                {
                    SetSpeed(speed);
                    Event.current.Use();
                }
            }
            if (KeyBindingDefOf.TimeSpeed_Slower.KeyDownEvent && tickManager.CurTimeSpeed != TimeSpeed.Paused)
            {
                SetSpeed(tickManager.CurTimeSpeed - 1);
                Event.current.Use();
            }
            if (KeyBindingDefOf.TimeSpeed_Faster.KeyDownEvent && tickManager.CurTimeSpeed < TimeSpeed.Ultrafast)
            {
                SetSpeed(tickManager.CurTimeSpeed + 1);
                Event.current.Use();
            }
            if (Prefs.DevMode && KeyBindingDefOf.Dev_TickOnce.KeyDownEvent && tickManager.CurTimeSpeed == TimeSpeed.Paused)
            {
                tickManager.DoSingleTick();
                SoundDefOf.Clock_Stop.PlayOneShotOnCamera();
            }
        }

        // ------------------------------------------------------------------ icon

        private static Color32[] Pixels(Texture2D texture, out int width, out int height)
        {
            width = texture.width;
            height = texture.height;
            RenderTexture rt = RenderTexture.GetTemporary(width, height, 0, RenderTextureFormat.ARGB32);
            RenderTexture previous = RenderTexture.active;
            Graphics.Blit(texture, rt);
            RenderTexture.active = rt;
            var copy = new Texture2D(width, height, TextureFormat.RGBA32, false);
            copy.ReadPixels(new Rect(0, 0, width, height), 0, 0);
            copy.Apply();
            RenderTexture.active = previous;
            RenderTexture.ReleaseTemporary(rt);
            Color32[] pixels = copy.GetPixels32();
            UnityEngine.Object.Destroy(copy);
            return pixels;
        }

        private static void Columns(Color32[] p, int w, int h, out int left, out int right)
        {
            left = w;
            right = -1;
            for (int x = 0; x < w; x++)
            {
                for (int y = 0; y < h; y++)
                {
                    if (p[y * w + x].a > 24)
                    {
                        left = Math.Min(left, x);
                        right = Math.Max(right, x);
                        break;
                    }
                }
            }
        }

        /// <summary>Four arrows: the game's three-arrow icon with one more of its arrows, spaced the same way and fitted to the button.</summary>
        public static Texture2D BuildIcon()
        {
            Color32[] three = Pixels(TexButton.SpeedButtonTextures[(int)TimeSpeed.Superfast], out int w, out int h);
            Color32[] one = Pixels(TexButton.SpeedButtonTextures[(int)TimeSpeed.Normal], out int w1, out int h1);
            if (w1 != w || h1 != h)
            {
                return null;
            }
            Columns(three, w, h, out int l3, out int r3);
            Columns(one, w, h, out int l1, out int r1);
            int arrow = r1 - l1 + 1;
            float step = ((r3 - l3 + 1) - arrow) / 2f;
            if (arrow <= 0 || step <= 0f)
            {
                return null;
            }
            float group = 3f * step + arrow;
            int canvas = Mathf.CeilToInt(Mathf.Max(w, group + 4f));
            float start = (canvas - group) / 2f;
            var layer = new Color[canvas * h];
            void Over(Color32[] src, int srcLeft, int srcRight, float at)
            {
                for (int x = srcLeft; x <= srcRight; x++)
                {
                    int cx = Mathf.RoundToInt(at + (x - srcLeft));
                    if (cx < 0 || cx >= canvas) continue;
                    for (int y = 0; y < h; y++)
                    {
                        Color s = src[y * w + x];
                        Color d = layer[y * canvas + cx];
                        float a = s.a + d.a * (1f - s.a);
                        layer[y * canvas + cx] = a <= 0f ? Color.clear : new Color((s.r * s.a + d.r * d.a * (1f - s.a)) / a, (s.g * s.a + d.g * d.a * (1f - s.a)) / a, (s.b * s.a + d.b * d.a * (1f - s.a)) / a, a);
                    }
                }
            }
            Over(one, l1, r1, start + 3f * step);
            Over(three, l3, r3, start);
            var result = new Texture2D(w, h, TextureFormat.RGBA32, false) { name = "HeirsSpeedFourth", filterMode = FilterMode.Bilinear, wrapMode = TextureWrapMode.Clamp };
            var output = new Color[w * h];
            float scale = (float)canvas / w;
            for (int x = 0; x < w; x++)
            {
                float sx = (x + 0.5f) * scale - 0.5f;
                int x0 = Mathf.Clamp(Mathf.FloorToInt(sx), 0, canvas - 1);
                int x1 = Mathf.Min(x0 + 1, canvas - 1);
                float t = Mathf.Clamp01(sx - x0);
                for (int y = 0; y < h; y++)
                {
                    output[y * w + x] = Color.Lerp(layer[y * canvas + x0], layer[y * canvas + x1], t);
                }
            }
            result.SetPixels(output);
            result.Apply();
            return result;
        }

        public class Patch : HeirsPatch
        {
            public override string Id => "FourthSpeed";

            public override void Apply(HarmonyLib.Harmony harmony)
            {
                harmony.Patch(HeirsPatches.Need(typeof(TimeControls), nameof(TimeControls.DoTimeControlsGUI)),
                    prefix: new HarmonyLib.HarmonyMethod(typeof(HeirsSpeed), nameof(Prefix)));
            }
        }
    }
}
