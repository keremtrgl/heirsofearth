"""Heirs of Earth: vanilla-style sample set (style test only, not final mod art).

Draws a Roman shield, a katana, a Nordheim axe, a Roman aqueduct and a state banner with the
kut_render material renderer, then lays them out on one preview sheet.
Usage: python -I tools/heirs_style_sample.py <out_dir>
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kut_render import (BRONZE, DARKIRON, GOLD, IRON, LEATHER, LEATHER_D, SS, STEEL, STONE, STONE_D, STONE_L,
                        WOOD, WOOD_D, WOOD_V, Canvas, Mat, arc)

ROMA_RED = Mat("#8e2a24", .10, 2, tint="#6d1f1c")
BLADE = Mat("#9aa4aa", .05, 3, (9, 1), spec=.9)
HAMON = Mat("#dde3e6", .04, 2, (9, 1), spec=1.2)
ITO = Mat("#25293a", .10, 1.5)
SAME = Mat("#d8ccb0", .08, 1.5)
TSUBA = Mat("#3a342d", .10, 2, spec=.4)
AXE_IRON = Mat("#6f777c", .09, 3, spec=.7, tint="#5b5550")
WATER = Mat("#3d7ea3", .08, 6, (6, 1), spec=.9)
BEAM = Mat("#6b4a2e", .18, 3, (1, 9))


def axis(p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    length = math.hypot(x1 - x0, y1 - y0)
    d = ((x1 - x0) / length, (y1 - y0) / length)
    n = (-d[1], d[0])
    return (lambda u, v: (x0 + d[0] * u + n[0] * v, y0 + d[1] * u + n[1] * v)), length


def leaf(cx, cy, ang, ln, wd):
    a = math.radians(ang)
    d, n = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    pts = []
    for i in range(9):
        t = i / 8
        u, v = (t - .5) * ln, math.sin(t * math.pi) * wd / 2
        pts.append((cx + d[0] * u + n[0] * v, cy + d[1] * u + n[1] * v))
    for i in range(7, 0, -1):
        t = i / 8
        u, v = (t - .5) * ln, -math.sin(t * math.pi) * wd / 2
        pts.append((cx + d[0] * u + n[0] * v, cy + d[1] * u + n[1] * v))
    return pts


def mirror(points, cx):
    return [(2 * cx - x, y) for x, y in points]


def wear(c, n, box, seed, opacity=.22):
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        a, ln = rng.uniform(0, math.pi), rng.uniform(2, 6)
        c.scratch(.45, opacity, (x, y), (x + math.cos(a) * ln, y + math.sin(a) * ln))


def scutum():
    c = Canvas(128, seed=11)
    c.rect(BRONZE, 30, 8, 98, 120, 8, cyl=(30, 98), bevel=1.6)
    c.rect(ROMA_RED, 33.5, 11.5, 94.5, 116.5, 6, cyl=(30, 98), bevel=2.6, edge=.35)
    c.rect(BRONZE, 62.4, 14, 65.6, 114, 1, bevel=.9)
    wing = [(52, 60), (46, 56), (39, 49), (36, 44), (38, 52), (34, 53), (38, 58), (33, 61), (38, 65), (34, 69), (41, 71), (52, 69)]
    c.poly(GOLD, *wing, bevel=1.2)
    c.poly(GOLD, *mirror(wing, 64), bevel=1.2)
    for sx, sy, ex, ey in ((56, 50, 42, 22), (72, 50, 86, 22), (56, 78, 42, 106), (72, 78, 86, 106)):
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        nx, ny = -(ey - sy), ex - sx
        k = 3.2 / math.hypot(nx, ny)
        pts = [(sx, sy), (mx + nx * k, my + ny * k), (mx - nx * k, my - ny * k), (ex, ey)]
        c.line(GOLD, 2.4, *pts)
    c.ell(IRON, 64, 64, 12.5, 12.5, bevel=2.2)
    c.ell(STEEL, 64, 64, 7.5, 7.5, bevel=3.2)
    for i in range(9):
        y = 16 + i * 12
        for x in (36.5, 91.5):
            c.ell(BRONZE, x, y, 1.3, 1.3, bevel=.6, edge=.4)
    wear(c, 40, (36, 14, 92, 114), 4)
    c.scratch(.6, .35, (44, 92), (50, 98), (53, 97))
    c.glow(50, 52, 9, "#ffd27a", .15)
    return c.image()


def katana():
    c = Canvas(128, seed=12)
    at, length = axis((16, 114), (115, 13))
    off = lambda u: -6.5 * (u / length) ** 2
    pts = lambda segs: [at(u, v + off(u)) for u, v in segs]
    c.poly(ITO, *pts([(4, -3.6), (40, -3.4), (40, 3.4), (4, 3.6)]), bevel=1.0)
    for u in range(8, 39, 6):
        c.poly(SAME, *pts([(u - 2.5, 0), (u, -2.4), (u + 2.5, 0), (u, 2.4)]), bevel=.6, edge=.3)
    c.poly(GOLD, *pts([(20, -1.6), (25, -2.1), (25, 2.1), (20, 1.6)]), bevel=.6)
    c.poly(DARKIRON, *pts([(0, -3.0), (4.5, -3.9), (4.5, 3.9), (0, 3.0)]), bevel=.8)
    c.poly(TSUBA, *pts([(40, -8.5), (41.5, -9.5), (44, -9.5), (45, -8.5), (45, 8.5), (44, 9.5), (41.5, 9.5), (40, 8.5)]), bevel=1.0)
    spine = [(u, -2.6 + .7 * (u - 49) / 84) for u in range(49, 130, 3)]
    edge = [(u, 2.7 - .8 * (u - 49) / 84) for u in range(127, 48, -3)]
    c.poly(BLADE, *pts(spine + [(length - .5, -1.6)] + [(131, 1.2)] + edge), bevel=1.0)
    hamon = [(u, 2.7 - .8 * (u - 49) / 84) for u in range(50, 128, 3)] + [(131, 1.1)]
    inner = [(u, .6 + .55 * math.sin(u * .55) - .4 * (u - 49) / 84) for u in range(129, 49, -3)]
    c.poly(HAMON, *pts(hamon + inner), bevel=.5, edge=.0, clip=True)
    c.scratch(.55, .35, *pts([(52, -1.3), (118, -.9)]))
    c.poly(GOLD, *pts([(45, -3.4), (50, -3.0), (50, 3.0), (45, 3.4)]), bevel=.6)
    c.glow(*at(92, off(92)), 18, "#f4f7ff", .12)
    return c.image()


def nordheim_axe():
    c = Canvas(128, seed=13)
    at, length = axis((40, 121), (79, 6))
    pts = lambda segs: [at(u, v) for u, v in segs]
    c.poly(WOOD_V, *pts([(0, -2.8), (116, -2.4), (116, 2.4), (0, 2.8)]), bevel=1.0)
    upper = [(116, 5), (115, 12), (118, 20), (123, 28), (127, 34)]
    edge = [(127 - 45 * t, 34 + 9 * math.sin(math.pi * t) - 2 * t) for t in [i / 14 for i in range(15)]]
    beard = [(88, 26), (95, 19), (101, 14), (105, 10), (106, 5)]
    c.poly(AXE_IRON, *pts(upper + edge + beard), bevel=1.6)
    strip = edge + [(83 + 43 * t, 29 + 8 * math.sin(math.pi * t) - 1.5 * t) for t in [i / 14 for i in range(15)]]
    c.poly(STEEL, *pts(strip), bevel=.7, edge=.25, clip=True)
    c.poly(DARKIRON, *pts([(102, -4.2), (119, -3.8), (119, 5.6), (102, 5.6)]), bevel=1.1)
    for u in (105, 116):
        c.ell(IRON, *at(u, -1.2), 1.4, 1.4, bevel=.6)
    for u in range(16, 44, 4):
        c.poly(LEATHER if (u // 4) % 2 else LEATHER_D, *pts([(u, -3.3), (u + 4.4, -3.3), (u + 3.4, 3.3), (u - 1, 3.3)]), bevel=.6, edge=.3)
    c.poly(DARKIRON, *pts([(-1, -3.2), (6, -3.2), (6, 3.2), (-1, 3.2)]), bevel=.8)
    c.scratch(.5, .4, *pts([(110, 15), (104, 22), (112, 28), (106, 33)]))
    c.glow(*at(108, 26), 14, "#e8f0ff", .12)
    return c.image()


def aqueduct():
    c = Canvas(256, 160, seed=14)
    wall = c.rect_mask(8, 28, 248, 152)
    upper = [(24 + i * 34.6, 11) for i in range(7)]
    lower = [(38 + i * 60, 21) for i in range(4)]
    holes = []
    for x, r in upper:
        holes.append(c._mask(lambda d, x=x, r=r: (d.ellipse([(x - r) * SS, 35 * SS, (x + r) * SS, (35 + 2 * r) * SS], fill=255),
                                                  d.rectangle([(x - r) * SS, (35 + r) * SS, (x + r) * SS, 70 * SS], fill=255))))
    for x, r in lower:
        holes.append(c._mask(lambda d, x=x, r=r: (d.ellipse([(x - r) * SS, 82 * SS, (x + r) * SS, (82 + 2 * r) * SS], fill=255),
                                                  d.rectangle([(x - r) * SS, (82 + r) * SS, (x + r) * SS, 160 * SS], fill=255))))
    allholes = holes[0]
    for h in holes[1:]:
        allholes = ImageChops.lighter(allholes, h)
    c.paint(ImageChops.subtract(wall, allholes), STONE_L, bevel=2.2, vert=.12)
    for h in holes:
        shifted = h.transform(h.size, Image.AFFINE, (1, 0, 3 * SS, 0, 1, -2.5 * SS))
        reveal = ImageChops.subtract(h, shifted)
        c.paint(reveal, STONE_D, bevel=.8, edge=.2)
    for y in range(37, 152, 8):
        c.scratch(.45, .22, (8, y), (248, y))
        row = (y - 37) // 8
        for x in range(12 + (row % 2) * 9, 248, 18):
            c.scratch(.4, .18, (x, y), (x, y + 8))
    for x, r in upper:
        for a in range(190, 351, 26):
            p, q = math.radians(a), r + 5
            c.scratch(.5, .32, (x + r * math.cos(p), 35 + r + r * math.sin(p)), (x + q * math.cos(p), 35 + r + q * math.sin(p)))
    for x, r in lower:
        for a in range(185, 356, 17):
            p, q = math.radians(a), r + 8
            c.scratch(.55, .34, (x + r * math.cos(p), 82 + r + r * math.sin(p)), (x + q * math.cos(p), 82 + r + q * math.sin(p)))
    c.rect(STONE, 5, 72, 251, 78, 1, bevel=1.0)
    c.rect(STONE, 4, 12, 252, 30, 2, bevel=1.4)
    c.rect(WATER, 10, 17, 246, 25, 1, bevel=1.0, edge=.3)
    for x in range(20, 240, 37):
        c.scratch(.6, .25, (x, 20), (x + 14, 20), color=(.85, .95, 1.0))
    c.scratch(.5, .3, (4, 30.5), (252, 30.5))
    rng = np.random.default_rng(5)
    for _ in range(60):
        x, y = rng.uniform(10, 246), rng.uniform(120, 152)
        c.scratch(rng.uniform(1.0, 2.6), .12, (x, y), (x + rng.uniform(-2, 2), y + rng.uniform(1, 3)), color=(.24, .32, .18))
    wear(c, 70, (10, 34, 246, 150), 6, .16)
    return c.image()


def banner():
    c = Canvas(128, 192, seed=15)
    c.rect(STONE, 44, 174, 84, 183, 2, bevel=1.2)
    c.rect(STONE_L, 38, 181, 90, 190, 2, bevel=1.4)
    c.rect(WOOD_V, 61, 30, 67, 176, 1, cyl=(61, 67), bevel=1.0)
    c.rect(BEAM, 30, 44, 98, 49.5, 2, bevel=1.0)
    for x in (31, 97):
        c.ell(GOLD, x, 46.7, 2.6, 2.6, bevel=1.0)
    c.rect(GOLD, 34.5, 49, 93.5, 127, 1, bevel=1.0)
    c.rect(ROMA_RED, 37.5, 51.5, 90.5, 124.5, 1, bevel=1.6, edge=.3)
    for x in range(37, 92, 4):
        c.line(GOLD, 1.5, (x, 127), (x + .4, 134))
        c.ell(GOLD, x + .4, 135, 1.3, 1.3, bevel=.5)
    for x, dark in ((44, True), (51, False), (58, True), (70, True), (77, False), (84, True)):
        c.scratch(2.6, .16 if dark else .10, (x, 53), (x + 1, 123), color=(.18, .03, .03) if dark else (1, .78, .7))
    for i in range(7):
        th = math.radians(108 + i * 22)
        lf = leaf(64 + 16 * math.cos(th), 88 + 16 * math.sin(th), math.degrees(th) + 112, 10, 4.6)
        c.poly(GOLD, *lf, bevel=.7, edge=.35)
        c.poly(GOLD, *mirror(lf, 64), bevel=.7, edge=.35)
    c.ell(GOLD, 64, 88, 7, 7, bevel=1.4)
    c.ell(ROMA_RED, 64, 88, 3.6, 3.6, bevel=1.0, edge=.3)
    c.rect(GOLD, 55, 31, 73, 35, 1.5, bevel=.8)
    wing = [(61, 26), (55, 21), (47, 11), (45, 4), (49, 7), (48, 2), (52, 6), (53, 1), (57, 8), (60, 15), (63, 22)]
    c.poly(GOLD, *wing, bevel=1.1)
    c.poly(GOLD, *mirror(wing, 64), bevel=1.1)
    c.ell(GOLD, 64, 24, 5, 7.5, bevel=1.4)
    c.ell(GOLD, 65, 14.5, 3.4, 3.4, bevel=1.0)
    c.poly(BRONZE, (67.5, 13.5), (71.5, 15.2), (67.5, 16.4), bevel=.4)
    c.poly(GOLD, (60, 29), (64, 33), (68, 29), (64, 31), bevel=.5)
    c.glow(56, 14, 10, "#fff0b0", .18)
    return c.image()


def drop_shadow(img, dx, dy, blur, strength=.5):
    pad = 20
    a = Image.new("L", (img.width + 2 * pad, img.height + 2 * pad), 0)
    a.paste(img.getchannel("A"), (pad + dx, pad + dy))
    a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * strength))
    sh = Image.new("RGBA", a.size, (15, 10, 6, 0))
    sh.putalpha(a)
    sh.alpha_composite(img, (pad, pad))
    return sh


def sheet(items, path):
    W, H = 1320, 980
    rng = np.random.default_rng(2)
    base = np.array((86, 74, 58), np.float32)
    n = np.asarray(Image.fromarray((rng.random((H // 6, W // 6)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - .5
    n2 = np.asarray(Image.fromarray((rng.random((H // 40, W // 40)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - .5
    bg = np.clip(base[None, None] * (1 + n[..., None] * .10 + n2[..., None] * .16), 0, 255).astype(np.uint8)
    out = Image.fromarray(bg, "RGB").convert("RGBA")
    d = ImageDraw.Draw(out)
    fonts = "C:/Windows/Fonts/"
    title = ImageFont.truetype(fonts + "georgiab.ttf", 34)
    label = ImageFont.truetype(fonts + "seguisb.ttf", 21)
    small = ImageFont.truetype(fonts + "segoeui.ttf", 17)
    d.text((44, 30), "Dünyanın Mirasçıları", font=title, fill=(242, 232, 210))
    d.text((44, 74), "Stil örneği · kodla çizildi · oyunda bu boyutun yarısı", font=small, fill=(214, 200, 176))
    top = [("Lejyoner kalkanı", "Nova Roma · scutum", items["scutum"]),
           ("Katana", "Yamato · kılıç", items["katana"]),
           ("Dane baltası", "Nordheim · iki el", items["axe"]),
           ("Devlet sancağı", "Nova Roma · bina", items["banner"])]
    x, floor = 44, 520
    for name, sub, img in top:
        big = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
        sh = drop_shadow(big, 8, 10, 7)
        out.alpha_composite(sh, (x - 20, floor - big.height - 20))
        cx = x + big.width // 2
        d.text((cx, floor + 16), name, font=label, fill=(244, 236, 218), anchor="mt")
        d.text((cx, floor + 44), sub, font=small, fill=(200, 186, 162), anchor="mt")
        x += big.width + 56
    aq = items["aqueduct"]
    big = aq.resize((aq.width * 2, aq.height * 2), Image.LANCZOS)
    ax = (W - big.width) // 2
    out.alpha_composite(drop_shadow(big, 10, 12, 9), (ax - 20, 586 - 20))
    d.text((W // 2, 586 + big.height + 14), "Roma su kemeri", font=label, fill=(244, 236, 218), anchor="mt")
    out.convert("RGB").save(path, optimize=True)


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    items = {"scutum": scutum(), "katana": katana(), "axe": nordheim_axe(), "banner": banner(), "aqueduct": aqueduct()}
    for name, img in items.items():
        img.save(os.path.join(out_dir, f"{name}.png"))
    sheet(items, os.path.join(out_dir, "heirs_stil_ornegi.png"))
    print("ok", sorted(items))


if __name__ == "__main__":
    main()
