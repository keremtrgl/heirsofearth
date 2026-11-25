"""Heirs of Earth 3.5: books of the heir nations, seen from above. Every nation writes in its own way: leather codices (Nova Roma,
Albion, Pars), stitched books (Yamato), rune boards (Nordheim), scrolls (Hellas, Kemet), bamboo slips (Tianxia) and knotted
khipu cords (Inti). A worn copy is a lost original: scorched, stained and scratched."""
import math

from heirs_art import m, painter
from kut_render import GOLD, IRON, WOOD, WOOD_D, Canvas

SHADOW = m("#1a140e", .1)
PAGES = m("#e6dcc0", .05, 2, (8, 1))
PAPYRUS = m("#d8c48a", .12, 2, (9, 1), tint="#b8a066")
BAMBOO = m("#b89a52", .10, 2, (1, 9), tint="#8a6e34")
CORD = m("#3a2a1e", .08, 2)
INK = m("#2a2018", .05)
BURN = m("#20140c", .15, 3)


def _shade(hexcol, f):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))


def _emblem(c, kind, cx, cy, s, mat):
    if kind == "laurel":
        for side in (-1, 1):                                            # two branches curving up into a wreath
            for k in range(6):
                a = math.radians(105 + k * 26)
                x, y = cx + side * s * math.cos(a) * -1, cy + s * .9 * math.sin(a) * -1 + s * .1
                c.poly(mat, (x, y - s * .3), (x + side * s * .24, y), (x, y + s * .3), (x - side * s * .12, y), bevel=.7)
        c.line(mat, s * .08, (cx - s * .3, cy + s * .95), (cx + s * .3, cy + s * .95))
    elif kind == "sun":
        for k in range(12):
            a = k * math.pi / 6
            c.line(mat, s * .12, (cx + s * .55 * math.cos(a), cy + s * .55 * math.sin(a)), (cx + s * math.cos(a), cy + s * math.sin(a)))
        c.ell(mat, cx, cy, s * .45, s * .45, bevel=1.2)
    elif kind == "mon":
        c.ell(mat, cx, cy, s * .95, s * .95, bevel=1.0)
        c.ell(m("#1a1a22", .05), cx, cy, s * .78, s * .78)
        for k in range(3):
            a = k * 2 * math.pi / 3 - math.pi / 2
            c.ell(mat, cx + s * .36 * math.cos(a), cy + s * .36 * math.sin(a), s * .3, s * .3, bevel=.8)
    elif kind == "rune":
        c.line(mat, s * .16, (cx, cy - s), (cx, cy + s))
        c.line(mat, s * .16, (cx, cy - s * .2), (cx + s * .6, cy - s * .8))
        c.line(mat, s * .16, (cx, cy + s * .2), (cx - s * .6, cy - s * .4))
    elif kind == "star":
        pts = []
        for k in range(16):
            a = k * math.pi / 8 - math.pi / 2
            r = s if k % 2 == 0 else s * .45
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        c.poly(mat, *pts, bevel=1.0)
    elif kind == "lattice":
        c.rect(mat, cx - s, cy - s, cx + s, cy + s, 2, bevel=1.0)
        c.rect(m("#2a1010", .05), cx - s * .78, cy - s * .78, cx + s * .78, cy + s * .78, 2)
        for t in (-.4, .4):
            c.line(mat, s * .14, (cx - s * .78, cy + s * t), (cx + s * .78, cy + s * t))
            c.line(mat, s * .14, (cx + s * t, cy - s * .78), (cx + s * t, cy + s * .78))
    elif kind == "rose":
        for k in range(5):
            a = k * 2 * math.pi / 5 - math.pi / 2
            c.ell(mat, cx + s * .5 * math.cos(a), cy + s * .5 * math.sin(a), s * .48, s * .48, bevel=1.0)
        c.ell(m("#8c1a1f", .08, 2), cx, cy, s * .4, s * .4, bevel=1.0)
        c.ell(mat, cx, cy, s * .16, s * .16)
    elif kind == "wing":
        for side in (-1, 1):
            for k in range(4):
                c.poly(mat, (cx + side * s * .15, cy - s * .3 + k * s * .2), (cx + side * s * (1.0 - k * .14), cy - s * .55 + k * s * .24),
                       (cx + side * s * (.95 - k * .14), cy - s * .35 + k * s * .24), bevel=.6)
        c.ell(mat, cx, cy, s * .3, s * .3, bevel=1.0)


def _worn(c, seed, form):
    """A lost original: charred corners on bound books, and scratches and wear on everything."""
    rnd = (seed * 7919) % 97
    if form in ("codex", "stitched", "boards"):
        for (x, y, dx, dy) in ((18, 12, 1, 1), (102, 108, -1, -1), (102, 12, -1, 1)):
            k = 14 + rnd % 7
            c.poly(BURN, (x, y), (x + dx * k, y), (x, y + dy * (k + 4)), bevel=.6)
    for k in range(6):
        x = 30 + (rnd * (k + 3)) % 56
        c.scratch(1.1, .55, (x, 34 + k * 11), (x + 14, 39 + k * 11))


