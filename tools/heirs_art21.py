"""Heirs of Earth 4.3 "Electric Age": the late-game guns, steel helmets and field uniforms of the nine nations.

Guns use the long-gun build of 4.2 (heirs_art20.gun) with the age's machinery added (pan magazine and cooling jacket, telescope,
pump, box magazine, a broom-handled pistol in its wooden box). Helmets are drawn like the 3.6 headgear (heirs_art18.Hat): the
painted steel is the "stuff" part, so the helmet's own colour (one per nation) tints it, and badges keep their colours. The field
uniforms are worn garments drawn like the 4.2 coats (heirs_art19 / heirs_art20), cloth tinted by the uniform colour.
"""
import math

import heirs_art18 as H
import heirs_art19 as W
from heirs_art import DARKIRON, GOLD, STEEL, Canvas, axis, m, painter
from heirs_art2 import LACQUER_R
from heirs_art4 import BRASS, IMP_RED
from heirs_art18 import GOLD as GOLD_H
from heirs_art18 import STUFF, STUFF_D, STUFF_DD, Hat, arcpts, dome
from heirs_art19 import BLACK, BRONZE, belt, folds, front_u, px, studs, trim_line
from heirs_art20 import BIRCH, BLACK_LAC, BLUED, GUNMETAL, IVORY, PINE, RED_CORD, SILVER, TEAK, TURQ, WALNUT, WALNUT_L, coat_base, collar, gun, sling

# ------------------------------------------------------------------ guns
PARKER = m("#30343a", .07, 3, (9, 1), spec=.7)          # parkerised steel, the dull grey of the new arms
OLIVE_WOOD = m("#6a4a2a", .14, 3, (9, 1))


def box_mag(c, at, u, length=7, depth=7, mat=PARKER):
    c.poly(mat, at(u, 3.2), at(u + length, 3.2), at(u + length - 1, 3.2 + depth), at(u - 0.5, 3.2 + depth), bevel=.8)


def scope(c, at, u0, u1, mat=BLACK_LAC, rings=BRASS):
    c.poly(mat, at(u0, -6.6), at(u1, -6.4), at(u1, -3.8), at(u0, -4.0), bevel=.8)
    c.poly(mat, at(u0 - 3, -7.4), at(u0, -6.8), at(u0, -3.6), at(u0 - 3, -3.0), bevel=.6)
    c.poly(mat, at(u1, -7.0), at(u1 + 4, -7.6), at(u1 + 4, -2.8), at(u1, -3.4), bevel=.6)
    c.ell(m("#7ab0d8", .05, spec=1.4), *at(u1 + 4, -5.2), 1.0, 2.0)
    for u in (u0 + 3, u1 - 3):
        c.line(rings, 1.6, at(u, -7), at(u, -2.6))


def lmg(c_seed):
    """The pan-fed light machine gun: a cooling jacket round the barrel, a flat drum on top and a folded bipod."""
    c, at, ln, L = gun(c_seed, WALNUT, "bolt", length=114, barrel=PARKER, bands=PARKER, band_at=(), butt=PARKER, slim=1.15)
    c.poly(m("#3a4036", .08, 3, (9, 1), spec=.6), at(40, -4.6), at(L - 12, -4.2), at(L - 12, 2.6), at(40, 3.2), bevel=1.2)   # jacket
    for k in range(9):
        u = 44 + k * (L - 60) / 8
        c.line(m("#22261f", .05), .9, at(u, -4.3), at(u, 2.8))                                                     # fins
    c.ell(m("#2e3236", .06, spec=.7), *at(32, -8.5), 9.0, 2.8, bevel=1.0)                                       # the pan magazine
    c.ell(m("#4a5056", .06, spec=.9), *at(32, -9.4), 3.0, 1.2)
    c.line(PARKER, 1.4, at(L - 16, 2.8), at(L - 30, 9), at(L - 44, 10))                                         # bipod, folded
    c.line(PARKER, 1.4, at(L - 16, 2.8), at(L - 28, 10.5), at(L - 42, 12))
    return c, at, ln, L


