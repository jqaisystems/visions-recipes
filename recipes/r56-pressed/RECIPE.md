# R56 · Pressed

**Style:** a pin screen in code: a wall of 36,864 steel pins under one low raking lamp. Every picture, every word and the briefing is a relief pressed into the wall from behind, and nothing is drawn on top.
Every pin's height is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Research & Briefing Systems, a service: it watches the sources that matter, reads a knowledge document of the client's field first, and writes up what changed, and why, in the client's format and voice, daily or weekly, where the client keeps the code, the prompts and the knowledge document.
**Length:** 38 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 38-second 1920x1080 film in HyperFrames for AI Research & Briefing Systems, a service that watches the sources that matter, filters out the noise and writes up what changed, and why, in the client's format and voice. Make it a pin screen in code: a wall of steel pins under one low raking lamp, where every picture, every word and the briefing is a relief pressed into the wall from behind. Nothing is drawn on top.
Lay out a wall of 256 by 144 pins. Every frame, work out each pin's height from the time alone and upload the heights as one small texture. Draw every picture once as a relief on a canvas, four samples to a pin, and let the pins follow it in from one side, from the middle or scattered. One WebGL2 shader finds the frontmost pin at each pixel, its shaft and domed head, in a slight perspective, then traces back towards the lamp through the pins in between for a soft shadow, so raised pins catch the light and the reliefs read by light, not by outline. One table holds every relief, the noise, the wave, the light and the captions, and drives both the film and the score, at 100 bpm. A "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING" label stays on screen. The score is composed in code from metal: pins sliding are a wash of tiny ticks, the noise is a clatter, and the briefing is a tune on struck metal.
The wall: black, then the lamp comes on across a flat wall and a ripple runs through it like a breath. "YOUR SOURCES."
Pressed in: a page, a feed, a site, a magnifier and a chart, all plain shapes, push in from behind one after another, then more all at once, until every pin jitters at its own height. "NEWS. SITES." "FEEDS. COMPETITORS."
What you know: one structured page is pressed in softly underneath everything and stays. "BRIEFED ON YOUR FIELD." "IT READS THIS FIRST."
The filter: one wave rolls across the wall and flattens the noise behind it, and the page, the magnifier and the chart slide and shrink into a column. "ONLY WHAT MATTERS." "WHAT CHANGED, AND WHY."
Written up: they become the bullets of a short briefing pushed up out of the wall line by line, and the lamp swings across it once. "IN YOUR FORMAT." "IN YOUR VOICE."
On schedule: two weeks of days. Daily, the briefing presses up on every day in turn; weekly, on one day only. "DAILY OR WEEKLY." "ON YOUR RHYTHM."
Yours: a folder presses up. "THE CODE. THE PROMPTS." "THE KNOWLEDGE DOCUMENT. YOURS." The lamp slides off the wall.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Research & Briefing Systems", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The sources, the field and the briefing are demos, and the sources are shapes with no names. Name no weekday or time for the schedule. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made of a wall of steel pins in code under one low raking lamp. Work out every pin's height from the time alone, and draw each pixel as the frontmost pin there, with its shadow traced back towards the lamp. Press {your_sources} into the wall from behind until it's noise, then roll one wave across that flattens everything but {what_matters}, and press up {your_message} line by line. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code from metal.
```

Ideas:

- A product launch: every feature presses up out of the wall in turn, and the wave leaves only the product's name.
- A portrait: a face pressed in from behind, with the lamp swinging round so it seems to turn.
- A city's skyline as reliefs, pressed in building by building as the lamp goes from dawn to dusk.
- A countdown: each number pressed up on the beat, and the last one swept flat by the wave.

## How it's built

1. **The wall.** The lamp comes on across a flat wall of pins, and a ripple runs through it like a breath.
2. **Pressed in.** The sources push in from behind one after another, then more all at once, until every pin jitters at its own height.
3. **What you know.** One structured page is pressed in softly underneath the noise and stays.
4. **The filter.** One wave rolls across the wall and flattens everything that doesn't matter; the page, the magnifier and the chart slide and shrink into a column.
5. **Written up.** They become the bullets of a short briefing pushed up out of the wall line by line, and the lamp swings across it once.
6. **On schedule.** Two weeks of days: daily, the briefing presses up on every day in turn; weekly, on one day only.
7. **Yours.** A folder presses up, and the lamp slides off the wall.

## Gotchas worth knowing

- Thousands of pins at 1080p can read as a grey dot pattern. Keep each pin big enough for its head to catch a highlight, and let raised pins catch more of the lamp, so a relief reads by light, not by outline.
- Drawing every pin as geometry is slow. Draw one full-screen pass instead: each pixel checks only the few pins that could cover it, looking back along the way they lean.
- Pins that sample a sliding, shrinking relief at their own position pop and tear. Sample the relief where each pin came from, between its four neighbours, instead.
- Text pressed into noise disappears. Hold the noise down in the band where the captions sit, so each word rises clean.
- The portrait cut can't be a crop: turn the wall upright, break the captions onto two lines, restack the briefing and set the days as two columns.
