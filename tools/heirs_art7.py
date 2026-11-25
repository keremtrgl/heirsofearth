"""Heirs of Earth 3.0 painters: Satrapy of Pars.

Emblem (griffin), weapons (pomegranate spear, akinakes, recurve bow, jezail), armour icons (torso4, helmet4),
buildings (paradise garden, post station lamp, carpet loom), floor (girih tiles), food4, goods4, relic4 and the King's Eye.
Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module after heirs_art6.
"""
import math

import numpy as np

import heirs_art6
from heirs_art import BRONZE, DARKIRON, EMBLEMS, GOLD, STONE_D, Canvas, axis, finish_floor, floor_canvas, haft, m, painter, shade
from heirs_art2 import ring
from heirs_art3 import _halo
from heirs_art4 import BRASS, _spline, _tube
from heirs_art6 import IVORY, LAPIS, TURQ

# ------------------------------------------------------------------ materials
RUBY = m("#9e1f2b", .08, 2, spec=.6, tint="#5a0e16")
RUBY_D = m("#5e1018", .10, 2)
SILVER = m("#c8ccd2", .05, 2, spec=1.3, tint="#6a7078")
STEEL = m("#8a9098", .06, 2, spec=1.1, tint="#4a5058")
STEEL_D = m("#4e545c", .08, 2, spec=.8)
GOLD_D = m("#9a7224", .10, 2, spec=.6)
CORNEL = m("#6e3e26", .14, 3, (1, 9), spec=.3)
WALNUT = m("#4a2a18", .14, 3, (9, 1), spec=.5)
WALNUT_V = m("#4a2a18", .14, 3, (1, 9), spec=.5)
BONE = m("#e6dcc0", .05, 2, spec=.6)
SILK = m("#a8202e", .06, 2, (1, 5), spec=.7, tint="#5a0a14")
SILK_D = m("#6e1420", .08, 2, (1, 5), spec=.5)
COTTON = m("#ece4d0", .05, 2)
INDIGO = m("#22305e", .08, 2)
LEAF = m("#2e5a2a", .12, 2)
CYPRESS = m("#1e3a24", .14, 2, spec=.2)
WATER = m("#3f7fa0", .04, 2, spec=1.4, tint="#1e4a66")
RICE = m("#f2ead6", .08, 1.2)
SAFFRON = m("#e2a21a", .06, 1.2, spec=.4)


# ================================================================== emblem
def _closed(pts, n=5):
    """A smooth closed outline through the control points."""
    p = list(pts) + list(pts[:3])
    out = _spline(p, n)
    return out[n:n * (len(pts) + 1)]


def _talons(c, x, y, ang, mat, s=1.0):
    """Three hooked eagle talons spreading from (x, y) towards angle `ang` (degrees)."""
    for k in (-1, 0, 1):
        a = math.radians(ang + k * 28)
        mid = (x + 5 * s * math.cos(a), y + 5 * s * math.sin(a))
        tip = (mid[0] + 3 * s * math.cos(a + 1.2), mid[1] + 3 * s * math.sin(a + 1.2))
        c.line(mat, 1.5 * s, (x, y), mid, tip)


