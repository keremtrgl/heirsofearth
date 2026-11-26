using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    public static partial class Probe43
    {
        private static List<ThingDef> AgeFour(NationDef n) => DefDatabase<ThingDef>.AllDefsListForReading
            .Where(d => d.GetModExtension<HeirsAgeExt>() is HeirsAgeExt e && e.nation == n && e.age == 4).ToList();

        /// <summary>Each nation has exactly one Electric gun, helmet, uniform and work, all drawn, and its two researches.</summary>
        public static void Content()
        {
            foreach (string name in Nations)
            {
                NationDef n = N("HE_" + name);
                List<ThingDef> items = AgeFour(n);
                List<ThingDef> guns = items.Where(d => d.IsRangedWeapon).ToList();
                List<ThingDef> helmets = items.Where(d => d.IsApparel && d.apparel.bodyPartGroups.Any(g => g == BodyPartGroupDefOf.UpperHead || g == BodyPartGroupDefOf.FullHead)).ToList();
                List<ThingDef> uniforms = items.Where(d => d.IsApparel && d.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.Torso)).ToList();
                List<ThingDef> works = items.Where(d => d.category == ThingCategory.Building).ToList();
                P.Check(name + " Electric items: 1 gun, 1 helmet, 1 uniform, 1 work",
                    guns.Count == 1 && helmets.Count == 1 && uniforms.Count == 1 && works.Count == 1,
                    guns.Count + "/" + helmets.Count + "/" + uniforms.Count + "/" + works.Count);
                ThingDef gun = guns.FirstOrDefault();
                P.Check(name + " Electric gun is tagged for troops", gun?.weaponTags != null && gun.weaponTags.Contains(HeirsAges.Tag(n, 4)), gun?.defName);
                P.Check(name + " Electric items are drawn", items.All(d => d.graphicData != null && P.HasTexture(d.graphicData.texPath)),
                    string.Join(",", items.Where(d => d.graphicData == null || !P.HasTexture(d.graphicData.texPath)).Select(d => d.defName)));
                ResearchProjectDef army = DefDatabase<ResearchProjectDef>.GetNamedSilentFail("HE_" + name + "_ElectricArmy");
                ResearchProjectDef worksR = DefDatabase<ResearchProjectDef>.GetNamedSilentFail("HE_" + name + "_Works");
                P.Check(name + " Electric researches", army != null && worksR != null && army.techLevel == TechLevel.Industrial
                    && Mathf.Approximately(army.baseCost, 3000f) && Mathf.Approximately(worksR.baseCost, 2600f)
                    && army.GetModExtension<HeirsResearchExt>()?.age == 4 && worksR.GetModExtension<HeirsResearchExt>()?.age == 4,
                    (army?.baseCost ?? -1) + " / " + (worksR?.baseCost ?? -1));
                ThingDef work = works.FirstOrDefault();
                P.Check(name + " work needs power and its research", work != null && work.HasComp(typeof(CompPowerTrader))
                    && work.researchPrerequisites != null && work.researchPrerequisites.Contains(worksR), work?.defName);
            }
        }

        private static Thing Powered(Thing t, bool on)
        {
            CompPowerTrader power = t.TryGetComp<CompPowerTrader>();
            if (power != null) power.PowerOn = on;
            return t;
        }

        private static Thing Place(Map map, string def, IntVec3 at, Rot4 rot)
        {
            ThingDef d = DefDatabase<ThingDef>.GetNamed(def);
            Thing t = ThingMaker.MakeThing(d, d.MadeFromStuff ? GenStuff.DefaultStuffFor(d) : null);
            if (d.CanHaveFaction) t.SetFaction(Faction.OfPlayer);
            return GenSpawn.Spawn(t, at, map, rot);
        }

        /// <summary>The nine works spawn and do what they say while powered, and nothing when the power is off.</summary>
        public static void Works()
        {
            Map map = P.Home;
            foreach (string name in Nations)
            {
                ThingDef work = AgeFour(N("HE_" + name)).FirstOrDefault(d => d.category == ThingCategory.Building);
                if (work == null) continue;
                P.Run("spawn " + work.defName, () =>
                {
                    Thing b = P.SpawnBuilding(work, map);
                    P.Check("spawn " + work.defName, b.Spawned && b.TryGetComp<CompPowerTrader>() != null);
                    string unused = b.GetInspectString();
                    b.Destroy();
                });
            }

            P.Run("lectern speeds research only with power", () =>
            {
                IntVec3 patch = P.FreeSpot(map, new IntVec2(10, 10));
                Thing bench = Place(map, "SimpleResearchBench", patch + new IntVec3(0, 0, -2), Rot4.South);
                float before = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                Thing lectern = Powered(Place(map, "HE_Hellas_Lectern", patch + new IntVec3(0, 0, 2), Rot4.North), true);
                P.Ticks(10);
                CompAffectedByFacilities links = bench.TryGetComp<CompAffectedByFacilities>();
                float on = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                Powered(lectern, false);
                float off = bench.GetStatValue(StatDefOf.ResearchSpeedFactor);
                P.Check("lectern linked", links != null && links.LinkedFacilitiesListForReading.Contains(lectern));
                P.Check("lectern speeds research when powered", on > before + 0.005f && Mathf.Abs(off - before) < 0.001f,
                    before.ToString("F3") + " -> " + on.ToString("F3") + ", off " + off.ToString("F3"));
                lectern.Destroy();
                bench.Destroy();
            });

            P.Run("printing press speeds tailoring", () =>
            {
                IntVec3 patch = P.FreeSpot(map, new IntVec2(10, 10));
                Thing bench = Place(map, "HandTailoringBench", patch + new IntVec3(0, 0, -2), Rot4.South);
                StatDef speed = DefDatabase<StatDef>.GetNamed("WorkTableWorkSpeedFactor");
                float before = bench.GetStatValue(speed);
                Thing press = Powered(Place(map, "HE_Tianxia_PrintingPress", patch + new IntVec3(0, 0, 2), Rot4.North), true);
                P.Ticks(10);
                float on = bench.GetStatValue(speed);
                P.Check("press speeds tailoring", on > before + 0.05f, before.ToString("F2") + " -> " + on.ToString("F2"));
                press.Destroy();
                bench.Destroy();
            });

            P.Run("forge and loom take the old tables' bills", () =>
            {
                ThingDef forge = DefDatabase<ThingDef>.GetNamed("HE_Nord_ElectricForge"), smithy = DefDatabase<ThingDef>.GetNamed("ElectricSmithy");
                ThingDef loom = DefDatabase<ThingDef>.GetNamed("HE_Pars_ElectricLoom"), old = DefDatabase<ThingDef>.GetNamed("HE_Pars_CarpetLoom");
                List<RecipeDef> missing = smithy.AllRecipes.Where(r => !forge.AllRecipes.Contains(r)).ToList();
                P.Check("forge has every smithy bill", smithy.AllRecipes.Count > 5 && missing.Count == 0,
                    forge.AllRecipes.Count + " bills, missing " + string.Join(",", missing.Select(r => r.defName)));
                P.Check("electric loom has every carpet loom bill", old.AllRecipes.Count > 0 && old.AllRecipes.All(loom.AllRecipes.Contains),
                    old.AllRecipes.Count + " / " + loom.AllRecipes.Count);
                StatDef speed = DefDatabase<StatDef>.GetNamed("WorkTableWorkSpeedFactor");
                P.Check("forge and loom are faster", Mathf.Approximately(forge.GetStatValueAbstract(speed), 1.25f) && Mathf.Approximately(loom.GetStatValueAbstract(speed), 1.4f));
            });

            P.Run("telegraph sends goodwill only when powered", () =>
            {
                HeirsGame g = HeirsGame.Get;
                int keepTick = g.lastTelegramTick;
                Thing office = Powered(P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Albion_TelegraphOffice"), map), true);
                Thing second = Powered(P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Albion_TelegraphOffice"), map), true);
                Dictionary<Faction, int> before = HeirsWorld.LiveNations.Select(HeirsWorld.FactionOf)
                    .Where(f => f != null && !f.HostileTo(Faction.OfPlayer)).ToDictionary(f => f, f => f.PlayerGoodwill);
                int raised = 0;
                try
                {
                    raised = HeirsWorks.SendTelegrams(g);
                    int up = before.Count(p => p.Key.PlayerGoodwill == Mathf.Min(100, p.Value + 1));
                    P.Check("telegraph raises each friendly nation by 1 (two offices count once)", before.Count > 0 && up == before.Count && raised <= before.Count,
                        up + "/" + before.Count + " raised " + raised);
                    Powered(office, false);
                    Powered(second, false);
                    P.Check("unpowered telegraph sends nothing", HeirsWorks.SendTelegrams(g) == 0);
                }
                finally
                {
                    foreach (KeyValuePair<Faction, int> p in before)
                    {
                        int diff = p.Value - p.Key.PlayerGoodwill;
                        if (diff != 0) p.Key.TryAffectGoodwillWith(Faction.OfPlayer, diff, false, false, null);
                    }
                    g.lastTelegramTick = keepTick;
                    office.Destroy();
                    second.Destroy();
                }
            });

            P.Run("irrigation pump waters plants within 6 cells", () =>
            {
                IntVec3 patch = P.FreeSpot(map, new IntVec2(16, 3));
                Thing pump = Powered(Place(map, "HE_Kemet_IrrigationPump", patch + new IntVec3(-6, 0, 0), Rot4.South), true);
                ThingDef potato = DefDatabase<ThingDef>.GetNamed("Plant_Potato");
                Plant near = (Plant)GenSpawn.Spawn(ThingMaker.MakeThing(potato), patch + new IntVec3(-3, 0, 0), map);
                Plant far = (Plant)GenSpawn.Spawn(ThingMaker.MakeThing(potato), patch + new IntVec3(7, 0, 0), map);
                HeirsWorks.ResetIrrigation();
                try
                {
                    P.Check("irrigation factor", Mathf.Approximately(HeirsWorks.GrowthFactorFor(near), 1.15f) && HeirsWorks.GrowthFactorFor(far) == 1f,
                        HeirsWorks.GrowthFactorFor(near) + " / " + HeirsWorks.GrowthFactorFor(far));
                    float rNear = near.GrowthRate, rFar = far.GrowthRate;
                    float fNear = near.Position.GetTerrain(map).fertility, fFar = far.Position.GetTerrain(map).fertility;
                    if (rFar > 0f && Mathf.Approximately(fNear, fFar))
                    {
                        P.Check("irrigated plant grows 15% faster", Mathf.Abs(rNear / rFar - 1.15f) < 0.02f, rFar.ToString("F3") + " -> " + rNear.ToString("F3"));
                    }
                    else
                    {
                        P.Say("growth compare skipped: rate " + rFar.ToString("F2") + ", fertility " + fNear + "/" + fFar);
                    }
                    Powered(pump, false);
                    HeirsWorks.ResetIrrigation();
                    P.Check("pump without power waters nothing", HeirsWorks.GrowthFactorFor(near) == 1f);
                }
                finally
                {
                    near.Destroy();
                    far.Destroy();
                    pump.Destroy();
                    HeirsWorks.ResetIrrigation();
                }
            });

            P.Run("cold store slows rot only with power", () =>
            {
                Thing store = Powered(P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Inti_ColdStore"), map), true);
                Thing qullqa = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Inti_Qullqa"), map);
                HeirsFoodStorePatch.Reset();
                Thing meat = ThingMaker.MakeThing(ThingDefOf.Meat_Human);
                meat.stackCount = 10;
                GenSpawn.Spawn(meat, store.Position, map);
                Thing meat2 = ThingMaker.MakeThing(ThingDefOf.Meat_Human);
                meat2.stackCount = 10;
                GenSpawn.Spawn(meat2, qullqa.Position, map);
                try
                {
                    float cold = HeirsFoodStorePatch.FactorFor(meat), dry = HeirsFoodStorePatch.FactorFor(meat2);
                    P.Check("cold store rots slower than the qullqa", Mathf.Abs(cold - 0.35f) < 0.01f && cold < dry, cold + " vs " + dry);
                    Powered(store, false);
                    HeirsFoodStorePatch.Reset();
                    P.Check("cold store without power is a plain shelf", HeirsFoodStorePatch.FactorFor(meat) == 1f, HeirsFoodStorePatch.FactorFor(meat).ToString());
                }
                finally
                {
                    if (!meat.Destroyed) meat.Destroy();
                    if (!meat2.Destroyed) meat2.Destroy();
                    store.Destroy();
                    qullqa.Destroy();
                    HeirsFoodStorePatch.Reset();
                }
            });
        }
    }
}
