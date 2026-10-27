"""Cuts 60 frames from each Motion loop onto one atlas per machine, choosing the stretch whose last frame best
matches its first, and cross-fades the last 8 frames into the frames before the start so the 60 play as a loop.
Writes assets/frames/<id>.jpg (10 x 6 cells) and the frame list into bake/frames.json.
Usage: python bake/frames.py [folder of loops]   (needs ffmpeg, numpy and Pillow)"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "loops")   # the folder that holds the loops
N, COLS, ROWS, FADE = 60, 10, 6, 8
CW, CH = 512, 288
LOOPS = [  # machine id, loop, crop box in the source (x, y, w, h as fractions)
    ("zoetrope", "thermal-horse", (0.0, 0.0, 1.0, 1.0)),
    ("praxinoscope", "minimalist-pixel-art-dancing-ballerina-composed", (0.2, 0.0, 0.6, 1.0)),
    ("disc", "vibrant-kingfisher-bird-bursting-out-water", (0.0, 0.0, 1.0, 1.0)),
    ("flipbook", "young-child-run-dusty-ruins-warm", (0.0, 0.0, 1.0, 1.0)),
]

def read(name, w, h, crop):
    x, y, cw, ch = crop
    vf = f"crop=iw*{cw}:ih*{ch}:iw*{x}:ih*{y},scale={w}:{h}:flags=lanczos,format=rgb24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SRC, name + ".mp4"), "-vf", vf, "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)

out = {}
for mid, name, crop in LOOPS:
    F = read(name, CW, CH, crop).astype(np.float32)
    small = F[:, ::8, ::8].mean(axis=3)
    # skip the ballerina's glitch frames: only stretches whose frames all stay close to their neighbours
    jumps = np.abs(np.diff(small, axis=0)).mean(axis=(1, 2))
    best = None
    for s in range(FADE, len(F) - N):
        if jumps[s:s + N].max() > 3 * np.median(jumps): continue
        d = np.abs(small[s] - small[s + N]).mean()
        if best is None or d < best[0]: best = (d, s)
    d, s = best
    seq = F[s:s + N].copy()
    for k in range(FADE):  # the last frames blend toward the frames just before the start
        a = (k + 1) / (FADE + 1)
        seq[N - FADE + k] = seq[N - FADE + k] * (1 - a) + F[s - FADE + k] * a
    atlas = Image.new("RGB", (COLS * CW, ROWS * CH))
    for i in range(N):
        atlas.paste(Image.fromarray(seq[i].clip(0, 255).astype(np.uint8)), ((i % COLS) * CW, (i // COLS) * CH))
    atlas.save(os.path.join(ROOT, "assets", "frames", mid + ".jpg"), quality=86)
    out[mid] = {"loop": name, "start": s, "seam": round(float(d), 2), "n": N, "cols": COLS, "rows": ROWS}
    print(mid, name, "start", s, "seam", round(float(d), 2), "median step", round(float(np.median(jumps)), 2))

json.dump(out, open(os.path.join(ROOT, "bake", "frames.json"), "w"), indent=1)
