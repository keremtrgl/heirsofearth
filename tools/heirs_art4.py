"""Heirs of Earth 2.0 painters: Hellas, Tianxia and Albion.

Emblems (owl, dragon, lion), weapons, armour icons, buildings, floors, food, trade goods, relics and artifacts.
Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module after heirs_art2/3,
so the wrapped painters (table, spear_long, relic) take over their old names and fall back to the old kinds.
"""
import math

import numpy as np
from PIL import Image

import heirs_art2
import heirs_art3
from heirs_art import (BRONZE, DARKIRON, EMBLEMS, GOLD, IRON, LEATHER, LEATHER_D, MARBLE, STEEL, STONE, STONE_D, STONE_L, WOOD,
                       WOOD_D, WOOD_V, Canvas, axis, blade, finish_floor, floor_canvas, haft, m, painter, shade, wraps)
from heirs_art2 import CERAMIC, LACQUER, LACQUER_R, ring
from heirs_art3 import _halo

# ------------------------------------------------------------------ materials
LINEN = m("#e9e1cc", .06, 2)
LINEN_D = m("#cbbf9f", .08, 2)
HELLAS_BLUE = m("#2e5c8c", .08, 2)
OLIVE = m("#6d7a3a", .12, 2)
HORSEHAIR = m("#8e2a24", .16, 1.5, (1, 5))
HORSEHAIR_D = m("#2a1c18", .16, 1.5, (1, 5))
JADE = m("#3f8a63", .12, 2, spec=.9, tint="#2a5e45")
JADE_L = m("#7cc29a", .08, 2, spec=1.0)
IMP_RED = m("#9c2a20", .08, 2, tint="#6e1a14")
SILK_GOLD = m("#d9a93a", .06, 2, spec=.8)
PORCELAIN = m("#eef1f2", .03, 2, spec=1.0)
COBALT = m("#28468c", .06, 2)
BAMBOO = m("#b9a35a", .10, 2, (1, 6))
YIXING = m("#7a3e26", .10, 2, spec=.5)
PAPER_RED = m("#c8322a", .06, 2, tint="#a01e18")
COAT_RED = m("#a51e22", .08, 2, tint="#7a1418")
FACING = m("#efe9da", .04, 2)
BRASS = m("#c9a24a", .08, 2, spec=1.1, tint="#9a7a2a")
FELT = m("#1c1c22", .08, 2, spec=.2)
OAK = m("#7a5634", .16, 3, (9, 1))
OAK_V = m("#7a5634", .16, 3, (1, 9))
PEWTER = m("#9ea4a6", .06, 2, spec=.9)
CRUST = m("#c98a3a", .12, 2, tint="#9a5a22")
CHEESE = m("#efdc9a", .06, 2)
DOUGH = m("#efe6d0", .05, 2, spec=.2)
BARLEY = m("#c9a25e", .14, 2)
TEA_DARK = m("#3a2418", .14, 2)
TWEED = m("#6a6a4e", .16, 1.2)
CEDAR = m("#8a4e2e", .16, 3, (9, 1))
PARCH = m("#e2d3ae", .06, 2)
DRUM_SKIN = m("#e9dfc4", .05, 2)
SMOKE = m("#3a3a3e", .1, 2)


class _At:
    """Draws an emblem function (written for the shield at centre 64,56) scaled and moved onto another canvas."""

    def __init__(self, c, s=1.0, cx=64.0, cy=56.0):
        self.c, self.s, self.cx, self.cy = c, s, cx, cy

    def _p(self, pts):
        return [(self.cx + (x - 64) * self.s, self.cy + (y - 56) * self.s) for x, y in pts]

    def poly(self, mt, *pts, **kw):
        return self.c.poly(mt, *self._p(pts), **kw)

    def ell(self, mt, x, y, rx, ry, **kw):
        (px, py), = self._p([(x, y)])
        return self.c.ell(mt, px, py, rx * self.s, ry * self.s, **kw)

    def line(self, mt, w, *pts, **kw):
        return self.c.line(mt, w * self.s, *self._p(pts), **kw)

    def scratch(self, w, o, *pts, **kw):
        return self.c.scratch(w * self.s, o, *self._p(pts), **kw)

    def glow(self, x, y, r, color="#ffb648", strength=.8):
        (px, py), = self._p([(x, y)])
        return self.c.glow(px, py, r * self.s, color, strength)


def _spline(pts, n=8):
    """Catmull-Rom points through the given control points."""
    out = []
    p = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                   + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(pts[-1])
    return out


def _tube(c, mat, pts, w0, w1, bevel=1.6):
    """A tapering tube along a polyline: one polygon with smooth sides."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        xa, ya = pts[max(0, i - 1)]
        xb, yb = pts[min(n - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    c.poly(mat, *(left + right[::-1]), bevel=bevel)
    return left, right


# ================================================================== emblems
def _owl(c):
    """The owl of the league: front-facing, wings folded, perched on an olive branch."""
    body = m("#e8e2d0", .06, 2)
    wing = m("#c9c0a8", .08, 2)
    c.line(m("#5a3e26", .12), 3.2, (34, 98), (64, 95), (94, 98))
    for x, y, a in ((40, 92, -1), (50, 101, 1), (80, 92, -1), (90, 101, 1)):
        c.ell(OLIVE, x, y, 4.5, 2.2, bevel=.8)
    c.poly(wing, (48, 50), (40, 66), (42, 84), (52, 96), (58, 74), bevel=1.4)
    c.poly(wing, (80, 50), (88, 66), (86, 84), (76, 96), (70, 74), bevel=1.4)
    c.ell(body, 64, 70, 17, 25, bevel=1.8)
    for row, y in enumerate((60, 68, 76, 84)):
        for x in range(54 + (row % 2) * 3, 76, 6):
            c.scratch(.8, .4, (x - 2.2, y - 1.5), (x, y), (x + 2.2, y - 1.5), color=(.45, .4, .32))
    c.poly(body, (48, 30), (52, 20), (58, 30), bevel=1.0)
    c.poly(body, (80, 30), (76, 20), (70, 30), bevel=1.0)
    c.ell(body, 64, 40, 18, 15, bevel=1.8)
    for x in (57, 71):
        c.ell(m("#f7f3e6", .03), x, 40, 7.5, 7.5, bevel=1.2)
        c.ell(GOLD, x, 40, 4.4, 4.4, bevel=.8)
        c.ell(m("#141210", .05), x, 40, 2.2, 2.2)
        c.ell(m("#ffffff", .02), x - 1.2, 38.8, .8, .8)
    c.poly(GOLD, (64, 44), (61, 48), (64, 54), (67, 48), bevel=.8)
    for x in (58, 70):
        c.line(GOLD, 1.6, (x, 93), (x - 2, 97))
        c.line(GOLD, 1.6, (x, 93), (x + 2, 97))


def _dragon(c):
    """A coiled imperial dragon: S-shaped body with spines, two clawed legs and a horned head."""
    gold, gold_d = GOLD, m("#9a7224", .10, 2, spec=.6)
    path = _spline([(44, 38), (58, 30), (76, 34), (82, 48), (72, 60), (54, 64), (44, 76), (50, 92), (68, 98), (84, 90), (90, 78)], 6)
    for i in range(4, len(path) - 2, 3):
        x, y = path[i]
        xa, ya = path[i - 1]
        dx, dy = x - xa, y - ya
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = 9.5 - 7 * i / len(path)
        c.poly(gold_d, (x + nx * w, y + ny * w), (x + nx * (w + 7) - dx / ln * 2, y + ny * (w + 7) - dy / ln * 2), (x + nx * w - dx / ln * 4, y + ny * w - dy / ln * 4), bevel=.6)
    left, right = _tube(c, gold, path, 10, 2.2, bevel=2.0)
    for i in range(3, len(path) - 3, 2):
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        c.scratch(.8, .35, ((x0 + left[i][0]) / 2, (y0 + left[i][1]) / 2), ((x1 + right[i + 1][0]) / 2, (y1 + right[i + 1][1]) / 2), color=(.4, .28, .08))
    for i, flip in ((12, 1), (36, -1)):
        x, y = path[i]
        c.line(gold, 3.2, (x, y), (x - 8 * flip, y + 8), (x - 12 * flip, y + 6))
        for k in (-1, 0, 1):
            c.line(gold_d, 1.2, (x - 12 * flip, y + 6), (x - 15 * flip, y + 4 + k * 3))
    for k in range(5):
        x = 48 + k * 5
        c.poly(gold_d, (x, 32 - k), (x + 4, 22 - k * 1.5), (x + 6, 31 - k), bevel=.6)
    c.line(gold_d, 2.4, (46, 32), (54, 22), (62, 20), (66, 14))
    c.line(gold_d, 2.0, (54, 22), (56, 16))
    c.ell(gold, 40, 38, 11, 9, bevel=1.8)
    c.poly(gold, (34, 32), (18, 34), (16, 38), (34, 40), bevel=1.4)
    c.poly(gold, (34, 42), (20, 46), (22, 50), (36, 46), bevel=1.2)
    c.poly(m("#7a1a14", .08), (34, 40), (18, 39), (21, 45), (34, 42), bevel=.4)
    for x in (22, 27):
        c.poly(m("#f4ecd8", .03), (x, 39), (x + 1.5, 42), (x + 3, 39), bevel=.3)
    c.ell(m("#f4ecd8", .03), 37, 34, 2.6, 2.0)
    c.ell(m("#8e1f1a", .08), 37, 34, 1.3, 1.3)
    for k in (0, 1):
        c.line(gold_d, 1.0, (18, 35 + k * 12), (10, 30 + k * 18), (8, 24 + k * 26), bevel=.5)
    c.poly(gold_d, (30, 48), (32, 58), (36, 50), bevel=.6)
    c.ell(m("#f0d070", .05, spec=1.0), 30, 52, 4.5, 4.5, bevel=1.0)
    c.glow(30, 52, 8, "#fff0b0", .3)


def _lion(c):
    """A lion rampant facing the viewer's left: raised forepaws with claws, full mane, tongue out, tail curled over the back."""
    gold, gold_d = GOLD, m("#9a7224", .10, 2, spec=.6)
    claw = m("#f4ecd8", .03)
    tail = _spline([(76, 80), (90, 70), (94, 52), (88, 36), (94, 26)], 6)
    _tube(c, gold, tail, 3.2, 2.0, bevel=1.2)
    c.poly(gold_d, (92, 20), (100, 22), (98, 32), (90, 30), bevel=1.0)
    c.poly(gold, (66, 80), (80, 82), (82, 96), (90, 106), (88, 110), (72, 110), (70, 100), (62, 90), bevel=1.6)
    c.poly(gold, (74, 74), (88, 74), (98, 84), (96, 92), (88, 90), (80, 84), bevel=1.6)
    for x, y in ((74, 110), (80, 110), (86, 110), (97, 90), (99, 86)):
        c.ell(claw, x, y, 1.6, 1.6)
    c.poly(gold, (48, 48), (62, 44), (76, 56), (82, 76), (74, 88), (62, 84), (52, 70), bevel=2.0)
    c.scratch(1.0, .4, (60, 52), (70, 66), (72, 80), color=(.4, .28, .08))
    for y in (60, 66, 72):
        c.scratch(.9, .35, (60, y), (70, y + 3), color=(.4, .28, .08))
    c.poly(gold, (50, 52), (40, 50), (30, 40), (28, 32), (34, 30), (40, 38), (52, 44), bevel=1.6)
    c.poly(gold, (54, 62), (44, 66), (32, 62), (28, 56), (34, 54), (44, 58), (56, 56), bevel=1.6)
    for x, y in ((27, 31), (30, 28), (34, 28), (27, 56), (28, 60), (31, 63)):
        c.line(claw, 1.0, (x, y), (x - 3, y - 2), bevel=.4)
    mane = []
    for k in range(32):
        a = k * 2 * math.pi / 32
        r = 14 if k % 2 else 19
        mane.append((50 + r * math.cos(a), 40 + r * .95 * math.sin(a)))
    c.poly(gold_d, *mane, bevel=1.6)
    for k in range(8):
        a = k * 2 * math.pi / 8 + .2
        c.scratch(.9, .4, (50 + 8 * math.cos(a), 40 + 8 * math.sin(a)), (50 + 16 * math.cos(a), 40 + 16 * math.sin(a)), color=(.35, .24, .06))
    c.ell(gold, 46, 40, 10, 10, bevel=1.8)
    c.poly(gold, (40, 36), (30, 40), (30, 47), (40, 48), bevel=1.2)
    c.ell(m("#2a1810", .1), 31, 40, 1.4, 1.0)
    c.line(m("#b2241e", .08), 2.0, (32, 47), (26, 51), (24, 49))
    c.line(m("#2a1810", .1), 1.0, (30, 45), (38, 46), bevel=.4)
    c.ell(m("#2a1810", .1), 42, 36, 1.8, 1.4)
    c.poly(gold, (48, 30), (52, 24), (55, 31), bevel=.8)


