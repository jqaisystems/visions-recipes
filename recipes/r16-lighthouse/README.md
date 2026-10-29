# R16 · Lighthouse

![The word found in warm harbour lights above a stone quay at night, mirrored in a calm sea under the moon.](poster.jpg)

## Purpose

Lead generation as a lighthouse at night. The beam sweeps a dark sea and every boat it finds lights up; it stops on a
few to check them, scores every one from 0 to 100, and the cold ones fade while the hot ones turn for shore. A first
message writes itself for the best one, and a person pulls the brass SEND lever. Then the hot leads moor at the quay
and their lights rise into the word "found", mirrored in the water.
Made for AI Lead Generation & Outreach, a service of JQ AI SYSTEMS.

**Watch it:** [visions.joaoqueiros.com/recipes/lighthouse](https://visions.joaoqueiros.com/recipes/lighthouse/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

32 s · 1920×1080 · 30 fps · Three.js (WebGPU renderer on WebGL2, TSL reflector sea), GSAP · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render                             # MP4 to renders/

## Editable elements

1. The prospects and the beam are one table, written by `bake/boats.py`: the beam's path (`BEAM`), the three boats it
   stops on (`SPECIAL`), how many boats and which are hot. Change it and run it:

        python bake/boats.py

   It writes `assets/boats.js` for the film and `bake/boats.json` for the score.
2. The enrichment cards, the draft message, the station titles, the HUD lines (`STATE`) and the end card are plain
   text in `index.html`.
3. To change the final word, edit `WORD` in `bake/word.py` and run it (needs `pip install fonttools brotli`).
4. Rebuild the score (needs `pip install numpy`):

        python score/compose.py

## Source files

- `index.html`: the whole film. `renderAt(t)` poses the beam, every boat, the message and the word from the clock;
  one painter draws the type, the cards and the scores.
- `bake/boats.py`: the one table, seeded. `bake/word.py`: the word's outlines, from the film's own font.
- `score/compose.py`: the score, timed to the same table.
- `CONCEPT.md`: the concept card for this recipe.

## Credits and licences

- Code, composition and score: MIT (see the repo [LICENSE](../../LICENSE)).
- Three.js, `BloomNode.js` and `RoomEnvironment.js` (`assets/vendor/`): MIT, © three.js authors.
- GSAP (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- Inter, Libre Baskerville and JetBrains Mono: SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- The prospects, cards and message are made up: no real people or companies.
- **Not licensed:** the names JQ AI SYSTEMS and João Queirós, and the service name, line and URL on the end card.
  Replace them with your own before you publish a remix.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
