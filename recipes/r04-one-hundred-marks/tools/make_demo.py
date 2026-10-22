"""Draw twelve plain demo shapes as PNGs, so the pipeline runs end to end without anyone's logos.

py make_demo.py <out folder>   ->  <out>/01.png ... 12.png, plus <out>/captions.json and <out>/order.json
Swap these for your own marks, icons or silhouettes: any PNG, WebP or JPG with dark ink on a light ground.
"""
import json, math, sys
from pathlib import Path

from PIL import Image, ImageDraw

S = 640


def poly(d, pts):
    d.polygon([(S / 2 + x * S * 0.4, S / 2 + y * S * 0.4) for x, y in pts], fill="black")


def star(k, inner):
    return [((1 if i % 2 == 0 else inner) * math.sin(math.pi * i / k), -(1 if i % 2 == 0 else inner) * math.cos(math.pi * i / k))
            for i in range(2 * k)]


def ngon(k, rot=0.0):
    return [(math.sin(2 * math.pi * i / k + rot), -math.cos(2 * math.pi * i / k + rot)) for i in range(k)]


def heart():
    return [(16 * math.sin(t) ** 3 / 17, -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17)
            for t in [i / 200 * 2 * math.pi for i in range(200)]]


def flower(k=6):
    return [((0.62 + 0.38 * math.cos(k * t)) * math.sin(t), -(0.62 + 0.38 * math.cos(k * t)) * math.cos(t))
            for t in [i / 400 * 2 * math.pi for i in range(400)]]


def drop():
    return [(0.75 * math.sin(t) * (1 - math.cos(t)) / 2 * 1.6, -math.cos(t)) for t in [i / 200 * 2 * math.pi for i in range(200)]]


SHAPES = [
    ("Circle", lambda d: d.ellipse((S * 0.1, S * 0.1, S * 0.9, S * 0.9), fill="black")),
    ("Triangle", lambda d: poly(d, ngon(3))),
    ("Star", lambda d: poly(d, star(5, 0.42))),
    ("Heart", lambda d: poly(d, heart())),
    ("Square", lambda d: poly(d, ngon(4, math.pi / 4))),
    ("Flower", lambda d: poly(d, flower())),
    ("Cross", lambda d: poly(d, [(-0.3, -1), (0.3, -1), (0.3, -0.3), (1, -0.3), (1, 0.3), (0.3, 0.3), (0.3, 1), (-0.3, 1), (-0.3, 0.3), (-1, 0.3), (-1, -0.3), (-0.3, -0.3)])),
    ("Hexagon", lambda d: poly(d, ngon(6))),
    ("Drop", lambda d: poly(d, drop())),
    ("Arrow", lambda d: poly(d, [(-1, -0.28), (0.2, -0.28), (0.2, -0.75), (1, 0), (0.2, 0.75), (0.2, 0.28), (-1, 0.28)])),
    ("Sun", lambda d: poly(d, star(12, 0.72))),
    ("House", lambda d: poly(d, [(-0.8, 1), (-0.8, -0.1), (0, -0.9), (0.8, -0.1), (0.8, 1), (0.25, 1), (0.25, 0.4), (-0.25, 0.4), (-0.25, 1)])),
]

if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    order, caps = [], {}
    for i, (name, draw) in enumerate(SHAPES, 1):
        im = Image.new("RGB", (S, S), "white")
        draw(ImageDraw.Draw(im))
        key = f"{i:02d}"
        im.save(out / f"{key}.png")
        order.append(key); caps[key] = f"{key} · {name} · Demo shape"
    (out / "order.json").write_text(json.dumps(order))
    (out / "captions.json").write_text(json.dumps(caps, indent=0))
    print(len(order), "demo shapes ->", out)
