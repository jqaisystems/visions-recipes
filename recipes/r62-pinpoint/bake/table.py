"""The one table for R62 · Pinpoint, read by the film and by score/compose.py: the beat grid and every cue, so each cut, slam,
whoosh, key click and hit in the picture lands on the same beat in the music. The pipeline, its prospects and the message are a
demo. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 124; BEAT = 60 / BPM; BEATS = 80

# ---------------- every cue, in beats. One coral dot is carried through every scene, each scene handing it to the next
Q = {
    # the open: the dot drops, bounces, swells and bursts into a field of prospects
    "drop": 1.0, "bounce": 2.0, "burst": 3.0, "settle": 4.6,
    # 01 find: a lens scans the field, the fits light up, it locks on one and the camera dives into it
    "lens": [9.0, 13.2], "lock": 13.2, "zoom": 14.4, "score": 16.0,
    # 02 score: a gauge draws itself, the dot becomes its needle, the gauge unrolls into a bar and the bars sort themselves
    "dial": 18.4, "needle": 19.6, "morph": 23.6, "bars": 24.4, "sort": 26.0, "warm": 27.6, "toCard": 28.6, "wipe": 29.2,
    # 03 enrich: the top bar becomes a card, details fly in from the edges and are ticked, then the card flips
    "card": 31.6, "rows": 32.4, "rowGap": 0.5, "ticks": 35.6, "flip": 38.6, "flipMid": 39.1,
    # 04 draft: the card's back is a message that writes itself, the dot as its cursor; it is stamped, then folds into a plane
    "subject": 41.6, "typing": [42.6, 48.4], "stamp": 48.8, "fold": 50.4, "fly": 51.8, "ink": 52.6,
    # 05 your call: the plane flies at a send button and freezes short of it; the dot comes to rest beside the button
    "button": 53.2, "freeze": 56.0, "cursor": 60.6, "collapse": 66.6, "close": 68.0,
}
# the big words: [lines, beat in, beat out, size, centre y, colour, mode]. "slam" letters drop in on the beat; "type" letters appear
# one by one in the stillness after the freeze
HEADS = [
    [["FIND"], 5.0, 8.6, 360, 560, "bone", "slam"],
    [["SCORE"], 16.3, 18.0, 330, 470, "ink", "slam"],
    [["ENRICH"], 30.2, 31.8, 300, 540, "ink", "slam"],
    [["DRAFT"], 39.8, 41.6, 300, 600, "ink", "slam"],
    [["NOTHING SENDS", "AUTOMATICALLY."], 56.3, 59.8, 132, 300, "bone", "type"],
    [["YOU KEEP", "THE SEND BUTTON."], 60.4, 66.4, 132, 300, "bone", "slam"],
]
STAG = {"slam": 0.07, "type": 0.09}
for h in HEADS:   # the beat each letter lands, shared with the score
    k, lands = 0, []
    for line in h[0]:
        row = []
        for ch in line:
            row.append(round(h[1] + 0.22 + k * STAG[h[6]], 4) if ch != " " else None); k += 1
        lands.append(row)
    h.append(lands)

SUBS = [   # the small typed lines under each scene: [text, beat in, beat out, y]
    ["PROSPECTS THAT MATCH YOUR IDEAL CUSTOMER", 9.4, 14.2, 980],
    ["EVERY PROSPECT SCORED FOR FIT, 0 TO 100", 20.2, 23.6, 980],
    ["WARM LEADS FIRST, NOT A RANDOM PILE", 27.4, 29.4, 980],
    ["EACH RECORD ENRICHED WITH PUBLIC EVIDENCE", 33.4, 38.4, 905],
    ["A PERSONALISED FIRST MESSAGE", 43.0, 46.8, 960],
    ["READY FOR A PERSON TO REVIEW", 47.0, 50.4, 960],
    ["WAITING FOR YOUR REVIEW", 61.6, 66.4, 905],
]
CHAPTERS = [[5.0, "01", "FIND"], [16.1, "02", "SCORE"], [30.0, "03", "ENRICH"], [39.7, "04", "DRAFT"], [53.2, "05", "YOUR CALL"]]

DIAL_TICKS = [round(Q["dial"] + k * 0.025, 4) for k in range(41)]           # 0 to 100 in steps of 2.5
BARS = [64, 31, 87, 18, 72, 55, 79, 42]; HERO_BAR = 2
BAR_IDS = ["0187", "0233", "0412", "0519", "0604", "0771", "0838", "0905"]
ROWS = [["COMPANY", "Halden Studio"], ["SECTOR", "Design studio"], ["TEAM", "12 to 40 people"],
        ["SIGNAL", "Hiring a designer"], ["SOURCE", "Public website"], ["FIT", "87 / 100"]]

# the message, typed. Each character has its beat; a line break costs four characters of time
HDR = ["TO   Ana, Halden Studio", "RE   Your designer hire"]
MSG = ["Hi Ana,", "saw that Halden Studio is hiring a designer.", "We help small studios find the right clients.", "Worth a quick chat next week?"]
MARKS = [[1, "Halden Studio"], [1, "hiring a designer"], [0, "Ana"]]   # the words that came from the record
def schedule(lines, b0, b1, brk):
    units = sum(len(l) for l in lines) + brk * (len(lines) - 1)
    out, u = [], 0
    for l in lines:
        row = []
        for _ in l:
            row.append(round(b0 + (b1 - b0) * u / units, 4)); u += 1
        out.append(row); u += brk
    return out
TYPE_HDR = schedule(HDR, Q["subject"], Q["subject"] + 0.8, 2)
TYPE_MSG = schedule(MSG, Q["typing"][0], Q["typing"][1], 4)

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "q": Q, "heads": HEADS, "subs": SUBS, "chapters": CHAPTERS, "dialTicks": DIAL_TICKS,
    "bars": BARS, "heroBar": HERO_BAR, "barIds": BAR_IDS, "rows": ROWS,
    "hdr": HDR, "msg": MSG, "marks": MARKS, "typeHdr": TYPE_HDR, "typeMsg": TYPE_MSG,
    "label": "AI LEAD GENERATION & OUTREACH · DEMO PIPELINE",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
