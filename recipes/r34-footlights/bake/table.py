"""The one table for R34 · Footlights: every beat of the film on a 96 bpm grid, the phone's settings, the pairing PIN,
the bridge's controls, the frames on the pulley and the lines of type. The film reads assets/table.js, the score reads
bake/table.json. The PIN digits are a sample; the control labels are the bridge's own.
Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, POSES = 30, 96, 12                     # shot on twos: 12 poses a second
BEAT = 60 / BPM                                  # 0.625 s
b = lambda x: round(x * BEAT, 4)
DUR = b(53)

T = {
    "curtain": [0.0, b(4.5)],     # the curtains part on a paper home office at night
    "phone": [b(4.5), b(10)],     # a phone rises from a trap; two flaps pick 1080p and the front camera
    "pair": [b(10), b(16)],       # six PIN tiles flip on the phone and match on the PC; the phone's screen goes dark
    "link": [b(16), b(21)],       # a USB cable unrolls across the stage, Wi-Fi rings ripple behind it
    "feed": [b(21), b(33)],       # the picture runs to the PC as paper frames on a pulley; zoom, exposure, camera
    "stage": [b(33), b(40)],      # Start OBS Camera: the meeting tile lights, the footlights pop up
    "local": [b(40), b(46)],      # a roller blind drops over the cloud: 0 accounts, no server, no telemetry
    "title": b(46),
    "end": DUR,
}

PIN = "418302"
SETTINGS = [["720p", "1080p"], ["back", "front"]]   # each flap turns from the first to the second
TAGS = ["0 accounts", "no server", "no telemetry"]
PEOPLE = [  # the other tiles in the meeting: invented paper puppets
    {"skin": "#d9a27c", "hair": "#2a1d18", "top": "#5f7f6a", "wall": "#3b3550"},
    {"skin": "#a8714f", "hair": "#141012", "top": "#c9a24f", "wall": "#2e3b55"},
    {"skin": "#efc9a7", "hair": "#8a4a2a", "top": "#6b5a9a", "wall": "#40304a"},
]

E = {
    # I · curtain up
    "lamp": [b(0.2), b(1.2)], "curtain": [b(1), b(3.2)], "line0": b(2.5),
    # II · the phone
    "phoneUp": [b(4.6), b(6.2)], "beam": [b(6.4), b(7.2)], "flaps": [b(7.5), b(9)], "line1": b(7),
    # III · pairing
    "panelIn": [b(10), b(11)], "pinPhone": [b(11.5 + 0.25 * k) for k in range(6)], "pinPC": [b(13 + 0.25 * k) for k in range(6)],
    "match": b(14.6), "screenOff": [b(15), b(15.6)],
    # IV · USB or Wi-Fi
    "usbBtn": b(16.5), "cable": [b(16.6), b(18.6)], "wifi": [b(18.8), b(19.4), b(20)], "line2": b(17),
    # V · the feed
    "pulley": [b(21), b(22)], "run": b(22), "fps": b(23), "zoom": [b(25), b(26)], "expo": [b(27), b(28)],
    "switch": [b(29.5), b(31)], "line3": b(26),
    # VI · on stage
    "start": b(33.5), "panelOut": [b(34), b(35)], "tile": b(35.4), "foot": [b(36 + 0.3 * k) for k in range(6)], "line4": b(35.5),
    # VII · stays local
    "blind": [b(41), b(42.6)], "tags": [b(43), b(43.6), b(44.2)], "line5": b(41.2),
    # VIII · title
    "close": [b(46), b(47.2)], "cloth": [b(47.2), b(48)], "logo": b(48), "name": b(49), "url": b(50),
}
LINES = [
    {"words": ["Your", "phone"], "accent": 1, "t": E["line0"], "out": b(13.4), "at": [150, 130]},
    {"words": ["is", "the", "camera."], "accent": 2, "t": E["line1"], "out": b(13.6), "at": [150, 250]},
    {"words": ["USB", "or", "Wi-Fi."], "accent": 2, "t": E["line2"], "out": b(20.4), "at": [150, 130]},
    {"words": ["You", "run", "the", "picture."], "accent": 3, "t": E["line3"], "out": b(32.4), "at": [150, 130]},
    {"words": ["Live", "in", "your", "meeting."], "accent": 3, "t": E["line4"], "out": b(39.4), "at": [150, 130]},
    {"words": ["Nothing", "leaves", "the", "room."], "accent": 3, "t": E["line5"], "out": b(45.6), "at": [150, 130]},
]
HUD = [[0, "01 curtain up"], [b(4.5), "02 the phone"], [b(10), "03 pairing"], [b(16), "04 usb or wi-fi"], [b(21), "05 the feed"],
       [b(33), "06 on stage"], [b(40), "07 stays local"]]

table = {"fps": FPS, "bpm": BPM, "beat": BEAT, "poses": POSES, "dur": DUR, "T": T, "E": E, "pin": PIN, "settings": SETTINGS,
         "tags": TAGS, "people": PEOPLE, "lines": LINES, "hud": HUD}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8", newline="\n").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8", newline="\n"), indent=1)
print(json.dumps(T), DUR)
