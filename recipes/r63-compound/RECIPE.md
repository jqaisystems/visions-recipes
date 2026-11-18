# R63 · Compound

**Style:** string art in code, the classic ring loom: a ring of 300 pins and one thread whose straight passes, each chosen to add the most light the picture still owes, slowly draw a flower, then coral, amber and teal threads bloom it in colour.
Every frame is worked out from the time alone. No footage, no images: the flower is drawn in code.
**Made for:** Pinterest Growth Automation, a service: a batch of on-brand pins is designed once and approved as a batch, then one pin is published every day without anyone touching a scheduler. Pins keep surfacing for months, so reach compounds, and everything runs on your own accounts.
**Length:** 40 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · GSAP · Python (winding, table and score) · NumPy · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 40-second 1920x1080 film in HyperFrames for Pinterest Growth Automation, a service that designs a batch of on-brand pins once, which you approve as a batch rather than post by post, then publishes one every day without anyone touching a scheduler. Pins keep surfacing for months, so reach compounds over weeks and months, and everything runs on your own accounts, so you own the system and the audience. Make it string art in code, the classic ring loom: a ring of nails and one thread, where every pass is a straight line and none means anything alone, but together they draw a picture.
Wind it in Python first. Draw a flower in code (twelve petals, a seed disc, a stem, two leaves) and split it into one brightness map per thread: bone for the whole flower, then coral, amber and teal. From the nail it is on, each thread takes the pass to another nail, never a near neighbour, that covers the most light still owed, then takes that light off. Let each pass carry little light, so the picture needs many fine passes, and charge a pass for every bit of empty board it crosses, so the colour stays on the flower.
Draw it in WebGL2: 300 pins with round heads in the brand colours on a dark wooden board, every pass an instanced ribbon at the thread's true width, faded where it is thinner than a pixel and a half and added up as light, so passes build like real thread. One low key light with a shadow map. Work out every frame from the time alone. One table holds the pins, the passes, the camera and the captions, and drives both the film and the score, at 96 bpm. A "PINTEREST GROWTH AUTOMATION · DEMO BOARD" label stays on screen. The score is composed in code, strings and wood: a tap for every pin, and a pluck for every pass, its pitch set by its length like a real string, kept in A major pentatonic.
The batch: a low camera watches the pins press into the board in a ring, a mallet on every beat. "A BATCH OF ON-BRAND PINS." "DESIGNED ONCE."
Approved: one light runs round the ring and every pin flashes as it passes. "YOU APPROVE THE BATCH," "NOT EACH POST."
Day one: from a three-quarter view of the whole ring, the thread ties on and lays one pass, a day, labelled DAY 1, then DAY 2 and DAY 3, each a single plucked note. "ONE PIN, EVERY DAY." "NOBODY TOUCHING A SCHEDULER."
It compounds: the passes speed up to hundreds a second, the plucks merge into a shimmer, the camera pulls back, and a flower comes out of nothing but straight lines. "PINS KEEP SURFACING" "FOR MONTHS." "IT COMPOUNDS."
In your brand: coral, amber and teal threads wind over it and the flower blooms in colour. "IN YOUR BRAND," "ON YOUR ACCOUNTS."
Yours: the thread ties off, and the camera glides low across the finished piece and back out. "YOU OWN THE SYSTEM." "AND THE AUDIENCE."
Close: the logo placed flat, never redrawn or recoloured, on dark with "Pinterest Growth Automation", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The board is a demo. Name no tools, figures or results, and claim no prices and no running costs.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made as string art in code: a ring of {nails} nails and one thread that winds {your_picture} out of straight lines, each pass chosen in Python to add the most light the picture still owes. Start slowly, {your_first_steps}, a pass at a time, then speed up until the picture comes out, and let {your_colours} threads bloom it, then end with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code where every pass is a pluck pitched by its length.
```

Ideas:

- A brand mark wound in its own colours, the thread speeding up as the mark comes out.
- A newsletter's hundredth issue: one pass per issue, and the hundredth draws the last line of a portrait.
- A product launch: the thread winds the product's silhouette, and the colour threads bring in its finishes.
- A habit tracker: one pass a day for a year, and the year draws the picture.

## How it's built

1. **The batch.** 300 pins press into a dark board in a ring, a mallet on every beat.
2. **Approved.** One light runs round the ring and every pin flashes as it passes.
3. **Day one.** The thread ties on and lays a pass a day, DAY 1, 2 and 3, each a single note.
4. **It compounds.** The passes speed up to hundreds a second and a flower comes out of straight lines.
5. **In your brand.** Coral, amber and teal threads wind over it and the flower blooms in colour.
6. **Yours.** The thread ties off and the camera glides low across the finished piece.
7. **The mark.** The logo, the service and the link, flat on dark.

## Gotchas worth knowing

- If each pass carries a lot of light, the picture is paid for in a couple of hundred passes and the winding stops. Let each pass carry little, so the picture needs a thousand fine ones, and draw them faint to match.
- Every pass on a ring crosses from rim to rim, so colour threads wash the whole ring. Charge a pass for every bit of empty board it crosses; too high a charge and a colour hardly winds at all.
- A thread far thinner than a pixel sparkles under multisampling. Draw it at least a pixel and a half wide and fade it by how much thinner it really is.
- Blend the thread additively, as light, and don't write it to the depth buffer, or later passes vanish behind earlier ones.
- A camera that follows the thread's tip loses the ring, since a pass crosses the whole board. Show the first days from a view of the whole ring, so each pass reads from nail to nail.
- The portrait cut can't be a crop: widen the lens until the ring fills the width, and set the captions above it.