EMBLEMS.update({"owl": _owl, "dragon": _dragon, "lion": _lion})


# ================================================================== weapons
@painter
def xiphos():
    c = Canvas(128, seed=101)
    at, ln = axis((24, 110), (106, 20))
    c.ell(BRONZE, *at(5, 0), 5.5, 5.5, bevel=1.4)
    haft(c, at, 7, 27, 3.0, m("#3a2618", .12, 2, (1, 5)))
    for u in (12, 19):
        c.ell(BRONZE, *at(u, 0), 1.6, 1.6, bevel=.6)
    c.poly(BRONZE, at(26, -8), at(31, -6), at(31, 6), at(26, 8), bevel=1.0)
    u0, u1 = 31, ln
    left, right = [], []
    for i in range(15):
        t = i / 14
        u = u0 + (u1 - u0 - 6) * t
        w = 4.6 + 2.6 * math.sin(math.pi * min(1, t * 1.25)) * (1 - t) ** .3
        left.append(at(u, -w))
        right.append(at(u, w))
    c.poly(m("#8a7a5a", .08, 3, (9, 1), spec=.9, tint="#6a5a3a"), *(left + [at(u1, 0)] + right[::-1]), bevel=1.0)
    c.scratch(.7, .45, at(u0 + 2, 0), at(u1 - 8, 0))
    c.glow(*at(60, -2), 14, "#fff4dc", .10)
    return c.image()


@painter
def kopis():
    c = Canvas(128, seed=102)
    at, ln = axis((26, 108), (104, 22))
    c.poly(DARKIRON, at(0, -2), at(4, -7), at(8, -6), at(6, 0), at(8, 3), at(3, 3), bevel=.8)
    haft(c, at, 4, 26, 3.4, m("#4a2e1c", .14, 2, (1, 5)))
    wraps(c, at, 8, 24, 3.6, 3, (LEATHER, LEATHER_D))
    c.poly(BRONZE, at(25, -6), at(30, -5), at(30, 5), at(25, 6), bevel=1.0)
    curve = lambda u: -5.5 * math.sin(math.pi * (u - 30) / (ln - 30)) + 3 * ((u - 30) / (ln - 30)) ** 2
    u0 = 30
    left, right = [], []
    for i in range(16):
        t = i / 15
        u = u0 + (ln - 4 - u0) * t
        w_back = 3.2
        w_edge = 2.6 + 6.5 * t ** 1.6 * (1 - t * .55)
        left.append(at(u, curve(u) - w_back))
        right.append(at(u, curve(u) + w_edge))
    tip = at(ln, curve(ln) - 2)
    c.poly(STEEL, *(left + [tip] + right[::-1]), bevel=1.0)
    edge = [at(u0 + (ln - 4 - u0) * i / 15, curve(u0 + (ln - 4 - u0) * i / 15) + 1.5 + 4 * (i / 15) ** 1.6) for i in range(16)]
    c.poly(m("#dfe5e8", .04, 2, spec=1.2), *(right + [tip] + edge[::-1]), bevel=.5, edge=0, clip=True)
    c.scratch(.6, .35, at(u0 + 4, curve(u0 + 4) - 1), at(ln - 14, curve(ln - 14) - 1))
    return c.image()


@painter
def jian():
    c = Canvas(128, seed=103)
    at, ln = axis((22, 112), (110, 14))
    c.line(IMP_RED, 2.0, at(0, 0), at(-4, 8), at(-2, 16))
    for k in (-1, 0, 1):
        c.line(IMP_RED, 1.2, at(-2, 16), at(-1 + k * 1.5, 24))
    c.ell(GOLD, *at(3, 0), 4.5, 4.0, bevel=1.2)
    haft(c, at, 6, 26, 2.8, m("#2a1a16", .1, 2, (1, 5)))
    wraps(c, at, 8, 25, 3.0, 2.6, (m("#3a1a16", .1), m("#5a2a22", .1)))
    c.poly(GOLD, at(25, -7), at(28, -4), at(30, -4), at(30, 4), at(28, 4), at(25, 7), bevel=1.0)
    blade(c, at, 30, ln, 4.0, 3.2, m("#a8b2b8", .05, 3, (9, 1), spec=1.0), tip=10, edge_mat=m("#e4e9ec", .04, 2, spec=1.2), fuller=False)
    c.scratch(.7, .5, at(32, 0), at(ln - 10, 0), color=(.3, .33, .36))
    c.glow(*at(70, -1), 14, "#f4f7ff", .10)
    return c.image()


