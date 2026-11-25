using System.Collections.Generic;
using RimWorld;
using UnityEngine;
using Verse;

namespace HeirsOfEarth
{
    /// <summary>One heir nation: its faction, player faction, start, colors and natural friends and rivals.</summary>
    public class NationDef : Def
    {
        public Color color = Color.white;
        public FactionDef faction;
        public FactionDef playerFaction;
        public ScenarioDef scenario;
        public ThingDef archive;
        public string rulerTitle;
        public string adjective;
        public int release = 1;
        public List<NationDef> friends = new List<NationDef>();
        public List<NationDef> rivals = new List<NationDef>();
        public string iconPath;
        public RaidDoctrine doctrine;
        public List<Temperament> temperamentBias = new List<Temperament>();
        public string honoraryTitle;
        public PawnKindDef animal;

        [Unsaved] private Texture2D icon;

        public Texture2D Icon
        {
            get
            {
                if (icon == null)
                {
                    icon = iconPath.NullOrEmpty() ? BaseContent.BadTex : ContentFinder<Texture2D>.Get(iconPath, false) ?? BaseContent.BadTex;
                }
                return icon;
            }
        }

        public bool IsFriendOf(NationDef other)
        {
            return friends.Contains(other) || other.friends.Contains(this);
        }

        public bool IsRivalOf(NationDef other)
        {
            return rivals.Contains(other) || other.rivals.Contains(this);
        }
    }

    public enum EffectScope
    {
        Colonists,
        PlayerBuildings
    }

    public class StatEffect
    {
        public StatDef stat;
        public float offset;
        public float factor = 1f;
        public EffectScope scope;
    }

    /// <summary>Marks a research project as part of a nation's branch; traditions also carry rule changes.</summary>
    public class HeirsResearchExt : DefModExtension
    {
        public NationDef nation;
        public float knowledge;
        public bool tradition;
        public List<StatEffect> stats = new List<StatEffect>();
        public float qualityChance;
        public float caravanSpeed;
        public float studyFactor;
        public ChainDef requiresChain;
        public bool council;
        public int age;
    }

    /// <summary>On things and backstories: which culture they carry and how much knowledge studying them gives.</summary>
    public class HeirsCultureExt : DefModExtension
    {
        public NationDef nation;
        public float knowledge;
    }

    [DefOf]
    public static class HeirsDefOf
    {
        public static ResearchTabDef HE_WorldHeritage;
        public static NationDef HE_Roma;

        static HeirsDefOf()
        {
            DefOfHelper.EnsureInitializedInCtor(typeof(HeirsDefOf));
        }
    }
}
