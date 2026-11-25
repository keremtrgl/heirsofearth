using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>4.1 checks: every heir body garment has its own worn look for all five body types and three sides, with a stuff mask.</summary>
    public static class Probe41
    {
        private static readonly string[] Bodies = { "Male", "Female", "Thin", "Hulk", "Fat" };
        private static readonly string[] Rots = { "_south", "_east", "_north" };

        public static void Garments()
        {
            List<ThingDef> garments = DefDatabase<ThingDef>.AllDefsListForReading
                .Where(d => d.IsApparel && d.defName.StartsWith("HE_") && d.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.Torso)).ToList();
            P.Check("heir garments found", garments.Count >= 26, garments.Count.ToString());
            foreach (ThingDef def in garments)
            {
                string path = def.apparel.wornGraphicPath;
                var missing = new List<string>();
                foreach (string body in Bodies)
                    foreach (string r in Rots)
                    {
                        if (ContentFinder<Texture2D>.Get(path + "_" + body + r, false) == null) missing.Add(body + r);
                        if (ContentFinder<Texture2D>.Get(path + "_" + body + r + "m", false) == null) missing.Add(body + r + "m");
                    }
                P.Check("worn look " + def.defName, path != null && path.StartsWith("HeirsOfEarth/Apparel/Worn/Body/") && def.apparel.useWornGraphicMask && missing.Count == 0,
                    path + " " + string.Join(",", missing.Take(4)));
            }

            // each body type really draws them: the graphic record resolves to our own textures, not the error texture
            var bad = new List<string>();
            foreach (BodyTypeDef body in new[] { BodyTypeDefOf.Male, BodyTypeDefOf.Female, BodyTypeDefOf.Thin, BodyTypeDefOf.Hulk, BodyTypeDefOf.Fat })
            {
                foreach (ThingDef def in garments)
                {
                    var a = (Apparel)ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                    if (!ApparelGraphicRecordGetter.TryGetGraphicApparel(a, body, false, out ApparelGraphicRecord rec)
                        || rec.graphic == null || rec.graphic.MatSouth == null || rec.graphic.MatSouth.mainTexture == BaseContent.BadTex
                        || rec.graphic.MatEast.mainTexture == BaseContent.BadTex || !rec.graphic.path.Contains("/Worn/Body/"))
                    {
                        bad.Add(def.defName + "/" + body.defName);
                    }
                    a.Destroy();
                }
            }
            P.Check("garments draw on every body", bad.Count == 0, string.Join(", ", bad.Take(6)));

            // the stuff really tints them: the game finds our colour mask (named <side>m) for every heir garment and headgear
            var untinted = new List<string>();
            foreach (ThingDef def in DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.IsApparel && d.defName.StartsWith("HE_") && d.apparel.useWornGraphicMask))
            {
                var a = (Apparel)ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                if (ApparelGraphicRecordGetter.TryGetGraphicApparel(a, BodyTypeDefOf.Male, false, out ApparelGraphicRecord rec))
                {
                    foreach (Material mat in new[] { rec.graphic.MatSouth, rec.graphic.MatEast, rec.graphic.MatNorth })
                    {
                        Texture mask = mat.HasProperty(ShaderPropertyIDs.MaskTex) ? mat.GetTexture(ShaderPropertyIDs.MaskTex) : null;
                        if (mask == null || !mask.name.EndsWith("m"))
                        {
                            untinted.Add(def.defName);
                            break;
                        }
                    }
                }
                a.Destroy();
            }
            P.Check("the stuff tints every heir garment", untinted.Count == 0, string.Join(", ", untinted.Take(6)));
        }
    }
}
