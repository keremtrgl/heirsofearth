"""Heirs of Earth 3.0 painters: New Kemet.

Emblem (falcon), weapons (lotus spear, khopesh, composite bow, desert rifle), armour icons (torso3, helmet3),
buildings (obelisk, senet table, papyrus workshop), floors (silt, lotus tiles), food3, goods3, relic3 and the Sun Disc.
Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module after heirs_art5.
"""
import math

import numpy as np
from PIL import ImageFilter

import heirs_art4
import heirs_style_sample as sample
from heirs_art import (BRONZE, DARKIRON, EMBLEMS, GOLD, STONE_D, WOOD_D, Canvas, axis, finish_floor, floor_canvas, haft, m,
                       painter, shade)
from heirs_art2 import ring
from heirs_art3 import _halo
from heirs_art4 import BRASS, LINEN, LINEN_D, _spline, _tube

# ------------------------------------------------------------------ materials
LAPIS = m("#22437e", .08, 2, spec=.5, tint="#14295a")
LAPIS_D = m("#14295a", .10, 2)
TURQ = m("#3fa39a", .08, 2, spec=.6)
CARNELIAN = m("#b2402a", .08, 2, spec=.7)
EBONY = m("#2a1e18", .10, 3, (9, 1), spec=.5)
IVORY = m("#ece2c6", .04, 2, spec=.5)
ACACIA = m("#9a6a3a", .14, 3, (9, 1))
ACACIA_V = m("#9a6a3a", .14, 3, (1, 9))
SANDSTONE = m("#d2b07a", .12, 2.5)
SANDSTONE_D = m("#a8844e", .12, 2.5)
REED = m("#a8a25a", .12, 1.5, (1, 6))
HORN = m("#3a2a1e", .12, 2, (6, 1), spec=.5)
BLUE_LEATHER = m("#2b4f8c", .10, 2, spec=.3)
SCALE = m("#b07a3a", .08, 2, spec=.9, tint="#7a4a1a")
CRUST = m("#c08a46", .12, 2, tint="#8a5a26")
DATE = m("#5a2416", .10, 2, spec=.8)
CHEESE = m("#efe2b8", .05, 2)
ONION = m("#c9a07a", .08, 2, spec=.4)
PAPY = m("#e6d7a6", .06, 1.5, (1, 3))
PAPY_H = m("#e6d7a6", .06, 1.5, (3, 1))


