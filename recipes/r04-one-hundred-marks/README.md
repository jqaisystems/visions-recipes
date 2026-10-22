# R04 · One Hundred Marks, One Line

![The JQ mark above the word Marks and the line "398 identities · 160 pages · one book"](poster.jpg)

One line that never lifts off the page. It closes into the outline of one shape, then flows straight into the
next, faster and faster, and finally settles on one. Made for Marks, João Queirós' 160-page book of 398 logo
identities: in the film the line runs through 100 marks from the book and lands on the JQ mark.

**Watch it:** [visions.joaoqueiros.com/recipes/one-hundred-marks](https://visions.joaoqueiros.com/recipes/one-hundred-marks/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)
· **The book:** [joaoqueiros.com/marks](https://www.joaoqueiros.com/marks.html?utm_source=github&utm_medium=referral&utm_campaign=recipes)

26 s · 1920×1080 · 30 fps · one SVG path · score composed in code · €0 to make

## What's in this folder (and what isn't)

The logos in the film belong to their owners, so they are **not** here. This folder ships the whole pipeline
with twelve plain demo shapes (circle, star, heart, house…) in their place, so it runs as is. Swap in your own
images and it becomes your film.

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

## Use your own shapes

Needs Python 3 with numpy and Pillow (`pip install numpy pillow`). Put your images (PNG, WebP or JPG, dark ink on
a light ground) in a folder, list their file names (without extension) in film order in `order.json`, and
optionally give each a caption in `captions.json` (`{"01": "01 · Circle · Demo shape"}`). Then:

    python tools/trace.py <your folder> data/outlines.json --sheet data/sheet.png
    python tools/build.py data/outlines.json <your folder>/order.json <your folder>/captions.json data/jq-outline.json assets/outlines.js
    python score/compose.py

Check `data/sheet.png` first: each image should read as a clear silhouette. `tools/make_demo.py data/demo` redraws
the demo shapes. The last argument to `build.py` is the outline the line settles on; trace your own logo the same
way and change `JQ` and `jq-mark.svg` in `index.html` to match.

## Files

- `index.html`: the whole film. One SVG path; outlines are rolled to match at load and one painter morphs them from time.
- `tools/trace.py`: images to outlines (threshold, close gaps, keep the symbol, fill holes, trace, smooth, resample).
- `tools/build.py`: packs outlines and captions into `assets/outlines.js`.
- `score/compose.py`: pencil on paper, one piano note per shape, pads in G, synced to the same tempo curve.
- `data/jq-outline.json`: the JQ mark's outer path, traced from its SVG.
- `CONCEPT.md`: the approved concept card.

## Licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Manrope: SIL Open Font License 1.1 (`assets/fonts/OFL-Manrope.txt`).
- Instrument Serif: SIL Open Font License 1.1 (`assets/fonts/OFL-InstrumentSerif.txt`).
- **Not licensed:** the JQ mark (`assets/img/jq-mark.svg`, `data/jq-outline.json`), the Marks book and the name
  João Queirós. Replace the mark and the end card with your own before you publish a remix.
