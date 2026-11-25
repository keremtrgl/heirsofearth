"""Heirs of Earth 3.2: weapon painters for the ten new weapons (128x128, handle bottom-left, point top-right)."""
import math

from heirs_art import BRONZE, DARKIRON, GOLD, IRON, LEATHER, LEATHER_D, STEEL, STONE_L, WOOD, WOOD_D, WOOD_V, Canvas, axis, blade, haft, m, painter, wraps

BRASS = m("#c9a24a", .08, 2, spec=1.1, tint="#9a7a2a")
BLADE = m("#b0b8bc", .05, 3, (9, 1), spec=1.0)
EDGE = m("#e4e9ec", .04, 2, spec=1.2)
DAMASK = m("#9aa0a4", .10, 1.2, (9, 1), spec=1.0)
WALNUT = m("#5a3a20", .14, 3, (9, 1))
GUNMETAL = m("#3e4246", .08, 3, (9, 1), spec=.9)
CORD = m("#b8a070", .12, 2, (6, 1))
WOOL_R = m("#a82a22", .1, 2)
WOOL_Y = m("#d8a830", .1, 2)
RED_SILK = m("#a51e22", .08, 2)
HORN = m("#e0d6bf", .06, 2)


@painter
def spatha():
    """The long cavalry sword of the late legions: a round pommel, a bone grip and a long straight blade."""
    c = Canvas(128, seed=1401)
    at, ln = axis((14, 116), (118, 10))
    c.ell(BRONZE, *at(2, 0), 6.0, 5.6, bevel=1.4)
    haft(c, at, 6, 24, 3.4, HORN)
    for u in range(8, 24, 4):
        c.line(m("#b8ad94", .06), .9, at(u, -3.4), at(u, 3.4))
    c.poly(BRONZE, at(24, -10), at(28, -10), at(28, 10), at(24, 10), bevel=1.2)
    blade(c, at, 28, ln, 4.2, 3.6, BLADE, tip=10, edge_mat=EDGE, fuller=True)
    return c.image()


@painter
def seax():
    """A single-edged Norse knife with a broken back, a horn grip and a brass-mounted leather sheath edge."""
    c = Canvas(128, seed=1402)
    at, ln = axis((22, 108), (104, 22))
    haft(c, at, 2, 30, 4.0, m("#3a2a1e", .14, 2, (1, 5)))
    for u in (4, 28):
        c.poly(BRASS, at(u - 2, -4.6), at(u + 2, -4.6), at(u + 2, 4.6), at(u - 2, 4.6), bevel=.8)
    pts = [at(32, -5), at(ln - 24, -6.5), at(ln - 4, 1.5), at(ln, 3.0), at(ln - 8, 4.6), at(32, 4.6)]
    c.poly(DAMASK, *pts, bevel=1.0)
    c.poly(EDGE, at(32, 2.2), at(ln - 8, 2.6), at(ln - 6, 4.4), at(32, 4.6), bevel=.4)
    c.scratch(.6, .35, at(36, -2.5), at(ln - 28, -3.4))
    return c.image()


@painter
def gastraphetes():
    """The Greek belly bow: a long stock with a curved rest for the belly, a slider and a heavy horn-and-sinew bow."""
    c = Canvas(128, seed=1403)
    at, ln = axis((14, 112), (114, 14))
    c.poly(WOOD, at(0, -9), at(10, -9), at(10, 9), at(0, 9), bevel=1.4)
    c.line(WOOD_D, 3, at(0, -9), at(-2, 0), at(0, 9))
    haft(c, at, 8, ln - 12, 3.4, m("#7a5634", .16, 3, (9, 1)))
    c.poly(WOOD_D, at(30, -4.2), at(ln - 18, -4.2), at(ln - 18, -2), at(30, -2), bevel=.8)
    pts = [at(ln - 22 + 8 * (1 - (k / 10) ** 2), -28 + 5.6 * k) for k in range(11)]
    for i in range(10):
        c.line(m("#3a2a1e", .12, 2), 5.0 - abs(i - 5) * .35, pts[i], pts[i + 1])
    c.line(CORD, 1.2, pts[0], at(40, 0), pts[-1])
    c.line(WOOD_V, 1.8, at(40, 0), at(ln - 4, 0))
    c.poly(BRONZE, at(ln - 6, -2.5), at(ln + 2, 0), at(ln - 6, 2.5), bevel=.6)
    c.ell(BRONZE, *at(36, -3), 3, 3, bevel=1.0)
    return c.image()