@painter
def heirs_e_gun(kind):
    k = kind.split("_")[-1]
    nation = kind.split("_")[1]
    if nation == "Albion":                                  # light machine gun
        c, at, ln, L = lmg(401)
        c.ell(BRASS, *at(18, 1), 2.4, 2.4, bevel=.8)
        sling(c, at, 10, 50, m("#6a5a3a", .06))
    elif nation == "Yamato":                                # sniper rifle with telescope
        c, at, ln, L = gun(402, BLACK_LAC, "bolt", length=122, band_at=(56, 78), bands=BLUED, barrel=BLUED, butt=BLUED)
        scope(c, at, 28, 50)
        c.ell(BRASS, *at(18, 1), 2.4, 2.4, bevel=.8)
        for a in range(0, 360, 72):
            c.ell(m("#f2c4cc", .05), *at(18 + 1.5 * math.cos(math.radians(a)), 1 + 1.5 * math.sin(math.radians(a))), .8, .8)
        sling(c, at, 10, 54)
    elif nation == "Nord":                                  # pump-action trench gun
        c, at, ln, L = gun(403, BIRCH, "block", length=104, barrel=PARKER, bands=PARKER, band_at=(), butt=PARKER, slim=1.1)
        c.poly(m("#3a3e42", .08, 3, (9, 1)), at(40, -4.2), at(L - 6, -3.8), at(L - 6, 0.6), at(40, 1.0), bevel=.8)  # heat shield
        for k2 in range(6):
            c.ell(m("#1e2024", .04), *at(44 + k2 * (L - 54) / 5, -1.8), 1.0, 1.0)
        c.poly(m("#7a5a38", .14, 3, (1, 6)), at(52, 1.4), at(66, 1.4), at(66, 5.6), at(52, 5.6), bevel=1.0)      # the pump grip
        for u in range(53, 66, 2):
            c.line(m("#5a3e22", .05), .6, at(u, 1.8), at(u, 5.2))
        c.poly(m("#1a1a1c", .04), at(28, -1.6), at(33, -3.2), at(36, -1.6), at(33, 0), bevel=.4)                  # raven on the receiver
    elif nation == "Roma":                                  # self-loading rifle
        c, at, ln, L = gun(404, WALNUT, "bolt", length=116, wrist=LACQUER_R, band_at=(54, 74), bands=PARKER, barrel=PARKER, butt=BRASS, bayonet=True)
        box_mag(c, at, 30, 8, 9)
        c.poly(PARKER, at(40, -3.6), at(56, -3.4), at(56, -1.6), at(40, -1.8), bevel=.6)                          # gas tube
        c.ell(BRASS, *at(20, 1), 2.8, 2.8, bevel=1.0)
        c.poly(m("#f0d070", .05), at(18.6, 0.3), at(20, -1.2), at(21.4, 0.3), at(20, 2.0), bevel=.4)
        sling(c, at, 10, 52)
    elif nation == "Tianxia":                               # broom-handled pistol with its holster-stock
        c = Canvas(128, seed=405)
        at, ln = axis((14, 108), (110, 18))
        c.poly(m("#6a3a1e", .14, 3, (9, 1)), at(0, -6), at(34, -4.5), at(34, 6), at(0, 7.5), bevel=1.4)          # the wooden box-stock
        c.line(m("#3a2010", .06), 1.0, at(4, -5.6), at(4, 7.2))
        c.poly(BRASS, at(34, -4), at(38, -4), at(38, 5), at(34, 5), bevel=.6)
        c.poly(m("#5a2a16", .12, 3, (1, 6)), at(38, -3), at(48, -3), at(46, 10), at(40, 12), bevel=1.0)          # broom handle
        for v in range(-2, 11, 2):
            c.line(m("#3a1a0c", .05), .5, at(39.5, v), at(46.5, v))
        c.poly(PARKER, at(44, -6), at(72, -6), at(72, -0.5), at(44, -0.5), bevel=1.0)                             # receiver
        c.poly(PARKER, at(56, -0.5), at(66, -0.5), at(65, 7), at(57, 7), bevel=.8)                                # magazine ahead of the trigger
        c.poly(BLUED, at(72, -4.8), at(ln, -4.4), at(ln, -2.2), at(72, -1.8), bevel=.6)                           # barrel
        c.line(DARKIRON, 1.4, at(52, -0.5), at(50, 3.5), at(46, 4))
        c.line(RED_CORD, 1.2, at(42, 10), at(40, 15), at(43, 19))
        c.ell(IMP_RED, *at(43, 19.6), 1.6, 2.4)
        return c.image()
    elif nation == "Hellas":                                # mountain carbine
        c, at, ln, L = gun(406, WALNUT_L, "bolt", length=98, bands=SILVER, butt=SILVER, barrel=BLUED, band_at=(50, 66))
        c.ell(m("#2e5c8c", .06), *at(18, 1), 2.3, 2.3, bevel=.8)
        c.poly(m("#efefef", .03), at(16.6, 0.6), at(19.4, 0.6), at(19.4, 1.4), at(16.6, 1.4), bevel=.2)
        sling(c, at, 10, 46, m("#2e5c8c", .06))
    elif nation == "Kemet":                                 # Nile carbine
        c, at, ln, L = gun(407, TEAK, "bolt", length=106, band_at=(52, 70), barrel=BLUED, bands=BRASS)
        for u in (7, 12):
            c.ell(TURQ, *at(u, 2.4), 1.2, 1.2, bevel=.4)
        c.poly(GOLD, at(3, -2), at(6, 0), at(3, 2), at(5, 0), bevel=.4)
        c.poly(m("#d8c8a0", .06), at(L - 4, -2.6), at(L, -2.6), at(L, 0.6), at(L - 4, 0.6), bevel=.4)            # muzzle cap against sand
        sling(c, at, 10, 50, m("#2aa09a", .06))
    elif nation == "Pars":                                  # long rifle with a fine sight
        c, at, ln, L = gun(408, m("#4a2a1a", .12, 3, (9, 1)), "bolt", length=124, bands=SILVER, butt=SILVER, barrel=BLUED, band_at=(56, 80, 100))
        for k2 in range(6):
            u = 4 + k2 * 4
            for dv in (-2.2, 1.6):
                c.poly(IVORY, at(u, dv - 1), at(u + 1, dv), at(u, dv + 1), at(u - 1, dv), bevel=.2)
        c.poly(BRASS, at(40, -4.2), at(46, -4.2), at(46, -6.6), at(40, -6.0), bevel=.5)                           # ladder sight
        c.line(BRASS, .7, at(41, -6.4), at(45, -6.4))
        sling(c, at, 10, 56, m("#2a4a7a", .06))
    else:                                                   # Inti light carbine
        c, at, ln, L = gun(409, m("#7a4a2a", .14, 3, (9, 1)), "bolt", length=94, bands=GOLD, butt=GOLD, barrel=PARKER, band_at=(48, 62))
        c.ell(GOLD, *at(18, 1), 3.0, 3.0, bevel=1.0)
        for a in range(0, 360, 45):
            c.line(GOLD, .8, at(18 + 3 * math.cos(math.radians(a)), 1 + 3 * math.sin(math.radians(a))),
                   at(18 + 4.6 * math.cos(math.radians(a)), 1 + 4.6 * math.sin(math.radians(a))))
        sling(c, at, 10, 44, m("#c8322a", .06))
    return c.image()


# ------------------------------------------------------------------ steel helmets
def shell(h, rot, rx=27, top=26, yb=62, brim=0.0, neck=0.0, color=STUFF, gloss=.3):
    """The steel bowl, with an optional all-round brim (Brodie) or flared neck (coal-scuttle)."""
    cx = 64 if rot != "east" else 63
    if brim:
        h.add(("curve", [(cx - rx - brim, yb + 1), (cx, yb - 3), (cx + rx + brim, yb + 1), (cx + rx + brim - 2, yb + 5),
                         (cx, yb + 3), (cx - rx - brim + 2, yb + 5)]), STUFF_D, True, "flat", lw=1.0)
    if neck and rot != "south":
        back = -1 if rot == "east" else 0
        if rot == "east":
            h.add(("curve", [(cx - rx + 2, yb - 10), (cx - rx - neck, yb + 6), (cx - rx + 6, yb + 8), (cx, yb + 2)]), STUFF_D, True, "cyl", lw=1.0)
        else:
            h.add(("curve", [(cx - rx - neck * .6, yb + 7), (cx, yb + 4), (cx + rx + neck * .6, yb + 7), (cx + rx, yb - 6), (cx - rx, yb - 6)]),
                  STUFF_D, True, "cyl", lw=1.0)
        del back
    pts = dome(cx, yb, rx, top)
    h.add(("poly", pts), color, True, "dome", gloss=gloss)
    if neck and rot == "south":
        for sx in (-1, 1):
            h.add(("curve", [(cx + sx * (rx - 2), yb - 8), (cx + sx * (rx + neck * .5), yb + 6), (cx + sx * (rx - 4), yb + 6)]), STUFF_D, True, "cyl", lw=.9)
    h.add(("stroke", [(cx - rx + 1, yb - 1), (cx, yb + 1.5), (cx + rx - 1, yb - 1)], 2.2), STUFF_DD, True, "cyl", lw=.8)   # rolled rim
    return cx


def badge(h, rot, x_south=64, y=46, east_x=84, draw=None):
    if rot == "north" or draw is None:
        return
    draw(x_south if rot == "south" else east_x, y, rot)


def roma_helmet(h, rot):
    """An Adrian-pattern helmet with a tall bronze comb and the eagle on the front."""
    cx = shell(h, rot, rx=26, top=28, brim=4)
    if rot == "east":
        h.add(("curve", [(cx - 22, 40), (cx - 6, 24), (cx + 14, 26), (cx + 22, 38), (cx + 4, 32)]), BRONZE, shade="cyl", gloss=.4, lw=.9)
    else:
        h.add(("curve", [(cx - 3, 46), (cx - 2.4, 30), (cx, 24), (cx + 2.4, 30), (cx + 3, 46)]), BRONZE, shade="cyl", gloss=.5, lw=.9)

    def eagle(x, y, r):
        h.add(("curve", [(x - 6, y - 2), (x, y - 6), (x + 6, y - 2), (x + 3, y + 4), (x, y + 6), (x - 3, y + 4)]), GOLD_H, shade="dome", gloss=.6, lw=.8)
        h.add(("ell", x, y - 1, 1.5, 1.5), "#7a1a1e", shade="none", line=False)
    badge(h, rot, 64, 48, 82, eagle)


def yamato_helmet(h, rot):
    """A round helmet with a short rim and the red sun on a white disc."""
    cx = shell(h, rot, rx=26, top=28, brim=2)
    if rot != "north":
        h.add(("stroke", [(cx - 18, 58), (cx, 60), (cx + 18, 58)] if rot == "south" else [(cx + 6, 58), (cx + 26, 60), (cx + 32, 62)], 2.6),
              STUFF_D, True, "cyl", lw=.8)                                                                       # short visor rim

    def sun(x, y, r):
        h.add(("ell", x, y, 5.6, 5.6), "#f2efe6", shade="dome", lw=.8)
        h.add(("ell", x, y, 3.4, 3.4), "#b4282a", shade="dome", gloss=.3, line=False)
    badge(h, rot, 64, 44, 82, sun)


