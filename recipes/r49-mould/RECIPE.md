# R49 · Mould

**Style:** stop-motion clay made entirely in code. One hand-written WebGL2 raymarcher, posed at 12 poses a second over a 30 fps render, under one hard spotlight with a real
cone. The pictures are height maps on one plaque shape, so a wall of 45 costs the same as one, and colour runs through the lump's volume, so it twists as the clay is kneaded. Flat labels and the mark sit on a 2D layer above.
**Made for:** AI Brand Visuals, a service: on-brand images, motion and music made with AI by a brand designer, starting from a style system the client keeps.
**Length:** 32.88 s · 1920×1080 · 30 fps, with a 9:16 cut re-laid for portrait.
**Stack:** HyperFrames · WebGL2 · Canvas 2D · GSAP · Python (table, score) · FFmpeg.
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32.88-second 1920x1080 film in HyperFrames for AI Brand Visuals, a service where a brand designer makes on-brand images, motion and music with AI, starting from a
visual style system the client keeps. Make it dynamic motion design, a showreel piece. It's stop-motion clay made entirely in code: one hand-written WebGL2 raymarcher with signed distance fields, thumbprints
pressed into the surface, posed at 12 poses a second over a 30 fps render with tiny per-pose jitter and flicker. A black box studio under one hard, warm spotlight with a real cone and a hard edge, and a little sheen on the clay. 104 bpm, 57 beats.
Ember, bone and deep teal once the system is on, clashing colours before it, and hot pink only for the one wrong picture. Archivo at 900 extruded as clay, and near-black #0B0C12 for the end card. Pictures are height maps of layered flat clay on one
plaque shape, so a wall of 45 costs the same as one. A "AI BRAND VISUALS · DEMO PICTURES" label stays on screen. One Python table holds the beat grid and every event, and the film and score both read it. The score is composed in code in D minor: upright bass, brushes and vibraphone,
with the press as the kick and a wet slap for each picture.
The mismatch: six clay pictures in six clashing colour schemes and six shapes land one by one, each with a wrong note. "ONE BRAND?"
The lump: they're squashed together into one marbled ball, with colour that runs through the volume, and it's kneaded on the beat as the colours twist. "NOT A DEFAULT AI IMAGE."
The press: a screw comes down, and four plates slide onto it from alternate sides and lock: REFERENCES, RECIPES, RULES, DO-NOT. The marbling settles into the system's palette. "A STYLE SYSTEM FOR YOUR BRAND."
The first set: the press comes down once, slowly, and flattens the lump. It lifts, and six pictures slide out. A clay arm comes in from the side and a thumb marks each one. "YOU APPROVE THE FIRST SET."
The run: the six fly up onto a wall. The press slams on every beat and more pictures fly out each time, while the camera pulls back. It lifts away to show 45 different pictures with one palette. "ONE LOOK."
The do-not: one picture is hot pink. The band stops dead and the light narrows to it. One rising note, then a heavy stamp with DO-NOT on its back slams down on it, holds, and lifts past the camera. The splat slides down, a picture that fits flies in, and the band comes back. "THAT'S WHAT THE DO-NOT LIST IS FOR."
It moves: every picture but three sinks into the wall. A boat rocks, a bird flaps and a record spins. "IMAGES. MOTION. MUSIC."
Yours: the press lands on the table without its screw and slides towards the camera until its plates fill the frame. "THE SYSTEM IS YOURS TO KEEP."
Close: the logo lands flat on dark, never redrawn or recoloured, with "AI Brand Visuals", the URL and "A SERVICE · THIS FILM IS CODE".
Take facts only from the service page. "Yours to keep" is about the style system only, never ownership or copyright of images. Claim no prices and no results, and use no third-party names or logos.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {product}, whose story is {the_story}, as stop-motion clay made entirely in code. Use one hand-written
WebGL2 raymarcher, with thumbprints pressed into the surface, posed at 12 poses a second, under one hard spotlight in a black studio, in {your_palette}. Squash {the_mess_before} into one marbled lump, build {the_tool_you_sell} from its {labelled_parts},
and press out a wall of {what_it_makes}, drawn as height maps on one shape so the wall stays cheap. Put {the_one_wrong_thing} in the wall, stop the music dead, and flatten it with a heavy stamp. Hand over {what_they_keep}. End with {your_mark},
placed flat, with {line} and {url}, at {bpm} bpm with a late-night score composed in code.
```

Ideas:

- A brand guide: a stack of plates for logo, colour, type and tone, pressing out a wall of posters that all belong together.
- A template pack for a social team: one press, and a wall of posts in many formats and one look.
- A code style guide: a press built from rules, a wall of tidy files, and one messy file that gets stamped flat.
- A recipe book: a press of ingredients and methods, and a wall of plates from one kitchen, with one burnt dish.

## How it's built

1. **Six wrong pictures.** Each lands with its own colours, its own shape and its own wrong note. There's no band yet, because there's nothing holding them together.
2. **Colour that twists.** The pictures melt into one lump. Its colour runs through the volume, so kneading it really does twist the bands, and it moves to the system's palette as the plates arrive.
3. **Four plates on a screw.** They slide in from alternate sides and lock with a hit each. Naming the four parts of the system this way means the film never has to explain them.
4. **One slow press.** It takes a long time to come down, then flattens the lump in one frame. Six pictures slide out, and an arm comes in from the side to mark each one, because the client approves the first set.
5. **The run.** The press is the kick. Each slam sends more pictures to the wall than the last, starting from the middle, while the camera pulls back.
6. **One look.** The press lifts away and the whole wall shows for the first time: 45 different pictures from one palette and one set of rules.
7. **The do-not.** One picture is hot pink. Everything stops. The stamp has no handle, so you see its back, with DO-NOT on it. It slams down, holds, then lifts past the camera, and the flat picture slides down the wall.
8. **Three that move.** All the others sink into the wall, so the boat, the bird and the record have the frame to themselves. Then the press slides to the camera without its screw.

## Gotchas worth knowing

- A word's distance field stops at its box. Keep the distance growing outside it, or its shadow comes out as a soft rectangle and not as letters.
- An empty cell has to give a safe step, but that step reads as an occluder. Give shadows and ambient light their own version, or a faint grid shows up on the wall behind.
- A word far from the wall casts a second, readable line of type. Move it close to the wall, and the shadow turns into relief.
- A long arm that passes the camera gets enormous. Bring it in across the frame.
- A hard spotlight also leaves objects dark as they slide out of it. Move the light with whatever is heading for the camera.
