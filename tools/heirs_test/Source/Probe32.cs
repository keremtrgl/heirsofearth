using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using Verse;

namespace HeProbe
{
    /// <summary>3.2 checks: every nation has the same depth of content, the eight new defensive structures shoot,
    /// the new lamps and altars light and burn, clothes have worn graphics, and regalia raise social impact.</summary>
    public static class Probe32
    {
        static string Key(NationDef n) => n.defName.Substring(3);

        static bool Of(Def d, NationDef n) => d.GetModExtension<HeirsCultureExt>()?.nation == n;

        public static void Content()
        {
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                List<ThingDef> things = DefDatabase<ThingDef>.AllDefsListForReading.Where(d => Of(d, n)).ToList();
                int weapons = things.Count(d => d.IsWeapon);
                int apparel = things.Count(d => d.IsApparel);
                int buildings = things.Count(d => d.category == ThingCategory.Building && d.designationCategory != null);
                int food = things.Count(d => d.IsIngestible && !d.IsDrug);
                int floors = DefDatabase<TerrainDef>.AllDefsListForReading.Count(t => t.defName.StartsWith("HE_" + Key(n) + "_"));
                bool turret = things.Any(d => d.building?.turretGunDef != null);
                P.Check("equal heritage " + n.defName, weapons >= 5 && apparel >= 5 && buildings >= 5 && food >= 3 && floors >= 3 && turret,
                    "weapons " + weapons + ", apparel " + apparel + ", buildings " + buildings + ", food " + food + ", floors " + floors + ", turret " + turret);
            }
            var spots = new Dictionary<string, string>();
            var clash = new List<string>();
            foreach (ResearchProjectDef r in DefDatabase<ResearchProjectDef>.AllDefsListForReading.Where(r => r.tab?.defName == "HE_WorldHeritage"))
            {
                string key = r.ResearchViewX.ToString("F2") + "," + r.ResearchViewY.ToString("F2");
                if (spots.TryGetValue(key, out string other)) clash.Add(other + "/" + r.defName);
                else spots[key] = r.defName;
            }
            P.Check("no two heir research projects share a spot", clash.Count == 0, string.Join(" ", clash));
        }

