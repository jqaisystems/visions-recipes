# R30 · Ninefold

**Style:** raymarched glass field. One WebGL2 fragment shader on a full-screen triangle, with no meshes and no 3D
library: one glass tile repeated across space by domain repetition, three refracted rays per tile so the photo splits
into colour at every bevel, waves launched on the beat, per-cell shape blends for hard cuts, and a polar fold for a
kaleidoscope, under heavy kinetic type.

**Made for:** Grid Studio, twelve free Instagram tools that run in the browser.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Grid Studio, twelve free Instagram tools that run in the
browser. Cut it like a motion designer's showreel. Everything in the picture is one WebGL2 fragment shader that
raymarches signed distance fields; heavy kinetic type is HTML over the canvas. Ink #181512, paper #faf8f4, terracotta
#c24d21 and #ff8a52 for the type. Archivo at its heaviest, Instrument Serif and JetBrains Mono. Use the app's own demo
photo of a coastline.
The shader: one glass tile repeated across space by domain repetition, the nearest four cells checked per step, a
window mask that decides which cells exist; each tile refracts three rays, one per colour, and reads the photo through
its base, so the picture splits into colour at every bevel.
Open: one tile spins out of black with the photo inside it. "One image." It bursts into nine.
Field: the camera ramps back over an endless field to the horizon; a wave rolls out on every beat and each tile tilts
to its slope. "Nine posts." "Zero seams."
Feed: a dolly zoom down a profile column, a hard cut to straight above, and nine tiles drop in posting order, post 1
bottom-right in terracotta. "Posted in order." "Seamless on your profile."
Tools: ten hard cuts, one every beat and a half, each a new shape of the same field with its name: Grid Maker,
Carousel, Covers, Palette, Resize, QR Code, Icon Maker, Captions, Hashtags, Bio. Then "Twelve free tools."
Browser: a kaleidoscope folds the field into a mandala that collapses into one tile in a browser window; UPLOAD,
ACCOUNT and WATERMARK fly at the glass and shatter on it.
Title: nine tiles lock into the mark at exactly the official file's size, then the official mark, flat, never redrawn
or recoloured, then the line and the URL. Score: compose it in code from the same table, 128 bpm, D minor to F major.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, cut like a showreel, as one
raymarched fragment shader with heavy kinetic type over it, in {palette}. One {the_object} of glass spins out of black
with {the_picture} split into colour through it and bursts into {the_count}; the camera ramps back over an endless
field of them with a wave on every beat; a dolly zoom runs down {the_destination} where they land in order; {n} hard
cuts turn the field into {the_features}; a kaleidoscope folds it into one inside {the_container}, where {the_objections}
fly at the glass and shatter; and the pieces lock into the logo at its official size. Then the flat logo with {line}
and {url}. One baked table drives the beats, the cuts, the shapes and a score composed in code.
```

Ideas: a print shop, with one glass print multiplied into a wall and ten cuts for ten paper stocks; a photo editor,
with every cut a different edit across the field; a music app, with an album cover pulsing to the horizon on the beat;
a font foundry, with one glass letter repeated and every cut a different weight.

## How it's built

1. **One shader.** `index.html` holds one fragment shader in a JavaScript template string. A GSAP tween drives the
   clock and calls `paint(t)`, a pure function of time: `scene(t)` sets every uniform for that moment (the window, the
   waves, the shapes, the camera), so any frame can be seeked in any order.
2. **An endless field from one cell.** `cellD` is one rounded glass tile. Each march step finds the four nearest cells
   and takes the closest, so a tile that rises or tilts into its neighbour is never cut off. A soft square window
   (`uMask`) decides which cells exist, from nine touching tiles to the horizon.
3. **Glass that splits the light.** At a hit, the shader refracts three rays, one per colour with a slightly different
   index, and reads the photo where each lands at the tile's base. Fresnel mixes in the reflected studio.
4. **Waves on the beat.** `uWave` launches a ring on each beat; every cell rises with it and tilts to the slope under
   it. `uBurst` lifts and turns each tile by its own hash for the opening burst.
5. **Ten cuts.** Each tool sets `uShape` (sphere, bars, lines, squircle), `uQR` or `uBio` and a new camera, so a hard
   cut is a new set of weights for the same field. `TOOLCFG` in the script lists all ten.
6. **A kaleidoscope.** `toField` folds the plane into mirrored wedges around the centre when `uKal` is set, and turns
   them with `uKalRot`.
7. **Type on the beat.** The slams, the tool names and the flying words are HTML over the canvas. The flying words
   scale toward the camera and break into pieces on impact, each piece on its own hashed path.
8. **The mark, matched.** The title camera sits at the height that makes one unit 93.75 px, so the nine tiles lock
   into the mark at exactly the official file's size before it takes over, flat.
9. **A vertical cut.** The 9:16 version uses the same shader on a 1080×1920 canvas with a wider lens, pulls every shot
   back about its target, and resets the type and the title camera for portrait.

## Gotchas worth knowing

- With domain repetition, check the neighbouring cells as well as your own: a tile that rises or tilts pokes into the
  next cell, and checking one cell alone cuts it off.
- Three refraction rays triple the texture reads, not the march: march once, then refract three times from the hit.
- A difference blend on type over a busy shader reads as noise: plain white with a soft shadow holds up on every
  frame.
- Measure the flying words' widths once when the film is built: reading `offsetWidth` inside `paint(t)` forces a
  layout on every frame.
- Keep the shader in a JavaScript template string, not a script tag with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
