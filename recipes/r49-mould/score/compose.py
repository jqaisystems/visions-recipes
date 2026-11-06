"""The score for R49 · Mould, composed in code at 104 bpm in D minor, late-night and physical: upright bass, brushed drums and vibraphone, with the
press as the kick and a wet slap for each picture. The band only starts once the system is on. Full stop for the pink picture, one stamp, then the
band comes back. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
B = lambda x: x * BEAT
out = np.zeros((N, 2))


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_c = {}
def bass(m, dur=0.62):
    """An upright bass: a plucked string with a soft, woody attack."""
    k = (m, dur)
    if k not in _c:
        n = int(dur * SR); p = max(2, int(SR / midi(m))); g = np.random.default_rng(m); buf = np.convolve(g.uniform(-1, 1, p), np.ones(12) / 12, "same") * 2.4; x = np.zeros(n)
        for i in range(n):
            x[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.9975
        t = np.arange(n) / SR
        _c[k] = (x + 0.5 * np.sin(2 * np.pi * midi(m) * t) * np.exp(-t * 3)) * np.minimum(1, t * 500) * np.minimum(1, (dur - t) * 30)
    return _c[k]


def vib(m, dur=1.4):
    """A vibraphone: a bar with a slow motor on it."""
    t = np.arange(int(dur * SR)) / SR; f = midi(m)
    x = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 7) + 0.1 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t * 18)
    return x * np.exp(-t * 2.1) * (1 - 0.32 * (0.5 + 0.5 * np.sin(2 * np.pi * 4.6 * t))) * np.minimum(1, t * 900) * np.minimum(1, (dur - t) * 20)


def hp(x, w=10): return x - np.convolve(x, np.ones(w) / w, "same")


def brush(dur, seed=0, up=True):
    """A brush on a snare: soft noise that swells."""
    g = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; x = hp(g.normal(0, 1, n), 14)
    e = (t / dur) ** 1.3 if up else np.exp(-t * 9)
    return x * e * np.minimum(1, (dur - t) * 60)


def ride(seed=0):
    g = np.random.default_rng(seed); n = int(0.42 * SR); t = np.arange(n) / SR; x = hp(g.normal(0, 1, n), 4) + 0.4 * np.sin(2 * np.pi * 5400 * t) * np.sin(2 * np.pi * 7300 * t)
    return x * np.exp(-t * 11)


def thud(f=62.0, dur=0.7, drop=2.2):
    t = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(f * (1 + drop * np.exp(-t * 34))) / SR) * np.exp(-t * 6.0) * np.minimum(1, t * 800)


def slap(dur=0.16, seed=0, f=340.0):
    """Wet clay on a hard surface."""
    g = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR; x = np.convolve(g.normal(0, 1, n), np.ones(18) / 18, "same") * 3.4
    return (x + 0.5 * np.sin(2 * np.pi * f * (1 - 0.5 * t / dur) * t)) * np.exp(-t * 26) * np.minimum(1, t * 3000)


def squelch(dur=0.42, f0=240.0, f1=70.0, seed=0):
    t = np.arange(int(dur * SR)) / SR; g = np.random.default_rng(seed)
    x = np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (t / dur) * (1 + 0.16 * np.sin(2 * np.pi * 27 * t))) / SR)
    return (x + 0.55 * np.convolve(g.normal(0, 1, len(t)), np.ones(40) / 40, "same") * 2.2) * np.exp(-t * 4.2 / dur) * np.minimum(1, t * 300) * np.minimum(1, (dur - t) * 60)


def press(dur=0.9):
    """The press: a low kick with iron in it."""
    t = np.arange(int(dur * SR)) / SR
    return thud(44, dur, 3.2) + 0.2 * np.sin(2 * np.pi * 187 * t) * np.sin(2 * np.pi * 311 * t) * np.exp(-t * 16)


CH = {"Dm": [38, 45, 50, 53, 57, 60, 62, 65, 69], "Gm": [43, 50, 55, 58, 62, 65, 67, 70, 74], "Bb": [46, 53, 58, 62, 65, 69, 70, 74, 77], "A7": [45, 52, 57, 61, 64, 67, 69, 73, 76]}
PROG = ["Dm", "Dm", "Gm", "Gm", "Bb", "Bb", "A7", "A7"]
def chord_at(b): return PROG[int(b // 2) % 8]


def walk(b0, b1, level=1.0):
    """A walking bass, one note a beat."""
    for b in np.arange(math.ceil(b0), b1, 1.0):
        c = CH[chord_at(b)]; nxt = CH[chord_at(b + 1)][0]; k = int(b) % 4
        m = [c[0], c[1], c[0] + 12 - 2 if k == 2 else c[2], nxt - 1 if nxt != c[0] else c[1] - 2][k]
        add(B(b), bass(m + 12), 0.58 * level, -0.08)


def kit(b0, b1, level=1.0, ride_on=True):
    """Brushes on two and four, a ride in swing."""
    for b in np.arange(math.ceil(b0), b1, 1.0):
        if int(b) % 2 == 1: add(B(b) - 0.09, brush(0.2, int(b)), 0.1 * level, 0.1); add(B(b), brush(0.14, int(b) + 99, False), 0.12 * level, 0.1)
        if ride_on:
            add(B(b), ride(int(b)), 0.042 * level, 0.35)
            if int(b) % 2 == 1: add(B(b + 0.66), ride(int(b) + 7), 0.03 * level, 0.35)


def vibes(b0, b1, level=1.0):
    """Sparse chords on the vibes, late and quiet."""
    for b in np.arange(math.ceil(b0 / 4) * 4, b1, 4.0):
        c = CH[chord_at(b)]
        for j, m in enumerate(c[4:8]): add(B(b + 0.5) + j * 0.012, vib(m + 12), 0.1 * level, -0.3 + j * 0.2)
        c2 = CH[chord_at(b + 2)]
        if b + 2.66 < b1:
            for j, m in enumerate(c2[5:8]): add(B(b + 2.66) + j * 0.012, vib(m + 12, 1.0), 0.075 * level, 0.3 - j * 0.2)


# ---- 1. the mismatch: one slap per picture and a wrong note on each. No band
WRONG = [75, 66, 83, 61, 79, 70]
for i, b in enumerate(TB["drops"]):
    add(B(b), slap(0.18, i), 0.5, -0.6 + i * 0.24); add(B(b), thud(70 + i * 7, 0.26, 1.4), 0.4); add(B(b), vib(WRONG[i], 0.8), 0.14, -0.6 + i * 0.24)
# ---- 2. the lump: squashed, then kneaded on the beat
add(B(TB["morph"]), press(0.8), 0.8); add(B(TB["morph"]), squelch(0.55, 200, 60, 5), 0.42)
for b in np.arange(TB["morph"] + 2, TB["plates"][0], 2.0): add(B(b), squelch(0.34, 160, 80, int(b)), 0.28); add(B(b), thud(58, 0.3, 1.5), 0.32)
walk(TB["morph"] + 1.6, TB["plates"][0] - 0.1, 0.72); kit(TB["morph"] + 1.6, TB["plates"][0], 0.4, ride_on=False)
# ---- 3. the press: each plate locks with a hit, and the band builds on it
for b in [TB["rod"]]: add(B(b), squelch(0.9, 90, 200, 12), 0.14)
for i, b in enumerate(TB["plates"]):
    add(B(b), thud(52, 0.6, 2.4), 0.7); add(B(b), slap(0.14, 20 + i, 220), 0.3, -0.5 if i % 2 == 0 else 0.5)
    for j, m in enumerate(CH["Dm"][4 + i:6 + i]): add(B(b) + j * 0.01, vib(m + 12, 1.2), 0.17, -0.4 + i * 0.25)
walk(TB["plates"][0], TB["pressStart"] - 0.2); kit(TB["plates"][1], TB["pressStart"], 0.72); vibes(TB["plates"][3] + 0.5, TB["pressStart"], 0.8)
# ---- the one slow press
n = int(B(TB["pressHit"] - TB["pressStart"]) * SR); t = np.arange(n) / SR
add(B(TB["pressStart"]), np.sin(2 * np.pi * np.cumsum(48 + 60 * (t / t[-1]) ** 3) / SR) * (t / t[-1]) ** 2, 0.22); add(B(TB["pressStart"]), brush(B(TB["pressHit"] - TB["pressStart"]), 30), 0.13)
add(B(TB["pressHit"]), press(1.2), 1.2); add(B(TB["pressHit"]), squelch(0.7, 170, 44, 31), 0.5)
for j, m in enumerate(CH["Dm"][3:8]): add(B(TB["pressHit"]) + j * 0.012, vib(m + 12, 1.7), 0.14)
# ---- 4. the first set: six pictures slide out, a thumb on each
for i in range(6): add(B(TB["pressHit"] + 0.5 + i * 0.06), slap(0.1, 40 + i, 420), 0.16, -0.5 + i * 0.2)
walk(TB["pressHit"] + 1, TB["fly"], 0.8); kit(TB["pressHit"] + 1, TB["fly"], 0.55)
for i in range(6):
    b = TB["seals"] + i * 0.42; add(B(b), slap(0.09, 50 + i, 520), 0.26, -0.5 + i * 0.2); add(B(b), vib([69, 72, 74, 77, 81, 84][i], 0.9), 0.17, -0.5 + i * 0.2)
# ---- 5. the run: the press is the kick, and each picture is a slap
for i in range(6): add(B(TB["fly"] + i * 0.08 + 0.72), slap(0.14, 60 + i), 0.25, -0.4 + i * 0.16)
walk(TB["fly"], TB["slams"][-1] + 0.8); kit(TB["fly"], TB["slams"][-1] + 0.8, 1.0); vibes(TB["fly"], TB["slams"][-1], 0.9)
for j, b in enumerate(TB["slams"]):
    add(B(b), press(0.75), 0.82 + j * 0.03); add(B(b), squelch(0.2, 200, 90, 70 + j), 0.16)
    for i in range(TB["bursts"][j]): add(B(b + 0.76 + i * 0.03), slap(0.1, 90 + j * 10 + i, 360 + (i * 37) % 200), 0.14, (-0.7 + 0.35 * i) % 1.4 - 0.7)
# the whole wall: a held chord
add(B(TB["retract"] + 0.3), press(1.0), 0.76)
for j, m in enumerate(CH["Dm"][2:9]): add(B(TB["retract"] + 0.3) + j * 0.02, vib(m + 12, 2.3), 0.15, -0.5 + j * 0.16)
for j, m in enumerate((50, 57)): add(B(TB["retract"] + 0.3), bass(m, 1.4), 0.46)
walk(TB["retract"] + 1.5, TB["stop"] - 0.1, 0.8); kit(TB["retract"] + 1.5, TB["stop"] - 0.1, 0.8)
# ---- 6. silence, one rising note, then the stamp, then the band
n = int(B(0.6) * SR); t = np.arange(n) / SR; add(B(TB["stamp"] - 0.6), np.sin(2 * np.pi * np.cumsum(70 + 240 * (t / t[-1]) ** 3) / SR) * (t / t[-1]) ** 2, 0.26); add(B(TB["stamp"] - 0.6), brush(B(0.6), 80), 0.2)
add(B(TB["stamp"]), press(1.4), 1.3); add(B(TB["stamp"]), squelch(0.8, 240, 44, 81), 0.7); add(B(TB["stamp"] + 0.05), slap(0.3, 82), 0.5)
add(B(TB["replace"] + 0.62), slap(0.14, 83), 0.34); add(B(TB["replace"] + 0.62), vib(74, 1.1), 0.2)
walk(TB["replace"], TB["moves"], 0.92); kit(TB["replace"], TB["moves"], 0.82); vibes(TB["replace"] - 1, TB["moves"], 0.8)
# ---- 7. it moves: a little tune on the vibes over the band, and one bar for each word
walk(TB["moves"], TB["yours"], 1.0); kit(TB["moves"], TB["yours"], 0.95); vibes(TB["moves"], TB["yours"], 0.7)
for j, m in enumerate((74, 77, 81, 84, 81, 77, 74, 72, 74, 81, 86, 89)): add(B(TB["moves"] + 0.75 + j * 0.33), vib(m, 0.8), 0.13, -0.45 + (j % 4) * 0.3)
# ---- 8. yours: the press lands, the slide, the last chord
add(B(TB["yours"] + 0.6), press(0.9), 0.86); walk(TB["yours"] + 1, TB["logo"] - 0.6, 0.92); kit(TB["yours"] + 1, TB["logo"] - 0.6, 0.86); vibes(TB["yours"], TB["logo"] - 1, 0.74)
add(B(TB["slide"]), brush(B(TB["logo"] - TB["slide"]), 100), 0.13)
add(B(TB["logo"]), press(1.2), 0.9); add(B(TB["logo"]), bass(50, 2.2), 0.7)
for j, m in enumerate((62, 65, 69, 72, 76, 81)): add(B(TB["logo"]) + j * 0.03, vib(m + 12, 2.6), 0.15, -0.4 + j * 0.16)

# a small dark room
ir = np.zeros(int(0.42 * SR))
for ms, g in ((17, 0.28), (29, 0.22), (47, 0.18), (71, 0.12), (107, 0.09), (149, 0.06), (211, 0.04), (307, 0.02)): ir[int(ms * SR / 1000)] = g
for ch in range(2): out[:, ch] += np.convolve(out[:, ch], np.roll(ir, ch * 31))[:N] * 0.55
# the stop: nothing at all until the rising note
i0, i1, i2 = int(B(TB["stop"]) * SR), int(B(TB["stop"] + 0.12) * SR), int(B(TB["stamp"] - 0.62) * SR)
env = np.ones(N); env[i0:i1] = np.linspace(1, 0.0, i1 - i0); env[i1:i2] = 0.0; env[i2:i2 + 400] = np.linspace(0, 1, 400); out *= env[:, None]
i3 = int(B(TB["beats"] - 0.8) * SR); out[i3:] *= np.linspace(1, 0, N - i3)[:, None] ** 2
out = np.tanh(out * 0.95)
pk = np.max(np.abs(out)); out = out / pk * 0.72
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print("score", round(DUR, 3), "peak", float(pk))
