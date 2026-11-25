"""Heirs of Earth 4.1: worn body garments. Every heir tunic, coat, robe, cloak and armour gets its own worn graphic for the five
vanilla body types and three sides (west is east flipped by the game). Each garment is built on the real vanilla body outline
(tools/art_ref/body_<type>_<rot>.png, the alpha of the game's naked body textures, kept locally and never shipped), grown by the
layer's thickness, and its details are placed in coordinates relative to that body, so one design fits every body.
Vanilla manner: a bold dark outline, soft cylindrical shading, dark inner lines. Parts made of the item's stuff are painted in
neutral greys and marked red in the _m mask; trims, gold, lacing and dyes keep their own colours."""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from heirs_art import painter
from heirs_art18 import catmull, hexrgb, INK, STUFF, STUFF_D, STUFF_DD, GOLD, GOLD_D, RED, RED_D

K = 4
S = 128 * K
OUTLINE = 2.6
INNER = 1.2
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art_ref")
YY, XX = np.mgrid[0:S, 0:S].astype(np.float32) / K
BODIES = ["Male", "Female", "Thin", "Hulk", "Fat"]
ROTS = ["south", "east", "north"]

# fixed colours
WHITE = "#ece8dc"
LINEN = "#efe9d6"
BLACK = "#26221f"
NAVY = "#25345a"
BLUE = "#2f5f9e"
TEAL = "#2a8a86"
PURPLE = "#6a2a6e"
BROWN = "#6b4a2c"
BROWN_D = "#4a311c"
LEATHER = "#8a6038"
BRONZE = "#b98a3e"
GREEN = "#3c7a3a"
YELLOW = "#e6c23a"
ORANGE = "#d8742a"
CRIMSON = "#a51e2c"

_bodies = {}


def body_mask(body, rot):
    if (body, rot) not in _bodies:
        a = Image.open(os.path.join(REF, f"body_{body}_{rot}.png")).convert("L").resize((S, S), Image.BILINEAR)
        m = (np.asarray(a, np.float32) / 255.0 > 0.5).astype(np.float32)
        _bodies[(body, rot)] = m
    return _bodies[(body, rot)]


def to_img(m):
    return Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8))


def grow(m, px):
    """Grows a mask by px (at 128) with a rounded edge."""
    if px <= 0:
        return m
    img = to_img(m)
    for _ in range(int(round(px * K))):
        img = img.filter(ImageFilter.MaxFilter(3))
    img = img.filter(ImageFilter.GaussianBlur(K * 0.8))
    return (np.asarray(img, np.float32) / 255.0 > 0.5).astype(np.float32)


_grown = {}


def grown_body(body, rot, px):
    if (body, rot, px) not in _grown:
        _grown[(body, rot, px)] = grow(body_mask(body, rot), px)
    return _grown[(body, rot, px)]


def shrink(m, px):
    img = to_img(m)
    for _ in range(int(round(px * K))):
        img = img.filter(ImageFilter.MinFilter(3))
    return np.asarray(img, np.float32) / 255.0


def smooth(m, r=0.6):
    return np.asarray(to_img(m).filter(ImageFilter.GaussianBlur(K * r)), np.float32) / 255.0


class Wear:
    """One garment on one body from one side. Details are given in (u, v): 0..1 across the body's own box; u grows to the
    viewer's right, v downward. From the east the pawn faces right, so the front is at high u."""

    def __init__(self, body, rot, grow_px=0.0, thin_extra=0.0):
        self.body, self.rot = body, rot
        b = body_mask(body, rot)
        ys, xs = np.nonzero(b)
        self.x0, self.x1 = xs.min() / K, xs.max() / K
        self.y0, self.y1 = ys.min() / K, ys.max() / K
        self.w, self.h = self.x1 - self.x0, self.y1 - self.y0
        self.U = (XX - self.x0) / self.w
        self.V = (YY - self.y0) / self.h
        px = grow_px + (thin_extra if body == "Thin" else 0.0)
        self.G = grown_body(body, rot, px).copy()
        self.parts = []
        self.cut = np.zeros((S, S), np.float32)

    # -- geometry -------------------------------------------------------------------------------------------------------
    def xy(self, u, v):
        return self.x0 + u * self.w, self.y0 + v * self.h

    def poly(self, pts, smooth_curve=False):
        pts = catmull(pts, 8) if smooth_curve else pts
        img = Image.new("L", (S, S), 0)
        ImageDraw.Draw(img).polygon([(x * K, y * K) for x, y in (self.xy(u, v) for u, v in pts)], fill=255)
        return np.asarray(img, np.float32) / 255.0

    def ell(self, u, v, ru, rv):
        x, y = self.xy(u, v)
        rx, ry = ru * self.w, rv * self.h
        img = Image.new("L", (S, S), 0)
        ImageDraw.Draw(img).ellipse([(x - rx) * K, (y - ry) * K, (x + rx) * K, (y + ry) * K], fill=255)
        return np.asarray(img, np.float32) / 255.0

    def circle(self, u, v, r_px):
        x, y = self.xy(u, v)
        img = Image.new("L", (S, S), 0)
        ImageDraw.Draw(img).ellipse([(x - r_px) * K, (y - r_px) * K, (x + r_px) * K, (y + r_px) * K], fill=255)
        return np.asarray(img, np.float32) / 255.0

    def stroke(self, pts, w_px, curve=True):
        pts = catmull(pts, 8, closed=False) if curve and len(pts) > 2 else pts
        xy = [self.xy(u, v) for u, v in pts]
        img = Image.new("L", (S, S), 0)
        d = ImageDraw.Draw(img)
        d.line([(x * K, y * K) for x, y in xy], fill=255, width=max(1, int(w_px * K)), joint="curve")
        for x, y in (xy[0], xy[-1]):
            d.ellipse([(x - w_px / 2) * K, (y - w_px / 2) * K, (x + w_px / 2) * K, (y + w_px / 2) * K], fill=255)
        return np.asarray(img, np.float32) / 255.0

    def smile(self, u):
        """How far a horizontal band sags at u: bands round the body bow toward the viewer."""
        return 0.035 * (1 - (2 * u - 1) ** 2) if self.rot != "east" else 0.02 * (1 - (2 * u - 1) ** 2)

    def band(self, v0, v1, curve=True):
        s = self.smile(np.clip(self.U, 0, 1)) if curve else 0
        return ((self.V >= v0 + s) & (self.V < v1 + s)).astype(np.float32)

    def below(self, v0, curve=True):
        s = self.smile(np.clip(self.U, 0, 1)) if curve else 0
        return (self.V >= v0 + s).astype(np.float32)

    def cols(self, u0, u1):
        return ((self.U >= u0) & (self.U < u1)).astype(np.float32)

    def extend(self, m):
        """Adds to the garment's outline (shoulder pieces, flared hems)."""
        self.G = np.maximum(self.G, m)

    def open(self, m):
        """Cuts the garment open (an open front shows what is worn beneath)."""
        self.cut = np.maximum(self.cut, m)

    # -- painting -------------------------------------------------------------------------------------------------------
    def add(self, m, color, stuff=False, shade="cyl", line=True, lw=INNER, gloss=0.0, clip=True):
        if clip:
            m = m * self.G
        if m.max() <= 0:
            return self
        self.parts.append((m, color, stuff, shade, line, lw, gloss))
        return self

    def base(self, color=STUFF, stuff=True, gloss=0.0):
        return self.add(self.G.copy(), color, stuff, "cyl", line=False, gloss=gloss)

    def lines(self, m, color=STUFF_DD, stuff=True):
        return self.add(m, color, stuff, "none", line=False)

    def render(self):
        G = self.G * (1 - self.cut)
        rgb = np.zeros((S, S, 3), np.float32)
        alpha = np.zeros((S, S), np.float32)
        stuffmap = np.zeros((S, S), np.float32)
        light = 0.36 if self.rot != "east" else 0.55
        soft = np.asarray(to_img(G).filter(ImageFilter.GaussianBlur(4.0 * K)), np.float32) / 255.0
        softf = 0.82 + 0.18 * np.clip(soft * 1.6 - 0.25, 0, 1)
        u = np.clip(self.U, 0, 1)
        v = np.clip(self.V, 0, 1)
        for m, color, stuff, shade, line, lw, gloss in self.parts:
            m = np.clip(m * G, 0, 1)
            if m.max() <= 0:
                continue
            mimg = to_img(m)
            if shade == "cyl":
                f = 0.72 + 0.34 * np.sin(np.pi * np.clip(u * 0.9 + 0.05 + (0.36 - light) * 0.4, 0, 1)) ** 0.8 - 0.10 * v
            elif shade == "dome":
                f = 1.06 - 0.6 * ((u - light) ** 2 + 0.7 * (v - 0.35) ** 2)
            elif shade == "flat":
                f = 1.0 - 0.12 * v
            else:
                f = np.ones_like(u)
            f = f * softf
            col = hexrgb(color)[None, None, :] * f[..., None]
            if gloss:
                g = np.exp(-(((u - light + 0.08) / 0.18) ** 2 + ((v - 0.42) / 0.2) ** 2)) * gloss
                col = col + (255 - col) * g[..., None]
            col = np.clip(col, 0, 255)
            a = m[..., None]
            rgb = rgb * (1 - a) + col * a
            alpha = np.maximum(alpha, m)
            stuffmap = stuffmap * (1 - m) + m * (1.0 if stuff else 0.0)
            if line:
                k = int(round(lw * K)) * 2 + 1
                inner = np.asarray(mimg.filter(ImageFilter.MinFilter(k)), np.float32) / 255.0
                edge = np.clip(m - inner, 0, 1)
                rgb = rgb * (1 - edge[..., None]) + np.array(INK, np.float32) * edge[..., None]
        alpha = np.minimum(alpha, G)
        aimg = to_img(alpha)
        k = int(round(OUTLINE * K)) * 2 + 1
        # the outline sits inside the garment's edge so the garment never grows past the body sizes vanilla expects
        inner = np.asarray(aimg.filter(ImageFilter.MinFilter(k)), np.float32) / 255.0
        inner = smooth(inner, 0.35)
        edge = np.clip(alpha - inner, 0, 1)
        final_rgb = rgb * (1 - edge[..., None]) + np.array(INK, np.float32) * edge[..., None]
        img = Image.fromarray(np.dstack([final_rgb, alpha * 255]).astype(np.uint8), "RGBA").resize((128, 128), Image.LANCZOS)
        mask = Image.fromarray((stuffmap * inner * 255).astype(np.uint8)).resize((128, 128), Image.LANCZOS)
        z = Image.new("L", (128, 128), 0)
        return img, Image.merge("RGBA", (mask, z, z, Image.new("L", (128, 128), 255)))


