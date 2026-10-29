# R07 · Gommage

![A swirling cloud of autumn leaves in lantern colours, settling into a painting of a ship among giant flowers](poster.jpg)

## Purpose

An image doesn't cut or fade. It comes apart from one edge into thousands of small leaves, each one the colour of
the spot it left; a wind gathers them into one swirling cloud, and they settle into the next image. Made from two
of João Queirós' Midjourney stills, "Lantern Festival" and "Sea of Blooms", from the Stills collection on visions.

"Gommage" is the name this dissolve goes by; nothing in this project comes from the game the word is linked to.

**Watch it:** [visions.joaoqueiros.com/recipes/gommage](https://visions.joaoqueiros.com/recipes/gommage/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The stills:** [visions.joaoqueiros.com/stills](https://visions.joaoqueiros.com/stills/?utm_source=github&utm_medium=referral&utm_campaign=recipes)

26 s · 1920×1080 · 30 fps · Three.js + TSL, 32,400 leaves, no simulation · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge with WebGL2.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

Swap `assets/img/lantern-festival.jpg` and `assets/img/sea-of-blooms.jpg` for your own images (3:2, 1920×1280 is
plenty). The score is already in `assets/bgm/score.wav`; to rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Editable elements

Start with the remix template in [RECIPE.md](RECIPE.md). Its editable brief includes `{image_a}`, `{edge}`, `{n}`, `{particle_shape}`, `{wind_path}`, `{direction}`, `{image_b}`, `{final_line}`, `{url}`, `{score_idea}`.

Apply the new copy, palette and closing identity in `index.html`. Use the source map below for the image, drawing or data files specific to this recipe. If the timing changes, rebuild the score using the commands above.

## Source files

- `index.html`: the whole film. Two image planes and the instanced leaves share the same fronts in time; the DOM carries the type.
- `score/compose.py`: the autumn waltz, wind and leaf rustle, from the same timing table.
- `CONCEPT.md`: the approved concept card.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- Three.js (`assets/vendor/three.*.js`, `BloomNode.js`): MIT, © three.js authors.
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Manrope and Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the two images in `assets/img/` (João Queirós' Midjourney stills, included only so the film
  runs) and the names Imagined Worlds and João Queirós. Use your own images in a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
