"""The score for R47 · Flywheel, composed in code at 120 bpm in G major: wooden and toy-like. Marimba, woodblock and an upright bass, with a soft
wet squelch on each big clay move. The wheel's click is the tempo, so as the days speed up the music speeds up with them. One held breath
before day one. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR); rng = np.random.default_rng(47)
B = lambda x: x * BEAT
out = np.zeros((N, 2))


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_m = {}
def marimba(m, dec=7.0, dur=0.6):
    k = (m, dec, dur)
    if k not in _m:
        t = np.arange(int(dur * SR)) / SR; f = midi(m)
        _m[k] = (np.sin(2 * np.pi * f * t) + 0.32 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * dec * 3) + 0.08 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t * dec * 7)) * np.exp(-t * dec) * np.minimum(1, t * 600)
    return _m[k]


def block(f=1250.0, dec=46.0, dur=0.09):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.42 * t)) * np.exp(-t * dec) * np.minimum(1, t * 3000)


def bass(m, dur=0.62):
    t = np.arange(int(dur * SR)) / SR; f = midi(m)
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 9) + 0.2 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t * 16)
    return x * np.exp(-t * 3.6) * np.minimum(1, t * 260) * np.minimum(1, (dur - t) * 40)


def squelch(dur=0.42, f0=240.0, f1=70.0, seed=0):
    """Wet clay: a falling, gurgling tone under a little filtered noise."""
    t = np.arange(int(dur * SR)) / SR; g = np.random.default_rng(seed)
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.16 * np.sin(2 * np.pi * 27 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    n = g.normal(0, 1, len(t)); w = 40; n = np.convolve(n, np.ones(w) / w, "same") * 2.2
    return (x + 0.55 * n) * np.exp(-t * 7 / dur * 0.6) * np.minimum(1, t * 300) * np.minimum(1, (dur - t) * 60)


def thud(f=62.0, dur=0.7, drop=2.2):
    t = np.arange(int(dur * SR)) / SR
    p = 2 * np.pi * np.cumsum(f * (1 + drop * np.exp(-t * 34))) / SR
    return np.sin(p) * np.exp(-t * 6.0) * np.minimum(1, t * 800)


CH = {"G": [43, 55, 59, 62, 67, 71, 74], "C": [48, 55, 60, 64, 67, 72, 76], "Em": [40, 52, 59, 64, 67, 71, 76], "D": [50, 57, 62, 66, 69, 74, 78]}
PROG = ["G", "C", "Em", "D"]
PENTA = [55, 57, 59, 62, 64, 67, 69, 71, 74, 76, 79, 81]


def chord_at(b): return PROG[int(b // 4) % 4]


# ---- 1. one lump: a fall, a thud, a wobble, and a thumb
add(B(TB["drop"]) - 0.02, np.sin(2 * np.pi * np.cumsum(np.linspace(900, 180, int(0.26 * SR))) / SR) * np.linspace(0, 1, int(0.26 * SR)) ** 2, 0.1)
add(B(TB["drop"] + 0.5), thud(), 0.95); add(B(TB["drop"] + 0.5), squelch(0.5, 170, 60, 1), 0.34)
add(B(2.25), marimba(55, 8), 0.18); add(B(2.75), marimba(62, 8), 0.14)
add(B(3.0), squelch(0.3, 340, 150, 2), 0.3)
# ---- 2 and 3. strategy, batch: the band comes in
for b in np.arange(TB["strat"], TB["breath"], 1.0):
    ch = chord_at(b); add(B(b), bass(CH[ch][0] + (12 if b % 2 else 0)), 0.3 if b < TB["batch"] else 0.34)
    if b % 2 == 0: add(B(b), thud(58, 0.28, 1.7), 0.42)
    else: add(B(b), block(780, 34), 0.1, -0.2)
    if int(b) % 4 == 3: add(B(b + 0.5), block(980, 40), 0.09, 0.2)
for k, b in enumerate(np.arange(TB["strat"], TB["batch"], 0.5)):
    c = CH[chord_at(b)]; m = c[2 + (k * 3) % 5]; add(B(b), marimba(m + 12), 0.17, 0.45 * math.sin(k))
for i in range(5):                                        # each board growing
    add(B(TB["strat"] + 0.5 + i * 0.34), squelch(0.22, 180 + i * 50, 340 + i * 60, 3 + i), 0.15, -0.5 + i * 0.25)
add(B(TB["strat"]), squelch(0.55, 200, 70, 8), 0.3)
add(B(TB["batch"]), squelch(0.55, 230, 75, 9), 0.3)
# the rolling pin: a low rumble
r0, r1 = B(TB["batch"] + 0.2), B(TB["cut"] - 0.1); nr = int((r1 - r0) * SR); rum = rng.normal(0, 1, nr); rum = np.convolve(rum, np.ones(160) / 160, "same") * 6 * np.sin(np.linspace(0, np.pi, nr)) ** 0.7
add(r0, rum, 0.12)
# the cutter: a tick for every pin, a marimba run through the chord
for i, b in enumerate(TB["cuts"]):
    add(B(b), block(1700 + 240 * (i % 3), 70, 0.05), 0.07, -0.7 + 1.4 * ((i % 12) / 11))
    if i % 3 == 0:
        c = CH[chord_at(b)]; add(B(b), marimba(c[1 + (i // 3) % 6] + 12, 11, 0.35), 0.16, -0.5 + ((i % 12) / 11))
for b in np.arange(TB["cut"], TB["approve"], 2.0):
    add(B(b), marimba(CH[chord_at(b)][3] + 24, 6, 0.8), 0.09, 0.3)
# ---- 4. one stamp: everything stops, then the biggest thud in the film
add(B(TB["stamp"] - 1.4), squelch(0.7, 60, 240, 12), 0.1)
add(B(TB["stamp"]), thud(46, 1.3, 3.2), 1.25); add(B(TB["stamp"]), squelch(0.6, 150, 50, 13), 0.5)
for m in (43, 55, 62, 67, 71): add(B(TB["stamp"]), marimba(m + 12, 3.6, 1.3), 0.24)
for j, m in enumerate((74, 71, 74, 79)): add(B(TB["stamp"] + 1.0 + j * 0.5), marimba(m, 7), 0.2)
# ---- 5. the wheel: pins load upward, the wheel groans under the weight, one breath
add(B(TB["wheel"]), squelch(0.8, 120, 280, 15), 0.34)
for i in range(36):
    b = TB["wheel"] + 0.4 + (TB["breath"] - 0.65 - TB["wheel"]) * math.sqrt(i / 36)
    add(B(b), marimba(PENTA[(i * 2) % len(PENTA)] + (12 if i > 24 else 0), 13, 0.28), 0.13, math.sin(i * 0.7) * 0.5)
n = int(B(TB["breath"] - TB["wheel"] - 1.8) * SR); t = np.arange(n) / SR
groan = np.sin(2 * np.pi * np.cumsum(58 + 11 * (t / t[-1]) ** 2 + 2.2 * np.sin(2 * np.pi * 5.2 * t)) / SR) * (t / t[-1]) ** 1.3 * np.minimum(1, (t[-1] - t) * 18)
add(B(TB["wheel"] + 1.8), groan, 0.2)
# silence from the breath to day one is the point: anything still ringing is faded below
# ---- 6. the days: the click is the tempo. Each day is a woodblock and one marimba note
for d, b in enumerate(TB["clicks"]):
    slow = d < 20; v = 1.0 if d < 5 else 0.82 if slow else 0.52
    add(B(b), block(1300 + 90 * ((d * 5) % 3), 40), 0.3 * v, -0.15)
    if d < 5: add(B(b), thud(68, 0.4, 2.2), 0.62)
    c = CH[chord_at(b)]; m = PENTA[(d * 3) % len(PENTA)] if d >= 5 else [67, 71, 74, 79, 81][d]
    add(B(b), marimba(m + (0 if d < 20 else 12), 8.5 if slow else 15, 0.5), 0.24 * v, -0.55 + 1.1 * ((d % 12) / 11))
    if slow: add(B(b + 0.42), squelch(0.1, 300, 150, 40 + d), 0.1, 0.5)
# the band under the acceleration, on its own grid, while the clicks run past it
for b in np.arange(TB["day1"] + 6, TB["pull"], 1.0):
    ch = chord_at(b); add(B(b), bass(CH[ch][0] + (12 if b % 2 else 0)), 0.34)
    if b % 2 == 0: add(B(b), thud(58, 0.26, 1.7), 0.42)
    if b >= TB["seasons"]:
        for s in (0, 0.5): add(B(b + s), block(2300, 90, 0.04), 0.05 + 0.05 * (b - TB["seasons"]) / 11, 0.35)
for b in np.arange(TB["seasons"], TB["pull"], 4.0):       # each season, a chord that opens
    for j, m in enumerate(CH[chord_at(b)][1:6]): add(B(b + j * 0.08), marimba(m + 12, 3.0, 1.6), 0.13, -0.5 + j * 0.25)
# ---- 7. nobody touches it: the band leaves, the wheel keeps ticking slowly
for k, b in enumerate(np.arange(TB["pull"], TB["melt"], 0.5)):
    add(B(b), block(1250, 44), 0.13, -0.15)
    if k % 2 == 0: add(B(b), marimba([67, 71, 74, 71, 69, 67, 62, 67, 71, 74][(k // 2) % 10] + 12, 5.5, 1.0), 0.22, 0.25 * math.sin(k))
    if k % 4 == 0: add(B(b), bass(CH[chord_at(b)][0]), 0.3)
# ---- 8. it all slumps, one last squash, and the chord
add(B(TB["melt"]), squelch(1.3, 210, 44, 80), 0.52)
add(B(TB["melt"] + 1.1), thud(50, 0.9, 2.4), 0.95); add(B(TB["melt"] + 1.1), squelch(0.45, 150, 60, 81), 0.32)
n = int(B(1.2) * SR); add(B(TB["logo"] - 1.1), np.sin(2 * np.pi * np.cumsum(np.linspace(46, 34, n)) / SR) * np.linspace(0, 1, n) ** 2, 0.24)
for j, m in enumerate((43, 55, 62, 67, 71, 74, 79)): add(B(TB["logo"]) + j * 0.03, marimba(m + 0, 1.9, 3.0), 0.2 if m > 50 else 0.34, -0.45 + j * 0.15)

# a small room, so it sounds like a table and not a computer
ir = np.zeros(int(0.32 * SR))
for k, (ms, g) in enumerate(((13, 0.3), (23, 0.24), (37, 0.2), (53, 0.13), (79, 0.09), (113, 0.05), (167, 0.03))):
    ir[int(ms * SR / 1000)] = g
for ch in range(2):
    wet = np.convolve(out[:, ch], np.roll(ir, ch * 31))[:N]
    out[:, ch] += wet * 0.55
# the breath: everything fades just before it, and day one lands in silence
i0, i1, i2 = int(B(TB["breath"] - 0.25) * SR), int(B(TB["breath"]) * SR), int(B(TB["day1"] - 0.03) * SR)
env = np.ones(N); env[i0:i1] = np.linspace(1, 0.02, i1 - i0); env[i1:i2] = 0.02; out *= env[:, None]
# the last fade
i3 = int(B(63.3) * SR); out[i3:] *= np.linspace(1, 0, N - i3)[:, None] ** 2
out = np.tanh(out * 0.95)
pk = np.max(np.abs(out)); out = out / pk * 0.72
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print("score", DUR, "peak", float(pk))