@painter
def sabre():
    c = Canvas(128, seed=104)
    at, ln = axis((26, 110), (104, 16))
    curve = lambda u: -7 * ((u - 28) / (ln - 28)) ** 1.7
    c.ell(BRASS, *at(3, 1), 4.5, 4.0, bevel=1.2)
    haft(c, at, 5, 26, 3.2, m("#1f1712", .12, 2, (1, 5)))
    for u in range(7, 26, 3):
        c.line(BRASS, .8, at(u, -3.2), at(u + 1.5, 3.2), bevel=.4)
    pts = [at(28, -4)] + [at(28 - 10 * math.sin(a), 6 + 10 * math.cos(a) - 4) for a in np.linspace(0, math.pi, 10)] + [at(3, 5)]
    c.line(STEEL, 2.6, *pts)
    c.line(STEEL, 1.8, at(26, 1), at(14, 12), at(5, 6))
    c.poly(STEEL, at(26, -6), at(30, -5), at(30, 5), at(26, 6), bevel=1.0)
    blade(c, at, 30, ln, 3.6, 2.6, m("#b0b8bc", .05, 3, (9, 1), spec=1.0), tip=12, edge_mat=m("#e4e9ec", .04, 2, spec=1.2),
          fuller=True, off=curve)
    return c.image()


@painter
def recurve_bow():
    c = Canvas(128, seed=105)
    at, ln = axis((22, 120), (106, 8))
    pts = []
    for t in np.linspace(0, 1, 48):
        v = -12 * math.sin(math.pi * t)
        e = max(0, abs(t - .5) - .32) / .18
        v += 9 * e ** 1.6
        pts.append(at(t * ln, v))
    c.line(m("#3a2418", .12, 2), 5.6, *pts)
    c.line(m("#d9c9a0", .08, 2, spec=.5), 2.4, *pts[6:42])
    c.line(m("#d8cfb8", .05), 1.0, pts[0], pts[-1])
    mid = len(pts) // 2
    c.line(LEATHER_D, 6.4, pts[mid - 3], pts[mid + 3])
    for k in (0, len(pts) - 1):
        c.ell(BONE_TIP, *pts[k], 2.6, 2.6, bevel=.8)
    return c.image()


BONE_TIP = m("#e0d6bf", .06, 2)


@painter
def repeater():
    c = Canvas(128, seed=106)
    at, ln = axis((20, 108), (106, 22))
    haft(c, at, 0, 92, 4.4, m("#5a2a1c", .12, 2, (9, 1)))
    c.poly(LACQUER, at(0, -5), at(14, -5), at(14, 5), at(0, 5), bevel=1.0)
    bow = [at(78 + 5 * math.sin(t * math.pi), -42 + 84 * t) for t in np.linspace(0, 1, 22)]
    c.line(m("#3a2a1a", .12, 2), 4.8, *bow)
    c.line(m("#d8cfb8", .05), 1.0, bow[0], at(58, 0), bow[-1])
    c.poly(m("#6a3a22", .12, 2, (9, 1)), at(34, -11), at(86, -11), at(86, -4), at(34, -4), bevel=1.4)
    for u in range(40, 84, 8):
        c.scratch(.6, .35, at(u, -11), at(u, -4))
    c.poly(BRONZE, at(84, -12), at(90, -12), at(90, -3), at(84, -3), bevel=.8)
    c.line(m("#4a2a1a", .12, 2, (1, 5)), 3.2, at(40, -11), at(30, -30), at(14, -36))
    c.ell(BRONZE, *at(40, -11), 2.6, 2.6, bevel=.8)
    for k in range(3):
        c.poly(STEEL, at(70 + k * 4, -14), at(96 + k * 4, -13.5), at(98 + k * 4, -13), at(70 + k * 4, -12.5), bevel=.4)
    return c.image()


@painter
def fire_lance():
    c = Canvas(128, seed=107)
    at, ln = axis((16, 118), (112, 12))
    haft(c, at, 0, ln - 24, 2.4, m("#5a3a22", .18, 3, (1, 9)))
    c.poly(STEEL, at(ln - 24, -3.2), at(ln - 6, -2.6), at(ln, 0), at(ln - 6, 2.6), at(ln - 24, 3.2), bevel=1.0)
    c.poly(BAMBOO, at(ln - 56, 2.6), at(ln - 28, 2.6), at(ln - 28, 10), at(ln - 56, 10), bevel=1.6)
    for u in (ln - 50, ln - 40, ln - 32):
        c.line(IMP_RED, 1.8, at(u, 1.6), at(u + 1, 11))
    c.ell(m("#2a1a10", .1), *at(ln - 27, 6.3), 2.2, 3.2)
    c.line(m("#d8b078", .1), .9, at(ln - 56, 6), at(ln - 62, 12), at(ln - 60, 16), bevel=.4)
    c.ell(m("#ffd070", .1), *at(ln - 60, 16.5), 1.8, 1.8)
    c.glow(*at(ln - 60, 16.5), 6, "#ffb040", .7)
    for u in (ln - 70, ln - 64):
        c.line(IMP_RED, 1.4, at(u, -3), at(u + .5, 3))
    return c.image()


@painter
def musket():
    c = Canvas(128, seed=108)
    at, ln = axis((12, 112), (118, 12))
    c.poly(m("#6a4224", .14, 3, (9, 1)), at(0, -7), at(18, -5), at(28, -3), at(84, -2.6), at(84, 2.6), at(28, 3.6), at(16, 7), at(0, 8), bevel=1.6)
    c.poly(BRASS, at(-1, -7), at(2, -7), at(2, 8), at(-1, 8), bevel=.8)
    c.poly(m("#3e4246", .08, 3, (9, 1), spec=.9), at(26, -2.2), at(ln, -1.6), at(ln, 1.6), at(26, 2.2), bevel=.8)
    for u in (48, 66, 82):
        c.line(BRASS, 1.6, at(u, -3), at(u, 3))
    c.line(m("#2c2a28", .08, spec=.6), 1.0, at(34, 3.4), at(ln - 4, 3.0))
    c.poly(m("#3e4246", .08, spec=.9), at(26, -3), at(36, -3), at(36, -6), at(26, -6), bevel=.8)
    c.line(DARKIRON, 1.8, at(29, -5), at(26, -10), at(30, -12))
    c.line(DARKIRON, 1.6, at(32, 3), at(30, 7), at(26, 8))
    c.line(m("#d8cfb8", .05), 1.2, at(12, 7), at(34, 5.5), bevel=.4)
    return c.image()


@painter
def bayonet_rifle():
    c = Canvas(128, seed=109)
    at, ln = axis((14, 114), (118, 10))
    L = ln - 20
    c.poly(m("#5a3a20", .14, 3, (9, 1)), at(0, -7), at(16, -5), at(26, -3), at(L - 14, -2.6), at(L - 14, 2.6), at(26, 3.6), at(14, 7), at(0, 8), bevel=1.6)
    c.poly(BRASS, at(-1, -7), at(2, -7), at(2, 8), at(-1, 8), bevel=.8)
    c.poly(m("#2e3236", .08, 3, (9, 1), spec=.9), at(24, -2.0), at(L, -1.6), at(L, 1.6), at(24, 2.0), bevel=.8)
    for u in (44, 62, L - 16):
        c.line(m("#3a3e42", .08, spec=.8), 1.6, at(u, -3), at(u, 3))
    c.poly(m("#2e3236", .08, spec=.9), at(24, -3), at(34, -3), at(34, -6), at(24, -6), bevel=.8)
    c.line(DARKIRON, 1.8, at(27, -5), at(24, -10), at(28, -12))
    c.poly(STEEL, at(L - 4, 2), at(L, 2), at(L, 4.5), at(L - 4, 4.5), bevel=.6)
    c.poly(m("#c0c8cc", .04, 3, (9, 1), spec=1.2), at(L - 2, 3.4), at(ln - 4, 3.6), at(ln, 3.4), at(ln - 4, 5.8), at(L - 2, 5.6), bevel=.6)
    c.line(m("#d8cfb8", .05), 1.4, at(10, 7.5), at(30, 10), at(56, 4), bevel=.4)
    return c.image()


# ------------------------------------------------------------------ spear_long gains the guandao head
_spear_long_old = heirs_art2.spear_long


@painter
def spear_long(head="leaf", shaft="#6b4a2e", length=1.0):
    if head != "guandao":
        return _spear_long_old(head=head, shaft=shaft, length=length)
    c = Canvas(128, seed=110)
    at, ln = axis((12, 120), (114, 8))
    haft(c, at, 0, ln - 30, 2.6, m(shaft, .14, 3, (1, 9), spec=.4))
    c.poly(DARKIRON, at(-1, -3), at(6, -3), at(6, 3), at(-1, 3), bevel=.6)
    for u in (ln - 34, ln - 64):
        c.line(GOLD, 1.4, at(u, -2.8), at(u, 2.8))
    pts_back = [at(ln - 30 + 30 * t, -2.5 - 2 * t) for t in np.linspace(0, 1, 8)]
    pts_edge = [at(ln - 30 + 34 * t, 4 + 9 * math.sin(math.pi * t * .9)) for t in np.linspace(1, 0, 10)]
    c.poly(STEEL, *(pts_back + [at(ln + 2, -6)] + pts_edge), bevel=1.0)
    c.poly(m("#dfe5e8", .04, 2, spec=1.2), *([at(ln - 30 + 34 * t, 1.5 + 9 * math.sin(math.pi * t * .9) * .7) for t in np.linspace(0, 1, 10)]
                                             + pts_edge), bevel=.4, edge=0, clip=True)
    c.poly(STEEL, at(ln - 18, -4.5), at(ln - 14, -9), at(ln - 12, -4.5), bevel=.6)
    c.ell(GOLD, *at(ln - 31, 0), 4.6, 4.6, bevel=1.2)
    c.ell(m("#7a1a14", .08), *at(ln - 31, 0), 2.0, 2.0)
    c.line(IMP_RED, 2.0, at(ln - 33, 2), at(ln - 40, 9))
    for k in (-1, 0, 1):
        c.line(IMP_RED, 1.2, at(ln - 40, 9), at(ln - 44 + k * 2, 16))
    return c.image()


