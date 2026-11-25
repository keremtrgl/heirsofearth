"""Heirs of Earth 2.1 painters: industrial weapons of the 1.0 nations and the missing signature buildings.

carbine (Nova Roma), tanegashima (Yamato), harpoon_gun and harpoon (Nordheim), arrow_battery_base/top (Tianxia),
loom (Albion textile mill), lyceum (Hellas academy) and asclepion (Hellas healing shrine).
Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module last.
"""
import math

import numpy as np

from heirs_art import BRONZE, DARKIRON, GOLD, IRON, MARBLE, STEEL, STONE, STONE_D, STONE_L, WOOD, WOOD_D, Canvas, axis, haft, m, painter
from heirs_art2 import LACQUER, LACQUER_R
from heirs_art4 import BAMBOO, BRASS, IMP_RED, LINEN, OAK, PARCH, TWEED, _spline, _tube

ROMA_RED = m("#8e2a24", .08, 2, tint="#5e1612")
WALNUT = m("#5a3a20", .14, 3, (9, 1))
BLACK_LAC = m("#1e1a18", .06, 2, spec=.7)
GUNMETAL = m("#3a3e42", .08, 3, (9, 1), spec=.9)
ROPE = m("#b89a62", .14, 1.5, (1, 4))
CEDAR = m("#8a4e2e", .16, 3, (9, 1))
CEDAR_V = m("#8a4e2e", .16, 3, (1, 9))
PINE = m("#a77a4a", .16, 3, (9, 1))
YARN = m("#e9e1cc", .08, 1.2, (1, 6))
BRONZE_G = m("#7a8a5a", .12, 2, spec=.6, tint="#4a6a4a")


# ================================================================== weapons
@painter
def carbine():
    """Nova Roma legion carbine: short breech-loader, red-lacquered stock, brass eagle on the side plate."""
    c = Canvas(128, seed=201)
    at, ln = axis((18, 104), (112, 28))
    c.poly(WALNUT, at(0, -7), at(14, -6), at(24, -3.4), at(70, -2.8), at(70, 2.8), at(24, 4), at(12, 8), at(0, 8.5), bevel=1.6)
    c.poly(ROMA_RED, at(2, -6), at(12, -5.4), at(20, -3), at(20, 4), at(10, 7.4), at(2, 7.6), bevel=1.2)
    c.poly(BRASS, at(-1, -7), at(2, -7), at(2, 8.5), at(-1, 8.5), bevel=.8)
    c.poly(GUNMETAL, at(22, -2.2), at(ln, -1.8), at(ln, 1.8), at(22, 2.2), bevel=.8)
    c.poly(GUNMETAL, at(22, -3.6), at(36, -3.6), at(36, 3.8), at(22, 3.8), bevel=1.0)
    c.ell(BRASS, *at(29, 0), 3.6, 3.6, bevel=1.0)
    c.poly(m("#f0d070", .05), at(27, -1), at(29, -2.6), at(31, -1), at(29, 1.4), bevel=.4)
    c.line(DARKIRON, 1.8, at(34, -3.4), at(30, -8), at(34, -9))
    c.line(DARKIRON, 1.6, at(26, 3.8), at(24, 7.5), at(19, 8))
    c.poly(WALNUT, at(38, 2), at(66, 2), at(66, 4.6), at(38, 4.6), bevel=.8)
    for u in (46, 62):
        c.line(BRASS, 1.6, at(u, -2.6), at(u, 4.6))
    c.poly(GUNMETAL, at(ln - 4, -3.2), at(ln - 2, -3.2), at(ln - 2, -1.8), at(ln - 4, -1.8), bevel=.4)
    c.line(m("#c9b08a", .05), 1.2, at(8, 8), at(40, 5.4), bevel=.4)
    return c.image()


