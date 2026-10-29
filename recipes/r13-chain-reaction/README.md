# R13 · Chain Reaction

![A chrome ball frozen against a brass bell, with sparks and a shockwave ring hanging in the air above a glowing teal track.](poster.jpg)

## Purpose

One command drops a chrome ball into a machine built from a weekly report. It collects the inbox, knocks messy
spreadsheet rows clean, sorts them through a glass peg board, waits for a person to approve, and rings a brass bell
as the report goes out. The physics is real and baked once, so the film can bend time: slow motion through the
dominoes, and bullet time at the bell while the camera orbits the strike. Then the whole run becomes one glowing
line that re-forms into the word "automation".
Made for AI Automation Systems, a service of JQ AI SYSTEMS.

**Watch it:** [visions.joaoqueiros.com/recipes/chain-reaction](https://visions.joaoqueiros.com/recipes/chain-reaction/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

34 s · 1920×1080 · 30 fps · Three.js (WebGPU renderer on WebGL2), Matter.js physics, GSAP · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

## Editable elements

1. Change the machine in `bake/bake.mjs` (the ramps, the tray, the dominoes, the peg board, the gate, the bell), then
   bake it again. The script prints where the balls are every half second, so you can see if the run gets stuck:

        cd bake && npm install && node bake.mjs

2. To change the word at the end, edit `WORD` in `bake/word.py` and run it (needs `pip install fonttools brotli`).
3. Rebuild the score from the new impacts (needs `pip install numpy`):

        python score/compose.py

4. Change the station titles, the command and the end card in `index.html`.

## Source files

- `index.html`: the whole film. One clock drives the camera, the type and the physics clock (`physAt`), which is
  what makes the slow motion and the freeze possible.
- `bake/bake.mjs`: the machine and its physics run (Matter.js). Writes `assets/bake.js` and `bake/events.json`.
- `bake/word.py`: the word's outlines, from the film's own font. Writes `assets/word.js`.
- `score/compose.py`: the score, built from `bake/events.json` with the same time remap as the picture.
- `CONCEPT.md`: the concept card for this recipe.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- Three.js, `BloomNode.js` and `RoomEnvironment.js` (`assets/vendor/`): MIT, © three.js authors.
- Matter.js (installed by `bake/package.json`): MIT, © Liam Brummitt.
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Inter, Libre Baskerville and JetBrains Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the names JQ AI SYSTEMS and João Queirós, and the service name, tagline and URL on the end card.
  Replace them with your own before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
