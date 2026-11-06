# R47 · Flywheel

**Style:** stop-motion clay made entirely in code. One hand-written WebGL2 raymarcher with smooth-blended distance fields, so any form
melts into any other without a cut, posed at 12 poses a second over a 30 fps render. Flat labels and the mark sit on a 2D layer above.
**Made for:** Pinterest Growth Automation, a service that plans a board strategy, designs a batch of pins once and posts them daily from a queue, with the client approving the batch and not each post.
**Length:** 32 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Pinterest Growth Automation, a service that plans a board strategy, designs a batch of
typically 100+ pins once, and posts them daily from a queue, with the client approving the batch and not each post. Make it dynamic motion design, a
showreel piece. It's stop-motion clay made entirely in code: one hand-written WebGL2 raymarcher with smooth-blended signed distance fields, so any form
can melt into any other without a cut. Press thumbprints and tool marks into the surface in object coordinates and shift them slightly on every pose. Pose at 12
poses a second over a 30 fps render, with tiny per-pose camera jitter and exposure flicker. One soft key light, a plain dithered shadow and a painted card backdrop. 120 bpm, 64 beats.
Terracotta, mustard, cream and a dusty teal, with plum for the stand, bone #F3EAD6 and near-black #14090C for the end card. Words are distance fields made from Archivo at 900,
extruded into clay, so they squash and melt with everything else. One Python table holds the beat grid, 108 pins and the 75 days, and the film and score both read it.
The score is composed in code in G major: marimba, woodblock, upright bass and a wet squelch on each big move. Every pin is invented, and the film carries a
"PINTEREST GROWTH AUTOMATION · DEMO DATA" label throughout.
One lump: a lump drops, settles with a heavy squash and takes a thumb dent.
The strategy: it flattens and sprouts labelled shelves on a plum base. "A STRATEGY, / THEN A BATCH."
The batch: a roller rolls out a cream sheet, then a teal cutter stamps pins row by row, one tick for each of the 108. "100+ PINS, / DESIGNED ONCE."
One stamp: one huge stamp comes down on the whole sheet and lifts. "YOU APPROVE / THE BATCH." with a flat pill, "NOT EACH POST".
The wheel: the pins fly up and load onto a heavy terracotta wheel beside an empty board.
One breath: silence for a beat and a half.
Day one: one notch, one pin on the board, "DAY 1" on a still clay dial on the axle. Then day 2, day 3, each a clean click.
The year goes by: the clicks speed up to day 75 while a clay sun crosses, a tree changes and snow falls, and the backdrop melts through the seasons. "A FLYWHEEL, / NOT A FAUCET."
It runs: the camera pushes in on the filling board, then pulls back to the wheel turning alone. "IT RUNS / WHILE YOU DON'T."
Close: the machine slumps into one lump, one last squash, the lump swells to fill the frame, and the logo lands flat on dark, never redrawn or recoloured, with "Pinterest Growth Automation", the URL and "A SERVICE · ALL PINS HERE ARE DEMO DATA".
Take facts only from the service page. Claim no views, followers, saves or sales, draw no chart going up, name no client, and use no third-party logo.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose story is {the_story}, as stop-motion clay made entirely in code. Use one
hand-written WebGL2 raymarcher with smooth-blended signed distance fields, so {your_first_form} can melt into {your_second_form} without a cut. Press thumbprints and
tool marks into the surface, and pose at 12 poses a second with tiny per-pose jitter and flicker, under one soft key light against a painted card backdrop, in {your_palette}.
Start from one lump, and make everything else from it. Build {your_words} as extruded clay from distance fields of your typeface, so they squash and melt too. Keep one table
of {your_repeating_event}, and let each one be a click and a note in the score. Hold one silent breath before the first. End with the whole thing melting back into the lump, then
{your_mark}, placed flat, with {line} and {url}, at {bpm} bpm with a plucked, wooden score composed in code.
```

Ideas:

- A savings app: coins pressed from one lump, one more on the pile each month, while the years pass behind it.
- A language app: one clay word set on a shelf every day, and each one a note, until the shelf holds a sentence.
- A weekly newsletter: one clay issue per click on a growing rack, and the seasons melting past the window.
- A toy maker's own film: one lump that becomes each toy in turn, then slumps back on the last beat.

## How it's built

1. **One lump, real weight.** The lump drops and settles with a slow, heavy squash, so it has weight before anything else happens. The thumb dent is the first sign that a hand was here.
2. **Melt, don't cut.** The lump flattens and the shelves grow out of it, because the two scenes are mixed as distance fields rather than faded. It's the one thing real clay does that nothing else can.
3. **A tick per pin.** The cutter visits each of the 108 pins in order and each visit is a tick in the score, so a batch has a sound before you've counted it.
4. **One stamp.** A stamp the size of the whole sheet comes down once and lifts. The size carries the meaning: you approve the batch, not each post.
5. **One held breath.** The picture holds and the score goes silent for a beat and a half, so the first small click lands as an event.
6. **Day one.** One notch, one pin. The count stands on a still clay dial on the axle, since nothing can be read against turning spokes.
7. **A year in the background.** The clicks speed up while a clay sun crosses, a tree turns and snow falls. The board only fills, and no chart ever goes up: it shows pins posted, not reach.
8. **Back to the lump.** The whole machine slumps into the single lump it came from, with one last squash, and the lump swells to fill the frame so the dark end card has somewhere to come from.

## Gotchas worth knowing

- Clay colours overexpose fast under one strong key. Bring the albedo down until the shadow side still has colour, or it reads as plastic.
- Soft raymarched shadows band and speckle on a bumpy surface. A plain shadow with fewer, longer steps and a dither looked better and rendered faster.
- Small falling things throw big dark blots. Let snow fall through the light without casting anything.
- A morph can pass through nothing. Two scenes that both shrink at the midpoint will leave an empty frame, and a contact sheet can miss it, so spot-check the middle of each morph by time.
- A rotation sign error looks fine until something is meant to line up. Test your rotation helper on one pin before you load a whole wheel.
