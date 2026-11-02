# R35 · Pop-Up

**Style:** paper pop-up book, as paper cut-out stop motion. One Canvas 2D: every piece a path whose edge is torn by
noise, filled with a paper stock generated from noise, posed twelve times a second like stop motion on twos, and set
in an orthographic 3D view where every page, card and flap is one flat plane drawn through a single affine transform,
with HTML only for the HUD and the end card.

**Made for:** the AI Brief Generator, a tool that turns a client intake form into a structured creative brief.
**Length:** 33.4 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · Canvas 2D · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 33.4-second 1920x1080 film in HyperFrames for the AI Brief Generator, my tool that turns a client
intake form into a structured creative brief, as paper cut-out stop motion: a pop-up book on a linen table in morning
light. Reuse the paper engine from Footlights: one Canvas 2D, each piece a cut path with an edge torn by noise, filled
with a paper stock generated from noise, poses on twos with the edges re-cut on each pose. Put it in 3D: an
orthographic view of the table from the front and above, so every flat piece on any plane (a page at any angle, a card
standing on its hinge, a flap) is drawn through one affine setTransform. Leaves turn about the spine, and a spread's
pop-ups rise as its leaf lands and fold flat as the next one lifts. Linen grey-green, ivory and cream pages,
terracotta, teal, ochre and ink, with a red pencil. Archivo, Instrument Serif italic and JetBrains Mono, each word of
the lines on its own strip of paper. The client and everything in the brief are an invented sample, labelled as one.
Intake: an intake form of ten questions slides in, two of its answers vague ("everyone who needs it", "professional
but friendly"), then a card of call notes tagged optional; both slide under a closed book, "Creative brief · sample".
"Intake form in,"
Synthesis: the cover opens on the project context; each vague answer is pulled through a slot and comes out the other
side as three concrete chips; the brief's seven section tabs fan out of the fore-edge. "Vague words in, concrete out."
Audience: a page turns and three invented personas stand up on a box fold. "Who it's for,"
Tone and competition: a pull tab slides a pointer along a tone scale and three tone words pop up; a skyline of
Competitor A, B and C rises, with a card for the gap between them. "how it should sound,"
Visual and scope: a fan of swatches and a type specimen spring up; the deliverables stand up line by line. "and what
to make."
Questions: a ? flap swings open on two question tags for a person to follow up. "Questions flagged."
Edit: a red pencil strikes one weak word in the summary, writes a better one above it and ticks the lines; a stamp
comes down: reviewed. "Then a person edits it."
Export and title: the book closes, folds flat into brief.pdf and slides into an envelope; a black sheet slides over
the table and the JQ AI SYSTEMS logo lands flat, never redrawn or recoloured, with the system's name, "Intake form in,
full brief out." and the URL. Score: compose it in code from the same table, 88 bpm, piano, pizzicato and celesta over
a sub, a soft kick and a shaker, with every page turn, pop-up, tab, pencil stroke and the stamp on the beat.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject} as paper cut-out stop motion,
a pop-up book on {the_table}: an orthographic view where every page, card and flap is one affine transform, torn edges,
paper stocks made from noise and poses on twos. {the_input} slides in under a closed book titled {the_title}; the cover
opens and {the_raw_part} is pulled through a slot and comes out as {the_refined_part}; {the_sections} fan out as tabs;
each spread pops up a section as its page lands: {spread_1}, {spread_2}, {spread_3} and {spread_4}; {the_human_step};
and the book closes into {the_output} for the logo, placed flat with {line} and {url}. One baked table drives the
beats, the pieces, the type and a score composed in code.
```

Ideas: a recipe app, with a craving pulled through the slot as three dishes and the book closing into a printed menu;
a trip planner, with "somewhere warm" coming out as three towns and the book closing into a boarding pass; a lesson
planner, with a broad topic coming out as three lessons and a teacher's pencil marking it; an onboarding guide, with
the team, the tools and the first week popping up before it closes into a welcome pack.

## How it's built

1. **One canvas, one clock.** A GSAP tween drives the clock and calls `paint(t)`, which snaps `t` to twelve poses a
   second and draws the whole frame for that pose, back to front. Any frame can be seeked in any order.
2. **Paper in 3D, drawn flat.** The table is seen from the front and above in an orthographic view (`PSI`, `PHI`), so
   any plane in the scene maps to the screen by one affine transform. `plane(O, U, V)` sets it, and a flat piece on a
   page at any angle, a card on its hinge or a flap is drawn with `piece()` as usual, keeping its torn edge, its stock
   and its print.
3. **Cut paper.** `piece(P)` resamples a shape every few pixels and pushes each point along its normal by value
   noise, so every edge is torn; the outline is filled with one of 19 paper stocks generated once from a seeded random.
4. **Page turns.** Each leaf turns about the spine on an eased angle (`leafA`); its front is drawn until it passes
   upright, then its back, and its shadow grows with its height. The stacks on each side rise and fall as leaves cross.
5. **Pop-ups that follow the page.** `rise(k, t)` stands a spread's cards up as its leaf lands and folds them as the
   next leaf lifts, so every card's angle comes from the pages, and the draw order flips once the turning page passes
   upright.
6. **Through the slot.** Each vague answer is a strip clipped at the slot so it vanishes into the page, and three chips
   slide out the other side and stand up one after another.
7. **A door flap and a pencil.** The ? flap is hinged on its side so it never covers the heading; the pencil's strike,
   new words and ticks are drawn up to a moving length, with the pencil's tip on the point being drawn.
8. **Export.** The book closes as one, its pages squash flat while the cover turns into a printed sheet, and the
   sheet slides into an envelope whose flap folds down over it.
9. **The logo, flat.** A black sheet slides over the table and the official file lands on it as an image, untouched,
   with the name, the line and the URL typed as text.

## Gotchas worth knowing

- Keep the projection orthographic: every plane stays one affine transform, so torn edges, stocks and print never
  need a perspective warp.
- Tie each spread's pop-ups to the page angles, not to the clock, so they always fold flat before the next page could
  pass through them.
- Flip the draw order when the turning page passes upright: before that it covers the spread beneath it, after that
  the new spread's cards stand in front of it.
- Hinge a lift-the-flap on its side rather than its top: a flap lifted upward in this view covers the heading and the
  type above it.
- Key every per-pose cache by the pose, never by time, so the same frame always boils the same way.
- Re-lay the portrait cut rather than cropping it: bind the book at the top so the pages turn upward, and give every
  pop-up its place on its own page.
