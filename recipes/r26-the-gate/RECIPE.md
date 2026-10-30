# R26 · The Gate

**Style:** 2D vector motion design. One SVG stage and GSAP, with no canvas, no WebGL and no 3D: shapes that morph into
other shapes, lines that draw themselves, clip-path mattes, kinetic type, impact frames, and a camera that is a single
group, flying through a flat world in navy, cream and gold.

**Made for:** OutreachIQ, a self-hosted outreach workspace.
**Length:** 32 s · 1920×1080 · 30 fps · score composed in code.
**Stack:** HyperFrames · SVG · GSAP · Python (table, score).
**Cost:** €0. Everything here is free and open source.

## The prompt

```
Make a 32-second 1920x1080 film in HyperFrames for OutreachIQ, a self-hosted outreach workspace whose line is
"The system drafts and checks. You decide what gets sent." 2D vector motion design only: one SVG stage and GSAP, no
canvas, no WebGL. Flat navy #08111C and #0D1B2A, cream #F7F4EF on cards and envelopes only, gold #C9A84C hairlines;
red and amber only on score chips and flags. Cormorant Garamond and JetBrains Mono. Shape morphs, lines drawing on by
their dash offset, clip-path mattes, two-frame impact frames, no drop shadows.
The flood: one envelope stamps in and multiplies into a three-arm vortex of envelopes; a gold kill line slices the
frame on an impact frame, the storm freezes, drains to navy and falls.
Find: the kill line becomes the first street of a map that draws itself; six gold pins drop with a squash and a ripple,
and four morph into shopfronts with awnings: CAFÉ, STUDIO, CLINIC, BAKERY.
Score: six sample lead cards pass a gold dial one at a time; the needle sweeps, a score chip lands, and each card files
into HOT, WARM, COLD or SKIP; the SKIP lane folds away.
Draft and check: the café card splits into three drafts that type themselves; a tone-audit scan line strikes an
overused phrase, a bad greeting and a hard sell, and each is rewritten a beat later.
The gate: a monumental art-deco gate draws itself in gold from the centre out; four locks click shut, DUPLICATE
CONTACT, DO-NOT-CONTACT, TONE, RECIPIENT; a dead stop; a cursor clicks Approve; the panels fold open onto gold rays and
one envelope steps through on the beat under a daily cap.
Title: a reply arrow comes back, everything collapses into the official IQ tile, flat, then the line and the URL.
Never redraw or recolour the mark. Score: compose it in code from the same table, 112 bpm, E minor to G major:
typewriter keys in the storm, a clockwork pulse, a stamp per card, a lock clunk per check, silence before the click,
bells on the title.
```

## Remix it

```
Make a {duration}-second {width}x{height} film in HyperFrames for {subject}, in 2D vector motion design only (one SVG
stage and GSAP), flat {palette}, with shape morphs, lines drawing on, clip-path mattes and impact frames. {the_problem}
fills the frame as a storm until a kill switch freezes it; a line draws {the_map} and pins drop and morph into
{the_places}; a dial scores {the_items} into lanes; {the_drafts} are struck and repaired by {the_check}; and {the_gate}
draws itself, {the_locks} click shut, and it opens only when a person clicks {the_button}. Then the flat lockup with
{line} and {url}. One baked table drives the morphs, the locks and a score composed in code.
```

Ideas: a clinic's booking system, where a flood of requests meets a calendar, triage lanes and a door that opens only
when the doctor confirms; a newsletter tool, with a storm of drafts, an editor's checks and a press that runs only on
Publish; a grant review, with a scoring dial and a seal applied by hand; a hiring pipeline, where an offer is sent only
on Approve.

## How it's built

1. **One SVG stage.** No canvas and no WebGL. The stage holds a camera group (one translate and scale), one group per
   scene inside it, and a screen-space group above it for the kill line and the flash. One GSAP tween drives the
   clock and calls `paint(t)`, a pure function of time, so any frame can be seeked in any order.
2. **Any shape into any shape.** Every closed outline is resampled to 120 points along its own length with a hidden
   path's `getPointAtLength`. The second outline's point order is rotated to the least total travel, then the two are
   interpolated. That is how a map pin becomes a shopfront without a cut.
3. **Lines drawn on.** Each line is drawn by its `stroke-dasharray` and `stroke-dashoffset`. The gate is 46
   separate paths, each given an order from the centre out, so the arch, the radials, the panels and the diamonds
   draw themselves as one wave.
4. **A vortex from one symbol.** The storm is 340 `<use>` copies of one envelope symbol. Each is born on a
   square-root schedule (faster and faster) and flung out along one of three spiral arms.
5. **Mattes.** The gold rays behind the gate are clipped to the arch's outline, so light appears only where the
   panels have folded open.
6. **Impact frames.** On the kill switch and on Approve, the whole stage is inverted for two frames with a CSS
   filter, and the camera shakes for a third of a second.
7. **A vertical cut.** The 9:16 version is the same take: the camera reframes each scene and the wide layouts (the
   map, the dial and lanes, the drafts, the Approve button, the throttle) are laid out again for portrait.

## Gotchas worth knowing

- A top-level `const top` collides with `window.top` in a classic script: the page throws and renders blank. Name
  it something else.
- Measure text with `getComputedTextLength` only after its content is set in the same frame, so a strike line is the
  width of what is on screen at that moment.
- Morphs look wrong when the two outlines start at different points. Rotate one outline's point order to the least
  total travel before interpolating.
- Gold on cream fails contrast for small type. Darken the gold for labels on cards and keep the bright gold for lines.
- Brand rules hold in motion: the mark is never redrawn or recoloured, it arrives as the official tile, flat, and the
  cream app colour stays on cards and envelopes, never the background.
