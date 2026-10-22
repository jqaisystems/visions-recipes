# R08 · Boiling Line

**Style:** everything looks drawn by hand. Ink lines never sit still: they are redrawn with a new wobble 12 times
a second, like hand-drawn animation "on twos", over warm paper with one watercolour wash. Nothing is drawn by
hand: every stroke, wobble and wash is computed from time.
**Made for:** the Music page on visions.joaoqueiros.com (calm piano and ocean tracks made with Suno).
**Length:** 26 s · 1920×1080 · 30 fps file, 12 drawings a second · score composed in code.
**Stack:** HyperFrames · HTML · SVG · GSAP (one clock) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for the Music page of my site: calm piano and ocean tracks made
with Suno. Draw it like hand-drawn animation in sepia ink (#2B2420) on warm paper (#F4EEE2): a pen draws a shaky
horizon and a sun with small rays; rows of short wave strokes are sketched, smaller toward the horizon, and roll
toward the shore; three birds flap across; a small upright piano is sketched on the sand, part by part, and its
keys press one by one on a table of notes; the sun sinks, an orange watercolour wash spreads through the sky, its
reflection runs down the water and a teal wash fills the sea. End on "Music", "piano, ocean, made with Suno" and
visions.joaoqueiros.com/music, boiling like the lines. No track count.
Technique: pure SVG. Every stroke is a polyline drawn in two fineliner passes; on every drawing step (12 a
second) its points get a new seeded wobble; strokes draw on with pathLength and a dash. Motion steps on the same
12 drawings a second. The wash is gradients pushed through a turbulence displacement whose seed also changes on
the steps; the type gets a gentler one. One painter computes every frame from time.
Score: compose it in code with numpy in the spirit of my tracks: a pen scratch while lines draw, an ocean swell,
soft pads, and the drawn piano playing the same notes its keys press.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames, drawn like hand-drawn animation.
In {ink_colour} ink on {paper}: {scene_drawings}, drawn on stroke by stroke, then {motion}.
{instrument_or_object} reacts to {event_table}. A {wash_colour} watercolour wash {wash_moment}.
End on {final_line} and {url}, boiling like the lines.
Pure SVG: polylines with a seeded wobble that changes 12 times a second, two passes, dash draw-on.
Score composed in code: {score_idea}, with a pen scratch while lines draw.
```

Ideas: a recipe drawn ingredient by ingredient, a city skyline for a travel page, a product sketched before its
photo appears, a map of a route drawn as you hear the place names.

## How it's built

1. **Boil on twos.** The drawing step is the time rounded down to twelfths of a second. Each point of each stroke
   gets an offset from a hash of (step, stroke, pass, point), so the same frame always wobbles the same way and
   the line changes 12 times a second, not 30, which is what makes it read as drawn.
2. **Two passes.** Every stroke is drawn twice: a firm line and a thinner, lighter one slightly offset with its
   own wobble, like a fineliner going over a pencil line.
3. **Draw-on without measuring.** Each path has `pathLength="1"`, so the dash array is just "how much is drawn" and
   "the rest", whatever the shape.
4. **Motion on the same steps.** Waves, birds and the sun move by the stepped time too, so nothing glides
   smoothly between drawings.
5. **Watercolour from a filter.** The wash is gradients run through an SVG turbulence displacement with a soft
   blur. Its seed changes every other step, so the wet edge shimmers more slowly than the ink.
6. **Picture and sound share the notes.** One table of note times and keys drives both the pressed keys in the
   drawing and the piano in the score.

## Gotchas worth knowing

- Fill drawn objects with the paper colour, or the lines behind them show through.
- Clip the sky and the sea washes apart; two multiply washes that overlap turn brown.
- A press on a drawn key needs more than a thicker line: fill the lower part of the key for a moment.