# ================================================================== apparel icons
@painter
def helmet2(kind="corinthian"):
    c = Canvas(128, seed=111)
    if kind == "corinthian":
        crest = [(64 + 40 * math.cos(math.radians(a)), 46 + 34 * math.sin(math.radians(a))) for a in np.linspace(195, 345, 16)]
        for i, (x, y) in enumerate(crest):
            c.line(HORSEHAIR if i % 3 else HORSEHAIR_D, 6.4, (64 + (x - 64) * .45, 40 + (y - 46) * .45), (x, y))
        c.rect(BRONZE, 60, 14, 68, 32, 2, bevel=1.0)
        shell = [(30, 66), (32, 44), (44, 30), (64, 25), (84, 30), (96, 44), (98, 66), (96, 92), (88, 112), (74, 112), (70, 86), (58, 86), (54, 112),
                 (40, 112), (32, 92)]
        c.poly(BRONZE, *shell, bevel=2.6)
        c.poly(m("#1a1410", .1), (40, 62), (60, 60), (61, 66), (61, 84), (67, 84), (67, 66), (68, 60), (88, 62), (86, 72), (70, 70), (70, 90),
               (58, 90), (58, 70), (42, 72), bevel=.6)
        c.poly(BRONZE, (61, 64), (67, 64), (67, 86), (64, 90), (61, 86), bevel=1.0)
        for pts in (((34, 56), (50, 52), (62, 54)), ((94, 56), (78, 52), (66, 54))):
            c.scratch(1.2, .45, *pts)
        c.line(m("#e6c070", .05, spec=1.2), 1.2, (36, 104), (40, 74), (38, 60))
        c.glow(50, 40, 18, "#fff0c0", .2)
    elif kind == "tianxia":
        for i in range(9):
            x0 = 26 + i * 9
            c.rect(IRON if i % 2 else STEEL, x0, 74, x0 + 10, 108 - abs(i - 4) * 2, 2, bevel=1.0)
            c.line(m("#b72f22", .1), 1.0, (x0 + 5, 78), (x0 + 5, 104 - abs(i - 4) * 2))
        c.ell(IRON, 64, 66, 34, 30, bevel=2.6)
        for x in range(40, 92, 8):
            c.line(DARKIRON, 1.6, (x, 72), (64 + (x - 64) * .2, 40))
        c.rect(GOLD, 30, 70, 98, 77, 3, bevel=1.2)
        c.rect(GOLD, 60, 22, 68, 40, 2, bevel=1.0)
        c.ell(GOLD, 64, 22, 5, 3, bevel=1.0)
        for k in range(9):
            a = math.radians(-90 + (k - 4) * 14)
            c.line(m("#c8322a", .1, 1.5, (1, 4)), 3.0, (64, 20), (64 + 18 * math.cos(a) * .6, 20 + 22 * math.sin(a) * .3 - 2 + abs(k - 4) * 3))
    elif kind == "shako":
        c.poly(FELT, (36, 36), (92, 36), (88, 98), (40, 98), bevel=2.2, cyl=(36, 92))
        c.ell(FELT, 64, 36, 28, 7, bevel=1.4)
        c.rect(m("#d8d2c4", .05), 38, 38, 90, 44, 2, bevel=.8)
        c.poly(BRASS, (52, 56), (76, 56), (78, 72), (64, 84), (50, 72), bevel=1.6)
        c.ell(m("#a51e22", .08), 64, 68, 5, 5, bevel=1.0)
        c.poly(m("#141418", .06, spec=.8), (36, 96), (92, 96), (100, 108), (28, 108), bevel=1.4)
        c.line(BRASS, 1.6, (40, 94), (64, 104), (88, 94))
        c.ell(FACING, 64, 22, 8, 9, bevel=2.0)
        c.ell(m("#a51e22", .08), 64, 30, 7, 4, bevel=1.2)
    return c.image()


@painter
def torso2(kind="linothorax"):
    c = Canvas(128, seed=112)
    if kind == "linothorax":
        for i in range(10):
            x = 30 + i * 7
            c.rect(LINEN if i % 2 else LINEN_D, x, 88, x + 7, 118, 2, bevel=1.0)
        c.poly(LINEN, (34, 30), (94, 30), (98, 60), (94, 92), (34, 92), (30, 60), bevel=2.4)
        c.rect(HELLAS_BLUE, 32, 80, 96, 88, 1, bevel=.8)
        for x in range(34, 94, 8):
            c.line(FACING, 1.0, (x, 86), (x, 82), (x + 4, 82), (x + 4, 85), (x + 2, 85))
        for side in (0, 1):
            x0 = 22 if side == 0 else 74
            c.poly(LINEN, (x0, 22), (x0 + 32, 22), (x0 + 30, 40), (x0 + 2, 40), bevel=1.8)
            c.rect(HELLAS_BLUE, x0 + 2, 24, x0 + 30, 28, 1, bevel=.6)
        c.ell(GOLD, 64, 56, 9, 9, bevel=1.6)
        c.ell(m("#2a1c10", .1), 64, 56, 4, 4)
        for x in (40, 88):
            c.ell(BRONZE, x, 38, 2.2, 2.2, bevel=.8)
    elif kind == "chiton":
        c.poly(LINEN, (40, 24), (88, 24), (110, 42), (100, 54), (90, 48), (96, 116), (32, 116), (38, 48), (28, 54), (18, 42), bevel=2.0)
        for x in (46, 56, 72, 82):
            c.scratch(1.4, .3, (x, 66), (x + (x - 64) * .2, 114))
        c.rect(HELLAS_BLUE, 32, 106, 96, 114, 1, bevel=.8)
        for x in range(34, 94, 8):
            c.line(FACING, 1.0, (x, 112), (x, 108), (x + 4, 108), (x + 4, 111), (x + 2, 111))
        c.rect(m("#8a6a3a", .1), 38, 58, 90, 64, 2, bevel=1.2)
        for x in (44, 84):
            c.ell(GOLD, x, 28, 3.2, 3.2, bevel=1.0)
    elif kind == "lamellar":
        for side in (-1, 1):
            for j in range(4):
                x0 = 64 + side * (34 + j * 3)
                c.poly(IRON if j % 2 else STEEL, (x0, 24 + j * 9), (x0 + side * 16, 30 + j * 9), (x0 + side * 14, 40 + j * 9), (x0 - side * 2, 34 + j * 9), bevel=1.0)
                c.line(m("#b72f22", .1), .9, (x0, 29 + j * 9), (x0 + side * 15, 35 + j * 9))
        body = [(38, 22), (90, 22), (98, 50), (96, 84), (104, 118), (24, 118), (32, 84), (30, 50)]
        c.poly(m("#3a1c18", .1), *body, bevel=2.2)
        for row in range(10):
            y = 24 + row * 9.4
            for i in range(14):
                x = 22 + i * 6.4 + (row % 2) * 3.2
                c.rect(STEEL if (i + row) % 3 else IRON, x, y, x + 6, y + 9, 1.4, bevel=.8, clip=True)
            c.line(m("#b72f22", .1), .9, (22, y + 4.5), (106, y + 4.5))
        c.rect(IMP_RED, 30, 80, 98, 87, 2, bevel=1.2, clip=True)
        c.ell(GOLD, 64, 50, 12, 12, bevel=1.8)
        c.ell(m("#d8e0e4", .03, spec=1.4), 64, 50, 8, 8, bevel=.8)
    elif kind == "hanfu":
        sleeve = m("#2a3e6a", .08, 2)
        c.poly(sleeve, (36, 28), (6, 60), (12, 90), (36, 78), bevel=2.0)
        c.poly(sleeve, (92, 28), (122, 60), (116, 90), (92, 78), bevel=2.0)
        c.poly(m("#2f467a", .08, 2), (38, 22), (90, 22), (96, 116), (32, 116), bevel=2.2)
        c.poly(FACING, (52, 22), (64, 22), (80, 62), (74, 66), bevel=1.0)
        c.poly(m("#d8ccb0", .05), (76, 22), (64, 22), (48, 62), (54, 66), bevel=1.0)
        c.rect(IMP_RED, 32, 62, 96, 72, 2, bevel=1.4)
        c.line(GOLD, 1.4, (34, 67), (94, 67))
        c.line(IMP_RED, 2.2, (70, 72), (74, 92))
        c.line(IMP_RED, 2.2, (74, 72), (80, 90))
        for x, y in ((14, 86), (114, 86)):
            c.rect(FACING, x - 8, y - 2, x + 8, y + 4, 2, bevel=.8)
    elif kind == "redcoat":
        c.poly(COAT_RED, (34, 24), (6, 52), (14, 70), (36, 50), bevel=2.0)
        c.poly(COAT_RED, (94, 24), (122, 52), (114, 70), (92, 50), bevel=2.0)
        c.poly(COAT_RED, (38, 20), (90, 20), (96, 92), (104, 122), (84, 122), (64, 96), (44, 122), (24, 122), (32, 92), bevel=2.2)
        c.poly(FACING, (50, 20), (78, 20), (72, 90), (56, 90), bevel=1.0)
        for y in range(30, 90, 10):
            c.ell(BRASS, 52, y, 2.0, 2.0, bevel=.8)
            c.ell(BRASS, 76, y, 2.0, 2.0, bevel=.8)
        c.line(FACING, 4.2, (40, 24), (88, 86))
        c.line(FACING, 4.2, (88, 24), (40, 86))
        c.ell(BRASS, 64, 55, 5, 5, bevel=1.2)
        for x in (10, 118):
            c.rect(FACING, x - 7, 62, x + 7, 70, 2, bevel=.8)
        c.rect(m("#efe9da", .04), 40, 18, 88, 24, 3, bevel=1.0)
    return c.image()