# ------------------------------------------------------------------ shared pieces
def front_u(w):
    """Where the front centre is: the middle from the south and north, toward the right from the east."""
    return 0.5 if w.rot != "east" else 0.74


def folds(w, n, v0, v1, color=STUFF_DD, width=0.9, sway=0.02, stuff=True, region=None):
    """Soft vertical fabric folds."""
    for i in range(n):
        u = 0.08 + 0.84 * (i + 0.5) / n
        pts = [(u + sway * math.sin(i * 1.7), v0), (u - sway * 0.6, (v0 + v1) / 2), (u + sway * 0.8 * math.cos(i), v1)]
        m = w.stroke(pts, width)
        if region is not None:
            m = m * region
        w.lines(m, color, stuff)


def hem_band(w, v0, v1, color, stuff=False, pattern=None):
    w.add(w.below(v0) * w.band(v0, v1 + 1), color, stuff, "cyl", lw=1.0)
    if pattern:
        pattern(w, v0, v1)


def belt(w, v, h, color, buckle=None, stuff=False):
    w.add(w.band(v, v + h), color, stuff, "cyl", lw=1.0)
    if buckle and w.rot != "north":
        fu = front_u(w)
        w.add(w.ell(fu, v + h / 2 + w.smile(fu), 0.07, h * 0.75), buckle, False, "dome", lw=0.9, gloss=0.35)


def rows_of_scales(w, v0, v1, step, color=STUFF_DD, stuff=True, size=0.06, region=None):
    """Overlapping scale rows: little downward arcs, staggered."""
    r = 0
    v = v0
    acc = np.zeros((S, S), np.float32)
    while v < v1:
        off = (r % 2) * size
        u = -size + off
        while u < 1 + size:
            pts = [(u - size, v), (u, v + step * 0.9), (u + size, v)]
            acc = np.maximum(acc, w.stroke(pts, 0.8))
            u += 2 * size
        v += step
        r += 1
    if region is not None:
        acc = acc * region
    w.lines(acc * w.band(v0, v1, False), color, stuff)


def mail(w, v0, v1, color=STUFF_DD, region=None):
    """Riveted mail: a dense grid of tiny rings."""
    m = np.zeros((S, S), np.float32)
    sy = 3.0
    sx = 3.0
    yy = (YY - w.y0) / sy
    xx = (XX - w.x0) / sx + 0.5 * (np.floor(yy) % 2)
    fx = xx - np.floor(xx) - 0.5
    fy = yy - np.floor(yy) - 0.5
    d = np.sqrt(fx ** 2 + fy ** 2)
    ring = ((d > 0.2) & (d < 0.46)).astype(np.float32)
    m = ring * w.band(v0, v1, False)
    if region is not None:
        m = m * region
    w.lines(m, color, True)
    rowline = ((yy - np.floor(yy)) > 0.82).astype(np.float32) * w.band(v0, v1, False)
    if region is not None:
        rowline = rowline * region
    w.lines(rowline, STUFF_D, True)


