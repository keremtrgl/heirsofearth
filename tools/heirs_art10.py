"""Heirs of Earth 3.1: world map settlement icons, one per nation.

RimWorld tints a settlement texture with the faction colour, so these are painted in pale stone greys:
light faces take the colour, dark openings and outlines keep the shape readable at every zoom.
"""
import math

from heirs_art import m, painter
from kut_render import Canvas, arc

W = m("#f4f2ec", .05, 2)        # sunlit face
L = m("#dcd8cf", .07, 2)        # second face
M = m("#b4afa5", .08, 2)        # shade face
D = m("#55514b", .10, 2)        # openings
ROOF = m("#c9c4ba", .10, 2, (3, 1))
GROUND = 110


def ground(c, x0=10, x1=118):
    c.ell(M, 64, GROUND + 4, (x1 - x0) / 2, 7, bevel=1.0, edge=.3)


def columns(c, x0, x1, top, bottom, n, w=3.2):
    step = (x1 - x0) / (n - 1)
    for i in range(n):
        x = x0 + i * step
        c.rect(W, x - w, top, x + w, bottom, 1, bevel=1.0)
        c.rect(L, x - w - 1.5, top - 3, x + w + 1.5, top, 1, bevel=.6)


def door(c, x, base, w, h, arch=True):
    if arch:
        pts = [(x - w, base), (x - w, base - h + w)] + arc(x, base - h + w, w, w, 180, 360, 12) + [(x + w, base)]
        c.poly(D, *pts, bevel=.4, edge=.2)
    else:
        c.rect(D, x - w, base - h, x + w, base, 0, bevel=.4, edge=.2)


@painter
def settlement_roma():
    c = Canvas(128, seed=310)
    ground(c)
    # Domed basilica behind, triumphal arch and colonnade in front.
    c.rect(L, 30, 54, 98, 92, 1, bevel=1.4)
    c.poly(W, *arc(64, 56, 26, 22, 180, 360, 28), bevel=2.0)
    c.rect(L, 61, 28, 67, 36, 1, bevel=.6)
    c.rect(M, 30, 54, 98, 59, 0, bevel=.6)
    for x in range(36, 96, 10):
        door(c, x + 2, 76, 2.6, 12)
    c.rect(W, 14, 72, 54, 108, 1, bevel=1.4)
    c.rect(L, 12, 66, 56, 73, 1, bevel=.8)
    door(c, 34, 108, 8, 26)
    c.rect(D, 20, 80, 23, 90, 0, bevel=.3)
    c.rect(D, 45, 80, 48, 90, 0, bevel=.3)
    c.poly(W, (60, 80), (88, 64), (116, 80), bevel=1.2)
    c.rect(L, 60, 80, 116, 84, 0, bevel=.6)
    columns(c, 64, 112, 88, 106, 5)
    c.rect(L, 58, 105, 118, 110, 1, bevel=.8)
    return c.image()


@painter
def settlement_yamato():
    c = Canvas(128, seed=311)
    ground(c)
    # Stone base with a three-tier castle keep and curved roofs.
    c.poly(M, (22, 110), (106, 110), (96, 84), (32, 84), bevel=1.6)
    for i in range(4):
        c.scratch(.7, .25, (28 + i * 2, 102 - i * 5), (100 - i * 2, 102 - i * 5))
    tiers = [(36, 92, 84, 70), (42, 86, 70, 54), (48, 80, 54, 40)]
    for x0, x1, base, top in tiers:
        c.rect(W, x0, top, x1, base, 0, bevel=1.2)
        for wx in range(int(x0) + 6, int(x1) - 3, 9):
            c.rect(D, wx, top + 4, wx + 4, top + 9, 0, bevel=.3)
        mid = (x0 + x1) / 2
        span = (x1 - x0) / 2 + 12
        c.poly(ROOF, (mid - span, top + 2), (mid - span + 6, top - 2), (mid, top - 9), (mid + span - 6, top - 2), (mid + span, top + 2),
               (mid + span - 4, top + 4), (mid - span + 4, top + 4), bevel=1.2)
    c.poly(ROOF, (52, 32), (64, 18), (76, 32), bevel=1.0)
    c.poly(L, (60, 18), (64, 12), (68, 18), bevel=.6)
    door(c, 64, 84, 5, 10, arch=False)
    return c.image()


