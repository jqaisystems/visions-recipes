# R01 · Token Rain

![Token particles pouring through a glowing ring labelled 01 DRAFT](poster.jpg)

## Purpose

Text dissolves into particles sampled from its own letters, rains through a sequence of gates and recompiles
as new text. Made for the Prompt Engineering service of JQ AI SYSTEMS: a stock AI paragraph has its clichés
caught, burns into tokens, rains through draft, critique and rewrite, and lands as "Same model. Your voice."

**Watch it:** [visions.joaoqueiros.com/recipes/token-rain](https://visions.joaoqueiros.com/recipes/token-rain/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

26 s · 1920×1080 · 30 fps · 88,872 GPU particles · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/ (one worker, see RECIPE.md)

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Editable elements

Start with the remix template in [RECIPE.md](RECIPE.md). Its editable brief includes `{source_text}`, `{what_is_wrong}`, `{n}`, `{gate_labels}`, `{final_line}`, `{lockup}`, `{palette}`, `{fonts}`.

Apply the new copy, palette and closing identity in `index.html`. Use the source map below for the image, drawing or data files specific to this recipe. If the timing changes, rebuild the score using the commands above.

## Source files

- `index.html`: the whole film (DOM type layers + the Three.js/TSL particle stage), driven by one timing table.
- `score/compose.py`: the music and sound design, generated from the same timings (`score/timings.json`).
- `CONCEPT.md`, `BRIEF.md`, `STORYBOARD.md`, `frame.md`: the concept card, brief, storyboard and design spec.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- Three.js r181 (`assets/vendor/three.*.js`, `BloomNode.js`): MIT, © three.js authors.
- GSAP 3.14.2 (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Geist and Geist Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-Geist.txt`).
- Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-InstrumentSerif.txt`).
- **Not licensed:** the JQ AI SYSTEMS logo (`assets/img/jqai-logo-nav.png`) and the names JQ AI SYSTEMS and
  João Queirós. Replace the logo and the end card with your own before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
