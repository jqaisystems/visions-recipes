# R29 · Seamless

**Style:** raymarched liquid shader. One WebGL2 fragment shader on a full-screen triangle, with no meshes and no
3D library: rounded slabs joined by a smooth minimum, so one pool of liquid chrome can tear into tiles and melt back
into one, a coastline photo read on the liquid's top faces and bent by its normals, a procedural studio for the
reflections, and soft shadows and ambient occlusion from the same distance field.

**Made for:** Grid Studio, twelve free Instagram tools that run in the browser.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for Grid Studio, twelve free Instagram tools that run in the
browser ("No upload, no account, no watermark: your images never leave your device."). Everything in the picture is one
WebGL2 fragment shader that raymarches signed distance fields: no meshes, no 3D library. Type is HTML over the canvas.
Grid Studio's palette: ink #181512, paper #faf8f4, line #e2ddd2, muted #6f685e, terracotta #c24d21. Instrument Serif,
Archivo and JetBrains Mono. Use the app's own demo photo of a coastline.
The pour: a chrome drop falls into a pool, rings run out, and the photo surfaces inside the liquid, bent by its normals.
The cut: seams draw across the pool in a 3x3; on the beat each seam stretches into a neck and snaps, until nine liquid
tiles stand apart. Numbers rise in posting order, post 1 bottom-right in terracotta.
Posted: the tiles fall one by one, in posting order, into a profile grid, and the seams melt into one picture again.
The tools: the liquid becomes a carousel that splits into slides, round covers, a palette of five drops coloured from
the photo, a resize from 1:1 to 4:5 to 9:16, a QR code that sets into blocks, and back to the grid.
In your browser: the liquid sits in a browser window; an upload tries to pull a drop out, it stretches to the edge and
springs back. "No upload. No account. No watermark."
Title: the liquid gathers into the 3x3 mark at exactly the official file's size, then the official mark, flat, never
redrawn or recoloured, then the line and the URL. Score: compose it in code from the same table, 112 bpm, E minor to
G major.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, as one raymarched fragment shader, in
{palette}. A drop of {the_material} falls into a pool and {the_picture} surfaces inside it; seams draw across it and
snap on the beat into {the_pieces}; the pieces fall into {the_destination} in order and melt back into one; the liquid
becomes {the_features}; {the_threat} tries to pull a drop away and it springs back; and the liquid gathers into the
logo at its official size. Then the flat logo with {line} and {url}. One baked table drives the snaps, the order, the
shapes and a score composed in code.
```

Ideas: a photo printing service, with ink tearing into prints that fall into an album; a tile shop, with glaze
cracking along the grout lines into a wall; a puzzle app, with a picture pouring in and snapping into pieces; a design
tool's export panel, with one frame split into the sizes it exports to.

## How it's built

1. **One shader.** `index.html` holds one fragment shader in a JavaScript template string. A GSAP tween drives the
   clock and calls `paint(t)`, a pure function of time: `scene(t)` works out every body, the camera and the effects
   for that moment, and `paint` sends them to the shader as uniforms, so any frame can be seeked in any order.
2. **Bodies, not meshes.** `map(p)` is the whole world: up to twelve rounded boxes (`uE` centres, `uH` half sizes),
   a capsule for the stretched drop and a block field for the QR code, joined by a smooth minimum of radius `uK`.
   The ray marches up to 110 steps; shadows march the same field again.
3. **A seam that snaps.** The pool is one slab until a beat before each seam's time. `groups()` then splits it into
   two slabs that drift apart; the smooth minimum keeps them joined by a thinning neck until the gap outgrows it,
   exactly on the beat, and both halves wobble.
4. **The picture on the liquid.** Each body carries its rectangle of the photo. On the top faces the shader reads the
   photo at that point's place in the grid, pushed by the surface normal, so ripples and melts bend the picture.
5. **The tools.** Each tool is a new set of bodies for the same smooth minimum: a strip that splits into slides, round
   drops for the covers, five drops coloured from the photo's palette, a squash from 1:1 to 4:5 to 9:16, and a field
   of blocks for the QR code.
6. **The mark, matched.** The camera sits at the height that makes one unit 93.75 px, so the liquid's 3×3 (blended to
   flat-extruded tiles by `sdFlat`) lands exactly under the official mark, which then takes over, flat.
7. **A vertical cut.** The 9:16 version uses the same shader on a 1080×1920 canvas with a wider lens, pulls every shot
   back about its target, and moves the type and the title camera so the mark still matches.

## Gotchas worth knowing

- Keep the shader in a JavaScript template string, not a script tag with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
- A smooth minimum of boxes that already touch leaves bulges along the seams: keep the slabs as one body until the
  seam's time instead of blending touching boxes.
- Give any detailed field, like the QR blocks, a bounding box distance: outside it, return the distance to the box,
  or the march takes tiny steps everywhere and the frame goes black.
- Measure the DOM once when the film is built, never inside `paint(t)`: a measurement every frame forces a layout
  during the render.
- Brand rules hold in motion: the liquid tiles echo the mark, but the mark itself is the official file, flat, never
  redrawn or recoloured.
