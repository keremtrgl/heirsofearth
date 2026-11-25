"""Heirs of Earth 4.2 "Ages of Progress": the firearms of the Powder and Steam ages and each nation's uniform coat.

Guns share one build (stock, lock, barrel, bands) and differ by the lock of their age (matchlock, flintlock, bolt, falling block)
and by the nation's own decoration. Uniforms are worn garments in the 4.1 manner (heirs_art19): drawn on the vanilla bodies, the
cloth part marked in the mask so the uniform's own colour (a fixed colour per nation) tints it; trims and badges keep theirs.
"""
import math

import numpy as np

import heirs_art19 as W
from heirs_art import DARKIRON, GOLD, STEEL, Canvas, axis, m, painter
from heirs_art2 import LACQUER, LACQUER_R
from heirs_art4 import BRASS, IMP_RED
from heirs_art18 import GOLD as GOLD_H
from heirs_art19 import BLACK, BRONZE, NAVY, STUFF_D, STUFF_DD, belt, folds, front_u, grown_body, px, studs, trim_line

# ------------------------------------------------------------------ materials
WALNUT = m("#5a3a20", .14, 3, (9, 1))
WALNUT_L = m("#7a5232", .14, 3, (9, 1))
BIRCH = m("#c8a878", .12, 3, (9, 1))
PINE = m("#a77a4a", .16, 3, (9, 1))
TEAK = m("#6e4026", .14, 3, (9, 1))
BLACK_LAC = m("#1e1a18", .06, 2, spec=.7)
GUNMETAL = m("#3a3e42", .08, 3, (9, 1), spec=.9)
BLUED = m("#2a3038", .08, 3, (9, 1), spec=1.1)
SILVER = m("#c8ccd0", .05, 2, spec=1.2)
TURQ = m("#2aa09a", .08, 2, spec=.8)
ROPE = m("#b89a62", .14, 1.5, (1, 4))
RED_CORD = m("#b02a22", .1, 1.5, (1, 4))
IVORY = m("#e8dcc0", .05, 2, spec=.5)


def gun(seed, stock, lock, *, length=118, barrel=GUNMETAL, bands=BRASS, band_at=(48, 66, 82), butt=BRASS, wrist=None,
        fore=None, bayonet=False, slim=1.0):
    """A long gun on the diagonal. Returns the canvas and helpers so a nation's decoration can be added on top.
    lock: "match" (serpentine and glowing cord), "flint" (cock and frizzen), "bolt" (bolt handle, magazine), "block" (lever under the wrist)."""
    c = Canvas(128, seed=seed)
    at, ln = axis((12, 112), (length, 12))
    L = ln - (18 if bayonet else 0)
    s = slim
    # the stock runs under the barrel to near the muzzle (the fore-end), so the wood reads along the whole gun
    c.poly(stock, at(0, -7 * s), at(16, -5 * s), at(26, -3 * s), at(L - 10, -1.4 * s), at(L - 8, 0.4 * s), at(L - 10, 3.0 * s),
           at(40, 3.6 * s), at(26, 4.2 * s), at(14, 7 * s), at(0, 8 * s), bevel=1.6)
    if wrist is not None:
        c.poly(wrist, at(14, -5.2 * s), at(26, -3.2 * s), at(26, 4.2 * s), at(14, 6.6 * s), bevel=1.0)
    if fore is not None:
        c.poly(fore, at(40, -1.2 * s), at(L - 14, -1.0 * s), at(L - 14, 2.8 * s), at(40, 3.4 * s), bevel=.8)
    c.poly(butt, at(-1, -7 * s), at(2, -7 * s), at(2, 8 * s), at(-1, 8 * s), bevel=.8)
    c.poly(barrel, at(24, -2.8 * s), at(L, -2.3 * s), at(L, 0.3 * s), at(24, 0.6 * s), bevel=.8)
    c.line(m("#2c2a28", .08, spec=.6), 0.9, at(42, 2.6 * s), at(L - 6, 1.6 * s))                     # ramrod
    for u in band_at:
        if u < L - 2:
            c.line(bands, 1.6, at(u, -3.2 * s), at(u, 3.4 * s))
    if lock == "match":
        c.poly(barrel, at(24, -3), at(36, -3), at(36, -5.6), at(24, -5.6), bevel=.8)
        c.line(BRASS, 2.0, at(28, 2.4), at(31, -4), at(35, -4.6))
        c.line(ROPE, 1.3, at(35, -4.6), at(39, -7.5), at(35, -10), at(29, -9), at(27, -6.5))       # the slow match, coiled at the lock
        c.ell(m("#ffb040", .1), *at(35, -4.8), 1.5, 1.5)
        c.glow(*at(35, -4.8), 6, "#ff9a3a", .55)
    elif lock == "flint":
        c.poly(barrel, at(24, -3), at(36, -3), at(36, -6), at(24, -6), bevel=.8)
        c.line(DARKIRON, 1.8, at(29, -5), at(26, -10), at(30, -12))
        c.line(DARKIRON, 1.4, at(34, -5.6), at(35, -9))
    elif lock == "bolt":
        c.poly(barrel, at(22, -3.2), at(40, -3.2), at(40, 3.4), at(22, 3.4), bevel=1.0)
        c.line(STEEL, 1.6, at(34, -3), at(36, -8))
        c.ell(STEEL, *at(36, -8.6), 1.7, 1.7, bevel=.6)
        c.poly(barrel, at(30, 3.4), at(38, 3.4), at(37, 8.5), at(30, 8.5), bevel=.8)           # magazine
    elif lock == "block":
        c.poly(barrel, at(22, -3.4), at(36, -3.4), at(36, 3.6), at(22, 3.6), bevel=1.0)
        c.line(barrel, 1.8, at(30, 3.6), at(24, 9), at(12, 9.5))                               # the lever under the wrist
    c.line(DARKIRON, 1.6, at(32, 3 * s), at(30, 7 * s), at(26, 8 * s))                       # trigger guard
    if bayonet:
        c.poly(STEEL, at(L - 4, 2), at(L, 2), at(L, 4.5), at(L - 4, 4.5), bevel=.6)
        c.poly(m("#c0c8cc", .04, 3, (9, 1), spec=1.2), at(L - 2, 3.4), at(ln - 4, 3.6), at(ln, 3.4), at(ln - 4, 5.8), at(L - 2, 5.6), bevel=.6)
    return c, at, ln, L