@painter
def tanegashima():
    """Yamato matchlock: long black-lacquered stock, brass serpentine and pan, a glowing match cord."""
    c = Canvas(128, seed=202)
    at, ln = axis((10, 110), (120, 16))
    c.poly(BLACK_LAC, at(0, -5), at(6, -5), at(26, -3.2), at(96, -2.8), at(96, 2.8), at(26, 3.4), at(6, 6), at(0, 6), bevel=1.6)
    c.poly(LACQUER_R, at(0, -5), at(4, -5), at(4, 6), at(0, 6), bevel=.8)
    c.poly(m("#4a4c50", .08, 3, (9, 1), spec=1.0), at(20, -1.9), at(ln, -1.6), at(ln, 1.6), at(20, 1.9), bevel=.8)
    for u in (40, 60, 80):
        c.line(BRASS, 1.4, at(u, -3), at(u, 3))
    c.poly(BRASS, at(ln - 3, -2.6), at(ln, -2.6), at(ln, 2.6), at(ln - 3, 2.6), bevel=.6)
    c.poly(BRASS, at(24, 1.4), at(38, 1.4), at(38, 5.4), at(24, 5.4), bevel=1.0)
    c.ell(BRASS, *at(36, -3), 2.6, 1.8, bevel=.8)
    c.line(BRASS, 2.2, at(28, 2.4), at(31, -4), at(35, -4.6))
    c.line(ROPE, 1.6, at(35, -4.6), at(40, -8), at(52, -6), at(64, -9), at(74, -7))
    c.ell(m("#ffb040", .1), *at(35, -4.8), 1.6, 1.6)
    c.glow(*at(35, -4.8), 7, "#ff9a3a", .6)
    for u in (30, 44, 58, 72, 86):
        c.scratch(.5, .3, at(u, -2.6), at(u + 6, -2.4))
    return c.image()


@painter
def harpoon_gun():
    """Nordheim harpoon gun: a heavy short barrel on a carved stock, a barbed iron harpoon sitting in the muzzle."""
    c = Canvas(128, seed=203)
    at, ln = axis((12, 108), (122, 22))
    c.poly(PINE, at(0, -7), at(10, -7), at(30, -4), at(58, -4), at(58, 4.4), at(30, 5), at(10, 9), at(0, 9), bevel=1.8)
    for k in range(4):
        c.scratch(.8, .45, at(4 + k * 6, -4), at(8 + k * 6, 6))
    c.poly(IRON, at(-1, -7), at(2, -7), at(2, 9), at(-1, 9), bevel=.8)
    c.poly(m("#34383c", .08, 3, (9, 1), spec=.8), at(30, -4.6), at(76, -4.2), at(76, 4.2), at(30, 4.6), bevel=1.4, cyl=None)
    for u in (36, 54, 72):
        c.line(DARKIRON, 2.6, at(u, -5), at(u, 5))
    c.line(DARKIRON, 2.0, at(32, 4.6), at(30, 9), at(24, 10))
    haft(c, at, 60, ln - 16, 1.4, m("#6a4a2e", .14, 3, (9, 1)))
    c.poly(STEEL, at(ln - 18, -2.4), at(ln - 6, -1.6), at(ln, 0), at(ln - 6, 1.6), at(ln - 18, 2.4), bevel=.8)
    for s in (-1, 1):
        c.poly(STEEL, at(ln - 14, s * 2), at(ln - 20, s * 6), at(ln - 11, s * 2.2), bevel=.5)
    c.line(ROPE, 1.4, at(64, 1.4), at(56, 8), at(44, 10), at(34, 12))
    return c.image()


@painter
def harpoon():
    """The flying harpoon projectile, pointing right."""
    c = Canvas(64, seed=204)
    at, ln = axis((4, 32), (60, 32))
    haft(c, at, 0, ln - 12, 1.4, m("#6a4a2e", .14, 3, (9, 1)))
    c.poly(STEEL, at(ln - 14, -2.4), at(ln - 4, -1.6), at(ln, 0), at(ln - 4, 1.6), at(ln - 14, 2.4), bevel=.8)
    for s in (-1, 1):
        c.poly(STEEL, at(ln - 10, s * 2), at(ln - 16, s * 5.4), at(ln - 8, s * 2.2), bevel=.5)
    c.line(ROPE, 1.2, at(0, 0), at(-4, 3))
    return c.image()


# ================================================================== Tianxia fire-arrow battery
@painter
def arrow_battery_base(size=(2, 2)):
    """A low wheeled cart of lacquered wood with iron-rimmed wheels, seen from above."""
    c = Canvas(256, 256, seed=205)
    c.ell(m("#2a2018", .1), 132, 140, 104, 92)
    for x in (34, 222):
        for y in (70, 186):
            c.rect(DARKIRON, x - 14, y - 34, x + 14, y + 34, 10, bevel=1.6)
            c.rect(CEDAR_V, x - 10, y - 30, x + 10, y + 30, 8, bevel=1.4)
            for k in (-18, 0, 18):
                c.line(DARKIRON, 2.0, (x - 10, y + k), (x + 10, y + k))
    c.rect(DARKIRON, 30, 124, 226, 132, 3, bevel=1.0)
    c.rect(CEDAR, 52, 44, 204, 212, 12, bevel=2.6)
    c.rect(LACQUER_R, 62, 54, 194, 202, 8, bevel=1.6)
    for x in (62, 194):
        c.line(GOLD, 2.0, (x, 58), (x, 198))
    c.rect(CEDAR, 104, 212, 152, 250, 4, bevel=1.4)
    c.line(DARKIRON, 2.6, (98, 246), (158, 246))
    c.ell(BRASS, 128, 128, 22, 22, bevel=2.0)
    c.ell(DARKIRON, 128, 128, 12, 12, bevel=1.2)
    return c.image()


