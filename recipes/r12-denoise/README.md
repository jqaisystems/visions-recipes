# R12 · Denoise

![A close-up of an eye halfway out of noise: coarse mosaic blocks and grain over a grey iris, with a HUD reading step 12 of 40.](poster.jpg)

A prompt types out and an eye resolves out of noise the way a generation preview does: mosaic, blur, grain and
grey fall away in forty visible steps while the HUD counts them. The camera dives through the pupil into a page
that renders card by card, then the last card pulls back into a wall of every image.
Made as the intro film for the Stills page on Imagined Worlds. Any set of images works: a portfolio, a product
range, a lookbook.

**Watch it:** [visions.joaoqueiros.com/recipes/stills-intro](https://visions.joaoqueiros.com/recipes/stills-intro/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

10 s · 1920×1080 · 30 fps · Canvas 2D, HTML and GSAP · one take · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

## Make it yours

1. Replace the images with your own, keeping the file names: the eye (`assets/img/w-eye.jpg`, 3:2, the pupil at
   about 46% across and 46% down, or move `F` in `index.html`), the seven page cards (`assets/img/`) and the wall
   tiles (`assets/tiles/01.jpg` to `43.jpg`, 480 by 320). Tile 18 is the one the last card becomes.
2. In `index.html`, change `PROMPT` and the title (`#t-prompt`, `#t-title`, `#t-sub`).
3. To rebuild the score after changing timings:

        pip install numpy
        python score/compose.py

For a portrait version, change `data-width` and `data-height` on `#root` (the site's phone version is `1080` by
`1350`): the layout reads the canvas size.

## Files

- `index.html`: the whole film. One painter draws every frame from the clock; `denoise()` draws any image at any
  step.
- `score/compose.py`: the score in D major, timed to the picture.
- `CONCEPT.md`: the concept card for this recipe.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Fraunces, Instrument Sans and IBM Plex Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not licensed:** every image in `assets/img/` and `assets/tiles/` (João Queirós' Midjourney stills, included only
  so the film runs), the names Imagined Worlds and João Queirós, and the site's own lines used as the example (the
  prompt and the title). Use your own images in a remix.
