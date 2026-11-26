using System.Collections.Generic;
using System.Linq;
using HeirsOfEarth;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeProbe
{
    /// <summary>4.2 checks: the fourth speed button and the ages of progress (data, progress and letters, troops' guns and uniforms,
    /// the research gate, traders and the setback floor).</summary>
    public static class Probe42
    {
        private static NationDef N(string name) => DefDatabase<NationDef>.GetNamed(name);

        public static void Speed()
        {
            P.Check("fourth speed patch active", HeirsPatches.Active("FourthSpeed") && HeirsSpeed.Enabled);
            Texture2D icon = HeirsSpeed.BuildIcon();
            Texture2D three = TexButton.SpeedButtonTextures[(int)TimeSpeed.Superfast];
            P.Check("fourth speed icon built from the game's arrows", icon != null && icon.width == three.width && icon.height == three.height,
                icon == null ? "null" : icon.width + "x" + icon.height);
            P.Check("fourth speed key shown outside dev mode", !KeyBindingDefOf.TimeSpeed_Ultrafast.devModeOnly);
            // 4.2.2: the row of five buttons stays on the screen when the game gives room for four at the right edge.
            float but = TimeControls.TimeButSize.x;
            Rect four = new Rect(1920f - but * 4f, 1000f, but * 4f, 24f);
            Rect fit = HeirsSpeed.Fit(four, but * 5f, 1920f);
            P.Check("fourth speed row stays on screen", fit.xMax <= 1920.01f && Mathf.Approximately(fit.width, but * 5f) && fit.x >= 0f,
                fit.x + ".." + fit.xMax);
            Rect wide = HeirsSpeed.Fit(new Rect(1700f, 1000f, 400f, 24f), but * 5f, 1920f);
            P.Check("fourth speed row pulled back from past the edge", wide.x + but * 5f <= 1920.01f, wide.x.ToString());
            TimeSpeed before = Find.TickManager.CurTimeSpeed;
            Find.TickManager.CurTimeSpeed = TimeSpeed.Ultrafast;
            P.Check("fourth speed runs at 15x", Mathf.Approximately(Find.TickManager.TickRateMultiplier, 15f) || Find.TickManager.slower.ForcedNormalSpeed,
                Find.TickManager.TickRateMultiplier.ToString());
            Find.TickManager.CurTimeSpeed = before;
        }

        public static void Data()
        {
            var bad = new List<string>();
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                for (int age = 2; age <= 3; age++)
                {
                    string tag = HeirsAges.Tag(n, age);
                    List<ThingDef> guns = DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.weaponTags != null && d.weaponTags.Contains(tag)).ToList();
                    if (guns.Count == 0) bad.Add(tag + " no gun");
                    if (guns.Any(gun => gun.GetModExtension<HeirsAgeExt>() is HeirsAgeExt e && (e.nation != n || e.age != age))) bad.Add(tag + " ext");
                }
                ThingDef coat = HeirsAges.UniformOf(n);
                if (coat == null) bad.Add(n.defName + " no uniform");
                else if (coat.MadeFromStuff || coat.colorGenerator == null) bad.Add(coat.defName + " colour");
            }
            P.Check("every nation has guns for ages II and III and a uniform", bad.Count == 0, string.Join(", ", bad));
            List<ResearchProjectDef> gated = DefDatabase<ResearchProjectDef>.AllDefsListForReading.Where(r => r.GetModExtension<HeirsResearchExt>()?.age > 1).ToList();
            P.Check("age research gated", gated.Count >= 15 && gated.All(r => r.GetModExtension<HeirsResearchExt>().nation != null), gated.Count.ToString());
            P.Check("ages patch active", HeirsPatches.Active("Ages"));
        }

        /// <summary>Progress grows each day, an age is announced once with a letter, and a setback never takes an age away.</summary>
        public static void Progress()
        {
            HeirsGame g = HeirsGame.Get;
            NationDef nord = N("HE_Nord");
            float keep = g.AgeProgress(nord);
            int shown = g.AgeShown(nord);
            try
            {
                g.SetAgeProgress(nord, 1.0f);
                g.SetAgeShown(nord, 1);
                HeirsAges.DailyTick(g);
                float after = g.AgeProgress(nord);
                P.Check("ages advance daily", after > 1.0f && after < 1.1f, after.ToString("0.0000"));
                P.Check("age I below the Age of Powder", HeirsAges.AgeOf(nord) == 1);

                int letters = Find.LetterStack.LettersListForReading.Count;
                g.SetAgeProgress(nord, HeirsAges.AgeTwoAt + 0.001f);
                HeirsAges.DailyTick(g);
                P.Check("age II announced once", g.AgeShown(nord) == 2 && Find.LetterStack.LettersListForReading.Count == letters + 1,
                    g.AgeShown(nord) + " / " + (Find.LetterStack.LettersListForReading.Count - letters));
                HeirsAges.DailyTick(g);
                P.Check("no second letter", Find.LetterStack.LettersListForReading.Count == letters + 1);

                g.SetAgeProgress(nord, HeirsAges.AgeTwoAt + 0.05f);
                HeirsAges.Setback(nord, false);
                P.Check("a setback never takes an age away", g.AgeProgress(nord) >= HeirsAges.AgeTwoAt && HeirsAges.AgeOf(nord) == 2,
                    g.AgeProgress(nord).ToString("0.000"));
                g.SetAgeProgress(nord, 1.0f);
                HeirsAges.Setback(nord, true);
                P.Check("a setback slows age I", Mathf.Abs(g.AgeProgress(nord) - (1.0f - HeirsAges.SetbackHelped)) < 0.001f, g.AgeProgress(nord).ToString("0.000"));
                // a 4.2.0 save: age II was announced at 2.5, below the 4.2.1 threshold; the nation keeps its age
                g.SetAgeProgress(nord, 2.6f);
                g.SetAgeShown(nord, 2);
                HeirsAges.DailyTick(g);
                P.Check("a 4.2.0 save keeps its ages", HeirsAges.AgeOf(nord) == 2 && g.AgeProgress(nord) >= HeirsAges.AgeTwoAt, g.AgeProgress(nord).ToString("0.000"));
                var parts = new List<string>();
                float rate = HeirsAges.Rate(nord, parts);
                P.Check("rate explained", rate >= HeirsAges.MinRate && parts.Count >= 1, rate + " " + string.Join("; ", parts));
            }
            finally
            {
                g.SetAgeProgress(nord, keep);
                g.SetAgeShown(nord, shown);
                while (Find.LetterStack.LettersListForReading.Count > 0) Find.LetterStack.RemoveLetter(Find.LetterStack.LettersListForReading[0]);
            }
        }

        /// <summary>Troops of a nation carry its age guns and uniforms only once it has reached that age.</summary>
        public static void Troops()
        {
            HeirsGame g = HeirsGame.Get;
            foreach (string name in new[] { "HE_Roma", "HE_Albion" })
            {
                NationDef n = N(name);
                float keep = g.AgeProgress(n);
                string tag = n.defName.Substring(3);
                List<PawnKindDef> kinds = DefDatabase<PawnKindDef>.AllDefsListForReading
                    .Where(k => !k.factionLeader && k.weaponTags != null && k.weaponTags.Contains("HE_" + tag + "Ranged") && HeirsKits.NationOfKind(k) == n).ToList();
                Faction faction = Find.FactionManager.FirstFactionOfDef(n.faction);
                if (kinds.Count == 0 || faction == null)
                {
                    P.Check(name + " troop kinds", false, kinds.Count + " " + (faction != null));
                    continue;
                }
                try
                {
                    int[] ageGuns = new int[4], coats = new int[4], armed = new int[4];
                    foreach (int age in new[] { 1, 3 })
                    {
                        g.SetAgeProgress(n, age == 1 ? 0f : HeirsAges.AgeThreeAt + 0.1f);
                        for (int i = 0; i < 40; i++)
                        {
                            PawnKindDef kind = kinds[i % kinds.Count];
                            Pawn p = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, faction, PawnGenerationContext.NonPlayer, forceGenerateNewPawn: true, mustBeCapableOfViolence: true));
                            if (p.equipment?.Primary != null) armed[age]++;
                            ThingDef gun = p.equipment?.Primary?.def;
                            // age I: no gun held back for a later age; age III: guns of the nation's ages (new ones and its older guns tagged for an age)
                            if (gun != null && (age == 1 ? gun.GetModExtension<HeirsAgeExt>()?.nation == n
                                : gun.weaponTags != null && (gun.weaponTags.Contains(HeirsAges.Tag(n, 2)) || gun.weaponTags.Contains(HeirsAges.Tag(n, 3))))) ageGuns[age]++;
                            if (p.apparel != null && p.apparel.WornApparel.Any(a => a.def.GetModExtension<HeirsAgeExt>()?.nation == n)) coats[age]++;
                            p.Destroy();
                            // 4.2.1: a destroyed pawn stays among the world's dead until the world pawn GC runs, and its name stays taken;
                            // 80 per nation here used up a good part of the name pool the name test below then measures.
                            if (Find.WorldPawns.Contains(p)) Find.WorldPawns.RemoveAndDiscardPawnViaGC(p);
                        }
                    }
                    P.Check(name + " age I troops keep the old arms", ageGuns[1] == 0 && coats[1] == 0, ageGuns[1] + " guns, " + coats[1] + " coats");
                    P.Check(name + " age III troops carry age guns", ageGuns[3] >= 12 && armed[3] >= 36, ageGuns[3] + "/40 age guns, armed " + armed[3]);
                    P.Check(name + " age III troops wear the uniform", coats[3] >= 8, coats[3] + "/40");
                }
                finally
                {
                    g.SetAgeProgress(n, keep);
                }
            }
        }

        /// <summary>Research of another nation's age waits for that age; traders do not sell an age's items before it.</summary>
        public static void Gates()
        {
            HeirsGame g = HeirsGame.Get;
            NationDef n = DefDatabase<NationDef>.AllDefsListForReading.First(x => x != g.heritage);
            float keep = g.AgeProgress(n);
            ResearchProjectDef project = DefDatabase<ResearchProjectDef>.AllDefsListForReading
                .First(r => r.GetModExtension<HeirsResearchExt>() is HeirsResearchExt e && e.nation == n && e.age == 3);
            ThingDef coat = HeirsAges.UniformOf(n);
            var stock = new StockGenerator_Tag();
            P.Set(stock, "tradeTag", "HE_" + n.defName.Substring(3) + "Goods");
            try
            {
                g.SetAgeProgress(n, 0f);
                bool can = g.CanStart(project, out string reason);
                P.Check("research waits for the age", !can && reason != null && reason.Contains(HeirsAges.AgeLabel(3)), project.defName + ": " + reason);
                P.Check("traders hold back an age's items", !stock.HandlesThingDef(coat), coat.defName);
                g.SetAgeProgress(n, HeirsAges.AgeThreeAt + 0.1f);
                can = g.CanStart(project, out reason);
                P.Check("research opens with the age", can || reason == null || !reason.Contains(HeirsAges.AgeLabel(3)), reason);
                P.Check("traders sell them once the age comes", stock.HandlesThingDef(coat), coat.defName);
            }
            finally
            {
                g.SetAgeProgress(n, keep);
            }
        }

        /// <summary>4.2.1: the storehouse patch costs almost nothing per rottable thing, and a store that is torn down stops counting.</summary>
        public static void StoreSpeed()
        {
            Map map = P.Home;
            Thing potato = ThingMaker.MakeThing(ThingDefOf.RawPotatoes);
            potato.stackCount = 5;
            GenSpawn.Spawn(potato, P.FreeSpot(map, new IntVec2(1, 1)), map);
            HeirsFoodStorePatch.Reset();
            var watch = System.Diagnostics.Stopwatch.StartNew();
            for (int i = 0; i < 100000; i++) HeirsFoodStorePatch.FactorFor(potato);
            watch.Stop();
            P.Check("storehouse lookup is cheap", watch.ElapsedMilliseconds < 60, watch.ElapsedMilliseconds + " ms per 100000 rottable checks");
            Thing store = P.SpawnBuilding(DefDatabase<ThingDef>.GetNamed("HE_Inti_Qullqa"), map);
            Thing inStore = ThingMaker.MakeThing(ThingDefOf.RawPotatoes);
            inStore.stackCount = 5;
            GenSpawn.Spawn(inStore, store.Position, map);
            HeirsFoodStorePatch.Reset();
            bool seen = HeirsFoodStorePatch.FactorFor(inStore) < 1f;
            IntVec3 cell = store.Position;
            store.Destroy();
            P.Ticks(HeirsFoodStorePatch.RefreshTicks + 5);
            bool forgotten = !inStore.Destroyed && inStore.Position == cell ? HeirsFoodStorePatch.FactorFor(inStore) == 1f : true;
            P.Check("a torn-down store stops slowing rot", seen && forgotten, seen + " / " + forgotten);
            if (!potato.Destroyed) potato.Destroy();
            if (!inStore.Destroyed) inStore.Destroy();
        }

        /// <summary>4.2.1: the tab's bars reuse one texture per nation instead of making a new one every frame.</summary>
        public static void BarTextures()
        {
            NationDef roma = N("HE_Roma");
            P.Check("bar texture made once", MainTabWindow_Heirs.BarTex(roma) == MainTabWindow_Heirs.BarTex(roma) && MainTabWindow_Heirs.BarTex(roma) != null);
            string tip = MainTabWindow_Heirs.AgeTip(roma);
            P.Check("age tooltip", tip.Contains("Roma") || tip.Length > 40, tip.Length.ToString());
            P.Check("age items cached", HeirsAges.AgeItems(roma, 2).Any() && ReferenceEquals(HeirsAges.AgeItems(roma, 3), HeirsAges.AgeItems(roma, 3)));
        }

        /// <summary>4.2.1: ten years of the world in fast forward. Politics run every month and ages every day, with the clock moved
        /// forward by hand (nothing else on the map ticks). Reports when each nation reaches each age, the wars and the towns that change hands.</summary>
        public static void TenYears()
        {
            HeirsGame g = HeirsGame.Get;
            HeirsWorld world = HeirsWorld.Get;
            if (g == null || world == null) { P.Check("ten years: game", false); return; }
            var field = typeof(TickManager).GetField("ticksGameInt", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
            if (field == null) { P.Check("ten years: clock", false); return; }
            List<NationDef> nations = HeirsWorld.LiveNations.ToList();
            var towns0 = nations.ToDictionary(n => n, n => Find.WorldObjects.Settlements.Count(s => s.Faction == HeirsWorld.FactionOf(n)));
            var reached = new Dictionary<NationDef, float[]>();
            foreach (NationDef n in nations) reached[n] = new[] { 0f, 0f, -1f, -1f };
            int days = 10 * GenDate.DaysPerYear, interval = Mathf.Max(1, HeirsMod.Settings.politicsIntervalDays), warMonths = 0, maxWars = 0;
            var wars = new HashSet<string>();
            var watch = System.Diagnostics.Stopwatch.StartNew();
            for (int d = 1; d <= days; d++)
            {
                field.SetValue(Find.TickManager, Find.TickManager.TicksGame + GenDate.TicksPerDay);
                HeirsAges.DailyTick(g);
                if (d % interval == 0)
                {
                    world.MonthlyTick();
                    foreach (NationPair w in world.wars) wars.Add(w.a.defName + "-" + w.b.defName + "@" + w.startTick);
                    if (world.wars.Count > 0) warMonths++;
                    maxWars = Mathf.Max(maxWars, world.wars.Count);
                }
                foreach (NationDef n in nations)
                {
                    int age = HeirsAges.AgeOf(n);
                    for (int a = 2; a <= age; a++) if (reached[n][a] < 0f) reached[n][a] = d / (float)GenDate.DaysPerYear;
                }
                if (d % 20 == 0) while (Find.LetterStack.LettersListForReading.Count > 0) Find.LetterStack.RemoveLetter(Find.LetterStack.LettersListForReading[0]);
            }
            watch.Stop();
            while (Find.LetterStack.LettersListForReading.Count > 0) Find.LetterStack.RemoveLetter(Find.LetterStack.LettersListForReading[0]);
            foreach (NationDef n in nations)
            {
                int towns = Find.WorldObjects.Settlements.Count(s => s.Faction == HeirsWorld.FactionOf(n));
                P.Say("ten years " + n.defName + ": age II at year " + (reached[n][2] < 0 ? "-" : reached[n][2].ToString("0.0"))
                      + ", age III at year " + (reached[n][3] < 0 ? "-" : reached[n][3].ToString("0.0")) + ", towns " + towns0[n] + " -> " + towns
                      + ", progress " + g.AgeProgress(n).ToString("0.00") + ", pace now " + HeirsAges.Rate(n).ToStringPercent());
            }
            P.Say("ten years: " + wars.Count + " wars, " + warMonths + " of " + (days / interval) + " months with a war, at most " + maxWars + " at once, "
                  + watch.ElapsedMilliseconds + " ms");
            int two = nations.Count(n => reached[n][2] >= 0f), three = nations.Count(n => reached[n][3] >= 0f);
            P.Check("ten years: most nations reach the Age of Powder", two >= nations.Count - 2, two + "/" + nations.Count);
            P.Check("ten years: no nation rushes to steam", nations.All(n => reached[n][3] < 0f || reached[n][3] >= 4f), three + " reached steam");
            P.Check("ten years: the world keeps living", wars.Count >= 1 && nations.Count(n => HeirsWorld.FactionOf(n) != null) >= 1, wars.Count + " wars");
        }

        /// <summary>4.2.1: a nation can field a hundred living people at once without running out of names (RimWorld keeps each
        /// pawn's short name unique, and the old pools of 44-66 first names ran dry in long wars).</summary>
        public static void NamePools()
        {
            foreach (NationDef n in DefDatabase<NationDef>.AllDefsListForReading)
            {
                Faction faction = HeirsWorld.FactionOf(n);
                PawnKindDef kind = DefDatabase<PawnKindDef>.AllDefsListForReading.FirstOrDefault(k => HeirsKits.NationOfKind(k) == n && !k.factionLeader && k.RaceProps.Humanlike);
                if (faction == null || kind == null) continue;
                var pawns = new List<Pawn>();
                int before = PawnsFinder.AllMapsWorldAndTemporary_AliveOrDead.Count(x => x.Faction == faction);
                foreach (Gender gender in new[] { Gender.Female, Gender.Male })
                {
                    for (int i = 0; i < 50; i++)
                    {
                        Pawn p = PawnGenerator.GeneratePawn(new PawnGenerationRequest(kind, faction, PawnGenerationContext.NonPlayer, forceGenerateNewPawn: true, fixedGender: gender));
                        Find.WorldPawns.PassToWorld(p, RimWorld.Planet.PawnDiscardDecideMode.KeepForever);
                        pawns.Add(p);
                    }
                }
                int distinct = pawns.Select(p => p.Name?.ToStringShort).Distinct().Count();
                P.Check("name pool " + n.defName, distinct == pawns.Count, distinct + "/" + pawns.Count + " distinct short names, " + before + " of the nation's people already in the world");
                foreach (Pawn p in pawns)
                {
                    if (Find.WorldPawns.Contains(p)) Find.WorldPawns.RemoveAndDiscardPawnViaGC(p);
                }
            }
        }
    }
}