@painter
def dao():
    """A broad single-edged sabre with a disc guard, a red silk tassel and a ring pommel."""
    c = Canvas(128, seed=1404)
    at, ln = axis((22, 110), (108, 16))
    for k in range(5):
        c.line(RED_SILK, 1.6, at(0, 0), at(-10 + k, 10 + k * 3))
    c.ell(BRASS, *at(2, 0), 4.6, 4.6, bevel=1.2)
    c.ell(m("#1a1410", .1), *at(2, 0), 2.2, 2.2)
    wraps(c, at, 6, 26, 3.4, step=4, mats=(m("#2a1c18", .1, 2), m("#3e2a20", .1, 2)))
    c.ell(BRASS, *at(28, 0), 4, 9, bevel=1.4)
    curve = lambda u: -9 * ((u - 30) / (ln - 30)) ** 2
    widen = lambda u: 0
    blade(c, at, 30, ln, 4.0, 6.4, BLADE, tip=14, edge_mat=EDGE, fuller=False, off=curve)
    return c.image()


@painter
def blunderbuss():
    """A short flintlock gun with a flared brass muzzle and a walnut stock."""
    c = Canvas(128, seed=1405)
    at, ln = axis((14, 110), (116, 18))
    c.poly(WALNUT, at(0, -8), at(20, -5.6), at(34, -3.6), at(66, -3), at(66, 3), at(34, 4), at(18, 7.6), at(0, 9), bevel=1.6)
    c.poly(BRASS, at(-1, -8), at(2, -8), at(2, 9), at(-1, 9), bevel=.8)
    c.poly(BRASS, at(30, -2.8), at(ln - 16, -3.4), at(ln - 2, -8), at(ln, -8), at(ln, 8), at(ln - 2, 8), at(ln - 16, 3.4), at(30, 2.8), bevel=1.2)
    c.ell(m("#1a1410", .1), *at(ln, 0), 1.6, 6.6)
    for u in (44, 60):
        c.line(DARKIRON, 1.4, at(u, -3.4), at(u, 3.4))
    c.poly(GUNMETAL, at(28, -3), at(38, -3), at(38, -6), at(28, -6), bevel=.8)
    c.line(DARKIRON, 1.8, at(31, -5), at(28, -10), at(32, -12))
    c.line(DARKIRON, 1.6, at(34, 3.6), at(32, 7.6), at(28, 8.4))
    return c.image()


@painter
def flintlock_pistol():
    """A holster pistol: a curved walnut grip with a brass butt cap, an iron barrel and a flint cock."""
    c = Canvas(128, seed=1406)
    at, ln = axis((26, 100), (110, 34))
    c.poly(WALNUT, at(0, 4), at(6, -6), at(22, -5), at(30, -3.4), at(70, -2.8), at(70, 2.8), at(30, 3.4), at(22, 6), at(12, 14), at(2, 16), bevel=1.6)
    c.ell(BRASS, *at(2, 10), 5, 6.4, bevel=1.4)
    c.poly(GUNMETAL, at(28, -2.6), at(ln, -2.2), at(ln, 2.2), at(28, 2.6), bevel=.8)
    c.ell(GUNMETAL, *at(ln, 0), 1.6, 3.2, bevel=.6)
    c.line(BRASS, 1.6, at(ln - 8, -3), at(ln - 8, 3))
    c.poly(GUNMETAL, at(24, -3), at(34, -3), at(34, -6), at(24, -6), bevel=.8)
    c.line(DARKIRON, 1.8, at(27, -5), at(24, -10), at(28, -12))
    c.line(DARKIRON, 1.6, at(28, 3.4), at(26, 8), at(22, 8.6))
    c.line(DARKIRON, 1.2, at(26, 3.4), at(20, 8), at(30, 9), at(30, 4))
    return c.image()