def lamellae(w, v0, v1, rows, lace, stuff=True, plate=STUFF, gap=0.05, lacing_dots=True):
    """Rows of small plates laced together: each row a band, upright plate edges, and coloured lacing between rows."""
    hgt = (v1 - v0) / rows
    for r in range(rows):
        a = v0 + r * hgt
        w.add(w.band(a, a + hgt), plate if r % 2 == 0 else STUFF_D, stuff, "cyl", lw=0.9)
        n = 16
        acc = np.zeros((S, S), np.float32)
        for i in range(n + 1):
            u = i / n + (0.5 / n if r % 2 else 0)
            acc = np.maximum(acc, w.stroke([(u, a + 0.012), (u, a + hgt - 0.01)], 0.7, curve=False))
        w.lines(acc * w.band(a, a + hgt), STUFF_DD, stuff)
        w.add(w.band(a + hgt - 0.018, a + hgt + 0.008), lace, False, "none", line=False)
        if lacing_dots:
            dots = np.zeros((S, S), np.float32)
            for i in range(n):
                u = (i + 0.5) / n
                dots = np.maximum(dots, w.circle(u, a + hgt * 0.5 + w.smile(u), 0.55))
            w.add(dots, lace, False, "none", line=False)


def strips(w, v0, v1, n, color, stuff, gap_color=None):
    """Hanging strips (pteruges, tassets): a skirt cut into tabs."""
    hgt = v1 - v0
    w.extend(w.poly([(0.06, v0), (0.94, v0), (0.96, v1 + 0.04), (0.04, v1 + 0.04)]) * grown_body(w.body, w.rot, 3))
    for i in range(n):
        u0 = 0.02 + 0.96 * i / n
        u1 = 0.02 + 0.96 * (i + 1) / n - 0.012
        tab = w.poly([(u0, v0), (u1, v0), (u1, v1), ((u0 + u1) / 2, v1 + 0.025), (u0, v1)])
        w.add(tab, color, stuff, "cyl", lw=0.9)


def trim_line(w, pts, width, color, stuff=False, gloss=0.0):
    w.add(w.stroke(pts, width), color, stuff, "flat", lw=0.8, gloss=gloss)


def studs(w, pts, r, color=GOLD, gloss=0.4):
    for u, v in pts:
        w.add(w.circle(u, v, r), color, False, "dome", lw=0.6, gloss=gloss)


def shoulder_pads(w, v, ru, rv, color=STUFF, stuff=True, rows=0, edge=None):
    sides = [0.08, 0.92] if w.rot != "east" else [0.5]
    for su in sides:
        m = w.ell(su, v, ru, rv)
        w.extend(m)
        w.add(m, color, stuff, "dome", lw=1.0)
        for r in range(rows):
            vv = v - rv * 0.2 + r * rv * 0.45
            w.lines(w.stroke([(su - ru * 0.85, vv), (su, vv + rv * 0.25), (su + ru * 0.85, vv)], 0.8) * m, STUFF_DD, stuff)
        if edge:
            w.add(np.clip(m - shrink(m, 1.6), 0, 1), edge, False, "none", line=False)


def wrap_front(w, color, width=3.0, stuff=False, over="right", v_end=0.82):
    """A wrapped front (kimono, hanfu, kaftan): the overlapping panel's edge runs from the neck down to the waist."""
    fu = front_u(w)
    if w.rot == "north":
        return
    if w.rot == "south":
        a = (fu - 0.16, 0.12) if over == "right" else (fu + 0.16, 0.12)
        b = (fu + 0.10, v_end) if over == "right" else (fu - 0.10, v_end)
        trim_line(w, [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 0.02), b], px(w, width), color, stuff)
        c = (fu + 0.16, 0.12) if over == "right" else (fu - 0.16, 0.12)
        trim_line(w, [c, (fu, 0.34)], px(w, width) * 0.9, color, stuff)
    else:
        trim_line(w, [(fu - 0.12, 0.12), (fu + 0.06, 0.4), (fu + 0.1, v_end)], px(w, width), color, stuff)


def px(w, v):
    """A stroke width in px scaled a little with the body width (thin bodies get thinner trims)."""
    return v * max(0.7, min(1.25, w.w / 51.0))


# ------------------------------------------------------------------ the garments
def redcoat(w):
    w.base()
    fu = front_u(w)
    if w.rot == "south":
        for a, b in (((0.12, 0.18), (0.82, 0.86)), ((0.88, 0.18), (0.18, 0.86))):
            trim_line(w, [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.03), b], px(w, 3.6), WHITE)
        w.add(w.ell(0.5, 0.56, 0.08, 0.05), GOLD, False, "dome", lw=0.8, gloss=0.4)
        studs(w, [(0.5, v) for v in (0.70, 0.80)], px(w, 1.3))
        w.add(w.band(0.9, 1.1), STUFF_D, True, "cyl", lw=1.0)
    elif w.rot == "east":
        trim_line(w, [(0.38, 0.16), (0.58, 0.5), (0.78, 0.86)], px(w, 3.6), WHITE)
        trim_line(w, [(fu + 0.12, 0.2), (fu + 0.14, 0.9)], px(w, 2.4), NAVY)
        studs(w, [(fu + 0.04, v) for v in (0.42, 0.56, 0.70)], px(w, 1.3))
        w.add(w.poly([(-0.1, 0.66), (0.22, 0.66), (0.2, 1.1), (-0.1, 1.1)]), STUFF_D, True, "cyl", lw=1.0)         # coat tail
    else:
        for a, b in (((0.14, 0.2), (0.84, 0.82)), ((0.86, 0.2), (0.16, 0.82))):
            trim_line(w, [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.03), b], px(w, 3.4), WHITE)
        w.lines(w.stroke([(0.5, 0.78), (0.5, 1.02)], 1.0), STUFF_DD)
        studs(w, [(0.42, 0.74), (0.58, 0.74)], px(w, 1.3))
    belt(w, 0.62, 0.05, WHITE)


def frockcoat(w):
    w.extend(w.poly([(0.0, 0.6), (1.0, 0.6), (1.06, 1.08), (-0.06, 1.08)], True) * grown_body(w.body, w.rot, 4))
    w.base()
    fu = front_u(w)
    if w.rot == "south":
        w.add(w.poly([(0.36, 0.1), (0.64, 0.1), (0.6, 0.74), (0.4, 0.74)]), "#cdb88a", False, "cyl", lw=1.0)  # buff waistcoat
        studs(w, [(0.5, v) for v in (0.42, 0.52, 0.62)], px(w, 1.1), BRONZE)
        for s in (-1, 1):
            w.lines(w.stroke([(0.5 + s * 0.15, 0.12), (0.5 + s * 0.2, 0.4), (0.5 + s * 0.13, 1.0)], 1.1), STUFF_DD)
            studs(w, [(0.5 + s * 0.24, v) for v in (0.44, 0.56)], px(w, 1.3), GOLD)
        w.add(w.poly([(0.42, 0.74), (0.58, 0.74), (0.62, 1.1), (0.38, 1.1)]), STUFF_DD, True, "flat", lw=1.0)
    elif w.rot == "east":
        w.lines(w.stroke([(fu, 0.14), (fu + 0.06, 0.6), (fu - 0.04, 1.0)], 1.1), STUFF_DD)
        studs(w, [(fu + 0.06, v) for v in (0.44, 0.56)], px(w, 1.3), GOLD)
        w.add(w.ell(0.62, 0.48, 0.12, 0.06), STUFF_D, True, "cyl", lw=0.9)                                  # pocket flap
    else:
        w.lines(w.stroke([(0.5, 0.6), (0.5, 1.1)], 1.2), STUFF_DD)
        studs(w, [(0.44, 0.6), (0.56, 0.6)], px(w, 1.3), GOLD)
        w.lines(w.stroke([(0.2, 0.56), (0.5, 0.6), (0.8, 0.56)], 1.0), STUFF_DD)
    folds(w, 4, 0.7, 1.05, width=0.8)


