# R19 · Phoropter

**Style:** choosing a solution as an optician's phoropter in a black studio, filmed in macro like a watch commercial.
One problem sits on the eye chart, out of focus; every lens that clicks in front of it is one option, "one, or two?"
is the method, and the lens that locks brings the chart into focus as one recommendation.
**Made for:** AI Problem-to-Solution Assessment (ai.joaoqueiros.com/services/ai-tools-assessment).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom and a reflector floor) · GSAP · Python (table, word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Problem-to-Solution Assessment service: an optician's
phoropter in a black studio, filmed in macro like a watch commercial, Three.js with bloom, brass and black enamel,
glass lenses with real refraction, a polished floor that reflects everything (a TSL reflector), an eye chart in a
lightbox in cool paper white, teal #00BFB4 for the HUD, the bottleneck ring and the checks.
One problem: the chart is out of focus, its rows a made-up workflow from big to small ("QUOTES", "TAKE THREE DAYS",
"RE-TYPED INTO TWO SYSTEMS", "PRICED BY HAND, CHASED BY EMAIL", "ONE WORKFLOW · EVERY WEEK").
How it runs now: the phoropter swings in on a side arm and settles with a damped wobble, the lens wheel turns a full
eight detents, five gauges on the bridge sweep, and the chart sharpens row by row into a process map ("Request in",
"Re-typed", "Priced by hand", "Checked", "Sent"); a teal ring draws around "Priced by hand", the bottleneck.
One, or two?: three numbered lenses click into the aperture in turn, an off-the-shelf tool, a connected workflow and a
simpler process change. Each time the chart drops out of focus and redraws as that option's version of the workflow,
and the gauges (cost, setup, risk, upkeep, undo) swing to its readings.
Checked, not guessed: the three lenses fly out and line up in front of the chart, each over a dark card of five checks
("Price fits", "Connects to your tools", "Data stays where it should", "Upkeep you can carry", "Solves the
bottleneck") that tick or cross row by row. Lens 1 fogs and swings away; lens 3, which ticks everything but the
bottleneck, slides off.
One recommendation: lens 2 flies back to the wheel, turns into the aperture and locks with a click and a ring of light.
Through the eyepiece the chart snaps sharp: "A connected workflow.", its steps, "SUCCESS METRIC, TO TEST · QUOTES OUT
THE SAME DAY" and a strip of 30 days that tick on, with check-ins at days 7, 14, 21 and 30.
The brief: the chart leaves the lightbox, turns over in flight and lands on the desk as the decision brief, stamped
"DAY 5"; light leaves the brass eye rings and draws the word "clear" in beads. End on "AI Problem-to-Solution
Assessment", "One problem, the real options checked, one recommendation in five business days." and the URL. Station
titles wipe on bottom left; a HUD names each stage.
Technique: one seeded table baked in Python holds the film's clock, the chart's lines, each option's steps, gauge
readings and checks, every detent of the wheel and the 30 days; the film and the score both read it. The focus is one
TSL shader that mixes a sharp, a mid and a soft copy of the chart, with a softness and a row gradient driven by the
clock. No promised savings: the metric is shown as something to test.
Score: compose it in code from the same table: a D minor drone under a pad that stays muffled while the chart is out
of focus and opens as it sharpens, a click for every detent, an 84 bpm pulse over Dm, Bb, F, C, a soft "one... two"
for each lens, needle ticks, a bright tick for every check that holds and a muted knock for every one that fails, a
hiss as the lens fogs, a reverse swell into the lock, then D major with bells, a tick for every test day and a bell at
each check-in, a paper swish, a thud and the stamp, and one wide D chord under the word.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: choosing {what_is_chosen} as an
optician's phoropter in a black studio, Three.js with bloom, brass and black enamel, glass lenses, a reflective floor,
{accent} accents. The eye chart shows {the_problem}, out of focus; the phoropter swings in and it sharpens into
{how_it_runs_now}, with {the_bottleneck} ringed. Three lenses click in: {option_1}, {option_2}, {option_3}; through
each the chart redraws, and gauges read {five_measures}. Each lens is checked against {five_checks}; two leave.
{the_winner} locks, and the chart snaps sharp: {the_recommendation}, {the_metric_to_test} and {the_test_period}.
The chart lands as {the_deliverable}, stamped "{the_stamp}". Then the lens rings draw the word "{word}".
End on {title}, {line} and {url}. One baked table drives the picture and a score composed in code.
```

Ideas: three suppliers checked before one is chosen; three hiring routes for one open role; three ways to fix a slow
handover; three venues for one event.

## How it's built

1. **One table.** `bake/table.py` holds the film's clock, the problem, the process map, the three options (steps,
   gauge readings, checks), the brief, every detent of the wheel and the 30 days of the test. The film reads
   `assets/table.js` and the score reads `bake/table.json`, so every click lands on what you see.
2. **Focus in one shader.** Every chart state is drawn once on a canvas, then copied twice with a canvas blur filter.
   A TSL shader mixes the sharp, mid and soft copies by a softness and a row gradient, so a chart can sharpen from the
   top row down; swapping a texture node's `value` changes the state.
3. **The phoropter.** The arm, the bridge, the wheel, the gauges and the eye rings are plain geometry in brass and
   enamel lit by a RoomEnvironment; the swing is a damped cosine on the clock and the wheel snaps detent to detent.
4. **Glass lenses.** Each option lens is a `MeshPhysicalNodeMaterial` with transmission, a thin thickness and a low
   IOR, so the chart reads through it without a big zoom. Lens 1 fogs by raising its roughness and dropping its
   transmission.
5. **Check cards.** Six card textures per option are drawn ahead of time, one for each number of checks shown, so a
   frame just picks one; the ring round the bottleneck is a tube revealed with a draw range.
6. **Through the eyepiece.** The camera sits on the line from the aperture to the chart, close behind the ring; the
   winning lens's glass is hidden once it locks, so the chart snaps sharp. The 30 days are one instanced mesh.
7. **The brief and the word.** The chart flips to the desk by a quaternion slerp and shows the brief on its back;
   points sampled from the word's outlines are reached from the four brass eye rings.

## Gotchas worth knowing

- Looking through an aperture, put the camera on the line from the aperture to the subject and close to it, or the
  ring hides half the chart; widen the lens in the portrait cut.
- Glass with real thickness magnifies what is behind it: keep it thin and the IOR low when the text must stay readable.
- A white chart and a brief on the desk blow out under bloom: keep their albedo and emissive low, and dim the key light
  while the camera is behind the eyepiece.
- A side arm keeps the instrument clear of the chart; an overhead arm crosses the very thing you are trying to read.
