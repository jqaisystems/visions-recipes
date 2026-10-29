# R06 · Brand Readiness Scan

![A business card in teal ridge lines with a scanner line and a checklist](poster.jpg)

## Purpose

A scanner line raises an object into a relief of ridge lines and stops on one feature after another while a
list ticks them off. Made for João Queirós' free Brand Readiness Check: the scanner reads his own business card
against the check's eight questions, then shows the four score bands as a scale.

**Watch it:** [visions.joaoqueiros.com/recipes/brand-readiness-scan](https://visions.joaoqueiros.com/recipes/brand-readiness-scan/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The check:** [Brand Readiness Check](https://www.joaoqueiros.com/brand-readiness-check.html?utm_source=github&utm_medium=referral&utm_campaign=recipes)

26 s · 1920×1080 · 30 fps · Canvas 2D only · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Editable elements

Start with the remix template in [RECIPE.md](RECIPE.md). Its editable brief includes `{object}`, `{n}`, `{features}`, `{questions}`, `{scale_or_result}`, `{final_line}`, `{url}`, `{palette}`, `{fonts}`.

Apply the new copy, palette and closing identity in `index.html`. Use the source map below for the image, drawing or data files specific to this recipe. If the timing changes, rebuild the score using the commands above.

## Source files

- `index.html`: the whole film. The card is drawn once into a height map; one painter redraws it as ridge lines from time.
- `score/compose.py`: scanner drone, blips and ticks moving from A minor to C, from the same timing table.
- `CONCEPT.md`: the approved concept card.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Manrope: SIL Open Font License 1.1 (`assets/fonts/OFL-Manrope.txt`).
- Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-InstrumentSerif.txt`).
- **Not licensed:** the JQ mark (`assets/img/jq-mark.svg` and its path data in `index.html`), the business card's
  content and the name João Queirós. Replace the card with your own object before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
