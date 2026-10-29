# R14 · Orrery

![A brass-and-glass orrery in the dark: a glowing sun, gold rings and glass planets in teal, amber and violet.](poster.jpg)

## Purpose

A multi-agent system as a brass-and-glass orrery. The orchestrator is the sun; each agent is a glass planet on its own
gimballed ring, with a moon for its memory and small satellites for its skills. A typed brief becomes a comet that
strikes the sun, the agents research, write and review (one piece goes back, one goes to a person), then every ring
snaps into one plane and the result fires out as a beam that becomes the word "agents".
Made for AI Agent Architecture, a service of JQ AI SYSTEMS.

**Watch it:** [visions.joaoqueiros.com/recipes/orrery](https://visions.joaoqueiros.com/recipes/orrery/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

32 s · 1920×1080 · 30 fps · Three.js (WebGPU renderer on WebGL2), GSAP · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

## Editable elements

1. The agents are the `AG` list in `index.html`: name, ring radius, speed, tilt and colour. Add a planet or rename them.
2. The story's timing is the table `T` at the top of `index.html`; `score/compose.py` mirrors it, so change both.
3. The brief, the station titles, the review tiles (`PH`) and the end card are plain text in `index.html`.
4. To change the final word, edit `WORD` in `bake/word.py` and run it (needs `pip install fonttools brotli`).
5. Rebuild the score (needs `pip install numpy`):

        python score/compose.py

## Source files

- `index.html`: the whole film. `pose(t)` sets every ring's angle from the clock; one painter draws the rest.
- `bake/word.py`: the word's outlines, from the film's own font. Writes `assets/word.js`.
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