def _griffin(c):
    """A rampant griffin in gold, facing left: lion body, eagle head with a tall ear and a spiky crest, a curled sickle wing."""
    gold_l = m("#e8c25a", .06, 2, spec=1.2, tint="#8a5a14")
    shadow = m("#3a0a10", .1, 2)
    # tail: an S-curve up behind the haunch with a tuft
    tail = _spline([(86, 92), (96, 88), (100, 76), (96, 64), (90, 58)], 6)
    _tube(c, GOLD, tail, 2.6, 1.4, bevel=.8)
    c.poly(GOLD_D, *_closed([(90, 58), (86, 52), (84, 58), (82, 62), (88, 63)], 3), bevel=.6)
    # far legs, darker and set back
    _tube(c, GOLD_D, _spline([(68, 86), (62, 96), (58, 104), (54, 106)], 5), 4.6, 2.6, bevel=1.0)
    _tube(c, GOLD_D, _spline([(52, 70), (44, 74), (36, 72)], 5), 3.8, 2.4, bevel=1.0)
    _talons(c, 36, 72, 180, GOLD_D)
    # wing behind the body: rises from the shoulder and curls forward at the top
    wing = _closed([(58, 58), (60, 44), (66, 32), (76, 22), (88, 17), (96, 20), (93, 25), (84, 26), (77, 33), (72, 44), (68, 56)], 5)
    c.poly(shadow, *[(x + 1.2, y + 1.6) for x, y in wing])
    c.poly(gold_l, *wing, bevel=1.6)
    for k in range(7):
        t = k / 6
        root = (62 + 6 * t, 58 - 2 * t)
        tip = (60 + 30 * t, 46 - 26 * t - 4 * math.sin(math.pi * t))
        c.line(GOLD_D, .9, root, tip, bevel=.2)
    for k in range(6):
        x, y = 64 + k * 4, 46 - k * 4.6
        c.scratch(.9, .55, (x - 2.4, y), (x, y + 2.2), (x + 2.4, y), color=(.45, .26, .04))
    # lion body
    body = _closed([(46, 48), (56, 46), (68, 56), (80, 68), (90, 82), (88, 94), (76, 98), (64, 88), (54, 76), (46, 62)], 6)
    c.poly(shadow, *[(x + 1.2, y + 1.6) for x, y in body])
    c.poly(GOLD, *body, bevel=2.2)
    for k in range(3):
        c.scratch(.8, .45, (56 + k * 5, 62 + k * 4), (52 + k * 5, 70 + k * 4), color=(.45, .28, .05))
    c.scratch(1.0, .4, (70, 78), (78, 84), (82, 92), color=(.45, .28, .05))
    # near hind leg: thigh, shin and paw planted on the ground line
    c.ell(gold_l, 78, 86, 10, 8, bevel=1.6)
    _tube(c, gold_l, _spline([(80, 90), (78, 100), (74, 106)], 5), 4.4, 3.0, bevel=1.2)
    c.ell(GOLD, 77, 107, 5.4, 2.8, bevel=.8)
    # near foreleg raised high, ending in talons
    _tube(c, gold_l, _spline([(50, 60), (42, 58), (36, 52), (34, 46)], 5), 4.6, 2.8, bevel=1.2)
    _talons(c, 34, 46, 225, GOLD_D, 1.1)
    # neck with a crest of spiky feathers down its back
    neck = _spline([(50, 52), (46, 42), (46, 32)], 5)
    for k in range(5):
        x, y = 51 - k * .6, 50 - k * 4.2
        c.poly(GOLD_D, (x, y), (x + 7, y - 3), (x + 1, y - 4), bevel=.5)
    _tube(c, GOLD, neck, 6.0, 5.0, bevel=1.4)
    # eagle head
    head = _closed([(48, 24), (52, 30), (50, 36), (44, 38), (38, 35), (37, 29), (42, 24)], 5)
    c.poly(GOLD, *head, bevel=1.6)
    beak = [(38, 28), (32, 28), (27, 31), (26, 36), (28, 38), (29, 35), (32, 33), (38, 34)]
    c.poly(gold_l, *beak, bevel=.9)
    c.line(RUBY_D, .8, (30, 33.5), (38, 31.5))
    c.poly(gold_l, (46, 25), (50, 11), (52, 26), bevel=.9)
    c.line(GOLD_D, .8, (49, 24), (50.5, 15))
    c.ell(RUBY_D, 42.5, 29, 2.2, 2.0)
    c.ell(m("#ffffff", .02), 41.8, 28.4, .6, .6)
    c.line(GOLD_D, 2.4, (54, 110), (96, 110))


EMBLEMS["griffin"] = _griffin


# ================================================================== weapons
_spear_long_prev = heirs_art6.spear_long


@painter
def spear_long(head="leaf", shaft="#6b4a2e", length=1.0):
    if head != "pomegranate":
        return _spear_long_prev(head=head, shaft=shaft, length=length)
    c = Canvas(128, seed=401)
    at, ln = axis((16, 116), (114, 10))
    haft(c, at, 6, ln - 22, 1.9, m(shaft, .14, 3, (1, 9), spec=.3))
    # the silver pomegranate counterweight with its little crown
    c.ell(m("#2a2018", .1), *at(3, 1), 6.2, 6.2)
    c.ell(SILVER, *at(3, 0), 6, 6, bevel=1.8)
    c.poly(SILVER, at(-4, -3), at(-7, -4), at(-6, 0), at(-7, 4), at(-4, 3), bevel=.6)
    c.ell(m("#ffffff", .02), *at(5, -2.4), 1.4, 1.2)
    for u in (12, 16, ln - 30):
        c.line(GOLD, 1.8, at(u, -2.3), at(u, 2.3))
    c.poly(STEEL, at(ln - 26, -2.6), at(ln - 18, -2.2), at(ln - 18, 2.2), at(ln - 26, 2.6), bevel=.8)
    leaf = [at(ln - 19, -2.0), at(ln - 13, -6.4), at(ln - 6, -5.0), at(ln, 0), at(ln - 6, 5.0), at(ln - 13, 6.4), at(ln - 19, 2.0)]
    c.poly(m("#b8c0c8", .05, 2, spec=1.3, tint="#5a6068"), *leaf, bevel=1.0)
    c.line(STEEL_D, 1.0, at(ln - 18, 0), at(ln - 2, 0), bevel=.3)
    c.glow(*at(ln - 10, -2), 10, "#ffffff", .2)
    return c.image()


