"""Heirs of Earth 3.6: worn headgear. Every heir hat and helmet gets its own worn graphic, drawn on the vanilla head frame
(128 px, head roughly x 41-87, y 39-89, eyes at y 70) in the vanilla manner: a bold dark outline, soft rounded shading.
Parts made of the item's stuff are painted in neutral greys and marked in a _m mask (red), so CutoutComplex tints them with
the stuff colour while the fixed parts (plumes, gold, lacquer, cords) keep their own colours."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from heirs_art import painter

K = 4                      # supersampling
S = 128 * K
OUTLINE = 3.0              # px at 128
INNER = 1.4
INK = (24, 22, 22)

YY, XX = np.mgrid[0:S, 0:S].astype(np.float32) / K


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


STUFF = "#e4e4e4"
STUFF_D = "#c4c4c4"
STUFF_DD = "#a2a2a2"
GOLD = "#e0b440"
GOLD_D = "#b8862a"
RED = "#b4282a"
RED_D = "#80181c"


def catmull(pts, n=10, closed=True):
    """A smooth closed curve through the points."""
    out = []
    m = len(pts)
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0, p1, p2, p3 = pts[(i - 1) % m], pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
        if not closed:
            p0 = pts[max(i - 1, 0)]
            p3 = pts[min(i + 2, m - 1)]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed:
        out.append(pts[-1])
    return out


def arcpts(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in np.linspace(a0, a1, n)]


def dome(cx, yb, rx, top, sag=2.0, skew=0.0):
    """The upper half of an egg from (cx-rx, yb) over `top` to (cx+rx, yb), with a slightly sagging lower edge."""
    up = [(cx + skew * math.sin(math.radians(a)) + rx * math.cos(math.radians(a)), yb - (yb - top) * math.sin(math.radians(a)))
          for a in np.linspace(0, 180, 30)]
    low = [(cx - rx + 2 * rx * t, yb + sag * math.sin(math.pi * t)) for t in np.linspace(0, 1, 12)]
    return up + low


class Hat:
    def __init__(self, outline=OUTLINE):
        self.parts = []
        self.outline = outline

    def add(self, shape, color, stuff=False, shade="dome", line=True, gloss=0.0, lw=INNER, light=(0.32, 0.22)):
        self.parts.append((shape, color, stuff, shade, line, gloss, lw, light))
        return self

    # shapes
    @staticmethod
    def _mask(shape):
        img = Image.new("L", (S, S), 0)
        d = ImageDraw.Draw(img)
        kind = shape[0]
        if kind == "poly":
            d.polygon([(x * K, y * K) for x, y in shape[1]], fill=255)
        elif kind == "curve":
            d.polygon([(x * K, y * K) for x, y in catmull(shape[1])], fill=255)
        elif kind == "ell":
            _, cx, cy, rx, ry = shape
            d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=255)
        elif kind == "stroke":
            _, pts, w = shape
            pts = catmull(pts, 8, closed=False) if len(pts) > 2 else pts
            d.line([(x * K, y * K) for x, y in pts], fill=255, width=int(w * K), joint="curve")
            for x, y in (pts[0], pts[-1]):
                d.ellipse([(x - w / 2) * K, (y - w / 2) * K, (x + w / 2) * K, (y + w / 2) * K], fill=255)
        elif kind == "multi":
            for sub in shape[1]:
                img = Image.fromarray(np.maximum(np.asarray(img), np.asarray(Hat._mask(sub))))
        return img

    def render(self):
        rgb = np.zeros((S, S, 3), np.float32)
        alpha = np.zeros((S, S), np.float32)
        stuffmap = np.zeros((S, S), np.float32)
        for shape, color, stuff, shade, line, gloss, lw, light in self.parts:
            mimg = self._mask(shape)
            m = np.asarray(mimg, np.float32) / 255.0
            box = mimg.getbbox()
            if not box:
                continue
            x0, y0, x1, y1 = (v / K for v in box)
            u = np.clip((XX - x0) / max(x1 - x0, 1e-3), 0, 1)
            v = np.clip((YY - y0) / max(y1 - y0, 1e-3), 0, 1)
            lx, ly = light
            if shade == "dome":
                f = 1.06 - 0.62 * ((u - lx) ** 2 + 0.8 * (v - ly) ** 2)
            elif shade == "cyl":
                f = 0.70 + 0.36 * np.sin(np.pi * np.clip(u * 0.92 + 0.04, 0, 1)) ** 0.8 - 0.10 * v
            elif shade == "flat":
                f = 1.0 - 0.16 * v
            else:  # "none"
                f = np.ones_like(u)
            # soft darkening toward the part's edge, the vanilla rounded look
            soft = np.asarray(mimg.filter(ImageFilter.GaussianBlur(3.2 * K)), np.float32) / 255.0
            f = f * (0.80 + 0.20 * np.clip(soft * 1.6 - 0.25, 0, 1))
            col = hexrgb(color)[None, None, :] * f[..., None]
            if gloss:
                g = np.exp(-(((u - lx + 0.06) / 0.16) ** 2 + ((v - ly + 0.04) / 0.12) ** 2)) * gloss
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
        # the bold outer outline
        aimg = Image.fromarray((alpha * 255).astype(np.uint8))
        k = int(round(self.outline * K)) * 2 + 1
        outer = np.asarray(aimg.filter(ImageFilter.MaxFilter(k)), np.float32) / 255.0
        outer = np.asarray(Image.fromarray((outer * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(K * 0.35)), np.float32) / 255.0
        final_rgb = rgb * alpha[..., None] + np.array(INK, np.float32) * (1 - alpha[..., None])
        final_a = np.maximum(alpha, outer)
        img = Image.fromarray(np.dstack([final_rgb, final_a * 255]).astype(np.uint8), "RGBA").resize((128, 128), Image.LANCZOS)
        mask = Image.fromarray((stuffmap * alpha * 255).astype(np.uint8)).resize((128, 128), Image.LANCZOS)
        z = Image.new("L", (128, 128), 0)
        return img, Image.merge("RGBA", (mask, z, z, Image.new("L", (128, 128), 255)))


# ------------------------------------------------------------------ pieces shared by several hats
def plume_fan(h, cx, base, n, spread, length, colors, w=5.6, tilt=0.0):
    for i in range(n):
        a = math.radians(-90 + tilt + (i - (n - 1) / 2) * spread)
        tip = (cx + length * math.cos(a), base + length * math.sin(a))
        mid = (cx + 0.55 * length * math.cos(a) + 1.5 * math.sin(a), base + 0.55 * length * math.sin(a))
        h.add(("stroke", [(cx, base), mid, tip], w), colors[i % len(colors)], shade="flat", lw=1.0)


def leaves(h, path, color, color2, stuff, size=4.2, every=1, flip=False, lw=1.0):
    """Paired leaves along a path, pointing along it."""
    for i in range(0, len(path) - 1, every):
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        ang = math.atan2(y1 - y0, x1 - x0)
        for side in (-1, 1):
            a = ang + side * 0.75
            tip = (x0 + size * 1.9 * math.cos(a), y0 + size * 1.9 * math.sin(a))
            nx, ny = -math.sin(a), math.cos(a)
            mid = ((x0 + tip[0]) / 2, (y0 + tip[1]) / 2)
            pts = [(x0, y0), (mid[0] + nx * size * .55, mid[1] + ny * size * .55), tip, (mid[0] - nx * size * .55, mid[1] - ny * size * .55)]
            h.add(("curve", pts), color if (i + side) % 2 else color2, stuff=stuff, shade="flat", lw=lw)


def lames(h, rows, x0, x1, y0, step, color, stuff, flare=0.0, curve=2.0, lacing=None):
    """Overlapping horizontal plates (neck guards, curtains), the lowest drawn first."""
    for r in reversed(range(rows)):
        yt = y0 + r * step
        fl = flare * r
        pts = [(x0 - fl, yt), (x1 + fl, yt), (x1 + fl + 1, yt + step + 2), ((x0 + x1) / 2, yt + step + 2 + curve), (x0 - fl - 1, yt + step + 2)]
        h.add(("curve", pts) if curve else ("poly", pts), color, stuff=stuff, shade="cyl", lw=1.1)
        if lacing:
            for k in range(int((x1 - x0 + 2 * fl) // 7)):
                x = x0 - fl + 4 + k * 7
                h.add(("stroke", [(x, yt + 2), (x, yt + step)], 1.6), lacing, shade="none", line=False)


# ------------------------------------------------------------------ the hats
def shako(h, rot):
    cx = 64 if rot != "east" else 63
    h.add(("poly", [(cx - 22, 62), (cx - 25, 18), (cx + 25, 18), (cx + 22, 62)]), STUFF, True, "cyl")
    h.add(("ell", cx, 18, 25, 5), STUFF_D, True, "flat")
    h.add(("poly", [(cx - 25, 17), (cx + 25, 17), (cx + 25, 23), (cx - 25, 23)]), "#2a2a2e", shade="cyl")          # top band
    h.add(("poly", [(cx - 22, 56), (cx + 22, 56), (cx + 22, 63), (cx - 22, 63)]), "#2a2a2e", shade="cyl")          # lower band
    if rot == "south":
        h.add(("curve", [(cx - 22, 61), (cx, 68), (cx + 22, 61), (cx, 64)]), "#1c1c20", gloss=.5, shade="flat")     # peak
        h.add(("curve", [(cx - 9, 31), (cx + 9, 31), (cx + 10, 43), (cx, 53), (cx - 10, 43)]), GOLD, gloss=.6)      # brass plate
        h.add(("ell", cx, 41, 4, 4), RED, gloss=.4)
        h.add(("ell", cx, 10, 6, 7), "#f2f2ee", shade="dome")                                                       # pompom
        h.add(("ell", cx, 6, 4, 4), RED, shade="dome")
    elif rot == "east":
        h.add(("curve", [(cx + 14, 60), (cx + 33, 66), (cx + 30, 69), (cx + 16, 64)]), "#1c1c20", gloss=.5, shade="flat")
        h.add(("poly", [(cx + 19, 31), (cx + 24, 31), (cx + 23, 51), (cx + 18, 49)]), GOLD, gloss=.5)
        h.add(("ell", cx + 18, 10, 6, 7), "#f2f2ee", shade="dome")
        h.add(("ell", cx + 18, 6, 4, 4), RED, shade="dome")
    else:
        h.add(("ell", cx, 10, 6, 7), "#f2f2ee", shade="dome")


def tophat(h, rot):
    cx = 64 if rot != "east" else 63
    h.add(("curve", [(cx - 32, 59), (cx, 54), (cx + 32, 59), (cx + 30, 64), (cx, 66), (cx - 30, 64)]), STUFF_D, True, "flat")
    h.add(("poly", [(cx - 19, 60), (cx - 20, 12), (cx + 20, 12), (cx + 19, 60)]), STUFF, True, "cyl", gloss=.15)
    h.add(("ell", cx, 12, 20, 4), STUFF_D, True, "flat")
    h.add(("poly", [(cx - 19.5, 48), (cx + 19.5, 48), (cx + 19, 58), (cx - 19, 58)]), "#26262a", shade="cyl")
    if rot == "south":
        h.add(("poly", [(cx + 8, 49), (cx + 14, 49), (cx + 14, 57), (cx + 8, 57)]), GOLD, gloss=.5, lw=1.0)       # buckle


def bicorne(h, rot):
    if rot in ("south", "north"):
        body = [(22, 58), (34, 42), (50, 30), (64, 27), (78, 30), (94, 42), (106, 58), (96, 63), (64, 60), (32, 63)]
        h.add(("curve", body), STUFF_D if rot == "north" else STUFF, True, "dome", light=(.5, .25))
        trim = [(22, 58), (34, 42), (50, 30), (64, 27), (78, 30), (94, 42), (106, 58)]
        h.add(("stroke", trim, 2.6), GOLD, shade="none", lw=0.8)
        if rot == "south":
            h.add(("ell", 64, 44, 7.5, 7.5), "#1e3a7a", shade="dome")                                               # cockade
            h.add(("ell", 64, 44, 4.6, 4.6), "#f0f0ea", shade="dome", lw=1.0)
            h.add(("ell", 64, 44, 2.2, 2.2), RED, shade="none", line=False)
            h.add(("stroke", [(64, 36), (64, 56)], 1.8), GOLD, shade="none", line=False)
    else:
        h.add(("curve", [(38, 62), (40, 44), (52, 26), (62, 20), (72, 26), (84, 44), (88, 62), (63, 58)]), STUFF, True, "dome")
        h.add(("stroke", [(40, 52), (46, 36), (56, 24), (62, 21), (70, 24), (80, 36), (86, 52)], 2.4), GOLD, shade="none", lw=.8)
        h.add(("curve", [(40, 58), (63, 54), (88, 58), (86, 66), (63, 63), (42, 66)]), STUFF_DD, True, "cyl")


def corinthian(h, rot):
    hair, hair2 = "#a5242a", "#2a1c18"
    if rot == "south":
        # the crest seen end-on: a tall narrow fan
        h.add(("curve", [(58, 32), (57, 12), (64, 4), (71, 12), (70, 32)]), hair, shade="cyl")
        for x in (60, 64, 68):
            h.add(("stroke", [(x, 30), (x + (x - 64) * .2, 9)], 1.0), hair2, shade="none", line=False)
        helm = [(38, 64), (39, 44), (48, 32), (64, 28), (80, 32), (89, 44), (90, 64), (89, 84), (84, 96), (74, 96), (71, 82), (57, 82),
                (54, 96), (44, 96), (39, 84)]
        h.add(("curve", helm), STUFF, True, "dome", gloss=.25)
        h.add(("curve", [(45, 64), (52, 62), (61, 64), (61, 70), (54, 74), (46, 72)]), "#141214", shade="none")         # eyes
        h.add(("curve", [(83, 64), (76, 62), (67, 64), (67, 70), (74, 74), (82, 72)]), "#141214", shade="none")
        h.add(("poly", [(61, 62), (67, 62), (66.5, 84), (64, 88), (61.5, 84)]), STUFF_D, True, "cyl")                   # nasal
        h.add(("stroke", [(42, 54), (52, 50), (63, 52)], 1.4), STUFF_DD, True, "none", line=False)
        h.add(("stroke", [(86, 54), (76, 50), (65, 52)], 1.4), STUFF_DD, True, "none", line=False)
    elif rot == "east":
        fan = [(40, 34)] + arcpts(62, 42, 30, 34, 200, 340, 14) + [(86, 34), (78, 34), (62, 30), (46, 34)]
        h.add(("curve", fan), hair, shade="dome", light=(.4, .2))
        for k in range(7):
            a = math.radians(205 + k * 21)
            h.add(("stroke", [(62 + 15 * math.cos(a), 40 + 15 * math.sin(a)), (62 + 28 * math.cos(a), 42 + 31 * math.sin(a))], 1.0), hair2,
                  shade="none", line=False)
        h.add(("poly", [(58, 36), (66, 36), (66, 31), (58, 31)]), STUFF_D, True, "flat")
        helm = [(34, 72), (34, 52), (42, 38), (60, 31), (78, 35), (88, 48), (91, 62), (90, 74), (93, 86), (88, 96), (78, 96), (76, 84),
                (66, 80), (52, 86), (40, 90)]
        h.add(("curve", helm), STUFF, True, "dome", gloss=.25, light=(.55, .25))
        h.add(("curve", [(76, 64), (90, 63), (90, 70), (80, 72)]), "#141214", shade="none")
        h.add(("curve", [(34, 74), (40, 84), (36, 92), (30, 88)]), STUFF_D, True, "flat")                              # neck flare
        h.add(("stroke", [(42, 54), (60, 48), (84, 52)], 1.4), STUFF_DD, True, "none", line=False)
    else:
        h.add(("curve", [(58, 32), (57, 12), (64, 4), (71, 12), (70, 32)]), hair, shade="cyl")
        h.add(("curve", [(37, 70), (38, 46), (48, 32), (64, 28), (80, 32), (90, 46), (91, 70), (96, 84), (64, 80), (32, 84)]), STUFF, True, "dome")


def wreath(h, rot, stuff):
    col, col2 = (STUFF, STUFF_D) if stuff else ("#7d8c3c", "#5e6e2a")
    if rot == "south":
        for side in (-1, 1):
            path = [(64 + side * 23, 47), (64 + side * 18, 51), (64 + side * 11, 53.5), (64 + side * 3, 54.5)]
            h.add(("stroke", path, 2.0), "#6a5a30" if not stuff else STUFF_DD, stuff, "none", line=False)
            leaves(h, path, col, col2, stuff, size=5.2 if not stuff else 5.8)
        if not stuff:
            for x, y in ((52, 52), (76, 52)):
                h.add(("ell", x, y, 1.8, 1.8), "#3e3a52", shade="dome", line=False)                                     # olives
    elif rot == "east":
        path = [(38, 52), (46, 49), (56, 47), (66, 47), (76, 49), (85, 52)]
        h.add(("stroke", path, 2.0), "#6a5a30" if not stuff else STUFF_DD, stuff, "none", line=False)
        leaves(h, path, col, col2, stuff, size=5.2 if not stuff else 5.8)
        h.add(("stroke", [(38, 53), (33, 62), (35, 70)], 3.4), RED if stuff else "#e8e0c8", shade="none", lw=.8)        # ribbon
        if not stuff:
            h.add(("ell", 60, 46, 1.8, 1.8), "#3e3a52", shade="dome", line=False)
    else:
        for side in (-1, 1):
            path = [(64 + side * 2, 56), (64 + side * 9, 54), (64 + side * 17, 53), (64 + side * 24, 55)]
            h.add(("stroke", path, 2.0), "#6a5a30" if not stuff else STUFF_DD, stuff, "none", line=False)
            leaves(h, path, col, col2, stuff, size=5.2 if not stuff else 5.8)
        ribbon = RED if stuff else "#e8e0c8"
        h.add(("stroke", [(62, 56), (58, 66), (56, 76)], 3.4), ribbon, shade="none", lw=.8)
        h.add(("stroke", [(66, 56), (70, 66), (73, 75)], 3.4), ribbon, shade="none", lw=.8)
        h.add(("ell", 64, 56, 3, 2.4), ribbon, shade="dome", lw=.8)


def plumed(h, rot):
    feathers = ["#c8302a", "#e8b430", "#2e8a4a", "#e8b430"]
    cx = 64 if rot != "east" else 62
    if rot == "east":
        plume_fan(h, cx + 10, 34, 5, 15, 26, feathers, tilt=-28)
    else:
        plume_fan(h, cx, 34, 6, 20, 26, feathers)
    h.add(("poly", dome(cx, 64, 25, 32)), STUFF, True, "dome", gloss=.3)
    h.add(("stroke", [(cx - 25, 60), (cx, 63), (cx + 25, 60)], 3.0), STUFF_D, True, "cyl", lw=.9)
    if rot == "south":
        h.add(("ell", cx, 47, 7, 7), GOLD, shade="dome", gloss=.6)                                                     # sun disc
        for k in range(12):
            a = math.radians(k * 30)
            h.add(("stroke", [(cx + 8 * math.cos(a), 47 + 8 * math.sin(a)), (cx + 11 * math.cos(a), 47 + 11 * math.sin(a))], 1.6), GOLD,
                  shade="none", line=False)
        h.add(("ell", cx, 47, 2.4, 2.4), GOLD_D, shade="none", line=False)
    elif rot == "east":
        h.add(("ell", cx + 21, 48, 3, 6), GOLD, shade="dome", gloss=.5)


def mascaypacha(h, rot):
    band = 50
    if rot == "south":
        for k, x in enumerate((58, 64, 70)):
            plume_fan(h, x, 46, 1, 0, 22, ["#2a2a2a" if k != 1 else "#f0ece0"], w=4.6, tilt=(k - 1) * 12)
        h.add(("curve", [(41, band - 4), (64, band), (87, band - 4), (87, band + 4), (64, band + 7), (41, band + 4)]), STUFF, True, "cyl")
        for x in range(44, 86, 5):
            h.add(("stroke", [(x, band - 3 + (1 - abs(x - 64) / 23) * 4), (x + 3, band + 3 + (1 - abs(x - 64) / 23) * 4)], 1.3), STUFF_DD, True, "none", line=False)          # braid
        for k in range(8):                                                                                           # the red fringe
            x = 52 + k * 3.4
            h.add(("stroke", [(x, band + 6), (x + .3, band + 17)], 3.0), RED if k % 2 else "#c8342e", shade="cyl", lw=.7)
        h.add(("curve", [(50, band + 4), (64, band + 6), (79, band + 4), (79, band + 8), (64, band + 9.5), (50, band + 8)]), GOLD, shade="flat", lw=.8)
    elif rot == "east":
        plume_fan(h, 70, 46, 2, 14, 22, ["#2a2a2a", "#f0ece0"], w=4.6, tilt=-6)
        h.add(("curve", [(38, band - 2), (64, band - 6), (88, band - 3), (88, band + 5), (64, band + 2), (38, band + 7)]), STUFF, True, "cyl")
        for x in range(41, 86, 5):
            h.add(("stroke", [(x, band - 3), (x + 3, band + 4)], 1.3), STUFF_DD, True, "none", line=False)
        for k in range(3):
            x = 83 + k * 2.6
            h.add(("stroke", [(x, band + 2), (x + .5, band + 14)], 3.0), RED if k % 2 else "#c8342e", shade="cyl", lw=.7)
    else:
        for k, x in enumerate((58, 64, 70)):
            plume_fan(h, x, 46, 1, 0, 22, ["#2a2a2a" if k != 1 else "#f0ece0"], w=4.6, tilt=(k - 1) * 12)
        h.add(("curve", [(39, band - 1), (64, band - 3), (89, band - 1), (89, band + 7), (64, band + 6), (39, band + 7)]), STUFF, True, "cyl")
        for x in range(42, 88, 5):
            h.add(("stroke", [(x, band - 1), (x + 3, band + 6)], 1.3), STUFF_DD, True, "none", line=False)


def khepresh(h, rot):
    if rot == "east":
        body = [(40, 64), (34, 44), (30, 24), (40, 12), (58, 10), (74, 18), (82, 34), (86, 52), (88, 64), (64, 66)]
        cx = 60
    else:
        body = [(42, 64), (37, 42), (36, 24), (46, 12), (64, 8), (82, 12), (92, 24), (91, 42), (86, 64), (64, 66)]
        cx = 64
    h.add(("curve", body), STUFF, True, "dome", light=(.4, .2), gloss=.15)
    rng = np.random.default_rng(7)
    bm = Hat._mask(("curve", body))
    for y in range(19, 58, 8):                                                                                      # the studs
        for x in range(30, 96, 8):
            xx = x + (4 if (y // 8) % 2 else 0)
            if all(bm.getpixel((int((xx + d) * K), int(y * K))) > 0 for d in (-3.5, 0, 3.5)):
                h.add(("ell", xx, y + rng.uniform(-.3, .3), 1.7, 1.7), GOLD, shade="dome", line=False)
    if rot == "east":
        h.add(("stroke", [(40, 62), (64, 64), (88, 62)], 3.4), GOLD, shade="cyl", lw=.8)
        h.add(("curve", [(84, 60), (90, 52), (94, 46), (92, 40), (89, 44), (88, 54)]), GOLD, shade="dome", gloss=.5, lw=1.0)   # uraeus
    else:
        h.add(("stroke", [(42, 62), (64, 64), (86, 62)], 3.4), GOLD, shade="cyl", lw=.8)
        if rot == "south":
            h.add(("curve", [(60, 62), (61, 52), (64, 44), (67, 52), (68, 62)]), GOLD, shade="dome", gloss=.5, lw=1.0)
            h.add(("ell", 64, 49, 2.2, 3.2), "#2a6ab0", shade="dome", line=False)


def nemes(h, rot):
    blue = "#2c4a8e"
    if rot == "south":
        cloth = [(36, 66), (38, 44), (48, 33), (64, 30), (80, 33), (90, 44), (92, 66), (98, 98), (90, 112), (82, 112), (84, 92), (82, 70),
                 (78, 56), (50, 56), (46, 70), (44, 92), (46, 112), (38, 112), (30, 98)]
        h.add(("curve", cloth), STUFF, True, "dome", light=(.5, .2))
        for y in range(36, 56, 5):                                                                                     # stripes over the crown
            h.add(("stroke", [(42 + (56 - y) * .2, y + 4), (64, y + 1), (86 - (56 - y) * .2, y + 4)], 1.8), blue, shade="none", line=False)
        for side in (-1, 1):
            for k in range(6):
                y = 64 + k * 8
                x0 = 64 + side * 19
                h.add(("stroke", [(x0, y), (x0 + side * 12, y + 4)], 2.0), blue, shade="none", line=False)
        h.add(("curve", [(46, 55), (64, 52), (82, 55), (82, 59), (64, 57), (46, 59)]), GOLD, shade="cyl", lw=.9)           # brow band
        h.add(("curve", [(61, 55), (62, 47), (64, 42), (66, 47), (67, 55)]), GOLD, shade="dome", gloss=.5, lw=1.0)
        h.add(("ell", 64, 46, 1.8, 2.6), "#2a6ab0", shade="dome", line=False)
    elif rot == "east":
        cloth = [(32, 80), (32, 50), (42, 36), (60, 30), (76, 34), (86, 46), (86, 56), (70, 58), (62, 70), (62, 88), (52, 100), (36, 100)]
        h.add(("curve", cloth), STUFF, True, "dome", light=(.55, .2))
        for k in range(7):
            y = 40 + k * 7
            h.add(("stroke", [(36 + k * .5, y + 4), (60, y - 2), (80 - k * 2, y + 1)], 1.8), blue, shade="none", line=False)
        h.add(("stroke", [(70, 56), (86, 55)], 3.0), GOLD, shade="cyl", lw=.8)
        h.add(("curve", [(84, 56), (89, 48), (90, 42), (87, 44), (85, 50)]), GOLD, shade="dome", lw=.9)
        h.add(("curve", [(40, 96), (46, 104), (42, 114), (36, 108)]), STUFF_D, True, "cyl")                         # the queue
    else:
        cloth = [(36, 66), (38, 44), (48, 33), (64, 30), (80, 33), (90, 44), (92, 66), (98, 96), (64, 92), (30, 96)]
        h.add(("curve", cloth), STUFF, True, "dome", light=(.5, .2))
        for y in range(38, 92, 6):
            w = 26 + (y - 38) * .2
            h.add(("stroke", [(64 - w, y + 2), (64, y), (64 + w, y + 2)], 1.8), blue, shade="none", line=False)
        h.add(("curve", [(58, 90), (70, 90), (68, 106), (64, 110), (60, 106)]), STUFF_D, True, "cyl")


def nordhelm(h, rot):
    cx = 64 if rot != "east" else 63
    pts = dome(cx, 64, 26, 24) if rot != "east" else dome(cx, 64, 27, 25)
    # a slight point at the top
    pts = [(x, y - max(0.0, 5 - abs(x - cx) * 0.6)) for x, y in pts]
    h.add(("poly", pts), STUFF, True, "dome", gloss=.3)
    h.add(("stroke", [(cx - 26, 60), (cx, 63), (cx + 26, 60)], 3.6), STUFF_D, True, "cyl", lw=.9)                     # brow band
    if rot != "north":
        h.add(("stroke", [(cx, 22), (cx, 62)] if rot == "south" else [(cx + 6, 22), (cx + 22, 40), (cx + 26, 60)], 3.0), STUFF_D, True, "cyl", lw=.9)
    if rot == "south":
        for sx in (-1, 1):                                                                                           # spectacle guard
            ex = 64 + sx * 7.5
            h.add(("ell", ex, 69, 7, 5.5), STUFF_D, True, "dome", lw=1.0)
            h.add(("ell", ex, 69.5, 4.2, 3.0), "#141214", shade="none", lw=.6)
        h.add(("poly", [(62, 62), (66, 62), (65.5, 80), (64, 82), (62.5, 80)]), STUFF_D, True, "cyl", lw=.9)          # nasal
        for x in (cx - 18, cx + 18):
            h.add(("ell", x, 61, 1.3, 1.3), STUFF_DD, True, "none", line=False)
    elif rot == "east":
        h.add(("curve", [(72, 62), (90, 62), (92, 72), (84, 76), (74, 72)]), STUFF_D, True, "dome", lw=1.0)
        h.add(("ell", 83, 69.5, 4.0, 3.0), "#141214", shade="none", lw=.6)
        h.add(("stroke", [(46, 61), (36, 66)], 1.5), STUFF_DD, True, "none", line=False)
    else:
        h.add(("stroke", [(cx, 22), (cx, 62)], 3.0), STUFF_D, True, "cyl", lw=.9)
        for k in range(9):                                                                                         # a mail curtain at the nape
            h.add(("ell", 44 + k * 5, 66, 2.6, 2.6), STUFF_DD, True, "dome", lw=.6)


def circlet(h, rot):
    if rot == "south":
        h.add(("curve", [(41, 49), (64, 54), (87, 49), (87, 53.5), (64, 58.5), (41, 53.5)]), STUFF, True, "cyl", lw=1.0)
        h.add(("curve", [(58, 56), (64, 48), (70, 56), (64, 63)]), STUFF_D, True, "dome", lw=1.0)                    # knot piece
        h.add(("ell", 64, 55.5, 2.6, 2.6), "#b0302a", shade="dome", gloss=.7, line=False)
        for x in (50, 78):
            h.add(("ell", x, 54, 1.6, 1.6), STUFF_DD, True, "dome", line=False)
    elif rot == "east":
        h.add(("curve", [(38, 54), (64, 49), (88, 51), (88, 55), (64, 53.5), (38, 58)]), STUFF, True, "cyl", lw=1.0)
        h.add(("curve", [(82, 52), (87, 46), (90, 52), (87, 57)]), STUFF_D, True, "dome", lw=1.0)
        h.add(("ell", 87, 51.5, 1.6, 1.8), "#b0302a", shade="dome", gloss=.7, line=False)
    else:
        h.add(("curve", [(39, 55), (64, 56), (89, 55), (89, 59), (64, 60.5), (39, 59)]), STUFF, True, "cyl", lw=1.0)


def winged(h, rot):
    cx = 64 if rot != "east" else 62

    def wing(base, sx, length=26, n=6):
        bx, by = base
        for k in range(n):
            a = math.radians(-90 + sx * (8 + k * 12))
            tip = (bx + length * (1 - k * .06) * math.cos(a) * 1.0, by + length * (1 - k * .06) * math.sin(a))
            h.add(("stroke", [(bx, by), ((bx + tip[0]) / 2 + sx * 1.5, (by + tip[1]) / 2), tip], 5.0), STUFF if k % 2 == 0 else STUFF_D, True,
                  "flat", lw=1.0)

    if rot == "east":
        wing((cx - 6, 44), -1, 30, 6)
    else:
        wing((cx - 20, 46), -1)
        wing((cx + 20, 46), 1)
    h.add(("poly", dome(cx, 64, 24, 34)), STUFF, True, "dome", gloss=.35)
    h.add(("stroke", [(cx - 24, 60), (cx, 63), (cx + 24, 60)], 3.4), GOLD, shade="cyl", lw=.9)
    for k in range(7):
        h.add(("ell", cx - 18 + k * 6, 61.5, 1.4, 1.4), "#e8e4dc", shade="dome", line=False)                         # pearls
    gx = cx if rot != "east" else cx - 2
    h.add(("curve", arcpts(gx, 30, 9, 7, 200, 340, 9) + arcpts(gx, 29, 6, 4, 340, 200, 9)), GOLD, shade="dome", lw=.9)   # crescent
    h.add(("ell", gx, 20, 7, 7.5), "#2c3a7a", shade="dome", gloss=.35)                                              # korymbos
    if rot == "east":
        wing((cx - 4, 46), -1, 24, 5)


def kidaris(h, rot):
    cx = 64 if rot != "east" else 63
    body = [(cx - 21, 62), (cx - 23, 28), (cx + 23, 28), (cx + 21, 62)]
    h.add(("poly", body), STUFF, True, "cyl", gloss=.2)
    # crenellations: stepped merlons
    for k in range(5):
        x = cx - 23 + k * (46 - 8.5) / 4
        h.add(("poly", [(x, 29), (x, 20), (x + 2.5, 20), (x + 2.5, 16), (x + 6, 16), (x + 6, 20), (x + 8.5, 20), (x + 8.5, 29)]), STUFF, True, "flat", lw=1.0)
    h.add(("poly", [(cx - 23, 26), (cx + 23, 26), (cx + 23, 31), (cx - 23, 31)]), STUFF_D, True, "cyl", lw=1.0)
    h.add(("poly", [(cx - 21.5, 55), (cx + 21.5, 55), (cx + 21, 62), (cx - 21, 62)]), STUFF_D, True, "cyl", lw=1.0)
    if rot != "north":
        span = range(-2, 3) if rot == "south" else range(0, 3)
        for k in span:
            x = cx + k * 8 + (6 if rot == "east" else 0)
            h.add(("ell", x, 43, 2.6, 3.2), ["#2a6ab0", RED, "#2a8a5a"][k % 3], shade="dome", gloss=.6, lw=.8)
        for k in range(-3, 4) if rot == "south" else range(0, 4):
            x = cx + k * 6 + (6 if rot == "east" else 0)
            h.add(("ell", x, 58.5, 1.4, 1.4), "#e8e4dc", shade="dome", line=False)


def galea(h, rot):
    crest, crest2 = "#b0242a", "#6a1418"
    if rot == "south":
        h.add(("curve", [(58, 34), (57, 16), (64, 8), (71, 16), (70, 34)]), crest, shade="cyl")
        h.add(("poly", [(61, 34), (67, 34), (67, 28), (61, 28)]), STUFF_D, True, "flat", lw=.9)
        for sx in (-1, 1):                                                                                          # cheek guards
            x0 = 64 + sx * 24
            h.add(("curve", [(x0, 58), (x0 - sx * 8, 60), (x0 - sx * 9, 76), (x0 - sx * 4, 86), (x0 + sx * 1, 76)]), STUFF_D, True, "dome", lw=1.0)
            h.add(("ell", x0 - sx * 4, 66, 1.2, 1.2), GOLD, shade="none", line=False)
        h.add(("poly", dome(64, 62, 25, 32)), STUFF, True, "dome", gloss=.35)
        h.add(("curve", [(39, 58), (64, 54), (89, 58), (89, 62), (64, 60), (39, 62)]), STUFF_D, True, "cyl", lw=1.0)      # brow guard
        h.add(("stroke", [(44, 46), (52, 40), (64, 38), (76, 40), (84, 46)], 1.6), GOLD, shade="none", line=False)
    elif rot == "east":
        fan = [(36, 36)] + arcpts(62, 40, 26, 30, 200, 340, 12) + [(88, 36), (62, 32)]
        h.add(("curve", fan), crest, shade="dome", light=(.4, .2))
        for k in range(6):
            a = math.radians(207 + k * 24)
            h.add(("stroke", [(62 + 12 * math.cos(a), 39 + 12 * math.sin(a)), (62 + 24 * math.cos(a), 40 + 27 * math.sin(a))], 1.0), crest2,
                  shade="none", line=False)
        h.add(("curve", [(38, 58), (28, 64), (22, 70), (34, 72), (44, 64)]), STUFF_D, True, "flat", lw=1.0)           # neck guard
        h.add(("poly", dome(62, 62, 25, 32)), STUFF, True, "dome", gloss=.35, light=(.55, .25))
        h.add(("curve", [(66, 58), (80, 58), (82, 74), (76, 86), (70, 76)]), STUFF_D, True, "dome", lw=1.0)           # cheek guard
        h.add(("curve", [(70, 55), (88, 57), (90, 61), (72, 60)]), STUFF_D, True, "cyl", lw=1.0)                      # brow guard
        h.add(("ell", 74, 66, 1.2, 1.2), GOLD, shade="none", line=False)
    else:
        h.add(("curve", [(58, 34), (57, 16), (64, 8), (71, 16), (70, 34)]), crest, shade="cyl")
        h.add(("curve", [(34, 62), (64, 58), (94, 62), (98, 70), (64, 68), (30, 70)]), STUFF_D, True, "cyl", lw=1.0)     # neck guard
        h.add(("poly", dome(64, 62, 25, 32)), STUFF, True, "dome", gloss=.3)
        h.add(("stroke", [(44, 50), (64, 46), (84, 50)], 1.4), STUFF_DD, True, "none", line=False)


def tianxia_helm(h, rot):
    cx = 64 if rot != "east" else 63
    curtain = STUFF_D
    if rot == "south":
        for sx in (-1, 1):
            x0 = 64 + sx * 22
            h.add(("curve", [(x0, 56), (x0 + sx * 10, 58), (x0 + sx * 12, 86), (x0 + sx * 2, 90), (x0 - sx * 3, 70)]), curtain, True, "cyl", lw=1.0)
            for y in range(62, 88, 5):
                h.add(("stroke", [(x0 - sx * 1, y), (x0 + sx * 11, y + 1)], 1.0), STUFF_DD, True, "none", line=False)
    elif rot == "east":
        h.add(("curve", [(40, 56), (52, 60), (54, 80), (44, 94), (30, 92), (32, 70)]), curtain, True, "cyl", lw=1.0)
        for y in range(62, 92, 5):
            h.add(("stroke", [(32, y), (52, y - 1)], 1.0), STUFF_DD, True, "none", line=False)
    else:
        h.add(("curve", [(36, 56), (64, 58), (92, 56), (96, 88), (64, 94), (32, 88)]), curtain, True, "cyl", lw=1.0)
        for y in range(62, 92, 5):
            h.add(("stroke", [(36, y), (64, y + 2), (92, y)], 1.0), STUFF_DD, True, "none", line=False)
    # tassel and spike
    h.add(("curve", [(cx - 8, 28), (cx - 10, 20), (cx, 16), (cx + 10, 20), (cx + 8, 28), (cx, 30)]), RED, shade="dome")
    for k in range(-3, 4):
        h.add(("stroke", [(cx + k * 1.6, 20), (cx + k * 2.8, 29)], .9), RED_D, shade="none", line=False)
    h.add(("poly", [(cx - 2, 18), (cx, 4), (cx + 2, 18)]), STUFF_D, True, "cyl", lw=.9)
    h.add(("ell", cx, 18, 3.4, 2), GOLD, shade="dome", lw=.8)
    pts = dome(cx, 62, 25, 26)
    pts = [(x, y - max(0.0, 4 - abs(x - cx) * 0.4)) for x, y in pts]
    h.add(("poly", pts), STUFF, True, "dome", gloss=.3)
    for k in range(-2, 3):
        h.add(("stroke", [(cx + k * 9, 61), (cx + k * 3, 28)], 1.3), STUFF_DD, True, "none", line=False)
    h.add(("curve", [(cx - 26, 57), (cx, 54), (cx + 26, 57), (cx + 26, 62), (cx, 60), (cx - 26, 62)]), GOLD, shade="cyl", lw=1.0)


def futou(h, rot):
    cx = 64 if rot != "east" else 62
    if rot != "east":
        for sx in (-1, 1):                                                                                           # the long wings
            h.add(("curve", [(cx + sx * 16, 40), (cx + sx * 48, 38), (cx + sx * 51, 41), (cx + sx * 48, 44), (cx + sx * 16, 45)]), STUFF_D, True,
                  "flat", lw=1.0)
        h.add(("curve", [(cx - 14, 46), (cx - 14, 24), (cx, 18), (cx + 14, 24), (cx + 14, 46)]), STUFF_D, True, "dome")      # raised back
        h.add(("poly", dome(cx, 62, 24, 36)), STUFF, True, "dome", gloss=.2)
        h.add(("stroke", [(cx - 24, 59), (cx, 62), (cx + 24, 59)], 2.4), STUFF_DD, True, "cyl", lw=.8)
    else:
        h.add(("curve", [(cx - 22, 46), (cx - 20, 24), (cx - 8, 18), (cx + 4, 24), (cx + 4, 46)]), STUFF_D, True, "dome")
        h.add(("poly", dome(cx, 62, 26, 36)), STUFF, True, "dome", gloss=.2)
        h.add(("curve", [(cx - 20, 36), (cx - 12, 34), (cx - 11, 46), (cx - 19, 48)]), STUFF_DD, True, "flat", lw=1.0)     # wing seen end-on
        h.add(("stroke", [(cx - 26, 59), (cx, 62), (cx + 26, 59)], 2.4), STUFF_DD, True, "cyl", lw=.8)


def kabuto(h, rot):
    lace = "#2a3e7e"
    gold = GOLD
    if rot == "south":
        for sx in (-1, 1):                                                                                           # shikoro, one side each
            for r in reversed(range(4)):
                y = 54 + r * 7
                x_in, x_out = 64 + sx * 20, 64 + sx * (30 + r * 4)
                pts = [(x_in, y), (x_out, y + 1), (x_out + sx * 2, y + 7), (x_in + sx * 2, y + 8)]
                h.add(("poly", pts), STUFF_D, True, "cyl", lw=1.0)
                h.add(("stroke", [(x_in + sx * 3, y + 4), (x_out - sx * 1, y + 4.5)], 1.4), lace, shade="none", line=False)
            h.add(("curve", [(64 + sx * 24, 52), (64 + sx * 34, 50), (64 + sx * 36, 58), (64 + sx * 26, 62)]), STUFF, True, "flat", lw=1.0)  # fukigaeshi
        h.add(("poly", dome(64, 60, 25, 30)), STUFF, True, "dome", gloss=.35)
        for k in range(-3, 4):
            h.add(("stroke", [(64 + k * 7.5, 58), (64 + k * 1.5, 32)], 1.2), STUFF_DD, True, "none", line=False)
        h.add(("curve", [(39, 56), (64, 52), (89, 56), (89, 61), (64, 58), (39, 61)]), STUFF_D, True, "cyl", lw=1.0)        # mabizashi (peak)
        for sx in (-1, 1):                                                                                           # kuwagata, the gilt horns
            h.add(("curve", [(64 + sx * 2, 52), (64 + sx * 9, 36), (64 + sx * 15, 18), (64 + sx * 21, 6), (64 + sx * 18, 18), (64 + sx * 12, 36), (64 + sx * 6, 50)]), gold, shade="cyl", gloss=.4, lw=.8)
        h.add(("ell", 64, 50, 4, 3.6), gold, shade="dome", gloss=.5, lw=.9)
        h.add(("ell", 64, 50, 1.6, 1.6), "#b0302a", shade="none", line=False)
    elif rot == "east":
        for r in reversed(range(4)):
            y = 52 + r * 7
            pts = [(56, y), (34 - r * 4, y + 2), (32 - r * 4, y + 9), (58, y + 8)]
            h.add(("poly", pts), STUFF_D, True, "cyl", lw=1.0)
            h.add(("stroke", [(55, y + 4.5), (35 - r * 4, y + 6)], 1.4), lace, shade="none", line=False)
        h.add(("poly", dome(62, 60, 26, 30)), STUFF, True, "dome", gloss=.35, light=(.55, .25))
        for k in range(-3, 4):
            h.add(("stroke", [(62 + k * 7.5, 58), (62 + k * 1.5, 32)], 1.2), STUFF_DD, True, "none", line=False)
        h.add(("curve", [(66, 55), (92, 57), (92, 61), (66, 60)]), STUFF_D, True, "cyl", lw=1.0)
        h.add(("curve", [(80, 50), (90, 46), (92, 56), (84, 60)]), STUFF, True, "flat", lw=1.0)
        h.add(("curve", [(83, 52), (89, 36), (92, 20), (91, 6), (95, 20), (93, 38), (87, 52)]), gold, shade="cyl", gloss=.4, lw=.8)
    else:
        for r in reversed(range(4)):
            y = 54 + r * 7
            w = 30 + r * 4
            h.add(("curve", [(64 - w, y), (64, y - 2), (64 + w, y), (64 + w + 2, y + 7), (64, y + 6), (64 - w - 2, y + 7)]), STUFF_D, True, "cyl", lw=1.0)
            h.add(("stroke", [(64 - w + 2, y + 4), (64, y + 2.5), (64 + w - 2, y + 4)], 1.4), lace, shade="none", line=False)
        h.add(("poly", dome(64, 58, 25, 30)), STUFF, True, "dome", gloss=.3)
        for k in range(-3, 4):
            h.add(("stroke", [(64 + k * 7.5, 56), (64 + k * 1.5, 32)], 1.2), STUFF_DD, True, "none", line=False)
        h.add(("ell", 64, 30, 4, 2.2), gold, shade="dome", lw=.8)                                                       # tehen ring


def jingasa(h, rot):
    cx = 64 if rot != "east" else 63
    cone = [(cx - 44, 58), (cx - 30, 46), (cx - 8, 30), (cx, 28), (cx + 8, 30), (cx + 30, 46), (cx + 44, 58), (cx + 30, 62), (cx, 64), (cx - 30, 62)]
    h.add(("curve", cone), STUFF, True, "dome", light=(.45, .2), gloss=.2)
    h.add(("curve", [(cx - 44, 58), (cx, 63), (cx + 44, 58), (cx + 42, 61), (cx, 66), (cx - 42, 61)]), STUFF_D, True, "cyl", lw=.9)
    for k in range(-4, 5):
        if k:
            h.add(("stroke", [(cx + k * 2, 31), (cx + k * 9.5, 60)], 1.0), STUFF_DD, True, "none", line=False)
    if rot == "south":
        h.add(("ell", cx, 47, 7.5, 6.5), "#1a1a1c", shade="dome", gloss=.3, lw=.9)                                  # lacquered mon
        h.add(("ell", cx, 47, 5.2, 4.4), GOLD, shade="dome", lw=.6)
        for k in range(3):
            a = math.radians(-90 + k * 120)
            h.add(("ell", cx + 2.2 * math.cos(a), 47 + 1.9 * math.sin(a), 1.7, 1.5), "#1a1a1c", shade="none", line=False)
    elif rot == "east":
        h.add(("ell", cx + 30, 50, 3, 5.5), "#1a1a1c", shade="dome", lw=.8)
        h.add(("ell", cx + 30, 50, 1.6, 3.4), GOLD, shade="none", line=False)
    h.add(("ell", cx, 29, 3.4, 2.2), "#1a1a1c", shade="dome", gloss=.4, lw=.8)


KINDS = {
    "HE_Albion_Shako": shako, "HE_Albion_TopHat": tophat, "HE_Albion_Bicorne": bicorne, "HE_Hellas_Corinthian": corinthian,
    "HE_Hellas_OliveWreath": lambda h, r: wreath(h, r, False), "HE_Roma_Laurel": lambda h, r: wreath(h, r, True),
    "HE_Inti_PlumedHelm": plumed, "HE_Inti_Mascaypacha": mascaypacha, "HE_Kemet_Khepresh": khepresh, "HE_Kemet_Nemes": nemes,
    "HE_Nord_Helm": nordhelm, "HE_Nord_Circlet": circlet, "HE_Pars_WingedHelm": winged, "HE_Pars_Kidaris": kidaris,
    "HE_Roma_Galea": galea, "HE_Tianxia_Helmet": tianxia_helm, "HE_Tianxia_Futou": futou, "HE_Yamato_Kabuto": kabuto,
    "HE_Yamato_Jingasa": jingasa,
}
THIN = {"HE_Hellas_OliveWreath": 2.0, "HE_Roma_Laurel": 2.0, "HE_Nord_Circlet": 2.2, "HE_Inti_Mascaypacha": 2.4}
UNSTUFFED = {"HE_Hellas_OliveWreath"}
_cache = {}


def draw(kind, rot):
    if (kind, rot) not in _cache:
        h = Hat(THIN.get(kind, OUTLINE))
        KINDS[kind](h, rot)
        _cache[(kind, rot)] = h.render()
    return _cache[(kind, rot)]


@painter
def heirs_worn(kind, rot, mask=False):
    img, m = draw(kind, rot)
    return m if mask else img