@painter
def arrow_battery_top(size=(2, 2)):
    """The 'nest of bees' rack: a hexagonal box of fire arrows with red-paper fuses, pointing right."""
    c = Canvas(256, 256, seed=206)
    cx, cy = 118, 128
    c.ell(m("#1e1610", .1), cx + 6, cy + 8, 74, 60)
    box = [(cx - 70, cy - 34), (cx - 40, cy - 58), (cx + 64, cy - 58), (cx + 82, cy - 34), (cx + 82, cy + 34), (cx + 64, cy + 58), (cx - 40, cy + 58), (cx - 70, cy + 34)]
    c.poly(BAMBOO, *box, bevel=2.6)
    c.poly(LACQUER_R, (cx - 60, cy - 30), (cx - 34, cy - 50), (cx + 58, cy - 50), (cx + 74, cy - 30), (cx + 74, cy + 30), (cx + 58, cy + 50), (cx - 34, cy + 50), (cx - 60, cy + 30), bevel=1.8)
    for x in (cx - 46, cx + 4, cx + 54):
        c.line(DARKIRON, 3.2, (x, cy - 56), (x, cy + 56))
    rng = np.random.default_rng(8)
    rows = 7
    for r in range(rows):
        y = cy - 42 + r * 14
        c.rect(m("#5a1c14", .1), cx - 50, y - 4, cx + 44, y + 4, 4, bevel=.8)
        for k in range(3):
            yy = y - 2.4 + k * 2.4
            c.line(m("#d8c89a", .06, 1.5, (6, 1)), .9, (cx - 48, yy), (cx + 42, yy))
    for r in range(rows):
        y = cy - 42 + r * 14
        for k in range(5):
            x = cx + 40 + k * 8 + (r % 2) * 4
            if abs(y - cy) > 44 - (k * 3):
                continue
            c.poly(STEEL, (x, y - 2.6), (x + 14, y), (x, y + 2.6), bevel=.6)
            c.line(m("#d8d0b8", .05), 1.0, (x - 6, y), (x, y))
    for r in range(rows):
        y = cy - 42 + r * 14 + rng.uniform(-1, 1)
        c.line(m("#c8322a", .06), 2.0, (cx - 64, y), (cx - 52, y + rng.uniform(-3, 3)))
    c.ell(BRASS, cx - 8, cy, 9, 9, bevel=1.6)
    c.glow(cx - 66, cy, 14, "#ffb040", .4)
    return c.image()


# ================================================================== Albion textile mill
@painter
def loom(size=(3, 1)):
    """A steam-driven power loom seen from above: iron frame, warp threads, a tweed roll and a belt wheel."""
    w, h = size
    W, H = 128 * w, 128 * h
    c = Canvas(W, H, seed=207)
    c.rect(m("#22201e", .1), 10, 18, W - 6, H - 4, 10)
    c.rect(GUNMETAL, 6, 12, W - 10, H - 12, 8, bevel=2.2)
    c.rect(OAK, 20, 24, W - 90, H - 24, 4, bevel=1.4)
    for k in range(40):
        x = 26 + k * (W - 122) / 40
        c.line(YARN, .9, (x, 28), (x, H - 30))
    c.rect(TWEED, 36, H / 2 - 10, W - 108, H / 2 + 10, 4, bevel=1.6)
    for k in range(0, int(W - 144), 8):
        c.scratch(1.0, .35, (40 + k, H / 2 - 9), (40 + k, H / 2 + 9), color=(.2, .18, .1))
    c.scratch(1.0, .4, (38, H / 2), (W - 110, H / 2), color=(.5, .2, .15))
    c.rect(m("#d9c9a0", .05), 30, H - 36, W - 100, H - 26, 4, bevel=1.2, cyl=None)
    c.poly(m("#8a5a2e", .1, spec=.4), (W / 2 - 30, 34), (W / 2 + 20, 34), (W / 2 + 28, 39), (W / 2 + 20, 44), (W / 2 - 30, 44), (W / 2 - 38, 39), bevel=1.2)
    c.rect(TWEED, W - 88, 22, W - 52, H - 22, 14, bevel=2.2, cyl=(W - 88, W - 52))
    for y in range(30, H - 26, 6):
        c.scratch(.8, .35, (W - 86, y), (W - 54, y), color=(.25, .22, .12))
    wx, wy, wr = W - 28, H / 2, 22
    for k in range(6):
        a = k * math.pi / 3
        c.line(DARKIRON, 3.0, (wx, wy), (wx + wr * math.cos(a), wy + wr * math.sin(a)))
    c.line(GUNMETAL, 6, *[(wx + wr * math.cos(t), wy + wr * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)])
    c.ell(BRASS, wx, wy, 6, 6, bevel=1.2)
    c.line(m("#3a2a1e", .1), 4.0, (wx - 4, wy - wr), (W - 92, 30))
    return c.image()


