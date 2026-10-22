# R04 · One Hundred Marks, One Line

**Style:** one line that never lifts off the page. It closes into the outline of one shape, then flows straight
into the next, a hundred times, faster and faster, and finally settles on one.
**Made for:** Marks, the 160-page book of 398 logo identities by João Queirós (joaoqueiros.com/marks).
**Length:** 26 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · HTML · SVG · GSAP (one clock) · Python (tracing and score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for Marks, my book of 398 logo identities.
Story: a warm paper page. A pen draws one straight line, and the line closes into the outline of the Digitalift
bird. Then it flows, without ever lifting, through the outlines of 100 marks from the book, in book order: three
a second at first, a blur of about twenty a second near the end, then slow again. A small caption in the book's index style names each mark
it lands on ("033 · Rancho Monte Alegre · Symbol · page 20") and a counter reads "007 / 100". The last mark
opens into the outer stroke of my JQ mark, the line turns teal as it lands, and the real mark fills in. End on
"Marks", "398 identities · 160 pages · one book" and joaoqueiros.com/marks.
Outlines: only marks already public on the Marks page, never Veriti. Trace each image with numpy and Pillow:
threshold the ink, close small gaps, keep the biggest blob that isn't a line of text, fill its holes, trace its
outer edge, smooth it and resample it to the same number of points.
Technique: one SVG path. Every outline has the same number of points; roll each one so its first point sits
where the previous one's does, so morphs never twist. One painter computes every frame from time.
Look: #F7F5F0 paper, #151515 ink, grey captions, Manrope for captions, Instrument Serif for "Marks".
Score: compose it in code with numpy: a pencil scratch that follows the line's speed, one soft piano note per
mark climbing as the pace quickens, slow pads, a G major landing and bells for the lockup.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames.
On {surface}, a pen draws one line that closes into {first_shape}.
Without lifting, it flows through the outlines of {n} {shapes}, slow, then fast, then slow,
with a caption naming each one: "{caption_format}".
The last one opens into {final_shape}, which fills in as {final_fill}. Close on {final_line}.
One SVG path, every outline resampled to the same point count and rolled to match the previous one.
Palette: {palette}. Fonts: {fonts}. Score composed in code: {score_idea}, synced to the line's speed.
```

Ideas: every icon in a design system flowing into the app's logo, a country's regions drawn as one line ending
on the map, a product range (bottles, chairs, shoes) as silhouettes, a typeface's letters from A to Z.

## How it's built

1. **Trace, don't redraw.** Each image is thresholded, its gaps are closed, and the biggest blob that isn't a
   line of text is kept. Holes are filled and its outer edge is traced into one contour: a silhouette, not the
   detailed drawing. Plain circles and badges were left out because they all look alike.
2. **The same number of points.** Every contour is smoothed and resampled to 400 points by arc length, clockwise,
   centred and scaled to the same size. Now any shape can blend into any other, point by point.
3. **Roll to match.** Before the film starts, each outline is rotated (its points, not the shape) so its first
   point sits nearest the previous outline's. Without that, a morph turns inside out halfway.
4. **One path, one painter.** The film is a single SVG path whose `d` is rewritten every frame from time: which
   two outlines, how far between them. The tempo curve gives 99 steps of different lengths, each one moving for
   72% of its time and resting for the rest.
5. **Land on the real mark.** The last outline is the JQ mark's outer path, traced from its own SVG at the exact
   size it will appear, so the line lands on the logo and the logo fades in under it.
6. **Sound from the same clock.** The pencil's loudness and brightness follow the line's speed. Each landing gets
   one piano note, higher as the pace quickens and softer as it gets denser, so the fast run becomes a shimmer.

## Gotchas worth knowing

- Logos are their owners' trademarks. The source on GitHub ships the tracer, twelve demo shapes and the film; the
  100 client outlines stay out. Trace your own images with the tools in the folder.
- An out-and-back loop draws as a line: make the opening line a closed loop with the same point count as every
  outline, and the first morph is just another morph.
- Threshold on the darkest channel (255 minus min of R, G and B), not on brightness, or pale coloured logos vanish.
