"""The one table for R37 · Batch: every beat on a 96 bpm grid, the batch's real rows (from the uploader's CSV, via
bake/prep.py), the concept groups, the checks re-run on the real file, and the title. It reads assets/img/batch.json
and writes assets/table.js for the film and bake/table.json for the score.
Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 96
BEAT = 60 / BPM                                   # 0.625 s
b = lambda x: round(x * BEAT, 4)
DUR = b(54)                                       # 33.75 s

T = {
    "open": [0.0, b(7)],           # the batch plays as a flipbook; a slit freezes it into one image
    "read": [b(7), b(15)],         # one still read: a scan line, and its words lift out of it
    "keys": [b(15), b(23)],        # forty-six keywords, in order, under the real title
    "dupes": [b(23), b(31)],       # the batch as one strip: variants melt, concepts cut hard
    "wall": [b(31), b(42)],        # the CSV as a wall of rows, and the checks
    "tunnel": [b(42), b(48)],      # one file; a tunnel of stills; the boxes a human ticks
    "title": b(48),                # type cut out of the batch
    "mark": b(51),                 # the JQ AI SYSTEMS logo
    "end": DUR,
}

BA = json.load(open(os.path.join(ROOT, "assets", "img", "batch.json"), encoding="utf-8"))
rows = BA["rows"]
BANNED = ["stock", "photo", "image", "picture", "download", "preview", "ai", "generated", "generative"]


# the uploader's own checks, re-run on the real file: the film shows what they return
def checks(rows):
    tags = [r["keywords"] for r in rows]
    res = [
        ["46 keywords", sum(len(t) == 46 for t in tags)],
        ["no repeats", sum(len(set(t)) == len(t) for t in tags)],
        ["lowercase", sum(all(k == k.lower() for k in t) for t in tags)],
        ["no banned terms", sum(not (set(t) & set(BANNED)) for t in tags)],
        ["title length", sum(0 < len(r["title"]) <= 200 for r in rows)],
        ["unique filenames", len(rows) if len({r["file"] for r in rows}) == len(rows) else 0],
    ]
    if any(r["category"] for r in rows):
        res.append(["category 1 to 21", sum(r["category"].isdigit() and 1 <= int(r["category"]) <= 21 for r in rows)])
    return res


CH = checks(rows)
errors = sum(len(rows) - n for _, n in CH)

# the six words the scan lifts out of the first still: its own first six keywords. Place each over what it names.
first = rows[0]
POS = [(420, 820), (1460, 150), (520, 205), (1100, 880), (1030, 470), (900, 300)]   # centres, in the 1920 x 1080 frame
LIFT = [(w, x, y) for w, (x, y) in zip(first["keywords"][:6], POS)]

TABLE = {
    "dur": DUR, "beat": round(BEAT, 6), "bpm": BPM, "T": T,
    "n": len(rows), "groups": BA["groups"], "csvName": BA["csvName"],
    "rows": [{"file": r["file"], "title": r["title"], "category": r["category"], "nk": len(r["keywords"])} for r in rows],
    "first": first, "lift": LIFT, "checks": CH, "errors": errors, "banned": BANNED,
    "lines": [
        [b(1), b(7), "One folder in,"],
        [b(8), b(15), "every image read,"],
        [b(16), b(23), "forty-six keywords, in order,"],
        [b(24), b(31), "near-duplicates found,"],
        [b(32), b(42), "validated first,"],
        [b(43), b(48), "then a human checks."],
    ],
    "sweep": [b(1), b(6.5)],            # I: the flipbook, and the slit that freezes it
    "scan": [b(8), b(13)],              # II: the scan line reads the first still
    "fly": [b(14.4), b(15.6)],          # the lifted words fly to their slots
    "typeTitle": [b(15), b(16.6)],      # III: the real title types on
    "pop": [b(16), b(20)],              # the other forty keywords, one by one
    "cat": b(20.5),                     # the category
    "melt": [b(23), b(31)],             # IV: the strip
    "bands": [b(24.5), b(29.5)],        # each concept lights up in turn
    "scroll": [b(31.5), b(41.5)],       # V: the wall runs past
    "rules": [b(33), b(34.3), b(35.6), b(36.9), b(38.2), b(39.5), b(40.6)],
    "verdict": b(41.2),
    "collapse": [b(42), b(43)],         # VI: the wall becomes one file
    "gate": [b(43.2), b(48)],           # the tunnel of stills
    "portal": [b(45), b(46), b(46.8)],  # the checklist, and its two boxes
    "titleType": [b(48), b(50)],
    "line": b(51.6),
    "name": "Adobe Stock Uploader",
    "claim": "Batch metadata, validated first.",
    "url": "ai.joaoqueiros.com/systems/adobe-stock-uploader",
}
TABLE["cuts"] = [T["read"][0], T["keys"][0], T["dupes"][0], T["wall"][0], T["tunnel"][0], T["title"], T["mark"]]

with open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8") as f:
    f.write("window.TABLE = " + json.dumps(TABLE, ensure_ascii=False) + ";\n")
json.dump(TABLE, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("table:", DUR, "s,", BPM, "bpm;", len(rows), "rows,", errors, "errors;", [c[0] + " " + str(c[1]) for c in CH])