# ================================================================== emblem
def _falcon(c):
    """A displayed falcon in lapis and gold: wings spread and lowered, head in profile with the dark cheek stripe."""
    gold_d = m("#9a7224", .10, 2, spec=.6)
    lapis_l = m("#3462ac", .08, 2, spec=.5)
    cream = m("#efe4c4", .05, 2)

    def feather(base, tip, w, mat):
        bx, by = base
        tx, ty = tip
        dx, dy = tx - bx, ty - by
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        mid = (bx + dx * .45, by + dy * .45)
        c.poly(mat, (bx + nx * w * .6, by + ny * w * .6), (mid[0] + nx * w, mid[1] + ny * w), (tx, ty),
               (mid[0] - nx * w, mid[1] - ny * w), (bx - nx * w * .6, by - ny * w * .6), bevel=1.0)
        c.scratch(.7, .45, (bx, by), (bx + dx * .85, by + dy * .85), color=(.85, .7, .3))

    for flip in (False, True):
        fx = (lambda p: sample.mirror([p], 64)[0]) if flip else (lambda p: p)
        # primaries and secondaries fan from the wing's trailing edge, outermost first so the inner ones overlap
        for k in range(7, -1, -1):
            t = k / 7
            base = (56 - 18 * t, 57 - 9 * t)
            a = math.radians(100 + 42 * t)
            tip = (base[0] + 27 * math.cos(a) * (1 - .12 * t), base[1] + 30 * math.sin(a) * (1 - .25 * t))
            feather(fx(base), fx(tip), 4.2, LAPIS if k % 2 else lapis_l)
        cov = [(60, 50), (51, 40), (39, 34), (27, 35), (19, 42), (22, 48), (34, 50), (46, 55), (56, 60)]
        c.poly(TURQ, *[fx(p) for p in cov], bevel=1.4)
        for row in range(2):
            for k in range(6):
                x, y = 24 + k * 6 + row * 3, 44 + row * 5 + k * 1.2
                c.scratch(.9, .55, fx((x - 2.6, y)), fx((x, y + 2.4)), fx((x + 2.6, y)), color=(.6, .45, .1))
        lead = [(60, 50), (51, 40), (39, 34), (27, 35), (19, 42), (30, 40), (42, 41), (54, 49)]
        c.poly(LAPIS, *[fx(p) for p in lead], bevel=1.2)
        c.line(GOLD, 1.2, *[fx(p) for p in lead[:5]], bevel=.4)
    for k in range(5):
        x0 = 59 + k * 2.5
        tip = (52 + k * 6, 106 - abs(k - 2) * 2)
        feather((x0, 82), tip, 3.4, LAPIS if k % 2 else lapis_l)
    c.line(GOLD, 1.4, (55, 98), (73, 98))
    body = [(64, 44), (71, 50), (74, 64), (71, 78), (64, 86), (57, 78), (54, 64), (57, 50)]
    c.poly(LAPIS, *body, bevel=1.8)
    chest = [(64, 52), (69, 57), (70, 68), (66, 78), (64, 80), (62, 78), (58, 68), (59, 57)]
    c.poly(cream, *chest, bevel=1.0)
    for row, y in enumerate((60, 65, 70, 75)):
        for x in range(60 + (row % 2) * 2, 70, 4):
            c.scratch(.8, .6, (x - 1.4, y - 1.2), (x, y), (x + 1.4, y - 1.2), color=(.1, .14, .3))
    for x in (60, 68):
        c.line(GOLD, 2.2, (x, 84), (x + (x - 64) * .4, 92))
        for k in (-1, 0, 1):
            c.line(gold_d, 1.1, (x + (x - 64) * .4, 92), (x + (x - 64) * .4 + k * 2.6, 96))
    head = [(68, 30), (62, 27), (55, 28), (50, 32), (49, 37), (52, 42), (58, 47), (66, 48), (71, 42), (71, 35)]
    c.poly(LAPIS, *head, bevel=1.6)
    c.poly(cream, (52, 41), (56, 46), (63, 48), (66, 44), (60, 41), (56, 40), bevel=.8)
    c.line(LAPIS_D, 2.4, (56, 36), (55, 41), (57, 46))
    c.poly(GOLD, (51, 33), (45, 34), (42, 37), (43, 41), (45, 39), (49, 40), (52, 38), bevel=.8)
    c.poly(gold_d, (43, 41), (42, 37), (44, 37), bevel=.3)
    c.ell(TURQ, 51.5, 34.5, 1.6, 1.4)
    c.ell(GOLD, 56, 34, 2.8, 2.6, bevel=.5)
    c.ell(m("#141210", .05), 55.8, 34, 1.7, 1.7)
    c.ell(m("#ffffff", .02), 55.2, 33.3, .6, .6)
    c.line(LAPIS_D, 1.2, (53, 31), (60, 30), (68, 31))


EMBLEMS["falcon"] = _falcon


# ================================================================== weapons
_spear_long_prev = heirs_art4.spear_long


@painter
def spear_long(head="leaf", shaft="#6b4a2e", length=1.0):
    if head != "lotus":
        return _spear_long_prev(head=head, shaft=shaft, length=length)
    c = Canvas(128, seed=301)
    at, ln = axis((14, 118), (114, 10))
    haft(c, at, 0, ln - 22, 1.9, m(shaft, .14, 3, (1, 9), spec=.3))
    c.poly(BRONZE, at(-1, -2.4), at(5, -2.4), at(5, 2.4), at(-1, 2.4), bevel=.6)
    for u in (ln - 50, ln - 46):
        c.line(m("#3a8a80", .08, spec=.6), 1.6, at(u, -2.2), at(u, 2.2))
    c.poly(BRONZE, at(ln - 26, -2.6), at(ln - 18, -2.4), at(ln - 18, 2.4), at(ln - 26, 2.6), bevel=.8)
    leaf = [at(ln - 18, -2.2), at(ln - 12, -6.0), at(ln - 5, -4.6), at(ln, 0), at(ln - 5, 4.6), at(ln - 12, 6.0), at(ln - 18, 2.2)]
    c.poly(m("#c89a4a", .06, 2, spec=1.1, tint="#8a5a1a"), *leaf, bevel=1.0)
    c.line(m("#8a5a22", .08), 1.0, at(ln - 17, 0), at(ln - 2, 0), bevel=.3)
    for s in (-1, 1):
        c.scratch(.6, .35, at(ln - 13, s * 1.2), at(ln - 9, s * 4.4))
    return c.image()