def sling(c, at, a, b, mat=m("#d8cfb8", .05)):
    c.line(mat, 1.2, at(a, 7.5), at((a + b) / 2, 10), at(b, 4), bevel=.4)


# ------------------------------------------------------------------ Powder age (II)
@painter
def roma_arquebus():
    """Nova Roma: a matchlock arquebus with a red-lacquered stock and a brass eagle on the lock plate."""
    c, at, ln, L = gun(301, WALNUT, "match", wrist=LACQUER_R)
    c.ell(BRASS, *at(20, 1), 3.0, 3.0, bevel=1.0)
    c.poly(m("#f0d070", .05), at(18.5, 0.2), at(20, -1.4), at(21.5, 0.2), at(20, 2.2), bevel=.4)
    c.poly(BRASS, at(ln - 3, -2.4), at(ln, -2.4), at(ln, 2.4), at(ln - 3, 2.4), bevel=.6)
    sling(c, at, 10, 52)
    return c.image()


@painter
def nord_hookgun():
    """Nordheim: a heavy hook gun (hakebosse) on a carved pine stock, the iron hook under the barrel to brace on a rail."""
    c, at, ln, L = gun(302, PINE, "match", band_at=(46, 70), bands=DARKIRON, butt=DARKIRON, slim=1.15)
    c.poly(DARKIRON, at(L - 30, 1.8), at(L - 26, 1.8), at(L - 27, 7.5), at(L - 33, 8), at(L - 32, 6.2), at(L - 29, 6), bevel=.6)
    for k in range(4):
        c.scratch(.8, .45, at(3 + k * 5, -4), at(7 + k * 5, 6))
    c.line(m("#5a3a20", .1), 1.0, at(4, -5), at(10, 0), at(4, 5))                            # knot carving
    return c.image()


@painter
def hellas_musket():
    """Hellas: a flintlock musket with silver bands and a running meander inlaid along the stock."""
    c, at, ln, L = gun(303, WALNUT_L, "flint", bands=SILVER, butt=SILVER)
    for k in range(5):
        u = 4 + k * 4
        c.line(SILVER, .8, at(u, 4.5), at(u, 2.5), at(u + 2, 2.5), at(u + 2, 3.6))
    c.poly(SILVER, at(ln - 3, -2.4), at(ln, -2.4), at(ln, 2.4), at(ln - 3, 2.4), bevel=.6)
    sling(c, at, 10, 54, m("#2e5c8c", .06))
    return c.image()


