# R10 · One Line

![The whole film as one teal line through its stations, a curve, type, a chart, a product card, a timeline, a waveform and three formats, above the words One line. Forty seconds. All code.](poster.jpg)

One glowing line never leaves the screen and the film never cuts. A single camera rides the head of the line
as it becomes an easing curve, a baseline for type, a chart, a product screen, an editing timeline, a waveform
and three formats; then a pull-back shows the whole journey was one stroke, and the line signs off as a mark.
Made for Product Films, the video service of JQ AI SYSTEMS.

**Watch it:** [visions.joaoqueiros.com/recipes/productfilms-oneline](https://visions.joaoqueiros.com/recipes/productfilms-oneline/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

40 s · 1920×1080 · 30 fps · HTML, SVG and GSAP · one take, no cuts · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

The score is already in `assets/bgm/score.wav`. To rebuild it after changing timings:

    pip install numpy
    python score/compose.py

## Files

- `index.html`: the whole film. The world, the camera keyframes, the line's paths, every station and the end
  card all come from one painter.
- `score/compose.py`: the 120 BPM score in A minor, timed to the picture.
- `assets/clips/clip-1.mp4` to `clip-6.mp4`: placeholders for the editing timeline. The film on the site uses
  six of my other films there; drop your own in with the same names.
- `CONCEPT.md`: the concept card for this recipe.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Inter, Libre Baskerville and JetBrains Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the JQ AI SYSTEMS logo and the JQ mark (`assets/img/`), the names JQ AI SYSTEMS and João
  Queirós, and the Product Films offer on the end card. Replace the mark and the end card with your own before
  you publish a remix.