def meander(w, v0, v1, color, ground):
    """A Greek key border: a dark band with a running key in the trim colour."""
    w.add(w.band(v0, v1), ground, False, "cyl", lw=0.9)
    hgt = v1 - v0
    n = 9
    for i in range(n):
        u = (i + 0.2) / n
        du = 0.6 / n
        pts = [(u, v0 + hgt * 0.75), (u, v0 + hgt * 0.25), (u + du, v0 + hgt * 0.25), (u + du, v0 + hgt * 0.6), (u + du * 0.5, v0 + hgt * 0.6)]
        sm = [(x, y + w.smile(x)) for x, y in pts]
        w.add(w.stroke(sm, 0.9, curve=False) * w.band(v0, v1), color, False, "none", line=False)


def linothorax(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    strips(w, 0.8, 0.98, 9, STUFF_D, True)
    w.add(w.below(-1) * (1 - w.below(0.8)), STUFF, True, "cyl", line=False)
    w.lines(w.band(0.3, 0.31), STUFF_DD)
    meander(w, 0.52, 0.6, GOLD, CRIMSON)
    w.add(w.band(0.74, 0.8), STUFF_D, True, "cyl", lw=0.9)
    if w.rot == "south":
        for su in (0.2, 0.8):
            w.add(w.poly([(su - 0.12, 0.14), (su + 0.12, 0.14), (su + 0.1, 0.36), (su - 0.1, 0.36)], True), STUFF_D, True, "cyl", lw=1.0)
            studs(w, [(su, 0.33)], px(w, 1.4), BRONZE)
        w.add(w.circle(0.5, 0.42, px(w, 4.0)), BRONZE, False, "dome", lw=0.8, gloss=0.4)             # gorgon boss
        w.add(w.circle(0.5, 0.42, px(w, 2.0)), RED_D, False, "dome", line=False)
    elif w.rot == "east":
        w.add(w.poly([(0.36, 0.1), (0.66, 0.1), (0.64, 0.38), (0.38, 0.38)], True), STUFF_D, True, "cyl", lw=1.0)
        studs(w, [(0.52, 0.34)], px(w, 1.4), BRONZE)
    else:
        w.lines(w.stroke([(0.2, 0.2), (0.5, 0.26), (0.8, 0.2)], 1.0), STUFF_DD)


def chiton(w):
    w.base()
    folds(w, 7, 0.18, 1.0, width=0.8, sway=0.015)
    trim_line(w, [(0.04, 0.6), (0.5, 0.6 + w.smile(0.5)), (0.96, 0.6)], px(w, 1.8), "#b8955a")             # cord girdle
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.stroke([(fu - 0.02, 0.6), (fu - 0.04, 0.76)], px(w, 1.4)), "#b8955a", False, "flat", lw=0.6)
        w.add(w.stroke([(fu + 0.03, 0.6), (fu + 0.05, 0.74)], px(w, 1.4)), "#b8955a", False, "flat", lw=0.6)
    meander(w, 0.9, 0.97, WHITE, NAVY)


def himation(w):
    w.base()
    fu = front_u(w)
    if w.rot == "south":
        w.add(w.poly([(0.0, 0.08), (0.5, 0.2), (1.02, 0.66), (1.02, 1.1), (-0.02, 1.1)]), STUFF_D, True, "cyl", lw=1.1)
        for k in range(4):
            w.lines(w.stroke([(0.08 + k * 0.08, 0.22 + k * 0.05), (0.45 + k * 0.1, 0.5 + k * 0.08), (0.9, 0.86 + k * 0.03)], 0.9), STUFF_DD)
        trim_line(w, [(0.02, 0.1), (0.5, 0.22), (1.0, 0.68)], px(w, 2.4), NAVY)
    elif w.rot == "east":
        w.add(w.poly([(-0.02, 0.1), (0.6, 0.34), (1.02, 0.5), (1.02, 1.1), (-0.02, 1.1)]), STUFF_D, True, "cyl", lw=1.1)
        trim_line(w, [(0.0, 0.12), (0.6, 0.36), (1.0, 0.52)], px(w, 2.4), NAVY)
        folds(w, 4, 0.5, 1.0, width=0.8)
    else:
        for k in range(4):
            w.lines(w.stroke([(0.1 + k * 0.08, 0.18), (0.5, 0.5 + k * 0.08), (0.92, 0.7 + k * 0.06)], 0.9), STUFF_DD)
    meander(w, 0.92, 0.99, WHITE, NAVY)


TOCAPU = [CRIMSON, YELLOW, BLACK, WHITE, GREEN, ORANGE]


def tocapu_band(w, v0, v1, cols=8, rows=2):
    hgt = (v1 - v0) / rows
    for r in range(rows):
        for c in range(cols):
            u0, u1 = c / cols, (c + 1) / cols
            a = v0 + r * hgt
            cell = w.band(a, a + hgt) * w.cols(u0, u1)
            col = TOCAPU[(c * 2 + r * 3) % len(TOCAPU)]
            w.add(cell, col, False, "flat", lw=0.6)
            if (c + r) % 2 == 0:
                w.add(w.ell((u0 + u1) / 2, a + hgt / 2 + w.smile((u0 + u1) / 2), 0.025, hgt * 0.22), BLACK if col != BLACK else WHITE, False, "none", line=False)


def unku(w):
    w.base()
    if w.rot == "south":
        w.add(w.poly([(0.28, 0.12), (0.72, 0.12), (0.5, 0.42)]), CRIMSON, False, "flat", lw=1.0)            # stepped yoke
        for k in range(3):
            w.add(w.poly([(0.36 + k * 0.03, 0.12), (0.64 - k * 0.03, 0.12), (0.5, 0.36 - k * 0.07)]), (YELLOW, BLACK, CRIMSON)[k], False, "none", lw=0.6)
    tocapu_band(w, 0.56, 0.7)
    for k in range(9):
        u = (k + 0.5) / 9
        w.lines(w.stroke([(u - 0.05, 0.9), (u, 0.96), (u + 0.05, 0.9)], 1.0, curve=False), BLACK, False)
    folds(w, 4, 0.72, 0.88, width=0.7)


def quilted(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    w.base()
    n = 7
    for i in range(-n, 2 * n):
        u = i / n
        w.lines(w.stroke([(u, 0.0), (u + 0.6, 1.0)], 0.8, curve=False), STUFF_DD)
        w.lines(w.stroke([(u, 0.0), (u - 0.6, 1.0)], 0.8, curve=False), STUFF_DD)
    hem_band(w, 0.88, 0.96, CRIMSON)
    w.add(w.band(0.88, 0.96) * w.cols(0, 2), CRIMSON, False, "cyl", lw=1.0)
    for k in range(8):
        studs(w, [((k + 0.5) / 8, 0.92)], px(w, 1.0), YELLOW, 0.2)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.circle(fu, 0.46, px(w, 6.0)), GOLD, False, "dome", lw=0.9, gloss=0.5)                  # sun disc
        for k in range(8):
            a = k * math.pi / 4
            r = px(w, 6.0) / w.w
            w.add(w.stroke([(fu + r * 1.1 * math.cos(a), 0.46 + r * 1.1 * math.sin(a) * w.w / w.h),
                            (fu + r * 1.5 * math.cos(a), 0.46 + r * 1.5 * math.sin(a) * w.w / w.h)], 1.2, False), GOLD_D, False, "none", line=False)
        w.add(w.circle(fu, 0.46, px(w, 2.4)), GOLD_D, False, "dome", line=False)


