"""The one table for R31 · True North: every beat, the stills and their order, the globe's map of tiles, the opening
prompt (quoted from the Atlas library as written) and the title, on a 116 bpm grid. It also bakes the stills from
public/images into assets/img (not committed). The film reads assets/table.js, the score reads bake/table.json.
Usage: python bake/table.py"""
import json, os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.normpath(os.path.join(ROOT, "..", ".."))
FPS, BPM = 30, 116
BEAT = 60 / BPM                                   # 0.5172 s
b = lambda x: round(x * BEAT, 4)
DUR = round(b(64), 3)

T = {
    "open": [0.0, b(6)],          # the needle spins in its ring; a real Atlas prompt types out
    "globe": [b(6), b(20)],       # a glass globe of stills; it whips round and brakes, the needle points
    "droste": [b(20), b(36)],     # an endless zoom, each still inside the compass ring of the last
    "tunnel": [b(36), b(46)],     # a fly-through of a tunnel of stills
    "motion": [b(46), b(54)],     # three rings come alive as --motion clips
    "title": b(54),
    "end": DUR,
}

# ---------------- the stills: the site's own files, titles and prompts (content/portfolio.json)
PICK = ["kaleidoscopic-journey-through-wormhole", "color-photo-pristine-white-background-focal",
        "beautiful-colorful-fantasy-beta-fish-black", "aurora-over-crystal-lake-borealis", "mystical-lantern-festival",
        "voyage-through-time-space-grand-ancient", "path-discovery-cutting-through", "path-success-business-photo",
        "fresh-raspberry-transparent-background", "colorful-mushroom-forest-filled", "sailing-among-giant-floating-flowers",
        "space-explorers-uncharted-nebulae", "radical-expressive-portrait-woman-her-face", "blue-car", "banner-mojito-photo",
        "yacht-close-up-ocean-sunset", "magical-train-journey-traveling", "colorful-background-smiling-solar-woman-leaflet",
        "colorful-zone-space-stars-planets", "whimsical-submarine-adventure"]
PF_PATH = os.path.join(SITE, "content", "portfolio.json")
if os.path.exists(PF_PATH):
    from PIL import Image
    BYID = {s["id"]: s for s in json.load(open(PF_PATH, encoding="utf-8"))["stills"]}
    STILLS = []
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    for k, sid in enumerate(PICK):
        s = BYID[sid]
        dst = os.path.join(ROOT, "assets", "img", f"s{k:02d}.jpg")
        if not os.path.exists(dst):
            Image.open(os.path.join(SITE, "public", s["src"].lstrip("/"))).convert("RGB").resize((1024, 683), Image.LANCZOS).save(dst, quality=90)
        STILLS.append({"id": sid, "title": s["title"], "prompt": s["prompt"], "src": f"assets/img/s{k:02d}.jpg"})
else:
    # Outside the site: keep the titles and prompts already in bake/table.json (edit them there) and read your own
    # images from assets/img/s00.jpg to s19.jpg (see assets/img/README.md).
    STILLS = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))["stills"]

# ---------------- I · open: a real prompt from the Atlas library (v6 Light Architecture · Backgrounds · Prompt 3)
PROMPT = ("night beach, bioluminescent tide washing in, each wave glowing electric blue-white as the plankton light, "
          "dark sky above, wet dark sand reflecting the glow, long exposure night photography --ar 16:9 --style raw")
PROMPT_META = "v6 Light Architecture · Backgrounds · Prompt 3"
typing = [b(0.5), b(4.5)]
openLine = b(2.5)

# ---------------- II · globe: 16 longitudes x 8 latitude bands (-60..60 degrees); a still on some tiles, glass on the rest
NLON, NLAT = 16, 8
h = lambda n: (math.sin(n * 12.9898 + 78.233) * 43758.5453) % 1.0
GMAP = []
for j in range(NLAT):
    for i in range(NLON):
        GMAP.append(int(h(i * 7 + j * 31) * len(STILLS)) if h(i * 3.1 + j * 17.7) < 0.62 else -1)
build = [b(6.5), b(9)]                             # the tiles arrive
pull = [b(6), b(9)]                                # the camera pulls back from the needle
DROSTE = [5, 1, 2, 3, 4, 0, 9, 6]                  # the zoom's order; it starts on the globe's last tile
brakes = []
for k, (lon, layer) in enumerate([(3, 10), (11, 13), (6, DROSTE[0])]):
    GMAP[4 * NLON + lon] = layer                   # the tile each brake lands on carries that still
    brakes.append({"t": b(10 + 3 * k), "lon": lon, "layer": layer})
dive = [b(17.5), b(20)]

# ---------------- III · droste: one still every two beats
drosteSteps = [b(20 + 2 * k) for k in range(len(DROSTE))]

# ---------------- IV · tunnel, V · --motion (the site's own clips, muted)
tunnelLines = [b(37), b(41)]
CLIPS = [{"id": "vibrant-kingfisher-bird-bursting-out-water", "title": "The Dive", "src": "assets/clips/the-dive.mp4", "from": 1.0},
         {"id": "close-up-human-eye-iris", "title": "Iris", "src": "assets/clips/iris.mp4", "from": 0.5},
         {"id": "dynamic-surfer-giant-abstract-wave", "title": "Painted Swell", "src": "assets/clips/painted-swell.mp4", "from": 1.0}]
rings = [b(46.5 + k * 0.5) for k in range(3)]
motionLine = b(48)

# ---------------- VI · title
gather = [b(54), b(56)]
mark = b(56)
line = b(58)

cuts = [T["globe"][0], dive[1], T["tunnel"][0], T["motion"][0], mark]
table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "stills": STILLS, "prompt": PROMPT, "promptMeta": PROMPT_META,
         "typing": typing, "openLine": openLine, "nlon": NLON, "nlat": NLAT, "gmap": GMAP, "build": build, "pull": pull,
         "brakes": brakes, "dive": dive, "droste": DROSTE, "drosteSteps": drosteSteps, "tunnelLines": tunnelLines,
         "clips": CLIPS, "rings": rings, "motionLine": motionLine, "gather": gather, "mark": mark, "line": line, "cuts": sorted(cuts)}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8", newline="\n").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8", newline="\n"), indent=1)
print(json.dumps(T), DUR)
