"""Full Stop: the score, composed in code. Rubbery bounces, a slap bass and a tight funk kit in A minor, a new instrument for each style in the roll, and one hard stop. It reads the same timing table as the picture."""
import json, os, re, wave
import numpy as np
from scipy.signal import butter, sosfilt

here = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(here, "..", "assets", "table.js"), encoding="utf-8").read()
T = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
SR, BEAT, DUR = 48000, T["beat"], T["dur"]
N = int(SR * DUR); L, R = np.zeros(N), np.zeros(N)
rng = np.random.default_rng(51)
B = lambda b: int(round(b * BEAT * SR))
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
tt = lambda d: np.arange(int(SR * d)) / SR
def add(i, s, g=1.0, pan=0.0):
    i = max(0, i); e = min(N, i + len(s))
    if e <= i: return
    s = s[: e - i] * g; L[i:e] += s * np.cos((pan + 1) * np.pi / 4); R[i:e] += s * np.sin((pan + 1) * np.pi / 4)
def lp(x, f): return sosfilt(butter(2, f / (SR / 2), "low", output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f / (SR / 2), "high", output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a / (SR / 2), b / (SR / 2)], "band", output="sos"), x)
noise = lambda d: rng.standard_normal(int(SR * d))

# ---------- the kit
def kick(g=1.0):
    t = tt(0.32); ph = 2 * np.pi * (52 * t + (170 / 38) * (1 - np.exp(-38 * t)))
    return (np.sin(ph) * np.exp(-t * 11) + 0.25 * np.exp(-t * 400) * rng.standard_normal(len(t))) * g
def snare():
    t = tt(0.22); return bp(noise(0.22), 1400, 7000) * np.exp(-t * 20) + np.sin(2 * np.pi * 196 * t) * np.exp(-t * 26) * 0.6
def clap():
    t = tt(0.18); e = sum(np.exp(-np.maximum(t - d, 0) * 90) * (t >= d) for d in (0, 0.012, 0.024)); return bp(noise(0.18), 900, 4200) * e * 0.5
def hat(d=0.04): return hp(noise(d), 8500) * np.exp(-tt(d) * 95)
def rim(): t = tt(0.05); return (np.sin(2 * np.pi * 1700 * t) + np.sin(2 * np.pi * 2450 * t)) * np.exp(-t * 130) * 0.5
def tick(): t = tt(0.03); return bp(noise(0.03), 2400, 6000) * np.exp(-t * 200) + np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 240) * 0.4
# ---------- the dot: a rubber ball. Bigger landings go lower
def boing(size=1.0):
    d = 0.2 + 0.1 * size; t = tt(d); f0 = 780 - 420 * size; f1 = f0 * 0.42; f = f1 + (f0 - f1) * np.exp(-t * 26)
    ph = 2 * np.pi * np.cumsum(f) / SR; return (np.sin(ph) + 0.25 * np.sin(2 * ph)) * np.exp(-t * (20 - 6 * size)) * np.minimum(t / 0.001, 1)
def slap(m, d=0.2, drive=2.6):
    t = tt(d); f = hz(m); x = np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 26) * np.sin(2 * np.pi * f * 3 * t))
    return np.tanh(x * drive) * np.exp(-t * 3.5) * np.minimum(t / 0.002, 1) * np.minimum((d - t) / 0.012, 1) * 0.6
def stab(ms, d=0.26, cut=3200):
    t = tt(d); x = sum(2 * ((hz(m) * t) % 1) - 1 + 2 * ((hz(m) * 1.006 * t) % 1) - 1 for m in ms) / len(ms)
    return lp(x, cut) * np.exp(-t * 7) * np.minimum(t / 0.003, 1) * 0.5
def marimba(m, d=0.5): t = tt(d); f = hz(m); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 28)) * np.exp(-t * 8) * np.minimum(t / 0.001, 1)
def ep(ms, d=0.8): t = tt(d); return sum(np.sin(2 * np.pi * hz(m) * t + 0.9 * np.exp(-t * 7) * np.sin(2 * np.pi * hz(m) * 14 * t)) for m in ms) / len(ms) * np.exp(-t * 3.4) * np.minimum(t / 0.002, 1)

