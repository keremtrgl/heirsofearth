"""Heirs of Earth 3.0c painters: the World Council.
The council hall (5x5): a stepped octagonal stone dais, a ring table of polished dark wood with a gold rim around a
mosaic of this world, nine envoy chairs with cushions in the nation colours and nine banners on the rim.
Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module after heirs_art8.
"""
import math

import numpy as np

from heirs_art import GOLD, Canvas, m, painter
from heirs_art7 import GOLD_D

# ------------------------------------------------------------------ materials
STONE = m("#b9b0a2", .12, 3, spec=.25)
STONE_L = m("#d2cabb", .10, 3, spec=.3)
STONE_D = m("#7d766c", .14, 3)
WOOD = m("#4a2c1c", .12, 3, (1, 8), spec=.55)
WOOD_D = m("#2e1a10", .12, 3, (1, 8))
SEA = m("#2f5c86", .10, 2, spec=.4, tint="#4d86b0")
LAND = m("#6f8a4a", .14, 1.5, tint="#a8915a")
SAND = m("#c7ad74", .12, 1.5)
POLE = m("#3a2a1e", .10, 2, (1, 4))

# The nine heirs in the order of their research columns, as banner colours.
NATIONS = ("#8f2924", "#3a3f5e", "#3b5866", "#2e5c8c", "#a3241f", "#8c1a1f", "#cc9e3d", "#9e1f2b", "#c74f29")


def _ring(cx, cy, r, n, start=-90.0):
    return [(cx + r * math.cos(math.radians(start + k * 360.0 / n)), cy + r * math.sin(math.radians(start + k * 360.0 / n))) for k in range(n)]


def _quad(cx, cy, ang, w, h):
    """A rectangle of w (across) by h (along the radius) centred on (cx, cy), turned to face the angle."""
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for u, v in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        out.append((cx + v * ca - u * sa, cy + v * sa + u * ca))
    return out


