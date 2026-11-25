using System.Collections.Generic;
using System.Linq;
using RimWorld;
using Verse;

namespace HeProbe
{
    /// <summary>4.0 checks: the heir crowns satisfy Royalty's noble headgear rule (tested with the game's own ApparelRequirement).</summary>
    public static class Probe40
    {
        private static List<ThingDef> Matching(string tag) => new ApparelRequirement
        {
            bodyPartGroupsMatchAny = new List<BodyPartGroupDef> { BodyPartGroupDefOf.UpperHead, BodyPartGroupDefOf.FullHead },
            requiredTags = new List<string> { tag },
        }.AllRequiredApparel().Where(d => d.defName.StartsWith("HE_")).ToList();

        public static void Royalty()
        {
            var tier5 = Matching("RoyalTier5").Select(d => d.defName).ToList();
            var tier6 = Matching("RoyalTier6").Select(d => d.defName).ToList();
            var crowns = new[] { "HE_Kemet_Khepresh", "HE_Pars_Kidaris", "HE_Inti_Mascaypacha" };
            var lesser = new[] { "HE_Roma_Laurel", "HE_Kemet_Nemes", "HE_Nord_Circlet" };
            P.Check("crowns fit a baron or count", crowns.Concat(lesser).All(tier5.Contains) && tier5.Count == 6, string.Join(",", tier5));
            P.Check("crowns fit a consul", crowns.All(tier6.Contains) && tier6.Count == 3, string.Join(",", tier6));
            P.Check("helmets and hats are not noble headgear", !tier5.Any(n => n.Contains("Helm") || n.Contains("Hat") || n.Contains("Kabuto") || n.Contains("Galea")));
        }
    }
}
