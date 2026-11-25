"""Heirs of Earth 3.2: icons for the new clothes and leader regalia (128x128)."""
import math

from heirs_art import BRONZE, GOLD, Canvas, m, painter

WOOL_W = m("#ece4d0", .06, 2)
WOOL_W_D = m("#cfc3a6", .08, 2)
PURPLE = m("#5a1e4a", .08, 2, tint="#3e1030")
GOLD_T = m("#d9a93a", .06, 2, spec=.9)
GOLD_S = m("#e2b440", .05, 2, spec=1.3)
LEAF = m("#4e6a2a", .12, 2, spec=.4)
LEAF_G = m("#c9a23a", .08, 2, spec=1.2)
OLIVE = m("#7a8a4a", .10, 2, spec=.3)
INDIGO = m("#2a3450", .08, 2)
HEMP = m("#8a8a7a", .14, 1.2)
SILK_Y = m("#d8a828", .06, 2, spec=.7)
SILK_R = m("#a8221e", .08, 2)
BLACK = m("#1c1a1e", .08, 2, spec=.3)
BLACK_F = m("#24242a", .1, 1.5, spec=.2)
NAVY = m("#1e2a44", .08, 2)
WHITE = m("#efe9da", .04, 2)
LEOPARD = m("#d8a458", .10, 2)
SPOT = m("#3a2614", .1)
BLUE_K = m("#2a4a8a", .06, 2)
CRIMSON = m("#8a1e2a", .08, 2)
TURQ = m("#2a8a96", .08, 2, spec=.6)
FEATHER_R = m("#c83a22", .1, 2, (1, 4))
FEATHER_Y = m("#e8b830", .1, 2, (1, 4))
FEATHER_G = m("#2a8a5a", .1, 2, (1, 4))
FEATHER_B = m("#2a5aa8", .1, 2, (1, 4))
RED_WOOL = m("#b8221e", .1, 2)


def _robe(c, mat, hem=None, sleeve=True, length=116):
    pts = [(44, 20), (84, 20), (112, 40), (104, 58), (90, 50), (98, length), (30, length), (38, 50), (24, 58), (16, 40)] if sleeve else \
          [(44, 20), (84, 20), (96, 40), (100, length), (28, length), (32, 40)]
    c.poly(mat, *pts, bevel=2.0)
    for x in (48, 58, 70, 80):
        c.scratch(1.2, .3, (x, 64), (x + (x - 64) * .25, length - 4))
    if hem:
        c.rect(hem, 30, length - 8, 98, length - 2, 1, bevel=.8)


def _leaves(c, cx, cy, rx, ry, mat, gap=70, n=18, size=7):
    for k in range(n):
        a = math.radians(gap / 2 + (360 - gap) * k / (n - 1) + 90)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        t = a + math.pi / 2 + (.5 if k % 2 else -.5)
        c.poly(mat, (x - size * math.cos(t) * .2, y - size * math.sin(t) * .2), (x + size * math.cos(t + .5) * .6, y + size * math.sin(t + .5) * .6),
               (x + size * math.cos(t), y + size * math.sin(t)), (x + size * math.cos(t - .5) * .6, y + size * math.sin(t - .5) * .6), bevel=.8)