@painter
def heirs_book(form="codex", color="#8f2924", emblem="laurel", worn=False, seed=1700):
    c = Canvas(128, seed=seed)
    if worn:
        color = _shade(color, .72)
    cover = m(color, .14 if worn else .10, 2, spec=.1 if worn else .3)
    cover_d = m(_shade(color, .62), .10, 2)
    trim = m("#b89048", .07, 2, spec=1.0) if not worn else m("#8a7040", .12, 2, spec=.4)
    if form in ("codex", "stitched"):
        c.rect(SHADOW, 26, 22, 112, 120, 6)
        c.rect(PAGES, 24, 18, 108, 114, 4, bevel=1.4)                   # page block
        for k in range(4):
            c.line(m("#bfb498", .05), 1, (104, 24 + k * 22), (104, 36 + k * 22))
        c.rect(cover_d, 18, 12, 102, 108, 6, bevel=2.4)
        c.rect(cover, 22, 16, 98, 104, 5, bevel=1.8)
        if form == "codex":
            c.rect(cover_d, 22, 16, 34, 104, 3, bevel=1.2)              # spine
            for y in (30, 52, 74, 92):
                c.line(trim, 2.4, (22, y), (34, y))
            c.rect(trim, 42, 24, 92, 96, 3, bevel=.5)
            c.rect(cover, 45, 27, 89, 93, 2)
            for x, y in ((40, 22), (92, 22), (40, 98), (92, 98)):     # corner pieces
                c.poly(trim, (x - 4, y - 4), (x + 4, y - 4), (x, y + 4), bevel=.8)
            _emblem(c, emblem, 67, 60, 15, trim)
        else:
            c.rect(m("#efe6d0", .04, 2), 74, 22, 92, 80, 1, bevel=.8)  # title slip
            for k in range(5):
                c.line(INK, 1.6, (79, 28 + k * 10), (87, 28 + k * 10))
            for y in (24, 46, 70, 96):                                 # stitched binding on the right
                c.ell(m("#ddd0a8", .05), 28, y, 2.2, 2.2)
                c.line(m("#d8c89a", .05), 1.6, (22, y), (28, y))
            _emblem(c, emblem, 50, 74, 12, trim)
    elif form == "boards":
        c.rect(SHADOW, 22, 20, 114, 118, 4)
        c.rect(PAGES, 22, 18, 106, 112, 2, bevel=1.2)
        c.rect(WOOD_D, 16, 12, 100, 106, 3, bevel=2.4)
        c.rect(WOOD, 20, 16, 96, 102, 2, bevel=1.4)
        for y in (30, 88):
            c.rect(IRON, 14, y - 5, 104, y + 5, 2, bevel=1.4)
            c.ell(IRON, 24, y, 3, 3, bevel=1.0)
            c.ell(IRON, 94, y, 3, 3, bevel=1.0)
        for k in range(3):
            c.scratch(1.6, .75, (36 + k * 10, 44), (36 + k * 10, 74))
            c.scratch(1.4, .7, (36 + k * 10, 52), (42 + k * 10, 46))
        _emblem(c, emblem, 74, 59, 12, m(color, .1, 2, spec=.6))
    elif form == "scroll":
        paper = PAPYRUS if emblem == "sun" else PAGES
        c.rect(SHADOW, 18, 50, 118, 92, 10)
        c.rect(paper, 22, 44, 106, 84, 4, bevel=1.4)
        for k in range(5):
            c.line(m("#6a5a40", .06), 1.2, (40, 52 + k * 6), (88 + (k % 2) * 8, 52 + k * 6))
        for x in (20, 108):                                            # rolled ends with rods
            c.ell(paper, x, 64, 10, 22, bevel=1.8)
            c.rect(WOOD_D, x - 3, 36, x + 3, 92, 2, bevel=1.0)
            c.ell(trim, x, 36, 5, 4, bevel=1.0)
            c.ell(trim, x, 92, 5, 4, bevel=1.0)
        c.rect(cover, 56, 40, 66, 88, 2, bevel=1.2)                    # ribbon and seal
        c.ell(m(_shade(color, .8), .08, 2, spec=.5), 61, 64, 9, 9, bevel=1.4)
        _emblem(c, emblem, 61, 64, 6, trim)
    elif form == "bamboo":
        c.rect(SHADOW, 16, 26, 116, 110, 4)
        for k in range(13):
            x = 18 + k * 7
            c.rect(BAMBOO, x, 22, x + 6, 104, 2, bevel=1.0)
            for j in range(6):
                c.line(INK, 1.4, (x + 2, 34 + j * 11), (x + 4, 34 + j * 11))
        for y in (36, 90):
            c.line(cover, 2.6, (14, y), (112, y))
        c.rect(m(_shade(color, .9), .06, 2), 92, 52, 116, 74, 2, bevel=1.0)
        _emblem(c, emblem, 104, 63, 8, trim)
    elif form == "khipu":
        c.ell(m("#2a2018", .1), 66, 74, 46, 36)
        c.line(m(_shade(color, .7), .1, 2), 5, (16, 26), (112, 26))  # main cord
        cols = (color, "#e2d3a8", "#4a6a8a", "#c99a2e", "#2e2a24", "#8a3a2a", "#6a8a4a")
        for k in range(13):
            x = 22 + k * 7.2
            sway = 6 * math.sin(k * 1.3)
            cm = m(cols[k % len(cols)], .1, 2)
            c.line(cm, 2.6, (x, 26), (x + sway * .5, 70), (x + sway, 112 - (k % 3) * 8))
            for j in range(1 + (k * 5) % 4):
                c.ell(m(_shade(cols[k % len(cols)], .7), .1, 2), x + sway * (.3 + j * .15), 44 + j * 14, 3.2, 3.6, bevel=1.0)
        c.ell(trim, 16, 26, 5, 5, bevel=1.2)
        c.ell(trim, 112, 26, 5, 5, bevel=1.2)
        if worn:
            for k in range(4):
                c.line(m("#5a4a3a", .2), 2.2, (40 + k * 14, 60), (52 + k * 10, 74), (44 + k * 12, 88))
    if worn:
        _worn(c, seed, form)
    return c.image()
