"""The score for Clatter, built from the film's own flip schedule at 112 bpm in F minor. Every flap in bake/flips.npz is one
click at its real time, panned by its column, so a wave crossing the wall crosses the speakers. Under it, the same clatter rings
through tuned resonators, which give the harmony, with a sub, a kick on the grid, one held breath and a drop.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
F = np.load(os.path.join(ROOT, "bake", "flips.npz"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR); STEP = float(F["step"])
rng = np.random.default_rng(44)
B = lambda x: x * BEAT


def fft_conv(a, ir):
    n = len(a) + len(ir); m = 1 << int(np.ceil(np.log2(n)))
    return np.fft.irfft(np.fft.rfft(a, m) * np.fft.rfft(ir, m), m)[:len(a)]


def click(f1, f2, dec, thunk=0.0):
    n = int(0.05 * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n) * np.exp(-t * dec) * 0.5 + np.sin(2 * np.pi * f1 * t) * np.exp(-t * 300) + 0.6 * np.sin(2 * np.pi * f2 * t) * np.exp(-t * 520)
    if thunk: x += thunk * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 130)
    return x / np.abs(x).max()


# ---------------- every flap is one click, at its real time and place
ts = F["t"].astype(np.float64); ns = F["n"].astype(int); xs = F["x"].astype(np.float64) / TB["cols"]
rows_t, rows_x = [], []
for k in range(int(ns.max())):
    m = ns > k; rows_t.append(ts[m] + k * STEP + 0.02); rows_x.append(xs[m])
ft = np.concatenate(rows_t); fx = np.concatenate(rows_x)
print("clicks", len(ft))
ft = ft + rng.uniform(-0.004, 0.004, len(ft))     # no two mechanisms are identical
idx = np.clip((ft * SR).astype(int), 0, N - 1); var = rng.integers(0, 3, len(ft))
panL, panR = np.cos(fx * np.pi / 2), np.sin(fx * np.pi / 2)
stems = [(click(2600, 4300, 900), 0), (click(1700, 3100, 700), 1), (click(1100, 2300, 480, 0.8), 2)]
clatL = np.zeros(N); clatR = np.zeros(N)
for ir, v in stems:
    m = var == v
    L = np.bincount(idx[m], panL[m], minlength=N)[:N]; R = np.bincount(idx[m], panR[m], minlength=N)[:N]
    clatL += fft_conv(L, ir); clatR += fft_conv(R, ir)
# one flap must be heard alone, and thousands must roar without burying it: the level is pulled down as the density rises
cnt = np.bincount(idx, minlength=N)[:N].astype(np.float64); win = np.hanning(int(0.03 * SR)); win /= win.sum()
dens = fft_conv(cnt, win) * SR * 0.03
g = (1 + np.maximum(dens, 0) / 1.5) ** -0.6
clatL *= g; clatR *= g
clat = np.tanh(np.c_[clatL, clatR] * 1.1)
out = clat * 0.62

# ---------------- the harmony is the clatter, ringing through tuned resonators
hz = lambda name: {"F": 87.31, "Ab": 103.83, "C": 130.81, "Db": 69.30, "Eb": 77.78, "G": 98.0, "Bb": 116.54}[name]
CH = [(0, 14, ["F", "C", "Ab"]), (14, 21, ["Db", "Ab", "F"]), (21, 25, ["Eb", "Bb", "G"]), (25.5, 31, ["F", "C", "Ab"]), (31, 37, ["Db", "Ab", "F"]),
      (37, 39, ["Ab", "C", "Eb"]), (39, 46, ["Db", "F", "Ab"]), (46, 53, ["Eb", "G", "Bb"]), (53, 64, ["F", "C", "Ab"])]
ring = np.zeros((N, 2))
for a, b, notes in CH:
    i, j = int(B(a) * SR), min(N, int(B(b) * SR)); e = np.zeros(N); w = int(0.02 * SR)
    e[i:j] = 1; e[i:i + w] = np.linspace(0, 1, w); e[max(i, j - w):j] = np.linspace(1, 0, min(w, j - i))
    n = int(2.4 * SR); t = np.arange(n) / SR; ir = np.zeros(n)
    for nm in notes:
        for mul, gn, de in ((4, 1.0, 2.0), (8, 0.55, 3.4), (2, 0.5, 1.6), (12, 0.22, 5)):
            ir += gn * np.sin(2 * np.pi * hz(nm) * mul * t) * np.exp(-t * de)
    for ch in (0, 1):
        ring[:, ch] += fft_conv(clat[:, ch] * e, ir)
ring /= max(1e-6, np.abs(ring).max()); out += ring * 0.46

# ---------------- what's under it


def add(at, sig, gain=1.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]; out[i:i + len(sig), 0] += sig * gain; out[i:i + len(sig), 1] += sig * gain


def kick(g=1.0, f0=46):
    n = int(0.42 * SR); t = np.arange(n) / SR; f = f0 + 95 * np.exp(-t * 38); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.2 * np.sin(ph) * np.exp(-t * 7)) * g


def sub(f, dur, att=0.03):
    n = int(dur * SR); t = np.arange(n) / SR; e = np.minimum(1, t / att) * np.exp(-t * 0.5) * np.minimum(1, (dur - t) / 0.08)
    return np.sin(2 * np.pi * f * t) * e + 0.14 * np.sin(4 * np.pi * f * t) * e


for a, b, f in [(4, 14, 43.65), (14, 21, 34.65), (21, 25, 38.89), (25.5, 31, 43.65), (31, 37, 34.65), (39, 46, 34.65), (46, 53, 38.89), (53, 57, 43.65)]:
    add(B(a), sub(f, B(b - a)), 0.25 + 0.1 * (a >= 14))
for bt in np.arange(14, 21, 1): add(B(bt), kick(0.72))
for bt in np.arange(21, 25, 1): add(B(bt), kick(0.55 + 0.05 * (bt - 21)))
for bt in np.arange(27.5, 31, 1): add(B(bt), kick(0.75))
for bt in np.arange(46, 53, 1): add(B(bt), kick(0.72))
for bt in (37, 37.5, 37.75, 38, 38.25, 38.75): add(B(bt), kick(0.8))
for bt in (39, 42.625, 44.5, 44.875): add(B(bt), kick(0.65))
# the riser into the hold
i, j = int(B(22) * SR), int(B(25) * SR); nz = rng.normal(0, 1, j - i); tn = np.arange(j - i) / (j - i)
nz = np.diff(np.r_[0, np.cumsum(nz) * 0.02]) + nz * (0.05 + 0.6 * tn); out[i:j, 0] += nz * tn ** 2.2 * 0.08; out[i:j, 1] += nz[::-1] * tn ** 2.2 * 0.08
# one held breath: everything but the last click stops
i, j = int(B(25) * SR), int(B(25.5) * SR); fade = np.ones(N); fade[i:j] = 0.0; w = int(0.012 * SR); fade[i:i + w] = np.linspace(1, 0, w); out *= fade[:, None]
# the drop
n = int(2.6 * SR); t = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(30 + 110 * np.exp(-t * 7)) / SR; add(B(25.5), np.tanh(2.6 * np.sin(ph) * np.exp(-t * 1.7)), 0.95)
# the last flap, alone, then a chord that the logo lands in
i = int(B(56.3) * SR); j = int(B(56.75) * SR); out[i:j] *= np.linspace(1, 0.15, j - i)[:, None]
n = int(B(7) * SR); t = np.arange(n) / SR; chord = sum(g_ * np.sin(2 * np.pi * f * t) for f, g_ in ((174.61, 0.5), (261.63, 0.42), (349.23, 0.34), (415.3, 0.28), (87.31, 0.55)))
add(B(57), chord * np.minimum(1, t / 0.05) * np.exp(-t * 0.55) * np.minimum(1, (B(7) - t) / 0.4), 0.3)

# ---------------- out
mx = np.abs(out).max(); out = out / mx * 0.72
out = np.tanh(out * 1.25) / np.tanh(1.25) * 0.8
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("peak", round(float(np.abs(out).max()), 3), "dur", DUR)
