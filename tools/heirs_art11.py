"""Heirs of Earth 3.2 "Equal Heritage": the new dishes (two per nation)."""
import math

from heirs_art import m, painter
from heirs_art2 import AMBER, CERAMIC, CERAMIC_B, RICE, TERRACOTTA
from kut_render import BRONZE, GOLD, WOOD, Canvas

CRUST = m("#c08a48", .14, 2, tint="#8a5a2a")
CRUST_D = m("#8a5a2c", .14, 2)
HONEY = m("#e0a640", .06, 2, spec=1.0, tint="#a06a14")
CHEESE = m("#efe2b8", .06, 2)
MEAT = m("#8a3e2a", .16, 2, tint="#5a2416")
MEAT_L = m("#b0603e", .14, 2)
GREENS = m("#5e7a32", .14, 2)
BEANS = m("#8a6232", .16, 2)
BROTH = m("#a8743a", .08, 2, spec=.6)
MISO = m("#b88a4a", .06, 2, spec=.5)
TOFU = m("#f2ecdc", .04, 2)
FISH = m("#c9b9a0", .10, 2, (4, 1))
FISH_SKIN = m("#7d6a52", .14, 2, (4, 1))
CORN = m("#e8c44a", .12, 1.5)
HUSK = m("#c8b06a", .12, 2, (1, 6))
POTATO = m("#c8b08a", .12, 2)
SAFFRON = m("#e8a422", .06, 2, spec=.5)
PISTACHIO = m("#8aa04a", .1, 2)
DATE = m("#5a2a16", .1, 2, spec=.7)
RED_SAUCE = m("#9a2a1a", .1, 2, spec=.5)
SCONE = m("#d8a868", .14, 2)
CREAM = m("#f4efe2", .04, 2)
JAM = m("#9a1a2a", .06, 2, spec=.8)
LEAF = m("#4e6a2a", .12, 2, (5, 1))
SKEWER = m("#d8c49a", .06, 2, (8, 1))
CHILI = m("#b8321e", .1, 2)
MOON = m("#c88a3e", .1, 2, spec=.4)
PORCELAIN = m("#eef0ec", .03, 2, spec=.8)
LACQUER = m("#2a1412", .06, 2, spec=.9)


def plate(c, mat=CERAMIC, cx=64, cy=78, rx=50, ry=26):
    c.ell(mat, cx, cy + 4, rx, ry, bevel=2.0)
    c.ell(m("#ffffff", .02, 2) if mat is CERAMIC else mat, cx, cy, rx - 8, ry - 6, bevel=.8, edge=.2)


def bowl(c, mat, fill, cx=64, cy=70, r=40):
    c.ell(mat, cx, cy + 6, r + 6, r * .62, bevel=2.2)
    c.poly(mat, (cx - r - 6, cy + 6), (cx + r + 6, cy + 6), (cx + r * .7, cy + r * .9), (cx - r * .7, cy + r * .9), bevel=2.0)
    c.ell(fill, cx, cy + 2, r, r * .5, bevel=1.4)


def skewer(c, x0, y0, x1, y1, pieces, mats):
    c.line(SKEWER, 2.2, (x0, y0), (x1, y1))
    for i in range(pieces):
        t = (i + .8) / (pieces + .6)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        c.ell(mats[i % len(mats)], x, y, 8, 7, bevel=1.6)


