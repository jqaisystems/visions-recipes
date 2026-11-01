"""The one table for R33 · Planner: every beat of the film on a 108 bpm grid, the sample brief, the four weekly themes,
thirty days of posts, the three drafts the variety check throws out, and the rows of the CSV. The film reads
assets/table.js, the score reads bake/table.json.
The brief and the month are a sample for JQ VISIONS, written to show what the Social Media Content Calendar makes: they
are illustrative, not the system's own output.
Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, POSES = 30, 108, 12                    # shot on twos: 12 poses a second
BEAT = 60 / BPM                                  # 0.5556 s
b = lambda x: round(x * BEAT, 4)
DUR = b(60)

T = {
    "brief": [0.0, b(8)],         # a paper form slides in, its fields pull out as tabs
    "themes": [b(8), b(17)],      # a volvelle clicks four times, a banner unrolls for each week
    "month": [b(17), b(28)],      # an accordion of card unfolds into a month, the flaps lift in a wave
    "variety": [b(28), b(38)],    # stamps throw out a repeated hook, a repeated CTA and a third post of one format
    "export": [b(38), b(48)],     # the month folds into a printer and a tractor-feed CSV scrolls out
    "review": [b(48), b(52)],     # a pencil ticks down the margin, the strip tears off
    "title": b(52),
    "end": DUR,
}

BRIEF = [
    ["voice", "curious, exact, warm"],
    ["audience", "designers, founders, makers"],
    ["goal", "launch the recipe library"],
    ["themes", "films made in code"],
    ["highlight", "free prompts and source"],
    ["frequency", "Instagram 3 · LinkedIn 2 · Pinterest 2 a week"],
]
THEMES = [
    {"head": "Made in code.", "why": "Lead with the craft, so the rest makes sense."},
    {"head": "Open the recipe.", "why": "Show that every film comes with its method."},
    {"head": "Remix it.", "why": "Turn the people watching into people making."},
    {"head": "The whole library.", "why": "Close the month on the launch itself."},
]
# a week starts on Monday: Instagram, LinkedIn, Instagram, Pinterest, Instagram, LinkedIn, Pinterest
ROT = ["Instagram", "LinkedIn", "Instagram", "Pinterest", "Instagram", "LinkedIn", "Pinterest"]
P = [  # format, hook, hashtag, CTA, visual
    ["reel", "Every frame here is code", "#creativecoding", "Watch the film", "the paper desk"],
    ["article", "Why I make films in code", "#motiondesign", "Read the post", "desk from above"],
    ["carousel", "No camera, no timeline app", "#generativeart", "Swipe through", "four stills"],
    ["pin", "A film you can rebuild", "#designinspo", "Save the pin", "poster frame"],
    ["still", "One canvas, one clock", "#javascript", "Ask me how", "canvas grid"],
    ["carousel", "Five films, five techniques", "#brandfilm", "See all five", "contact sheet"],
    ["pin", "Paper, drawn in code", "#papercraft", "Pin for later", "torn edge"],
    ["reel", "The prompt behind the film", "#aiart", "Copy the prompt", "prompt card"],
    ["still", "A recipe, not a secret", "#opensource", "Open the recipe", "recipe page"],
    ["carousel", "Prompt, template, source", "#promptdesign", "Swipe for all three", "three cards"],
    ["pin", "Steal this film recipe", "#motiongraphics", "Save the recipe", "ingredients"],
    ["still", "MIT, first frame to last", "#opensource", "Grab the source", "source folder"],
    ["article", "What a remix template is", "#ai", "Read the breakdown", "the template"],
    ["pin", "Recipe card: paper cut-out", "#papercraft", "Pin the card", "recipe card"],
    ["reel", "Your brand, my recipe", "#creativecoding", "Make your own", "split screen"],
    ["carousel", "Four remixes of one film", "#brandfilm", "Pick a remix", "four frames"],
    ["carousel", "Change three lines, new film", "#motiondesign", "Try it tonight", "a code diff"],
    ["pin", "Remix ideas for makers", "#diy", "Save the ideas", "idea list"],
    ["still", "Swap the logo, keep the motion", "#branding", "Tag a designer", "logo swap"],
    ["still", "Remixing is the point", "#opensource", "Share a remix", "two posters"],
    ["pin", "A week of remixes", "#designinspo", "Pin a favourite", "mood board"],
    ["reel", "Every recipe in one place", "#creativecoding", "Browse the library", "library grid"],
    ["article", "How the library is built", "#motiondesign", "Read the story", "the shelf"],
    ["carousel", "Four seasons of technique", "#animation", "Swipe the seasons", "four styles"],
    ["pin", "Film recipes, sorted by style", "#designinspo", "Save the board", "style index"],
    ["still", "Start with any recipe", "#generativeart", "Pick one", "index card"],
    ["carousel", "From anime to paper", "#brandfilm", "See the range", "style strip"],
    ["pin", "Free recipes for code films", "#motiongraphics", "Pin the library", "poster wall"],
    ["reel", "Your first code film", "#creativecoding", "Start here", "first frame"],
    ["still", "The library stays open", "#opensource", "Follow along", "open door"],
]
POSTS = [{"day": i + 1, "platform": ROT[i % 7], "format": f, "hook": h, "tag": tg, "cta": c, "visual": v, "week": min(3, i // 7)}
         for i, (f, h, tg, c, v) in enumerate(P)]

# what the variety check catches: the first drafts of three days, each thrown out and drafted again
REJECTS = [
    {"day": 9, "stamp": "REPEAT HOOK", "of": 3, "field": "hook", "draft": {"hook": "No camera, no timeline app"}},
    {"day": 17, "stamp": "SAME CTA", "of": 15, "field": "cta", "draft": {"cta": "Make your own"}},
    {"day": 19, "stamp": "SAME FORMAT", "of": [16, 17], "field": "format", "draft": {"format": "carousel"}},
]
# the check holds for the final month: no hook or CTA twice, never three posts of one format in a week
assert len({p["hook"] for p in POSTS}) == 30 and len({p["cta"] for p in POSTS}) == 30
for w in range(5):
    fm = [p["format"] for p in POSTS[w * 7:(w + 1) * 7]]
    assert max(fm.count(f) for f in fm) <= 2, (w, fm)

CSV_HEAD = "date,platform,format,caption,hashtags,cta,visual"
CSV = [f'{p["day"]:02d},{p["platform"]},{p["format"]},"{p["hook"]}",{p["tag"]},{p["cta"]},{p["visual"]}' for p in POSTS]

E = {
    # I · brief
    "formIn": [b(0.5), b(2)], "tabs": [b(2.5 + 0.55 * k) for k in range(6)], "line0": b(3),
    # II · themes
    "formOut": [b(8), b(9)], "wheelIn": [b(8.5), b(9.5)], "clicks": [b(10 + 1.5 * k) for k in range(4)], "line1": b(10.5), "wheelOut": [b(16.4), b(17.2)],
    # III · thirty days
    "toRows": [b(17), b(18.2)], "rows": [b(17.5 + 0.55 * k) for k in range(5)], "flaps": b(21), "line2": b(23),
    # IV · variety check: a stamp lands, the draft crumples and rolls off, the new card slides in under the flap
    "stamps": [b(29.4), b(32.4), b(35.4)], "line3": b(29),
    # V · export
    "foldUp": [b(38), b(39.4)], "printerIn": [b(38), b(39)], "feedIn": [b(39.4), b(40.4)], "feed": [b(40.6), b(47.6)], "line4": b(42),
    # VI · review
    "ticks": [b(48), b(50.6)], "tear": b(51),
    # VII · title
    "plane": [b(52), b(52.8)], "fly": [b(52.8), b(54.6)], "line5": b(52.6),
    "sweep": [b(55), b(56)], "logo": b(56), "name": b(57), "url": b(58),
}
LINES = [
    {"words": ["One", "brief", "in,"], "accent": 1, "t": E["line0"], "out": b(7.4), "at": [150, 130]},
    {"words": ["Four", "weeks,", "each", "with", "a", "reason."], "accent": 5, "t": E["line1"], "out": b(16.2), "at": [150, 130]},
    {"words": ["Every", "platform,", "in", "its", "own", "voice."], "accent": 5, "t": E["line2"], "out": b(27.4), "at": [150, 130]},
    {"words": ["No", "repeats."], "accent": 1, "t": E["line3"], "out": b(37.4), "at": [150, 130]},
    {"words": ["One", "row", "per", "post."], "accent": 3, "t": E["line4"], "out": b(47.6), "at": [150, 130]},
    {"words": ["A", "month", "of", "posts", "out."], "accent": 1, "t": E["line5"], "out": b(55.0), "at": [0, 170], "big": True},
]
HUD = [[0, "01 brand brief"], [b(8), "02 themes"], [b(17), "03 thirty days"], [b(28), "04 variety check"], [b(38), "05 csv export"], [b(48), "06 review"]]

table = {"fps": FPS, "bpm": BPM, "beat": BEAT, "poses": POSES, "dur": DUR, "T": T, "E": E, "brief": BRIEF, "themes": THEMES,
         "posts": POSTS, "rejects": REJECTS, "csvHead": CSV_HEAD, "csv": CSV, "lines": LINES, "hud": HUD}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8", newline="\n").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8", newline="\n"), indent=1)
print(json.dumps(T), DUR, max(len(r) for r in CSV))