# ================================================================== Hellas academy and healing shrine
@painter
def lyceum(size=(2, 1)):
    """A cedar scroll cabinet with a marble philosopher's bust on top, seen from above at an angle."""
    w, h = size
    W, H = 128 * w, 128 * h
    c = Canvas(W, H, seed=208)
    c.rect(m("#2a2018", .1), 14, 50, W - 6, H - 2, 8)
    c.rect(CEDAR, 8, 42, W - 12, H - 8, 6, bevel=2.4)
    for row in range(3):
        y0 = 50 + row * 22
        c.rect(m("#3a2216", .12), 18, y0, W - 22, y0 + 18, 3, bevel=1.0)
        for k in range(12):
            x = 28 + k * 17
            if x > W - 34:
                break
            c.ell(m("#2a1a10", .1), x + 1, y0 + 10, 6.5, 6.5)
            c.ell(PARCH, x, y0 + 9, 6.5, 6.5, bevel=1.4)
            c.ell(m("#b8a272", .06), x, y0 + 9, 2.4, 2.4)
            if (k + row) % 4 == 0:
                c.line(IMP_RED, 1.6, (x - 3, y0 + 3), (x + 3, y0 + 15))
    bx = W - 54
    c.ell(m("#2a2018", .12), bx + 4, 44, 26, 6)
    c.rect(MARBLE, bx - 16, 30, bx + 16, 46, 3, bevel=1.4)
    c.poly(MARBLE, (bx - 22, 30), (bx - 12, 22), (bx + 12, 22), (bx + 22, 30), bevel=1.4)
    c.ell(MARBLE, bx, 13, 10, 11, bevel=2.0)
    c.ell(m("#d8d2c4", .05), bx, 22, 9, 5, bevel=1.4)
    c.line(m("#a8a094", .06), 1.0, (bx - 6, 23), (bx + 6, 23))
    c.rect(BRONZE, 26, 30, 58, 38, 2, bevel=1.0)
    c.line(PARCH, 3.0, (32, 38), (44, 44), (60, 42))
    return c.image()


@painter
def asclepion(size=(1, 1)):
    """A small healing altar: marble block, bronze bowl with smouldering herbs and the rod of Asclepius."""
    c = Canvas(128, 160, seed=209)
    c.ell(m("#2a2420", .1), 66, 148, 40, 10)
    c.rect(MARBLE, 30, 92, 98, 150, 4, bevel=2.2)
    c.rect(m("#cfc8b8", .05), 26, 86, 102, 96, 3, bevel=1.4)
    for x in (40, 54, 68, 82):
        c.line(m("#b8b0a2", .05), 1.0, (x, 100), (x, 146))
    c.ell(BRONZE, 64, 82, 26, 10, bevel=2.0)
    c.ell(m("#3a2a1a", .12), 64, 80, 20, 6)
    for k, x in enumerate((54, 62, 70)):
        c.line(m("#6d7a3a", .12), 1.6, (x, 80), (x + 4, 72 - k))
    c.glow(64, 78, 18, "#ffb648", .45)
    for k in range(3):
        y = 60 - k * 14
        c.ell(m("#cfcfcf", .1), 64 + (k % 2) * 6 - 3, y, 7 - k, 4)
    rod = [(98, 150), (98, 18)]
    c.line(WOOD_D, 3.6, *rod)
    snake = _spline([(98, 132), (108, 120), (90, 104), (108, 88), (90, 72), (106, 56), (96, 40), (100, 28)], 6)
    _tube(c, BRONZE_G, snake, 2.6, 1.6, bevel=1.2)
    c.ell(BRONZE_G, 100, 26, 3.6, 2.8, bevel=1.0)
    c.ell(m("#1a1a1a", .1), 101, 25, .8, .8)
    return c.image()