def nord_helmet(h, rot):
    """A coal-scuttle helmet with a flared neck guard, a raised nasal ridge and a black raven."""
    cx = shell(h, rot, rx=27, top=24, neck=8)
    if rot == "south":
        h.add(("ell", 50, 50, 2.0, 2.0), STUFF_DD, True, "dome", line=False)                                         # vent lugs
        h.add(("ell", 78, 50, 2.0, 2.0), STUFF_DD, True, "dome", line=False)

    def raven(x, y, r):
        h.add(("curve", [(x - 6, y + 1), (x - 1, y - 4), (x + 5, y - 3), (x + 7, y - 5), (x + 6, y + 1), (x, y + 4)]), "#1a1a1c", shade="flat", lw=.7)
    badge(h, rot, 64, 42, 80, raven)


def hellas_helmet(h, rot):
    """An Adrian-pattern helmet with a short crest stub and the blue and white roundel."""
    cx = shell(h, rot, rx=26, top=29, brim=4)
    if rot == "east":
        h.add(("curve", [(cx - 18, 38), (cx - 4, 26), (cx + 12, 28), (cx + 18, 36), (cx, 33)]), STUFF_D, True, "cyl", lw=.9)
    else:
        h.add(("curve", [(cx - 2.6, 40), (cx - 2, 30), (cx, 26), (cx + 2, 30), (cx + 2.6, 40)]), STUFF_D, True, "cyl", lw=.9)

    def roundel(x, y, r):
        h.add(("ell", x, y, 5.6, 5.6), "#2e5c8c", shade="dome", lw=.8)
        h.add(("ell", x, y, 3.6, 3.6), "#f2f2f2", shade="dome", line=False)
        h.add(("ell", x, y, 1.6, 1.6), "#2e5c8c", shade="none", line=False)
    badge(h, rot, 64, 48, 82, roundel)


def tianxia_helmet(h, rot):
    """A deep rounded helmet with a narrow brim all round and a red star."""
    cx = shell(h, rot, rx=27, top=27, brim=5)

    def star(x, y, r):
        pts = []
        for i in range(10):
            a = math.radians(-90 + i * 36)
            rr = 5.6 if i % 2 == 0 else 2.4
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        h.add(("poly", pts), "#c42a22", shade="flat", gloss=.3, lw=.7)
    badge(h, rot, 64, 46, 82, star)


def albion_helmet(h, rot):
    """The shallow dish helmet with a wide brim all round, and a small brass badge."""
    cx = 64 if rot != "east" else 63
    yb = 58
    h.add(("curve", [(cx - 40, yb + 2), (cx - 20, yb - 4), (cx, yb - 5), (cx + 20, yb - 4), (cx + 40, yb + 2), (cx + 36, yb + 7),
                     (cx, yb + 6), (cx - 36, yb + 7)] if rot != "east" else
                    [(cx - 36, yb + 4), (cx, yb - 4), (cx + 38, yb + 2), (cx + 34, yb + 8), (cx, yb + 5), (cx - 32, yb + 9)]),
          STUFF_D, True, "flat", lw=1.0)
    h.add(("poly", dome(cx, yb, 25, 32)), STUFF, True, "dome", gloss=.25)
    h.add(("stroke", [(cx - 38, yb + 3), (cx, yb + 6), (cx + 38, yb + 3)], 1.6), STUFF_DD, True, "none", line=False)

    def lion(x, y, r):
        h.add(("ell", x, y, 3.6, 3.6), BRASS_HEX, shade="dome", gloss=.6, lw=.7)
        h.add(("ell", x, y, 1.6, 1.6), "#7a5a1a", shade="none", line=False)
    badge(h, rot, 64, 44, 80, lion)


def kemet_helmet(h, rot):
    """A light helmet with a sun cloth hanging at the nape and a gold falcon."""
    cx = 64 if rot != "east" else 63
    if rot == "east":
        h.add(("curve", [(cx - 24, 54), (cx - 32, 80), (cx - 12, 84), (cx - 4, 60)]), "#d8ccb0", shade="cyl", lw=.9)
    elif rot == "north":
        h.add(("curve", [(cx - 26, 56), (cx - 28, 82), (cx, 86), (cx + 28, 82), (cx + 26, 56)]), "#d8ccb0", shade="cyl", lw=.9)
        for x in (cx - 12, cx, cx + 12):
            h.add(("stroke", [(x, 60), (x + (x - cx) * .1, 84)], 1.0), "#b8ac90", shade="none", line=False)
    cx = shell(h, rot, rx=26, top=27, brim=3)

    def falcon(x, y, r):
        h.add(("curve", [(x - 7, y - 3), (x - 2, y - 1), (x, y - 5), (x + 2, y - 1), (x + 7, y - 3), (x + 3, y + 3), (x, y + 5), (x - 3, y + 3)]),
              GOLD_H, shade="dome", gloss=.5, lw=.7)
    badge(h, rot, 64, 46, 82, falcon)


def pars_helmet(h, rot):
    """A domed helmet with a silver spike on top and a silver lion-and-sun plate."""
    cx = shell(h, rot, rx=26, top=28, brim=2)
    sx = cx if rot != "east" else cx - 1
    h.add(("poly", [(sx - 4, 30), (sx - 1.4, 14), (sx, 10), (sx + 1.4, 14), (sx + 4, 30)]), "#c8ccd0", shade="cyl", gloss=.6, lw=.8)
    h.add(("ell", sx, 30, 5.5, 2.4), "#c8ccd0", shade="cyl", gloss=.5, lw=.8)

    def sun(x, y, r):
        h.add(("ell", x, y, 5.0, 5.0), "#c8ccd0", shade="dome", gloss=.6, lw=.7)
        for i in range(8):
            a = math.radians(i * 45)
            h.add(("stroke", [(x + 3 * math.cos(a), y + 3 * math.sin(a)), (x + 4.6 * math.cos(a), y + 4.6 * math.sin(a))], .8), "#8a8e92",
                  shade="none", line=False)
    badge(h, rot, 64, 46, 82, sun)


def inti_helmet(h, rot):
    """A round helmet with a small brim and a gold sun disc on the front."""
    cx = shell(h, rot, rx=26, top=28, brim=3)
    if rot != "north":
        for k in range(5 if rot == "south" else 3):
            x = cx - 16 + k * 8 if rot == "south" else cx + 6 + k * 8
            h.add(("poly", [(x, 54), (x + 6, 54), (x + 6, 58), (x, 58)]), ["#c8322a", "#e6c23a", "#2a2a2a", "#2f5f9e", "#2a7a3a"][k], shade="flat", lw=.5)

    def sun(x, y, r):
        h.add(("ell", x, y, 6.0, 6.0), GOLD_H, shade="dome", gloss=.6, lw=.8)
        for i in range(12):
            a = math.radians(i * 30)
            h.add(("stroke", [(x + 6 * math.cos(a), y + 6 * math.sin(a)), (x + 8.4 * math.cos(a), y + 8.4 * math.sin(a))], 1.2), GOLD_H,
                  shade="none", line=False)
        h.add(("ell", x - 1.6, y - 1, .8, .8), "#5a3a10", shade="none", line=False)
        h.add(("ell", x + 1.6, y - 1, .8, .8), "#5a3a10", shade="none", line=False)
    badge(h, rot, 64, 42, 82, sun)


BRASS_HEX = "#c89a3a"

