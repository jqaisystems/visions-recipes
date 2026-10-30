"""The one table for R26 The Gate: the clock of every scene on a 112 bpm grid, the flood and the kill switch, the
pins, the scores and lanes, the drafts and their repairs, the gate's locks, Approve and the throttled send. The film
reads assets/table.js, the score reads bake/table.json. Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, DUR = 30, 112, 32.0
BEAT = 60 / BPM                                   # 0.5357 s
q = lambda b: round(b * BEAT, 4)                  # beat number to seconds

T = {
    "flood": [0.0, q(8)],          # one envelope stamps in and multiplies into a storm; the kill switch freezes it
    "find": [q(8), q(17)],         # the gold line draws a street map; pins drop; pins morph into shopfronts
    "score": [q(17), q(26)],       # cards pass a dial and sort into four lanes; the skip lane folds away
    "draft": [q(26), q(37)],       # one hot lead splits into drafts A, B, C; the tone audit strikes and repairs
    "gate": [q(37), q(50)],        # the gate draws itself, four locks, a dead stop, Approve, the gate opens
    "title": q(50),
    "end": DUR,
}
stamp = q(1)                                      # the first envelope stamps in
storm = [q(1.5), q(5.5)]                          # it multiplies into a spiral storm
kill = q(6)                                       # the kill switch slices the frame
streets = [q(8), q(10.5)]                         # the street map draws on
pins = [q(10.5 + k * 0.5) for k in range(6)]      # six pins drop on the half beat
shops = [q(13.5 + k * 0.5) for k in range(4)]     # four pins open and morph into shopfronts
LEADS = [("CAFÉ", 92, "HOT"), ("STUDIO", 74, "WARM"), ("CLINIC", 41, "COLD"), ("WORKSHOP", 18, "SKIP"),
         ("BAKERY", 88, "HOT"), ("GYM", 63, "WARM")]
cards = [{"t": q(17.5 + 1.25 * k), "name": n, "score": s, "lane": l} for k, (n, s, l) in enumerate(LEADS)]
fold = q(25)                                      # the skip lane folds away
split = q(26.5)                                   # the hot café card splits into three drafts
drafts = [q(27 + 0.5 * k) for k in range(3)]      # A, B, C land
scan = [q(30), q(34.5)]                           # the tone audit's scan line runs down the drafts
flags = [{"t": q(30.75 + 1.25 * k), "draft": d} for k, d in enumerate((1, 0, 2))]   # each struck, then repaired a beat later
gate_draw = [q(37), q(41)]                        # the gate draws itself in gold hairlines
locks = [{"t": q(41.5 + k), "word": w} for k, w in enumerate(("DUPLICATE CONTACT", "DO-NOT-CONTACT", "TONE", "RECIPIENT"))]
cursor = [q(45), q(46.25)]                        # the cursor glides to Approve
stop = q(46.25)                                   # a dead stop
approve = q(46.5)                                 # the click
gate_open = [q(46.5), q(48)]                      # the panels fold open
sends = [q(47 + k) for k in range(4)]             # the envelope steps through on the beat: the throttle
reply = q(51)                                     # a reply arrow draws back
mark = q(52)                                      # everything collapses into the IQ tile

impacts = [{"t": kill, "n": 2}, {"t": approve, "n": 2}, {"t": T["title"], "n": 1}]

table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "stamp": stamp, "storm": storm, "kill": kill,
         "streets": streets, "pins": pins, "shops": shops, "cards": cards, "fold": fold, "split": split, "drafts": drafts,
         "scan": scan, "flags": flags, "gate_draw": gate_draw, "locks": locks, "cursor": cursor, "stop": stop,
         "approve": approve, "gate_open": gate_open, "sends": sends, "reply": reply, "mark": mark, "impacts": impacts}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(T)); print("cards", [c["t"] for c in cards], "approve", approve, "sends", sends)
