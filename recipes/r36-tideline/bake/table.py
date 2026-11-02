"""The one table for R36 · Tideline: every beat, the track's real energy, the strongest minute, the captions the
pipeline writes (quoted from its own caption builder) and the title, on a 72 bpm grid. It reads assets/img/energy.json
(from bake/prep.py) and writes assets/table.js for the film and bake/table.json for the score.
Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 72
BEAT = 60 / BPM                                   # 0.8333 s
b = lambda x: round(x * BEAT, 4)
DUR = 33.4

T = {
    "open": [0.0, b(5)],           # one whole video, laid out as a strip of time
    "minute": [b(5), b(11)],       # its real energy; a 60 s window locks onto the strongest minute
    "vertical": [b(11), b(17)],    # slits outside the centre crop drift back in time and fall
    "link": [b(17), b(22)],        # a datamosh hold, then the frame collapses into one link
    "phones": [b(22), b(31)],      # three phones, one wave at three moments, three captions
    "queue": [b(31), b(35)],       # spaced out in a queue, then a slit-scan tunnel of sea
    "title": b(35),                # type cut out of time
    "mark": b(37),                 # the Tidesstunes mark
    "end": DUR,
}

EN = json.load(open(os.path.join(ROOT, "assets", "img", "energy.json")))
mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"

TITLE = "Oceansong - Piano Waves for Inner Peace"
DESC = "Dive into a serene auditory journey where gentle piano melodies harmonize with the soothing sound of ocean waves."
TAGS = "#relaxingmusic #pianomusic #innerpeace #meditationmusic #oceanvibes #calmmusic #mindfulness"
# the three captions, in the three styles the pipeline's build_caption() writes (platform names left out)
CAPS = [
    {"kind": "short, hashtags", "lines": [TITLE, TAGS]},
    {"kind": "a hook, link in bio", "lines": [TITLE, DESC, "Full version: link in bio!"]},
    {"kind": "keyword-rich, a board", "lines": [TITLE, DESC, "board · Ocean Piano Meditation Music"]},
]

TABLE = {
    "dur": DUR, "beat": round(BEAT, 6), "bpm": BPM, "T": T,
    "energy": EN["energy"], "trackDur": EN["duration"], "best": EN["best"],
    "bestLabel": f"{mmss(EN['best'])} to {mmss(EN['best'] + 60)}",
    "slabN": EN["slabN"], "slabFps": EN["slabFps"], "src": EN["src"],
    "lines": [
        [b(1), b(5), "One video in,"],
        [b(6), b(11), "the strongest minute,"],
        [b(12.5), b(17), "cut to vertical,"],
        [b(18.5), b(22), "one link,"],
        [b(25), b(31), "three captions,"],
        [b(31.5), b(35), "spaced out, queued."],
    ],
    # beats the picture moves on
    "sweep": [b(0.6), b(4.6)],          # I: the slit writes the strip
    "graph": [b(5.2), b(7)],            # II: the energy line draws on
    "slide": [b(7), b(8.5)],            # the window leaves the first minute for the strongest
    "zoom": [b(9), b(10.4)],            # the window opens to the frame
    "unfold": [b(9.6), b(11)],          # and the strip unfolds into the moving picture
    "drift": [b(11.3), b(13)],          # III: the outside slits drift back in time
    "fall": [b(13), b(15.6)],           # and fall
    "freeze": b(17),                    # IV: the hold
    "mosh": [b(17.3), b(20.4)],
    "collapse": [b(20.4), b(21.3)],
    "linkLine": [b(21.0), b(22.4)],
    "phones": [b(22), b(22.6), b(23.2)],
    "ripple": [b(22.4), b(26)],
    "caps": [b(24), b(25.2), b(26.4)],
    "queue": [b(31), b(32.6)],
    "tunnel": [b(32.6), b(35)],
    "titleType": [b(35), b(37)],
    "line": b(37.6),
    "caps_text": CAPS,
    "name": "Tidesstunes Social Pipeline",
    "claim": "One video in, three platforms out.",
    "url": "ai.joaoqueiros.com/systems/tidesstunes-social-pipeline",
}
TABLE["cuts"] = [T["minute"][0], T["vertical"][0], T["link"][0], b(32.6), T["title"], T["mark"]]

os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
with open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8") as f:
    f.write("window.TABLE = " + json.dumps(TABLE, ensure_ascii=False) + ";\n")
json.dump(TABLE, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("table:", DUR, "s,", BPM, "bpm, strongest minute", TABLE["bestLabel"])
