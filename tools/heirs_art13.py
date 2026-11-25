"""Heirs of Earth 3.2: new buildings for Albion, Kemet, Pars and Inti, and the eight defensive structures
(a 2x2 base plus a turning top that points right, like the Tianxia fire-arrow battery)."""
import math

from heirs_art import m, painter
from kut_render import BRONZE, DARKIRON, GOLD, IRON, LEATHER, STEEL, STONE, STONE_D, STONE_L, WOOD, WOOD_D, WOOD_V, Canvas

SAND = m("#d6b072", .10, 3, tint="#a8804a")
SAND_D = m("#a07a44", .12, 3)
BRICK = m("#8e4a32", .14, 2)
OAK = m("#6a4024", .16, 3, (1, 8))
OAK_D = m("#3e2414", .14, 3, (1, 8))
GLASS = m("#e8d8a0", .04, 2, spec=1.2, tint="#ffd27a")
BRASS = m("#c0963c", .06, 2, spec=1.2)
FACE = m("#efe6cc", .04, 2)
FLAME = m("#ffb648", .2, 2, tint="#ff6a2a")
LIME = m("#d8d2c4", .07, 4)
LIME_D = m("#9a9488", .09, 4)
TURQ = m("#2a8a96", .08, 2, spec=.6)
ROPE = m("#b8a070", .12, 2, (6, 1))
BAMBOO = m("#b8a05a", .12, 2, (8, 1))
LACQ_R = m("#8a2420", .08, 2, spec=.6)
CLAY = m("#a85a32", .12, 2)
SHADOW = m("#1e1610", .1)


def shadow(c, cx, cy, rx, ry):
    c.ell(SHADOW, cx, cy, rx, ry)


# ================================================================== Albion
@painter
def gas_lamp(size=(1, 1)):
    c = Canvas(128, 230, seed=1301)
    shadow(c, 64, 220, 26, 7)
    c.rect(DARKIRON, 50, 206, 78, 222, 3, bevel=1.4)
    c.rect(DARKIRON, 59, 70, 69, 210, 2, bevel=1.2, cyl=(59, 69))
    for y in (120, 170):
        c.rect(IRON, 55, y, 73, y + 6, 2, bevel=.8)
    c.line(DARKIRON, 3, (40, 70), (88, 70))
    c.poly(DARKIRON, (42, 34), (86, 34), (80, 26), (48, 26), bevel=1.0)
    c.poly(DARKIRON, (54, 26), (74, 26), (64, 14), bevel=1.0)
    c.poly(GLASS, (44, 36), (84, 36), (78, 70), (50, 70), bevel=1.4)
    for x in (58, 70):
        c.line(DARKIRON, 1.6, (x, 36), (x - (x - 64) * .2, 70))
    c.glow(64, 52, 34, "#ffd27a", .5)
    return c.image()


@painter
def grandfather_clock(size=(1, 1)):
    c = Canvas(128, 230, seed=1302)
    shadow(c, 64, 222, 34, 7)
    c.rect(OAK_D, 30, 200, 98, 224, 3, bevel=1.6)
    c.rect(OAK, 38, 92, 90, 204, 3, bevel=1.8)
    c.rect(OAK_D, 50, 108, 78, 188, 4, bevel=.8, edge=.2)
    c.line(BRASS, 2, (64, 112), (64, 166))
    c.ell(BRASS, 64, 170, 9, 9, bevel=1.6)
    c.rect(OAK, 28, 24, 100, 96, 4, bevel=2.0)
    c.poly(OAK_D, (28, 26), (64, 8), (100, 26), bevel=1.4)
    c.ell(BRASS, 64, 60, 28, 28, bevel=1.6)
    c.ell(FACE, 64, 60, 23, 23, bevel=1.0)
    for k in range(12):
        a = k * math.pi / 6
        c.line(DARKIRON, 1.6, (64 + 18 * math.cos(a), 60 + 18 * math.sin(a)), (64 + 21 * math.cos(a), 60 + 21 * math.sin(a)))
    c.line(DARKIRON, 2.2, (64, 60), (64, 45))
    c.line(DARKIRON, 1.6, (64, 60), (76, 64))
    return c.image()


