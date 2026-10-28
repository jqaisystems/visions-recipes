# R25 · First Line

**Style:** cel-shaded anime, told as the anime production pipeline. 3D rendered like a hand-drawn anime cut, flat
colour in three hard bands of light, ink outlines, screentone, the drawings changing 12 times a second while the
camera moves on every frame, and the same world shown in three passes:
- a boiling blue-pencil pass;
- a clean ink pass;
- a cel colour pass, wiped in from the others.
Around it: a flip book of roughs, ribbons that draw themselves along the mark's paths, a painted Porto from blue hour
to dawn, and manga panels.

**Made for:** joaoqueiros.com, the brand identity studio of João Queirós.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL toon materials, outline pass, shadow maps) ·
Canvas 2D · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my brand identity studio, whose mark is a JQ monogram drawn as
four parallel strokes in a teal to cyan gradient (#00A79D to #0095DA) on black #0D1114. Cel-shaded anime told as an
anime cut is made: the same Three.js world rendered in three passes, a boiling blue-pencil pass, a clean ink pass and
a cel colour pass, wiped from one to the next. Three-band toon ramp, ink outlines, screentone, the 3D on twos and the
camera on ones, smear and impact frames. A desk by a window over the Douro in Porto, the river, the iron arch of the
bridge and the riverside roofs as painted layers. Montserrat and IBM Plex Mono.
The brief: night, a blank sheet under a lamp; the lamp clicks on, a pencil draws one line and lands on an impact frame.
Roughs: a wipe turns the world to blue pencil that boils on twos; rough marks land on the sheet in triplets, and a
flip book of roughs riffles under the camera, all abstract tries, never a client's mark.
Ink and paint: the four strokes of the mark draw themselves as 3D ribbons along the official paths, stand up off the
paper with a smear, a wipe turns pencil to ink and a second wipe brings colour, and the mark locks front-on.
The system: manga panels slam in on the beat, each a cel-shaded application of a generic identity in the same
colours, a business card, a box, a shop sign, a bag, a bottle label, a phone, stamped LOGO, COLOUR, TYPE, PACKAGING,
LABELS, SOCIAL.
Worldwide: the camera flies out of the window over Porto at dawn, the four strokes fly out as trails into the sun,
and the figures land as lettering: 1,200+ BRANDS, 40+ COUNTRIES, SINCE 2014.
Title: the official logo, flat, "Brand identity design for businesses ready to grow." and the URL. Never stretch,
redraw, crop or recolour the logo; the camera moves around the mark, the mark does not spin.
Score: compose it in code from the same table, 96 bpm, D minor to F major: pencil scratches, a page flutter on every
flip, a plucked twelve-string, piano and strings as the colour arrives, a hit on every panel, a rising chord as the
trails fly out, bells on the title.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: cel-shaded anime told as an anime
cut is made, the same Three.js world rendered as a boiling blue-pencil pass, a clean ink pass and a cel colour pass,
wiped from one to the next, with a toon ramp, ink outlines, the 3D on twos and the camera on ones, in {palette}. Set
it in {a_room_and_a_view}. {the_first_mark} is drawn on a blank sheet; {the_tries} pile up in pencil and a flip book
riffles; {the_parts_of_the_mark} draw themselves as ribbons, stand up and are wiped to ink and colour; {the_work}
slams in as manga panels; and the camera flies out over {the_place} as {the_figures} land, then the flat lockup with
{line} and {url}. One baked table drives the passes, the wipes, the panels and a score composed in code.
```

Ideas: an architect's studio, where one line becomes a plan, a model and a building at dawn; a type foundry, where one
stroke becomes a letter, a family and a poster wall; a tattoo studio, one line in pencil, inked, coloured, then out to
the street; a furniture maker, one sketch, a set of drawings, and the chair in a sunlit room.

## How it's built

1. **One world, three passes.** The scene is one Three.js world with two sets of materials: cel colour, and line art
   (toon materials whose output is overridden to flat white, so the outline pass still inks them). A frame can render
   both. The line-art render becomes:
   - **ink:** multiplied onto paper with grain;
   - **pencil:** screened blue and multiplied twice, each copy nudged by an offset that changes on twos, so every line
     boils like a rough.
2. **Wipes between passes.** On a wipe both passes are composited, and a slanted clip with a brush edge shows one on
   each side as it crosses the frame.
3. **Strokes from the mark.** The four strokes are centrelines traced from the official symbol (lines and arcs), each
   a ribbon of the stroke's width with mitred offsets and capped ends. The ribbon is rebuilt at the length drawn so
   far, and each carries its own teal to cyan gradient as vertex colours across its own width, as in the logo file.
4. **The sheet and the flip book.** The first page is a live canvas: the pencil's line and the roughs are drawn into
   it as they happen. The flip book pages curl over a hinge, bent vertex by vertex, with a border drawn on their backs.
5. **A painted Porto.** Hills, the far bank, the iron arch bridge, the near roofs and the river are painted canvases
   at real depths, repainted in night, dawn and line-art palettes, so the window has parallax as the camera moves.
6. **Manga panels.** Each application is lit in its own corner of the set, rendered for its panel, cropped into a
   slanted frame, shown in pencil for a moment and wiped to colour, with its word stamped in and fitted to the panel.
7. **On twos, with impacts.** The 3D reads `floor(t * 12) / 12`, the camera moves on every frame. The lift has two
   smear frames, every page flip one, and impact frames print the stage in ink and paper.
8. **Trails into the sun.** In the room the strokes leave as 3D trails; outside, four parallel ribbons are drawn in
   screen space from the bottom left into the sun's projected position, so they arc cleanly over the bridge.

## Gotchas worth knowing

- A toon outline pass only outlines toon materials. For a line pass, keep the materials toon and override their
  output with flat white.
- A render pass runs once per frame by default. Rendering the scene twice in one frame needs the node frame advanced
  before the second render, or it returns the first image again.
- Planes get no outline from back faces, so a page's back needs its border drawn into its texture, or a white page
  vanishes against white paper.
- Brand rules hold in motion: the strokes follow the official paths and gradients, the camera moves around the mark,
  and the logo at the end is the official file, flat.
