using System.Collections.Generic;
using System.Linq;
using RimWorld;
using RimWorld.Planet;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>On a weapon, garment or building that belongs to a nation's later age (4.2): which nation, which age (2 Powder, 3 Steam, 4 Electric).</summary>
    public class HeirsAgeExt : DefModExtension
    {
        public NationDef nation;
        public int age = 2;
    }

    /// <summary>
    /// 4.2 "Ages of Progress": every nation moves from its founding age (I) to the age of powder (II) and the age of steam (III).
    /// Progress is counted in "years at the normal pace"; a scholarly court, allies, wealth and links with the player speed it up,
    /// war slows it, famine and plague set it back. Later ages arm the nation's troops with its own firearms and uniforms, open its
    /// age items to its traders and let the player learn them.
    /// </summary>
    public static class HeirsAges
    {
        public const float AgeTwoAt = 3f;   // 4.2.1: from 2.5 and 7, after the ten-year test showed most nations run at about 130%
        public const float AgeThreeAt = 9f;
        public const float AgeFourAt = 18f;  // 4.3: the Electric Age, a late-game step (about 14 years at the usual pace)
        public const int LastAge = 4;
        public const float MinRate = 0.2f;
        public const float SetbackRefused = 0.3f;
        public const float SetbackHelped = 0.1f;

        public static bool On => HeirsMod.Settings.ages;

        public static float Progress(NationDef nation) => HeirsGame.Get?.AgeProgress(nation) ?? 0f;

        public static int AgeFor(float progress) => progress >= AgeFourAt ? 4 : progress >= AgeThreeAt ? 3 : progress >= AgeTwoAt ? 2 : 1;

        /// <summary>Progress at which an age starts (0 for the first).</summary>
        public static float StartOf(int age) => age >= 4 ? AgeFourAt : age == 3 ? AgeThreeAt : age == 2 ? AgeTwoAt : 0f;

        /// <summary>The nation's age: 1 founding, 2 powder, 3 steam. With ages switched off every nation stays in its founding age.</summary>
        public static int AgeOf(NationDef nation) => nation == null || !On ? 1 : AgeFor(Progress(nation));

        public static string AgeLabel(int age) => ("HE_Age" + age).Translate().Resolve();

        /// <summary>Share of the way to the next age (1 at the last age).</summary>
        public static float ToNext(NationDef nation)
        {
            float p = Progress(nation);
            int age = AgeFor(p);
            if (age >= LastAge) return 1f;
            float from = StartOf(age);
            float to = StartOf(age + 1);
            return Mathf.Clamp01((p - from) / (to - from));
        }

        /// <summary>Yearly pace and what makes it, for the tooltip.</summary>
        public static float Rate(NationDef nation, List<string> parts = null)
        {
            Faction faction = HeirsWorld.FactionOf(nation);
            if (faction == null)
            {
                return 0f;
            }
            float rate = 1f;
            void Part(string key, float value)
            {
                if (value == 0f) return;
                rate += value;
                parts?.Add(key.Translate().Resolve() + ": " + (value > 0f ? "+" : "") + value.ToStringPercent());
            }
            parts?.Add("HE_AgeRateBase".Translate().Resolve() + ": 100%");
            if (HeirsCourt.Is(nation, Temperament.Scholarly)) Part("HE_AgeRateScholarly", 0.5f);
            HeirsWorld world = HeirsWorld.Get;
            if (world != null)
            {
                Part("HE_AgeRateAllies", 0.15f * world.alliances.Count(p => p.a == nation || p.b == nation));
                if (world.wars.Any(p => p.a == nation || p.b == nation)) Part("HE_AgeRateWar", -0.4f);
            }
            if (HeirsTreaties.Has(nation, TreatyKind.Science)) Part("HE_AgeRateScience", 0.25f);
            if (HeirsEvents.Linked(nation)) Part("HE_AgeRateTrade", 0.1f);
            int towns = Find.WorldObjects.Settlements.Count(s => s.Faction == faction);
            Part("HE_AgeRateTowns", Mathf.Min(0.3f, 0.05f * Mathf.Max(0, towns - 3)));
            return Mathf.Max(MinRate, rate);
        }

        public static void DailyTick(HeirsGame game)
        {
            if (!On)
            {
                return;
            }
            foreach (NationDef nation in HeirsWorld.LiveNations.ToList())
            {
                if (!game.HasAgeProgress(nation))
                {
                    // nations do not all start level: a small head start, so their ages do not turn on the same day
                    game.SetAgeProgress(nation, Rand.Range(0f, 0.8f));
                    game.SetAgeShown(nation, 1);
                }
                // a save from 4.2.0 (lower thresholds) keeps the age it already announced
                int shown = game.AgeShown(nation);
                if (shown >= 2 && AgeFor(game.AgeProgress(nation)) < shown)
                {
                    game.SetAgeProgress(nation, StartOf(shown));
                }
                float before = game.AgeProgress(nation);
                game.SetAgeProgress(nation, before + Rate(nation) * HeirsMod.Settings.ageSpeed / GenDate.DaysPerYear);
                Announce(game, nation);
            }
        }

        /// <summary>Famine or plague: the nation loses some ground (less if the player helped). Never drops it out of an age it reached.</summary>
        public static void Setback(NationDef nation, bool helped)
        {
            HeirsGame game = HeirsGame.Get;
            if (game == null || nation == null || !On)
            {
                return;
            }
            float p = game.AgeProgress(nation);
            float floor = StartOf(AgeFor(p));
            game.SetAgeProgress(nation, Mathf.Max(floor, p - (helped ? SetbackHelped : SetbackRefused)));
        }

        /// <summary>A letter and a chronicle entry the first time a nation is seen in a new age.</summary>
        public static void Announce(HeirsGame game, NationDef nation)
        {
            int age = AgeFor(game.AgeProgress(nation));
            int shown = game.AgeShown(nation);
            if (age <= shown)
            {
                return;
            }
            game.SetAgeShown(nation, age);
            if (shown == 0 && age == 1)
            {
                return;
            }
            string items = string.Join(", ", AgeItems(nation, age).Select(d => d.LabelCap.Resolve()));
            string text = ("HE_AgeText" + age).Translate(nation.LabelCap, HeirsCourt.RulerLine(nation), items);
            game.AddChronicle(("HE_AgeChronicle").Translate(nation.LabelCap, AgeLabel(age)), nation);
            HeirsMusic.Sting(nation);
            Find.LetterStack.ReceiveLetter("HE_AgeLabel".Translate(nation.LabelCap, AgeLabel(age)), text, LetterDefOf.NeutralEvent);
            OnAgeReached?.Invoke(nation, age);
        }

        /// <summary>4.3: raised once when a nation is first seen in a new age (after its letter); the World Fair listens.</summary>
        public static event System.Action<NationDef, int> OnAgeReached;

        private static Dictionary<NationDef, List<ThingDef>[]> ageItems;

        /// <summary>The items a nation's age brings (cached: defs never change during a game, and the tab asks every frame).</summary>
        public static IEnumerable<ThingDef> AgeItems(NationDef nation, int age)
        {
            if (ageItems == null)
            {
                ageItems = new Dictionary<NationDef, List<ThingDef>[]>();
                foreach (ThingDef d in DefDatabase<ThingDef>.AllDefsListForReading)
                {
                    if (d.GetModExtension<HeirsAgeExt>() is HeirsAgeExt e && e.nation != null && e.age >= 1 && e.age <= LastAge)
                    {
                        if (!ageItems.TryGetValue(e.nation, out List<ThingDef>[] lists))
                        {
                            lists = Enumerable.Range(0, LastAge + 1).Select(_ => new List<ThingDef>()).ToArray();
                            ageItems[e.nation] = lists;
                        }
                        lists[e.age].Add(d);
                    }
                }
            }
            return nation != null && age >= 0 && age <= LastAge && ageItems.TryGetValue(nation, out List<ThingDef>[] l) ? l[age] : Enumerable.Empty<ThingDef>();
        }

        public static string Tag(NationDef nation, int age) => "HE_" + nation.defName.Substring(3) + "Age" + age;

        /// <summary>Whether a thing is held back because its nation has not reached its age yet.</summary>
        public static bool Locked(ThingDef def)
        {
            HeirsAgeExt ext = def?.GetModExtension<HeirsAgeExt>();
            return ext != null && ext.nation != null && On && AgeOf(ext.nation) < ext.age;
        }

        // ------------------------------------------------------------------ troops: guns

        private static readonly Dictionary<string, float> tagPrice = new Dictionary<string, float>();
        private static bool regenerating;

        public class WeaponState
        {
            public PawnKindDef kind;
            public List<string> tags;
            public FloatRange money;
        }

        private static float PriceOf(string tag)
        {
            if (!tagPrice.TryGetValue(tag, out float price))
            {
                price = DefDatabase<ThingDef>.AllDefsListForReading.Where(d => d.weaponTags != null && d.weaponTags.Contains(tag))
                    .Select(d => d.GetStatValueAbstract(StatDefOf.MarketValue, d.MadeFromStuff ? GenStuff.DefaultStuffFor(d) : null)).DefaultIfEmpty(-1f).Max();
                tagPrice[tag] = price;
            }
            return price;
        }

        /// <summary>The age tag a troop of this kind carries this time, or null to keep the usual weapon.</summary>
        public static string RollGun(Pawn pawn)
        {
            PawnKindDef kind = pawn?.kindDef;
            NationDef nation = HeirsKits.NationOfKind(kind);
            if (nation == null || kind.factionLeader || kind.weaponTags == null || pawn.WorkTagIsDisabled(WorkTags.Shooting))
            {
                return null;
            }
            int age = AgeOf(nation);
            if (age < 2)
            {
                return null;
            }
            string n = nation.defName.Substring(3);
            bool ranged = kind.weaponTags.Contains("HE_" + n + "Ranged");
            bool melee = kind.weaponTags.Contains("HE_" + n + "Melee");
            if (!ranged && !melee)
            {
                return null;
            }
            float roll = Rand.Value;
            int pick = 0;
            if (age == 2)
            {
                pick = roll < (ranged ? 0.5f : 0.1f) ? 2 : 0;
            }
            else if (age == 3)
            {
                float three = ranged ? 0.45f : 0.2f, two = ranged ? 0.3f : 0.1f;
                pick = roll < three ? 3 : roll < three + two ? 2 : 0;
            }
            else
            {
                // 4.3: in the Electric Age the new guns lead, the older ones stay in the ranks
                float four = ranged ? 0.4f : 0.15f, three = ranged ? 0.3f : 0.15f, two = ranged ? 0.1f : 0.05f;
                pick = roll < four ? 4 : roll < four + three ? 3 : roll < four + three + two ? 2 : 0;
            }
            if (pick > 0 && PriceOf(Tag(nation, pick)) <= 0f && pick > 2 && PriceOf(Tag(nation, pick - 1)) > 0f)
            {
                pick--;
            }
            if (pick == 0)
            {
                return null;
            }
            string tag = Tag(nation, pick);
            return PriceOf(tag) > 0f ? tag : null;
        }

        public static void WeaponPrefix(Pawn pawn, out WeaponState __state)
        {
            __state = null;
            if (regenerating || !On)
            {
                return;
            }
            string tag = RollGun(pawn);
            if (tag == null)
            {
                return;
            }
            PawnKindDef kind = pawn.kindDef;
            __state = new WeaponState { kind = kind, tags = kind.weaponTags, money = kind.weaponMoney };
            float price = PriceOf(tag) + 1f;
            kind.weaponTags = new List<string> { tag };
            kind.weaponMoney = new FloatRange(price, price);
        }

        public static System.Exception WeaponFinalizer(System.Exception __exception, Pawn pawn, PawnGenerationRequest request, WeaponState __state)
        {
            if (__state == null)
            {
                return __exception;
            }
            __state.kind.weaponTags = __state.tags;
            __state.kind.weaponMoney = __state.money;
            if (__exception == null && pawn?.equipment != null && pawn.equipment.Primary == null)
            {
                // the gun could not be given (a quirk of the pawn): fall back to the usual weapon
                regenerating = true;
                try
                {
                    PawnWeaponGenerator.TryGenerateWeaponFor(pawn, request);
                }
                finally
                {
                    regenerating = false;
                }
            }
            return __exception;
        }

        // ------------------------------------------------------------------ troops: uniforms

        public const float UniformChance = 0.55f;

        /// <summary>The uniform troops wear: the Electric Age field uniform once the nation is there, else the steam coat.</summary>
        public static ThingDef UniformOf(NationDef nation) => UniformOf(nation, Mathf.Max(3, AgeOf(nation)));

        public static ThingDef UniformOf(NationDef nation, int age)
        {
            for (int a = Mathf.Min(age, LastAge); a >= 3; a--)
            {
                ThingDef d = AgeItems(nation, a).FirstOrDefault(x => x.IsApparel && x.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.Torso));
                if (d != null) return d;
            }
            return null;
        }

        /// <summary>4.3: the nation's Electric Age steel helmet.</summary>
        public static ThingDef HelmetOf(NationDef nation) =>
            AgeItems(nation, 4).FirstOrDefault(d => d.IsApparel && (d.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.FullHead)
                                                                    || d.apparel.bodyPartGroups.Contains(BodyPartGroupDefOf.UpperHead)));

        public const float HelmetChance = 0.55f;

        /// <summary>
        /// For an armed troop of a nation in the age of steam or later, now and then: its required clothes with the uniform in place of
        /// what it covers; in the Electric Age, independently, the steel helmet too. Null keeps the usual wardrobe.
        /// </summary>
        public static List<ThingDef> UniformKit(Pawn pawn)
        {
            PawnKindDef kind = pawn?.kindDef;
            NationDef nation = HeirsKits.NationOfKind(kind);
            if (!On || nation == null || kind.factionLeader || kind.weaponTags.NullOrEmpty())
            {
                return null;
            }
            int age = AgeOf(nation);
            if (age < 3)
            {
                return null;
            }
            string n = nation.defName.Substring(3);
            if (!kind.weaponTags.Any(t => t == "HE_" + n + "Ranged" || t == "HE_" + n + "Melee"))
            {
                return null;
            }
            var wear = new List<ThingDef>();
            ThingDef coat = Rand.Chance(UniformChance) ? UniformOf(nation, age) : null;
            if (coat != null) wear.Add(coat);
            ThingDef helmet = age >= 4 && Rand.Chance(HelmetChance) ? HelmetOf(nation) : null;
            if (helmet != null) wear.Add(helmet);
            if (wear.Count == 0)
            {
                return null;
            }
            BodyDef body = kind.RaceProps?.body ?? BodyDefOf.Human;
            List<ThingDef> required = (kind.apparelRequired ?? new List<ThingDef>())
                .Where(r => wear.All(w => ApparelUtility.CanWearTogether(r, w, body))).ToList();
            required.AddRange(wear);
            return required;
        }

        // ------------------------------------------------------------------ traders and research

        public static void StockPostfix(ThingDef thingDef, ref bool __result)
        {
            if (__result && Locked(thingDef))
            {
                __result = false;
            }
        }

        public class Patch : HeirsPatch
        {
            public override string Id => "Ages";

            public override void Apply(HarmonyLib.Harmony harmony)
            {
                System.Type k = typeof(HeirsAges);
                harmony.Patch(HeirsPatches.Need(typeof(PawnWeaponGenerator), nameof(PawnWeaponGenerator.TryGenerateWeaponFor)),
                    prefix: new HarmonyLib.HarmonyMethod(k, nameof(WeaponPrefix)), finalizer: new HarmonyLib.HarmonyMethod(k, nameof(WeaponFinalizer)));
                harmony.Patch(HeirsPatches.Need(typeof(StockGenerator_Tag), nameof(StockGenerator_Tag.HandlesThingDef)),
                    postfix: new HarmonyLib.HarmonyMethod(k, nameof(StockPostfix)));
            }
        }
    }
}