@painter
def settlement_nord():
    c = Canvas(128, seed=312)
    ground(c)
    # Long hall with a steep turf roof and carved gable beasts, a smaller hut and a palisade.
    for x in range(10, 120, 7):
        c.poly(L, (x, 110), (x, 86), (x + 3, 82), (x + 6, 86), (x + 6, 110), bevel=.8)
    c.rect(W, 24, 66, 104, 100, 1, bevel=1.4)
    for x in range(30, 100, 8):
        c.scratch(.6, .3, (x, 68), (x, 99))
    c.poly(ROOF, (16, 70), (64, 30), (112, 70), (106, 74), (64, 40), (22, 74), bevel=1.6)
    c.poly(ROOF, (22, 74), (64, 40), (106, 74), bevel=1.0)
    for sx in (-1, 1):
        x = 64 + sx * 2
        c.poly(L, (x, 34), (x + sx * 8, 22), (x + sx * 14, 22), (x + sx * 10, 28), (x + sx * 4, 36), bevel=.8)
    door(c, 64, 100, 6, 16)
    c.rect(D, 40, 78, 46, 84, 0, bevel=.3)
    c.rect(D, 82, 78, 88, 84, 0, bevel=.3)
    return c.image()


@painter
def settlement_hellas():
    c = Canvas(128, seed=313)
    # Rocky hill with a temple on top.
    c.poly(M, (6, 114), (24, 92), (40, 84), (88, 82), (104, 90), (122, 114), bevel=2.0)
    for i in range(6):
        y = 96 + i * 3
        c.scratch(.6, .3, (20 + i * 3, y), (108 - i * 3, y))
    c.rect(L, 28, 76, 100, 84, 0, bevel=1.0)
    c.rect(W, 24, 72, 104, 78, 0, bevel=.8)
    columns(c, 32, 96, 44, 72, 7)
    c.rect(L, 26, 36, 102, 44, 0, bevel=.8)
    for x in range(30, 100, 6):
        c.rect(M, x, 38, x + 3, 42, 0, bevel=.3)
    c.poly(W, (22, 36), (64, 16), (106, 36), bevel=1.4)
    c.poly(M, (38, 33), (64, 21), (90, 33), bevel=.6, edge=.2)
    return c.image()


@painter
def settlement_tianxia():
    c = Canvas(128, seed=314)
    ground(c)
    # City wall with a gate tower under a double eaved roof.
    c.rect(L, 8, 78, 120, 110, 0, bevel=1.4)
    for x in range(8, 120, 10):
        c.rect(W, x, 72, x + 6, 79, 0, bevel=.6)
    c.rect(W, 34, 60, 94, 110, 0, bevel=1.4)
    door(c, 64, 110, 10, 26)
    c.rect(W, 42, 40, 86, 60, 0, bevel=1.2)
    for wx in (48, 58, 68, 78):
        c.rect(D, wx, 46, wx + 4, 54, 0, bevel=.3)

    def roof(y, half, lift):
        c.poly(ROOF, (64 - half - 8, y - lift), (64 - half, y), (64 + half, y), (64 + half + 8, y - lift),
               (64 + half - 4, y - 8), (64 - half + 4, y - 8), bevel=1.2)

    roof(62, 34, 6)
    roof(42, 26, 6)
    c.poly(ROOF, (46, 34), (64, 20), (82, 34), bevel=1.0)
    c.ell(L, 64, 18, 3, 3, bevel=.6)
    return c.image()


@painter
def settlement_albion():
    c = Canvas(128, seed=315)
    ground(c)
    # Brick row houses, a clock tower and a factory chimney.
    c.rect(L, 88, 30, 98, 104, 0, bevel=1.0)
    for y in range(36, 100, 8):
        c.scratch(.6, .25, (89, y), (97, y))
    c.ell(M, 93, 22, 9, 4, bevel=.6)
    for x0, top in ((8, 74), (28, 70), (66, 76)):
        c.rect(W, x0, top, x0 + 22, 108, 0, bevel=1.2)
        c.poly(ROOF, (x0 - 2, top), (x0 + 11, top - 12), (x0 + 24, top), bevel=1.0)
        for wy in (top + 8, top + 20):
            c.rect(D, x0 + 4, wy, x0 + 8, wy + 6, 0, bevel=.3)
            c.rect(D, x0 + 14, wy, x0 + 18, wy + 6, 0, bevel=.3)
    c.rect(W, 50, 36, 66, 108, 0, bevel=1.4)
    c.ell(L, 58, 50, 6, 6, bevel=1.0)
    c.line(D, 1.2, (58, 50), (58, 46))
    c.line(D, 1.2, (58, 50), (61, 51))
    c.poly(ROOF, (48, 36), (58, 16), (68, 36), bevel=1.0)
    door(c, 58, 108, 4, 12)
    c.rect(W, 102, 84, 120, 108, 0, bevel=1.0)
    return c.image()