@painter
def khopesh():
    """The sickle-sword: ebony grip with gold bands, a straight neck and a crescent bronze blade with a hooked tip."""
    c = Canvas(128, seed=302)
    at, ln = axis((22, 112), (100, 34))
    c.ell(GOLD, *at(0, 0), 5, 5, bevel=1.4)
    haft(c, at, 3, 26, 3.4, EBONY, bevel=1.2)
    for u in (8, 15, 22):
        c.poly(GOLD, at(u, -3.7), at(u + 2, -3.7), at(u + 2, 3.7), at(u, 3.7), bevel=.5)
    c.poly(BRONZE, at(25, -5.5), at(30, -5.5), at(30, 5.5), at(25, 5.5), bevel=.8)
    c.poly(BRONZE, at(30, -2.4), at(50, -2.2), at(50, 2.6), at(30, 2.4), bevel=.9)
    # The blade bends away from the axis in a wide sickle; its cutting edge is the outer (convex) side and the tip hooks back.
    centre = _spline([(48, 0), (60, -6), (74, -7), (86, -2), (94, 8), (96, 18)], 6)
    pts = [at(u, v) for u, v in centre]
    bronze_b = m("#c08a3a", .06, 2, spec=1.2, tint="#7a4a1a")
    left, right = _tube(c, bronze_b, pts, 8.5, 2.2, bevel=1.4)
    outer = left if sum(p[1] for p in left) < sum(p[1] for p in right) else right
    c.line(m("#f6dc96", .04, 2, spec=1.5), 1.6, *outer[2:-1], bevel=.4)
    c.line(m("#6a3a14", .08), 1.0, *pts[3:-6], bevel=.3)
    c.glow(*pts[len(pts) // 2], 14, "#fff0c0", .16)
    return c.image()


@painter
def composite_bow():
    """The angular composite bow: two nearly straight limbs meeting at the grip, horn tips and painted bands."""
    c = Canvas(128, seed=303)
    top, grip, bot = (40, 8), (74, 64), (40, 120)
    wood = m("#5a3620", .14, 3, (1, 8), spec=.4)
    belly = m("#c2a874", .08, 2, (1, 6), spec=.7)
    c.line(m("#efe6cc", .04), 1.2, (42, 10), (42, 118))
    for a, b in ((top, grip), (grip, bot)):
        pts = [(a[0] + (b[0] - a[0]) * t + 3.0 * math.sin(math.pi * t), a[1] + (b[1] - a[1]) * t) for t in np.linspace(0, 1, 12)]
        _tube(c, wood, pts, 4.6, 4.6, bevel=1.6)
        _tube(c, belly, [(x - 2.4, y) for x, y in pts[1:-1]], 1.6, 1.6, bevel=.6)
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        for t, mat in ((.2, GOLD), (.28, CARNELIAN), (.36, GOLD), (.62, TURQ), (.7, GOLD)):
            x, y = a[0] + dx * t + 3.0 * math.sin(math.pi * t), a[1] + dy * t
            c.line(mat, 2.2, (x - nx * 5, y - ny * 5), (x + nx * 5, y + ny * 5))
    c.rect(m("#e2d4ae", .06, 1.5, (4, 1)), 67, 54, 81, 74, 3, bevel=1.4)
    for y in range(56, 74, 3):
        c.line(m("#9a7a4a", .1), .8, (67, y), (81, y + 1))
    for y in (54, 74):
        c.line(GOLD, 2.0, (66, y), (82, y))
    for (x, y), d in ((top, 1), (bot, -1)):
        c.poly(IVORY, (x - 2, y + d * 6), (x - 4, y - d * 2), (x + 1, y - d * 5), (x + 3, y + d * 4), bevel=.8)
        c.line(m("#efe6cc", .04), 1.2, (x - 2, y + d * 2), (42, y + d * 2))
    c.glow(60, 40, 16, "#fff0c8", .12)
    return c.image()


@painter
def desert_rifle():
    """Kemet desert rifle: long slim stock bound in brass, a gold falcon on the lock plate, very long barrel."""
    c = Canvas(128, seed=304)
    at, ln = axis((8, 112), (122, 14))
    stock = m("#6a4426", .14, 3, (9, 1))
    c.poly(stock, at(0, -6), at(10, -5.6), at(28, -3), at(92, -2.4), at(92, 2.4), at(28, 3.4), at(10, 7.4), at(0, 7.6), bevel=1.6)
    c.poly(BRASS, at(-1, -6), at(2, -6), at(2, 7.6), at(-1, 7.6), bevel=.8)
    for u in (36, 56, 76, 90):
        c.line(BRASS, 1.8, at(u, -2.8), at(u, 2.8))
    c.poly(m("#3e4246", .08, 3, (9, 1), spec=1.0), at(24, -1.7), at(ln, -1.4), at(ln, 1.4), at(24, 1.7), bevel=.8)
    c.poly(m("#3e4246", .08, 3, spec=.9), at(24, -3.2), at(38, -3.2), at(38, 3.4), at(24, 3.4), bevel=1.0)
    c.ell(GOLD, *at(31, 0), 2.8, 2.6, bevel=.8)
    c.poly(LAPIS, at(29.6, -1), at(31, -2.2), at(32.4, -1), at(31, 1), bevel=.3)
    c.line(DARKIRON, 1.6, at(35, -3), at(32, -7), at(36, -8))
    c.line(DARKIRON, 1.5, at(27, 3.4), at(25, 7), at(20, 7.4))
    c.poly(BRASS, at(ln - 3, -2.2), at(ln, -2.2), at(ln, 2.2), at(ln - 3, 2.2), bevel=.5)
    c.poly(DARKIRON, at(ln - 6, -2.6), at(ln - 5, -3.8), at(ln - 4, -2.6), bevel=.3)
    for k in range(5):
        c.scratch(.5, .3, at(6 + k * 6, -4), at(9 + k * 6, 5))
    return c.image()


# ================================================================== apparel icons
@painter
def torso3(kind="kalasiris"):
    c = Canvas(128, seed=305)
    if kind == "kalasiris":
        dress = [(44, 30), (84, 30), (90, 60), (94, 118), (34, 118), (38, 60)]
        c.poly(LINEN, *dress, bevel=2.2)
        for x in range(42, 90, 5):
            c.scratch(.9, .32, (x, 52), (x + (x - 64) * .18, 116), color=(.55, .5, .4))
        c.poly(LINEN_D, (38, 30), (20, 40), (22, 56), (38, 50), bevel=1.6)
        c.poly(LINEN_D, (90, 30), (108, 40), (106, 56), (90, 50), bevel=1.6)
        c.rect(m("#b2402a", .08), 38, 66, 90, 72, 2, bevel=1.0)
        c.line(m("#b2402a", .08), 2.0, (60, 72), (56, 96))
        c.line(m("#b2402a", .08), 2.0, (66, 72), (68, 98))
        rows = (TURQ, CARNELIAN, LAPIS, GOLD, TURQ)
        for i, mat in enumerate(rows):
            r = 14 + i * 4.2
            for k in range(13 + i * 2):
                t = math.pi * (.08 + .84 * k / (12 + i * 2))
                c.ell(mat, 64 - r * 1.25 * math.cos(t), 26 + r * .9 * math.sin(t), 2.3, 2.6, bevel=.7)
        c.ell(m("#3a2a1e", .1), 64, 26, 9, 4)
    elif kind == "corselet":
        leather = m("#5a3a22", .12, 2)
        for i in range(9):
            x = 31 + i * 7.6
            c.rect(leather, x, 88, x + 6.4, 120 - abs(i - 4) * 1.5, 2, bevel=.9)
            c.rect(SCALE, x + 1, 112 - abs(i - 4) * 1.5, x + 5.4, 117 - abs(i - 4) * 1.5, 1, bevel=.6)
        body = [(36, 20), (52, 20), (64, 36), (76, 20), (92, 20), (100, 32), (98, 58), (96, 90), (32, 90), (30, 58), (28, 32)]
        c.poly(leather, *body, bevel=2.2)
        tints = [SCALE, BRONZE, m("#c08a46", .08, 2, spec=1.0, tint="#7a4a1a"), m("#9a6a30", .08, 2, spec=.8, tint="#6a3a12")]
        rng = np.random.default_rng(42)
        for row in range(10, -1, -1):
            y = 22 + row * 6.6
            for i in range(-1, 12):
                x = 31 + i * 6.6 + (row % 2) * 3.3
                sc = [(x - 3.2, y), (x + 3.2, y), (x + 3.2, y + 6), (x + 2.2, y + 8.6), (x, y + 9.8), (x - 2.2, y + 8.6), (x - 3.2, y + 6)]
                c.poly(m("#2a1a10", .1), *[(px + .5, py + 1.2) for px, py in sc], bevel=0, clip=True)
                c.poly(tints[rng.integers(0, 4)], *sc, bevel=.9, clip=True)
                c.ell(m("#2a1a10", .1), x, y + 1.6, .7, .7, clip=True)
        c.poly(BLUE_LEATHER, (48, 20), (54, 20), (64, 34), (74, 20), (80, 20), (64, 42), bevel=1.2)
        c.line(GOLD, 1.4, (50, 20), (64, 38), (78, 20), bevel=.4)
        for x0, x1 in ((28, 48), (80, 100)):
            c.rect(m("#3a2416", .12), x0, 14, x1, 24, 3, bevel=1.2)
            c.ell(GOLD, (x0 + x1) / 2, 19, 2.2, 2.2, bevel=.8)
        c.rect(BLUE_LEATHER, 30, 82, 98, 92, 2, bevel=1.4)
        for x in range(34, 98, 7):
            c.ell(GOLD, x, 87, 1.7, 1.7, bevel=.5)
        c.glow(44, 40, 26, "#fff0c8", .16)
    return c.image()


@painter
def helmet3(kind="khepresh"):
    c = Canvas(128, seed=306)
    if kind == "khepresh":
        # Three-quarter view facing left: a low upright front, then the crown swells up and back to a rounded peak.
        for k, (x0, y0) in enumerate(((98, 94), (104, 92))):
            ribbon = _spline([(x0, y0), (x0 + 6, y0 + 10), (x0 + 2, y0 + 20), (x0 + 8, y0 + 30)], 5)
            _tube(c, CARNELIAN if k else GOLD, ribbon, 2.6, 2.0, bevel=.8)
        crown = [(36, 96), (32, 82), (33, 68), (40, 54), (50, 42), (64, 32), (80, 24), (94, 22), (104, 28), (110, 40), (110, 56),
                 (106, 72), (102, 86), (102, 96)]
        c.poly(BLUE_LEATHER, *crown, bevel=2.8)
        for row in range(10):
            y = 26 + row * 8
            for k in range(11):
                x = 30 + k * 8 + (row % 2) * 4
                c.ell(m("#1a2e58", .1), x + .5, y + .8, 2.1, 2.1, clip=True)
                c.ell(GOLD, x, y, 2.1, 2.1, bevel=.7, clip=True)
        c.scratch(1.4, .4, (40, 56), (60, 38), (84, 28), (100, 28), color=(.08, .12, .26))
        flap = [(40, 78), (30, 82), (24, 92), (28, 102), (38, 104), (44, 98), (38, 94), (36, 88)]
        c.poly(m("#244682", .10, 2, spec=.3), *flap, bevel=1.6)
        c.line(GOLD, 1.2, (31, 84), (26, 93), (30, 101), (38, 103), bevel=.4)
        c.rect(GOLD, 34, 92, 104, 102, 3, bevel=1.5)
        for x in range(38, 102, 6):
            c.line(LAPIS, 1.6, (x, 94), (x, 100))
        c.ell(GOLD, 42, 86, 5.2, 5.2, bevel=1.2)
        c.ell(CARNELIAN, 42, 86, 2.8, 2.8, bevel=.8)
        c.glow(60, 40, 26, "#d8e6ff", .22)
    return c.image()


# ================================================================== buildings
@painter
def obelisk(size=(1, 1)):
    """A needle of dressed sandstone with carved sign columns and a gilded pyramidion; drawn 1x2.4 cells tall."""
    c = Canvas(128, 307, seed=307)
    c.ell(m("#2a2018", .1), 70, 292, 44, 10)
    c.rect(SANDSTONE_D, 30, 270, 98, 296, 3, bevel=1.8)
    c.rect(SANDSTONE, 34, 262, 94, 274, 2, bevel=1.4)
    lit = [(44, 264), (52, 58), (64, 58), (64, 264)]
    dark = [(64, 264), (64, 58), (76, 58), (84, 264)]
    c.poly(SANDSTONE, *lit, bevel=1.4)
    c.poly(m("#b8945e", .12, 2.5), *dark, bevel=1.4)
    rng = np.random.default_rng(31)
    for y in range(70, 256, 11):
        w = 6 + (y - 58) / 206 * 9
        for x in (64 - w * .55, 64 + w * .55):
            kind = rng.integers(0, 4)
            if kind == 0:
                c.ell(m("#7a5a32", .1), x, y, 2.4, 2.4)
            elif kind == 1:
                c.line(m("#7a5a32", .1), 1.4, (x - 2.6, y), (x + 2.6, y))
                c.line(m("#7a5a32", .1), 1.4, (x, y - 2.6), (x, y + 2.6))
            elif kind == 2:
                c.poly(m("#7a5a32", .1), (x - 2.6, y + 2.4), (x, y - 2.6), (x + 2.6, y + 2.4), bevel=.3)
            else:
                c.rect(m("#7a5a32", .1), x - 2.4, y - 1.6, x + 2.4, y + 1.6, 1)
    for y in (66, 258):
        c.line(m("#8a6a3e", .1), 1.0, (46, y), (82, y))
    c.poly(GOLD, (52, 58), (64, 26), (64, 58), bevel=1.2)
    c.poly(m("#b88a2a", .06, 2, spec=1.0), (64, 26), (76, 58), (64, 58), bevel=1.2)
    c.glow(62, 34, 22, "#fff0b0", .5)
    return c.image()


@painter
def senet_table(size=(2, 1)):
    """An ebony table with an ivory senet board of thirty squares, pieces and throwing sticks, seen from above."""
    W, H = 256, 128
    c = Canvas(W, H, seed=308)
    c.rect(m("#1a1410", .1), 14, 18, W - 6, H - 6, 10)
    c.rect(EBONY, 8, 10, W - 12, H - 14, 8, bevel=2.4)
    c.rect(IVORY, 30, 26, W - 34, H - 30, 4, bevel=1.4)
    cell = (W - 64) / 10
    for row in range(3):
        for col in range(10):
            x, y = 30 + col * cell, 26 + row * (H - 56) / 3
            if (row + col) % 2:
                c.rect(m("#d8cba4", .05), x + 1, y + 1, x + cell - 1, y + (H - 56) / 3 - 1, 1)
            c.rect(m("#5a4a36", .1), x, y, x + 1, y + (H - 56) / 3, 0)
    for col, mark in ((5, "ankh"), (6, "x"), (7, "w"), (8, "3"), (9, "2")):
        x, y = 30 + col * cell + cell / 2, 26 + 2 * (H - 56) / 3 + (H - 56) / 6
        if mark == "x":
            c.line(LAPIS, 1.6, (x - 5, y - 5), (x + 5, y + 5))
            c.line(LAPIS, 1.6, (x + 5, y - 5), (x - 5, y + 5))
        elif mark == "w":
            c.line(LAPIS, 1.4, (x - 6, y), (x - 3, y - 3), (x, y), (x + 3, y - 3), (x + 6, y))
        elif mark in ("3", "2"):
            for k in range(int(mark)):
                c.ell(LAPIS, x - 4 + k * 4, y, 1.4, 1.4)
        else:
            c.ell(GOLD, x, y - 3, 3, 3.6, bevel=.6)
            c.line(GOLD, 1.6, (x, y), (x, y + 6))
            c.line(GOLD, 1.6, (x - 4, y + 1), (x + 4, y + 1))
    for i, col in enumerate((0, 2, 3, 4, 8)):
        x, y = 30 + col * cell + cell / 2, 26 + (H - 56) / 6
        c.ell(m("#2a1a10", .1), x + 1, y + 2, 4.8, 4.8)
        c.ell(m("#3a3e44", .06, spec=1.0), x, y, 4.8, 4.8, bevel=1.4)
        c.ell(m("#7a8088", .04, spec=1.0), x - .4, y - .6, 2.4, 2.4, bevel=.8)
    for i, col in enumerate((1, 3, 5, 6, 9)):
        x, y = 30 + col * cell + cell / 2, 26 + (H - 56) / 2
        c.ell(m("#2a1a10", .1), x + 1, y + 2, 4.4, 4.4)
        c.ell(CARNELIAN, x, y, 4.4, 4.4, bevel=1.4)
        c.ell(m("#e8a07a", .04, spec=.8), x - .4, y - .6, 2.0, 2.0, bevel=.6)
    for k in range(4):
        x = 52 + k * 16
        c.rect(IVORY if k % 2 else m("#c9b88a", .06), x, H - 22, x + 10, H - 16, 2, bevel=.8)
    return c.image()


@painter
def papyrus_bench(size=(2, 1)):
    """A reed-splitting table: a bundle of reeds, crosswise strips being laid, a beating stone and finished sheets on a rack."""
    W, H = 256, 128
    c = Canvas(W, H, seed=309)
    c.rect(m("#2a2018", .1), 12, 16, W - 6, H - 6, 8)
    c.rect(ACACIA, 6, 8, W - 12, H - 14, 6, bevel=2.2)
    for k in range(7):
        y = 22 + k * 6
        c.line(REED, 3.2, (16, y), (92, y + 2))
        c.ell(m("#7a8a3a", .1), 94, y + 2, 3, 2.6, bevel=.6)
    c.line(m("#c9a26a", .1), 2.4, (30, 20), (30, 64))
    c.line(m("#c9a26a", .1), 2.4, (74, 20), (74, 66))
    c.rect(m("#b8a878", .08), 104, 22, 168, 86, 2, bevel=1.0)
    for k in range(8):
        c.rect(PAPY, 106 + k * 7.8, 24, 112 + k * 7.8, 84, 1, bevel=.5)
    for k in range(5):
        c.rect(PAPY_H, 106, 26 + k * 12, 166, 32 + k * 12, 1, bevel=.5)
    c.ell(m("#4a4440", .1), 136, 104, 15, 9)
    c.ell(STONE_D, 134, 100, 14, 9, bevel=2.0)
    c.line(WOOD_D, 4.0, (36, 82), (78, 98))
    c.ell(m("#6a4a2a", .12), 82, 100, 8, 6, bevel=1.4)
    c.rect(m("#5a3a22", .12), 182, 16, 236, 104, 3, bevel=1.4)
    for k in range(3):
        y = 22 + k * 28
        c.rect(PAPY, 186, y, 232, y + 22, 1, bevel=1.0)
        for x in range(190, 232, 6):
            c.scratch(.6, .25, (x, y + 2), (x, y + 20))
    return c.image()


# ================================================================== floors
def _tile(d, box, fill, outline=None, width=0):
    for ox in (-1024, 0, 1024):
        for oy in (-1024, 0, 1024):
            d.rectangle((box[0] + ox, box[1] + oy, box[2] + ox, box[3] + oy), fill=fill, outline=outline, width=width)


@painter
def floor_silt():
    """Black river silt in raised beds, edged by narrow water channels; tiles every 256 pixels."""
    base = (86, 68, 50)
    img, d, rng = floor_canvas(base, 311)
    for y in range(0, 1024, 64):
        for x in range(0, 1024, 256):
            ph = rng.uniform(0, 6.3)
            wave = [(x + 14 + k * 8, y + 30 + 5 * math.sin(ph + k * .35)) for k in range(29)]
            d.line(wave, fill=shade(base, 1.22), width=14, joint="curve")
            d.line([(px, py + 10) for px, py in wave], fill=shade(base, .7), width=4, joint="curve")
    for _ in range(3200):
        x, y, r = rng.uniform(0, 1024), rng.uniform(0, 1024), rng.uniform(1.5, 5)
        col = shade(base, rng.uniform(.7, 1.35))
        for ox in (-1024, 0, 1024):
            for oy in (-1024, 0, 1024):
                d.ellipse((x - r + ox, y - r * .7 + oy, x + r + ox, y + r * .7 + oy), fill=col)
    for _ in range(160):
        x, y = rng.uniform(0, 1024), rng.uniform(0, 1024)
        d.line((x, y, x + rng.uniform(-3, 3), y - rng.uniform(4, 8)), fill=(86, 120, 50), width=2)
    for k in range(0, 1024, 256):
        _tile(d, (k - 11, 0, k + 11, 1024), (120, 96, 66))
        _tile(d, (k - 6, 0, k + 6, 1024), (58, 88, 100))
        _tile(d, (k - 2, 0, k + 1, 1024), (104, 140, 150))
        for j in range(0, 1024, 48):
            d.line((k - 4, j, k + 3, j + 14), fill=(150, 176, 178), width=1)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(1.6)), 311, 3.4)