@painter
def council_hall(size=(5, 5)):
    W = 640
    c = Canvas(W, W, seed=901)
    cx, cy = 320, 316
    rng = np.random.default_rng(91)

    # stepped octagonal dais with a soft ground shadow
    c.poly(m("#1c1712", .05), *_ring(cx + 10, cy + 14, 312, 8, -67.5))
    c.poly(STONE_D, *_ring(cx, cy, 308, 8, -67.5), bevel=3.0)
    c.poly(STONE, *_ring(cx, cy, 292, 8, -67.5), bevel=2.6)
    c.poly(STONE_L, *_ring(cx, cy, 250, 8, -67.5), bevel=2.2)
    # paving joints: radial seams and two rings of slabs
    for k in range(24):
        a = math.radians(k * 15 + 7.5)
        c.scratch(1.2, .35, (cx + 160 * math.cos(a), cy + 160 * math.sin(a)), (cx + 288 * math.cos(a), cy + 288 * math.sin(a)))
    for r in (200, 248):
        pts = _ring(cx, cy, r, 8, -67.5)
        for k in range(8):
            c.scratch(1.2, .35, pts[k], pts[(k + 1) % 8])
    c.poly(STONE_D, *_ring(cx, cy, 232, 8, -67.5), bevel=1.6)
    c.poly(STONE_L, *_ring(cx, cy, 222, 8, -67.5), bevel=1.6)
    for k, (x, y) in enumerate(_ring(cx, cy, 227, 48)):
        c.ell(GOLD_D if k % 2 else GOLD, x, y, 2.2, 2.2, bevel=.6)
    for _ in range(26):
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(170, 280)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        c.scratch(.8, .14, (x, y), (x + rng.uniform(-9, 9), y + rng.uniform(-6, 6)))

    # nine envoy chairs, set out before the table so the table rim overlaps their fronts
    for k, (x, y) in enumerate(_ring(cx, cy, 186, 9)):
        ang = math.atan2(y - cy, x - cx)
        bx, by = cx + 206 * math.cos(ang), cy + 206 * math.sin(ang)
        c.poly(WOOD_D, *_quad(bx, by, ang, 46, 12), bevel=1.4)
        c.poly(WOOD, *_quad(x, y, ang, 40, 34), bevel=1.6)
        c.poly(m(NATIONS[k], .10, 1.5, spec=.3), *_quad(x - 2 * math.cos(ang), y - 2 * math.sin(ang), ang, 30, 24), bevel=2.0)

    # the ring table: dark wood, a gold rim outside and in, then the world mosaic in the middle
    c.ell(m("#140e0a", .05), cx + 6, cy + 9, 164, 164)
    c.ell(GOLD_D, cx, cy, 162, 162, bevel=2.0)
    c.ell(WOOD, cx, cy, 156, 156, bevel=3.2)
    for k in range(36):
        a = math.radians(k * 10)
        c.scratch(.9, .18, (cx + 92 * math.cos(a), cy + 92 * math.sin(a)), (cx + 152 * math.cos(a + .05), cy + 152 * math.sin(a + .05)), color=(.08, .04, .02))
    for k, (x, y) in enumerate(_ring(cx, cy, 128, 9)):
        c.ell(GOLD, x, y, 7, 7, bevel=1.2)
        c.ell(m(NATIONS[k], .06, 1.5, spec=.5), x, y, 4, 4, bevel=.8)
    c.ell(GOLD, cx, cy, 94, 94, bevel=1.6)
    c.ell(SEA, cx, cy, 86, 86, bevel=2.4)
    # continents of the world map: irregular coastlines, a desert belt and two ice caps
    def coast(x0, y0, r, seed, squash=1.0):
        g = np.random.default_rng(seed)
        ph = g.uniform(0, 2 * math.pi, 4)
        pts = []
        for k in range(48):
            t = k * 2 * math.pi / 48
            rr = r * (1 + .22 * math.sin(2 * t + ph[0]) + .14 * math.sin(3 * t + ph[1]) + .08 * math.sin(5 * t + ph[2]) + .05 * math.sin(9 * t + ph[3]))
            pts.append((x0 + rr * math.cos(t), y0 + rr * squash * math.sin(t)))
        return pts
    c.ell(m("#e8eef2", .05, 2), cx, cy - 78, 26, 7, bevel=1.0)
    c.ell(m("#e8eef2", .05, 2), cx + 4, cy + 79, 22, 6, bevel=1.0)
    for (dx, dy, r, sd, sq) in ((-34, -24, 26, 1, .8), (26, -34, 18, 2, .7), (32, 14, 28, 3, .85), (-26, 32, 20, 4, .7), (-58, 4, 11, 5, 1.4), (8, 50, 12, 6, .7)):
        c.poly(LAND, *coast(cx + dx, cy + dy, r, sd, sq), bevel=1.6)
    for (dx, dy, r, sd, sq) in ((32, 18, 13, 7, .6), (-26, 34, 9, 8, .6), (-30, -18, 9, 9, .7)):
        c.poly(SAND, *coast(cx + dx, cy + dy, r, sd, sq), bevel=1.0)
    for (dx, dy) in ((-40, -30), (20, -38), (40, 6)):
        c.ell(m("#5a6a3a", .1, 1.5), cx + dx, cy + dy, 5, 3, bevel=.8)
    # nine settlement marks and the routes between them, in gold
    marks = [(cx - 40, cy - 30), (cx + 22, cy - 42), (cx + 40, cy + 8), (cx + 18, cy + 22), (cx - 30, cy + 30),
             (cx - 54, cy + 4), (cx + 6, cy + 50), (cx - 10, cy - 12), (cx + 50, cy - 20)]
    for a_, b_ in ((0, 7), (7, 1), (1, 8), (8, 2), (2, 3), (3, 6), (3, 4), (4, 5), (5, 0), (7, 3)):
        c.scratch(1.4, .7, marks[a_], marks[b_], color=(.92, .74, .3))
    for k, (x, y) in enumerate(marks):
        c.ell(m(NATIONS[k], .05, 1.5, spec=.6), x, y, 4.2, 4.2, bevel=.8)
    c.glow(cx - 30, cy - 34, 70, "#cfe6ff", .22)

    # nine banners on the rim of the dais: swallow-tailed cloths hanging outward from gold-capped poles
    for k, (x, y) in enumerate(_ring(cx, cy, 258, 9)):
        ang = math.atan2(y - cy, x - cx)
        ca, sa = math.cos(ang), math.sin(ang)
        tx, ty = -sa, ca
        p0 = (x + 2 * ca, y + 2 * sa)
        L, Wd = 58, 17

        def at(u, v):
            return (p0[0] + u * ca + v * tx, p0[1] + u * sa + v * ty)
        cloth = [at(0, Wd), at(0, -Wd), at(L * .5, -Wd + 1.5), at(L, -Wd + 2), at(L - 15, 0), at(L, Wd - 2), at(L * .5, Wd - 1.5)]
        c.poly(m("#1a1410", .05), *[(px + 5, py + 7) for px, py in cloth])
        c.poly(m(NATIONS[k], .12, 1.5, (1, 3), spec=.3), *cloth, bevel=2.2)
        for u in (14, 30, 44):
            c.scratch(1.6, .28, at(u, -Wd + 2), at(u + 3, Wd - 2))
        c.line(GOLD_D, 1.6, at(4, -Wd + 3), at(L - 1, -Wd + 3.5))
        c.line(GOLD_D, 1.6, at(4, Wd - 3), at(L - 1, Wd - 3.5))
        c.ell(GOLD, *at(22, 0), 6, 6, bevel=1.2)
        c.ell(m(NATIONS[k], .05, 1.5, spec=.6), *at(22, 0), 3, 3, bevel=.6)
        c.line(POLE, 4.0, at(0, -Wd - 4), at(0, Wd + 4))
        c.ell(GOLD, *at(0, -Wd - 4), 3.2, 3.2, bevel=.8)
        c.ell(GOLD, *at(0, Wd + 4), 3.2, 3.2, bevel=.8)
        c.ell(POLE, x - 2 * ca, y - 2 * sa, 7.5, 7.5, bevel=1.4)
        c.ell(GOLD, x - 2 * ca, y - 2 * sa, 4.2, 4.2, bevel=1.0)

    c.glow(cx - 150, cy - 160, 260, "#fff2d6", .16)
    return c.image()