# ================================================================== buildings
@painter
def hoplon(size=(1, 1)):
    c = Canvas(128, seed=113)
    c.ell(m("#2a1c10", .1), 66, 68, 54, 54)
    c.ell(BRONZE, 64, 64, 54, 54, bevel=2.6)
    c.ell(HELLAS_BLUE, 64, 64, 44, 44, bevel=1.2)
    ring(c, 64, 64, 48.5, m("#e6c070", .05, spec=1.2), 1.2)
    for k in range(20):
        a = k * 2 * math.pi / 20
        c.ell(GOLD, 64 + 49 * math.cos(a), 64 + 49 * math.sin(a), 1.4, 1.4, bevel=.6)
    _owl(_At(c, .72, 64, 66))
    c.glow(46, 44, 26, "#ffffff", .14)
    return c.image()


@painter
def column(size=(1, 1)):
    c = Canvas(128, 256, seed=114)
    c.rect(MARBLE, 30, 222, 98, 252, 3, bevel=1.8)
    c.rect(MARBLE, 36, 210, 92, 224, 2, bevel=1.4)
    c.rect(MARBLE, 42, 96, 86, 212, 2, bevel=1.6, cyl=(42, 86))
    for x in range(46, 84, 5):
        c.scratch(1.2, .35, (x, 100), (x, 208), color=(.55, .52, .46))
    c.rect(MARBLE, 34, 86, 94, 98, 3, bevel=1.6)
    for x in (40, 88):
        c.ell(MARBLE, x, 86, 7, 6, bevel=1.4)
    c.rect(MARBLE, 30, 78, 98, 86, 2, bevel=1.4)
    statue = m("#6a5a3a", .14, 2, spec=.9, tint="#3e5a48")
    c.poly(statue, (56, 78), (72, 78), (74, 54), (78, 40), (68, 34), (60, 34), (50, 40), (54, 54), bevel=1.8)
    c.ell(statue, 64, 26, 7, 8, bevel=1.6)
    c.poly(statue, (58, 22), (64, 10), (70, 22), bevel=1.0)
    c.line(statue, 2.0, (76, 40), (84, 14))
    c.poly(statue, (84, 14), (86, 6), (88, 14), bevel=.6)
    c.ell(statue, 50, 52, 9, 12, bevel=1.6)
    c.glow(54, 30, 16, "#fff4d0", .18)
    return c.image()


@painter
def theatre(size=(3, 2)):
    c = Canvas(384, 256, seed=115)
    c.rect(STONE_L, 20, 26, 364, 150, 6, bevel=2.2)
    for x in range(50, 350, 50):
        c.rect(MARBLE, x - 8, 40, x + 8, 146, 2, bevel=1.4, cyl=(x - 8, x + 8))
        c.rect(MARBLE, x - 12, 36, x + 12, 44, 2, bevel=1.0)
    c.rect(MARBLE, 16, 18, 368, 32, 3, bevel=1.6)
    c.poly(MARBLE, (16, 18), (368, 18), (192, 2), bevel=1.6)
    for x0, x1 in ((86, 130), (170, 214), (254, 298)):
        c.rect(m("#2a1c14", .1), x0, 82, x1, 146, 20, bevel=.8)
        c.rect(m("#6a2a4a", .1, 2, (1, 4)), x0 + 2, 84, x1 - 2, 146, 18, bevel=1.0)
    c.rect(OAK, 8, 146, 376, 210, 4, bevel=2.0)
    for y in range(152, 206, 11):
        c.scratch(1.0, .4, (12, y), (372, y))
    c.rect(OAK_V, 8, 206, 376, 246, 4, bevel=1.6)
    for x in range(20, 372, 24):
        c.scratch(1.0, .35, (x, 208), (x, 244))
    for cx, smile in ((150, 1), (234, -1)):
        face = m("#efe6cc", .05, 2, spec=.4) if smile > 0 else m("#d8cba8", .06, 2, spec=.4)
        c.ell(face, cx, 60, 18, 21, bevel=1.8)
        for ex in (-7, 7):
            c.ell(m("#1a1410", .1), cx + ex, 56, 4, 3 if smile > 0 else 2.4)
        mouth = [(cx - 9, 70 - smile * 2), (cx, 70 + smile * 6), (cx + 9, 70 - smile * 2)]
        c.line(m("#1a1410", .1), 2.4, *mouth)
    c.line(GOLD, 2.0, (130, 48), (150, 38), (170, 46), (192, 40), (214, 46), (234, 38), (254, 48))
    for x in (40, 344):
        c.rect(BRONZE, x - 6, 176, x + 6, 204, 2, bevel=1.0)
        c.ell(m("#ff9a3a", .2, tint="#ff5a1a"), x, 170, 6, 8, bevel=1.0)
        c.glow(x, 170, 22, "#ffb040", .4)
    return c.image()


@painter
def vase(size=(1, 1)):
    c = Canvas(128, 192, seed=116)
    c.ell(m("#2a2420", .1), 66, 180, 32, 8)
    prof = [(64, 184), (44, 182), (40, 170), (34, 140), (30, 108), (36, 82), (48, 64), (52, 46), (46, 30), (50, 22), (78, 22), (82, 30), (76, 46),
            (80, 64), (92, 82), (98, 108), (94, 140), (88, 170), (84, 182)]
    c.poly(PORCELAIN, *prof, bevel=2.8, cyl=(30, 98))
    c.rect(COBALT, 40, 168, 88, 176, 2, bevel=.6, clip=True)
    c.rect(COBALT, 48, 28, 80, 34, 2, bevel=.6, clip=True)
    c.rect(COBALT, 36, 80, 92, 85, 2, bevel=.6, clip=True)
    path = _spline([(36, 128), (52, 112), (70, 124), (86, 108), (96, 116)], 6)
    for i in range(len(path) - 1):
        c.line(COBALT, 4.2 - 2.6 * i / len(path), path[i], path[i + 1], bevel=.4)
    c.ell(COBALT, 34, 128, 5, 4, bevel=.6)
    for x, y in ((48, 96), (78, 150), (58, 154), (86, 94)):
        for k in range(3):
            c.ell(COBALT, x + k * 5, y - (k % 2) * 3, 3.6, 2.6, bevel=.4)
    c.glow(48, 100, 26, "#ffffff", .25)
    return c.image()


@painter
def moon_gate(size=(3, 1)):
    c = Canvas(384, 288, seed=117)
    cx, cy, r = 192, 170, 86
    wall = m("#e4ddd0", .06, 4)
    top, bottom, left, right = 56, 282, 6, 378
    arc_l = [(cx - r * math.sin(t), cy + r * math.cos(t)) for t in np.linspace(0, math.pi, 30)]
    c.poly(wall, (cx, top), (left, top), (left, bottom), (cx, bottom), (cx, cy + r), *arc_l, (cx, cy - r), bevel=2.0)
    arc_r = [(cx + r * math.sin(t), cy + r * math.cos(t)) for t in np.linspace(0, math.pi, 30)]
    c.poly(wall, (cx, top), (right, top), (right, bottom), (cx, bottom), (cx, cy + r), *arc_r, (cx, cy - r), bevel=2.0)
    ring_pts = [(cx + (r + 7) * math.cos(t), cy + (r + 7) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 80)]
    c.line(m("#6a6a68", .08, 3), 10, *ring_pts)
    c.line(m("#4a4a4a", .08), 3, *[(cx + (r + 1) * math.cos(t), cy + (r + 1) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 80)])
    roof = m("#2e3a36", .1, 2, spec=.5)
    c.poly(roof, (0, 60), (384, 60), (370, 34), (14, 34), bevel=1.6)
    c.poly(roof, (14, 34), (0, 22), (6, 36), bevel=.8)
    c.poly(roof, (370, 34), (384, 22), (378, 36), bevel=.8)
    for x in range(18, 372, 12):
        c.scratch(1.2, .45, (x, 38), (x - 2, 58), color=(.1, .14, .12))
    c.rect(m("#3a2a22", .1), 6, 60, 378, 66, 1, bevel=.6)
    for x in (40, 344):
        c.rect(m("#2a3a32", .1, spec=.3), x - 18, 110, x + 18, 150, 4, bevel=1.2)
        for k in range(3):
            c.ell(JADE_L, x - 9 + k * 9, 130, 3, 3, bevel=.6)
    c.rect(STONE, cx - 70, 274, cx + 70, 286, 3, bevel=1.2)
    return c.image()


