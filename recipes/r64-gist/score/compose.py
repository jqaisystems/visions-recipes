"""The score for R64 · Gist, composed in code from assets/table.js and assets/wind.js. Season 11 is string art, so the score is
strings and wood. The nails land scattered as eight waves of small hammer taps, each wave on the beat; a ripple lifts and taps
every one home onto the grid; a soft rising tone carries the theme light, with a bell as it reaches each theme. Then every pass of
thread is plucked: its pitch is set by its length, like a real string, kept in D major pentatonic, so the first slow passes are
single notes and the rest become a shimmer. The last pass waits on one held note until the reviewer's lamp has passed; only then is
it plucked. As the camera pulls back to the wall of earlier days, a soft bell for each one, and one full chord brings in the mark.
The board and its signals are a demo.
Needs NumPy.  Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda name, pre: json.loads(open(os.path.join(ROOT, "assets", name), encoding="utf-8").read()[len(pre):-1])
T = rd("table.js", "window.TABLE="); WD = rd("wind.js", "window.WIND=")
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); t = np.arange(N) / SR; bt = t / BEAT
rng = np.random.default_rng(64)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
PENTA = [0, 2, 4, 7, 9]                       # D major pentatonic: D E F# A B
NAIL = np.array(WD["nails"]).reshape(-1, 2); BW = WD["w"]


def put(x, at, pan=0.0, g=1.0):
    i = int(at * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR); X = np.fft.rfft(x)
    g = 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-6)) ** 4) / np.sqrt(1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))


def keyv(K, b): return np.interp(b, [k[0] for k in K], [k[1] for k in K])
def sm(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)
def panx(x): return float(np.clip((x / BW) * 2 - 1, -1, 1)) * 0.7


# ---------------- sounds
def tap_variant():                            # one small nail tapped home: a bright tick and a short metallic ring
    n = int(0.09 * SR); tt = np.arange(n) / SR; f = rng.uniform(2600, 4200)
    x = band(rng.standard_normal(n), 1800, 9000) * np.exp(-tt / 0.0025) * 0.8
    x += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.018) * 0.35 + np.sin(2 * np.pi * f * 1.52 * tt) * np.exp(-tt / 0.01) * 0.2
    return x
TAPS = [tap_variant() for _ in range(10)]


def mallet(at, g=1.0):                        # the hammer on the board: a dull wooden thud
    n = int(0.35 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(70 + 120 * np.exp(-tt / 0.012)) / SR) * np.exp(-tt / 0.07)
    put(body + band(rng.standard_normal(n), 300, 2500) * np.exp(-tt / 0.006) * 0.5, at, 0.0, g)


PL = {}
def pluck_buf(m):                             # a plucked string, Karplus-Strong, cached by note
    if m in PL: return PL[m]
    f = hz(m); p = int(round(SR / f)); n = int(1.6 * SR); y = np.zeros(n)
    y[:p] = band(rng.standard_normal(p * 6), 60, 5000)[:p]
    for i in range(p, n): y[i] = 0.995 * 0.5 * (y[i - p] + y[i - p - 1])
    y /= np.abs(y).max() + 1e-9; PL[m] = y; return y


def pitch_of(length):                         # shorter passes ring higher, like a shorter string, kept in the scale
    raw = 88 - 26 * np.log2(max(length, 30) / 30) / np.log2(15)
    oct_, deg = divmod(int(round(raw)) - 62, 12)
    deg = min(PENTA, key=lambda d: abs(d - deg)); return 62 + 12 * oct_ + deg


def bell(m, at, g=1.0, d=2.0, pan=0.0):
    n = int(d * 3 * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.25 * np.sin(2 * np.pi * f * 3.0 * tt) * np.exp(-tt / (d * 0.2))
    put(x * np.minimum(1, tt / 0.004), at, pan, g)


def pad(notes, b0, b1, g, fade=0.8):          # a soft bed: a few detuned sines, swelling in and out
    env = sm((bt - b0) / fade) * (1 - sm((bt - b1) / fade)); x = np.zeros(N)
    for m in notes:
        for dt in (-0.12, 0.0, 0.11): x += np.sin(2 * np.pi * hz(m + dt) * t + m)
    x *= env / (3 * len(notes))
    out[:, 0] += x * g; out[:, 1] += np.roll(x, 211) * g


# ---------------- the nails go in: eight waves of taps, each opened by a mallet on the beat
def jhash(i, s):                              # the film's own seeded hash, so every tap lands with its nail
    x = (i * 374761393 + s * 668265263) & 0xFFFFFFFF
    x = ((x ^ (x >> 13)) * 1274126177) & 0xFFFFFFFF
    return (x ^ (x >> 16)) / 4294967296
LAND = []
for i, (x, y) in enumerate(NAIL):
    w = int(np.clip(np.floor(x / BW * T["waves"] + (jhash(i, 1) - 0.5) * 0.9), 0, T["waves"] - 1))
    LAND.append(T["wave0"] + w + jhash(i, 2) * T["waveSpread"])
for k in range(T["waves"]): mallet(sec(T["wave0"] + k), 0.55)
for i, L in enumerate(LAND):
    put(TAPS[i % len(TAPS)], sec(L), panx(NAIL[i, 0]), rng.uniform(0.02, 0.06))

# ---------------- normalize: the ripple lifts every nail and taps it home on the grid, centre first
N0, N1, ND = T["norm"]; MAXR = np.hypot(BW / 2, WD["h"] / 2)
for i, (x, y) in enumerate(NAIL):
    gx, gy = x - BW / 2, WD["h"] / 2 - y
    home = N0 + (N1 - ND - N0) * (0.85 * np.hypot(gx, gy) / MAXR + 0.15 * jhash(i, 25)) + ND
    put(TAPS[(i * 7) % len(TAPS)], sec(home), panx(x), rng.uniform(0.012, 0.035))
for k in range(4): mallet(sec(N0 + 0.6 + k * (N1 - N0 - 0.6) / 4), 0.3)

# ---------------- classify: a rising tone under the light, and a bell as it reaches each theme's patch
s0, s1 = T["sweep"]
env = sm((bt - s0 + 0.3) / 0.8) * (1 - sm((bt - s1 - 0.2) / 1.0)); f = hz(57) * 2 ** (sm((bt - s0) / (s1 - s0)) * 7 / 12)
sweep = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + band(rng.standard_normal(N), 900, 3500) * 0.25
pan_l = np.clip((bt - s0) / (s1 - s0), 0, 1)
out[:, 0] += sweep * env * 0.05 * np.sqrt(1 - pan_l); out[:, 1] += sweep * env * 0.05 * np.sqrt(pan_l + 1e-9)
for k, (sx, sy) in enumerate(sorted(WD["seeds"])):
    bi = s0 + (sx - BW / 2 + 1150) / 2300 * (s1 - s0)
    bell(74 + PENTA[k % 5] + (12 if k == 5 else 0), sec(bi), 0.045, 0.8, panx(sx))

# ---------------- the winding: every pass is plucked as it lands, its pitch from its length; the last one waits
P = WD["passes"]; LAST = max(j for j, p in enumerate(P) if p[2])
f0, f1, ease = T["wind"]
times = [f0 + (f1 - f0) * ((j + 1) / LAST) ** (1 / ease) for j in range(LAST)]
for j in range(LAST):
    a, c_, v = P[j]
    if not v: continue
    L = float(np.hypot(*(NAIL[a] - NAIL[c_])))
    rate = 1 / max(1e-3, sec(times[j] - (times[j - 1] if j else f0)))
    put(pluck_buf(pitch_of(L)), sec(times[j]), panx((NAIL[a, 0] + NAIL[c_, 0]) / 2), 0.34 / np.sqrt(1 + rate / 3))
a, c_, _ = P[LAST]; L = float(np.hypot(*(NAIL[a] - NAIL[c_])))
put(pluck_buf(pitch_of(L)), sec(T["approve"] + 0.2), panx((NAIL[a, 0] + NAIL[c_, 0]) / 2), 0.42)    # approved: the last pass at last
bell(74, sec(T["approve"] + 0.2), 0.07, 2.2)

# ---------------- the lamp: a soft breath of air as the reviewer's light crosses
l0, l1 = T["lamp"]; env = sm((bt - l0) / 0.6) * (1 - sm((bt - l1) / 0.6))
air = band(rng.standard_normal(N), 300, 1800) * env * 0.05; out[:, 0] += air; out[:, 1] += np.roll(air, 157)

# ---------------- the wall: a soft bell for each earlier day as the camera pulls back, falling through the scale
a0, a1 = T["archive"]
for d in range(14):
    m = 86 - 12 * (d // 5) + PENTA[4 - d % 5]
    bell(m, sec(a0 + 0.6 + d * (a1 - a0 - 1.6) / 14), 0.03, 1.4, (d % 5 / 2 - 1) * 0.6)

# ---------------- the bed: a low drone while the nails land, a lift as they straighten, a chord for the brief, one held note
# while the last pass waits, then the chord opens out over the wall
pad([38, 45], 0.5, N0 + 0.5, 0.05, 1.5)
pad([45, 52, 57], N0, s1 + 0.4, 0.04)
pad([50, 57, 62, 66], f0, T["loose"], 0.035)
pad([69], T["loose"] - 0.2, T["approve"] + 0.3, 0.045, 0.5)          # the waiting note
pad([43, 50, 55, 59, 62, 69], T["approve"], T["logo"], 0.04, 1.2)

# ---------------- the close: one full chord brings in the mark
for j, m in enumerate((38, 50, 57, 62, 66, 69, 74)): put(pluck_buf(m), sec(T["logo"]) + 0.03 * j, (j / 6 - 0.5) * 1.2, 0.3)
for j, m in enumerate((50, 62, 66, 69)): bell(m, sec(T["logo"]) + 0.01 * j, 0.08, 3.0, (j / 3 - 0.5))

# ---------------- a small room, then the level
n = int(0.6 * SR); tt = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-tt / 0.14)
ir = band(ir, 200, 7000); ir /= np.sqrt((ir ** 2).sum())
L = 1 << int(np.ceil(np.log2(N + n)))
for c in range(2):
    wet = np.fft.irfft(np.fft.rfft(out[:, c], L) * np.fft.rfft(np.roll(ir, 41 * c), L), L)[:N]
    out[:, c] += wet * 0.25
fade = np.minimum(1, (DUR - t) / 0.6); out *= fade[:, None]
out *= 10 ** (-1.5 / 20) / np.abs(out).max()
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
print("score %.1f s, peak -1.5 dBFS, %d pluck notes" % (DUR, len(PL)))
