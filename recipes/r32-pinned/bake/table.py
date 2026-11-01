"""The one table for R32 · Pinned: every beat of the film on a 100 bpm grid, João's own Kayak listing and the pins the
system made from it (titles, alt text and boards as written by the system), and the schedule. The film reads assets/table.js, the score reads bake/table.json.
Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, POSES = 30, 100, 12                    # shot on twos: 12 poses a second
BEAT = 60 / BPM                                  # 0.6 s
b = lambda x: round(x * BEAT, 4)
DUR = b(56)

T = {
    "listing": [0.0, b(7)],       # a paper listing slides onto the table
    "split": [b(7), b(15)],       # the gallery fans out; scissors cut out the charts; the video peels away
    "pins": [b(15), b(23)],       # each photo is cut to a 2:3 pin and a tag unfolds with its SEO
    "boards": [b(23), b(31)],     # a spread opens, two boards pop up, pins are pushed on
    "schedule": [b(31), b(40)],   # a week of strips, pins dropped into slots with gaps
    "video": [b(40), b(47)],      # the filmstrip folds to 9:16, gets a cover and goes into the manual folder
    "title": b(47),
    "end": DUR,
}

# João's own listing: its title, five of its tags and the two boards its pins went to
LISTING = {"title": "Kayak Hoodie Graphic Pullover for Outdoor Lovers", "tags": ["kayak hoodie", "lake life hoodie", "gift for kayaker", "outdoor hoodie", "kayak gifts"]}
BOARDS = ["Kayak and Paddle Gear", "Kayak Life & Outdoor Gifts"]
# the gallery as it fans out: four photos, the size and colour charts the filter leaves out, one video
GALLERY = ["photo0", "photo1", "size", "photo2", "colour", "photo3", "film"]
# the listing's media, local and never committed (see README): photos, charts, the video cover, the video at 12 fps
MEDIA = {"photos": ["photo0", "photo1", "photo2", "photo3"], "charts": ["size", "colour"], "cover": "cover", "frames": 73}
# one pin per photo, with the title, alt text and board the system gave it
PINS = [
    {"photo": 0, "title": "Kayak Graphic for Outdoor Lovers Sweater for Kayaker", "alt": "Kayak Graphic for Outdoor Lovers graphic on crewneck sweater, mockup product photo", "board": 0},
    {"photo": 1, "title": "Kayak Graphic for Outdoor Lovers Sweater for Outdoor Enthusiast", "alt": "Kayak Graphic for Outdoor Lovers graphic on crewneck sweater, mockup product photo", "board": 0},
    {"photo": 2, "title": "Kayak Graphic Hoodie for Kayakers", "alt": "A man near calm water wears a bright royal-blue hoodie and matching knit beanie.", "board": 1},
    {"photo": 3, "title": "Kayak Graphic Hoodie for Kayakers", "alt": "Woman wearing a burgundy pullover hoodie with a white “KAYAK” graphic and paddle shapes.", "board": 1},
]
# the schedule: day, time, in board rotation (Outdoor, Beach, Outdoor, Beach), never two together
SLOTS = [{"pin": 0, "day": 0, "time": "09:40"}, {"pin": 2, "day": 1, "time": "19:15"},
         {"pin": 1, "day": 2, "time": "13:05"}, {"pin": 3, "day": 3, "time": "20:30"}]

E = {
    # I · listing
    "listIn": [b(0.5), b(2)], "line0": b(3),
    # II · split
    "lift": b(7), "fan": [b(7.5), b(9)], "line1": b(9), "snips": [b(10.5), b(12)], "scissorsIn": b(9.5),
    "filmPark": [b(13), b(14)], "listOut": [b(13), b(14)], "align": [b(14), b(15)],
    # III · pins: scissors run down each dotted line, the scrap falls on the beat
    "dots": b(15), "cuts": [[b(15.4 + k), b(16.3 + k)] for k in range(4)], "tags": [b(19.6 + 0.5 * k) for k in range(4)], "line2": b(20.6),
    # IV · boards
    "tagsIn": [b(23), b(23.5)], "hover": [b(23), b(24)], "bookIn": [b(23.5), b(24.5)], "open": [b(25), b(26.5)],
    "pinOn": [b(27 + 0.75 * k) for k in range(4)], "line3": b(29.5),
    # V · schedule
    "bookOut": [b(31), b(32)], "days": [b(31.5 + 0.3 * k) for k in range(5)], "drops": [b(34 + k) for k in range(4)], "line4": b(37.5),
    # VI · video
    "schedOut": [b(40), b(40.8)], "filmIn": [b(40), b(41)], "fold": [b(41.5), b(42.5)], "grow": [b(42.5), b(43)],
    "cover": b(43.5), "folderIn": [b(43.8), b(44.5)], "file": [b(45), b(46)], "line5": b(44),
    # VII · title
    "line6": b(47), "sweep": [b(50), b(51)], "logo": b(51), "name": b(52), "url": b(53),
}
# each line of type: the beat its words drop in, the beat they are picked off
LINES = [
    {"words": ["Etsy", "media", "in,"], "accent": -1, "t": E["line0"], "out": b(6.6), "at": [150, 150]},
    {"words": ["Not", "every", "image", "is", "a", "pin."], "accent": 5, "t": E["line1"], "out": b(14.4), "at": [150, 150]},
    {"words": ["A", "unique", "pin", "for", "every", "image."], "accent": 1, "t": E["line2"], "out": b(22.6), "at": [150, 130]},
    {"words": ["Matched", "to", "its", "board."], "accent": 3, "t": E["line3"], "out": b(30.6), "at": [150, 130]},
    {"words": ["Scheduled,", "never", "bunched."], "accent": 2, "t": E["line4"], "out": b(39.6), "at": [150, 130]},
    {"words": ["Video", "pins", "stay", "manual,", "by", "design."], "accent": 3, "t": E["line5"], "out": b(46.6), "at": [150, 130]},
    {"words": ["Pinterest", "queue", "out."], "accent": 2, "t": E["line6"], "out": b(50.2), "at": [0, 170], "big": True},
]
HUD = [[0, "01 import"], [b(7), "02 filter"], [b(15), "03 pins"], [b(23), "04 boards"], [b(31), "05 schedule"], [b(40), "06 video queue"]]

table = {"fps": FPS, "bpm": BPM, "beat": BEAT, "poses": POSES, "dur": DUR, "T": T, "E": E, "listing": LISTING, "boards": BOARDS,
         "gallery": GALLERY, "media": MEDIA, "pins": PINS, "slots": SLOTS, "lines": LINES, "hud": HUD}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8", newline="\n").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8", newline="\n"), indent=1)
print(json.dumps(T), DUR)