def cloak_open(w, gap=0.22, v_open=0.2):
    """A cloak from the front is open down the middle; from behind it covers the back whole."""
    fu = front_u(w)
    if w.rot == "south":
        w.open(w.poly([(0.5 - gap * 0.3, v_open), (0.5 + gap * 0.3, v_open), (0.5 + gap, 1.2), (0.5 - gap, 1.2)], True))
    elif w.rot == "east":
        w.open(w.poly([(fu - 0.04, v_open + 0.05), (1.2, v_open), (1.2, 1.2), (fu + 0.06, 1.2)], True))


def feathercape(w):
    w.extend(grown_body(w.body, w.rot, 3.5) * w.below(0.12, False))
    cloak_open(w, 0.2, 0.24)
    w.base()
    colors = [CRIMSON, YELLOW, "#2a6fb0", ORANGE, TEAL]
    rows = 9
    for r in range(rows):
        v = 0.12 + r * 0.1
        col = colors[r % len(colors)]
        n = 10
        for i in range(-1, n + 1):
            u = (i + (0.5 if r % 2 else 0)) / n
            s = w.smile(u)
            fe = w.poly([(u - 0.05, v + s), (u + 0.05, v + s), (u + 0.045, v + 0.1 + s), (u, v + 0.17 + s), (u - 0.045, v + 0.1 + s)], True)
            w.add(fe, col, False, "flat", lw=0.7)
            w.lines(w.stroke([(u, v + 0.02 + s), (u, v + 0.14 + s)], 0.6, False) * fe, "#3a2a20", False)
    if w.rot == "south":
        studs(w, [(0.38, 0.22), (0.62, 0.22)], px(w, 2.2), GOLD, 0.5)
    elif w.rot == "east":
        studs(w, [(front_u(w) - 0.06, 0.24)], px(w, 2.2), GOLD, 0.5)


def kalasiris(w):
    w.base(LINEN, True)
    folds(w, 9, 0.3, 1.0, width=0.7, sway=0.01)
    if w.rot != "north":
        cu = front_u(w)
        for k, col in enumerate([GOLD, "#2f6fb6", CRIMSON, GOLD, TEAL]):
            r0 = 0.12 + k * 0.045
            m = w.ell(cu, 0.06, 0.42 - k * 0.0, r0 + 0.05) - w.ell(cu, 0.06, 0.42 - k * 0.0, r0)
            w.add(np.clip(m, 0, 1) * w.below(0.12, False), col, False, "flat", line=False)
        w.add(np.clip(w.ell(cu, 0.06, 0.42, 0.36) - w.ell(cu, 0.06, 0.42, 0.35), 0, 1), BLACK, False, "none", line=False)
    belt(w, 0.6, 0.05, CRIMSON)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.04, 0.64), (fu + 0.04, 0.64), (fu + 0.05, 0.9), (fu - 0.05, 0.9)]), CRIMSON, False, "flat", lw=0.8)
        w.add(w.band(0.86, 0.9) * w.cols(fu - 0.05, fu + 0.05), GOLD, False, "none", line=False)


def corselet(w):
    w.G = grown_body(w.body, w.rot, 1.8 + (1.5 if w.body == "Thin" else 0))
    w.G = w.G * (1 - w.below(0.84))
    w.base()
    rows_of_scales(w, 0.08, 0.8, 0.065, size=0.055)
    hem_band(w, 0.78, 0.84, GOLD)
    w.add(w.band(0.78, 0.84), GOLD, False, "cyl", lw=0.8, gloss=0.3)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.05, 0.2), (fu + 0.05, 0.2), (fu + 0.05, 0.78), (fu - 0.05, 0.78)]), "#2f6fb6", False, "flat", lw=0.9)
        for k in range(6):
            w.add(w.band(0.24 + k * 0.09, 0.27 + k * 0.09) * w.cols(fu - 0.05, fu + 0.05), GOLD, False, "none", line=False)


def leopard(w):
    w.G = grown_body(w.body, w.rot, 3.0) * (1 - w.below(0.78))
    cloak_open(w, 0.16, 0.36)
    w.base()
    rng = np.random.RandomState(7 + BODIES.index(w.body) * 3 + ROTS.index(w.rot))
    for _ in range(60):
        u, v = rng.uniform(0, 1), rng.uniform(0.0, 0.78)
        r = rng.uniform(1.4, 2.3)
        ring = np.clip(w.circle(u, v, px(w, r)) - w.circle(u, v, px(w, r * 0.55)), 0, 1)
        w.add(ring * (0.75 + 0.25 * (rng.rand() > 0.5)), "#2a1e14", False, "none", line=False)
        w.add(w.circle(u, v, px(w, r * 0.5)), "#b88a46", True, "none", line=False)
    # the hem: the tails of the hide
    if w.rot == "south":
        for su in (0.18, 0.82):
            m = w.poly([(su - 0.05, 0.6), (su + 0.05, 0.6), (su + 0.03, 0.96), (su, 1.0), (su - 0.03, 0.96)])
            w.extend(m)
            w.add(m, STUFF_D, True, "cyl", lw=0.9)
            w.add(w.circle(su, 0.98, px(w, 1.8)), "#2a1e14", False, "dome", line=False)
        studs(w, [(0.42, 0.34), (0.58, 0.34)], px(w, 2.4), GOLD, 0.5)
    elif w.rot == "east":
        studs(w, [(front_u(w) - 0.08, 0.36)], px(w, 2.4), GOLD, 0.5)


