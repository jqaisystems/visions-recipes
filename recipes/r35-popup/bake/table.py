"""The one table for R35 · Pop-Up: every beat of the film on an 88 bpm grid, the sample intake form, the sections of
the brief and the lines of type. The film reads assets/table.js, the score reads bake/table.json. The client, the
answers, the personas and everything in the brief are an illustrative sample written for this film; the section
template is the system's own.
Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, POSES = 30, 88, 12                     # shot on twos: 12 poses a second
BEAT = 60 / BPM                                  # 0.6818 s
b = lambda x: round(x * BEAT, 4)
DUR = b(49)

T = {
    "intake": [0.0, b(6)],        # an intake form and the call notes slide in and feed into the book
    "synth": [b(6), b(13)],       # the cover opens: vague answers are pulled through a slot and come out concrete
    "audience": [b(13), b(19)],   # three personas stand up on a box fold
    "tone": [b(19), b(26.5)],     # a pull tab on a tone scale; a skyline of three competitors and the gap
    "visual": [b(26.5), b(34)],   # a fan of swatches and type; the deliverables stand up line by line
    "questions": [b(34), b(38)],  # a ? flap lifts on two questions for a person
    "edit": [b(38), b(42.5)],     # a red pencil goes through it, and a stamp: reviewed
    "export": [b(42.5), b(45.2)], # the book closes, folds flat into a PDF and goes into an envelope
    "title": b(45.2),
    "end": DUR,
}

FORM = [  # the intake form: a sample; two answers are the vague kind the case study names
    ["business", "a neighbourhood fitness studio"], ["offer", "small-group classes"], ["audience", "everyone who needs it"],
    ["tone", "professional but friendly"], ["competitors", "two gyms and an app"], ["goal", "fill the morning classes"],
    ["timeline", "spring"], ["budget", "small"], ["deliverables", "logo, timetable, signs"], ["anything else", "a second room opens"],
]
NOTES = ["call notes", "mornings are quiet", "people come back after injury", "the coaches know everyone"]
CONTEXT = ["A neighbourhood fitness studio,", "small-group classes,", "opening a second room.", "Goal: fill the mornings."]
STRIPS = [  # a vague answer pulled through the slot, and what comes out the other side
    {"in": "professional but friendly", "out": ["plain words", "short sentences", "a warm sign-off"]},
    {"in": "everyone who needs it", "out": ["new to training", "busy, near work", "back after injury"]},
]
TABS = ["context", "audience", "tone", "competition", "visual", "scope", "questions"]   # the system's fixed sections
PERSONAS = [
    {"name": "Ana, 34", "line": "trains before work", "skin": "#d9a27c", "hair": "#2a1d18", "top": "#2f6f73", "wall": "#e8d6b8"},
    {"name": "Rui, 52", "line": "back after an injury", "skin": "#a8714f", "hair": "#8a8a86", "top": "#dda04a", "wall": "#d9e2d6"},
    {"name": "Mia, 27", "line": "new to training", "skin": "#efc9a7", "hair": "#8a4a2a", "top": "#c4553b", "wall": "#e3d3cf"},
]
TONE = {"ends": ["formal", "casual"], "at": 0.62, "words": ["plain", "warm", "direct"]}
COMP = [["Competitor A", "big gym, low price", 200], ["Competitor B", "boutique, high price", 150], ["Competitor C", "an app, no people", 118]]
GAP = "the gap: small groups, real coaches"
SWATCH = ["#2f6f73", "#dda04a", "#f4eedf", "#c4553b", "#1d1a1f"]
SCOPE = ["logo refresh", "class timetable", "signage", "social templates", "launch poster"]
QUESTIONS = ["Second room: same name?", "Opening date confirmed?"]
SUMMARY = [["voice", "plain, direct"], ["tone", "friendly"], ["launch", "spring"]]
EDIT = {"line": 1, "strike": "friendly", "write": "warm, never pushy"}

E = {
    # I · intake form in
    "form": [b(0.3), b(1.8)], "notes": [b(2.2), b(3.2)], "feed": [b(4), b(5.4)], "line0": b(1.2),
    # II · the synthesis
    "leaf0": [b(6), b(7.4)], "strip0": [b(8), b(9.2)], "chips0": [b(9.3 + 0.35 * k) for k in range(3)],
    "strip1": [b(10.4), b(11.4)], "chips1": [b(11.5 + 0.35 * k) for k in range(3)], "tabs": [b(12 + 0.15 * k) for k in range(7)],
    "line1": b(8),
    # III · audience
    "leaf1": [b(13), b(14.4)], "per": [b(14.4 + 0.5 * k) for k in range(3)], "line2": b(15.5),
    # IV · tone and competition
    "leaf2": [b(19), b(20.4)], "tone": [b(21), b(22.6)], "toneW": [b(22.8 + 0.3 * k) for k in range(3)],
    "sky": [b(23.4 + 0.4 * k) for k in range(3)], "gap": [b(24.8), b(25.6)], "line3": b(21),
    # V · visual and scope
    "leaf3": [b(26.5), b(27.9)], "fan": [b(28.2), b(29.4)], "spec": b(29.6), "rows": [b(30.4 + 0.45 * k) for k in range(5)],
    "line4": b(28.5),
    # VI · questions
    "leaf4": [b(34), b(35.4)], "flap": [b(35.6), b(36.4)], "qt": [b(36.6 + 0.4 * k) for k in range(2)], "line5": b(35.8),
    # VII · the human edit
    "strike": [b(38.4), b(39.1)], "write": [b(39.3), b(40.4)], "ticks": [b(40.8 + 0.35 * k) for k in range(3)], "stamp": b(41.8),
    "line6": b(38.2),
    # VIII · export and title
    "close": [b(42.5), b(43.6)], "flat": [b(43.6), b(44.2)], "env": [b(44.2), b(45.2)],
    "cloth": [b(45.2), b(46)], "logo": b(46), "name": b(46.8), "url": b(47.4),
}
LINES = [
    {"words": ["Intake", "form", "in,"], "accent": 1, "t": E["line0"], "out": b(5.6), "at": [150, 130]},
    {"words": ["Vague", "words", "in,", "concrete", "out."], "accent": 3, "t": E["line1"], "out": b(12.6), "at": [150, 130]},
    {"words": ["Who", "it's", "for,"], "accent": 2, "t": E["line2"], "out": b(18.6), "at": [150, 130]},
    {"words": ["how", "it", "should", "sound,"], "accent": 3, "t": E["line3"], "out": b(26), "at": [150, 130]},
    {"words": ["and", "what", "to", "make."], "accent": 3, "t": E["line4"], "out": b(33.6), "at": [150, 130]},
    {"words": ["Questions", "flagged."], "accent": 1, "t": E["line5"], "out": b(37.8), "at": [150, 130]},
    {"words": ["Then", "a", "person", "edits", "it."], "accent": 3, "t": E["line6"], "out": b(42.2), "at": [150, 130]},
]
HUD = [[0, "01 intake"], [b(6), "02 synthesis"], [b(13), "03 audience"], [b(19), "04 tone and competition"],
       [b(26.5), "05 visual and scope"], [b(34), "06 questions"], [b(38), "07 human edit"], [b(42.5), "08 export"]]

table = {"fps": FPS, "bpm": BPM, "beat": BEAT, "poses": POSES, "dur": DUR, "T": T, "E": E, "form": FORM, "notes": NOTES,
         "context": CONTEXT, "strips": STRIPS, "tabs": TABS, "personas": PERSONAS, "tone": TONE, "comp": COMP, "gap": GAP,
         "swatch": SWATCH, "scope": SCOPE, "questions": QUESTIONS, "summary": SUMMARY, "edit": EDIT, "lines": LINES, "hud": HUD}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8", newline="\n").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8", newline="\n"), indent=1)
print(json.dumps(T), DUR)
