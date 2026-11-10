# R55 · Overview

**Style:** a field of 61,440 steel pins in code, in 3D, with a camera in flight. Every pixel is a ray walked through the grid of pins to the first domed head or shaft, then back towards a low lamp for its shadow.
Every pin's height, and whether it's steel or brass, is worked out from the time alone. No footage and no 3D engine.
**Made for:** AI Research & Briefing Systems, a service: it watches the sources that matter, reads a knowledge document of the client's field first, and writes up what changed, and why, in the client's format and voice, daily or weekly, where the client keeps the code, the prompts and the knowledge document.
**Length:** 36 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table and score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 36-second 1920x1080 film in HyperFrames for AI Research & Briefing Systems, a service that watches the sources that matter, filters out the noise and writes up what changed, and why, in the client's format and voice. Make it a field of steel pins in code, in 3D, with a camera in flight over it: from the ground the sources are noise, from above they're a briefing.
Lay out a field of 192 by 320 pins. Every frame, work out each pin's height and whether it's steel or brass from the time alone, and upload them as one small texture. Draw every picture once as a relief on a canvas, four samples to a pin, and let the pins follow it in from one side, from the middle or scattered. One WebGL2 shader traces a ray per pixel through the grid, cell by cell, to the first domed head or shaft, traces a second ray back towards a low lamp for a soft shadow, and shades steel and brass reflecting a dark room; keep the shafts in shade so raised words read by their tops. A second pass adds depth of field. Clear the noise a few pins around every word so it always reads. One table holds every word, source, ripple, light and camera key, framed on what it looks at, and drives both the film and the score, at 112 bpm. A "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING" label stays on screen. The score is composed in code from metal: pins rising are ticks, the flight runs on a pulse like a press, and every word that lands slams.
Ground level: black, then the lamp comes on over the pins at head height and the camera lifts off to "YOUR SOURCES."
The flight: it flies over "NEWS." "SITES." "FEEDS." "COMPETITORS.", each word rising just ahead of it on the beat with a ripple through the field, and the sources (a page, a feed, a site, a magnifier and a chart, all plain shapes) rising alongside.
Down here: it drops into the noise while the sources slam up all around. "FROM DOWN HERE," "IT'S ALL NOISE."
From above: a crane straight up to a bird's-eye view while the noise settles from the middle out. "FROM ABOVE," Then the knowledge document rises. "BRIEFED ON YOUR FIELD."
The filter: the sources pop up around it, everything that doesn't matter drops, and the page, the magnifier and the chart turn brass and slide into a column. "ONLY WHAT MATTERS." "WHAT CHANGED, AND WHY."
Written up: a dive down to a low angle. "IN YOUR FORMAT." The briefing rises line by line next to its brass bullets, and the camera pulls back to read it whole. "IN YOUR VOICE."
On schedule: a grid of days. Daily, the briefing rises on every day in turn; weekly, once, taller and in brass. "DAILY OR WEEKLY." "ON YOUR RHYTHM."
Yours: a brass folder. "THE CODE. THE PROMPTS." "THE KNOWLEDGE DOCUMENT. YOURS." The camera pulls all the way out to the whole field and the lamp goes off.
Close: the logo placed flat, never redrawn or recoloured, on dark with "AI Research & Briefing Systems", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. The sources, the field and the briefing are demos, and the sources are shapes with no names. Name no weekday or time for the schedule. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, made of a field of steel pins in code with a camera in flight over it. Work out every pin's height from the time alone, and trace a ray per pixel through the grid to the first pin head, with a soft shadow back towards a low lamp. Raise {your_words} out of the field just ahead of the camera, each on a downbeat with a ripple, then drop into {what_the_noise_is} and crane up to a bird's-eye view where {what_gets_clear}. Turn {what_matters} brass. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm, with a score composed in code from metal.
```

Ideas:

- A product launch: the camera flies over the features as they rise, and cranes up to the product's name in brass.
- A conference opener: the speakers' names rise out of the field one by one, and the pull-out shows the whole programme.
- A city map: streets rise as pins, the camera skims them at street level, then cranes up to show the route.
- A data story: noisy charts rise all around, and from above only the one that matters stays standing.

## How it's built

1. **Ground level.** The lamp comes on over the pins at head height, and the camera lifts off to the first words.
2. **The flight.** The camera flies over the words as they rise just ahead of it on the beat, each with a ripple through the field, the sources rising alongside.
3. **Down here.** It drops into the noise while the sources slam up all around, and the words still read because the noise clears around them.
4. **From above.** A crane straight up to a bird's-eye view while the noise settles from the middle out, and the knowledge document rises.
5. **The filter.** Everything that doesn't matter drops, and the page, the magnifier and the chart turn brass and slide into a column.
6. **Written up.** A dive down to a low angle, and the briefing rises line by line next to its brass bullets before the camera pulls back to read it whole.
7. **On schedule and yours.** The briefing rises on a grid of days, a brass folder rises, and the camera pulls all the way out to the whole field as the lamp goes off.

## Gotchas worth knowing

- A raised word seen at an angle reads double: its lit tops and its sides. Keep the shafts in deep shade so the word reads by its tops alone.
- Words drown in the noise from a low camera. Hold the noise down a few pins around every word, not just under it, so each one stands clean.
- A ray walking a grid at a grazing angle can take hundreds of steps. Start it where it enters the tallest pin height, stop it where it meets the floor, and skip any cell the ray passes above.
- Framing a moving camera by hand is guesswork. Work each key out from what it frames: the words, how wide they are and the angle, then check where they land on screen before rendering.
- The portrait cut can't be a crop: the camera frames by width, so long lines push it far away. Break the captions onto two lines, restack the briefing, and lengthen the field so the camera never sees past its edge.