        public static void Turrets()
        {
            Map map = P.Home;
            Faction enemy = Find.FactionManager.AllFactions.FirstOrDefault(f => !f.IsPlayer && f.HostileTo(Faction.OfPlayer) && f.def.humanlikeFaction);
            foreach (ThingDef def in DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.defName.StartsWith("HE_") && d.building?.turretGunDef != null && !d.HasComp(typeof(CompMannable))).ToList())
            {
                ThingDef turretDef = def;
                P.Run("turret " + turretDef.defName, () =>
                {
                    P.Calm();
                    P.FairWeather(map);
                    var turret = (Building_TurretGun)P.SpawnBuilding(turretDef, map);
                    CompRefuelable fuel = turret.TryGetComp<CompRefuelable>();
                    VerbProperties verb = turretDef.building.turretGunDef.Verbs[0];
                    P.Check("turret gun " + turretDef.defName, turret.gun != null && turret.gun.def == turretDef.building.turretGunDef
                        && turret.gun.Graphic?.MatSingle?.mainTexture != BaseContent.BadTex);
                    P.Check("turret starts empty " + turretDef.defName, fuel != null && fuel.Fuel == 0f);
                    if (fuel == null) { turret.Destroy(); return; }
                    fuel.Refuel(fuel.Props.fuelCapacity / fuel.Props.FuelMultiplierCurrentDifficulty);
                    float full = fuel.Fuel;
                    P.Check("turret loaded " + turretDef.defName, full >= fuel.Props.fuelCapacity - 0.5f, full.ToString("F1"));
                    if (enemy == null) { P.Say("no hostile faction"); turret.Destroy(); return; }
                    float near = System.Math.Max(verb.minRange + 2f, 7f), far = System.Math.Min(verb.range - 2f, 16f);
                    Pawn target = PawnGenerator.GeneratePawn(PawnKindDefOf.Villager, enemy);
                    IntVec3 cell = GenRadial.RadialCellsAround(turret.Position, far, false)
                        .Where(x => x.InBounds(map) && x.DistanceTo(turret.Position) >= near && x.Standable(map) && !x.Fogged(map)
                                    && GenSight.LineOfSight(turret.Position, x, map, true))
                        .OrderBy(x => x.Roofed(map) ? 1 : 0).FirstOrDefault();
                    if (!cell.IsValid) cell = CellFinder.RandomClosewalkCellNear(turret.Position + new IntVec3((int)near + 2, 0, 0), map, 2);
                    GenSpawn.Spawn(target, cell, map);
                    Verse.AI.Group.LordMaker.MakeNewLord(enemy, new Verse.AI.Group.LordJob_DefendPoint(cell, 0f, 1f, false, false), map, new[] { target }); // hold the spot: a charging target slips inside the minimum range
                    P.Ticks(1200);
                    P.Check("turret fires " + turretDef.defName, fuel.Fuel < full,
                        "fuel " + fuel.Fuel.ToString("F1") + "/" + full.ToString("F1") + ", target " + (target.Dead ? "dead" : target.Downed ? "downed" : target.Spawned ? "standing" : "gone")
                        + ", distance " + turret.Position.DistanceTo(target.Position).ToString("F0") + ", current " + (turret.CurrentTarget.Thing?.LabelShort ?? "none"));
                    P.Gone(target);
                    turret.Destroy();
                    P.Calm();
                });
            }
        }

        public static void Lights()
        {
            Map map = P.Home;
            P.Run("3.2 lights", () =>
            {
                P.FairWeather(map);
                foreach (string name in new[] { "HE_Kemet_LotusLamp", "HE_Pars_FireAltar" })
                {
                    Thing t = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed(name), map);
                    CompRefuelable fuel = t.TryGetComp<CompRefuelable>();
                    CompGlower glow = t.TryGetComp<CompGlower>();
                    P.Ticks(300);
                    P.Check("fire burns " + name, fuel != null && fuel.HasFuel && fuel.Fuel < fuel.Props.fuelCapacity && glow != null, fuel == null ? "no fuel" : fuel.Fuel.ToString("F2"));
                    t.Destroy();
                }
                Thing lamp = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Albion_GasLamp"), map);
                P.Check("gas lamp needs power", lamp.TryGetComp<CompPowerTrader>() != null && lamp.TryGetComp<CompFlickable>() != null && lamp.TryGetComp<CompGlower>() != null);
                lamp.Destroy();
                ThingDef altar = DefDatabase<ThingDef>.GetNamed("HE_Pars_FireAltar");
                P.Check("fire altar warms", altar.comps.Any(c => c is CompProperties_HeatPusher));
            });
        }

        public static void Clothes()
        {
            Map map = P.Home;
            Pawn pawn = P.Colonist(map);
            var missing = new List<string>();
            foreach (ThingDef d in DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.IsApparel && d.defName.StartsWith("HE_") && !d.apparel.wornGraphicPath.NullOrEmpty()))
            {
                bool head = d.apparel.LastLayer == ApparelLayerDefOf.Overhead || d.apparel.LastLayer == ApparelLayerDefOf.EyeCover;
                string path = head ? d.apparel.wornGraphicPath + "_south" : d.apparel.wornGraphicPath + "_" + pawn.story.bodyType.defName + "_south";
                if (!P.HasTexture(path)) missing.Add(d.defName + ":" + path);
            }
            P.Check("every heir garment has a worn graphic for this body", missing.Count == 0, string.Join(" ", missing));

            P.Run("3.2 regalia", () =>
            {
                foreach (string name in new[] { "HE_Roma_Laurel", "HE_Nord_Circlet", "HE_Tianxia_DragonRobe", "HE_Albion_Bicorne", "HE_Kemet_Nemes", "HE_Pars_Kidaris", "HE_Inti_Mascaypacha" })
                {
                    ThingDef def = DefDatabase<ThingDef>.GetNamed(name);
                    var worn = pawn.apparel.WornApparel.ToList();
                    float before = pawn.GetStatValue(StatDefOf.SocialImpact, true, 0);
                    var item = (Apparel)ThingMaker.MakeThing(def, def.MadeFromStuff ? GenStuff.DefaultStuffFor(def) : null);
                    pawn.apparel.Wear(item, true);
                    float after = pawn.GetStatValue(StatDefOf.SocialImpact, true, 0);
                    P.Check("regalia raises social impact " + name, pawn.apparel.WornApparel.Contains(item) && after > before + 0.05f, before.ToString("F2") + " -> " + after.ToString("F2"));
                    pawn.apparel.Remove(item);
                    item.Destroy();
                    foreach (Apparel a in worn.Where(a => !pawn.apparel.WornApparel.Contains(a) && !a.Destroyed && !a.Spawned && a.ParentHolder == null))
                    {
                        pawn.apparel.Wear(a, false);
                    }
                }
            });
        }
    }
}
