"""The score for R37 · Batch, composed in code at 96 bpm and timed to bake/table.json:
  a soft pad on A minor, F, C, G and a muted pluck pulse in eighths, the whole way through;
  the flipbook as a shutter clatter that rises into a pitch, and a tone as the slit freezes it;
  a rising pluck for each of the forty-six keywords; a low swell under the strip; a dry tick and a bell for each
  check; a filtered wash under the tunnel; two soft clicks for the portal's boxes; a resolving chord on the logo.
Writes assets/bgm/score.wav (not committed).
Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000
DUR = TB["dur"]
BEAT = TB["beat"]
N = int(SR * DUR)
rng = np.random.default_rng(37)
T = TB["T"]


def env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    return e * np.exp(-np.arange(n) / SR / d)


def lp(x, fc):
    """One-pole low pass, vectorised by blocks so it stays quick."""
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


def pluck(f, d=0.6, bright=1.0):
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (5 + 7 * m / bright)) for m, a in [(1, 1), (2, 0.45), (3, 0.22), (4, 0.1)])
    return s * env(n, 0.002, d)


def bell(f, d=2.2):
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (1.3 + 1.7 * m)) for m, a in [(1, 1), (2.76, 0.38), (5.4, 0.16), (8.9, 0.06)])
    return s * env(n, 0.003, 9)


def pad(freqs, d):
    n = int(SR * d); x = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            s += np.sin(2 * np.pi * f * (1 + det / 100) * x + rng.uniform(0, 6)) * 0.33
            s += 0.12 * np.sin(2 * np.pi * 2 * f * (1 + det / 100) * x)
    a = min(0.5, d / 3)
    e = np.minimum(1, np.minimum(x / a, (d - x) / a))
    return s * np.clip(e, 0, 1) / len(freqs)


def noise_burst(d, fc):
    n = int(SR * d); x = rng.standard_normal(n)
    return lp(x, fc) * env(n, 0.0005, d / 3)


def swell(d, fc=900):
    n = int(SR * d); x = rng.standard_normal(n)
    y = lp(x, fc) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y / (np.abs(y).max() + 1e-9)


out = np.zeros((N, 2), np.float32)

# the harmony: A minor, F, C, G, two bars each (8 beats), from the first downbeat to the logo
CH = [[57, 60, 64], [53, 57, 60], [48, 55, 60, 64], [55, 59, 62]]
BASS = [45, 41, 48, 43]
bar = 8 * BEAT
k = 0; at = 0.0
while at < T["mark"]:
    ch = CH[k % 4]
    add(out, at, pad([mtof(m) for m in ch], bar + 0.3), 0.07 * (0.6 if at < T["read"][0] else 1.0), pan=0)
    add(out, at, pad([mtof(BASS[k % 4])], bar + 0.2), 0.08)
    k += 1; at += bar
# the pulse: a muted pluck on every eighth, the chord's notes in turn, a little louder from the strip on
i = 0; at = BEAT * 1
while at < T["title"]:
    ch = CH[int(at / bar) % 4]
    g = 0.035 if at < T["dupes"][0] else 0.05
    if T["read"][0] - 0.05 < at < T["read"][0] + 0.6: g *= 0.5
    add(out, at, pluck(mtof(ch[i % len(ch)] + 12), 0.25, 0.6), g, pan=0.35 * np.sin(i * 0.9))
    i += 1; at += BEAT / 2
# a soft low pulse on the beat through the strip and the wall
at = T["dupes"][0]
while at < T["tunnel"][0]:
    n = int(0.25 * SR); x = np.arange(n) / SR
    add(out, at, np.sin(2 * np.pi * (52 + 30 * np.exp(-x * 30)) * x) * env(n, 0.002, 0.08), 0.18)
    at += BEAT

# I · the flipbook: a shutter clatter that speeds up into a pitch, then a tone as the slit freezes it
s0, s1 = TB["sweep"]
for j in range(TB["n"]):
    tj = s0 + (s1 - s0) * j / TB["n"]
    add(out, tj, noise_burst(0.018, 3500 + 30 * j), 0.05 + 0.0006 * j, pan=-0.6 + 1.2 * j / TB["n"])
add(out, s0, swell(s1 - s0, 1400), 0.05)
add(out, s1, bell(mtof(76), 2.4), 0.06)
add(out, s1, bell(mtof(81), 2.4), 0.04)

# II · the scan: a high, quiet sweep; a bell as each word lifts
add(out, TB["scan"][0], swell(TB["scan"][1] - TB["scan"][0], 2400), 0.03, pan=0.2)
for j, (w, x, y) in enumerate(TB["lift"]):
    ts = TB["scan"][0] + (y + 20) / (TB.get("H", 1080) + 60) * (TB["scan"][1] - TB["scan"][0])
    add(out, ts, bell(mtof([69, 72, 76, 79, 81, 84][j]), 1.6), 0.05, pan=(x - 960) / 1400)
add(out, TB["fly"][0], swell(TB["fly"][1] - TB["fly"][0], 1800), 0.04)

# III · forty-six keywords: a pluck each, climbing the A minor pentatonic
PENT = [0, 3, 5, 7, 10]
for j in range(40):
    ti = TB["pop"][0] + (TB["pop"][1] - TB["pop"][0]) * j / 40
    m = 69 + 12 * (j // 5 // 3) + PENT[j % 5] + 12 * ((j // 5) % 3 == 2)
    add(out, ti, pluck(mtof(57 + PENT[j % 5] + 12 * (j // 10)), 0.4), 0.05 + 0.0008 * j, pan=0.5 * np.sin(j * 1.3))
add(out, TB["cat"], bell(mtof(88), 1.4), 0.05)

# IV · the strip: a low swell; a soft tick as each concept lights
add(out, T["dupes"][0], swell(T["wall"][0] - T["dupes"][0], 420), 0.06)
for j in range(len(TB["groups"])):
    tk = TB["bands"][0] + (TB["bands"][1] - TB["bands"][0]) * j / len(TB["groups"])
    tick = np.sin(2 * np.pi * 1800 * np.arange(int(0.04 * SR)) / SR) * env(int(0.04 * SR), 0.001, 0.01)
    add(out, tk, tick, 0.12, pan=-0.8 + 1.6 * j / len(TB["groups"]))

# V · the checks: a dry tick and a bell each; the verdict
for j, tk in enumerate(TB["rules"]):
    tick = np.sin(2 * np.pi * 2400 * np.arange(int(0.05 * SR)) / SR) * env(int(0.05 * SR), 0.001, 0.012)
    add(out, tk, tick, 0.2)
    add(out, tk, bell(mtof(72 + [0, 2, 4, 7, 9, 12, 14][j]), 1.2), 0.045)
for m, d in [(69, 0), (76, 0.05), (81, 0.1)]:
    add(out, TB["verdict"] + d, bell(mtof(m), 2.0), 0.06)

# VI · one file, the tunnel, the portal's boxes
add(out, TB["collapse"][0], swell(TB["collapse"][1] - TB["collapse"][0], 2000), 0.05)
wash = swell(TB["gate"][1] - TB["gate"][0] + 0.4, 700)
sub = np.sin(2 * np.pi * 55 * np.arange(len(wash)) / SR) * np.sin(np.linspace(0, np.pi, len(wash)))
add(out, TB["gate"][0], wash * 0.09 + sub * 0.06)
for tk in TB["portal"][1:]:
    add(out, tk, noise_burst(0.012, 5000), 0.18)
    add(out, tk + 0.02, pluck(mtof(81), 0.4), 0.05)

# VII · the title and the logo: a resolving chord
add(out, T["title"], swell(T["mark"] - T["title"], 1200), 0.04)
for m, d in [(57, 0), (64, 0.03), (69, 0.06), (72, 0.09), (76, 0.12)]:
    add(out, T["mark"] + d, bell(mtof(m), 3.2), 0.07)
add(out, T["mark"], pad([mtof(m) for m in [45, 52, 57, 60, 64]], DUR - T["mark"]), 0.08)

# in from silence, out at the end
g = np.ones(N); fi = int(0.4 * SR); g[:fi] = np.linspace(0, 1, fi)
t = np.arange(N) / SR
g *= np.where(t > DUR - 1.6, np.clip((DUR - t) / 1.6, 0, 1), 1)
out *= g[:, None]
peak = np.abs(out).max()
out = out / max(peak, 1e-9) * 0.89
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("score:", round(DUR, 2), "s")
