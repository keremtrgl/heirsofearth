"""Heirs of Earth 3.0 painters: the Inti Empire.

Emblem (condor), weapons (sling, star mace, mountain carbine), armour icons (torso5, helmet5), buildings (qullqa,
quipu table, sun stone), floor (terraces), food5, relic5, the Golden Thread and the sling stone projectile.
Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module after heirs_art7.
"""
import math

import numpy as np

from heirs_art import BRONZE, DARKIRON, EMBLEMS, GOLD, Canvas, axis, finish_floor, floor_canvas, haft, m, painter, shade
from heirs_art3 import _halo
from heirs_art4 import BRASS, _spline, _tube
from heirs_art7 import GOLD_D, _closed

# ------------------------------------------------------------------ materials
TERRA = m("#c8502a", .08, 2, spec=.5, tint="#6a2410")
TERRA_D = m("#7a2a14", .10, 2)
JUNGLE = m("#2e6a46", .08, 2, spec=.4)
BLACK_F = m("#1c1c20", .10, 2, spec=.5)
BLACK_F2 = m("#2c2c32", .10, 2, spec=.4)
WHITE_F = m("#ece8dc", .06, 2, spec=.4)
WOOL_R = m("#b0302a", .10, 1.5, (1, 4))
WOOL_Y = m("#e0a82a", .10, 1.5, (1, 4))
WOOL_W = m("#ece4d0", .08, 1.5, (1, 4))
WOOL_K = m("#262426", .10, 1.5, (1, 4))
HARDWOOD = m("#5a3622", .14, 3, (1, 9), spec=.4)
GRANITE = m("#8a8480", .16, 2.5, spec=.3)
GRANITE_D = m("#5e5854", .16, 2.5)
THATCH = m("#c4a25a", .16, 1.5, (1, 6))
CANE = m("#b8955a", .12, 1.5, (6, 1))


# ================================================================== emblem
def _feather(c, base, tip, w, mat, vein=(.85, .85, .85)):
    bx, by = base
    tx, ty = tip
    dx, dy = tx - bx, ty - by
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    mid = (bx + dx * .5, by + dy * .5)
    c.poly(mat, (bx + nx * w * .7, by + ny * w * .7), (mid[0] + nx * w, mid[1] + ny * w), (tx, ty),
           (mid[0] - nx * w, mid[1] - ny * w), (bx - nx * w * .7, by - ny * w * .7), bevel=.9)
    c.scratch(.6, .35, (bx, by), (bx + dx * .85, by + dy * .85), color=vein)


