# R57 · Impression

**Style:** a pin screen that remembers: 11,520 steel pins drawn as real shafts and domed heads behind clear acrylic, with real shadows. The problem is pressed in and the pins keep its shape; each path is pressed into that impression, and the pins that don't fit glow amber.
Every pin is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Problem-to-Solution Assessment, a service: it maps one workflow as it runs now, compares up to three paths against official sources and recommends one, with a 30-day test, an owner and one measure of success, in a decision brief within five business days, with no code written and nothing connected.
**Length:** 40 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 40-second 1920x1080 film in HyperFrames for AI Problem-to-Solution Assessment, a service that takes one business workflow, maps how it runs now, compares up to three paths (a ready-made tool, a connected workflow, a simpler process change) against official sources, and recommends one, with a 30-day test, an owner and one measure of success, in a decision brief within five business days, with no code written and nothing connected. Make it a pin screen in code, the toy that remembers: a frame of steel pins behind clear acrylic, seen side on so you see every shaft.
Lay out 144 by 80 pins and draw each one as real geometry, instanced in WebGL2: a steel shaft and a domed head, lit by one warm key with a shadow map and a cool rim, behind two clear acrylic faces, in a frame in a stand on a desk. Work out every pin from the time alone: the events in one table run in order on every pin, each with a weight that rises once and then stays. "Back" pushes pins out to a shape from behind and they stay; "front" presses a mould onto the heads and nothing can stay further out than it allows; "tilt" and "flat" send every pin home. Where a mould shoves a pin, the distance turns amber; where it rests on a pin, the pin glows cool blue. One table holds every shape, event, camera key and caption, and drives both the film and the score, at 96 bpm. A "AI PROBLEM-TO-SOLUTION ASSESSMENT · DEMO WORKFLOW" label stays on screen. The score is composed in code from metal: a pin moving is a tick, a misfit scrapes, a fit is one soft note.
One problem: the lamp comes on over a flat frame, and one workflow pushes in from behind and withdraws: five steps, burrs on the handoffs, a ring where work waits and a loop where it's redone. The pins keep it. "ONE PROBLEM." "TAKEN AS IT IS."
The map: the camera moves along the impression and small labels follow their pins: STEPS, HANDOFFS, DELAYS, REWORK. "MAPPED BEFORE ANYTHING IS BOUGHT."
Up to three paths: "A READY-MADE TOOL · A CONNECTED WORKFLOW · A SIMPLER PROCESS", named once, together. Three frosted moulds press onto the front in turn while a panel ticks off price, setup, integrations, privacy, maintenance and reversibility and counts the pins each one moved. The first shoves 1,103 pins amber, the second 303. "WHERE IT DOESN'T FIT, THE PINS MOVE." "CHECKED, NOT GUESSED."
One recommendation: the third fits flush. No pin moves and the whole workflow glows blue. Never say which kind of path it is. "ONE RECOMMENDATION." "EVEN IF IT'S NO CHANGE."
The reset: the frame tips back and every pin slides home in one wave from the top, with a cascade of ticks.
The test: a calendar of thirty days presses up, one day after another, then a head and shoulders for the owner and a target for the measure. "A 30-DAY TEST." "AN OWNER. ONE MEASURE OF SUCCESS."
The brief: a palm presses the frame flat, and the decision brief presses up with a tick. "THE DECISION BRIEF." "WITHIN FIVE BUSINESS DAYS." "NO CODE WRITTEN. NOTHING CONNECTED." The lamp goes off.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Problem-to-Solution Assessment", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The workflow and the paths are demos, and the paths are shapes with no names. Claim no prices, no savings and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made of a pin screen in code: steel pins drawn as real shafts and heads behind clear acrylic, with real shadows. Work out every pin from the time alone, running the events in order so the pins remember. Press {the_problem} in from behind and let the pins keep it, then press {your_options} onto the front one by one: the pins each one shoves glow amber and the pins it fits glow blue, until {the_one_that_fits} sits flush. Tilt the frame so every pin slides home, press up {your_message}, and end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code from metal.
```

Ideas:

- A fitting room: a body's shape pressed in, then three cuts of a jacket pressed onto it, and only the one that fits leaves no amber.
- A product launch: last year's product pressed in, the new one pressed over it, and the amber is everything that changed.
- A key and a lock: the lock's shape in the pins, three keys tried, one turns.
- A team portrait: everyone's hand pressed in one after another, and the frame tilted clean at the end.

## How it's built

1. **One problem.** One workflow pushes in from behind and withdraws, and the pins keep its exact shape, snags and all.
2. **The map.** The camera moves along the impression while labels name the steps, the handoffs, the delays and the rework.
3. **Three paths.** Three moulds press onto the front in turn; the pins each one shoves glow amber and a panel ticks off the checks.
4. **It fits.** The third fits flush: no pin moves, and the whole workflow glows blue.
5. **The reset.** The frame tips back and every pin slides home in one wave, top row first.
6. **The test.** Thirty days press up one by one, then an owner and a target.
7. **The brief.** The frame is pressed flat and the decision brief presses up out of the metal.

## Gotchas worth knowing

- Seen straight on, raised pins look the same as flat ones. Film from an angle and light pins further out a little brighter, so depth reads.
- Thousands of shafts side on can turn into a grey mesh. Keep the pins few enough and big enough for each head to catch the key.
- Pins that remember can't be simulated frame by frame if any frame must render on its own. Run every event in order on every pin from the time alone instead.
- Drawing 4x antialiased WebGL2 into a page canvas can fail silently with a black stage. Make the blit's formats match: an alpha canvas, not premultiplied.
- Frosted moulds drawn with ordinary blending lower the canvas alpha and vanish in the render. Keep the destination alpha when blending.
- The portrait cut can't be a crop: stand the frame upright so the workflow runs top to bottom, break the captions onto two lines and move the check panel under the frame.
