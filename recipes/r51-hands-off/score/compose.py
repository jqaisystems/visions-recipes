"""The score for R51 · Hands Off, composed in code at 100 bpm in A minor, warm and close: plucked strings and a hand drum, with the sand itself as noise shaped to every stroke in the table.
While the finger works, the music follows it, loose. When it lifts there's near silence. Then the rhythm comes back machine-tight, with the sand on every sixteenth.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
B = lambda x: x * BEAT
out = np.zeros((N, 2)); rng = np.random.default_rng(50)


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_c = {}
def pluck(m, dur=1.3, bright=6, damp=0.996):
    """A plucked string (Karplus-Strong), worked out one period at a time."""
    k = (m, dur, bright, damp)
    if k not in _c:
        n = int(dur * SR); p = max(2, int(round(SR / midi(m)))); g = np.random.default_rng(m); buf = np.convolve(g.uniform(-1, 1, p), np.ones(bright) / bright, "same") * 1.8; x = np.zeros(n)
        for i in range(0, n, p):
            e = min(p, n - i); x[i:i + e] = buf[:e]; buf = 0.5 * (buf + np.roll(buf, -1)) * damp
        t = np.arange(n) / SR
        _c[k] = x * np.minimum(1, t * 1200) * np.minimum(1, (dur - t) * 25)
    return _c[k]


def noise(n, seed): return np.random.default_rng(seed).normal(0, 1, n)


def band(x, lo, hi):
    """A plain FFT band-pass."""
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(f * np.exp(-((np.log(np.maximum(fr, 1)) - math.log(math.sqrt(lo * hi))) / (0.5 * math.log(hi / lo))) ** 2), len(x))


SAND = band(noise(SR * 4, 1), 2400, 11000); SAND /= np.abs(SAND).max()
LOWS = band(noise(SR * 4, 2), 300, 1800); LOWS /= np.abs(LOWS).max()


def sand(dur, seed=0, low=0.3):
    """Sand moving: bright noise with a little body, full of tiny uneven grains."""
    n = int(dur * SR); i = (seed * 9973) % (SR * 3); j = (seed * 4111) % (SR * 3)
    x = np.resize(SAND[i:], n) + low * np.resize(LOWS[j:], n)
    g = np.random.default_rng(seed).uniform(0.45, 1.0, n // 240 + 2); e = np.interp(np.arange(n), np.arange(len(g)) * 240, g)
    return x * e


def drum(f=74.0, dur=0.5, drop=1.9, seed=0):
    """A hand drum: a low skin that bends, with the slap of a palm on it."""
    t = np.arange(int(dur * SR)) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + drop * np.exp(-t * 46))) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.22 * sand(dur, seed + 300, 1.0) * np.exp(-t * 80)


def tak(seed=0):
    t = np.arange(int(0.16 * SR)) / SR
    return (np.sin(2 * np.pi * 430 * t) * 0.55 + 0.7 * band(noise(len(t), seed + 40), 700, 4000) * 3) * np.exp(-t * 42)


def click(f=2400.0):
    t = np.arange(int(0.05 * SR)) / SR; return (np.sin(2 * np.pi * f * t) * 0.5 + noise(len(t), 8) * 0.5) * np.exp(-t * 240)


def pad(m, dur):
    t = np.arange(int(dur * SR)) / SR; x = sum(np.sin(2 * np.pi * midi(m) * q * t + q) / q for q in (1.0, 1.003, 2.0, 3.0))
    return x * np.minimum(1, t * 0.7) * np.minimum(1, (dur - t) * 0.8)


# ---- the harmony, four beats a bar: Am, F, C, G, in the low strings
CH = [(45, [57, 60, 64, 69]), (41, [57, 60, 65, 69]), (48, [55, 60, 64, 67]), (43, [55, 59, 62, 67])]
def chord(b): return CH[int(b // 4) % 4]


# ---- light on
add(B(TB["clickOn"]), click(), 0.5, -0.2)
add(B(TB["clickOn"]) + 0.01, click(900.0), 0.5, 0.2)
p0, p1 = TB["pour"]; dp = B(p1 - p0); x = sand(dp, 5, 0.9); t = np.arange(len(x)) / SR
add(B(p0), x * np.minimum(1, t * 7) * (0.8 + 0.2 * np.sin(t * 5)) * np.minimum(1, (dp - t) * 1.8), 0.24)

# ---- the sand itself: every stroke in the table, as loud as it's fast
for k, (b0, b1, loud, kind) in enumerate(TB["hiss"]):
    if kind == 9 or loud <= 0: continue
    d = B(b1 - b0) + 0.04; x = sand(d, k + 7, 0.6 if kind == 1 else 0.2); t = np.arange(len(x)) / SR
    env = np.minimum(1, t * 90) * np.minimum(1, (d - t) * 26)
    add(B(b0), x * env, (0.22 if kind == 1 else 0.075) * loud, (k % 5 - 2) * 0.14)

# ---- by hand: loose, a little late, following the finger
lift, alone = TB["lift"], TB["alone"]
j = np.random.default_rng(3)
for b in range(5, int(lift)):
    root, up = chord(b); late = float(j.uniform(0, 0.02)); busy = b >= 16
    if b % 2 == 0: add(B(b) + late, pluck(root - 12 + 12, 1.8, 8), 0.34, -0.1)
    if b % 4 == 0: add(B(b) + late, drum(70, 0.5, seed=b), 0.3, 0.05)
    if busy and b % 4 == 2: add(B(b) + late, tak(b), 0.1, 0.25)
    add(B(b) + late, pluck(up[b % 4], 1.2), 0.15, -0.3 + 0.2 * (b % 4))
    if b >= 11: add(B(b + 0.5) + float(j.uniform(0, 0.025)), pluck(up[(b * 3 + 1) % 4] + 12 * (b >= 19), 0.9), 0.1, 0.3)
    if busy and b % 2 == 1: add(B(b + 0.75) + late, tak(b + 50), 0.05, -0.25)

# ---- the last dot, the lift, and one note left in the room
add(B(29.5), drum(58, 0.8, seed=2), 0.55)
add(B(29.5), pluck(45, 3.2, 10, 0.998), 0.3)
add(B(lift), pluck(69, 2.6, 10, 0.998), 0.1, 0.2)
add(B(lift + 1.0), pluck(76, 2.4, 10, 0.998), 0.05, -0.2)

# ---- alone: exactly on the grid, with the sand as the hi-hat
wall = TB["wall0"]; clear = TB["morning"][0] + 0.4; off = TB["clickOff"]
for s16 in range(int(alone * 4), int(off * 4)):
    b = s16 / 4; root, up = chord(b); ib = int(b // 1); frac = s16 % 4
    grow = min(1.0, (b - alone) / 8)
    night = 0.55 if TB["night"][0] + 1 < b < clear else 1.0
    add(B(b), sand(0.05 + 0.03 * (frac == 2), s16 % 37 + 90, 0.1) * np.exp(-np.arange(int((0.05 + 0.03 * (frac == 2)) * SR)) / SR * 70), (0.22 if frac == 2 else 0.13) * (0.5 + 0.5 * grow), 0.3 if frac % 2 else -0.3)
    if frac == 0:
        add(B(b), drum(62, 0.42, 2.4, s16), 0.72 * night if b >= alone else 0)
        if ib % 2 == 1: add(B(b), tak(ib) , 0.24 * night, 0.1)
    if frac in (0, 3) or (frac == 2 and ib % 2 == 1): add(B(b), pluck(root, 0.5, 8, 0.99), 0.42 * night, -0.05)
    if b >= wall or frac % 2 == 0: add(B(b), pluck(up[(s16 * 3) % 4] + 12 * (s16 % 8 == 3), 0.42, 5, 0.99), (0.13 if b >= wall else 0.1) * (0.7 + 0.3 * grow), 0.45 * math.sin(s16 * 1.7))
# the wall is many: a shimmer of sand under it all
if wall < clear:
    d = B(clear - wall); x = sand(d, 77, 0.2); t = np.arange(len(x)) / SR
    add(B(wall), x * np.minimum(1, t * 1.2) * np.minimum(1, (d - t) * 8), 0.05)
# the night: something long and cold under it
n0, n1 = TB["night"]; d = B(TB["morning"][1] - n0)
add(B(n0), pad(57, d) * 0.5 + pad(64, d) * 0.3, 0.05, -0.1)
# the wall lands whole: one big hit, with every string
add(B(TB["land"]), drum(50, 1.3, 2.6, seed=21), 0.7)
for m, pn in [(33, 0), (45, 0.1), (57, -0.2), (60, 0.2), (64, -0.3), (69, 0.3)]: add(B(TB["land"]), pluck(m, 2.4, 5, 0.998), 0.2, pn)
# morning: the sweep, and the tune lands
for q, m in enumerate([69, 72, 76, 81]): add(B(clear + 1.0 + q * 0.5), pluck(m, 2.4, 6, 0.998), 0.2, -0.3 + q * 0.2)

# ---- light off, and one last chord on the mark
stop = int(B(off) * SR); fade = np.ones(N); fade[stop:] = 0.0; fade[stop - 200:stop] = np.linspace(1, 0, 200); out *= fade[:, None]
add(B(off), click(), 0.55)
add(B(off) + 0.01, click(900.0), 0.5)
add(B(TB["logo"]), drum(52, 1.2, 1.6, seed=9), 0.4)
for m, pn in [(33, 0), (45, -0.1), (57, 0.1), (64, -0.25), (69, 0.25), (72, 0.05)]: add(B(TB["logo"]), pluck(m, 2.9, 7, 0.999), 0.24, pn)

# ---- a small room, and the master
L = int(0.34 * SR); ir = np.random.default_rng(11).normal(0, 1, L) * np.exp(-np.arange(L) / SR * 14)
for c in (0, 1):
    wet = np.fft.irfft(np.fft.rfft(out[:, c], N + L) * np.fft.rfft(np.roll(ir, c * 7), N + L), N + L)[:N]
    out[:, c] += wet * 0.016
out = np.tanh(out * 1.05)
tail = int(0.25 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
pk = np.abs(out).max(); out = out / pk * 0.76
print("score", round(N / SR, 3), "peak", pk)
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
