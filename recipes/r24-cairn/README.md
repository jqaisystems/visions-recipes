# R24 · Cairn

![The Cairn stones stacked into a C on a summit at dawn, the sun breaking through with rays over a sea of cloud and inked peaks.](poster.jpg)

An anime film for an SEO service, in cel-shaded 3D with painted background art.

- **Night:** forty dashboard numbers hail onto a summit and blow away, leaving three that matter.
- **The first stone:** it falls out of a dawn-lit cloud bank.
- **Every four weeks:** weeks race past as a time-lapse while stones land and a trail sign's search result climbs.
- **The checkpoint:** a real checkpoint's decisions slam in as manga lettering.
- **The summit:** the last stones land as the sun breaks over a sea of cloud.

Made for Cairn, the SEO service of João Queirós.

**Watch it:** [visions.joaoqueiros.com/recipes/cairn](https://visions.joaoqueiros.com/recipes/cairn/?utm_source=github&utm_medium=referral&utm_campaign=recipes)
· **Prompt, remix template and breakdown:** [RECIPE.md](RECIPE.md)

32 s · 1920×1080 · 30 fps · Three.js (WebGPU renderer on WebGL2, TSL toon materials, outline pass, shadow maps),
Canvas 2D, GSAP · score composed in code · €0 to make

## Run it

Needs Node 22+ and Chrome or Edge.

    npx --yes hyperframes@0.8.184 preview      # Studio preview in the browser
    npm run render                             # MP4 to renders/

## Make it yours

1. **Your mark.** Put it in `assets/brand/` as an SVG, one filled path per piece, and point the `fetch` in
   `index.html` at it. Each path becomes one piece that falls and lands where the logo puts it.
2. **The clock.** Every scene, the landings, the checkpoint stamps, the impacts and the smears are in
   `bake/table.py`. So are the forty numbers and the three that stay. Change them and run `python bake/table.py`.
3. **The world.** The mountain rings are `RINGS`, the sea of cloud is `seaTex`, the sky colours are `SKY`, and the
   sun's path is `sunAngle`.
4. **The words.** The station titles, the HUD and the end card are plain text in `index.html`. The trail sign is
   drawn in `drawSign`.
5. **The score.** Rebuild it with `python score/compose.py` (needs `pip install numpy`).

## Files

- `index.html`: the whole film.
  - `renderAt(t)` poses every scene, lights it from the sun and renders it through the outline pass.
  - `drawSky` paints the sky against the horizon.
  - `paintFx(t)` draws the 2D layer.
  - `paint(t)` adds the impact frames and the type.
- `bake/table.py`: the one table. `score/compose.py`: the score, timed to the table.
- `CONCEPT.md`: the concept card for this recipe.

## Licences

- **Code, composition and score:** MIT (see the repo [LICENSE](../../LICENSE)).
- **Three.js and `SVGLoader.js`** (`assets/vendor/`): MIT, © three.js authors.
- **GSAP** (`assets/vendor/gsap.min.js`): GSAP Standard License, free (gsap.com/standard-license).
- **Fonts:** Outfit, Instrument Serif and IBM Plex Mono are under the SIL Open Font License 1.1
  (`assets/fonts/OFL-*.txt`).
- **Not licensed:** the Cairn logo (`assets/brand/`) and the names Cairn and João Queirós. Use your own mark in a
  remix.