@painter
def settlement_kemet():
    c = Canvas(128, seed=316)
    ground(c)
    # Pyramid, an obelisk and a pylon gate.
    c.poly(W, (18, 104), (60, 30), (102, 104), bevel=1.6)
    c.poly(M, (60, 30), (102, 104), (74, 104), bevel=.8, edge=.2)
    for i in range(1, 7):
        y = 30 + i * 11
        half = (y - 30) * 42 / 74
        c.scratch(.6, .3, (60 - half, y), (60 + half * .6, y))
    c.poly(L, (104, 106), (106, 46), (110, 40), (114, 46), (116, 106), bevel=1.0)
    c.poly(W, (8, 110), (12, 78), (34, 78), (38, 110), bevel=1.2)
    c.poly(W, (50, 110), (54, 78), (76, 78), (80, 110), bevel=1.2)
    c.rect(L, 36, 86, 52, 110, 0, bevel=1.0)
    door(c, 44, 110, 4, 14, arch=False)
    for x0 in (12, 54):
        c.rect(L, x0 - 1, 76, x0 + 23, 80, 0, bevel=.6)
    return c.image()


@painter
def settlement_pars():
    c = Canvas(128, seed=317)
    # Raised palace terrace with twin stairs, tall columns with bull capitals, and a pavilion.
    c.rect(M, 8, 88, 120, 112, 0, bevel=1.4)
    for i in range(5):
        c.poly(L, (40 - i * 5, 112 - i * 5), (48 - i * 5, 112 - i * 5), (48 - i * 5, 107 - i * 5), (40 - i * 5, 107 - i * 5), bevel=.4)
        c.poly(L, (80 + i * 5, 112 - i * 5), (88 + i * 5, 112 - i * 5), (88 + i * 5, 107 - i * 5), (80 + i * 5, 107 - i * 5), bevel=.4)
    c.rect(W, 6, 84, 122, 90, 0, bevel=.8)
    for x in range(16, 118, 14):
        c.rect(W, x - 2.6, 44, x + 2.6, 84, 1, bevel=1.0)
        c.poly(L, (x - 8, 44), (x - 4, 38), (x + 4, 38), (x + 8, 44), bevel=.6)
    c.rect(L, 8, 32, 120, 40, 0, bevel=1.0)
    for x in range(10, 118, 6):
        c.poly(W, (x, 32), (x + 2, 26), (x + 4, 26), (x + 6, 32), bevel=.4)
    c.ell(W, 64, 30, 18, 14, bevel=1.4)
    c.poly(L, (62, 16), (64, 8), (66, 16), bevel=.5)
    return c.image()


@painter
def settlement_inti():
    c = Canvas(128, seed=318)
    # Mountain peak behind stepped farming terraces and a stone sun temple with trapezoid doors.
    c.poly(M, (40, 92), (74, 14), (84, 24), (92, 18), (124, 92), bevel=2.0)
    c.poly(L, (74, 14), (84, 24), (92, 18), (88, 34), (78, 32), bevel=.8)
    for i in range(4):
        y = 112 - i * 9
        c.poly(L if i % 2 else W, (4 + i * 8, y), (124 - i * 8, y), (122 - i * 8, y - 8), (6 + i * 8, y - 8), bevel=1.0)
        c.scratch(.6, .3, (8 + i * 8, y - 2), (120 - i * 8, y - 2))
    c.poly(W, (36, 76), (40, 54), (88, 54), (92, 76), bevel=1.4)
    for x in range(40, 90, 8):
        c.scratch(.6, .3, (x, 55), (x - 1, 75))
    c.poly(ROOF, (34, 56), (64, 40), (94, 56), bevel=1.0)
    for x in (52, 64, 76):
        c.poly(D, (x - 3.6, 76), (x - 2.4, 62), (x + 2.4, 62), (x + 3.6, 76), bevel=.3, edge=.2)
    c.ell(W, 64, 32, 7, 7, bevel=1.2)
    for k in range(8):
        a = math.radians(k * 45)
        c.line(L, 1.4, (64 + math.cos(a) * 9, 32 + math.sin(a) * 9), (64 + math.cos(a) * 13, 32 + math.sin(a) * 13))
    return c.image()
