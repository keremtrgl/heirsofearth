using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>4.3 checks: the Electric Age (thresholds, troops, gates), its items, the nine works and the World Fair.</summary>
    public static partial class Probe43
    {
        private static NationDef N(string name) => DefDatabase<NationDef>.GetNamed(name);

        public static readonly string[] Nations = { "Roma", "Yamato", "Nord", "Hellas", "Tianxia", "Albion", "Kemet", "Pars", "Inti" };

        private static void Discard(Pawn p)
        {
            if (!p.Destroyed) p.Destroy();
            if (Find.WorldPawns.Contains(p)) Find.WorldPawns.RemoveAndDiscardPawnViaGC(p);
        }

        /// <summary>Thresholds, the bar toward the next age, the setback floor and the once-only letter.</summary>
        public static void Ages()
        {
            P.Check("age IV starts at 18", HeirsAges.AgeFor(17.99f) == 3 && HeirsAges.AgeFor(18f) == 4 && HeirsAges.LastAge == 4,
                HeirsAges.AgeFor(17.99f) + "/" + HeirsAges.AgeFor(18f));
            HeirsGame g = HeirsGame.Get;
            NationDef roma = N("HE_Roma");
            float keep = g.AgeProgress(roma);
            int shown = g.AgeShown(roma);
            try
            {
                g.SetAgeProgress(roma, 13.5f);
                P.Check("bar toward the Electric Age", Mathf.Abs(HeirsAges.ToNext(roma) - 0.5f) < 0.01f, HeirsAges.ToNext(roma).ToString("0.00"));
                g.SetAgeProgress(roma, 18.05f);
                HeirsAges.Setback(roma, false);
                P.Check("setback never drops out of the Electric Age", g.AgeProgress(roma) >= 18f, g.AgeProgress(roma).ToString("0.00"));
                P.Check("last age has a full bar", Mathf.Approximately(HeirsAges.ToNext(roma), 1f));

                g.SetAgeProgress(roma, 17.5f);
                g.SetAgeShown(roma, 3);
                int letters = Find.LetterStack.LettersListForReading.Count;
                int heard = 0;
                bool fairHeld = g.worldFairHeld;
                g.worldFairHeld = true; // the age IV event would also send the World Fair letter; that has its own probe
                System.Action<NationDef, int> listen = (n, a) => { if (n == roma && a == 4) heard++; };
                HeirsAges.OnAgeReached += listen;
                try
                {
                    g.SetAgeProgress(roma, 18.2f);
                    HeirsAges.Announce(g, roma);
                    HeirsAges.Announce(g, roma);
                    // a 4.2 save whose nation is already past 18: shown stays 4 after a reload, so no second letter
                    g.SetAgeShown(roma, 4);
                    HeirsAges.Announce(g, roma);
                }
                finally
                {
                    HeirsAges.OnAgeReached -= listen;
                    g.worldFairHeld = fairHeld;
                }
                P.Check("Electric Age letter comes once", Find.LetterStack.LettersListForReading.Count - letters == 1 && heard == 1,
                    (Find.LetterStack.LettersListForReading.Count - letters) + " letters, " + heard + " events");
                P.Check("Electric Age label", HeirsAges.AgeLabel(4) == "HE_Age4".Translate().Resolve() && !HeirsAges.AgeLabel(4).StartsWith("HE_"), HeirsAges.AgeLabel(4));
            }
            finally
            {
                g.SetAgeProgress(roma, keep);
                g.SetAgeShown(roma, shown);
                while (Find.LetterStack.LettersListForReading.Count > 0) Find.LetterStack.RemoveLetter(Find.LetterStack.LettersListForReading[0]);
            }
        }

        /// <summary>Gates and switching ages off: age IV items wait for the age; with ages off nothing is held back.</summary>
        public static void Gates()
        {
            HeirsGame g = HeirsGame.Get;
            NationDef roma = N("HE_Roma");
            float keep = g.AgeProgress(roma);
            bool on = HeirsMod.Settings.ages;
            ThingDef gun = HeirsAges.AgeItems(roma, 4).FirstOrDefault(d => d.IsRangedWeapon);
            if (gun == null)
            {
                P.Check("Roma has an Electric Age gun", false);
                return;
            }
            try
            {
                g.SetAgeProgress(roma, 10f);
                P.Check("Electric gun held back in the Age of Steam", HeirsAges.Locked(gun), gun.defName);
                g.SetAgeProgress(roma, 18.1f);
                P.Check("Electric gun opens in the Electric Age", !HeirsAges.Locked(gun), gun.defName);
                g.SetAgeProgress(roma, 10f);
                HeirsMod.Settings.ages = false;
                P.Check("ages off: nothing held back", !HeirsAges.Locked(gun) && HeirsAges.AgeOf(roma) == 1);
            }
            finally
            {
                HeirsMod.Settings.ages = on;
                g.SetAgeProgress(roma, keep);
            }
        }

        /// <summary>Electric Age troops: new guns, field uniforms and helmets in the expected shares, and no clothes that clash.</summary>
        public static void Troops()
        {
            HeirsGame g = HeirsGame.Get;
            foreach (string name in new[] { "HE_Roma", "HE_Yamato" })
            {
                NationDef n = N(name);
                float keep = g.AgeProgress(n);
                string tag = n.defName.Substring(3);
                List<PawnKindDef> kinds = DefDatabase<PawnKindDef>.AllDefsListForReading
                    .Where(k => !k.factionLeader && k.weaponTags != null && k.weaponTags.Contains("HE_" + tag + "Ranged") && HeirsKits.NationOfKind(k) == n).ToList();
                Faction faction = Find.FactionManager.FirstFactionOfDef(n.faction);
                if (kinds.Count == 0 || faction == null)
                {
                    P.Check(name + " electric troop kinds", false, kinds.Count + " " + (faction != null));
                    continue;
                }
                ThingDef uniform = HeirsAges.UniformOf(n, 4), helmet = HeirsAges.HelmetOf(n);
                int total = 120, guns = 0, uniforms = 0, helmets = 0, clashes = 0;
                try
                {
                    g.SetAgeProgress(n, 18.5f);
                    for (int i = 0; i < total; i++)
                    {
                        PawnKindDef kind = kinds[i % kinds.Count];
                        Pawn p = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, faction, PawnGenerationContext.NonPlayer, forceGenerateNewPawn: true, mustBeCapableOfViolence: true));
                        ThingDef gun = p.equipment?.Primary?.def;
                        if (gun?.weaponTags != null && gun.weaponTags.Contains(HeirsAges.Tag(n, 4))) guns++;
                        List<Apparel> worn = p.apparel?.WornApparel ?? new List<Apparel>();
                        if (worn.Any(a => a.def == uniform)) uniforms++;
                        if (worn.Any(a => a.def == helmet)) helmets++;
                        for (int a = 0; a < worn.Count; a++)
                            for (int b = a + 1; b < worn.Count; b++)
                                if (!ApparelUtility.CanWearTogether(worn[a].def, worn[b].def, p.RaceProps.body)) clashes++;
                        Discard(p);
                    }
                }
                finally
                {
                    g.SetAgeProgress(n, keep);
                }
                P.Check(name + " Electric troops carry the new gun", guns >= total * 0.22f && guns <= total * 0.58f, guns + "/" + total);
                P.Check(name + " Electric troops wear the field uniform", uniform != null && uniforms >= total * 0.36f && uniforms <= total * 0.72f, uniforms + "/" + total);
                P.Check(name + " Electric troops wear the steel helmet", helmet != null && helmets >= total * 0.3f && helmets <= total * 0.72f, helmets + "/" + total);
                P.Check(name + " Electric troops wear nothing that clashes", clashes == 0, clashes.ToString());
            }
        }
    }
}
