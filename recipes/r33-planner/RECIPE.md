# R33 · Planner

**Style:** paper planner mechanics, as paper cut-out stop motion. One Canvas 2D: every piece a path whose edge is torn
by noise, filled with a paper stock generated from noise and lit by a tabletop light whose shadows grow with height,
posed twelve times a second like stop motion on twos, worked like paper toys: pull tabs, a volvelle, an accordion,
lift-the-flaps, rubber stamps and a tractor-feed printout, with HTML only for the HUD and the end card.

**Made for:** the Social Media Content Calendar, a tool that turns one brand brief into a month of posts.
**Length:** 33.3 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.3-second 1920x1080 film in HyperFrames for the Social Media Content Calendar, my tool that turns one
brand brief into a month of posts, as paper cut-out stop motion on a desk. Reuse the paper engine from Pinned: one
Canvas 2D, each piece a cut path with an edge torn by noise, filled with a paper stock generated from noise, a shadow
that grows with its height, poses on twos with the edges re-cut on each pose. A birch desk with a felt blotter, leather
corners, a mug of pencils, a stamp pad and a stapler; navy, mustard, coral and cream; a slow crane camera that pushes
in only on the variety check and the export. Archivo, Instrument Serif italic and JetBrains Mono, each word of the
lines on its own strip of paper. The brief and the month are a sample for JQ VISIONS launching the recipe library,
labelled as a sample.
Brief: a form slides onto the blotter and six tabs pull out of its slots: voice, audience, goal, themes, highlight,
frequency per platform. "One brief in,"
Themes: a paper wheel on a brass pin clicks four times, and each click unrolls a banner with that week's headline
and the reason for it. "Four weeks, each with a reason."
Thirty days: the banners shrink to label the weeks, an accordion of card unfolds row by row into the month, and
thirty navy flaps lift in a diagonal wave over post cards: platform, format, hook, hashtag, call to action and a
pencil sketch of the visual. Instagram, LinkedIn and Pinterest as type only. "Every platform, in its own voice."
Variety check: the camera pushes in and rubber stamps hit three drafts: REPEAT HOOK, SAME CTA and SAME FORMAT, with a
pencil ring on the post each one repeats. Each draft crumples into a ball, rolls off, and a new card slides in.
"No repeats."
Export: the month folds back up into a printer and a tractor-feed strip with sprocket holes rises out of it a line at
a time, header first. "One row per post."
Review: a pencil ticks down the margin and the strip tears at the perforation.
Title: the strip folds into a paper plane and flies off, "A month of posts out.", a black sheet sweeps the desk, and
the JQ AI SYSTEMS logo lands flat, never redrawn or recoloured, with the system's name, "One brief in, a month of
posts out" and the URL. Score: compose it in code from the same table, 108 bpm, marimba, felt piano, upright bass
and shaker, with the tabs, the wheel, the flaps, the stamps, the printer and the pencil on the beat.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject} as paper cut-out stop motion on
{the_desk}, drawn on one Canvas 2D with torn edges, paper stocks made from noise, shadows from a tabletop light and
poses on twos. {the_input} slides in and its fields pull out as tabs; a paper wheel clicks {n} times and a banner
unrolls for each {group}; an accordion unfolds into {the_grid} and flaps lift in a wave over {the_items}; rubber
stamps throw out {what_the_check_catches}; the grid folds into a printer and {the_output} feeds out a line at a
time; a pencil ticks it off; and a black sheet sweeps the desk for the logo, placed flat with {line} and {url}. One
baked table drives the beats, the items, the type and a score composed in code.
```

Ideas: a meal planner, with thirty dinners under flaps and a stamp for the same dish twice; a course builder, with a
banner per module and the timetable feeding out of the printer; a newsletter editor, with issues under flaps and a
stamp for a repeated headline; a training plan, with sessions under flaps and a stamp for two hard days in a row.

## How it's built

1. **One canvas, one clock.** A GSAP tween drives the clock and calls `paint(t)`, which snaps `t` to twelve poses a
   second and draws the whole frame for that pose: the desk, the props, every piece of paper, the type and the light.
   Any frame can be seeked in any order.
2. **Cut paper.** `piece(P)` resamples a shape every few pixels and pushes each point along its normal by value
   noise, so every edge is torn; the outline is filled with a paper stock, a 512 px tile of fibres, mottling and
   speckle generated once from a seeded random. Felt is all short fibres, birch has a grain running one way.
3. **Pull tabs.** Each tab is a strip whose right end slides out from under the form's edge through a drawn slot, so
   it reads as pulled from inside the paper. Its width is measured from its value.
4. **A volvelle.** The wheel turns a quarter at each click with a little overshoot; the click starts a banner
   unrolling, with a paper roll travelling along its moving edge.
5. **An accordion and its flaps.** The first row arrives folded and each row unfolds out of the one above. Each flap
   is hinged at its card's top edge: its height is the cosine of its lift angle, so it foreshortens to a standing
   strip, and the wave is timed by row plus column.
6. **Stamped out.** A stamp comes down on a keyed path, a pencil ring closes on the post the draft repeats, the draft
   crumples into a ball and rolls off, and the new card slides in under its flap.
7. **A printout.** The strip advances quickly for each line, then holds while it prints. It is clipped to the area
   above the printer's lip, so it rises out of the machine header first; the pencil ticks each row as its tip passes.
8. **The logo, flat.** A black sheet sweeps the desk and the official file lands on it as an image, untouched, with
   the name, the line and the URL typed as text.

## Gotchas worth knowing

- Clip a printout to the area above the printer's lip, or the part still inside the machine shows below it.
- Put the printer under the paper's leading edge: if the strip feeds downward from the top, the header ends up at the
  bottom and the rows read upside down.
- Make the sample data pass the same rules as the story: if the film says no repeats, check in the bake that no hook
  or call to action repeats.
- Key every per-pose cache by the pose, never by time, so the same frame always boils the same way.
- Re-lay the portrait cut rather than cropping it: the month stands on end, a column per week, and the accordion
  opens sideways.