@painter
def tianxia_birdgun():
    """Tianxia: the long, slender bird gun (niaochong) with a curved pistol stock, black lacquer and a red cord."""
    c, at, ln, L = gun(304, BLACK_LAC, "match", length=122, band_at=(42, 58, 74, 90), slim=0.85)
    c.poly(LACQUER_R, at(0, -6), at(6, -6), at(10, 7), at(0, 7), bevel=.8)
    c.line(RED_CORD, 1.3, at(20, 6), at(22, 11), at(18, 15))
    c.ell(IMP_RED, *at(18, 15.5), 1.8, 2.4)
    return c.image()


@painter
def kemet_musket():
    """New Kemet: a long musket with brass bands, turquoise inlay and a lotus on the butt."""
    c, at, ln, L = gun(305, TEAK, "flint", length=120)
    for u in (8, 14, 20):
        c.ell(TURQ, *at(u, 2.5), 1.3, 1.3, bevel=.4)
    c.poly(GOLD, at(3, -2), at(6, 0), at(3, 2), at(5, 0), bevel=.4)
    c.poly(BRASS, at(ln - 3, -2.4), at(ln, -2.4), at(ln, 2.4), at(ln - 3, 2.4), bevel=.6)
    sling(c, at, 10, 56, m("#2aa09a", .06))
    return c.image()


@painter
def inti_arquebus():
    """Inti: an arquebus whose stock is inlaid with tocapu squares and bound with gold."""
    c, at, ln, L = gun(306, m("#7a4a2a", .14, 3, (9, 1)), "match", bands=GOLD, butt=GOLD)
    colours = ("#c8322a", "#e6c23a", "#2a2a2a", "#2f5f9e")
    for k in range(4):
        u = 4 + k * 4.5
        c.poly(m(colours[k], .05), at(u, -2.4), at(u + 3.4, -2.4), at(u + 3.4, 1.4), at(u, 1.4), bevel=.3)
    return c.image()


# ------------------------------------------------------------------ Steam age (III)
@painter
def yamato_rifle():
    """Yamato: a bolt-action rifle with a black-lacquered stock, brass cherry blossom and a sword bayonet."""
    c, at, ln, L = gun(311, BLACK_LAC, "bolt", band_at=(50, 70), bands=BLUED, barrel=BLUED, butt=BLUED, bayonet=True)
    c.ell(BRASS, *at(18, 1), 2.6, 2.6, bevel=.8)
    for k in range(5):
        a = k * 72
        c.ell(m("#f2c4cc", .05), *at(18 + 1.6 * math.cos(math.radians(a)), 1 + 1.6 * math.sin(math.radians(a))), .9, .9)
    sling(c, at, 10, 50)
    return c.image()


@painter
def nord_rifle():
    """Nordheim: a bolt rifle with a pale birch stock and the box magazine on its side."""
    c, at, ln, L = gun(312, BIRCH, "bolt", band_at=(52, 74), bands=BLUED, barrel=BLUED, butt=BLUED)
    c.poly(BLUED, at(36, -3.2), at(46, -3.2), at(46, -6.4), at(36, -6.4), bevel=.8)            # side magazine
    c.line(m("#5a3a20", .1), 1.0, at(4, -5), at(10, 0), at(4, 5))
    sling(c, at, 10, 52, m("#5a4a3a", .06))
    return c.image()


@painter
def hellas_rifle():
    """Hellas: a single-shot bolt rifle with a walnut stock, silver bands and a long sword bayonet."""
    c, at, ln, L = gun(313, WALNUT_L, "bolt", bands=SILVER, butt=SILVER, barrel=BLUED, bayonet=True)
    c.ell(m("#2e5c8c", .06), *at(18, 1), 2.4, 2.4, bevel=.8)
    c.poly(m("#efefef", .03), at(16.6, 0.6), at(19.4, 0.6), at(19.4, 1.4), at(16.6, 1.4), bevel=.2)
    sling(c, at, 10, 50, m("#2e5c8c", .06))
    return c.image()


@painter
def tianxia_rifle():
    """Tianxia: a bolt rifle with a dark red stock, brass bands and a red tassel at the muzzle."""
    c, at, ln, L = gun(314, m("#5a2018", .12, 3, (9, 1)), "bolt", band_at=(50, 72), barrel=BLUED)
    c.line(RED_CORD, 1.2, at(ln - 6, 1.6), at(ln - 8, 6), at(ln - 6, 10))
    c.ell(IMP_RED, *at(ln - 6, 10.5), 1.6, 2.2)
    c.ell(GOLD, *at(18, 1), 2.2, 2.2, bevel=.8)
    return c.image()