@painter
def garment(kind="toga"):
    c = Canvas(128, seed=1500 + len(kind))
    if kind == "toga":            # white wool draped over the left shoulder, purple border for magistrates
        _robe(c, WOOL_W, sleeve=False)
        c.poly(WOOL_W_D, (40, 22), (60, 20), (96, 104), (84, 116), bevel=1.6)
        c.line(PURPLE, 4, (42, 22), (88, 116))
        for k in range(4):
            c.scratch(1.2, .35, (50 + k * 6, 30 + k * 4), (80 + k * 4, 100))
        c.rect(PURPLE, 28, 108, 100, 115, 1, bevel=.8)
    elif kind == "kamishimo":     # sleeveless winged jacket over a striped hakama
        for i in range(6):
            c.rect(HEMP if i % 2 else m("#6a6a5e", .14, 1.2), 34 + i * 10, 64, 44 + i * 10, 118, 1, bevel=.8)
        c.poly(INDIGO, (22, 24), (54, 30), (64, 62), (74, 30), (106, 24), (100, 70), (28, 70), bevel=2.2)
        c.poly(WHITE, (54, 30), (64, 62), (74, 30), (70, 28), (64, 50), (58, 28), bevel=.8)
        for x in (40, 88):
            c.ell(WHITE, x, 46, 5, 5, bevel=.8)
            c.ell(INDIGO, x, 46, 2.4, 2.4)
    elif kind == "himation":      # a large wrapped mantle of blue-bordered wool
        _robe(c, m("#d8d0b8", .06, 2), sleeve=False)
        c.poly(m("#c0b598", .08, 2), (32, 40), (96, 30), (100, 70), (30, 84), bevel=1.6)
        c.rect(BLUE_K, 30, 106, 98, 113, 1, bevel=.8)
        c.line(BLUE_K, 3, (32, 84), (100, 70))
    elif kind == "dragon_robe":   # imperial yellow robe with a dragon and waves at the hem
        _robe(c, SILK_Y)
        for k in range(5):
            c.line(m("#2a5aa8", .06, 2), 2.4, (32 + k * 2, 112 - k * 4), (96 - k * 2, 112 - k * 4))
        pts = [(44, 90), (54, 76), (70, 80), (78, 64), (66, 52), (54, 58)]
        for i in range(len(pts) - 1):
            c.line(SILK_R, 4, pts[i], pts[i + 1])
        c.ell(SILK_R, 52, 58, 6, 5, bevel=1.0)
        c.ell(GOLD_S, 50, 57, 1.6, 1.6)
        c.poly(m("#2a2a3a", .08), (52, 20), (76, 20), (64, 44), bevel=1.0)
    elif kind == "frock_coat":    # black frock coat with tails, lapels and brass buttons
        c.poly(BLACK_F, (40, 20), (88, 20), (110, 38), (106, 70), (96, 64), (98, 118), (68, 112), (64, 70), (60, 112), (30, 118), (32, 64), (22, 70), (18, 38), bevel=2.0)
        c.poly(WHITE, (54, 20), (74, 20), (64, 46), bevel=.8)
        c.poly(m("#3a3a40", .08, 2, spec=.4), (50, 20), (64, 52), (58, 60), (44, 26), bevel=.8)
        c.poly(m("#3a3a40", .08, 2, spec=.4), (78, 20), (64, 52), (70, 60), (84, 26), bevel=.8)
        for y in (56, 68, 80):
            for x in (56, 72):
                c.ell(GOLD_S, x, y, 2.2, 2.2, bevel=.8)
    elif kind == "leopard_mantle":  # a priest's leopard skin over a white linen robe
        _robe(c, WHITE, sleeve=False)
        c.poly(LEOPARD, (34, 22), (80, 20), (100, 56), (94, 100), (60, 92), (40, 70), bevel=1.8)
        rnd = [(46, 34), (60, 30), (74, 32), (52, 48), (68, 46), (84, 50), (58, 62), (76, 64), (88, 76), (66, 80), (82, 90), (48, 58)]
        for x, y in rnd:
            c.ell(SPOT, x, y, 3.2, 2.6)
            c.ell(LEOPARD, x + .6, y + .2, 1.2, 1.0)
        c.ell(GOLD, 44, 28, 5, 5, bevel=1.2)
    elif kind == "candys":        # long Median robe with hanging sleeves
        _robe(c, CRIMSON, hem=GOLD_T)
        c.line(GOLD_T, 3, (64, 22), (64, 116))
        for side in (-1, 1):
            c.poly(m("#6a1620", .08, 2), (64 + side * 40, 42), (64 + side * 50, 50), (64 + side * 44, 96), (64 + side * 34, 90), bevel=1.4)
        for y in (40, 60, 80, 100):
            c.ell(TURQ, 64, y, 2.6, 2.6, bevel=.8)
    else:                         # feather cape: rows of red, yellow, green and blue feathers
        c.poly(m("#3a2a1e", .1), (44, 18), (84, 18), (108, 112), (20, 112), bevel=1.6)
        mats = (FEATHER_R, FEATHER_Y, FEATHER_G, FEATHER_B)
        for row in range(9):
            y = 24 + row * 10
            half = 22 + row * 4.5
            n = 6 + row
            for i in range(n):
                x = 64 - half + (2 * half) * (i + .5) / n
                c.poly(mats[(row + i) % 4], (x - 4, y), (x + 4, y), (x + 2, y + 13), (x, y + 15), (x - 2, y + 13), bevel=.8)
        c.rect(GOLD, 42, 16, 86, 22, 2, bevel=1.0)
    return c.image()


