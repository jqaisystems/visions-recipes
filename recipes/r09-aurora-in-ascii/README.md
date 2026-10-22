# R09 · Aurora in ASCII

![The word Recipes built from text characters over an aurora drawn in green ASCII glyphs](poster.jpg)

A live 3D scene drawn only in text characters, like an old terminal screen: every cell of a grid picks a glyph
by how bright the picture is behind it, from ` .:-=+*#%@`, and takes that spot's colour. Made for the Recipes
library on visions.joaoqueiros.com: a command types itself, an aurora rises in glyphs, the cells shrink to
almost a smooth picture and grow back, and the glyphs settle into the title.

**Watch it:** [visions.joaoqueiros.com/recipes/aurora-in-ascii](https://visions.joaoqueiros.com/recipes/aurora-in-ascii/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

26 s · 1920×1080 · 30 fps · Three.js (WebGPURenderer, TSL) and one post shader · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Files

- `index.html`: the whole film. The aurora scene, the ASCII pass, the glyph atlas, the title mask and the
  terminal type all come from one painter.
- `score/compose.py`: key clicks, crackle, pad, arpeggio and the hum that follows the cell size.
- `CONCEPT.md`: the approved concept card.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- Three.js (`assets/vendor/three.*.js`): MIT, © three.js authors.
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- IBM Plex Mono and Fraunces: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the names Imagined Worlds and João Queirós. Replace the end card with your own before you
  publish a remix.