# ================================================================== Kemet
@painter
def sphinx(size=(2, 1)):
    c = Canvas(256, 180, seed=1303)
    shadow(c, 128, 166, 116, 14)
    c.rect(SAND_D, 14, 140, 242, 170, 3, bevel=1.8)
    c.poly(SAND, (40, 140), (44, 104), (70, 84), (170, 84), (178, 100), (180, 140), bevel=2.4)
    for x0 in (176, 204):
        c.poly(SAND, (x0, 140), (x0, 124), (x0 + 30, 122), (x0 + 36, 130), (x0 + 34, 140), bevel=1.6)
    c.poly(SAND, (150, 104), (156, 50), (176, 30), (200, 30), (214, 52), (214, 104), bevel=2.4)
    c.poly(m("#2a4a8a", .06, 2), (152, 64), (160, 40), (182, 24), (206, 26), (218, 50), (222, 104), (210, 104), (206, 60), (162, 62), bevel=1.6)
    for k in range(5):
        c.line(GOLD, 2.2, (160 + k, 44 + k * 12), (220 - k, 50 + k * 11))
    c.poly(SAND, (166, 54), (204, 54), (200, 92), (172, 92), bevel=1.8)
    c.ell(m("#3a2a1a", .1), 178, 68, 3, 2, bevel=.4)
    c.ell(m("#3a2a1a", .1), 194, 68, 3, 2, bevel=.4)
    c.poly(GOLD, (180, 92), (192, 92), (188, 108), (184, 108), bevel=1.0)
    c.poly(SAND_D, (28, 132), (14, 110), (24, 100), (40, 124), bevel=1.0)
    return c.image()


@painter
def lotus_lamp(size=(1, 1)):
    c = Canvas(128, 200, seed=1304)
    shadow(c, 64, 190, 28, 7)
    c.ell(BRONZE, 64, 184, 26, 8, bevel=1.6)
    c.rect(BRONZE, 58, 80, 70, 182, 2, bevel=1.2, cyl=(58, 70))
    for y in (110, 150):
        c.ell(GOLD, 64, y, 9, 4, bevel=1.0)
    for k in range(7):
        a = math.radians(-160 + k * 23)
        c.poly(m("#e8d8b0", .05, 2), (64, 80), (64 + 34 * math.cos(a) - 8, 70 + 30 * math.sin(a)), (64 + 40 * math.cos(a), 66 + 34 * math.sin(a)),
               (64 + 34 * math.cos(a) + 8, 70 + 30 * math.sin(a)), bevel=1.2)
    c.ell(BRONZE, 64, 72, 22, 8, bevel=1.4)
    c.poly(FLAME, (56, 70), (64, 34), (72, 70), bevel=1.0)
    c.glow(64, 56, 34, "#ffb040", .55)
    return c.image()


# ================================================================== Pars
@painter
def fire_altar(size=(1, 1)):
    c = Canvas(128, 190, seed=1305)
    shadow(c, 64, 180, 50, 9)
    for i, (w, y) in enumerate(((52, 170), (44, 152), (34, 134))):
        c.rect(LIME if i % 2 == 0 else LIME_D, 64 - w, y - 16, 64 + w, y + 6, 2, bevel=1.6)
    c.rect(LIME, 46, 70, 82, 118, 2, bevel=1.8)
    for x in (50, 78):
        c.line(LIME_D, 2, (x, 76), (x, 114))
    c.rect(LIME_D, 36, 60, 92, 72, 2, bevel=1.4)
    for k in range(5):
        c.poly(LIME, (38 + k * 11, 60), (42 + k * 11, 52), (46 + k * 11, 60), bevel=.6)
    c.ell(BRONZE, 64, 58, 22, 7, bevel=1.2)
    c.poly(FLAME, (48, 58), (56, 26), (64, 40), (70, 14), (80, 58), bevel=1.0)
    c.glow(64, 40, 40, "#ffa040", .6)
    return c.image()


