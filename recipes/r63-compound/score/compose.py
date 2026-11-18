"""The score for R63 · Compound, composed in code from assets/table.js and assets/wind.js. Season 11 is string art, so the score is
strings and wood. The pins go in round the ring as a run of small taps, a mallet on every beat; one light approves them with a rising
tone. Then every pass of thread is plucked as it lands: its pitch is set by its length, like a real string, kept in A major
pentatonic. The first three passes are single notes, a day each. Then the passes speed up until the plucks merge into a shimmer, and
the bed swells with them: it compounds. Each colour thread plays in its own register. The thread ties off on one held note, and one
full chord brings in the mark. The board is a demo.
Needs NumPy.  Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda name, pre: json.loads(open(os.path.join(ROOT, "assets", name), encoding="utf-8").read()[len(pre):-1])
T = rd("table.js", "window.TABLE="); WD = rd("wind.js", "window.WIND=")
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); t = np.arange(N) / SR; bt = t / BEAT
rng = np.random.default_rng(63)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
PENTA = [0, 2, 4, 7, 9]                       # A major pentatonic: A B C# E F#
ROOTN = 57
NAIL = np.array(WD["nails"]).reshape(-1, 2); NN = WD["n"]; RAD = WD["r"]


def put(x, at, pan=0.0, g=1.0):
    i = int(at * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR); X = np.fft.rfft(x)
    g = 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-6)) ** 4) / np.sqrt(1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))


def sm(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)
def panx(x): return float(np.clip(x / RAD, -1, 1)) * 0.7


def jhash(i, s):                              # the film's own seeded hash, so every tap lands with its pin
    x = (i * 374761393 + s * 668265263) & 0xFFFFFFFF
    x = ((x ^ (x >> 13)) * 1274126177) & 0xFFFFFFFF
    return (x ^ (x >> 16)) / 4294967296


# ---------------- sounds
def tap_variant():                            # one pin pressed home: a bright tick and a short ring
    n = int(0.09 * SR); tt = np.arange(n) / SR; f = rng.uniform(2400, 3800)
    x = band(rng.standard_normal(n), 1800, 9000) * np.exp(-tt / 0.0025) * 0.8
    x += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.02) * 0.35 + np.sin(2 * np.pi * f * 1.52 * tt) * np.exp(-tt / 0.01) * 0.2
    return x
TAPS = [tap_variant() for _ in range(10)]


def mallet(at, g=1.0):                        # a dull wooden thud on the beat
    n = int(0.35 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(66 + 120 * np.exp(-tt / 0.012)) / SR) * np.exp(-tt / 0.08)
    put(body + band(rng.standard_normal(n), 300, 2500) * np.exp(-tt / 0.006) * 0.5, at, 0.0, g)


PL = {}
def pluck_buf(m, damp=0.995):                 # a plucked string, Karplus-Strong, cached by note
    key = (m, damp)
    if key in PL: return PL[key]
    f = hz(m); p = int(round(SR / f)); n = int(1.8 * SR); y = np.zeros(n)
    y[:p] = band(rng.standard_normal(p * 6), 60, 6000)[:p]
    for i in range(p, n): y[i] = damp * 0.5 * (y[i - p] + y[i - p - 1])
    y /= np.abs(y).max() + 1e-9; PL[key] = y; return y


def snap(raw):                                # a pitch, kept in the scale
    oct_, deg = divmod(int(round(raw)) - ROOTN, 12)
    deg = min(PENTA, key=lambda d: abs(d - deg)); return ROOTN + 12 * oct_ + deg


def pitch_of(length, base):                   # shorter passes ring higher, like a shorter string
    return snap(base - 14 * np.log2(max(length, 60) / 60) / np.log2(16))


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


# ---------------- the pins go in round the ring, a mallet on every beat
L0, L1 = T["land"]
for k in range(int(np.ceil(L0)), int(L1) + 1): mallet(sec(k), 0.5)
for i in range(NN):
    L = L0 + (L1 - L0) * i / NN + (jhash(i, 2) - 0.5) * 0.05
    put(TAPS[i % len(TAPS)], sec(L), panx(NAIL[i, 0]), rng.uniform(0.03, 0.07))

# ---------------- the approval: a rising tone runs round with the light, a tick every few pins, a bell when it closes
a0, a1 = T["approve"]
env = sm((bt - a0 + 0.3) / 0.6) * (1 - sm((bt - a1 - 0.1) / 0.8)); f = hz(ROOTN) * 2 ** (sm((bt - a0) / (a1 - a0)) * 12 / 12)
tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + band(rng.standard_normal(N), 900, 3500) * 0.2
ang = 2 * np.pi * np.clip((bt - a0) / (a1 - a0), 0, 1)
out[:, 0] += tone * env * 0.05 * (0.5 - 0.35 * np.sin(ang)); out[:, 1] += tone * env * 0.05 * (0.5 + 0.35 * np.sin(ang))
for i in range(0, NN, 6): bell(ROOTN + 24 + PENTA[(i // 6) % 5], sec(a0 + (a1 - a0) * i / NN), 0.012, 0.25, panx(NAIL[i, 0]))
bell(ROOTN + 24, sec(a1), 0.06, 1.5)

# ---------------- the windings: every pass plucked as it lands, its pitch from its length
def times_of(k, n):
    f0, f1, e = T["wind"][k]
    if k == 0:
        D = T["days"]; ts = [D[1][0], D[2][0], D[3][0]]
        return ts + [f0 + (f1 - f0) * ((j - 3) / (n - 3)) ** (1 / e) for j in range(4, n + 1)]
    return [f0 + (f1 - f0) * (j / n) ** (1 / e) for j in range(1, n + 1)]
BASE = [76, 81, 76, 69]                       # each thread's register: bone, coral higher, amber, teal lower
GAIN = [1.0, 0.8, 0.8, 0.9]
tie = T["tie"]
put(band(rng.standard_normal(int(0.08 * SR)), 300, 2000) * np.exp(-np.arange(int(0.08 * SR)) / SR / 0.02) * 0.5, sec(tie), 0.0, 0.5)  # the knot
for k, th in enumerate(WD["threads"]):
    seq = th["seq"]; n = len(seq) - 1; ts = times_of(k, n)
    for j in range(n):
        a, c = seq[j], seq[j + 1]; L = float(np.hypot(*(NAIL[a] - NAIL[c])))
        prev = ts[j - 1] if j else (T["days"][0][0] if k == 0 else T["wind"][k][0])
        rate = 1 / max(1e-3, sec(ts[j] - prev))            # passes per second around this one
        g = GAIN[k] * 0.36 / np.sqrt(1 + rate / 2.5)
        if k == 0 and j < 3: g = 0.55; bell(pitch_of(L, BASE[0]) - 12, sec(ts[j]), 0.06, 1.8)   # a day each: a note you can hear
        put(pluck_buf(pitch_of(L, BASE[k])), sec(ts[j]), panx((NAIL[a, 0] + NAIL[c, 0]) / 2), g)

# ---------------- the bed: a low drone under the pins, then chords that swell as the passes speed up
pad([45, 52], 0.5, 13.5, 0.05, 1.5)
pad([57, 64, 69], 13.6, 19.5, 0.025, 1.0)
rush = np.clip((bt - 19) / 17, 0, 1) ** 2 * (1 - sm((bt - 36) / 1.0))
for ch, g0 in (([45, 57, 61, 64, 68], 0.0),):
    x = np.zeros(N)
    for m in ch:
        for dt in (-0.1, 0.0, 0.09): x += np.sin(2 * np.pi * hz(m + dt) * t + m)
    x *= rush / (3 * len(ch)) * 0.07; out[:, 0] += x; out[:, 1] += np.roll(x, 173)
pad([50, 57, 62, 66], 36.2, 40.8, 0.035)      # coral
pad([52, 59, 64, 68], 40.6, 44.4, 0.035)      # amber
pad([45, 52, 57, 61, 64], 44.3, T["tieoff"] + 0.4, 0.04)   # teal
pad([69], T["tieoff"], T["logo"], 0.045, 0.5)  # the held note after the tie-off
put(pluck_buf(69), sec(T["tieoff"]), 0.0, 0.5)

# ---------------- the close: one full chord brings in the mark
for j, m in enumerate((45, 57, 64, 69, 73, 76, 81)): put(pluck_buf(m), sec(T["logo"]) + 0.03 * j, (j / 6 - 0.5) * 1.2, 0.3)
for j, m in enumerate((57, 69, 73, 76)): bell(m, sec(T["logo"]) + 0.01 * j, 0.08, 3.0, (j / 3 - 0.5))

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