def byrnie(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    w.extend(w.poly([(0.0, 0.7), (1.0, 0.7), (1.03, 1.06), (-0.03, 1.06)], True) * grown_body(w.body, w.rot, 3))
    w.base(gloss=0.15)
    mail(w, 0.0, 1.2)
    belt(w, 0.6, 0.06, LEATHER, BRONZE)
    if w.rot != "east":
        w.lines(w.stroke([(0.5, 0.86), (0.5, 1.08)], 1.2), "#1c1a19", False)                                   # riding slit
    hem_band(w, 0.97, 1.02, BRONZE)
    w.add(w.band(0.97, 1.06), STUFF_D, True, "cyl", lw=0.8)


def fur_edge(w, v0, v1, color=STUFF_D, stuff=True):
    w.add(w.band(v0, v1), color, stuff, "cyl", line=False)
    n = 22
    for i in range(n):
        u = (i + 0.5) / n
        w.lines(w.stroke([(u, v0 + 0.01 + w.smile(u)), (u + 0.015, v1 - 0.01 + w.smile(u))], 0.8, False), STUFF_DD, stuff)
    for i in range(n):
        u = (i + 0.5) / n
        w.add(w.poly([(u - 0.03, v1 + w.smile(u) - 0.01), (u + 0.03, v1 + w.smile(u) - 0.01), (u, v1 + 0.035 + w.smile(u))]), color, stuff, "none", line=False)


def furcloak(w):
    w.extend(grown_body(w.body, w.rot, 3.5) * w.below(0.05, False))
    cloak_open(w, 0.16, 0.42)
    w.base()
    folds(w, 6, 0.42, 1.05, width=0.9)
    fur_edge(w, 0.0, 0.34, "#d6d0c4", True)
    if w.rot == "south":
        w.add(w.circle(0.7, 0.34, px(w, 4.2)), BRONZE, False, "dome", lw=0.9, gloss=0.5)                 # ring brooch
        w.add(w.circle(0.7, 0.34, px(w, 2.2)), STUFF_DD, True, "dome", line=False)
        w.add(w.stroke([(0.64, 0.4), (0.78, 0.28)], 1.2, False), BRONZE, False, "none", line=False)
    elif w.rot == "east":
        w.add(w.circle(front_u(w) - 0.08, 0.36, px(w, 4.2)), BRONZE, False, "dome", lw=0.9, gloss=0.5)
    hem_band(w, 0.97, 1.03, STUFF_DD, True)


def woven(w, v0, v1, c1, c2):
    w.add(w.band(v0, v1), c1, False, "cyl", lw=0.8)
    n = 14
    hgt = v1 - v0
    for i in range(n):
        u = (i + 0.5) / n
        w.add(w.poly([(u - 0.03, v0 + hgt * 0.5 + w.smile(u)), (u, v0 + hgt * 0.15 + w.smile(u)), (u + 0.03, v0 + hgt * 0.5 + w.smile(u)),
                      (u, v0 + hgt * 0.85 + w.smile(u))]), c2, False, "none", line=False)


def nordtunic(w):
    w.base()
    folds(w, 6, 0.3, 1.0, width=0.8)
    woven(w, 0.88, 0.96, CRIMSON, YELLOW)
    if w.rot == "south":
        w.add(w.poly([(0.38, 0.1), (0.62, 0.1), (0.56, 0.34), (0.44, 0.34)]), CRIMSON, False, "flat", lw=0.9)
    belt(w, 0.6, 0.05, LEATHER, BRONZE)


def kaftan(w):
    w.extend(w.poly([(-0.02, 0.6), (1.02, 0.6), (1.06, 1.08), (-0.06, 1.08)], True) * grown_body(w.body, w.rot, 4))
    w.base()
    fu = front_u(w)
    if w.rot == "south":
        trim_line(w, [(0.28, 0.1), (0.42, 0.42), (0.7, 0.62), (0.64, 1.06)], px(w, 3.2), GOLD, gloss=0.25)
        for k in range(5):
            studs(w, [(0.4 + k * 0.07, 0.4 + k * 0.045)], px(w, 0.9), CRIMSON, 0.2)
    elif w.rot == "east":
        trim_line(w, [(fu - 0.08, 0.12), (fu + 0.06, 0.5), (fu + 0.04, 1.06)], px(w, 3.2), GOLD, gloss=0.25)
    else:
        w.lines(w.stroke([(0.5, 0.66), (0.5, 1.08)], 1.1), STUFF_DD)
    belt(w, 0.6, 0.06, CRIMSON, GOLD)
    hem_band(w, 0.98, 1.06, GOLD)
    folds(w, 5, 0.68, 1.0, width=0.8)


def scalecoat(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    w.extend(w.poly([(-0.02, 0.66), (1.02, 0.66), (1.04, 1.04), (-0.04, 1.04)], True) * grown_body(w.body, w.rot, 3))
    w.base(gloss=0.2)
    rows_of_scales(w, 0.06, 1.04, 0.06, size=0.05)
    belt(w, 0.58, 0.06, CRIMSON, GOLD)
    w.add(w.band(0.97, 1.05), GOLD, False, "cyl", lw=0.8, gloss=0.3)
    if w.rot != "east":
        w.lines(w.stroke([(0.5, 0.82), (0.5, 1.05)], 1.2), "#1c1a19", False)


def candys(w):
    w.extend(w.poly([(-0.06, 0.5), (1.06, 0.5), (1.1, 1.08), (-0.1, 1.08)], True) * grown_body(w.body, w.rot, 5))
    w.base()
    for k in range(9):
        u = 0.06 + k * 0.11
        w.lines(w.stroke([(0.5 + (u - 0.5) * 0.5, 0.56), (u, 0.8), (u + (u - 0.5) * 0.15, 1.06)], 0.9), STUFF_DD)
    belt(w, 0.5, 0.05, GOLD, GOLD)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.06, 0.14), (fu + 0.06, 0.14), (fu + 0.04, 0.5), (fu - 0.04, 0.5)]), PURPLE, False, "flat", lw=0.8)
        for k in range(4):
            studs(w, [(fu, 0.22 + k * 0.08)], px(w, 1.0), GOLD, 0.3)
    hem_band(w, 0.99, 1.07, PURPLE)


