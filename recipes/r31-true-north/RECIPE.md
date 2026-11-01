# R31 · True North

**Style:** raymarched compass in a globe of images. One WebGL2 shader in two passes on a full-screen triangle, with no
meshes and no 3D library: a needle and ring as signed distance fields marched inside an analytic glass globe tiled with
stills, a Droste map for an endless zoom of stills nested in compass rings, and a cylinder of stills flown through with
a time smear, under HTML type.

**Made for:** Atlas Studio, a visual prompt studio.
**Length:** 33 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · WebGL2 · GLSL · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33-second 1920x1080 film in HyperFrames for Atlas Studio, my visual prompt studio, cut like a
showreel. Everything in the picture is one WebGL2 shader in two passes: the scene, then bloom, a chromatic kick on the
beats and the logo's light. Type is HTML over the canvas. Ink #0C1324, paper #FDFCFB, Atlas blue #2B6FFF, coral
#FF6848. Instrument Serif for the lines, Archivo, JetBrains Mono for the prompt and the labels. The images are my own
stills and clips from my site's --stills and --motion pages, each with its own title and prompt.
Open: a compass needle and its ring, raymarched, spin up out of black while a real prompt from the library types out.
"Every image starts as a prompt."
Globe: the camera pulls back to a glass globe tiled with the stills, ruled by the logo's meridians and dashed
parallels, the needle inside it. The globe whips round and brakes on the beat three times; each time the needle points
at one still and its title tags in. "--stills" slams in as the camera dives into the last one.
Zoom: an endless Droste zoom, every still inside the compass ring of the one before, a push on every second beat,
the needle sweeping the next still in, each with its title and prompt.
Tunnel: the last ring opens into a tunnel of stills flown through at speed. "Prompts from Atlas Studio." "Images on
--stills." with the site's address typed under it.
Motion: the tunnel brakes and three compass rings open with three clips playing. "Some became --motion."
Title: light gathers into the needle and ring where the logo will land, then the paper opens from the needle's hub with
the official logo, flat, never redrawn or recoloured, the line and the URL. Score: compose it in code from the same
table, 116 bpm, E minor to G major.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, cut like a showreel, as one
raymarched shader carrying {the_images}, in {palette}. {the_object} spins up out of black while {the_seed} types out;
the camera pulls back to a glass globe tiled with the images, which whips round and brakes on the beat while
{the_object} points at one after another; it dives into one, and an endless zoom carries each image inside a ring of
the one before; the zoom opens into a tunnel of images; {the_finale}; and everything collapses into the logo, placed
flat with {line} and {url}. One baked table drives the beats, the tiles, the zoom, the flight and a score composed in
code.
```

Ideas: a photographer's portfolio, with a lens aperture for the needle and the zoom running through each frame; a
travel brand, with a compass over a globe of destinations and a tunnel of postcards; a music label, with a turntable
needle over a globe of album covers and every brake on a downbeat; a design studio, with a cursor for the needle and
each project nested inside the last.

## How it's built

1. **Two passes.** `index.html` holds two shaders in JavaScript template strings. The first draws the scene into a
   half-float target and builds its mip chain; the second adds bloom from three mip levels, a chromatic kick on the
   beats, grain, the motion rings and the logo's light. A GSAP tween drives the clock and calls `paint(t)`, a pure
   function of time, so any frame can be seeked in any order.
2. **A needle and its ring.** The ring is a torus masked by its angle from north, so it draws itself on. The blades
   are extruded triangles, scaled in from the hub and turned by one angle.
3. **A globe of images.** Each pixel's ray hits an analytic sphere twice. The front hit reads a still by latitude and
   longitude from one texture array (16 longitudes by 8 bands, from a baked map), the needle is marched between the
   two hits, and the back tile shows dimly through the glass. Meridians and dashed parallels come from the logo.
4. **Whip and brake.** The globe turns a whole turn and more into each brake, so the chosen tile stops just right of
   centre; the needle's angle is worked out from that tile's place on screen.
5. **An endless zoom.** A Droste map: inside a ring, scale by four and turn by 0.35 rad, until the pixel lands in the
   deepest still it reaches. The frame zooms by four for each still, and the needle's sweep reveals the next one by
   angle.
6. **A tunnel with no cut.** The last ring shows the tunnel instead of a still, already in flight, so the zoom arrives
   inside it. Eight samples along the flight per pixel smear it with speed.
7. **Clips in rings.** Three muted video elements sit over the canvas, and the shader draws the compass rings around
   them as they open.
8. **The logo, unrecoloured.** The needle and ring gather as light where the logo will land, then the paper opens
   from the hub with the official file, its own paper feathered into the card at its edges.

## Gotchas worth knowing

- In a Droste zoom the nested ring is wider than the image's frame: mirror the image past its edges, or clamped edge
  pixels smear into streaks inside the ring.
- Keep the factor and the turn consistent across levels: turn the screen by the fraction of the step and each level
  back by the full step, or the zoom jumps at every image.
- A glow term with a step inside a smoothstep can be 1 everywhere: check what it does when the step is 0, or every
  tile picks up the line colour.
- Feather a logo file's own background into the end card rather than matching it by colour: a textured paper never
  matches a flat fill.
- Wait for every image's `decode()` and the fonts before the first paint, and upload the images once into a texture
  array: the renderer seeks frames out of order.
- Keep the shaders in JavaScript template strings, not script tags with a custom type: the HyperFrames linter parses
  inline scripts and fails on GLSL.
