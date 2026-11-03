"""The score for R38 · Twice, composed in code at 88 bpm and timed to bake/table.json:
  a felt piano and a soft pad on F, D minor, B flat, C, the whole way through;
  a page-turn rustle as the brief writes out of the slit; a quiet scan;
  a two-note motif for the client's question, played alone in rehearsal, then against its own echo when the frame
  splits into rehearsal and live; a soft swell as the slit sweeps it all live;
  room tone with two filtered murmurs, Them left and You right, shaped by the table's envelopes (never real speech);
  a click for each debrief line; a wash under the tunnel; a resolving chord on the lockup.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR); T = TB["T"]
rng = np.random.default_rng(38)


def env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    return e * np.exp(-np.arange(n) / SR / d)


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y


def add(out, at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * (1 - max(0, pan))
    out[i:i + len(sig), 1] += sig * gain * (1 + min(0, pan))


def mtof(m): return 440 * 2 ** ((m - 69) / 12)


def piano(f, d=1.6, vel=1.0):
    """A felt piano: soft attack, a few slightly stretched partials, the hammer muffled."""
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * (1 + 0.0004 * m * m) * x) * np.exp(-x * (1.6 + 1.9 * m)) for m, a in [(1, 1), (2, 0.38), (3, 0.14), (4, 0.06)])
    return s * env(n, 0.006, d * 0.7) * vel


def bell(f, d=2.0):
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (1.4 + 1.8 * m)) for m, a in [(1, 1), (2.76, 0.3), (5.4, 0.1)])
    return s * env(n, 0.003, 9)


def pad(freqs, d):
    n = int(SR * d); x = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.1, 0.0, 0.09):
            s += np.sin(2 * np.pi * f * (1 + det / 100) * x + rng.uniform(0, 6)) * 0.33
    a = min(0.6, d / 3); e = np.minimum(1, np.minimum(x / a, (d - x) / a))
    return s * np.clip(e, 0, 1) / len(freqs)


def noise(d, fc, a=0.002, dec=None):
    n = int(SR * d); x = lp(rng.standard_normal(n), fc)
    return x * env(n, a, dec or d / 3)


def swell(d, fc=900):
    n = int(SR * d); y = lp(rng.standard_normal(n), fc) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y / (np.abs(y).max() + 1e-9)


out = np.zeros((N, 2), np.float32)
CH = [[65, 69, 72], [62, 65, 69], [58, 62, 65], [60, 64, 67]]     # F, Dm, Bb, C
BASS = [41, 38, 46, 36]
bar = 4 * BEAT
k = 0; at = 0.0
while at < T["mark"]:
    ch = CH[(k // 2) % 4]
    if k % 2 == 0:
        add(out, at, pad([mtof(m - 12) for m in ch], 2 * bar + 0.3), 0.05)
        add(out, at, pad([mtof(BASS[(k // 2) % 4])], 2 * bar + 0.2), 0.07)
    # the piano: a broken chord in eighths, softer while the voices murmur
    for j, m in enumerate([ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]):
        tj = at + j * BEAT / 2
        if tj >= T["mark"]: break
        g = 0.05 if j % 2 == 0 else 0.032
        if T["sides"][0] <= tj < T["sides"][1]: g *= 0.6
        add(out, tj, piano(mtof(m), 1.4), g, pan=0.3 * np.sin(j * 0.8 + k))
    k += 1; at += bar

# I · the brief writes out: a page-turn rustle across the sweep
add(out, TB["sweep"][0], swell(TB["sweep"][1] - TB["sweep"][0], 3200), 0.035, pan=-0.3)
for j in range(9):
    add(out, TB["sweep"][0] + j * (TB["sweep"][1] - TB["sweep"][0]) / 9, noise(0.09, 4200, 0.01, 0.04), 0.06, pan=-0.6 + 0.15 * j)

# II · the scan, then the question held: the motif alone
add(out, TB["scanIn"][0], swell(TB["scanIn"][1] - TB["scanIn"][0], 2000), 0.03)
MOTIF = [(77, 0.0), (74, 0.5)]
for m, d in MOTIF:
    add(out, TB["hold"] + d * BEAT, bell(mtof(m), 2.4), 0.07, pan=-0.2)

# III · twice: the motif against its own echo, both sides on the same beat
for m, d in MOTIF:
    add(out, TB["both"] + d * BEAT, bell(mtof(m), 2.6), 0.07, pan=-0.6)
    add(out, TB["both"] + d * BEAT + 0.012, bell(mtof(m + 12), 2.6), 0.045, pan=0.6)
add(out, TB["split"][0], noise(0.25, 2500, 0.004, 0.08), 0.12)
add(out, TB["sweep2"][0], swell(TB["sweep2"][1] - TB["sweep2"][0] + 0.4, 1600), 0.06)
add(out, TB["help"], bell(mtof(84), 1.8), 0.05, pan=0.4)

# IV · two sides: room tone and two filtered murmurs shaped by the table's envelopes
s0, s1 = T["sides"]
n = int((s1 - s0 + 0.5) * SR)
room = lp(rng.standard_normal(n), 500) * 0.25
add(out, s0 - 0.2, room * np.sin(np.linspace(0, np.pi, n)) ** 0.5, 0.06)
ENV = np.array(TB["env"])
for side, pan, fc, f0 in [(0, -0.55, 900, 180), (1, 0.55, 1300, 230)]:
    tt = np.arange(n) / SR + s0
    e = np.interp(tt, np.arange(len(ENV)) / 30, ENV[:, side])
    syl = 0.5 + 0.5 * np.sin(2 * np.pi * 4.3 * tt + side) * np.sin(2 * np.pi * 1.7 * tt)
    voice = lp(rng.standard_normal(n), fc) * 0.6 + 0.4 * np.sin(2 * np.pi * (f0 + 20 * np.sin(2 * np.pi * 0.9 * tt)) * tt)
    add(out, s0, voice * e * syl, 0.07, pan=pan)
add(out, TB["trans"], bell(mtof(81), 1.4), 0.045, pan=0.3)

# V · the call as one image, folded and unfolded; a click for each debrief line
add(out, TB["strip"][0], swell(TB["strip"][1] - TB["strip"][0], 2400), 0.04)
add(out, TB["fold"][0], swell(TB["fold"][1] - TB["fold"][0] + 0.2, 700), 0.06)
add(out, TB["unfold"][0], swell(TB["unfold"][1] - TB["unfold"][0] + 0.2, 1400), 0.05)
for tk, _, _ in TB["dbItems"]:
    add(out, tk, noise(0.012, 6000, 0.0005, 0.006), 0.2)
    add(out, tk + 0.01, piano(mtof(84), 0.8), 0.045)
add(out, TB["email"], noise(0.2, 3000, 0.01, 0.06), 0.06)

# VI · the tunnel back to the next prep
wash = swell(TB["gate"][1] - TB["gate"][0] + 0.4, 800)
sub = np.sin(2 * np.pi * 43.65 * np.arange(len(wash)) / SR) * np.sin(np.linspace(0, np.pi, len(wash)))
add(out, TB["gate"][0], wash * 0.08 + sub * 0.05)

# VII · the title and the lockup: the motif resolved, a chord
add(out, T["title"], swell(T["mark"] - T["title"], 1200), 0.03)
for m, d in [(77, 0), (74, 0.5), (72, 1.0)]:
    add(out, TB["titleType"][0] + d * BEAT, bell(mtof(m), 2.2), 0.05)
for m, d in [(53, 0), (60, 0.03), (65, 0.06), (69, 0.09), (72, 0.12)]:
    add(out, T["mark"] + d, piano(mtof(m), 3.0), 0.09)
add(out, T["mark"], pad([mtof(m) for m in [41, 48, 53, 57, 60]], DUR - T["mark"]), 0.07)

g = np.ones(N); fi = int(0.3 * SR); g[:fi] = np.linspace(0, 1, fi)
t = np.arange(N) / SR
g *= np.where(t > DUR - 1.6, np.clip((DUR - t) / 1.6, 0, 1), 1)
out *= g[:, None]
out = out / max(np.abs(out).max(), 1e-9) * 0.89
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("score:", round(DUR, 2), "s")
