# R08 · Boiling Line

![A hand-drawn sea at sunset with a small piano on the sand, in sepia ink and a watercolour wash](poster.jpg)

Everything looks drawn by hand: ink lines that wobble anew twelve times a second, like hand-drawn animation on
twos, over warm paper with one watercolour wash. Nothing is drawn by hand. Made for the Music page on
visions.joaoqueiros.com: a sea, a sunset and a small piano whose keys press on the score's own notes.

**Watch it:** [visions.joaoqueiros.com/recipes/boiling-line](https://visions.joaoqueiros.com/recipes/boiling-line/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The music:** [visions.joaoqueiros.com/music](https://visions.joaoqueiros.com/music/?utm_source=github&utm_medium=referral&utm_campaign=recipes)

26 s · 1920×1080 · drawn at 12 a second · pure SVG, no canvas or WebGL · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings or notes:

    pip install numpy
    python score/compose.py

## Files

- `index.html`: the whole film. Strokes, wobble, washes and the key presses all come from one painter.
- `score/compose.py`: pen scratch, ocean and piano; the piano plays the same NOTES table the drawn keys press.
- `CONCEPT.md`: the approved concept card.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Manrope and Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the names Imagined Worlds and João Queirós. Replace the end card with your own before you
  publish a remix.
