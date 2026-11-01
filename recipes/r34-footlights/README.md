# R34 · Footlights

![A paper toy theatre with red curtains and a gold valance: a phone on a rod at stage left throws cyan light, paper frames run on a pulley across a starry window, a monitor shows a video meeting of four paper puppets, and six footlights glow along the front of the stage, under the words "Live in your meeting."](poster.jpg)

## Purpose

A film for Phone Webcam Bridge, João's system that turns an Android phone into the webcam on a Windows PC, made as
paper cut-out stop motion in a backlit toy theatre. Every scene on the stage is a step the system really takes.

- **Curtain up:** a lamp flickers on and the curtains part on a paper home office at night.
- **The phone:** it rises through a trap, and two flaps turn it to 1080p and the front camera.
- **Pairing:** six PIN tiles flip on the phone and match on the PC; the screen goes dark while it keeps streaming.
- **Link:** a USB cable unrolls across the stage, with Wi-Fi rings behind it.
- **The feed:** the picture runs to the PC as paper frames on a pulley while zoom, exposure and the camera are set.
- **On stage:** Start OBS Camera lights the meeting tile and the footlights come up.
- **Stays local:** a roller blind drops over the cloud, with 0 accounts, no server, no telemetry.
- **Title:** the curtains close, a front-cloth drops and the logo lands, flat.

Made for Phone Webcam Bridge. The PIN and the people in the meeting are invented, and no speed, delay or result is
claimed.

**Source release:** [Footlights source](https://github.com/jqaisystems/visions-recipes/releases/tag/r34-footlights-v1)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

33.1 s · 1920×1080 · 30 fps · one Canvas 2D, paper cut-out on twos in five depth layers · score composed in code · €0 to make

## Requirements and commands

Needs Node 22+ and Chrome or Edge. The bake and the score need Python; the score needs `pip install numpy`.

    npm run dev       # browser preview, using the version pinned in package.json
    npm run check     # validate the composition
    npm run render    # MP4 to renders/

## Editable elements

1. **Your device and your story.** The PIN, the phone's two settings, the three tags, the meeting's puppets and the
   lines of type are in `bake/table.py`. Change them and run `python bake/table.py`.
2. **Your mark.** The end card is the image in `assets/brand/`, placed flat as `#t-logo`, with the name, line and URL
   set as text in `index.html`.
3. **The clock.** The beat grid, every event (`E`), the sections (`T`) and the HUD are in `bake/table.py`.
4. **The look.** The paper stocks (`STOCK`), the layer depths (`D`), the layout constants (`WIN`, `MON`, `PH`, the
   pulley wheels), the camera's keys (`camAt`) and the light (`makePost`, `post`) are in `index.html`.
5. **The score.** Rebuild it with `python score/compose.py`.

## Source files

- `index.html`: the whole film.
  - `piece(P)`: one piece of paper, a torn outline, a stock, a shadow, an optional backlight glow and whatever is
    printed on it.
  - `layer(d)`: sets the transform for a layer at depth `d` from the camera's position, which gives the parallax.
  - `cone()`, `glowAt()`: light added on top of the paper.
  - `drawBack`, `drawSet`, `drawPanel`, `drawPhone`, `drawCable`, `drawWifi`, `drawPulley`, `drawApron`, `drawArch`,
    `drawCurtains`: the theatre, back to front.
  - `paint(t)` snaps `t` to a pose and draws the whole frame for it.
- `bake/table.py`: the one table. `score/compose.py`: the score, timed to the table.
- `CONCEPT.md`: the concept card for this recipe.

## Credits and licences

- **Code, composition and score:** MIT (see the repo [LICENSE](../../LICENSE)).
- **GSAP** (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- **Fonts:** Archivo, Instrument Serif and JetBrains Mono are under the SIL Open Font License 1.1
  (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the JQ AI SYSTEMS logo (`assets/brand/jqai-logo.png`) and the names JQ AI SYSTEMS and Phone Webcam
  Bridge. Use your own mark in a remix. Phone Webcam Bridge itself is not open source and is not in this repo; only
  the film's code is. "Start OBS Camera" is the bridge's own button label, set as type.
- **Sample data:** the PIN and the people in the meeting are invented for this film.

[All recipes](../../docs/catalog.md) · [Setup and first example](../../README.md#first-working-example)
