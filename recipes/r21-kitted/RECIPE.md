# R21 · Kitted

**Style:** an AI stack setup as a precision tool kit in a dark workshop, filmed in macro like a product launch. A pile
of loose tools is audited, a laser cuts a two-tone foam insert to the outline of each tool that earns a place, every
tool clicks in with its name engraved, and the same kit opens at every bench.
**Made for:** AI Stack Setup & Enablement (ai.joaoqueiros.com/services/ai-stack-setup).
**Length:** 32 s · 1920×1080 · 30 fps · one take · score composed in code.
**Stack:** HyperFrames · Three.js (WebGPU renderer, WebGL2 backend, TSL bloom) · GSAP · Python (table, word, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for my AI Stack Setup & Enablement service: a precision tool kit in a
dark workshop, filmed in macro like a product launch, Three.js with bloom, a brushed steel bench under one cool work
light, steel tools drawn as symbols (a nib, a spanner, a lens, a gear, a film gate, a report sheet, a page frame), a
case of charcoal foam over a teal under-layer, teal #00BFB4 for the laser, the HUD and everything once it is set up.
Scattered: a work light flickers on over a pile of loose tools with edges in clashing colours, duplicates, a ring of
mismatched keys, sticky notes ("pasted prompt", "v3 final") and tangled cables. The HUD: "everyone's using AI
differently".
The audit: a teal light sheet crosses the bench and tags every piece as it passes: each tool with the work it does
("Writing", "Code", "Images", "Automations", "Video", "Reports", "Pages") and KEEP, the rest DUPLICATE, PERSONAL
LOGINS or TANGLED. The clutter slides off the edge into a bin; the seven kept tools rise and hover upright in a row.
Cut to fit: a case slides in and its lid opens on blank foam. A laser head comes down and cuts the outline of each
tool, the first in macro, the rest at speed, a hot teal trail cooling behind the beam, sparks and smoke; each plug
pops out to show the teal layer underneath. The last outline is an empty slot.
Installed and configured: on the beat, each tool drops into its cutout, its edge turns teal and its engraved name
lights. Twenty prompt cards ("Weekly report", "Client reply", "Meeting notes") riffle into a box marked PROMPTS.
Onboarding: four more benches light up, the same kit slides in and opens at each one in sync, and over every bench a
job runs in light: a weekly report prints, a product shot develops, a landing page builds, a social cut plays, an
invoice check ticks through its steps, each ending on "DONE".
Handed over: a playbook lands in the empty slot and the laser engraves the word "equipped" into the foam of the lid.
End on "AI Stack Setup & Enablement", "Your AI stack, installed and running properly." and the URL. Station titles
wipe on bottom left; a HUD names each stage.
Technique: one seeded table baked in Python holds the film's clock and every tool: its outline, the work it does,
where it lies in the pile, where it hovers and where it fits in the case, the clutter and when it is binned, the
prompt cards and the five benches' jobs. The cutout, the plug and the laser's path all come from the same outline
pushed out by a small margin. No tool, vendor or model names and no logos; no promised hours, savings or ROI.
Score: compose it in code from the same table: a work light clunk, a fluorescent hum and a low E drone, a scanner tone
across the audit with a blip for every tool kept and a buzz for every piece binned, a clang as each lands in the bin,
a 100 bpm groove under the laser (Em, C, G, D), a hiss that follows each cut with a crackle and a pop for every plug, a
click and one note of a rising arpeggio as each tool lands, card riffles, a clunk for each bench light, a chime as
each job starts, and one wide E major chord under the word.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}: {what_gets_set_up} as a precision tool kit
in a dark workshop, Three.js with bloom, one work light, steel tools drawn as symbols, a two-tone foam case, {accent}
accents. A pile of {the_mess} is audited: each of {the_tools} is tagged with the work it does and kept, {the_clutter}
slides off into a bin. A laser cuts the foam to the outline of each kept tool and each clicks into its cutout with
its name engraved. {the_library} fills a box beside the case. The same kit opens at {how_many} benches, each running
{the_jobs}. {the_handover} lands in the last slot and the laser engraves the word "{word}" into the lid.
End on {title}, {line} and {url}. One baked table drives the picture and a score composed in code.
```

Ideas: a new starter's first-day kit, desk by desk; a photographer's travel kit, packed for one shoot; a kitchen's mise
en place, every knife and spice in its place; a band's touring rig, cased for the road.

## How it's built

1. **One table.** `bake/table.py` holds the film's clock and every tool: its outline, the work it does, its colour in
   the pile, where it hovers and where it fits in the case, the clutter and when each piece is binned, the prompt
   cards and the five benches' jobs. It refuses a layout that leaves less than a strip of foam between two cutouts.
   The film reads `assets/table.js` and the score reads `bake/table.json`, so every click lands on what you see.
2. **One outline, three uses.** Each tool's outline is pushed out by a small margin with mitred corners. That one path
   is the hole in the foam (an `ExtrudeGeometry` with every cutout as a hole), the plug that fills it until it is cut,
   and the path the laser follows, so they always match.
3. **The cut.** Each outline is a `TubeGeometry` along a path of straight segments. A dim seam is revealed with a draw
   range up to the beam, and a bright stretch draws just the last part of it, so the cut runs hot at the beam and cools
   behind it. Sparks are one `InstancedMesh`: each spark is born on the path at its own time and flies out under
   gravity.
4. **The tools.** Each is the same outline extruded with a bevel, with two materials: brushed steel on the faces and a
   coloured edge on the sides. A tool's name is drawn on a canvas fitted to its outline's box and set as both the map
   and the emissive map, so it reads engraved and then lights. Landing turns the edge teal.
5. **The moves.** A tool goes from the pile to its hover on a quadratic Bézier while its rotation slerps from its pile
   angle to upright; it then flies over its cutout, turns flat and drops in with a damped bounce. The case slides in on
   an ease-out and its lid opens on a back ease.
6. **The jobs.** Each job over a bench is a canvas redrawn every frame while it runs: a report printing, a picture
   developing out of grain, a page assembling block by block, a clip playing, an automation ticking through its steps.
7. **The word.** Points sampled from the word's outlines are lit in order along their length, each glowing hot as the
   beam reaches it and settling to teal, so the laser seems to engrave the word into the lid.

## Gotchas worth knowing

- A tool seated below the foam's surface disappears from low angles behind the cutout's walls. Seat it just proud of
  the foam, as in a real shadow board.
- Polished steel in a dark room reflects the dark, so the tools read as empty slots. Lower the metalness and lighten
  the base colour until the steel reads from every angle.
- Extruded faces get their UVs in the shape's own units: fit a texture to the outline's box with `repeat` and `offset`,
  or the engraving lands mirrored or off the tool.
- A Studio preview session can add `data-hf-id` attributes to your `index.html`; check your diff before you commit.