@painter
def albion_breechloader():
    """Albion: a falling-block breech-loader, lever under the wrist, walnut stock and a brass butt plate."""
    c, at, ln, L = gun(315, WALNUT, "block", band_at=(54, 76), barrel=BLUED, bands=BLUED, bayonet=True)
    c.poly(BLUED, at(24, -3.0), at(36, -3.0), at(36, 3.2), at(24, 3.2), bevel=.6)
    sling(c, at, 10, 52)
    return c.image()


@painter
def pars_rifle():
    """Pars: a bolt rifle with a stock inlaid in khatam (tiny stars of bone, brass and wood) and silver bands."""
    c, at, ln, L = gun(316, m("#4a2a1a", .12, 3, (9, 1)), "bolt", bands=SILVER, butt=SILVER, barrel=BLUED)
    for k in range(5):
        u = 4 + k * 4
        for dv in (-2.2, 1.6):
            c.poly(IVORY, at(u, dv - 1), at(u + 1, dv), at(u, dv + 1), at(u - 1, dv), bevel=.2)
    sling(c, at, 10, 52, m("#2a4a7a", .06))
    return c.image()


# ------------------------------------------------------------------ uniform coats (worn)
def coat_base(w, length=1.02):
    """A knee-length military coat: full body, flared skirt, a dark seam down the front."""
    w.extend(w.poly([(0.02, 0.6), (0.98, 0.6), (1.03, length + 0.06), (-0.03, length + 0.06)], True) * grown_body(w.body, w.rot, 3.5))
    w.base()


def collar(w, color, stuff=False):
    if w.rot == "north":
        w.add(w.band(0.0, 0.07), color, stuff, "cyl", lw=0.9)
    else:
        fu = front_u(w)
        w.add(w.poly([(fu - 0.2, 0.0), (fu + 0.2, 0.0), (fu + 0.12, 0.1), (fu - 0.12, 0.1)]), color, stuff, "cyl", lw=0.9)


def buttons(w, color=GOLD_H, rows=(0.22, 0.34, 0.46, 0.58), double=False, r=1.2):
    if w.rot == "north":
        return
    fu = front_u(w)
    for v in rows:
        pts = [(fu - 0.09, v), (fu + 0.09, v)] if double and w.rot == "south" else [(fu + (0.03 if w.rot == "east" else 0), v)]
        studs(w, pts, px(w, r), color)


def front_seam(w, v0=0.1, v1=1.05):
    if w.rot == "north":
        w.lines(w.stroke([(0.5, 0.62), (0.5, v1)], 1.1), STUFF_DD)
        return
    fu = front_u(w)
    w.lines(w.stroke([(fu, v0), (fu + 0.01, 0.6), (fu - 0.01, v1)], 1.1), STUFF_DD)


def roma_coat(w):
    coat_base(w)
    collar(w, BRONZE)
    front_seam(w)
    buttons(w, BRONZE, double=True)
    belt(w, 0.6, 0.06, BLACK, buckle=BRONZE)
    if w.rot == "south":
        w.add(w.ell(0.5, 0.15, 0.07, 0.05), GOLD_H, False, "dome", lw=0.7, gloss=0.4)                       # eagle gorget
    folds(w, 4, 0.7, 1.05, width=0.8)


def yamato_coat(w):
    coat_base(w, 0.86)
    collar(w, "#a51e2c")
    if w.rot == "south":
        for v in (0.24, 0.32, 0.40, 0.48):                                                               # gold frogging across the chest
            trim_line(w, [(0.3, v), (0.5, v + 0.01), (0.7, v)], px(w, 1.4), GOLD_H)
    elif w.rot == "east":
        for v in (0.26, 0.36, 0.46):
            trim_line(w, [(0.6, v), (0.84, v)], px(w, 1.4), GOLD_H)
    front_seam(w, v1=0.92)
    belt(w, 0.6, 0.05, BLACK, buckle=GOLD_H)
    w.add(w.band(0.88, 0.95), "#a51e2c", False, "cyl", lw=0.8)


