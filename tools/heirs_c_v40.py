"""Heirs of Earth 4.0: the DLC extras that can be proven without the DLCs.
Royalty: noble titles ask for headgear carrying an apparel tag (ApparelRequirement.requiredTags): RoyalTier5 for Baron and Count
(the coronet), RoyalTier6 for Consul (the crown). Tags are plain strings, so without Royalty they do nothing."""
from heirs_c_v33 import find

NOBLE_HEADGEAR = {
    "HE_Kemet_Khepresh": ["RoyalTier5", "RoyalTier6"],
    "HE_Pars_Kidaris": ["RoyalTier5", "RoyalTier6"],
    "HE_Inti_Mascaypacha": ["RoyalTier5", "RoyalTier6"],
    "HE_Roma_Laurel": ["RoyalTier5"],
    "HE_Kemet_Nemes": ["RoyalTier5"],
    "HE_Nord_Circlet": ["RoyalTier5"],
}
for hat, tags in NOBLE_HEADGEAR.items():
    app = find("ThingDef", hat).fields["apparel"]
    app["tags"] = list(app["tags"]) + [t for t in tags if t not in app["tags"]]
