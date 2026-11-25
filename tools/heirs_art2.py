"""Heirs of Earth 1.0 painters: Roma, Yamato and Nordheim weapons, apparel icons, buildings, floors and food.

Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

import heirs_style_sample as sample
from heirs_art import (GOLD, IRON, LEATHER, LEATHER_D, ROMA_RED, STEEL, WOOD, WOOD_D, WOOD_V, BRONZE, DARKIRON,
                       STONE, STONE_D, STONE_L, MARBLE, Canvas, axis, blade, finish_floor, floor_canvas, haft, m, painter,
                       shade, wraps)

CLOTH_RED = m("#8e2a24", .10, 2, tint="#6d1f1c")
INDIGO = m("#2b3654", .10, 2)
INDIGO_L = m("#46557a", .10, 2)
LACQUER = m("#3a1f1c", .08, 2, spec=.6)
LACQUER_R = m("#8a2420", .08, 2, spec=.6)
SILK = m("#d9c9a3", .06, 2)
FUR = m("#8a6a48", .22, 1.5, tint="#5e4630")
FUR_L = m("#b39270", .2, 1.5)
WOOL = m("#7c6a52", .14, 2)
WOOL_B = m("#4f5d6e", .13, 2)
MAIL = m("#8e959a", .25, 1, spec=.6)
BONE = m("#e0d6bf", .06, 2)
RICE = m("#efeadf", .05, 1.5)
NORI = m("#1f2a22", .1, 1.5)
CERAMIC = m("#d7d2c4", .05, 2, spec=.5)
CERAMIC_B = m("#2f4f6f", .06, 2, spec=.6)
TERRACOTTA = m("#b0603a", .12, 2)
AMBER = m("#d18a2a", .08, 2, spec=1.0, tint="#8a4a12")
STRAW = m("#c8b072", .14, 2, (6, 1))
SAND = m("#cfc6b0", .07, 4)
PINE = m("#a57a4e", .2, 3, (9, 1))
PINE_V = m("#a57a4e", .2, 3, (1, 9))
FIRE = m("#ffb648", .2, 2, tint="#ff6a2a")


def ring(c, cx, cy, r, mat, width=2.0):
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]
    c.line(mat, width, *pts)


# ================================================================== weapons
@painter
def crossbow():
    c = Canvas(128, seed=51)
    at, ln = axis((22, 106), (104, 24))
    haft(c, at, 0, 92, 4.2, WOOD)
    c.poly(DARKIRON, at(10, -3), at(26, -3), at(26, 3), at(10, 3), bevel=.8)
    pa, _ = axis(at(74, 0), at(74, 1))
    bow_pts = [at(74 + 6 * math.sin(t * math.pi), -44 + 88 * t) for t in np.linspace(0, 1, 20)]
    c.line(IRON, 4.5, *bow_pts)
    c.line(m("#d8cfb8", .05), 1.1, bow_pts[0], at(50, 0), bow_pts[-1])
    c.poly(BRONZE, at(70, -5), at(80, -5), at(80, 5), at(70, 5), bevel=1.0)
    c.poly(STEEL, at(48, -1.2), at(92, -1.2), at(98, 0), at(92, 1.2), at(48, 1.2), bevel=.5)
    return c.image()


@painter
def spear_long(head="leaf", shaft="#6b4a2e", length=1.0):
    c = Canvas(128, seed=52)
    at, ln = axis((14, 118), (114, 10))
    haft(c, at, 0, ln - 26, 2.4, m(shaft, .18, 3, (1, 9)))
    if head == "leaf":
        c.poly(STEEL, *[at(ln - 30 + 30 * t, (1 - t) ** .7 * 6 * math.sin(math.pi * min(1, t * 1.6))) for t in np.linspace(0, 1, 12)],
               *[at(ln - 30 + 30 * t, -(1 - t) ** .7 * 6 * math.sin(math.pi * min(1, t * 1.6))) for t in np.linspace(1, 0, 12)], bevel=1.0)
    elif head == "yari":
        c.poly(STEEL, at(ln - 32, -2.6), at(ln - 6, -2.0), at(ln, 0), at(ln - 6, 2.0), at(ln - 32, 2.6), bevel=1.0)
        c.scratch(.5, .4, at(ln - 30, 0), at(ln - 6, 0))
        c.poly(LACQUER, at(ln - 40, -3.4), at(ln - 31, -3.4), at(ln - 31, 3.4), at(ln - 40, 3.4), bevel=.8)
    elif head == "naginata":
        curve = lambda u: -7 * ((u - (ln - 40)) / 40) ** 2
        blade(c, at, ln - 42, ln + 2, 3.6, 4.4, STEEL, tip=10, edge_mat=m("#dde3e6", .04, 2, spec=1.2), fuller=False, off=curve)
        c.poly(LACQUER, at(ln - 50, -3.2), at(ln - 41, -3.2), at(ln - 41, 3.2), at(ln - 50, 3.2), bevel=.8)
        c.ell(GOLD, *at(ln - 42, 0), 4.2, 4.2, bevel=.8)
    c.poly(DARKIRON, at(-1, -2.6), at(5, -2.6), at(5, 2.6), at(-1, 2.6), bevel=.6)
    return c.image()


@painter
def long_bow(kind="yumi"):
    c = Canvas(128, seed=53)
    at, ln = axis((24, 122), (104, 6))
    grip = .66 if kind == "yumi" else .5
    bend = 15 if kind == "yumi" else 11
    pts = []
    for t in np.linspace(0, 1, 40):
        v = -bend * math.sin(math.pi * t) + (4 if kind == "yumi" else 0) * math.sin(2 * math.pi * t)
        pts.append(at(t * ln, v))
    c.line(m("#3a2418", .12, 3) if kind == "yumi" else WOOD_V, 5.2, *pts)
    c.line(m("#d8cfb8", .05), 1.0, pts[0], pts[-1])
    g = int(len(pts) * (1 - grip))
    c.line(m("#b72f22", .1) if kind == "yumi" else LEATHER, 6.0, pts[g - 2], pts[g + 2])
    if kind == "yumi":
        for k in (8, 16, 24, 32):
            c.line(m("#c9a35a", .1), 5.6, pts[k], pts[k + 1])
    return c.image()


@painter
def katana_blade():
    return sample.katana()


@painter
def dane_axe():
    return sample.nordheim_axe()


@painter
def nordic_sword():
    c = Canvas(128, seed=54)
    at, ln = axis((22, 112), (108, 14))
    blade(c, at, 30, ln, 6.0, 4.6, STEEL, tip=12, edge_mat=m("#dfe5e8", .04, 2, spec=1.2))
    c.poly(DARKIRON, at(26, -14), at(31, -14), at(31, 14), at(26, 14), bevel=1.0)
    for u in (27.5,):
        c.line(GOLD, 1.0, at(u, -12), at(u, 12))
    wraps(c, at, 8, 26, 3.4)
    c.ell(DARKIRON, *at(4, 0), 6.5, 5.0, bevel=1.4)
    c.line(GOLD, 1.0, at(1, -4), at(7, 4))
    return c.image()


# ================================================================== apparel icons
@painter
def helmet(kind="galea", color="#8e2a24"):
    c = Canvas(128, seed=55)
    crest = m(color, .12, 2)
    if kind == "galea":
        for ang in np.linspace(200, 340, 15):
            r = math.radians(ang)
            c.line(crest, 6.5, (64 + 18 * math.cos(r), 40 + 18 * math.sin(r)), (64 + 44 * math.cos(r), 40 + 40 * math.sin(r)))
        c.rect(BRONZE, 58, 18, 70, 34, 2, bevel=1.0)
        c.poly(BRONZE, (26, 84), (34, 104), (46, 100), (44, 76), bevel=1.4)
        c.poly(BRONZE, (102, 84), (94, 104), (82, 100), (84, 76), bevel=1.4)
        c.ell(BRONZE, 64, 66, 34, 32, bevel=2.4)
        c.ell(m("#1e1714", .1), 64, 86, 15, 16)
        c.poly(BRONZE, (34, 74), (48, 72), (50, 108), (38, 112), (30, 96), bevel=1.6)
        c.poly(BRONZE, (94, 74), (80, 72), (78, 108), (90, 112), (98, 96), bevel=1.6)
        c.rect(IRON, 30, 58, 98, 66, 3, bevel=1.2)
        for x in (40, 52, 76, 88):
            c.ell(GOLD, x, 62, 1.6, 1.6, bevel=.6)
    elif kind == "kabuto":
        c.ell(LACQUER, 64, 62, 34, 28, bevel=2.2)
        for x in range(36, 94, 7):
            c.line(m("#1a1210", .1), 1.0, (x, 40), (64, 34))
        for i, y in enumerate((80, 90, 100)):
            c.poly(LACQUER_R if i % 2 else LACQUER, (22 - i * 4, y - 8), (106 + i * 4, y - 8), (110 + i * 4, y + 4), (18 - i * 4, y + 4), bevel=1.2)
            c.line(m("#c9a35a", .1), 1.2, (22 - i * 4, y - 2), (106 + i * 4, y - 2))
        c.poly(GOLD, (64, 46), (40, 12), (46, 10), (64, 38), (82, 10), (88, 12), bevel=1.4)
        c.ell(GOLD, 64, 50, 6, 6, bevel=1.4)
    elif kind == "norse":
        c.ell(IRON, 64, 64, 32, 34, bevel=2.4)
        c.poly(DARKIRON, (62, 30), (66, 30), (68, 98), (60, 98), bevel=1.0)
        c.rect(DARKIRON, 30, 70, 98, 78, 3, bevel=1.0)
        c.poly(DARKIRON, (44, 74), (84, 74), (84, 84), (72, 96), (64, 86), (56, 96), (44, 84), bevel=1.4)
        c.ell(m("#121212", .1), 54, 86, 6, 4)
        c.ell(m("#121212", .1), 74, 86, 6, 4)
        for x in (40, 52, 76, 88):
            c.ell(IRON, x, 74, 1.6, 1.6, bevel=.6)
    return c.image()


@painter
def torso(kind="lorica", color="#8e2a24"):
    c = Canvas(128, seed=56)
    cloth = m(color, .1, 2)
    if kind == "lorica":
        c.poly(cloth, (40, 98), (88, 98), (92, 116), (36, 116), bevel=1.4)
        for i in range(6):
            y = 46 + i * 9
            c.rect(STEEL if i % 2 else IRON, 30 + i, y, 98 - i, y + 10, 3, bevel=1.4, cyl=(30, 98))
        for x in (30, 82):
            c.rect(IRON, x, 26, x + 16, 48, 4, bevel=1.4)
        c.rect(BRONZE, 50, 30, 78, 40, 2, bevel=1.0)
        for y in range(50, 100, 9):
            c.ell(BRONZE, 64, y, 1.6, 1.6, bevel=.6)
    elif kind == "domaru":
        for i in range(7):
            y = 32 + i * 10
            c.rect(LACQUER if i % 2 else LACQUER_R, 30, y, 98, y + 11, 2, bevel=1.2, cyl=(30, 98))
            for x in range(34, 96, 6):
                c.line(m("#c9a35a", .1), 1.0, (x, y + 2), (x, y + 9))
        for side in (0, 1):
            x0 = 18 if side == 0 else 92
            for j in range(3):
                c.rect(LACQUER_R, x0, 34 + j * 9, x0 + 18, 44 + j * 9, 2, bevel=1.0)
    elif kind == "byrnie":
        shape = [(42, 22), (86, 22), (110, 42), (104, 70), (90, 62), (94, 116), (34, 116), (38, 62), (24, 70), (18, 42)]
        c.poly(MAIL, *shape, bevel=2.2)
        for row, y in enumerate(range(26, 116, 5)):
            for x in range(20 + (row % 2) * 3, 110, 6):
                c.scratch(.7, .35, (x - 2, y + 2), (x, y), (x + 2, y + 2), color=(.18, .19, .21))
        c.poly(m("#5a4a36", .12, 2), (48, 22), (80, 22), (76, 32), (64, 36), (52, 32), bevel=1.4)
        c.rect(LEATHER, 36, 74, 92, 82, 2, bevel=1.2)
        c.rect(BRONZE, 58, 72, 70, 84, 2, bevel=1.2)
        for x in (20, 26, 102, 108):
            c.line(m("#6a7076", .2, spec=.6), 1.2, (x, 44), (x - 2 if x < 64 else x + 2, 66))
        c.line(BRONZE, 1.4, (34, 113), (94, 113))
    elif kind == "kimono":
        c.poly(INDIGO, (40, 20), (88, 20), (112, 40), (104, 58), (90, 50), (92, 116), (36, 116), (38, 50), (24, 58), (16, 40), bevel=2.0)
        c.poly(SILK, (52, 20), (64, 46), (76, 20), (70, 20), (64, 36), (58, 20), bevel=1.0)
        c.rect(m("#8a6a3a", .1), 36, 62, 92, 74, 2, bevel=1.4)
        for x, y in ((48, 90), (78, 98), (56, 104), (82, 80)):
            c.ell(INDIGO_L, x, y, 4, 4, bevel=.6)
    elif kind == "tunica":
        c.poly(cloth, (42, 22), (86, 22), (108, 40), (100, 54), (88, 48), (90, 112), (38, 112), (40, 48), (28, 54), (20, 40), bevel=2.0)
        c.poly(m("#e8dcc0", .05), (54, 22), (74, 22), (70, 30), (58, 30), bevel=.8)
        c.rect(LEATHER, 38, 66, 90, 74, 2, bevel=1.0)
        c.line(GOLD, 1.2, (38, 104), (90, 104))
    elif kind == "furcloak":
        c.poly(WOOL, (34, 30), (94, 30), (114, 114), (14, 114), bevel=2.2)
        for x in (38, 52, 64, 76, 90):
            c.scratch(1.6, .35, (64 + (x - 64) * .55, 40), (x, 112))
        c.rect(FUR, 14, 106, 114, 118, 4, bevel=1.8, edge=.25)
        c.poly(FUR, (22, 22), (106, 22), (112, 46), (94, 54), (64, 48), (34, 54), (16, 46), bevel=2.6, edge=.25)
        rng = np.random.default_rng(7)
        for _ in range(70):
            x = rng.uniform(22, 106); y = rng.uniform(24, 48)
            c.line(FUR_L if rng.random() < .6 else m("#5e4630", .2), 1.6, (x, y), (x + rng.uniform(-3, 3), y + rng.uniform(4, 8)))
        c.ell(BRONZE, 64, 52, 8, 8, bevel=1.6)
        ring(c, 64, 52, 5, GOLD, 1.2)
        c.line(GOLD, 1.4, (60, 52), (68, 52))
    elif kind == "woolshirt":
        c.poly(WOOL_B, (42, 22), (86, 22), (108, 40), (102, 60), (88, 52), (90, 112), (38, 112), (40, 52), (26, 60), (20, 40), bevel=2.0)
        for y in (96, 102):
            c.line(m("#a1452f", .1), 2, (40, y), (88, y))
        c.line(m("#a1452f", .1), 2, (54, 24), (64, 36), (74, 24))
    return c.image()


# ================================================================== buildings and decor
@painter
def wall_shield(kind="scutum", size=(1, 1)):
    if kind == "scutum":
        return sample.scutum()
    c = Canvas(128, seed=57)
    if kind == "round":
        c.ell(WOOD, 64, 64, 50, 50, bevel=2.4)
        for i in range(8):
            a = i * math.pi / 4
            c.poly(m("#9b2b23", .1) if i % 2 else m("#d8c8a0", .08), (64, 64), (64 + 48 * math.cos(a), 64 + 48 * math.sin(a)),
                   (64 + 48 * math.cos(a + math.pi / 4), 64 + 48 * math.sin(a + math.pi / 4)), bevel=1.2, edge=.15)
        ring(c, 64, 64, 49, DARKIRON, 4.0)
        c.ell(IRON, 64, 64, 12, 12, bevel=2.4)
        c.ell(STEEL, 64, 64, 6, 6, bevel=2.4)
    return c.image()


@painter
def statue(kind="forum", size=(1, 1)):
    c = Canvas(128, 192, seed=58)
    c.rect(MARBLE, 30, 150, 98, 186, 3, bevel=1.8)
    c.rect(MARBLE, 36, 140, 92, 152, 2, bevel=1.4)
    c.poly(MARBLE, (50, 140), (78, 140), (82, 80), (88, 66), (74, 58), (54, 58), (40, 66), (46, 80), bevel=2.4)
    c.poly(MARBLE, (40, 66), (30, 96), (36, 100), (48, 78), bevel=1.6)
    c.poly(MARBLE, (88, 66), (104, 40), (98, 36), (80, 60), bevel=1.6)
    c.ell(MARBLE, 64, 44, 12, 14, bevel=2.4)
    c.poly(GOLD, (102, 40), (106, 20), (110, 22), (106, 42), bevel=1.0)
    for x in (52, 60, 68, 76):
        c.line(m("#a8a092", .1), 1.0, (x, 64), (x - 2, 136))
    return c.image()


@painter
def table(kind="triclinium", size=(2, 2)):
    w, h = size
    c = Canvas(128 * w, 128 * h, seed=59)
    W, H = 128 * w, 128 * h
    top = {"triclinium": MARBLE, "tea": m("#4a2e22", .14, 3, (9, 1)), "mead": WOOD}[kind]
    for x, y in ((14, 14), (W - 30, 14), (14, H - 30), (W - 30, H - 30)):
        c.rect(WOOD_D, x, y, x + 16, y + 16, 3, bevel=1.0)
    c.rect(top, 8, 8, W - 8, H - 8, 10, bevel=2.4)
    if kind == "triclinium":
        c.rect(CLOTH_RED, 28, 28, W - 28, H - 28, 6, bevel=1.0)
        c.ell(BRONZE, W / 2, H / 2, 22, 22, bevel=2.0)
        for dx, dy in ((-8, -6), (6, -2), (-2, 8)):
            c.ell(m("#5b2a55", .1), W / 2 + dx, H / 2 + dy, 7, 7, bevel=1.6)
        c.ell(TERRACOTTA, 60, 60, 12, 12, bevel=1.8)
    elif kind == "tea":
        c.rect(m("#2f1d16", .12, spec=.7), 18, 18, W - 18, H - 18, 8, bevel=.8)
        c.rect(m("#5b7a3a", .12, 2), 26, H - 70, 90, H - 26, 4, bevel=1.0)  # folded cloth
        for x, y in ((W / 2 - 52, H / 2 + 24), (W / 2 + 52, H / 2 + 24), (W / 2 - 52, H / 2 - 40), (W / 2 + 52, H / 2 - 40)):
            c.ell(m("#6a4a36", .1, spec=.4), x + 3, y + 4, 13, 12)
            c.ell(CERAMIC, x, y, 13, 12, bevel=2.0)
            c.ell(m("#7c9a3a", .08, spec=.8), x, y, 8.5, 8, bevel=.5)
        cx, cy = W / 2, H / 2 - 6
        c.ell(m("#121212", .1), cx + 4, cy + 6, 26, 22)
        c.ell(DARKIRON, cx, cy, 26, 22, bevel=2.6)
        for i in range(10):
            a2 = i * 2 * math.pi / 10
            c.ell(IRON, cx + 17 * math.cos(a2), cy + 14 * math.sin(a2), 2.6, 2.6, bevel=1.0)
        c.ell(IRON, cx, cy, 7, 6, bevel=1.6)
        c.line(DARKIRON, 3.2, (cx - 24, cy - 6), (cx - 10, cy - 30), (cx + 10, cy - 30), (cx + 24, cy - 6))
        c.line(DARKIRON, 4.0, (cx + 24, cy + 4), (cx + 38, cy - 2))
        c.line(m("#c9b48a", .1), 2.0, (W - 60, H - 40), (W - 30, H - 56))  # bamboo whisk
        c.ell(m("#c9b48a", .12), W - 62, H - 39, 6, 5, bevel=1.2)
    else:
        for i in range(0, W - 16, 22):
            c.scratch(1.2, .4, (10 + i, 10), (10 + i, H - 10))
        cx, cy = W / 2, H / 2
        c.ell(m("#2a1a10", .1), cx + 4, cy + 6, 30, 26)
        c.ell(WOOD_D, cx, cy, 30, 26, bevel=2.4)
        c.ell(m("#d49a2c", .06, 2, spec=1.0, tint="#a8661a"), cx, cy, 23, 19, bevel=.6)
        c.ell(m("#f4d48a", .05), cx - 8, cy - 6, 6, 3)
        for (x0, y0, x1, y1) in ((36, 40, 92, 62), (W - 40, 44, W - 96, 66), (40, H - 40, 96, H - 58), (W - 36, H - 44, W - 92, H - 66)):
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 10
            c.line(BONE, 9, (x0, y0), (mx, my), (x1, y1))
            c.line(m("#3a2a1a", .1), 9, (x0, y0), (x0 + (mx - x0) * .2, y0 + (my - y0) * .2))
            c.ell(GOLD, x1, y1, 5.5, 5.5, bevel=1.4)
        for x, y in ((cx - 70, cy + 4), (cx + 66, cy - 2)):
            c.ell(m("#b07a3e", .14, 2), x, y, 16, 12, bevel=2.0)
            c.scratch(1.0, .45, (x - 9, y - 3), (x + 9, y - 3))
            c.scratch(1.0, .45, (x - 7, y + 4), (x + 7, y + 4))
    return c.image()


@painter
def bath(kind="thermae", size=(3, 2)):
    w, h = size
    W, H = 128 * w, 128 * h
    c = Canvas(W, H, seed=60)
    edge = MARBLE if kind == "thermae" else PINE
    c.rect(edge, 6, 6, W - 6, H - 6, 12, bevel=2.4)
    if kind == "thermae":
        c.rect(m("#2c7d95", .06, 6, (6, 1), spec=.9), 26, 26, W - 26, H - 26, 10, bevel=1.0)
        for x in range(40, W - 40, 34):
            c.scratch(.8, .25, (x, 60), (x + 18, 64), color=(.95, .98, 1))
        for x in (16, W - 16):
            for y in (16, H - 16):
                c.ell(MARBLE, x, y, 10, 10, bevel=2.0)
        c.rect(MARBLE, W / 2 - 40, H - 34, W / 2 + 40, H - 18, 3, bevel=1.4)
    else:
        c.rect(m("#6a4a2e", .18, 3, (9, 1)), 20, 20, W - 20, H - 20, 6, bevel=.8)
        for i, y in enumerate(range(24, H - 120, 18)):
            c.rect(PINE, 24, y, W - 120, y + 15, 3, bevel=1.6)
        for i, x in enumerate(range(24, 90, 18)):
            c.rect(PINE_V, x, H - 116, x + 15, H - 24, 3, bevel=1.6)
        sx, sy = W - 66, H / 2
        c.rect(STONE_D, sx - 44, sy - 52, sx + 44, sy + 52, 10, bevel=2.4)
        rng = np.random.default_rng(11)
        for _ in range(22):
            x = sx + rng.uniform(-32, 32); y = sy + rng.uniform(-40, 40)
            c.ell(STONE if rng.random() < .5 else STONE_L, x, y, rng.uniform(7, 11), rng.uniform(6, 9), bevel=1.8)
        c.glow(sx, sy, 50, "#ff8a3a", .3)
        c.glow(sx - 20, sy - 30, 70, "#ffffff", .12)
        bx, by = 140, H - 70
        c.ell(m("#2a1a10", .1), bx + 3, by + 4, 20, 18)
        c.ell(WOOD_D, bx, by, 20, 18, bevel=2.2)
        c.ell(m("#3a6a7a", .05, 2, spec=1.0), bx, by, 14, 12, bevel=.6)
        ring(c, bx, by, 19, DARKIRON, 2.0)
        c.line(WOOD, 3.2, (bx + 4, by - 2), (bx + 40, by - 26))
        for k in range(5):
            c.line(m("#4f6a2a", .2), 2.0, (W - 150 + k * 4, 40), (W - 160 + k * 6, 78))
    return c.image()


@painter
def torii(size=(3, 1)):
    c = Canvas(384, 288, seed=61)
    for x in (88, 296):
        c.rect(LACQUER_R, x - 12, 70, x + 12, 284, 4, bevel=2.0, cyl=(x - 12, x + 12))
        c.rect(LACQUER, x - 16, 262, x + 16, 284, 3, bevel=1.4)
    c.rect(LACQUER_R, 54, 96, 330, 114, 3, bevel=1.6)
    c.poly(LACQUER, (14, 50), (370, 50), (382, 34), (360, 46), (24, 46), (2, 34), bevel=1.6)
    c.rect(LACQUER_R, 24, 50, 360, 72, 4, bevel=1.8)
    c.rect(LACQUER, 176, 72, 208, 96, 2, bevel=1.0)
    return c.image()


@painter
def stone_lantern(size=(1, 1)):
    c = Canvas(128, 192, seed=62)
    c.rect(STONE_D, 34, 168, 94, 188, 3, bevel=1.6)
    c.rect(STONE, 54, 110, 74, 170, 2, bevel=1.6, cyl=(54, 74))
    c.rect(STONE, 36, 96, 92, 112, 3, bevel=1.6)
    c.rect(STONE_L, 42, 60, 86, 98, 3, bevel=1.6)
    c.rect(m("#ffcf6a", .1, tint="#ff8a3a"), 54, 68, 74, 90, 2, bevel=.8)
    c.poly(STONE, (24, 62), (104, 62), (82, 38), (46, 38), bevel=2.0)
    c.ell(STONE_L, 64, 32, 9, 9, bevel=1.8)
    c.glow(64, 80, 26, "#ffb648", .4)
    return c.image()


@painter
def weapon_rack(size=(2, 1)):
    c = Canvas(256, 160, seed=63)
    c.rect(LACQUER, 14, 120, 242, 150, 4, bevel=1.8)
    for x in (34, 222):
        c.rect(LACQUER, x - 8, 30, x + 8, 124, 3, bevel=1.4)
    for i, y in enumerate((48, 76, 104)):
        c.poly(LACQUER if i else m("#1a1210", .1), (26, y - 3), (230, y - 7), (230, y + 1), (26, y + 5), bevel=1.0)
        c.poly(m("#1f1b1a", .1), (36, y - 1), (90, y - 2), (90, y + 3), (36, y + 4), bevel=.8)
        c.ell(GOLD, 92, y + 0.5, 4, 6, bevel=1.0)
    return c.image()


@painter
def training_post(size=(1, 1)):
    c = Canvas(128, 192, seed=64)
    c.ell(m("#7a6a50", .12), 64, 176, 40, 12, bevel=1.4)
    c.rect(WOOD_V, 56, 30, 72, 178, 3, bevel=1.6, cyl=(56, 72))
    for y in (60, 90, 120):
        c.rect(STRAW, 46, y - 10, 82, y + 10, 5, bevel=1.6)
        c.line(m("#4a3520", .1), 1.4, (46, y), (82, y))
    c.rect(WOOD_V, 24, 70, 104, 80, 3, bevel=1.2)
    return c.image()


@painter
def hearth(size=(2, 2)):
    w, h = size
    W, H = 128 * w, 128 * h
    c = Canvas(W, H, seed=65)
    c.ell(STONE_D, W / 2, H / 2, W / 2 - 8, H / 2 - 8, bevel=2.0)
    n = 16
    for i in range(n):
        a = i * 2 * math.pi / n
        c.ell(STONE if i % 2 else STONE_L, W / 2 + (W / 2 - 22) * math.cos(a), H / 2 + (H / 2 - 22) * math.sin(a), 18, 15, bevel=2.0)
    c.ell(m("#2a1e18", .3), W / 2, H / 2, W / 2 - 42, H / 2 - 42, bevel=1.0)
    for dx, dy, a in ((-30, -6, 20), (20, 10, -30), (-8, 22, 70)):
        at, _ = axis((W / 2 + dx - 26 * math.cos(math.radians(a)), H / 2 + dy - 26 * math.sin(math.radians(a))),
                     (W / 2 + dx + 26 * math.cos(math.radians(a)), H / 2 + dy + 26 * math.sin(math.radians(a))))
        haft(c, at, 0, 52, 7, WOOD_D)
    for dx, dy, r in ((-10, -4, 9), (8, 4, 10), (-2, 14, 7), (16, -12, 6)):
        c.ell(m("#ff8a3a", .25, 2, tint="#ff4a1a"), W / 2 + dx, H / 2 + dy, r, r * .7, bevel=1.2, edge=.15)
    c.glow(W / 2, H / 2, W / 3, "#ff8a3a", .35)
    return c.image()


@painter
def rune_stone(size=(1, 1)):
    c = Canvas(128, 192, seed=66)
    c.ell(m("#5a6a3a", .15), 64, 176, 40, 12, bevel=1.4)
    c.poly(STONE, (36, 178), (30, 110), (38, 50), (58, 18), (84, 26), (96, 70), (98, 130), (92, 178), bevel=2.6)
    band = m("#9b2b23", .1)
    pts = [(48, 168), (42, 120), (46, 72), (62, 40), (80, 46), (88, 86), (88, 130), (82, 168)]
    c.line(band, 5, *pts)
    for x, y in ((56, 70), (62, 90), (70, 110), (60, 130), (72, 150), (66, 60)):
        c.line(m("#2b2622", .1), 1.6, (x - 4, y - 6), (x, y + 6), (x + 4, y - 6))
    c.ell(m("#9b2b23", .1), 70, 36, 5, 5, bevel=1.0)
    return c.image()


# ================================================================== floors
@painter
def floor_mosaic():
    img, d, rng = floor_canvas((214, 205, 186), 71)
    S = 1024
    cell = 32
    palette = [(214, 205, 186), (200, 190, 168), (142, 42, 36), (60, 70, 92), (184, 150, 80)]
    for y in range(0, S, cell):
        for x in range(0, S, cell):
            gx, gy = (x // cell) % 16, (y // cell) % 16
            border = gx in (0, 15) or gy in (0, 15)
            diamond = abs(gx - 7.5) + abs(gy - 7.5) < 5
            col = palette[2] if border else (palette[4] if diamond and (gx + gy) % 2 == 0 else (palette[3] if diamond else palette[rng.integers(0, 2)]))
            j = rng.integers(-8, 8)
            d.rectangle([x + 2, y + 2, x + cell - 2, y + cell - 2], fill=tuple(int(max(0, min(255, v + j))) for v in col))
    return finish_floor(img, 71, 2.6)


@painter
def floor_tatami():
    img, d, rng = floor_canvas((176, 170, 112), 72)
    S = 1024
    mats = [(0, 0, 512, 256), (512, 0, 1024, 256), (0, 256, 256, 768), (256, 256, 768, 512), (768, 256, 1024, 768),
            (256, 512, 768, 768), (0, 768, 512, 1024), (512, 768, 1024, 1024)]
    for x0, y0, x1, y1 in mats:
        base = np.array((176, 170, 112)) + rng.integers(-8, 8)
        d.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], fill=tuple(int(v) for v in base))
        horizontal = (x1 - x0) > (y1 - y0)
        for k in range(0, int((y1 - y0) if horizontal else (x1 - x0)), 5):
            if horizontal:
                d.line([x0 + 6, y0 + k, x1 - 6, y0 + k], fill=tuple(int(v) for v in base - 14), width=1)
            else:
                d.line([x0 + k, y0 + 6, x0 + k, y1 - 6], fill=tuple(int(v) for v in base - 14), width=1)
        edge = (36, 44, 36)
        if horizontal:
            d.rectangle([x0 + 4, y0 + 4, x0 + 18, y1 - 4], fill=edge)
            d.rectangle([x1 - 18, y0 + 4, x1 - 4, y1 - 4], fill=edge)
        else:
            d.rectangle([x0 + 4, y0 + 4, x1 - 4, y0 + 18], fill=edge)
            d.rectangle([x0 + 4, y1 - 18, x1 - 4, y1 - 4], fill=edge)
    return finish_floor(img, 72, 2.0)


@painter
def floor_gravel():
    img, d, rng = floor_canvas((206, 200, 186), 73)
    S = 1024
    for y in range(0, S, 16):
        for x in range(0, S, 4):
            yy = y + 4 * math.sin(x / S * 2 * math.pi * 4)
            d.line([x, yy, x + 4, yy], fill=(176, 170, 156), width=3)
    for _ in range(2600):
        x, y = rng.integers(0, S, 2)
        r = rng.integers(2, 5)
        v = int(rng.integers(150, 225))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(v, v - 4, v - 12))
    return finish_floor(img, 73, 2.2)


@painter
def floor_planks():
    img, d, rng = floor_canvas((126, 92, 60), 74)
    S = 1024
    for i, x in enumerate(range(0, S, 64)):
        off = (i * 173) % 512
        for y0 in range(-512 + off, S, 512):
            col = np.array((126, 92, 60)) + rng.integers(-14, 14)
            d.rectangle([x + 2, y0 + 2, x + 62, y0 + 510], fill=tuple(int(v) for v in col))
            for _ in range(10):
                gx = x + rng.integers(6, 58)
                d.line([gx, y0 + 6, gx + rng.integers(-3, 3), y0 + 504], fill=tuple(int(v) for v in col - 16), width=1)
            for yy in (y0 + 24, y0 + 486):
                d.ellipse([x + 10, yy - 3, x + 16, yy + 3], fill=(60, 52, 46))
                d.ellipse([x + 48, yy - 3, x + 54, yy + 3], fill=(60, 52, 46))
    return finish_floor(img, 74, 2.8)


# ================================================================== food and goods
@painter
def bowl(kind="puls"):
    c = Canvas(128, seed=75)
    if kind == "onigiri":
        for dx, dy in ((-20, 6), (20, 6), (0, -14)):
            cx, cy = 64 + dx, 70 + dy
            c.poly(RICE, (cx - 20, cy + 18), (cx + 20, cy + 18), (cx + 4, cy - 18), (cx - 4, cy - 18), bevel=2.4)
            c.rect(NORI, cx - 12, cy + 2, cx + 12, cy + 18, 2, bevel=1.0)
        c.ell(m("#c0392b", .1), 64, 58, 4, 4, bevel=1.0)
        return c.image()
    rim = TERRACOTTA if kind == "puls" else (WOOD if kind == "skyr" else CERAMIC)
    c.ell(rim, 64, 76, 46, 30, bevel=2.4)
    c.poly(rim, (18, 76), (110, 76), (96, 108), (32, 108), bevel=2.0)
    fill = {"puls": m("#c8a66a", .12), "skyr": m("#f2efe6", .05), "rice": RICE}[kind]
    c.ell(fill, 64, 72, 40, 22, bevel=1.8)
    if kind == "puls":
        for dx, dy in ((-12, -2), (10, 4), (2, -8)):
            c.ell(m("#5b6b2a", .1), 64 + dx, 72 + dy, 4, 3, bevel=.8)
    elif kind == "skyr":
        for dx, dy in ((-10, -4), (8, 2), (0, 6)):
            c.ell(m("#3a2a5a", .1), 64 + dx, 72 + dy, 4, 4, bevel=1.2)
        c.ell(AMBER, 72, 64, 6, 3, bevel=1.0)
    return c.image()


@painter
def jar(kind="amphora"):
    c = Canvas(128, seed=76)
    if kind == "amphora":
        c.poly(TERRACOTTA, (64, 122), (52, 104), (40, 72), (44, 44), (54, 32), (74, 32), (84, 44), (88, 72), (76, 104), bevel=2.6)
        c.rect(TERRACOTTA, 56, 14, 72, 34, 3, bevel=1.6, cyl=(56, 72))
        for s in (-1, 1):
            c.line(TERRACOTTA, 4, (64 + s * 8, 20), (64 + s * 24, 24), (64 + s * 22, 44))
        c.rect(m("#d8cfb8", .06), 50, 58, 78, 72, 2, bevel=.8)
        c.line(CLOTH_RED, 1.6, (54, 65), (74, 65))
    elif kind == "tokkuri":
        c.ell(CERAMIC, 64, 86, 30, 32, bevel=2.6)
        c.rect(CERAMIC, 56, 26, 72, 60, 3, bevel=1.6, cyl=(56, 72))
        c.ell(CERAMIC, 64, 26, 10, 4, bevel=1.0)
        c.poly(CERAMIC_B, (40, 80), (88, 80), (92, 94), (36, 94), bevel=.8, clip=True)
        c.line(m("#d8cfb8", .05), 2.0, (58, 46), (70, 46))
    elif kind == "horn":
        at, ln = axis((22, 100), (104, 30))
        pts = [at(ln * t, -10 * math.sin(math.pi * t * .8)) for t in np.linspace(0, 1, 20)]
        for i in range(len(pts) - 1):
            wdt = 4 + 14 * (i / len(pts))
            c.line(BONE, wdt, pts[i], pts[i + 1])
        c.line(BRONZE, 3, pts[-2], pts[-1])
        c.line(BRONZE, 2.4, pts[2], pts[3])
        c.ell(AMBER, *pts[-1], 8, 4, bevel=1.0)
    elif kind == "amber":
        rng = np.random.default_rng(5)
        for dx, dy, r in ((-18, 10, 16), (16, 14, 14), (0, -12, 18), (24, -18, 9), (-26, -14, 8)):
            pts = [(64 + dx + r * (1 + .2 * rng.standard_normal()) * math.cos(a), 64 + dy + r * (1 + .2 * rng.standard_normal()) * math.sin(a))
                   for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
            c.poly(AMBER, *pts, bevel=2.2)
            c.glow(64 + dx - 3, 64 + dy - 3, r * .6, "#ffe0a0", .25)
    return c.image()
