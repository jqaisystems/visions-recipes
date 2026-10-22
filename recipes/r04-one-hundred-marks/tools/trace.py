"""Trace logo images into one closed outline each, ready to morph.

Needs only numpy and Pillow:  py trace.py <images folder> <out.json> [--sheet sheet.png]
Each image becomes a silhouette: ink is thresholded, small gaps are closed, the symbol (the biggest blob
that isn't a line of text) is kept, its holes are filled and its outer edge is traced, smoothed and
resampled to N points, clockwise, centred, with its longest side scaled to 1.
"""
import json, math, sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

N = 600          # points per outline: every shape gets the same count so any one can morph into any other
WORK = 320       # images are traced at this size (longest side)
GAP = 7          # px at WORK size: strokes closer than this merge into one shape (odd)


def ink_mask(path):
    im = Image.open(path).convert("RGB")
    s = WORK / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    ink = (255 - a.min(axis=2)) > 60                        # anything darker or more coloured than paper
    pad = GAP * 2
    m = np.pad(ink, pad)
    return m


def close(m, k):
    img = Image.fromarray((m * 255).astype(np.uint8))
    img = img.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))
    return np.asarray(img) > 127


def dilate(m, k):
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(k))) > 127


def components(m):
    lab = np.zeros(m.shape, np.int32)
    h, w = m.shape
    comps = []
    for y, x in zip(*np.nonzero(m)):
        if lab[y, x]:
            continue
        idx = len(comps) + 1
        q = deque([(y, x)]); lab[y, x] = idx; pts = []
        while q:
            cy, cx = q.popleft(); pts.append((cy, cx))
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = idx; q.append((ny, nx))
        comps.append(np.array(pts))
    return lab, comps


def fill_holes(m):
    h, w = m.shape
    bg = np.zeros_like(m)
    q = deque()
    for y in range(h):
        for x in (0, w - 1):
            if not m[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if not m[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and not m[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; q.append((ny, nx))
    return ~bg


def symbol(m):
    """The biggest blob that isn't a line of text, with its holes filled."""
    merged = dilate(m, GAP)
    lab, comps = components(merged)
    best, best_score = None, -1
    for i, c in enumerate(comps):
        y0, x0 = c.min(0); y1, x1 = c.max(0)
        bh, bw = y1 - y0 + 1, x1 - x0 + 1
        if bh / bw < 0.33 or bh < 24:                       # a wordmark or tagline line
            continue
        score = len(c)
        if score > best_score:
            best, best_score = i + 1, score
    if best is None:
        return None
    blob = (lab == best) & close(m, GAP)
    return fill_holes(close(blob, GAP))


def trace(m):
    """Moore-neighbour trace of the outer edge; returns points in order."""
    ys, xs = np.nonzero(m)
    start = (ys.min(), xs[ys == ys.min()].min())
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    pts = [start]; cur = start; back = 6                     # came from the left
    for _ in range(200000):
        for k in range(8):
            d = (back + 1 + k) % 8
            ny, nx = cur[0] + dirs[d][0], cur[1] + dirs[d][1]
            if m[ny, nx]:
                back = (d + 4) % 8
                cur = (ny, nx)
                break
        else:
            break
        if cur == start:
            break
        pts.append(cur)
    return np.array([(x, y) for y, x in pts], float)


def smooth(p, r=3):
    out = np.zeros_like(p)
    for k in range(-r, r + 1):
        out += np.roll(p, k, 0)
    return out / (2 * r + 1)


def resample(p, n=N):
    q = np.vstack([p, p[:1]])
    seg = np.hypot(*np.diff(q, axis=0).T)
    t = np.concatenate([[0], np.cumsum(seg)])
    u = np.linspace(0, t[-1], n, endpoint=False)
    return np.stack([np.interp(u, t, q[:, 0]), np.interp(u, t, q[:, 1])], 1), t[-1]


def area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def hull_area(p):
    pts = sorted(map(tuple, p))
    def half(seq):
        h = []
        for q in seq:
            while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (q[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (q[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(q)
        return h
    h = half(pts)[:-1] + half(pts[::-1])[:-1]
    return abs(area(np.array(h)))


def outline(path):
    m = ink_mask(path)
    s = symbol(m)
    if s is None or s.sum() < 400:
        return None
    raw = smooth(trace(s))
    if len(raw) < 40:
        return None
    pts, perim = resample(raw)
    if area(pts) < 0:                                        # clockwise on screen (y down)
        pts = pts[::-1]
    a = abs(area(pts))
    lo, hi = pts.min(0), pts.max(0)
    pts = (pts - (lo + hi) / 2) / (hi - lo).max()
    return {
        "pts": np.round(pts, 4).tolist(),
        "solidity": round(a / hull_area(pts * (hi - lo).max()), 3),
        "circularity": round(4 * math.pi * a / perim ** 2, 3),
        "aspect": round(float((hi - lo)[1] / (hi - lo)[0]), 3),
    }


def sheet(shapes, out, cols=20, cell=96):
    from PIL import ImageDraw
    rows = math.ceil(len(shapes) / cols)
    im = Image.new("RGB", (cols * cell, rows * cell), "#F7F5F0"); d = ImageDraw.Draw(im)
    for i, s in enumerate(shapes):
        ox, oy = (i % cols) * cell + cell / 2, (i // cols) * cell + cell / 2 + 6
        pts = [(ox + x * cell * 0.7, oy + y * cell * 0.7) for x, y in s["pts"]]
        d.line(pts + pts[:1], fill="#151515", width=1)
        d.text(((i % cols) * cell + 3, (i // cols) * cell + 2), f"{s['id']}", fill="#888")
    im.save(out)


if __name__ == "__main__":
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    shapes = []
    for f in sorted(src.glob("*.*")):
        if f.suffix.lower() not in (".png", ".webp", ".jpg", ".jpeg"):
            continue
        o = outline(f)
        if o:
            shapes.append({"id": f.stem, **o})
    out.write_text(json.dumps(shapes))
    print(f"{len(shapes)} outlines -> {out}")
    if "--sheet" in sys.argv:
        sheet(shapes, sys.argv[sys.argv.index("--sheet") + 1])