# (key, en, tr, desc en, desc tr, paint colour)
HELMETS = {
    "Roma": ("SteelHelmet", "legion steel helmet", "lejyon çelik miğferi",
             "A steel helmet with a narrow brim and a tall bronze comb, painted crimson, with a bronze eagle on the front.",
             "Dar kenarlı ve uzun, bronz bir sırtı olan, kızıla boyanmış, önünde bronz bir kartal bulunan çelik bir miğfer.", "(0.46, 0.14, 0.16)"),
    "Yamato": ("SteelHelmet", "Yamato steel helmet", "Yamato çelik miğferi",
               "A round steel helmet with a short rim, painted in khaki, and the red sun on a white disc.",
               "Kısa kenarlı, hakiye boyanmış ve beyaz bir disk üzerinde kırmızı güneş olan yuvarlak bir çelik miğfer.", "(0.50, 0.46, 0.30)"),
    "Nord": ("SteelHelmet", "Nordic steel helmet", "Nord çelik miğferi",
             "A deep steel helmet that flares over the neck, with a raised nasal ridge and a black raven painted on the side.",
             "Ensenin üstünde genişleyen, burun sırtı kabarık ve yanına siyah bir kuzgun boyanmış derin bir çelik miğfer.", "(0.36, 0.40, 0.42)"),
    "Hellas": ("SteelHelmet", "Hellenic steel helmet", "Helen çelik miğferi",
               "A steel helmet with a narrow brim and a short crest, in olive drab, with the blue and white roundel.",
               "Dar kenarlı ve kısa sırtlı, zeytin rengi, mavi beyaz bir yuvarlak arması olan çelik bir miğfer.", "(0.40, 0.42, 0.30)"),
    "Tianxia": ("SteelHelmet", "Tianxia steel helmet", "Tianxia çelik miğferi",
                "A deep rounded steel helmet with a narrow brim all round, in grey-blue, with a red star.",
                "Her yanında dar bir kenarı olan, gri maviye boyanmış, kırmızı yıldızlı derin ve yuvarlak bir çelik miğfer.", "(0.34, 0.40, 0.46)"),
    "Albion": ("SteelHelmet", "Albion steel helmet", "Albion çelik miğferi",
               "A shallow steel bowl with a wide brim all round, khaki-painted, keeping off what falls from above. A small brass badge on the front.",
               "Her yanında geniş bir kenarı olan, hakiye boyanmış, yukarıdan düşeni tutan sığ bir çelik kâse. Önünde küçük pirinç bir rozet var.",
               "(0.46, 0.42, 0.28)"),
    "Kemet": ("SteelHelmet", "Kemetic sun helmet", "Kemet güneş miğferi",
              "A light steel helmet in sand colour with a linen cloth hanging over the neck against the sun, and a gold falcon on the front.",
              "Kum renginde, ensesine güneşe karşı keten bir bez sarkan ve önünde altın bir şahin olan hafif bir çelik miğfer.", "(0.70, 0.62, 0.44)"),
    "Pars": ("SteelHelmet", "Persian spiked helmet", "Pers sivri miğferi",
             "A domed steel helmet in olive, crowned with a silver spike and fronted by a silver plate of the lion and sun.",
             "Zeytin renginde, tepesinde gümüş bir sivri ve önünde aslan ve güneşli gümüş bir levha olan kubbeli bir çelik miğfer.", "(0.38, 0.38, 0.26)"),
    "Inti": ("SteelHelmet", "Inti steel helmet", "Inti çelik miğferi",
             "A round steel helmet in ochre with a small brim, a band of tocapu and the golden sun on the front.",
             "Küçük kenarlı, hardal sarısı, bir tokapu şeridi ve önünde altın güneş olan yuvarlak bir çelik miğfer.", "(0.60, 0.46, 0.22)"),
}
H.KINDS.update({
    "HE_Roma_SteelHelmet": roma_helmet, "HE_Yamato_SteelHelmet": yamato_helmet, "HE_Nord_SteelHelmet": nord_helmet,
    "HE_Hellas_SteelHelmet": hellas_helmet, "HE_Tianxia_SteelHelmet": tianxia_helmet, "HE_Albion_SteelHelmet": albion_helmet,
    "HE_Kemet_SteelHelmet": kemet_helmet, "HE_Pars_SteelHelmet": pars_helmet, "HE_Inti_SteelHelmet": inti_helmet,
})


@painter
def heirs_e_helmet_icon(kind, mask=False):
    """The inventory icon: the helmet seen from the side and a little from the front, fitted to the icon."""
    from PIL import Image
    img, mk = H.draw(kind, "east")
    im = mk if mask else img
    box = img.getbbox()
    scale = min(110 / (box[2] - box[0]), 104 / (box[3] - box[1]))
    im = im.crop(box)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0) if not mask else (0, 0, 0, 255))
    out.paste(im, ((128 - im.width) // 2, (128 - im.height) // 2))
    return out


# ------------------------------------------------------------------ field uniforms (worn)
def tunic(w, length=0.86):
    coat_base(w, length)


def pockets(w, v=0.24, h=0.1, flap=STUFF_D):
    if w.rot == "south":
        for u in (0.3, 0.7):
            w.add(w.poly([(u - 0.1, v), (u + 0.1, v), (u + 0.09, v + h), (u - 0.09, v + h)]), STUFF_D, True, "cyl", lw=0.8)
            w.add(w.poly([(u - 0.11, v - 0.02), (u + 0.11, v - 0.02), (u, v + 0.035)]), flap, True, "flat", lw=0.7)
    elif w.rot == "east":
        u = 0.72
        w.add(w.poly([(u - 0.08, v), (u + 0.08, v), (u + 0.07, v + h), (u - 0.07, v + h)]), STUFF_D, True, "cyl", lw=0.8)


def low_pockets(w, v=0.66):
    if w.rot == "south":
        for u in (0.28, 0.72):
            w.add(w.poly([(u - 0.12, v), (u + 0.12, v), (u + 0.11, v + 0.12), (u - 0.11, v + 0.12)]), STUFF_D, True, "cyl", lw=0.8)


def patches(w, color):
    """Collar patches in the nation's colour."""
    if w.rot == "south":
        fu = front_u(w)
        for s in (-1, 1):
            w.add(w.poly([(fu + s * 0.06, 0.02), (fu + s * 0.16, 0.02), (fu + s * 0.14, 0.08), (fu + s * 0.06, 0.08)]), color, False, "flat", lw=0.6)
    elif w.rot == "east":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.12, 0.02), (fu - 0.02, 0.02), (fu - 0.03, 0.08), (fu - 0.11, 0.08)]), color, False, "flat", lw=0.6)


def boards(w, color):
    """Shoulder boards."""
    if w.rot == "east":
        w.add(w.poly([(0.42, 0.0), (0.62, 0.0), (0.62, 0.05), (0.42, 0.05)]), color, False, "flat", lw=0.6)
    else:
        for u in (0.1, 0.9):
            w.add(w.poly([(u - 0.08, 0.0), (u + 0.08, 0.0), (u + 0.08, 0.05), (u - 0.08, 0.05)]), color, False, "flat", lw=0.6)


def roma_field(w):
    tunic(w, 0.86)
    collar(w, STUFF_D, True)
    patches(w, "#a51e2c")
    front_seam_e(w)
    buttons_e(w, BRONZE)
    pockets(w)
    belt(w, 0.6, 0.05, "#3a2a1c", buckle=BRONZE)
    if w.rot == "south":
        trim_line(w, [(0.86, 0.1), (0.62, 0.36), (0.4, 0.6)], px(w, 1.8), "#3a2a1c")
    folds(w, 3, 0.68, 0.9, width=0.7)


