# R02 · Paper Terminal

![A sheet of paper folding along its sections, the brand-voice-linter SKILL.md printed on it](poster.jpg)

A terminal drawn as paper prints a document, folds along its sections into a card, and files the card on a shelf
of many. Made for JQ AI Skills, a public library of 47 MIT skill folders: the same long prompt typed for the
103rd time becomes the brand-voice-linter skill, folded along its four real steps and filed with the other 46.

**Watch it:** [visions.joaoqueiros.com/recipes/paper-terminal](https://visions.joaoqueiros.com/recipes/paper-terminal/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The skills it shows:** [jqaisystems/jqai-ai-skills](https://github.com/jqaisystems/jqai-ai-skills)

26 s · 1920×1080 · 30 fps · CSS 3D only, no WebGL · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Files

- `index.html`: the whole film. Four nested hinged strips make the sheet; one painter writes every element from time.
- `score/compose.py`: paper and keyboard sounds plus a warm F major bed, generated from the same timing table.
- `CONCEPT.md`, `BRIEF.md`: the approved concept card and the brief.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP 3.14.2 (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Geist and Geist Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-Geist.txt`).
- Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-InstrumentSerif.txt`).
- **Not licensed:** the JQ AI SYSTEMS logo (`assets/img/jqai-logo-nav.png`) and the names JQ AI SYSTEMS and
  João Queirós. Replace the logo and the end card with your own before you publish a remix.
