"""Heirs of Earth 4.1: every heir tunic, coat, robe, cloak and armour has its own worn look for the five body types (heirs_art19).
The stuff tints the cloth or metal through a mask; trims, gold, lacing and dyes keep their colours. The feather cape and leopard
mantle no longer borrow the Royalty cape graphic, which a game without Royalty cannot show."""
from heirs_c_v33 import find
from heirs_art19 import GARMENTS, BODIES, ROTS
from heirs_data import tex
from heirs_art20 import COATS  # the 4.2 uniform coats share the garment table; heirs_c_v42 sets those up
from heirs_art21 import FIELD_UNIFORMS  # and so do the 4.3 field uniforms (heirs_c_v43)

for garment in [g for g in GARMENTS if g not in COATS and g not in FIELD_UNIFORMS]:
    app = find("ThingDef", garment).fields["apparel"]
    path = f"HeirsOfEarth/Apparel/Worn/Body/{garment}"
    app["wornGraphicPath"] = path
    app["useWornGraphicMask"] = True
    for body in BODIES:
        for rot in ROTS:
            tex(f"{path}_{body}_{rot}", "heirs_body", kind=garment, body=body, rot=rot)
            tex(f"{path}_{body}_{rot}m", "heirs_body", kind=garment, body=body, rot=rot, mask=True)
