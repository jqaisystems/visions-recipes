"""The one table for R22 Zoetrope: the film's clock, the strobe (which film frames it fires on), the machines' spin
(in slots per film frame) and its integral, the phase every machine turns by. The film reads assets/table.js and the
score reads bake/table.json, so every flash, lock and hoofbeat lands on the same frame."""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, DUR = 30, 32.0
frames = json.load(open(os.path.join(ROOT, "bake", "frames.json")))

T = {
    "lamp": [0.0, 0.6],          # a warm lamp comes up on a drum already spinning
    "stutter": [2.4, 4.6],       # the strobe stutters on: flash frames grow denser, the pictures drift
    "lock": 4.6,                 # one flash a frame: the drum stands still and the horse gallops
    "dive": [8.6, 9.6],          # the camera drops into the drum and through the far panel
    "video": [9.6, 12.4],        # inside the loop: the clip itself, full frame
    "cabinet": 12.4,             # back out: the cabinet of machines
    "drift": [20.4, 21.6],       # the strobe drifts out of phase: sharp, but the pictures slide
    "dark": [21.6, 24.0],        # the strobe stops: the machines smear under the lamp and slow
    "relock": 24.0,              # one flash and everything locks again
    "end": 26.0,                 # the last flash: the carousel and the title
    "dur": DUR,
}

def hash1(n):
    x = math.sin(n * 127.1 + 311.7) * 43758.5453
    return x - math.floor(x)

def smooth(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)

def omega(t):
    """Spin in slots per film frame. 1 is the lock: one slot per flash."""
    a, b = T["stutter"]
    if t < a: return 1.0
    if t < T["lock"]: return 1.0 + 0.32 * (1 - smooth((t - a) / (T["lock"] - a))) ** 2
    if t < T["drift"][0]: return 1.0
    if t < T["drift"][1]: return 1.0 + 0.22 * smooth((t - T["drift"][0]) / 0.8)
    if t < T["relock"]: return 1.22 - 0.9 * smooth((t - T["dark"][0]) / (T["relock"] - T["dark"][0] - 0.3))
    return 1.0

def flash(f):
    """Does the strobe fire on film frame f? (Locked: every frame.)"""
    t = f / FPS
    a, b = T["stutter"]
    if t < a: return False
    if t < T["lock"]:
        u = (t - a) / (b - a)
        return hash1(f) < 0.12 + 0.88 * u ** 1.6
    if T["video"][0] <= t < T["video"][1]: return False
    if T["dark"][0] <= t < T["relock"]: return False
    return True

# the phase: the integral of the spin, sampled 20 times a frame; snapped to whole slots at each lock so the
# drum stands still with its slots exactly where they were
STEP = 20
phase, p = [], 0.0
for i in range(int(DUR * FPS * STEP) + STEP + 1):
    t = i / (FPS * STEP)
    phase.append(round(p, 5))
    p += omega(t) / STEP
lockF = [round(T["lock"] * FPS), round(T["relock"] * FPS)]
for lf in lockF:  # shift everything from a lock on so the phase there is a whole number of slots
    i0 = lf * STEP
    d = round(phase[i0]) - phase[i0]
    phase = phase[:i0] + [round(v + d, 5) for v in phase[i0:]]

flashes = [f for f in range(int(DUR * FPS)) if flash(f)]
table = {"T": T, "fps": FPS, "step": STEP, "phase": phase, "flash": flashes, "frames": frames,
         "omega": [round(omega(f / FPS), 4) for f in range(int(DUR * FPS) + 1)]}
open(os.path.join(ROOT, "assets", "table.js"), "w").write("window.TABLE = " + json.dumps(table, separators=(",", ":")) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w"))
print("flash frames", len(flashes), "phase at end", phase[-1])