@painter
def dish(kind):
    c = Canvas(128, seed=900 + sum(map(ord, kind)))
    if kind == "lucanica":  # Roma: smoked sausage coil with bread
        plate(c, TERRACOTTA)
        pts = [(64 + (8 + a * 4.2) * math.cos(a), 76 + (8 + a * 4.2) * math.sin(a) * .55) for a in [i * .3 for i in range(26)]]
        for i in range(len(pts) - 1):
            c.line(MEAT, 9, pts[i], pts[i + 1])
        c.ell(CRUST, 30, 70, 14, 9, bevel=1.6)
    elif kind == "libum":  # Roma: honey cheesecake on bay leaves
        for a in (-30, 20, 160, 210):
            r = math.radians(a)
            c.ell(LEAF, 64 + 40 * math.cos(r), 82 + 16 * math.sin(r), 16, 6, bevel=.8)
        c.ell(CRUST_D, 64, 82, 38, 18, bevel=1.6)
        c.rect(CHEESE, 26, 64, 102, 82, 0, bevel=1.0)
        c.ell(CRUST, 64, 64, 38, 16, bevel=1.6)
        c.ell(HONEY, 64, 62, 26, 9, bevel=1.2)
    elif kind == "miso":  # Yamato: lacquer bowl of miso soup
        bowl(c, LACQUER, MISO)
        for dx, dy in ((-12, -2), (6, 4), (16, -4)):
            c.rect(TOFU, 64 + dx - 5, 72 + dy - 4, 64 + dx + 5, 72 + dy + 4, 1, bevel=.8)
        for dx in (-20, -2, 22):
            c.ell(GREENS, 64 + dx, 68, 4, 2, bevel=.6)
    elif kind == "mochi":  # Yamato: three rice cakes on a skewer and a plate
        plate(c, CERAMIC_B, ry=22)
        for i, col in enumerate(("#f2c8cc", "#f4efe2", "#a8c48a")):
            c.ell(m(col, .04, 2), 40 + i * 24, 72 - i * 4, 13, 12, bevel=2.0)
        c.line(SKEWER, 2.4, (22, 82), (104, 58))
    elif kind == "hunter_stew":  # Nord: iron pot of venison stew
        c.ell(m("#3a3c40", .08, 2), 64, 80, 48, 28, bevel=2.2)
        c.ell(BROTH, 64, 72, 40, 20, bevel=1.4)
        for dx, dy, mat in ((-16, -2, MEAT), (10, 4, POTATO), (0, -8, MEAT_L), (20, -6, MEAT), (-6, 8, POTATO)):
            c.ell(mat, 64 + dx, 72 + dy, 7, 5, bevel=1.2)
        for s in (-1, 1):
            c.line(m("#3a3c40", .08, 2), 3, (64 + s * 44, 66), (64 + s * 50, 52))
    elif kind == "flatbread":  # Nord: honey flatbread
        c.ell(CRUST_D, 64, 78, 50, 30, bevel=2.0)
        c.ell(CRUST, 64, 74, 46, 26, bevel=1.6)
        for i in range(14):
            a = i * 2.4
            c.ell(CRUST_D, 64 + 30 * math.cos(a) * (i % 3 + 1) / 3, 74 + 16 * math.sin(a) * (i % 3 + 1) / 3, 2.4, 1.8, bevel=.4)
        c.poly(HONEY, (40, 66), (70, 60), (88, 70), (66, 80), (44, 76), bevel=1.0)
    elif kind == "skewers":  # Hellas: grilled lamb skewers with olives
        plate(c)
        skewer(c, 22, 92, 104, 58, 5, (MEAT, MEAT_L, GREENS))
        skewer(c, 22, 76, 104, 44, 5, (MEAT_L, MEAT, CHILI))
        for dx, dy in ((-30, 4), (30, 14), (36, 4)):
            c.ell(m("#2a2a1a", .1, 2, spec=.8), 64 + dx, 82 + dy, 4, 3, bevel=.8)
    elif kind == "plakous":  # Hellas: layered honey cake
        plate(c, TERRACOTTA, ry=22)
        for i in range(4):
            c.rect(CRUST if i % 2 == 0 else CHEESE, 32, 48 + i * 7, 96, 56 + i * 7, 2, bevel=.8)
        c.poly(HONEY, (32, 48), (96, 48), (90, 56), (38, 58), bevel=.8)
    elif kind == "congee":  # Tianxia: porcelain bowl of rice congee
        bowl(c, PORCELAIN, RICE)
        c.ell(m("#5e8ab8", .04, 2), 64, 102, 30, 4, bevel=.4)
        for dx, dy in ((-10, -2), (12, 2)):
            c.ell(GREENS, 64 + dx, 72 + dy, 5, 2, bevel=.6)
        c.ell(m("#c87a3a", .1, 2), 64, 70, 7, 4, bevel=.8)
    elif kind == "mooncake":  # Tianxia: two mooncakes, one cut
        c.ell(MOON, 44, 74, 24, 20, bevel=2.0)
        for i in range(8):
            a = i * math.pi / 4
            c.ell(m("#a86a2a", .1, 2), 44 + 18 * math.cos(a), 74 + 15 * math.sin(a), 4, 3, bevel=.6)
        c.ell(m("#a86a2a", .1, 2), 44, 74, 9, 8, bevel=.6, edge=.2)
        c.poly(MOON, (70, 70), (106, 60), (104, 96), (74, 98), bevel=2.0)
        c.poly(m("#6a3a1a", .1, 2), (76, 74), (100, 66), (98, 92), (78, 94), bevel=.6)
        c.ell(m("#e8a63a", .06, 2), 88, 80, 6, 6, bevel=1.0)
    elif kind == "roast":  # Albion: roast with pudding and gravy
        plate(c)
        c.ell(MEAT_L, 54, 74, 24, 16, bevel=2.0)
        for i in range(3):
            c.scratch(.8, .4, (38 + i * 10, 66), (44 + i * 10, 84))
        c.ell(CRUST, 88, 70, 12, 10, bevel=2.0)
        c.ell(CRUST_D, 88, 68, 6, 4, bevel=.6)
        c.ell(GREENS, 82, 90, 8, 4, bevel=.8)
        c.poly(m("#5a3418", .06, 2, spec=.6), (30, 84), (60, 80), (64, 90), (34, 94), bevel=.6)
    elif kind == "scones":  # Albion: scones with cream and jam, teacup
        plate(c, ry=22)
        for dx in (-22, 4):
            c.ell(SCONE, 54 + dx, 72, 15, 12, bevel=2.0)
            c.ell(CREAM, 54 + dx, 66, 9, 4, bevel=.8)
            c.ell(JAM, 54 + dx, 64, 5, 2.4, bevel=.6)
        c.ell(PORCELAIN, 92, 64, 16, 8, bevel=1.4)
        c.poly(PORCELAIN, (76, 64), (108, 64), (102, 80), (82, 80), bevel=1.2)
        c.ell(m("#7a3a1a", .04, 2), 92, 64, 12, 5, bevel=.4)
    elif kind == "ful":  # Kemet: clay bowl of fava bean stew with bread
        bowl(c, TERRACOTTA, BEANS)
        for dx, dy in ((-14, -2), (2, 4), (16, -2), (-4, -6), (10, 6)):
            c.ell(m("#6a4422", .12, 2), 64 + dx, 72 + dy, 4, 3, bevel=.8)
        c.ell(m("#c8b04a", .06, 2, spec=.8), 70, 68, 8, 3, bevel=.6)
        c.ell(CRUST, 102, 54, 16, 10, bevel=1.6)
    elif kind == "date_cake":  # Kemet: date and honey cakes on a palm leaf
        for i in range(6):
            c.line(LEAF, 5, (20 + i * 4, 98 - i * 2), (108, 66 - i * 4))
        for dx, dy in ((-24, 6), (0, 0), (24, -6)):
            c.ell(m("#7a3e1e", .12, 2), 64 + dx, 72 + dy, 14, 11, bevel=2.0)
            c.ell(DATE, 64 + dx, 68 + dy, 5, 3, bevel=1.0)
        c.ell(HONEY, 64, 66, 30, 4, bevel=.6)
    elif kind == "kebab":  # Pars: kebab on saffron rice
        plate(c, CERAMIC_B)
        c.ell(SAFFRON, 64, 78, 36, 14, bevel=1.4)
        c.ell(RICE, 64, 82, 30, 10, bevel=1.0)
        skewer(c, 18, 78, 110, 64, 6, (MEAT, MEAT_L))
        c.ell(CHILI, 30, 92, 8, 4, bevel=.8)
    elif kind == "sholeh":  # Pars: saffron rice pudding with pistachio
        bowl(c, PORCELAIN, SAFFRON)
        c.line(m("#6a3a1a", .1, 2), 1.4, (46, 70), (82, 70))
        c.line(m("#6a3a1a", .1, 2), 1.4, (64, 62), (64, 80))
        for dx, dy in ((-14, -6), (14, 6), (-14, 6), (14, -6)):
            c.ell(PISTACHIO, 64 + dx, 72 + dy, 3, 2, bevel=.6)
    elif kind == "locro":  # Inti: clay pot of corn and potato stew
        bowl(c, m("#8a4a2a", .12, 2), m("#d8a84a", .08, 2, spec=.4))
        for dx, dy, mat in ((-14, -2, POTATO), (8, 4, CORN), (16, -4, POTATO), (-2, 6, CORN), (0, -6, m("#3a6a2a", .1, 2))):
            c.ell(mat, 64 + dx, 72 + dy, 6, 4, bevel=1.0)
        for s in (-1, 1):
            c.ell(m("#8a4a2a", .12, 2), 64 + s * 46, 74, 5, 8, bevel=1.0)
    elif kind == "humita":  # Inti: corn cakes steamed in husks
        for dx, dy, ang in ((-18, 6, -.4), (18, 2, .3), (0, -10, 0)):
            cx, cy = 64 + dx, 72 + dy
            ca, sa = math.cos(ang), math.sin(ang)
            pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in ((-30, 0), (-18, -11), (18, -11), (30, 0), (18, 11), (-18, 11))]
            c.poly(HUSK, *pts, bevel=1.6)
            c.ell(CORN, cx, cy, 14, 6, bevel=1.0)
            c.line(m("#a08a4a", .1, 2), 2, (cx - 12 * ca, cy - 12 * sa - 6), (cx - 12 * ca, cy - 12 * sa + 6))
    else:
        raise ValueError(kind)
    c.glow(52, 58, 30, "#ffffff", .06)
    return c.image()