@painter
def akinakes():
    """A short straight sword: griffin-head pommel bar, gold-wrapped grip, heart-shaped guard and a tapering double-edged blade."""
    c = Canvas(128, seed=402)
    at, ln = axis((26, 108), (108, 24))
    # pommel: a crosswise bar ending in two small griffin heads
    c.poly(GOLD, at(-2, -9), at(3, -9), at(3, 9), at(-2, 9), bevel=1.0)
    for s in (-1, 1):
        c.ell(GOLD, *at(0.5, s * 10), 3.4, 3.4, bevel=1.0)
        c.poly(GOLD_D, at(-1, s * 12), at(-4, s * 14.5), at(1, s * 13), bevel=.4)
        c.ell(RUBY_D, *at(1.4, s * 10.4), .9, .9)
    haft(c, at, 3, 22, 3.0, WALNUT, bevel=1.0)
    for u in range(5, 22, 3):
        c.line(GOLD, 1.0, at(u, -3.0), at(u + 1.5, 3.0))
    # heart-shaped guard: two lobes pointing down the blade
    guard = [at(21, -7), at(25, -8.5), at(30, -6), at(34, 0), at(30, 6), at(25, 8.5), at(21, 7)]
    c.poly(GOLD, *guard, bevel=1.2)
    c.line(GOLD_D, 1.0, at(23, 0), at(32, 0))
    c.ell(RUBY, *at(26, 0), 2.0, 2.0, bevel=.6)
    blade = [at(33, -4.2), at(ln - 10, -2.6), at(ln, 0), at(ln - 10, 2.6), at(33, 4.2)]
    c.poly(m("#c2c8d0", .05, 2, spec=1.4, tint="#5a6068"), *blade, bevel=1.2)
    c.line(m("#7a8088", .06), 1.1, at(34, 0), at(ln - 6, 0), bevel=.3)
    c.line(m("#f4f6fa", .03, spec=1.5), .8, at(34, -3.4), at(ln - 10, -2))
    c.glow(*at(ln - 26, -1), 12, "#ffffff", .2)
    return c.image()


@painter
def recurve_bow():
    """The Parsian bow, braced: limbs bulge away from the string, bend back to meet it and flick outward in bone ears."""
    c = Canvas(128, seed=403)
    sx = 66
    ctrl = [(56, 64), (48, 52), (42, 38), (43, 25), (51, 15), (62, 10)]
    top = _spline(ctrl, 5)
    ear = _spline([(62, 10), (60, 5), (52, 3)], 4)
    shade_mat = m("#3a1a10", .12, 2)
    c.line(m("#efe6cc", .04), 1.1, (sx, 12), (sx, 116))
    for flip in (False, True):
        fy = (lambda p: (p[0], 128 - p[1])) if flip else (lambda p: p)
        limb = [fy(p) for p in top]
        tip = [fy(p) for p in ear]
        _tube(c, shade_mat, [(x + 1, y + 1.4) for x, y in limb], 4.8, 3.0, bevel=.4)
        _tube(c, RUBY, limb, 4.6, 2.8, bevel=1.6)
        _tube(c, m("#d24a52", .04, 2, spec=1.2), [(x - 1.6, y - .4) for x, y in limb[2:-4]], 1.0, .6, bevel=.3)
        _tube(c, BONE, tip, 2.8, 1.4, bevel=.8)
        for k in (5, 11, 17, 23):
            x, y = limb[k]
            xb, yb = limb[k + 1]
            nx, ny = -(yb - y), xb - x
            ln = math.hypot(nx, ny) or 1
            nx, ny = nx / ln * 5.2, ny / ln * 5.2
            c.line(GOLD, 1.8, (x - nx, y - ny), (x + nx, y + ny))
    c.rect(m("#2a1a10", .1, 1.5, (4, 1)), 50, 55, 62, 73, 3, bevel=1.2)
    for y in (55, 73):
        c.line(GOLD, 2.0, (49, y), (63, y))
    c.poly(BONE, (62, 62), (66, 64), (62, 66), bevel=.4)
    c.glow(44, 36, 14, "#ffe0e0", .14)
    return c.image()


@painter
def jezail():
    """A very long flintlock: deeply curved walnut stock studded with bone and brass, many barrel bands."""
    c = Canvas(128, seed=404)
    at, ln = axis((6, 104), (124, 20))
    stock = [at(0, -2), at(8, -3), at(20, -3.4), at(34, -2.4), at(34, 3), at(22, 5), at(12, 9), at(4, 14), at(-2, 15), at(-3, 8)]
    c.poly(WALNUT, *stock, bevel=1.6)
    c.poly(BONE, at(-3, 8), at(-2, 15), at(1, 14.6), at(0, 7.8), bevel=.6)
    rng = np.random.default_rng(44)
    for k in range(9):
        u = 4 + k * 3.2
        v = rng.uniform(-1.4, 2.6) + max(0, 8 - u) * .6
        c.ell(BONE if k % 2 else BRASS, *at(u, v), 1.1, 1.1, bevel=.4)
    c.line(BRASS, 1.0, at(6, 6), at(30, 1))
    c.poly(m("#3e4246", .08, 3, (9, 1), spec=1.0), at(30, -1.6), at(ln, -1.3), at(ln, 1.3), at(30, 1.6), bevel=.8)
    c.poly(m("#3a2216", .14, 3, (9, 1)), at(34, -.6), at(ln - 14, -.4), at(ln - 14, 2.8), at(34, 3.0), bevel=.8)
    for u in range(42, int(ln) - 8, 9):
        c.line(BRASS, 1.6, at(u, -2.0), at(u, 3.2))
    c.poly(m("#5a5e62", .08, 2, spec=.9), at(28, -3.2), at(40, -3.2), at(40, 3.6), at(28, 3.6), bevel=1.0)
    c.line(DARKIRON, 1.6, at(33, -3), at(30, -7.5), at(34, -8.5))
    c.poly(m("#7a7e82", .06), at(37, -3.2), at(39, -6.5), at(41, -3.2), bevel=.4)
    c.line(DARKIRON, 1.4, at(30, 3.6), at(29, 7), at(24, 7.4))
    c.poly(BRASS, at(ln - 3, -1.8), at(ln, -1.8), at(ln, 1.8), at(ln - 3, 1.8), bevel=.5)
    c.line(m("#b8bcc0", .04, spec=1.2), .7, at(44, -1.0), at(ln - 6, -.9))
    return c.image()