@painter
def floor_lotus():
    """Sandstone slabs, each painted with a fan of blue lotus petals; a reed border runs along one edge of every slab."""
    base = (214, 186, 140)
    img, d, rng = floor_canvas(base, 312)
    cell = 256
    for i in range(4):
        for j in range(4):
            x, y = i * cell, j * cell
            d.rectangle((x + 4, y + 4, x + cell - 4, y + cell - 4), fill=shade(base, 1 + rng.uniform(-.05, .05)))
            for _ in range(80):
                px, py, r = x + rng.uniform(8, cell - 8), y + rng.uniform(8, cell - 8), rng.uniform(1, 3)
                d.ellipse((px - r, py - r, px + r, py + r), fill=shade(base, rng.uniform(.86, 1.05)))
            cx, cy = x + cell / 2, y + cell / 2 + 22
            for k in range(7):
                a = math.radians(-160 + k * 23.3)
                tip = (cx + 70 * math.cos(a), cy + 70 * math.sin(a))
                l = (cx + 24 * math.cos(a - .32), cy + 24 * math.sin(a - .32))
                r_ = (cx + 24 * math.cos(a + .32), cy + 24 * math.sin(a + .32))
                d.polygon([(cx, cy), l, tip, r_], fill=(52, 86, 150) if k % 2 else (74, 112, 176), outline=(30, 46, 86))
            d.ellipse((cx - 16, cy - 10, cx + 16, cy + 10), fill=(196, 150, 60), outline=(120, 84, 30))
            d.polygon([(cx - 26, cy + 8), (cx, cy + 30), (cx + 26, cy + 8)], fill=(70, 120, 70), outline=(40, 70, 40))
            for k in range(0, cell - 16, 12):
                d.line((x + 8 + k, y + cell - 20, x + 14 + k, y + cell - 38), fill=(70, 110, 66), width=3)
            d.rectangle((x, y, x + cell - 1, y + cell - 1), outline=shade(base, .72), width=5)
    return finish_floor(img, 312, 2.4)


