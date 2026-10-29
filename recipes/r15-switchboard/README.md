# R15 · Switchboard

![A walnut and brass telephone switchboard woven with cloth patch cables, every lamp glowing green.](poster.jpg)

## Purpose

Workflow integration as a 1940s telephone switchboard rebuilt as a luxury object: smoked walnut, brass jacks, cloth
patch cables and warm lamps. Requests arrive as lamps; cables lift off the shelf, arc through the air and click into
the right team, light runs down the wire and a card says what happened. An AI decision layer reads each one and sends
the urgent one straight to a person. Then every line goes busy, the lamps turn green, and a neon sign lights
"connected".
Made for AI Workflow Integration, a service of JQ AI SYSTEMS.

**Watch it:** [visions.joaoqueiros.com/recipes/switchboard](https://visions.joaoqueiros.com/recipes/switchboard/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

32 s · 1920×1080 · 30 fps · Three.js (WebGPU renderer on WebGL2), GSAP · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

## Editable elements

1. The jacks are `ROWS` in `index.html`: four rows of six labels, your tools on top and your teams below. Rename them.
2. Every patch is one row of `PATCHES`: from, to, start time, speed and the card it shows. Add, remove or retime them.
   `score/compose.py` mirrors the table, so change both.
3. The station titles, the HUD lines (`STATE`) and the end card are plain text in `index.html`.
4. To change the neon word, edit `WORD` in `bake/word.py` and run it (needs `pip install fonttools brotli`).
5. Rebuild the score (needs `pip install numpy`):

        python score/compose.py

## Source files

- `index.html`: the whole film. `renderAt(t)` poses every plug, cable, lamp and card from the clock; one painter draws
  the type.
- `bake/word.py`: the neon word's outlines, from the film's own font. Writes `assets/word.js`.
- `score/compose.py`: the score, timed to the same table.
- `CONCEPT.md`: the concept card for this recipe.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- Three.js, `BloomNode.js` and `RoomEnvironment.js` (`assets/vendor/`): MIT, © three.js authors.
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Inter, Libre Baskerville and JetBrains Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the names JQ AI SYSTEMS and João Queirós, and the service name, line and URL on the end card.
  Replace them with your own before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
