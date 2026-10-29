# R03 · Signal from Noise

![Iron-filing fragments gathered around six teal poles, each labelled with a research theme](poster.jpg)

## Purpose

Thousands of fragments line up like iron filings, gather around the poles that matter, and the strongest few are
pulled out into one reviewed list. Made for AI News Curator, JQ AI SYSTEMS' research briefing workflow: scattered
signals line up along a field, gather into its six real themes, and the strongest six become one daily brief that
a person reviews. Nothing in it is a real link or headline; the fragments carry only source types.

**Watch it:** [visions.joaoqueiros.com/recipes/signal-from-noise](https://visions.joaoqueiros.com/recipes/signal-from-noise/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The system it shows:** [AI News Curator case study](https://www.ai.joaoqueiros.com/systems/ai-news-curator?utm_source=github&utm_medium=referral&utm_campaign=recipes)

26 s · 1920×1080 · 30 fps · Canvas 2D only, no WebGL · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Editable elements

Start with the remix template in [RECIPE.md](RECIPE.md). Its editable brief includes `{n}`, `{fragment_labels}`, `{opening_line}`, `{k}`, `{pole_names}`, `{summary_object}`, `{review_step}`, `{archive_shape}`, `{final_line}`, `{palette}`, `{fonts}`.

Apply the new copy, palette and closing identity in `index.html`. Use the source map below for the image, drawing or data files specific to this recipe. If the timing changes, rebuild the score using the commands above.

## Source files

- `index.html`: the whole film. Field lines are traced once at load; one painter draws all 6,000 fragments from time.
- `score/compose.py`: metallic grains, a magnetic hum and struck tones over a D minor to F major bed, from the same timing table.
- `CONCEPT.md`, `BRIEF.md`: the approved concept card and the brief.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP 3.14.2 (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Geist and Geist Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-Geist.txt`).
- Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-InstrumentSerif.txt`).
- **Not licensed:** the JQ AI SYSTEMS logo (`assets/img/jqai-logo-nav.png`) and the names JQ AI SYSTEMS and
  João Queirós. Replace the logo and the end card with your own before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