def nord_coat(w):
    coat_base(w)
    if w.rot == "north":
        w.add(w.band(-0.02, 0.1), "#8a6a48", False, "cyl", lw=0.9)
    else:
        fu = front_u(w)
        w.add(w.poly([(fu - 0.26, -0.02), (fu + 0.26, -0.02), (fu + 0.16, 0.14), (fu - 0.16, 0.14)]), "#8a6a48", False, "cyl", lw=0.9)  # fur collar
    front_seam(w)
    buttons(w, "#c8ccd0", rows=(0.24, 0.36, 0.48, 0.6, 0.72), double=True)
    belt(w, 0.6, 0.05, "#3a2a1c", buckle="#c8ccd0")
    folds(w, 4, 0.7, 1.05, width=0.8)


def hellas_coat(w):
    """An evzone's dress: a dark blue embroidered jacket over the white pleated fustanella."""
    w.extend(w.poly([(0.0, 0.58), (1.0, 0.58), (1.12, 1.06), (-0.12, 1.06)], True) * grown_body(w.body, w.rot, 4.5))
    w.base()
    skirt = w.below(0.62)
    w.add(skirt, "#f2efe6", False, "cyl", lw=0.9)
    for i in range(10):
        u = 0.02 + 0.96 * (i + 0.5) / 10
        w.lines(w.stroke([(u, 0.66), (u + (u - 0.5) * 0.1, 1.04)], 0.7) * skirt, "#bdb6a6", False)
    if w.rot != "north":
        fu = front_u(w)
        trim_line(w, [(fu - 0.2, 0.1), (fu - 0.24, 0.36), (fu - 0.14, 0.58)], px(w, 1.6), GOLD_H)
        trim_line(w, [(fu + 0.2, 0.1), (fu + 0.24, 0.36), (fu + 0.14, 0.58)], px(w, 1.6), GOLD_H)
    else:
        trim_line(w, [(0.3, 0.2), (0.5, 0.32), (0.7, 0.2)], px(w, 1.6), GOLD_H)
    belt(w, 0.56, 0.06, "#a51e2c")


def tianxia_coat(w):
    """A short army coat with a dark border and the round placard on the chest."""
    coat_base(w, 0.9)
    w.add(w.band(0.86, 0.96), NAVY, False, "cyl", lw=0.8)
    collar(w, NAVY)
    if w.rot == "south":
        w.add(w.ell(0.5, 0.36, 0.17, 0.11), "#f0ead8", False, "flat", lw=0.9)
        w.add(w.ell(0.5, 0.36, 0.11, 0.07), "#9c2a20", False, "flat", lw=0.6)
    elif w.rot == "north":
        w.add(w.ell(0.5, 0.36, 0.17, 0.11), "#f0ead8", False, "flat", lw=0.9)
    front_seam(w, v1=0.94)
    if w.rot == "east":
        trim_line(w, [(0.52, 0.06), (0.8, 0.32), (0.86, 0.9)], px(w, 2.2), NAVY)


def albion_coat(w):
    """Rifle green with black facings and black buttons, a cross belt and pouch."""
    coat_base(w, 0.84)
    collar(w, BLACK)
    if w.rot == "south":
        for s in (-1, 1):
            trim_line(w, [(0.5 + s * 0.1, 0.1), (0.5 + s * 0.12, 0.64)], px(w, 2.6), BLACK)
        studs(w, [(0.5 + s * 0.14, v) for s in (-1, 1) for v in (0.22, 0.34, 0.46)], px(w, 1.1), BLACK)
        trim_line(w, [(0.86, 0.12), (0.5, 0.48), (0.18, 0.86)], px(w, 2.6), BLACK)
    elif w.rot == "east":
        trim_line(w, [(0.4, 0.12), (0.6, 0.5), (0.8, 0.84)], px(w, 2.6), BLACK)
        studs(w, [(0.78, v) for v in (0.26, 0.38, 0.5)], px(w, 1.1), BLACK)
    else:
        trim_line(w, [(0.16, 0.12), (0.5, 0.48), (0.84, 0.86)], px(w, 2.6), BLACK)
        w.add(w.ell(0.74, 0.74, 0.1, 0.07), BLACK, False, "dome", lw=0.7)                                  # pouch
    front_seam(w, v1=0.9)
    belt(w, 0.6, 0.05, BLACK)


