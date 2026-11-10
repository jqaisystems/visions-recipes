"""The score for R56 · Pressed, composed in code from assets/table.js: metal for a wall of steel pins.
Pins sliding are a wash of tiny ticks, like rain on a tin roof, as dense as the pins moving. The noise is a clatter, the filter wave
one long falling sweep that leaves near silence, and the briefing a tune on struck metal, one note per line as it rises.
A low pulse marks each day. Needs NumPy. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2))
rng = np.random.default_rng(54)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def put(x, t, pan=0.0, g=1.0):
    i = int(t * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


TICKS = []
for k in range(24):   # a small bank of pin ticks: a click of metal, each tuned a little differently
    f = rng.uniform(2600, 7200); n = int(0.03 * SR); t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.51 * t)) * np.exp(-t / rng.uniform(0.003, 0.008))
    TICKS.append(x * 0.5)


def ticks(t0, t1, count, g=1.0, shape=None):
    """count ticks spread over t0..t1, scattered across the stereo field. shape(u) weights where in the span they fall."""
    if count <= 0 or t1 <= t0: return
    u = rng.random(int(count))
    if shape is not None: u = shape(u)
    for v in u: put(TICKS[rng.integers(len(TICKS))], t0 + v * (t1 - t0), rng.uniform(-0.9, 0.9), g * rng.uniform(0.4, 1.0))


def bell(m, t, g=1.0, d=1.6, pan=0.0):   # struck metal, close to a celesta: a clean fundamental and a few bright, quickly dying partials
    n = int((d * 3) * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.35 * np.sin(2 * np.pi * f * 4.0 * tt) * np.exp(-tt / (d * 0.18)) \
        + 0.12 * np.sin(2 * np.pi * f * 9.9 * tt) * np.exp(-tt / (d * 0.06))
    put(x * np.minimum(1, tt / 0.002), t, pan, g)


def thud(t, g=1.0):      # a low pulse: a pitched-down knock with a click on top
    n = int(0.6 * SR); tt = np.arange(n) / SR; f = 46 + 70 * np.exp(-tt / 0.03)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.16)
    put(x, t, 0.0, g); put(TICKS[3], t, 0.0, g * 0.6)


# ---------------- the room: a low drone of the lamp, on with the light and off with it
on, off0, off1 = sec(T["light"]["on"]), sec(T["light"]["off"][0]), sec(T["light"]["off"][1])
t = np.arange(N) / SR
lamp = np.clip((t - on) / 0.3, 0, 1) * np.clip((off1 - t) / (off1 - off0), 0, 1)
drone = 0.5 * np.sin(2 * np.pi * hz(38) * t) + 0.3 * np.sin(2 * np.pi * hz(45) * t + 0.4 * np.sin(2 * np.pi * 0.11 * t)) + 0.12 * np.sin(2 * np.pi * hz(50) * t)
wv0, wv1 = sec(T["wave"][0][0]), sec(T["wave"][1][0])
duck = 1 - 0.65 * np.clip((t - wv1) / 0.3, 0, 1) * np.clip((sec(36.4) - t) / 1.0, 0, 1)
out[:, 0] += drone * lamp * duck * 0.05; out[:, 1] += drone * lamp * duck * 0.05
# the switch, on and off
for tt0, g in ((on, 0.9), (off1 - 0.05, 0.6)):
    n = int(0.12 * SR); x = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.012); put(np.convolve(x, np.ones(6) / 6, "same"), tt0, 0.0, g * 0.8); thud(tt0, g * 0.5)

# ---------------- pins sliding: every relief pressed in or let go is a wash of ticks, as dense as how much of the wall it moves
SIZE = {"cap": 260, "page": 420, "feed": 420, "site": 520, "lens": 300, "chart": 380, "echo": 900, "knowledge": 500,
        "brief": 220, "grid": 500, "day": 70, "folder": 420}
for l in T["layers"]:
    nm = next(k for k in SIZE if l["name"].startswith(k)); K = l["keys"]
    for a, b in zip(K, K[1:]):
        dw = abs(b[1] - a[1])
        if dw < 0.05: continue
        t0, t1 = sec(a[0]), sec(b[0] + l["spread"])
        ticks(t0, t1, SIZE[nm] * dw, 0.55 if nm != "day" else 0.8, lambda u: u ** 1.4)
    if l.get("move"):
        M = l["move"]; ticks(sec(M[0][0]), sec(M[-1][0]), 260, 0.4)

# ---------------- the noise: a clatter on the sixteenths, as loud as the noise is high, swept away by the wave
NZ = T["noise"]
amp = lambda b: np.interp(b, [k[0] for k in NZ], [k[1] for k in NZ])
for s in np.arange(NZ[0][0] * 4, NZ[-1][0] * 4 + 14) / 4:
    a = amp(s) if s <= NZ[-1][0] else NZ[-1][1]
    if s >= T["wave"][0][0]: a *= max(0.0, 1 - (s - T["wave"][0][0]) / (T["wave"][1][0] - T["wave"][0][0]))
    if a > 0.02: ticks(sec(s), sec(s + 0.25), 70 * a, 0.5)
# the wave: one long falling sweep of ticks and air, the ridge rolling across, leaving near silence
n = int((wv1 - wv0 + 0.6) * SR); tt = np.arange(n) / SR; u = tt / (wv1 - wv0)
air = rng.standard_normal(n); cut = 0.25 * (1 - np.clip(u, 0, 1)) + 0.01
y = np.zeros(n); acc = 0.0
for i in range(n): acc += cut[i] * (air[i] - acc); y[i] = acc
put(y * np.sin(np.pi * np.clip(u, 0, 1)) ** 0.7 * 0.5, wv0, 0.0, 1.0)
pan = lambda v: -0.9 + 1.8 * v
for k in range(700):
    v = rng.random() ** 0.8
    put(TICKS[rng.integers(len(TICKS))], wv0 + v * (wv1 - wv0), pan(v), 0.6 * (1 - v * 0.7) * rng.uniform(0.4, 1))

# ---------------- what you know: a quiet clock on the beat while the knowledge document is pressed in
for b in np.arange(20.0, 28.0, 1.0): put(TICKS[7], sec(b), -0.3, 0.35); put(TICKS[11], sec(b + 0.5), 0.3, 0.2)

# ---------------- the briefing: struck metal, one note per line as it rises. D minor, lifting to the fifth
NOTES = [62, 69, 65, 72, 69, 74, 69]
briefs = [l for l in T["layers"] if l["name"].startswith("brief")]
for l, m in zip(briefs, NOTES): bell(m, sec(l["keys"][0][0]) + 0.08, 0.32, 1.4, -0.2 if m < 70 else 0.2)
bell(50, sec(36.4), 0.25, 2.4)
# the light swings across the briefing: a soft shimmer of the same tune, high
for i, m in enumerate([74, 77, 81, 86]): bell(m, sec(40.6 + i * 0.4), 0.12, 1.0, -0.6 + i * 0.4)

# ---------------- on schedule: a low pulse for each day the briefing lands, and a heavier one for the weekly
for b, row in T["pops"]: thud(sec(b), 0.55 if row == 0 else 0.9); bell(74 if row == 0 else 62, sec(b), 0.1 if row == 0 else 0.22, 0.8)
# ---------------- yours: the folder, then the light slides off, and one bell for the mark
bell(62, sec(55.0), 0.22, 2.0); bell(69, sec(56.8), 0.2, 2.0)
bell(62, sec(T["logo"]) + 0.1, 0.32, 3.0); bell(74, sec(T["logo"]) + 0.1, 0.12, 2.0)

# ---------------- master: a touch of room, then the level
ir_n = int(0.9 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.22); ir /= np.sqrt(np.sum(ir ** 2))
for ch in range(2):
    f = np.fft.rfft(out[:, ch], N + ir_n); out[:, ch] += 0.18 * np.fft.irfft(f * np.fft.rfft(ir, N + ir_n))[:N]
fade = np.clip((DUR - t) / 0.4, 0, 1); out *= fade[:, None]
out *= 10 ** (-1.5 / 20) / np.max(np.abs(out))
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score", round(DUR, 2), "s, peak -1.5 dBFS")
