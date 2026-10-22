# R09 · Aurora in ASCII

**Style:** a real 3D scene drawn only in text characters, like an old terminal screen. Every cell of a grid picks
a glyph by how bright the picture is behind it, from ` .:-=+*#%@`, and takes that spot's colour.
**Made for:** the Recipes library on visions.joaoqueiros.com, the library's own film.
**Length:** 26 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPURenderer, TSL) · GSAP (one clock) · Canvas 2D (glyph atlas) · Python (score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 26-second 1920x1080 film in HyperFrames for the Recipes library on my site. Draw it like an old terminal:
on near-black #07090C, a cursor blinks and the command "render aurora --ascii" types itself. Then a live
Three.js scene appears only as text characters: curtains of aurora rise and ripple over a dark ridge under
stars, green #5CF2A2 at the hem through teal #3FC8D8 to violet #9B7BFF at the tops. Halfway, the character cells
shrink until the aurora is almost a smooth picture, then grow back. The aurora dims and the cells settle into
the title "Recipes", with "films, prompts and source" and visions.joaoqueiros.com/recipes typed under it.
Technique: render the scene to a texture; one post shader cuts the frame into 12x20 px cells, samples the
scene at each cell's centre and draws the matching glyph from " .:-=+*#%@" out of a font atlas drawn on a canvas
in IBM Plex Mono, tinted with that cell's colour. Cells switch on at seeded random times with a flicker of
random glyphs. The cell size is a uniform for the shrink; the title is a second mask texture read by the same
pass. Fraunces for the title mask. One painter computes every frame from time.
Score: compose it in code with numpy: key clicks for every typed character, a digital crackle as cells switch
on, a slow analog-style pad in A minor and a shimmering arpeggio that rises with the aurora, and a low hum that
swells when the cells shrink.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames, drawn only in text characters like a terminal.
A cursor types "{command}". Then {scene_3d}, rendered live in Three.js, appears as glyphs from "{ramp}",
each in its own colour, on {background}. At {moment} the cells shrink to almost a smooth picture and grow back.
End on {title} built from the same glyphs, with {subtitle} and {url} typed under it.
One post shader: cells of {cell_size}, sample the scene at the cell centre, glyph from a canvas font atlas.
Score composed in code: key clicks, a crackle as cells switch on, {score_idea}.
```

Ideas: a product turning on a stand drawn in characters, a city at night with lit windows as `@`, a logo in 3D
that resolves out of the text, a weather map whose clouds are made of glyphs.

## How it's built

1. **A real scene first.** Three aurora curtains are wide ribbon meshes moved by noise: the base line snakes up
   and down, the hem is brightest, rays run up them and patches drift along. Stars are instanced sprites and the
   ridge is a dark mesh with a lit rim. All of it is rendered to a texture, never shown directly.
2. **One pass makes the text.** The post shader divides the frame into cells, samples the scene at each cell's
   centre, turns its brightness into an index on the ramp, and reads that glyph from a font atlas, drawn once on
   a canvas in IBM Plex Mono.
3. **Colour without mud.** Each glyph takes the scene's hue at that cell, normalised to full strength, so a dim
   violet top stays violet instead of turning grey. A little of the picture bleeds behind the glyphs like
   phosphor, with scanlines and a soft vignette.
4. **Switch-on and flicker.** Every cell has a seeded time to switch on and shows random glyphs for a third of
   a second around it. The title's cells do the same with their own seeds.
5. **Shrink with one number.** The cell size is a uniform, and the grid zooms about the frame's centre. When the
   cells are tiny the picture shows through, so the aurora resolves to an almost smooth image and back.
6. **The title is a mask.** "Recipes" is drawn once in Fraunces on a canvas, softened so its edges make a ramp,
   and the same pass reads it as a second brightness.

## Gotchas worth knowing

- A canvas texture and the screen can disagree on which way is up: check the title mask in the first snapshot.
- Too much light turns every cell into `@`. Keep the scene darker than looks right and let the ramp do the work.
- Several additive curtains on top of each other become one flat wall of glyphs. Fewer curtains, patchy and
  bright at the hem, read as aurora.
