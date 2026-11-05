"""The score for R42 · Blackout, composed in code at 100 bpm and timed to bake/table.json: a teletype that speeds up under the
log, a hit per big word; from the first bar a heavy half-time groove in E minor with a wet slap per burst; a long descending
soak into a sub drop; chips flicking into place; a hard stamp with a splash, a dull thud for the refusal; a rush of water
for the wash; one drop; a resolving chord on the logo. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
rng = np.random.default_rng(41)
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


def kick(d=0.5, f=44):
    x = tm(d); return np.sin(2 * np.pi * (f * x + 120 * (1 - np.exp(-x * 30)) / 30)) * np.exp(-x / 0.16)


def click(f=2600, d=0.022):
    x = tm(d); n = rng.normal(size=len(x)); return hp(n, f) * np.exp(-x / 0.005) + 0.5 * np.sin(2 * np.pi * f * 0.6 * x) * np.exp(-x / 0.004)


def slap(d=0.3):   # a wet bar landing on paper
    x = tm(d); n = rng.normal(size=len(x)); return lp(hp(n, 300), 3800) * np.exp(-x / 0.05) * 0.9 + np.sin(2 * np.pi * 110 * x * np.exp(-x * 3)) * np.exp(-x / 0.07)


def snare(d=0.3):
    x = tm(d); return hp(rng.normal(size=len(x)), 1400) * np.exp(-x / 0.08) * 0.7 + np.sin(2 * np.pi * 190 * x) * np.exp(-x / 0.05) * 0.5


def hat(d=0.06):
    x = tm(d); return hp(rng.normal(size=len(x)), 7000) * np.exp(-x / 0.014)


def bass(f, d):
    x = tm(d); s = np.sin(2 * np.pi * f * x) + 0.35 * np.sin(4 * np.pi * f * x) + 0.2 * np.tanh(3 * np.sin(2 * np.pi * f * x))
    return s * np.minimum(1, x / 0.006) * np.minimum(1, (d - x) / 0.03)


def pad(fs, d):
    x = tm(d); s = sum(np.sin(2 * np.pi * f * (1 + e / 300) * x + 1.1 * k) for k, f in enumerate(fs) for e in (-1, 0, 1)) / (3 * len(fs))
    a = min(0.6, d / 3); return s * np.clip(np.minimum(x / a, (d - x) / a), 0, 1)


def stamp():
    x = tm(1.4); n = rng.normal(size=len(x))
    return (np.sin(2 * np.pi * (38 * x + 160 * (1 - np.exp(-x * 34)) / 34)) * np.exp(-x / 0.3) * 1.2 + lp(n, 5000) * np.exp(-x / 0.035) * 1.1 + lp(hp(n, 500), 2600) * np.exp(-x / 0.3) * 0.2)


def splash(d=0.9):
    x = tm(d); n = rng.normal(size=len(x)); drops = sum(np.sin(2 * np.pi * rng.uniform(700, 2400) * (x - t0).clip(0)) * np.exp(-(x - t0).clip(0) / 0.012) * (x > t0) for t0 in rng.uniform(0.03, 0.6, 18))
    return lp(hp(n, 900), 5200) * np.exp(-x / 0.12) * 0.45 + drops * 0.22


def thud():
    x = tm(0.9); return np.sin(2 * np.pi * (34 * x + 60 * (1 - np.exp(-x * 26)) / 26)) * np.exp(-x / 0.24) * 1.5 + lp(rng.normal(size=len(x)), 500) * np.exp(-x / 0.06)


# the log: a teletype that keeps speeding up, typed in the same curve as the film's head of the log
LOCK = 9.8; hits = []
n = len(TB["lines"])
last = -1
for i in range(int(B(LOCK) * 90)):
    t = i / 90; h = 1 + (n - 1) * (min(1, t / B(LOCK))) ** 2.0
    cps = 7 + 1.2 * (h - last) * 90 if last >= 0 else 7
    if not hits or t - hits[-1] > max(0.018, 1 / cps): hits.append(t)
    last = h
for t in hits:
    add(t, click(rng.uniform(2000, 3600)), 0.11 + 0.09 * t / B(LOCK), rng.uniform(-0.3, 0.3))
for at in range(0, 10):
    add(B(at), kick(0.3), 0.32 if at < 6 else 0.5)
for _w, at in TB["big"]:
    add(B(at), slap(), 0.5); add(B(at), bass(mtof(28), 0.4), 0.35)
# a rising line under the race, cut dead at the lock
x = tm(B(LOCK)); up = 55 * 2 ** (x / B(LOCK) * 2.5)
add(0, lp(np.tanh(2 * np.sin(2 * np.pi * np.cumsum(up) / SR)), 300 + 2600 * (x / B(LOCK)) ** 2) * (x / B(LOCK)) ** 2 * 0.34)

# the groove: half time, E minor, C, A minor, B
ROOTS = [28, 24, 33, 35]
def groove(a, z, g=1.0):
    bt = a
    while bt < z:
        k = int(bt) % 4
        if k == 0 or (k == 2 and (bt - a) % 8 > 3): add(B(bt), kick(), 0.85 * g)
        if k == 2: add(B(bt), snare(), 0.42 * g)
        add(B(bt), bass(mtof(ROOTS[int(bt // 4) % 4]), BEAT * 0.9), 0.26 * g)
        for s in range(4): add(B(bt + s / 4), hat(), (0.1 if s % 2 else 0.16) * g, 0.2 * (-1) ** s)
        bt += 1
groove(10, 16.5)
for bu in TB["bursts"]:
    add(B(bu["b"]), slap(), 0.75, rng.uniform(-0.3, 0.3)); add(B(bu["b"] + 0.06), splash(0.4), 0.22)
# the soak: one long descent and water rising, into the sub drop
d = B(17) - B(12.5); x = tm(d); f = 170 * 2 ** (-x / d * 2.6)
add(B(12.5), np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * (x / d) * 0.34)
add(B(12.5), lp(rng.normal(size=len(x)), 300 + 3000 * (1 - x / d) ** 2) * (x / d) ** 2 * 0.2)
xd = tm(3.2); add(B(16.8), np.sin(2 * np.pi * (30 * xd + 50 * (1 - np.exp(-xd * 9)) / 9)) * np.exp(-xd / 1.1), 0.95)
add(B(16.8), stamp(), 0.42); add(B(17.3), slap(), 0.5)
add(B(17), pad([mtof(52), mtof(59), mtof(64), mtof(67)], B(3.2)), 0.1)

# observe: chips flick into place, the groove lighter, then back
for j in range(21):
    L = 20 + (j % 7) * 0.05 + (j // 7) * 0.12
    add(B(L), click(1600, 0.03), 0.3, (j / 21 - 0.5)); add(B(L + 0.9), click(3000, 0.018), 0.16, (j / 21 - 0.5))
add(B(20), kick(), 0.9); groove(21, 28, 0.82)
for at in (21.5, 22, 22.5): add(B(at), slap(), 0.42)
add(B(24), snare(), 0.5)
add(B(20), pad([mtof(40), mtof(52), mtof(55), mtof(59)], B(8)), 0.09)

# approve: tension, the slam, the run, the refusal
for at in (29, 29.5, 30): add(B(at), slap(), 0.45)
x = tm(B(1.6)); add(B(30.4), lp(rng.normal(size=len(x)), 200 + 3500 * (x / x[-1]) ** 3) * (x / x[-1]) ** 3 * 0.3)
add(B(30.8), kick(0.4), 0.5)
add(B(LA := 32), stamp(), 1.0); add(B(LA + 0.02), splash(), 0.6)
groove(32.5, 35.8, 0.85)
for s in range(int(2.4 * 8)): add(B(32.4 + s / 4), click(2800, 0.02), 0.12)
add(B(34.8), click(1200, 0.05), 0.4)
add(B(36), thud(), 1.0); add(B(36), stamp(), 0.42); add(B(36.03), splash(0.5), 0.25)
groove(36.5, 39.7, 0.9); add(B(39.7), kick(0.6), 0.5)
add(B(36), pad([mtof(40), mtof(47), mtof(55)], B(3.5)), 0.1)

# the wash: words appear, then a rush of water
for i in range(5): add(B(40.8 + i * 0.5), snare(), 0.3, -0.3); add(B(40.8 + i * 0.5), bass(mtof(28), 0.25), 0.25)
for i in range(4): add(B(42 + i * 0.5), click(1800, 0.04), 0.4, 0.4)
d = B(5.4); x = tm(d); u = x / d; ev = np.clip(u / 0.08, 0, 1) * np.clip((1 - u) / 0.45, 0, 1) ** 1.6
n1 = rng.normal(size=len(x)); add(B(44), lp(hp(n1, 200), 900 + 5200 * np.sin(np.pi * np.clip(u * 1.35, 0, 1))) * ev, 0.38)
add(B(44), splash(1.4), 0.55)
add(B(44), pad([mtof(40), mtof(47), mtof(52), mtof(56)], B(6)), 0.15)
for i in range(4): add(B(44.5 + i * 0.5), click(3200, 0.03), 0.26, 0.4)
add(B(47), kick(), 0.8); groove(48, 50, 0.6); add(B(47), snare(), 0.32)

# one drop, and the chord
x = tm(0.5); add(B(49.9), np.sin(2 * np.pi * np.cumsum(500 + 1600 * (x / 0.5) ** 2) / SR) * (x / 0.5) ** 2 * 0.1 * (x < 0.36))
x = tm(0.5); add(B(50.5), np.sin(2 * np.pi * np.cumsum(420 + 900 * np.exp(-x * 26)) / SR) * np.exp(-x / 0.06), 0.8)
xd = tm(2.2); add(B(50.5), np.sin(2 * np.pi * (28 * xd + 40 * (1 - np.exp(-xd * 9)) / 9)) * np.exp(-xd / 0.7), 0.9)
add(B(51.7), kick(0.7), 0.7); add(B(51.7), pad([mtof(40), mtof(52), mtof(59), mtof(64), mtof(68), mtof(71)], DUR - B(51.7)), 0.3)
for m, at in ((76, 51.7), (83, 52), (88, 52.3)):
    x = tm(2.6); add(B(at), sum(a * np.sin(2 * np.pi * mtof(m) * k * x) * np.exp(-x * (1.4 + 1.5 * k)) for k, a in ((1, 1), (2.76, 0.3))), 0.13)

# room, master
tail = int(0.18 * SR); wetb = np.zeros_like(out)
for dly, g in ((tail, 0.16), (int(tail * 1.7), 0.09), (int(tail * 2.6), 0.05)):
    wetb[dly:] += out[:-dly] * g
mix = out + wetb
mix = np.tanh(mix * 1.25) * 0.86
fade = np.ones(N); fade[-int(0.5 * SR):] = np.linspace(1, 0, int(0.5 * SR)); mix *= fade[:, None]
mix *= 0.82 / np.max(np.abs(mix)) * 0.42
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("score:", DUR, "s")
