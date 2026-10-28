"""The one table for R23 Scrollwork: the clock of every scene, the beat grid (100 bpm, 0.6 s a beat), the impact
frames, the smear frames and the moments each site lands. The film reads assets/table.js, the score reads
bake/table.json. Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BEAT, DUR = 30, 0.6, 32.0

T = {
    "open": [0.0, 1.8],          # ink, a brush stroke, the rod drops
    "mark": [1.8, 8.4],          # the spiral winds onto the rod, spins in, strikes a pose
    "spin": [2.4, 6.0],
    "pose": 6.0,
    "scroll": [8.4, 16.8],       # the mark unrolls into a scroll that flies through the sky
    "thumb": [16.8, 24.0],       # the thumb grinds down the rod; the page scrolls with it
    "cabinet": [24.0, 27.6],     # manga panels, one site each
    "title": 27.6,
    "end": DUR,
}
# six featured plates, in the order of the Scrollwork page
PLATES = ["ai-joaoqueiros", "cairn", "snapline", "tembr", "visions", "four-sparrows"]
NAMES = ["JQ AI Systems", "Cairn", "Snapline", "Tembr", "Imagined Worlds", "Four Sparrows Mahjong"]
CABINET = ["klatea", "outreachiq", "grid-studio", "joaoqueiros", "atlas-studio", "thumbnail-studio", "perto"]
CABNAMES = ["Klatea", "OutreachIQ", "Grid Studio", "joaoqueiros.com", "Atlas Studio", "Thumbnail Studio", "PERTO."]

stamps = [round(9.6 + 1.2 * k, 3) for k in range(6)]          # a plate passes the camera on the scroll
swaps = [round(16.8 + 1.2 * k, 3) for k in range(6)]          # the thumb lands on the next site
panels = [round(24.0 + 0.3 * k, 3) for k in range(7)]         # a manga panel slams in

# impact frames: a hard cut to ink and paper for n frames
impacts = [{"t": 1.8, "n": 3}, {"t": T["pose"], "n": 3}, {"t": T["scroll"][0], "n": 2}]
impacts += [{"t": s, "n": 2} for s in swaps]
impacts += [{"t": T["cabinet"][0], "n": 2}, {"t": T["title"], "n": 3}]
impacts.sort(key=lambda d: d["t"])

# smear frames: one frame in three while the mark spins fastest, and the frame before every impact
f0, f1 = round(T["spin"][0] * FPS), round(T["pose"] * FPS)
smears = [f for f in range(f0 + 12, f1 - 6) if (f - f0) % 3 == 0]
smears += [round(d["t"] * FPS) - 1 for d in impacts if d["t"] > 2]
smears = sorted(set(smears))

table = {"fps": FPS, "beat": BEAT, "dur": DUR, "T": T, "plates": PLATES, "names": NAMES, "cabinet": CABINET, "cabnames": CABNAMES,
         "stamps": stamps, "swaps": swaps, "panels": panels, "impacts": impacts, "smears": smears}
open(os.path.join(ROOT, "assets", "table.js"), "w").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w"), indent=1)
print(len(impacts), "impacts,", len(smears), "smear frames")