def yamato_field(w):
    tunic(w, 0.84)
    collar(w, STUFF_D, True)
    patches(w, "#b4282a")
    front_seam_e(w, v1=0.84)
    buttons_e(w, BRASS_HEX, rows=(0.2, 0.32, 0.44))
    pockets(w)
    low_pockets(w)
    belt(w, 0.6, 0.05, "#5a4026", buckle=BRASS_HEX)
    boards(w, "#b4282a")


def nord_field(w):
    tunic(w, 0.9)
    if w.rot == "north":
        w.add(w.band(0.0, 0.07), "#3a4a3e", False, "cyl", lw=0.9)
    else:
        fu = front_u(w)
        w.add(w.poly([(fu - 0.2, 0.0), (fu + 0.2, 0.0), (fu + 0.12, 0.1), (fu - 0.12, 0.1)]), "#3a4a3e", False, "cyl", lw=0.9)
    front_seam_e(w, v1=0.9)
    buttons_e(w, "#9aa0a4", rows=(0.22, 0.34, 0.46, 0.58))
    low_pockets(w, 0.64)
    belt(w, 0.6, 0.06, "#2a2018", buckle="#9aa0a4")
    folds(w, 4, 0.68, 0.94, width=0.8)


def hellas_field(w):
    tunic(w, 0.84)
    collar(w, STUFF_D, True)
    patches(w, "#2e5c8c")
    front_seam_e(w, v1=0.84)
    buttons_e(w, "#c8ccd0", rows=(0.22, 0.36, 0.5))
    pockets(w)
    belt(w, 0.6, 0.05, "#4a3a28", buckle="#c8ccd0")
    if w.rot != "east":
        w.add(w.band(0.66, 0.69), "#2e5c8c", False, "cyl", lw=0.5)


def tianxia_field(w):
    tunic(w, 0.86)
    collar(w, STUFF_D, True)
    patches(w, "#c42a22")
    front_seam_e(w, v1=0.86)
    buttons_e(w, "#2a2a2c", rows=(0.2, 0.32, 0.44, 0.56))
    pockets(w)
    low_pockets(w)
    belt(w, 0.6, 0.05, "#3a2a1c", buckle="#c8a040")


def albion_field(w):
    tunic(w, 0.82)
    collar(w, STUFF_D, True)
    front_seam_e(w, v1=0.82)
    buttons_e(w, BRASS_HEX, rows=(0.2, 0.32, 0.44))
    pockets(w)
    low_pockets(w, 0.64)
    belt(w, 0.6, 0.06, "#7a6a48", buckle=BRASS_HEX)                                                 # webbing
    if w.rot == "south":
        for s in (-1, 1):
            trim_line(w, [(0.5 + s * 0.3, 0.02), (0.5 + s * 0.26, 0.6)], px(w, 2.0), "#7a6a48")
    elif w.rot == "north":
        trim_line(w, [(0.2, 0.02), (0.5, 0.3), (0.8, 0.02)], px(w, 2.0), "#7a6a48")
        trim_line(w, [(0.5, 0.3), (0.5, 0.6)], px(w, 2.0), "#7a6a48")


def kemet_field(w):
    tunic(w, 0.84)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.2, 0.0), (fu + 0.2, 0.0), (fu + 0.13, 0.1), (fu - 0.13, 0.1)]), "#2aa09a", False, "cyl", lw=0.9)
    else:
        w.add(w.band(0.0, 0.07), "#2aa09a", False, "cyl", lw=0.9)
    front_seam_e(w, v1=0.84)
    buttons_e(w, BRONZE, rows=(0.22, 0.36, 0.5))
    pockets(w)
    belt(w, 0.6, 0.055, "#6b4a2c", buckle=BRONZE)


def pars_field(w):
    tunic(w, 0.9)
    collar(w, STUFF_D, True)
    patches(w, "#2a4a7a")
    front_seam_e(w, v1=0.9)
    buttons_e(w, "#c8ccd0", rows=(0.2, 0.32, 0.44, 0.56))
    pockets(w)
    belt(w, 0.58, 0.04, BLACK, buckle="#c8ccd0")
    if w.rot == "south":
        trim_line(w, [(0.82, 0.1), (0.6, 0.34), (0.4, 0.58)], px(w, 1.6), BLACK)
    folds(w, 4, 0.66, 0.92, width=0.8)


def inti_field(w):
    tunic(w, 0.86)
    collar(w, STUFF_D, True)
    if w.rot != "north":
        colours = ("#c8322a", "#e6c23a", "#2a2a2a", "#2f5f9e", "#2a7a3a")
        for i in range(8):
            u0 = 0.1 + i * 0.1
            w.add(w.poly([(u0, 0.5), (u0 + 0.095, 0.5), (u0 + 0.095, 0.55), (u0, 0.55)]), colours[i % 5], False, "flat", lw=0.5)
    front_seam_e(w, v1=0.86)
    buttons_e(w, GOLD_H, rows=(0.2, 0.32, 0.44))
    pockets(w)
    belt(w, 0.62, 0.05, "#4a311c", buckle=GOLD_H)


def front_seam_e(w, v0=0.1, v1=0.86):
    if w.rot == "north":
        w.lines(w.stroke([(0.5, 0.62), (0.5, v1)], 1.0), STUFF_DD)
        return
    fu = front_u(w)
    w.lines(w.stroke([(fu, v0), (fu + 0.01, 0.6), (fu - 0.01, v1)], 1.0), STUFF_DD)


def buttons_e(w, color, rows=(0.22, 0.34, 0.46, 0.58)):
    if w.rot == "north":
        return
    fu = front_u(w)
    studs(w, [(fu + (0.03 if w.rot == "east" else 0), v) for v in rows], px(w, 1.1), color)


