# R50 · Full Stop

![The word YOURS in heavy black capitals on cream paper, ending in one red dot as its full stop](poster.jpg)

## Purpose

A film for AI Automation Systems, a service. The hero is a full stop: one red dot ends every sentence in the film and won't stay put, because a full stop that keeps going is a task that keeps running.

- **The same task:** the dot falls, bounces, and drags the first sentence out behind it.
- **Again:** the same landing raises AGAIN, then AND AGAIN.
- **Doubling:** one tile becomes 64, and the camera falls into one dot.
- **The map:** karaoke on IF YOU CAN DESCRIBE IT, then the dot draws a workflow while the camera rolls at each corner.
- **Code:** the dot is the dot in task.run().
- **Not a template:** the same words and the same bounce in twenty cuts across sixteen styles.
- **On your schedule:** black, two ticks, then a fall through a day of clock faces.
- **Yours:** every file, every prompt, every config. Five letters slam in, the dot lands and stops, and so does the music.

The workflow, prompts, code and clock times are demos, and a label on screen says so. No client work appears, and no prices or results are claimed.

**Source release:** [Full Stop source](https://github.com/jqaisystems/visions-recipes/releases/tag/r50-full-stop-v1)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

40 s · 1920×1080 · 30 fps · 20 cuts in 16 styles · €0 to make

## Requirements and commands

Needs Node 22+, Chrome or Edge, FFmpeg on the path, and Python with `pip install numpy`.

    python score/compose.py           # the score, composed in code from assets/table.js
    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render    # MP4 to renders/

## Editable elements

1. **The timing.** `assets/table.js` holds the beat grid and every event. The film and the score both read it.
2. **The words and scenes.** Each `sceneX` function in `assets/film.js` draws one section, and `drawAt` says which one plays when.
3. **The styles.** `STYLES` in `assets/film.js` holds the sixteen looks, and `ORDER` sets the twenty cuts.
4. **The dot.** `hop` and `dot` in `assets/film.js`. A key is a beat, a position and the height of the hop that lands there.
5. **The print.** The `POST` shader in `assets/film.js` holds the eight modes.
6. **Your mark.** The end card is the image in `assets/brand/`, placed flat as `#logo`.
7. **The sound.** The score is in `score/compose.py`, and every event in it comes from the table.

## Source files

- `index.html`: the stage, the audio and the timeline.
- `assets/film.js`: the whole film.
- `assets/table.js`: the one table.
- `score/compose.py`: the score. Needs only NumPy.
- `assets/brand/your-mark.svg`: a placeholder for your own mark.

## Credits and licences

- **Code, composition and score:** MIT (see the repo [LICENSE](../../LICENSE)).
- **GSAP** (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- **Fonts:** Archivo and JetBrains Mono are under the SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not included:** the JQ AI SYSTEMS mark is not part of this repo or its licence. Use your own mark.
- **AI Automation Systems:** a service that isn't in this repo. Only the film's code is here.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
