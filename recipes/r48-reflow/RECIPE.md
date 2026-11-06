# R48 · Reflow

**Style:** stop-motion clay made entirely in code. One hand-written WebGL2 raymarcher, posed at 12 poses a second over a 30 fps render, with one page held in three
layouts, so the same nav, hero and cards physically travel between desktop, tablet and phone. Flat labels and the mark sit on a 2D layer above.
**Made for:** AI-Powered Web Design, a service: the client brings the brand and gets a finished, hand-coded, responsive website, built with AI assistance.
**Length:** 32.14 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32.14-second 1920x1080 film in HyperFrames for AI-Powered Web Design, a service where the client brings the brand and gets a finished, hand-coded,
responsive website, built with AI assistance. Make it dynamic motion design, a showreel piece. It's stop-motion clay made entirely in code: one hand-written WebGL2
raymarcher with smooth-blended signed distance fields, thumbprints and tool marks pressed into the surface, posed at 12 poses a second over a 30 fps render with tiny per-pose
jitter and flicker. Low, warm evening light with long shadows. 112 bpm, 60 beats. Tomato, cobalt, butter and bone clay on dusky lilac, with Archivo at 900 extruded as clay and
near-black #120C1E for the end card. The showpiece is one page in three layouts, desktop, tablet and phone, held in one table, each part arriving a moment after the last. The site says only
YOUR BRAND, and a "AI-POWERED WEB DESIGN · DEMO SITE" label stays on screen. One Python table holds the beat grid and every event, and the film and score both read it. The score is composed in code in F major: pizzicato,
tuba, claps, a slide whistle that climbs as the page narrows, and a wet squelch on each column change.
The brand: three lumps of tomato, cobalt and butter land one by one. "YOU BRING THE BRAND."
Not a template: the backdrop drains to grey. A plum mould stamps out nine identical grey sites along a rail, then one lump lands on the end and they fall like dominoes, each one resting on the next until it moves. "NOT A TEMPLATE."
Wireframes: the row melts into a blank slab, and grey coils draw a nav, a hero with a crossed box and three cards. "WIREFRAMES FIRST."
The colour: clay blobs land and flood each part with colour from the point they hit, and the backdrop returns to lilac. "HAND-CODED, WITH AI ASSISTANCE."
The squeeze: "DESKTOP." One held breath. Two huge tomato walls slam in, the camera shakes, the page buckles and bulges, and the cards travel from three columns to two and a wide one. "TABLET." on the left wall. They slam again, down to one column as tall as a phone. "MOBILE." The walls fly off, and the page springs back with a wobble.
The real thing: a clay cursor presses a clay button, which squashes, and a ripple runs through the page. "REVIEW THE REAL SITE, NOT A MOCK-UP."
The plumbing: the slab turns round against dark blue. Bulging pipes run to plates labelled SCHEMA, SITEMAP and META. "THE SEO PLUMBING IS INCLUDED."
Yours: the site shrinks into a butter folder and the flap shuts on it. "EVERY FILE IS YOURS." The folder slides towards the camera until its thumbprints fill the frame.
Close: the logo lands flat on dark, never redrawn or recoloured, with "AI-Powered Web Design", the URL and "A SERVICE · THE SITE HERE IS A DEMO".
Take facts only from the service page. "Hand-coded" always comes with "with AI assistance". Claim no speed, no prices, no scores and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose story is {the_story}, as stop-motion clay made entirely in code. Use one hand-written
WebGL2 raymarcher, with thumbprints pressed into the surface, posed at 12 poses a second, under one low warm light, in {your_palette}. Build {the_rigid_thing_you_sell} out of soft clay, and
keep {its_two_or_three_states} in one table so each part travels between them a moment after the last. Hold one breath, then squeeze it with two huge walls, so {the_change} is something you can see happen.
Let it spring back with a wobble. Show {what_people_never_see} by turning it round. End with {your_mark}, placed flat, with {line} and {url}, at {bpm} bpm with a bouncy score composed in code.
```

Ideas:

- A packaging designer: one clay box squeezed from a shelf carton to a travel size, with its panels moving as it shrinks.
- A font foundry: one clay word squeezed through its widths, from extended to condensed, between two walls.
- A slide template: a clay deck going from widescreen to a phone story, with its titles and images finding new places.
- A newsletter builder: one clay email squeezed from desktop to phone, with its columns dropping into a stack.

## How it's built

1. **Three lumps.** Tomato, cobalt and butter land one at a time with a heavy squash. They are the whole palette of the film, and everything after is made of them.
2. **The same site, nine times.** One mould stamps a row of identical grey sites, and the backdrop has lost its colour too, so the template looks as dull as the point it makes.
3. **Dominoes that lean.** One lump hits the end. Each site falls until it touches the next, and rests on it until that one moves, which is what stops them passing through each other.
4. **Coils draw the page.** Grey coils draw each box around its own centre, with a crossed box for the hero, so wireframing reads to anyone. Each coil tapers off at the point it has reached.
5. **Colour from a point.** A blob lands on each part and the colour spreads out from where it hit, while the blob sinks in and the tube swells into a solid shape.
6. **The squeeze.** After one held breath, the walls slam in, the camera shakes and the page buckles. Its parts arrive a moment apart, and the moving cards lift towards the camera so they pass over each other.
7. **A press that travels.** The cursor presses the button, the button squashes, and a ring of displacement runs out through the whole page, because it's all one piece of clay.
8. **Round the back.** The slab turns and the pipes grow on the back, with a bulge running along them, so the part no client sees gets the most playful shot in the film.

## Gotchas worth knowing

- A word on a wall stays behind when the wall leaves. Tie its position to the wall, or take it away first.
- Words that overshoot on the way in can hit the line above them. Cap the overshoot, not the move.
- Anything that displaces the surface makes the distance field lie. Reduce the step in proportion to how far you are bending, or you'll get holes.
- A melt between two scenes can leave the frame empty in the middle. Keep it short, and check the middle of each one by time.
- A portrait frame can't hold a wide layout up close. Pull right back for desktop and push in as the page narrows, and the format starts to help you.
