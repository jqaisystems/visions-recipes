"""Media prep for R36 · Tideline. Reads one Tidesstunes video and its track (never writes to the source folders) and
writes into assets/img/ (not committed):
  energy.json    the track's loudness, one value a second, and the strongest 60-second window (the pipeline's own rule)
  strip.jpg      the whole video as one slit-scan photograph: 1920 columns, each the centre column of one moment
  f000.jpg ...   a slab of consecutive frames from inside the strongest minute, for the time effects
  c000.jpg ...   the same frames' 9:16 centre at full resolution, for the vertical cut
  music.wav      the film's soundtrack: the strongest minute's own audio, from the slab's first frame
Usage: python bake/prep.py [video] [audio]   (defaults: the demo clip from bake/demo.py; or pass your own)"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
DEMO = os.path.join(ROOT, "assets", "demo")
SRC_VIDEO = os.path.join(DEMO, "demo.mp4")             # made by bake/demo.py; pass your own video and track instead
SRC_AUDIO = os.path.join(DEMO, "demo.wav")
VIDEO = sys.argv[1] if len(sys.argv) > 1 else SRC_VIDEO
AUDIO = sys.argv[2] if len(sys.argv) > 2 else SRC_AUDIO

SLAB_N, SLAB_FPS, SLAB_W, SLAB_H = 144, 12, 1024, 688     # 12 s of time, 12 frames a second
SR = 22050
MUSIC_LEN = 36.0                                          # a little longer than the film


def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)


def probe(path, entry):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entry, "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return r.stdout.strip().split("\n")[0]


os.makedirs(OUT, exist_ok=True)
vdur = float(probe(VIDEO, "format=duration"))
vw, vh = [int(x) for x in probe(VIDEO, "stream=width,height").split(",")[:2]]

# ---- the track's energy, a second at a time, and the strongest minute
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", AUDIO, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
adur = len(x) / SR
n = int(adur)
rms = np.array([np.sqrt(np.mean(x[i * SR:(i + 1) * SR] ** 2) + 1e-12) for i in range(n)])
db = 20 * np.log10(rms)
win = np.convolve(rms ** 2, np.ones(60), "valid")          # energy of every 60 s window
best = int(np.argmax(win))
e = (db - db.min()) / (db.max() - db.min())
print(f"audio {adur:.1f}s, video {vdur:.1f}s {vw}x{vh}; strongest minute {best // 60}:{best % 60:02d} to {(best + 60) // 60}:{(best + 60) % 60:02d}")

# the slab starts where the strongest minute's loudest 12 s begins, so the picture and the music are the same moment
inner = np.convolve(rms[best:best + 60] ** 2, np.ones(SLAB_N // SLAB_FPS), "valid")
slab0 = float(best + int(np.argmax(inner[:60 - 36])))      # leave room for the film's 36 s of music after it
json.dump({"duration": round(adur, 2), "videoDuration": round(vdur, 2), "energy": [round(float(v), 4) for v in e],
           "best": best, "slab0": slab0, "slabN": SLAB_N, "slabFps": SLAB_FPS, "src": [vw, vh]},
          open(os.path.join(OUT, "energy.json"), "w"))

# ---- the whole video as one slit-scan photograph
cols = 1920
ff("-i", VIDEO, "-vf", f"fps={cols}/{vdur:.3f},crop=2:{vh}:{vw // 2 - 1}:0,scale=1:1080:flags=area,tile={cols}x1",
   "-frames:v", "1", "-q:v", "2", os.path.join(OUT, "strip.jpg"))

# ---- the slab
for f in os.listdir(OUT):
    if f.startswith("f") and f.endswith(".jpg"):
        os.remove(os.path.join(OUT, f))
ff("-ss", f"{slab0:.3f}", "-i", VIDEO, "-vf", f"fps={SLAB_FPS},scale={SLAB_W}:{SLAB_H}:flags=lanczos", "-frames:v", str(SLAB_N),
   "-q:v", "3", os.path.join(OUT, "f%03d.jpg"))
got = len([f for f in os.listdir(OUT) if f.startswith("f") and f.endswith(".jpg")])
assert got == SLAB_N, got

# ---- the centre of the slab at the source's own resolution: every pixel the 9:16 crop has, for the vertical cut
cw = round(vh * 9 / 16 / 2) * 2
for f in os.listdir(OUT):
    if f.startswith("c") and f.endswith(".jpg"):
        os.remove(os.path.join(OUT, f))
ff("-ss", f"{slab0:.3f}", "-i", VIDEO, "-vf", f"fps={SLAB_FPS},crop={cw}:{vh}:{(vw - cw) // 2}:0", "-frames:v", str(SLAB_N),
   "-q:v", "3", os.path.join(OUT, "c%03d.jpg"))

# ---- the soundtrack: the strongest minute's own audio, from the slab's first frame
ff("-ss", f"{slab0:.3f}", "-t", f"{MUSIC_LEN}", "-i", AUDIO, "-ac", "2", "-ar", "48000", os.path.join(OUT, "music.wav"))
print(f"slab {SLAB_N} frames from {slab0:.1f}s, strip, music: done")