def _condor(c):
    """An Andean condor displayed: long straight-edged black wings, a white panel of secondaries along the trailing edge,
    finger primaries spread wide at the tips, a white ruff and a small bald head in profile."""
    for flip in (False, True):
        fx = (lambda p: (128 - p[0], p[1])) if flip else (lambda p: p)
        wing = [(60, 47), (38, 40), (35, 44), (36, 57), (46, 61), (60, 63)]
        c.poly(m("#2a0a06", .1), *[fx((x + .8, y + 1.4)) for x, y in wing])
        c.poly(BLACK_F, *[fx(p) for p in wing], bevel=1.6)
        for k in range(4):
            c.scratch(.7, .5, fx((58, 48 + k * 2)), fx((40, 42 + k * 3.4)), color=(.4, .4, .46))
        # white secondaries: a band of feather tips along the trailing edge
        for k in range(7):
            x = 58 - k * 3.2
            base = (x, 53 - k * .2)
            tip = (x - 1.6, 63 - k * .4 + (k % 2) * 1.2)
            _feather(c, fx(base), fx(tip), 1.9, WHITE_F, vein=(.55, .55, .5))
        # finger primaries fanning out from the wing tip, each outlined in the field colour so they read as separate fingers
        for k in range(5):
            base = (37.5, 41 + k * 4)
            a = math.radians(163 + k * 18)
            ln = 16 - abs(k - 1.5) * 1.2
            tip = (base[0] + ln * math.cos(a), base[1] + ln * math.sin(a))
            _feather(c, fx(base), fx((tip[0] + .6 * math.cos(a), tip[1] + .6 * math.sin(a))), 2.5, TERRA, vein=(.6, .25, .1))
            _feather(c, fx(base), fx(tip), 1.7, BLACK_F2 if k % 2 else BLACK_F, vein=(.55, .55, .6))
    tail = [(58, 82), (70, 82), (74, 97), (64, 100), (54, 97)]
    c.poly(BLACK_F2, *tail, bevel=1.2)
    for x in (59, 64, 69):
        c.line(m("#4a4a52", .1), .9, (64, 84), (x + (x - 64) * .5, 98))
    c.poly(BLACK_F, *_closed([(64, 47), (70, 55), (71, 69), (67, 83), (61, 83), (57, 69), (58, 55)], 5), bevel=1.8)
    for row in range(4):
        for x in range(60 + (row % 2) * 2, 69, 4):
            c.scratch(.7, .45, (x - 1.4, 59 + row * 6), (x, 61 + row * 6), (x + 1.4, 59 + row * 6), color=(.4, .4, .48))
    for x in (61, 67):
        c.line(m("#8a8478", .08), 1.8, (x, 83), (x + (x - 64) * .6, 89))
        for k in (-1, 0, 1):
            c.line(GOLD_D, 1.0, (x + (x - 64) * .6, 89), (x + (x - 64) * .6 + k * 2.2, 92))
    # white ruff
    c.ell(m("#2a2a30", .1), 64, 46, 7.5, 3.6)
    for k in range(6):
        a = math.pi * (.08 + .84 * k / 5)
        c.ell(WHITE_F, 64 - 6.6 * math.cos(a), 46 + 2.0 * math.sin(a), 2.5, 2.3, bevel=.7)
    # small bald head in profile facing left, comb on top, hooked pale beak
    hd = lambda pts: [(58 + (x - 58) * .72, 40 + (y - 40) * .72) for x, y in pts]
    skin = m("#7a4a44", .10, 2, spec=.5)
    c.poly(skin, *hd(_closed([(66, 44), (66, 35), (61, 30), (54, 30), (50, 34), (51, 40), (57, 44)], 4)), bevel=1.1)
    c.poly(m("#3a2020", .1), *hd(_closed([(52, 31), (54, 25), (59, 23), (63, 26), (61, 30), (56, 31)], 3)), bevel=.7)
    c.poly(m("#e0d0a8", .06, spec=.6), *hd([(51, 33), (45, 33), (41, 36), (42, 40), (44, 38), (50, 39)]), bevel=.5)
    c.poly(m("#3a3028", .08), *hd([(42, 40), (41, 36), (43, 35.5)]), bevel=.3)
    ex, ey = hd([(56, 34)])[0]
    c.ell(TERRA_D, ex, ey, 1.3, 1.2)
    c.ell(m("#ffffff", .02), ex - .4, ey - .4, .4, .4)


EMBLEMS["condor"] = _condor


# ================================================================== weapons
@painter
def sling():
    """A braided wool sling hanging in a loop: black and white cords, a woven diamond cradle with a stone, a finger loop and a tassel."""
    c = Canvas(128, seed=501)
    left = _spline([(26, 16), (24, 40), (30, 66), (44, 88), (58, 100)], 6)
    right = _spline([(32, 16), (44, 36), (60, 58), (72, 80), (76, 98)], 6)
    for cord in (left, right):
        for i in range(len(cord) - 1):
            c.line(WOOL_K if i % 2 else WOOL_W, 2.4, cord[i], cord[i + 1])
    cradle = _closed([(58, 100), (66, 92), (76, 98), (74, 110), (64, 116), (56, 110)], 4)
    c.poly(m("#1a1410", .1), *[(x + 1, y + 2) for x, y in cradle])
    c.poly(WOOL_R, *cradle, bevel=1.4)
    for k in range(5):
        c.line(WOOL_Y, 1.0, (60 + k * 3, 98 + k * 2), (58 + k * 3, 112 - k * .5))
    c.poly(WOOL_W, (66, 98), (72, 104), (66, 110), (60, 104), bevel=.6)
    c.ell(m("#8a8a86", .14, 2, spec=.5), 66, 104, 4.6, 3.8, bevel=1.4)
    c.ell(m("#c8c8c4", .04), 64.6, 102.8, 1.4, 1.0)
    # finger loop on the left cord and a tassel on the release cord
    for k in range(10):
        a = k * 2 * math.pi / 10
        c.line(WOOL_K if k % 2 else WOOL_W, 2.2, (26 + 6 * math.cos(a), 12 + 5 * math.sin(a)),
               (26 + 6 * math.cos(a + .63), 12 + 5 * math.sin(a + .63)))
    for k in range(6):
        c.line(WOOL_R if k % 2 else WOOL_Y, 1.4, (32, 16), (36 + k * 1.6, 30 + abs(k - 2.5) * 1.2))
    c.ell(WOOL_R, 33, 18, 3.0, 3.0, bevel=.8)
    return c.image()