# ================================================================== food, goods and relics
@painter
def food3(kind="bread"):
    c = Canvas(128, seed=313)
    if kind == "bread":
        c.ell(m("#4a3a1e", .1), 66, 84, 52, 28)
        c.ell(REED, 64, 80, 52, 28, bevel=2.2)
        for k in range(-40, 44, 8):
            c.scratch(.8, .4, (64 + k, 58), (64 + k * 1.1, 102))
        c.ell(m("#4a3018", .12), 63, 74, 36, 24)
        c.ell(m("#9a6a32", .12, 2), 60, 68, 36, 25, bevel=3.0)
        c.ell(CRUST, 58, 62, 31, 20, bevel=3.2)
        c.ell(m("#dca866", .08, 2), 52, 56, 18, 10, bevel=1.6)
        for k in range(6):
            a = k * math.pi / 3 + .3
            c.scratch(1.8, .6, (58 + 5 * math.cos(a), 62 + 3 * math.sin(a)), (58 + 26 * math.cos(a), 62 + 17 * math.sin(a)), color=(.38, .2, .06))
        rng = np.random.default_rng(13)
        for _ in range(26):
            a, r = rng.uniform(0, 6.3), rng.uniform(4, 26)
            c.ell(m("#f2e2b8", .03), 58 + r * math.cos(a), 62 + r * .62 * math.sin(a), 1.1, .7)
        c.glow(50, 52, 16, "#fff0c8", .25)
        for x, y in ((92, 70), (98, 80), (88, 86)):
            c.ell(DATE, x, y, 6, 3.6, bevel=1.2)
            c.ell(m("#c8806a", .05), x - 2, y - 1.4, 1.4, .8)
        c.ell(ONION, 34, 88, 9, 8, bevel=1.8)
        c.line(m("#7a8a3a", .1), 1.6, (34, 80), (30, 72))
        c.rect(CHEESE, 78, 90, 96, 102, 3, bevel=1.4)
    return c.image()


