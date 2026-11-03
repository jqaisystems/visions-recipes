"""R38 · Twice: the conversation into one texture array, in the order it happens.
Reads a folder of screens (the demo from bake/demo.py by default, or your own app's), read only:
  each screen in SHOTS becomes a slow shot, scaled to 1600 wide and panned through a 900-high window;
  the live call is either a folder live/ of 1600x900 PNGs used as they are, or live.mp4, sampled at LIVE_AT and
  cropped by LIVE_CROP (for a recording with burned-in captions, crop above them and pad with the ground colour).
Writes assets/img/f###.jpg (1600x900, uncommitted) and bake/frames.json (what each frame is).
Usage: python bake/prep.py [screens_dir]"""
import json, os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets", "demo", "screens")
OUT = os.path.join(ROOT, "assets", "img")
FW, FH = 1600, 900
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT, f))

# file, shot, frames, pan from y0 to y1 (in the 1600-wide screen), zoom z0 to z1 about (cx, cy)
SHOTS_BEFORE = [
    ("prep.png", "prep", 6, 0, 120),
    ("brief.png", "brief", 8, 0, 175),
    ("objections.png", "objections", 6, 0, 175),
    ("roleplay.png", "roleplay", 8, 0, 0, 1.0, 1.08, 0.3, 0.33),
]
LIVE_N = 16
LIVE_AT = [43.4 + 0.62 * j for j in range(LIVE_N)]      # seconds into live.mp4
LIVE_CROP = (160, 96, 1760, 876)                         # from a 1920x1080 recording, pasted 40 px down
SHOTS_AFTER = [
    ("debrief.png", "debrief", 8, 0, 175),
    ("next.png", "next", 4, 0, 60),
]

frames = []
def save(im, shot, note=""):
    k = len(frames) + 1
    im.convert("RGB").save(os.path.join(OUT, f"f{k:03d}.jpg"), quality=90)
    frames.append({"k": k - 1, "shot": shot, "note": note})

def pan(name, shot, n, y0, y1, z0=1.0, z1=1.0, cx=0.5, cy=0.3):
    src = Image.open(os.path.join(SRC, name)).convert("RGB")
    s = FW / src.width
    big = src.resize((FW, round(src.height * s)), Image.LANCZOS) if s != 1 else src
    for j in range(n):
        u = j / max(n - 1, 1); u = u * u * (3 - 2 * u)
        y = y0 + (y1 - y0) * u; z = z0 + (z1 - z0) * u
        w, h = FW / z, FH / z
        x = (FW - w) * cx; yy = y + (FH - h) * cy
        save(big.crop((round(x), round(yy), round(x + w), round(yy + h))).resize((FW, FH), Image.LANCZOS), shot, name)

for s in SHOTS_BEFORE: pan(*s)
live = os.path.join(SRC, "live")
if os.path.isdir(live):
    for f in sorted(os.listdir(live))[:LIVE_N]:
        save(Image.open(os.path.join(live, f)).convert("RGB").resize((FW, FH)), "live", f)
else:
    for ts in LIVE_AT:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ts:.3f}", "-i", os.path.join(SRC, "live.mp4"), "-frames:v", "1",
                              "-s", "1920x1080", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        im = Image.frombytes("RGB", (1920, 1080), raw)
        pad = Image.new("RGB", (FW, FH), im.getpixel((20, 20)))
        pad.paste(im.crop(LIVE_CROP), (0, 40))
        save(pad, "live", f"live.mp4 {ts:.2f}s")
for s in SHOTS_AFTER: pan(*s)

shots = {}
for f in frames: shots.setdefault(f["shot"], [f["k"], 0]); shots[f["shot"]][1] += 1
json.dump({"n": len(frames), "w": FW, "h": FH, "shots": shots, "frames": frames}, open(os.path.join(ROOT, "bake", "frames.json"), "w"), indent=1)
print(len(frames), "frames", shots)
