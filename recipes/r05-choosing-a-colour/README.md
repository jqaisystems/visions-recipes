# R05 · Choosing a Colour

![Four colour swatches, teal, blue, ink and bone, labelled with their HEX codes](poster.jpg)

## Purpose

Every colour at once swirls like marbled ink, then a method takes over: the colours that don't fit drain away,
one colour pools out of the ink, and it separates into a few clean, labelled swatches. Made for João Queirós'
article on how to choose brand colours: its five steps, in order, turn a swirl of every colour into one palette.

**Watch it:** [visions.joaoqueiros.com/recipes/choosing-a-colour](https://visions.joaoqueiros.com/recipes/choosing-a-colour/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The article:** [How to Choose Brand Colours](https://www.joaoqueiros.com/blog-how-to-choose-brand-colours.html?utm_source=github&utm_medium=referral&utm_campaign=recipes)

26 s · 1920×1080 · 30 fps · one WebGL2 fragment shader, no simulation · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge with WebGL2.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Editable elements

Start with the remix template in [RECIPE.md](RECIPE.md). Its editable brief includes `{opening_line}`, `{n}`, `{source}`, `{steps}`, `{k}`, `{palette_with_codes}`, `{applications}`, `{final_line}`, `{fonts}`, `{score_idea}`.

Apply the new copy, palette and closing identity in `index.html`. Use the source map below for the image, drawing or data files specific to this recipe. If the timing changes, rebuild the score using the commands above.

## Source files

- `index.html`: the whole film. The fragment shader paints the ink from time alone; HTML carries the steps.
- `score/compose.py`: liquid pads, water drops and chimes in D, from the same timing table.
- `CONCEPT.md`: the approved concept card.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Manrope: SIL Open Font License 1.1 (`assets/fonts/OFL-Manrope.txt`).
- Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-InstrumentSerif.txt`).
- **Not licensed:** the JQ mark (`assets/img/jq-mark.svg`) and the name João Queirós. Replace the mark and the end
  card with your own before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
