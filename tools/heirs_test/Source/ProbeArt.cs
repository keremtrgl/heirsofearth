using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>
    /// Art checks, only when run.ps1 -Portraits sets HE_PORTRAIT_DIR: dumps a few vanilla head and hat textures as alignment
    /// references (kept locally, never shipped), and renders every heir apparel worn by a colonist of each body type from three sides.
    /// </summary>
    public static class ProbeArt
    {
        public static string Dir => Environment.GetEnvironmentVariable("HE_PORTRAIT_DIR");

        public static bool Active => !Dir.NullOrEmpty();

        private static readonly string[] Rots = { "south", "east", "north" };

        private static void SaveTexture(Texture tex, string name, int w, int h)
        {
            RenderTexture rt = RenderTexture.GetTemporary(w, h, 0, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB);
            RenderTexture prev = RenderTexture.active;
            Graphics.Blit(tex, rt);
            RenderTexture.active = rt;
            var copy = new Texture2D(w, h, TextureFormat.ARGB32, false);
            copy.ReadPixels(new Rect(0, 0, w, h), 0, 0);
            copy.Apply();
            RenderTexture.active = prev;
            RenderTexture.ReleaseTemporary(rt);
            Directory.CreateDirectory(Dir);
            File.WriteAllBytes(Path.Combine(Dir, name + ".png"), copy.EncodeToPNG());
            UnityEngine.Object.Destroy(copy);
        }

        public static void References()
        {
            if (!Active) return;
            int saved = 0;
            var paths = new List<string>();
            foreach (string head in new[] { "Male/Male_Average_Normal", "Female/Female_Average_Normal" })
                foreach (string r in Rots) paths.Add("Things/Pawn/Humanlike/Heads/" + head + "_" + r);
            foreach (string hat in new[] { "SimpleHelmet/SimpleHelmet", "CowboyHat/CowboyHat", "BowlerHat/BowlerHat", "Hood/Hood", "TribalHeaddress/TribalHeaddress" })
                foreach (string r in Rots) paths.Add("Things/Pawn/Humanlike/Apparel/" + hat + "_" + r);
            foreach (string body in new[] { "Male", "Female", "Thin", "Hulk", "Fat" })
                foreach (string r in Rots) paths.Add("Things/Pawn/Humanlike/Bodies/Naked_" + body + "_" + r);
            foreach (string worn in new[] { "PlateArmor/PlateArmor", "Duster/Duster", "Robe/Robe", "Jacket/Jacket", "Parka/Parka", "TribalA/TribalA", "ShirtBasic/ShirtBasic", "Cape/Cape" })
                foreach (string body in new[] { "Male", "Female", "Thin", "Hulk", "Fat" })
                    foreach (string r in Rots) paths.Add("Things/Pawn/Humanlike/Apparel/" + worn + "_" + body + "_" + r);
            foreach (string path in paths)
            {
                Texture2D tex = ContentFinder<Texture2D>.Get(path, false);
                if (tex == null) continue;
                SaveTexture(tex, "ref_" + path.Substring(path.IndexOf("Humanlike/") + 10).Replace('/', '_'), tex.width, tex.height);
                saved++;
            }
            P.Check("art references saved", saved >= paths.Count - 3, saved + "/" + paths.Count);
        }

        public static void Portraits()
        {
            if (!Active) return;
            Map map = P.Home;
            var request = new PawnGenerationRequest(PawnKindDefOf.Colonist, Faction.OfPlayer, forceGenerateNewPawn: true, canGeneratePawnRelations: false,
                                                    fixedGender: Gender.Male, allowAddictions: false);
            Pawn pawn = PawnGenerator.GeneratePawn(request);
            GenSpawn.Spawn(pawn, CellFinder.RandomClosewalkCellNear(P.Colonist(map).Position, map, 6), map);
            List<ThingDef> apparel = DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.IsApparel && d.defName.StartsWith("HE_")).OrderBy(d => d.defName).ToList();
            string only = Environment.GetEnvironmentVariable("HE_PORTRAIT_ONLY");
            if (!only.NullOrEmpty()) apparel = apparel.Where(d => d.defName.Contains(only)).ToList();
            int saved = 0;
            foreach (BodyTypeDef body in new[] { BodyTypeDefOf.Male, BodyTypeDefOf.Female, BodyTypeDefOf.Thin, BodyTypeDefOf.Hulk, BodyTypeDefOf.Fat })
            {
                pawn.story.bodyType = body;
                foreach (ThingDef def in apparel)
                {
                    pawn.apparel.DestroyAll();
                    var a = (Apparel)ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                    pawn.apparel.Wear(a, false, true);
                    pawn.Drawer.renderer.SetAllGraphicsDirty();
                    PortraitsCache.SetDirty(pawn);
                    for (int r = 0; r < 3; r++)
                    {
                        Rot4 rot = r == 0 ? Rot4.South : r == 1 ? Rot4.East : Rot4.North;
                        RenderTexture rt = PortraitsCache.Get(pawn, new Vector2(160f, 160f), rot, new Vector3(0f, 0f, 0.2f), 1.35f, supersample: false, compensateForUIScale: false);
                        SaveTexture(rt, "wear_" + def.defName + "_" + body.defName + "_" + Rots[r], 160, 160);
                        saved++;
                    }
                }
            }
            P.Gone(pawn);
            P.Check("portraits saved", saved == apparel.Count * 15, saved + "/" + apparel.Count * 15);
        }
    }
}