@painter
def paper_lantern(size=(1, 1)):
    c = Canvas(128, 192, seed=118)
    c.ell(m("#3a3028", .1), 64, 182, 26, 7)
    c.rect(LACQUER, 58, 40, 70, 184, 3, bevel=1.4, cyl=(58, 70))
    c.rect(LACQUER, 40, 36, 92, 44, 2, bevel=1.0)
    c.line(m("#2a1e18", .1), 1.2, (84, 44), (84, 56))
    c.ell(PAPER_RED, 84, 92, 24, 34, bevel=2.6, cyl=(60, 108))
    for k in (-14, -7, 0, 7, 14):
        pts = [(84 + k * math.sin(t) * 1.0 + 0, 92 - 33 * math.cos(t)) for t in np.linspace(0, math.pi, 16)]
        c.scratch(.9, .35, *[(84 + k * math.sin(t), y) for (_, y), t in zip(pts, np.linspace(0, math.pi, 16))], color=(.4, .08, .05))
    c.rect(GOLD, 74, 56, 94, 62, 2, bevel=1.0)
    c.rect(GOLD, 74, 122, 94, 128, 2, bevel=1.0)
    c.line(GOLD, 1.6, (84, 128), (84, 138))
    for k in (-2, 0, 2):
        c.line(PAPER_RED, 1.4, (84, 138), (84 + k, 156))
    c.ell(GOLD, 84, 138, 2.6, 2.6, bevel=.8)
    c.glow(84, 92, 30, "#ffcf6a", .55)
    return c.image()


@painter
def steam_engine(size=(2, 2)):
    c = Canvas(256, 256, seed=119)
    c.rect(STONE_D, 12, 196, 244, 246, 6, bevel=2.0)
    c.rect(m("#8a3a22", .12, 3), 20, 188, 236, 204, 3, bevel=1.4)
    c.rect(m("#3e4246", .08, 3, spec=.7), 24, 104, 160, 192, 22, bevel=2.6)
    for x in range(40, 160, 22):
        c.line(DARKIRON, 2.0, (x, 106), (x, 190))
        for y in range(112, 190, 12):
            c.ell(m("#2a2c2e", .1, spec=.6), x, y, 1.5, 1.5, bevel=.5)
    c.rect(DARKIRON, 32, 150, 72, 190, 4, bevel=1.4)
    c.rect(m("#ff8a3a", .25, 2, tint="#ff4a1a"), 38, 158, 66, 184, 3, bevel=1.0)
    c.glow(52, 172, 30, "#ff8a3a", .5)
    c.rect(m("#2e3034", .08, 3, spec=.6), 120, 18, 146, 108, 3, bevel=1.6, cyl=(120, 146))
    c.rect(BRASS, 114, 14, 152, 24, 3, bevel=1.2)
    c.ell(SMOKE, 136, 8, 14, 6)
    c.rect(BRASS, 168, 120, 196, 176, 6, bevel=1.6, cyl=(168, 196))
    c.line(STEEL, 4.0, (182, 120), (182, 64))
    c.rect(OAK, 92, 56, 236, 70, 3, bevel=1.6)
    c.rect(m("#3e4246", .08, 3, spec=.7), 158, 66, 168, 190, 2, bevel=1.0)
    c.line(STEEL, 4.0, (226, 70), (214, 130))
    wx, wy, wr = 214, 150, 40
    for k in range(8):
        a = k * math.pi / 4
        c.line(DARKIRON, 4.0, (wx, wy), (wx + wr * math.cos(a), wy + wr * math.sin(a)))
    c.line(m("#2e3034", .08, 3, spec=.7), 9, *[(wx + wr * math.cos(t), wy + wr * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 60)])
    c.ell(BRASS, wx, wy, 8, 8, bevel=1.4)
    c.line(BRASS, 4.0, (160, 130), (168, 130))
    c.line(BRASS, 3.0, (60, 104), (60, 84), (120, 84))
    c.ell(BRASS, 92, 96, 9, 9, bevel=1.4)
    c.ell(m("#f2eee2", .03), 92, 96, 6, 6, bevel=.6)
    c.line(m("#1a1a1a", .1), 1.0, (92, 96), (95, 92))
    return c.image()


# ------------------------------------------------------------------ table gains the gongfu and pub kinds
_table_old = heirs_art2.table


@painter
def table(kind="triclinium", size=(2, 2)):
    if kind not in ("gongfu", "pub"):
        return _table_old(kind=kind, size=size)
    w, h = size
    W, H = 128 * w, 128 * h
    c = Canvas(W, H, seed=120)
    if kind == "gongfu":
        top = m("#5a2e1e", .14, 3, (9, 1), spec=.3)
        for x, y in ((14, 14), (W - 30, 14), (14, H - 30), (W - 30, H - 30)):
            c.rect(WOOD_D, x, y, x + 16, y + 16, 3, bevel=1.0)
        c.rect(top, 8, 8, W - 8, H - 8, 14, bevel=2.4)
        c.rect(m("#3a1e14", .12, 3, (9, 1), spec=.4), 30, 30, W - 30, H - 30, 8, bevel=1.0)
        for y in range(40, H - 36, 10):
            c.scratch(1.0, .5, (36, y), (W - 36, y), color=(.12, .06, .04))
        cx, cy = W / 2 - 10, H / 2 - 4
        c.ell(m("#1a0e0a", .1), cx + 4, cy + 6, 30, 24)
        c.ell(YIXING, cx, cy, 30, 24, bevel=2.8)
        c.ell(YIXING, cx, cy - 22, 10, 5, bevel=1.4)
        c.ell(YIXING, cx, cy - 26, 4, 3, bevel=1.0)
        c.line(YIXING, 6, (cx + 28, cy - 2), (cx + 46, cy - 18))
        c.line(YIXING, 5, (cx - 28, cy - 10), (cx - 42, cy - 2), (cx - 30, cy + 10))
        for x, y in ((W - 66, 60), (W - 44, 84), (W - 66, H - 76), (W - 44, H - 100), (60, H - 56)):
            c.ell(m("#3a2418", .1), x + 2, y + 3, 10, 9)
            c.ell(PORCELAIN, x, y, 10, 9, bevel=1.6)
            c.ell(m("#9a6a2a", .08, spec=.8), x, y, 6.5, 5.5, bevel=.4)
        c.ell(m("#6a7a4a", .12, spec=.3), 64, 64, 12, 10, bevel=1.6)
        c.line(BAMBOO, 2.2, (40, H - 30), (90, H - 70))
    else:
        for x, y in ((16, 16), (W - 32, 16), (16, H - 32), (W - 32, H - 32)):
            c.rect(WOOD_D, x, y, x + 18, y + 18, 3, bevel=1.0)
        c.rect(OAK, 8, 8, W - 8, H - 8, 8, bevel=2.4)
        for y in range(22, H - 12, 26):
            c.scratch(1.2, .45, (12, y), (W - 12, y))
        rng = np.random.default_rng(3)
        for _ in range(12):
            x, y = rng.uniform(30, W - 30), rng.uniform(30, H - 30)
            c.scratch(.8, .35, (x, y), (x + rng.uniform(-12, 12), y + rng.uniform(-3, 3)))
        for x, y in ((70, 60), (W - 70, 64), (90, H - 60), (W - 110, H - 56), (W / 2 + 30, H / 2 + 20)):
            c.ell(m("#2a1a10", .1), x + 4, y + 5, 21, 20)
            c.ell(PEWTER, x, y, 21, 20, bevel=2.4)
            c.ell(m("#c9902a", .06, spec=.8), x, y, 15, 14, bevel=.6)
            c.ell(m("#f4ead0", .05), x - 3, y - 3, 9, 6)
            c.line(PEWTER, 5.5, (x + 19, y - 6), (x + 30, y), (x + 19, y + 8))
        cx, cy = W / 2 - 40, H / 2
        c.ell(m("#2a1a10", .1), cx + 3, cy + 4, 26, 22)
        c.ell(PEWTER, cx, cy, 26, 22, bevel=2.0)
        c.ell(CRUST, cx, cy, 20, 16, bevel=1.8)
        c.poly(m("#7a3a22", .12), (cx, cy), (cx + 20, cy - 6), (cx + 20, cy + 6), bevel=.8)
        for i, (x, y) in enumerate(((W / 2 + 60, H / 2 - 30), (W / 2 + 74, H / 2 - 24), (W / 2 + 88, H / 2 - 30))):
            c.rect(FACING, x - 9, y - 13, x + 9, y + 13, 2, bevel=.8)
            c.ell(COAT_RED if i != 1 else m("#1a1a1a", .05), x, y, 3, 3)
        c.rect(m("#e9dfc4", .05), W - 40, H / 2 - 10, W - 26, H / 2 + 10, 2, bevel=1.0)
        c.glow(W - 33, H / 2 - 12, 30, "#ffcf6a", .35)
    return c.image()


