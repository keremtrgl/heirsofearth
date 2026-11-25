"""Heirs of Earth: Steam preview (1280x720) and mod icon (256x256).

The nation shields are re-rendered at four times their in-game resolution so they stay sharp.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import kut_render
import heirs_art
import heirs_art4  # noqa: F401  (owl, dragon and lion emblems)
import heirs_art6  # noqa: F401  (falcon)
import heirs_art7  # noqa: F401  (griffin)
import heirs_art8  # noqa: F401  (condor)
from heirs_art import GOLD, Canvas, m

ABOUT = Path(__file__).resolve().parent.parent / "HeirsOfEarth" / "About"
SERIF_B = "C:/Windows/Fonts/georgiab.ttf"
SERIF = "C:/Windows/Fonts/georgia.ttf"
W, H = 1280, 720


def hires(fn, k=4, **kw):
    """Runs a 128px painter at k times the size by enlarging the canvas output instead of shrinking it."""
    old_ss, old_image = kut_render.SS, Canvas.image

    def big(self, outline=1.3):
        alpha = Image.fromarray((np.clip(self.a, 0, 1) * 255).astype(np.uint8))
        grown = alpha.filter(ImageFilter.MaxFilter(2 * max(1, int(outline * kut_render.SS)) + 1)).filter(ImageFilter.GaussianBlur(.5 * kut_render.SS))
        out = np.asarray(grown, dtype=np.float32) / 255
        a = self.a[..., None]
        color = self.rgb * a + kut_render.INK * (1 - a)
        rgba = np.dstack([np.clip(color, 0, 1), np.maximum(out, self.a)])
        return Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").resize((self.w * k, self.h * k), Image.LANCZOS)

    kut_render.SS = 8
    Canvas.image = big
    try:
        return fn(**kw)
    finally:
        kut_render.SS = old_ss
        Canvas.image = old_image


def background(w, h, seed=7):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    top, bottom = np.array([14, 22, 38]), np.array([46, 38, 30])
    t = (y / h)[..., None]
    img = top * (1 - t) + bottom * t
    # soft continents: blurred noise thresholded into land, tinted like an old chart
    f = np.zeros((h, w), dtype=np.float32)
    for cell, amp in ((160, 1.0), (60, .35), (22, .12)):
        n = Image.fromarray((rng.random((h // cell + 2, w // cell + 2)) * 255).astype(np.uint8)).resize((w + cell * 2, h + cell * 2), Image.BICUBIC)
        f += np.asarray(n, dtype=np.float32)[cell:cell + h, cell:cell + w] / 255 * amp
    f /= 1.47
    land = np.clip((f - .53) * 12, 0, 1)[..., None]
    img = img * (1 - land * .45) + np.array([86, 72, 50]) * land * .45
    coast = np.clip(1 - np.abs(f - .53) * 60, 0, 1)[..., None]
    img = img * (1 - coast * .22) + np.array([196, 160, 96]) * coast * .22
    grain = rng.normal(0, 5, (h, w, 1))
    img = np.clip(img + grain, 0, 255)
    out = Image.fromarray(img.astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(out, "RGBA")
    for i in range(1, 6):
        yy = h * i / 6
        d.line([(0, yy), (w, yy)], fill=(214, 182, 112, 12), width=1)
    for i in range(-6, 7):
        pts = [(w / 2 + i * 120 * math.cos(math.asin(max(-1, min(1, (yy - h / 2) / (h * .9))))), yy) for yy in range(0, h + 1, 12)]
        d.line(pts, fill=(214, 182, 112, 12), width=1)
    # vignette
    cx, cy = w / 2, h / 2
    r = np.hypot((x - cx) / (w * .62), (y - cy) / (h * .62))
    v = np.clip((r - .55) * 1.4, 0, .85)
    shade = Image.fromarray((v * 255).astype(np.uint8))
    black = Image.new("RGBA", (w, h), (6, 6, 10, 255))
    out = Image.composite(black, out, shade)
    return out


def text(img, xy, s, size, font=SERIF_B, fill=(232, 198, 120), anchor="mm", shadow=6, spacing=0):
    f = ImageFont.truetype(font, size)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if spacing:
        s = (" " * spacing).join(s)
    d.text((xy[0] + 3, xy[1] + 4), s, font=f, fill=(0, 0, 0, 200), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(shadow))
    d = ImageDraw.Draw(layer)
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=max(1, size // 30), stroke_fill=(60, 40, 18))
    img.alpha_composite(layer)


def glow(img, cx, cy, r, color, strength):
    y, x = np.mgrid[0:img.size[1], 0:img.size[0]].astype(np.float32)
    v = np.clip(1 - np.hypot(x - cx, y - cy) / r, 0, 1) ** 2 * strength
    layer = Image.new("RGBA", img.size, color)
    layer.putalpha(Image.fromarray((v * 255).astype(np.uint8)))
    img.alpha_composite(layer)


def preview():
    img = background(W, H)
    glow(img, W / 2, 400, 520, (255, 196, 110, 255), .22)
    nations = [("#8e2a24", "eagle", "NOVA ROMA"), ("#2b3654", "mon", "YAMATO"), ("#3a5562", "raven", "NORDHEIM"),
               ("#2e5c8c", "owl", "HELLAS"), ("#9c2a20", "dragon", "TIANXIA"), ("#8c1c22", "lion", "ALBION"),
               ("#c99e3c", "falcon", "KEMET"), ("#9e1f2b", "griffin", "PARS"), ("#c74f29", "condor", "INTI")]
    size, gap = 128, 136
    mid = (len(nations) - 1) / 2
    xs = [W / 2 + (i - mid) * gap for i in range(len(nations))]
    for i, ((color, emblem, name), x) in enumerate(zip(nations, xs)):
        shield = hires(heirs_art.nation_icon, 4, color=color, emblem=emblem).resize((size, size), Image.LANCZOS)
        sh = Image.new("RGBA", shield.size, (0, 0, 0, 0))
        sh.putalpha(shield.split()[3].filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * .7)))
        lift = abs(i - mid) ** 2 * 4.5
        top = 318 + lift
        img.alpha_composite(sh, (int(x - size / 2 + 8), int(top + 12)))
        img.alpha_composite(shield, (int(x - size / 2), int(top)))
        text(img, (x, top + size + 14), name, 17, SERIF_B, (226, 206, 160), shadow=4, spacing=1)
    text(img, (W / 2, 120), "HEIRS OF EARTH", 96, SERIF_B, (240, 204, 120), shadow=10)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(W / 2 - 300, 186), (W / 2 - 40, 186)], fill=(214, 172, 96, 200), width=2)
    d.line([(W / 2 + 40, 186), (W / 2 + 300, 186)], fill=(214, 172, 96, 200), width=2)
    d.polygon([(W / 2, 178), (W / 2 + 9, 186), (W / 2, 194), (W / 2 - 9, 186)], fill=(232, 190, 110, 230))
    text(img, (W / 2, 218), "the old nations live on", 30, SERIF, (220, 204, 170), shadow=4)
    img.convert("RGB").save(ABOUT / "Preview.png", optimize=True)
    img.convert("RGB").save(ABOUT.parent.parent / "workshop" / "Heirs_Steam" / "preview.jpg", quality=90, optimize=True)


def mod_icon():
    c = Canvas(128, seed=5)
    rim, sea, land = GOLD, m("#1c3350", .08, 3), m("#c9b27a", .12, 2)
    c.ell(m("#2a1c10", .1), 66, 68, 58, 58)
    c.ell(rim, 64, 64, 58, 58, bevel=2.6)
    c.ell(sea, 64, 64, 50, 50, bevel=1.6)
    # continents on a globe: soft coastlines from a wobbling radius
    rng = np.random.default_rng(11)
    for cx, cy, r in ((48, 46, 13), (80, 60, 15), (52, 84, 10), (86, 36, 6)):
        pts = []
        ph = rng.uniform(0, 6.3, 3)
        for k in range(36):
            a = k * 2 * math.pi / 36
            rr = r * (1 + .22 * math.sin(3 * a + ph[0]) + .12 * math.sin(5 * a + ph[1]) + .07 * math.sin(9 * a + ph[2]))
            pts.append((cx + rr * math.cos(a), cy + rr * .85 * math.sin(a)))
        c.poly(land, *pts, bevel=1.4)
    for k in (-30, 0, 30):
        pts = [(64 + k * math.cos(math.radians(a)), 64 + 50 * math.sin(math.radians(a))) for a in range(-90, 91, 6)]
        c.scratch(1.0, .35, *pts, color=(.85, .75, .5))
    for yy in (40, 64, 88):
        half = math.sqrt(max(0, 50 ** 2 - (yy - 64) ** 2))
        c.scratch(1.0, .3, (64 - half, yy), (64 + half, yy), color=(.85, .75, .5))
    c.glow(52, 50, 40, "#ffffff", .18)
    # engraved rim
    for r in (54.5, 61):
        pts = [(64 + r * math.cos(t), 64 + r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 90)]
        c.scratch(.9, .45, *pts, color=(.35, .24, .08))
    for k in range(24):
        t = k * 2 * math.pi / 24
        c.ell(m("#f0d080", .05, spec=1.0), 64 + 57.8 * math.cos(t), 64 + 57.8 * math.sin(t), 1.5, 1.5, bevel=.8)
    icon = hires(lambda: c.image(), 2)
    icon.resize((256, 256), Image.LANCZOS).save(ABOUT / "ModIcon.png", optimize=True)


if __name__ == "__main__":
    preview()
    mod_icon()
    print("preview and icon written")