@painter
def lamassu(size=(2, 1)):
    c = Canvas(256, 210, seed=1306)
    shadow(c, 128, 196, 116, 12)
    c.rect(LIME_D, 16, 176, 240, 200, 3, bevel=1.8)
    c.poly(LIME, (44, 176), (48, 112), (64, 94), (170, 92), (186, 112), (190, 176), bevel=2.4)
    for x in (50, 86, 150, 180):
        c.rect(LIME, x, 140, x + 18, 178, 2, bevel=1.4)
        c.rect(LIME_D, x - 2, 170, x + 20, 178, 2, bevel=.8)
    for k in range(4):
        c.poly(LIME, (70 + k * 6, 98 - k * 4), (150, 30 + k * 12), (166, 40 + k * 12), (90 + k * 6, 104), bevel=1.2)
    c.poly(LIME, (172, 120), (180, 70), (200, 56), (222, 66), (226, 120), bevel=2.0)
    for k in range(5):
        c.line(LIME_D, 2, (186, 98 + k * 6), (222, 98 + k * 6))
    c.poly(LIME_D, (182, 64), (190, 34), (212, 30), (222, 62), bevel=1.6)
    for k in range(3):
        c.line(GOLD, 2, (186 + k, 48 + k * 8), (218 - k, 46 + k * 8))
    c.ell(m("#3a2a1a", .1), 198, 76, 3, 2, bevel=.4)
    c.ell(m("#3a2a1a", .1), 214, 76, 3, 2, bevel=.4)
    return c.image()


# ================================================================== Inti
@painter
def sun_disc(size=(1, 1)):
    c = Canvas(128, 210, seed=1307)
    shadow(c, 64, 200, 40, 9)
    c.poly(STONE, (28, 202), (34, 148), (94, 148), (100, 202), bevel=2.0)
    for y in (166, 184):
        c.scratch(.7, .3, (32, y), (96, y))
    c.rect(STONE_D, 56, 104, 72, 150, 2, bevel=1.2)
    for k in range(16):
        a = k * math.pi / 8
        r1, r2 = 30, 50 if k % 2 == 0 else 42
        c.poly(GOLD, (64 + r1 * math.cos(a - .14), 64 + r1 * math.sin(a - .14)), (64 + r2 * math.cos(a), 64 + r2 * math.sin(a)),
               (64 + r1 * math.cos(a + .14), 64 + r1 * math.sin(a + .14)), bevel=1.0)
    c.ell(GOLD, 64, 64, 32, 32, bevel=2.2)
    c.ell(m("#d8a83a", .06, 2, spec=1.4), 64, 64, 24, 24, bevel=1.2)
    c.ell(m("#8a5a1a", .08, 2), 56, 60, 3, 2, bevel=.4)
    c.ell(m("#8a5a1a", .08, 2), 72, 60, 3, 2, bevel=.4)
    c.line(m("#8a5a1a", .08, 2), 2, (56, 74), (72, 74))
    c.glow(56, 52, 30, "#fff0b0", .35)
    return c.image()


@painter
def puma_stone(size=(2, 1)):
    c = Canvas(256, 170, seed=1308)
    shadow(c, 128, 158, 114, 12)
    c.poly(STONE_D, (16, 162), (24, 136), (232, 136), (240, 162), bevel=1.8)
    c.poly(STONE_L, (46, 138), (52, 96), (80, 80), (170, 78), (190, 92), (196, 138), bevel=2.4)
    for x in (56, 92, 156, 182):
        c.rect(STONE_L, x, 118, x + 16, 140, 3, bevel=1.4)
    c.poly(STONE_L, (172, 98), (184, 54), (206, 46), (228, 60), (226, 100), bevel=2.0)
    c.poly(STONE_L, (188, 50), (192, 36), (200, 46), bevel=.8)
    c.poly(STONE_L, (210, 46), (218, 34), (222, 50), bevel=.8)
    c.ell(m("#2a2a1a", .1), 200, 66, 3, 2, bevel=.4)
    c.ell(m("#2a2a1a", .1), 216, 66, 3, 2, bevel=.4)
    pts = [(48, 100), (30, 92), (20, 70), (28, 56)]
    for i in range(3):
        c.line(STONE_L, 9 - i, pts[i], pts[i + 1])
    for k in range(4):
        c.scratch(.8, .35, (90 + k * 18, 84), (86 + k * 18, 132))
    return c.image()