# (key, en, tr, desc en, desc tr, cloth colour)
UNIFORMS_E = {
    "Roma": ("FieldUniform", "legion field uniform", "lejyon sahra üniforması",
             "A grey-green field tunic with crimson collar patches, bronze buttons, a cross strap and two breast pockets.",
             "Kızıl yaka işaretli, bronz düğmeli, çapraz kayışlı ve iki göğüs cepli, gri yeşil bir sahra ceketi.", "(0.40, 0.44, 0.36)"),
    "Yamato": ("FieldUniform", "Yamato field uniform", "Yamato sahra üniforması",
               "A khaki field tunic with red collar patches and shoulder boards, brass buttons and four pockets.",
               "Kırmızı yaka işaretli ve omuz apoletli, pirinç düğmeli ve dört cepli haki bir sahra ceketi.", "(0.56, 0.50, 0.32)"),
    "Nord": ("FieldUniform", "Nordic field uniform", "Nord sahra üniforması",
             "A long field-grey tunic with a dark green collar, pewter buttons and deep skirt pockets. Warm in the snow.",
             "Koyu yeşil yakalı, kalay düğmeli ve derin etek cepli, uzun, sahra grisi bir ceket. Karda sıcak tutar.", "(0.42, 0.45, 0.42)"),
    "Hellas": ("FieldUniform", "Hellenic field uniform", "Helen sahra üniforması",
               "An olive field tunic with blue collar patches, silver buttons and a thin blue band at the hem.",
               "Mavi yaka işaretli, gümüş düğmeli ve eteğinde ince mavi bir şerit olan zeytin rengi bir sahra ceketi.", "(0.46, 0.46, 0.32)"),
    "Tianxia": ("FieldUniform", "Tianxia field uniform", "Tianxia sahra üniforması",
                "A grey-blue field tunic with red collar patches, dark buttons and four pockets.",
                "Kırmızı yaka işaretli, koyu düğmeli ve dört cepli, gri mavi bir sahra ceketi.", "(0.38, 0.44, 0.50)"),
    "Albion": ("FieldUniform", "Albion service dress", "Albion hizmet üniforması",
               "A khaki service tunic with brass buttons, four pockets and the webbing of braces and belt.",
               "Pirinç düğmeli, dört cepli, askı ve kemer kayışlarıyla haki bir hizmet ceketi.", "(0.52, 0.46, 0.30)"),
    "Kemet": ("FieldUniform", "Kemetic desert uniform", "Kemet çöl üniforması",
              "A light sand tunic with a turquoise collar, bronze buttons and breast pockets, cut loose for the heat.",
              "Turkuaz yakalı, bronz düğmeli ve göğüs cepli, sıcağa göre bol kesilmiş açık kum renginde bir ceket.", "(0.74, 0.66, 0.48)"),
    "Pars": ("FieldUniform", "Persian field uniform", "Pers sahra üniforması",
             "An olive field tunic with dark blue collar patches, silver buttons, a narrow black belt and a cross strap.",
             "Lacivert yaka işaretli, gümüş düğmeli, dar siyah kemerli ve çapraz kayışlı zeytin rengi bir sahra ceketi.", "(0.42, 0.42, 0.30)"),
    "Inti": ("FieldUniform", "Inti field uniform", "Inti sahra üniforması",
             "An earth-brown field tunic with a band of tocapu at the waist and gold buttons.",
             "Belinde bir tokapu şeridi ve altın düğmeleri olan, toprak kahvesi bir sahra ceketi.", "(0.50, 0.38, 0.24)"),
}
FIELD_UNIFORMS = {
    "HE_Roma_FieldUniform": (roma_field, 2.6, 2.6), "HE_Yamato_FieldUniform": (yamato_field, 2.6, 2.6),
    "HE_Nord_FieldUniform": (nord_field, 2.8, 2.8), "HE_Hellas_FieldUniform": (hellas_field, 2.6, 2.6),
    "HE_Tianxia_FieldUniform": (tianxia_field, 2.6, 2.6), "HE_Albion_FieldUniform": (albion_field, 2.6, 2.6),
    "HE_Kemet_FieldUniform": (kemet_field, 2.6, 2.6), "HE_Pars_FieldUniform": (pars_field, 2.6, 2.6),
    "HE_Inti_FieldUniform": (inti_field, 2.6, 2.6),
}
W.GARMENTS.update(FIELD_UNIFORMS)


# ------------------------------------------------------------------ works (seen from above, 128 px a cell)
MARBLE_E = m("#ddd6c8", .07, 3, spec=.5)
MARBLE_ED = m("#a8a090", .08, 3)
WATER = m("#3a78a8", .05, 4, (3, 1), spec=1.6)
WATER_L = m("#8ac4e8", .04, 3, spec=1.8)
COPPER = m("#b0603a", .08, 2, spec=1.1)
CAST = m("#2c2e30", .10, 2, spec=.6)
CAST_L = m("#4a4e52", .10, 2, spec=.7)
OAK = m("#6a4a2c", .14, 3, (9, 1))
OLIVE_W = m("#7a6038", .14, 3, (9, 1))
BAKELITE = m("#2a1a12", .05, 2, spec=1.0)
CLAY = m("#a86a40", .14, 2.5)
GRAN = m("#8a8480", .16, 2.5, spec=.3)
GRAN_D = m("#5e5854", .16, 2.5)
SILK = m("#c43a3a", .06, 3, (6, 1), spec=.4)
WOOL_E = m("#8a2a2a", .14, 2, (2, 1))
ZINC = m("#9aa4aa", .06, 3, spec=.9)
MOTOR = m("#3a5a3a", .08, spec=.8)
WOLF = m("#8a6232", .08, 2, spec=1.3)


def shadow_box(c, x0, y0, x1, y1, r=6, d=8):
    c.rect(m("#141210", .08), x0 + d * .5, y0 + d, x1 + d * .5, y1 + d, r)


def lamp(c, x, y, r=5, col="#ffe8a8"):
    c.ell(m(col, .02, spec=1.6), x, y, r, r, bevel=1.0)
    c.glow(x, y, r * 4, col, .35)


def wire(c, *pts, w=1.6):
    c.line(m("#141414", .05), w, *pts, bevel=.3)


def ring(c, mat, cx, cy, r, ry=None, n=30, w=1.0):
    ry = r if ry is None else ry
    pts = [(cx + r * math.cos(t / n * 2 * math.pi), cy + ry * math.sin(t / n * 2 * math.pi)) for t in range(n + 1)]
    c.line(mat, w, *pts, bevel=.3)


@painter
def e_fountain(size=(2, 2)):
    """A round marble basin with a bronze she-wolf in the middle, rings of water thrown from the pump and lamps under the water."""
    c = Canvas(256, 256, seed=4301)
    cx, cy = 128, 126
    c.ell(m("#141210", .08), cx + 6, cy + 12, 116, 110)
    c.ell(MARBLE_ED, cx, cy, 116, 110, bevel=3.0)
    c.ell(MARBLE_E, cx, cy - 2, 110, 104, bevel=2.6)
    for k in range(24):
        a = k * 2 * math.pi / 24
        c.scratch(.8, .3, (cx + 98 * math.cos(a), cy + 92 * math.sin(a)), (cx + 110 * math.cos(a), cy + 104 * math.sin(a)))
    c.ell(m("#20384a", .06), cx, cy + 2, 92, 86)
    c.ell(WATER, cx, cy, 90, 84, bevel=1.2)
    for a in (0.6, 2.2, 3.8, 5.4):
        lamp(c, cx + 62 * math.cos(a), cy + 58 * math.sin(a), 4, "#b8e4ff")
    for r in (78, 64, 50):
        ring(c, WATER_L, cx, cy, r, r * .94, w=1.2)
    for k in range(12):
        a = k * 2 * math.pi / 12
        c.line(WATER_L, 2.2, (cx + 22 * math.cos(a), cy + 20 * math.sin(a)), (cx + 44 * math.cos(a), cy + 40 * math.sin(a)), bevel=.5)
        c.ell(WATER_L, cx + 46 * math.cos(a), cy + 42 * math.sin(a), 3.5, 3, bevel=.6)
    c.ell(MARBLE_ED, cx, cy, 26, 24, bevel=2.0)
    c.ell(MARBLE_E, cx, cy - 1, 22, 20, bevel=1.8)
    # the she-wolf seen from above, head to the south
    c.ell(WOLF, cx, cy - 4, 9, 15, bevel=2.0)
    c.ell(WOLF, cx, cy + 12, 6, 6, bevel=1.6)
    c.poly(WOLF, (cx - 5, cy + 15), (cx, cy + 22), (cx + 5, cy + 15), bevel=1.0)
    for s in (-1, 1):
        c.poly(WOLF, (cx + s * 4, cy + 8), (cx + s * 8, cy + 6), (cx + s * 6, cy + 11), bevel=.6)
        c.line(WOLF, 2.4, (cx + s * 7, cy - 12), (cx + s * 11, cy - 16))
        c.line(WOLF, 2.4, (cx + s * 7, cy + 4), (cx + s * 11, cy + 6))
    c.line(WOLF, 2.0, (cx, cy - 18), (cx + 6, cy - 24), (cx + 2, cy - 28))
    c.glow(cx - 40, cy - 44, 60, "#ffffff", .18)
    return c.image()