@painter
def goods3(kind="papyrus"):
    c = Canvas(128, seed=314)
    if kind == "papyrus":
        c.rect(m("#2a2018", .1), 22, 58, 110, 108, 4)
        for k in range(4):
            y = 52 - k * 5
            c.rect(PAPY if k % 2 else PAPY_H, 16 + k * 2, y, 104 + k * 2, y + 48, 2, bevel=1.4)
        for x in range(26, 110, 9):
            c.scratch(.6, .25, (x, 40), (x, 84))
        for y in range(42, 86, 7):
            c.scratch(.5, .2, (22, y), (106, y))
        c.rect(PAPY, 30, 82, 112, 100, 9, bevel=1.8, cyl=(82, 100))
        c.ell(m("#c9b488", .06), 112, 91, 4, 9, bevel=1.0)
        c.line(m("#8a2a1e", .1), 2.4, (70, 80), (70, 102))
    return c.image()


@painter
def relic3(kind="sundisc"):
    c = Canvas(128, seed=315)
    if kind == "sundisc":
        dull = m("#8a7444", .14, 2, spec=.3, tint="#5a4a2a")
        c.ell(m("#2a2018", .1), 68, 70, 50, 50)
        c.ell(dull, 64, 64, 50, 50, bevel=2.6)
        ring(c, 64, 64, 42, m("#6a5432", .12), 2.0)
        for k in range(24):
            a = k * 2 * math.pi / 24
            c.line(m("#5a4428", .12), 1.4 if k % 2 else 2.4, (64 + 44 * math.cos(a), 64 + 44 * math.sin(a)), (64 + 48 * math.cos(a), 64 + 48 * math.sin(a)))
        c.ell(m("#9a844e", .12, spec=.5), 64, 64, 16, 16, bevel=1.6)
        for k in range(12):
            a = k * 2 * math.pi / 12
            c.line(m("#7a6438", .12), 2.0, (64 + 18 * math.cos(a), 64 + 18 * math.sin(a)), (64 + 38 * math.cos(a), 64 + 38 * math.sin(a)))
        c.line(m("#2a2018", .1), 1.4, (40, 30), (52, 46), (48, 58), (60, 70))
        sand = m("#d6b880", .14, 2)
        c.poly(sand, (12, 112), (30, 92), (52, 96), (70, 84), (96, 94), (118, 90), (122, 118), (10, 120), bevel=2.0)
        for x in range(20, 116, 9):
            c.scratch(.8, .35, (x, 104), (x + 6, 102))
        c.glow(48, 44, 14, "#fff0c0", .2)
    return c.image()