def kemet_coat(w):
    """Khaki with a turquoise collar echoing the broad collar, a leather belt with a shoulder strap."""
    coat_base(w, 0.84)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.22, 0.0), (fu + 0.22, 0.0), (fu + 0.14, 0.12), (fu - 0.14, 0.12)]), "#2aa09a", False, "cyl", lw=0.9)
    else:
        w.add(w.band(0.0, 0.07), "#2aa09a", False, "cyl", lw=0.9)
    front_seam(w, v1=0.9)
    buttons(w, BRONZE, rows=(0.24, 0.38, 0.52))
    belt(w, 0.6, 0.055, "#6b4a2c", buckle=BRONZE)
    if w.rot == "south":
        trim_line(w, [(0.84, 0.1), (0.6, 0.36), (0.38, 0.6)], px(w, 2.0), "#6b4a2c")
        for u in (0.3, 0.7):
            w.add(w.poly([(u - 0.1, 0.24), (u + 0.1, 0.24), (u + 0.09, 0.32), (u - 0.09, 0.32)]), STUFF_D, True, "cyl", lw=0.8)  # pockets


def pars_coat(w):
    """A long chokha: rows of silver cartridge loops on the chest, a dark narrow belt with a silver dagger frog."""
    coat_base(w, 1.04)
    front_seam(w)
    if w.rot == "south":
        for side in (0.27, 0.73):
            for k in range(6):
                u = side - 0.1 + k * 0.04
                w.add(w.poly([(u - 0.012, 0.18), (u + 0.012, 0.18), (u + 0.012, 0.36), (u - 0.012, 0.36)]), "#c8ccd0", False, "flat", lw=0.5, gloss=0.3)
    elif w.rot == "east":
        for k in range(5):
            u = 0.6 + k * 0.045
            w.add(w.poly([(u - 0.012, 0.2), (u + 0.012, 0.2), (u + 0.012, 0.36), (u - 0.012, 0.36)]), "#c8ccd0", False, "flat", lw=0.5, gloss=0.3)
    belt(w, 0.58, 0.04, BLACK, buckle="#c8ccd0")
    folds(w, 5, 0.66, 1.06, width=0.8)


def inti_coat(w):
    """An ochre field coat with a tocapu band across the chest and a gold sun badge."""
    coat_base(w, 0.88)
    if w.rot != "north":
        colours = ("#c8322a", "#e6c23a", "#2a2a2a", "#2f5f9e", "#2a7a3a")
        for i in range(8):
            u0 = 0.1 + i * 0.1
            w.add(w.poly([(u0, 0.4), (u0 + 0.095, 0.4), (u0 + 0.095, 0.47), (u0, 0.47)]), colours[i % 5], False, "flat", lw=0.6)
    if w.rot == "south":
        w.add(w.ell(0.5, 0.22, 0.07, 0.05), GOLD_H, False, "dome", lw=0.7, gloss=0.5)
    front_seam(w, v1=0.94)
    belt(w, 0.62, 0.05, "#4a311c", buckle=GOLD_H)


COATS = {
    "HE_Roma_FieldCoat": (roma_coat, 2.6, 2.6), "HE_Yamato_ArmyCoat": (yamato_coat, 2.6, 2.6), "HE_Nord_FieldCoat": (nord_coat, 2.8, 2.8),
    "HE_Hellas_Evzone": (hellas_coat, 2.6, 2.6), "HE_Tianxia_ArmyCoat": (tianxia_coat, 2.6, 2.6), "HE_Albion_RifleGreen": (albion_coat, 2.6, 2.6),
    "HE_Kemet_FieldCoat": (kemet_coat, 2.6, 2.6), "HE_Pars_Chokha": (pars_coat, 2.6, 2.6), "HE_Inti_FieldCoat": (inti_coat, 2.6, 2.6),
}
W.GARMENTS.update(COATS)


@painter
def heirs_coat_icon(kind, mask=False):
    """The inventory icon: the coat as it is worn, seen from the front, on its own. Like the worn graphic it is painted in greys
    with a mask (the icon uses the CutoutComplex shader), so the coat's colour tints the cloth and leaves trims and buttons alone."""
    from PIL import Image
    img, m = W.draw(kind, "Male", "south")
    box = img.getbbox()
    scale = min(104 / (box[2] - box[0]), 112 / (box[3] - box[1]))

    def fit(im):
        im = im.crop(box)
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        out = Image.new("RGBA", (128, 128), (0, 0, 0, 0) if not mask else (0, 0, 0, 255))
        out.paste(im, ((128 - im.width) // 2, (128 - im.height) // 2))
        return out
    return fit(m) if mask else fit(img)
