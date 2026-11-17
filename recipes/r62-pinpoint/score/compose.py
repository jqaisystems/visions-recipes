"""The score for R62 · Pinpoint, composed in code from the same table as the picture (assets/table.js), so every slam, tick, key
click and whoosh lands on its frame. 124 bpm, A minor (Am, F, C, G). At the freeze the music stops dead; only one held note is left.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py  (run bake/table.py first)"""
import json, os, wave
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
Q, BEAT, NB = T["q"], T["beat"], T["beats"]
SR = 48000; N = int(np.ceil(T["dur"] * SR)) + SR; MIX = np.zeros((N, 2))
rng = np.random.default_rng(62)
sec = lambda b: b * BEAT
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def env(n, a, d):   # attack then exponential decay, in seconds
    t = np.arange(n) / SR; e = np.exp(-t / max(d, 1e-4)); na = int(a * SR)
    if na > 0: e[:na] *= np.linspace(0, 1, na)
    return e
def lp(x, f): b, a = butter(2, min(f, SR * 0.45) / (SR / 2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f / (SR / 2), "high"); return lfilter(b, a, x)
def bp(x, f, q=2.0): lo, hi = f / (1 + 0.5 / q), f * (1 + 0.5 / q); b, a = butter(2, [lo / (SR / 2), min(hi, SR * 0.45) / (SR / 2)], "band"); return lfilter(b, a, x)
def add(b, sig, gain=1.0, pan=0.0):
    i = int(round(sec(b) * SR));
    if i >= N: return
    sig = sig[: N - i] * gain; l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    MIX[i:i + len(sig), 0] += sig * l * 1.414; MIX[i:i + len(sig), 1] += sig * r * 1.414
noise = lambda d: rng.standard_normal(int(d * SR))
tt = lambda d: np.arange(int(d * SR)) / SR

# ---------------- the kit
def kick(big=1.0):
    t = tt(0.5); f = 45 + 95 * np.exp(-t / 0.035); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t / (0.16 * big)) + 0.3 * lp(noise(0.5), 3000) * np.exp(-t / 0.006))
def clap():
    n = noise(0.3); e = np.zeros(len(n)); t = tt(0.3)
    for o in (0, 0.009, 0.018): e += np.exp(-np.clip(t - o, 0, None) / 0.012) * (t >= o)
    e += 0.6 * np.exp(-t / 0.09); return bp(n, 1400, 1.2) * e
def hat(open_=False): t = tt(0.25); return hp(noise(0.25), 7000) * np.exp(-t / (0.09 if open_ else 0.022))
def snare(): t = tt(0.3); return 0.6 * bp(noise(0.3), 2200, 0.8) * np.exp(-t / 0.08) + 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.06)
def crash(d=2.2): t = tt(d); return hp(noise(d), 4500) * np.exp(-t / (d * 0.35))
def slam(size):   # a letter landing: a low tom and a slap of noise
    t = tt(0.4); f = (70 if size > 200 else 120) + 160 * np.exp(-t / 0.03); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.12) + 0.35 * bp(noise(0.4), 1800, 1) * np.exp(-t / 0.03)
def whoosh(d, f0, f1, rise=0.7):
    n = noise(d); t = tt(d); out = np.zeros(len(n)); seg = 1200
    for k in range(0, len(n), seg):
        u = k / len(n); out[k:k + seg] = bp(n[max(0, k - 600):k + seg], f0 * (f1 / f0) ** u, 1.4)[-len(n[k:k + seg]):]
    e = np.minimum(t / (d * rise), 1) ** 2 * np.minimum((d - t) / (d * (1 - rise)), 1); return out * e
def click(f=3200, d=0.012): t = tt(d * 4); return bp(noise(d * 4), f, 2) * np.exp(-t / d)
def bell(m, d=1.6):
    t = tt(d); f = mtof(m); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.2) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.08)) * env(len(t), 0.002, d * 0.3)
def pluck(m, d=0.35, bright=4000):
    t = tt(d); f = mtof(m); x = 2 * ((f * t) % 1) - 1; return lp(x, bright) * env(len(t), 0.002, d * 0.35)