@painter
def e_tea_urn(size=(1, 1)):
    """A tall black-lacquered copper urn seen from above with its lid knob, a brass tap and a tray of cups beside it."""
    c = Canvas(128, 128, seed=4302)
    shadow_box(c, 14, 20, 118, 116, 10, 6)
    c.rect(TEAK, 12, 16, 116, 112, 10, bevel=2.2)
    c.rect(m("#4a2c18", .1, 3, (9, 1)), 18, 22, 110, 106, 6, bevel=1.0)
    c.ell(m("#141210", .08), 56, 62, 32, 32)
    c.ell(BLACK_LAC, 52, 56, 32, 32, bevel=3.2)
    c.ell(COPPER, 52, 56, 22, 22, bevel=2.2)
    c.ell(BLACK_LAC, 52, 56, 12, 12, bevel=1.8)
    c.ell(BRASS, 52, 56, 5, 5, bevel=1.2)
    for k in range(8):
        a = k * math.pi / 4
        c.line(m("#d8a040", .05, spec=1.2), 1.2, (52 + 24 * math.cos(a), 56 + 24 * math.sin(a)), (52 + 30 * math.cos(a), 56 + 30 * math.sin(a)))
    c.rect(BRASS, 80, 52, 96, 60, 2, bevel=1.0)
    c.ell(BRASS, 98, 56, 4, 5, bevel=.8)
    for x, y in ((86, 86), (100, 94), (70, 96)):
        c.ell(m("#141210", .06), x + 2, y + 3, 9, 9)
        c.ell(m("#e8e0d0", .04, spec=.6), x, y, 9, 9, bevel=1.4)
        c.ell(m("#6a8a3a", .05, spec=1.2), x, y, 6, 6, bevel=.6)
    wire(c, (30, 82), (22, 100), (24, 118))
    lamp(c, 30, 30, 3, "#ff6a3a")
    return c.image()


@painter
def e_lectern(size=(1, 1)):
    """A tall olive-wood lectern seen from above: a slanted book board with an open book and a green-shaded reading lamp."""
    c = Canvas(128, 128, seed=4303)
    c.poly(m("#141210", .08), (24, 34), (112, 28), (116, 106), (28, 112))
    c.poly(OLIVE_W, (18, 26), (106, 20), (110, 98), (22, 104), bevel=2.6)
    c.poly(m("#5a4428", .12, 3, (9, 1)), (26, 34), (98, 29), (101, 90), (29, 95), bevel=1.2)
    c.poly(m("#efe6d0", .04, 2), (30, 40), (62, 38), (64, 86), (32, 88), bevel=1.0)
    c.poly(m("#e6dcc4", .04, 2), (64, 38), (94, 36), (96, 84), (66, 86), bevel=1.0)
    c.line(m("#7a5a3a", .06), 1.4, (63, 38), (65, 86))
    for k in range(9):
        y = 46 + k * 4.4
        c.scratch(.8, .45, (35, y), (58, y - .3))
        c.scratch(.8, .45, (69, y - .5), (90, y - .8))
    c.line(m("#a02a2a", .05), 1.8, (64, 86), (66, 100))
    c.line(BRASS, 2.4, (96, 26), (86, 14), (70, 12))
    c.ell(m("#1e5a3a", .06, spec=1.4), 62, 14, 14, 8, bevel=2.0)
    lamp(c, 62, 20, 4, "#fff0b8")
    c.glow(62, 56, 40, "#fff0c0", .25)
    wire(c, (104, 60), (118, 66), (124, 90))
    return c.image()


@painter
def e_press(size=(2, 1)):
    """A cast-iron printing press seen from above: a feed board of white silk, two carved rollers, a motor and printed red silk."""
    c = Canvas(256, 128, seed=4304)
    shadow_box(c, 8, 14, 250, 118, 8)
    c.rect(CAST, 6, 10, 246, 112, 8, bevel=2.6)
    c.rect(m("#f0ebe0", .04, 3, (6, 1), spec=.3), 16, 24, 84, 98, 2, bevel=1.0)
    for y in range(30, 96, 8):
        c.scratch(.5, .12, (18, y), (82, y))
    for x0 in (92, 124):
        c.rect(m("#141414", .06), x0 + 2, 18, x0 + 26, 106, 4)
        c.rect(CAST_L, x0, 16, x0 + 24, 104, 10, bevel=3.0)
        for y in range(22, 100, 6):
            c.line(m("#7a8288", .06, spec=.8), 1.4, (x0 + 4, y), (x0 + 20, y + 2))
    c.rect(SILK, 156, 24, 236, 98, 2, bevel=1.0)
    for k in range(5):
        for j in range(4):
            x, y = 166 + k * 15, 34 + j * 17
            c.ell(m("#e8c050", .05, spec=.8), x, y, 4, 4, bevel=.6)
            c.line(m("#e8c050", .05), 1.0, (x - 6, y), (x + 6, y))
    c.rect(MOTOR, 96, 2, 148, 14, 4, bevel=1.4)
    c.ell(CAST_L, 152, 8, 6, 6, bevel=1.2)
    c.line(m("#2a2a2a", .1), 2.4, (100, 8), (88, 8), (88, 18))
    lamp(c, 236, 14, 3, "#88ff88")
    return c.image()


@painter
def e_telegraph(size=(2, 1)):
    """An oak desk seen from above: a brass telegraph key, a sounder, a paper tape, a battery of glass cells and wires to the wall."""
    c = Canvas(256, 128, seed=4305)
    shadow_box(c, 8, 14, 250, 118, 6)
    c.rect(OAK, 6, 10, 246, 110, 6, bevel=2.6)
    c.rect(m("#2e4a32", .06, 2, spec=.3), 20, 22, 150, 98, 3, bevel=.8)
    c.rect(m("#4a2c18", .1), 36, 50, 92, 78, 3, bevel=1.4)
    c.line(BRASS, 4.0, (42, 64), (84, 62), bevel=.8)
    c.ell(BAKELITE, 86, 62, 7, 6, bevel=1.4)
    c.ell(BRASS, 44, 64, 5, 5, bevel=1.0)
    c.rect(m("#4a2c18", .1), 104, 34, 140, 62, 3, bevel=1.4)
    for x in (110, 134):
        c.ell(m("#141414", .05, spec=1.0), x, 48, 6, 8, bevel=1.4)
    c.line(BRASS, 3.0, (110, 48), (134, 46))
    c.line(m("#efe6d0", .03), 6, (108, 72), (124, 84), (136, 96), (150, 100), (170, 104), bevel=.4)
    for k in range(10):
        c.ell(m("#141414", .05), 112 + k * 5, 75 + k * 2.4, 1.0, .8)
    for k in range(4):
        x = 168 + k * 18
        c.rect(m("#141414", .05), x + 2, 26, x + 16, 58, 2)
        c.rect(m("#9ac8c0", .04, 2, spec=1.6), x, 22, x + 14, 54, 2, bevel=1.4)
        c.rect(ZINC, x + 3, 26, x + 11, 50, 1, bevel=.6)
        c.ell(BRASS, x + 7, 24, 2.4, 2.4, bevel=.5)
    for k in range(3):
        wire(c, (175 + k * 18, 24), (184 + k * 18, 16), (193 + k * 18, 24))
    wire(c, (60, 64), (60, 104), (240, 104), (246, 120), w=2.0)
    wire(c, (225, 24), (240, 10), (252, 2), w=2.0)
    c.rect(m("#efe6d0", .04), 170, 72, 230, 98, 1, bevel=.6)
    for y in (78, 84, 90):
        c.scratch(.8, .45, (176, y), (222, y))
    return c.image()


