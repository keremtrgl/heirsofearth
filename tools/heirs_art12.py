"""Heirs of Earth 3.2: the new floors. Every painter draws on a 1024 canvas whose pattern repeats exactly at its edges,
then heirs_art.finish_floor scales it to a seamless 512x512 texture."""
import math

import numpy as np
from PIL import ImageDraw, ImageFilter

from heirs_art import finish_floor, floor_canvas, painter, shade


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


@painter
def floor_slabs(base="#a8a296", joint="#5e5850", cols=4, rows=8, stagger=True, vein=None, moss=None, seed=1, speck=None):
    """Running-bond slabs: stone paving, marble, sandstone, adobe."""
    b, j = _rgb(base), _rgb(joint)
    img, d, rng = floor_canvas(j, seed)
    w, h = 1024 // cols, 1024 // rows
    for r in range(rows):
        off = (w // 2) if stagger and r % 2 else 0
        for ci in range(cols + 1):
            x0, y0 = ci * w - off, r * h
            col = shade(b, rng.uniform(.9, 1.08))
            for dx in (0, 1024, -1024):
                d.rectangle((x0 + 6 + dx, y0 + 6, x0 + w - 6 + dx, y0 + h - 6), fill=col)
                d.line((x0 + 8 + dx, y0 + 8, x0 + w - 8 + dx, y0 + 8), fill=shade(col, 1.12), width=3)
                d.line((x0 + 8 + dx, y0 + h - 8, x0 + w - 8 + dx, y0 + h - 8), fill=shade(col, .84), width=3)
            if vein:
                v = _rgb(vein)
                for _ in range(2):
                    px, py = x0 + rng.uniform(10, w - 10), y0 + rng.uniform(10, h - 10)
                    pts = [(px, py)]
                    for _ in range(6):
                        px += rng.uniform(-30, 30)
                        py += rng.uniform(-12, 12)
                        pts.append((min(max(px, x0 + 8), x0 + w - 8), min(max(py, y0 + 8), y0 + h - 8)))
                    for dx in (0, 1024, -1024):
                        d.line([(p[0] + dx, p[1]) for p in pts], fill=v, width=2)
            if speck:
                s = _rgb(speck)
                for _ in range(30):
                    px, py = x0 + rng.uniform(10, w - 10), y0 + rng.uniform(10, h - 10)
                    for dx in (0, 1024, -1024):
                        d.line((px + dx, py, px + dx + rng.uniform(-6, 6), py + rng.uniform(-2, 2)), fill=s, width=2)
    if moss:
        mo = _rgb(moss)
        for _ in range(90):
            x, y = rng.uniform(0, 1024), rng.uniform(0, 1024)
            x = round(x / w) * w - (w // 2 if stagger and int(y // h) % 2 else 0) + rng.uniform(-6, 6)
            r = rng.uniform(3, 8)
            for dx in (0, 1024, -1024):
                d.ellipse((x - r + dx, y - r, x + r + dx, y + r), fill=shade(mo, rng.uniform(.8, 1.1)))
    return finish_floor(img.filter(ImageFilter.GaussianBlur(1.0)), seed, 3.0)


@painter
def floor_flags(base="#5e646a", joint="#2e3034", seed=2):
    """Irregular split flagstones (slate)."""
    b, j = _rgb(base), _rgb(joint)
    img, d, rng = floor_canvas(j, seed)
    n = 6
    cell = 1024 / n
    pts = {}
    for i in range(n):
        for k in range(n):
            pts[(i, k)] = (i * cell + rng.uniform(-28, 28), k * cell + rng.uniform(-28, 28))
    for i in range(n):
        for k in range(n):
            quad = [pts[(i, k)], pts[((i + 1) % n, k)], pts[((i + 1) % n, (k + 1) % n)], pts[(i, (k + 1) % n)]]
            quad = [(quad[0][0], quad[0][1]),
                    (quad[1][0] + (1024 if i + 1 == n else 0), quad[1][1]),
                    (quad[2][0] + (1024 if i + 1 == n else 0), quad[2][1] + (1024 if k + 1 == n else 0)),
                    (quad[3][0], quad[3][1] + (1024 if k + 1 == n else 0))]
            cx, cy = sum(p[0] for p in quad) / 4, sum(p[1] for p in quad) / 4
            inner = [(cx + (p[0] - cx) * .9, cy + (p[1] - cy) * .9) for p in quad]
            col = shade(b, rng.uniform(.82, 1.12))
            for dx in (0, 1024, -1024):
                for dy in (0, 1024, -1024):
                    d.polygon([(p[0] + dx, p[1] + dy) for p in inner], fill=col)
                    d.line([(p[0] + dx, p[1] + dy) for p in inner[:2]], fill=shade(col, 1.15), width=3)
            for _ in range(4):
                a = rng.uniform(0, math.pi)
                L = rng.uniform(10, 30)
                for dx in (0, 1024, -1024):
                    for dy in (0, 1024, -1024):
                        d.line((cx + dx, cy + dy, cx + dx + L * math.cos(a), cy + dy + L * math.sin(a)), fill=shade(col, .9), width=2)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(1.0)), seed, 3.5)


