# R27 · Ten Seconds

**Style:** 2D vector motion design. One SVG stage and GSAP, with no canvas, no WebGL and no 3D: a voice drawn as a
filled ribbon whose width is its loudness, letters baked to outlines that melt into that ribbon, one ribbon branching
to many, and a camera that is a single group, in a flat dark ember palette.

**Made for:** Tembr, a local voice cloning studio.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · SVG · GSAP · Python (table, glyphs, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Tembr, a voice cloning studio that runs on your own machine,
whose line is "Your voice, everywhere you can't be." 2D vector motion design only: one SVG stage and GSAP, no canvas,
no WebGL. Flat dark ember: ground #131110, surface #1c1916, text #f2ead9, amber #f3a530, and ember #d1622b only on sound
that is playing. Archivo 800, Instrument Sans and IBM Plex Mono. A voice is a ribbon: a filled path whose width at
each point is its loudness.
Record: an amber hairline breathes, then ninety seconds of voice race past as a ribbon behind a record head, with a
timer to 01:30.
Keep: pull back over the whole take; a window weighs it, locks on the strongest ten seconds, and the rest drains to
grey and peels away in curls.
Your machine: a frame draws on around the ten seconds; the clone slides up as an outline and locks on; a cloud drifts
in, stops short and erases itself. 0 CLOUD CALLS · 0 API KEYS.
It speaks: the line types itself as glyph outlines, the cloned voice speaks it, and each letter melts into its slice of
a ribbon shaped by that word's real loudness.
Everywhere: "Hi {name}," flicks through sample names; the voice flows into one lead's player page; the camera pulls
out to a wall of pages and one ribbon branches to all of them; a scan flags LONG PAUSE, REPEATED WORD and MANGLED
ENDING, and each page redraws clean.
Title: everything pulls back into one bar, then the official lockup, flat, the line and the URL. Never redraw or
recolour the mark. Score: compose it in code from the same table, 96 bpm, D minor to F major.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, in 2D vector motion design only (one SVG
stage and GSAP), flat {palette}, where {the_signal} is a filled ribbon whose width is its strength. {the_raw_input}
races past; a window keeps {the_best_part} and the rest peels away; {the_safe_place} draws on around it while
{the_threat} stops short; {the_words} melt, letter by letter, into the ribbon; and one ribbon branches to a wall of
{the_destinations}, with {the_check} flagging and redrawing a few. Then the flat lockup with {line} and {url}. One baked
table drives the ribbons, the letters, the branches and a score composed in code.
```

Ideas: a podcast editor, with an hour of talk as a ribbon, the best clip kept and captions melting into the waveform; a
heart monitor app, with a night of readings kept on the device; a music sampler, where the best four bars are found and
looped; a translation tool, where one voice branches into every language.

## How it's built

1. **One SVG stage.** No canvas and no WebGL. The stage holds a camera group (one translate and scale) with the world
   inside it, and a screen layer above it for the labels, the spoken line and the title. One GSAP tween drives the clock
   and calls `paint(t)`, a pure function of time, so any frame can be seeked in any order.
2. **A voice is a ribbon.** `ribbonD` walks a centreline, goes out along the top at each point's half-width and back
   along the bottom: one filled path. The half-width is the loudness at that point, with a little per-sample variation
   so it reads as a waveform.
3. **A take that writes itself.** Ninety seconds of loudness, 1,800 samples, are cut into ninety one-second chunks, each
   its own path. A clip rectangle that follows the record head reveals them, and the chunks near the head are ember.
4. **The strongest ten seconds.** The bake finds the ten-second window with the highest mean loudness and snaps it to
   whole seconds. Outside it, each chunk drains to grey and rotates, shrinks and falls about its own centre.
5. **Letters into sound.** The bake sets the spoken line in Archivo with fontTools and writes every letter's outline and
   its outer contour. In the film each contour is resampled to 96 points, aligned with its slice of the voice ribbon and
   interpolated, starting as its word is spoken.
6. **Branching.** The pages are sorted by angle around the first page, split into three, then four, then their leaves.
   Each branch is a curve drawn on by its dash offset, and each page pops in as its branch lands.
7. **A vertical cut.** The 9:16 version is the same take: the bake sets the line in four rows and the wall eight pages
   wide, and the camera reframes each scene.

## Gotchas worth knowing

- Under a zooming camera, set each hairline's stroke-width to its screen width divided by the zoom every frame, so lines
  keep their weight while dash-based draw-ons stay in the same units.
- Letters with holes (a, e, o) cannot morph cleanly as a whole: morph only the outer contour and hide the full glyph the
  moment the melt starts.
- fontTools writes H and V commands with no separators, so do not split a glyph by parsing its path string: record it
  with a RecordingPen and split at each moveTo.
- Snap the strongest window to whole seconds, so its edges are chunk edges; otherwise a chunk straddles the window and
  half of the voice you kept peels away.
- Brand rules hold in motion: the mark is never redrawn or recoloured, it arrives as the official lockup, flat, and ember
  appears only on sound that is playing.