@painter
def hedj():
    """The pear-shaped mace of the pharaohs: a white stone head on a wooden haft bound with gold."""
    c = Canvas(128, seed=1407)
    at, ln = axis((24, 112), (100, 20))
    haft(c, at, 0, ln - 20, 3.2, WOOD_V)
    for u in (4, 20, ln - 26):
        c.poly(GOLD, at(u, -3.8), at(u + 4, -3.8), at(u + 4, 3.8), at(u, 3.8), bevel=.8)
    head = [at(ln - 24, -5), at(ln - 14, -10), at(ln - 4, -12), at(ln + 4, -8), at(ln + 6, 0), at(ln + 4, 8), at(ln - 4, 12), at(ln - 14, 10), at(ln - 24, 5)]
    c.poly(m("#e8e0cc", .06, 2, spec=.5), *head, bevel=2.2)
    c.line(m("#2a4a8a", .06, 2), 1.4, at(ln - 12, -10), at(ln - 12, 10))
    return c.image()


@painter
def shamshir():
    """The deeply curved Persian sabre: a horn grip with a capped pommel, a cross guard and a narrow, sharply bent blade."""
    c = Canvas(128, seed=1408)
    at, ln = axis((18, 112), (110, 24))
    c.poly(m("#2a1c18", .1, 2), at(0, -4), at(4, -6), at(6, 3.6), at(0, 3.6), bevel=1.0)
    haft(c, at, 2, 22, 3.0, m("#3a2a1e", .14, 2, (1, 5)))
    c.poly(GOLD, at(22, -10), at(25, -10), at(25, 10), at(22, 10), bevel=1.0)
    curve = lambda u: -16 * ((u - 26) / (ln - 26)) ** 2.2
    blade(c, at, 26, ln, 3.2, 2.2, DAMASK, tip=12, edge_mat=EDGE, fuller=False, off=curve)
    return c.image()


@painter
def bolas():
    """Three cord-wrapped stones joined by braided cords."""
    c = Canvas(128, seed=1409)
    centre = (62, 60)
    ends = [(30, 26), (100, 40), (54, 106)]
    for i, (x, y) in enumerate(ends):
        mid = ((centre[0] + x) / 2 + (8 if i == 1 else -6), (centre[1] + y) / 2 + 4)
        for k, mat in enumerate((WOOL_R, WOOL_Y)):
            c.line(mat, 1.8, (centre[0] + k, centre[1]), (mid[0] + k, mid[1]), (x + k, y))
    c.ell(WOOL_R, *centre, 4, 4, bevel=1.0)
    for x, y in ends:
        c.ell(m("#8a8a86", .14, 2, spec=.5), x, y, 11, 10, bevel=2.0)
        for k in range(3):
            c.line(CORD, 1.4, (x - 10, y - 4 + k * 4), (x + 10, y - 6 + k * 4))
    return c.image()


@painter
def chuki():
    """The Inca lance: a long dark hardwood shaft, a bronze leaf blade and a tuft of red and yellow wool below it."""
    c = Canvas(128, seed=1410)
    at, ln = axis((10, 118), (118, 10))
    haft(c, at, 0, ln - 26, 2.6, m("#3a2a1e", .14, 2, (9, 1)))
    c.poly(BRONZE, at(-2, -3), at(4, -3), at(4, 3), at(-2, 3), bevel=.8)
    for k in range(6):
        c.line(WOOL_R if k % 2 else WOOL_Y, 1.6, at(ln - 30, 0), at(ln - 44 + k, -6 + k * 2.4))
    c.poly(BRONZE, at(ln - 30, -3.2), at(ln - 26, -3.2), at(ln - 26, 3.2), at(ln - 30, 3.2), bevel=.8)
    blade(c, at, ln - 26, ln, 5.2, 3.0, m("#c08a3c", .08, 2, spec=1.1), tip=12, edge_mat=m("#e0b060", .05, 2, spec=1.2), fuller=False)
    return c.image()
