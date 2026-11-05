"""The score for R41 · Hatch, composed in code at 125 bpm in A minor: a low hum under still lines, a hard four-on-the-floor
from the first big word, a rolling sixteenth bass, a press-like tick for the lines, an impact per word, a silence at the gate, a boom
as it opens, a rush down the tunnel, a slam for the refusal, falling whooshes and bright ticks at the publish check, and one held chord.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
rng = np.random.default_rng(141)
B = lambda x: x * BEAT
out = np.zeros((N, 2))


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * (1 - max(0, pan))
    out[i:i + len(sig), 1] += sig * gain * (1 + min(0, pan))


def lp(x, fc):
    fc = np.broadcast_to(fc, x.shape); a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y


def hp(x, fc): return x - lp(x, fc)
def tm(d): return np.arange(int(SR * d)) / SR
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def noise(d): return rng.normal(size=int(SR * d))


def kick(d=0.42, f=46):
    x = tm(d); return np.tanh(1.6 * np.sin(2 * np.pi * (f * x + 150 * (1 - np.exp(-x * 34)) / 34))) * np.exp(-x / 0.13)


def clap(d=0.24):
    x = tm(d); n = hp(lp(noise(d), 5200), 900)
    env = sum(np.exp(-np.clip(x - t0, 0, None) / w) * (x >= t0) for t0, w in ((0, 0.006), (0.012, 0.006), (0.024, 0.07)))
    return n * env


def hat(d=0.05, f=8000):
    x = tm(d); return hp(noise(d), f) * np.exp(-x / 0.011)


def tick(f=2400, d=0.02):
    x = tm(d); return (np.sin(2 * np.pi * f * x) + 0.6 * hp(noise(d), 3000)) * np.exp(-x / 0.004)


def fmbass(m, d, bright=1.0):
    x = tm(d); f = mtof(m); idx = bright * 3.2 * np.exp(-x / 0.07)
    s = np.sin(2 * np.pi * f * x + idx * np.sin(2 * np.pi * f * 2 * x)) + 0.4 * np.sin(2 * np.pi * f * x)
    return np.tanh(1.5 * s) * np.minimum(1, x / 0.003) * np.clip((d - x) / 0.012, 0, 1)


def stab(ms, d=0.3):
    x = tm(d); s = sum(np.tanh(2 * np.sin(2 * np.pi * mtof(m) * x)) for m in ms) / len(ms)
    return lp(s, 500 + 4200 * np.exp(-x / 0.07)) * np.exp(-x / 0.11)


def impact(d=1.1, sub=36):
    x = tm(d); return np.sin(2 * np.pi * (sub * x + 170 * (1 - np.exp(-x * 30)) / 30)) * np.exp(-x / 0.32) * 1.2 + lp(noise(d), 6000) * np.exp(-x / 0.03)


def riser(d, a=300, z=5000):
    x = tm(d); u = x / d; return lp(noise(d), a + (z - a) * u ** 2) * u ** 2


def whoosh(d=0.5, down=True):
    x = tm(d); u = x / d; fc = 5000 * (1 - u) ** 2 + 240 if down else 240 + 5000 * u ** 2
    return lp(hp(noise(d), 120), fc) * np.sin(np.pi * u)


def pad(ms, d):
    x = tm(d); s = sum(np.sin(2 * np.pi * mtof(m) * (1 + e / 400) * x + k) for k, m in enumerate(ms) for e in (-1, 1)) / (2 * len(ms))
    a = min(0.5, d / 3); return s * np.clip(np.minimum(x / a, (d - x) / a), 0, 1)


ROOTS = [33, 33, 29, 31]   # A, A, F, G
PATTERN = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]


def groove(a, z, g=1.0, kicks=True, claps=True):
    s = int(a * 4)
    while s < int(z * 4):
        bt = s / 4; bar = int(bt // 4); pos = s % 16
        if kicks and s % 4 == 0: add(B(bt), kick(), 0.92 * g)
        if claps and s % 8 == 4: add(B(bt), clap(), 0.36 * g, 0.08)
        if s % 4 == 2: add(B(bt), hat(0.09, 7000), 0.17 * g)
        add(B(bt), hat(), (0.06 if s % 2 else 0.09) * g, 0.25 * (-1) ** s)
        if PATTERN[pos]:
            add(B(bt), fmbass(ROOTS[bar % 4] + (12 if pos in (6, 13) else 0), BEAT * 0.23), 0.3 * g)
        add(B(bt), tick(2600 + 300 * (s % 3), 0.014), 0.035 * g, 0.5 * np.sin(s * 0.7))
        s += 1


# rise: a hum under still lines, the sphere swelling, then the first hit
d = B(4); x = tm(d); u = x / d
add(0, (np.sin(2 * np.pi * 55 * x) + 0.3 * np.sin(2 * np.pi * 110.3 * x)) * (0.25 + 0.75 * u) * np.minimum(1, x / 0.8), 0.17)
add(B(0.5), riser(B(3.45), 120, 2600), 0.13)
add(B(4), impact(), 0.85); add(B(4), stab([57, 64, 69, 72], 0.6), 0.26)
for bt in range(5, 8):
    add(B(bt), kick(), 0.82); add(B(bt), stab([57, 64, 72], 0.2), 0.14)
for s in range(16): add(B(4 + s / 4), hat(), 0.05 + 0.006 * s, 0.2 * (-1) ** s)
add(B(6), riser(B(2), 300, 7000), 0.17)

# log and words
add(B(8), impact(), 0.72); groove(8, 20)
for bt in (8, 9, 10): add(B(bt), stab([69, 72, 76], 0.16), 0.16, -0.25 + 0.25 * (bt - 8))
for bt in (11, 14.2):
    add(B(bt), whoosh(B(1), True), 0.2)
for bt, ms in ((12, [57, 64, 69, 72]), (13, [57, 64, 72]), (14, [53, 60, 69, 72]), (17, [55, 62, 67, 71]), (18.5, [57, 64, 69, 76])):
    add(B(bt), impact(0.7), 0.5); add(B(bt), stab(ms, 0.45), 0.26)

# observe: the bars rise as ticks climb, a line on the headline, the drop
groove(20, 30, 0.92)
add(B(20), impact(), 0.62); add(B(20), pad([45, 57, 64, 72], B(10)), 0.07)
for i in range(7): add(B(20.3 + i * 0.3), tick(1200 * 2 ** (i / 6), 0.05), 0.2, -0.5 + i / 6)
for bt in (24, 26): add(B(bt), stab([57, 64, 69], 0.3), 0.25); add(B(bt), clap(), 0.25)
add(B(30), riser(B(1.9), 200, 8000), 0.25)
for i in range(8): add(B(30 + i * 0.25), kick(0.2, 70 + 10 * i), 0.3 + 0.03 * i)

# the gate: a slam, the tension, nothing, the boom
add(B(32), impact(1.3, 30), 0.92)
add(B(32), pad([33, 45, 52, 56], B(3.4)), 0.12)
for bt in (33, 33.5, 34): add(B(bt), kick(0.3), 0.5)
add(B(34), stab([56, 64, 71], 0.5), 0.2)
d = B(1.4); x = tm(d); add(B(34), np.sin(2 * np.pi * 880 * x) * (1 - x / d) ** 2, 0.03)
# beats 35.4 to 36 stay silent
add(B(36), impact(1.6, 28), 1.0); add(B(36), stab([45, 57, 64, 72], 1.0), 0.32); add(B(36), whoosh(0.9, False), 0.4)

# the tunnel: everything at once
groove(36.5, 42, 1.0)
d = B(5.5); x = tm(d); up = mtof(45) * 2 ** (x / d * 2)
add(B(36.5), np.tanh(2 * np.sin(2 * np.pi * np.cumsum(up) / SR)) * (x / d) * 0.11)
add(B(36.5), lp(noise(d), 600 + 7000 * (x / d) ** 2) * (0.3 + 0.7 * (x / d)), 0.11)
for bt in (38, 40):
    add(B(bt), impact(0.6), 0.5); add(B(bt + 1), whoosh(B(1), False), 0.26)
add(B(41), riser(B(1), 400, 9000), 0.3)

# the refusal: full access, a held breath, the X
add(B(42), impact(0.8), 0.74); add(B(42), stab([57, 60, 64], 0.4), 0.3)
add(B(43), impact(0.8), 0.74); add(B(43), stab([57, 60, 64], 0.4), 0.3)
add(B(43.6), riser(B(0.85), 300, 12000), 0.32)
add(B(44.5), impact(2.0, 26), 1.0); add(B(44.5), clap(0.4), 0.8)
x = tm(B(1.1)); add(B(44.5), np.sign(np.sin(2 * np.pi * 58 * x)) * np.exp(-x / 0.25), 0.16)
groove(46, 48, 0.85, claps=False); add(B(46), stab([57, 60, 64], 0.4), 0.26)

# publish check: three falls, three keeps
add(B(48), impact(0.9), 0.62); add(B(48), stab([60, 64, 69], 0.5), 0.22)
groove(49, 58, 0.78)
for i, bt in enumerate((49.6, 50.8, 52)):
    add(B(bt), whoosh(B(1.2), True), 0.4, (i - 1) * 0.5)
    add(B(bt + 0.96), hp(noise(0.14), 900) * np.exp(-tm(0.14) / 0.035), 0.2, (i - 1) * 0.5)
for i, bt in enumerate((53.4, 54.2, 55)):
    add(B(bt + 0.35), kick(0.22, 80), 0.5, (i - 1) * 0.5)
    x = tm(0.7); f = mtof(76 + i * 3 + (2 if i else 0))
    add(B(bt + 0.75), (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * f * 2.76 * x)) * np.exp(-x / 0.14), 0.2, (i - 1) * 0.5)
add(B(56), riser(B(2), 200, 6000), 0.18)

# close: the lines fall into one, a long breath, one chord
d = B(2.2); x = tm(d); f = 220 * 2 ** (-x / d * 3)
add(B(58), np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * (1 - x / d), 0.22)
add(B(58), impact(1.2), 0.75)
xd = tm(1.6); add(B(60), np.sin(2 * np.pi * 2093 * xd) * np.exp(-xd / 0.5), 0.022)
add(B(62), impact(1.6, 30), 0.72)
add(B(62), pad([33, 45, 52, 57, 60, 64, 71], DUR - B(62)), 0.33)
for m, at in ((76, 62), (81, 62.5), (88, 63)):
    x = tm(2.8); add(B(at), sum(a * np.sin(2 * np.pi * mtof(m) * k * x) * np.exp(-x * (1.1 + 1.5 * k)) for k, a in ((1, 1), (2.76, 0.28))), 0.12)

# room and master
tail = int(0.14 * SR); wet = np.zeros_like(out)
for dly, g in ((tail, 0.14), (int(tail * 1.8), 0.08), (int(tail * 2.9), 0.04)):
    wet[dly:] += out[:-dly] * g
mix = np.tanh((out + wet) * 1.2) * 0.9
fade = np.ones(N); fade[-int(0.6 * SR):] = np.linspace(1, 0, int(0.6 * SR)); mix *= fade[:, None]
mix *= 0.82 / np.max(np.abs(mix)) * 0.42
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("score:", DUR, "s")