# ================================================================== apparel icons
@painter
def torso4(kind="kaftan"):
    c = Canvas(128, seed=405)
    if kind == "kaftan":
        # a long open coat: wide sleeves, ivory tunic showing at the front, gold-embroidered hems and a gold sash
        for s in (-1, 1):
            sleeve = [(64 + s * 22, 24), (64 + s * 44, 38), (64 + s * 54, 70), (64 + s * 46, 76), (64 + s * 34, 52), (64 + s * 26, 46)]
            c.poly(SILK_D, *sleeve, bevel=1.8)
            c.line(GOLD, 2.2, (64 + s * 54, 70), (64 + s * 46, 76))
        c.poly(COTTON, (56, 26), (72, 26), (76, 120), (52, 120), bevel=1.2)
        for y in range(34, 118, 8):
            c.scratch(.6, .3, (58, y), (70, y + 1), color=(.6, .55, .45))
        for s in (-1, 1):
            panel = [(64 + s * 6, 22), (64 + s * 24, 22), (64 + s * 30, 60), (64 + s * 36, 120), (64 + s * 10, 120), (64 + s * 6, 60)]
            c.poly(SILK, *panel, bevel=2.2)
            for k in range(6):
                x = 64 + s * (14 + k * 3.4)
                c.scratch(.9, .3, (x, 64), (x + s * 2, 118), color=(.3, .02, .05))
            edge = [(64 + s * 6, 22), (64 + s * 6, 60), (64 + s * 10, 120)]
            c.line(GOLD, 3.2, *edge, bevel=.6)
            for t in np.linspace(.05, .95, 9):
                x = 64 + s * (6 + 4 * max(0, (t - .3) / .7))
                y = 22 + 98 * t
                c.ell(TURQ if int(t * 9) % 2 else RUBY_D, x, y, 1.3, 1.3, bevel=.4)
            c.line(GOLD, 3.0, (64 + s * 10, 119), (64 + s * 36, 119))
            for x in range(14, 36, 5):
                c.poly(GOLD_D, (64 + s * x, 116), (64 + s * (x + 2.5), 113), (64 + s * (x + 5), 116), bevel=.3)
        c.rect(GOLD, 38, 62, 90, 70, 2, bevel=1.2)
        c.line(m("#b88a2a", .05), 1.0, (40, 66), (88, 66))
        c.poly(GOLD, (70, 70), (74, 90), (78, 88), (75, 70), bevel=.8)
        c.ell(RUBY, 64, 66, 3.4, 3.4, bevel=.8)
        c.glow(48, 40, 22, "#ffd8d8", .14)
    elif kind == "scalecoat":
        # knee-length coat of small iron scales with brass rows, short sleeves and a red leather belt
        leather = m("#4a2a1a", .12, 2)
        coat = [(36, 18), (52, 16), (64, 26), (76, 16), (92, 18), (106, 34), (100, 48), (94, 44), (96, 120), (32, 120), (34, 44), (28, 48), (22, 34)]
        c.poly(leather, *coat, bevel=2.2)
        tints = [STEEL, STEEL, m("#9aa0a8", .06, 2, spec=1.2, tint="#4a5058"), m("#70767e", .06, 2, spec=.9)]
        rng = np.random.default_rng(45)
        for row in range(16, -1, -1):
            y = 18 + row * 6
            brass_row = row in (5, 11)
            for i in range(-2, 16):
                x = 22 + i * 5.6 + (row % 2) * 2.8
                sc = [(x - 2.7, y), (x + 2.7, y), (x + 2.7, y + 5), (x, y + 7.6), (x - 2.7, y + 5)]
                c.poly(m("#1a1410", .1), *[(px + .4, py + 1) for px, py in sc], bevel=0, clip=True)
                c.poly(BRASS if brass_row else tints[rng.integers(0, 4)], *sc, bevel=.8, clip=True)
        c.poly(leather, (52, 16), (64, 30), (76, 16), (70, 16), (64, 24), (58, 16), bevel=1.0)
        c.rect(RUBY, 30, 64, 98, 72, 2, bevel=1.2)
        c.ell(GOLD, 64, 68, 4.4, 3.6, bevel=1.0)
        for x in range(36, 96, 8):
            c.ell(GOLD, x, 68, 1.2, 1.2, bevel=.4)
        c.line(RUBY_D, 2.0, (32, 119), (96, 119))
        c.glow(50, 36, 24, "#e8f0ff", .18)
    return c.image()


