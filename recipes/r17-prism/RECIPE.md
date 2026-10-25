# R17 · Prism

**Style:** content systems as a glass prism in a black studio, filmed like a perfume commercial. Your best writing
becomes the glass, stock phrases break against it, one brief goes in as white light and comes out as a spectrum,
and every colour lands as a finished piece in its own format.
**Made for:** AI Content Systems (ai.joaoqueiros.com/services/content-systems).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL glass, bloom and a reflector floor) · GSAP · Python (table, word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Content Systems service: a glass prism in a black studio,
Three.js with bloom, real glass (transmission and dispersion), a polished floor that reflects everything (a TSL
reflector), a full spectrum, teal #00BFB4 for the HUD and the review marks.
Voice: four pages of demo writing float in the dark; their lines lift off as points of light and fly into a
triangular prism, whose edges draw in light while a flash sweeps each face as it is cut. The points stay inside the
glass. Guardrails: stock phrases ("In today's fast-paced world", "game-changer", "unlock your potential", "Let's dive
in") fly at the glass and break into shards that fall to the floor. One brief: a card reads "Our new studio opens in
Porto."; white light leaves it, enters the prism and fans out into six colours. Every format: each ray runs to its own
card and draws it on in its colour: a square post, a thread, a newsletter (the yellow ray splits into EN, PT and FR),
a blog draft, a caption and a 9:16 short. The cards are lit from behind. Review: a wide gallery; a cursor stamps
APPROVED on each card; the caption gets REWRITE, dissolves and comes back new, then is approved. A month: the cards
fly into their days on a 30-day calendar, the other days pop in, and the tiles rise into the word "everywhere", red
to violet, mirrored in the floor. End on "AI Content Systems", "On-brand, multilingual, and human-sounding at scale."
and the URL. Station titles wipe on bottom left.
Technique: one seeded table baked in Python holds every piece (format, text, position, when its ray lands, when it is
approved, its day), the pages, the phrases and the days; the film and the score both read it.
Score: compose it in code from the same table: a glass drone, pings as the lines lift, a glass ring for each cut, a
thud and falling shards for each phrase, a rush into the glass, a six-note chord that opens one note per colour, a
light pulse under the formats, a note and soft typing as each card lands, a click and two notes per approval, a
rewind for the rewrite, ticks as the month fills, one wide chord under the word.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {one_thing} becoming {many_things}, as a
glass prism in a black studio, Three.js with bloom, real glass and a reflective floor, {accent} accents.
The glass is made from {the_source}; {the_noise} breaks against it.
One brief goes in as white light: "{brief}". It splits into a spectrum, and each colour lands as {piece_1},
{piece_2}, {piece_3} (one ray splits again into {variants}). {human_moment}.
Then the pieces gather into {the_whole} and rise into the word "{word}", mirrored in the floor.
End on {title}, {line} and {url}. One baked table drives the picture and a score composed in code.
```

Ideas: one product photo becoming every ad size; one talk becoming clips, quotes and a summary; one dataset becoming
charts for every team; one song becoming every cut and format.

## How it's built

1. **One table.** `bake/pieces.py` holds the rays, the eight pieces (format, text, position, the moment its ray lands,
   the moment it is approved, its day), the pages, the phrases and the 30 days. The film reads `assets/pieces.js` and
   the score reads `bake/pieces.json`, so every note lands on what you see.
2. **Ink into glass.** The pages' ink is drawn to a canvas, about 1,400 lit pixels are sampled from it, and each one
   flies on a curve to a random point inside the prism, where it stays as the glass's inner light.
3. **Real glass.** The prism is a physical material with transmission, dispersion and clearcoat, lit by a room
   environment; its edges are thin lines that draw on, and a flash sweeps each face as it is cut.
4. **Shards.** Each phrase is one texture on a 4 by 2 jittered grid of triangles: whole while it flies, sixteen
   shards with their own velocity, spin and gravity after the hit.
5. **Light behind the cards.** Each ray is an additive cylinder that ends just behind its card, so the card hides
   the end and looks lit from the back; the card is drawn on by a wipe of its colour from the side the light enters.
6. **Month into a word.** The cards fly into their days and shrink to tiles; points sampled from the word's outlines
   then leave the tiles on arcs and land in the spectrum, red to violet, mirrored by the floor.

## Gotchas worth knowing

- A ray that ends at a card's centre runs across its face: end it just behind the card instead.
- A wipe with `step(x, u)` at `u = 0` still shows the first column of the texture: offset `x` a hair.
- A glowing interior needs restraint: too many bright points turn the prism into a white blob once bloom is on.
- Lay the pieces out as a gallery (rows by colour) so the review shot has room for the stamps and the titles.
