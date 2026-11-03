"""A demo call so the recipe runs out of the box: the screens of a fictional preparation app running a fictional
discovery call with "Example Co", drawn with Pillow and the fonts in assets/fonts. Every element the film outlines sits
where bake/table.py says it is (bubbleR, feedbackY, liveBubbleR, helpR, arabicR, dbItems), so the overlays land.
Writes assets/demo/screens/ (not committed): prep, brief, objections, roleplay, live/00..15, debrief, next.
Use your own app's screens instead, and move the rects in bake/table.py to match them.
Usage: python bake/demo.py"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "demo", "screens")
os.makedirs(os.path.join(OUT, "live"), exist_ok=True)
FD = os.path.join(ROOT, "assets", "fonts")
PAPER, CARD, INK, SAGE, HAIR, MUTED, CORAL = (244, 241, 234), (251, 249, 244), (17, 67, 83), (107, 138, 103), (221, 216, 203), (126, 134, 130), (214, 69, 80)
SOFT = (231, 236, 228)
F = lambda name, size: ImageFont.truetype(os.path.join(FD, name), size)
SANS = lambda s: F("InstrumentSans.ttf", s)
MONO = lambda s: F("IBMPlexMono-Regular.ttf", s)
SERIF = lambda s: F("Fraunces-Italic.ttf", s)


def page(h, tab):
    im = Image.new("RGB", (1600, h), PAPER); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1600, 60), fill=CARD); d.line((0, 60, 1600, 60), fill=HAIR, width=2)
    d.text((32, 20), "PREP STUDIO · DEMO", font=MONO(16), fill=INK)
    x = 1568
    for t in reversed(["PREPARE", "REHEARSE", "LIVE", "DEBRIEF"]):
        w = d.textlength(t, font=MONO(15)); x -= w
        d.text((x, 21), t, font=MONO(15), fill=INK if t == tab else MUTED)
        if t == tab: d.line((x, 52, x + w, 52), fill=CORAL if t == "LIVE" else INK, width=3)
        x -= 36
    return im, d


def box(d, r, fill=CARD, line=HAIR, w=2, rad=10):
    x, y, bw, bh = r
    d.rounded_rectangle((x, y, x + bw, y + bh), rad, fill=fill, outline=line, width=w)


def fit(d, xy, s, font_fn, size, maxw, fill=INK):
    while d.textlength(s, font=font_fn(size)) > maxw and size > 10: size -= 1
    d.text(xy, s, font=font_fn(size), fill=fill)


def bars(d, x, y, w, n, step=26, seed=0):
    for i in range(n):
        ww = w * (0.55 + 0.4 * ((i * 37 + seed * 11) % 10) / 10)
        d.rounded_rectangle((x, y + i * step, x + ww, y + i * step + 9), 4, fill=HAIR)


def label(d, xy, s, fill=MUTED): d.text(xy, s.upper(), font=MONO(14), fill=fill)


# prepare: the form
im, d = page(1020, "PREPARE")
d.text((48, 96), "New preparation", font=SERIF(46), fill=INK)
y = 190
for lab, val in [("Meeting type", "Client meeting · discovery call"), ("With", "Head of Finance, Example Co (demo)"),
                 ("Website", "example.com"), ("Goal", "Agree a two-week pilot on one entity")]:
    label(d, (48, y), lab); box(d, (48, y + 24, 1504, 60)); d.text((70, y + 40), val, font=SANS(24), fill=INK); y += 112
label(d, (48, y), "Context"); box(d, (48, y + 24, 1504, 230)); bars(d, 72, y + 52, 1300, 7, seed=1)
box(d, (48, 900, 300, 64), fill=SAGE, line=SAGE); d.text((84, 918), "Build the brief", font=SANS(24), fill=CARD)
im.save(os.path.join(OUT, "prep.png"))

# the brief, writing down the page
im, d = page(1075, "PREPARE")
d.text((48, 96), "Brief · discovery call · Example Co", font=SERIF(44), fill=INK)
cols = [("Talking points", ["Start with invoice reconciliation", "Offer a two-week pilot on one entity", "Name the success criteria up front"]),
        ("Security review", ["Expect it to be their gating step", "Bring the data-handling one-pager", "Offer to join their review call"]),
        ("Discovery questions", ["How do you close the month today?", "Who signs off on a pilot?", "What would make two weeks a win?"])]
for c, (h, items) in enumerate(cols):
    x = 48 + c * 512
    label(d, (x, 190), h, SAGE); d.line((x, 216, x + 470, 216), fill=HAIR, width=2)
    for i, it in enumerate(items):
        box(d, (x, 236 + i * 150, 470, 128)); fit(d, (x + 20, 252 + i * 150), it, SANS, 22, 430); bars(d, x + 20, 296 + i * 150, 400, 2, seed=c * 3 + i)
label(d, (48, 712), "Who they are"); box(d, (48, 736, 1504, 300)); bars(d, 72, 766, 1400, 9, seed=5)
im.save(os.path.join(OUT, "brief.png"))

# likely objections
im, d = page(1075, "PREPARE")
d.text((48, 96), "Likely objections", font=SERIF(44), fill=INK)
for i, q in enumerate(["We cannot send financial data to an external provider.", "We tried a tool like this last year.",
                       "The team has no time for a pilot.", "Who can see what is recorded?"]):
    y = 190 + i * 210
    box(d, (48, y, 1504, 184)); label(d, (72, y + 20), f"objection {i + 1}", SAGE)
    fit(d, (72, y + 48), "\u201c" + q + "\u201d", SERIF, 32, 1440); label(d, (72, y + 104), "answer"); bars(d, 170, y + 108, 1200, 2, seed=i)
im.save(os.path.join(OUT, "objections.png"))

# rehearse: the role-play (the client's question at bubbleR, the feedback at feedbackY)
im, d = page(900, "REHEARSE")
label(d, (32, 84), "mock session · the client, played for you", SAGE)
box(d, (872, 140, 696, 100)); label(d, (892, 154), "you"); bars(d, 892, 184, 620, 2, seed=2)
label(d, (32, 280), "the client")
box(d, (32, 306, 1228, 110)); fit(d, (56, 336), "We cannot send financial data to an external provider. How would this work?", SANS, 30, 1180)
box(d, (34, 424, 1180, 24), fill=SOFT, line=SOFT, rad=6); d.text((46, 427), "FEEDBACK · NAME WHERE THE DATA STAYS, THEN OFFER THE SECURITY REVIEW", font=MONO(14), fill=SAGE)
box(d, (872, 490, 696, 140)); label(d, (892, 504), "you"); bars(d, 892, 534, 620, 3, seed=4)
box(d, (32, 780, 1536, 72)); d.text((60, 802), "Answer out loud, or type", font=SANS(24), fill=MUTED)
d.ellipse((1500, 796, 1540, 836), outline=INK, width=3)
im.save(os.path.join(OUT, "roleplay.png"))

# live: sixteen frames of the call (the objection at liveBubbleR from frame 4, help at helpR, the translated line at arabicR)
OBJ = "We cannot send financial data to an external provider."
for j in range(16):
    im, d = page(900, "LIVE")
    d.ellipse((32, 84, 46, 98), fill=CORAL); label(d, (56, 82), f"live · discovery call · 00:12:{10 + j * 3:02d}", INK)
    box(d, (44, 120, 592, 64)); fit(d, (64, 138), "Thanks for making the time today.", SANS, 24, 552)
    box(d, (440, 204, 500, 64), fill=SOFT, line=SOFT); fit(d, (460, 222), "Shall we start with reconciliation?", SANS, 24, 460)
    if j >= 1: box(d, (44, 288, 592, 56)); fit(d, (64, 302), "Sure. One thing first.", SANS, 24, 552)
    if j >= 2:
        n = [15, 30, len(OBJ)][min(j - 2, 2)]
        box(d, (44, 368, 592, 64)); fit(d, (64, 386), OBJ[:n], SANS, 24, 552)
    if j >= 7: box(d, (560, 472, 380, 64), fill=SOFT, line=SOFT); fit(d, (580, 490), "It stays on your side.", SANS, 24, 340)
    if j >= 11:
        box(d, (44, 472, 478, 134)); fit(d, (64, 490), "\u00bfCu\u00e1l es el calendario del proyecto?", SANS, 24, 440)
        if j >= 12:
            d.line((64, 534, 502, 534), fill=HAIR, width=2); label(d, (64, 548), "EN", SAGE); fit(d, (100, 544), "What is the timeline for the project?", SANS, 20, 400, SAGE)
    if j >= 13: box(d, (560, 640, 380, 64), fill=SOFT, line=SOFT); fit(d, (580, 658), "Two weeks, one entity.", SANS, 24, 340)
    # the side panel: notes from the prep, then the help card
    label(d, (1032, 120), "from the prep"); box(d, (1032, 146, 528, 220)); bars(d, 1056, 176, 470, 6, seed=7)
    if j >= 4:
        box(d, (1032, 406, 528, 156), line=SAGE if j >= 5 else HAIR)
        if j >= 5: label(d, (1056, 424), "help · handle this objection", SAGE)
        if j >= 6: fit(d, (1056, 454), "Data stays on their side.", SANS, 24, 480)
        if j >= 7: fit(d, (1056, 494), "Offer the security review first.", SANS, 24, 480)
    # who is talking: a level strip that moves frame to frame
    for i in range(48):
        h = 6 + 26 * abs(((i * 7 + j * 5) % 13) / 13 - 0.5) * (1.6 if (j // 3) % 2 else 0.6)
        d.rounded_rectangle((44 + i * 18, 790 - h / 2, 52 + i * 18, 790 + h / 2), 3, fill=SAGE if i < 24 else HAIR)
    label(d, (44, 830), "them"); label(d, (476, 830), "you")
    im.save(os.path.join(OUT, "live", f"{j:02d}.png"))

# debrief (the items sit at dbItems in the last frame of the pan, 175 px down the page)
im, d = page(1075, "DEBRIEF")
d.text((48, 96), "Debrief · discovery call", font=SERIF(44), fill=INK)
rows = [(325, "How it went"), (420, "Talk time"), (520, "Summary"), (720, "Action items"), (903, "Gating step"), (997, "Decision")]
for y, lab in rows: label(d, (48, y + 8), lab); d.line((48, y - 16, 980, y - 16), fill=HAIR, width=1)
box(d, (405, 325, 187, 58)); d.text((428, 330), "8 / 10", font=SERIF(38), fill=INK)
d.text((405, 424), "You 44% · Them 56%", font=SANS(22), fill=INK)
bars(d, 405, 528, 560, 6, seed=3); bars(d, 405, 728, 560, 5, seed=6)
fit(d, (420, 905), "Security review is their gating step", SANS, 22, 360)
fit(d, (420, 999), "Two-week pilot on one entity", SANS, 22, 330)
im.save(os.path.join(OUT, "debrief.png"))

# the next one
im, d = page(960, "PREPARE")
d.text((48, 96), "New preparation", font=SERIF(46), fill=INK)
y = 190
for lab, val in [("Meeting type", "Client meeting · follow-up call"), ("With", "Example Co (demo)"), ("Carried over", "Two-week pilot on one entity · security review")]:
    label(d, (48, y), lab); box(d, (48, y + 24, 1504, 60)); d.text((70, y + 40), val, font=SANS(24), fill=INK); y += 112
label(d, (48, y), "Context"); box(d, (48, y + 24, 1504, 260)); bars(d, 72, y + 52, 1300, 8, seed=8)
im.save(os.path.join(OUT, "next.png"))
print("demo screens in", OUT)
