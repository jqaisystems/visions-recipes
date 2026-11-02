"""Media prep for R37 · Batch. Reads one folder of stills and the uploader's CSV for it (never writes to the source
folder) and writes into assets/img/ (not committed):
  s001.jpg ...   every still of the batch, in the CSV's order, 1280 wide, for the texture array
  hero.jpg       the first still at 1920 wide, for the moment it is read
  batch.json     the rows: filename, title, the 46 keywords, the category, and the concept groups
Usage: python bake/prep.py [folder] [csv]   (defaults: the demo batch from bake/demo.py; or pass your own)
The CSV needs the columns Filename, Title, Keywords (comma separated) and, optionally, Category."""
import csv, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
SRC_DIR = os.path.join(ROOT, "assets", "demo")          # made by bake/demo.py; pass your own folder and CSV instead
SRC_CSV = os.path.join(SRC_DIR, "batch.csv")
DIR = sys.argv[1] if len(sys.argv) > 1 else SRC_DIR
CSV = sys.argv[2] if len(sys.argv) > 2 else (SRC_CSV if DIR == SRC_DIR else os.path.join(DIR, "batch.csv"))
SW, SH = 1280, 720                                    # every still covers a 16:9 frame in the array


def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)


rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if re.fullmatch(r"s\d{3}\.jpg|hero\.jpg", f):
        os.remove(os.path.join(OUT, f))

cover = lambda w, h: f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h}"
for k, r in enumerate(rows):
    ff("-i", os.path.join(DIR, r["Filename"]), "-vf", cover(SW, SH), "-q:v", "3", os.path.join(OUT, f"s{k + 1:03d}.jpg"))
ff("-i", os.path.join(DIR, rows[0]["Filename"]), "-vf", cover(1920, 1080), "-q:v", "2", os.path.join(OUT, "hero.jpg"))

# the concepts: the variants of one idea share the prompt their filenames start with
key = lambda fn: re.sub(r"_[0-9a-f]{8}-[0-9a-f-]+_\d+\.\w+$", "", fn)
groups = []
for k, r in enumerate(rows):
    if groups and groups[-1]["key"] == key(r["Filename"]):
        groups[-1]["n"] += 1
    else:
        groups.append({"key": key(r["Filename"]), "start": k, "n": 1, "category": r.get("Category", "")})

out = {
    "rows": [{"file": r["Filename"], "title": r["Title"], "keywords": [t.strip() for t in r["Keywords"].split(",")],
              "category": r.get("Category", "")} for r in rows],
    "groups": [{"start": g["start"], "n": g["n"], "category": g["category"]} for g in groups],
    "csvName": os.path.basename(CSV),
}
json.dump(out, open(os.path.join(OUT, "batch.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len(rows)} stills in {len(groups)} concepts: {[g['n'] for g in groups]}")