@painter
def e_pump(size=(1, 1)):
    """An electric pump seen from above: a cast-iron casing on a stone well head, a green motor, and clay channels leading out."""
    c = Canvas(128, 128, seed=4306)
    for a in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
        x1, y1 = 64 + 70 * math.cos(a), 64 + 70 * math.sin(a)
        c.line(CLAY, 14, (64, 64), (x1, y1), bevel=1.4)
        c.line(WATER, 7, (64, 64), (x1, y1), bevel=.6)
    c.ell(m("#141210", .08), 68, 70, 44, 42)
    c.ell(GRAN_D, 64, 64, 44, 42, bevel=2.6)
    c.ell(GRAN, 64, 63, 38, 36, bevel=2.2)
    for k in range(12):
        a = k * math.pi / 6
        c.scratch(.9, .35, (64 + 26 * math.cos(a), 63 + 25 * math.sin(a)), (64 + 38 * math.cos(a), 63 + 36 * math.sin(a)))
    c.ell(WATER, 64, 64, 24, 22, bevel=1.0)
    c.rect(m("#141414", .06), 46, 40, 90, 84, 6)
    c.rect(CAST, 42, 36, 86, 80, 6, bevel=2.6)
    c.rect(MOTOR, 50, 42, 78, 62, 8, bevel=2.0)
    for y in range(46, 60, 3):
        c.line(m("#2a402a", .06), 1.0, (54, y), (74, y))
    c.ell(CAST_L, 64, 70, 8, 8, bevel=1.6)
    c.ell(BRASS, 64, 70, 3, 3, bevel=.6)
    lamp(c, 80, 42, 2.6, "#88ff88")
    return c.image()


@painter
def e_forge(size=(3, 1)):
    """An electric forge seen from above: a brick hearth with glowing coals and a blower, an anvil, a power hammer and a quench tub."""
    c = Canvas(384, 128, seed=4307)
    shadow_box(c, 8, 14, 378, 118, 6)
    c.rect(m("#3a3836", .12, 2.5), 6, 10, 376, 112, 6, bevel=2.4)
    brick = m("#8a3a2a", .16, 2)
    for j in range(5):
        for i in range(7):
            x = 14 + i * 16 + (8 if j % 2 else 0)
            c.rect(brick, x, 18 + j * 17, x + 15, 33 + j * 17, 1, bevel=.8)
    c.rect(m("#1a1210", .08), 30, 32, 100, 88, 6)
    c.ell(m("#ff6a1a", .2, 2, spec=.4), 65, 60, 28, 22, bevel=1.0)
    c.ell(m("#ffd060", .1, 2), 65, 60, 14, 10)
    c.glow(65, 60, 60, "#ff8a2a", .7)
    c.rect(MOTOR, 122, 22, 150, 50, 6, bevel=2.0)
    c.line(CAST_L, 8, (122, 36), (102, 48), bevel=1.2)
    c.ell(m("#141414", .06), 200, 68, 34, 16)
    c.poly(CAST_L, (166, 58), (226, 56), (236, 62), (226, 70), (172, 72), (160, 64), bevel=2.6)
    c.rect(m("#7a8288", .05, spec=1.2), 180, 59, 222, 66, 2, bevel=.8)
    c.rect(m("#141414", .06), 262, 24, 312, 98, 4)
    c.rect(CAST, 258, 20, 306, 94, 4, bevel=2.6)
    c.rect(CAST_L, 270, 34, 294, 80, 3, bevel=2.0)
    c.ell(MOTOR, 282, 26, 12, 8, bevel=1.4)
    c.ell(OAK, 344, 60, 26, 26, bevel=2.4)
    c.ell(m("#20303a", .05, spec=1.6), 344, 60, 20, 20, bevel=.8)
    c.line(m("#5a5a5a", .1, spec=.8), 3, (334, 92), (360, 70))
    wire(c, (136, 50), (136, 104), (282, 104), (282, 94))
    return c.image()


@painter
def e_loom(size=(2, 1)):
    """An electric carpet loom seen from above: a wooden frame, a half-knotted carpet in red and indigo, a motor and wool balls."""
    c = Canvas(256, 128, seed=4308)
    shadow_box(c, 8, 14, 250, 118, 6)
    c.rect(WALNUT, 6, 10, 246, 112, 6, bevel=2.6)
    c.rect(m("#3a2418", .1), 18, 20, 210, 100, 3)
    c.rect(WOOL_E, 22, 52, 206, 96, 2, bevel=1.0)
    c.rect(m("#22264a", .1, 2), 30, 58, 198, 90, 2, bevel=.6)
    c.rect(WOOL_E, 38, 62, 190, 86, 2, bevel=.4)
    for k in range(6):
        x = 50 + k * 26
        c.poly(m("#e8d8b0", .06), (x, 74), (x + 8, 66), (x + 16, 74), (x + 8, 82), bevel=.6)
        c.ell(m("#22264a", .1), x + 8, 74, 2.4, 2.4)
    for x in range(24, 206, 4):
        c.line(m("#efe6d0", .03), .8, (x, 22), (x, 52))
    c.line(OAK, 7, (18, 50), (210, 50), bevel=1.4)
    c.line(PARKER, 5, (18, 30), (210, 30), bevel=1.2)
    c.rect(MOTOR, 214, 18, 240, 44, 5, bevel=1.8)
    c.line(m("#141414", .08), 2.6, (220, 30), (206, 30))
    for x, y, col in ((222, 64, "#8a2a2a"), (232, 82, "#22264a"), (220, 98, "#e8d8b0")):
        c.ell(m(col, .12, 1.5), x, y, 8, 8, bevel=1.6)
        for k in range(3):
            c.scratch(.8, .35, (x - 6, y - 4 + k * 4), (x + 6, y - 2 + k * 4))
    return c.image()


@painter
def e_cold_store(size=(2, 2)):
    """A stone cold store seen from above: a flat roof of tarred slabs, a humming cooler with a fan grille, vents and a door frame."""
    c = Canvas(256, 256, seed=4309)
    shadow_box(c, 12, 16, 248, 250, 10, 10)
    c.rect(GRAN_D, 8, 8, 244, 244, 10, bevel=3.2)
    c.rect(GRAN, 18, 18, 234, 234, 6, bevel=2.2)
    for j in range(4):
        for i in range(4):
            x, y = 24 + i * 53, 24 + j * 53
            c.rect(m("#3a3836", .12, 2.5), x, y, x + 50, y + 50, 2, bevel=1.0)
            c.scratch(.8, .2, (x + 4, y + 40), (x + 44, y + 36))
    c.rect(m("#141414", .06), 92, 86, 172, 166, 8)
    c.rect(ZINC, 86, 80, 166, 160, 8, bevel=2.8)
    c.ell(CAST, 126, 120, 30, 30, bevel=2.0)
    for k in range(6):
        a = k * math.pi / 3
        c.poly(CAST_L, (126, 120), (126 + 26 * math.cos(a), 120 + 26 * math.sin(a)),
               (126 + 24 * math.cos(a + .5), 120 + 24 * math.sin(a + .5)), bevel=.8)
    c.ell(CAST, 126, 120, 6, 6, bevel=1.0)
    for r in (14, 22, 30):
        ring(c, m("#141414", .05), 126, 120, r, n=24, w=.9)
    for x in (40, 196):
        c.rect(CAST, x, 200, x + 22, 220, 2, bevel=1.2)
        for y in (204, 210, 216):
            c.line(m("#141414", .05), 1.0, (x + 3, y), (x + 19, y))
    c.rect(m("#6a4a2c", .14, 3, (9, 1)), 98, 232, 158, 248, 2, bevel=1.4)
    c.glow(126, 120, 40, "#c8e8ff", .2)
    lamp(c, 160, 88, 3, "#88ff88")
    wire(c, (166, 120), (200, 120), (236, 140), w=2.0)
    return c.image()
