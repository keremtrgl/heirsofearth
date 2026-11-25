using System.Linq;
using RimWorld;
using UnityEngine;
using Verse;
using Verse.Sound;

namespace HeirsOfEarth
{
    /// <summary>A reusable artifact: rallies the user's side, may scare hostile people away and may call a weather change.</summary>
    public class CompProperties_HeirsArtifact : CompProperties_UseEffect
    {
        public HediffDef allyHediff;
        public float allyRadius = 30f;
        public float fleeChance;
        public WeatherDef weather;
        public float cooldownDays = 10f;
        public SoundDef sound;
        /// <summary>Goodwill added with every heir nation that is not hostile to the user.</summary>
        public int goodwill;
        /// <summary>When true, a friendly heir nation sends a trade caravan to the map.</summary>
        public bool callCaravan;

        public CompProperties_HeirsArtifact()
        {
            compClass = typeof(CompUseEffect_HeirsArtifact);
        }
    }

    public class CompUseEffect_HeirsArtifact : CompUseEffect
    {
        private int lastUseTick = -9999999;

        public CompProperties_HeirsArtifact Props => (CompProperties_HeirsArtifact)props;

        public int CooldownTicksLeft => Mathf.Max(0, lastUseTick + Mathf.RoundToInt(Props.cooldownDays * GenDate.TicksPerDay) - Find.TickManager.TicksGame);

        public override AcceptanceReport CanBeUsedBy(Pawn p)
        {
            int left = CooldownTicksLeft;
            if (left > 0)
            {
                return "HE_ArtifactCooldown".Translate(left.ToStringTicksToPeriod());
            }
            return base.CanBeUsedBy(p);
        }

        public override void DoEffect(Pawn usedBy)
        {
            base.DoEffect(usedBy);
            Map map = usedBy.MapHeld;
            lastUseTick = Find.TickManager.TicksGame;
            if (map == null)
            {
                return;
            }
            int rallied = 0, fled = 0;
            foreach (Pawn pawn in map.mapPawns.AllPawnsSpawned.ToList())
            {
                if (pawn.Dead || pawn.Downed || !pawn.RaceProps.Humanlike)
                {
                    continue;
                }
                if (Props.allyHediff != null && pawn.Faction == usedBy.Faction && pawn.Position.InHorDistOf(usedBy.PositionHeld, Props.allyRadius))
                {
                    Hediff existing = pawn.health.hediffSet.GetFirstHediffOfDef(Props.allyHediff);
                    if (existing != null)
                    {
                        pawn.health.RemoveHediff(existing);
                    }
                    pawn.health.AddHediff(Props.allyHediff);
                    rallied++;
                }
                else if (Props.fleeChance > 0f && pawn.HostileTo(usedBy) && !pawn.InMentalState && Rand.Chance(Props.fleeChance))
                {
                    if (pawn.mindState.mentalStateHandler.TryStartMentalState(MentalStateDefOf.PanicFlee, null, true))
                    {
                        fled++;
                    }
                }
            }
            if (Props.weather != null)
            {
                map.weatherManager.TransitionTo(Props.weather);
            }
            Props.sound?.PlayOneShot(new TargetInfo(usedBy.PositionHeld, map));
            if (Props.goodwill != 0 && usedBy.Faction != null)
            {
                foreach (NationDef nation in HeirsWorld.LiveNations.ToList())
                {
                    Faction f = HeirsWorld.FactionOf(nation);
                    if (f != null && f.HasGoodwill && !f.HostileTo(usedBy.Faction))
                    {
                        f.TryAffectGoodwillWith(usedBy.Faction, Props.goodwill, true, true, null);
                    }
                }
            }
            if (Props.callCaravan)
            {
                CallCaravan(map, usedBy.Faction);
            }
            Messages.Message("HE_ArtifactUsed".Translate(usedBy.LabelShort, parent.LabelShort, rallied, fled), usedBy, MessageTypeDefOf.PositiveEvent);
        }

        private static void CallCaravan(Map map, Faction user)
        {
            if (user == null)
            {
                return;
            }
            Faction trader = HeirsWorld.LiveNations.Select(HeirsWorld.FactionOf)
                .Where(f => f != null && !f.HostileTo(user) && !f.defeated && f.def.caravanTraderKinds.Any())
                .RandomElementWithFallback();
            if (trader == null)
            {
                return;
            }
            IncidentParms parms = StorytellerUtility.DefaultParmsNow(IncidentCategoryDefOf.Misc, map);
            parms.faction = trader;
            parms.forced = true;
            IncidentDefOf.TraderCaravanArrival.Worker.TryExecute(parms);
        }

        public override string CompInspectStringExtra()
        {
            int left = CooldownTicksLeft;
            return left > 0 ? "HE_ArtifactCooldown".Translate(left.ToStringTicksToPeriod()).Resolve() : "HE_ArtifactReady".Translate().Resolve();
        }

        public override void PostExposeData()
        {
            base.PostExposeData();
            Scribe_Values.Look(ref lastUseTick, "heirsLastUse", -9999999);
        }
    }
}
