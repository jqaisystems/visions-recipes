# R10 · One Line · concept card (approved by João 2026-10-23: back catalogue, price chip kept)

The first back-catalogue recipe. The film already exists: /code 012 `productfilms-oneline` (40 s, live since
2026-10-18, also the film on the Product Films service page). Gates 2 and 3 (look, Studio preview) were passed when
it was made, so this card covers what the recipe adds and what the open source leaves out.

**Style (reusable):** One Line. A single glowing line never leaves the screen and the film never cuts. One camera
rides the head of the line as it turns into an easing curve, a baseline for type, a chart, a product screen, an
editing timeline, a waveform and three formats, then a hard pull-back shows the whole journey was one stroke, and
the line signs off as a mark. Anyone can swap the stations, the colour and the mark.

**Why this one first:** of the three back-catalogue candidates it's the only one that can ship almost whole: its
score is composed in code (`score/compose.py`), so the music ships too, and it has no client material. It also
sells Product Films directly, and is the most ambitious motion piece on /code.

**What the open source leaves out (the same rules as R01 to R09):**
- The six /code clips in the timeline scene (`assets/clips/*.mp4`) are renders of my other films. The repo ships
  six short placeholder clips made with ffmpeg (a colour card with a moving bar and a label), and the README says
  to drop your own clips in.
- The JQ logo and mark ship with the usual "not MIT" notice, as in every recipe.
- GSAP is vendored like the other recipes, instead of loading from the CDN.

**Site:** recipe R10 on /recipes, made for "Product Films". The /code page stays film 012 with its service link,
and the recipe points to it as with R01 to R09. No new render and no change to the film.

## Open choices for João
- **The price chip.** From 36 s the film shows "First 3 Showreels €900". That offer will go stale, and a public
  recipe keeps the film around. Keep it (recommended while the offer runs, it's the live service page film too),
  or cut a version without the chip for the recipe.
- **Go ahead with R10 at all**, or skip the back catalogue for now.