# ================================================================== floors
@painter
def floor_meander():
    base = (214, 206, 186)
    img, d, rng = floor_canvas(base, 121)
    for i in range(4):
        for j in range(4):
            x, y = i * 256, j * 256
            d.rectangle((x + 3, y + 3, x + 253, y + 253), fill=shade(base, 1 + rng.uniform(-.04, .04)))
            d.rectangle((x, y, x + 255, y + 255), outline=shade(base, .78), width=4)
    band = (46, 80, 120)
    for y0 in (0, 512):
        d.rectangle((0, y0 + 8, 1024, y0 + 56), fill=(206, 196, 170))
        for x in range(0, 1024, 32):
            pts = [(x + 4, y0 + 48), (x + 4, y0 + 16), (x + 28, y0 + 16), (x + 28, y0 + 40), (x + 12, y0 + 40), (x + 12, y0 + 24), (x + 20, y0 + 24),
                   (x + 20, y0 + 32)]
            d.line(pts, fill=band, width=4, joint="curve")
            d.line([(x + 4, y0 + 48), (x + 36, y0 + 48)], fill=band, width=4)
    for _ in range(500):
        px, py, r = rng.uniform(0, 1024), rng.uniform(0, 1024), rng.uniform(1, 3)
        d.ellipse((px - r, py - r, px + r, py + r), fill=shade(base, rng.uniform(.88, 1.04)))
    return finish_floor(img, 121, 2.4)


@painter
def floor_jade():
    base = (70, 128, 96)
    img, d, rng = floor_canvas(base, 122)
    cell = 128
    for i in range(8):
        for j in range(8):
            x, y = i * cell, j * cell
            d.rectangle((x + 3, y + 3, x + cell - 3, y + cell - 3), fill=shade(base, 1 + rng.uniform(-.08, .08)))
            for _ in range(6):
                px, py = x + rng.uniform(12, cell - 12), y + rng.uniform(12, cell - 12)
                d.line([(px, py), (px + rng.uniform(-20, 20), py + rng.uniform(-8, 8))], fill=shade(base, 1.2), width=2)
            if (i + j) % 2 == 0:
                cx, cy = x + cell / 2, y + cell / 2
                for k, rr in enumerate((30, 20, 10)):
                    d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 180, 360 + 90 * (k % 2), fill=(196, 168, 90), width=3)
            d.rectangle((x, y, x + cell - 1, y + cell - 1), outline=(40, 70, 54), width=4)
    return finish_floor(img, 122, 2.0)


@painter
def floor_cobble():
    base = (110, 104, 96)
    img, d, rng = floor_canvas((70, 64, 58), 123)
    step = 1024 / 24
    for row in range(24):
        for col in range(24):
            x = col * step + (row % 2) * step / 2 + rng.uniform(-7, 7)
            y = row * step + rng.uniform(-7, 7)
            rx, ry = rng.uniform(17, 25), rng.uniform(15, 23)
            col_ = shade(base, rng.uniform(.78, 1.22))
            for ox in (-1024, 0, 1024):
                for oy in (-1024, 0, 1024):
                    d.ellipse((x - rx + ox, y - ry + oy, x + rx + ox, y + ry + oy), fill=col_)
                    d.ellipse((x - rx * .6 + ox, y - ry * .7 + oy, x + rx * .3 + ox, y - ry * .1 + oy), fill=shade(col_, 1.12))
    return finish_floor(img, 123, 3.6)


@painter
def floor_brick():
    img, d, rng = floor_canvas((150, 138, 120), 124)
    bw, bh = 128, 64
    for gx in range(-2, 18):
        for gy in range(-2, 18):
            ox, oy = gx * 64, gy * 64
            horizontal = (gx + gy) % 2 == 0
            if horizontal:
                box = (ox + 3, oy + 3, ox + bw - 3, oy + bh - 3)
            else:
                box = (ox + 3, oy + 3, ox + bh - 3, oy + bw - 3)
            col = shade((156, 70, 48), rng.uniform(.82, 1.15))
            for sx in (-1024, 0, 1024):
                for sy in (-1024, 0, 1024):
                    b = (box[0] + sx, box[1] + sy, box[2] + sx, box[3] + sy)
                    d.rectangle(b, fill=col)
    return finish_floor(img, 124, 3.0)


# ================================================================== food and goods
@painter
def food2(kind="maza"):
    c = Canvas(128, seed=125)
    if kind == "maza":
        c.ell(m("#7a4a2a", .1), 66, 78, 50, 30)
        c.ell(m("#b0603a", .12, 2), 64, 74, 50, 30, bevel=2.2)
        c.ell(m("#c87a4a", .1), 64, 72, 42, 24, bevel=1.0)
        for dx, dy in ((-16, -2), (10, -8), (4, 10)):
            c.ell(BARLEY, 64 + dx, 72 + dy, 16, 9, bevel=1.8)
            c.scratch(.8, .45, (64 + dx - 8, 72 + dy), (64 + dx + 8, 72 + dy - 2))
        c.rect(CHEESE, 82, 66, 98, 78, 2, bevel=1.4)
        for x, y in ((36, 66), (42, 84), (34, 78), (90, 88)):
            c.ell(m("#2a2a1a", .08, spec=.9), x, y, 3.6, 2.8, bevel=.8)
    elif kind == "dumplings":
        c.ell(m("#5a4020", .1), 66, 80, 50, 34)
        c.ell(BAMBOO, 64, 76, 50, 34, bevel=2.4)
        c.ell(m("#8a7a4a", .12, 2), 64, 72, 42, 26, bevel=1.0)
        for y in range(54, 92, 6):
            c.scratch(.7, .3, (28, y), (100, y))
        for dx, dy in ((-20, -6), (2, -10), (22, -4), (-12, 10), (12, 12)):
            x, y = 64 + dx, 72 + dy
            c.ell(m("#3a3020", .1), x + 2, y + 3, 11, 8)
            c.ell(DOUGH, x, y, 11, 8, bevel=2.0)
            for k in (-4, 0, 4):
                c.scratch(.8, .4, (x + k, y - 7), (x + k * .6, y - 2), color=(.6, .55, .45))
        c.ell(m("#2a1a14", .08, spec=.8), 104, 98, 9, 6, bevel=1.0)
    elif kind == "pie":
        c.ell(m("#3a3a3a", .1), 66, 80, 48, 30)
        c.ell(PEWTER, 64, 76, 48, 30, bevel=2.2)
        c.ell(CRUST, 64, 72, 40, 24, bevel=2.6)
        for k in range(18):
            a = k * 2 * math.pi / 18
            c.ell(m("#b07a2e", .1), 64 + 38 * math.cos(a), 72 + 22 * math.sin(a), 4, 3, bevel=.8)
        for dx in (-10, 0, 10):
            c.scratch(1.2, .5, (64 + dx - 3, 64), (64 + dx + 3, 70))
        c.poly(m("#6a2a18", .12), (64, 72), (98, 64), (98, 82), bevel=.8)
        c.glow(52, 62, 18, "#fff0c0", .2)
    return c.image()


@painter
def goods(kind="oil"):
    c = Canvas(128, seed=126)
    if kind == "oil":
        glaze = m("#5a6a2a", .08, 2, spec=.8, tint="#3a4a1a")
        c.poly(glaze, (64, 120), (48, 112), (36, 84), (40, 54), (52, 40), (76, 40), (88, 54), (92, 84), (80, 112), bevel=2.6, cyl=(36, 92))
        c.rect(glaze, 56, 18, 72, 42, 3, bevel=1.6, cyl=(56, 72))
        c.ell(m("#c9b27a", .1), 64, 18, 10, 4, bevel=1.0)
        for s in (-1, 1):
            c.line(glaze, 4, (64 + s * 8, 26), (64 + s * 22, 30), (64 + s * 20, 48))
        c.line(m("#3a2a1a", .1), 1.6, (44, 80), (84, 70))
        for x, y in ((50, 78), (60, 75), (70, 72), (78, 70)):
            c.ell(OLIVE, x, y - 3, 4, 2, bevel=.6)
        c.glow(52, 64, 18, "#ffffff", .2)
    elif kind == "teabrick":
        c.rect(m("#1a100a", .1), 22, 38, 110, 102, 4)
        c.rect(TEA_DARK, 18, 32, 106, 96, 4, bevel=2.4)
        c.ell(m("#4a2e1e", .14), 62, 64, 22, 22, bevel=1.2)
        _dragon(_At(c, .36, 62, 64))
        c.line(m("#c9b27a", .1), 1.8, (18, 52), (106, 52))
        c.line(m("#c9b27a", .1), 1.8, (40, 32), (40, 96))
        c.rect(IMP_RED, 82, 70, 98, 90, 2, bevel=1.0)
    elif kind in ("silk", "tweed"):
        cloth = m("#a8322a", .06, 2, spec=.6) if kind == "silk" else TWEED
        c.rect(m("#2a1a10", .1), 24, 54, 112, 104, 20)
        c.rect(cloth, 18, 46, 104, 96, 22, bevel=2.4, cyl=(18, 104))
        c.ell(m("#7a2018", .1) if kind == "silk" else m("#4a4a34", .14), 100, 71, 10, 25, bevel=1.6)
        c.ell(m("#d8cba8", .06), 100, 71, 4, 8)
        if kind == "silk":
            for x in range(26, 92, 18):
                c.line(SILK_GOLD, 1.4, (x, 60), (x + 6, 56), (x + 12, 60))
                c.line(SILK_GOLD, 1.0, (x + 6, 56), (x + 6, 66))
            c.poly(cloth, (30, 96), (52, 96), (48, 116), (26, 112), bevel=1.6)
        else:
            for x in range(24, 98, 10):
                c.line(m("#8a3a2a", .1), 1.0, (x, 50), (x, 92), bevel=.3)
            for y in range(54, 92, 10):
                c.line(m("#2e3a4a", .1), 1.0, (22, y), (98, y), bevel=.3)
    return c.image()


