# R29 · Seamless · concept

**Style (season 3, film 1 of 3): raymarched liquid shader.** One fragment shader on a full-screen quad in WebGL2: no
meshes, no Three.js scene, no SVG for the picture. Everything you see is signed distance fields raymarched per pixel:
- **SDF metaballs:** blobs joined by a smooth minimum, so one pool can tear into pieces and pieces can flow back into one;
- **liquid chrome:** a glossy surface lit by a procedural studio (paper-white softboxes, one terracotta strip), with
  Fresnel reflections and soft shadows on the floor;
- **an image inside the liquid:** the coastline photo is sampled on the liquid's top surface and bent by its normals,
  so the picture rides the liquid as it splits, falls and merges;
- **the seam as a neck:** the smoothing radius of the union is driven by the clock, so a seam stretches into a thin neck
  and snaps exactly on the beat.
Type and labels are HTML above the canvas. `paint(t)` sets the uniforms from one baked table, so every frame is a pure
function of time.

**Made for:** Grid Studio (ai.joaoqueiros.com/gridstudio), twelve free Instagram tools that run entirely in the
browser. Its own line: "No upload, no account, no watermark: your images never leave your device." Its first film (the
showreel, /code 006) was a posting-order tile wipe in HTML; this one is all shader.

**The idea:** one image, poured into a seamless grid. Grid Studio cuts a picture into tiles that line up perfectly on a
profile; in the film the picture is a liquid, so the cut is a tear, and the profile is where it flows back into one.

1. **The pour (0 to 5 s).** Ink-dark ground. One chrome drop falls into a pool, rings run out, and as the surface
   settles the coastline photo surfaces inside it, bent by the last ripples.
2. **The cut (5 to 11 s).** Seams draw across the pool in a 3×3 grid. On the beat each seam stretches into a neck and
   snaps, until nine liquid tiles stand apart, each still carrying its piece of the picture. Numbers rise in posting
   order, post 1 bottom-right in terracotta. "One image. A seamless grid."
3. **Posted (11 to 16 s).** The tiles lift and fall one by one, in posting order, into a profile grid, and as the last
   lands the seams melt and the picture reads whole again: "Posted in order, seamless on the profile."
4. **Twelve tools (16 to 23 s).** The liquid morphs on the beat through the tools, each a shape with its label: a
   carousel strip that splits into slides, highlight covers as round drops, a palette of five drops coloured from the
   photo, a resize that squashes 1:1 to 4:5 to 9:16, a QR that sets into blocks, and back to the grid.
5. **On your device (23 to 27 s).** The liquid sits inside a browser window drawn as a glass tray. An upload arrow
   tries to pull a drop out; the drop stretches to the edge and springs back. "No upload. No account. No watermark."
6. **Title (27 to 32 s).** The liquid gathers into a 3×3 of rounded tiles, eight ink and one terracotta, and resolves
   into the official Grid Studio mark, flat. Then "Grid Studio", "Twelve free Instagram tools in your browser" and
   ai.joaoqueiros.com/gridstudio.

**Spec:**
- 32 s, 1920×1080, 30 fps, with a 9:16 cut (the same shader with a portrait camera and the grid re-laid for the frame).
- WebGL2, one fragment shader, raymarched SDF scene (smooth-min metaballs over a floor plane), about 96 steps, soft
  shadows and ambient occlusion from the distance field; drawn with `preserveDrawingBuffer` and repainted on every seek.
- One Python table holds the drops, the seams and their snap times, the posting order, the tool morph targets, the
  upload pull and the title tiles. The score is composed in code from it.

**Score:** 112 bpm, E minor to G major. A pitched drop and a low bloom for the pour; a glassy pluck for every seam
that snaps; a soft wooden tick per post in posting order; a quick filtered sweep for each tool morph; a rubbery stretch
and snap for the upload that never leaves; a warm chord and a bell on the mark.

**Palette and type (Grid Studio's own):**
- Ground ink #181512, paper #faf8f4, line #e2ddd2, muted #6f685e, terracotta #c24d21 (post 1, the one strip light,
  the mark's last tile).
- The chrome takes its colour from the studio: paper-white highlights, ink shadows, one terracotta edge.
- Type: Instrument Serif for the lines, Archivo for labels, JetBrains Mono for numbers and the URL.

**Brand rules kept in motion:**
- The liquid tiles echo the mark, but the mark itself is the official file, placed flat at the end, never redrawn or
  recoloured.
- Tool names exactly as the app lists them; no tool that is not in the app.

**Honesty:**
- The photo is the app's own demo image (Stefan Kunze, Unsplash License), credited in the recipe.
- "Twelve" is the product's own number of tools. No metric, user count or rating appears.
- "Your images never leave your device" only as the product says it: the tools run in the browser.