# ================================================================== defensive structures: bases (2x2)
@painter
def turret_base(style="stone", size=(2, 2)):
    c = Canvas(256, 256, seed=1310 + len(style))
    shadow(c, 132, 140, 112, 104)
    if style == "stone":       # Roma, Hellas: dressed stone platform
        c.rect(STONE_D, 22, 22, 234, 234, 10, bevel=2.4)
        c.rect(STONE_L, 34, 34, 222, 222, 8, bevel=2.0)
        for k in range(1, 4):
            c.scratch(.8, .3, (34, 34 + k * 47), (222, 34 + k * 47))
        c.ell(STONE, 128, 128, 60, 60, bevel=1.6)
    elif style == "yagura":    # Yamato: timber tower with white plaster and a tiled skirt
        c.rect(m("#2a2a30", .1, 2, (6, 1)), 14, 14, 242, 242, 6, bevel=2.4)
        for k in range(8):
            c.line(m("#4a4a52", .1, 2), 2, (14, 24 + k * 28), (242, 24 + k * 28))
        c.rect(m("#efe8da", .04, 2), 46, 46, 210, 210, 4, bevel=1.8)
        c.rect(WOOD_D, 46, 46, 210, 58, 2, bevel=1.0)
        c.rect(WOOD_D, 46, 198, 210, 210, 2, bevel=1.0)
        c.ell(WOOD, 128, 128, 54, 54, bevel=1.6)
    elif style == "loft":      # Nord: log platform on posts
        for k in range(7):
            c.rect(WOOD if k % 2 else WOOD_D, 20, 20 + k * 31, 236, 48 + k * 31, 8, bevel=1.8)
        for x, y in ((24, 24), (232, 24), (24, 232), (232, 232)):
            c.ell(WOOD_D, x, y, 12, 12, bevel=1.4)
        c.ell(WOOD, 128, 128, 56, 56, bevel=1.6)
    elif style == "gunpit":    # Albion: sandbags and brick
        c.rect(BRICK, 24, 24, 232, 232, 10, bevel=2.2)
        for k in range(10):
            a = k * math.pi / 5
            c.ell(m("#b8a47a", .14, 2), 128 + 96 * math.cos(a), 128 + 96 * math.sin(a), 26, 18, bevel=1.8)
        c.ell(m("#6a6058", .1, 2), 128, 128, 62, 62, bevel=1.4)
    elif style == "pylon":     # Kemet: sloped sandstone pylon top
        c.poly(SAND_D, (14, 14), (242, 14), (242, 242), (14, 242), bevel=2.2)
        c.rect(SAND, 34, 34, 222, 222, 4, bevel=2.0)
        for k in range(6):
            c.line(m("#2a4a8a", .06, 2), 3, (40, 46 + k * 34), (60, 46 + k * 34))
            c.line(m("#2a4a8a", .06, 2), 3, (196, 46 + k * 34), (216, 46 + k * 34))
        c.ell(SAND_D, 128, 128, 56, 56, bevel=1.6)
    elif style == "tiles":     # Pars: glazed parapet
        c.rect(LIME_D, 18, 18, 238, 238, 8, bevel=2.2)
        c.rect(LIME, 30, 30, 226, 226, 6, bevel=1.8)
        for k in range(8):
            for x, y in ((40 + k * 24, 38), (40 + k * 24, 210), (38, 40 + k * 24), (210, 40 + k * 24)):
                c.rect(TURQ, x, y, x + 16, y + 10, 2, bevel=.8)
        c.ell(LIME_D, 128, 128, 56, 56, bevel=1.6)
    elif style == "earthwork":  # trebuchet: rammed earth bed, sleeper beams and a heap of stones
        c.rect(m("#7a6448", .16, 2, (4, 1)), 14, 14, 242, 242, 14, bevel=2.2)
        c.rect(m("#8e7656", .14, 2, (4, 1)), 30, 30, 226, 226, 10, bevel=1.4, edge=.2)
        for y in (54, 202):
            c.rect(WOOD_D, 24, y - 9, 232, y + 9, 3, bevel=1.6)
        for x in (60, 196):
            c.rect(WOOD, x - 8, 30, x + 8, 226, 3, bevel=1.6)
        for k, (x, y) in enumerate(((40, 226), (54, 214), (34, 208), (220, 40), (206, 30))):
            c.ell(STONE_L if k % 2 else STONE, x, y, 11, 10, bevel=1.6)
        c.ell(m("#6a563c", .1, 2), 128, 128, 60, 60, bevel=1.2)
    else:                      # inti: fitted stone ring
        c.ell(STONE_D, 128, 128, 116, 116, bevel=2.4)
        for k in range(14):
            a = k * 2 * math.pi / 14
            c.ell(STONE_L, 128 + 92 * math.cos(a), 128 + 92 * math.sin(a), 22, 20, bevel=1.8)
        c.ell(STONE, 128, 128, 60, 60, bevel=1.6)
    return c.image()


