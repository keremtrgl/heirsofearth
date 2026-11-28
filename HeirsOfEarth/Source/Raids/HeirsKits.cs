using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using RimWorld;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>
    /// 3.3: on a cold map vanilla hands any pawn a "free" warm layer chosen from every piece of clothing in the game, and drops what it
    /// cannot be worn with. An Albion fusilier could lose his shako for a tuque and his shirt for a Nordic tunic. While a heir nation's
    /// pawn is dressed, the generator only sees that nation's clothes and the plain shirts and trousers it may wear, so any extra warmth
    /// comes from the nation's own wardrobe.
    /// </summary>
    public static class HeirsKits
    {
        private static FieldInfo pairsField;
        private static List<ThingStuffPair> source;
        private static readonly Dictionary<PawnKindDef, List<ThingStuffPair>> cache = new Dictionary<PawnKindDef, List<ThingStuffPair>>();
        private static readonly Dictionary<PawnKindDef, NationDef> nationOf = new Dictionary<PawnKindDef, NationDef>();

        public static NationDef NationOfKind(PawnKindDef kind)
        {
            if (kind == null || !kind.defName.StartsWith("HE_"))
            {
                return null;
            }
            if (!nationOf.TryGetValue(kind, out NationDef nation))
            {
                string[] parts = kind.defName.Split('_');
                nation = parts.Length >= 3 ? DefDatabase<NationDef>.GetNamedSilentFail("HE_" + parts[1]) : null;
                nationOf[kind] = nation;
            }
            return nation;
        }

        /// <summary>The clothes a heir pawn kind may be given: its nation's own, anything its tags allow and what it must wear.</summary>
        public static List<ThingStuffPair> Wardrobe(PawnKindDef kind, List<ThingStuffPair> all)
        {
            if (all != source)
            {
                cache.Clear();
                source = all;
            }
            if (!cache.TryGetValue(kind, out List<ThingStuffPair> list))
            {
                list = Build(kind, all, kind.apparelRequired);
                cache[kind] = list;
            }
            return list;
        }

        private static List<ThingStuffPair> Build(PawnKindDef kind, List<ThingStuffPair> all, List<ThingDef> requiredList)
        {
            string prefix = "HE_" + NationOfKind(kind).defName.Substring(3) + "_";
            HashSet<string> tags = new HashSet<string>(kind.apparelTags ?? new List<string>());
            List<ThingDef> required = requiredList ?? new List<ThingDef>();
            BodyDef body = kind.RaceProps?.body ?? BodyDefOf.Human;
            // Nothing that would push out a piece the kind must wear (a warm hat for the shako, a coat over the uniform shirt).
            // A later age's uniform never comes at random: only through HeirsAges.UniformKit, once the nation has reached that age.
            return all.Where(p => (required.Contains(p.thing) || (required.All(r => ApparelUtility.CanWearTogether(r, p.thing, body)) && !p.thing.HasModExtension<HeirsAgeExt>()))
                                  && (p.thing.defName.StartsWith(prefix)
                                      || (p.thing.apparel.tags != null && p.thing.apparel.tags.Any(tags.Contains))
                                      || required.Contains(p.thing))).ToList();
        }

        private static PawnKindDef uniformKind;
        private static List<ThingDef> uniformRestore;
        private static List<ThingDef> uniformWear;

        /// <summary>The kit pieces of pawns still being generated, put on again once the pawn is done.</summary>
        private static readonly Dictionary<Pawn, List<ThingDef>> pending = new Dictionary<Pawn, List<ThingDef>>();

        /// <summary>
        /// 4.3.2: after the clothes, Ideology gives a member the apparel its ideoligion desires (PreceptComp_Apparel_Desired), and
        /// that took the steel helmet off a troop for the ideoligion's hat. Once the pawn is fully generated, the kit goes back on.
        /// </summary>
        public static void GeneratePawnPostfix(Pawn __result)
        {
            if (__result != null && pending.TryGetValue(__result, out List<ThingDef> wear))
            {
                pending.Remove(__result);
                WearMissing(__result, wear);
            }
        }

        /// <summary>
        /// 4.3.2: the vanilla generator often drops a required piece of headgear (only about half of the steel helmets rolled were
        /// worn). Whatever the kit rolled and the pawn did not get is made and put on here, in place of what it cannot be worn with.
        /// </summary>
        public static void WearMissing(Pawn pawn, List<ThingDef> wear)
        {
            if (pawn?.apparel == null || wear.NullOrEmpty())
            {
                return;
            }
            BodyDef body = pawn.RaceProps?.body ?? BodyDefOf.Human;
            foreach (ThingDef def in wear)
            {
                if (pawn.apparel.WornApparel.Any(a => a.def == def) || !ApparelUtility.HasPartsToWear(pawn, def))
                {
                    continue;
                }
                try
                {
                    ThingDef stuff = def.MadeFromStuff ? GenStuff.RandomStuffByCommonalityFor(def) : null;
                    if (def.MadeFromStuff && stuff == null)
                    {
                        continue;
                    }
                    var apparel = (Apparel)ThingMaker.MakeThing(def, stuff);
                    apparel.TryGetComp<CompQuality>()?.SetQuality(QualityUtility.GenerateQualityGeneratingPawn(pawn.kindDef, def), ArtGenerationContext.Outsider);
                    foreach (Apparel old in pawn.apparel.WornApparel.Where(a => !ApparelUtility.CanWearTogether(a.def, def, body)).ToList())
                    {
                        pawn.apparel.Remove(old);
                        old.Destroy();
                    }
                    pawn.apparel.Wear(apparel, false);
                }
                catch (System.Exception e)
                {
                    Log.WarningOnce("[Heirs of Earth] could not dress " + pawn + " in " + def.defName + ": " + e.Message, def.shortHash ^ 0x4e1);
                }
            }
        }

        public static void Prefix(Pawn pawn, out List<ThingStuffPair> __state)
        {
            __state = null;
            if (pawn?.kindDef == null || NationOfKind(pawn.kindDef) == null)
            {
                return;
            }
            var all = (List<ThingStuffPair>)pairsField.GetValue(null);
            if (all == null)
            {
                return;
            }
            List<ThingDef> kit = HeirsAges.UniformKit(pawn);
            List<ThingStuffPair> own;
            if (kit != null)
            {
                // 4.2: in the age of steam an armed troop often wears the nation's uniform in place of the pieces it covers
                uniformKind = pawn.kindDef;
                uniformRestore = pawn.kindDef.apparelRequired;
                uniformWear = kit.Where(d => uniformRestore == null || !uniformRestore.Contains(d)).ToList();
                pawn.kindDef.apparelRequired = kit;
                own = Build(pawn.kindDef, all, kit);
            }
            else
            {
                own = Wardrobe(pawn.kindDef, all);
            }
            if (own.Count == 0)
            {
                return;
            }
            __state = all;
            pairsField.SetValue(null, own);
        }

        public static System.Exception Finalizer(System.Exception __exception, List<ThingStuffPair> __state, Pawn pawn)
        {
            if (uniformKind != null)
            {
                uniformKind.apparelRequired = uniformRestore;
                uniformKind = null;
                uniformRestore = null;
                if (__exception == null && pawn != null && uniformWear.Count > 0)
                {
                    WearMissing(pawn, uniformWear);
                    if (pending.Count > 64)
                    {
                        pending.Clear();
                    }
                    pending[pawn] = uniformWear;
                }
                uniformWear = null;
            }
            if (__state != null)
            {
                pairsField.SetValue(null, __state);
            }
            return __exception;
        }

        public class Patch : HeirsPatch
        {
            public override string Id => "NationKits";

            public override void Apply(HarmonyLib.Harmony harmony)
            {
                pairsField = HarmonyLib.AccessTools.Field(typeof(PawnApparelGenerator), "allApparelPairs");
                if (pairsField == null || !pairsField.IsStatic)
                {
                    throw new System.MissingFieldException("PawnApparelGenerator.allApparelPairs");
                }
                System.Type k = typeof(HeirsKits);
                harmony.Patch(HeirsPatches.Need(typeof(PawnApparelGenerator), "GenerateStartingApparelFor"),
                    prefix: new HarmonyLib.HarmonyMethod(k, nameof(Prefix)), finalizer: new HarmonyLib.HarmonyMethod(k, nameof(Finalizer)));
                harmony.Patch(HeirsPatches.Need(typeof(PawnGenerator), "GeneratePawn", new[] { typeof(PawnGenerationRequest) }),
                    postfix: new HarmonyLib.HarmonyMethod(k, nameof(GeneratePawnPostfix)));
            }
        }
    }
}