# ---------- a different instrument for each style in the roll
def inst(k, m):
    ch = [m, m + 3, m + 7]
    if k == 0: return ep(ch, 0.4)
    if k == 1: t = tt(0.2); return np.sign(np.sin(2 * np.pi * hz(m) * t)) * np.exp(-t * 16) * 0.3
    if k == 2: return stab(ch, 0.24, 2500)
    if k == 3: t = tt(0.18); return (((hz(m + 12) * t) % 1) < 0.25) * 0.6 * np.exp(-t * 14)
    if k == 4: t = tt(0.3); return np.sin(2 * np.pi * hz(m) * t) * np.sin(2 * np.pi * hz(m) * 1.41 * t) * np.exp(-t * 9) * 0.9
    if k == 5: t = tt(0.14); return np.sign(np.sin(2 * np.pi * hz(m + 24) * t)) * (np.sin(2 * np.pi * 37 * t) > 0) * np.exp(-t * 12) * 0.22
    if k == 6: return marimba(m + 12, 0.3) * 0.9
    if k == 7: t = tt(0.3); ph = 2 * np.pi * np.cumsum(hz(m) * (1 + 0.03 * np.sin(2 * np.pi * 7 * t))) / SR; return np.tanh(np.sin(ph) * 3) * np.exp(-t * 8) * 0.5
    if k == 8: return slap(m - 12, 0.2) * 1.0
    if k == 9: t = tt(0.26); return hp(noise(0.26), 500) * np.exp(-t * 16) * 0.2 + np.sin(2 * np.pi * hz(m) * t) * np.exp(-t * 12) * 0.5
    if k == 10: t = tt(0.3); return sum(np.sin(2 * np.pi * hz(x) * t) for x in ch) / 3 * np.exp(-t * 7)
    if k == 11: t = tt(0.16); return (((hz(m + 12) * t) % 1) * 2 - 1) * ((t * 60).astype(int) % 2) * np.exp(-t * 10) * 0.35
    if k == 12: t = tt(0.1); return np.sin(2 * np.pi * hz(m + 24) * t + 6 * np.sin(2 * np.pi * hz(m + 12) * 3.5 * t)) * np.exp(-t * 30) * 0.5
    if k == 13: return ep(ch, 0.3) * np.sin(2 * np.pi * 40 * tt(0.3))
    if k == 14: return stab([m + 12, m + 15, m + 19], 0.2, 6000)
    return marimba(m + 24, 0.2)

# ---------- landings and words
big = {1, 5, 7, 20, 30, 42, 65}
for b in T["lands"]:
    s = 1.0 if b in big else 0.55 if b < 8 or b >= 60 else 0.35
    if b >= 65.5: s = 0.18
    add(B(b), boing(s), 0.34 if b < 66 else 0.2, np.sin(b * 1.7) * 0.3)
for b in T["words"]:
    add(B(b), kick(), 0.8); add(B(b), rim(), 0.25, 0.2); add(B(b), hp(noise(0.12), 2500) * np.exp(-tt(0.12) * 30), 0.08)

# ---------- the groove: one bar of A minor funk, built up
BASS = {0: 33, 0.75: 33, 1.5: 36, 2: 33, 2.75: 31, 3.5: 28}
def groove(b0, b1, k=0.8, sn=0.34, ht=0.05, bs=0.32, chord=None, mar=None):
    b = b0
    while b < b1 - 1e-6:
        q = (b - b0) % 4
        for x, m in BASS.items():
            if bs and b0 + (b - q - b0) + x + 0 >= b0 and b - q + x < b1 and abs(q - int(q)) < 1e-9 and q == int(q) and x // 1 == q: add(B(b - q + x), slap(m, 0.2), bs)
        if k and (q in (0, 2) or q == 2.5 - 0): add(B(b), kick(), k)
        if k and q == 0: add(B(b + 2.5 - 0), kick(), k * 0.7)
        if sn and q in (1, 3): add(B(b), snare(), sn); add(B(b), clap(), sn * 0.7)
        if ht:
            for s_, g_ in ((0, 1), (0.5, 0.7), (0.25, 0.4), (0.75, 0.45)):
                add(B(b + s_ + (0.04 if s_ in (0.25, 0.75) else 0)), hat(), ht * g_, 0.25 * (-1) ** int(s_ * 4))
        if chord and q in (0, 1.5 - 0.5, 2.0, 3): add(B(b + 0.5), stab(chord, 0.2), 0.11, 0.2 * (-1) ** int(b))
        if mar: add(B(b), marimba(mar[int(b - b0) % len(mar)]), 0.13, np.sin(b) * 0.4); add(B(b + 0.5), marimba(mar[int(b - b0 + 2) % len(mar)] + 12), 0.08, -np.sin(b) * 0.4)
        b += 1
