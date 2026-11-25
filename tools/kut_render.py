"""Small material renderer: every shape gets lighting, volume, surface grain, contact shadow and an inked outline."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 3
INK = np.array((34, 26, 20), dtype=np.float32) / 255


def rgb(value):
    value = value.lstrip("#")
    return np.array([int(value[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255


class Mat:
    def __init__(self, color, noise=.10, scale=5, stretch=(1, 1), spec=0.0, tint=None):
        self.color, self.noise, self.scale, self.stretch, self.spec = rgb(color), noise, scale, stretch, spec
        self.tint = rgb(tint) if tint else None


FELT = Mat("#c9b892", .10, 3)
FELT_D = Mat("#a08d6c", .12, 3)
WOOD = Mat("#7a5233", .20, 3, (9, 1))
WOOD_V = Mat("#7a5233", .20, 3, (1, 9))
WOOD_D = Mat("#4e3423", .18, 3, (9, 1))
STONE = Mat("#a2927a", .15, 5, tint="#857460")
STONE_L = Mat("#bfb098", .12, 5, tint="#a4957d")
STONE_D = Mat("#6d6152", .16, 4)
MARBLE = Mat("#d6d0c3", .06, 9, tint="#bdb5a6")
TILE = Mat("#2f8582", .10, 3, spec=.5, tint="#23696c")
TILE_B = Mat("#27507f", .08, 3, spec=.5)
IRON = Mat("#7f868a", .07, 3, (7, 1), spec=.8)
STEEL = Mat("#b4bbbf", .05, 3, (9, 1), spec=1.1)
DARKIRON = Mat("#474c50", .08, 3, spec=.5)
BRONZE = Mat("#a2763a", .09, 3, spec=.9, tint="#7f5a2c")
GOLD = Mat("#c6983f", .07, 2, spec=1.1)
LEATHER = Mat("#6a4529", .13, 2)
LEATHER_D = Mat("#43291a", .12, 2)
RED = Mat("#8c2f2a", .11, 2)
RED_D = Mat("#5e1f20", .11, 2)
BLUE = Mat("#2d4a6d", .11, 2)
CREAM = Mat("#d9cdb2", .07, 2)
BLACK = Mat("#1f1b1a", .06, 2)
EMBER = Mat("#e0792c", .18, 2, tint="#ffcf6a")
GREEN = Mat("#476b45", .12, 2)


class Canvas:
    def __init__(self, w, h=None, seed=1):
        self.w, self.h = w, h or w
        self.W, self.H = self.w * SS, self.h * SS
        self.rgb = np.zeros((self.H, self.W, 3), dtype=np.float32)
        self.a = np.zeros((self.H, self.W), dtype=np.float32)
        self.rng = np.random.default_rng(seed)
        self.yy, self.xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)

    def noise(self, scale, stretch):
        out = np.zeros((self.H, self.W), dtype=np.float32)
        amp, total = 1.0, 0.0
        for octave in range(3):
            size = max(1.0, scale / (2 ** octave)) * SS
            sw, sh = max(2, int(self.W / (size * stretch[0]))), max(2, int(self.H / (size * stretch[1])))
            field = Image.fromarray((self.rng.random((sh, sw)) * 255).astype(np.uint8)).resize((self.W, self.H), Image.BICUBIC)
            out += (np.asarray(field, dtype=np.float32) / 127.5 - 1) * amp
            total += amp
            amp *= .55
        return out / total

    def _mask(self, painter):
        img = Image.new("L", (self.W, self.H), 0)
        painter(ImageDraw.Draw(img))
        return img

    def poly_mask(self, *points):
        return self._mask(lambda d: d.polygon([(x * SS, y * SS) for x, y in points], fill=255))

    def ellipse_mask(self, cx, cy, rx, ry):
        return self._mask(lambda d: d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=255))

    def rect_mask(self, a, b, c, e, r=0):
        return self._mask(lambda d: d.rounded_rectangle([a * SS, b * SS, c * SS, e * SS], radius=r * SS, fill=255))

    def line_mask(self, width, *points):
        def draw(d):
            pts = [(x * SS, y * SS) for x, y in points]
            d.line(pts, fill=255, width=max(1, int(width * SS)), joint="curve")
            for x, y in pts:
                r = width * SS / 2
                d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        return self._mask(draw)

    def paint(self, mask, mat, bevel=2.0, cyl=None, vert=.18, edge=.55, clip=False):
        m = np.asarray(mask, dtype=np.float32) / 255
        if clip:
            m = m * (self.a > .5)
        if m.max() <= 0:
            return
        h = np.asarray(mask.filter(ImageFilter.GaussianBlur(max(.6, bevel) * SS)), dtype=np.float32) / 255
        gy, gx = np.gradient(h)
        light = np.clip((gx * .75 + gy * .85) * bevel * SS * 1.9, -.42, .42)
        shade = 1 + light
        ys = np.where(m.any(axis=1))[0]
        top, bottom = ys[0], ys[-1] + 1
        shade *= 1 + vert * (.5 - np.clip((self.yy - top) / max(1, bottom - top), 0, 1))
        if cyl:
            t = np.clip((self.xx / SS - cyl[0]) / max(1, cyl[1] - cyl[0]), 0, 1)
            shade *= .58 + .62 * np.clip(np.sin(np.pi * t ** .78), 0, 1) ** .8
        grain = self.noise(mat.scale, mat.stretch)
        color = np.repeat(mat.color[None, None], self.H, 0).repeat(self.W, 1).copy()
        if mat.tint is not None:
            blend = np.clip(self.noise(mat.scale * 5, (1, 1)) * 1.4 + .35, 0, 1)[..., None]
            color = color * (1 - blend * .6) + mat.tint * blend * .6
        color = color * (1 + grain[..., None] * mat.noise * 1.6) * shade[..., None]
        if mat.spec:
            color += np.clip(light + (shade - 1) * .4, 0, 1)[..., None] * mat.spec * .9
        inner = np.asarray(mask.filter(ImageFilter.MinFilter(2 * max(1, SS // 2) + 1)), dtype=np.float32) / 255
        ring = np.clip(m - inner, 0, 1)[..., None] * edge
        color = color * (1 - ring) + INK * ring
        alpha = m[..., None]
        self.rgb = self.rgb * (1 - alpha) + np.clip(color, 0, 1) * alpha
        self.a = np.maximum(self.a, m)

    def shadow(self, mask, dx=2, dy=3, blur=3, strength=.45):
        s = Image.fromarray(np.asarray(mask, dtype=np.uint8)).transform((self.W, self.H), Image.AFFINE, (1, 0, -dx * SS, 0, 1, -dy * SS)).filter(ImageFilter.GaussianBlur(blur * SS))
        v = np.asarray(s, dtype=np.float32)[..., None] / 255 * strength * (self.a[..., None] > 0)
        self.rgb = self.rgb * (1 - v)

    def poly(self, mat, *points, **kw):
        m = self.poly_mask(*points)
        self.paint(m, mat, **kw)
        return m

    def ell(self, mat, cx, cy, rx, ry, **kw):
        m = self.ellipse_mask(cx, cy, rx, ry)
        self.paint(m, mat, **kw)
        return m

    def rect(self, mat, a, b, c, e, r=0, **kw):
        m = self.rect_mask(a, b, c, e, r)
        self.paint(m, mat, **kw)
        return m

    def line(self, mat, width, *points, **kw):
        kw.setdefault("bevel", max(.7, width * .35))
        m = self.line_mask(width, *points)
        self.paint(m, mat, **kw)
        return m

    def scratch(self, width, opacity, *points, color=(0.09, 0.07, 0.05)):
        m = np.asarray(self.line_mask(width, *points).filter(ImageFilter.GaussianBlur(.35 * SS)), dtype=np.float32)[..., None] / 255 * opacity * (self.a[..., None] > .3)
        self.rgb = self.rgb * (1 - m) + np.array(color, dtype=np.float32) * m

    def glow(self, cx, cy, r, color="#ffb648", strength=.8):
        d = np.hypot(self.xx / SS - cx, self.yy / SS - cy) / r
        v = np.clip(1 - d, 0, 1)[..., None] ** 2 * strength * (self.a[..., None] > .3)
        self.rgb = np.clip(self.rgb + rgb(color) * v, 0, 1)

    def image(self, outline=1.3):
        alpha = Image.fromarray((np.clip(self.a, 0, 1) * 255).astype(np.uint8))
        grown = alpha.filter(ImageFilter.MaxFilter(2 * max(1, int(outline * SS)) + 1)).filter(ImageFilter.GaussianBlur(.5 * SS))
        out = np.asarray(grown, dtype=np.float32) / 255
        a = self.a[..., None]
        color = self.rgb * a + INK * (1 - a)
        rgba = np.dstack([np.clip(color, 0, 1), np.maximum(out, self.a)])
        return Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").resize((self.w, self.h), Image.LANCZOS)


def arc(cx, cy, rx, ry, start, end, n=40):
    return [(cx + rx * math.cos(math.radians(start + (end - start) * i / n)), cy + ry * math.sin(math.radians(start + (end - start) * i / n))) for i in range(n + 1)]


def pointed_arch(x, base, half, spring, peak):
    left = [(x - half + half * (1 - math.cos(t / 12 * math.pi / 2)) * .98, spring - (spring - peak) * math.sin(t / 12 * math.pi / 2)) for t in range(13)]
    right = [(2 * x - a, b) for a, b in reversed(left)]
    return [(x - half, base)] + left + right + [(x + half, base)]


def volumize(path_or_image, seed=3, bevel=2.2):
    """Gives existing flat art lighting, grain and an inked outline."""
    src = path_or_image.convert("RGBA") if isinstance(path_or_image, Image.Image) else Image.open(path_or_image).convert("RGBA")
    c = Canvas(src.width, src.height, seed)
    big = src.resize((c.W, c.H), Image.BICUBIC)
    arr = np.asarray(big, dtype=np.float32) / 255
    alpha = big.getchannel("A")
    h = np.asarray(big.convert("L").filter(ImageFilter.GaussianBlur(bevel * SS * .6)), dtype=np.float32) / 255 * .6 + np.asarray(alpha.filter(ImageFilter.GaussianBlur(bevel * SS)), dtype=np.float32) / 255
    gy, gx = np.gradient(h)
    shade = 1 + np.clip((gx * .75 + gy * .85) * bevel * SS * 2.2, -.4, .4)
    muted = arr[..., :3] * .84 + arr[..., :3].mean(axis=2, keepdims=True) * .16
    c.rgb = np.clip(muted * .92 * (1 + c.noise(2.5, (1, 1))[..., None] * .13) * shade[..., None], 0, 1)
    c.a = arr[..., 3]
    return c.image(1.0)
