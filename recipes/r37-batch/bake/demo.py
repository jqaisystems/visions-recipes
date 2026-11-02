"""A demo batch so the recipe runs out of the box: ten concepts of generated patterns, each in 8 to 16 near-identical
takes, with a CSV in the uploader's format (Filename, Title, 46 lowercase keywords, Category). Only numpy and FFmpeg.
Writes assets/demo/ (not committed). Use your own folder and CSV instead for the real thing.
Usage: python bake/demo.py"""
import csv, os, subprocess, zlib
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "demo")
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = x / W, y / H
TEAL, ORANGE, CREAM, INK, BLUE = (np.array(c, np.float32) / 255 for c in [(63, 214, 192), (255, 138, 106), (244, 234, 214), (14, 22, 28), (60, 110, 200)])
mix = lambda a, b, t: a * (1 - t[..., None]) + b * t[..., None]

# each concept: a pattern, its words, its category; k is the take, 0..1
CONCEPTS = [
    ("stripes", 8, 8, ["stripes", "diagonal", "bands", "teal", "orange", "lines"],
     lambda k: mix(TEAL, ORANGE, 0.5 + 0.5 * np.sin((u * 9 + v * (4 + k)) * np.pi * 2 + k))),
    ("rings", 12, 8, ["rings", "circles", "concentric", "ripple", "radial", "target"],
     lambda k: mix(INK, CREAM, 0.5 + 0.5 * np.cos(np.hypot(u - 0.3 - 0.3 * k, (v - 0.5) * 0.56) * 70))),
    ("waves", 8, 11, ["waves", "sea", "horizon", "swell", "blue", "water"],
     lambda k: mix(BLUE, CREAM, np.clip((v - 0.45 - 0.05 * np.sin(u * 14 + k * 6)) * 6, 0, 1))),
    ("dots", 8, 8, ["dots", "polka", "grid", "spots", "round", "repeat"],
     lambda k: mix(CREAM, TEAL, (np.hypot((x % 120) - 60, (y % 120) - 60) < 18 + 22 * k).astype(np.float32))),
    ("dunes", 8, 11, ["dunes", "hills", "layers", "desert", "sand", "warm"],
     lambda k: mix(ORANGE, CREAM, np.clip((v - 0.3 - 0.12 * np.sin(u * 5 + k * 3) - 0.08 * np.sin(u * 13)) * 3, 0, 1))),
    ("sunset", 12, 11, ["sunset", "sky", "sun", "glow", "evening", "dusk"],
     lambda k: np.clip(mix(ORANGE, INK, v) + (np.hypot(u - 0.2 - 0.6 * k, (v - 0.55) * 0.56) < 0.06)[..., None] * 0.8, 0, 1)),
    ("checker", 8, 8, ["checker", "squares", "tiles", "warped", "board", "contrast"],
     lambda k: mix(INK, CREAM, (((x + 40 * np.sin(v * 9 + k * 4)) // 90 + (y // 90)) % 2).astype(np.float32))),
    ("blobs", 16, 8, ["blobs", "bubbles", "organic", "soft", "fluid", "shapes"],
     lambda k: mix(INK, TEAL, np.clip(sum(np.exp(-((u - 0.2 - 0.15 * i - 0.1 * np.sin(k * 6 + i)) ** 2 + ((v - 0.5 - 0.2 * np.cos(k * 4 + i)) * 0.56) ** 2) * 60) for i in range(5)), 0, 1))),
    ("honeycomb", 12, 8, ["honeycomb", "cells", "hexagon", "lattice", "mesh", "structure"],
     lambda k: mix(CREAM, ORANGE, np.clip(np.cos(x / 30 + k) + np.cos(x / 60 + y / 34) + np.cos(x / 60 - y / 34 + k * 2), -1, 1) * 0.5 + 0.5)),
    ("terrain", 8, 1, ["terrain", "contours", "topography", "relief", "map", "elevation"],
     lambda k: mix(INK, TEAL, 0.5 + 0.5 * np.sin((np.sin(u * 7 + k) + np.cos(v * 5 - k) + np.sin((u + v) * 11)) * 6))),
]
POOL = ("abstract pattern background texture design graphic digital modern minimal geometric smooth gradient bright calm "
        "clean simple colour colourful wallpaper backdrop surface layout shape form curve light shadow tone hue vivid "
        "decor print poster banner template copyspace horizontal wide creative contemporary decorative artistic "
        "flat composition balance harmony detail rhythm motion depth").split()
ADJ = ["Soft", "Bold", "Calm", "Bright", "Warm", "Cool", "Clean", "Vivid", "Quiet", "Deep", "Light", "Muted", "Rich", "Crisp", "Gentle", "Simple"]

rows = []
for name, n, cat, words, f in CONCEPTS:
    for j in range(n):
        img = (np.clip(f(j / max(n - 1, 1)), 0, 1) * 255).astype(np.uint8)
        # the uploader's filename shape: one prefix per concept, then a unique id, so the takes group into concepts
        fn = f"{name}_pattern_{zlib.crc32(name.encode()):08x}-{j:04x}-4000-8000-{j:012x}_0.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-",
                        "-q:v", "3", os.path.join(OUT, fn)], input=img.tobytes(), check=True)
        kw = list(dict.fromkeys(words + POOL))[:46]
        assert len(kw) == 46
        rows.append({"Filename": fn, "Title": f"{ADJ[j]} {name.title()} Pattern Background with Copy Space, Take {j + 1}",
                     "Keywords": ", ".join(kw), "Category": cat})
with open(os.path.join(OUT, "batch.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["Filename", "Title", "Keywords", "Category"])
    w.writeheader(); w.writerows(rows)
print(len(rows), "demo stills and batch.csv in", OUT)