@painter
def floor_herringbone(base="#8a5a32", joint="#3e2818", width=32, seed=3, grain=True):
    """Herringbone parquet or brick: an L-pair of 2:1 blocks repeated on the lattice (w, w), (2w, -2w), which tiles the plane exactly."""
    b, j = _rgb(base), _rgb(joint)
    img, d, rng = floor_canvas(j, seed)
    W, L, N = width, 2 * width, 1024
    seen = set()
    for i in range(N // W):
        for k in range(N // L):
            ox, oy = (i * W + k * L) % N, (i * W - k * L) % N
            if (ox, oy) in seen:
                continue
            seen.add((ox, oy))
            for x0, y0, w, h in ((ox, oy, L, W), (ox, oy + W, W, L)):
                col = shade(b, rng.uniform(.86, 1.12))
                for ex in (0, N, -N):
                    for ey in (0, N, -N):
                        r = (x0 + ex + 2, y0 + ey + 2, x0 + ex + w - 2, y0 + ey + h - 2)
                        if r[2] < 0 or r[3] < 0 or r[0] > N or r[1] > N:
                            continue
                        d.rectangle(r, fill=col)
                        d.line((r[0], r[1], r[2], r[1]), fill=shade(col, 1.12), width=2)
                        if grain:
                            for g in (1, 2):
                                if w > h:
                                    yy = r[1] + g * h / 3
                                    d.line((r[0] + 3, yy, r[2] - 3, yy + rng.uniform(-1.5, 1.5)), fill=shade(col, .9), width=1)
                                else:
                                    xx = r[0] + g * w / 3
                                    d.line((xx, r[1] + 3, xx + rng.uniform(-1.5, 1.5), r[3] - 3), fill=shade(col, .9), width=1)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(.8)), seed, 2.5)


@painter
def floor_boards(base="#7a3a24", joint="#2a1410", boards=8, seed=4, carve=None, spec=None):
    """Long boards with butt joints; optional carved knots (Nord) or lacquer shine (Tianxia)."""
    b, j = _rgb(base), _rgb(joint)
    img, d, rng = floor_canvas(j, seed)
    h = 1024 // boards
    for r in range(boards):
        y0 = r * h
        cut = rng.integers(1, 4) * 256
        for x0, x1 in ((cut - 1024, cut), (cut, cut + 1024)):
            col = shade(b, rng.uniform(.9, 1.08))
            for dx in (0, 1024, -1024):
                d.rectangle((x0 + 3 + dx, y0 + 3, x1 - 3 + dx, y0 + h - 3), fill=col)
                for g in range(5):
                    yy = y0 + 10 + g * (h - 20) / 4
                    d.line((x0 + 6 + dx, yy, x1 - 6 + dx, yy + rng.uniform(-3, 3)), fill=shade(col, .92), width=2)
                if spec:
                    d.line((x0 + 8 + dx, y0 + 10, x1 - 8 + dx, y0 + 10), fill=shade(col, 1.35), width=4)
        if carve:
            cv = _rgb(carve)
            for _ in range(2):
                cx, cy = rng.uniform(60, 960), y0 + h / 2
                for dx in (0, 1024, -1024):
                    for k in range(3):
                        a = k * 2.1
                        d.arc((cx - 18 + dx, cy - 18, cx + 18 + dx, cy + 18), math.degrees(a), math.degrees(a) + 140, fill=cv, width=4)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(.8)), seed, 2.5)