@painter
def headwear(kind="laurel"):
    c = Canvas(128, seed=1520 + len(kind))
    if kind == "laurel":          # gold laurel wreath
        _leaves(c, 64, 66, 40, 34, LEAF_G, n=22, size=10)
    elif kind == "olive":         # olive wreath of the games
        _leaves(c, 64, 66, 40, 34, OLIVE, n=22, size=10)
        for k in range(6):
            a = math.radians(140 + k * 52)
            c.ell(m("#3a4a2a", .1, 2, spec=.6), 64 + 34 * math.cos(a), 66 + 28 * math.sin(a), 2.6, 3.2, bevel=.8)
    elif kind == "circlet":       # a jarl's silver circlet with knotwork and a red stone
        c.ell(m("#c8ccd0", .06, 2, spec=1.2), 64, 68, 44, 22, bevel=2.0)
        c.ell(m("#2a2420", .1), 64, 64, 36, 15)
        for k in range(10):
            a = math.radians(30 + k * 12)
            c.line(m("#8a9094", .06, spec=.8), 1.2, (64 + 40 * math.cos(a), 68 + 19 * math.sin(a)), (64 + 40 * math.cos(a + .14), 68 + 19 * math.sin(a + .14)))
        c.ell(m("#9a1a1a", .06, 2, spec=1.4), 64, 88, 6, 5, bevel=1.4)
    elif kind == "jingasa":       # wide conical lacquered war hat with a mon
        c.poly(BLACK, (10, 82), (64, 40), (118, 82), (64, 94), bevel=2.4)
        c.poly(m("#2a2a30", .08, 2, spec=.6), (10, 82), (64, 94), (118, 82), (64, 98), bevel=1.0)
        c.ell(GOLD_S, 64, 66, 8, 6, bevel=1.2)
        c.ell(BLACK, 64, 66, 3, 2.2)
    elif kind == "futou":         # black gauze cap with two long stiff wings
        c.rect(BLACK, 40, 46, 88, 90, 10, bevel=2.0)
        c.ell(BLACK, 64, 46, 18, 12, bevel=1.6)
        for side in (-1, 1):
            c.poly(m("#2a2a30", .1, 2), (64 + side * 20, 64), (64 + side * 58, 58), (64 + side * 58, 64), (64 + side * 20, 70), bevel=.8)
    elif kind == "top_hat":       # tall black silk hat
        c.ell(BLACK, 64, 98, 48, 12, bevel=1.6)
        c.rect(BLACK, 38, 26, 90, 98, 4, bevel=2.2)
        c.ell(m("#2e2e34", .06, 2, spec=.8), 64, 26, 26, 7, bevel=1.2)
        c.rect(m("#3a2a2a", .08), 38, 84, 90, 92, 1, bevel=.6)
        c.scratch(1.4, .5, (46, 30), (46, 82))
    elif kind == "bicorne":       # an officer's bicorne with gold lace and a cockade
        c.poly(BLACK_F, (8, 80), (30, 50), (64, 36), (98, 50), (120, 80), (64, 70), bevel=2.2)
        c.line(GOLD_S, 3, (8, 80), (64, 70), (120, 80))
        c.ell(m("#1e2a5a", .06), 90, 56, 9, 9, bevel=1.0)
        c.ell(WHITE, 90, 56, 5, 5, bevel=.8)
        c.ell(RED_WOOL, 90, 56, 2.4, 2.4)
    elif kind == "nemes":         # striped royal headcloth with lappets and a gold cobra
        c.poly(GOLD_T, (36, 30), (92, 30), (110, 64), (98, 118), (82, 118), (84, 70), (44, 70), (46, 118), (30, 118), (18, 64), bevel=2.2)
        for k in range(8):
            y = 36 + k * 10
            c.line(BLUE_K, 3, (22 + (8 - k) * .4, y), (106 - (8 - k) * .4, y))
        c.poly(GOLD_S, (60, 30), (68, 30), (66, 18), (64, 14), (62, 18), bevel=1.0)
    elif kind == "kidaris":       # tall fluted royal tiara with a gold band
        c.poly(m("#e8d8b0", .06, 2), (34, 104), (40, 24), (88, 24), (94, 104), bevel=2.2)
        for x in range(44, 88, 8):
            c.line(m("#c8b890", .06), 2, (x, 28), (x + (x - 64) * .1, 100))
        for y in (24, 96):
            c.rect(GOLD_T, 34, y - 4, 94, y + 6, 2, bevel=1.2)
        for x in (46, 64, 82):
            c.ell(TURQ, x, 97, 3, 3, bevel=.8)
            c.poly(GOLD_S, (x - 5, 22), (x, 10), (x + 5, 22), bevel=.8)
    else:                         # mascaypacha: braided band with a red fringe and three feathers
        c.ell(m("#6a3a2a", .12, 2), 64, 56, 40, 18, bevel=1.8)
        c.ell(m("#2a1c10", .1), 64, 52, 32, 12)
        for k in range(12):
            x = 44 + k * 3.6
            c.line(RED_WOOL, 2.2, (x, 70), (x, 104))
        c.rect(GOLD, 42, 66, 86, 72, 2, bevel=.8)
        for k, mat in enumerate((FEATHER_R, m("#efe9da", .04, 2, (1, 4)), FEATHER_R)):
            x = 52 + k * 12
            c.poly(mat, (x - 3, 42), (x - 6, 16), (x, 6), (x + 4, 16), (x + 3, 42), bevel=1.0)
    return c.image()
