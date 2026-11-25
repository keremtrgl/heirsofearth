"""Heirs of Earth 1.0 painters for the story chains: lost relics and the three artifacts.

Registered into heirs_art.PAINTERS on import; heirs_art.render_all() imports this module.
"""
import math

import numpy as np
from PIL import Image, ImageFilter

import heirs_style_sample as sample
from heirs_art import (BRONZE, DARKIRON, GOLD, IRON, LEATHER, LEATHER_D, STEEL, STONE, STONE_D, WOOD, WOOD_D, WOOD_V, Canvas,
                       _eagle, axis, haft, m, painter, wraps)

TARNISH = m("#5e6a4a", .22, 2, spec=.3, tint="#3c4a34")
CRIMSON = m("#8e2a24", .10, 2, tint="#6d1f1c")
HORN = m("#d9c9a0", .10, 2, (1, 4), spec=.5, tint="#9a7a4a")
HORN_D = m("#6a4a2a", .12, 2, spec=.4)
SILVER = m("#c9d0d6", .06, 2, spec=1.2)
FROST = m("#e8f2fa", .10, 1.5, spec=.8)
SILK_R = m("#a8322a", .08, 2, spec=.4)
CUSHION = m("#5a2a6a", .10, 2, spec=.3)


def _halo(img, color, radius=7, strength=1.0):
    """Adds a soft coloured glow behind an RGBA image."""
    a = img.split()[3].filter(ImageFilter.GaussianBlur(radius))
    a = a.point(lambda v: int(min(255, v * 1.6 * strength)))
    glow = Image.new("RGBA", img.size, color)
    glow.putalpha(a)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(img)
    return out


def _eagle_at(c, mat, s=1.0, dx=0.0, dy=0.0, broken=False):
    """The legion eagle emblem drawn onto a scaled, moved copy of the canvas coordinates."""
    class Shift:
        def poly(self, mt, *pts, **kw):
            c.poly(mt, *[(64 + (x - 64) * s + dx, 50 + (y - 50) * s + dy) for x, y in pts], **kw)

        def ell(self, mt, x, y, rx, ry, **kw):
            c.ell(mt, 64 + (x - 64) * s + dx, 50 + (y - 50) * s + dy, rx * s, ry * s, **kw)

        def line(self, mt, w, *pts, **kw):
            c.line(mt, w * s, *[(64 + (x - 64) * s + dx, 50 + (y - 50) * s + dy) for x, y in pts], **kw)

        def scratch(self, w, o, *pts, **kw):
            c.scratch(w * s, o, *[(64 + (x - 64) * s + dx, 50 + (y - 50) * s + dy) for x, y in pts], **kw)
    _eagle(Shift(), mat)


def _horn(c, mat, band):
    """A drinking horn: narrow tip at the upper left, curving down and out to a wide mouth on the right."""
    p0, p1, p2 = (22, 30), (34, 104), (104, 86)
    pts = []
    for i in range(19):
        t = i / 18
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y, 2.5 + 15 * t ** 1.2))
    c.line(m("#2a1e14", .1), 26, *[(x + 2, y + 6) for x, y, _ in pts[9:]])
    for i in range(len(pts) - 1):
        (x0, y0, r0), (x1, y1, r1) = pts[i], pts[i + 1]
        nx, ny = -(y1 - y0), (x1 - x0)
        ln = math.hypot(nx, ny) or 1
        nx, ny = nx / ln, ny / ln
        c.poly(mat, (x0 + nx * r0, y0 + ny * r0), (x1 + nx * r1, y1 + ny * r1), (x1 - nx * r1, y1 - ny * r1), (x0 - nx * r0, y0 - ny * r0), bevel=2.4)
        c.ell(mat, x1, y1, r1, r1, bevel=2.4)
    x, y, r = pts[-1]
    c.ell(band, x + 1, y, 4.6, r + 1.6, bevel=1.6)
    c.ell(HORN_D, x + 2, y, 3.2, r - 2.4, bevel=1.0)
    for i in (6, 12):
        (xa, ya, _), (x, y, r) = pts[i - 1], pts[i]
        nx, ny = -(y - ya), (x - xa)
        ln = math.hypot(nx, ny) or 1
        nx, ny = nx / ln, ny / ln
        c.line(band, 4.2, (x + nx * (r + 1), y + ny * (r + 1)), (x - nx * (r + 1), y - ny * (r + 1)))
    c.ell(band, pts[0][0], pts[0][1], 4.0, 4.0, bevel=1.4)
    return pts


