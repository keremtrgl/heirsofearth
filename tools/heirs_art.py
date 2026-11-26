"""Heirs of Earth: draws every texture registered in heirs_data.TEXTURES.

Usage: python -I tools/heirs_art.py [only-substring]
Painters are looked up by name in PAINTERS; each returns a PIL image (RGBA, or RGB for terrain).
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import heirs_data as data  # noqa: E402
import heirs_style_sample as sample  # noqa: E402
from kut_render import (BRONZE, DARKIRON, GOLD, IRON, LEATHER, LEATHER_D, MARBLE, SS, STEEL, STONE, STONE_D, STONE_L,  # noqa: E402
                        WOOD, WOOD_D, WOOD_V, Canvas, Mat, arc, rgb)

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "HeirsOfEarth", "Textures")
PAINTERS = {}


def painter(fn):
    PAINTERS[fn.__name__] = fn
    return fn


def m(color, noise=.10, scale=2, stretch=(1, 1), spec=0.0, tint=None):
    return Mat(color, noise, scale, stretch, spec, tint)


def axis(p0, p1):
    return sample.axis(p0, p1)


# ------------------------------------------------------------------ shared weapon parts
def blade(c, at, u0, u1, w0, w1, mat, tip=6.0, edge_mat=None, fuller=True, off=lambda u: 0.0):
    """Straight or curved double-edged blade from u0 to u1 along an axis; w = half width."""
    n = 10
    left, right = [], []
    for i in range(n + 1):
        u = u0 + (u1 - tip - u0) * i / n
        w = w0 + (w1 - w0) * i / n
        left.append(at(u, -w + off(u)))
        right.append(at(u, w + off(u)))
    pts = left + [at(u1, off(u1))] + right[::-1]
    c.poly(mat, *pts, bevel=1.0)
    if edge_mat:
        inner = [at(u0 + (u1 - tip - u0) * i / n, (w0 + (w1 - w0) * i / n) * .45 + off(u0 + (u1 - tip - u0) * i / n)) for i in range(n + 1)]
        c.poly(edge_mat, *(right + [at(u1, off(u1))] + inner[::-1]), bevel=.5, edge=0, clip=True)
    if fuller:
        c.scratch(.6, .35, at(u0 + 3, off(u0 + 3)), at(u1 - tip - 4, off(u1 - tip - 4)))


def haft(c, at, u0, u1, w, mat=WOOD_V, bevel=1.0):
    c.poly(mat, at(u0, -w), at(u1, -w), at(u1, w), at(u0, w), bevel=bevel)


def wraps(c, at, u0, u1, w, step=4, mats=(LEATHER, LEATHER_D)):
    u, i = u0, 0
    while u < u1:
        c.poly(mats[i % 2], at(u, -w), at(u + step, -w), at(u + step - 1, w), at(u - 1, w), bevel=.5, edge=.3)
        u += step
        i += 1


# ------------------------------------------------------------------ Nova Roma
ROMA_RED = sample.ROMA_RED


@painter
def gladius():
    c = Canvas(128, seed=21)
    at, L = axis((22, 110), (108, 20))
    c.ell(BRONZE, *at(4, 0), 6, 6, bevel=1.4)
    haft(c, at, 6, 30, 3.4, m("#d9cdb2", .08, 2, (1, 6)))
    for u in (11, 17, 23):
        c.poly(BRONZE, at(u, -3.6), at(u + 1.6, -3.6), at(u + 1.6, 3.6), at(u, 3.6), bevel=.5)
    c.poly(BRONZE, at(29, -9), at(35, -8), at(35, 8), at(29, 9), bevel=1.0)
    blade(c, at, 35, L, 6.2, 5.0, sample.BLADE, tip=16, edge_mat=sample.HAMON)
    c.glow(*at(70, -2), 16, "#f4f7ff", .10)
    return c.image()


@painter
def pilum():
    c = Canvas(128, seed=22)
    at, L = axis((14, 116), (116, 10))
    haft(c, at, 0, 84, 2.3, WOOD_V)
    c.poly(BRONZE, at(80, -3.2), at(88, -3.0), at(88, 3.0), at(80, 3.2), bevel=.8)
    c.poly(IRON, at(88, -1.2), at(L - 9, -1.0), at(L - 9, 1.0), at(88, 1.2), bevel=.6)
    c.poly(STEEL, at(L - 10, -3.4), at(L, 0), at(L - 10, 3.4), at(L - 12, 0), bevel=.8)
    c.ell(DARKIRON, *at(0, 0), 2.6, 2.6, bevel=.6)
    return c.image()


@painter
def roma_standard(size=(1, 1)):
    return sample.banner()


@painter
def aqueduct(size=(3, 1)):
    img = sample.aqueduct()
    return img.resize((384, 240), Image.LANCZOS)


@painter
def brazier(size=(1, 1)):
    c = Canvas(128, seed=24)
    for x0, x1 in ((40, 52), (76, 88)):
        c.poly(DARKIRON, (x0, 118), (x0 + 6, 118), (64 + (x1 - 64) * .3, 66), (64 + (x0 - 64) * .3, 66), bevel=.8)
    c.poly(BRONZE, (30, 52), (98, 52), (88, 74), (40, 74), bevel=1.6)
    c.rect(BRONZE, 28, 48, 100, 55, 3, bevel=1.0)
    c.ell(m("#3a2a22", .3, 2), 64, 48, 28, 8, bevel=1.0, edge=.2)
    for dx, dy, r in ((-14, 47, 6), (-3, 45, 7), (9, 47, 6), (18, 49, 4), (2, 50, 5), (-20, 50, 4)):
        c.ell(m("#ff8a3a", .25, 2, tint="#ff4a1a"), 64 + dx, dy, r, r * .6, bevel=1.2, edge=.15)
    c.glow(64, 46, 30, "#ff8a3a", .35)
    return c.image()


@painter
def culture_table(size=(3, 1)):
    c = Canvas(384, 176, seed=25)
    for x in (30, 350):
        c.rect(WOOD_D, x - 7, 96, x + 7, 168, 2, bevel=1.0)
    c.rect(WOOD, 8, 70, 376, 104, 4, bevel=1.8)
    c.rect(WOOD_D, 8, 98, 376, 110, 3, bevel=1.0)
    c.rect(m("#d8cdb2", .06, 2), 40, 52, 120, 82, 2, bevel=1.0)
    for i in range(5):
        c.scratch(.6, .3, (46, 58 + i * 4.5), (112, 58 + i * 4.5))
    c.rect(m("#6e2b24", .1), 138, 50, 176, 84, 2, bevel=1.4)
    c.rect(m("#2f4a6d", .1), 178, 54, 212, 84, 2, bevel=1.4)
    c.line(BRONZE, 3, (236, 80), (262, 48))
    c.ell(m("#bfe4f0", .03, 2, spec=1.2), 266, 44, 10, 10, bevel=1.2)
    c.poly(sample.BLADE, (290, 78), (336, 62), (338, 66), (292, 82), bevel=.6)
    c.ell(m("#b98b4a", .12), 352, 70, 12, 9, bevel=1.4)
    c.poly(BRONZE, (220, 34), (230, 24), (240, 34), (236, 70), (224, 70), bevel=1.0)
    return c.image()


# ------------------------------------------------------------------ floors (512x512, 4x4 cells, seamless)
def floor_canvas(base, seed):
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (1024, 1024), base)
    return img, ImageDraw.Draw(img), rng


def finish_floor(img, seed, amount=3.0):
    arr = np.asarray(img.resize((512, 512), Image.LANCZOS), dtype=np.float32)
    rng = np.random.default_rng(seed)
    arr = arr + rng.normal(0, amount, arr.shape[:2])[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def shade(color, f):
    return tuple(int(max(0, min(255, v * f))) for v in color)


@painter
def floor_concrete():
    base = (168, 160, 146)
    img, d, rng = floor_canvas(base, 31)
    cell = 256
    for i in range(4):
        for j in range(4):
            x, y = i * cell, j * cell
            d.rectangle((x, y, x + cell, y + cell), fill=shade(base, 1 + rng.uniform(-.05, .05)))
            for _ in range(40):
                px, py, r = x + rng.uniform(10, cell - 10), y + rng.uniform(10, cell - 10), rng.uniform(3, 9)
                d.ellipse((px - r, py - r, px + r, py + r), fill=shade(base, rng.uniform(.82, 1.08)))
            d.rectangle((x, y, x + cell - 1, y + cell - 1), outline=shade(base, .7), width=5)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(1.2)), 31, 4.0)


@painter
def floor_road():
    base = (126, 120, 112)
    img, d, rng = floor_canvas(base, 32)
    # Irregular polygonal basalt slabs on a 4x4 grid, edges kept inside each cell so the texture tiles.
    for i in range(8):
        for j in range(8):
            x, y = i * 128, j * 128
            jitter = lambda: rng.uniform(-14, 14)
            pts = [(x + 6 + jitter() * .3, y + 6), (x + 64 + jitter(), y + 4), (x + 122, y + 8 + jitter() * .3), (x + 124, y + 64 + jitter()),
                   (x + 120, y + 122), (x + 64 + jitter(), y + 124), (x + 6, y + 120), (x + 4, y + 64 + jitter())]
            d.polygon(pts, fill=shade((104, 100, 96), rng.uniform(.85, 1.15)), outline=(70, 66, 62))
            d.line(pts[:3], fill=shade((150, 146, 140), 1.0), width=3)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(1.0)), 32, 4.5)


# ------------------------------------------------------------------ icons
@painter
def site_icon():
    c = Canvas(128, seed=40)
    c.ell(STONE_D, 64, 92, 46, 18, bevel=1.4)
    c.poly(STONE_L, (34, 92), (40, 44), (52, 40), (56, 92), bevel=1.6)
    c.poly(STONE_L, (72, 92), (76, 52), (88, 48), (94, 92), bevel=1.6)
    c.poly(STONE, (30, 46), (98, 40), (98, 50), (30, 56), bevel=1.2)
    c.poly(GOLD, (60, 22), (64, 10), (68, 22), (80, 24), (70, 31), (73, 44), (64, 36), (55, 44), (58, 31), (48, 24), bevel=1.0)
    return c.image()


@painter
def nation_icon(color="#8e2a24", emblem="eagle"):
    c = Canvas(128, seed=41)
    body = m(color, .08, 2)
    c.poly(GOLD, (20, 10), (108, 10), (108, 84), (64, 120), (20, 84), bevel=1.6)
    c.poly(body, (26, 16), (102, 16), (102, 81), (64, 113), (26, 81), bevel=2.0, edge=.3)
    EMBLEMS[emblem](c)
    return c.image()


@painter
def archive(color="#8e2a24", emblem="eagle"):
    """A tied bundle: leather-bound codex in the nation colour on top of two sealed scrolls."""
    c = Canvas(128, seed=43)
    parch = m("#e2d3ae", .06, 2)
    for y, x0, x1 in ((86, 18, 104), (100, 24, 110)):
        c.rect(parch, x0, y - 9, x1, y + 9, 8, bevel=1.4)
        c.ell(m("#c9b78c", .08, 2), x1 - 2, y, 5, 9, bevel=1.0)
        c.ell(m("#c9b78c", .08, 2), x0 + 2, y, 5, 9, bevel=1.0)
    c.ell(m("#8e1f1a", .2, 2), 62, 104, 7, 6, bevel=1.4)
    c.rect(m("#5a3b22", .12, 2), 26, 30, 100, 80, 4, bevel=1.6)
    c.rect(m(color, .1, 2), 30, 26, 104, 76, 4, bevel=1.8, edge=.3)
    c.rect(parch, 100, 30, 106, 74, 1, bevel=.6)
    c.rect(GOLD, 30, 26, 37, 76, 1, bevel=.8)
    c.rect(GOLD, 44, 36, 92, 66, 3, bevel=.0, edge=.0)
    c.rect(m(color, .1, 2), 47, 39, 89, 63, 2, bevel=1.0)
    c.ell(GOLD, 68, 51, 8, 8, bevel=1.4)
    c.line(m("#7a5a34", .2), 3, (66, 22), (66, 80))
    return c.image()


def _eagle(c, mat=None):
    """A heraldic legion eagle: wings raised with five primaries each, head turned right, fanned tail."""
    mat = mat or GOLD
    wing = [(60, 56), (54, 46), (46, 36), (38, 28), (30, 24), (29, 31), (34, 32), (28, 37), (35, 39), (30, 45), (38, 46),
            (34, 52), (42, 52), (41, 58), (49, 57), (54, 62)]
    c.poly(mat, *wing, bevel=1.2)
    c.poly(mat, *sample.mirror(wing, 64), bevel=1.2)
    for pts in (((50, 44), (40, 36)), ((48, 50), (38, 44)), ((52, 54), (44, 52))):
        c.scratch(1.0, .35, *pts)
        c.scratch(1.0, .35, *sample.mirror(list(pts), 64))
    c.poly(mat, (57, 74), (71, 74), (78, 90), (71, 87), (64, 92), (57, 87), (50, 90), bevel=1.2)
    c.ell(mat, 64, 62, 9, 15, bevel=1.8)
    c.ell(mat, 66, 44, 6.5, 6.5, bevel=1.4)
    c.poly(mat, (71, 42), (80, 45), (75, 47), (71, 49), bevel=1.0)
    c.ell(m("#3a2a12", .1), 68, 43, 1.4, 1.4)
    for x in (59, 69):
        c.line(mat, 2.2, (x, 74), (x - 2 if x < 64 else x + 2, 80))


def _blades(c):
    for flip in (False, True):
        pts = [(36, 30), (42, 26), (90, 86), (86, 92)]
        if flip:
            pts = sample.mirror(pts, 64)
        c.poly(IRON, *pts, bevel=1.0)
        hx, hy = (86, 90) if not flip else (42, 90)
        c.line(LEATHER, 5, (hx - 6 if not flip else hx + 6, hy - 6), (hx + 6 if not flip else hx - 6, hy + 6))
    c.ell(m("#d8cfc0", .1, 2), 64, 50, 12, 13, bevel=1.4)
    c.ell(m("#2a2624", .2), 59, 49, 3, 3)
    c.ell(m("#2a2624", .2), 69, 49, 3, 3)


def _mon(c):
    """Five-petal crest in a ring, the kind painted on Yamato banners and armour."""
    white = m("#efe9dc", .05, 2)
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        cx, cy = 64 + 15 * math.cos(a), 56 + 15 * math.sin(a)
        c.ell(white, cx, cy, 11, 11, bevel=1.4)
    c.ell(GOLD, 64, 56, 7, 7, bevel=1.4)
    for i in range(5):
        a = -math.pi / 2 + (i + .5) * 2 * math.pi / 5
        c.line(m("#8e2a24", .1), 1.4, (64 + 8 * math.cos(a), 56 + 8 * math.sin(a)), (64 + 22 * math.cos(a), 56 + 22 * math.sin(a)))


def _raven(c):
    """A raven in flight, wings raised, as on the old banners."""
    body = m("#1d1f24", .08, 2, spec=.5)
    feather = m("#2e323a", .08, 2, spec=.5)
    c.poly(feather, (60, 60), (54, 44), (50, 32), (60, 34), (70, 44), (74, 58), bevel=1.2)
    c.poly(body, (40, 64), (56, 58), (76, 60), (86, 68), (82, 76), (66, 82), (52, 82), (40, 90), (34, 96), (36, 86), (30, 84), (38, 74), bevel=1.8)
    c.ell(body, 86, 64, 8, 7, bevel=1.6)
    c.poly(m("#3a3a3e", .08, spec=.6), (91, 61), (100, 66), (91, 68), bevel=1.0)
    c.ell(m("#d9c27a", .1), 88, 62, 1.6, 1.6)
    c.poly(body, (54, 64), (44, 50), (36, 38), (32, 28), (44, 32), (58, 42), (70, 56), bevel=1.6)
    for x, y in ((34, 30), (38, 36), (42, 42), (47, 48)):
        c.scratch(.9, .45, (x + 6, y + 6), (x, y), color=(.32, .34, .38))
    c.line(m("#3a3a3e", .1), 1.6, (60, 82), (62, 92))
    c.line(m("#3a3a3e", .1), 1.6, (66, 81), (70, 91))


EMBLEMS = {"eagle": _eagle, "blades": _blades, "mon": _mon, "raven": _raven}


def render_all(only=None):
    import heirs_art as registry  # when run as a script this module is __main__; heirs_art2 registers into the imported copy
    import heirs_art2  # noqa: F401
    import heirs_art3  # noqa: F401
    import heirs_art4  # noqa: F401
    import heirs_art5  # noqa: F401
    import heirs_art6  # noqa: F401
    import heirs_art7  # noqa: F401
    import heirs_art8  # noqa: F401
    import heirs_art9  # noqa: F401
    import heirs_art10  # noqa: F401
    import heirs_art11  # noqa: F401
    import heirs_art12  # noqa: F401
    import heirs_art13  # noqa: F401
    import heirs_art14  # noqa: F401
    import heirs_art15  # noqa: F401
    import heirs_art16  # noqa: F401
    import heirs_art17  # noqa: F401
    import heirs_art18  # noqa: F401
    import heirs_art19  # noqa: F401
    import heirs_art20  # noqa: F401
    import heirs_art21  # noqa: F401
    PAINTERS.update(registry.PAINTERS)
    data.load_all()
    done = 0
    for path, (name, args) in data.TEXTURES.items():
        if only and only not in path:
            continue
        fn = PAINTERS[name]
        img = fn(**args)
        out = os.path.join(ROOT, *path.split("/")) + ".png"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        img.save(out, optimize=True)
        done += 1
    print("textures:", done)


def prune():
    """Deletes texture files that no longer belong to any registered path."""
    want = {os.path.normcase(os.path.join(ROOT, *p.split("/")) + ".png") for p in data.TEXTURES}
    removed = 0
    for folder, _, files in os.walk(os.path.join(ROOT, "HeirsOfEarth")):
        for f in files:
            full = os.path.normcase(os.path.join(folder, f))
            if full not in want:
                os.remove(full)
                removed += 1
    print("pruned:", removed)


if __name__ == "__main__":
    render_all(sys.argv[1] if len(sys.argv) > 1 else None)
    if len(sys.argv) == 1:
        prune()
