"""Heirs of Earth 3.6 "Sound and Sight": the music and signature calls of the nine nations, weapon and artifact sounds.
The audio itself is synthesised by heirs_music.py and heirs_sounds36.py (run them with plain python, they need scipy)."""
from heirs_c_v33 import find
from heirs_data import add, key, tex
from heirs_xml import Def

FS = "Core/HE_Sounds36.xml"
NATIONS = ["Roma", "Yamato", "Nord", "Hellas", "Tianxia", "Albion", "Kemet", "Pars", "Inti"]


def camera_sound(name, clip, volume):
    add(FS, Def("SoundDef", name, maxSimultaneous=1,
                subSounds=[{"onCamera": True, "grains": [{"@Class": "AudioGrain_Clip", "clipPath": "HeirsOfEarth/" + clip}],
                            "volumeRange": f"{volume}~{volume}"}]))
    return name


def map_sound(name, clip, volume, pitch="0.94~1.06", most=2):
    """A sound in the world (weapons): heard where it happens, a little pitch variety so volleys do not sound copied."""
    add(FS, Def("SoundDef", name, context="MapOnly", maxSimultaneous=most,
                subSounds=[{"grains": [{"@Class": "AudioGrain_Clip", "clipPath": "HeirsOfEarth/" + clip}],
                            "volumeRange": f"{volume}~{volume}", "pitchRange": pitch, "sustainLoop": False}]))
    return name


# ------------------------------------------------------------------ music and calls
for n in NATIONS:
    add(FS, Def("SongDef", f"HE_Song_{n}", clipPath=f"HeirsOfEarth/Music/HE_Music_{n}", volume=0.85, playOnMap=False, commonality=0))
    camera_sound(f"HE_Sound_Sting_{n}", f"HE_Sting_{n}", 34)

# ------------------------------------------------------------------ weapons
SHOTS = {
    "HE_Shot_Musket": (["HE_Albion_Musket", "HE_Pars_Jezail"], 48),
    "HE_Shot_Matchlock": (["HE_Yamato_Tanegashima"], 48),
    "HE_Shot_Flintlock": (["HE_Albion_FlintlockPistol"], 44),
    "HE_Shot_Blunderbuss": (["HE_Albion_Blunderbuss"], 50),
    "HE_Shot_Cannon": (["HE_Albion_FieldCannon_Gun"], 55),
    "HE_Shot_Scorpio": (["HE_Roma_Scorpio_Gun", "HE_Hellas_Gastraphetes"], 42),
    "HE_Shot_Manuballista": (["HE_Roma_Manuballista"], 40),
    "HE_Shot_Trebuchet": (["HE_Trebuchet_Gun", "HE_Hellas_Lithobolos_Gun"], 50),
    "HE_Shot_Sling": (["HE_Inti_Sling", "HE_Inti_SlingStand_Gun"], 36),
    "HE_Shot_Repeater": (["HE_Tianxia_Repeater"], 38),
    "HE_Shot_FireLance": (["HE_Tianxia_FireLance"], 46),
    "HE_Shot_Naft": (["HE_Pars_NaftThrower_Gun"], 46),
    "HE_Shot_FireArrows": (["HE_Tianxia_FireArrowBattery_Gun"], 44),
    "HE_Shot_Harpoon": (["HE_Nord_HarpoonGun"], 42),
}


def verbs_of(d):
    verbs = d.fields.get("verbs")
    if not verbs:
        raise KeyError(f"{d.name} has no verbs")
    return verbs


for sound, (weapons, volume) in SHOTS.items():
    map_sound(sound, sound, volume, pitch="0.9~1.0" if "Cannon" in sound or "Trebuchet" in sound else "0.94~1.06")
    for w in weapons:
        for v in verbs_of(find("ThingDef", w)):
            v["soundCast"] = sound
            if v.get("soundCastTail") and ("Sling" in sound or "Scorpio" in sound or "Trebuchet" in sound or "Repeater" in sound or "Manuballista" in sound):
                v["soundCastTail"] = None

# ------------------------------------------------------------------ artifacts: the three that borrowed another nation's call
ARTIFACT_SOUNDS = {
    "HE_Kemet_Artifact_SunDisc": camera_sound("HE_Sound_Sistrum", "HE_Sistrum", 42),
    "HE_Pars_Artifact_KingsEye": camera_sound("HE_Sound_Karnay", "HE_Karnay", 42),
    "HE_Inti_Artifact_GoldenThread": camera_sound("HE_Sound_Pututu", "HE_Pututu", 42),
}
for artifact, sound in ARTIFACT_SOUNDS.items():
    comps = [c for c in find("ThingDef", artifact).fields["comps"] if isinstance(c, dict) and c.get("@Class") == "HeirsOfEarth.CompProperties_HeirsArtifact"]
    if len(comps) != 1:
        raise KeyError(f"{artifact}: artifact comp not found")
    comps[0]["sound"] = sound

key("HE_SettingsNationMusic", "Music and calls of the nations", "Devletlerin müzikleri ve çağrıları")
key("HE_SettingsNationMusicTip",
    "Every nation has its own music and a short call. The call sounds when its news arrives; its music plays when one of its stories ends or it honours you, "
    "and now and then among the usual songs (your heritage, and nations that honoured you). All of it was made for this mod.",
    "Her devletin kendi müziği ve kısa bir çağrısı var. Çağrı, devletin haberi geldiğinde çalar; müziği, hikâyelerinden biri bittiğinde ya da seni onurlandırdığında "
    "ve ara sıra olağan şarkıların arasında (mirasın ve seni onurlandıran devletler) çalar. Hepsi bu mod için yapıldı.")

# ------------------------------------------------------------------ worn headgear (drawn by heirs_art18)
HEADGEAR = ["HE_Albion_Shako", "HE_Albion_TopHat", "HE_Albion_Bicorne", "HE_Hellas_Corinthian", "HE_Hellas_OliveWreath", "HE_Inti_PlumedHelm",
            "HE_Inti_Mascaypacha", "HE_Kemet_Khepresh", "HE_Kemet_Nemes", "HE_Nord_Helm", "HE_Nord_Circlet", "HE_Pars_WingedHelm", "HE_Pars_Kidaris",
            "HE_Roma_Galea", "HE_Roma_Laurel", "HE_Tianxia_Helmet", "HE_Tianxia_Futou", "HE_Yamato_Kabuto", "HE_Yamato_Jingasa"]
UNSTUFFED_HATS = {"HE_Hellas_OliveWreath"}
# bands and wreaths sit on the hair like the vanilla coronet; real hats and helmets hide it as vanilla hats do
BANDS = {"HE_Roma_Laurel", "HE_Hellas_OliveWreath", "HE_Nord_Circlet", "HE_Inti_Mascaypacha"}
for hat in HEADGEAR:
    app = find("ThingDef", hat).fields["apparel"]
    app["wornGraphicPath"] = f"HeirsOfEarth/Apparel/Worn/{hat}"
    if hat in BANDS:
        app["renderSkipFlags"] = ["None"]
    masked = hat not in UNSTUFFED_HATS
    if masked:
        app["useWornGraphicMask"] = True
    for rot in ("south", "east", "north"):
        tex(f"HeirsOfEarth/Apparel/Worn/{hat}_{rot}", "heirs_worn", kind=hat, rot=rot)
        if masked:
            tex(f"HeirsOfEarth/Apparel/Worn/{hat}_{rot}m", "heirs_worn", kind=hat, rot=rot, mask=True)
