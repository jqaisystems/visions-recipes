# R57 · Impression

![A frame of steel pins seen from the side behind clear acrylic: a workflow of blocks and a ring pressed into the pins, part of it glowing amber where a path doesn't fit and the rest blue, beside a panel headed PATH 2 that counts 303 pins moved, under CHECKED, NOT GUESSED.](poster.jpg)

## Purpose

A film for AI Problem-to-Solution Assessment, a service. Its idea: take the shape of the problem before you pick the solution. A pin screen does exactly that, because the pins remember.

- **One problem:** one workflow pushes in from behind and withdraws, and the pins keep its exact shape, snags and all.
- **The map:** the camera moves along the impression while labels name the steps, the handoffs, the delays and the rework.
- **Up to three paths:** three moulds press onto the front in turn. The pins each one shoves glow amber, the pins it fits glow blue, and a panel counts the pins moved.
- **One recommendation:** the third fits flush and not one pin moves. The film never says which kind of path it is.
- **The reset:** the frame tips back and every pin slides home in one wave.
- **The test and the brief:** thirty days, an owner and a target press up, then the decision brief.

The workflow and the paths are demos, and a label on screen says so. The paths are shapes with no names. No client work appears, and no prices or results are claimed.

**Source release:** [Impression source](https://github.com/jqaisystems/visions-recipes/releases/tag/r57-impression-v1)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

40 s · 1920×1080 · 30 fps · 11,520 instanced pins with real shadows · €0 to make

## Requirements and commands

Needs Node 22+, Chrome or Edge, FFmpeg on the path, and Python with `pip install numpy`. Every pin is real geometry with a shadow map and 4x antialiasing, so a GPU helps.

    python bake/table.py              # the one table: every shape, every event, the camera, the light and the captions, written to assets/table.js
    python score/compose.py           # the score, composed in code from that table
    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render    # MP4 to renders/

## Editable elements

1. **The words.** `CAPS` in `bake/table.py`: each caption's text and its beats in and out. `KINDS` names the paths, and `LABELS` names the map.
2. **The shapes.** `problem`, `cal`, `owner`, `target` and `brief` in `bake/table.py` are drawn from `rect`, `frame`, `circ`, `line` and `arc` marks in field units, each with how far it pushes the pins.
3. **The paths.** `PATHS` holds each mould: `cap` marks say how much it cuts off, and `fit=True` starts it as the exact negative of the problem.
4. **The timing.** `ev()` calls are the events, in order: `back`, `front`, `tilt` and `flat`, each with its beats, which way the pins follow (`x`, `y`, `r` or `n`) and how spread out they are.
5. **The frame.** `NX`, `NY`, `PITCH`, `EXT` and `LEN` in `bake/table.py` set how many pins, how far apart, how far they slide and how long they are.
6. **The camera and the light.** `CAM` holds the camera keys and `LIGHT` the key, the rim and when the lamp comes on and off. The steel, the amber and the blue are the shaders in `index.html`.
7. **Your mark.** The end card is the image in `assets/brand/`, placed flat as `#logo`.
8. **The sound.** The score is in `score/compose.py`. `MOVED` holds the pins each path moves, as the panel counts them: change it if the moulds change.

## Source files

- `index.html`: the stage, every pin's state per frame, the WebGL2 renderer, the overlay, the audio and the timeline.
- `bake/table.py`: the one table, standard library only.
- `score/compose.py`: the score. Needs only NumPy.
- `assets/brand/your-mark.svg`: a placeholder for your own mark.

## Credits and licences

- **Code, composition and score:** MIT (see the repo [LICENSE](../../LICENSE)).
- **GSAP** (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- **Fonts:** Archivo and JetBrains Mono are under the SIL Open Font License 1.1 (`assets/fonts/OFL-*.txt`).
- **Not included:** the JQ AI SYSTEMS mark is not part of this repo or its licence. Use your own mark.
- **AI Problem-to-Solution Assessment:** a service that isn't in this repo. Only the film's code is here.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