@painter
def sun_disc():
    """The Sun Disc of Iteru restored: polished gold with engraved rays, a lapis ring of hours and a carnelian centre."""
    c = Canvas(128, seed=316)
    c.ell(GOLD, 64, 64, 52, 52, bevel=2.8)
    for k in range(36):
        a = k * 2 * math.pi / 36
        c.scratch(.9, .4, (64 + 22 * math.cos(a), 64 + 22 * math.sin(a)), (64 + 40 * math.cos(a), 64 + 40 * math.sin(a)), color=(.5, .34, .06))
    ring(c, 64, 64, 45, LAPIS, 5.0)
    for k in range(24):
        a = k * 2 * math.pi / 24
        c.ell(GOLD if k % 2 else TURQ, 64 + 45 * math.cos(a), 64 + 45 * math.sin(a), 1.8, 1.8, bevel=.6)
    c.ell(m("#c89a2a", .05, spec=1.3), 64, 64, 20, 20, bevel=2.0)
    c.ell(CARNELIAN, 64, 64, 9, 9, bevel=1.6)
    c.ell(m("#f6d6c8", .03), 61, 61, 2.4, 2.0)
    c.glow(52, 48, 22, "#fff6d0", .45)
    return _halo(c.image(), (255, 214, 120, 255), 8, .9)