def bassnote(m, d):
    t = tt(d); f = mtof(m); x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + (2 * ((f * t) % 1) - 1) * 0.5
    return lp(x, 420) * env(len(t), 0.003, 0.22) + 0.5 * lp(x, 1800) * env(len(t), 0.002, 0.04) + 0.6 * np.sin(2 * np.pi * f * t) * env(len(t), 0.003, 0.3)
def pad(ms, d, cut=1400):
    t = tt(d); x = sum(sum(2 * ((mtof(m) * (1 + dt) * t) % 1) - 1 for dt in (-0.004, 0.0, 0.005)) for m in ms)
    a = np.minimum(t / 0.6, 1) * np.minimum((d - t) / 0.8, 1); return lp(x, cut) * a / (3 * len(ms))
def riser(d, f0=200, f1=2400):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR; e = (t / d) ** 2.2
    return (0.5 * np.sin(ph) + 0.5 * np.sign(np.sin(ph * 1.003)) * 0.3) * e + whoosh(d, 300, 6000, 0.98) * 0.8

CH = [[45, [69, 72, 76], [57, 60, 64]], [41, [65, 69, 72], [53, 57, 60]], [48, [67, 72, 76], [55, 60, 64]], [43, [67, 71, 74], [55, 59, 62]]]
chord = lambda b: CH[int(b // 4) % 4]

# ---------------- the open: a tick, the drop, the bounce, the gathering, the burst
add(0.15, click(5000, 0.02), 0.25)
t = tt(sec(1.0)); f = 1900 * (300 / 1900) ** (t / t[-1]); add(1.0, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.linspace(0.2, 1, len(t)), 0.12)
add(2.0, kick(0.8), 0.9); add(2.0, bell(81, 1.2), 0.08)
add(2.5, riser(sec(0.5), 150, 1800), 0.5)
add(3.0, kick(2.4), 1.2); add(3.0, crash(3.0), 0.5); add(3.0, whoosh(sec(1.6), 4000, 300, 0.05), 0.5)
t = tt(1.4); add(3.0, np.sin(2 * np.pi * np.cumsum(55 * (30 / 55) ** (t / 1.4)) / SR) * np.exp(-t / 0.6), 0.8)

# ---------------- the groove: where the drums, bass and arp play
def groove(b0, b1, claps=True, arp=True, hats16=False, gain=1.0):
    b = b0
    while b < b1 - 1e-6:
        add(b, kick(), 0.85 * gain)
        if claps and int(round(b)) % 2 == 1: add(b, clap(), 0.32 * gain)
        add(b + 0.5, hat(int(round(b)) % 4 == 3), 0.12 * gain, 0.3)
        if hats16: add(b + 0.25, hat(), 0.05 * gain, -0.3); add(b + 0.75, hat(), 0.05 * gain, -0.3)
        root = chord(b)[0]
        for k, o in enumerate((0, 0.5)): add(b + o, bassnote(root + (12 if (int(b * 2) + k) % 4 == 3 else 0), sec(0.45)), 0.42 * gain)
        if arp:
            tones = chord(b)[1]
            for k in range(4): add(b + k * 0.25, pluck(tones[(int(b * 4) + k) % 3] + (12 if k == 3 else 0), 0.3, 3200), 0.1 * gain, 0.35 if k % 2 else -0.35)
        b += 1
groove(5.0, 14.4, claps=False, arp=False)
for b in np.arange(9.0, 14.4, 0.25): tones = chord(b)[1]; add(b, pluck(tones[int(b * 4) % 3] + 12, 0.25, 3000), 0.07, 0.4 if int(b * 4) % 2 else -0.4)
groove(16.0, 39.7, hats16=True)
groove(39.7, 50.4, arp=False)
groove(50.4, 53.2, arp=False, gain=0.8)
add(16.0, crash(2.6), 0.45); add(30.0, crash(2.2), 0.35); add(39.7, crash(2.0), 0.3)
for b0, b1 in [(5.0, 14.4), (16.0, 39.7), (39.7, 50.4)]:
    b = b0
    while b < b1 - 0.01:
        d = min(4 - (b % 4), b1 - b); add(b, pad(chord(b)[2], sec(d) + 0.3, 1100), 0.16); b += d

# ---------------- every big word: each letter lands on a hit
for hi, h in enumerate(T["heads"]):   # the first four are the big words
    big = 400 if hi < 4 else 100
    lands = [L for row in h[7] for L in row if L is not None]
    for i, L in enumerate(lands):
        if h[6] == "slam": add(L, slam(big), 0.42 if hi < 4 else 0.26, ((i / max(1, len(lands) - 1)) - 0.5) * 0.8); add(L - 0.2, whoosh(sec(0.2), 1500, 5000, 0.9), 0.07)
        else: add(L, click(2600, 0.01), 0.16, ((i / max(1, len(lands) - 1)) - 0.5) * 0.6)

# ---------------- 01 find: the lens sparkles as the matches light; the lock; the dive
# the lens sweep: a sprinkle of high bells on an eighth-note grid as the matches light
for k, b in enumerate(np.arange(9.25, 13.2, 0.125)):
    if rng.random() < 0.6: add(b, bell([81, 84, 86, 88, 91][int(rng.integers(5))], 0.6), 0.03, float(rng.uniform(-0.7, 0.7)))
add(Q["lock"], click(1800, 0.02), 0.5); add(Q["lock"], bell(81, 1.4), 0.12); add(Q["lock"], bell(88, 1.4), 0.08)
add(Q["zoom"], riser(sec(Q["score"] - Q["zoom"]), 120, 3000), 0.55)
for k, b in enumerate(np.arange(Q["zoom"] + 0.6, Q["score"], 0.125)): add(b, snare(), 0.08 + 0.18 * k / 13)
add(Q["score"], kick(2.0), 1.0)

# ---------------- 02 score: the dial ticks, the needle sings its value, the gauge falls, the bars pluck and swish into order
for k, b in enumerate(T["dialTicks"]): add(b, click(4200 if k % 4 else 2600, 0.008), 0.18 if k % 4 else 0.3, -0.6 + 1.2 * k / 40)
b0, b1 = Q["needle"] + 0.4, Q["morph"]; t = tt(sec(b1 - b0)); bt = b0 + t / BEAT
v = np.clip(87 - 87 * np.exp(-2.2 * (bt - b0)) * np.cos(5.5 * (bt - b0)), 0, 100)
f = 220 * 2 ** (v / 40); add(b0, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / 0.05, 1) * np.minimum((t[-1] - t) / 0.3, 1) * 0.5, 0.18)
add(Q["needle"], whoosh(sec(0.5), 600, 3000, 0.8), 0.18)
for k in range(41):
    if k % 3 == 0: add(Q["morph"] + 0.3 + k * 0.012, bell(84 + (k * 5) % 12, 0.4), 0.025, -0.6 + 1.2 * k / 40)
RANK = sorted(range(8), key=lambda i: -T["bars"][i])
for rk, i in enumerate(RANK):
    if i != T["heroBar"]: add(Q["bars"] + rk * 0.1, pluck(57 + int(T["bars"][i] / 100 * 24), 0.4, 2600), 0.14)
    add(Q["sort"] + rk * 0.08, whoosh(sec(0.6), 900, 3500, 0.5), 0.05, -0.4 + rk * 0.1)
add(Q["warm"], pad([69, 72, 76, 79], sec(1.6), 2400), 0.22)
add(Q["toCard"], whoosh(sec(0.6), 3000, 600, 0.3), 0.18)
add(Q["wipe"], whoosh(sec(0.8), 400, 4000, 0.85), 0.3); add(30.0, kick(1.6), 0.7)

# ---------------- 03 enrich: the card opens, each row slams in, each is ticked, the scan, the flip
add(Q["card"], whoosh(sec(0.8), 500, 2500, 0.6), 0.2)
for i in range(len(T["rows"])):
    L = Q["rows"] + i * Q["rowGap"]; add(L - 0.3, whoosh(sec(0.3), 1200, 4000, 0.9), 0.14, -0.6 if i % 2 == 0 else 0.6); add(L, slam(100), 0.2, -0.3 if i % 2 == 0 else 0.3)
    add(Q["ticks"] + i * 0.25 + 0.15, bell(86 + [0, 2, 4, 7, 9, 12][i], 0.5), 0.06)
add(Q["ticks"] - 0.2, whoosh(sec(1.6), 800, 2400, 0.5), 0.08)
add(Q["flip"], whoosh(sec(1.0), 700, 4500, 0.5), 0.25); add(Q["flipMid"] + 0.5, kick(1.2), 0.5)

# ---------------- 04 draft: every key, the stamp, the fold, the flight and the build to the button
for lines, times in ((T["hdr"], T["typeHdr"]), (T["msg"], T["typeMsg"])):
    for ln, row in zip(lines, times):
        for ch, b in zip(ln, row):
            if ch != " ": add(b, click(float(rng.uniform(2400, 3800)), 0.006), float(rng.uniform(0.12, 0.2)), float(rng.uniform(-0.3, 0.3)))
add(Q["stamp"], kick(0.6), 0.5); add(Q["stamp"], snare(), 0.25)
for b in (Q["fold"], 50.85, 51.0, 51.15): add(b, bp(noise(0.14), 3000, 0.6) * env(int(0.14 * SR), 0.004, 0.03), 0.3, float(rng.uniform(-0.4, 0.4)))
add(Q["fly"], whoosh(sec(1.4), 500, 5000, 0.4), 0.35, 0.5)
add(Q["button"], pluck(81, 0.6, 5000), 0.2); add(Q["button"] + 0.35, kick(0.7), 0.4)
t = sec(Q["freeze"] - Q["button"]); add(Q["button"], riser(t, 200, 3200), 0.5)
for k, b in enumerate(np.arange(Q["button"], Q["freeze"], 0.25)): add(b, snare(), 0.06 + 0.2 * k / 11)
for b in np.arange(Q["button"], Q["freeze"]): add(b, kick(), 0.75); add(b, bassnote(45, sec(0.45)), 0.4); add(b + 0.5, bassnote(45, sec(0.45)), 0.4)

# ---------------- the freeze: everything stops. One quiet high note holds; it is only the button, waiting
CUT = int(round(sec(Q["freeze"]) * SR)); fade = int(0.012 * SR); MIX[CUT:CUT + fade] *= np.linspace(1, 0, fade)[:, None]; MIX[CUT + fade:] = 0
d = sec(Q["close"] - Q["freeze"]); t = tt(d); add(Q["freeze"], np.sin(2 * np.pi * mtof(81) * t) * np.minimum(t / 0.8, 1) * np.minimum((d - t) / 0.5, 1), 0.05)
for h in T["heads"][4:5]:
    for i, L in enumerate([L for row in h[7] for L in row if L is not None]): add(L, click(2600, 0.01), 0.16, (i / 13 - 0.5) * 0.6)
for h in T["heads"][5:6]:
    lands = [L for row in h[7] for L in row if L is not None]
    for i, L in enumerate(lands): add(L, slam(100), 0.2, ((i / max(1, len(lands) - 1)) - 0.5) * 0.8)
b = 60.4
while b < Q["collapse"]: d2 = min(4 - (b % 4), Q["collapse"] - b); add(b, pad(chord(b)[2], sec(d2) + 0.4, 900), 0.14); b += d2
for b in np.arange(60.4, Q["collapse"]): t = tt(0.4); add(b, np.sin(2 * np.pi * 50 * t) * env(len(t), 0.01, 0.15), 0.25)
add(Q["cursor"] + 1.0, bell(88, 1.0), 0.07)
add(Q["collapse"], riser(sec(Q["close"] - Q["collapse"]), 300, 4000), 0.4)

# ---------------- the close: one chord, a bell, the room
add(Q["close"], kick(2.2), 0.9); add(Q["close"], crash(4.0), 0.3)
for m in (45, 57, 64, 69, 71, 72, 76): add(Q["close"], pad([m], sec(NB - Q["close"]), 2000), 0.35)
for m in (81, 88, 93): add(Q["close"] + 0.3, bell(m, 3.0), 0.07)

# ---------------- a short room, the end fade, the level
ir = np.exp(-tt(1.2) / 0.3) * rng.standard_normal(int(1.2 * SR)) * 0.02; ir = lp(ir, 5000)
wet = np.stack([fftconvolve(MIX[:, c], ir)[:N] for c in range(2)], 1); out = MIX + wet * 0.5
n = int(round(T["dur"] * SR)); out = out[:n]; fe = int(0.6 * SR); out[-fe:] *= np.linspace(1, 0, fe)[:, None]
out *= 10 ** (-1.5 / 20) / np.max(np.abs(out))
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype("<i2").tobytes()); w.close(); print("score", round(n / SR, 3), "s")
