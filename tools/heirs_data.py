"""Heirs of Earth: single source of truth for generated content.

Content modules call add()/key()/tex() at import time; heirs_build.py and heirs_art.py read the registry.
"""
from collections import OrderedDict

from heirs_xml import T

MOD = {
    "packageId": "kerem.heirs",
    "name": "Heirs of Earth",
    "author": "Kerem",
    "version": "4.3.2",
    "harmony": "brrainz.harmony",
    "harmonyUrl": "https://steamcommunity.com/sharedfiles/filedetails/?id=2009463077",
}

FILES = OrderedDict()   # "Research/HE_Research_Roma.xml" -> [Def]
KEYED = OrderedDict()   # key -> T
TEXTURES = OrderedDict()  # texture path (no extension, under Textures/) -> (painter, args)


def add(file, *defs):
    FILES.setdefault(file, []).extend(defs)


def key(k, en, tr):
    if k in KEYED:
        raise ValueError("duplicate key " + k)
    KEYED[k] = T(en, tr)


def tex(path, painter, **args):
    TEXTURES[path] = (painter, args)


def load_all():
    """Imports every content module once, in a fixed order."""
    if FILES:
        return
    import heirs_c_core
    import heirs_c_world  # noqa: F401
    import heirs_c_roma  # noqa: F401
    import heirs_c_roma2  # noqa: F401
    import heirs_c_roma_people  # noqa: F401
    import heirs_c_yamato  # noqa: F401
    import heirs_c_yamato_people  # noqa: F401
    import heirs_c_nord  # noqa: F401
    import heirs_c_nord_people  # noqa: F401
    import heirs_c_hellas  # noqa: F401
    import heirs_c_hellas_people  # noqa: F401
    import heirs_c_tianxia  # noqa: F401
    import heirs_c_tianxia_people  # noqa: F401
    import heirs_c_albion  # noqa: F401
    import heirs_c_albion_people  # noqa: F401
    import heirs_c_kemet  # noqa: F401
    import heirs_c_kemet_people  # noqa: F401
    import heirs_c_pars  # noqa: F401
    import heirs_c_pars_people  # noqa: F401
    import heirs_c_inti  # noqa: F401
    import heirs_c_inti_people  # noqa: F401
    import heirs_c_common  # noqa: F401
    import heirs_c_chains  # noqa: F401
    import heirs_c_chains2  # noqa: F401
    import heirs_c_v21  # noqa: F401
    import heirs_c_chains3  # noqa: F401
    import heirs_c_v30  # noqa: F401
    import heirs_c_v31  # noqa: F401
    import heirs_c_v32  # noqa: F401
    import heirs_c_v32b  # noqa: F401
    import heirs_c_v32c  # noqa: F401
    import heirs_c_v32d  # noqa: F401
    import heirs_c_v33  # noqa: F401
    import heirs_c_v34  # noqa: F401
    import heirs_c_v35  # noqa: F401
    import heirs_c_v36  # noqa: F401
    import heirs_c_v37  # noqa: F401
    import heirs_c_v40  # noqa: F401
    import heirs_c_v41  # noqa: F401
    import heirs_c_v42  # noqa: F401
    import heirs_c_v43  # noqa: F401
    heirs_c_core.finalize()