AM = [57, 60, 64]; DM = [62, 65, 69]; FM = [53, 57, 60]; EM = [52, 56, 59]
# A: the dot alone. B, C: a kit arrives
for b in [4.5, 5.5, 6.5, 7.5]: add(B(b), rim(), 0.25)
groove(4, 8, 0.55, 0.2, 0.03, 0.22)
# D: every doubling doubles the hats and lifts the stab
for i, b0 in enumerate(T["doubles"]):
    steps = 2 ** (i + 1)
    for s in range(steps):
        add(B(b0 + s / steps), hat(0.03), 0.04 + 0.015 * i, 0.5 * np.sin(s * 2.1))
        if i >= 1: add(B(b0 + s / steps), boing(0.25), 0.05 + 0.012 * i, 0.7 * np.sin(s * 2.4 + i))
    add(B(b0), kick(), 0.9); add(B(b0), stab([57 + i * 2, 60 + i * 2, 64 + i * 2], 0.3), 0.22)
r = hp(noise(0.3), 1200) * np.linspace(0, 1, int(SR * 0.3)) ** 2; add(B(13.45), r, 0.14)
add(B(14), kick(), 1.0); add(B(14), slap(21, 0.8), 0.45)
# E: plain English, warm
groove(14, 20, 0.45, 0.2, 0.025, 0.24)
for b, ch in [(14.5, AM), (16.5, FM), (17.5, DM), (18.5, EM)]: add(B(b), ep(ch, 1.0), 0.14)
for x, m in zip((14.5, 15, 15.5, 16, 16.5, 16.59, 16.68, 16.77, 16.86, 16.95, 17.5), (69, 72, 76, 69, 72, 74, 76, 77, 79, 81, 84)): add(B(x), marimba(m), 0.15, 0.1)
# F: the map, a node, a note
groove(20, 28, 0.7, 0.3, 0.04, 0.3, chord=AM)
for b, m in zip([20.5, 22, 23.5, 25, 26.5, 28], [69, 72, 76, 74, 77, 81]): add(B(b), marimba(m, 0.9), 0.24); add(B(b), kick(), 0.7)
add(B(28.3), hp(noise(1.1), 1500) * np.linspace(0, 1, int(SR * 1.1)) ** 2, 0.12)
groove(28, 30, 0.8, 0.34, 0.05, 0.3, chord=DM)
# G: code, dry and tight
groove(30, 32, 0.9, 0.38, 0.06, 0.36)
# H: the roll. Each style has its own instrument, over the same kit
groove(32, 40, 0.85, 0.32, 0.05, 0.3)
notes = [69, 72, 76, 74, 77, 72, 76, 81, 69, 72, 74, 76, 77, 79, 81, 84, 81, 84, 86, 88]
for i, b in enumerate(T["styles"]): add(B(b), inst([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,2,5,4,7][i], notes[i]), 0.26 if i < 12 else 0.2, 0.25 * np.sin(i * 1.9))
for i in range(32): add(B(40 + i / 16), hat(0.03), 0.05 + 0.002 * i);
for i in range(16): add(B(40 + i / 8), snare(), 0.06 + 0.012 * i)
add(B(40), hp(noise(1.07), 1000) * np.linspace(0, 1, int(SR * 1.07)) ** 2, 0.2)
# I: nothing. A landing and two ticks
add(B(43), tick(), 0.32); add(B(43.5), tick(), 0.32)
# J: the schedule. Everything, four on the floor
def four(b0, b1, k=1.0):
    b = b0
    while b < b1 - 1e-6: add(B(b), kick(), k); b += 1
