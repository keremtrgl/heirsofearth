"""Heirs of Earth 3.4: the embassy, seen from above: a paved hall floor with a long rug, a writing desk with letters and a seal,
two envoy chairs and nine banner stands along the back wall, one in the colour of every heir nation."""
import math

from heirs_art import m, painter
from heirs_art9 import NATIONS
from kut_render import BRONZE, GOLD, STONE, STONE_D, STONE_L, WOOD, WOOD_D, Canvas

RUG = m("#7a2a2a", .10, 2, (1, 3))
RUG_EDGE = m("#c49a4a", .08, 2)
PAPER = m("#ece2c6", .03, 2)
WAX = m("#9a1e1e", .05, 2, spec=.6)
SHADOW = m("#1a140e", .1)


@painter
def embassy(size=(3, 3)):
    W = 384
    c = Canvas(W, W, seed=1601)
    c.rect(SHADOW, 14, 18, W - 6, W - 4, 16)
    c.rect(STONE_D, 8, 8, W - 8, W - 8, 14, bevel=2.6)
    c.rect(STONE_L, 20, 20, W - 20, W - 20, 10, bevel=1.8)
    for k in range(1, 6):                                   # paving joints
        c.scratch(1.0, .3, (20, 20 + k * 57), (W - 20, 20 + k * 57))
        c.scratch(1.0, .3, (20 + k * 57, 20), (20 + k * 57, W - 20))

    # nine banner stands along the back wall
    for k in range(9):
        x = 42 + k * 37.5
        c.ell(SHADOW, x + 3, 58, 9, 5)
        c.ell(BRONZE, x, 54, 7, 7, bevel=1.4)
        c.rect(m(NATIONS[k], .10, 1.5, spec=.3), x - 11, 30, x + 11, 50, 2, bevel=1.6)
        c.poly(m(NATIONS[k], .10, 1.5, spec=.3), (x - 11, 50), (x + 11, 50), (x, 60), bevel=1.2)
        c.line(GOLD, 2, (x - 13, 30), (x + 13, 30))

    # the long rug from the door to the desk
    c.rect(RUG_EDGE, 140, 120, 244, W - 22, 4, bevel=1.2)
    c.rect(RUG, 148, 128, 236, W - 30, 3, bevel=1.0)
    for y in range(150, W - 40, 40):
        c.poly(RUG_EDGE, (192, y), (204, y + 12), (192, y + 24), (180, y + 12), bevel=.8)

    # the desk with letters, an ink pot and the seal
    c.rect(SHADOW, 104, 116, 290, 176, 6)
    c.rect(WOOD_D, 96, 106, 288, 168, 6, bevel=2.4)
    c.rect(WOOD, 104, 112, 280, 160, 4, bevel=1.6)
    for k, (x, y, a) in enumerate(((140, 132, -.12), (176, 128, .08), (230, 134, -.05))):
        dx, dy = 18 * math.cos(a), 18 * math.sin(a)
        c.poly(PAPER, (x - dx + dy * .7, y - dy - dx * .7), (x + dx + dy * .7, y + dy - dx * .7),
               (x + dx - dy * .7, y + dy + dx * .7), (x - dx - dy * .7, y - dy + dx * .7), bevel=.6)
        c.line(m("#4a3a2a", .05), 1, (x - 12, y - 4), (x + 10, y - 4))
        c.line(m("#4a3a2a", .05), 1, (x - 12, y + 2), (x + 6, y + 2))
    c.ell(WAX, 234, 136, 6, 6, bevel=1.2)
    c.ell(m("#1a1a22", .05, 2, spec=.8), 262, 124, 7, 7, bevel=1.4)
    c.line(m("#e8e0d0", .05), 1.4, (262, 124), (272, 110))
    c.ell(GOLD, 120, 150, 7, 5, bevel=1.2)

    # two envoy chairs facing the desk, and the host's chair behind it
    for x in (150, 234):
        c.rect(SHADOW, x - 18, 196, x + 22, 236, 4)
        c.rect(WOOD_D, x - 20, 190, x + 20, 232, 4, bevel=1.6)
        c.rect(m("#5a2a3a", .1, 2), x - 15, 194, x + 15, 222, 3, bevel=1.4)
    c.rect(WOOD_D, 170, 76, 214, 104, 4, bevel=1.6)
    c.rect(m("#2a3a5a", .1, 2), 175, 80, 209, 100, 3, bevel=1.4)

    # two potted bay trees at the door
    for x in (60, W - 60):
        c.ell(SHADOW, x + 4, W - 50, 24, 14)
        c.ell(m("#8a5a3a", .1, 2), x, W - 56, 20, 20, bevel=1.8)
        for k in range(7):
            a = k * 2 * math.pi / 7
            c.ell(m("#3e5a2a", .16, 2), x + 10 * math.cos(a), W - 56 + 10 * math.sin(a), 12, 11, bevel=1.4)
        c.ell(m("#5a7a3a", .14, 2), x, W - 58, 10, 9, bevel=1.4)
    c.rect(STONE, 150, W - 18, 234, W - 6, 3, bevel=1.2)     # the threshold
    return c.image()
