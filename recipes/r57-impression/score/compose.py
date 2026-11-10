"""The score for R57 · Impression, composed in code from assets/table.js: the metal of season 9, drier and closer, a frame on a desk.
A pin moving is a tick, so a shape pressed in is a slide of ticks as dense as the pins it moves. A mould that doesn't fit scrapes, as loud
as the pins it shoves; one that fits is a single soft note. Each check is a tuned tap, the thirty days a rising run, the tilt reset a long
cascade of ball bearings, and the brief one low chord in D. Needs NumPy. Writes assets/bgm/score.wav (not committed).
Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2))
rng = np.random.default_rng(57)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def put(x, t, pan=0.0, g=1.0):
    i = int(t * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


TICKS = []
for k in range(24):   # pin ticks: a dry click of steel, each tuned a little differently
    f = rng.uniform(2400, 6800); n = int(0.025 * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 1.47 * t)) * np.exp(-t / rng.uniform(0.0025, 0.006))
    TICKS.append(x * 0.5)


def ticks(t0, t1, count, g=1.0, shape=None, pan=None):
    if count <= 0 or t1 <= t0: return
    u = rng.random(int(count))
    if shape is not None: u = shape(u)
    for v in u: put(TICKS[rng.integers(len(TICKS))], t0 + v * (t1 - t0), rng.uniform(-0.9, 0.9) if pan is None else pan(v), g * rng.uniform(0.4, 1.0))


def bell(m, t, g=1.0, d=1.6, pan=0.0):   # struck metal
    n = int((d * 3) * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.35 * np.sin(2 * np.pi * f * 4.0 * tt) * np.exp(-tt / (d * 0.18)) \
        + 0.1 * np.sin(2 * np.pi * f * 9.9 * tt) * np.exp(-tt / (d * 0.06))
    put(x * np.minimum(1, tt / 0.002), t, pan, g)


def tap(m, t, g=1.0, pan=0.0):           # a tuned tap, short and dry
    n = int(0.5 * SR); tt = np.arange(n) / SR; f = hz(m)
    x = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt / 0.03)) * np.exp(-tt / 0.12)
    put(x * np.minimum(1, tt / 0.001), t, pan, g)


def thud(t, g=1.0):
    n = int(0.6 * SR); tt = np.arange(n) / SR; f = 44 + 70 * np.exp(-tt / 0.03)
    put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.16), t, 0.0, g); put(TICKS[3], t, 0.0, g * 0.6)


def noise(t0, dur, g, cut0, cut1, pan=0.0):   # filtered noise, the filter moving from cut0 to cut1
    n = int(dur * SR); x = rng.standard_normal(n); c = np.linspace(cut0, cut1, n); y = np.zeros(n); acc = 0.0
    for i in range(n): acc += c[i] * (x[i] - acc); y[i] = acc
    put(y * np.sin(np.pi * np.arange(n) / n) ** 0.6, t0, pan, g)


# ---------------- the room: a low hum in D, on with the light and off with it
on, off0, off1 = sec(T["light"]["on"]), sec(T["light"]["off"][0]), sec(T["light"]["off"][1])
t = np.arange(N) / SR
lamp = np.clip((t - on) / 0.3, 0, 1) * np.clip((off1 - t) / (off1 - off0), 0, 1)
drone = 0.5 * np.sin(2 * np.pi * hz(38) * t) + 0.3 * np.sin(2 * np.pi * hz(45) * t + 0.4 * np.sin(2 * np.pi * 0.09 * t)) + 0.1 * np.sin(2 * np.pi * hz(50) * t)
quiet = 1 - 0.7 * np.clip((t - sec(35.0)) / 0.5, 0, 1) * np.clip((sec(41.0) - t) / 0.4, 0, 1)
out[:, 0] += drone * lamp * quiet * 0.05; out[:, 1] += drone * lamp * quiet * 0.05
n = int(0.12 * SR); x = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.012); put(np.convolve(x, np.ones(6) / 6, "same"), on, 0.0, 0.7); thud(on, 0.45)
thud(off1 - 0.05, 0.3)

# ---------------- the events
SIZE = {"problem": 900, "cal": 500, "owner": 160, "target": 200, "brief": 800}
fronts = [e for e in T["ev"] if e["kind"] == "front"]
MOVED = [1103, 303, 0]   # pins each mould shoves, as the film counts them
for e in T["ev"]:
    t0, t1 = sec(e["t0"]), sec(e["t1"] + e["spread"])
    if e["kind"] == "back":
        nm = e["shape"]
        if nm.startswith("day"):
            i = e["day"]; tap([62, 64, 66, 69, 71][i % 5] + 12 * (i // 10), sec(e["t0"]), 0.22, -0.6 + 1.2 * (i % 6) / 5); ticks(t0, t1, 24, 0.4)
        elif e.get("restore"): ticks(t0, t1, 380, 0.45, lambda u: u ** 1.2)
        else: ticks(t0, t1, SIZE[nm], 0.5, lambda u: u ** 1.4)
    elif e["kind"] == "front":
        i = e["path"]; mv = MOVED[i]
        noise(sec(e["t0"] - 0.7), sec(0.8), 0.05, 0.02, 0.12)                     # the mould coming down: air
        if mv > 0:
            ticks(t0, t1, mv * 0.6, 0.6, lambda u: u ** 0.8)                        # the scrape: pins shoved back
            noise(t0, t1 - t0 + 0.1, 0.16 * (mv / 1103) ** 0.5, 0.18, 0.05)
            thud(t1, 0.35 * (mv / 1103) ** 0.5)
        else:
            bell(74, t0 + 0.3, 0.26, 2.2); bell(81, t0 + 0.32, 0.12, 1.6, 0.3)     # it fits: one soft note
        for k in range(len(T["checks"])):                                          # each check, a tuned tap rising
            tap([62, 64, 66, 69, 71, 74][k], sec(e["t0"] + 1.1 + k * 0.32), 0.2, -0.4 + k * 0.16)
        noise(sec(e["lift"]), sec(0.6), 0.04, 0.03, 0.15)                          # the mould lifting
    elif e["kind"] == "tilt":                                                      # the reset: a long cascade, top row first
        ticks(sec(e["t0"]), sec(e["t1"] + e["spread"] + 0.3), 2600, 0.55, lambda u: u ** 0.9, pan=lambda v: -0.7 + 1.4 * v)
        noise(sec(e["t0"] - 0.6), sec(e["t1"] + e["spread"] + 1.0) - sec(e["t0"] - 0.6), 0.22, 0.04, 0.3)
        thud(sec(e["t1"] + e["spread"] + 0.3), 0.8)
    elif e["kind"] == "flat":                                                      # a palm pressed flat
        ticks(t0, t1 + 0.15, 700, 0.55); thud(t0 + 0.05, 0.7)

# ---------------- the words: a small tap under each, and the map's labels named on the beat
for s, b0, b1 in T["caps"]: tap(57, sec(b0), 0.08)
for lab in T["labels"]: tap(69, sec(lab[0]), 0.14, 0.3)
# one recommendation: the room goes quiet, one chord
bell(62, sec(37.0), 0.26, 3.0); bell(66, sec(37.02), 0.16, 2.6, -0.3); bell(69, sec(37.04), 0.16, 2.6, 0.3)
# the owner and the measure
bell(69, sec(48.0), 0.18, 1.4); bell(74, sec(48.9), 0.2, 1.6)
# the brief: one low chord in D, then the mark
bell(50, sec(52.0), 0.3, 3.5); bell(62, sec(52.05), 0.2, 3.0); bell(66, sec(52.1), 0.14, 3.0, -0.3); bell(69, sec(52.15), 0.14, 3.0, 0.3)
bell(62, sec(T["logo"]) + 0.1, 0.3, 3.0); bell(74, sec(T["logo"]) + 0.1, 0.12, 2.0)

# ---------------- master: a small room, then the level
ir_n = int(0.6 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.14); ir /= np.sqrt(np.sum(ir ** 2))
for ch in range(2):
    f = np.fft.rfft(out[:, ch], N + ir_n); out[:, ch] += 0.14 * np.fft.irfft(f * np.fft.rfft(ir, N + ir_n))[:N]
fade = np.clip((DUR - t) / 0.4, 0, 1); out *= fade[:, None]
out *= 10 ** (-1.5 / 20) / np.max(np.abs(out))
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score", round(DUR, 2), "s, peak -1.5 dBFS")
