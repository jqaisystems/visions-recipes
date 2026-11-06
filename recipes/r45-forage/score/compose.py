"""The score for R45 · Forage, composed in code at 108 bpm in F sharp minor and timed to bake/table.json: a sub drone that
thickens as the network grows and a wet patter that rises with its reach; a hit for each grown word; rolling score ticks;
one held breath, a huge descending collapse and a sub drop on the contraction; a tight pulse and a clean hit per word; a
snip for the rejected vein; a chord on the logo. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
rng = np.random.default_rng(44)
B = lambda x: x * BEAT
out = np.zeros((N, 2))
DROP, FLY, FLIP, MAIL, NEV, CLOSE, LOGO = 25.5, 31, 37, 39, 46, 53, 57


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * (1 - max(0, pan))
    out[i:i + len(sig), 1] += sig * gain * (1 + min(0, pan))


def lp1(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y


def lp(x, fc):
    if np.isscalar(fc): return lp1(x, fc)
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y


def hp(x, fc): return x - lp(x, fc)
def tm(d): return np.arange(int(SR * d)) / SR
def mtof(m): return 440 * 2 ** ((m - 69) / 12)


def kick(d=0.5, f=46):
    x = tm(d); return np.sin(2 * np.pi * (f * x + 130 * (1 - np.exp(-x * 30)) / 30)) * np.exp(-x / 0.17)


def snare(d=0.26):
    x = tm(d); return hp(rng.normal(size=len(x)), 1500) * np.exp(-x / 0.07) * 0.7 + np.sin(2 * np.pi * 185 * x) * np.exp(-x / 0.05) * 0.5


def hat(d=0.05):
    x = tm(d); return hp(rng.normal(size=len(x)), 7500) * np.exp(-x / 0.012)


def drip(f, d=0.09):   # one wet contact: a pitched drop that bends upward
    x = tm(d); return np.sin(2 * np.pi * (f * x + f * 0.6 * x * x / d)) * np.exp(-x / (d * 0.28)) * np.minimum(1, x / 0.001)


def tick(f=3200, d=0.018):
    x = tm(d); return np.sin(2 * np.pi * f * x) * np.exp(-x / 0.004)


def hit(f=46, d=1.1):
    x = tm(d); n = rng.normal(size=len(x))
    return np.tanh(2.2 * np.sin(2 * np.pi * (f * x + 90 * (1 - np.exp(-x * 26)) / 26))) * np.exp(-x / 0.34) + lp(hp(n, 500), 5000) * np.exp(-x / 0.07) * 0.7


def snip():
    x = tm(0.14); n = rng.normal(size=len(x)); a = hp(n, 3500) * np.exp(-x / 0.012); b = np.roll(hp(n, 2500) * np.exp(-x / 0.016), int(SR * 0.04)); return a + b * 0.8


def pad(notes, d, cut=1200, atk=0.4, rel=0.8):
    x = tm(d); s = np.zeros_like(x)
    for m in notes:
        f = mtof(m)
        for det in (-0.25, 0.25): s += np.sign(np.sin(2 * np.pi * (f + det) * x)) * 0.5 + 2 * ((f + det) * x % 1) - 1
    s = lp(s / (2.6 * len(notes)), cut)
    return s * np.minimum(1, x / atk) * np.minimum(1, (d - x) / rel)


def bass(m, d):
    f = mtof(m); x = tm(d); s = np.tanh(1.8 * (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(4 * np.pi * f * x)))
    return s * np.minimum(1, x / 0.005) * np.minimum(1, (d - x) / 0.03)


# ---------------- the growing drone: 0 to DROP
L = B(DROP); x = tm(L)
grow = np.clip(x / B(14), 0, 1) ** 1.5
f = mtof(30)
dr = np.sin(2 * np.pi * f * x) * (0.5 + 0.5 * grow) + 0.5 * np.tanh(2 * np.sin(2 * np.pi * f * 2 * x + 0.3 * np.sin(2 * np.pi * 0.31 * x))) * grow
dr += 0.28 * lp(np.sign(np.sin(2 * np.pi * mtof(42) * x)), 300 + 1400 * grow * np.ones_like(x)) * grow
dr *= np.minimum(1, x / 0.6) * 0.5
add(0, dr, 0.5); add(0, lp(rng.normal(size=len(x)), 700 + 3000 * grow * np.ones_like(x)) * 0.05 * grow, 1.0)

# the patter: a wet contact for each business reached, denser as the front spreads
D = [np.hypot(n[0] - 640, n[1] - 360) for n in TB["nodes"]]
def reach(b): return 6 + 44 * min(1, max(0, (b - 0.2) / 3.8)) if b < 4 else (3000 if b >= 13 else 50 + 710 * ((b - 4) / 9) ** 1.6)
for d, n in zip(D, TB["nodes"]):
    b = next((q / 20 for q in range(0, 300) if reach(q / 20) >= d), 14)
    if b < 13.9:
        m = [66, 69, 73, 76, 78, 81][int(n[2] + n[0]) % 6]
        add(B(b), drip(mtof(m)), 0.055, pan=(n[0] - 640) / 800)

# the spore's first heartbeat
for b in (0, 2): add(B(b), kick(0.7, 40), 0.75)
for b in np.arange(4, 14, 2.0): add(B(b), kick(0.6, 42), 0.7 + 0.03 * b)
for b in np.arange(8, 14, 1.0): add(B(b), kick(0.3, 50), 0.4)
for b in np.arange(10, 14, 0.5): add(B(b + 0.25), hat(), 0.14)

# ---------------- the words, and the groove behind them
for b in (14, 18): add(B(b), hit(44), 0.95); add(B(b), pad([42, 49, 54, 57], B(3.6), 1600, 0.05, 1.0), 0.32)
for b in np.arange(14, 21, 1.0): add(B(b), kick(0.42), 0.78)
for b in np.arange(15, 21, 2.0): add(B(b), snare(), 0.5)
for b in np.arange(14, 21, 0.5): add(B(b + 0.25), hat(), 0.2)
for k, b in enumerate(np.arange(14, 21, 0.5)): add(B(b), bass([30, 30, 33, 30, 28, 30, 35, 33][k % 8], B(0.46)), 0.42)
# the scores rolling: ticks, climbing
for k, b in enumerate(np.arange(21, DROP - 1.2, 0.125)):
    add(B(b), tick(1800 + k * 70), 0.2 + 0.006 * k, pan=np.sin(k * 1.9) * 0.6);
    if k % 4 == 0: add(B(b), kick(0.25, 54), 0.5)
x = tm(B(3.3)); add(B(21), lp(rng.normal(size=len(x)), 300 + 5000 * (x / x[-1]) ** 2) * (x / x[-1]) ** 2, 0.3)

# ---------------- one held breath (nothing from DROP-1 to DROP), then the collapse
x = tm(B(6)); ff = 92 * np.exp(-x / B(1.1)) + 26; ph = 2 * np.pi * np.cumsum(ff) / SR
sub = np.sin(ph) * np.exp(-x / B(2.4)); add(B(DROP), np.tanh(2.6 * sub), 1.05)
add(B(DROP), hit(36, 1.8), 1.0)
n = rng.normal(size=len(x)); fall = 8000 * np.exp(-x / B(0.8)) + 120
add(B(DROP), lp(n, fall) * np.exp(-x / B(1.5)), 0.42)
# the veins snapping as they starve
for k in range(70):
    b = DROP + 2.2 * (k / 70) ** 0.8 + rng.uniform(0, 0.05); add(B(b), drip(mtof(rng.integers(50, 74)), 0.05), 0.14 - 0.0012 * k, pan=rng.uniform(-0.9, 0.9))
# thirty: a low chord on the turn to 30
add(B(DROP + 2.5), hit(38), 0.85); add(B(DROP + 2.5), pad([30, 42, 49, 57, 61], B(3), 900, 0.05, 1.0), 0.42)

# ---------------- judgement: a tight pulse, the flight along the artery
x = tm(B(2.6)); add(B(FLY - 1), lp(rng.normal(size=len(x)), 200 + 3000 * np.sin(np.pi * x / x[-1]) ** 2) * np.sin(np.pi * x / x[-1]) ** 2, 0.3)
for b in np.arange(FLY, FLIP, 1.0): add(B(b), kick(0.34, 48), 0.72)
for k, b in enumerate(np.arange(FLY, FLIP, 0.5)): add(B(b + 0.25), hat(), 0.18); add(B(b), bass([30, 37, 30, 42][k % 4], B(0.3)), 0.3)
for k, b in enumerate(np.arange(FLY + 1.4, FLY + 2.6, 0.08)): add(B(b), tick(2400 + k * 50), 0.13)
add(B(FLY + 2.6), hit(60, 0.5), 0.5); add(B(FLY + 2.6), pad([54, 61, 66], B(3), 2400, 0.02, 1.0), 0.13)
for k, b in enumerate(np.arange(FLY + 2.6, FLY + 4, 0.05)): add(B(b), tick(4100, 0.01), 0.07)

# ---------------- the flip: three hits
for k, b in enumerate((FLIP, FLIP + 0.5, FLIP + 1.0)): add(B(b), hit(50 + 6 * k, 0.6), 0.92); add(B(b), snare(), 0.5)

# ---------------- the email: warm, with a typed line
add(B(MAIL), pad([42, 49, 54, 57, 61], B(7), 1400, 0.3, 1.2), 0.36)
for b in np.arange(MAIL, NEV, 2.0): add(B(b), kick(0.42), 0.68)
for b in np.arange(MAIL + 1, NEV, 2.0): add(B(b), snare(), 0.32)
for b in np.arange(MAIL, NEV, 0.5): add(B(b + 0.25), hat(), 0.12)
for k, b in enumerate(np.arange(MAIL + 1, MAIL + 3.4, 0.09)): add(B(b), tick(2100 + (k % 5) * 240, 0.012), 0.11, pan=np.sin(k) * 0.3)
add(B(42.6), hit(90, 0.32), 0.5); add(B(42.6), drip(mtof(73), 0.2), 0.3)
add(B(44.5), snip(), 0.85); add(B(44.5), kick(0.4, 34), 0.6)
x = tm(B(1.2)); add(B(44.6), lp(rng.normal(size=len(x)), 1000 * np.exp(-x / 0.25) + 80) * np.exp(-x / 0.25), 0.25)

# ---------------- never twice: the patter comes back, and bends
add(B(NEV), hit(42), 0.92); add(B(NEV + 1.5), hit(46), 0.72)
for b in np.arange(NEV, CLOSE, 1.0): add(B(b), kick(0.42), 0.8)
for b in np.arange(NEV + 1, CLOSE, 2.0): add(B(b), snare(), 0.55)
for b in np.arange(NEV, CLOSE, 0.25): add(B(b), hat(0.035), 0.14)
for k, b in enumerate(np.arange(NEV, CLOSE, 0.5)): add(B(b), bass([30, 30, 33, 30, 28, 28, 35, 33][k % 8], B(0.44)), 0.42)
for k in range(150):
    b = NEV + rng.uniform(0, 7); add(B(b), drip(mtof(rng.choice([66, 69, 73, 76, 78, 81])), 0.08), 0.05, pan=rng.uniform(-0.9, 0.9))

# ---------------- home: everything rushes to one point, then a single chord
x = tm(B(LOGO - CLOSE)); u = x / x[-1]
add(B(CLOSE), lp(rng.normal(size=len(x)), 300 + 9000 * u ** 2) * u ** 2.2, 0.42)
ff = 40 + 200 * u ** 2.4; add(B(CLOSE), np.tanh(2 * np.sin(2 * np.pi * np.cumsum(ff) / SR)) * u ** 1.4, 0.48)
for k, b in enumerate(np.arange(CLOSE, LOGO - 0.5, 0.5)): add(B(b), kick(0.3, 50), 0.5)
add(B(LOGO), hit(42, 2.6), 1.0)
add(B(LOGO), pad([42, 49, 54, 57, 61, 66], B(5), 1700, 0.02, 2.2), 0.42)
add(B(LOGO + 0.3), pad([66, 73, 78], B(4.4), 3000, 0.04, 2.2), 0.12)
for k, m in enumerate([78, 73, 69, 66]): add(B(LOGO + 1 + k * 0.5), drip(mtof(m), 0.3), 0.14)

# ---------------- out
kk = int(0.018 * SR); room = np.zeros_like(out)
for d, g in ((0.031, 0.18), (0.047, 0.15), (0.073, 0.11), (0.113, 0.08)):
    s = int(d * SR); room[s:, 0] += out[:-s, 1] * g; room[s:, 1] += out[:-s, 0] * g
out = out + room
fade = np.ones(N); fl = int(SR * B(0.8)); fade[-fl:] = np.linspace(1, 0, fl) ** 1.6
out[:, 0] *= fade; out[:, 1] *= fade
pk = np.abs(out).max(); out = np.tanh(out / pk * 1.2) * 0.85
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print("score:", DUR, "s, peak", float(np.abs(out).max()))