def ring(c, cx, cy, r, mat, width=2.0):
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]
    c.line(mat, width, *pts)


@painter
def relic(kind="eagle"):
    c = Canvas(128, seed=91)
    if kind == "eagle":
        c.rect(STONE_D, 30, 98, 98, 116, 3, bevel=2.0)
        c.poly(STONE, (36, 98), (92, 98), (88, 90), (40, 90), bevel=1.4)
        _eagle_at(c, m("#8a6a34", .14, 2, spec=.9, tint="#5a4a2a"), 1.05, 0, 22)
        for x, y in ((48, 52), (70, 66)):
            c.ell(m("#6a9478", .12), x, y, 2, 1.4)
        c.scratch(1.4, .7, (74, 44), (80, 52), (78, 60))
        c.scratch(1.2, .55, (64, 90), (58, 95), (62, 99))
    elif kind == "regalia":
        c.rect(m("#2a1414", .1), 22, 34, 110, 112, 10)
        c.rect(m("#7a1f24", .10, 2, spec=.4), 18, 30, 106, 108, 10, bevel=2.6)
        for x, y in ((18, 30), (106, 30), (18, 108), (106, 108)):
            c.line(GOLD, 2.4, (x, y), (x + (6 if x < 64 else -6) * -1, y + (8 if y > 64 else -8)))
            c.ell(GOLD, x, y, 3.4, 3.4, bevel=1.2)
        c.ell(m("#3a2a1a", .1), 66, 72, 32, 32)
        c.ell(BRONZE, 62, 68, 32, 32, bevel=2.8)
        c.ell(m("#c9d6dc", .04, 2, spec=1.6), 62, 68, 23, 23, bevel=.8)
        c.ell(m("#ffffff", .02), 54, 60, 7, 4)
        for i in range(12):
            a2 = i * math.pi / 6
            c.ell(GOLD, 62 + 27.5 * math.cos(a2), 68 + 27.5 * math.sin(a2), 2.0, 2.0, bevel=.8)
        c.line(SILK_R, 3.2, (62, 36), (58, 24), (66, 16))
    else:  # sealed barrow horn
        pts = _horn(c, HORN, DARKIRON)
        for x, y, r in pts[2:]:
            c.ell(FROST, x, y - r * .55, max(1.5, r * .55), max(1.2, r * .3))
    return c.image()


@painter
def eagle_standard():
    c = Canvas(128, seed=92)
    haft(c, axis((64, 126), (64, 30))[0], 0, 96, 4.0, WOOD_V)
    c.rect(GOLD, 38, 58, 90, 62, 2, bevel=1.2)
    c.poly(CRIMSON, (41, 62), (87, 62), (87, 100), (64, 108), (41, 100), bevel=2.0)
    c.rect(GOLD, 45, 67, 83, 70, 1, bevel=.8)
    c.rect(GOLD, 45, 90, 83, 93, 1, bevel=.8)
    c.ell(GOLD, 64, 80, 6, 6, bevel=1.4)
    for x in range(43, 87, 4):
        y0 = 100 + (23 - abs(x - 64)) * .35
        c.line(GOLD, 1.1, (x, y0), (x, y0 + 5))
    c.ell(GOLD, 64, 54, 6, 4, bevel=1.4)
    c.rect(GOLD, 56, 46, 72, 52, 2, bevel=1.2)
    _eagle_at(c, GOLD, .82, 0, -14)
    return _halo(c.image(), (255, 214, 120, 255), 5, .5)


@painter
def sky_sword():
    img = sample.katana().convert("RGBA")
    arr = np.asarray(img).astype(np.float32)
    # cool the steel toward a pale sky blue
    blue = np.array([180, 214, 255], dtype=np.float32)
    lum = arr[..., :3].mean(axis=2, keepdims=True) / 255
    mask = (lum > .55).astype(np.float32) * .35
    arr[..., :3] = arr[..., :3] * (1 - mask) + blue * mask
    img = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")
    return _halo(img, (140, 196, 255, 255), 6, .8)


@painter
def storm_horn():
    c = Canvas(128, seed=94)
    pts = _horn(c, HORN, SILVER)
    for i in (3, 7, 12):
        x, y, r = pts[i]
        for k in range(3):
            c.line(m("#4a7aaa", .1, spec=.8), 1.3, (x - 3 + k * 3, y - r * .45), (x - 1 + k * 3, y + r * .45))
    img = c.image()
    return _halo(img, (150, 200, 255, 255), 7, .7)