# ================================================================== defensive structures: turning tops (point right)
def _bolt(c, x0, y, x1, mat=STEEL):
    c.line(WOOD_V, 3, (x0, y), (x1 - 12, y))
    c.poly(mat, (x1 - 14, y - 5), (x1, y), (x1 - 14, y + 5), bevel=.8)
    c.poly(m("#d8d0b8", .05), (x0, y), (x0 + 10, y - 6), (x0 + 14, y), (x0 + 10, y + 6), bevel=.4)


def _bow(c, cx, cy, span, mat=WOOD_D, curve=22):
    pts = [(cx - curve * (1 - (t / 10) ** 2) * 1.0 + curve, cy - span + 2 * span * t / 20) for t in range(-10, 11)]
    pts = [(cx + curve * (1 - ((i - 10) / 10) ** 2), cy - span + span * i / 10) for i in range(21)]
    for i in range(20):
        c.line(mat, 6 - abs(i - 10) * .3, pts[i], pts[i + 1])
    c.line(ROPE, 1.4, pts[0], (cx - 14, cy), pts[-1])


@painter
def turret_top(kind="scorpio", size=(2, 2)):
    c = Canvas(256, 256, seed=1320 + len(kind))
    cx, cy = 118, 128
    if kind == "scorpio":       # Roma: torsion bolt thrower with two spring frames
        c.rect(WOOD, cx - 70, cy - 10, cx + 70, cy + 10, 3, bevel=1.8)
        for s in (-1, 1):
            c.rect(WOOD_D, cx + 20, cy + s * 18 - 14, cx + 40, cy + s * 18 + 14, 3, bevel=1.6)
            c.ell(m("#6a3a22", .14, 2), cx + 30, cy + s * 18, 7, 7, bevel=1.0)
            c.line(WOOD_V, 6, (cx + 30, cy + s * 30), (cx + 8, cy + s * 66))
        c.line(ROPE, 1.6, (cx + 8, cy - 66), (cx - 40, cy), (cx + 8, cy + 66))
        _bolt(c, cx - 44, cy, cx + 100)
        c.rect(BRONZE, cx - 74, cy - 14, cx - 60, cy + 14, 3, bevel=1.2)
    elif kind == "multibow":    # Yamato: three bows on a turning frame
        c.rect(LACQ_R, cx - 60, cy - 40, cx + 30, cy + 40, 4, bevel=2.0)
        for dy in (-30, 0, 30):
            _bow(c, cx + 34, cy + dy, 26, LACQ_R, 10)
            _bolt(c, cx - 30, cy + dy, cx + 70)
    elif kind == "longbow":     # Nord: a huge twin bow (springald)
        c.rect(WOOD_D, cx - 60, cy - 26, cx + 20, cy + 26, 4, bevel=2.0)
        for dy in (-14, 14):
            _bow(c, cx + 24, cy + dy, 70, WOOD_D, 18)
            _bolt(c, cx - 50, cy + dy, cx + 80, IRON)
    elif kind == "lithobolos":  # Hellas: torsion stone thrower, arm forward with a stone in the cup
        c.rect(WOOD, cx - 70, cy - 40, cx + 40, cy + 40, 4, bevel=2.0)
        c.rect(WOOD_D, cx - 60, cy - 30, cx + 30, cy + 30, 4, bevel=.8, edge=.2)
        for s in (-1, 1):
            c.ell(m("#6a3a22", .14, 2), cx - 10, cy + s * 34, 12, 12, bevel=1.4)
        c.line(WOOD_V, 10, (cx - 10, cy), (cx + 88, cy))
        c.ell(LEATHER, cx + 92, cy, 16, 14, bevel=1.4)
        c.ell(STONE_L, cx + 92, cy, 11, 10, bevel=1.8)
    elif kind == "cannon":      # Albion: field cannon on a carriage
        for s in (-1, 1):
            c.rect(WOOD_D, cx - 70, cy + s * 26 - 6, cx + 20, cy + s * 26 + 6, 2, bevel=1.4)
            c.ell(WOOD, cx - 10, cy + s * 40, 30, 8, bevel=1.6)
        c.rect(BRONZE, cx - 50, cy - 16, cx + 96, cy + 16, 12, bevel=2.4, cyl=None)
        for x in (cx - 30, cx + 20, cx + 70):
            c.rect(m("#8a6a2a", .08, 2, spec=1.0), x, cy - 18, x + 6, cy + 18, 2, bevel=.8)
        c.ell(DARKIRON, cx + 96, cy, 6, 12, bevel=1.0)
        c.ell(BRONZE, cx - 56, cy, 10, 10, bevel=1.4)
    elif kind == "pylonbows":   # Kemet: four composite bows on a turning stand
        c.rect(SAND_D, cx - 50, cy - 56, cx + 20, cy + 56, 6, bevel=2.0)
        for dy in (-42, -14, 14, 42):
            _bow(c, cx + 24, cy + dy, 14, m("#5a3a1e", .12, 2), 8)
            _bolt(c, cx - 30, cy + dy, cx + 56, BRONZE)
        c.ell(GOLD, cx - 26, cy, 10, 10, bevel=1.4)
    elif kind == "naft":        # Pars: naphtha siphon with a bronze tank and a long nozzle
        c.ell(BRONZE, cx - 30, cy, 46, 40, bevel=2.4)
        c.ell(m("#6a4a1e", .1, 2), cx - 30, cy, 30, 26, bevel=1.0, edge=.2)
        c.rect(BRONZE, cx, cy - 10, cx + 90, cy + 10, 6, bevel=1.8)
        c.poly(BRONZE, (cx + 86, cy - 16), (cx + 108, cy - 8), (cx + 108, cy + 8), (cx + 86, cy + 16), bevel=1.4)
        c.rect(WOOD, cx - 84, cy - 4, cx - 70, cy + 4, 2, bevel=.8)
        c.glow(cx + 112, cy, 12, "#ff8a3a", .5)
    elif kind == "trebuchet":   # shared: counterweight trebuchet, arm cocked back, sling laid out forward
        for s in (-1, 1):                       # the two side frames, an A seen from above
            c.rect(WOOD_D, cx - 78, cy + s * 34 - 7, cx + 58, cy + s * 34 + 7, 2, bevel=1.8)
            c.line(WOOD, 7, (cx - 70, cy + s * 34), (cx - 6, cy + s * 34))
            c.line(WOOD, 7, (cx + 50, cy + s * 34), (cx - 6, cy + s * 34))
        for x in (cx - 74, cx + 54):            # cross ties
            c.rect(WOOD_D, x - 6, cy - 40, x + 6, cy + 40, 2, bevel=1.4)
        c.rect(DARKIRON, cx - 12, cy - 44, cx, cy + 44, 3, bevel=1.4)   # the iron axle
        c.rect(m("#5a4a3a", .14, 2, (3, 1)), cx - 64, cy - 24, cx - 22, cy + 24, 4, bevel=2.2)  # counterweight box of stones
        for x, y in ((-54, -12), (-36, -14), (-48, 6), (-30, 8), (-42, -2)):
            c.ell(STONE, cx + x, cy + y, 8, 7, bevel=1.4)
        c.line(WOOD_V, 12, (cx - 30, cy), (cx + 104, cy))                 # the long throwing arm
        for x in (cx + 20, cx + 60):
            c.line(DARKIRON, 2.4, (x, cy - 7), (x, cy + 7))
        c.line(ROPE, 1.8, (cx + 104, cy), (cx + 66, cy - 16))
        c.line(ROPE, 1.8, (cx + 104, cy), (cx + 66, cy + 16))
        c.ell(LEATHER, cx + 62, cy, 13, 17, bevel=1.4)
        c.ell(STONE_L, cx + 62, cy, 9, 10, bevel=1.8)
    else:                       # inti sling stand: a long sling arm and a basket of stones
        c.ell(m("#8a7a4a", .14, 2, (5, 1)), cx - 34, cy, 40, 40, bevel=2.0)
        for k in range(9):
            a = k * 2 * math.pi / 9
            c.ell(STONE_L, cx - 34 + 20 * math.cos(a), cy + 20 * math.sin(a), 8, 7, bevel=1.4)
        c.line(WOOD_V, 8, (cx - 10, cy), (cx + 70, cy))
        c.line(ROPE, 2, (cx + 70, cy), (cx + 96, cy - 10))
        c.line(ROPE, 2, (cx + 70, cy), (cx + 96, cy + 10))
        c.ell(m("#8a7a4a", .14, 2), cx + 98, cy, 10, 12, bevel=1.2)
        c.ell(STONE_L, cx + 98, cy, 6, 6, bevel=1.4)
    return c.image()