four(44, 56)
groove(44, 56, 0, 0.42, 0.075, 0.42, chord=AM)
add(B(44), hp(noise(2.0), 500) * np.exp(-tt(2.0) * 2.6), 0.22); add(B(44), slap(21, 1.2, 3.2), 0.6); add(B(44), stab([45, 57, 60, 64], 0.8, 5000), 0.34)
for i in range(96): add(B(44 + i / 8), tick(), 0.05 + 0.0006 * i, np.sin(i * np.pi / 4) * 0.6)
for b, ch in zip(T["times"], [[57, 60, 64], [65, 69, 72], [62, 65, 69], [64, 68, 71]]): add(B(b), stab(ch, 0.5, 5200), 0.3); add(B(b), slap(ch[0] - 24, 0.5), 0.3)
for i in range(16): add(B(48 + i * 0.5), marimba([81, 84, 88, 86][i % 4], 0.3), 0.08, np.sin(i) * 0.5)
add(B(55), hp(noise(0.55), 900) * np.linspace(0, 1, int(SR * 0.55)) ** 2, 0.2)
# K: handing it over
groove(56, 62, 0.85, 0.36, 0.05, 0.36, chord=None)
for b, ch in zip([56, 58, 60], [AM, FM, DM]): add(B(b), stab(ch, 0.6, 4500), 0.26)
for i in range(13): add(B(56.26 + i * 0.13), marimba(69 + i, 0.14), 0.09, 0.4)
for i in range(10): add(B(58 + i * 0.04), hp(noise(0.05), 3000) * np.exp(-tt(0.05) * 60), 0.05, (-1) ** i * 0.6)
for i in range(24): add(B(60 + i * 0.06), tick(), 0.1, np.sin(i) * 0.6)
# L: five letters, five slams, a long way down, one hit, and it stops
for b, m in zip(T["letters"], [33, 33, 36, 40, 45]): add(B(b), kick(), 1.1); add(B(b), slap(m, 0.42, 3.2), 0.6); add(B(b), stab([m + 24, m + 27, m + 31], 0.3, 5000), 0.3)
d = (B(65) - B(64)) / SR; t = np.arange(int(d * SR)) / SR; f = 1400 * np.exp(-t * 2.4) + 120; ph = 2 * np.pi * np.cumsum(f) / SR; add(B(64), np.sin(ph) * np.linspace(0.05, 0.8, len(t)), 0.16)
add(B(65), kick(), 1.3); add(B(65), slap(21, 0.9, 3.4), 0.6); add(B(65), stab([45, 57, 60, 64, 69], 0.5, 6000), 0.34); add(B(65), hp(noise(0.5), 700) * np.exp(-tt(0.5) * 8), 0.2)

# one small room
ir = np.zeros(int(SR * 0.9)); idx = rng.integers(200, len(ir), 1500); ir[idx] = rng.standard_normal(1500) * np.exp(-idx / SR * 7); ir = hp(ir, 300)
wl = np.fft.irfft(np.fft.rfft(L, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]; wr = np.fft.irfft(np.fft.rfft(R, N + len(ir)) * np.fft.rfft(ir[::-1], N + len(ir)))[:N]
L += wl * 0.045; R += wr * 0.045
# master first, so the silences below are real silences
out = np.stack([L, R], 1); pk = np.abs(out).max(); out = np.tanh(out / pk * 3.2) / np.tanh(3.2) * 0.84
def gate(a, b, fade=0.012):
    i, j = B(a), B(b); f = int(SR * fade); env = np.zeros(j - i); env[:f] = np.linspace(1, 0, f); out[i:j] *= env[:, None]
gate(42.75, 43); gate(43.25, 43.5); gate(43.75, 44)        # the hush around the ticks
gate(T["stop"], T["card"])                                  # it stops
# the end card: one small landing and a warm chord, placed after the stop
c = np.zeros(N); i = B(T["card"]); s = ep([45, 57, 64, 69], 3.2) * 0.3; c[i:i + len(s)] = s[: max(0, N - i)];
s2 = boing(0.2) * 0.14; c[i:i + len(s2)] += s2
out[:, 0] += c; out[:, 1] += c
fade = np.ones(N); fade[B(74.3):] = np.linspace(1, 0, N - B(74.3)); out *= fade[:, None]
out = np.clip(out, -0.89, 0.89)
path = os.path.join(here, "..", "assets", "bgm", "score.wav")
os.makedirs(os.path.dirname(path), exist_ok=True)
with wave.open(path, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
print("score", DUR, "peak", pk)