def lorica(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    strips(w, 0.74, 0.94, 9, LEATHER, False)
    hoops = 6
    v0, v1 = 0.28, 0.74
    hgt = (v1 - v0) / hoops
    for r in range(hoops):
        a = v0 + r * hgt
        w.add(w.band(a, a + hgt + 0.012), STUFF if r % 2 == 0 else STUFF_D, True, "cyl", lw=1.0, gloss=0.25)
    w.add((1 - w.below(v0)) * w.G, STUFF, True, "cyl", lw=1.0, gloss=0.25)                     # breast plates
    shoulder_pads(w, 0.2, 0.16, 0.14, STUFF, True, rows=3)
    if w.rot == "south":
        w.lines(w.stroke([(0.5, v0 - 0.12), (0.5, v1)], 1.1, False), "#1c1a19", False)
        for r in range(hoops):
            studs(w, [(0.44, v0 + (r + 0.5) * hgt + w.smile(0.44)), (0.56, v0 + (r + 0.5) * hgt + w.smile(0.56))], px(w, 1.0), BRONZE, 0.4)
        studs(w, [(0.4, 0.22), (0.6, 0.22)], px(w, 1.5), BRONZE, 0.5)
    elif w.rot == "north":
        w.lines(w.stroke([(0.5, v0 - 0.15), (0.5, v1)], 1.1, False), "#1c1a19", False)
        studs(w, [(0.4, 0.2), (0.6, 0.2)], px(w, 1.3), BRONZE, 0.4)
    else:
        studs(w, [(front_u(w) + 0.02, v0 + (r + 0.5) * hgt) for r in range(hoops)], px(w, 1.0), BRONZE, 0.4)


def tunica(w):
    w.base()
    for cu in ((0.32, 0.68) if w.rot != "east" else (0.62,)):
        w.add(w.poly([(cu - 0.04, 0.0), (cu + 0.04, 0.0), (cu + 0.045, 1.02), (cu - 0.045, 1.02)]), CRIMSON, False, "flat", lw=0.7)
    folds(w, 6, 0.6, 1.0, width=0.8)
    trim_line(w, [(0.04, 0.6), (0.5, 0.6 + w.smile(0.5)), (0.96, 0.6)], px(w, 1.8), "#b8955a")


def toga(w):
    w.extend(w.poly([(-0.04, 0.5), (1.04, 0.5), (1.06, 1.08), (-0.06, 1.08)], True) * grown_body(w.body, w.rot, 4))
    w.base(LINEN, True)
    if w.rot == "south":
        w.add(w.poly([(-0.04, 0.02), (0.36, 0.24), (0.98, 0.56), (1.06, 0.62), (1.06, 1.1), (-0.06, 1.1)], True), "#dcd4bd", True, "cyl", lw=1.0)
        trim_line(w, [(0.0, 0.04), (0.36, 0.26), (1.0, 0.6)], px(w, 3.0), PURPLE)
        for k in range(4):
            w.lines(w.stroke([(0.05 + k * 0.06, 0.2 + k * 0.08), (0.5 + k * 0.05, 0.52 + k * 0.08), (0.96, 0.78 + k * 0.06)], 0.9), STUFF_DD)
    elif w.rot == "east":
        w.add(w.poly([(-0.06, 0.1), (0.5, 0.36), (1.06, 0.46), (1.06, 1.1), (-0.06, 1.1)], True), "#dcd4bd", True, "cyl", lw=1.0)
        trim_line(w, [(0.0, 0.12), (0.5, 0.38), (1.0, 0.48)], px(w, 3.0), PURPLE)
        folds(w, 4, 0.5, 1.02, width=0.8)
    else:
        for k in range(4):
            w.lines(w.stroke([(0.06 + k * 0.08, 0.16), (0.5, 0.48 + k * 0.08), (0.94, 0.66 + k * 0.08)], 0.9), STUFF_DD)
    hem_band(w, 0.99, 1.07, PURPLE)


def lamellar(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    w.extend(w.poly([(-0.02, 0.7), (1.02, 0.7), (1.05, 1.06), (-0.05, 1.06)], True) * grown_body(w.body, w.rot, 3))
    lamellae(w, 0.0, 1.06, 9, CRIMSON)
    shoulder_pads(w, 0.2, 0.15, 0.13, STUFF, True, rows=2, edge=CRIMSON)
    belt(w, 0.6, 0.05, CRIMSON, GOLD)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.circle(fu, 0.42, px(w, 5.6)), "#e8eef2", False, "dome", lw=0.9, gloss=0.7)            # breast mirror
        w.add(np.clip(w.circle(fu, 0.42, px(w, 5.6)) - w.circle(fu, 0.42, px(w, 4.4)), 0, 1), GOLD, False, "none", line=False)
    else:
        w.add(w.circle(0.5, 0.42, px(w, 4.4)), "#e8eef2", False, "dome", lw=0.9, gloss=0.6)
    if w.rot != "east":
        w.lines(w.stroke([(0.5, 0.66), (0.5, 1.07)], 1.2), "#1c1a19", False)


def hanfu(w):
    w.extend(w.poly([(-0.06, 0.52), (1.06, 0.52), (1.1, 1.08), (-0.1, 1.08)], True) * grown_body(w.body, w.rot, 5))
    w.base()
    wrap_front(w, BLACK, 2.6, over="right", v_end=0.56)
    w.add(w.band(0.52, 0.62), BLACK, False, "cyl", lw=0.9)                                            # broad sash
    belt(w, 0.555, 0.02, CRIMSON)
    if w.rot != "north":
        fu = front_u(w)
        w.add(w.poly([(fu - 0.02, 0.6), (fu + 0.03, 0.6), (fu + 0.05, 0.94), (fu - 0.01, 0.94)]), CRIMSON, False, "flat", lw=0.7)
        w.add(w.circle(fu + 0.02, 0.97, px(w, 1.8)), "#4caf7a", False, "dome", lw=0.6, gloss=0.4)        # jade
    folds(w, 6, 0.64, 1.04, width=0.8)
    hem_band(w, 1.0, 1.08, BLACK)


def dragonrobe(w):
    w.extend(w.poly([(-0.06, 0.52), (1.06, 0.52), (1.1, 1.08), (-0.1, 1.08)], True) * grown_body(w.body, w.rot, 5))
    w.base()
    # lishui: diagonal waves and stripes at the hem
    for k, col in enumerate([NAVY, WHITE, TEAL, WHITE, NAVY]):
        a = 0.84 + k * 0.045
        for i in range(10):
            u = i / 9
            w.add(w.stroke([(u - 0.08, a + 0.05), (u, a), (u + 0.08, a + 0.05)], 2.2, False) * w.below(0.84), col, False, "none", line=False)
    hem_band(w, 1.02, 1.08, NAVY)
    belt(w, 0.52, 0.04, GOLD, GOLD)
    if w.rot != "east":
        cu = 0.5
        w.add(w.circle(cu, 0.32, px(w, 8.0)), NAVY, False, "dome", lw=0.9)                            # roundel
        r = px(w, 8.0) / w.w
        pts = [(cu + r * 0.6 * math.cos(t) * (1 - t / 9), 0.32 + r * 0.6 * math.sin(t) * (1 - t / 9) * w.w / w.h) for t in np.linspace(0, 7, 18)]
        w.add(w.stroke(pts, px(w, 2.0)), GOLD, False, "flat", lw=0.5, gloss=0.4)                  # coiled dragon
        w.add(w.circle(cu + r * 0.55, 0.32, px(w, 1.3)), CRIMSON, False, "none", line=False)
        for su in (0.18, 0.82):
            w.add(w.stroke([(su - 0.06, 0.68), (su, 0.62), (su + 0.05, 0.7), (su - 0.02, 0.76)], px(w, 1.8)), GOLD, False, "flat", lw=0.5)
    else:
        w.add(w.circle(0.66, 0.34, px(w, 7.0)), NAVY, False, "dome", lw=0.9)
        w.add(w.stroke([(0.62, 0.3), (0.7, 0.32), (0.64, 0.38), (0.7, 0.4)], px(w, 1.8)), GOLD, False, "flat", lw=0.5)


def domaru(w):
    w.G = grown_body(w.body, w.rot, 2.0 + (1.5 if w.body == "Thin" else 0))
    w.G = w.G * (1 - w.below(0.66)) + w.below(0.66) * w.G
    # the tassets: overlapping skirts of laced lames, each a little wider than the one above
    v0, v1 = 0.62, 1.04
    w.extend(w.poly([(-0.03, v0), (1.03, v0), (1.07, v1 + 0.02), (-0.07, v1 + 0.02)], True) * grown_body(w.body, w.rot, 3))
    n = 4 if w.rot != "east" else 3
    for i in range(n):
        u0, u1 = i / n - 0.03, (i + 1) / n + 0.03
        panel = w.poly([(u0 + 0.02, v0), (u1 - 0.02, v0), (u1 + 0.01, v1), (u0 - 0.01, v1)])
        w.add(panel, STUFF if i % 2 == 0 else STUFF_D, True, "cyl", lw=1.0, gloss=0.2)
        for r in range(1, 4):
            a = v0 + r * (v1 - v0) / 4
            w.add(w.band(a - 0.012, a + 0.012, False) * panel, "#2a4a9a", False, "none", line=False)
            w.lines(w.band(a + 0.012, a + 0.022, False) * panel, STUFF_DD)
    lamellae(w, 0.0, 0.62, 6, "#2a4a9a", plate=STUFF)
    belt(w, 0.6, 0.06, "#2a4a9a")
    shoulder_pads(w, 0.24, 0.17, 0.17, STUFF, True, rows=3, edge="#2a4a9a")
    if w.rot == "south":
        w.add(w.poly([(0.34, 0.08), (0.66, 0.08), (0.62, 0.28), (0.38, 0.28)]), "#7a1c1c", False, "flat", lw=0.9)  # leather breast
        studs(w, [(0.5, 0.18)], px(w, 1.6), GOLD, 0.4)


def kimono(w):
    w.extend(w.poly([(-0.04, 0.52), (1.04, 0.52), (1.06, 1.08), (-0.06, 1.08)], True) * grown_body(w.body, w.rot, 4))
    w.base()
    for k in range(5):
        for j in range(7):
            u, v = (j + 0.5 * (k % 2)) / 6, 0.7 + k * 0.08
            w.lines(w.poly([(u, v - 0.025), (u + 0.025, v), (u, v + 0.025), (u - 0.025, v)]) * w.below(0.66), STUFF_D, True)
    wrap_front(w, NAVY, 3.2, over="left", v_end=0.58)
    w.add(w.band(0.5, 0.64), CRIMSON, False, "cyl", lw=0.9)                                           # obi
    w.add(w.band(0.555, 0.585), GOLD, False, "none", line=False)
    if w.rot == "north":
        w.add(w.poly([(0.32, 0.44), (0.68, 0.44), (0.62, 0.7), (0.38, 0.7)], True), CRIMSON, False, "cyl", lw=0.9)  # obi knot
    folds(w, 5, 0.66, 1.04, width=0.8)
    if w.rot == "north":
        w.add(w.circle(0.5, 0.26, px(w, 3.0)), WHITE, False, "flat", lw=0.8)                                       # family crest
        w.add(w.circle(0.5, 0.26, px(w, 1.3)), NAVY, False, "none", line=False)
    hem_band(w, 1.0, 1.08, NAVY)


def kamishimo(w):
    """The kataginu: a stiff-shouldered vest that narrows into the pleated hakama, over a light kimono."""
    if w.rot == "south":
        vest = w.poly([(-0.15, 0.18), (1.15, 0.18), (1.12, 0.3), (0.64, 0.6), (0.36, 0.6), (-0.12, 0.3)])
    elif w.rot == "north":
        vest = w.poly([(-0.15, 0.18), (1.15, 0.18), (1.1, 0.32), (1.0, 0.58), (0.0, 0.58), (-0.1, 0.32)])
    else:
        vest = w.poly([(0.1, 0.16), (0.9, 0.16), (0.86, 0.3), (0.82, 0.6), (0.3, 0.6), (0.14, 0.3)])
    w.extend(vest * w.band(0, 0.34, False))
    w.extend(w.poly([(-0.06, 0.52), (1.06, 0.52), (1.12, 1.08), (-0.12, 1.08)], True) * grown_body(w.body, w.rot, 5))
    w.add(w.G.copy() * (1 - w.below(0.58, False)), "#dcd6c8", False, "cyl", line=False)                       # the kimono beneath
    hak = w.G.copy() * w.below(0.56, False)
    w.add(hak, STUFF, True, "cyl", lw=1.0)
    for k in range(8):
        u = 0.05 + k * 0.128
        w.lines(w.stroke([(0.5 + (u - 0.5) * 0.8, 0.6), (u + (u - 0.5) * 0.12, 1.06)], 1.0, False), STUFF_DD)        # hakama pleats
    w.add(w.band(0.55, 0.61, False), STUFF_DD, True, "cyl", lw=0.9)
    w.add(vest, STUFF_D, True, "cyl", lw=1.1)
    w.lines(w.stroke([(-0.12, 0.2), (0.5, 0.21), (1.12, 0.2)], 1.0), STUFF_DD)                                  # the stiff fold
    if w.rot == "south":
        for cu in (0.2, 0.8):
            w.add(w.circle(cu, 0.3, px(w, 2.6)), WHITE, False, "flat", lw=0.8)                                   # mon
            w.add(w.circle(cu, 0.3, px(w, 1.1)), STUFF_DD, True, "none", line=False)
    elif w.rot == "north":
        w.add(w.circle(0.5, 0.3, px(w, 2.8)), WHITE, False, "flat", lw=0.8)
        w.add(w.circle(0.5, 0.3, px(w, 1.2)), STUFF_DD, True, "none", line=False)


# layer thickness: OnSkin hugs the body, Middle sits a little out, Shell clothes the rest
GARMENTS = {
    "HE_Albion_Redcoat": (redcoat, 2.0, 2.0), "HE_Albion_FrockCoat": (frockcoat, 3.0, 3.0),
    "HE_Hellas_Linothorax": (linothorax, 2.0, 1.5), "HE_Hellas_Chiton": (chiton, 0.0, 0.0), "HE_Hellas_Himation": (himation, 3.5, 4.0),
    "HE_Inti_Unku": (unku, 0.0, 0.0), "HE_Inti_QuiltedTunic": (quilted, 2.0, 1.5), "HE_Inti_FeatherCape": (feathercape, 3.0, 3.0),
    "HE_Kemet_Kalasiris": (kalasiris, 0.0, 0.0), "HE_Kemet_Corselet": (corselet, 1.8, 1.5), "HE_Kemet_LeopardMantle": (leopard, 3.0, 3.0),
    "HE_Nord_Byrnie": (byrnie, 2.0, 1.5), "HE_Nord_FurCloak": (furcloak, 3.5, 4.0), "HE_Nord_Tunic": (nordtunic, 0.0, 0.0),
    "HE_Pars_Kaftan": (kaftan, 3.0, 3.0), "HE_Pars_ScaleCoat": (scalecoat, 2.0, 1.5), "HE_Pars_Candys": (candys, 3.5, 4.0),
    "HE_Roma_Lorica": (lorica, 2.0, 1.5), "HE_Roma_Tunica": (tunica, 0.0, 0.0), "HE_Roma_Toga": (toga, 3.5, 4.0),
    "HE_Tianxia_Lamellar": (lamellar, 2.0, 1.5), "HE_Tianxia_Hanfu": (hanfu, 3.5, 4.0), "HE_Tianxia_DragonRobe": (dragonrobe, 3.5, 4.0),
    "HE_Yamato_Domaru": (domaru, 2.0, 1.5), "HE_Yamato_Kimono": (kimono, 3.0, 4.0), "HE_Yamato_Kamishimo": (kamishimo, 3.0, 4.0),
}
_cache = {}


def draw(kind, body, rot):
    key = (kind, body, rot)
    if key not in _cache:
        fn, g, thin = GARMENTS[kind]
        w = Wear(body, rot, g, thin)
        fn(w)
        _cache[key] = w.render()
    return _cache[key]


@painter
def heirs_body(kind, body, rot, mask=False):
    img, m = draw(kind, body, rot)
    return m if mask else img
