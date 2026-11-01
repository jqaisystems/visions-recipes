# R32 · Pinned

**Style:** paper cut-out stop motion. One Canvas 2D: every piece a path whose edge is torn by noise, filled with a
paper stock generated from noise and lit by a tabletop light whose shadows grow with height, posed twelve times a
second like stop motion on twos, under a stepped camera, with HTML only for the HUD and the end card.

**Made for:** Etsy to Pinterest, a pipeline that turns Etsy listings into Pinterest-ready image and video pins.
**Length:** 33.6 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.6-second 1920x1080 film in HyperFrames for Etsy to Pinterest, my pipeline that turns Etsy
listings into Pinterest-ready image and video pins ("Etsy media in, Pinterest queue out"), as paper cut-out stop
motion on a craft table. Everything in the picture is one Canvas 2D: each piece is a cut path with an edge torn by
noise, filled with a paper stock generated from noise, and a tabletop light gives it a shadow that grows with its
height. Shoot it on twos: snap time to 12 poses a second and re-cut every edge a little on each pose. A cutting mat
with a pencil, tape and a spool; a stepped camera; Archivo, Instrument Serif italic and JetBrains Mono, with each word
of the lines on its own strip of paper. The listing is my own, with its photos, charts, video and cover, and the pin
text and boards the system wrote.
Listing: the paper listing slides in with its photo, title, tags and gallery. "Etsy media in,"
Filter: the gallery fans out as prints; scissors snip out the size chart and the colour chart, which fly off.
"Not every image is a pin."
Pins: each photo's paper margin is trimmed along a dotted line to a 2:3 pin, the scrap is swept away, and a tag unfolds
with its title and alt text. "A unique pin for every image."
Boards: a spread opens, two boards pop up, and pushpins press each pin onto the board it matches. "Matched to its board."
Schedule: a week of paper strips drops in and the pins land in slots with gaps between them, a paper clock ticking.
"Scheduled, never bunched."
Video: the filmstrip folds into a 9:16 card playing the listing video, gets its cover and is filed in a folder marked
ready_manual. "Video pins stay manual, by design."
Title: "Pinterest queue out.", a black sheet sweeps the table, and the JQ AI SYSTEMS logo lands flat, never redrawn or
recoloured, with the system's name, its line and the URL. Score: compose it in code from the same table, 100 bpm,
kalimba, upright bass and brushes, with the paper, the scissors and the pins on the beat.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject} as paper cut-out stop motion on
{the_table}, drawn on one Canvas 2D with torn edges, paper stocks made from noise, shadows from a tabletop light and
poses on twos. {the_input} slides in; its parts fan out and scissors snip out {what_is_left_out}; each piece is
trimmed into {the_output} and a tag unfolds with {its_label}; {the_sorting}; {the_schedule}; {the_special_case} takes
its own path; and a black sheet sweeps the table for the logo, placed flat with {line} and {url}. One baked table
drives the beats, the pieces, the type and a score composed in code.
```

Ideas: a recipe app, with a cookbook page cut into ingredient cards pinned to a week planner; a newsletter tool, with an
article cut into quotes pasted onto postcards and dropped into send slots; a podcast studio, with an episode as a paper
tape snipped into captioned clips; a photographer's delivery, with a contact sheet whose rejects are snipped out and
whose keepers are trimmed to print sizes.

## How it's built

1. **One canvas, one clock.** A GSAP tween drives the clock and calls `paint(t)`, which snaps `t` to twelve poses a
   second and draws the whole frame for that pose: the mat, the props, every piece of paper, the type and the light.
   Any frame can be seeked in any order.
2. **Cut paper.** `piece(P)` resamples a shape every few pixels and pushes each point along its normal by value
   noise, so every edge is torn; the outline is filled with a paper stock, a 512 px tile of fibres, mottling and
   speckle generated once from a seeded random.
3. **A tabletop light.** Each piece has a height. Its shadow's blur and offset grow with it, and the camera slides the
   higher pieces a little further than the table, so a piece lifting off the mat reads as lifting.
4. **Boil.** On every new pose each piece is nudged by a hash of the pose and its edge is re-cut a little, the look of
   replaced paper parts. It is keyed by the pose, never by time, so the same frame always boils the same way.
5. **Prints and pins.** A print is a 2:3 photo drawn with a cover crop inside a square sheet, clipped to the sheet's
   torn path. The scissors run down a dotted line in the margin on every pose and the scrap is swept away.
6. **Pop-up boards.** As the spread opens, each board stands up from the gutter: its visible height is the sine of its
   fold angle, timed to rise after its page has opened.
7. **A flipbook.** The 9:16 card plays the listing video from 12 fps frames, one frame per pose, so the video moves
   on twos with everything else.
8. **The logo, flat.** A black sheet sweeps the table and the official file lands on it as an image, untouched, with
   the name, the line and the URL typed as text.

## Gotchas worth knowing

- Key every per-pose cache by the pose, never by time: a shape cached at one pose and reused at another boils on the
  wrong frame and breaks seeking.
- Pop a pop-up after its page has opened, not on the same clock as the cover, or the board stands up through the
  closed page.
- Draw photos into the paper with a cover crop and a clip on the piece's path, so the torn edge cuts the photo too,
  not just the card behind it.
- Wait for every image's `decode()` and the fonts before the first paint: the renderer seeks frames out of order.
- Re-lay the portrait cut rather than cropping it: a row of four becomes a 2x2 grid, the fan becomes two rows, and the
  type wraps to the frame.
