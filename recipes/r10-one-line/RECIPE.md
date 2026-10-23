# R10 · One Line

**Style:** one glowing line never leaves the screen and the film never cuts. A single camera rides the head of
the line as it turns into an easing curve, a baseline for type, a chart, a product screen, an editing timeline,
a waveform and three formats, then a hard pull-back shows the whole journey was one stroke, and the line signs
off as a mark.
**Made for:** Product Films, the video service of JQ AI SYSTEMS. It's the film on the service page.
**Length:** 40 s · 1920×1080 · 30 fps · one take, no cuts · score composed in code.
**Stack:** HyperFrames · HTML · SVG · GSAP (one clock and its eases) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 40-second 1920x1080 film in HyperFrames for Product Films, my service that makes product films in code.
It's my showreel, so make it impress. One teal #00BFB4 line never leaves the screen and the film never cuts:
one camera rides the glowing head of the line across a wide world on #111110.
Stations, each on the beat of a 120 BPM score: the line draws an expo.out easing curve on a small graph and
"One line." rises beside it; it becomes the baseline that "Every frame starts as a line." rises from, letter by
letter as the head passes; it climbs a staircase of five bars while a counter runs to "1,200+ brands designed";
it outlines a product card that renders itself (EN to PT under a scan line, the price rolls from 29 to 19 €/mo,
the line fills the Render button); it stretches into an editing timeline as the playhead, cutting six clips a
second apart; it vibrates into a waveform; it traces three formats, 16:9, 9:16 and 1:1, which fill in as each
closes. Then the camera pulls all the way back to show the whole journey was one line ("One line. Forty seconds.
All code."), and the line signs off by drawing the JQ mark as one stroke, which fills. End on "Product Films",
"by João Queirós, designer who builds systems", the three tiers, "First 3 Showreels €900" and
ai.joaoqueiros.com/services/product-films. A small minimap in the corner traces the line all the way.
Libre Baskerville for display, Inter for UI, JetBrains Mono for labels and timecode.
Technique: one painter computes every frame from time; SVG paths drawn with dash offsets; the head follows
getPointAtLength; the camera is a list of keyframes with zoom interpolated in log space.
Score: compose it in code with numpy, 120 BPM in A minor, one progression under the whole take, a hit on every
station, and every sound ending in a release.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}. One {colour} line never leaves the
screen and the film never cuts: a camera rides the line's glowing head across a wide world on {background}.
Stations, each on the beat: {station_1}, {station_2}, {station_3}, {station_4}, {station_5}.
Things react to the head, not the clock: {reaction}.
Then the camera pulls all the way back to show the whole journey was one line, and the line draws {mark} as
one stroke. End on {title}, {tagline} and {url}.
SVG paths drawn with dash offsets, camera keyframes with zoom in log space, a minimap tracing the line.
Score composed in code at {bpm} BPM: {score_idea}, a hit on every station.
```

Ideas: a recipe where the line becomes each utensil and ingredient; a startup's year as one line through its
milestones; a city tour where the line is the route; a résumé where the line draws each job.

## How it's built

1. **One world, one camera.** Every station sits on a single world about 11,000 by 3,400 px. The camera is a
   list of keyframes (time, x, y, zoom, ease). Zoom is interpolated in log space, so the pull-back from 1 to
   0.17 moves at an even pace.
2. **The line is a set of paths.** Each station's path has its own start, end and ease, and is revealed with a
   dash offset. The head is whichever path is drawing, read with `getPointAtLength`, so the glow, the ring and
   the playhead all sit exactly on the line.
3. **React to the head, not the clock.** Letters rise as the head passes their x, chart bars grow when the head
   reaches them, keyframes pop under the playhead, the waveform lights behind it.
4. **A product card that renders.** The line draws the card's outline, then a scan line swaps the copy from EN
   to PT, the price digits roll on the beat and the line itself fills the Render button.
5. **A real edit.** The timeline's playhead is the head of the line; six clips cut a second apart in the
   preview, the timecode counts, and the clip names update on each cut.
6. **The pull-back.** The camera zooms out to show every station on one line, while the minimap in the corner
   has traced the same paths all along.
7. **Signing the mark.** The JQ mark's four outlines and three short hops are drawn as one stroke in the mark's
   own coordinates, then the hops fade and the filled mark takes over.

## Gotchas worth knowing

- Divide the stroke width by the zoom, with a floor, or the line disappears in the pull-back.
- Interpolate zoom in log space. A linear zoom from 1 to 0.17 rushes at the start and crawls at the end.
- Videos inside a scaled world still need their own `data-start` and `data-media-start`, and stay muted: the
  framework seeks them, the score carries the sound.
- In the score, give every synthesised sound a release and let risers fall away; a sound that stops dead reads
  as a glitch.

## Your clips

`assets/clips/clip-1.mp4` to `clip-6.mp4` are placeholders made with ffmpeg (a colour card with a moving bar).
Drop your own films in with the same names, at least 14 s long, and rename the six labels in `CLIPS` in
`index.html`.