@painter
def champi():
    """The star mace: a hardwood staff bound with cord, a bronze collar and a six-pointed bronze star head."""
    c = Canvas(128, seed=502)
    at, ln = axis((16, 116), (104, 26))
    haft(c, at, 0, ln - 8, 2.6, HARDWOOD, bevel=1.0)
    for u in range(4, 26, 3):
        c.line(WOOL_R if (u // 3) % 2 else WOOL_Y, 1.4, at(u, -2.8), at(u + 1.2, 2.8))
    c.poly(BRONZE, at(ln - 16, -3.4), at(ln - 12, -3.4), at(ln - 12, 3.4), at(ln - 16, 3.4), bevel=.8)
    cx, cy = at(ln - 2, 0)
    star = []
    for k in range(12):
        a = k * math.pi / 6 + .3
        r = 15 if k % 2 == 0 else 6.5
        star.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    c.poly(m("#2a1a10", .1), *[(x + 1.4, y + 2) for x, y in star])
    c.poly(m("#c48a3a", .06, 2, spec=1.2, tint="#6a3a12"), *star, bevel=2.2)
    for k in range(6):
        a = k * math.pi / 3 + .3
        c.line(m("#e8b870", .03, spec=1.4), 1.0, (cx + 3 * math.cos(a), cy + 3 * math.sin(a)), (cx + 12 * math.cos(a), cy + 12 * math.sin(a)))
    c.ell(BRONZE, cx, cy, 4.2, 4.2, bevel=1.2)
    c.glow(cx - 4, cy - 5, 10, "#fff0c8", .25)
    return c.image()


@painter
def mountain_carbine():
    """A short carbine: dark wood stock, short barrel with a front band, brass butt plate, gold condor on the lock and a leather sling."""
    c = Canvas(128, seed=503)
    at, ln = axis((14, 100), (114, 34))
    stock = m("#5a3622", .14, 3, (9, 1), spec=.4)
    c.line(m("#6a4428", .12), 2.4, *[at(u, 6 + 10 * math.sin(math.pi * (u - 6) / 64)) for u in range(6, 72, 4)])
    c.poly(stock, at(0, -5), at(10, -4.6), at(26, -2.6), at(70, -2.2), at(70, 2.6), at(26, 3.2), at(10, 7.6), at(0, 8), bevel=1.6)
    c.poly(BRASS, at(-1, -5), at(2, -5), at(2, 8), at(-1, 8), bevel=.8)
    c.poly(m("#3e4246", .08, 3, (9, 1), spec=1.0), at(26, -1.8), at(ln, -1.6), at(ln, 1.6), at(26, 1.8), bevel=.8)
    c.poly(m("#3e4246", .08, 3, spec=.9), at(24, -3.4), at(38, -3.4), at(38, 3.6), at(24, 3.6), bevel=1.0)
    c.ell(GOLD, *at(31, 0), 2.6, 2.4, bevel=.8)
    c.line(BLACK_F, 1.0, at(29.4, -.4), at(31, .8), at(32.6, -.4))
    c.line(DARKIRON, 1.6, at(35, -3), at(33, -7), at(37, -8))
    c.line(DARKIRON, 1.4, at(27, 3.6), at(25, 7), at(20, 7.4))
    for u in (60, ln - 6):
        c.line(BRASS, 1.8, at(u, -2.6), at(u, 2.8))
    c.poly(DARKIRON, at(ln - 4, -2.2), at(ln - 3, -3.4), at(ln - 2, -2.2), bevel=.3)
    return c.image()


@painter
def sling_stone():
    c = Canvas(128, seed=504)
    c.ell(m("#7a7670", .14, 2, spec=.6), 64, 64, 9, 7, bevel=1.6)
    c.ell(m("#c8c4bc", .04), 61, 61.5, 2.6, 1.6)
    return c.image()


# ================================================================== apparel icons
@painter
def torso5(kind="unku"):
    c = Canvas(128, seed=505)
    if kind == "unku":
        # the classic black-and-white chequered unku with a red stepped yoke and a band of tocapu squares
        body = [(26, 22), (102, 22), (98, 118), (30, 118)]
        c.poly(m("#1a1410", .1), *[(x + 1, y + 2) for x, y in body])
        c.poly(WOOL_W, *body, bevel=2.0)
        for i in range(12):
            for j in range(8):
                if (i + j) % 2:
                    x, y = 30 + i * 5.7, 76 + j * 5.2
                    c.rect(WOOL_K, x, y, x + 5.7, y + 5.2, 0, clip=True)
        for i in range(12):
            for j in range(4):
                if (i + j) % 2:
                    x, y = 29 + i * 5.9, 24 + j * 5.2
                    c.rect(WOOL_K, x, y, x + 5.9, y + 5.2, 0, clip=True)
        yoke = [(44, 22), (84, 22), (84, 30), (78, 30), (78, 38), (72, 38), (72, 46), (56, 46), (56, 38), (50, 38), (50, 30), (44, 30)]
        c.poly(WOOL_R, *yoke, bevel=1.2)
        c.poly(m("#2a1a10", .1), (58, 22), (70, 22), (64, 36), bevel=.6)
        motifs = (WOOL_Y, WOOL_R, JUNGLE, WOOL_K)
        for i in range(10):
            x0, y0 = 31 + i * 6.6, 54
            c.rect(motifs[i % 4], x0, y0, x0 + 6.2, y0 + 14, 0, bevel=.5)
            inner = (WOOL_W, WOOL_Y, WOOL_R, WOOL_W)[i % 4]
            if i % 3 == 0:
                c.rect(inner, x0 + 1.6, y0 + 3, x0 + 4.6, y0 + 11, 0)
            elif i % 3 == 1:
                c.poly(inner, (x0 + 1, y0 + 12), (x0 + 1, y0 + 7), (x0 + 3, y0 + 7), (x0 + 3, y0 + 3), (x0 + 5.4, y0 + 3), (x0 + 5.4, y0 + 12))
            else:
                c.line(inner, 1.2, (x0 + 1, y0 + 2), (x0 + 5.4, y0 + 7), (x0 + 1, y0 + 12))
        for y in (53, 69):
            c.line(WOOL_R, 1.6, (30, y), (98, y))
        for x in range(32, 98, 4):
            c.line(WOOL_R, 1.4, (x, 118), (x + .6, 122))
        c.glow(46, 40, 24, "#fff4e0", .12)
    elif kind == "quilted":
        # thick cream quilting with diamond stitches, faced with a red-and-black chequer band at chest and hem
        body = [(30, 18), (52, 16), (64, 24), (76, 16), (98, 18), (108, 34), (100, 50), (96, 46), (96, 112), (32, 112), (32, 46), (28, 50), (20, 34)]
        c.poly(m("#1a1410", .1), *[(x + 1, y + 2) for x, y in body])
        c.poly(m("#e2d6b8", .06, 2), *body, bevel=2.4)
        for i in range(-4, 16):
            for j in range(-2, 16):
                x, y = 14 + i * 9 + (j % 2) * 4.5, 14 + j * 7
                c.poly(m("#e8dcc0", .06, 2), (x, y - 5), (x + 4.4, y), (x, y + 5), (x - 4.4, y), bevel=1.6, clip=True)
        for y0, rows in ((50, 3), (98, 2)):
            for j in range(rows):
                for i in range(12):
                    x = 32 + i * 5.33
                    mat = TERRA if (i + j) % 2 else BLACK_F
                    c.rect(mat, x, y0 + j * 4.6, x + 5.33, y0 + (j + 1) * 4.6, 0, bevel=.4)
        for y in (50, 63.8, 98, 107.2):
            c.line(GOLD_D, 1.0, (32, y), (96, y))
        for x in range(34, 96, 3):
            c.line(m("#ece4d0", .04), 1.4, (x, 112), (x + .8, 120))
        c.poly(m("#5a2a14", .1), (52, 16), (64, 26), (76, 16), (70, 16), (64, 22), (58, 16), bevel=.8)
        c.glow(48, 36, 24, "#fff4e0", .14)
    return c.image()


@painter
def helmet5(kind="plumed"):
    c = Canvas(128, seed=506)
    if kind == "plumed":
        # macaw feather fan behind the crown
        cols = ("#c8282a", "#e8b62a", "#2a6ab0", "#c8282a", "#2e8a4a", "#e8b62a", "#c8282a", "#2a6ab0", "#c8282a")
        for k, col in enumerate(cols):
            a = math.radians(-150 + k * 15)
            base = (64, 52)
            tip = (64 + 48 * math.cos(a), 52 + 44 * math.sin(a))
            _feather(c, base, tip, 4.2, m(col, .06, 2, spec=.6), vein=(.95, .9, .8))
        dome = _closed([(30, 84), (32, 64), (42, 50), (56, 44), (72, 44), (86, 50), (96, 64), (98, 84)], 5)
        c.poly(CANE, *dome, bevel=2.6)
        for k in range(-6, 8):
            c.scratch(.9, .45, (34 + k * 7, 86), (48 + k * 7, 46), color=(.35, .24, .1))
            c.scratch(.9, .45, (34 + k * 7, 46), (48 + k * 7, 86), color=(.35, .24, .1))
        c.rect(BRONZE, 28, 78, 100, 88, 3, bevel=1.4)
        for x in range(32, 98, 7):
            c.ell(m("#e8b870", .03, spec=1.2), x, 83, 1.4, 1.4, bevel=.4)
        c.ell(m("#2a1a10", .1), 65, 66, 11, 11)
        c.ell(GOLD, 64, 64, 11, 11, bevel=1.8)
        for k in range(12):
            a = k * math.pi / 6
            c.line(GOLD_D, 1.0, (64 + 5 * math.cos(a), 64 + 5 * math.sin(a)), (64 + 9.5 * math.cos(a), 64 + 9.5 * math.sin(a)))
        c.ell(m("#f0c860", .04, spec=1.3), 64, 64, 4, 4, bevel=1.0)
        for s in (-1, 1):
            c.line(WOOL_R, 2.2, (64 + s * 34, 88), (64 + s * 30, 104), (64 + s * 22, 112))
        c.glow(56, 56, 20, "#fff4e0", .2)
    return c.image()


# ================================================================== buildings
@painter
def qullqa(size=(2, 2)):
    """A round stone storehouse from above: a ring of fitted fieldstones under a conical thatch roof tied at the peak."""
    W = 256
    c = Canvas(W, W, seed=507)
    cx, cy = 128, 124
    c.ell(m("#1e1a16", .1), cx + 8, cy + 14, 112, 104)
    rng = np.random.default_rng(57)
    for ring_r in (112, 100):
        for k in range(28):
            a0 = k * 2 * math.pi / 28 + (ring_r == 100) * .11
            a1 = a0 + 2 * math.pi / 28 * .92
            r0, r1 = ring_r - 12, ring_r
            pts = [(cx + r1 * math.cos(a0), cy + r1 * .94 * math.sin(a0)), (cx + r1 * math.cos(a1), cy + r1 * .94 * math.sin(a1)),
                   (cx + r0 * math.cos(a1), cy + r0 * .94 * math.sin(a1)), (cx + r0 * math.cos(a0), cy + r0 * .94 * math.sin(a0))]
            c.poly(GRANITE if rng.random() > .3 else GRANITE_D, *pts, bevel=1.4)
    c.ell(m("#2a2018", .1), cx + 4, cy + 6, 90, 84)
    c.ell(THATCH, cx, cy, 90, 84, bevel=3.0)
    for k in range(72):
        a = k * 2 * math.pi / 72 + rng.uniform(-.02, .02)
        r0 = rng.uniform(6, 20)
        col = (.42, .3, .1) if k % 3 else (.95, .85, .55)
        c.scratch(1.0, .5, (cx + r0 * math.cos(a), cy + r0 * .93 * math.sin(a)), (cx + 89 * math.cos(a), cy + 83 * math.sin(a)), color=col)
    for r in (34, 62):
        for k in range(60):
            a0, a1 = k * 2 * math.pi / 60, (k + .7) * 2 * math.pi / 60
            c.line(m("#7a5a2a", .1), 1.4, (cx + r * math.cos(a0), cy + r * .93 * math.sin(a0)), (cx + r * math.cos(a1), cy + r * .93 * math.sin(a1)))
    c.ell(m("#7a5a2a", .12), cx, cy, 10, 9, bevel=1.4)
    c.ell(WOOL_R, cx, cy, 5, 4.6, bevel=1.0)
    c.glow(cx - 34, cy - 34, 50, "#fff4d0", .2)
    for a in (2.3, 3.9):
        x, y = cx + 106 * math.cos(a), cy + 100 * math.sin(a)
        c.rect(m("#141210", .1), x - 5, y - 4, x + 5, y + 4, 1)
    return c.image()


@painter
def quipu_table(size=(2, 1)):
    """A low table seen from above with a quipu laid out on it: a main cord and dozens of coloured pendant cords with knots."""
    W, H = 256, 128
    c = Canvas(W, H, seed=508)
    c.rect(m("#1e1a16", .1), 12, 16, W - 6, H - 4, 8)
    c.rect(m("#6a4428", .14, 3, (9, 1)), 6, 8, W - 12, H - 14, 6, bevel=2.2)
    c.rect(m("#d8c8a0", .06, 2), 16, 16, W - 22, H - 22, 3, bevel=1.0)
    for x in range(20, W - 26, 12):
        c.scratch(.5, .25, (x, 18), (x + 2, H - 24))
    main = [(24, 26), (W - 30, 24)]
    c.line(m("#5a3a22", .1), 4.0, *main, bevel=.8)
    rng = np.random.default_rng(58)
    cols = ("#b0302a", "#e0a82a", "#ece4d0", "#262426", "#2e6a46", "#6a3a8a", "#c86a2a")
    for k in range(30):
        x = 28 + k * 6.9
        ln = rng.uniform(46, 78)
        col = m(cols[rng.integers(0, len(cols))], .08, 1.5)
        pts = [(x, 25), (x + rng.uniform(-3, 3), 25 + ln * .5), (x + rng.uniform(-4, 4), 25 + ln)]
        c.line(col, 1.8, *_spline(pts, 4), bevel=.4)
        for kk in range(rng.integers(1, 5)):
            t = rng.uniform(.25, .95)
            px = pts[0][0] + (pts[2][0] - pts[0][0]) * t
            c.ell(col, px, 25 + ln * t, 2.0, 1.6, bevel=.6)
    c.ell(m("#7a5a2a", .14, 1.5), W - 34, H - 32, 12, 9, bevel=1.6)
    for k in range(4):
        c.ell(m(cols[k], .08, 1.5), W - 38 + k * 3, H - 34 + (k % 2) * 3, 3, 2.4, bevel=.6)
    return c.image()


@painter
def sun_stone(size=(1, 1)):
    """A carved granite outcrop with steps cut into it and a short square post rising from the top."""
    c = Canvas(128, seed=509)
    c.ell(m("#1e1a16", .1), 70, 104, 50, 14)
    rock = _closed([(18, 96), (16, 74), (26, 56), (46, 48), (76, 46), (102, 54), (112, 76), (108, 98), (78, 106), (44, 106)], 5)
    c.poly(GRANITE_D, *rock, bevel=2.6)
    c.poly(GRANITE, (30, 70), (36, 58), (90, 56), (100, 70), (96, 84), (34, 86), bevel=2.0)
    for k, (x0, x1, y) in enumerate(((26, 46, 92), (30, 46, 84), (34, 46, 76))):
        c.rect(GRANITE if k % 2 else m("#9a948e", .14, 2.5), x0, y, x1, y + 8, 1, bevel=1.2)
    c.poly(m("#9a948e", .12, 2.5), (54, 66), (74, 66), (74, 74), (54, 74), bevel=1.4)
    c.poly(m("#a8a29c", .10, 2.5, spec=.4), (58, 28), (70, 28), (72, 68), (56, 68), bevel=1.8)
    c.poly(m("#c4beb8", .08, 2.5, spec=.6), (58, 28), (64, 26), (70, 28), (64, 30), bevel=.6)
    c.line(m("#3a3430", .1), 1.0, (72, 68), (98, 76))
    c.glow(52, 30, 24, "#fff0c0", .3)
    rng = np.random.default_rng(59)
    for _ in range(60):
        x, y = rng.uniform(24, 104), rng.uniform(54, 100)
        c.ell(m("#4a4440", .1), x, y, rng.uniform(.6, 1.4), rng.uniform(.4, 1))
    return c.image()


# ================================================================== floor
@painter
def floor_terraces():
    """Stepped beds of dark soil held by dry-stone walls; every 256 pixels a wall of fitted fieldstones, sprouts in the soil."""
    base = (92, 66, 44)
    img, d, rng = floor_canvas(base, 511)
    for band in range(4):
        y0 = band * 256
        for y in range(y0, y0 + 186, 6):
            t = (y - y0) / 186
            d.rectangle((0, y, 1024, y + 6), fill=shade(base, 1.08 - .2 * t + rng.uniform(-.03, .03)))
        for _ in range(900):
            x, y, r = rng.uniform(0, 1024), rng.uniform(y0, y0 + 182), rng.uniform(1.5, 4)
            d.ellipse((x - r, y - r * .6, x + r, y + r * .6), fill=shade(base, rng.uniform(.75, 1.25)))
        for row in range(4):
            y = y0 + 34 + row * 40
            d.line((0, y + 6, 1024, y + 6), fill=shade(base, .7), width=5)
            x = 10 + rng.uniform(0, 20)
            while x < 1024:
                for dx in (-6, 0, 6):
                    d.line((x, y, x + dx, y - rng.uniform(10, 16)), fill=(86, 128, 56), width=4)
                x += rng.uniform(30, 44)
        d.rectangle((0, y0 + 184, 1024, y0 + 256), fill=(64, 60, 56))
        for course, (yy, hh) in enumerate(((y0 + 186, 23), (y0 + 209, 23), (y0 + 232, 23))):
            x = -rng.uniform(0, 40)
            while x < 1060:
                w = rng.uniform(34, 62)
                col = shade((132, 126, 118), rng.uniform(.75, 1.2))
                d.rounded_rectangle((x + 2, yy + 2, x + w - 2, yy + hh - 1), radius=7, fill=col, outline=(54, 50, 46), width=2)
                d.line((x + 8, yy + 5, x + w - 10, yy + 5), fill=shade(col, 1.18), width=2)
                x += w
    return finish_floor(img, 511, 2.8)


# ================================================================== food, relics
@painter
def food5(kind="pachamanca"):
    c = Canvas(128, seed=513)
    if kind == "pachamanca":
        leaf = m("#3a6a2a", .10, 2, (6, 1), spec=.5)
        outline = _closed([(8, 80), (26, 60), (60, 50), (96, 52), (120, 72), (112, 94), (80, 108), (40, 106), (16, 96)], 5)
        c.poly(m("#1e1a16", .1), *[(x + 2, y + 4) for x, y in outline])
        c.poly(leaf, *outline, bevel=1.8)
        c.line(m("#6a9a4a", .06), 1.6, (10, 80), (60, 78), (118, 74))
        for k in range(9):
            x = 20 + k * 11
            c.scratch(.7, .4, (x, 79), (x - 8, 58 + abs(k - 4) * 1.5), color=(.15, .3, .1))
            c.scratch(.7, .4, (x, 79), (x - 8, 100 - abs(k - 4) * 1.5), color=(.15, .3, .1))
        for x, y in ((24, 96), (104, 92), (100, 62)):
            c.ell(GRANITE_D, x, y, 8, 6, bevel=1.6)
        c.poly(m("#e0b02a", .08, 2, spec=.6), (32, 64), (70, 52), (74, 58), (36, 72), bevel=2.0)
        for k in range(10):
            for r in (-1, 0, 1):
                x, y = 36 + k * 3.6, 66 - k * 1.2 + r * 2.4
                c.ell(m("#f0c84a", .04, spec=.8), x, y, 1.6, 1.3, bevel=.4)
        for x, y, col in ((52, 82, "#6a3a6a"), (68, 88, "#c8a04a"), (84, 80, "#6a3a6a"), (60, 94, "#c8a04a")):
            c.ell(m(col, .1, 2, spec=.5), x, y, 9, 7, bevel=2.0)
            c.scratch(.6, .4, (x - 3, y - 2), (x - 1, y - 1))
        c.ell(m("#7a3a22", .12, 2, spec=.6), 86, 64, 13, 8, bevel=2.2)
        for k in range(4):
            c.scratch(.8, .5, (78 + k * 4, 60), (80 + k * 4, 68), color=(.3, .1, .05))
        c.ell(m("#e8e0cc", .05), 40, 88, 10, 6, bevel=1.2)
        c.ell(m("#5a9a3a", .06, spec=.8), 40, 87, 8, 4.4)
        for x, y in ((46, 76), (72, 72), (94, 92)):
            c.ell(m("#6a8a3a", .1), x, y, 4, 2, bevel=.6)
        c.glow(60, 60, 18, "#fff4e0", .3)
    return c.image()


def _quipu(c, top_y, mats, n, length, seed, gold=None, mess=0.0):
    rng = np.random.default_rng(seed)
    main = _spline([(14, top_y + 4), (40, top_y), (88, top_y), (114, top_y + 4)], 5)
    c.line(gold or m("#5a3a22", .1), 4.2, *main, bevel=.8)
    for k in range(n):
        x = 20 + k * (88 / (n - 1))
        y = top_y + 1
        ln = length * rng.uniform(.75, 1.0)
        mat = mats[k % len(mats)]
        pts = [(x, y), (x + rng.uniform(-2, 2) + mess * rng.uniform(-10, 10), y + ln * .5),
               (x + rng.uniform(-3, 3) + mess * rng.uniform(-14, 14), y + ln)]
        c.line(mat, 1.8, *_spline(pts, 4), bevel=.4)
        for _kk in range(rng.integers(1, 4)):
            t = rng.uniform(.3, .9)
            px = pts[0][0] + (pts[2][0] - pts[0][0]) * t + (pts[1][0] - (pts[0][0] + pts[2][0]) / 2) * 2 * t * (1 - t)
            c.ell(mat, px, y + ln * t, 2.2, 1.7, bevel=.7)


@painter
def relic5(kind="quipu"):
    c = Canvas(128, seed=515)
    if kind == "quipu":
        mud = m("#6a5236", .18, 2)
        c.poly(m("#4a3a26", .2, 2), (10, 112), (34, 98), (64, 104), (96, 96), (120, 108), (122, 120), (8, 122), bevel=1.6)
        mats = [m(col, .16, 1.5) for col in ("#7a4a36", "#8a7a5a", "#5a4a3a", "#8a5a30", "#6a6a56")]
        _quipu(c, 28, mats, 22, 74, 61, gold=m("#4a3420", .14), mess=1.0)
        rng = np.random.default_rng(62)
        for _ in range(14):
            x, y = rng.uniform(22, 106), rng.uniform(34, 96)
            c.line(GOLD, 1.0, (x, y), (x + rng.uniform(-4, 4), y + rng.uniform(3, 7)))
        for _ in range(30):
            x, y = rng.uniform(16, 112), rng.uniform(40, 104)
            c.ell(mud, x, y, rng.uniform(2, 5), rng.uniform(1.4, 3), bevel=.6)
        c.glow(64, 60, 14, "#fff0c0", .2)
    return c.image()


@painter
def golden_thread():
    """The Golden Thread: the great quipu restrung on a golden main cord, its pendants in bright wool and gold, hanging from two pegs."""
    c = Canvas(128, seed=516)
    mats = [WOOL_R, m("#f0c040", .04, 1.5, spec=1.2, tint="#8a5a14"), WOOL_W, JUNGLE, WOOL_K, m("#f0c040", .04, 1.5, spec=1.2, tint="#8a5a14"), TERRA]
    _quipu(c, 26, mats, 22, 82, 63, gold=GOLD)
    for x in (14, 114):
        c.ell(GOLD, x, 30, 4.4, 4.4, bevel=1.2)
        c.ell(m("#2e6a46", .06, spec=.8), x, 30, 2, 2)
    c.ell(GOLD, 64, 24, 6, 5, bevel=1.4)
    c.ell(TERRA, 64, 24, 3, 2.6, bevel=.6)
    c.glow(56, 40, 22, "#fff6d0", .4)
    return _halo(c.image(), (255, 214, 120, 255), 8, .9)