# ================================================================== relics and artifacts
_relic_old = heirs_art3.relic


@painter
def relic(kind="eagle"):
    if kind not in ("scroll", "jade", "drum"):
        return _relic_old(kind=kind)
    c = Canvas(128, seed=127)
    if kind == "scroll":
        c.rect(m("#2a1810", .1), 18, 62, 116, 116, 6)
        c.rect(CEDAR, 14, 56, 110, 110, 6, bevel=2.4)
        c.rect(m("#5a321e", .12), 20, 62, 104, 104, 4, bevel=1.0)
        for i, (x, y, rot) in enumerate(((30, 70, 0), (54, 66, 1), (78, 72, 0), (42, 86, 1), (70, 88, 0))):
            c.rect(PARCH, x - 4, y - 12 + rot * 4, x + 22, y + 4 + rot * 4, 8, bevel=1.6)
            c.ell(m("#c9b78c", .08), x + 22, y - 4 + rot * 4, 4, 8, bevel=1.0)
            c.ell(m("#8e1f1a", .2), x + 9, y - 4 + rot * 4, 3.4, 3.0, bevel=1.0)
        c.poly(CEDAR, (14, 56), (110, 56), (100, 22), (24, 22), bevel=2.0)
        c.rect(BRONZE, 54, 50, 70, 60, 2, bevel=1.0)
        c.ell(m("#7a6a3a", .14, 2, spec=.8), 92, 98, 12, 9, bevel=1.6)
        c.ell(GOLD, 92, 97, 4, 4, bevel=.8)
    elif kind == "jade":
        c.rect(m("#1a2a20", .1), 30, 70, 104, 118, 4)
        c.rect(JADE, 26, 64, 98, 112, 4, bevel=2.6)
        _knob(c, 0)
        c.line(m("#0e1a12", .1), 1.2, (96, 66), (86, 80), (90, 92), (82, 110), bevel=.4)
        c.ell(m("#8e1f1a", .1, 2), 86, 110, 10, 4, bevel=1.0)
        c.glow(44, 80, 20, "#ffffff", .2)
    else:  # dented drum
        c.ell(m("#2a2018", .1), 66, 96, 44, 18)
        c.rect(m("#8a7a4a", .14, 2, spec=.6, tint="#5a4a2a"), 22, 44, 106, 96, 6, bevel=2.4, cyl=(22, 106))
        c.ell(DRUM_SKIN, 64, 44, 42, 13, bevel=1.6)
        c.line(m("#3a2a1a", .1), 1.4, (40, 40), (60, 48), (72, 42))
        for y in (44, 96):
            c.line(m("#5a1a16", .12), 5, *[(64 + 42 * math.cos(t), y + 13 * math.sin(t)) for t in np.linspace(0, math.pi, 20)])
        for k in range(7):
            x0 = 26 + k * 12
            c.line(m("#d8cfb8", .1), 1.2, (x0, 52), (x0 + 6, 90))
            c.line(m("#d8cfb8", .1), 1.2, (x0 + 12, 52), (x0 + 6, 90))
        _lion(_At(c, .34, 64, 70))
        c.ell(m("#3a2a1a", .1), 88, 64, 6, 9)
        c.scratch(2.0, .45, (34, 60), (40, 80))
    return c.image()


def _knob(c, dy, eye=None):
    """A crouching dragon carved on top of a seal block: arched back, raised head on the left, tail curling right."""
    path = _spline([(84, 62 + dy), (92, 54 + dy), (84, 44 + dy), (66, 40 + dy), (50, 44 + dy), (40, 52 + dy)], 6)
    _tube(c, JADE_L, path, 3, 10, bevel=2.4)
    for x in (48, 74):
        c.ell(JADE_L, x, 60 + dy, 5, 4, bevel=1.2)
    c.ell(JADE_L, 36, 46 + dy, 10, 8, bevel=2.0)
    c.poly(JADE_L, (28, 46 + dy), (20, 50 + dy), (28, 54 + dy), bevel=1.0)
    c.line(JADE, 1.8, (40, 40 + dy), (46, 30 + dy))
    c.line(JADE, 1.8, (34, 39 + dy), (36, 29 + dy))
    c.ell(eye or m("#8e1f1a", .08), 34, 44 + dy, 1.6, 1.6)
    for i in range(6, len(path) - 4, 4):
        x, y = path[i]
        c.poly(JADE, (x - 3, y - 6), (x, y - 12), (x + 3, y - 6), bevel=.6)


@painter
def owl_aegis():
    c = Canvas(128, seed=128)
    for k in range(16):
        a = k * 2 * math.pi / 16
        x, y = 64 + 54 * math.cos(a), 64 + 54 * math.sin(a)
        c.line(m("#5a6a3a", .12, spec=.6), 2.2, (64 + 48 * math.cos(a), 64 + 48 * math.sin(a)), (x, y), (x + 4 * math.sin(a), y - 4 * math.cos(a)))
    c.ell(BRONZE, 64, 64, 50, 50, bevel=2.8)
    for row in range(6):
        r = 44 - row * 6
        for k in range(12 + row * 2):
            a = k * 2 * math.pi / (12 + row * 2) + row * .2
            c.scratch(.7, .35, (64 + r * math.cos(a - .1), 64 + r * math.sin(a - .1)), (64 + (r - 3) * math.cos(a), 64 + (r - 3) * math.sin(a)),
                      (64 + r * math.cos(a + .1), 64 + r * math.sin(a + .1)), color=(.3, .2, .08))
    c.ell(HELLAS_BLUE, 64, 64, 28, 28, bevel=1.6)
    ring(c, 64, 64, 29, GOLD, 2.4)
    _owl(_At(c, .5, 64, 66))
    return _halo(c.image(), (255, 220, 140, 255), 6, .7)


@painter
def dragon_seal():
    c = Canvas(128, seed=129)
    c.ell(m("#5a1612", .1), 70, 104, 38, 12)
    c.ell(m("#b02a20", .08, 2), 68, 100, 36, 11, bevel=1.4)
    c.rect(m("#1a2a20", .1), 30, 64, 100, 108, 4)
    c.rect(JADE, 26, 58, 94, 102, 4, bevel=2.6)
    c.line(SILK_GOLD, 2.0, (92, 60), (82, 74), (86, 86), (78, 100), bevel=.6)
    _knob(c, -6, eye=GOLD)
    for x in range(30, 94, 9):
        c.scratch(.8, .35, (x, 96), (x + 4, 100), color=(.1, .2, .14))
    return _halo(c.image(), (140, 230, 170, 255), 7, .8)


@painter
def war_drum():
    c = Canvas(128, seed=130)
    c.ell(m("#2a2018", .1), 66, 100, 46, 16)
    c.rect(BRASS, 20, 46, 108, 98, 6, bevel=2.4, cyl=(20, 108))
    for k in range(8):
        x0 = 24 + k * 11
        c.line(FACING, 1.4, (x0, 54), (x0 + 5.5, 92))
        c.line(FACING, 1.4, (x0 + 11, 54), (x0 + 5.5, 92))
    for y in (48, 96):
        c.line(m("#8c1c22", .08), 6, *[(64 + 44 * math.cos(t), y + 14 * math.sin(t)) for t in np.linspace(0, math.pi, 22)])
    c.ell(DRUM_SKIN, 64, 46, 43, 14, bevel=1.6)
    c.ell(m("#8c1c22", .08), 64, 72, 15, 15, bevel=1.4)
    _lion(_At(c, .3, 64, 73))
    for (x0, y0, x1, y1) in ((40, 22, 60, 42), (90, 20, 72, 42)):
        c.line(m("#d8c8a0", .08, spec=.4), 3.2, (x0, y0), (x1, y1))
        c.ell(m("#efe6cc", .05), x0, y0, 3.4, 3.4, bevel=1.0)
    return _halo(c.image(), (255, 190, 120, 255), 6, .7)
