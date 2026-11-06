"""The score for Main Street, composed in code at 120 bpm in C major: bright and played by hand. Each of the 500 businesses plays one
marimba note at the moment it's found, picked from the scale by how far it is from the plaza, so the search is the tune. A pizzicato bass,
hand claps and a glockenspiel motif, one held breath, a sub drop as the town falls and a sparse night, then the morning.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR); rng = np.random.default_rng(44)
B = lambda x: x * BEAT
out = np.zeros((N, 2))
DROP, FLY, FLIP, MAIL, NEV, CLOSE, LOGO = 25.5, 31, 37, 39, 46, 53, 57


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_mem = {}
def marimba(m, dec=7.0, dur=0.55):
    k = (m, dec, dur)
    if k in _mem: return _mem[k]
    f = midi(m); t = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * dec) + 0.5 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * dec * 3.4) + 0.18 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * dec * 7)
    _mem[k] = x * np.minimum(1, t / 0.0015); return _mem[k]


def glock(m, dur=1.4):
    f = midi(m); t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.32 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 7) + 0.14 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)) * np.minimum(1, t / 0.001)


def pizz(m, dur=0.42):
    f = midi(m); t = np.arange(int(dur * SR)) / SR
    return np.tanh(1.4 * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 14))) * np.exp(-t * 6.5) * np.minimum(1, t / 0.003)


def clap(g=1.0):
    n = int(0.16 * SR); t = np.arange(n) / SR; x = rng.normal(0, 1, n); x = np.diff(np.r_[0, x])
    e = np.exp(-t * 34) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 90) * (t > 0.012) + 0.6 * np.exp(-np.maximum(0, t - 0.024) * 90) * (t > 0.024)
    return x * e * 0.5 * g


def kick(g=1.0, f0=52):
    n = int(0.3 * SR); t = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(f0 + 90 * np.exp(-t * 40)) / SR
    return np.sin(ph) * np.exp(-t * 11) * g


SCALE = [0, 2, 4, 7, 9]  # C major pentatonic: 500 notes can't clash
def scale(i, base=72): o, k = divmod(i, 5); return base + 12 * o + SCALE[k]


# ---------------- the search is the tune: 500 notes, one per business
for h in TB["houses"]:
    d = math.hypot(h["x"] - TB["cx"], h["z"] - TB["cz"]); note = scale(int((d / 340) * 13) % 13 + int(h["f"] * 2) % 3)
    add(B(h["f"]), marimba(note), 0.075, (h["x"] / TB["sw"]) * 1.4 - 0.7)
# and once again for a fresh search
for f in TB["fresh"]:
    add(B(f[2]), marimba(scale(int(f[0] / 40) % 12), 9, 0.4), 0.09, (f[0] / TB["sw"]) * 1.4 - 0.7)
# the first notes on their own
for bt, m in ((0, 72), (1, 76), (2, 79), (3, 84), (3.5, 83)): add(B(bt), marimba(m, 3.4, 1.2), 0.55)
# ---------------- bass and claps
BASS = {0: [36, 43], 1: [41, 48], 2: [43, 50], 3: [38, 45]}
for bar in range(1, 7):
    s = bar * 4; a, b = BASS[(bar - 1) % 4]
    for off, m in ((0, a), (1.5, b), (2, a), (3, b), (3.5, a)):
        if s + off < 25: add(B(s + off), pizz(m), 0.6)
for bt in np.arange(4, 25, 1): add(B(bt), kick(0.5 + 0.2 * (bt >= 14)))
for bt in np.arange(5, 25, 2): add(B(bt), clap(0.6 + 0.3 * (bt >= 14)))
for bt in np.arange(14.5, 25, 1): add(B(bt), clap(0.16), 1, 0.3)
# ---------------- a motif on the glockenspiel, for the words
for a, ms in ((14, (84, 88, 91, 96)), (17.5, (86, 91, 93, 98))):
    for k, m in enumerate(ms): add(B(a + k * 0.25), glock(m), 0.55, -0.3 + k * 0.2)
# a rolling marimba for the scores, up the scale
for k, bt in enumerate(np.arange(21, 25, 0.125)): add(B(bt), marimba(scale(int(k * 0.72) % 16, 67), 12, 0.25), 0.2 + k * 0.006, 0.6 * math.sin(k * 0.7))
# ---------------- one held breath, then the town falls
i, j = int(B(25) * SR), int(B(25.5) * SR); w = int(0.01 * SR); fade = np.ones(N); fade[i:j] = 0; fade[i:i + w] = np.linspace(1, 0, w); out *= fade[:, None]
n = int(3.2 * SR); t = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(28 + 120 * np.exp(-t * 7)) / SR; add(B(DROP), np.tanh(2.8 * np.sin(ph) * np.exp(-t * 1.4)), 0.95)
nz = rng.normal(0, 1, int(1.8 * SR)); nz = np.convolve(nz, np.ones(14) / 14, "same"); add(B(DROP), nz * np.exp(-np.arange(len(nz)) / SR * 3) * 0.75, 0.95)
# rubble: every filtered business lands with a small knock, in the low strings' range
for h in TB["houses"]:
    if h["s"] < 60 and h["gone"] < 28:
        add(B(h["gone"] + 0.4), marimba(36 + (h["c"] * 5) % 13, 22, 0.14), 0.09, (h["x"] / TB["sw"]) * 1.2 - 0.6)
# ---------------- the night: thirty windows, each a soft note
for k, i_ in enumerate(TB["surv"]):
    add(B(27.75 + k * 0.1), glock(scale(k % 10, 79), 1.2), 0.1, (TB["houses"][i_]["x"] / TB["sw"]) * 1.4 - 0.7)
for bt, m in ((28.5, 36), (30, 43)): add(B(bt), pizz(m, 1.0), 0.8)
add(B(28.5), kick(1.0, 40))
# ---------------- morning: the queue, a walking bass
for bt, m in zip(np.arange(31, 37, 1), (48, 52, 55, 57, 55, 52)): add(B(bt), pizz(m - 12), 0.55); add(B(bt + 0.5), marimba(m + 24, 6, 0.5), 0.26, 0.2)
for bt, m in ((33, 79), (33.5, 84), (34, 88)): add(B(bt), glock(m), 0.24)
for bt in np.arange(32, 37, 2): add(B(bt), clap(0.34))
# ---------------- the flip
for bt, m in ((FLIP, 36), (37.5, 36), (37.75, 43), (38.25, 36), (38.75, 43)): add(B(bt), kick(1.0)); add(B(bt), pizz(m), 0.75); add(B(bt), clap(0.7))
for k, m in enumerate((96, 91, 88)): add(B(FLIP + k * 0.5), glock(m), 0.3)
# ---------------- the draft: typing, a click on approve, a thud on reject
for k in range(32): add(B(39.8 + k * 0.0625), marimba(96, 40, 0.06), 0.05, rng.uniform(-0.3, 0.3))
for bt, m in zip(np.arange(39, 46, 1), (41, 45, 48, 45, 43, 47, 50)): add(B(bt), pizz(m - 12), 0.5)
for m in (72, 76, 79, 84): add(B(42.625), marimba(m, 4, 1), 0.36)
add(B(44.05), kick(0.9, 34)); add(B(44.05), marimba(40, 12, 0.3), 0.5)
for bt, m in ((44.875, 36), (45.5, 43)): add(B(bt), kick(1.0)); add(B(bt), pizz(m), 0.7)
for k, m in enumerate((84, 88, 91)): add(B(44.875 + k * 0.25), glock(m), 0.26)
# ---------------- never twice: the groove returns
for bar, s in enumerate((46, 50)):
    a, b = BASS[(bar + 2) % 4]
    for off, m in ((0, a), (1.5, b), (2, a), (3, b), (3.5, a)): add(B(s + off), pizz(m), 0.6)
for bt in np.arange(46, 53, 1): add(B(bt), kick(0.68))
for bt in np.arange(47, 53, 2): add(B(bt), clap(0.75))
for k, m in enumerate((84, 88, 91, 96)): add(B(48.75 + k * 0.25), glock(m), 0.32)
# ---------------- evening, and the first notes again, then a chord for the logo
for k, h in enumerate(sorted(TB["houses"], key=lambda q: -math.hypot(q["x"] - TB["cx"], q["z"] - TB["cz"]))):
    if k % 3 == 0: add(B(53 + 3 * k / 500), marimba(scale((k // 18) % 12 + 2, 67), 12, 0.25), 0.06, (h["x"] / TB["sw"]) * 1.2 - 0.6)
for bt, m in ((56, 84), (56.25, 79), (56.5, 76), (56.75, 72)): add(B(bt), marimba(m, 4, 1.2), 0.42)
n = int(B(7) * SR); t = np.arange(n) / SR; chord = sum(g_ * marimba(m, 1.0, B(7)) for m, g_ in ((48, 0.9), (60, 0.8), (64, 0.6), (67, 0.6), (72, 0.6), (76, 0.5)))
add(B(LOGO), chord * np.minimum(1, (B(7) - t) / 0.4), 0.42)

# ---------------- a little room, then out
ir_n = int(0.5 * SR); ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 11) * 0.02
m = 1 << int(np.ceil(np.log2(N + ir_n)))
wet = np.stack([np.fft.irfft(np.fft.rfft(out[:, ch], m) * np.fft.rfft(ir, m), m)[:N] for ch in (0, 1)], 1)
out = out + wet * 0.8
out = out / np.abs(out).max() * 0.86; out = np.tanh(out * 1.3) / np.tanh(1.3) * 0.85
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("peak", round(float(np.abs(out).max()), 3), "dur", DUR)