@painter
def helmet4(kind="winged"):
    c = Canvas(128, seed=406)
    if kind == "winged":
        gold_l = m("#e8c25a", .06, 2, spec=1.2, tint="#8a5a14")
        # mail curtain: fine riveted rings with a scalloped lower edge
        mail = [(36, 70), (92, 70), (96, 96)] + [(92 - k * 7, 100 + (k % 2) * 4) for k in range(9)] + [(32, 96)]
        c.poly(m("#2a2e34", .1, 2), *mail, bevel=1.2)
        for row in range(9):
            y = 72 + row * 3.4
            for k in range(22):
                x = 33 + k * 3.0 + (row % 2) * 1.5
                c.ell(m("#a8aeb6", .05, spec=1.0), x, y, 1.5, 1.3, bevel=.3, clip=True)
                c.ell(m("#1a1e24", .05), x, y + .2, .6, .5, clip=True)
        # tall pointed bowl, fluted, with a gold ridge and finial
        bowl = _closed([(34, 74), (35, 58), (42, 42), (53, 26), (64, 8), (75, 26), (86, 42), (93, 58), (94, 74)], 5)
        c.poly(STEEL, *bowl, bevel=2.8)
        for k in range(-4, 5):
            if k:
                c.scratch(.9, .35, (64 + k * .8, 12), (64 + k * 7, 70), color=(.2, .22, .26))
        c.line(GOLD, 2.4, (64, 10), (64, 68))
        c.ell(GOLD, 64, 8, 3.2, 3.2, bevel=1.0)
        c.glow(52, 40, 16, "#ffffff", .3)
        c.rect(GOLD, 32, 64, 96, 74, 2, bevel=1.4)
        for x in range(36, 94, 6):
            c.ell(RUBY if (x // 6) % 2 else TURQ, x, 69, 1.6, 1.6, bevel=.5)
        # gilded wings on both temples: a fan of tapered feathers sweeping up and out
        for s in (-1, 1):
            root = (64 + s * 30, 64)
            for k in range(6, -1, -1):
                a = math.radians(-90 + s * (14 + k * 11))
                ln = 34 - k * 2.4
                tip = (root[0] + ln * math.cos(a), root[1] + ln * math.sin(a))
                dx, dy = tip[0] - root[0], tip[1] - root[1]
                nx, ny = -dy / ln, dx / ln
                w = 3.4
                mid = (root[0] + dx * .55, root[1] + dy * .55)
                c.poly(gold_l if k % 2 else GOLD, (root[0] + nx * 2, root[1] + ny * 2), (mid[0] + nx * w, mid[1] + ny * w), tip,
                       (mid[0] - nx * w, mid[1] - ny * w), (root[0] - nx * 2, root[1] - ny * 2), bevel=.9)
                c.scratch(.6, .45, root, (root[0] + dx * .85, root[1] + dy * .85), color=(.5, .32, .06))
            c.ell(GOLD, *root, 4.2, 4.2, bevel=1.2)
            c.ell(RUBY, *root, 2.2, 2.2, bevel=.6)
    return c.image()


@painter
def pars_garden(size=(2, 2)):
    """A walled chahar bagh from above: four flower beds split by water channels, a central pool and cypresses in the corners."""
    W = 256
    c = Canvas(W, W, seed=407)
    wall = m("#c9a878", .12, 2.5)
    c.rect(m("#2a2018", .1), 10, 12, W - 4, W - 2, 8)
    c.rect(wall, 4, 4, W - 8, W - 8, 8, bevel=2.4)
    c.rect(m("#a8845a", .12, 2.5), 16, 16, W - 20, W - 20, 4, bevel=1.0)
    rng = np.random.default_rng(47)
    beds = [(20, 20, 116, 116), (136, 20, W - 24, 116), (20, 136, 116, W - 24), (136, 136, W - 24, W - 24)]
    for x0, y0, x1, y1 in beds:
        c.rect(m("#4a6a2e", .14, 2), x0, y0, x1, y1, 4, bevel=1.4)
        for _ in range(26):
            x, y = rng.uniform(x0 + 8, x1 - 8), rng.uniform(y0 + 8, y1 - 8)
            r = rng.uniform(5, 8)
            c.ell(m("#2a3e1a", .1), x + 1.5, y + 2, r, r)
            c.ell(LEAF, x, y, r, r, bevel=1.4)
            for _k in range(rng.integers(2, 5)):
                a, d = rng.uniform(0, 6.3), rng.uniform(0, r * .6)
                col = ("#c8283a", "#e65a6a", "#f2d6dc", "#e8b82a")[rng.integers(0, 4)]
                c.ell(m(col, .04, spec=.6), x + d * math.cos(a), y + d * math.sin(a), 1.8, 1.8, bevel=.5)
    tile = m("#3a8a9a", .06, 2, spec=.8)
    for a, b in (((116, 16), (136, W - 20)), ((16, 116), (W - 20, 136))):
        c.rect(tile, *a, *b, 1, bevel=.8)
    c.rect(WATER, 122, 20, 130, W - 24, 1, bevel=.6)
    c.rect(WATER, 20, 122, W - 24, 130, 1, bevel=.6)
    for k in range(20, W - 24, 10):
        c.scratch(.6, .5, (124, k), (128, k + 4), color=(.8, .9, 1))
        c.scratch(.6, .5, (k, 124), (k + 4, 128), color=(.8, .9, 1))
    pts = [(126 + 26 * math.cos(math.pi / 8 + k * math.pi / 4), 126 + 26 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    c.poly(m("#e6dcc8", .05, 2), *pts, bevel=1.8)
    pts = [(126 + 20 * math.cos(math.pi / 8 + k * math.pi / 4), 126 + 20 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    c.poly(WATER, *pts, bevel=1.4)
    for r in (6, 11, 15):
        ring(c, 126, 126, r, m("#9ac8dc", .03), .8)
    c.ell(m("#e6dcc8", .05), 126, 126, 4, 4, bevel=1.0)
    c.glow(126, 126, 18, "#e8f8ff", .4)
    for x, y in ((30, 30), (W - 34, 30), (30, W - 34), (W - 34, W - 34)):
        c.ell(m("#14201a", .1), x + 4, y + 6, 13, 13)
        c.ell(CYPRESS, x, y, 12, 12, bevel=2.4)
        c.ell(m("#2e5a36", .12, spec=.3), x - 3, y - 3, 6, 6, bevel=1.4)
    return c.image()


@painter
def post_lamp(size=(1, 1)):
    """A tall post with a pierced bronze lantern under a little dome, drawn 1x1.6 cells high."""
    c = Canvas(128, 205, seed=408)
    c.ell(m("#2a2018", .1), 68, 194, 26, 7)
    c.rect(STONE_D, 46, 178, 82, 196, 3, bevel=1.6)
    c.rect(CORNEL, 59, 70, 69, 182, 2, bevel=1.2)
    for y in (90, 140):
        c.rect(BRONZE, 57, y, 71, y + 5, 1, bevel=.8)
    c.line(BRONZE, 2.4, (64, 70), (64, 58))
    c.rect(BRONZE, 42, 52, 86, 58, 2, bevel=1.0)
    c.rect(m("#2a1a10", .1), 44, 22, 84, 52, 3)
    lit = m("#ffcf6a", .04, 2, spec=.3)
    c.rect(lit, 46, 24, 82, 50, 2)
    c.glow(64, 38, 40, "#ffb050", .55)
    for col in range(4):
        for row in range(3):
            x, y = 50 + col * 9, 28 + row * 8
            c.poly(BRONZE, (x - 3, y), (x, y - 3), (x + 3, y), (x, y + 3), bevel=.4)
    for x in (44, 84):
        c.rect(BRONZE, x - 2, 22, x + 2, 52, 1, bevel=.8)
    c.poly(BRONZE, (40, 24), (48, 12), (64, 6), (80, 12), (88, 24), bevel=1.6)
    c.ell(GOLD, 64, 5, 3, 3, bevel=.8)
    return _halo(c.image(), (255, 190, 110, 255), 6, .6)


@painter
def carpet_loom(size=(2, 1)):
    """An upright loom seen from above-front: beam, warp threads, a half-woven carpet, wool balls and the weaver's bench."""
    W, H = 256, 128
    c = Canvas(W, H, seed=409)
    c.rect(m("#2a2018", .1), 12, 16, W - 6, H - 4, 8)
    for x in (14, W - 30):
        c.rect(WALNUT_V, x, 6, x + 14, H - 14, 3, bevel=1.6)
    c.rect(WALNUT, 10, 6, W - 12, 18, 4, bevel=1.8, cyl=(6, 18))
    c.rect(WALNUT, 10, H - 26, W - 12, H - 14, 4, bevel=1.6, cyl=(H - 26, H - 14))
    for x in range(32, W - 32, 3):
        c.line(m("#efe6d0", .04), .7, (x, 18), (x, 70))
    c.rect(RUBY, 32, 66, W - 34, H - 26, 1, bevel=1.0)
    c.rect(INDIGO, 36, 70, W - 38, H - 30, 1, bevel=.6)
    c.rect(RUBY, 42, 74, W - 44, H - 30, 1, bevel=.6)
    for x in range(48, W - 48, 16):
        c.poly(m("#ece0c4", .05), (x, 82), (x + 6, 76), (x + 12, 82), (x + 6, 88), bevel=.5)
        c.ell(INDIGO, x + 6, 82, 1.6, 1.6)
    c.poly(m("#e8c25a", .06), (110, 96), (128, 84), (146, 96), (128, H - 30), bevel=.6)
    c.line(m("#3a2216", .1), 2.4, (30, 66), (W - 32, 66))
    for k, col in enumerate(("#9e1f2b", "#22305e", "#e8c25a", "#ece0c4", "#2e5a2a", "#c86a2a")):
        x = 46 + k * 30
        c.line(m("#efe6d0", .04), .8, (x, 18), (x, 30))
        c.ell(m(col, .1, 1.5), x, 34, 6, 5, bevel=1.4)
        c.scratch(.6, .4, (x - 4, 32), (x + 4, 36))
    c.rect(m("#6a4428", .14, 3, (9, 1)), 70, H - 12, 186, H - 2, 3, bevel=1.4)
    return c.image()


# ================================================================== floor
@painter
def floor_girih():
    """Star-and-cross glazed tiles: turquoise eight-pointed stars, cobalt crosses and white grout; tiles every 256 pixels."""
    base = (34, 58, 128)
    img, d, rng = floor_canvas(base, 411)
    cell = 256
    s = cell * .5
    for i in range(-1, 5):
        for j in range(-1, 5):
            cx, cy = i * cell + cell / 2, j * cell + cell / 2
            star = []
            for k in range(16):
                a = math.pi / 8 * k
                r = s * (1.0 if k % 2 == 0 else .74)
                star.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            d.polygon(star, fill=(236, 232, 220))
            inner = [(cx + (px - cx) * .9, cy + (py - cy) * .9) for px, py in star]
            col = shade((52, 156, 150), 1 + rng.uniform(-.06, .06))
            d.polygon(inner, fill=col)
            core = []
            for k in range(16):
                a = math.pi / 8 * k + math.pi / 16
                r = s * (.36 if k % 2 == 0 else .26)
                core.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            d.polygon(core, fill=(236, 232, 220))
            d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=(196, 150, 60))
            for k in range(8):
                a = math.pi / 4 * k
                d.line((cx + 20 * math.cos(a), cy + 20 * math.sin(a), cx + s * .7 * math.cos(a), cy + s * .7 * math.sin(a)),
                       fill=(30, 100, 100), width=5)
    for _ in range(2200):
        x, y = rng.uniform(0, 1024), rng.uniform(0, 1024)
        d.line((x, y, x + rng.uniform(-6, 6), y + rng.uniform(-6, 6)), fill=shade(base, rng.uniform(.8, 1.3)), width=1)
    return finish_floor(img, 411, 2.0)


# ================================================================== food, goods and relics
@painter
def food4(kind="pilaf"):
    c = Canvas(128, seed=413)
    if kind == "pilaf":
        c.ell(m("#2a2018", .1), 66, 86, 56, 26)
        c.ell(m("#f2f0ea", .04, 2, spec=.8), 64, 80, 56, 28, bevel=2.4)
        c.ell(m("#2a4a9a", .05), 64, 80, 50, 24.5)
        c.ell(m("#f2f0ea", .04, 2, spec=.8), 64, 80, 47.5, 22.8, bevel=1.0)
        for k in range(16):
            a = k * 2 * math.pi / 16
            c.ell(m("#2a4a9a", .05), 64 + 52 * math.cos(a), 80 + 25 * math.sin(a), 1.6, 1.2)
        for x, y in ((30, 86), (96, 90), (40, 96)):
            c.poly(m("#b8761a", .1, 2, spec=.6), (x - 9, y), (x - 4, y - 6), (x + 9, y - 4), (x + 6, y + 4), bevel=1.2)
        c.ell(m("#b8a880", .08), 64, 74, 38, 22)
        c.ell(RICE, 64, 68, 37, 24, bevel=3.2)
        rng = np.random.default_rng(14)
        for _ in range(140):
            a, r = rng.uniform(0, 6.3), rng.uniform(0, 1) ** .5
            x, y = 64 + 34 * r * math.cos(a), 68 + 21 * r * math.sin(a)
            c.line(m("#ffffff", .02), 1.0, (x - 1.4, y), (x + 1.4, y + rng.uniform(-.6, .6)))
        c.ell(SAFFRON, 60, 58, 20, 11, bevel=1.6)
        for _ in range(40):
            a, r = rng.uniform(0, 6.3), rng.uniform(0, 1) ** .5
            c.line(m("#f6c23a", .03), 1.0, (60 + 18 * r * math.cos(a), 58 + 10 * r * math.sin(a)),
                   (61.5 + 18 * r * math.cos(a), 58.3 + 10 * r * math.sin(a)))
        for _ in range(18):
            a, r = rng.uniform(0, 6.3), rng.uniform(.2, 1)
            c.ell(m("#c41a2a", .04, spec=1.2), 64 + 30 * r * math.cos(a), 66 + 16 * r * math.sin(a), 1.7, 1.5, bevel=.5)
        for _ in range(12):
            a, r = rng.uniform(0, 6.3), rng.uniform(.1, .9)
            x, y = 64 + 28 * r * math.cos(a), 64 + 14 * r * math.sin(a)
            c.line(m("#7aa63a", .05), 1.4, (x, y), (x + 2.6, y - 1.2))
        c.glow(52, 52, 16, "#fff6e0", .3)
    return c.image()


@painter
def goods4(kind="carpet"):
    c = Canvas(128, seed=414)
    if kind == "carpet":
        flat = [(12, 76), (82, 52), (118, 78), (46, 108)]
        c.poly(m("#2a1810", .1), *[(x + 2, y + 4) for x, y in flat])
        c.poly(RUBY, *flat, bevel=1.6)

        def lerp(p, q, t):
            return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

        def quad(t0, t1):
            a, b, cc, dd = flat
            return [lerp(lerp(a, dd, t0), lerp(b, cc, t0), t0), lerp(lerp(a, dd, t0), lerp(b, cc, t0), t1),
                    lerp(lerp(a, dd, t1), lerp(b, cc, t1), t1), lerp(lerp(a, dd, t1), lerp(b, cc, t1), t0)]

        c.poly(INDIGO, *quad(.08, .92), bevel=.6)
        c.poly(RUBY, *quad(.14, .86), bevel=.6)
        for t in np.linspace(.11, .89, 12):
            a, b, cc, dd = flat
            p = lerp(lerp(a, dd, .11), lerp(b, cc, .11), t)
            q = lerp(lerp(a, dd, .89), lerp(b, cc, .89), t)
            c.ell(m("#e8c25a", .05), *p, 1.3, 1.0)
            c.ell(m("#e8c25a", .05), *q, 1.3, 1.0)
        mx, my = 65, 79
        c.poly(m("#ece0c4", .05), (mx - 20, my), (mx, my - 10), (mx + 20, my), (mx, my + 10), bevel=.8)
        c.poly(INDIGO, (mx - 13, my), (mx, my - 6.5), (mx + 13, my), (mx, my + 6.5), bevel=.6)
        c.ell(RUBY, mx, my, 4, 2.4, bevel=.5)
        for k in range(8):
            x = 46 + k * 4.4
            c.line(m("#ece0c4", .04), .9, (x, 108 - k * 3.3), (x - 1.5, 113 - k * 3.3))
        # the far end is rolled up
        roll_a, roll_b = (12, 70), (82, 46)
        c.line(m("#2a1810", .1), 15, (13, 74), (83, 50))
        c.line(RUBY, 14, roll_a, roll_b, bevel=2.4)
        c.line(INDIGO, 2.2, (14, 64), (84, 40))
        c.line(m("#e8c25a", .05), 1.2, (12, 76), (82, 52))
        c.ell(RUBY_D, 12, 70, 5, 7, bevel=1.0)
        ring(c, 12, 70, 3.4, INDIGO, 1.0)
        c.glow(70, 60, 22, "#ffe0e0", .12)
    return c.image()


def _eye(c, cx, cy, s, gold, lapis, ivory, wing):
    """An almond eye in a winged frame, centred at (cx, cy), scale s."""
    for side in (-1, 1):
        for k in range(5):
            tip = (cx + side * s * (40 - k * 3), cy - s * (14 - k * 7))
            root = (cx + side * s * 16, cy - s * (2 - k * 2))
            c.poly(wing if k % 2 else gold, root, (tip[0], tip[1] - s * 3), (tip[0] + side * s * 3, tip[1] + s * 3),
                   (root[0], root[1] + s * 5), bevel=.8)
    almond = [(cx - s * 22, cy), (cx - s * 10, cy - s * 11), (cx + s * 10, cy - s * 11), (cx + s * 22, cy),
              (cx + s * 10, cy + s * 11), (cx - s * 10, cy + s * 11)]
    c.poly(gold, *almond, bevel=1.8)
    inner = [(cx - s * 17, cy), (cx - s * 8, cy - s * 7.5), (cx + s * 8, cy - s * 7.5), (cx + s * 17, cy),
             (cx + s * 8, cy + s * 7.5), (cx - s * 8, cy + s * 7.5)]
    c.poly(ivory, *inner, bevel=1.0)
    c.ell(lapis, cx, cy, s * 7, s * 7, bevel=1.4)
    c.ell(m("#0e1020", .05), cx, cy, s * 3, s * 3)


@painter
def relic4(kind="eye"):
    c = Canvas(128, seed=415)
    if kind == "eye":
        soot = m("#5a4a2e", .16, 2, spec=.3, tint="#2a2214")
        soot_l = m("#7a6640", .14, 2, spec=.3)
        c.ell(m("#2a2018", .1), 66, 70, 46, 20)
        _eye(c, 64, 60, 1.25, soot, m("#2a3450", .12, 2), m("#a89a80", .12, 2), soot_l)
        rng = np.random.default_rng(16)
        for _ in range(40):
            x, y = rng.uniform(20, 108), rng.uniform(40, 80)
            c.ell(m("#14100a", .1), x, y, rng.uniform(1, 3), rng.uniform(.8, 2))
        c.glow(50, 52, 10, "#fff0c0", .25)
        ash = m("#6a6460", .2, 2)
        c.poly(ash, (14, 112), (34, 96), (60, 102), (84, 92), (114, 100), (120, 118), (10, 120), bevel=2.0)
        for x in range(20, 116, 7):
            c.scratch(.8, .35, (x, 106), (x + 4, 104), color=(.2, .2, .2))
    return c.image()


@painter
def kings_eye():
    """The King's Eye restored: polished gold eye with a lapis iris in a winged frame, set on the head of a short staff."""
    c = Canvas(128, seed=416)
    c.rect(WALNUT_V, 61, 70, 67, 124, 2, bevel=1.2)
    for y in (84, 104, 120):
        c.rect(GOLD, 59, y, 69, y + 4, 1, bevel=.8)
    c.ell(GOLD, 64, 70, 6, 5, bevel=1.4)
    _eye(c, 64, 46, 1.35, GOLD, LAPIS, IVORY, m("#e8c25a", .06, 2, spec=1.2))
    for x in (34, 94):
        c.ell(RUBY, x, 52, 2.6, 2.6, bevel=.8)
    c.ell(m("#ffffff", .02), 61, 43, 2, 1.6)
    c.glow(56, 38, 20, "#fff6d0", .45)
    return _halo(c.image(), (255, 214, 120, 255), 8, .9)
