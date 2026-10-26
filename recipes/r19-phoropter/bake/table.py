"""R19 · Phoropter. The one table: the workflow on the chart, the three options (one lens each), every gauge reading
and every check, the clicks of the lens wheel and the thirty days of the test.
Writes ../assets/table.js for the film and table.json for the score, so every sound lands on what you see.
Usage: python table.py   (standard library only, seeded)"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(19)

# the clock of the film, in seconds
T = dict(
    swing=3.7, settle=4.9,            # the phoropter swings in on its arm and settles
    dial=[5.0, 5.9],                  # a full turn of the wheel, eight detents, while the chart starts to sharpen
    sharpen=[5.5, 7.4], ring=[7.5, 8.2],
    opt=[9.0, 11.4, 13.8],            # the three lenses click in, one, or two, or three
    out=15.9,                         # the three lenses leave the wheel and line up in front of the chart
    checks=17.0,
    fog=18.8, out3=19.7,              # lens 1 fogs and swings out, then lens 3 slides away
    back=20.5, lock=21.5,             # lens 2 returns to the wheel, the wheel turns it into the aperture and locks
    days=[22.2, 24.6],                # the 30-day test
    lift=25.0, land=26.4, stamp=26.75,
    word=[27.3, 28.7], end=29.0,
)

# the problem, as an eye chart: big to small
PROBLEM = ["QUOTES", "TAKE THREE DAYS", "RE-TYPED INTO TWO SYSTEMS", "PRICED BY HAND, CHASED BY EMAIL", "ONE WORKFLOW · EVERY WEEK"]

# how it runs now, from one example; the bottleneck is ringed
MAP = dict(title="Quotes take three days.", head="HOW IT RUNS NOW · ONE REAL EXAMPLE",
           steps=["Request in", "Re-typed", "Priced by hand", "Checked", "Sent"],
           days=["day 1", "day 1", "days 1 to 3", "day 3", "day 3"], neck=2,
           foot="BOTTLENECK · PRICING WAITS FOR ONE PERSON")

GAUGES = ["COST", "SETUP", "RISK", "UPKEEP", "UNDO"]
CHECKS = ["Price fits", "Connects to your tools", "Data stays where it should", "Upkeep you can carry", "Solves the bottleneck"]

# the three paths; gauges are 0 (low) to 1 (high); checks are true / false, in the order of CHECKS
OPTIONS = [
    dict(n=1, name="An off-the-shelf tool", head="LENS 1 · AN OFF-THE-SHELF TOOL",
         steps=["Request in", "Typed into the tool", "Priced by the tool", "Checked", "Sent"],
         gauges=[0.72, 0.3, 0.7, 0.35, 0.55], checks=[True, False, False, True, True]),
    dict(n=2, name="A connected workflow", head="LENS 2 · A CONNECTED WORKFLOW",
         steps=["Request in", "Form to sheet", "Price drafted", "You check", "Sent"],
         gauges=[0.45, 0.62, 0.25, 0.42, 0.35], checks=[True, True, True, True, True]),
    dict(n=3, name="A simpler process change", head="LENS 3 · A SIMPLER PROCESS CHANGE",
         steps=["Request in", "One price list", "Priced by hand", "Checked", "Sent"],
         gauges=[0.1, 0.15, 0.1, 0.2, 0.1], checks=[True, True, True, True, False]),
]
WINNER = 1   # lens 2

FINAL = dict(head="RECOMMENDED · LENS 2", title="A connected workflow.",
             steps=["Request in", "Form to sheet", "Price drafted", "You check", "Sent"],
             metric="SUCCESS METRIC, TO TEST · QUOTES OUT THE SAME DAY")

BRIEF = dict(head="DECISION BRIEF", lines=[
    ("The workflow", "Quotes, from request to sent"),
    ("Options compared", "3 · checked on price, tools, data, upkeep"),
    ("Recommendation", "A connected workflow"),
    ("30-day test", "Owner, steps and one success metric"),
    ("Next", "45-minute review call"),
])

# when every check lands: lens by lens, row by row
for k, o in enumerate(OPTIONS):
    o["checkT"] = [round(T["checks"] + 0.55 * k + 0.1 * j, 3) for j in range(len(CHECKS))]

# the wheel: [time, angle in detents]; a detent is 45 degrees, slot k sits in the aperture at -k detents
WHEEL = [[0, 0]]
for j in range(8):                                             # one full turn while the dials are set
    WHEEL.append([round(T["dial"][0] + (T["dial"][1] - T["dial"][0]) * (j + 1) / 8, 3), -(j + 1)])
WHEEL.append([T["opt"][0], -9])                                # lens 1
WHEEL.append([T["opt"][1], -10])                               # lens 2
WHEEL.append([T["opt"][2], -11])                               # lens 3
WHEEL.append([round(T["back"] + 0.4, 3), -10])                 # back to slot 2, ready for lens 2 to come home

# the thirty days of the test: each one ticks on; a few are marked as check-ins
DAYS = [round(T["days"][0] + (T["days"][1] - T["days"][0]) * (d / 29) ** 0.9, 3) for d in range(30)]
CHECKIN = [7, 14, 21, 30]

TABLE = dict(T=T, problem=PROBLEM, map=MAP, gauges=GAUGES, checks=CHECKS, options=OPTIONS, winner=WINNER,
             final=FINAL, brief=BRIEF, wheel=WHEEL, days=DAYS, checkin=CHECKIN)
with open(os.path.join(HERE, "..", "assets", "table.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.TABLE = " + json.dumps(TABLE, ensure_ascii=False) + ";\n")
with open(os.path.join(HERE, "table.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(TABLE, f, ensure_ascii=False, indent=1)
print("wheel steps:", len(WHEEL), "days:", len(DAYS))