@painter
def floor_pebbles(ground="#c8b89a", colors=("#2a2a2a", "#e8e2d6"), pattern="wave", border=None, seed=5):
    """Pebble mosaic: small stones set in mortar, laid in a wave (Hellas) or a quatrefoil (Pars garden) pattern."""
    g = _rgb(ground)
    img, d, rng = floor_canvas(g, seed)
    cols = [_rgb(c) for c in colors]
    step = 22
    for yi in range(1024 // step):
        for xi in range(1024 // step):
            x = xi * step + step / 2 + rng.uniform(-3, 3)
            y = yi * step + step / 2 + rng.uniform(-3, 3)
            u, v = (xi * step) / 1024.0, (yi * step) / 1024.0
            if pattern == "wave":
                band = (v * 4) % 1
                k = 1 if abs(band - (.5 + .22 * math.sin(u * 4 * 2 * math.pi))) < .14 else 0
            else:
                cu, cv = (u * 4 % 1) - .5, (v * 4 % 1) - .5
                k = 1 if (abs(cu) + abs(cv) < .32 or (cu * cu + cv * cv) < .02) else 0
            col = shade(cols[k], rng.uniform(.85, 1.12))
            r = rng.uniform(7, 10)
            d.ellipse((x - r, y - r * .8, x + r, y + r * .8), fill=col)
            d.arc((x - r, y - r * .8, x + r, y + r * .8), 200, 320, fill=shade(col, 1.25), width=2)
    if border:
        bc = _rgb(border)
        for k in range(4):
            d.line((0, k * 256, 1024, k * 256), fill=bc, width=8)
            d.line((k * 256, 0, k * 256, 1024), fill=bc, width=8)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(.7)), seed, 2.5)


@painter
def floor_glazed(base="#1f6e8a", star="#e8d8a8", ground="#f2ece0", seed=6):
    """Glazed tiles: eight-pointed stars on turquoise, cross tiles between (Pars)."""
    img, d, rng = floor_canvas(_rgb(ground), seed)
    cell = 256
    b, s = _rgb(base), _rgb(star)
    for yi in range(4):
        for xi in range(4):
            cx, cy = xi * cell + cell / 2, yi * cell + cell / 2
            col = shade(b, rng.uniform(.92, 1.06))
            d.rectangle((xi * cell + 3, yi * cell + 3, xi * cell + cell - 3, yi * cell + cell - 3), fill=col)
            pts = []
            for k in range(16):
                a = k * math.pi / 8
                r = 104 if k % 2 == 0 else 60
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            d.polygon(pts, fill=shade(s, rng.uniform(.95, 1.05)))
            d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=shade(b, .8))
            d.line((xi * cell + 10, yi * cell + 10, xi * cell + 50, yi * cell + 10), fill=shade(col, 1.4), width=3)
    return finish_floor(img.filter(ImageFilter.GaussianBlur(.7)), seed, 2.0)


@painter
def floor_polygonal(base="#9a9488", joint="#4a463e", seed=7):
    """Fitted polygonal masonry: many-sided stones with tight joints and pillowed faces (Inti)."""
    b, j = _rgb(base), _rgb(joint)
    img, d, rng = floor_canvas(j, seed)
    n = 5
    cell = 1024 / n
    centers = {(i, k): (i * cell + cell / 2 + rng.uniform(-30, 30), k * cell + cell / 2 + rng.uniform(-30, 30)) for i in range(n) for k in range(n)}
    arr = np.zeros((1024, 1024), dtype=np.int32)
    ys, xs = np.mgrid[0:1024, 0:1024]
    best = np.full((1024, 1024), 1e9)
    idx = 0
    lut = []
    for (i, k), (cx, cy) in centers.items():
        for dx in (0, 1024, -1024):
            for dy in (0, 1024, -1024):
                dist = np.abs(xs - cx - dx) ** 1.6 + np.abs(ys - cy - dy) ** 1.6
                mask = dist < best
                best = np.where(mask, dist, best)
                arr = np.where(mask, idx, arr)
        lut.append(shade(b, rng.uniform(.84, 1.12)))
        idx += 1
    out = np.zeros((1024, 1024, 3), dtype=np.float32)
    lut = np.array(lut, dtype=np.float32)
    out[:] = lut[arr]
    edge = (np.roll(arr, 1, 0) != arr) | (np.roll(arr, 1, 1) != arr) | (np.roll(arr, -1, 0) != arr) | (np.roll(arr, -1, 1) != arr)
    edge = edge | np.roll(edge, 2, 0) | np.roll(edge, 2, 1)
    out[edge] = j
    from PIL import Image
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")
    return finish_floor(img.filter(ImageFilter.GaussianBlur(1.4)), seed, 3.5)
